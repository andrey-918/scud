import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import time as time_module
from hardware.rtc import set_rtc_time

def open_rtc_time_setting(root):
    rtc_window = tk.Toplevel(root)
    rtc_window.title("Настройка времени на DS3231")
    rtc_window.attributes('-fullscreen', True)

    content_frame = tk.Frame(rtc_window)
    content_frame.pack(expand=True, fill='both', padx=20, pady=20)

    label_font = ('Arial', 32)
    time_font = ('Arial', 32)
    button_font = ('Arial', 32)

    current_time = datetime.now()

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

    button_frame = tk.Frame(content_frame)
    button_frame.pack(fill='x', pady=20)

    def set_time():
        set_rtc_time(year_var, month_var, day_var, hour_var, minute_var, second_var, rtc_window)

    tk.Button(button_frame, text="Установить время", command=set_time,
             font=button_font, bg="#2196F3", fg="white").pack(fill='x', pady=5)
    tk.Button(button_frame, text="Выход", command=rtc_window.destroy,
             font=button_font, bg="#f44336", fg="white").pack(fill='x', pady=5)