import json
import os
from config.constants import SETTINGS_FILE, DEFAULT_MEAL_TIMES, DEFAULT_PASSWORD, DEFAULT_MIN_PERCENT

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            try:
                settings = json.load(file)
                # Ensure all required fields are present
                if "password" not in settings:
                    settings["password"] = DEFAULT_PASSWORD
                if "min_percent" not in settings:
                    settings["min_percent"] = DEFAULT_MIN_PERCENT
                for meal, times in DEFAULT_MEAL_TIMES.items():
                    if meal not in settings:
                        settings[meal] = times
                return settings
            except json.JSONDecodeError:
                # Return default settings if file is corrupted
                return {
                    **DEFAULT_MEAL_TIMES,
                    "password": DEFAULT_PASSWORD,
                    "min_percent": DEFAULT_MIN_PERCENT
                }
    # Return default settings if file doesn't exist
    return {
        **DEFAULT_MEAL_TIMES,
        "password": DEFAULT_PASSWORD,
        "min_percent": DEFAULT_MIN_PERCENT
    }

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)