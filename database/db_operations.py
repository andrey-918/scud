import pandas as pd
from tkinter import messagebox, filedialog
from database.db_init import create_connection
from config.constants import DATABASE_STUDENTS, DATABASE_VISITS, DATABASE_REQUESTS

def load_database(root):
    file_path = filedialog.askopenfilename(title="Выберите файл базы данных", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        try:
            df = pd.read_excel(file_path, engine="openpyxl")
            conn_students = create_connection(DATABASE_STUDENTS)
            if conn_students:
                cursor = conn_students.cursor()
                cursor.execute("DELETE FROM students")
                for _, row in df.iterrows():
                    cursor.execute("INSERT INTO students (uid, name, student_group) VALUES (?, ?, ?)",
                                  (row["uid"], row["name"], row["student_group"]))
                conn_students.commit()
                conn_students.close()
                messagebox.showinfo("Успех", "База данных успешно загружена!", parent=root)

                # Initialize visits database
                conn_visits = create_connection(DATABASE_VISITS)
                if conn_visits:
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

def load_requests_database(root):
    file_path = filedialog.askopenfilename(title="Выберите заявочный файл", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        try:
            df = pd.read_excel(file_path, engine="openpyxl")
            conn_students = create_connection(DATABASE_STUDENTS)
            conn_requests = create_connection(DATABASE_REQUESTS)
            if conn_students and conn_requests:
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
            else:
                messagebox.showerror("Ошибка", "Не удалось подключиться к базе данных.", parent=root)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить заявочный файл: {e}", parent=root)
        finally:
            if conn_students:
                conn_students.close()
            if conn_requests:
                conn_requests.close()