import os

# Database paths
DATABASE_STUDENTS = "students.db"
DATABASE_VISITS = "visits.db"
DATABASE_REQUESTS = "requests.db"
DATABASE_VISITS_REPORT = "visits_report.db"
SETTINGS_FILE = "settings.json"
REPORTS_FOLDER = "Отчеты"

DEFAULT_MEAL_TIMES = {
    "breakfast": {"start": (7, 0), "end": (10, 0)},
    "lunch": {"start": (12, 0), "end": (15, 0)},
    "dinner": {"start": (18, 0), "end": (21, 0)}
}

DEFAULT_MIN_PERCENT = 65
DEFAULT_PASSWORD = "1111"

WEEKDAYS = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}

SHORT_NAMES = {
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

if not os.path.exists(REPORTS_FOLDER):
    os.makedirs(REPORTS_FOLDER)

def disable_ntp():
    print("Отключаем NTP...")
    os.system("sudo timedatectl set-ntp false")
    import time
    time.sleep(1)  