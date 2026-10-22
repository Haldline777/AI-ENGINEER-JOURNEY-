# src/dashboard/app.py
import streamlit as st
import sys
import os

# Ensure root path is accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.core.database import init_db, add_student, get_all_students, log_attendance
from src.ai.anomaly_engine import run_ai_diagnostics
from datetime import date

# Initialize Database
init_db()

st.set_page_config(page_title="EduGuardian AI - Command Center", layout="wide")

st.title("🛡️ EduGuardian AI — Intelligent School Operations Platform")
st.markdown("### Real-time Campus Intelligence & Administration Control Center")

# Sidebar navigation
menu = st.sidebar.selectbox("Navigation", ["Admin Overview & AI", "Student Management", "Attendance Logging"])

if menu == "Admin Overview & AI":
    st.subheader("🤖 AI Decision Engine & Operational Insights")
    
    if st.button("Run System Diagnostics"):
        alerts = run_ai_diagnostics()
        for alert in alerts:
            if "Critical" in alert:
                st.error(alert)
            elif "Stable" in alert:
                st.success(alert)
            else:
                st.info(alert)
    else:
        st.info("Click the button above to execute automated AI risk assessment across school classes.")
        
    st.markdown("---")
    st.metric(label="Registered Students in Database", value=len(get_all_students()))

elif menu == "Student Management":
    st.subheader("📚 Student Admission & Records")
    
    with st.form("student_form"):
        col1, col2 = st.columns(2)
        with col1:
            adm_no = st.text_input("Admission Number (e.g., ADM/2026/001)")
            name = st.text_input("Full Name")
        with col2:
            form_class = st.selectbox("Form / Class", ["Form 1 East", "Form 2 North", "Form 3 West", "Form 4 South"])
            dorm = st.text_input("Dormitory")
            
        submitted = st.form_submit_button("Register Student")
        if submitted and adm_no and name:
            success = add_student(adm_no, name, form_class, dorm)
            if success:
                st.success(f"Successfully registered {name} ({adm_no})!")
            else:
                st.error("Failed to register student. Admission number might already exist.")
                
    st.markdown("### Current Student Registry")
    students = get_all_students()
    if students:
        for s in students:
            st.write(f"- **{s['admission_no']}** | {s['full_name']} | Class: {s['form_class']} | Dorm: {s['dormitory']}")
    else:
        st.info("No students registered yet.")

elif menu == "Attendance Logging":
    st.subheader("📋 Daily Attendance Register")
    students = get_all_students()
    
    if not students:
        st.warning("Please register students first under Student Management.")
    else:
        with st.form("attendance_form"):
            selected_adm = st.selectbox("Select Student", options=[s['admission_no'] for s in students], format_func=lambda x: f"{x} - {[s['full_name'] for s in students if s['admission_no'] == x][0]}")
            att_date = st.date_input("Date", value=date.today())
            status = st.selectbox("Status", ["Present", "Absent", "Late"])
            
            log_submitted = st.form_submit_button("Log Attendance")
            if log_submitted:
                log_attendance(selected_adm, str(att_date), status)
                st.success(f"Logged {status} for {selected_adm} on {att_date}")