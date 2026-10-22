import streamlit as st
import requests
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="ELPELET Intelligence Command Center",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
        .stButton>button {
            width: 100%;
            background-color: #2b6cb0;
            color: white;
            font-weight: bold;
            border-radius: 6px;
        }
        .stButton>button:hover {
            background-color: #3182ce;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation & Controls
with st.sidebar:
    st.image("https://img.icons8.com/color/96/experimental-layout.png", width=70)
    st.title("Navigation & Controls")
    st.markdown("---")
    
    target_region = st.selectbox(
        "Select Target Region",
        [
            "Rift_Valley_Kenya", 
            "Nigeria_North", 
            "Ogun_Basin", 
            "South_Africa_Highveld", 
            "Central_Highlands", 
            "Coastal_Belt", 
            "Western_Basin"
        ]
    )
    
    st.markdown("---")
    fetch_btn = st.button("Fetch Live Telemetry & AI Advisory")

# Main Dashboard Title
st.title("🌍 ELPELET Core Intelligence & Risk Blueprint")
st.markdown(f"Displaying real-time analytical telemetry and strategic risk briefing for: **{target_region.replace('_', ' ')}**")

# Backend URLs
BACKEND_TELEMETRY_URL = f"http://127.0.0.1:8000/telemetry/{target_region}"
BACKEND_ADVISORY_URL = f"http://127.0.0.1:8000/advisory/{target_region}"

if fetch_btn:
    st.session_state["fetched"] = True

if st.session_state.get("fetched", False):
    try:
        response = requests.get(BACKEND_TELEMETRY_URL, timeout=20)
        if response.status_code == 200:
            telemetry_data = response.json()
            df = pd.DataFrame(telemetry_data)
        else:
            st.error(f"Telemetry API Error Code {response.status_code}: {response.text}")
            df = pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Connection error: {str(e)}")
        df = pd.DataFrame()

    if not df.empty:
        
        # ==========================================
        # 1. CHARTS IN DESCENDING PRIORITY ORDER
        # ==========================================
        st.markdown("---")
        st.subheader("📊 Multi-Variable Environmental & Trend Analytics")
        
        if "timestamp" in df.columns:
            indexed_df = df.set_index("timestamp")
            
            # Row 1 (Highest Priority): Soil Moisture & Soil Temperature
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("##### 💧 1. Root-Zone Soil Moisture Index")
                if "soil_moisture_m3" in indexed_df.columns:
                    st.line_chart(indexed_df[["soil_moisture_m3"]])
                else:
                    st.info("Data unavailable.")
                    
            with col2:
                st.markdown("##### 🌡️ 2. Soil Temperature Dynamics")
                if "soil_temp_c" in indexed_df.columns:
                    st.line_chart(indexed_df[["soil_temp_c"]])
                else:
                    st.info("Data unavailable.")

            # Row 2 (Supporting Priority): Air Temperature & Precipitation/UV
            col3, col4 = st.columns(2)
            with col3:
                st.markdown("##### 🌤️ 3. Air Temperature Trends")
                if "air_temp_c" in indexed_df.columns:
                    st.line_chart(indexed_df[["air_temp_c"]])
                else:
                    st.info("Data unavailable.")
                    
            with col4:
                st.markdown("##### 🌧️ 4. Precipitation & UV Exposure Index")
                precip_cols = [c for c in ["rainfall_mm", "uv_index"] if c in indexed_df.columns]
                if precip_cols:
                    st.line_chart(indexed_df[precip_cols])
                else:
                    st.info("Data unavailable.")

        # ==========================================
        # 2. AI RISK BLUEPRINT & ADVISORY (MIDDLE)
        # ==========================================
        st.markdown("---")
        st.subheader("🧠 Elpelet Core Intelligence & Risk Blueprint")

        try:
            ai_response = requests.get(BACKEND_ADVISORY_URL, timeout=20)
            if ai_response.status_code == 200:
                ai_data = ai_response.json()
                
                risk_flags = ai_data.get("risk_flags", [])
                if risk_flags:
                    for flag in risk_flags:
                        st.warning(f"⚠️ Algorithmic Risk Flags Triggered: {flag}")
                else:
                    st.success("✅ System Nominal: No critical environmental flags triggered.")
                
                st.markdown("---")
                st.markdown(ai_data.get("advisory", "No advisory generated."))
            else:
                st.error("Failed to retrieve advisory blueprint from backend engine.")
        except Exception as e:
            st.error(f"Connection error while fetching advisory: {str(e)}")

        # ==========================================
        # 3. RAW DATA TABLE AT THE VERY END
        # ==========================================
        st.markdown("---")
        st.subheader("📋 Raw Telemetry Data Matrix Log")
        st.dataframe(df, use_container_width=True)

    else:
        st.warning("⚠️ No active telemetry records found to display for this region.")
else:
    st.info("👈 Select your target region in the sidebar and click **'Fetch Live Telemetry & AI Advisory'** to load the dashboard.")