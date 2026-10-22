# src/ai/anomaly_engine.py
from src.core.database import get_attendance_summary

def run_ai_diagnostics():
    """Analyzes student attendance metrics and generates operational warnings."""
    summary = get_attendance_summary()
    alerts = []
    
    for row in summary:
        form_class = row["form_class"]
        total = row["total_logs"]
        present = row["present_count"] or 0
        
        if total > 0:
            attendance_rate = (present / total) * 100
            if attendance_rate < 80:
                alerts.append(f"⚠️ Critical Risk: {form_class} attendance rate has dropped to {attendance_rate:.1f}%. Immediate review required.")
            else:
                alerts.append(f"✅ Stable: {form_class} is performing normally at {attendance_rate:.1f}% attendance.")
        else:
            alerts.append(f"ℹ️ Notice: No attendance data recorded yet for {form_class}.")
            
    return alerts