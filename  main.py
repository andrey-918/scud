import sqlite3
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import pandas as pd
from datetime import datetime, timedelta, time, date
import threading 
import json
import os
import time as time_module
from time import sleep
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Side, Alignment
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font
from openpyxl.formatting.rule import CellIsRule
from tkinter import simpledialog
"""import board
import busio
import digitalio
from adafruit_pn532.spi import PN532_SPI
from adafruit_ds3231 import DS3231"""

# Пути к базам данных и файлу настроек
DATABASE_STUDENTS = "students.db"
DATABASE_VISITS = "visits.db"
DATABASE_REQUESTS = "requests.db"
DATABASE_VISITS_REPORT = "visits_report.db"
SETTINGS_FILE = "settings.json"

# Инициализация PN532 через SPI
"""spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = digitalio.DigitalInOut(board.D5)  # Пин для выбора устройства (SS)
pn532 = PN532_SPI(spi, cs_pin, debug=False)
pn532.SAM_configuration()  # Настройка модуля 

# Инициализация RTC через I2C
i2c = busio.I2C(board.SCL, board.SDA)
rtc = DS3231(i2c)"""

# Пользовательские настройки времени приёмов пищи (по умолчанию)
DEFAULT_MEAL_TIMES = {
    "breakfast": {"start": (7, 0), "end": (10, 0)},
    "lunch": {"start": (12, 0), "end": (15, 0)},
    "dinner": {"start": (18, 0), "end": (21, 0)}
} 

DEFAULT_MIN_PERCENT = 65
default_password = "1111"
REPORTS_FOLDER = "Отчеты"

# Создаём папку, если её нет
if not os.path.exists(REPORTS_FOLDER):
    os.makedirs(REPORTS_FOLDER)

# Словарь для преобразования числа в название дня недели
WEEKDAYS = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}

# Словарь для переименования колонок
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

# Загрузка настроек из JSON-файла
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as file:
            try:
                settings = json.load(file)
                # Убедимся, что в настройках есть все необходимые поля
                if "password" not in settings:
                    settings["password"] = default_password  # Пароль по умолчанию
                if "min_percent" not in settings:
                    settings["min_percent"] = DEFAULT_MIN_PERCENT  # Минимальный процент по умолчанию
                # Убедимся, что время приёмов пищи присутствует
                for meal, times in DEFAULT_MEAL_TIMES.items():
                    if meal not in settings:
                        settings[meal] = times  # Добавляем время приёмов пищи по умолчанию
                return settings
            except json.JSONDecodeError:
                # Если файл повреждён, возвращаем настройки по умолчанию
                return {
                    **DEFAULT_MEAL_TIMES,
                    "password": default_password,
                    "min_percent": DEFAULT_MIN_PERCENT
                }
    # Если файла нет, возвращаем настройки по умолчанию
    return {
        **DEFAULT_MEAL_TIMES,
        "password": default_password,
        "min_percent": DEFAULT_MIN_PERCENT
    }

# Сохранение настроек в JSON-файл
def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)

# Загрузка настроек при запуске программы
meal_times = load_settings()

# Функция для создания подключения к базе данных
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")
    return conn

