import attacut
from gtts import gTTS
from mutagen.mp3 import MP3
import os
from playsound import playsound
from pythainlp.tokenize import word_tokenize
from pythainlp.util import normalize
import queue
import shutil
import time
import uuid

class queuedTTS:
  def __init__(self, save_dir:str="temp_speech"):
    self.queue : queue.Queue = queue.Queue()
    self.save_dir : str = save_dir
    self.is_active : bool = False
    self.is_playing : bool = False
    self.start_playing_time : float = None
    self.last_sound_duration : float = None

  def add_queue(self, text:str, lang:str="th", top_level_domain:str="com", save_dir:str=None):
    if not save_dir:
      save_dir = self.save_dir

    os.makedirs(save_dir, exist_ok=True)
    
    tempfile_name = f"{uuid.uuid4()}.mp3"

    tts = gTTS(text=normalize(text.replace("*", "")), lang=lang, tld=top_level_domain)
    tts.save(os.path.join(save_dir, tempfile_name))

    self.queue.put(tempfile_name)

    if self.is_active:
      self.play()

  def speak(self, speech_path:str, save_dir:str=None):
    if self.is_active:
      if not save_dir:
        save_dir = self.save_dir
      
      speech_path = os.path.join(save_dir, speech_path)

      duration = MP3(speech_path).info.length
      playsound(speech_path, block=False)
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
          path = self.queue.get()
          self.last_sound_duration = self.speak(path)
          self.start_playing_time = time.time()
      
      # if self.queue.qsize() == 0:
        # shutil.rmtree(self.save_dir)
    
    else:
      raise Exception("Queue is not activated")

if __name__ == "__main__":
  
  test = ["สวัสดีชาวไทย", "เรามาทำอะไรกันที่นี่", "ฉันชื่ออะไร", "คุณชื่ออะไร", "ไม่มีใครรู้"]
  
  queue_manager = queuedTTS()

  queue_manager.activate_queue()

  for text in test:
    queue_manager.add_queue(text)
  
  # queue_manager.play()