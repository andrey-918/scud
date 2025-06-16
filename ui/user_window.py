import tkinter as tk
from tkinter import messagebox
from config.settings import load_settings
from config.constants import DEFAULT_PASSWORD
from database.db_operations import load_database, load_requests_database
from database.db_report import load_visits_report
from reports.report_generator import generate_visits_report, generate_visits_report_everyday, generate_analytics_report
from ui.settings_window import open_settings

def open_user_window(root):
    settings = load_settings()
    correct_password = settings.get("password", DEFAULT_PASSWORD)

    password_window = tk.Toplevel(root)
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
            show_user_window(root)
        else:
            messagebox.showerror("Ошибка", "Неверный пароль", parent=password_window)

    password_entry.bind('<Return>', lambda event: check_password())
    tk.Button(password_frame, text="Войти", command=check_password,
             font=button_font, bg="#2196F3", fg="white").pack(pady=20, ipady=20, fill='x')
    tk.Button(password_frame, text="Выход", command=password_window.destroy,
             font=button_font, bg="#f44336", fg="white").pack(pady=20, ipady=20, fill='x')

def show_user_window(root):
    user_window = tk.Toplevel(root)
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

    tk.Button(top_frame, text="Загрузить базу данных",
             command=lambda: load_database(root),
             font=button_font, bg="#2196F3", fg="white").pack(side='left', expand=True, fill='both', padx=10)
    tk.Button(top_frame, text="Загрузить заявочный файл",
             command=lambda: load_requests_database(root),
             font=button_font, bg="#2196F3", fg="white").pack(side='left', expand=True, fill='both', padx=10)

    tk.Button(middle_frame, text="Отчёт №1",
             command=lambda: generate_visits_report(root=root),
             font=button_font, bg="#2196F3", fg="white").pack(side='left', expand=True, fill='both', padx=10)
    tk.Button(middle_frame, text="Отчёт №1 РГ",
             command=lambda: generate_visits_report_everyday(root),
             font=button_font, bg="#2196F3", fg="white").pack(side='left', expand=True, fill='both', padx=10)

    tk.Button(bottom_frame, text="Отчёт №2",
             command=lambda: generate_analytics_report(root),
             font=button_font, bg="#2196F3", fg="white").pack(side='left', expand=True, fill='both', padx=10)
    tk.Button(bottom_frame, text="Настройки",
             command=lambda: open_settings(root),
             font=button_font, bg="#2196F3", fg="white").pack(side='left', expand=True, fill='both', padx=10)
    tk.Button(bottom_frame, text="Выход",
             command=user_window.destroy,
             font=button_font, bg="#f44336", fg="white").pack(side='left', expand=True, fill='both', padx=10)