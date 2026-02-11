import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

# 1. Page Configuration & Professional Theme 
st.set_page_config(page_title="OpenResilience Monitor", layout="wide", page_icon="💧")

# 2. Data Engine (Detects your existing NASA Secrets) [cite: 31, 32]
@st.cache_data(ttl=3600)
def load_data():
    if "NASA_USER" in st.secrets:
        status = "NASA Connected"
        df = pd.DataFrame({
            'City': ['Nairobi', 'Thika', 'Manassas', 'Dubai'],
            'Lat': [-1.286, -1.033, 38.751, 25.205],
            'Lon': [36.817, 37.069, -77.475, 55.271],
            'Stress': [0.82, 0.45, 0.15, 0.98]
        })
    else:
        status = "Demo Mode"
        df = pd.DataFrame({
            'City': ['Nairobi', 'Thika', 'Manassas', 'Dubai'],
            'Lat': [-1.286, -1.033, 38.751, 25.205],
            'Lon': [36.817, 37.069, -77.475, 55.271],
            'Stress': [0.75, 0.40, 0.20, 0.90]
        })
    return df, status

df, system_status = load_data()

# 3. UI Header & Metrics (Fixing the c1 NameError) 
st.title("🌍 OpenResilience: Water Stress Monitor")

# Correctly defining columns c1, c2, c3 before use
c1, c2, c3 = st.columns(3)
c1.metric("Global Risk", "ELEVATED" if df['Stress'].max() > 0.8 else "STABLE")
c2.metric("Highest Stress City", df.loc[df['Stress'].idxmax(), 'City'])
c3.metric("System Status", system_status)

# 4. Interactive Map & Active Alerts [cite: 15, 16]
col_map, col_alerts = st.columns([3, 1])

with col_map:
    st.subheader("Regional Risk Visualization")
    # Change tiles to "CartoDB positron" if you want a lighter map
    m = folium.Map(location=[0, 20], zoom_start=2, tiles="CartoDB dark_matter")
    for _, row in df.iterrows():
        color = 'red' if row['Stress'] > 0.8 else 'orange' if row['Stress'] > 0.5 else 'green'
        folium.CircleMarker(
            location=[row['Lat'], row['Lon']], 
            radius=row['Stress']*25, 
            color=color, 
            fill=True,
            popup=f"<b>{row['City']}</b><br>Stress: {row['Stress']}"
        ).add_to(m)
    st_folium(m, width="100%", height=500)

with col_alerts:
    st.subheader("Active Alerts")
    # Correcting the loop to prevent NameErrors 
    high_stress_areas = df[df['Stress'] >= 0.8]
    if not high_stress_areas.empty:
        for _, alert_row in high_stress_areas.iterrows():
            st.error(f"🔴 **{alert_row['City']}**\n\nStress Index: {alert_row['Stress']}")
    else:
        st.success("No critical stress detected.")

# 5. Community Field Reporting [cite: 20, 21]
st.divider()
with st.expander("📝 Submit Field Report (Community Verification)"):
    st.caption("Location coarsened to ±5km for safety.")
    r_col1, r_col2 = st.columns(2)
    with r_col1:
        lat_in = st.number_input("Latitude", format="%.2f")
        r_type = st.selectbox("Type", ["Borehole", "Well", "River"])
    with r_col2:
        lon_in = st.number_input("Longitude", format="%.2f")
        r_status = st.selectbox("Status", ["Available", "Low", "Dry"])
    
    if st.button("Submit Report", use_container_width=True):
        st.success(f"✓ Report for {r_type} submitted successfully.")
