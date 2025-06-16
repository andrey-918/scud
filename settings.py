import json
import os

SETTINGS_FILE = "settings.json"
DEFAULT_MEAL_TIMES = {
    "breakfast": {"start": (7, 0), "end": (10, 0)},
    "lunch": {"start": (12, 0), "end": (15, 0)},
    "dinner": {"start": (18, 0), "end": (21, 0)}
}
DEFAULT_MIN_PERCENT = 65
default_password = "1111"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            try:
                settings = json.load(file)
                if "password" not in settings:
                    settings["password"] = default_password
                if "min_percent" not in settings:
                    settings["min_percent"] = DEFAULT_MIN_PERCENT
                for meal, times in DEFAULT_MEAL_TIMES.items():
                    if meal not in settings:
                        settings[meal] = times
                return settings
            except json.JSONDecodeError:
                return {**DEFAULT_MEAL_TIMES, "password": default_password, "min_percent": DEFAULT_MIN_PERCENT}
    return {**DEFAULT_MEAL_TIMES, "password": default_password, "min_percent": DEFAULT_MIN_PERCENT}

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)