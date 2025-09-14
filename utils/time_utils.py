from datetime import datetime, timedelta, time, date
from config.settings import load_settings

def get_meal_type(current_time):
    settings = load_settings()
    print(f"Текущее время: {current_time}")
    print(f"Настройки: {settings}")
    hour = current_time.hour
    minute = current_time.minute
    valid_meals = ["breakfast", "lunch", "dinner"]

    for meal_type in valid_meals:
        if meal_type not in settings:
            continue
            
        meal_settings = settings[meal_type]
        if not isinstance(meal_settings, dict) or 'start' not in meal_settings or 'end' not in meal_settings:
            continue
            
        try:
            start_hour = int(meal_settings['start'][0])
            start_minute = int(meal_settings['start'][1])
            end_hour = int(meal_settings['end'][0])
            end_minute = int(meal_settings['end'][1])
            
            current_total_minutes = hour * 60 + minute
            start_total_minutes = start_hour * 60 + start_minute
            end_total_minutes = end_hour * 60 + end_minute
            
            if start_total_minutes <= current_total_minutes < end_total_minutes:
                return meal_type
                
        except (ValueError, TypeError, IndexError) as e:
            print(f"Ошибка в настройках для {meal_type}: {e}")
            continue
            
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

def check_and_generate_report(root):
    global report_generated
    report_generated = False
    try:
        from reports.report_generator import generate_visits_report
        last_report_date = get_last_report_date()
        last_saturday = get_last_saturday()
        if last_saturday is None:
            return
        if is_saturday_dinner_end() and not report_generated:
            generate_visits_report(last_saturday, root)
            report_generated = True
            print("Отчёт №1 сформирован автоматически.")
        elif not is_saturday_dinner_end():
            report_generated = False
        if last_report_date and last_report_date == last_saturday:
            return
        if last_report_date is None or last_report_date < last_saturday:
            generate_visits_report(last_saturday, root)
            report_generated = True
    except Exception as e:
        print(f"Ошибка в check_and_generate_report: {e}")
    finally:
        root.after(60000, lambda: check_and_generate_report(root))

def update_time_date(label, root):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%d.%m.%Y")
    label.config(text=f"{current_time}\n{current_date}")
    root.after(1000, lambda: update_time_date(label, root))