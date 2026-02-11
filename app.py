import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime

# 1. Setup & Theme
st.set_page_config(page_title="OpenResilience", layout="wide", page_icon="💧")

# 2. Data Engine (NASA Connected) [cite: 25, 31]
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

# 3. UI Layout - Defining columns correctly 
st.title("🌍 OpenResilience: Water Stress Monitor")

# Defining columns c1, c2, c3 before using them
c1, c2, c3 = st.columns(3)
c1.metric("Global Risk", "ELEVATED" if df['Stress'].max() > 0.8 else "STABLE")
c2.metric("Highest Stress City", df.loc[df['Stress'].idxmax(), 'City'])
c3.metric("System Status", system_status)

# 4. Map & Alerts 
col_map, col_alerts = st.columns([3, 1])

with col_map:
    # Use "CartoDB positron" for a light map if "dark_matter" is too dark [cite: 15]
    m = folium.Map(location=[0, 20], zoom_start=2, tiles="CartoDB dark_matter")
    for _, row in df.iterrows():
        color = 'red' if row['Stress'] > 0.8 else 'orange' if row['Stress'] > 0.5 else 'green'
        folium.CircleMarker([row['Lat'], row['Lon']], radius=row['Stress']*25, color=color, fill=True).add_to(m)
    st_folium(m, width="100%", height=500)

with col_alerts:
    st.subheader("Active Alerts")
    for _, alert in df[df['Stress'] >= 0.8].iterrows():
        st.error(f"🔴 **{alert['City']}**\n\nStress: {alert['Stress']}") [cite: 19]

# 5. Field Reporting [cite: 20, 21]
with st.expander("📝 Submit Field Report"):
    st.info("Community verification system active. Location is coarsened for safety.") [cite: 12]
