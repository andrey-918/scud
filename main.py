import tkinter as tk #hfiuewh
import threading
from database import create_tables
from gui import update_time_date, open_user_window
from rfid import read_rfid
from utils import check_and_generate_report

def main():
    create_tables()
    root = tk.Tk()
    root.title("Учёт льготного питания")
    root.attributes('-fullscreen', True)

    time_date_label = tk.Label(root, font=("Arial", 48), fg="black")
    time_date_label.pack(expand=True, fill='both', pady=50)
    update_time_date(time_date_label)

    tk.Button(root, text="Пользователь", command=lambda: open_user_window(root), 
             font=("Arial", 36), bg="#2196F3", fg="white", height=3).pack(expand=True, fill='both', padx=100, pady=50)

    rfid_thread = threading.Thread(target=read_rfid, args=(root,), daemon=True)
    rfid_thread.start()

    check_and_generate_report()

    root.mainloop()

if __name__ == "__main__":
    main()