import os
import pandas as pd
from anthropic import Anthropic

class ElpeletIntelligenceAdvisor:
    def __init__(self):
        # Secure initialization of the Anthropic SDK client
        self.api_key = os.getenv("ANTHROPIC_API_KEY", "mock_key_for_testing_and_ci")
        self.client = Anthropic(api_key=self.api_key)

    def analyze_telemetry_risks(self, metrics_row: dict) -> dict:
        """ Pure Data Science Logic: Programmatically evaluates raw telemetry thresholds
        across Earth, Food, Health, and Finance vectors before passing context to the LLM agent. """
        flags = []
        
        # 1. Earth & Food Vector: Volumetric soil moisture under 0.2 indicates drought stress
        if metrics_row.get("soil_moisture_m3", 0.5) < 0.20:
            flags.append("CRITICAL_DROUGHT_RISK: Low root-zone soil telemetry detected.")
            
        # 2. Health Vector: UV index exceeding 8 indicates severe heat-stress thresholds
        if metrics_row.get("uv_index", 0) > 8:
            flags.append("HIGH_HEAT_HEALTH_HAZARD: Elevated UV exposure risk for field workforces.")
            
        # 3. Finance/Logistics Vector: Heavy precipitation risks supply chain bottlenecks
        if metrics_row.get("rainfall_mm", 0) > 10.0:
            flags.append("FINANCIAL_LOGISTICS_WARNING: Potential supply chain/market disruption.")
            
        return {
            "region": metrics_row.get("region", "Unknown"),
            "risk_flags": flags,
            "has_warnings": len(flags) > 0
        }

    def generate_localized_advisory(self, metrics_row: dict) -> str:
        """ AI Engineering Architecture: Orchestrates contextual prompt plumbing
        integrating live parameters to yield structurally deterministic outputs. """
        evaluation = self.analyze_telemetry_risks(metrics_row)
        
        system_prompt = (
            "You are the ELPELET Systems Core Intelligence Engine, an advanced agent "
            "optimizing resources across Africa. You synthesize multi-disciplinary data inputs "
            "(Earth, Food, Health, Finance) into short, definitive, actionable directives. "
            "Never use generic fluff or filler phrases. Speak directly to field personnel."
        )
        
        user_content = f"""
        Execute cross-disciplinary risk assessment for the following localized metrics:
        - Region Base: {evaluation['region']}
        - Soil Moisture: {metrics_row.get('soil_moisture_m3')} m³/m³
        - Soil Temp: {metrics_row.get('soil_temp_c')} °C
        - Precipitation: {metrics_row.get('rainfall_mm')} mm/hr
        - UV Index Exposure: {metrics_row.get('uv_index')}
        - Solar Radiation: {metrics_row.get('solar_radiation_wm2')} W/m²
        
        Engine Algorithmic Flags: {", ".join(evaluation['risk_flags']) if evaluation['has_warnings'] else 'SYSTEM_NOMINAL'}
        
        Provide a concise, execution-ready blueprint broken down exactly into these three headers:
        1. 🌾 AGRICULTURAL ACTIONS (Crop & Water Management)
        2. 🏥 COMMUNITY HEALTH SAFEGUARDS (Workforce & Nutrition Mitigation)
        3. 📉 MICRO-FINANCE & LOGISTICS PLAN (Buying Power & Risk Allocation)
        """

        if self.api_key == "mock_key_for_testing_and_ci":
            return (
                f"🚧 [TEST MODE] ELPELET Intelligence Output for {evaluation['region']}:\n"
                f"Flags processed successfully: {evaluation['risk_flags'] or 'None'}\n"
                f"Connect a valid ANTHROPIC_API_KEY environment variable to stream production inferences."
            )

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                temperature=0.2,
                system=system_prompt,
                messages=[{"role": "user", "content": user_content}]
            )
            return message.content[0].text
        except Exception as e:
            return f"❌ AI Engine invocation failed: {str(e)}"

if __name__ == "__main__":
    # Simulate a high-risk telemetry entry matching real environmental threats
    sample_telemetry = {
        "region": "Rift_Valley_Kenya",
        "soil_temp_c": 28.4,
        "soil_moisture_m3": 0.14,  # Triggers drought flag
        "rainfall_mm": 0.0,
        "uv_index": 9.2,           # Triggers health hazard flag
        "solar_radiation_wm2": 820.0
    }
    
    advisor = ElpeletIntelligenceAdvisor()
    print("🤖 Processing telemetry data array through ELPELET AI Framework...")
    output_advisory = advisor.generate_localized_advisory(sample_telemetry)
    print("\n================== LIVE INTEL OUTPUT ==================")
    print(output_advisory)