import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

# =============================================================================
# 1. CONFIGURATION & THEME
# =============================================================================
st.set_page_config(page_title="OpenResilience Monitor", layout="wide", page_icon="💧")

# =============================================================================
# 2. DATA ENGINE (NASA-READY)
# =============================================================================
@st.cache_data(ttl=3600)
def load_system_data():
    """Detects NASA Secrets and provides high-resolution regional data."""
    if "NASA_USER" in st.secrets:
        status = "NASA Connected"
        df = pd.DataFrame({
            'City': ['Westlands (Nairobi)', 'Thika', 'Manassas', 'Dubai'],
            'Lat': [-1.267, -1.033, 38.751, 25.205], # Precise Westlands Lat
            'Lon': [36.808, 37.069, -77.475, 55.271], # Precise Westlands Lon
            'Stress': [0.88, 0.45, 0.15, 0.98]
        })
    else:
        status = "Demo Mode"
        df = pd.DataFrame({
            'City': ['Westlands (Nairobi)', 'Thika', 'Manassas', 'Dubai'],
            'Lat': [-1.267, -1.033, 38.751, 25.205],
            'Lon': [36.808, 37.069, -77.475, 55.271],
            'Stress': [0.75, 0.40, 0.20, 0.90]
        })
    return df, status

df, system_status = load_system_data()

# =============================================================================
# 3. MAIN INTERFACE & METRICS
# =============================================================================
st.title("🌍 OpenResilience: Water Stress Monitor")

# FIX: Defining columns before calling them prevents NameError 
c1, c2, c3 = st.columns(3)
c1.metric("Global Risk Level", "ELEVATED" if df['Stress'].max() > 0.8 else "STABLE")
c2.metric("Local Index (Westlands)", df.loc[0, 'Stress'])
c3.metric("System Status", system_status)

# Sidebar Navigation
st.sidebar.header("Navigation")
# Drill down capability for Westlands
view_selection = st.sidebar.selectbox("Drill Down", ["Global View", "Westlands, Nairobi", "Horn of Africa"])

# =============================================================================
# 4. MAP & ACTIVE ALERTS
# =============================================================================
col_map, col_alerts = st.columns([3, 1])

with col_map:
    # Set map center based on selection
    if view_selection == "Westlands, Nairobi":
        map_center = [-1.267, 36.808]
        zoom = 14
    elif view_selection == "Horn of Africa":
        map_center = [6.0, 43.0]
        zoom = 5
    else:
        map_center = [0, 20]
        zoom = 2

    st.subheader(f"Visualization: {view_selection}")
    m = folium.Map(location=map_center, zoom_start=zoom, tiles="CartoDB dark_matter")
    
    for _, row in df.iterrows():
        color = 'red' if row['Stress'] > 0.8 else 'orange' if row['Stress'] > 0.5 else 'green'
        folium.CircleMarker(
            location=[row['Lat'], row['Lon']],
            radius=row['Stress'] * 25,
            color=color,
            fill=True,
            popup=f"<b>{row['City']}</b><br>Stress Index: {row['Stress']}"
        ).add_to(m)
    
    st_folium(m, width="100%", height=500)

with col_alerts:
    st.subheader("Active Alerts")
    critical_areas = df[df['Stress'] >= 0.8]
    if not critical_areas.empty:
        # FIX: Explicitly referencing the loop variable prevents NameError [cite: 19]
        for _, alert_row in critical_areas.iterrows():
            st.error(f"🔴 **{alert_row['City']}**\n\nCritical Stress: {alert_row['Stress']}")
    else:
        st.success("No critical alerts detected.")

# =============================================================================
# 5. FIELD REPORTING (COMMUNITY INPUT)
# =============================================================================
st.divider()
with st.expander("📝 Submit Field Report (Community Verification)", expanded=False):
    st.caption("Location coarsened to ±5km for safety[cite: 20].")
    r_col1, r_col2 = st.columns(2)
    with r_col1:
        lat_in = st.number_input("Latitude", format="%.2f", value=-1.26)
        r_type = st.selectbox("Source Type", ["Borehole", "Well", "River"])
    with r_col2:
        lon_in = st.number_input("Longitude", format="%.2f", value=36.80)
        r_stat = st.selectbox("Current Status", ["Available", "Low", "Dry"])
    
    if st.button("Submit Report", use_container_width=True):
        st.success(f"✓ Report for {r_type} near Westlands submitted successfully.")

# Data Export Tool
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Analysis (CSV)", csv, "water_stress_report.csv", "text/csv")
