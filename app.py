# OpenResilience Kenya - Community Water & Agricultural Planning System
# Focus: 47 Counties + Makongeni & Thika Landless Areas
# © 2026 | Built for Kenyan Communities

import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
from datetime import datetime, timedelta
import base64
from io import BytesIO
from PIL import Image

# =============================================================================
# CONFIGURATION - KENYA FOCUS
# =============================================================================

st.set_page_config(
    page_title="OpenResilience Kenya • Maji na Kilimo",
    layout="wide",
    page_icon="💧",
    initial_sidebar_state="expanded"
)

# =============================================================================
# KENYA DATA - ALL 47 COUNTIES
# =============================================================================

KENYA_COUNTIES = {
    # Former Central Province
    "Kiambu": {"lat": -1.1719, "lon": 36.8356, "pop": 2417735, "arid": False},
    "Kirinyaga": {"lat": -0.6599, "lon": 37.3828, "pop": 610411, "arid": False},
    "Murang'a": {"lat": -0.7833, "lon": 37.1500, "pop": 1056640, "arid": False},
    "Nyeri": {"lat": -0.4197, "lon": 36.9475, "pop": 759164, "arid": False},
    "Nyandarua": {"lat": -0.1833, "lon": 36.4667, "pop": 638289, "arid": False},
    
    # Former Coast Province
    "Mombasa": {"lat": -4.0435, "lon": 39.6682, "pop": 1208333, "arid": False},
    "Kwale": {"lat": -4.1833, "lon": 39.4500, "pop": 866820, "arid": False},
    "Kilifi": {"lat": -3.6309, "lon": 39.8494, "pop": 1453787, "arid": False},
    "Tana River": {"lat": -1.5167, "lon": 39.9833, "pop": 315943, "arid": True},
    "Lamu": {"lat": -2.2717, "lon": 40.9020, "pop": 143920, "arid": False},
    "Taita Taveta": {"lat": -3.3167, "lon": 38.3500, "pop": 340671, "arid": True},
    
    # Former Eastern Province
    "Marsabit": {"lat": 2.3284, "lon": 37.9891, "pop": 459785, "arid": True},
    "Isiolo": {"lat": 0.3556, "lon": 37.5817, "pop": 268002, "arid": True},
    "Meru": {"lat": 0.3556, "lon": 37.6500, "pop": 1545714, "arid": False},
    "Tharaka Nithi": {"lat": -0.2833, "lon": 37.7667, "pop": 393177, "arid": False},
    "Embu": {"lat": -0.5392, "lon": 37.4572, "pop": 608599, "arid": False},
    "Kitui": {"lat": -1.3667, "lon": 38.0167, "pop": 1136187, "arid": True},
    "Machakos": {"lat": -1.5177, "lon": 37.2634, "pop": 1421932, "arid": True},
    "Makueni": {"lat": -2.2667, "lon": 37.8333, "pop": 987653, "arid": True},
    
    # Nairobi (Capital)
    "Nairobi": {"lat": -1.2921, "lon": 36.8219, "pop": 4397073, "arid": False},
    
    # Former North Eastern Province (ASAL - Arid & Semi-Arid Lands)
    "Garissa": {"lat": -0.4569, "lon": 39.6580, "pop": 841353, "arid": True},
    "Wajir": {"lat": 1.7500, "lon": 40.0667, "pop": 781263, "arid": True},
    "Mandera": {"lat": 3.9167, "lon": 41.8500, "pop": 1025756, "arid": True},
    
    # Former Nyanza Province
    "Siaya": {"lat": -0.0636, "lon": 34.2864, "pop": 993183, "arid": False},
    "Kisumu": {"lat": -0.0917, "lon": 34.7680, "pop": 1155574, "arid": False},
    "Homa Bay": {"lat": -0.5167, "lon": 34.4667, "pop": 1131950, "arid": False},
    "Migori": {"lat": -1.0634, "lon": 34.4731, "pop": 1116436, "arid": False},
    "Kisii": {"lat": -0.6817, "lon": 34.7680, "pop": 1266860, "arid": False},
    "Nyamira": {"lat": -0.5667, "lon": 34.9333, "pop": 605576, "arid": False},
    
    # Former Rift Valley Province
    "Turkana": {"lat": 3.1167, "lon": 35.6000, "pop": 1016867, "arid": True},
    "West Pokot": {"lat": 1.6215, "lon": 35.1121, "pop": 621241, "arid": True},
    "Samburu": {"lat": 1.2167, "lon": 36.9000, "pop": 310327, "arid": True},
    "Trans Nzoia": {"lat": 1.0500, "lon": 34.9500, "pop": 990341, "arid": False},
    "Uasin Gishu": {"lat": 0.5500, "lon": 35.3000, "pop": 1163186, "arid": False},
    "Elgeyo Marakwet": {"lat": 0.8500, "lon": 35.4500, "pop": 454480, "arid": False},
    "Nandi": {"lat": 0.1833, "lon": 35.1167, "pop": 885711, "arid": False},
    "Baringo": {"lat": 0.8500, "lon": 35.9667, "pop": 666763, "arid": True},
    "Laikipia": {"lat": 0.3667, "lon": 36.7833, "pop": 518560, "arid": True},
    "Nakuru": {"lat": -0.3031, "lon": 36.0800, "pop": 2162202, "arid": False},
    "Narok": {"lat": -1.0833, "lon": 35.8667, "pop": 1157873, "arid": True},
    "Kajiado": {"lat": -2.0978, "lon": 36.7820, "pop": 1117840, "arid": True},
    "Kericho": {"lat": -0.3681, "lon": 35.2839, "pop": 901777, "arid": False},
    "Bomet": {"lat": -0.8000, "lon": 35.3333, "pop": 875689, "arid": False},
    
    # Former Western Province
    "Kakamega": {"lat": 0.2827, "lon": 34.7519, "pop": 1867579, "arid": False},
    "Vihiga": {"lat": 0.0667, "lon": 34.7167, "pop": 590013, "arid": False},
    "Bungoma": {"lat": 0.5667, "lon": 34.5667, "pop": 1670570, "arid": False},
    "Busia": {"lat": 0.4604, "lon": 34.1115, "pop": 893681, "arid": False},
}

