from datetime import datetime, time, date, timedelta
from logging import root
from reports import generate_visits_report
from settings import load_settings

def get_meal_type(current_time):
    hour = current_time.tm_hour
    minute = current_time.tm_min
    valid_meals = ["breakfast", "lunch", "dinner"]
    settings = load_settings()
    for meal_type, times in settings.items():
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

def check_and_generate_report():
    global report_generated
    try:
        last_report_date = get_last_report_date()
        last_saturday = get_last_saturday()
        if last_saturday is None:
            return
        if is_saturday_dinner_end() and not report_generated:
            generate_visits_report(last_saturday)
            report_generated = True
            print("Отчёт №1 сформирован автоматически.")
        elif not is_saturday_dinner_end():
            report_generated = False
        if last_report_date and last_report_date == last_saturday:
            return
        if last_report_date is None or last_report_date < last_saturday:
            generate_visits_report(last_saturday)
            report_generated = True
    except Exception as e:
        print(f"Ошибка в check_and_generate_report: {e}")
    finally:
        root.after(60000, check_and_generate_report)

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