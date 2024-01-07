#   SpeakingAlerts
#   Created by Di (AdAvAn) on 08.01.2024.

import os
from pathlib import Path
from configparser import ConfigParser
from typing import List, Optional

class Settings:

    LOCALES = ["uk", "en", "de"]

    LOCATIONS = [
            "Автономна Республіка Крим",
            "Волинська область",
            "Вінницька область",
            "Дніпропетровська область",
            "Донецька область",
            "Житомирська область",
            "Закарпатська область",
            "Запорізька область",
            "Івано-Франківська область",
            "м. Київ",
            "Київська область",
            "Кіровоградська область",
            "Луганська область",
            "Львівська область",
            "Миколаївська область",
            "Одеська область",
            "Полтавська область",
            "Рівненська область",
            "м. Севастополь",
            "Сумська область",
            "Тернопільська область",
            "Харківська область",
            "Херсонська область",
            "Хмельницька область",
            "Черкаська область",
            "Чернівецька область",
            "Чернігівська область"
        ]

    def __init__(self, filename: str = "config.ini"):
  
        path = Path(__file__)
        ROOT_DIR = path.parent.absolute()
        config_path = os.path.join(ROOT_DIR, filename)
        parser = ConfigParser()
        result = parser.read(config_path)
        if result is None:
             raise ValueError(f"The settings file {filename} cannot be read.")
            
        try:    
            #General
            self._state_file_name:str = parser.get('General', 'STATE_HANDLER_FILE_NAME')
            self._alerts_token:str = parser.get('General', 'ALERTS_IN_UA_TOKEN')
            self._locale:str = self._check_is_correct_locale(parser.get('General', 'LOCALE').strip())
            self._ptt_sound:bool  = parser.getboolean('General', 'PTT_SOUND')
            self._notify_only_when_status_changed:bool = parser.getboolean('General', 'NOTIFY_ONLY_WHEN_STATUS_CHANGED')
        
            #Alert
            self._favorite_location:str = self._check_is_correct_locations([parser.get('Alert', 'FAVORITE_LOCATION').strip()])[0]
            self._report_the_type_of_alarm:bool = parser.getboolean('Alert', 'REPORT_THE_TYPE_OF_ALARM')
            self._repeat_favorite_location_alarm:int = parser.getint('Alert', 'REPEAT_FAVORITE_LOCATION_ALARM')
        except ConfigParser.NoOptionError :
            raise ValueError(f"The settings file {config_path} cannot be read.")

        exclude:str = parser.get('Alert', 'EXCLUDE_LOCATIONS').strip()

        if exclude:
            excluded = [item.strip() for item in exclude.split(',')]
            correct_locations = self._check_is_correct_locations(excluded)
            self._exclude_location = self._check_is_everything_is_filtered(correct_locations)
        else:
            self._exclude_location = []

        if self._alerts_token is None:
             raise KeyError(f"A token for accessing the service must be specified")
        
    def _check_is_correct_locations(self, locations:List[str]) -> List[str] :
        if len(locations) == 0: 
            return []
        
        received_locations = set(locations)
        available_locations = set(Settings.LOCATIONS)
        incorrect_elements = received_locations - available_locations

        if incorrect_elements:
            available_text = ', \n'.join(Settings.LOCATIONS)
            incorrect = ','.join(incorrect_elements) 
            raise ValueError(f"Incorrect location: '{incorrect}'. \n\nThe location name can be one of:\n {available_text} ")
        
        return locations
    
    def _check_is_correct_locale(self, locale:str) -> str :
        if locale in Settings.LOCALES:
            return locale
        else:
            available_text = ','.join(Settings.LOCALES)
            raise ValueError(f"Incorrect locale: {locale}. \n\nThe locale name can be one of:\n {available_text}")
    
    
    def _check_is_everything_is_filtered(self, locations:List[str]) -> List[str] :
        everything_is_filtered = locations == Settings.LOCATIONS

        if everything_is_filtered:
            raise ValueError(f"You have added all available locations to the filter, there must be at least one location that I can track.")
        
        return locations

    def get_state_file_path(self) -> str:
        return "alerts_state-2.json" if self._state_file_name == "" else self._state_file_name
    
    def get_alerts_service_token(self) -> str:
        return self._alerts_token
    
    def get_favorite_location(self) -> Optional[str]:
        return None if self._favorite_location == "" else self._favorite_location
    
    def get_exclude_location(self) -> List[str]:
        return [] if self._exclude_location == "" else self._exclude_location
    
    def get_ptt_sound_state(self) -> bool:
        return False if self._ptt_sound == "" else self._ptt_sound

    def get_locale(self) -> str:
        return "uk" if self._locale == "" else self._locale

    def get_notify_only_when_status_changed(self) -> bool:
        return self._notify_only_when_status_changed
    
    def get_report_the_type_of_alarm(self) -> bool:
        return self._report_the_type_of_alarm
    
    def get_repeat_favorite_location_alarm(self) -> int:
        if self._repeat_favorite_location_alarm is None:
            return 3
        return self._repeat_favorite_location_alarm  if 1 <= self._repeat_favorite_location_alarm <= 5 else 3
    