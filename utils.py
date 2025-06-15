from datetime import datetime, timedelta
import os
from config import *

def delete_old_reports(folder_path, days_old=30):
    try:
        current_time = datetime.now()
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) and filename.endswith(".xlsx"):
                file_creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
                time_difference = current_time - file_creation_time
                if time_difference > timedelta(days=days_old):
                    os.remove(file_path)
                    print(f"Удалён файл: {filename}")
    except Exception as e:
        print(f"Ошибка при удалении старых файлов: {e}")

def disable_ntp():
    print("Отключаем NTP...")
    os.system("sudo timedatectl set-ntp false")
    sleep(1)