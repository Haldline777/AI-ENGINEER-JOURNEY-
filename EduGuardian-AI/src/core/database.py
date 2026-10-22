# EduGuardian-AI/src/core/database.py
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../../../eduguardian.db")

def get_connection():
    """Establishes a connection to SQLite with foreign keys enabled and row factory set."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the relational database schema."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Students Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            admission_no TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            form_class TEXT NOT NULL,
            dormitory TEXT NOT NULL,
            status TEXT DEFAULT 'Active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 2. Attendance Logs Table (Relational with Students)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admission_no TEXT NOT NULL,
            date TEXT NOT NULL,
            status TEXT CHECK(status IN ('Present', 'Absent', 'Late')) NOT NULL,
            FOREIGN KEY (admission_no) REFERENCES students (admission_no) ON DELETE CASCADE
        )
    """)

    # 3. AI Risk Audits Table (Relational with Classes/Metrics)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_risk_audits (
            audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
            form_class TEXT NOT NULL,
            attendance_rate REAL NOT NULL,
            risk_level TEXT NOT NULL,
            evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    print("Relational database schema initialized successfully.")

def insert_student(admission_no: str, full_name: str, form_class: str, dormitory: str):
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
        print(f"Database Error: {e}")
        return False
    finally:
        conn.close()

def fetch_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def log_student_attendance(admission_no: str, date: str, status: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO attendance_logs (admission_no, date, status) VALUES (?, ?, ?)",
        (admission_no, date, status)
    )
    conn.commit()
    conn.close()

def get_class_attendance_analytics():
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
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

if __name__ == "__main__":
    init_db()