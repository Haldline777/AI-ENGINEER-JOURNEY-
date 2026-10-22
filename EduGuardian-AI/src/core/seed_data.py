# src/core/seed_data.py
import sqlite3
import os
from datetime import datetime, timedelta
import random

DB_PATH = os.path.join(os.path.dirname(__file__), "../../eduguardian.db")

FIRST_NAMES = ["Kiprono", "Amina", "Baraka", "Wanjiku", "Ochieng", "Mutua", "Cheptoo", "Omondi", "Adhiambo", "Kamau", "Fatuma", "Juma"]
LAST_NAMES = ["Kenyatta", "Otieno", "Mwangi", "Njoroge", "Cheruiyot", "Odhiambo", "Kiplagat", "Abdi", "Mutiso", "Awuor"]
FORMS = ["Form 1 East", "Form 1 West", "Form 2 North", "Form 2 South", "Form 3 East", "Form 3 West", "Form 4 North", "Form 4 South"]
DORMS = ["Tsavo Hall", "Mara Hostel", "Elgon House", "Kilimanjaro Block"]

def seed_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("Initializing tables...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            admission_no TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            form_class TEXT NOT NULL,
            dormitory TEXT NOT NULL,
            status TEXT DEFAULT 'Active'
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admission_no TEXT,
            date TEXT,
            status TEXT,
            FOREIGN KEY (admission_no) REFERENCES students (admission_no)
        )
    """)
    
    # Check if students already exist
    cursor.execute("SELECT COUNT(*) FROM students")
    count = cursor.fetchone()[0]
    
    if count > 0:
        print("Database already has data. Skipping seed.")
        conn.close()
        return

    print("Generating realistic student records...")
    students = []
    for i in range(1, 120): # Generate 115 realistic student profiles
        adm_no = f"ADM/2026/{i:03d}"
        name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        form_class = random.choice(FORMS)
        dorm = random.choice(DORMS)
        students.append((adm_no, name, form_class, dorm, "Active"))
        
    cursor.executemany("INSERT OR REPLACE INTO students VALUES (?, ?, ?, ?, ?)", students)
    
    print("Generating historical attendance logs for the past 14 days...")
    attendance_records = []
    cursor.execute("SELECT admission_no FROM students")
    all_students = [row[0] for row in cursor.fetchall()]
    
    base_date = datetime.now()
    for day_offset in range(14, 0, -1):
        current_date = (base_date - timedelta(days=day_offset)).strftime("%Y-%m-%d")
        for adm in all_students:
            # Simulate realistic attendance patterns (mostly present, occasional late/absent)
            status = random.choices(["Present", "Absent", "Late"], weights=[85, 8, 7])[0]
            attendance_records.append((adm, current_date, status))
            
    cursor.executemany("INSERT INTO attendance_logs (admission_no, date, status) VALUES (?, ?, ?)", attendance_records)
    
    conn.commit()
    conn.close()
    print("✅ Successfully seeded EduGuardian database with realistic local data!")

if __name__ == "__main__":
    seed_database()