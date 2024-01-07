#   SpeakingAlerts
#   Created by Di (AdAvAn) on 08.01.2024.

from alerts_in_ua import Client 
from typing import List, Optional
from Models.AlertState import AlertState
from Models.AlertLocation import AlertLocation
from Models.AlertType import AlertType
from Settings import Settings

class DataSource:

    FILTER_LOCATION_KEY = "oblast"

    # Initializes a StateHandler object with the specified state file name.
    def __init__(self, settings:Settings):
        self.alerts_client:Client = Client(token=settings.get_alerts_service_token())
        self._exclude_location:Optional[List[str]] = settings.get_exclude_location() 
        self._favorite_location:Optional[str] = settings.get_favorite_location()

        if self._favorite_location is not None and self._exclude_location is not None and self._favorite_location in self._exclude_location:
             self._exclude_location.remove(self._favorite_location)
             

    # Receive fresh data about current alarms and send information in the form of json
    def get_current_alert_state(self) -> AlertState:
        try:
            active_alerts = self.alerts_client.get_active_alerts()
            alerts_by_location = active_alerts.get_alerts_by_location_type(DataSource.FILTER_LOCATION_KEY)
        except Exception as e:
            raise ConnectionError(f"Unable to receive data, error:: {e}")
      
       
        # Make content
        filtered_locations: List[AlertLocation] = []
        for alert in self._get_filtrated_alerts(alerts_by_location):
            is_favorite_location:bool = False
            if self._favorite_location is not None:
                is_favorite_location = self._favorite_location == alert.location_title
     
            type = AlertType(alert.alert_type)
            location = AlertLocation(alert.location_title, is_favorite_location, type)
            filtered_locations.append(location)
         
        return AlertState(filtered_locations)

    # Select data for only the locations that interest us
    def _get_filtrated_alerts(self, alerts_by_location) -> List:
        if self._exclude_location is not None:
            return [alert for alert in alerts_by_location if alert.location_title not in self._exclude_location]
        else:
            return alerts_by_location

 