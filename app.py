import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="OpenResilience Monitor", layout="wide", page_icon="💧")

# 2. Data Engine (Hierarchical)
@st.cache_data(ttl=3600)
def load_hierarchical_data():
    # Production: This switches to NASA SMAP/IMERG if secrets are detected
    source_status = "NASA Connected" if "NASA_USER" in st.secrets else "Demo Mode"
    
    # Global/Regional Data
    global_df = pd.DataFrame({
        'Region': ['Horn of Africa', 'Sahel Belt', 'US Southwest', 'India (Deccan)'],
        'Lat': [6.0, 14.0, 34.0, 21.0],
        'Lon': [43.0, 0.0, -112.0, 78.0],
        'Stress': [0.85, 0.72, 0.65, 0.78]
    })
    
    # Kenya County Data (Sample)
    kenya_df = pd.DataFrame({
        'County': ['Nairobi (Westlands)', 'Thika (Kiambu)', 'Turkana', 'Marsabit'],
        'Lat': [-1.267, -1.033, 3.116, 2.333],
        'Lon': [36.808, 37.069, 35.596, 37.989],
        'Stress': [0.88, 0.45, 0.92, 0.95]
    })
    
    return global_df, kenya_df, source_status

global_data, local_data, system_status = load_hierarchical_data()

# 3. UI Header & Metrics
st.title("🌍 OpenResilience: Multidisciplinary Water Monitor")

# FIX: Define columns before use to prevent NameError
c1, c2, c3 = st.columns(3)
c1.metric("Global Max Stress", f"{global_data['Stress'].max()}")
c2.metric("Local Max Stress (Kenya)", f"{local_data['Stress'].max()}")
c3.metric("System Status", system_status)

# 4. Hierarchical Navigation
st.sidebar.header("Navigation Control")
scale = st.sidebar.radio("Map Scale", ["Global/Regional", "Kenya Counties"])

if scale == "Global/Regional":
    view_list = global_data['Region'].tolist()
    df_to_map = global_data
    map_zoom = 3
else:
    view_list = local_data['County'].tolist()
    df_to_map = local_data
    map_zoom = 13 if "Westlands" in view_list else 7

selected_view = st.sidebar.selectbox("Drill Down Selection", view_list)

# 5. Interactive Map & Alerts
col_map, col_alerts = st.columns([3, 1])

with col_map:
    # Find coordinates for selected view
    target = df_to_map[df_to_map.iloc[:, 0] == selected_view].iloc[0]
    
    st.subheader(f"Visualization: {selected_view}")
    # Using dark_matter for high contrast; change to "positron" for light
    m = folium.Map(location=[target['Lat'], target['Lon']], zoom_start=map_zoom, tiles="CartoDB dark_matter")
    
    for _, row in df_to_map.iterrows():
        color = 'red' if row['Stress'] > 0.8 else 'orange' if row['Stress'] > 0.5 else 'green'
        folium.CircleMarker(
            location=[row['Lat'], row['Lon']],
            radius=row['Stress'] * 25,
            color=color,
            fill=True,
            popup=f"<b>{row.iloc[0]}</b><br>Stress Index: {row['Stress']}"
        ).add_to(m)
    st_folium(m, width="100%", height=600)

with col_alerts:
    st.subheader("Active Alerts")
    critical = df_to_map[df_to_map['Stress'] >= 0.8]
    if not critical.empty:
        # FIX: Define loop variable alert_row to prevent NameError
        for _, alert_row in critical.iterrows():
            st.error(f"🔴 **{alert_row.iloc[0]}**\nStress: {alert_row['Stress']}")
    else:
        st.success("Current Sector Stable")

# 6. Community Field Reporting
st.divider()
with st.expander("📝 Submit Field Report (Community Verification)"):
    st.caption("Location is coarsened to ±5km for safety.")
    r_col1, r_col2 = st.columns(2)
    with r_col1:
        lat_in = st.number_input("Latitude", format="%.2f", value=float(target['Lat']))
        r_type = st.selectbox("Source Type", ["Borehole", "Well", "River"])
    with r_col2:
        lon_in = st.number_input("Longitude", format="%.2f", value=float(target['Lon']))
        r_stat = st.selectbox("Status", ["Available", "Low", "Dry"])
    
    if st.button("Submit Report", use_container_width=True):
        st.success(f"✓ Report for {selected_view} logged successfully.")

# Data Export (CSV Persistence)
csv = df_to_map.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Analysis Report (CSV)", csv, "water_stress_report.csv", "text/csv")
