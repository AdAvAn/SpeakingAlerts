#   SpeakingAlerts
#   Created by Di (AdAvAn) on 08.01.2024.

import os
import pygame
from gtts import gTTS
from Settings import Settings
from io import BytesIO

class Speaker:

    def __init__(self, settings: Settings):
        self.settings:Settings = settings
    
    def speak(self, text:str):
        try:
            stream = BytesIO()
            tts = gTTS(text=text, lang=self.settings.get_locale())
            tts.write_to_fp(stream)
            stream.seek(0)
            self._ptt()
            self._play(stream)
            self._ptt()
        except Exception as e:
           raise ChildProcessError(f"Speaker services. Error when pronouncing text. Error: {e}")
            
    def _ptt(self):
        if self.settings.get_ptt_sound_state() == False:
            return
        script_directory = os.path.dirname(os.path.abspath(__file__))
        ptt_path = os.path.join(script_directory, "ptt.mp3")
        self._play(ptt_path)

    def _play(self, stream):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(stream)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue                      
        except Exception as e:
           raise ChildProcessError(f"Speaker services. Error: {e}")