# Функция для создания таблиц
def create_tables():
    conn_students = create_connection(DATABASE_STUDENTS)
    if conn_students is not None:
        conn_students.execute('''
            CREATE TABLE IF NOT EXISTS students (
                uid TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                student_group TEXT NOT NULL
            );
        ''')
        conn_students.close()

    conn_visits = create_connection(DATABASE_VISITS)
    if conn_visits is not None:
        conn_visits.execute('''
            CREATE TABLE IF NOT EXISTS visits (
                uid TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                student_group TEXT NOT NULL,
                Понедельник_Завтрак INTEGER DEFAULT 0,
                Понедельник_Обед INTEGER DEFAULT 0,
                Понедельник_Ужин INTEGER DEFAULT 0,
                Вторник_Завтрак INTEGER DEFAULT 0,
                Вторник_Обед INTEGER DEFAULT 0,
                Вторник_Ужин INTEGER DEFAULT 0,
                Среда_Завтрак INTEGER DEFAULT 0,
                Среда_Обед INTEGER DEFAULT 0,
                Среда_Ужин INTEGER DEFAULT 0,
                Четверг_Завтрак INTEGER DEFAULT 0,
                Четверг_Обед INTEGER DEFAULT 0,
                Четверг_Ужин INTEGER DEFAULT 0,
                Пятница_Завтрак INTEGER DEFAULT 0,
                Пятница_Обед INTEGER DEFAULT 0,
                Пятница_Ужин INTEGER DEFAULT 0,
                Суббота_Завтрак INTEGER DEFAULT 0,
                Суббота_Обед INTEGER DEFAULT 0,
                Суббота_Ужин INTEGER DEFAULT 0
            );
        ''')
        conn_visits.close()

    conn_requests = create_connection(DATABASE_REQUESTS)
    if conn_requests is not None:
        conn_requests.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                uid TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                student_group TEXT NOT NULL,
                Понедельник_Завтрак INTEGER DEFAULT 0,
                Понедельник_Обед INTEGER DEFAULT 0,
                Понедельник_Ужин INTEGER DEFAULT 0,
                Вторник_Завтрак INTEGER DEFAULT 0,
                Вторник_Обед INTEGER DEFAULT 0,
                Вторник_Ужин INTEGER DEFAULT 0,
                Среда_Завтрак INTEGER DEFAULT 0,
                Среда_Обед INTEGER DEFAULT 0,
                Среда_Ужин INTEGER DEFAULT 0,
                Четверг_Завтрак INTEGER DEFAULT 0,
                Четверг_Обед INTEGER DEFAULT 0,
                Четверг_Ужин INTEGER DEFAULT 0,
                Пятница_Завтрак INTEGER DEFAULT 0,
                Пятница_Обед INTEGER DEFAULT 0,
                Пятница_Ужин INTEGER DEFAULT 0,
                Суббота_Завтрак INTEGER DEFAULT 0,
                Суббота_Обед INTEGER DEFAULT 0,
                Суббота_Ужин INTEGER DEFAULT 0
            );
        ''')
        conn_requests.close()

    # Создаем таблицу для отчетных данных
    conn_visits_report = create_connection(DATABASE_VISITS_REPORT)
    if conn_visits_report is not None:
        conn_visits_report.execute('''
            CREATE TABLE IF NOT EXISTS visits_report (
                uid TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                student_group TEXT NOT NULL,
                Понедельник_Завтрак INTEGER DEFAULT 0,
                Понедельник_Обед INTEGER DEFAULT 0,
                Понедельник_Ужин INTEGER DEFAULT 0,
                Вторник_Завтрак INTEGER DEFAULT 0,
                Вторник_Обед INTEGER DEFAULT 0,
                Вторник_Ужин INTEGER DEFAULT 0,
                Среда_Завтрак INTEGER DEFAULT 0,
                Среда_Обед INTEGER DEFAULT 0,
                Среда_Ужин INTEGER DEFAULT 0,
                Четверг_Завтрак INTEGER DEFAULT 0,
                Четверг_Обед INTEGER DEFAULT 0,
                Четверг_Ужин INTEGER DEFAULT 0,
                Пятница_Завтрак INTEGER DEFAULT 0,
                Пятница_Обед INTEGER DEFAULT 0,
                Пятница_Ужин INTEGER DEFAULT 0,
                Суббота_Завтрак INTEGER DEFAULT 0,
                Суббота_Обед INTEGER DEFAULT 0,
                Суббота_Ужин INTEGER DEFAULT 0
            );
        ''')
        conn_visits_report.close()

# Функция для загрузки общей базы данных из Excel
def load_database():
    file_path = filedialog.askopenfilename(title="Выберите файл базы данных", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        try:
            df = pd.read_excel(file_path, engine="openpyxl")
            conn_students = create_connection(DATABASE_STUDENTS)
            if conn_students is not None:
                cursor = conn_students.cursor()
                cursor.execute("DELETE FROM students")
                for _, row in df.iterrows():
                    cursor.execute("INSERT INTO students (uid, name, student_group) VALUES (?, ?, ?)",
                                  (row["uid"], row["name"], row["student_group"]))
                conn_students.commit()
                conn_students.close()
                messagebox.showinfo("Успех", "База данных успешно загружена!", parent=root)

                # Инициализация базы данных №2 (посещения)
                conn_visits = create_connection(DATABASE_VISITS)
                if conn_visits is not None:
                    cursor = conn_visits.cursor()
                    cursor.execute("DROP TABLE IF EXISTS visits")
                    cursor.execute('''
                        CREATE TABLE visits (
                            uid TEXT PRIMARY KEY,
                            name TEXT NOT NULL,
                            student_group TEXT NOT NULL,
                            Понедельник_Завтрак INTEGER DEFAULT 0,
                            Понедельник_Обед INTEGER DEFAULT 0,
                            Понедельник_Ужин INTEGER DEFAULT 0,
                            Вторник_Завтрак INTEGER DEFAULT 0,
                            Вторник_Обед INTEGER DEFAULT 0,
                            Вторник_Ужин INTEGER DEFAULT 0,
                            Среда_Завтрак INTEGER DEFAULT 0,
                            Среда_Обед INTEGER DEFAULT 0,
                            Среда_Ужин INTEGER DEFAULT 0,
                            Четверг_Завтрак INTEGER DEFAULT 0,
                            Четверг_Обед INTEGER DEFAULT 0,
                            Четверг_Ужин INTEGER DEFAULT 0,
                            Пятница_Завтрак INTEGER DEFAULT 0,
                            Пятница_Обед INTEGER DEFAULT 0,
                            Пятница_Ужин INTEGER DEFAULT 0,
                            Суббота_Завтрак INTEGER DEFAULT 0,
                            Суббота_Обед INTEGER DEFAULT 0,
                            Суббота_Ужин INTEGER DEFAULT 0
                        );
                    ''')
                    # Вставка всех студентов с нулевыми значениями посещений
                    for _, row in df.iterrows():
                        cursor.execute('''
                            INSERT INTO visits (uid, name, student_group) VALUES (?, ?, ?)
                        ''', (row["uid"], row["name"], row["student_group"]))
                    conn_visits.commit()
                    conn_visits.close()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить базу данных: {e}", parent=root)

# Функция для загрузки заявочного файла в заявочную базу данных
def load_requests_database():
    file_path = filedialog.askopenfilename(title="Выберите заявочный файл", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        try:
            # Чтение заявочного файла
            df = pd.read_excel(file_path, engine="openpyxl")
            
            # Подключение к базе данных №1 (студенты)
            conn_students = create_connection(DATABASE_STUDENTS)
            if conn_students is None:
                messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных студентов.", parent=root)
                return

            # Подключение к базе данных №3 (заявочные данные)
            conn_requests = create_connection(DATABASE_REQUESTS)
            if conn_requests is None:
                messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных заявок.", parent=root)
                return

            cursor_students = conn_students.cursor()
            cursor_requests = conn_requests.cursor()

            # Очистка таблицы заявочных данных перед загрузкой
            cursor_requests.execute("DELETE FROM requests")
            conn_requests.commit()

            # Загрузка всех студентов из базы данных №1
            cursor_students.execute("SELECT uid, name, student_group FROM students")
            all_students = cursor_students.fetchall()

            # Вставка всех студентов в базу данных №3 с нулевыми значениями
            for student in all_students:
                uid, name, student_group = student
                cursor_requests.execute('''
                    INSERT INTO requests (uid, name, student_group) VALUES (?, ?, ?)
                ''', (uid, name, student_group))

            # Обработка каждой строки заявочного файла
            for _, row in df.iterrows():
                name = row["ФИО"]
                group = row["Группа"]

                # Поиск UID студента в базе данных №1
                cursor_students.execute("SELECT uid FROM students WHERE name = ? AND student_group = ?", (name, group))
                result = cursor_students.fetchone()

                if result:
                    uid = result[0]  # UID студента
                    # Обновляем данные в базе данных №3 на основе заявочного файла
                    for column in df.columns[2:]:  # Пропускаем первые два столбца (ФИО и Группа)
                        if "_" in column:
                            requested = row[column]
                            if requested == 1:
                                cursor_requests.execute(f'''
                                    UPDATE requests
                                    SET {column} = 1
                                    WHERE uid = ?
                                ''', (uid,))

            conn_requests.commit()
            messagebox.showinfo("Успех", "Заявочный файл успешно загружен!", parent=root)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить заявочный файл: {e}", parent=root)
        finally:
            if conn_students:
                conn_students.close()
            if conn_requests:
                conn_requests.close()

def load_visits_report():
    file_path = filedialog.askopenfilename(
        title="Выберите отчет №1", 
        filetypes=[("Excel files", "*.xlsx")]
    )
    if file_path:
        try:
            # Чтение Excel файла
            df = pd.read_excel(file_path, engine="openpyxl")
            
            # Проверка структуры файла
            required_columns = [
                "uid", "name", "student_group",
                "Понедельник_З", "Понедельник_О", "Понедельник_У",
                "Вторник_З", "Вторник_О", "Вторник_У",
                "Среда_З", "Среда_О", "Среда_У",
                "Четверг_З", "Четверг_О", "Четверг_У",
                "Пятница_З", "Пятница_О", "Пятница_У",
                "Суббота_З", "Суббота_О", "Суббота_У"
            ]
            
            if not all(col in df.columns for col in required_columns):
                raise ValueError("Неверный формат файла отчета №1")
            
            # Словарь для преобразования коротких имен в полные
            full_names = {
                "Понедельник_З": "Понедельник_Завтрак",
                "Понедельник_О": "Понедельник_Обед",
                "Понедельник_У": "Понедельник_Ужин",
                "Вторник_З": "Вторник_Завтрак",
                "Вторник_О": "Вторник_Обед",
                "Вторник_У": "Вторник_Ужин",
                "Среда_З": "Среда_Завтрак",
                "Среда_О": "Среда_Обед",
                "Среда_У": "Среда_Ужин",
                "Четверг_З": "Четверг_Завтрак",
                "Четверг_О": "Четверг_Обед",
                "Четверг_У": "Четверг_Ужин",
                "Пятница_З": "Пятница_Завтрак",
                "Пятница_О": "Пятница_Обед",
                "Пятница_У": "Пятница_Ужин",
                "Суббота_З": "Суббота_Завтрак",
                "Суббота_О": "Суббота_Обед",
                "Суббота_У": "Суббота_Ужин"
            }
            
            # Переименовываем колонки
            df.rename(columns=full_names, inplace=True)
            
            conn = create_connection(DATABASE_VISITS_REPORT)
            if conn is not None:
                # Очистка старой базы
                conn.execute("DELETE FROM visits_report")
                
                # Запись новых данных
                df.to_sql('visits_report', conn, if_exists='append', index=False)
                conn.commit()
                messagebox.showinfo("Успех", "Данные отчета успешно загружены!", parent=root)
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки отчета: {e}", parent=root)
        finally:
            if conn:
                conn.close()

# Функция для определения текущего приёма пищи
def get_meal_type(current_time):
    hour = current_time.tm_hour
    minute = current_time.tm_min

    # Список допустимых приёмов пищи
    valid_meals = ["breakfast", "lunch", "dinner"]

    for meal_type, times in meal_times.items():
        # Пропускаем элементы, которые не являются приёмами пищи
        if meal_type not in valid_meals:
            continue

        # Проверяем, что times является словарем
        if not isinstance(times, dict):
            print(f"Ошибка: times для {meal_type} не является словарем. times = {times}")
            continue

        start_hour, start_minute = times["start"]
        end_hour, end_minute = times["end"]

        if (hour > start_hour or (hour == start_hour and minute >= start_minute)) and \
           (hour < end_hour or (hour == end_hour and minute < end_minute)):
            return meal_type

    return None

# Функция для отображения окна "Успешно"
def show_success_window():
    success_window = tk.Toplevel(root)
    success_window.title("Успешно")
    success_window.attributes('-fullscreen', True)
    tk.Label(success_window, text="Успешно!", font=("Arial", 48), bg="green", fg="white").pack(expand=True, fill='both')
    success_window.after(3000, success_window.destroy)  # Закрыть окно через 3 секунды

def show_no_meal_window():
    no_meal_window = tk.Toplevel(root)
    no_meal_window.title("Сейчас не время приёма пищи")
    no_meal_window.attributes('-fullscreen', True)
    tk.Label(no_meal_window, text="Сейчас не время приёма пищи", font=("Arial", 36), bg="red", fg="white").pack(expand=True, fill='both')
    no_meal_window.after(3000, no_meal_window.destroy)  # Закрыть окно через 3 секунды

"""def process_uid(uid):
    current_time = rtc.datetime
    meal_type = get_meal_type(current_time)
    if meal_type:
        # Используем модуль datetime для вычисления дня недели
        year = current_time.tm_year
        month = current_time.tm_mon
        day = current_time.tm_mday
        date_obj = datetime(year, month, day)
        day_of_week = date_obj.weekday()  # 0 - понедельник, 6 - воскресенье

        # Преобразуем число в русское название дня недели
        russian_weekdays = {
            0: "Понедельник",
            1: "Вторник",
            2: "Среда",
            3: "Четверг",
            4: "Пятница",
            5: "Суббота",
            6: "Воскресенье"
        }
        day_name = russian_weekdays[day_of_week]  # Используем русские названия

        # Преобразуем английские названия приёмов пищи в русские
        meal_type_translation = {
            "breakfast": "Завтрак",
            "lunch": "Обед",
            "dinner": "Ужин"
        }
        russian_meal_type = meal_type_translation.get(meal_type, meal_type)  # Если нет перевода, оставляем как есть

        # Формируем название колонки для обновления (например, "Понедельник_Завтрак")
        column_name = f"{day_name}_{russian_meal_type}"

        conn_visits = create_connection(DATABASE_VISITS)
        if conn_visits is not None:
            try:
                cursor = conn_visits.cursor()
                # Проверяем, есть ли запись о студенте в таблице visits
                cursor.execute("SELECT * FROM visits WHERE uid = ?", (uid,))
                result = cursor.fetchone()

                if result:
                    # Если запись существует, обновляем соответствующую колонку
                    cursor.execute(f'''
                        UPDATE visits
                        SET {column_name} = 1
                        WHERE uid = ?
                    ''', (uid,))
                else:
                    # Если записи нет, проверяем базу данных №1 (students)
                    conn_students = create_connection(DATABASE_STUDENTS)
                    if conn_students is not None:
                        cursor_students = conn_students.cursor()
                        cursor_students.execute("SELECT name, student_group FROM students WHERE uid = ?", (uid,))
                        student_data = cursor_students.fetchone()

                        if student_data:
                            # Если UID найден в базе данных №1, используем данные оттуда
                            name, student_group = student_data
                        else:
                            # Если UID не найден, используем значения по умолчанию
                            name, student_group = "Неизвестный", "Неизвестная группа"

                        # Создаем новую запись в базе данных №2
                        cursor.execute('''
                            INSERT INTO visits (uid, name, student_group)
                            VALUES (?, ?, ?)
                        ''', (uid, name, student_group))
                        cursor.execute(f'''
                            UPDATE visits
                            SET {column_name} = 1
                            WHERE uid = ?
                        ''', (uid,))

                        conn_students.close()

                conn_visits.commit()
                print(f"UID {uid} обработан для {meal_type} ({russian_meal_type}) в {day_name}.")
                show_success_window()  # Показать окно "Успешно"
            except Exception as e:
                print(f"Ошибка при обработке UID: {e}")
            finally:
                conn_visits.close()
    else:
        print("Сейчас не время приёма пищи.")
        show_no_meal_window()
        
        
# Функция для считывания карт в фоновом режиме
def read_rfid():
    try:
        while True:
            print("Поднесите карту к считывателю...")
            uid = pn532.read_passive_target(timeout=0.5)  # Считывание UID
            if uid is not None:
                uid_str = "".join([f"{byte:02X}" for byte in uid])  # Преобразование UID в строку
                print(f"Считан UID: {uid_str}")
                process_uid(uid_str)
            sleep(1)
    except KeyboardInterrupt:
        print("Считывание карт остановлено.")"""

def is_saturday_dinner_end():
    now = datetime.now()
    
    # Загружаем настройки
    settings = load_settings()
    
    # Получаем время окончания ужина из настроек
    dinner_end_hour, dinner_end_minute = settings["dinner"]["end"]
    dinner_end_time = time(dinner_end_hour, dinner_end_minute)
    
    # Проверяем, что сегодня суббота (5 - суббота)
    if now.weekday() == 5:
        current_time = now.time()
        return current_time >= dinner_end_time
    return False

report_generated = False

def check_and_generate_report():
    global report_generated
    
    try:
        last_report_date = get_last_report_date()
        last_saturday = get_last_saturday()
        
        # Если не удалось определить последнюю субботу - выходим
        if last_saturday is None:
            return
            
        # Если сейчас суббота после ужина и отчет еще не сформирован
        if is_saturday_dinner_end() and not report_generated:
            generate_visits_report(last_saturday)
            report_generated = True
            print("Отчёт №1 сформирован автоматически.")
        elif not is_saturday_dinner_end():
            report_generated = False
        
        # Если отчет уже был сформирован для последней субботы - пропускаем
        if last_report_date and last_report_date == last_saturday:
            return

        # Если отчет не был сформирован для последней субботы
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
        today = date.today()  # Используем date из datetime
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

# Функция для создания выпадающего списка времени
def create_time_combobox(parent, default_value, range_max, width=3):
    frame = tk.Frame(parent)
    frame.pack(fill='x', padx=5, pady=5)
    var = tk.StringVar(value=str(default_value).zfill(2))
    combobox = ttk.Combobox(frame, textvariable=var, values=[str(i).zfill(2) for i in range(range_max)], 
                           font=('Arial', 36), state='readonly', width=width)  # Увеличенный шрифт
    combobox.pack(side='left', padx=5)
    return var

# Функция для открытия окна настроек
def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Настройки")
    settings_window.attributes('-fullscreen', True)  # Полноэкранный режим
    
    # Загрузка текущих настроек
    settings = load_settings()
    
    # Основной фрейм для содержимого
    content_frame = tk.Frame(settings_window)
    content_frame.pack(expand=True, fill='both', padx=20, pady=20)

    # Шрифты
    title_font = ('Arial', 36)  # Увеличенные шрифты
    label_font = ('Arial', 28)
    time_font = ('Arial', 28)
    button_font = ('Arial', 32)

    def create_time_section(parent, meal_name, meal_data):
        meal_frame = tk.Frame(parent)
        meal_frame.pack(fill='x', pady=10)
        
        tk.Label(meal_frame, text=meal_name.capitalize() + ":", font=title_font).pack(anchor='w', pady=5)
        
        # Фрейм для времени начала
        start_frame = tk.Frame(meal_frame)
        start_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(start_frame, text="Начало:", font=label_font).pack(side='left', padx=5)
        
        hour_var = tk.StringVar(value=str(meal_data['start'][0]).zfill(2))
        minute_var = tk.StringVar(value=str(meal_data['start'][1]).zfill(2))
        
        ttk.Combobox(start_frame, textvariable=hour_var, 
                    values=[str(i).zfill(2) for i in range(24)], 
                    font=time_font, width=3, state='readonly').pack(side='left', padx=5)
        tk.Label(start_frame, text=":", font=label_font).pack(side='left')
        ttk.Combobox(start_frame, textvariable=minute_var, 
                    values=[str(i).zfill(2) for i in range(60)], 
                    font=time_font, width=3, state='readonly').pack(side='left', padx=5)
        
        # Фрейм для времени окончания
        end_frame = tk.Frame(meal_frame)
        end_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(end_frame, text="Окончание:", font=label_font).pack(side='left', padx=5)
        
        end_hour_var = tk.StringVar(value=str(meal_data['end'][0]).zfill(2))
        end_minute_var = tk.StringVar(value=str(meal_data['end'][1]).zfill(2))
        
        ttk.Combobox(end_frame, textvariable=end_hour_var, 
                    values=[str(i).zfill(2) for i in range(24)], 
                    font=time_font, width=3, state='readonly').pack(side='left', padx=5)
        tk.Label(end_frame, text=":", font=label_font).pack(side='left')
        ttk.Combobox(end_frame, textvariable=end_minute_var, 
                    values=[str(i).zfill(2) for i in range(60)], 
                    font=time_font, width=3, state='readonly').pack(side='left', padx=5)
        
        return {
            'start': (hour_var, minute_var),
            'end': (end_hour_var, end_minute_var)
        }

    # Создаем секции времени
    time_vars = {
        'breakfast': create_time_section(content_frame, "Завтрак", settings['breakfast']),
        'lunch': create_time_section(content_frame, "Обед", settings['lunch']),
        'dinner': create_time_section(content_frame, "Ужин", settings['dinner'])
    }

    # Разделительная линия
    tk.Frame(content_frame, height=2, bg='gray').pack(fill='x', pady=20)

    # Дополнительные настройки
    tk.Label(content_frame, text="Минимальный процент посещений:", font=label_font).pack(anchor='w', pady=5)
    min_percent_entry = tk.Entry(content_frame, font=time_font)
    min_percent_entry.insert(0, str(settings.get("min_percent", DEFAULT_MIN_PERCENT)))
    min_percent_entry.pack(fill='x', padx=20, pady=5)

    tk.Label(content_frame, text="Новый пароль:", font=label_font).pack(anchor='w', pady=5)
    new_password_entry = tk.Entry(content_frame, font=time_font, show='*')
    new_password_entry.pack(fill='x', padx=20, pady=5)

    # Фрейм для кнопок
    button_frame = tk.Frame(content_frame)
    button_frame.pack(fill='x', pady=20)

    def save_settings_handler():
        try:
            for meal_type in ['breakfast', 'lunch', 'dinner']:
                settings[meal_type]['start'] = (
                    int(time_vars[meal_type]['start'][0].get()),
                    int(time_vars[meal_type]['start'][1].get())
                )
                settings[meal_type]['end'] = (
                    int(time_vars[meal_type]['end'][0].get()),
                    int(time_vars[meal_type]['end'][1].get())
                )

            settings["min_percent"] = int(min_percent_entry.get())
            
            if new_password := new_password_entry.get():
                settings["password"] = new_password

            save_settings(settings)
            messagebox.showinfo("Успех", "Настройки сохранены!", parent=settings_window)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Неверный формат данных: {e}", parent=settings_window)

    tk.Button(button_frame, text="Настройка времени на ПК", 
             command=lambda: open_rtc_time_setting(), 
             font=button_font, bg="#2196F3", fg="white").pack(fill='x', pady=5)
    
    tk.Button(button_frame, text="Сохранить", command=save_settings_handler, 
             font=button_font, bg="#2196F3", fg="white").pack(fill='x', pady=5)
    
    # Кнопка "Выход"
    tk.Button(button_frame, text="Выход", command=settings_window.destroy, 
             font=button_font, bg="#f44336", fg="white").pack(fill='x', pady=5)

def open_rtc_time_setting():
    rtc_window = tk.Toplevel(root)
    rtc_window.title("Настройка времени на DS3231")
    rtc_window.attributes('-fullscreen', True)

    # Основной фрейм для содержимого
    content_frame = tk.Frame(rtc_window)
    content_frame.pack(expand=True, fill='both', padx=20, pady=20)

    # Шрифты (увеличенные)
    label_font = ('Arial', 32)
    time_font = ('Arial', 32)
    button_font = ('Arial', 32)

    current_time = datetime.now()

    # Поля для ввода времени
    tk.Label(content_frame, text="Год (YYYY):", font=label_font).pack(anchor='w', pady=5)
    year_var = tk.StringVar(value=str(current_time.year))
    ttk.Combobox(content_frame, textvariable=year_var, 
                values=[str(i) for i in range(2000, 2100)], 
                font=time_font, state='readonly').pack(fill='x', padx=20)

    tk.Label(content_frame, text="Месяц (MM):", font=label_font).pack(anchor='w', pady=5)
    month_var = tk.StringVar(value=str(current_time.month).zfill(2))
    ttk.Combobox(content_frame, textvariable=month_var, 
                values=[str(i).zfill(2) for i in range(1, 13)], 
                font=time_font, state='readonly').pack(fill='x', padx=20)

    tk.Label(content_frame, text="День (DD):", font=label_font).pack(anchor='w', pady=5)
    day_var = tk.StringVar(value=str(current_time.day).zfill(2))
    ttk.Combobox(content_frame, textvariable=day_var, 
                values=[str(i).zfill(2) for i in range(1, 32)], 
                font=time_font, state='readonly').pack(fill='x', padx=20)

    tk.Label(content_frame, text="Час (HH):", font=label_font).pack(anchor='w', pady=5)
    hour_var = tk.StringVar(value=str(current_time.hour).zfill(2))
    ttk.Combobox(content_frame, textvariable=hour_var, 
                values=[str(i).zfill(2) for i in range(24)], 
                font=time_font, state='readonly').pack(fill='x', padx=20)

    tk.Label(content_frame, text="Минуты (MM):", font=label_font).pack(anchor='w', pady=5)
    minute_var = tk.StringVar(value=str(current_time.minute).zfill(2))
    ttk.Combobox(content_frame, textvariable=minute_var, 
                values=[str(i).zfill(2) for i in range(60)], 
                font=time_font, state='readonly').pack(fill='x', padx=20)

    tk.Label(content_frame, text="Секунды (SS):", font=label_font).pack(anchor='w', pady=5)
    second_var = tk.StringVar(value=str(current_time.second).zfill(2))
    ttk.Combobox(content_frame, textvariable=second_var, 
                values=[str(i).zfill(2) for i in range(60)], 
                font=time_font, state='readonly').pack(fill='x', padx=20)

    # Фрейм для кнопок
    button_frame = tk.Frame(content_frame)
    button_frame.pack(fill='x', pady=20)

    def set_time():
        try:
            new_time = time_module.struct_time((
                int(year_var.get()),
                int(month_var.get()),
                int(day_var.get()),
                int(hour_var.get()),
                int(minute_var.get()),
                int(second_var.get()),
                0, -1, -1
            ))
            #rtc.datetime = new_time
            #sync_time_with_ds3231()
            messagebox.showinfo("Успех", "Время успешно установлено!", parent=rtc_window)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось установить время: {e}", parent=rtc_window)

    # Кнопка "Установить время"
    tk.Button(button_frame, text="Установить время", command=set_time,
             font=button_font, bg="#2196F3", fg="white").pack(fill='x', pady=5)
    
    # Кнопка "Выход"
    tk.Button(button_frame, text="Выход", command=rtc_window.destroy,
             font=button_font, bg="#f44336", fg="white").pack(fill='x', pady=5)

def set_rtc_time(year_var, month_var, day_var, hour_var, minute_var, second_var, window=None):
    try:
        # Получаем значения из полей ввода
        year = int(year_var.get())
        month = int(month_var.get())
        day = int(day_var.get())
        hour = int(hour_var.get())
        minute = int(minute_var.get())
        second = int(second_var.get())

        # Создаем структуру времени с помощью time.struct_time
        new_time = time_module.struct_time((year, month, day, hour, minute, second, 0, -1, -1))

        # Устанавливаем время на DS3231
        #rtc.datetime = new_time

        # Синхронизируем время Raspberry Pi с DS3231
        #sync_time_with_ds3231()

        # Показываем сообщение об успехе
        messagebox.showinfo("Успех", "Время успешно установлено!", parent=window)
    except Exception as e:
        # Показываем сообщение об ошибке
        messagebox.showerror("Ошибка", f"Не удалось установить время: {e}", parent=window)

"""def sync_time_with_ds3231():
    try:
        # Получение времени с DS3231
        rtc_time = rtc.datetime
        print(f"Время на DS3231: {rtc_time.tm_year}-{rtc_time.tm_mon}-{rtc_time.tm_mday} {rtc_time.tm_hour}:{rtc_time.tm_min}:{rtc_time.tm_sec}")

        # Установка системного времени Raspberry Pi
        time_str = f"{rtc_time.tm_year}-{rtc_time.tm_mon}-{rtc_time.tm_mday} {rtc_time.tm_hour}:{rtc_time.tm_min}:{rtc_time.tm_sec}"
        os.system(f"sudo date -s '{time_str}'")
        print("Время синхронизировано с DS3231.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось синхронизировать время: {e}", parent=root)"""

def disable_ntp():
    print("Отключаем NTP...")
    os.system("sudo timedatectl set-ntp false")
    sleep(1)  # Даем системе время на выполнение команды

# Функция для формирования отчёта о посещениям
def generate_visits_report(report_date=None):
    try:
        if report_date is None:
            report_date = datetime.now().date()

        conn_visits = create_connection(DATABASE_VISITS)
        if conn_visits is not None:
            # Чтение данных о посещениях
            visits_df = pd.read_sql_query("SELECT * FROM visits", conn_visits)

            # Переименование колонок
            visits_df.rename(columns=short_names, inplace=True)

            # Формируем имя файла с текущей датой
            date_str = report_date.strftime("%Y-%m-%d")
            default_filename = f"Отчет_по_посещениям_{date_str}.xlsx"
            report_path = os.path.join(REPORTS_FOLDER, default_filename)

            # Сохранение в Excel с настройкой стилей
            wb = Workbook()
            ws = wb.active

            # Записываем данные из DataFrame в Excel
            for r in dataframe_to_rows(visits_df, index=False, header=True):
                ws.append(r)

            # Настройка стилей
            thin_border = Border(
                left=Side(style='thin'),
                right=Side(style='thin'),
                top=Side(style='thin'),
                bottom=Side(style='thin')
            )

            # Границы для заголовков и колонок uid, name, student_group
            for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
                for cell in row:
                    if cell.row == 1:
                        cell.border = thin_border
                    elif cell.column_letter in ["A", "B", "C"]:
                        cell.border = thin_border

            # Автоматическая ширина колонок
            for col in ws.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2)
                ws.column_dimensions[column].width = adjusted_width

            # Сохранение файла
            wb.save(report_path)
            messagebox.showinfo("Успех", f"Отчёт №1 сохранён в {report_path}", parent=root)

            with open("last_report_date.txt", "w") as file:
                file.write(date_str)

            # Очистка БД №2 после успешного сохранения
            # Обнуление данных о посещениях в БД №2
            cursor = conn_visits.cursor()
            
            # Список колонок, которые нужно обнулить (все колонки, кроме uid, name, student_group)
            columns_to_reset = [
                "Понедельник_Завтрак", "Понедельник_Обед", "Понедельник_Ужин",
                "Вторник_Завтрак", "Вторник_Обед", "Вторник_Ужин",
                "Среда_Завтрак", "Среда_Обед", "Среда_Ужин",
                "Четверг_Завтрак", "Четверг_Обед", "Четверг_Ужин",
                "Пятница_Завтрак", "Пятница_Обед", "Пятница_Ужин",
                "Суббота_Завтрак", "Суббота_Обед", "Суббота_Ужин"
            ]

            # Формируем SQL-запрос для обнуления колонок
            reset_query = f"""
                UPDATE visits
                SET {', '.join([f"{col} = 0" for col in columns_to_reset])}
            """
            
            save_last_report_date()

            # Выполняем запрос
            cursor.execute(reset_query)
            conn_visits.commit()

            delete_old_reports(REPORTS_FOLDER)    
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сформировать отчёт №1: {e}", parent=root)
    finally:
        if conn_visits:
            conn_visits.close()

def generate_visits_report_everyday():
    try:
        conn_visits = create_connection(DATABASE_VISITS)
        if conn_visits is not None:
            # Чтение данных о посещениях
            visits_df = pd.read_sql_query("SELECT * FROM visits", conn_visits)

            # Переименование колонок
            visits_df.rename(columns=short_names, inplace=True)

            # Формируем имя файла с текущей датой
            current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            default_filename = f"Отчет_по_посещениям_РГ_{current_date}.xlsx"
            report_path = os.path.join(REPORTS_FOLDER, default_filename)  # Сохраняем в папку "отчеты"

            # Сохранение в Excel с настройкой стилей
            wb = Workbook()
            ws = wb.active

            # Записываем данные из DataFrame в Excel
            for r in dataframe_to_rows(visits_df, index=False, header=True):
                ws.append(r)

            # Настройка стилей
            thin_border = Border(
                left=Side(style='thin'),
                right=Side(style='thin'),
                top=Side(style='thin'),
                bottom=Side(style='thin')
            )

            # Границы для заголовков и колонок uid, name, student_group
            for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
                for cell in row:
                    if cell.row == 1:
                        cell.border = thin_border
                    elif cell.column_letter in ["A", "B", "C"]:
                        cell.border = thin_border

            # Автоматическая ширина колонок
            for col in ws.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2)
                ws.column_dimensions[column].width = adjusted_width

            # Сохранение файла
            wb.save(report_path)
            messagebox.showinfo("Успех", f"Отчёт №1 сохранён в {report_path}", parent=root)

            delete_old_reports(REPORTS_FOLDER)    
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сформировать отчёт №1: {e}", parent=root)
    finally:
        if conn_visits:
            conn_visits.close()

# Функция для формирования отчета с аналитикой
def generate_analytics_report():
    try:
        load_requests_database()
        load_visits_report()

        conn_visits = create_connection(DATABASE_VISITS_REPORT)
        conn_requests = create_connection(DATABASE_REQUESTS)

        if conn_visits is not None and conn_requests is not None:
            # 1. Чтение данных
            visits_df = pd.read_sql_query("SELECT * FROM visits_report", conn_visits)
            requests_df = pd.read_sql_query("SELECT * FROM requests", conn_requests)
            
            # 2. Объединение таблиц
            report_df = pd.merge(
                visits_df, 
                requests_df, 
                on=["uid", "name", "student_group"], 
                suffixes=("_visit", "_request")
            )
            
            # 3. Переименование колонок с '_visit' в чистые названия
            meal_columns = [
                "Понедельник_Завтрак", "Понедельник_Обед", "Понедельник_Ужин",
                "Вторник_Завтрак", "Вторник_Обед", "Вторник_Ужин",
                "Среда_Завтрак", "Среда_Обед", "Среда_Ужин",
                "Четверг_Завтрак", "Четверг_Обед", "Четверг_Ужин",
                "Пятница_Завтрак", "Пятница_Обед", "Пятница_Ужин",
                "Суббота_Завтрак", "Суббота_Обед", "Суббота_Ужин"
            ]

            # Создаем словарь для переименования: {'Понедельник_Завтрак_visit': 'Понедельник_Завтрак', ...}
            rename_dict = {col + "_visit": col for col in meal_columns}
            report_df.rename(columns=rename_dict, inplace=True)
            
            # 4. Удаление колонок с '_request'
            report_df.drop(columns=[col + "_request" for col in meal_columns], inplace=True)
            
            """#Фильтрация: удаляем студентов, которые ни разу не посещали приемы пищи
            report_df["total_visits"] = report_df[meal_columns].sum(axis=1)
            report_df = report_df[report_df["total_visits"] > 0]
            report_df.drop(columns=["total_visits"], inplace=True)"""

            # 5. Добавление аналитических колонок
            report_df["Всего заявок"] = requests_df[meal_columns].sum(axis=1)
            report_df["Посещения по заявке"] = report_df.apply(
                lambda row: sum(
                    1 for col in meal_columns 
                    if requests_df.loc[row.name, col] == 1 and row[col] == 1
                ), 
                axis=1
            )
            report_df["Посещения без заявки"] = report_df.apply(
                lambda row: sum(
                    1 for col in meal_columns 
                    if requests_df.loc[row.name, col] == 0 and row[col] == 1
                ), 
                axis=1
            )
            report_df["Процент посещения"] = report_df.apply(
                lambda row: round((row["Посещения по заявке"] / row["Всего заявок"] * 100)) 
                if row["Всего заявок"] > 0 
                else 0, 
                axis=1
            )

            # 6. Формирование финальной таблицы
            final_columns = [
                "name", "student_group", 
                *meal_columns, 
                "Всего заявок", "Посещения по заявке", 
                "Посещения без заявки", "Процент посещения"
            ]
            final_report_df = report_df[final_columns].copy()
            
            # Переименование name и student_group
            final_report_df.rename(columns={
                "name": "ФИО",
                "student_group": "Группа"
            }, inplace=True)

            # 7. Сокращение названий колонок
            final_report_df.rename(columns=short_names, inplace=True)

            # 8. Добавление строки с итогами посещений
            # Создаем словарь для итоговой строки
            total_row = {"ФИО": "Итого", "Группа": ""}  # Первые две колонки

            # Используем переименованные названия колонок для суммирования
            for col in meal_columns:
                renamed_col = short_names.get(col, col)  # Получаем переименованное название колонки
                total_row[renamed_col] = final_report_df[renamed_col].sum()  # Сумма по каждому столбцу

            # Добавляем пустые значения для аналитических колонок
            total_row["Всего заявок"] = ""
            total_row["Посещения по заявке"] = ""
            total_row["Посещения без заявки"] = ""
            total_row["Процент посещения"] = ""

            # Преобразуем словарь в DataFrame и добавляем в конец final_report_df
            total_df = pd.DataFrame([total_row])
            final_report_df = pd.concat([final_report_df, total_df], ignore_index=True)

            settings = load_settings()
            min_percent = settings.get("min_percent", DEFAULT_MIN_PERCENT)

            current_date = datetime.now().strftime("%Y-%m-%d")  # Формат: Год-Месяц-День_Часы-Минуты-Секунды
            default_filename = f"Отчет_с_аналитикой_{current_date}.xlsx"

            # 9. Сохранение в Excel с настройкой стилей
            report_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx", 
                filetypes=[("Excel files", "*.xlsx")],
                initialfile=default_filename  # Указываем имя файла по умолчанию
            )
            if report_path:
                # Создаем Excel-файл
                wb = Workbook()
                ws = wb.active

                # Записываем данные из DataFrame в Excel
                for r in dataframe_to_rows(final_report_df, index=False, header=True):
                    ws.append(r)

                # Настройка стилей
                yellow_fill = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")  # Желтый цвет
                thin_border = Border(
                    left=Side(style='thin'),
                    right=Side(style='thin'),
                    top=Side(style='thin'),
                    bottom=Side(style='thin')
                )

                # Подсветка ячеек с посещениями без заявки
                for row in ws.iter_rows(min_row=2, max_row=ws.max_row - 1, min_col=1, max_col=ws.max_column):
                    for cell in row:
                        if cell.column_letter in ["C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S"]:
                            if cell.value == 1 and requests_df.loc[cell.row - 2, meal_columns[cell.column - 3]] == 0:
                                cell.fill = yellow_fill

                # Границы для заголовков, колонок "ФИО", "Группа" и аналитических колонок
                for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
                    for cell in row:
                        if cell.row == 1:
                            cell.border = thin_border
                        elif cell.column_letter in ["A", "B"]:
                            cell.border = thin_border
                        elif cell.column_letter in ["U", "V", "W", "X"]:
                            cell.border = thin_border
                        elif cell.row == ws.max_row:  # Итоговая строка
                            cell.border = thin_border

                # Условное форматирование для процента посещения (красный шрифт, если < min_percent)
                red_font = Font(color="FF0000")  # Красный цвет шрифта
                conditional_rule = CellIsRule(operator='lessThan', formula=[min_percent], font=red_font)
                ws.conditional_formatting.add(f"X2:X{ws.max_row - 1}", conditional_rule)

                # Автоматическая ширина колонок
                for col in ws.columns:
                    max_length = 0
                    column = col[0].column_letter
                    for cell in col:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = (max_length + 2)
                    ws.column_dimensions[column].width = adjusted_width

                # Объединение ячеек в итоговой строке
                last_row = ws.max_row  # Номер последней строки

                # Объединяем первые две ячейки (A и B)
                ws.merge_cells(start_row=last_row, start_column=1, end_row=last_row, end_column=2)

                # Объединяем последние четыре ячейки (U, V, W, X)
                ws.merge_cells(start_row=last_row, start_column=21, end_row=last_row, end_column=24)

                # Выравнивание текста в объединенных ячейках по центру
                ws.cell(row=last_row, column=1).alignment = Alignment(horizontal="center", vertical="center")
                ws.cell(row=last_row, column=21).alignment = Alignment(horizontal="center", vertical="center")

                # Выравнивание текста по центру во всем файле
                for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
                    for cell in row:
                        cell.alignment = Alignment(horizontal="center", vertical="center")

                # Сохранение файла
                wb.save(report_path)
                messagebox.showinfo("Успех", f"Отчёт №2 сохранён в {report_path}", parent=root)
                
                delete_old_reports(REPORTS_FOLDER)

    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сформировать отчёт №2: {e}", parent=root)
    finally:
        if conn_visits:
            conn_visits.close()
        if conn_requests:
            conn_requests.close()

def delete_old_reports(folder_path, days_old=30):
    try:
        # Получаем текущее время
        current_time = datetime.now()
        
        # Проходим по всем файлам в папке
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            # Проверяем, является ли это файлом и имеет ли расширение .xlsx
            if os.path.isfile(file_path) and filename.endswith(".xlsx"):
                # Получаем время создания файла
                file_creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
                
                # Вычисляем разницу во времени
                time_difference = current_time - file_creation_time
                
                # Если файл старше 30 дней, удаляем его
                if time_difference > timedelta(days=days_old):
                    os.remove(file_path)
                    print(f"Удалён файл: {filename}")
    except Exception as e:
        print(f"Ошибка при удалении старых файлов: {e}")

def update_time_date(label):
    now = datetime.now()  # Получаем текущее время и дату
    current_time = now.strftime("%H:%M:%S")  # Форматируем время
    current_date = now.strftime("%d.%m.%Y")  # Форматируем дату
    label.config(text=f"{current_time}\n{current_date}")  # Обновляем текст в Label
    root.after(1000, update_time_date, label)  # Обновляем каждую секунду (1000 мс)

def open_user_window():
    # Загружаем настройки
    settings = load_settings()
    correct_password = settings.get("password", default_password)

    # Создаем окно для ввода пароля
    password_window = tk.Toplevel(root)
    password_window.title("Ввод пароля")
    password_window.attributes('-fullscreen', True)
    
    # Шрифты
    label_font = ('Arial', 36)
    entry_font = ('Arial', 36)
    button_font = ('Arial', 36)

    # Фрейм для элементов ввода пароля
    password_frame = tk.Frame(password_window)
    password_frame.pack(expand=True, fill='both', padx=50, pady=50)

    # Метка и поле ввода пароля
    tk.Label(password_frame, text="Введите пароль:", font=label_font).pack(pady=20)
    password_entry = tk.Entry(password_frame, show='*', font=entry_font)
    password_entry.pack(pady=20, ipady=20)
    password_entry.focus_set()  # Устанавливаем фокус на поле ввода пароля

    def check_password():
        if password_entry.get() == correct_password:
            password_window.destroy()
            show_user_window()
        else:
            messagebox.showerror("Ошибка", "Неверный пароль", parent=password_window)

    # Привязываем обработчик нажатия Enter к проверке пароля
    password_entry.bind('<Return>', lambda event: check_password())

    # Кнопка подтверждения
    tk.Button(password_frame, text="Войти", command=check_password, 
             font=button_font, bg="#2196F3", fg="white").pack(pady=20, ipady=20, fill='x')

    # Кнопка выхода
    tk.Button(password_frame, text="Выход", command=password_window.destroy, 
             font=button_font, bg="#f44336", fg="white").pack(pady=20, ipady=20, fill='x')

def show_user_window():
    user_window = tk.Toplevel(root)
    user_window.title("Управление")
    user_window.attributes('-fullscreen', True)

    # Основной фрейм для кнопок
    main_frame = tk.Frame(user_window)
    main_frame.pack(expand=True, fill='both', padx=50, pady=50)

    # Шрифт для кнопок
    button_font = ('Arial', 42)

    # Создаем фреймы для кнопок
    top_frame = tk.Frame(main_frame)
    top_frame.pack(expand=True, fill='both', pady=20)
    
    middle_frame = tk.Frame(main_frame)
    middle_frame.pack(expand=True, fill='both', pady=20)
    
    bottom_frame = tk.Frame(main_frame)
    bottom_frame.pack(expand=True, fill='both', pady=20)

    # Кнопки управления
    tk.Button(top_frame, text="Загрузить базу данных", command=load_database, 
             font=button_font, bg="#2196F3", fg="white").pack(expand=True, fill='both', pady=10)
    
    tk.Button(top_frame, text="Сформировать отчёт по посещениям", command=generate_visits_report_everyday, 
             font=button_font, bg="#2196F3", fg="white").pack(expand=True, fill='both', pady=10)
    
    tk.Button(middle_frame, text="Сформировать отчёт с аналитикой", command=generate_analytics_report, 
             font=button_font, bg="#2196F3", fg="white").pack(expand=True, fill='both', pady=10)
    
    tk.Button(middle_frame, text="Настройки", command=open_settings, 
             font=button_font, bg="#2196F3", fg="white").pack(expand=True, fill='both', pady=10)
    
    tk.Button(bottom_frame, text="Выход", command=user_window.destroy, 
             font=button_font, bg="#f44336", fg="white").pack(expand=True, fill='both', pady=10)
    
    
# Основное окно приложения
def main():
    create_tables()
    #disable_ntp()

    global root
    root = tk.Tk()
    root.title("Учёт льготного питания")
    root.attributes('-fullscreen', True)  # Открываем на весь экран

    # Добавляем Label для отображения времени и даты
    time_date_label = tk.Label(root, font=("Arial", 48), fg="black")
    time_date_label.pack(expand=True, fill='both', pady=50)

    # Запускаем обновление времени и даты
    update_time_date(time_date_label)

    # Кнопка "Пользователь" с увеличенным контрастом
    tk.Button(
        root, 
        text="Пользователь", 
        command=open_user_window, 
        font=("Arial", 36),
        bg="#2196F3",
        fg="white",
        height=3
    ).pack(expand=True, fill='both', padx=100, pady=50)
    
    # Запуск считывания карт в фоновом режиме
    #rfid_thread = threading.Thread(target=read_rfid, daemon=True)
    #rfid_thread.start()

    check_and_generate_report()

    root.mainloop()

if __name__ == "__main__":
    main()