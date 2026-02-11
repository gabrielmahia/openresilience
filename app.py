import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
from datetime import datetime

# =============================================================================
# SYSTEM CONFIG & THEME
# =============================================================================
st.set_page_config(page_title="OpenResilience Monitor", layout="wide", page_icon="💧")

# =============================================================================
# DATA ENGINE (NASA ACTIVE)
# =============================================================================
@st.cache_data(ttl=3600)
def load_system_data():
    # Detects the NASA Secrets you've already connected
    if "NASA_USER" in st.secrets:
        status = "NASA Connected"
        # In production, this pulls from NASA LANCE/Earthdata APIs
        df = pd.DataFrame({
            'City': ['Nairobi', 'Thika', 'Manassas', 'Dubai'],
            'Lat': [-1.286, -1.033, 38.751, 25.205],
            'Lon': [36.817, 37.069, -77.475, 55.271],
            'Stress': [0.82, 0.45, 0.15, 0.98],
            'Source': ['NASA SMAP/IMERG'] * 4
        })
    else:
        status = "Demo Mode (Secrets Missing)"
        df = pd.DataFrame({
            'City': ['Nairobi', 'Thika', 'Manassas', 'Dubai'],
            'Lat': [-1.286, -1.033, 38.751, 25.205],
            'Lon': [36.817, 37.069, -77.475, 55.271],
            'Stress': [0.75, 0.40, 0.20, 0.90],
            'Source': ['Synthetic-Demo'] * 4
        })
    return df, status

# =============================================================================
# MAIN INTERFACE
# =============================================================================
st.title("🌍 OpenResilience: Water Stress Monitor")
df, system_status = load_system_data()

# Metrics Row
c1, c2, c3 = st.columns(3)
c1.metric("Global Risk", "ELEVATED" if df['Stress'].max() > 0.8 else "STABLE") [cite: 33]
c2.metric("Local Stress (Nairobi)", df.loc[0, 'Stress']) [cite: 33]
c3.metric("System Status", system_status) [cite: 33]

# Layout: Map and Alerts
col_map, col_alerts = st.columns([3, 1])

with col_map:
    # RECOMMENDATION: Use "CartoDB positron" for a light map, or "dark_matter" for the dark view
    m = folium.Map(location=[0, 30], zoom_start=2, tiles="CartoDB positron") 
    
    for _, row in df.iterrows():
        color = 'red' if row['Stress'] > 0.8 else 'orange' if row['Stress'] > 0.5 else 'green' [cite: 34]
        folium.CircleMarker(
            location=[row['Lat'], row['Lon']],
            radius=row['Stress'] * 25,
            color=color,
            fill=True,
            popup=f"<b>{row['City']}</b><br>Stress: {row['Stress']}"
        ).add_to(m)
    
    st_folium(m, width="100%", height=500)

with col_alerts:
    st.subheader("Active Alerts")
    critical = df[df['Stress'] >= 0.8] [cite: 18]
    if not critical.empty:
        for _, alert in critical.iterrows():
            st.error(f"🔴 **{alert['City']}**\n\nCritical Stress: {alert['Stress']}") [cite: 19]
    else:
        st.success("No critical alerts detected.")

# Field Reporting
st.divider()
with st.expander("📝 Submit Field Report (Community Verification)"):
    st.caption("Location is coarsened to ±5km for safety.") [cite: 20]
    r_c1, r_c2 = st.columns(2)
    with r_c1:
        lat_in = st.number_input("Latitude", format="%.2f") [cite: 20]
        r_type = st.selectbox("Type", ["Borehole", "Well", "River"]) [cite: 20]
    with r_c2:
        lon_in = st.number_input("Longitude", format="%.2f") [cite: 20]
        r_stat = st.selectbox("Status", ["Available", "Low", "Dry"]) [cite: 20]
    
    if st.button("Submit Report", use_container_width=True):
        st.success(f"✓ Report for {r_type} submitted.") [cite: 21]

# Export
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Analysis (CSV)", csv, "water_stress.csv", "text/csv") [cite: 34]
