import tkinter as tk
from tkinter import messagebox, ttk
from config.settings import load_settings, save_settings
from config.constants import DEFAULT_MIN_PERCENT
from ui.widgets import create_time_combobox
from ui.time_window import open_rtc_time_setting

def open_settings(root):
    settings_window = tk.Toplevel(root)
    settings_window.title("Настройки")
    settings_window.attributes('-fullscreen', True)
    settings_window.configure(bg="#f0f0f0")
    settings_window.transient(root) 
    settings_window.grab_set()

    def on_closing():
        settings_window.grab_release()
        settings_window.destroy()
    
    settings_window.protocol("WM_DELETE_WINDOW", on_closing)

    # Create a canvas with a scrollbar
    canvas = tk.Canvas(settings_window, bg="#f0f0f0", highlightthickness=0)
    scrollbar = ttk.Scrollbar(settings_window, orient="vertical", command=canvas.yview)
    content_frame = tk.Frame(canvas, bg="#f0f0f0")

    content_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=content_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Place canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scrollbar.pack(side="right", fill="y")

    title_font = ('Arial', 20)
    label_font = ('Arial', 16)
    time_font = ('Arial', 16)
    button_font = ('Arial', 16)

    settings = load_settings()
    time_vars = {}

    def create_time_section(parent, meal_name, meal_data, row):
        tk.Label(parent, text=meal_name.capitalize() + ":", font=title_font, bg="#f0f0f0").grid(row=row, column=0, sticky='w', pady=5)

        tk.Label(parent, text="Начало:", font=label_font, bg="#f0f0f0").grid(row=row+1, column=0, sticky='w', padx=10)
        start_frame = tk.Frame(parent, bg="#f0f0f0")
        start_frame.grid(row=row+1, column=1, sticky='ew', padx=5)
        hour_var = create_time_combobox(start_frame, meal_data['start'][0], 24)
        tk.Label(start_frame, text=":", font=label_font, bg="#f0f0f0").pack(side='left')
        minute_var = create_time_combobox(start_frame, meal_data['start'][1], 60)

        tk.Label(parent, text="Окончание:", font=label_font, bg="#f0f0f0").grid(row=row+2, column=0, sticky='w', padx=10)
        end_frame = tk.Frame(parent, bg="#f0f0f0")
        end_frame.grid(row=row+2, column=1, sticky='ew', padx=5)
        end_hour_var = create_time_combobox(end_frame, meal_data['end'][0], 24)
        tk.Label(end_frame, text=":", font=label_font, bg="#f0f0f0").pack(side='left')
        end_minute_var = create_time_combobox(end_frame, meal_data['end'][1], 60)

        return {
            'start': (hour_var, minute_var),
            'end': (end_hour_var, end_minute_var)
        }

    # Create time sections for breakfast, lunch, dinner
    row = 0
    for meal in ['breakfast', 'lunch', 'dinner']:
        time_vars[meal] = create_time_section(content_frame, meal, settings[meal], row)
        row += 3
        tk.Frame(content_frame, height=2, bg='gray').grid(row=row, column=0, columnspan=2, sticky='ew', pady=5)
        row += 1

    # Minimum percent section
    tk.Label(content_frame, text="Минимальный % посещений:", font=label_font, bg="#f0f0f0").grid(row=row, column=0, sticky='w', pady=5, padx=10)
    min_percent_entry = tk.Entry(content_frame, font=time_font)
    min_percent_entry.insert(0, str(settings.get("min_percent", DEFAULT_MIN_PERCENT)))
    min_percent_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
    row += 1

    # Password section
    tk.Label(content_frame, text="Новый пароль:", font=label_font, bg="#f0f0f0").grid(row=row, column=0, sticky='w', pady=5, padx=10)
    new_password_entry = tk.Entry(content_frame, font=time_font, show='*')
    new_password_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
    row += 1

    # Separator
    tk.Frame(content_frame, height=2, bg='gray').grid(row=row, column=0, columnspan=2, sticky='ew', pady=5)
    row += 1

    # Buttons
    button_frame = tk.Frame(content_frame, bg="#f0f0f0")
    button_frame.grid(row=row, column=0, columnspan=2, sticky='ew', pady=5)

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
             font=button_font, bg="#2196F3", fg="white", relief="flat", activebackground="#1976D2").pack(fill='x', pady=3, padx=5)
    tk.Button(button_frame, text="Сохранить", command=save_settings_handler,
             font=button_font, bg="#2196F3", fg="white", relief="flat", activebackground="#1976D2").pack(fill='x', pady=3, padx=5)
    tk.Button(button_frame, text="Выход", command=settings_window.destroy,
             font=button_font, bg="#f44336", fg="white", relief="flat", activebackground="#d32f2f").pack(fill='x', pady=3, padx=5)

    # Configure grid weights
    content_frame.columnconfigure(1, weight=1)