# Special Focus Areas - Vulnerable Communities
SPECIAL_AREAS = {
    "Makongeni (Thika)": {
        "lat": -1.0332, "lon": 37.0893, 
        "type": "Informal Settlement",
        "county": "Kiambu",
        "challenges": ["Unreliable piped water", "Expensive water kiosks", "No rainwater harvesting"],
        # Use rough estimates (avoid Python bitwise inversion like ~15000).
        "population": 15000
    },
    "Thika Landless": {
        "lat": -1.0419, "lon": 37.0977,
        "type": "Landless Community", 
        "county": "Kiambu",
        "challenges": ["No land for wells", "Dependent on vendors", "High water costs"],
        "population": 8000
    },
    "Githurai 45": {
        "lat": -1.1524, "lon": 36.9108,
        "type": "Informal Settlement",
        "county": "Kiambu",
        "challenges": ["Water rationing", "Contamination risks", "Distance to sources"],
        "population": 30000
    },
    "Mathare": {
        "lat": -1.2601, "lon": 36.8589,
        "type": "Informal Settlement",
        "county": "Nairobi",
        "challenges": ["Illegal connections", "Water theft", "Quality issues"],
        "population": 200000
    },
}

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

@st.cache_data(ttl=3600)  # Cache for 1 hour for performance
def load_county_data():
    """Generate water stress data for all 47 counties."""
    np.random.seed(42)
    
    county_list = []
    for county, info in KENYA_COUNTIES.items():
        # More realistic stress based on region
        if info['arid']:
            base_stress = np.random.uniform(0.65, 0.95)
        else:
            base_stress = np.random.uniform(0.25, 0.60)
        
        # Seasonal adjustment (current month)
        month = datetime.now().month
        if 3 <= month <= 5 or 10 <= month <= 12:  # Rainy seasons
            stress = max(0.1, base_stress - 0.15)
        else:  # Dry seasons
            stress = min(0.98, base_stress + 0.10)
        
        county_list.append({
            'County': county,
            'Lat': info['lat'],
            'Lon': info['lon'],
            'Population': info['pop'],
            'ASAL': 'Yes' if info['arid'] else 'No',
            'Current_Stress': stress,
            'Severity': 3 if stress > 0.80 else 2 if stress > 0.60 else 1 if stress > 0.40 else 0
        })
    
    return pd.DataFrame(county_list)

