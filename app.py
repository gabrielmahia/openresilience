# OpenResilience - Simplified Streamlit Edition
# Single-file water stress monitoring app
# © 2026 | Educational Use Only

import streamlit as st
import numpy as np
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta
import base64
from io import BytesIO
from PIL import Image

# =============================================================================
# CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="OpenResilience • Water Stress Map",
    layout="wide",
    page_icon="💧"
)

# Styling
st.markdown("""
<style>
    .stButton>button { 
        width: 100%; 
        border-radius: 4px; 
        height: 3em; 
        font-weight: 600; 
    }
    .alert-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 10px;
        margin: 10px 0;
        border-radius: 4px;
    }
    .info-box {
        background-color: #d1ecf1;
        border-left: 4px solid #0c5460;
        padding: 10px;
        margin: 10px 0;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SESSION STATE
# =============================================================================

if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.last_update = None
    st.session_state.wsi_data = None
    st.session_state.alerts = []
    st.session_state.confidence = "high"

# =============================================================================
# DATA GENERATION (Synthetic for Demo)
# =============================================================================

def generate_synthetic_data():
    """Generate synthetic water stress data for demonstration."""
    np.random.seed(42)
    
    # Create global grid (simplified)
    lats = np.linspace(90, -90, 180)
    lons = np.linspace(-180, 180, 360)
    
    # Generate WSI (Water Stress Index) values
    wsi = np.zeros((180, 360))
    
    # Add some stress patterns
    for _ in range(10):
        center_lat = np.random.randint(20, 160)
        center_lon = np.random.randint(20, 340)
        size = np.random.randint(10, 30)
        severity = np.random.choice([1, 2, 3], p=[0.5, 0.3, 0.2])
        
        for i in range(max(0, center_lat-size), min(180, center_lat+size)):
            for j in range(max(0, center_lon-size), min(360, center_lon+size)):
                dist = np.sqrt((i-center_lat)**2 + (j-center_lon)**2)
                if dist < size:
                    wsi[i, j] = max(wsi[i, j], severity)
    
    return wsi, lats, lons

def generate_alerts(wsi_data, lats, lons):
    """Generate alerts from WSI data."""
    alerts = []
    
    for i in range(0, len(lats), 5):  # Sample every 5 degrees
        for j in range(0, len(lons), 5):
            if wsi_data[i, j] >= 2:  # Warning or severe
                alerts.append({
                    'lat': lats[i],
                    'lon': lons[j],
                    'severity': int(wsi_data[i, j]),
                    'title': f"Water stress {'severe' if wsi_data[i,j] == 3 else 'elevated'}",
                    'region': f"Grid {lats[i]:.1f}°, {lons[j]:.1f}°"
                })
    
    return alerts[:100]  # Limit to 100 alerts

def create_tile_overlay(wsi_data):
    """Create a base64 encoded image overlay for the map."""
    # Color mapping: 0=transparent, 1=yellow, 2=orange, 3=red
    rgba = np.zeros((*wsi_data.shape, 4), dtype=np.uint8)
    rgba[wsi_data == 1] = [255, 204, 0, 160]   # Yellow
    rgba[wsi_data == 2] = [255, 128, 0, 180]   # Orange
    rgba[wsi_data == 3] = [255, 0, 0, 200]     # Red
    
    # Create image
    img = Image.fromarray(rgba, 'RGBA')
    
    # Resize for performance
    img = img.resize((720, 360), Image.NEAREST)
    
    # Convert to base64
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"

# =============================================================================
# MAIN APP
# =============================================================================

st.title("💧 OpenResilience • Water Stress Map")
st.caption("⚠️ Crisis signals are probabilistic. Always verify locally.")

# Disclaimer
with st.expander("⚠️ Important: Please Read", expanded=False):
    st.markdown("""
    **Educational Tool:** This is a demonstration system for educational purposes.
    
    **Data Source:** Currently using synthetic data for demonstration. In production, 
    this would use NASA IMERG precipitation and SMAP soil moisture data.
    
    **Verification:** Always verify water availability through local sources before 
    making any decisions. This tool provides risk signals, not definitive information.
    
    **Privacy:** Field reports use coarse geolocation (±5km) to protect exact water point locations.
    """)

# Sidebar
st.sidebar.header("Navigation & Controls")

# Quick jump locations
presets = {
    "Global View": (10, 0, 2),
    "Horn of Africa": (6.0, 43.0, 5),
    "Sahel Belt": (14.0, 0.0, 5),
    "Southern Africa": (-17.0, 28.0, 5),
    "India (Deccan)": (21.0, 78.0, 5),
    "US Southwest": (34.0, -112.0, 5),
}

selected_preset = st.sidebar.selectbox(
    "Quick Jump",
    list(presets.keys()),
    help="Jump to regions of interest"
)

# Alert filtering
severity_filter = st.sidebar.select_slider(
    "Minimum Alert Severity",
    options=["Watch (1)", "Warning (2)", "Severe (3)"],
    value="Warning (2)",
    help="Filter alerts by severity level"
)
severity_min = int(severity_filter.split("(")[1].split(")")[0])

# Data refresh
st.sidebar.subheader("Data Status")

if st.sidebar.button("🔄 Refresh Data", use_container_width=True):
    with st.spinner("Generating data..."):
        st.session_state.wsi_data, lats, lons = generate_synthetic_data()
        st.session_state.alerts = generate_alerts(st.session_state.wsi_data, lats, lons)
        st.session_state.last_update = datetime.now()
        st.session_state.initialized = True
        st.success("✓ Data updated!")

# Initialize data if needed
if not st.session_state.initialized:
    with st.spinner("Loading initial data..."):
        st.session_state.wsi_data, lats, lons = generate_synthetic_data()
        st.session_state.alerts = generate_alerts(st.session_state.wsi_data, lats, lons)
        st.session_state.last_update = datetime.now()
        st.session_state.initialized = True

# Show update time
if st.session_state.last_update:
    st.sidebar.info(f"**Last Update:** {st.session_state.last_update.strftime('%Y-%m-%d %H:%M')}")
    st.sidebar.caption(f"**Confidence:** {st.session_state.confidence.upper()}")
    st.sidebar.caption(f"**Data Source:** Synthetic (Demo)")

# =============================================================================
# MAIN LAYOUT
# =============================================================================

col_map, col_alerts = st.columns([3, 1])

with col_map:
    st.subheader("Global Water Stress Map")
    
    # Get preset coordinates
    lat, lon, zoom = presets[selected_preset]
    
    # Create map
    m = folium.Map(
        location=[lat, lon],
        zoom_start=zoom,
        tiles="CartoDB dark_matter"
    )
    
    # Add overlay if data exists
    if st.session_state.wsi_data is not None:
        # Create tile overlay
        tile_data = create_tile_overlay(st.session_state.wsi_data)
        
        folium.raster_layers.ImageOverlay(
            image=tile_data,
            bounds=[[-90, -180], [90, 180]],
            opacity=0.7,
            name="Water Stress Index"
        ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Display map
    st_folium(m, width=None, height=600, returned_objects=[])
    
    # Legend
    st.markdown("""
    **Legend:**  
    🟡 **Watch (1)** - Monitor conditions  
    🟠 **Warning (2)** - Elevated stress  
    🔴 **Severe (3)** - Critical stress
    """)

with col_alerts:
    st.subheader("Active Alerts")
    
    if st.session_state.alerts:
        # Filter alerts by severity
        filtered_alerts = [a for a in st.session_state.alerts if a['severity'] >= severity_min]
        
        st.caption(f"Showing {len(filtered_alerts)} alerts (severity ≥{severity_min})")
        
        # Display alerts
        for alert in filtered_alerts[:50]:  # Limit display
            severity_emoji = "🔴" if alert['severity'] == 3 else "🟠" if alert['severity'] == 2 else "🟡"
            
            with st.container():
                st.markdown(f"{severity_emoji} **{alert['title']}**")
                st.caption(f"Region: {alert['region']}")
                st.caption(f"Severity: {alert['severity']}/3")
                st.divider()
    else:
        st.info("No alerts at this severity level")

# =============================================================================
# FIELD REPORTING
# =============================================================================

st.divider()

with st.expander("📝 Submit Field Report (Community Input)", expanded=False):
    st.caption("Report water point status. Location is coarsened to ±5km for safety.")
    
    col_r1, col_r2 = st.columns(2)
    
    with col_r1:
        report_lat = st.number_input("Latitude", value=0.0, step=0.1, format="%.2f")
        report_type = st.selectbox("Type", ["Borehole", "Well", "River", "Other"])
    
    with col_r2:
        report_lon = st.number_input("Longitude", value=0.0, step=0.1, format="%.2f")
        report_status = st.selectbox("Status", ["Available", "Low", "Dry", "Inaccessible"])
    
    report_notes = st.text_area("Notes (optional)")
    
    if st.button("Submit Report", use_container_width=True):
        # Coarse geohash (simplified)
        coarse_lat = round(report_lat / 0.05) * 0.05
        coarse_lon = round(report_lon / 0.05) * 0.05
        
        st.success(f"✓ Report submitted! Coarse location: {coarse_lat:.2f}°, {coarse_lon:.2f}°")
        st.info("In production, this would be saved to a database for validation and aggregation.")

# =============================================================================
# INFORMATION & HELP
# =============================================================================

st.divider()

with st.expander("ℹ️ About This System", expanded=False):
    st.markdown("""
    ### Water Stress Index (WSI)
    
    Combines rainfall deficits and soil moisture to identify regions at risk of water stress.
    
    **Severity Levels:**
    - **Watch (1):** Conditions bear monitoring
    - **Warning (2):** Water stress elevated, verify local sources
    - **Severe (3):** Critical stress likely, coordinate response
    
    ### Data Sources (Production)
    
    - **NASA GPM IMERG:** Precipitation data (30min updates, 0.1° resolution)
    - **NASA SMAP:** Soil moisture data (3hr updates, 9km resolution)
    - **Updates:** Every 3 hours automatically
    
    ### Current Demo
    
    This demonstration uses synthetic data to show the system's capabilities.
    To use real NASA data, deploy the full production system (see documentation).
    
    ### Trust & Safety
    
    - All data includes timestamps and confidence scores
    - Field reports use coarse geolocation (±5km) to prevent weaponization
    - Signals are probabilistic - always verify locally
    
    ### Technical Details
    
    - **Grid Resolution:** 0.25° (~25-28km at equator)
    - **Update Frequency:** Configurable (default: 3 hours)
    - **Data Retention:** 30 days rolling window
    - **Backup:** Daily automated backups
    """)

with st.expander("🚀 Deploy Full Production System", expanded=False):
    st.markdown("""
    ### This Is a Simplified Demo
    
    For production deployment with:
    - Real NASA satellite data
    - Automatic scheduled updates
    - PostgreSQL database
    - Monitoring dashboards
    - Automated backups
    - API for external integration
    
    **See:** ZERO_INSTALL_GUIDE.md for complete deployment instructions
    
    **Or:** Use Railway/Render deployment for full system (no local install needed)
    
    ### Quick Deploy Full System:
    
    1. Upload code to GitHub (via web interface)
    2. Deploy to Railway (free tier)
    3. Deploy frontend to Streamlit Cloud
    4. Done! Fully automated water stress monitoring
    
    **Time:** 20 minutes | **Cost:** $0 (free tiers)
    """)

# Footer
st.divider()
st.caption("💧 OpenResilience • Water Stress Monitoring | Educational Use Only")
st.caption("© 2026 | Built with trust, resilience, and sovereignty in mind")
