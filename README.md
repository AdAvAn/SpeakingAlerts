
# Voice Alerts for Air Raid Warnings in Ukraine 🚨

I want to share with you the Python program to provide voice alerts for air raid warnings in Ukraine. 🇺🇦

## About the Program
The main goal is to use voice messages to inform you about air raid warnings declared in your region. It is not only useful for visually impaired individuals but also for anyone who wants to stay informed without being distracted from their daily activities.

The program uses the API of the website [Alerts.in.ua](https://alerts.in.ua) to obtain real-time information.

## Features
1. **Region Filtering:** Ignore warnings in undesired regions.
2. **Favorite Region:** Specify a special region where you are advised to take shelter during a warning.
3. **Multilingual:** Choose one of three languages (uk, en, de) for notifications.
4. **Warning Type:** Optional notification of the warning type (air raid warning, threat of artillery shelling, etc.).
5. **Audible Signal Before Notification:** To avoid sudden alerts.
6. **Status Unchanged Notification:** If you want to receive a message after each synchronization, the script can notify you about the unchanged status.

## Getting Started
⚠️ First, you need to obtain an API token. Simply submit a request by filling out the [form here](https://alerts.in.ua/api-request).

## Requirements
- Python3 and several dependencies (see `requirements.txt`).
- Device with a sound card and connected speakers, internet access.

```bash
sudo apt install python3 && pip install -r requirements.txt --break-system-packages
```

## Configuration
- Use example.config.ini for configuration by renaming it to config.ini.
```bash
mv example.config.ini config.ini
```

## Configuration File Parameters (`config.ini`).
| Parameter                        | Data Type | Default Value                               | Description                                                                                                     |
|----------------------------------|-----------|---------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| STATE_HANDLER_FILE_NAME          | String    | /tmp/alerts_state-2.json                    | Path to the file storing the current state in JSON format. Requires read/write access to the directory.       |
| ALERTS_IN_UA_TOKEN               | String    |                                             | Access key to the API alerts.in.ua                                                                             |
| PTT_SOUND                        | Bool      | true                                        | Play PTT sound before and after the message to avoid sudden alerts.                                            |
| LOCALE                           | String    | uk                                          | Localization used for notifications.                                                                            |
| NOTIFY_ONLY_WHEN_STATUS_CHANGED  | Bool      | true                                        | Notification is spoken only when the status changes.                                                           |
| FAVORITE_LOCATION                | String    | м. Київ                                     | Favorite region for special alerts.                                                                             |
| EXCLUDE_LOCATIONS                | String    | Автономна Республіка Крим, Луганська область | List of excluded locations, separated by commas, from observation.                                              |
| REPORT_THE_TYPE_OF_ALARM         | Bool      | true                                        | Include the type of alarm in the notification.                                                                 |
| REPEAT_FAVORITE_LOCATION_ALARM   | Int       | 1                                           | Number of repeats for notifications when a favorite location has a warning.                                     |
| List of all locations            | String    |                                             | List of available regions; use it to fill in EXCLUDE_LOCATIONS and FAVORITE_LOCATION parameters.              |

## Running
Launching the program is very simple. 
With this launch, the application will work as long as the console is open. For background work you will need to use the service.
```bash
/usr/bin/python3 alarms.py
```

## Service
To run the program as a service, you need to follow these steps
1. Rename example.config.ini to config.ini.
2. Move alarms.service to /lib/systemd/system/ and execute:

```bash
mv /SpeakingAlerts/alarms.service /lib/systemd/system/alarms.service && systemctl daemon-reload && systemctl start alarms.service
```

## Acknowledgments
I want to express my gratitude to my son **Constantin** for the idea and inspiration to create this program. Now we will always be informed and ready for possible dangers! 🙌🏼
