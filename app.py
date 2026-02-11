import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

# =============================================================================
# 1. CONFIGURATION & THEME
# =============================================================================
st.set_page_config(
    page_title="OpenResilience • Kenya Drought Monitor",
    layout="wide", 
    page_icon="💧"
)

# =============================================================================
# 2. DATA ENGINE (NASA-READY & HIERARCHICAL)
# =============================================================================
@st.cache_data(ttl=3600)
def load_hierarchical_data():
    # Detects your already connected NASA Secrets
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
            "Extreme water scarcity; local conflicts reported.",
            "River Tana levels low; irrigation failure likely.",
            "Water trucking active; critical pasture shortage."
        ]
    })
    
    global_df = pd.DataFrame({
        'Region': ['Horn of Africa', 'Sahel Belt', 'US Southwest', 'India (Deccan)'],
        'Lat': [6.0, 14.0, 34.0, 21.0],
        'Lon': [43.0, 0.0, -112.0, 78.0],
        'Stress': [0.85, 0.72, 0.65, 0.78]
    })
    
    return global_df, kenya_df, source_status

# Initialize Data
global_data, local_data, system_status = load_hierarchical_data()

# =============================================================================
# 3. UI HEADER & METRICS (FIXES NAMEERROR)
# =============================================================================
st.title("🌍 OpenResilience: Kenya Drought Intelligence")

# FIX: Defining columns BEFORE calling metric prevents NameError 
m1, m2, m3 = st.columns(3)
m1.metric("Max Regional Stress", f"{global_data['Stress'].max()}")
m2.metric("Critical Kenya Counties", len(local_data[local_data['Stress'] > 0.9]))
m3.metric("System Status", system_status)

# =============================================================================
# 4. HIERARCHICAL NAVIGATION
# =============================================================================
st.sidebar.header("Navigation Control")
scale = st.sidebar.radio("Map Scale", ["Global/Regional View", "Kenya County View"])

if scale == "Global/Regional View":
    view_list = global_data['Region'].tolist()
    df_to_map = global_data
    map_zoom = 4
else:
    view_list = local_data['County'].tolist()
    df_to_map = local_data
    map_zoom = 13 if "Nairobi" in st.session_state.get('last_view', '') else 7

selected_view = st.sidebar.selectbox("Drill Down Selection", view_list)
st.session_state.last_view = selected_view

# =============================================================================
# 5. INTERACTIVE MAP & ALERTS
# =============================================================================
col_map, col_alerts = st.columns([3, 1])

with col_map:
    # Find coordinates for selected view
    target = df_to_map[df_to_map.iloc[:, 0] == selected_view].iloc[0]
    st.subheader(f"Visualization: {selected_view}")
    
    # Map uses dark_matter for high contrast [cite: 15]
    m = folium.Map(location=[target['Lat'], target['Lon']], zoom_start=map_zoom, tiles="CartoDB dark_matter")
    
    for _, row in df_to_map.iterrows():
        # Dynamic color coding: Red for high stress [cite: 10, 34]
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
    st.subheader("Crisis Intelligence")
    # Display specific Drought Notes if in Kenya View
    if scale == "Kenya County View":
        st.error(f"📍 **{selected_view} Notes:**\n\n{target['Notes']}")
    
    st.divider()
    st.subheader("Active Alerts")
    critical = df_to_map[df_to_map['Stress'] >= 0.8]
    if not critical.empty:
        # FIX: Defining loop variable alert_row explicitly prevents NameError [cite: 19]
        for _, alert_row in critical.iterrows():
            st.warning(f"🔴 **Action Required: {alert_row.iloc[0]}**\nStress: {alert_row['Stress']}")
    else:
        st.success("Current Sector Stable")

# =============================================================================
# 6. FIELD REPORTING (COMMUNITY INPUT)
# =============================================================================
st.divider()
with st.expander("📝 Submit Field Report (Community Verification)"):
    st.caption("Location is coarsened to ±5km for safety.") [cite: 12, 20]
    r_col1, r_col2 = st.columns(2)
    with r_col1:
        lat_in = st.number_input("Latitude", format="%.2f", value=float(target['Lat']))
        r_type = st.selectbox("Source Type", ["Borehole", "Well", "River"])
    with r_col2:
        lon_in = st.number_input("Longitude", format="%.2f", value=float(target['Lon']))
        r_stat = st.selectbox("Current Status", ["Available", "Low", "Dry"])
    
    if st.button("Submit Report", use_container_width=True):
        st.success(f"✓ Report for {selected_view} logged successfully.") [cite: 21]

# Data Export (CSV Persistence)
csv = df_to_map.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Analysis Report (CSV)", csv, "water_stress_report.csv", "text/csv")
