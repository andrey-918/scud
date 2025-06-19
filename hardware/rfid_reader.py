import tkinter as tk
from config.settings import load_settings
from database.db_init import create_connection
from database.db_operations import DATABASE_STUDENTS, DATABASE_VISITS
from hardware import rtc
from utils.time_utils import get_meal_type
from datetime import datetime

import board
import busio
import digitalio
from adafruit_pn532.spi import PN532_SPI
from adafruit_ds3231 import DS3231

from time import sleep

def show_success_window(root):
    success_window = tk.Toplevel(root)
    success_window.title("Успешно")
    success_window.attributes('-fullscreen', True)
    tk.Label(success_window, text="Успешно!", font=("Arial", 48), bg="green", fg="white").pack(expand=True, fill='both')
    success_window.after(3000, success_window.destroy)

def show_no_meal_window(root):
    no_meal_window = tk.Toplevel(root)
    no_meal_window.title("Сейчас не время приёма пищи")
    no_meal_window.attributes('-fullscreen', True)
    tk.Label(no_meal_window, text="Сейчас не время приёма пищи", font=("Arial", 36), bg="red", fg="white").pack(expand=True, fill='both')
    no_meal_window.after(3000, no_meal_window.destroy)

# def process_uid(uid, root, current_time):
#     meal_type = get_meal_type(current_time)
#     if meal_type:
#         year = current_time.tm_year
#         month = current_time.tm_mon
#         day = current_time.tm_mday
#         date_obj = datetime(year, month, day)
#         day_of_week = date_obj.weekday()

#         russian_weekdays = {
#             0: "Понедельник",
#             1: "Вторник",
#             2: "Среда",
#             3: "Четверг",
#             4: "Пятница",
#             5: "Суббота",
#             6: "Воскресенье"
#         }
#         day_name = russian_weekdays[day_of_week]

#         meal_type_translation = {
#             "breakfast": "Завтрак",
#             "lunch": "Обед",
#             "dinner": "Ужин"
#         }
#         russian_meal_type = meal_type_translation.get(meal_type, meal_type)
#         column_name = f"{day_name}_{russian_meal_type}"

#         conn_visits = create_connection(DATABASE_VISITS)
#         if conn_visits:
#             try:
#                 cursor = conn_visits.cursor()
#                 cursor.execute("SELECT * FROM visits WHERE uid = ?", (uid,))
#                 result = cursor.fetchone()

#                 if result:
#                     cursor.execute(f'''
#                         UPDATE visits
#                         SET {column_name} = 1
#                         WHERE uid = ?
#                     ''', (uid,))
#                 else:
#                     conn_students = create_connection(DATABASE_STUDENTS)
#                     if conn_students:
#                         cursor_students = conn_students.cursor()
#                         cursor_students.execute("SELECT name, student_group FROM students WHERE uid = ?", (uid,))
#                         student_data = cursor_students.fetchone()
#                         name, student_group = student_data if student_data else ("Неизвестный", "Неизвестная группа")
#                         cursor.execute('''
#                             INSERT INTO visits (uid, name, student_group)
#                             VALUES (?, ?, ?)
#                         ''', (uid, name, student_group))
#                         cursor.execute(f'''
#                             UPDATE visits
#                             SET {column_name} = 1
#                             WHERE uid = ?
#                         ''', (uid,))
#                         conn_students.close()

#                 conn_visits.commit()
#                 print(f"UID {uid} обработан для {meal_type} ({russian_meal_type}) в {day_name}.")
#                 show_success_window(root)
#             except Exception as e:
#                 print(f"Ошибка при обработке UID: {e}")
#             finally:
#                 conn_visits.close()
#     else:
#         print("Сейчас не время приёма пищи.")
#         show_no_meal_window(root)

# def read_rfid(root):

#     spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
#     cs_pin = digitalio.DigitalInOut(board.D5)
#     pn532 = PN532_SPI(spi, cs_pin, debug=False)
#     pn532.SAM_configuration()

#     try:
#         while True:
#             print("Поднесите карту к считывателю...")
#             uid = pn532.read_passive_target(timeout=0.5)
#             if uid is not None:
#                 uid_str = "".join([f"{byte:02X}" for byte in uid])
#                 print(f"Считан UID: {uid_str}")
#                 process_uid(uid_str, root, datetime.now())
#             sleep(1)
#     except KeyboardInterrupt:
#         print("Считывание карт остановлено.")

def process_uid(uid):
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
        print("Считывание карт остановлено.")