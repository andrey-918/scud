import os
import threading
from database import create_tables
from gui import main
from reports import check_and_generate_report
from rfid import read_rfid
from utils import disable_ntp
from config import REPORTS_FOLDER

if not os.path.exists(REPORTS_FOLDER):
    os.makedirs(REPORTS_FOLDER)

report_generated = False

if __name__ == "__main__":
    create_tables()
    disable_ntp()
    rfid_thread = threading.Thread(target=read_rfid, daemon=True)
    rfid_thread.start()
    check_and_generate_report()
    main()