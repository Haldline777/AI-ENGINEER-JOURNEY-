# EduGuardian-AI/src/ai/risk_engine.py
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../../../eduguardian.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def evaluate_student_risk_profiles():
    """
    Analyzes attendance records per student and calculates a risk score.
    Returns a list of students with calculated attendance percentages and risk tiers.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Query to calculate individual student attendance rates
    cursor.execute("""
        SELECT s.admission_no, s.full_name, s.form_class, s.dormitory,
               COUNT(a.id) as total_logs,
               SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) as present_count,
               SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END) as absent_count,
               SUM(CASE WHEN a.status = 'Late' THEN 1 ELSE 0 END) as late_count
        FROM students s
        LEFT JOIN attendance_logs a ON s.admission_no = a.admission_no
        GROUP BY s.admission_no
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    evaluated_students = []
    for row in rows:
        data = dict(row)
        total = data["total_logs"] if data["total_logs"] > 0 else 1 # Prevent division by zero
        present = data["present_count"] or 0
        
        attendance_rate = (present / total) * 100
        
        # Determine AI Risk Tier
        if attendance_rate < 75 or data["absent_count"] >= 3:
            risk_level = "High Risk (Dropout/Welfare Alert)"
        elif attendance_rate < 85:
            risk_level = "Moderate Risk (Monitor Closely)"
        else:
            risk_level = "Low Risk (Stable)"
            
        data["attendance_rate"] = round(attendance_rate, 1)
        data["risk_level"] = risk_level
        evaluated_students.append(data)
        
    return evaluated_students

def generate_campus_ai_summary():
    """Generates overall systemic alerts for the administrator command center."""
    students = evaluate_student_risk_profiles()
    total_students = len(students)
    
    if total_students == 0:
        return ["System Stable: No student records available for AI evaluation yet."]
        
    high_risk_count = sum(1 for s in students if "High Risk" in s["risk_level"])
    mod_risk_count = sum(1 for s in students if "Moderate Risk" in s["risk_level"])
    
    alerts = []
    alerts.append(f"🔍 Evaluated {total_students} student profiles successfully.")
    
    if high_risk_count > 0:
        alerts.append(f"🚨 Critical Alert: Detected **{high_risk_count} student(s)** exhibiting high-risk absenteeism patterns requiring immediate counselor intervention.")
    else:
        alerts.append("✅ Stability Notice: Zero critical attendance dropouts detected across current logs.")
        
    if mod_risk_count > 0:
        alerts.append(f"⚠️ Advisory: **{mod_risk_count} student(s)** are in the moderate risk tier. Early notices recommended.")
        
    return alerts