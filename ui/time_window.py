import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import time as time_module
from hardware.rtc import set_rtc_time

def open_rtc_time_setting(root):
    rtc_window = tk.Toplevel(root)
    rtc_window.title("Настройка времени на DS3231")
    rtc_window.attributes('-fullscreen', True)
    rtc_window.configure(bg="#f0f0f0")
    rtc_window.transient(root)
    rtc_window.grab_set() 

    def on_closing():
        rtc_window.grab_release()
        rtc_window.destroy()
    
    rtc_window.protocol("WM_DELETE_WINDOW", on_closing)

    content_frame = tk.Frame(rtc_window, bg="#f0f0f0")
    content_frame.pack(expand=True, fill='both', padx=10, pady=10)

    label_font = ('Arial', 18)
    time_font = ('Arial', 18)
    button_font = ('Arial', 18)

    current_time = datetime.now()

    tk.Label(content_frame, text="Год (YYYY):", font=label_font, bg="#f0f0f0").pack(anchor='w', pady=3)
    year_var = tk.StringVar(value=str(current_time.year))
    ttk.Combobox(content_frame, textvariable=year_var,
                values=[str(i) for i in range(2000, 2100)],
                font=time_font, state='readonly').pack(fill='x', padx=10, pady=3)

    tk.Label(content_frame, text="Месяц (MM):", font=label_font, bg="#f0f0f0").pack(anchor='w', pady=3)
    month_var = tk.StringVar(value=str(current_time.month).zfill(2))
    ttk.Combobox(content_frame, textvariable=month_var,
                values=[str(i).zfill(2) for i in range(1, 13)],
                font=time_font, state='readonly').pack(fill='x', padx=10, pady=3)

    tk.Label(content_frame, text="День (DD):", font=label_font, bg="#f0f0f0").pack(anchor='w', pady=3)
    day_var = tk.StringVar(value=str(current_time.day).zfill(2))
    ttk.Combobox(content_frame, textvariable=day_var,
                values=[str(i).zfill(2) for i in range(1, 32)],
                font=time_font, state='readonly').pack(fill='x', padx=10, pady=3)

    tk.Label(content_frame, text="Час (HH):", font=label_font, bg="#f0f0f0").pack(anchor='w', pady=3)
    hour_var = tk.StringVar(value=str(current_time.hour).zfill(2))
    ttk.Combobox(content_frame, textvariable=hour_var,
                values=[str(i).zfill(2) for i in range(24)],
                font=time_font, state='readonly').pack(fill='x', padx=10, pady=3)

    tk.Label(content_frame, text="Минуты (MM):", font=label_font, bg="#f0f0f0").pack(anchor='w', pady=3)
    minute_var = tk.StringVar(value=str(current_time.minute).zfill(2))
    ttk.Combobox(content_frame, textvariable=minute_var,
                values=[str(i).zfill(2) for i in range(60)],
                font=time_font, state='readonly').pack(fill='x', padx=10, pady=3)

    tk.Label(content_frame, text="Секунды (SS):", font=label_font, bg="#f0f0f0").pack(anchor='w', pady=3)
    second_var = tk.StringVar(value=str(current_time.second).zfill(2))
    ttk.Combobox(content_frame, textvariable=second_var,
                values=[str(i).zfill(2) for i in range(60)],
                font=time_font, state='readonly').pack(fill='x', padx=10, pady=3)

    button_frame = tk.Frame(content_frame, bg="#f0f0f0")
    button_frame.pack(fill='x', pady=10)

    def set_time():
        set_rtc_time(year_var, month_var, day_var, hour_var, minute_var, second_var, rtc_window)

    tk.Button(button_frame, text="Установить время", command=set_time,
             font=button_font, bg="#2196F3", fg="white", relief="flat", activebackground="#1976D2").pack(fill='x', pady=3)
    tk.Button(button_frame, text="Выход", command=rtc_window.destroy,
             font=button_font, bg="#f44336", fg="white", relief="flat", activebackground="#d32f2f").pack(fill='x', pady=3)