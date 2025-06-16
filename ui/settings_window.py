import tkinter as tk
from tkinter import messagebox
from config.settings import load_settings, save_settings
from config.constants import DEFAULT_MIN_PERCENT
from ui.widgets import create_time_combobox
from ui.time_window import open_rtc_time_setting

def open_settings(root):
    settings_window = tk.Toplevel(root)
    settings_window.title("Настройки")
    settings_window.attributes('-fullscreen', True)

    content_frame = tk.Frame(settings_window)
    content_frame.pack(expand=True, fill='both', padx=20, pady=20)

    title_font = ('Arial', 36)
    label_font = ('Arial', 28)
    time_font = ('Arial', 28)
    button_font = ('Arial', 32)

    settings = load_settings()
    time_vars = {}

    def create_time_section(parent, meal_name, meal_data):
        meal_frame = tk.Frame(parent)
        meal_frame.pack(fill='x', pady=10)
        tk.Label(meal_frame, text=meal_name.capitalize() + ":", font=title_font).pack(anchor='w', pady=5)
        
        start_frame = tk.Frame(meal_frame)
        start_frame.pack(fill='x', padx=10, pady=5)
        tk.Label(start_frame, text="Начало:", font=label_font).pack(side='left', padx=5)
        hour_var = create_time_combobox(start_frame, meal_data['start'][0], 24)
        tk.Label(start_frame, text=":", font=label_font).pack(side='left')
        minute_var = create_time_combobox(start_frame, meal_data['start'][1], 60)
        
        end_frame = tk.Frame(meal_frame)
        end_frame.pack(fill='x', padx=10, pady=5)
        tk.Label(end_frame, text="Окончание:", font=label_font).pack(side='left', padx=5)
        end_hour_var = create_time_combobox(end_frame, meal_data['end'][0], 24)
        tk.Label(end_frame, text=":", font=label_font).pack(side='left')
        end_minute_var = create_time_combobox(end_frame, meal_data['end'][1], 60)
        
        return {
            'start': (hour_var, minute_var),
            'end': (end_hour_var, end_minute_var)
        }

    for meal in ['breakfast', 'lunch', 'dinner']:
        time_vars[meal] = create_time_section(content_frame, meal, settings[meal])

    tk.Frame(content_frame, height=2, bg='gray').pack(fill='x', pady=20)

    tk.Label(content_frame, text="Минимальный процент посещений:", font=label_font).pack(anchor='w', pady=5)
    min_percent_entry = tk.Entry(content_frame, font=time_font)
    min_percent_entry.insert(0, str(settings.get("min_percent", DEFAULT_MIN_PERCENT)))
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
             command=lambda: open_rtc_time_setting(root),
             font=button_font, bg="#2196F3", fg="white").pack(fill='x', pady=5)
    tk.Button(button_frame, text="Сохранить", command=save_settings_handler,
             font=button_font, bg="#2196F3", fg="white").pack(fill='x', pady=5)
    tk.Button(button_frame, text="Выход", command=settings_window.destroy,
             font=button_font, bg="#f44336", fg="white").pack(fill='x', pady=5)
