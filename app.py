# OpenResilience Kenya - Community Water & Agricultural Planning System
# Focus: 47 Counties + Makongeni & Thika Landless Areas
# © 2026 | Built for Kenyan Communities

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
from datetime import datetime, timedelta
import base64
from io import BytesIO
from PIL import Image

from openresilience.constants import KENYA_COUNTIES, SPECIAL_AREAS
from openresilience.data import load_county_data as _load_county_data, generate_forecast
from openresilience.models import get_community_advice


def get_data_mode():
    """Detect whether the system is running on real or demo data."""
    return os.environ.get("OR_DATA_MODE", "DEMO").upper()


DATA_MODE = get_data_mode()

# =============================================================================
# CONFIGURATION - KENYA FOCUS
# =============================================================================

st.set_page_config(
    page_title="OpenResilience Kenya • Maji na Kilimo",
    layout="wide",
    page_icon="💧",
    initial_sidebar_state="expanded"
)

# KENYA_COUNTIES and SPECIAL_AREAS imported from openresilience.constants

# Styling
st.markdown("""
<style>
    .stButton>button { 
        width: 100%; 
        border-radius: 6px; 
        height: 3em; 
        font-weight: 600; 
        transition: all 0.3s;
    }
    .forecast-good {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .forecast-warning {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .advice-card {
        background-color: #f8f9fa;
        border-left: 5px solid #28a745;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .critical-card {
        background-color: #fff3cd;
        border-left: 5px solid #dc3545;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
    }
    .special-area-badge {
        background-color: #6f42c1;
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.85em;
        font-weight: 600;
    }
    @media (prefers-color-scheme: dark) {
        .advice-card {
            background-color: #1e1e1e;
            border-left-color: #38ef7d;
        }
        .critical-card {
            background-color: #3a2929;
            border-left-color: #f5576c;
        }
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SESSION STATE & CACHING
# =============================================================================

if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.selected_county = "Nairobi"
    st.session_state.language = "English"

@st.cache_data(ttl=3600)
def load_county_data():
    """Cached wrapper around the extracted data loader."""
    return _load_county_data()

# =============================================================================
# MAIN APP
# =============================================================================

# Header
col_h1, col_h2 = st.columns([5, 1])
with col_h1:
    st.title("💧 OpenResilience Kenya")
    st.subheader("🇰🇪 Maji na Kilimo • Water & Agricultural Planning for 47 Counties")
with col_h2:
    lang = st.selectbox("", ["English", "Kiswahili"], label_visibility="collapsed")
    st.session_state.language = lang

# Load data
df = load_county_data()

# Disclaimer
with st.expander("⚠️ Important - Please Read / Soma Kwanza", expanded=True):
    if lang == "Kiswahili":
        st.markdown("""
        **Elimu Tu:** Zana ya elimu. Hakikisha taarifa na serikali kabla ya maamuzi.
        
        **Data:** Kwa sasa tunatumia data ya majaribio. Baadaye, data halisi ya NASA.
        
        **Uhakiki:** Thibitisha maji kupitia vyanzo vya karibu kabla ya hatua yoyote.
        """)
    else:
        st.markdown("""
        **Educational Tool:** For planning purposes. Verify with local authorities before major decisions.
        
        **Data:** Currently demonstration data. Production system uses real NASA satellite data (IMERG + SMAP).
        
        **Verification:** Always confirm water availability through local sources before acting.
        """)

st.divider()

# =============================================================================
# SIDEBAR - COUNTY & SPECIAL AREA SELECTION
# =============================================================================

# --- Data mode status card ---
_dm_color = "#dc3545" if DATA_MODE == "DEMO" else "#28a745"
_dm_label = "DEMO / Simulated" if DATA_MODE == "DEMO" else "REAL / Live"
st.sidebar.markdown(
    f"""<div style="background:{_dm_color};color:white;padding:10px 14px;
    border-radius:8px;text-align:center;font-weight:700;margin-bottom:12px;">
    Data Mode: {_dm_label}</div>""",
    unsafe_allow_html=True,
)
if DATA_MODE == "DEMO":
    st.sidebar.caption(
        "All values are simulated. Set env var OR_DATA_MODE=REAL when live adapters are connected."
    )
st.sidebar.divider()

st.sidebar.header("🗺️ Select Location / Chagua Eneo")

# Special areas first (Makongeni, Thika Landless, etc.)
st.sidebar.subheader("⭐ Special Focus: Vulnerable Communities")
special_area = st.sidebar.radio(
    "Landless & Informal Settlements",
    ["None"] + list(SPECIAL_AREAS.keys()),
    help="Areas with unique water challenges"
)

if special_area != "None":
    area_info = SPECIAL_AREAS[special_area]
    st.sidebar.markdown(f"""
    <div class="special-area-badge">{area_info['type'].upper()}</div>
    
    **Location**: {area_info['county']} County  
    **Population**: ~{area_info['population']:,}
    
    **Key Challenges**:
    """, unsafe_allow_html=True)
    for challenge in area_info['challenges']:
        st.sidebar.markdown(f"• {challenge}")

st.sidebar.divider()

# County selector
st.sidebar.subheader("📍 Select County / Chagua Kaunti")
selected_county = st.sidebar.selectbox(
    "47 Counties of Kenya",
    sorted(KENYA_COUNTIES.keys()),
    index=sorted(KENYA_COUNTIES.keys()).index("Nairobi")
)

# County stats
county_row = df[df['County'] == selected_county].iloc[0]
st.sidebar.metric("Population", f"{county_row['Population']:,}")
st.sidebar.metric("ASAL Status", county_row['ASAL'])
st.sidebar.metric("Current Stress", f"{county_row['Current_Stress']:.0%}")

severity_label = {
    3: "🔴 CRITICAL",
    2: "🟠 HIGH",
    1: "🟡 MODERATE",
    0: "🟢 LOW"
}[county_row['Severity']]
st.sidebar.metric("Risk Level", severity_label)

# =============================================================================
# MAIN CONTENT - FORECAST & GUIDANCE
# =============================================================================

# Generate forecast
is_asal = KENYA_COUNTIES[selected_county]['arid']
forecast = generate_forecast(
    selected_county,
    county_row['Current_Stress'],
    is_asal
)

# Key metrics row
st.subheader(f"📊 Water Stress Analysis: {selected_county} County")
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Current",
    f"{county_row['Current_Stress']:.0%}",
    delta=severity_label,
    delta_color="inverse"
)
col2.metric(
    "1-2 Months",
    f"{forecast['short']:.0%}",
    delta=f"{(forecast['short'] - county_row['Current_Stress']):.1%}",
    delta_color="inverse"
)
col3.metric(
    "3-6 Months",
    f"{forecast['medium']:.0%}",
    delta=f"{(forecast['medium'] - county_row['Current_Stress']):.1%}",
    delta_color="inverse"
)
col4.metric(
    "7-12 Months",
    f"{forecast['long']:.0%}",
    delta=f"{(forecast['long'] - county_row['Current_Stress']):.1%}",
    delta_color="inverse"
)
col5.metric(
    "Trend",
    forecast['trend'].title(),
    delta=forecast['season_note']
)

# Trend alert card
if forecast['trend'] == 'worsening':
    st.markdown(f"""
    <div class="forecast-warning">
        <h3>{forecast['trend_emoji']} ALERT: Water Stress Increasing</h3>
        <p style="font-size: 1.1em; margin: 10px 0;">
        <strong>{selected_county} County</strong> is expected to experience <strong>worsening water stress</strong> 
        over the next 6-12 months.
        </p>
        <p style="margin: 5px 0;">
        <strong>📅 Season:</strong> {forecast['season_note']}<br>
        <strong>🎯 Confidence:</strong> {forecast['confidence']}<br>
        <strong>⏰ Action needed:</strong> Immediate preparation recommended
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="forecast-good">
        <h3>{forecast['trend_emoji']} Good News: Conditions Improving</h3>
        <p style="font-size: 1.1em; margin: 10px 0;">
        <strong>{selected_county} County</strong> water stress is expected to <strong>improve or stabilize</strong> 
        over the next 6-12 months.
        </p>
        <p style="margin: 5px 0;">
        <strong>📅 Season:</strong> {forecast['season_note']}<br>
        <strong>🎯 Confidence:</strong> {forecast['confidence']}<br>
        <strong>💡 Recommendation:</strong> Maintain conservation, invest in infrastructure
        </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Two-column layout
col_map, col_advice = st.columns([2, 3])

with col_map:
    st.subheader("🗺️ Kenya Water Stress Map")
    
    # Create map
    m = folium.Map(
        location=[county_row['Lat'], county_row['Lon']],
        zoom_start=7,
        tiles="OpenStreetMap"
    )
    
    # Add all 47 counties
    for _, row in df.iterrows():
        color = 'red' if row['Severity'] >= 3 else 'orange' if row['Severity'] >= 2 else 'yellow' if row['Severity'] >= 1 else 'green'
        size = 12 if row['County'] == selected_county else 6
        
        folium.CircleMarker(
            location=[row['Lat'], row['Lon']],
            radius=size,
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.7 if row['County'] == selected_county else 0.5,
            popup=f"<b>{row['County']}</b><br>Stress: {row['Current_Stress']:.0%}<br>Pop: {row['Population']:,}",
            tooltip=row['County']
        ).add_to(m)
    
    # Add special areas with star markers
    for area, info in SPECIAL_AREAS.items():
        folium.Marker(
            location=[info['lat'], info['lon']],
            popup=f"<b>⭐ {area}</b><br>{info['type']}<br>Pop: ~{info['population']:,}",
            icon=folium.Icon(color='purple', icon='star'),
            tooltip=f"⭐ {area}"
        ).add_to(m)
    
    folium_static(m, width=500, height=500)
    
    st.caption("""
    **Legend:** 🔴 Critical (>80%) • 🟠 High (60-80%) • 🟡 Moderate (40-60%) • 🟢 Low (<40%)  
    ⭐ Purple stars = Special focus areas (Makongeni, Thika Landless, etc.)
    """)

with col_advice:
    st.subheader("📋 Practical Action Plan")
    
    # Generate detailed advice
    advice = get_community_advice(
        county_row['Current_Stress'],
        forecast,
        selected_county,
        is_asal,
        county_row['Population']
    )
    
    # Tabbed interface for different advice categories
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🚨 Immediate",
        "💧 Water",
        "🌾 Agriculture",
        "🐄 Livestock" if is_asal else "📅 Timeline",
        "📞 Resources"
    ])
    
    with tab1:
        for item in advice['immediate']:
            st.markdown(item)
    
    with tab2:
        for item in advice['water_mgmt']:
            st.markdown(item)
    
    with tab3:
        for item in advice['agriculture']:
            st.markdown(item)
    
    with tab4:
        items = advice['livestock'] if is_asal else advice['timeline']
        for item in items:
            st.markdown(item)
    
    with tab5:
        for item in advice['resources']:
            st.markdown(item)

