import tkinter as tk
from tkinter import messagebox, ttk
from database import *
from reports import *
from settings import *
from utils import *
from config import *

def show_success_window():
    success_window = tk.Toplevel(root)
    success_window.title("Успешно")
    success_window.attributes('-fullscreen', True)
    tk.Label(success_window, text="Успешно!", font=("Arial", 48), bg="green", fg="white").pack(expand=True, fill='both')
    success_window.after(3000, success_window.destroy)

def show_no_meal_window():
    no_meal_window = tk.Toplevel(root)
    no_meal_window.title("Сейчас не время приёма пищи")
    no_meal_window.attributes('-fullscreen', True)
    tk.Label(no_meal_window, text="Сейчас не время приёма пищи", font=("Arial", 36), bg="red", fg="white").pack(expand=True, fill='both')
    no_meal_window.after(3000, no_meal_window.destroy)

def update_time_date(label):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%d.%m.%Y")
    label.config(text=f"{current_time}\n{current_date}")
    root.after(1000, update_time_date, label)

def open_user_window():
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
            show_user_window()
        else:
            messagebox.showerror("Ошибка", "Неверный пароль", parent=password_window)

    password_entry.bind('<Return>', lambda event: check_password())
    tk.Button(password_frame, text="Войти", command=check_password, 
             font=button_font, bg="#2196F3", fg="white").pack(pady=20, ipady=20, fill='x')
    tk.Button(password_frame, text="Выход", command=password_window.destroy, 
             font=button_font, bg="#f44336", fg="white").pack(pady=20, ipady=20, fill='x')

def show_user_window():
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
    tk.Button(top_frame, text="Загрузить базу данных", command=load_database, 
             font=button_font, bg="#2196F3", fg="white").pack(expand=True, fill='both', pady=10)
    tk.Button(top_frame, text="Сформировать отчёт по посещениям", command=generate_visits_report_everyday, 
             font=button_font, bg="#2196F3", fg="white").pack(expand=True, fill='both', pady=10)
    tk.Button(middle_frame, text="Сформировать отчёт с аналитикой", command=generate_analytics_report, 
             font=button_font, bg="#2196F3", fg="white").pack(expand=True, fill='both', pady=10)
    tk.Button(middle_frame, text="Настройки", command=open_settings, 
             font=button_font, bg="#2196F3", fg="white").pack(expand=True, fill='both', pady=10)
    tk.Button(bottom_frame, text="Выход", command=user_window.destroy, 
             font=button_font, bg="#f44336", fg="white").pack(expand=True, fill='both', pady=10)

def main():
    global root
    root = tk.Tk()
    root.title("Учёт льготного питания")
    root.attributes('-fullscreen', True)
    time_date_label = tk.Label(root, font=("Arial", 48), fg="black")
    time_date_label.pack(expand=True, fill='both', pady=50)
    update_time_date(time_date_label)
    tk.Button(
        root, 
        text="Пользователь", 
        command=open_user_window, 
        font=("Arial", 36),
        bg="#2196F3",
        fg="white",
        height=3
    ).pack(expand=True, fill='both', padx=100, pady=50)
    root.mainloop()