from dotenv import load_dotenv
load_dotenv()

import os
import re
import shutil
import sys
import time

from gcp_asr_api import ResumableMicrophoneStream, get_current_time

from queued_tts import QueuedTTS

from google.cloud import speech
from google import genai
from google.genai import types

from thefuzz import fuzz
import sounddevice as sd

# Audio recording parameters
STREAMING_LIMIT = 240000  # 4 minutes
SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE / 10)  # 100ms
BARGE_IN_SIMILARITY_THRESHOLD = 70 # Adjust % similarity (lower means more likely to barge-in)

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
BLUE = "\033[0;34m"
MAGENTA = "\033[0;35m"
CYAN = "\033[0;36m"
WHITE = "\033[0;37m"
REWRITE = "\033[K"
RESET = "\033[0m" # Reset color

def setup_gemini_api(
        system_instruction:str="You are a helpful assistant, help the user with any task. Be sure to keep everything concise. Answer in the user's language.",
        max_output_tokens:int=128,
        temperature:float=1.0):
    """Set up the Gemini API with the API key.
    
    Returns:
        Optional[genai.GenerativeModel]: The Gemini model or None if setup fails.
    """
    api_key = os.environ.get("GOOGLE_API_KEY", None)
    
    if not api_key:
        print(f"{YELLOW}GOOGLE_API_KEY environment variable not set.{RESET}")
        api_key = input("Please enter your Gemini API key: ").strip()
        if not api_key:
            print(f"{RED}No API key provided. Voice response functionality will be disabled.{RESET}")
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
        print(f"{RED}Error setting up Gemini API: {e}{RESET}")
        return None


def get_ai_response(model, transcript: str, streaming: bool=False) -> str:
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
        if streaming:
            response = model.send_message_stream(transcript)
        else:
            response = model.send_message(transcript)
        return response
    except Exception as e:
        return f"Error generating response: {e}"


def conversation_loop(responses: object, stream: object, queue_manager: QueuedTTS|None = None,  mode: str= "listen") -> None:
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

        speaking = re.sub(r"[\s\.!@#?]", "", queue_manager.speaking_text)[:len(transcript)] if queue_manager.speaking_text else None
        similarity = fuzz.ratio(transcript, speaking) if speaking else None 

        if result.is_final:
            if mode == "listen":
                print(f"{GREEN}{REWRITE}USER\t\t: {transcript}{RESET}", flush=True)
            elif mode == "speak":
                print(
                    f"{YELLOW}{REWRITE}Comparing {transcript} and {speaking.replace("\n", "")}. Similarity: {similarity}{RESET}", 
                    # end="\r", 
                    flush=True
                    )
                if similarity < BARGE_IN_SIMILARITY_THRESHOLD:
                    sd.stop()
                    print(f"{YELLOW}User barged-in, listening....{RESET}", flush=True)
                    return True
                else:
                    return False
            else:
                print(f"{RED}UNRECOGNIZED MODE! MODES ALLOWED: listen/speak{RESET}")

            stream.is_final_end_time = stream.result_end_time
            stream.last_transcript_was_final = True

            stream.closed = True

            return transcript

        else:
            if mode == "listen":
                print(f"{RED}{REWRITE}USER {str(corrected_time)}\t\t: {transcript}{RESET}", end="\r", flush=True)
            elif mode == "speak":
                # pass
                print(
                    f"{YELLOW}{REWRITE}Comparing {transcript} and {speaking.replace("\n", "")}. Similarity: {similarity}{RESET}", 
                    # end="\r", 
                    flush=True
                    )
                if similarity < BARGE_IN_SIMILARITY_THRESHOLD and len(transcript) >= 10:
                    sd.stop()
                    print(f"{YELLOW}User barged-in, listening....{RESET}", flush=True)
                    return True
            #     else:
            #         return False
            # else:
            #     print(f"{RED}UNRECOGNIZED MODE! MODES ALLOWED: listen/speak{RESET}")

            stream.last_transcript_was_final = False


