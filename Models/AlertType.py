#   SpeakingAlerts
#   Created by Di (AdAvAn) on 08.01.2024.

import json

class AlertType:
     
    _TYPE_KEY = "type"

    def __init__(self, type: str):
        self.type:str = type

    def get_type(self) -> str:
        return self.type
        
    ## From / to JSON
    def to_dict(self):
        return {
            AlertType._TYPE_KEY: self.get_type()
        }

    def to_json(self):
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=4)
    
    @classmethod
    def from_json(cls, json_str:str):
        try:
            json_dict = json.loads(json_str)
            type = json_dict.get(AlertType._TYPE_KEY)
            if type is None:
                raise KeyError(f"Values for key '{AlertType._TYPE_KEY}' in AlertType model is not different")
       
            return cls(type)
        except Exception as e:
            raise ValueError(f"Error decoding JSON to AlertType model. Error: {e}")

        