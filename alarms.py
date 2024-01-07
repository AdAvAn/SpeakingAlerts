#   SpeakingAlerts
#   Created by Di (AdAvAn) on 08.01.2024.

from Settings import Settings
from DataSource import DataSource
from Comparator import Comparator
from Keeper import Keeper
from Translator import Translator
from Speaker import Speaker

try:
    settings = Settings()
    keeper = Keeper(settings)
    new_alert_state = DataSource(settings).get_current_alert_state()
    previews_state = keeper.load_or_update_state(new_alert_state)
    comparator = Comparator(new_alert_state, previews_state, settings, Translator(settings))
    keeper.update_state(new_alert_state)
    Speaker(settings).speak(comparator.get_text_to_speech())
except Exception as e:
    print(f"Failed to start services. Reason: \n\n {e}")