def main() -> None:
    """start bidirectional streaming from microphone input to speech API"""

    print(f"{BLUE}\n=====================================================")
    print("Voice Bot Application")
    print(f"====================================================={RESET}")

    prompt_dict = {
        "th-TH" : "ทำตัวเป็นเพื่อนสนิทของผู้ใช้ การสนทนานี้เป็นการคุยกันด้วยเสียง ฉะนั้นตอบไม่เกินสองประโยค ชวนผู้ใช้คุยด้วยตนเอง",
        "en-US" : "You are the user's best friend. This is a communication by voice, so please keep your answers to no more than two sentences. Engage the user in conversation.",
        "en-UK" : "You are the user's best friend. This is a communication by voice, so please keep your answers to no more than two sentences. Engage the user in conversation.",
        "de-DE" : "Verhalte dich wie ein enger Freund des Benutzers. Bitte lass dich maximal bis zwei Sätzen per eine Antwort. Fängst du bitte den Gespräch mit dem Benutzer an.",
        "ja-JP" : "君はユーザーの親友であり、今からユーザーと音声会話を行うから、返答は二文以内にしてほしい。ユーザーに話しかけることを忘れないで。"
        }

    BARGE_IN_ENABLED = True # Set False to enable barge-in feature.
    STREAM_RESPONSE = False

    lang = "th-TH" # "th-TH" for Thai, "en-UK" for British English, "en-US" for American English, "de-DE" for standard German, and "ja-JP" for Japanese 
    prompt = prompt_dict[lang]

    print(f"{YELLOW}{REWRITE}Setting up.....{RESET}", end="\r")

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

    # user_prompt = input(f"{BLUE}Here's the default prompt for the LLM: {RESET}\n\n{WHITE}{prompt}\n\n{BLUE}You can write your own prompt here, or simply press [ENTER] to move on with the default prompt without typing anything.: {RESET}")

    # if user_prompt:
    #     prompt = user_prompt
    # else:
    #     print(f"\n{YELLOW}Using default prompt...{RESET}")

    # user_choice = input(f"{BLUE}Start voice conversation? (y/n): {RESET}").lower()
    
    # if user_choice not in ('y', 'yes'):
    #     print(f"{BLUE}Exiting Voice Bot. Goodbye!{RESET}")
    #     return
    
    print(f'{YELLOW}Listening... (Say "exit" or "หยุดการทำงาน" to end the conversation){RESET}', end='\n\n')
    print(f"{BLUE}ROLE :            Transcript Results/Status")
    print(f"====================================================={RESET}")

    llm = setup_gemini_api(
            system_instruction=prompt, 
            max_output_tokens=256, 
            temperature=0.7
    )
    queue_manager = QueuedTTS()

    app_running = True

    while app_running:
        if (queue_manager.start_playing_time is None) or (time.time() - queue_manager.start_playing_time > queue_manager.last_sound_duration) or not BARGE_IN_ENABLED:
            print(f"{BLUE}\n###YOU CAN TALK NOW###{RESET}", end="\r", flush=True)
            with ResumableMicrophoneStream(SAMPLE_RATE, CHUNK_SIZE) as user_listen_stream:
                while not user_listen_stream.closed:

                    user_listen_stream.audio_input = []
                    audio_generator = user_listen_stream.generator()

                    requests = (
                        speech.StreamingRecognizeRequest(audio_content=content)
                        for content in audio_generator
                    )

                    responses = client.streaming_recognize(streaming_config, requests)

                    # Now, put the transcription responses to use.
                    transcript = conversation_loop(responses, user_listen_stream, queue_manager, mode="listen")

                    # if user_listen_stream.result_end_time > 0:
                    #     user_listen_stream.final_request_end_time = user_listen_stream.is_final_end_time
                    # user_listen_stream.result_end_time = 0
                    # user_listen_stream.last_audio_input = []
                    # user_listen_stream.last_audio_input = user_listen_stream.audio_input
                    # user_listen_stream.audio_input = []
                    # user_listen_stream.restart_counter = user_listen_stream.restart_counter + 1

                    # if not user_listen_stream.last_transcript_was_final:
                    #     print("\n", end="")
                    user_listen_stream.new_stream = True

                    # Exit recognition if any of the transcribed phrases could be
                    # one of our keywords.
                    if re.search(r"\b(exit|quit|今日はこれで|หยุดการทำงาน|พอแล้ว|วันนี้พอแค่นี้)\b", transcript, re.I):
                        print(f"{YELLOW}Exiting...{RESET}")
                        user_listen_stream.closed = True
                        app_running = False
                        break

            queue_manager.activate_queue()

            # Get a response from the AI model based on the user's transcript
            print(f"{YELLOW}Thinking....{RESET}", end="\r")
            
            ai_response = get_ai_response(llm, transcript, STREAM_RESPONSE)
            print(f"{MAGENTA}{REWRITE}Assistant\t: ", end="")
            response_buffer = ""

            if STREAM_RESPONSE:

                for stream_chunk in ai_response:
                    print(stream_chunk.text, end="", flush=True)
                    response_buffer += stream_chunk.text
                    if " " in response_buffer:
                        splitted_str = response_buffer.split(" ")
                        queue_manager.add_queue(splitted_str.pop(0), lang=lang[:2], top_level_domain="co.uk" if lang[3:].upper() == "UK" else "com")
                        response_buffer = " ".join(splitted_str)
            
            else:
                response_buffer = ai_response.text
                print(response_buffer, end="")
            
            if response_buffer != "":
                queue_manager.add_queue(response_buffer, lang=lang[:2], top_level_domain="co.uk" if lang[3:].upper() == "UK" else "com")
                response_buffer = ""

            print(RESET)

            if not BARGE_IN_ENABLED:
                sd.wait()

            queue_manager.deactivate_queue()

        elif (queue_manager.start_playing_time is not None) and (time.time() - queue_manager.start_playing_time < queue_manager.last_sound_duration) and BARGE_IN_ENABLED:
            print(f"{BLUE}\n###LISTENING FOR BARGE-IN###{RESET}", end="\r", flush=True)
            with ResumableMicrophoneStream(SAMPLE_RATE, CHUNK_SIZE) as response_playing_stream:
                while not response_playing_stream.closed:

                    response_playing_stream.audio_input = []
                    audio_generator = response_playing_stream.generator()

                    requests = (
                        speech.StreamingRecognizeRequest(audio_content=content)
                        for content in audio_generator
                    )

                    responses = client.streaming_recognize(streaming_config, requests)

                    # Now, put the transcription responses to use.
                    user_barge_in = conversation_loop(responses, user_listen_stream, queue_manager, mode="speak")

                    # if response_playing_stream.result_end_time > 0:
                    #     response_playing_stream.final_request_end_time = response_playing_stream.is_final_end_time
                    # response_playing_stream.result_end_time = 0
                    # response_playing_stream.last_audio_input = []
                    # response_playing_stream.last_audio_input = response_playing_stream.audio_input
                    # response_playing_stream.audio_input = []
                    # response_playing_stream.restart_counter = response_playing_stream.restart_counter + 1

                    # if not response_playing_stream.last_transcript_was_final:
                    #     print("\n", end="")
                    if user_barge_in:
                        response_playing_stream.closed = True
                        queue_manager.clear_queue()
                        print(f"{YELLOW}User barged-in, listening....{RESET}", flush=True)
                        break
                    else:
                        queue_manager.clear_queue()
                        response_playing_stream.closed = True
                        break

            queue_manager.deactivate_queue()

if __name__ == "__main__":
    main()