st.divider()

# =============================================================================
# ADDITIONAL FEATURES
# =============================================================================

# County comparison table
with st.expander("📊 Compare All 47 Counties"):
    # Pandas styling gradients require matplotlib. If it's missing, fall back to a plain table.
    df_sorted = df.sort_values('Current_Stress', ascending=False)
    try:
        import matplotlib  # noqa: F401
        styled = (
            df_sorted.style
            .format({'Current_Stress': '{:.0%}', 'Population': '{:,.0f}'})
            .background_gradient(subset=['Current_Stress'], cmap='RdYlGn_r')
        )
        st.dataframe(styled, use_container_width=True, height=400)
    except Exception:
        st.warning("Table heatmap requires the optional dependency 'matplotlib'. Showing a plain table instead.")
        st.dataframe(
            df_sorted.assign(
                Current_Stress=(df_sorted['Current_Stress'] * 100).round(0).astype(int).astype(str) + "%"
            ),
            use_container_width=True,
            height=400
        )

# Community water point reporting
with st.expander("📝 Report Water Point Status (Community Reporting)"):
    st.caption("Help your community by reporting water availability. Location is coarsened for safety.")
    
    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        report_county = st.selectbox("County", sorted(KENYA_COUNTIES.keys()), key="rep_county")
    with col_r2:
        source_type = st.selectbox("Source", [
            "Borehole", "Well", "River", "Spring", "Water Kiosk",
            "County Piped", "Private Vendor", "Rainwater Tank"
        ])
    with col_r3:
        status = st.selectbox("Status", [
            "✅ Available (Normal)",
            "⚠️ Low/Rationed",
            "🕐 Long queues (1hr+)",
            "❌ Dry/Not working",
            "💰 Very expensive (>100 KES/20L)"
        ])
    
    queue_time = st.slider("Waiting time (minutes)", 0, 180, 15)
    cost = st.number_input("Cost per 20L jerrican (KES)", 0, 200, 50, 10)
    notes = st.text_area("Additional details (optional)")
    
    if st.button("Submit Report", use_container_width=True, type="primary"):
        st.success(f"✅ Report received for {report_county} County. Thank you!")
        st.info("In production: This data helps county governments allocate water trucks and prioritize infrastructure repairs.")

# SMS Alert Registration
st.divider()
col_sms1, col_sms2 = st.columns(2)

with col_sms1:
    st.subheader("📱 SMS Alert Service")
    st.info("""
    **Planned: Free water alerts via SMS** - No smartphone or internet needed!

    When active, you will receive:
    - Weekly water stress updates
    - Critical shortage warnings
    - Planting season reminders
    - Water truck schedules

    **Status:** SMS service is under development. Not yet active.
    """)

with col_sms2:
    st.subheader("👥 Join Community Groups")
    st.info("""
    **WhatsApp Groups** (by county):
    - Get local updates
    - Coordinate water purchases
    - Share vendor information
    - Emergency assistance
    
    **Contact your county water office** to join your area's WhatsApp group.
    
    Or form your own neighborhood water committee!
    """)

# Footer
st.divider()
st.caption("💧 OpenResilience Kenya • Built WITH and FOR Kenyan Communities")
st.caption("🇰🇪 Data Sovereignty • Community Resilience • Climate Adaptation • Agricultural Planning")
st.caption("© 2026 | Open-source research infrastructure — not affiliated with any government body")
st.caption("🙏 Special thanks to communities in Makongeni, Thika Landless, and all 47 counties")
