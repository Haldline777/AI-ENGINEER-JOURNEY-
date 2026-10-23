# EduGuardian-AI/src/core/api_backend.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# Internal project imports using correct relative paths
from .database import init_db, insert_student, fetch_all_students, log_student_attendance, get_class_attendance_analytics
from ..ai.risk_engine import evaluate_student_risk_profiles, generate_campus_ai_summary
from .notification_engine import generate_guardian_alert
from .portal_sync import simulate_moodle_portal_sync

app = FastAPI(title="EduGuardian AI Core API", version="1.0.0")

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

# Pydantic Schemas
class StudentModel(BaseModel):
    admission_no: str
    full_name: str
    form_class: str
    dormitory: str

class AttendanceModel(BaseModel):
    admission_no: str
    date: str
    status: str  # Present, Absent, Late

@app.get("/")
def home():
    return {"message": "Welcome to EduGuardian AI Core Backend API", "status": "Active"}

@app.post("/students/", status_code=201)
def register_student(student: StudentModel):
    success = insert_student(student.admission_no, student.full_name, student.form_class, student.dormitory)
    if not success:
        raise HTTPException(status_code=400, detail="Could not register student. Admission number might conflict.")
    return {"message": f"Student {student.full_name} registered successfully."}

@app.get("/students/", response_model=List[StudentModel])
def get_students():
    return fetch_all_students()

@app.post("/attendance/")
def record_attendance(log: AttendanceModel):
    if log.status not in ["Present", "Absent", "Late"]:
        raise HTTPException(status_code=400, detail="Invalid status. Must be Present, Absent, or Late.")
    log_student_attendance(log.admission_no, log.date, log.status)
    return {"message": "Attendance logged successfully", "data": log}

@app.get("/analytics/attendance")
def attendance_analytics():
    return get_class_attendance_analytics()

@app.get("/ai/risk-report")
def get_risk_report():
    """Returns AI-calculated risk profiles for all students."""
    return evaluate_student_risk_profiles()

@app.get("/ai/diagnostics")
def get_ai_diagnostics():
    """Returns high-level AI campus health alerts."""
    return {"alerts": generate_campus_ai_summary()}

@app.post("/notifications/alert")
def trigger_alert(admission_no: str, student_name: str, form_class: str, attendance_rate: float):
    """Triggers and returns an automated guardian/admin notification draft."""
    alert_text = generate_guardian_alert(student_name, admission_no, form_class, attendance_rate)
    return {"status": "Alert Generated", "notification_content": alert_text}

@app.post("/portal/sync")
def sync_portal_data():
    """Triggers synchronization from external student portals or Moodle."""
    sync_results = simulate_moodle_portal_sync()
    return {"status": "Sync Complete", "details": sync_results}