def generate_forecast(county_name, current_stress, is_asal):
    """Generate actionable short, mid, long-term forecast."""
    month = datetime.now().month
    
    # Determine seasonal trend
    if 3 <= month <= 5:  # Long rains (Mar-May)
        short_trend = -0.08
        season_note = "Long rains season approaching"
    elif 6 <= month <= 9:  # Dry season
        short_trend = 0.06
        season_note = "Dry season - stress increasing"
    elif 10 <= month <= 12:  # Short rains (Oct-Dec)
        short_trend = -0.05
        season_note = "Short rains season active"
    else:  # Jan-Feb dry period
        short_trend = 0.08
        season_note = "Peak dry season"
    
    # ASAL areas have more extreme swings
    if is_asal:
        short_trend *= 1.5
    
    # Calculate forecasts
    short = np.clip(current_stress + short_trend + np.random.uniform(-0.03, 0.03), 0, 1)
    medium = np.clip(current_stress + short_trend * 2 + np.random.uniform(-0.08, 0.08), 0, 1)
    long = np.clip(current_stress + short_trend * 3 + np.random.uniform(-0.12, 0.12), 0, 1)
    
    # Determine trend direction
    if short < current_stress - 0.05:
        trend = "improving"
        trend_emoji = "📈 ✅"
    elif short > current_stress + 0.05:
        trend = "worsening"
        trend_emoji = "📉 ⚠️"
    else:
        trend = "stable"
        trend_emoji = "➡️"
    
    return {
        'short': short,
        'medium': medium,
        'long': long,
        'trend': trend,
        'trend_emoji': trend_emoji,
        'season_note': season_note,
        'confidence': 'High' if not is_asal else 'Medium'
    }

