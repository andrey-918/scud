import threading
from ui import *
from database import *
from settings import *
from reports import *
from utils import *
from hardware import read_rfid  # Uncomment if needed

def main():
    create_tables()
    # disable_ntp()
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
    # Uncomment the following line to start RFID reading
    # rfid_thread = threading.Thread(target=read_rfid, daemon=True)
    # rfid_thread.start()
    check_and_generate_report()
    root.mainloop()

if __name__ == "__main__":
    main()