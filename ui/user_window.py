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

    # Single main frame for all buttons
    main_frame = tk.Frame(user_window, bg="#f0f0f0")
    main_frame.pack(expand=True, fill='both', padx=50, pady=50)  # Increased padding for better spacing

    button_font = ('Arial', 18, 'bold')  # Bold font for better readability

    # Configure grid with 2 columns: one for buttons, one empty for centering
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure((0, 1, 2, 3, 4), weight=1)  # Equal weight for all rows

    # Button styling parameters
    button_style = {
        "font": button_font,
        "fg": "white",
        "relief": "raised",  # Subtle raised effect for depth
        "bd": 3,  # Border width
        "ipadx": 20,  # Internal padding for consistent width
        "ipady": 10,  # Internal padding for consistent height
    }

    # Hover effect functions
    def on_enter(event, button, hover_bg):
        button.config(bg=hover_bg)

    def on_leave(event, button, original_bg):
        button.config(bg=original_bg)

    # Create buttons with consistent styling
    buttons = [
        ("Загрузить базу данных", lambda: load_database(root), "#2196F3", "#1976D2"),
        ("Сформировать отчёт по посещениям", lambda: generate_visits_report_everyday(root), "#2196F3", "#1976D2"),
        ("Сформировать отчёт с аналитикой", lambda: generate_analytics_report(root), "#2196F3", "#1976D2"),
        ("Настройки", lambda: open_settings(root), "#2196F3", "#1976D2"),
        ("Выход", user_window.destroy, "#f44336", "#d32f2f"),
    ]

    for row, (text, command, bg, hover_bg) in enumerate(buttons):
        btn = tk.Button(main_frame, text=text, command=command, bg=bg, activebackground=hover_bg, **button_style)
        btn.grid(row=row, column=0, sticky='ew', padx=20, pady=15)  # Increased padding
        # Bind hover effects
        btn.bind("<Enter>", lambda e, b=btn, h=hover_bg: on_enter(e, b, h))
        btn.bind("<Leave>", lambda e, b=btn, o=bg: on_leave(e, b, o))

    # Add empty label in column 1 to balance the grid
    tk.Label(main_frame, text="", bg="#f0f0f0").grid(row=0, column=1, sticky='ew')