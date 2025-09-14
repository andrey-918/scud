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
    password_window.transient(root) 
    password_window.grab_set()

    def on_closing():
        password_window.grab_release()
        password_window.destroy()
    
    password_window.protocol("WM_DELETE_WINDOW", on_closing)

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
    user_window.transient(root)
    user_window.grab_set()

    def on_closing():
        user_window.grab_release()
        user_window.destroy()
    
    user_window.protocol("WM_DELETE_WINDOW", on_closing)

    main_frame = tk.Frame(user_window, bg="#f0f0f0")
    main_frame.pack(expand=True, fill='both', padx=20, pady=20)

    button_font = ('Arial', 18)

    # Configure grid for main_frame
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    main_frame.columnconfigure(2, weight=1)
    main_frame.rowconfigure(0, weight=1)
    main_frame.rowconfigure(1, weight=1)
    main_frame.rowconfigure(2, weight=1)

    # Create and grid buttons
    btn_load_db = tk.Button(main_frame, text="Загрузить базу данных",
                            command=lambda: load_database(root),
                            font=button_font, bg="#2196F3", fg="white", relief="flat", activebackground="#1976D2")
    btn_load_db.grid(row=0, column=0, columnspan=3, sticky='nsew', padx=10, pady=10)

    btn_generate_report = tk.Button(main_frame, text="Сформировать отчёт по посещениям",
                                    command=lambda: generate_visits_report_everyday(root),
                                    font=button_font, bg="#2196F3", fg="white", relief="flat", activebackground="#1976D2")
    btn_generate_report.grid(row=1, column=0, columnspan=3, sticky='nsew', padx=10, pady=10)

    btn_analytics = tk.Button(main_frame, text="Сформировать отчёт с аналитикой",
                              command=lambda: generate_analytics_report(root),
                              font=button_font, bg="#2196F3", fg="white", relief="flat", activebackground="#1976D2")
    btn_analytics.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)

    btn_settings = tk.Button(main_frame, text="Настройки",
                             command=lambda: open_settings(root),
                             font=button_font, bg="#2196F3", fg="white", relief="flat", activebackground="#1976D2")
    btn_settings.grid(row=2, column=1, sticky='nsew', padx=10, pady=10)

    btn_exit = tk.Button(main_frame, text="Выход",
                         command=user_window.destroy,
                         font=button_font, bg="#f44336", fg="white", relief="flat", activebackground="#d32f2f")
    btn_exit.grid(row=2, column=2, sticky='nsew', padx=10, pady=10)