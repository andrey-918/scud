from datetime import datetime, time
from config import *
from settings import load_settings

def get_meal_type(current_time):
    hour = current_time.tm_hour
    minute = current_time.tm_min
    meal_times = load_settings()
    valid_meals = ["breakfast", "lunch", "dinner"]
    for meal_type, times in meal_times.items():
        if meal_type not in valid_meals:
            continue
        if not isinstance(times, dict):
            print(f"Ошибка: times для {meal_type} не является словарем. times = {times}")
            continue
        start_hour, start_minute = times["start"]
        end_hour, end_minute = times["end"]
        if (hour > start_hour or (hour == start_hour and minute >= start_minute)) and \
           (hour < end_hour or (hour == end_hour and minute < end_minute)):
            return meal_type
    return None

def is_saturday_dinner_end():
    now = datetime.now()
    settings = load_settings()
    dinner_end_hour, dinner_end_minute = settings["dinner"]["end"]
    dinner_end_time = time(dinner_end_hour, dinner_end_minute)
    if now.weekday() == 5:
        current_time = now.time()
        return current_time >= dinner_end_time
    return False