# EduGuardian-AI/src/core/seed_api_data.py
import requests
import random
from datetime import datetime, timedelta

API_BASE_URL = "http://127.0.0.1:8000"

# Realistic sample data lists to generate clean, non-harmful test records
FIRST_NAMES = ["Amani", "Karanja", "Wanjiku", "Otieno", "Akinyi", "Cheruiyot", "Kiprop", "Mutua", "Nduta", "Omondi", "Cheptoo", "Barasa", "Njeri", "Maina", "Atieno"]
LAST_NAMES = ["Kamau", "Ochieng", "Kipkorir", "Njeri", "Kimani", "Odhiambo", "Kiptoo", "Wamalwa", "Mutisya", "Naliaka", "Kibet", "Nyongesa", "Chebet", "Karanja", "Muthoni"]
CLASSES = ["Form 1 East", "Form 2 North", "Form 3 West", "Form 4 South"]
DORMITORIES = ["Tsavo Hall", "Mara House", "Serengeti Block", "Amboseli Wing"]

def generate_students(num_students=40):
    print("🚀 Seeding student records via API...")
    success_count = 0
    
    for i in range(1, num_students + 1):
        adm_no = f"ADM/2026/{i:03d}"
        full_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        form_class = random.choice(CLASSES)
        dormitory = random.choice(DORMITORIES)
        
        payload = {
            "admission_no": adm_no,
            "full_name": full_name,
            "form_class": form_class,
            "dormitory": dormitory
        }
        
        try:
            res = requests.post(f"{API_BASE_URL}/students/", json=payload)
            if res.status_code == 201:
                success_count += 1
        except Exception as e:
            print(f"Connection error while seeding student {adm_no}: {e}")
            
    print(f"✅ Successfully registered {success_count} students into the database via API.")

def generate_attendance_logs(days_back=5):
    print("📋 Generating historical attendance logs via API...")
    
    # First, fetch all registered students from the API
    try:
        res = requests.get(f"{API_BASE_URL}/students/")
        if res.status_code != 200:
            print("Failed to fetch students for attendance seeding.")
            return
        students = res.json()
    except Exception as e:
        print(f"Could not connect to API to fetch students: {e}")
        return
        
    if not students:
        print("No students found in database to log attendance for.")
        return

    today = datetime.now().date()
    log_count = 0
    
    for student in students:
        admission_no = student["admission_no"]
        # Generate attendance for the past few days
        for d in range(days_back):
            log_date = today - timedelta(days=d)
            # 85% chance present, 10% absent, 5% late (realistic school pattern)
            status = random.choices(["Present", "Absent", "Late"], weights=[85, 10, 5])[0]
            
            payload = {
                "admission_no": admission_no,
                "date": str(log_date),
                "status": status
            }
            
            try:
                res = requests.post(f"{API_BASE_URL}/attendance/", json=payload)
                if res.status_code == 200:
                    log_count += 1
            except Exception as e:
                print(f"Error logging attendance: {e}")
                
    print(f"✅ Successfully generated and pushed {log_count} attendance logs into the database.")

if __name__ == "__main__":
    print("Checking if FastAPI server is reachable...")
    try:
        health_check = requests.get(f"{API_BASE_URL}/")
        if health_check.status_code == 200:
            print("API is online. Starting data population...")
            generate_students(45)
            generate_attendance_logs(7)
            print("🎉 Database population complete! Refresh your Streamlit dashboard.")
        else:
            print("API returned an unexpected status code.")
    except Exception:
        print("❌ Could not connect to FastAPI server. Make sure Uvicorn is running on http://127.0.0.1:8000")