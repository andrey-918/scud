import sqlite3
import pandas as pd
from tkinter import messagebox, filedialog
from config import *

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")
    return conn

def create_tables():
    conn_students = create_connection(DATABASE_STUDENTS)
    if conn_students is not None:
        conn_students.execute('''
            CREATE TABLE IF NOT EXISTS students (
                uid TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                student_group TEXT NOT NULL
            );
        ''')
        conn_students.close()

    conn_visits = create_connection(DATABASE_VISITS)
    if conn_visits is not None:
        conn_visits.execute('''
            CREATE TABLE IF NOT EXISTS visits (
                uid TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                student_group TEXT NOT NULL,
                Понедельник_Завтрак INTEGER DEFAULT 0,
                Понедельник_Обед INTEGER DEFAULT 0,
                Понедельник_Ужин INTEGER DEFAULT 0,
                Вторник_Завтрак INTEGER DEFAULT 0,
                Вторник_Обед INTEGER DEFAULT 0,
                Вторник_Ужин INTEGER DEFAULT 0,
                Среда_Завтрак INTEGER DEFAULT 0,
                Среда_Обед INTEGER DEFAULT 0,
                Среда_Ужин INTEGER DEFAULT 0,
                Четверг_Завтрак INTEGER DEFAULT 0,
                Четверг_Обед INTEGER DEFAULT 0,
                Четверг_Ужин INTEGER DEFAULT 0,
                Пятница_Завтрак INTEGER DEFAULT 0,
                Пятница_Обед INTEGER DEFAULT 0,
                Пятница_Ужин INTEGER DEFAULT 0,
                Суббота_Завтрак INTEGER DEFAULT 0,
                Суббота_Обед INTEGER DEFAULT 0,
                Суббота_Ужин INTEGER DEFAULT 0
            );
        ''')
        conn_visits.close()

    conn_requests = create_connection(DATABASE_REQUESTS)
    if conn_requests is not None:
        conn_requests.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                uid TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                student_group TEXT NOT NULL,
                Понедельник_Завтрак INTEGER DEFAULT 0,
                Понедельник_Обед INTEGER DEFAULT 0,
                Понедельник_Ужин INTEGER DEFAULT 0,
                Вторник_Завтрак INTEGER DEFAULT 0,
                Вторник_Обед INTEGER DEFAULT 0,
                Вторник_Ужин INTEGER DEFAULT 0,
                Среда_Завтрак INTEGER DEFAULT 0,
                Среда_Обед INTEGER DEFAULT 0,
                Среда_Ужин INTEGER DEFAULT 0,
                Четверг_Завтрак INTEGER DEFAULT 0,
                Четверг_Обед INTEGER DEFAULT 0,
                Четверг_Ужин INTEGER DEFAULT 0,
                Пятница_Завтрак INTEGER DEFAULT 0,
                Пятница_Обед INTEGER DEFAULT 0,
                Пятница_Ужин INTEGER DEFAULT 0,
                Суббота_Завтрак INTEGER DEFAULT 0,
                Суббота_Обед INTEGER DEFAULT 0,
                Суббота_Ужин INTEGER DEFAULT 0
            );
        ''')
        conn_requests.close()

    conn_visits_report = create_connection(DATABASE_VISITS_REPORT)
    if conn_visits_report is not None:
        conn_visits_report.execute('''
            CREATE TABLE IF NOT EXISTS visits_report (
                uid TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                student_group TEXT NOT NULL,
                Понедельник_Завтрак INTEGER DEFAULT 0,
                Понедельник_Обед INTEGER DEFAULT 0,
                Понедельник_Ужин INTEGER DEFAULT 0,
                Вторник_Завтрак INTEGER DEFAULT 0,
                Вторник_Обед INTEGER DEFAULT 0,
                Вторник_Ужин INTEGER DEFAULT 0,
                Среда_Завтрак INTEGER DEFAULT 0,
                Среда_Обед INTEGER DEFAULT 0,
                Среда_Ужин INTEGER DEFAULT 0,
                Четверг_Завтрак INTEGER DEFAULT 0,
                Четверг_Обед INTEGER DEFAULT 0,
                Четверг_Ужин INTEGER DEFAULT 0,
                Пятница_Завтрак INTEGER DEFAULT 0,
                Пятница_Обед INTEGER DEFAULT 0,
                Пятница_Ужин INTEGER DEFAULT 0,
                Суббота_Завтрак INTEGER DEFAULT 0,
                Суббота_Обед INTEGER DEFAULT 0,
                Суббота_Ужин INTEGER DEFAULT 0
            );
        ''')
        conn_visits_report.close()

def load_database():
    file_path = filedialog.askopenfilename(title="Выберите файл базы данных", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        try:
            df = pd.read_excel(file_path, engine="openpyxl")
            conn_students = create_connection(DATABASE_STUDENTS)
            if conn_students is not None:
                cursor = conn_students.cursor()
                cursor.execute("DELETE FROM students")
                for _, row in df.iterrows():
                    cursor.execute("INSERT INTO students (uid, name, student_group) VALUES (?, ?, ?)",
                                  (row["uid"], row["name"], row["student_group"]))
                conn_students.commit()
                conn_students.close()
                messagebox.showinfo("Успех", "База данных успешно загружена!", parent=root)

                conn_visits = create_connection(DATABASE_VISITS)
                if conn_visits is not None:
                    cursor = conn_visits.cursor()
                    cursor.execute("DROP TABLE IF EXISTS visits")
                    cursor.execute('''
                        CREATE TABLE visits (
                            uid TEXT PRIMARY KEY,
                            name TEXT NOT NULL,
                            student_group TEXT NOT NULL,
                            Понедельник_Завтрак INTEGER DEFAULT 0,
                            Понедельник_Обед INTEGER DEFAULT 0,
                            Понедельник_Ужин INTEGER DEFAULT 0,
                            Вторник_Завтрак INTEGER DEFAULT 0,
                            Вторник_Обед INTEGER DEFAULT 0,
                            Вторник_Ужин INTEGER DEFAULT 0,
                            Среда_Завтрак INTEGER DEFAULT 0,
                            Среда_Обед INTEGER DEFAULT 0,
                            Среда_Ужин INTEGER DEFAULT 0,
                            Четверг_Завтрак INTEGER DEFAULT 0,
                            Четверг_Обед INTEGER DEFAULT 0,
                            Четверг_Ужин INTEGER DEFAULT 0,
                            Пятница_Завтрак INTEGER DEFAULT 0,
                            Пятница_Обед INTEGER DEFAULT 0,
                            Пятница_Ужин INTEGER DEFAULT 0,
                            Суббота_Завтрак INTEGER DEFAULT 0,
                            Суббота_Обед INTEGER DEFAULT 0,
                            Суббота_Ужин INTEGER DEFAULT 0
                        );
                    ''')
                    for _, row in df.iterrows():
                        cursor.execute('''
                            INSERT INTO visits (uid, name, student_group) VALUES (?, ?, ?)
                        ''', (row["uid"], row["name"], row["student_group"]))
                    conn_visits.commit()
                    conn_visits.close()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить базу данных: {e}", parent=root)

def load_requests_database():
    file_path = filedialog.askopenfilename(title="Выберите заявочный файл", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        try:
            df = pd.read_excel(file_path, engine="openpyxl")
            conn_students = create_connection(DATABASE_STUDENTS)
            if conn_students is None:
                messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных студентов.", parent=root)
                return
            conn_requests = create_connection(DATABASE_REQUESTS)
            if conn_requests is None:
                messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных заявок.", parent=root)
                return
            cursor_students = conn_students.cursor()
            cursor_requests = conn_requests.cursor()
            cursor_requests.execute("DELETE FROM requests")
            conn_requests.commit()
            cursor_students.execute("SELECT uid, name, student_group FROM students")
            all_students = cursor_students.fetchall()
            for student in all_students:
                uid, name, student_group = student
                cursor_requests.execute('''
                    INSERT INTO requests (uid, name, student_group) VALUES (?, ?, ?)
                ''', (uid, name, student_group))
            for _, row in df.iterrows():
                name = row["ФИО"]
                group = row["Группа"]
                cursor_students.execute("SELECT uid FROM students WHERE name = ? AND student_group = ?", (name, group))
                result = cursor_students.fetchone()
                if result:
                    uid = result[0]
                    for column in df.columns[2:]:
                        if "_" in column:
                            requested = row[column]
                            if requested == 1:
                                cursor_requests.execute(f'''
                                    UPDATE requests
                                    SET {column} = 1
                                    WHERE uid = ?
                                ''', (uid,))
            conn_requests.commit()
            messagebox.showinfo("Успех", "Заявочный файл успешно загружен!", parent=root)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить заявочный файл: {e}", parent=root)
        finally:
            if conn_students:
                conn_students.close()
            if conn_requests:
                conn_requests.close()

def load_visits_report():
    file_path = filedialog.askopenfilename(
        title="Выберите отчет №1", 
        filetypes=[("Excel files", "*.xlsx")]
    )
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
            full_names = {
                "Понедельник_З": "Понедельник_Завтрак",
                "Понедельник_О": "Понедельник_Обед",
                "Понедельник_У": "Понедельник_Ужин",
                "Вторник_З": "Вторник_Завтрак",
                "Вторник_О": "Вторник_Обед",
                "Вторник_У": "Вторник_Ужин",
                "Среда_З": "Среда_Завтрак",
                "Среда_О": "Среда_Обед",
                "Среда_У": "Среда_Ужин",
                "Четверг_З": "Четверг_Завтрак",
                "Четверг_О": "Четверг_Обед",
                "Четверг_У": "Четверг_Ужин",
                "Пятница_З": "Пятница_Завтрак",
                "Пятница_О": "Пятница_Обед",
                "Пятница_У": "Пятница_Ужин",
                "Суббота_З": "Суббота_Завтрак",
                "Суббота_О": "Суббота_Обед",
                "Суббота_У": "Суббота_Ужин"
            }
            df.rename(columns=full_names, inplace=True)
            conn = create_connection(DATABASE_VISITS_REPORT)
            if conn is not None:
                conn.execute("DELETE FROM visits_report")
                df.to_sql('visits_report', conn, if_exists='append', index=False)
                conn.commit()
                messagebox.showinfo("Успех", "Данные отчета успешно загружены!", parent=root)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки отчета: {e}", parent=root)
        finally:
            if conn:
                conn.close()