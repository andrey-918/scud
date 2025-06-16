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
    password_window.configure(bg="#f0f0f0")

    label_font = ('Arial', 24)
    entry_font = ('Arial', 20)
    button_font = ('Arial', 20)

    password_frame = tk.Frame(password_window, bg="#f0f0f0")
    password_frame.pack(expand=True, fill='both', padx=20, pady=20)

    tk.Label(password_frame, text="Введите пароль:", font=label_font, bg="#f0f0f0").pack(pady=10)
    password_entry = tk.Entry(password_frame, show='*', font=entry_font)
    password_entry.pack(pady=10, ipady=10, fill='x', padx=50)
    password_entry.focus_set()

    def check_password():
        if password_entry.get() == correct_password:
            password_window.destroy()
            show_user_window(root)
        else:
            messagebox.showerror("Ошибка", "Неверный пароль", parent=password_window)

    password_entry.bind('<Return>', lambda event: check_password())
    tk.Button(password_frame, text="Войти", command=check_password,
             font=button_font, bg="#2196F3", fg="white", relief="flat", activebackground="#1976D2").pack(pady=10, fill='x', padx=50)
    tk.Button(password_frame, text="Выход", command=password_window.destroy,
             font=button_font, bg="#f44336", fg="white", relief="flat", activebackground="#d32f2f").pack(pady=10, fill='x', padx=50)

def show_user_window(root):
    user_window = tk.Toplevel(root)
    user_window.title("Управление")
    user_window.attributes('-fullscreen', True)
    user_window.configure(bg="#f0f0f0")

    main_frame = tk.Frame(user_window, bg="#f0f0f0")
    main_frame.pack(expand=True, fill='both', padx=20, pady=20)

    button_font = ('Arial', 18)

    # Use grid layout for better button organization
    top_frame = tk.Frame(main_frame, bg="#f0f0f0")
    top_frame.pack(expand=True, fill='both', pady=10)
    middle_frame = tk.Frame(main_frame, bg="#f0f0f0")
    middle_frame.pack(expand=True, fill='both', pady=10)
    bottom_frame = tk.Frame(main_frame, bg="#f0f0f0")
    bottom_frame.pack(expand=True, fill='both', pady=10)

    tk.Button(top_frame, text="Загрузить базу данных",
             command=lambda: load_database(root),
             font=button_font, bg="#2196F3", fg="white", relief="flat", activebackground="#1976D2").grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    
    tk.Button(middle_frame, text="Сформировать отчёт по посещениям",
             command=lambda: generate_visits_report_everyday(root),
             font=button_font, bg="#2196F3", fg="white", relief="flat", activebackground="#1976D2").grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
    
    tk.Button(bottom_frame, text="Сформировать отчёт с аналитикой",
             command=lambda: generate_analytics_report(root),
             font=button_font, bg="#2196F3", fg="white", relief="flat", activebackground="#1976D2").grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    
    tk.Button(bottom_frame, text="Настройки",
             command=lambda: open_settings(root),
             font=button_font, bg="#2196F3", fg="white", relief="flat", activebackground="#1976D2").grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
    
    tk.Button(bottom_frame, text="Выход",
             command=user_window.destroy,
             font=button_font, bg="#f44336", fg="white", relief="flat", activebackground="#d32f2f").grid(row=0, column=2, sticky='nsew', padx=5, pady=5)

    # Configure grid weights to make buttons expand evenly
    top_frame.columnconfigure((0, 1), weight=1)
    middle_frame.columnconfigure((0, 1), weight=1)
    bottom_frame.columnconfigure((0, 1, 2), weight=1)