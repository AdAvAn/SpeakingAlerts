#   SpeakingAlerts
#   Created by Di (AdAvAn) on 08.01.2024.

from typing import List, Optional
from Models.AlertState import AlertState
from Models.AlertLocation import AlertLocation
from Translator import Translator
from Settings import Settings

class Comparator:

    def __init__(self, new:AlertState, old:AlertState, settings: Settings, translator:Translator):
        self._new:AlertState = new
        self._old:AlertState = old

        self.settings:Settings = settings
        self.translator:Translator = translator
        
    def get_new(self) -> AlertState:
        return self._new
    
    def get_old(self) -> AlertState:
        return self._old

    def state_is_changed(self) -> bool: 
        return self.get_new() != self.get_old()

    def get_text_to_speech(self) -> str :
        if self.get_new() > self.get_old(): 
            return self._get_text_for_increasing_alerts()
        elif self.get_new() < self.get_old():
            return self._get_text_for_decreasing_alerts()
        else:
            if self.settings.get_notify_only_when_status_changed() == False:
                return self._get_text_for_no_change()
            else: 
                raise ValueError(f"Service state is not changed")
    
    def _get_different_locations(self) -> List[AlertLocation]:
        new_set = set(self.get_new().get_alert_in_locations())
        old_set = set(self.get_old().get_alert_in_locations())
        if new_set == old_set:
            return []
        else:
            return list(new_set - old_set) if self.get_new() > self.get_old() else list(old_set - new_set)
    
    def _get_different_and_favorites_locations(self) -> (List[AlertLocation], List[AlertLocation]):
        locations = self._get_different_locations()
        favorites = [location for location in locations if (location.get_is_favorite() == True)]
        return (locations, favorites)
        
    #increasing
    def _get_text_for_increasing_alerts(self) -> str:
        all_new, favorites = self._get_different_and_favorites_locations()
        if not favorites:
            return self._get_text_for_increasing_without_favorite_location(all_new)
        else:
            return self._get_text_for_increasing_with_favorite_location(favorites, all_new)
        
    def _get_text_for_increasing_with_favorite_location(self, favorites:List[AlertLocation], all_new:List[AlertLocation])-> str:
        not_favorites_locations = [location for location in all_new if (location.get_is_favorite() == False)]
        favorite_location_text = (f"{self.translator.translate('attention')}!!! {self.translator.translate('declared')} {self.translator.translate('alert_in')} {self._get_text_for_locations(favorites)}. {self.translator.translate('seek_shelter')}")
        double = self._repeat_text(favorite_location_text, self.settings.get_repeat_favorite_location_alarm())
        if not not_favorites_locations:
            return double    
        else: 
            return double + ". " + self._get_text_for_increasing_without_favorite_location(not_favorites_locations) 

    def _get_text_for_increasing_without_favorite_location(self, locations:List[AlertLocation])-> str:
        added_text = self.translator.translate('added_single') if len(locations) == 1 else self.translator.translate('added_plural')
        return (f"{self.translator.translate('number_of_locations_with_alert')} {self.translator.translate('increased_to')} {str(self._new.get_total_alerts())}. {added_text}: {self._get_text_for_locations(locations)}")

    #decreasing
    def _get_text_for_decreasing_alerts(self) -> str:
        all_new, favorites = self._get_different_and_favorites_locations()
        if not favorites:
            return self._get_text_for_decreasing_without_favorite_location(all_new)
        else: 
            return self._get_text_for_decreasing_with_favorite_location(favorites, all_new)
        
    def _get_text_for_decreasing_with_favorite_location(self, favorites:List[AlertLocation], all_new:List[AlertLocation]) -> str:
        favorites_locations = [region.get_title() for region in favorites] 
        not_favorites_locations = [location for location in all_new if (location.get_is_favorite() == False)]
        favorite_location_text = (f"{self.translator.translate('attention')}!!! {self.translator.translate('canceled')} {self.translator.translate('alert_in')} {', '.join(favorites_locations)}. ")
        double = self._repeat_text(favorite_location_text, self.settings.get_repeat_favorite_location_alarm())
        if not not_favorites_locations:
            return double    
        else: 
            return double + ". " +  self._get_text_for_decreasing_without_favorite_location(not_favorites_locations)
    
    def _get_text_for_decreasing_without_favorite_location(self, locations:List[AlertLocation]) -> str:
        if self._new.get_total_alerts() > 0:
            removed_locations = [location.get_title() for location in locations] 
            removed_text = self.translator.translate('alert_in') if len(locations) == 1 else self.translator.translate('alerts_in')
            return (f"{self.translator.translate('number_of_locations_with_alert')} {self.translator.translate('decreased_to')} {str(self._new.get_total_alerts())}. {self.translator.translate('canceled')} {removed_text} {', '.join(removed_locations)}")
        else: 
            return self.translator.translate('clear_sky')
  
    #not changed
    def _get_text_for_no_change(self) -> str:
        if self._new.get_total_alerts() > 0:
            region_text = self.translator.translate('location') if self._new.get_total_alerts() == 1 else self.translator.translate('locations')
            return (f"{self.translator.translate('no_change')}. {self.translator.translate('alerts_announced_in')} {self._new.get_total_alerts()} {region_text}")
        else:        
            return  (f"{self.translator.translate('no_change')}. {self.translator.translate('clear_sky')}") 
        

    def _get_text_for_locations(self, locations: List[AlertLocation]) -> str:
        if locations is None:
            return ""
        
        text: List[str] = []
        for location in locations:
            location_title = location.get_title()
            if self.settings.get_report_the_type_of_alarm() == True:
                type = location.get_alert_type().get_type()
                location_title_and_type = f"{self.translator.translate(type)}  {self.translator.translate('in')}: {location_title}"  
                text.append(location_title_and_type)
            else:
                text.append(location_title)

        return ', '.join(text)
    
    def _repeat_text(self, text: str, count:int):
       return (text + ", ") * (count - 1) + text
