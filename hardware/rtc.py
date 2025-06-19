import time as time_module
from tkinter import messagebox
import os

from adafruit_ds3231 import DS3231
import busio

def set_rtc_time(year_var, month_var, day_var, hour_var, minute_var, second_var, window):
    try:
        year = int(year_var.get())
        month = int(month_var.get())
        day = int(day_var.get())
        hour = int(hour_var.get())
        minute = int(minute_var.get())
        second = int(second_var.get())

        new_time = time_module.struct_time((year, month, day, hour, minute, second, 0, -1, -1))
        rtc = DS3231(busio.I2C(board.SCL, board.SDA))
        rtc.datetime = new_time
        sync_time_with_ds3231()
        messagebox.showinfo("Успех", "Время успешно установлено!", parent=window)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось установить время: {e}", parent=window)

def sync_time_with_ds3231():
    rtc = DS3231(busio.I2C(board.SCL, board.SDA))
    rtc_time = rtc.datetime
    time_str = f"{rtc_time.tm_year}-{rtc_time.tm_mon}-{rtc_time.tm_mday} {rtc_time.tm_hour}:{rtc_time.tm_min}:{rtc_time.tm_sec}"
    os.system(f"sudo date -s '{time_str}'")
    print("Время синхронизировано с DS3231.")

    pass