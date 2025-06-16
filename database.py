import sqlite3
import pandas as pd

DATABASE_STUDENTS = "students.db"
DATABASE_VISITS = "visits.db"
DATABASE_REQUESTS = "requests.db"
DATABASE_VISITS_REPORT = "visits_report.db"

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
                Среда_Завтрак INTEGER disable_ntpDEFAULT 0,
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

def load_database(file_path):
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
            return True
    except Exception as e:
        print(f"Не удалось загрузить базу данных: {e}")
        return False