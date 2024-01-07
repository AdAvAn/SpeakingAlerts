#   SpeakingAlerts
#   Created by Di (AdAvAn) on 08.01.2024.

import json
from string import Template
import glob
import os
from Settings import Settings

class Translator:
    
    def __init__(self, settings: Settings):
        # initialization
        self._data:dict = {}
        self._locale = settings.get_locale()

        script_directory = os.path.dirname(os.path.abspath(__file__))
        translations_directory = os.path.join(script_directory, "Translations")
        translations = glob.glob(os.path.join(translations_directory, '*.json'))

        for file in translations:
            locale = os.path.splitext(os.path.basename(file))[0]
            with open(file, 'r', encoding='utf8') as f:
                self._data[locale] = json.load(f)

    def get_locale(self):
        return self._locale

    def translate(self, key, **kwargs):
        if self._locale not in self._data:
            return key

        text = self._data[self._locale].get(key, key)
        return Template(text).safe_substitute(**kwargs)
