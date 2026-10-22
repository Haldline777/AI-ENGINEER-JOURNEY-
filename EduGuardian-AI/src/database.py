# src/core/database.py
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../../eduguardian.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Students Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            admission_no TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            form_class TEXT NOT NULL,
            dormitory TEXT NOT NULL,
            status TEXT DEFAULT 'Active'
        )
    """)
    
    # Attendance Logs Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admission_no TEXT,
            date TEXT,
            status TEXT, -- 'Present', 'Absent', 'Late'
            FOREIGN KEY (admission_no) REFERENCES students (admission_no)
        )
    """)
    
    conn.commit()
    conn.close()

def add_student(admission_no, full_name, form_class, dormitory):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT OR REPLACE INTO students (admission_no, full_name, form_class, dormitory, status) VALUES (?, ?, ?, ?, 'Active')",
            (admission_no, full_name, form_class, dormitory)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        conn.close()

def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()
    return rows

def log_attendance(admission_no, date, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO attendance_logs (admission_no, date, status) VALUES (?, ?, ?)",
        (admission_no, date, status)
    )
    conn.commit()
    conn.close()

def get_attendance_summary():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.form_class, 
               COUNT(a.id) as total_logs,
               SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) as present_count
        FROM students s
        LEFT JOIN attendance_logs a ON s.admission_no = a.admission_no
        GROUP BY s.form_class
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows