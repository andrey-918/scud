import threading
from database.db_init import create_tables
from ui.main_window import create_main_window
from utils.time_utils import check_and_generate_report
from hardware.rfid_reader import read_rfid
from config.constants import disable_ntp

def main():
    create_tables()  # Initialize database tables
    disable_ntp()    # Disable NTP for time synchronization

    # Create the main application window
    root = create_main_window()

    # Start RFID reading in a background thread (if hardware is enabled)
    rfid_thread = threading.Thread(target=read_rfid, daemon=True)
    rfid_thread.start()

    # Schedule periodic report generation
    check_and_generate_report(root)

    root.mainloop()

if __name__ == "__main__":
    main()