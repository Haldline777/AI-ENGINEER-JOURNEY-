import os
import sys
from fastapi import FastAPI, HTTPException
import pandas as pd

# Ensure Python can resolve sibling modules in the backend directory
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from earth_and_food_ml.ingestion_engine import ElpeletDataEngine # type: ignore
from dynamic_advisor import ElpeletIntelligenceAdvisor # type: ignore
from database import init_db, save_telemetry_batch, get_stored_telemetry, save_advisory_log

app = FastAPI(
    title="Elpelet AI Intelligence Backend",
    description="Cross-disciplinary real-time telemetry, database logging, and risk advisory engine.",
    version="2.0.0"
)

# Initialize database on startup
init_db()

# Initialize engines
data_engine = ElpeletDataEngine()
ai_advisor = ElpeletIntelligenceAdvisor()

@app.get("/")
def read_root():
    return {
        "status": "online",
        "system": "Elpelet AI Core Intelligence Engine with Database Persistence",
        "supported_regions": [
            "Rift_Valley_Kenya", 
            "Nigeria_North", 
            "Ogun_Basin", 
            "South_Africa_Highveld", 
            "Central_Highlands", 
            "Coastal_Belt", 
            "Western_Basin"
        ]
    }

@app.get("/telemetry/{region_name}")
def get_region_telemetry(region_name: str):
    try:
        # 1. Fetch live generated data from engine
        df = data_engine.fetch_live_telemetry(region_name)
        if df is None or df.empty:
            raise HTTPException(status_code=404, detail=f"No telemetry data found for region: {region_name}")
        
        # 2. Persist batch into SQLite database automatically
        save_telemetry_batch(region_name, df)
        
        # 3. Fetch consolidated history from DB to return complete trends
        historical_df = get_stored_telemetry(region_name)
        if historical_df is not None and not historical_df.empty:
            records = historical_df.to_dict(orient="records")
        else:
            records = df.to_dict(orient="records")
        
        # Return list directly so pd.DataFrame(response.json()) in Streamlit works seamlessly
        return records
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/advisory/{region_name}")
def get_region_ai_advisory(region_name: str):
    """Pulls telemetry data, runs AI analysis, logs warnings, and returns strategic blueprints."""
    try:
        df = data_engine.fetch_live_telemetry(region_name)
        if df is None or df.empty:
            raise HTTPException(status_code=404, detail=f"No telemetry data found for region: {region_name}")
        
        latest_row = df.iloc[-1].to_dict()
        latest_row["region"] = region_name
        
        # Run risk assessment & generate AI blueprint
        risk_evaluation = ai_advisor.analyze_telemetry_risks(latest_row)
        ai_blueprint = ai_advisor.generate_localized_advisory(latest_row)
        
        # Save advisory log to database
        save_advisory_log(region_name, risk_evaluation, ai_blueprint)
        
        # Ensure keys strictly match what Streamlit expects: risk_flags, has_warnings, and advisory
        return {
            "region": region_name,
            "risk_flags": risk_evaluation.get("risk_flags", []),
            "has_warnings": risk_evaluation.get("has_warnings", False),
            "advisory": ai_blueprint
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))