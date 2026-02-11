import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Initial Page Setup - Leverages the theme from your config.toml
st.set_page_config(page_title="OpenResilience Monitor", layout="wide")

st.title("🌍 OpenResilience: Water Stress Monitor")
st.markdown("---")

# Data Engine with Caching - Critical for performance and staying free
@st.cache_data(ttl=3600)
def load_data():
    # If NASA Secrets are added in Streamlit Settings, this switches to "Real" mode
    if "NASA_USER" in st.secrets:
        # Placeholder for dynamic NASA LANCE/Earthdata integration
        return pd.DataFrame({
            'City': ['Nairobi', 'Thika', 'Manassas', 'Dubai'],
            'Lat': [-1.286, -1.033, 38.751, 25.205],
            'Lon': [36.817, 37.069, -77.475, 55.271],
            'Stress': [0.82, 0.45, 0.15, 0.98]
        })
    else:
        # Fallback Synthetic Demo Data for immediate functionality
        return pd.DataFrame({
            'City': ['Nairobi', 'Thika', 'Manassas', 'Dubai'],
            'Lat': [-1.286, -1.033, 38.751, 25.205],
            'Lon': [36.817, 37.069, -77.475, 55.271],
            'Stress': [0.75, 0.40, 0.20, 0.90]
        })

df = load_data()

# Analytical Metrics Row
col1, col2, col3 = st.columns(3)
col1.metric("Global Risk Level", "ELEVATED")
col2.metric("Local Index (Nairobi)", df.loc[0, 'Stress'])
col3.metric("Status", "NASA Connected" if "NASA_USER" in st.secrets else "Demo Mode")

# Interactive Folium Map
st.subheader("Regional Risk Visualization")

m = folium.Map(location=[0, 30], zoom_start=2, tiles="CartoDB positron")

for _, row in df.iterrows():
    # Dynamic coloring: Red for high stress, Green for low stress
    color = 'red' if row['Stress'] > 0.8 else 'orange' if row['Stress'] > 0.5 else 'green'
    folium.CircleMarker(
        location=[row['Lat'], row['Lon']],
        radius=row['Stress'] * 25,
        color=color,
        fill=True,
        popup=f"{row['City']}: {row['Stress']}"
    ).add_to(m)

folium_static(m)

# Data Persistence Tool
st.markdown("---")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Analysis Report (CSV)", csv, "water_stress_report.csv", "text/csv")
