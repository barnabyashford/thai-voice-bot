from dotenv import load_dotenv
load_dotenv()

from mutagen.mp3 import MP3
import os
import sounddevice as sd
import soundfile as sf
import queue
import shutil
import time
import uuid

from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

class QueuedTTS:
  def __init__(self, save_dir:str="temp_speech"):
    self.queue : queue.Queue = queue.Queue()
    self.save_dir : str = save_dir
    self.is_active : bool = False
    self.is_playing : bool = False
    self.start_playing_time : float | None = None
    self.last_sound_duration : float | None = None
    self.speaking_text : str | None = None
    self.synthesis_duration : float | None = None

  def add_queue(self, text:str, lang:str="th-TH", save_dir:str=None):
    if not save_dir:
      save_dir = self.save_dir

    synthesis_start_time = time.time()

    os.makedirs(save_dir, exist_ok=True)
    
    tempfile_name = f"{uuid.uuid4()}.mp3"

    voice = texttospeech.VoiceSelectionParams(
        language_code=lang,
        name=f"{lang}-Chirp3-HD-Orus",
    )

    input_text = texttospeech.SynthesisInput(text=text)

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # Write the response audio content to a file
    with open(os.path.join(save_dir, tempfile_name), "wb") as out:
        out.write(response.audio_content)

    synthesis_end_time = time.time()
    synthesis_duration = synthesis_end_time - synthesis_start_time

    self.queue.put((tempfile_name, text, synthesis_duration))

    if self.is_active:
      self.play()

  def speak(self, speech_path:str, save_dir:str=None):
    if self.is_active:
      if not save_dir:
        save_dir = self.save_dir
      
      speech_path = os.path.join(save_dir, speech_path)

      duration = MP3(speech_path).info.length

      data, fs = sf.read(speech_path, dtype='float32')
      sd.play(data, fs)

      os.remove(speech_path)

      return duration
  
  def activate_queue(self):
    self.is_active = True
    if self.queue.qsize() > 0:
      self.play()

  def deactivate_queue(self):
    self.is_active = False

  def play(self):
    if self.is_active:

      while self.queue.qsize() > 0:

        self.is_playing = (self.start_playing_time is not None) and (time.time() - self.start_playing_time < self.last_sound_duration)

        if not self.is_playing:
          path, text, synthesis_duration = self.queue.get()
          self.synthesis_duration = synthesis_duration
          self.speaking_text = text
          self.last_sound_duration = self.speak(path)
          self.start_playing_time = time.time()
    
    else:
      raise Exception("Queue is not activated")

  def clear_queue(self):
    self.queue.queue.clear()
    self.start_playing_time = None
    self.last_sound_duration = None
    self.speaking_text = None
    self.is_playing = False

    shutil.rmtree(self.save_dir)

if __name__ == "__main__":
  
  test = ["สวัสดีชาวไทย", "เรามาทำอะไรกันที่นี่", "ฉันชื่ออะไร", "คุณชื่ออะไร", "ไม่มีใครรู้"]
  
  queue_manager = QueuedTTS()

  queue_manager.activate_queue()

  for text in test:
    queue_manager.add_queue(text)
  
  # queue_manager.play()

  sd.wait()

  queue_manager.deactivate_queue()
