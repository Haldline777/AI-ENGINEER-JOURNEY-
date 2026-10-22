import os
import requests
import pandas as pd
from datetime import datetime

class ElpeletDataEngine:
    def __init__(self):
        # ALL target regions mapped precisely for Africa
        self.regions = {
            "Rift_Valley_Kenya": {"lat": -1.2921, "lon": 36.8219},
            "Nigeria_North": {"lat": 12.0022, "lon": 8.5920},
            "Ogun_Basin": {"lat": 7.1557, "lon": 3.3451},
            "South_Africa_Highveld": {"lat": -26.2041, "lon": 28.0473},
            "Central_Highlands": {"lat": -0.4217, "lon": 36.9517},
            "Coastal_Belt": {"lat": 4.0511, "lon": 9.7679},
            "Western_Basin": {"lat": 7.3775, "lon": 3.9470}
        }
        # CORRECT Open-Meteo endpoint URL
        self.base_url = "https://api.open-meteo.com/v1/forecast"

    def fetch_live_telemetry(self, region_name):
        """Pulls real-time multi-dimensional telemetry tracking environmental,
        agricultural, and public health risk vectors across the continent."""
        
        # Clean up any formatting discrepancies
        region_name = region_name.strip()
        
        if region_name not in self.regions:
            raise ValueError(f"Region '{region_name}' is not registered in the network pipeline.")
        
        coords = self.regions[region_name]
        
        params = {
            "latitude": coords["lat"],
            "longitude": coords["lon"],
            "hourly": "temperature_2m,relative_humidity_2m,soil_temperature_0cm,soil_moisture_0_to_1cm,rain,uv_index,direct_radiation",
            "timezone": "auto",
            "forecast_days": 1
        }
        
        print(f"📡 [INGESTION] Extracting live multi-variable matrix for {region_name}...")
        response = requests.get(self.base_url, params=params)
        
        if response.status_code == 200:
            payload = response.json()
            hourly_data = payload.get("hourly", {})
            
            df = pd.DataFrame({
                "timestamp": pd.to_datetime(hourly_data.get("time")),
                "air_temp_c": hourly_data.get("temperature_2m"),
                "humidity_pct": hourly_data.get("relative_humidity_2m"),
                "soil_temp_c": hourly_data.get("soil_temperature_0cm"),
                "soil_moisture_m3": hourly_data.get("soil_moisture_0_to_1cm"),
                "rainfall_mm": hourly_data.get("rain"),
                "uv_index": hourly_data.get("uv_index"),
                "solar_radiation_wm2": hourly_data.get("direct_radiation")
            })
            
            df["region"] = region_name
            df["ingested_at"] = datetime.utcnow()
            return df
        else:
            print(f"❌ [ERROR] Extraction failed. Code: {response.status_code} - Response: {response.text}")
            return None

    def execute_global_pipeline(self):
        master_frames = []
        for region in self.regions.keys():
            data_frame = self.fetch_live_telemetry(region)
            if data_frame is not None:
                master_frames.append(data_frame)
        
        if master_frames:
            return pd.concat(master_frames, ignore_index=True)
        return pd.DataFrame()

if __name__ == "__main__":
    engine = ElpeletDataEngine()
    print(engine.fetch_live_telemetry("Rift_Valley_Kenya").head(3))