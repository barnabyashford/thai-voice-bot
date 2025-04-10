from dotenv import load_dotenv
load_dotenv()

import os
import re
import shutil
import sys
import time

from gcp_asr_api import ResumableMicrophoneStream, get_current_time

from queued_tts import queuedTTS

from google.cloud import speech
from google import genai
from google.genai import types

# Audio recording parameters
STREAMING_LIMIT = 240000  # 4 minutes
SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
BLUE = "\033[0;36m"

def setup_gemini_api(
        system_instruction:str="You are a helpful assistant, help the user with any task. Be sure to keep everything concise. Answer in the user's language.",
        max_output_tokens:int=128,
        temperature:float=0.0):
    """Set up the Gemini API with the API key.
    
    Returns:
        Optional[genai.GenerativeModel]: The Gemini model or None if setup fails.
    """
    api_key = os.environ.get("GOOGLE_API_KEY", None)
    
    if not api_key:
        sys.stdout.write(YELLOW)
        sys.stdout.write(f"GOOGLE_API_KEY environment variable not set.\n")
        api_key = input("Please enter your Gemini API key: ").strip()
        if not api_key:
            sys.stdout.write(RED)
            sys.stdout.write(f"No API key provided. Voice response functionality will be disabled.\n")
            return None
        
    # genai.configure(api_key=api_key)
    
    client = genai.Client(api_key=api_key)

    try:
        # Initialize the Gemini model
        model = client.chats.create(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
            max_output_tokens=max_output_tokens,
            system_instruction=system_instruction,
            temperature=temperature
        ))
        return model
    except Exception as e:
        sys.stdout.write(RED)
        sys.stdout.write(f"Error setting up Gemini API: {e}\n")
        return None


def get_ai_response(model, transcript: str) -> str:
    """Get a response from the AI model based on the user's transcript.
    
    Args:
        model: The Gemini model.
        transcript: The user's speech transcript.
        
    Returns:
        str: The AI's response.
    """
    if not model:
        return "AI response functionality is disabled. Please set up your Gemini API key."
    
    try:
        # Generate a response from the AI model
        # response = model.send_message(transcript)
        response = model.send_message_stream(transcript)
        return response
    except Exception as e:
        return f"Error generating response: {e}"

def transcribe_loop(responses: object, stream: object) -> None:
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.

    Arg:
        responses: The responses returned from the API.
        stream: The audio stream to be processed.
    """
    for response in responses:
        if get_current_time() - stream.start_time > STREAMING_LIMIT:
            stream.start_time = get_current_time()
            break

        if not response.results:
            continue

        result = response.results[0]

        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript

        result_seconds = 0
        result_micros = 0

        if result.result_end_time.seconds:
            result_seconds = result.result_end_time.seconds

        if result.result_end_time.microseconds:
            result_micros = result.result_end_time.microseconds

        stream.result_end_time = int((result_seconds * 1000) + (result_micros / 1000))

        corrected_time = (
            stream.result_end_time
            - stream.bridging_offset
            + (STREAMING_LIMIT * stream.restart_counter)
        )
        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.

        if result.is_final:
            sys.stdout.write(GREEN)
            sys.stdout.write("\033[K")
            # sys.stdout.write("USER " + str(corrected_time) + ": " + transcript + "\n")
            sys.stdout.write("USER\t\t: " + transcript + "\n")

            stream.is_final_end_time = stream.result_end_time
            stream.last_transcript_was_final = True

            stream.closed = True

            return transcript

        else:
            sys.stdout.write(RED)
            sys.stdout.write("\033[K")
            sys.stdout.write("USER " + str(corrected_time) + "\t\t: " + transcript + "\r")

            stream.last_transcript_was_final = False


def main() -> None:
    """start bidirectional streaming from microphone input to speech API"""
    lang = "th-TH" # "th-TH" for Thai, "en-UK" for British English, "en-US" for American English, and "ja-JP" for Japanese
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=SAMPLE_RATE,
        language_code=lang,
        max_alternatives=1,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    
    # print(mic_manager.chunk_size)
    sys.stdout.write(BLUE)
    sys.stdout.write("\n" + "="*50 + "\n")
    sys.stdout.write("Voice Bot Application\n")
    sys.stdout.write("=====================================================\n")
    
    user_choice = input("Start voice conversation? (y/n): ").lower()
    
    if user_choice not in ('y', 'yes'):
        sys.stdout.write(YELLOW)
        sys.stdout.write("Exiting Voice Bot. Goodbye!\n")
        return
    
    sys.stdout.write(YELLOW)
    sys.stdout.write('\nListening... (Say "exit" or "หยุดการทำงาน" to end the conversation)\n\n')
    sys.stdout.write("ROLE :            Transcript Results/Status\n")
    sys.stdout.write("=====================================================\n")

    # llm = setup_gemini_api()
    llm = setup_gemini_api(
            system_instruction="Be the user's best friend. Use casual language. Escalate the conversation by inviting the user to talk about some random topic. Talk as if you're talking by mouth, so don't say anything too long, keep each turn under three sentences.", 
            max_output_tokens=128, 
            temperature=0.2
    )
    queue_manager = queuedTTS()

    while True:
        if not queue_manager.is_active:
            with ResumableMicrophoneStream(SAMPLE_RATE, CHUNK_SIZE) as stream:
                while not stream.closed:
                    sys.stdout.write(YELLOW)
                    sys.stdout.write(
                        # "\n" + str(STREAMING_LIMIT * stream.restart_counter) + ": NEW REQUEST\n"
                        "\n###YOU CAN TALK NOW###\r"
                    )

                    stream.audio_input = []
                    audio_generator = stream.generator()

                    requests = (
                        speech.StreamingRecognizeRequest(audio_content=content)
                        for content in audio_generator
                    )

                    responses = client.streaming_recognize(streaming_config, requests)

                    # Now, put the transcription responses to use.
                    transcript = transcribe_loop(responses, stream)

                    if not stream.last_transcript_was_final:
                        sys.stdout.write("\n")
                    stream.new_stream = True

            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r"\b(exit|quit|今日はこれで|หยุดการทำงาน|พอแล้ว|(วันนี้)?พอแค่นี้)\b", transcript, re.I):
                sys.stdout.write(YELLOW)
                sys.stdout.write("Exiting...\n")
                stream.closed = True
                break

        queue_manager.activate_queue()

        # Get a response from the AI model based on the user's transcript
        sys.stdout.write(YELLOW)
        sys.stdout.write("Thinking....\r")
        ai_response = get_ai_response(llm, transcript)
        sys.stdout.write(BLUE)
        sys.stdout.write("\033[K")
        sys.stdout.write(f"Assistant\t: ")
        response_buffer = ""
        for stream_chunk in ai_response:
            sys.stdout.write(stream_chunk.text)
            response_buffer += stream_chunk.text
            if "\n" in response_buffer:
                queue_manager.add_queue(response_buffer, lang=lang[:2], top_level_domain="co.uk" if lang[3:].upper() == "UK" else "com")
                response_buffer = ""
        
        if response_buffer != "" and queue_manager.start_playing_time is None:
            queue_manager.add_queue(response_buffer, lang=lang[:2], top_level_domain="co.uk" if lang[3:].upper() == "UK" else "com")
            response_buffer = ""


        after_loop_time = time.time()
        if (queue_manager.start_playing_time is not None) and after_loop_time - queue_manager.start_playing_time < queue_manager.last_sound_duration:
            time.sleep(queue_manager.last_sound_duration - (after_loop_time - queue_manager.start_playing_time))
        queue_manager.deactivate_queue()


if __name__ == "__main__":
    main()
