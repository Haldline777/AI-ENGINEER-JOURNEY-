# EduGuardian-AI/src/dashboard/app.py
import streamlit as st
import requests
from datetime import date

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="EduGuardian AI - Command Center", layout="wide")

st.title("🛡️ EduGuardian AI — Intelligent School Operations Platform")
st.markdown("### Real-time Campus Intelligence & Administration Control Center")

# Sidebar navigation
menu = st.sidebar.selectbox("Navigation", ["Admin Overview & AI", "Student Management", "Attendance Logging"])

if menu == "Admin Overview & AI":
    st.subheader("🤖 EduGuardian AI Decision Engine & Risk Analytics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Automated Campus Health Check")
        if st.button("Run Deep AI Diagnostics"):
            try:
                res = requests.get(f"{API_BASE_URL}/ai/diagnostics")
                if res.status_code == 200:
                    data = res.json()
                    st.success("AI Diagnostics completed successfully!")
                    for alert in data.get("alerts", []):
                        if "Critical" in alert or "🚨" in alert:
                            st.error(alert)
                        elif "Advisory" in alert or "⚠️" in alert:
                            st.warning(alert)
                        else:
                            st.info(alert)
                else:
                    st.error("Failed to fetch AI diagnostics from backend.")
            except Exception as e:
                st.error(f"Connection error: {e}")
        else:
            st.info("Click to run background risk modeling across student records.")

    with col2:
        st.markdown("#### Real-time System Metrics")
        try:
            res = requests.get(f"{API_BASE_URL}/students/")
            student_count = len(res.json()) if res.status_code == 200 else 0
            st.metric(label="Total Active Students", value=student_count)
        except:
            st.metric(label="Total Active Students", value="Offline")

    st.markdown("---")
    st.subheader("📊 Individual Student Risk & Intervention Register")
    
    try:
        risk_res = requests.get(f"{API_BASE_URL}/ai/risk-report")
        if risk_res.status_code == 200:
            risk_data = risk_res.json()
            if risk_data:
                for student in risk_data:
                    badge = student['risk_level']
                    rate = student['attendance_rate']
                    
                    if "High Risk" in badge:
                        st.error(f"**{student['full_name']}** ({student['admission_no']}) — Class: {student['form_class']} | Attendance: **{rate}%** | Status: **{badge}**")
                    elif "Moderate Risk" in badge:
                        st.warning(f"**{student['full_name']}** ({student['admission_no']}) — Class: {student['form_class']} | Attendance: **{rate}%** | Status: **{badge}**")
                    else:
                        st.info(f"**{student['full_name']}** ({student['admission_no']}) — Class: {student['form_class']} | Attendance: **{rate}%** | Status: **{badge}**")
            else:
                st.info("No student data available for risk analysis.")
        else:
            st.warning("Could not fetch risk report from backend.")
    except Exception as e:
        st.warning(f"Could not connect to backend API: {e}")

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
            
        submitted = st.form_submit_button("Register Student via API")
        if submitted and adm_no and name:
            payload = {
                "admission_no": adm_no,
                "full_name": name,
                "form_class": form_class,
                "dormitory": dorm
            }
            try:
                res = requests.post(f"{API_BASE_URL}/students/", json=payload)
                if res.status_code == 201:
                    st.success(f"Successfully registered {name} ({adm_no}) via API!")
                else:
                    st.error(f"Failed: {res.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Connection error: {e}")
                
    st.markdown("### Current Student Registry")
    try:
        res = requests.get(f"{API_BASE_URL}/students/")
        if res.status_code == 200:
            students = res.json()
            if students:
                for s in students:
                    st.write(f"- **{s['admission_no']}** | {s['full_name']} | Class: {s['form_class']} | Dorm: {s['dormitory']}")
            else:
                st.info("No students registered yet.")
        else:
            st.warning("Could not fetch student list from backend.")
    except:
        st.info("API server offline.")

elif menu == "Attendance Logging":
    st.subheader("📋 Daily Attendance Register")
    try:
        res = requests.get(f"{API_BASE_URL}/students/")
        students = res.json() if res.status_code == 200 else []
    except:
        students = []
    
    if not students:
        st.warning("Please register students first or ensure backend API is running.")
    else:
        with st.form("attendance_form"):
            selected_adm = st.selectbox("Select Student", options=[s['admission_no'] for s in students], format_func=lambda x: f"{x} - {[s['full_name'] for s in students if s['admission_no'] == x][0]}")
            att_date = st.date_input("Date", value=date.today())
            status = st.selectbox("Status", ["Present", "Absent", "Late"])
            
            log_submitted = st.form_submit_button("Log Attendance via API")
            if log_submitted:
                payload = {
                    "admission_no": selected_adm,
                    "date": str(att_date),
                    "status": status
                }
                try:
                    res = requests.post(f"{API_BASE_URL}/attendance/", json=payload)
                    if res.status_code == 200:
                        st.success(f"Logged {status} for {selected_adm} on {att_date} via API!")
                    else:
                        st.error("Failed to log attendance.")
                except Exception as e:
                    st.error(f"Connection error: {e}")