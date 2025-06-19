import sqlite3
from config.constants import DATABASE_STUDENTS, DATABASE_VISITS, DATABASE_REQUESTS, DATABASE_VISITS_REPORT

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(f"Ошибка при подключении к базе данных: {e}")
    return None

def create_tables():
    conn_students = create_connection(DATABASE_STUDENTS)
    if conn_students:
        conn_students.execute('''
            CREATE TABLE IF NOT EXISTS students (
                uid TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                student_group TEXT NOT NULL
            );
        ''')
        conn_students.close()

    conn_visits = create_connection(DATABASE_VISITS)
    if conn_visits:
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
    if conn_requests:
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
    if conn_visits_report:
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