import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "elpelet_intelligence.db"

def init_db():
    """Initializes SQLite tables for telemetry and AI advisories."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Telemetry historical log table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telemetry_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region TEXT,
            timestamp TEXT,
            air_temp_c REAL,
            soil_temp_c REAL,
            soil_moisture_m3 REAL,
            rainfall_mm REAL,
            uv_index REAL,
            solar_radiation_wm2 REAL,
            humidity_pct REAL,
            created_at TEXT
        )
    """)
    
    # AI Risk Advisory historical log table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS advisory_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region TEXT,
            risk_flags TEXT,
            has_warnings INTEGER,
            ai_blueprint TEXT,
            created_at TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def save_telemetry_batch(region: str, df: pd.DataFrame):
    """Saves incoming telemetry dataframes into the database."""
    conn = sqlite3.connect(DB_NAME)
    now = datetime.utcnow().isoformat()
    
    for _, row in df.iterrows():
        conn.execute("""
            INSERT INTO telemetry_logs (
                region, timestamp, air_temp_c, soil_temp_c, soil_moisture_m3, 
                rainfall_mm, uv_index, solar_radiation_wm2, humidity_pct, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            region,
            str(row.get("timestamp")),
            float(row.get("air_temp_c", 0)),
            float(row.get("soil_temp_c", 0)),
            float(row.get("soil_moisture_m3", 0)),
            float(row.get("rainfall_mm", 0)),
            float(row.get("uv_index", 0)),
            float(row.get("solar_radiation_wm2", 0)),
            float(row.get("humidity_pct", 0)),
            now
        ))
    conn.commit()
    conn.close()

def get_stored_telemetry(region: str) -> pd.DataFrame:
    """Retrieves historical telemetry data for a region from the database."""
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query(
        "SELECT * FROM telemetry_logs WHERE region = ? ORDER BY timestamp ASC",
        conn,
        params=(region,)
    )
    conn.close()
    return df

def save_advisory_log(region: str, risk_evaluation: dict, blueprint: str):
    """Saves generated AI blueprints and risk flags."""
    conn = sqlite3.connect(DB_NAME)
    now = datetime.utcnow().isoformat()
    flags_str = ", ".join(risk_evaluation.get("risk_flags", []))
    has_warnings = 1 if risk_evaluation.get("has_warnings", False) else 0
    
    conn.execute("""
        INSERT INTO advisory_logs (region, risk_flags, has_warnings, ai_blueprint, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (region, flags_str, has_warnings, blueprint, now))
    
    conn.commit()
    conn.close()