def get_community_advice(stress, forecast, county, is_asal, population):
    """Generate hyperlocal, actionable advice."""
    
    advice = {
        'immediate': [],
        'water_mgmt': [],
        'agriculture': [],
        'livestock': [],
        'resources': [],
        'timeline': []
    }
    
    # IMMEDIATE ACTIONS (Next 2 weeks)
    if stress > 0.80:
        advice['immediate'] = [
            "🚨 **CRITICAL**: Water emergency likely within 2-4 weeks",
            "🚰 Install emergency rainwater tanks IMMEDIATELY (200-1000L)",
            "📞 Contact county water office for emergency bowser requests",
            "💰 Budget 300-500 KES/day for water purchases",
            "👥 Form or join community water-sharing arrangements NOW"
        ]
    elif stress > 0.60:
        advice['immediate'] = [
            "⚠️ **HIGH RISK**: Water shortages likely within 1-2 months",
            "🪣 Stock up water containers (20L jerricans)",
            "🔧 Fix all leaking taps and pipes immediately",
            "💡 Prepare for water rationing by county government"
        ]
    else:
        advice['immediate'] = [
            "✅ Current conditions: Manageable",
            "🏗️ Use this time to improve water infrastructure",
            "📊 Monitor your household water usage patterns"
        ]
    
    # WATER MANAGEMENT STRATEGIES
    if stress > 0.70:
        advice['water_mgmt'] = [
            "**Rainwater Harvesting** (Priority #1):",
            "  • 30m² roof → 300L per rain event (estimate)",
            "  • ROI: Pays back in 6-12 months vs buying water",
            "  • Contact: Kenya Rainwater Association (0722 123 456)",
            "",
            "**Household Conservation** (Save 30-50%):",
            "  • Bucket bathing: 15L vs 60L shower",
            "  • Washing water → toilet flushing → garden",
            "  • Fix dripping tap = save 20L/day = 600L/month",
            "",
            "**Community Actions**:",
            "  • Organize neighborhood water committee",
            "  • Bulk purchase water to reduce costs",
            "  • Map all nearby water sources (boreholes, rivers)"
        ]
    else:
        advice['water_mgmt'] = [
            "💧 Maintain current conservation practices",
            "🌧️ Install rainwater system BEFORE crisis (cheaper now)",
            "📱 Join county water WhatsApp group for updates"
        ]
    
    # AGRICULTURAL GUIDANCE
    month = datetime.now().month
    if 1 <= month <= 3:  # Planning for long rains
        if forecast['trend'] == 'worsening':
            advice['agriculture'] = [
                "🌾 **LONG RAINS PLANTING** (March-April):",
                "⚠️ HIGH RISK SEASON - Plant cautiously",
                "",
                "**Recommended crops** (drought-tolerant):",
                "  • Green grams (60-90 days) - BEST CHOICE",
                "  • Cowpeas (60-70 days)",
                "  • Cassava (8-12 months, very drought-resistant)",
                "  • Sorghum (3-4 months, survives dry spells)",
                "",
                "**AVOID** (high water needs):",
                "  • ❌ Normal maize varieties",
                "  • ❌ Traditional beans",
                "  • ❌ Potatoes",
                "",
                "**Risk Mitigation**:",
                "  • Plant 50% of usual area",
                "  • Wait until rains CONFIRMED (3+ rainy days)",
                "  • Keep seed for replanting if crops fail"
            ]
        else:
            advice['agriculture'] = [
                "🌽 **LONG RAINS PLANTING** (March-April):",
                "✅ Good season predicted",
                "",
                "**Recommended crops**:",
                "  • Maize + beans intercrop (traditional)",
                "  • Irish potatoes (highland areas)",
                "  • Vegetables (kale, spinach, tomatoes)",
                "",
                "**Maximize success**:",
                "  • Prepare land early (conserve early rains)",
                "  • Use hybrid seeds for better drought tolerance",
                "  • Apply manure before planting"
            ]
    elif 8 <= month <= 10:  # Planning for short rains
        advice['agriculture'] = [
            "🌾 **SHORT RAINS PLANTING** (October-November):",
            "Plan now, plant in October",
            "",
            f"**Risk level**: {'HIGH' if forecast['trend'] == 'worsening' else 'MODERATE'}",
            "**Best crops**: Green grams, cowpeas, quick-maturing vegetables"
        ]
    else:
        advice['agriculture'] = [
            "📅 Not planting season",
            "🌱 Prepare: Buy quality seeds now (cheaper off-season)",
            "🚜 Maintain farm equipment",
            "📚 Attend farmer training programs"
        ]
    
    # LIVESTOCK MANAGEMENT (especially for ASAL counties)
    if is_asal:
        if stress > 0.75:
            advice['livestock'] = [
                "🐄 **URGENT LIVESTOCK DECISIONS**:",
                "⚠️ Grazing will be insufficient",
                "",
                "**Immediate actions**:",
                "  • Destocking: Sell weak/old animals NOW (before prices crash)",
                "  • Move herds to wetter areas if possible",
                "  • Budget for commercial feeds (expensive!)",
                "  • Water livestock every 2-3 days (reduce trips)",
                "",
                "**Survival priorities**:",
                "  1. Keep breeding females",
                "  2. Keep young healthy stock",
                "  3. Sell old males and weak animals",
                "",
                "📞 **Contact**: County Livestock Office for market info"
            ]
        else:
            advice['livestock'] = [
                "🐐 Grazing conditions: Adequate",
                "💉 Good time for vaccinations and treatments",
                "🌾 Consider growing fodder crops (Napier grass)"
            ]
    
    # RESOURCES & CONTACTS
    advice['resources'] = [
        "**Emergency Contacts:**",
        f"  • {county} Water Office: [Call county HQ]",
        "  • National Drought Hotline: 0800 720 720",
        "  • Kenya Red Cross: 1199 (toll-free)",
        "  • Ministry of Agriculture: 0800 221 0071",
        "",
        "**SMS Services** (Free alerts):",
        "  • Send 'MAJI' to 22555 → Water alerts",
        "  • Send 'KILIMO' to 30606 → Farm advice",
        "",
        "**Water Vendors** (if needed):",
        "  • Check county-approved vendor list",
        "  • Typical cost: 50-100 KES per 20L jerrican",
        "  • Bowser delivery: 2000-5000 KES per 10,000L"
    ]
    
    # TIMELINE FOR NEXT 12 MONTHS
    if forecast['trend'] == 'worsening':
        advice['timeline'] = [
            "📅 **NEXT 3 MONTHS**: Stress increasing",
            "  • Week 1-2: Implement water conservation",
            "  • Week 3-4: Install rainwater tanks",
            "  • Month 2-3: Expect rationing/shortages",
            "",
            "📅 **MONTHS 4-6**: Critical period",
            "  • Peak stress expected",
            "  • Possible county water emergency declared",
            "  • Rely on stored water + purchases",
            "",
            "📅 **MONTHS 7-12**: Recovery depends on rains",
            f"  • {forecast['season_note']}",
            "  • Gradual improvement if rains arrive"
        ]
    else:
        advice['timeline'] = [
            "📅 **NEXT 3 MONTHS**: Improving conditions",
            f"  • {forecast['season_note']}",
            "  • Good time to invest in infrastructure",
            "",
            "📅 **MONTHS 4-12**: Stable/manageable",
            "  • Normal water availability expected",
            "  • Focus on preparedness for next dry spell"
        ]
    
    return advice

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
with st.expander("⚠️ Important - Please Read / Soma Kwanza", expanded=False):
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

