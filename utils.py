from datetime import datetime, timedelta, time, date
import os
from settings import load_settings

WEEKDAYS = {
    0: "Понедельник",
    1: "Вторник",
    2: "Среда",
    3: "Четверг",
    4: "Пятница",
    5: "Суббота",
    6: "Воскресенье"
}

short_names = {
    "Понедельник_Завтрак": "Понедельник_З",
    "Понедельник_Обед": "Понедельник_О",
    "Понедельник_Ужин": "Понедельник_У",
    "Вторник_Завтрак": "Вторник_З",
    "Вторник_Обед": "Вторник_О",
    "Вторник_Ужин": "Вторник_У",
    "Среда_Завтрак": "Среда_З",
    "Среда_Обед": "Среда_О",
    "Среда_Ужин": "Среда_У",
    "Четверг_Завтрак": "Четверг_З",
    "Четверг_Обед": "Четверг_О",
    "Четверг_Ужин": "Четверг_У",
    "Пятница_Завтрак": "Пятница_З",
    "Пятница_Обед": "Пятница_О",
    "Пятница_Ужин": "Пятница_У",
    "Суббота_Завтрак": "Суббота_З",
    "Суббота_Обед": "Суббота_О",
    "Суббота_Ужин": "Суббота_У"
}

REPORTS_FOLDER = "Отчеты"
if not os.path.exists(REPORTS_FOLDER):
    os.makedirs(REPORTS_FOLDER)

def get_meal_type(current_time, meal_times=None):
    if meal_times is None:
        meal_times = load_settings()
    hour = current_time.tm_hour
    minute = current_time.tm_min
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
    return now.weekday() == 5 and now.time() >= dinner_end_time

def get_last_report_date():
    try:
        with open("last_report_date.txt", "r") as file:
            last_date_str = file.read().strip()
            if last_date_str:
                return datetime.strptime(last_date_str, "%Y-%m-%d").date()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Ошибка чтения last_report_date.txt: {e}")
        return None

def get_last_saturday():
    try:
        today = date.today()
        days_since_saturday = (today.weekday() + 2) % 7
        return today - timedelta(days=days_since_saturday)
    except Exception as e:
        print(f"Ошибка при вычислении последней субботы: {e}")
        return None

def save_last_report_date(report_date=None):
    try:
        if report_date is None:
            report_date = get_last_saturday()
            if report_date is None:
                return
        with open("last_report_date.txt", "w") as file:
            file.write(report_date.strftime("%Y-%m-%d"))
    except Exception as e:
        print(f"Ошибка сохранения даты отчёта: {e}")

def delete_old_reports(folder_path, days_old=30):
    try:
        current_time = datetime.now()
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) and filename.endswith(".xlsx"):
                file_creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
                if (current_time - file_creation_time) > timedelta(days=days_old):
                    os.remove(file_path)
                    print(f"Удалён файл: {filename}")
    except Exception as e:
        print(f"Ошибка при удалении старых файлов: {e}")