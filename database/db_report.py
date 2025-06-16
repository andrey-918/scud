import pandas as pd
from tkinter import messagebox, filedialog
from database.db_init import create_connection
from config.constants import DATABASE_VISITS_REPORT, SHORT_NAMES

def load_visits_report(root):
    file_path = filedialog.askopenfilename(title="Выберите отчет №1", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        try:
            df = pd.read_excel(file_path, engine="openpyxl")
            required_columns = [
                "uid", "name", "student_group",
                "Понедельник_З", "Понедельник_О", "Понедельник_У",
                "Вторник_З", "Вторник_О", "Вторник_У",
                "Среда_З", "Среда_О", "Среда_У",
                "Четверг_З", "Четверг_О", "Четверг_У",
                "Пятница_З", "Пятница_О", "Пятница_У",
                "Суббота_З", "Суббота_О", "Суббота_У"
            ]
            if not all(col in df.columns for col in required_columns):
                raise ValueError("Неверный формат файла отчета №1")
            full_names = {v: k for k, v in SHORT_NAMES.items()}
            df.rename(columns=full_names, inplace=True)
            conn = create_connection(DATABASE_VISITS_REPORT)
            if conn:
                conn.execute("DELETE FROM visits_report")
                df.to_sql('visits_report', conn, if_exists='append', index=False)
                conn.commit()
                messagebox.showinfo("Успех", "Данные отчета успешно загружены!", parent=root)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки отчета: {e}", parent=root)
        finally:
            if conn:
                conn.close()