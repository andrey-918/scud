import tkinter as tk
from ui.user_window import open_user_window
from utils.time_utils import update_time_date

def create_main_window():
    root = tk.Tk()
    root.title("Учёт льготного питания")
    root.attributes('-fullscreen', True)

    time_date_label = tk.Label(root, font=("Arial", 48), fg="black")
    time_date_label.pack(expand=True, fill='both', pady=50)
    update_time_date(time_date_label, root)

    tk.Button(
        root,
        text="Пользователь",
        command=lambda: open_user_window(root),
        font=("Arial", 36),
        bg="#2196F3",
        fg="white",
        height=3
    ).pack(expand=True, fill='both', padx=100, pady=50)

    return root