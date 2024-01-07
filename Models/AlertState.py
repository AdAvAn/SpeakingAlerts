#   SpeakingAlerts
#   Created by Di (AdAvAn) on 08.01.2024.

import json
from typing import List, Optional
from .AlertLocation import AlertLocation

class AlertState:

    _LOCATIONS_KEY = "alert_in_locations"

    def __init__(self, alert_in_locations:List[AlertLocation]):
        self.alert_in_locations:List[AlertLocation] = sorted(alert_in_locations)
        
    def get_total_alerts(self)->int:
        return len(self.get_alert_in_locations()) 
    
    def get_alert_in_locations(self) -> List[AlertLocation]:
        return self.alert_in_locations
    
    def __lt__(self, other):
        if isinstance(other, AlertState):
            return self.get_total_alerts() < other.get_total_alerts()
        return False
       
    def __eq__(self, other):
        if isinstance(other, AlertState):
            return self.get_total_alerts() == other.get_total_alerts()
        return False

    def __ne__(self, other):
        if isinstance(other, AlertState):
            return self.get_total_alerts() != other.get_total_alerts()
        return False

    def __gt__(self, other):
        if isinstance(other, AlertState):
            return self.get_total_alerts() > other.get_total_alerts()
        return False


    ## From / to JSON
    def to_dict(self) ->dict:
        return {
            AlertState._LOCATIONS_KEY: [location.to_dict() for location in self.get_alert_in_locations()]
        }
    
    def to_json(self) -> str:
       return json.dumps(self.to_dict(), ensure_ascii=False, indent=4)
    
    @classmethod
    def from_json(cls, json_str:str):
        try:
            json_dict:dict = json.loads(json_str)
            #decode all location if exist
            if AlertState._LOCATIONS_KEY in json_dict and isinstance(json_dict[AlertState._LOCATIONS_KEY], list):
                locations_json = json_dict.get(AlertState._LOCATIONS_KEY)
                alert_in_locations = [AlertLocation.from_json(json.dumps(location_json)) for location_json in locations_json]
                return cls(alert_in_locations)
            
            raise KeyError(f"Values for key '{AlertState._LOCATIONS_KEY}' in AlertState model is not different")
        except Exception as e:
            raise ValueError(f"Error decoding JSON to AlertState model. Error: {e}")
    