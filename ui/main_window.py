import tkinter as tk
from ui.user_window import open_user_window
from utils.time_utils import update_time_date

def create_main_window():
    root = tk.Tk()
    root.title("Учёт льготного питания")
    root.attributes('-fullscreen', True)
    root.configure(bg="#f0f0f0")  # Light gray background for better contrast

    time_date_label = tk.Label(root, font=("Arial", 32), fg="black", bg="#f0f0f0")
    time_date_label.pack(expand=True, fill='both', pady=20)
    update_time_date(time_date_label, root)

    tk.Button(
        root,
        text="Пользователь",
        command=lambda: open_user_window(root),
        font=("Arial", 24),
        bg="#2196F3",
        fg="white",
        height=2,
        relief="flat",
        activebackground="#1976D2"
    ).pack(expand=True, fill='x', padx=50, pady=20)

    return root