import board
import busio
import digitalio
from adafruit_pn532.spi import PN532_SPI
from adafruit_ds3231 import DS3231
from time import sleep
from datetime import datetime
from config import *
from database import create_connection
from time_utils import get_meal_type
from gui import show_success_window, show_no_meal_window

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = digitalio.DigitalInOut(board.D5)
pn532 = PN532_SPI(spi, cs_pin, debug=False)
pn532.SAM_configuration()

i2c = busio.I2C(board.SCL, board.SDA)
rtc = DS3231(i2c)

def process_uid(uid):
    current_time = rtc.datetime
    meal_type = get_meal_type(current_time)
    if meal_type:
        year = current_time.tm_year
        month = current_time.tm_mon
        day = current_time.tm_mday
        date_obj = datetime(year, month, day)
        day_of_week = date_obj.weekday()
        russian_weekdays = {
            0: "Понедельник",
            1: "Вторник",
            2: "Среда",
            3: "Четверг",
            4: "Пятница",
            5: "Суббота",
            6: "Воскресенье"
        }
        day_name = russian_weekdays[day_of_week]
        meal_type_translation = {
            "breakfast": "Завтрак",
            "lunch": "Обед",
            "dinner": "Ужин"
        }
        russian_meal_type = meal_type_translation.get(meal_type, meal_type)
        column_name = f"{day_name}_{russian_meal_type}"
        conn_visits = create_connection(DATABASE_VISITS)
        if conn_visits is not None:
            try:
                cursor = conn_visits.cursor()
                cursor.execute("SELECT * FROM visits WHERE uid = ?", (uid,))
                result = cursor.fetchone()
                if result:
                    cursor.execute(f'''
                        UPDATE visits
                        SET {column_name} = 1
                        WHERE uid = ?
                    ''', (uid,))
                else:
                    conn_students = create_connection(DATABASE_STUDENTS)
                    if conn_students is not None:
                        cursor_students = conn_students.cursor()
                        cursor_students.execute("SELECT name, student_group FROM students WHERE uid = ?", (uid,))
                        student_data = cursor_students.fetchone()
                        if student_data:
                            name, student_group = student_data
                        else:
                            name, student_group = "Неизвестный", "Неизвестная группа"
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
                show_success_window()
            except Exception as e:
                print(f"Ошибка при обработке UID: {e}")
            finally:
                conn_visits.close()
    else:
        print("Сейчас не время приёма пищи.")
        show_no_meal_window()

def read_rfid():
    try:
        while True:
            print("Поднесите карту к считывателю...")
            uid = pn532.read_passive_target(timeout=0.5)
            if uid is not None:
                uid_str = "".join([f"{byte:02X}" for byte in uid])
                print(f"Считан UID: {uid_str}")
                process_uid(uid_str)
            sleep(1)
    except KeyboardInterrupt:
        print("Считывание карт остановлено.")