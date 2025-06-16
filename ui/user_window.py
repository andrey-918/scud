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
    password_window.update()  # Ensure window is rendered before adding widgets

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
    user_window.update()  # Force window update to apply fullscreen
    print("User window created with fullscreen attribute")  # Debug

    # Fallback geometry if fullscreen fails
    try:
        user_window.geometry("800x480")  # Common Raspberry Pi resolution
    except tk.TclError as e:
        print(f"Geometry error: {e}")

    main_frame = tk.Frame(user_window, bg="#f0f0f0")
    main_frame.pack(expand=True, fill='both', padx=100, pady=100)  # Increased padding
    print("Main frame packed")  # Debug

    button_font = ('Arial', 18, 'bold')  # Bold for readability

    # Button styling
    button_style = {
        "font": button_font,
        "fg": "white",
        "relief": "raised",
        "bd": 3,
        "ipadx": 30,  # Increased for wider buttons
        "ipady": 15,  # Increased for taller buttons
    }

    # Hover effects
    def on_enter(event, button, hover_bg):
        button.config(bg=hover_bg)

    def on_leave(event, button, original_bg):
        button.config(bg=original_bg)

    # Buttons
    buttons = [
        ("Загрузить базу данных", lambda: load_database(root), "#2196F3", "#1976D2"),
        ("Сформировать отчёт по посещениям", lambda: generate_visits_report_everyday(root), "#2196F3", "#1976D2"),
        ("Сформировать отчёт с аналитикой", lambda: generate_analytics_report(root), "#2196F3", "#1976D2"),
        ("Настройки", lambda: open_settings(root), "#2196F3", "#1976D2"),
        ("Выход", user_window.destroy, "#f44336", "#d32f2f"),
    ]

    for idx, (text, command, bg, hover_bg) in enumerate(buttons):
        btn = tk.Button(main_frame, text=text, command=command, bg=bg, activebackground=hover_bg, **button_style)
        btn.pack(fill='x', padx=20, pady=20)  # Vertical stacking with generous padding
        btn.bind("<Enter>", lambda e, b=btn, h=hover_bg: on_enter(e, b, h))
        btn.bind("<Leave>", lambda e, b=btn, o=bg: on_leave(e, b, o))
        print(f"Button '{text}' added at index {idx}")  # Debug

    # Ensure frame is visible
    main_frame.update()
    print("Main frame updated")  # Debug