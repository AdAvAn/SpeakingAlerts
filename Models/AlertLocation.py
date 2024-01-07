#   SpeakingAlerts
#   Created by Di (AdAvAn) on 08.01.2024.

import json
from .AlertType import AlertType

class AlertLocation:

    _TITLE_KEY = "title"
    _IS_FAVORITE_KEY = "is_favorite"
    _ALERT_TYPE_KEY = "alert_type"

    def __init__(self, title:str, is_favorite:bool, alert_type:AlertType):
        self.title:str = title
        self.is_favorite:bool = is_favorite
        self.alert_type:AlertType = alert_type

    def get_title(self)->str:
        return self.title
    
    def get_alert_type(self)->AlertType:
        return self.alert_type

    def get_is_favorite(self)->bool:
        return self.is_favorite
    
    def __hash__(self):
        return hash(self.title)

    def __eq__(self, other):
        if isinstance(other, AlertLocation):
            return self.title == other.title
        return False

    def __lt__(self, other):
        if isinstance(other, AlertLocation):
            return self.get_is_favorite() > other.get_is_favorite()
        return False    

    ## From / to JSON
    def to_dict(self):
        return {
            AlertLocation._TITLE_KEY: self.get_title(), 
            AlertLocation._IS_FAVORITE_KEY: self.get_is_favorite(), 
            AlertLocation._ALERT_TYPE_KEY: self.get_alert_type().to_dict()
        }
    
    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=4)
    
    @classmethod
    def from_json(cls, json_str:str):
        try:
            json_dict = json.loads(json_str)
            is_favorite = json_dict.get(AlertLocation._IS_FAVORITE_KEY, False)
            title = json_dict.get(AlertLocation._TITLE_KEY)
            alert_type_json = json_dict.get(AlertLocation._ALERT_TYPE_KEY)

            if title is None or alert_type_json is None:
                  raise KeyError(f"Values for keys '{AlertLocation._TITLE_KEY}' or {AlertLocation._ALERT_TYPE_KEY} in AlertState model is not different")

            alert_type = AlertType.from_json(json.dumps(alert_type_json))
            
            return cls(title, is_favorite, alert_type)
        except Exception as e:
            raise ValueError(f"Error decoding JSON to AlertLocation model. Error: {e}")
    

