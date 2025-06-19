import threading
import queue
from database.db_init import create_tables
from ui.main_window import create_main_window
from utils.time_utils import check_and_generate_report
from hardware.rfid_reader import read_rfid, show_success_window, show_no_meal_window
from config.constants import disable_ntp

def main():
    create_tables()  # Initialize database tables
    disable_ntp()    # Disable NTP for time synchronization

    # Create the main application window
    root = create_main_window()

    # Create a queue for thread-safe communication
    message_queue = queue.Queue()

    # Start RFID reading in a background thread
    rfid_thread = threading.Thread(target=read_rfid, args=(root, message_queue), daemon=True)
    rfid_thread.start()

    # Function to process the queue and update GUI safely
    def process_queue(root):
        try:
            while True:
                message, window_root = message_queue.get_nowait()
                if message == "show_success":
                    show_success_window(window_root)
                elif message == "show_no_meal":
                    show_no_meal_window(window_root)
        except queue.Empty:
            pass
        root.after(100, lambda: process_queue(root))

    # Start processing the queue
    process_queue(root)

    # Schedule periodic report generation
    check_and_generate_report(root)

    root.mainloop()

if __name__ == "__main__":
    main()