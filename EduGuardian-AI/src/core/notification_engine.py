# EduGuardian-AI/src/core/notification_engine.py

def generate_guardian_alert(student_name: str, admission_no: str, form_class: str, attendance_rate: float):
    """
    Generates a professional, automated SMS/Email intervention notice 
    for school administration or parents regarding high absenteeism risk.
    """
    message = (
        f"URGENT EDUGUARDIAN WELFARE ALERT\n"
        f"----------------------------------------\n"
        f"Student: {student_name} ({admission_no})\n"
        f"Class: {form_class}\n"
        f"Current Attendance Rate: {attendance_rate}%\n"
        f"Status: HIGH RISK - Immediate counselor intervention or guardian meeting required.\n"
        f"Action: Please contact the school administration office."
    )
    return message