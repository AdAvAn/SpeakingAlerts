#   SpeakingAlerts
#   Created by Di (AdAvAn) on 08.01.2024.

import json
from Models.AlertState import AlertState
from Settings import Settings

class Keeper:

    # Initializes a StateHandler object with the specified state file name.
    def __init__(self, settings: Settings):
        self._file_path = settings.get_state_file_path()

    def get_file_path(self) -> str:
        return self._file_path

    # Saves the current Alert state to the file.
    def update_state(self, alert: AlertState):
        try:
            with open(self.get_file_path(), 'w', encoding='utf-8') as file:
                json.dump(alert.to_dict(), file, ensure_ascii=False, indent=4)
        except Exception as e:
            raise FileExistsError(f"Unable to write alert data to file, error: {e}")

    # Loads the state from the file if it exists; otherwise, returns an empty dictionary.
    def load_or_update_state(self, new_state: AlertState) -> AlertState:
        try:
            with open(self.get_file_path(), 'r', encoding='utf-8') as file:
                content = file.read()
                if content is None:
                    self.update_state(new_state)
                    return new_state
                return AlertState.from_json(content)
        except FileNotFoundError:
            self.update_state(new_state) 
            return new_state
        except Exception as e:
            raise FileExistsError(f"Unable to read data from file, error: {e}")