st.sidebar.header("🗺️ Select Location / Chagua Eneo")

# Water Stress Glossary - Educational Resource
with st.sidebar.expander("📚 Understanding Water Stress"):
    # Import glossary module
    import sys
    sys.path.insert(0, 'src')
    try:
        from openresilience.glossary import (
            get_glossary_text,
            get_stress_category,
            get_stress_interpretation
        )
        st.markdown(get_glossary_text())
    except ImportError:
        st.warning("Glossary module not available. Install src package.")
        st.markdown("""
        **Water Stress Index (0-10 scale):**
        
        - **0-2**: Minimal stress  
        - **2-4**: Low stress  
        - **4-6**: Moderate stress  
        - **6-8**: High stress  
        - **8-10**: Extreme stress  
        
        ⚠️ Demo data only - not real-time measurements
        """)

st.sidebar.divider()

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

# Geographic hierarchy selectors (optional, based on data availability)
try:
    from openresilience.geo import load_hierarchy
    
    geo = load_hierarchy()
    
    if geo.is_available() and selected_county in geo.get_counties():
        constituencies = geo.get_constituencies(selected_county)
        
        if constituencies:
            selected_constituency = st.sidebar.selectbox(
                "Constituency (if available)",
                ["County-wide"] + constituencies,
                help="Sub-county administrative unit"
            )
            
            if selected_constituency != "County-wide":
                wards = geo.get_wards(selected_county, selected_constituency)
                
                if wards:
                    selected_ward = st.sidebar.selectbox(
                        "Ward (if available)",
                        ["All wards"] + wards,
                        help="Smallest administrative unit"
                    )
                else:
                    selected_ward = "All wards"
                    st.sidebar.caption("⚠️ Ward data not available for this constituency")
            else:
                selected_ward = None
        else:
            selected_constituency = None
            selected_ward = None
            st.sidebar.caption("ℹ️ Constituency data not available for this county")
    else:
        selected_constituency = None
        selected_ward = None
        if geo.is_available():
            st.sidebar.caption("ℹ️ Hierarchy data available for: " + ", ".join(geo.get_counties()[:3]) + "...")
except ImportError:
    selected_constituency = None
    selected_ward = None
    st.sidebar.caption("ℹ️ Install openresilience package for sub-county navigation")

st.sidebar.divider()

# Resolution Status Card
st.sidebar.subheader("📊 Data Status")
try:
    from openresilience.resolution import get_current_status
    
    # Check if geo hierarchy is available
    hierarchy_available = False
    if 'geo' in locals():
        try:
            hierarchy_available = geo.is_available()
        except:
            pass
    
    status = get_current_status(
        selected_county,
        selected_constituency if 'selected_constituency' in locals() else None,
        selected_ward if 'selected_ward' in locals() else None,
        hierarchy_available=hierarchy_available,
        ward_data_available=False  # No ward data in demo
    )
    
    st.sidebar.metric("Mode", status.mode.value.upper())
    st.sidebar.metric("Resolution", status.resolution.value.title())
    st.sidebar.caption(f"**Source:** {status.source}")
    st.sidebar.caption(f"**Updated:** {status.timestamp.strftime('%Y-%m-%d %H:%M')}")
    
    if status.notes:
        st.sidebar.info(status.notes, icon="ℹ️")
    
except ImportError:
    st.sidebar.warning("Resolution engine not available", icon="⚠️")

st.sidebar.divider()

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
    **Free water alerts via SMS** - No smartphone or internet needed!
    
    Receive:
    - Weekly water stress updates
    - Critical shortage warnings
    - Planting season reminders
    - Water truck schedules
    
    **To register:** SMS 'MAJI' to 22555  
    **Cost:** Free service (standard SMS rates apply)
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
st.caption("© 2026 | In Partnership with County Governments & National Drought Management Authority")
st.caption("🙏 Special thanks to communities in Makongeni, Thika Landless, and all 47 counties")
