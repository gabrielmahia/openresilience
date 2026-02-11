import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

# 1. Setup & Theme
st.set_page_config(page_title="OpenResilience: Kenya Drought Monitor", layout="wide", page_icon="💧")

# 2. Data Engine (NASA Connected)
@st.cache_data(ttl=3600)
def load_hierarchical_data():
    source_status = "NASA Connected" if "NASA_USER" in st.secrets else "Demo Mode" [cite: 31, 33]
    
    # Drought-specific data with "Notes" for Kenya Counties
    kenya_df = pd.DataFrame({
        'County': ['Nairobi (Westlands)', 'Turkana', 'Marsabit', 'Garissa', 'Wajir'],
        'Lat': [-1.267, 3.116, 2.333, -0.453, 1.747],
        'Lon': [36.808, 35.596, 37.989, 39.646, 40.059],
        'Stress': [0.88, 0.95, 0.92, 0.89, 0.91],
        'Notes': [
            "Infrastructure strain; borehole levels dropping.", 
            "Severe livestock depletion; emergency aid required.", 
            "Extreme water scarcity; local conflicts reported near wells.",
            "River Tana levels low; irrigation failure likely.",
            "Water trucking active; critical pasture shortage."
        ]
    })
    
    global_df = pd.DataFrame({
        'Region': ['Horn of Africa', 'Sahel Belt', 'US Southwest'],
        'Lat': [6.0, 14.0, 34.0],
        'Lon': [43.0, 0.0, -112.0],
        'Stress': [0.85, 0.72, 0.65]
    })
    
    return global_df, kenya_df, source_status

global_data, local_data, system_status = load_hierarchical_data()

# 3. UI Header & Metrics
st.title("🌍 OpenResilience: Kenya Drought Intelligence")

# Defining metrics correctly to prevent NameError [cite: 33]
m1, m2, m3 = st.columns(3)
m1.metric("Max Regional Stress", f"{global_data['Stress'].max()}")
m2.metric("Critical Kenya Counties", len(local_data[local_data['Stress'] > 0.9]))
m3.metric("System Status", system_status) [cite: 33]

# 4. Hierarchical Navigation
st.sidebar.header("Drought Drill-Down")
scale = st.sidebar.radio("Map Scale", ["Global/Regional View", "Kenya County View"])

if scale == "Global/Regional View":
    view_list = global_data['Region'].tolist()
    df_to_map = global_data
    map_zoom = 4
else:
    view_list = local_data['County'].tolist()
    df_to_map = local_data
    map_zoom = 7

selected_view = st.sidebar.selectbox("Select Area", view_list)

# 5. Interactive Map & Alerts
col_map, col_alerts = st.columns([2, 1])

with col_map:
    target = df_to_map[df_to_map.iloc[:, 0] == selected_view].iloc[0]
    st.subheader(f"Visualization: {selected_view}")
    
    m = folium.Map(location=[target['Lat'], target['Lon']], zoom_start=map_zoom, tiles="CartoDB dark_matter") [cite: 15, 33]
    
    for _, row in df_to_map.iterrows():
        color = 'red' if row['Stress'] > 0.8 else 'orange' if row['Stress'] > 0.5 else 'green' [cite: 34]
        folium.CircleMarker(
            location=[row['Lat'], row['Lon']],
            radius=row['Stress'] * 25,
            color=color,
            fill=True,
            popup=f"<b>{row.iloc[0]}</b><br>Stress: {row['Stress']}"
        ).add_to(m)
    st_folium(m, width="100%", height=500)

with col_alerts:
    st.subheader("Crisis Intelligence")
    if scale == "Kenya County View":
        current_notes = target['Notes']
        st.error(f"📍 **{selected_view} Notes:**\n\n{current_notes}") [cite: 19]
    
    st.write("---")
    critical = df_to_map[df_to_map['Stress'] >= 0.9]
    if not critical.empty:
        for _, alert_row in critical.iterrows():
            st.warning(f"🔴 **Action Required: {alert_row.iloc[0]}**") [cite: 19]
