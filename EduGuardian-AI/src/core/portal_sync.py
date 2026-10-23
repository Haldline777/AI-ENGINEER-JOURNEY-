# EduGuardian-AI/src/core/portal_sync.py
import requests

API_BASE_URL = "http://127.0.0.1:8000"

def simulate_moodle_portal_sync():
    """
    Simulates external data capture from a Moodle LMS or Student Portal.
    Pushes automated access logs and status updates to the EduGuardian API.
    """
    payloads = [
        {"admission_no": "ADM/2026/001", "date": "2026-10-22", "status": "Present"},
        {"admission_no": "ADM/2026/002", "date": "2026-10-22", "status": "Absent"},
    ]
    
    results = []
    for payload in payloads:
        try:
            res = requests.post(f"{API_BASE_URL}/attendance/", json=payload)
            if res.status_code == 200:
                results.append(f"Synced portal record for {payload['admission_no']}: Success")
            else:
                results.append(f"Synced portal record for {payload['admission_no']}: Failed")
        except Exception as e:
            results.append(f"Connection error during sync: {e}")
            
    return results