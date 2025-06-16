import os
from datetime import datetime, timedelta

def delete_old_reports(folder_path, days_old=30):
    try:
        current_time = datetime.now()
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) and filename.endswith(".xlsx"):
                file_creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
                if current_time - file_creation_time > timedelta(days=days_old):
                    os.remove(file_path)
                    print(f"Удалён файл: {filename}")
    except Exception as e:
        print(f"Ошибка при удалении старых файлов: {e}")