import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from datetime import datetime
from settings import load_settings, save_settings
from database import load_database, load_requests_database, load_visits_report
from reports import generate_visits_report, generate_analytics_report
import time as time_module

def show_success_window():
    success_window = tk.Toplevel()
    success_window.title("Успешно")
    success_window.attributes('-fullscreen', True)
    tk.Label(success_window, text="Успешно!", font=("Arial", 48), bg="green", fg="white").pack(expand=True, fill='both')
    success_window.after(3000, success_window.destroy)

def show_no_meal_window():
    no_meal_window = tk.Toplevel()
    no_meal_window.title("Сейчас не время приёма пищи")
    no_meal_window.attributes('-fullscreen', True)
    tk.Label(no_meal_window, text="Сейчас не время приёма пищи", font=("Arial", 36), bg="red", fg="white").pack(expand=True, fill='both')
    no_meal_window.after(3000, no_meal_window.destroy)

def open_settings():
    settings_window = tk.Toplevel()
    settings_window.title("Настройки")
    settings_window.attributes('-fullscreen', True)
    settings = load_settings()
    content_frame = tk.Frame(settings_window)
    content_frame.pack(expand=True, fill='both', padx=20, pady=20)
    title_font = ('Arial', 36)
    label_font = ('Arial', 28)
    time_font = ('Arial', 28)
    button_font = ('Arial', 32)

    def create_time_section(parent, meal_name, meal_data):
        meal_frame = tk.Frame(parent)
        meal_frame.pack(fill='x', pady=10)
        tk.Label(meal_frame, text=meal_name.capitalize() + ":", font=title_font).pack(anchor='w', pady=5)
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

    time_vars = {
        'breakfast': create_time_section(content_frame, "Завтрак", settings['breakfast']),
        'lunch': create_time_section(content_frame, "Обед", settings['lunch']),
        'dinner': create_time_section(content_frame, "Ужин", settings['dinner'])
    }
    tk.Frame(content_frame, height=2, bg='gray').pack(fill='x', pady=20)
    tk.Label(content_frame, text="Минимальный процент посещений:", font=label_font).pack(anchor='w', pady=5)
    min_percent_entry = tk.Entry(content_frame, font=time_font)
    min_percent_entry.insert(0, str(settings.get("min_percent", 65)))
    min_percent_entry.pack(fill='x', padx=20, pady=5)
    tk.Label(content_frame, text="Новый пароль:", font=label_font).pack(anchor='w', pady=5)
    new_password_entry = tk.Entry(content_frame, font=time_font, show='*')
    new_password_entry.pack(fill='x', padx=20, pady=5)
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
    tk.Button(button_frame, text="Выход", command=settings_window.destroy, 
             font=button_font, bg="#f44336", fg="white").pack(fill='x', pady=5)

def open_rtc_time_setting():
    rtc_window = tk.Toplevel()
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
            # rtc.datetime = new_time
            # sync_time_with_ds3231()
            messagebox.showinfo("Успех", "Время успешно установлено!", parent=rtc_window)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось установить время: {e}", parent=rtc_window)

    tk.Button(button_frame, text="Установить время", command=set_time,
             font=button_font, bg="#2196F3", fg="white").pack(fill='x', pady=5)
    tk.Button(button_frame, text="Выход", command=rtc_window.destroy,
             font=button_font, bg="#f44336", fg="white").pack(fill='x', pady=5)

def open_user_window():
    settings = load_settings()
    correct_password = settings.get("password", "1111")
    password_window = tk.Toplevel()
    password_window.title("Ввод пароля")
    password_window.attributes('-fullscreen', True)
    label_font = ('Arial', 36)
    entry_font = ('Arial', 36)
    button_font = ('Arial', 36)
    password_frame = tk.Frame(password_window)
    password_frame.pack(expand=True, fill='both', padx=50, pady=50)
    tk.Label(password_frame, text="Введите пароль:", font=label_font).pack(pady=20)
    password_entry = tk.Entry(password_frame, show='*', font=entry_font)
    password_entry.pack(pady=20, ipady=20)
    password_entry.focus_set()

    def check_password():
        if password_entry.get() == correct_password:
            password_window.destroy()
            show_user_window()
        else:
            messagebox.showerror("Ошибка", "Неверный пароль", parent=password_window)

    password_entry.bind('<Return>', lambda event: check_password())
    tk.Button(password_frame, text="Войти", command=check_password, 
             font=button_font, bg="#2196F3", fg="white").pack(pady=20, ipady=20, fill='x')
    tk.Button(password_frame, text="Выход", command=password_window.destroy, 
             font=button_font, bg="#f44336", fg="white").pack(pady=20, ipady=20, fill='x')

def show_user_window():
    user_window = tk.Toplevel()
    user_window.title("Управление")
    user_window.attributes('-fullscreen', True)
    main_frame = tk.Frame(user_window)
    main_frame.pack(expand=True, fill='both', padx=50, pady=50)
    button_font = ('Arial', 42)
    top_frame = tk.Frame(main_frame)
    top_frame.pack(expand=True, fill='both', pady=20)
    middle_frame = tk.Frame(main_frame)
    middle_frame.pack(expand=True, fill='both', pady=20)
    bottom_frame = tk.Frame(main_frame)
    bottom_frame.pack(expand=True, fill='both', pady=20)
    tk.Button(top_frame, text="Загрузить базу данных", command=lambda: load_database(filedialog.askopenfilename(title="Выберите файл базы данных", filetypes=[("Excel files", "*.xlsx")])), 
             font=button_font, bg="#2196F3", fg="white").pack(expand=True, fill='both', pady=10)
    tk.Button(top_frame, text="Сформировать отчёт по посещениям", command=generate_visits_report, 
             font=button_font, bg="#2196F3", fg="white").pack(expand=True, fill='both', pady=10)
    tk.Button(middle_frame, text="Сформировать отчёт с аналитикой", command=generate_analytics_report, 
             font=button_font, bg="#2196F3", fg="white").pack(expand=True, fill='both', pady=10)
    tk.Button(middle_frame, text="Настройки", command=open_settings, 
             font=button_font, bg="#2196F3", fg="white").pack(expand=True, fill='both', pady=10)
    tk.Button(bottom_frame, text="Выход", command=user_window.destroy, 
             font=button_font, bg="#f44336", fg="white").pack(expand=True, fill='both', pady=10)

def update_time_date(label):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%d.%m.%Y")
    label.config(text=f"{current_time}\n{current_date}")
    label.after(1000, update_time_date, label)