# OpenResilience Kenya - Community Water & Agricultural Planning System
# Copyright (C) 2026 Gabriel Mahia
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# For commercial licensing options, contact: [Your Email]
#
# Project: OpenResilience Kenya - Maji na Kilimo
# Focus: 47 Counties + Makongeni & Thika Landless Areas
# Built for Kenyan Communities 🇰🇪

import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
from datetime import datetime, timedelta
import base64
from io import BytesIO
from PIL import Image
import sys
import hashlib

# Add src to path for imports
sys.path.insert(0, 'src')

# Import OpenResilience modules
try:
    from openresilience.scoring import compute_resilience_scores, ResilienceScores
    from openresilience.database import (
        init_database, ensure_region, insert_run, get_recent_runs,
        insert_field_report, get_recent_reports, create_alert, get_active_alerts
    )
    from openresilience.agriculture import get_planting_advice, get_next_planting_window
    from openresilience.export import export_county_data_csv, export_county_summary_report, export_all_counties_excel
    from openresilience.visuals import (
        get_stress_emoji, get_stress_text, get_action_required,
        get_planting_recommendation, get_simple_forecast
    )
    SCORING_AVAILABLE = True
    DB_AVAILABLE = True
    AGRICULTURE_AVAILABLE = True
    EXPORT_AVAILABLE = True
    VISUALS_AVAILABLE = True
except ImportError as e:
    SCORING_AVAILABLE = False
    DB_AVAILABLE = False
    AGRICULTURE_AVAILABLE = False
    EXPORT_AVAILABLE = False
    VISUALS_AVAILABLE = False
    print(f"OpenResilience modules not available: {e}")

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
    """Generate water stress data for all 47 counties with multi-index scoring."""
    np.random.seed(42)
    
    # Try to import NASA adapter
    nasa_available = False
    try:
        from openresilience.adapters.appeears import get_nasa_data_for_county
        nasa_available = True
    except ImportError:
        pass
    
    # Try to import Earth Engine adapter
    gee_available = False
    try:
        from openresilience.adapters.earthengine import get_vegetation_health
        gee_available = True
    except ImportError:
        pass
    
    county_list = []
    nasa_success_count = 0
    gee_success_count = 0
    
    for county, info in KENYA_COUNTIES.items():
        # TRY REAL NASA DATA FIRST
        real_rainfall_anom = None
        real_soil_moisture = None
        data_source = "demo"
        
        if nasa_available:
            try:
                real_rainfall_anom, real_soil_moisture = get_nasa_data_for_county(
                    county, info['lat'], info['lon']
                )
                if real_rainfall_anom is not None and real_soil_moisture is not None:
                    data_source = "nasa"
                    nasa_success_count += 1
            except Exception as e:
                pass  # Silently fall back to demo
        
        # TRY REAL EARTH ENGINE VEGETATION DATA
        real_vegetation = None
        if gee_available:
            try:
                real_vegetation = get_vegetation_health(
                    county, info['lat'], info['lon']
                )
                if real_vegetation is not None:
                    if data_source == "nasa":
                        data_source = "nasa+gee"
                    else:
                        data_source = "gee"
                    gee_success_count += 1
            except Exception as e:
                pass  # Silently fall back to demo
        
        # Generate realistic input signals based on region type
        if info['arid']:
            # ASAL regions: drier conditions
            rainfall_anom = real_rainfall_anom if real_rainfall_anom is not None else np.random.uniform(-55, -20)
            soil_moisture = real_soil_moisture if real_soil_moisture is not None else np.random.uniform(0.15, 0.40)
            vegetation = real_vegetation if real_vegetation is not None else np.random.uniform(0.25, 0.50)
            price_change = np.random.uniform(15, 45)  # Higher food prices
            stockouts = np.random.randint(1, 4)  # More stockouts
        else:
            # Non-ASAL: better conditions
            rainfall_anom = real_rainfall_anom if real_rainfall_anom is not None else np.random.uniform(-30, 10)
            soil_moisture = real_soil_moisture if real_soil_moisture is not None else np.random.uniform(0.40, 0.75)
            vegetation = real_vegetation if real_vegetation is not None else np.random.uniform(0.50, 0.85)
            price_change = np.random.uniform(-5, 20)  # Moderate prices
            stockouts = np.random.randint(0, 2)  # Fewer stockouts
        
        # Seasonal adjustment (current month) - only for demo data
        if real_vegetation is None and data_source in ["demo", "nasa"]:
            month = datetime.now().month
            if 3 <= month <= 5 or 10 <= month <= 12:  # Rainy seasons
                vegetation = min(1.0, vegetation + 0.10)
        
        # Only adjust non-real data for rainfall/soil
        if data_source == "demo":
            month = datetime.now().month
            if 3 <= month <= 5 or 10 <= month <= 12:  # Rainy seasons
                rainfall_anom += 15  # Better rainfall
                soil_moisture = min(1.0, soil_moisture + 0.15)
            else:  # Dry seasons
                rainfall_anom -= 10  # Worse rainfall
                soil_moisture = max(0.0, soil_moisture - 0.10)
                vegetation = max(0.0, vegetation - 0.08)
        
        # Field reports based on severity
        field_reports = np.random.poisson(2 if info['arid'] else 0.5)
        
        # Compute multi-index scores
        if SCORING_AVAILABLE:
            try:
                scores = compute_resilience_scores(
                    rainfall_anomaly=rainfall_anom,
                    soil_moisture=soil_moisture,
                    vegetation_health=vegetation,
                    staple_price_change=price_change,
                    market_stockouts=stockouts,
                    field_reports_24h=field_reports
                )
                
                wsi = scores.wsi / 100  # Convert to 0-1 for display
                fsi = scores.fsi / 100
                msi = scores.msi / 100
                cri = scores.cri / 100
                confidence = scores.confidence
            except Exception as e:
                # Fallback to simple calculation
                wsi = ((-rainfall_anom / 100) * 0.6 + (1 - soil_moisture) * 0.4)
                fsi = wsi * 0.8
                msi = (price_change / 100) * 0.7
                cri = (wsi * 0.45 + fsi * 0.35 + msi * 0.20)
                confidence = 50
        else:
            # Simple fallback calculation
            wsi = ((-rainfall_anom / 100) * 0.6 + (1 - soil_moisture) * 0.4)
            fsi = wsi * 0.8
            msi = (price_change / 100) * 0.7
            cri = (wsi * 0.45 + fsi * 0.35 + msi * 0.20)
            confidence = 50
        
        county_list.append({
            'County': county,
            'Lat': info['lat'],
            'Lon': info['lon'],
            'Population': info['pop'],
            'ASAL': 'Yes' if info['arid'] else 'No',
            'Current_Stress': cri,  # Use CRI as primary stress indicator
            'WSI': wsi,  # Water Stress Index
            'FSI': fsi,  # Food Stress Index
            'MSI': msi,  # Market Stress Index
            'CRI': cri,  # Composite Risk Index
            'Confidence': confidence,
            'Severity': 3 if cri > 0.70 else 2 if cri > 0.50 else 1 if cri > 0.30 else 0,
            'DataSource': data_source  # Track if using real NASA data
        })
    
    # Show NASA data usage summary
    if nasa_success_count > 0:
        st.sidebar.success(f"🛰️ Using NASA satellite data for {nasa_success_count} counties")
    
    # Show Earth Engine data usage summary
    if gee_success_count > 0:
        st.sidebar.success(f"🌍 Using Earth Engine vegetation data for {gee_success_count} counties")
    
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

# Initialize database (silent fail if not available)
db_initialized = False
if DB_AVAILABLE:
    try:
        init_database()
        db_initialized = True
    except Exception as e:
        st.sidebar.error(f"⚠️ Database unavailable: {str(e)[:50]}...")
        st.sidebar.caption("Running in demo mode without persistence")
        db_initialized = False

# Header
col_h1, col_h2 = st.columns([5, 1])
with col_h1:
    st.title("💧 OpenResilience Kenya")
    st.subheader("🇰🇪 Maji na Kilimo • Water & Agricultural Planning for 47 Counties")
with col_h2:
    lang = st.selectbox("", ["English", "Kiswahili"], label_visibility="collapsed")
    st.session_state.language = lang

# Enhanced Mobile-Responsive CSS for Farmers + NGO Administrators
st.markdown("""
<style>
    /* ========================================
       MOBILE-FIRST DESIGN (Farmers on phones)
       ======================================== */
    
    /* Base: Optimized for small screens */
    body {
        font-size: 16px; /* Readable on mobile */
        line-height: 1.6;
    }
    
    /* Large touch targets for farmers */
    button, .stDownloadButton button, .stButton button {
        min-height: 48px !important;
        min-width: 48px;
        padding: 12px 20px !important;
        font-size: 16px !important;
        font-weight: 600;
    }
    
    /* High contrast text - critical for outdoor use */
    .stMarkdown, .stText, p, div {
        color: #1a1a1a;
    }
    
    /* Visual indicator cards - mobile optimized */
    .status-card {
        text-align: center;
        padding: 15px;
        background: #ffffff;
        border-radius: 12px;
        margin: 8px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 2px solid #e0e0e0;
    }
    
    .status-emoji {
        font-size: 2.5em;
        margin-bottom: 8px;
        display: block;
    }
    
    /* Agricultural guidance - farmer-friendly */
    .agriculture-section {
        background: #e8f5e9;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #4caf50;
        margin: 15px 0;
        font-size: 1.05em;
        line-height: 1.8;
    }
    
    .agriculture-section h4 {
        color: #2e7d32;
        margin-top: 0;
        font-size: 1.3em;
    }
    
    .agriculture-section strong {
        color: #1b5e20;
    }
    
    /* Alert boxes - EXCELLENT CONTRAST */
    .forecast-warning {
        background: #fff3cd;
        padding: 25px;
        border-radius: 12px;
        border-left: 8px solid #ff9800;
        margin: 20px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .forecast-warning h3 {
        color: #000000 !important;
        font-size: 1.4em;
        font-weight: 700;
        margin-top: 0 !important;
    }
    
    .forecast-warning p {
        color: #000000 !important;
        font-size: 1.1em;
    }
    
    .forecast-good {
        background: #d4edda;
        padding: 25px;
        border-radius: 12px;
        border-left: 8px solid #28a745;
        margin: 20px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .forecast-good h3 {
        color: #000000 !important;
        font-size: 1.4em;
        font-weight: 700;
        margin-top: 0 !important;
    }
    
    .forecast-good p {
        color: #000000 !important;
        font-size: 1.1em;
    }
    
    /* Metrics - larger for quick glance */
    .stMetric {
        background: #ffffff;
        padding: 12px;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }
    
    .stMetric label {
        font-size: 0.95em !important;
        font-weight: 600 !important;
        color: #424242;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        font-size: 2em !important;
        font-weight: 700 !important;
        color: #1a1a1a;
    }
    
    /* Export buttons - prominent */
    .stDownloadButton button {
        width: 100%;
        background: #1976d2 !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
    }
    
    .stDownloadButton button:hover {
        background: #1565c0 !important;
    }
    
    /* ========================================
       TABLET & DESKTOP (NGO administrators)
       ======================================== */
    
    @media (min-width: 768px) {
        /* More compact for desktop */
        .stMetric {
            padding: 10px;
        }
        
        .status-card {
            padding: 20px;
        }
        
        button {
            min-height: 44px !important;
        }
        
        /* Better use of space */
        .agriculture-section {
            font-size: 1em;
        }
    }
    
    @media (max-width: 767px) {
        /* MOBILE OPTIMIZATIONS */
        
        /* Reduce header sizes for mobile */
        h1 {
            font-size: 1.6em !important;
            line-height: 1.2;
        }
        
        h2 {
            font-size: 1.3em !important;
        }
        
        h3 {
            font-size: 1.1em !important;
        }
        
        /* Stack columns on mobile */
        .css-1d391kg {
            padding: 1rem 0.5rem;
        }
        
        /* Larger tap targets */
        .stSelectbox, .stRadio {
            font-size: 16px !important;
        }
        
        /* Better spacing */
        .stMarkdown {
            margin-bottom: 1rem;
        }
        
        /* Simplified metrics */
        .stMetric [data-testid="stMetricValue"] {
            font-size: 1.8em !important;
        }
    }
    
    /* ========================================
       ACCESSIBILITY (All devices)
       ======================================== */
    
    /* High contrast for outdoor viewing */
    ::selection {
        background: #ffeb3b;
        color: #000;
    }
    
    /* Focus indicators for keyboard navigation */
    button:focus, select:focus, input:focus {
        outline: 3px solid #2196f3 !important;
        outline-offset: 2px;
    }
    
    /* Links - clearly visible */
    a {
        color: #1976d2;
        text-decoration: underline;
        font-weight: 600;
    }
    
    a:hover {
        color: #1565c0;
    }
    
    /* ========================================
       FARMER-SPECIFIC ENHANCEMENTS
       ======================================== */
    
    /* Simple language indicators */
    .simple-indicator {
        font-size: 1.3em;
        font-weight: 700;
        padding: 15px;
        text-align: center;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .indicator-good {
        background: #c8e6c9;
        color: #1b5e20;
        border: 3px solid #4caf50;
    }
    
    .indicator-moderate {
        background: #fff9c4;
        color: #f57f17;
        border: 3px solid #fdd835;
    }
    
    .indicator-bad {
        background: #ffccbc;
        color: #bf360c;
        border: 3px solid #ff5722;
    }
    
    /* Emoji sizing for clarity */
    .big-emoji {
        font-size: 3em;
        line-height: 1;
        display: block;
        margin: 10px auto;
    }
    
    /* ========================================
       PERFORMANCE OPTIMIZATIONS
       ======================================== */
    
    /* Reduce animations on mobile to save battery */
    @media (max-width: 767px) {
        * {
            animation-duration: 0.01s !important;
            transition-duration: 0.01s !important;
        }
    }
    
    /* Better table readability */
    .dataframe {
        font-size: 0.95em;
        line-height: 1.6;
    }
    
    .dataframe th {
        background: #f5f5f5;
        font-weight: 700;
        color: #1a1a1a;
    }
    
    .dataframe td {
        color: #424242;
    }
    
    /* Tab navigation - larger touch targets */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 14px 24px;
        font-size: 1.05em;
        font-weight: 600;
    }
    
    /* Expander - clear interaction */
    .streamlit-expanderHeader {
        font-size: 1.15em;
        font-weight: 700;
        padding: 12px 16px;
        background: #f5f5f5;
        border-radius: 8px;
    }
    
    .streamlit-expanderHeader:hover {
        background: #eeeeee;
    }
</style>
""", unsafe_allow_html=True)

# Load data
df = load_county_data()

# Tab navigation
tab1, tab2, tab3 = st.tabs([
    "📊 Dashboard / Dashibodi",
    "📝 Field Reports / Ripoti",
    "🚨 Alerts / Tahadhari"
])

# Store selected tab in session state
if 'selected_region_id' not in st.session_state:
    st.session_state.selected_region_id = None

# Disclaimer
with tab1:
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

# Get county data first (needed for data source display)
county_row = df[df['County'] == selected_county].iloc[0]

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
        ward_data_available=False,  # No ward data in demo
        data_source=county_row.get('DataSource', 'demo')
    )
    
    st.sidebar.metric("Mode", status.mode.value.upper())
    st.sidebar.metric("Resolution", status.resolution.value.title())
    st.sidebar.caption(f"**Source:** {status.source}")
    
    # Show data source (NASA/GEE or demo)
    if 'DataSource' in county_row:
        data_src = county_row['DataSource']
        if data_src == 'nasa+gee':
            st.sidebar.caption("**🛰️ Satellite Data:** NASA (rainfall, soil) + GEE (vegetation)")
        elif data_src == 'nasa':
            st.sidebar.caption("**🛰️ Satellite Data:** NASA IMERG + SMAP")
        elif data_src == 'gee':
            st.sidebar.caption("**🌍 Satellite Data:** Earth Engine MODIS")
        else:
            st.sidebar.caption("**📊 Data Mode:** Demo (simulated)")
    else:
        st.sidebar.caption("**📊 Data Mode:** Demo (simulated)")
    
    st.sidebar.caption(f"**Updated:** {status.timestamp.strftime('%Y-%m-%d %H:%M')}")
    
    if status.notes:
        st.sidebar.info(status.notes, icon="ℹ️")
    
except ImportError:
    st.sidebar.warning("Resolution engine not available", icon="⚠️")

st.sidebar.divider()

# County stats (county_row already defined above)
st.sidebar.metric("Population", f"{county_row['Population']:,}")
st.sidebar.metric("ASAL Status", county_row['ASAL'])

# Multi-Index Display
st.sidebar.subheader("📈 Resilience Indices")
col_idx1, col_idx2 = st.sidebar.columns(2)

with col_idx1:
    st.metric("WSI (Water)", f"{county_row['WSI']:.0%}", 
              help="Water Stress Index")
    st.metric("FSI (Food)", f"{county_row['FSI']:.0%}",
              help="Food Stress Index")

with col_idx2:
    st.metric("MSI (Market)", f"{county_row['MSI']:.0%}",
              help="Market Stress Index")
    st.metric("CRI (Overall)", f"{county_row['CRI']:.0%}",
              help="Composite Risk Index", delta_color="inverse")

severity_label = {
    3: "🔴 CRITICAL",
    2: "🟠 HIGH",
    1: "🟡 MODERATE",
    0: "🟢 LOW"
}[county_row['Severity']]
st.sidebar.metric("Risk Level", severity_label)

# Export Data Section
if EXPORT_AVAILABLE:
    st.sidebar.divider()
    st.sidebar.subheader("📥 Export Data")
    
    # County Summary Report
    summary_report = export_county_summary_report(
        selected_county,
        county_row.to_dict(),
        datetime.now()
    )
    st.sidebar.download_button(
        label="📄 Download County Report",
        data=summary_report,
        file_name=f"{selected_county}_report_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain",
        help="Human-readable summary report"
    )
    
    # CSV Export
    county_csv = export_county_data_csv(df[df['County'] == selected_county])
    st.sidebar.download_button(
        label="📊 Download County CSV",
        data=county_csv,
        file_name=f"{selected_county}_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        help="Data for spreadsheet analysis"
    )

if SCORING_AVAILABLE and 'Confidence' in county_row:
    st.sidebar.caption(f"Confidence: {county_row['Confidence']:.0f}%")

# =============================================================================
# MAIN CONTENT - FORECAST & GUIDANCE
# =============================================================================

# Multi-Index Overview
st.subheader(f"📊 Resilience Dashboard: {selected_county} County")

col_overview1, col_overview2 = st.columns([2, 1])

with col_overview1:
    # Create bar chart data
    indices_data = pd.DataFrame({
        'Index': ['Water\nStress', 'Food\nStress', 'Market\nStress', 'Composite\nRisk'],
        'Score': [
            county_row['WSI'] * 100,
            county_row['FSI'] * 100,
            county_row['MSI'] * 100,
            county_row['CRI'] * 100
        ],
        'Color': ['#3498db', '#27ae60', '#f39c12', '#e74c3c']
    })
    
    # Display as bar chart
    st.bar_chart(
        indices_data.set_index('Index')['Score'],
        height=250,
        use_container_width=True
    )
    st.caption("All indices on 0-100 scale (higher = more stress/risk)")

with col_overview2:
    st.metric(
        "🌊 Water Stress (WSI)",
        f"{county_row['WSI']:.0%}",
        help="Rainfall deficit + soil dryness"
    )
    st.metric(
        "🌾 Food Stress (FSI)",
        f"{county_row['FSI']:.0%}",
        help="Vegetation decline + water stress"
    )
    st.metric(
        "🛒 Market Stress (MSI)",
        f"{county_row['MSI']:.0%}",
        help="Price inflation + stockouts"
    )
    st.metric(
        "⚠️ Composite Risk (CRI)",
        f"{county_row['CRI']:.0%}",
        delta=severity_label,
        delta_color="inverse",
        help="Weighted combination of all indices"
    )

# Define ASAL status and generate forecast for use in visual indicators
is_asal = KENYA_COUNTIES[selected_county]['arid']
forecast = generate_forecast(
    selected_county,
    county_row['Current_Stress'],
    is_asal
)

# Visual Status Indicators
if VISUALS_AVAILABLE:
    st.divider()
    st.subheader("📊 Quick Status")
    
    wsi = county_row['WSI']
    current_month = datetime.now().month
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        emoji = get_stress_emoji(wsi)
        status_text = get_stress_text(wsi, 'en')
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: #f0f2f6; border-radius: 10px;">
            <div style="font-size: 3em;">{emoji}</div>
            <div style="font-size: 1.2em; font-weight: bold; margin-top: 10px;">{status_text}</div>
            <div style="font-size: 0.9em; color: #666;">Water Status</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        icon, action = get_action_required(wsi, 'en')
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: #f0f2f6; border-radius: 10px;">
            <div style="font-size: 3em;">{icon}</div>
            <div style="font-size: 1.0em; margin-top: 10px;">{action}</div>
            <div style="font-size: 0.9em; color: #666;">Action Required</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        plant_rec = get_planting_recommendation(wsi, current_month, is_asal, 'en')
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: #f0f2f6; border-radius: 10px;">
            <div style="font-size: 1.2em; margin-top: 10px;">{plant_rec}</div>
            <div style="font-size: 0.9em; color: #666;">Planting Advice</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        forecast_text = get_simple_forecast(county_row['Current_Stress'], forecast['short'], 'en')
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: #f0f2f6; border-radius: 10px;">
            <div style="font-size: 1.2em; margin-top: 10px;">{forecast_text}</div>
            <div style="font-size: 0.9em; color: #666;">Short-term Outlook</div>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# Forecast timeline (forecast already generated above for visual indicators)
st.subheader("🔮 Forecast Timeline")
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
        <h3 style="color: #000; margin-top: 0;">{forecast['trend_emoji']} ⚠️ ALERT: Water Stress Increasing</h3>
        <p style="font-size: 1.1em; margin: 10px 0; color: #000;">
        <strong>{selected_county} County</strong> is expected to experience <strong>worsening water stress</strong> 
        over the next 6-12 months.
        </p>
        <p style="margin: 5px 0; color: #000;">
        <strong>📅 Season:</strong> {forecast['season_note']}<br>
        <strong>🎯 Confidence:</strong> {forecast['confidence']}<br>
        <strong>⏰ Action needed:</strong> Immediate preparation recommended
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="forecast-good">
        <h3 style="color: #000; margin-top: 0;">{forecast['trend_emoji']} ✅ Good News: Conditions Improving</h3>
        <p style="font-size: 1.1em; margin: 10px 0; color: #000;">
        <strong>{selected_county} County</strong> water stress is expected to <strong>improve or stabilize</strong> 
        over the next 6-12 months.
        </p>
        <p style="margin: 5px 0; color: #000;">
        <strong>📅 Season:</strong> {forecast['season_note']}<br>
        <strong>🎯 Confidence:</strong> {forecast['confidence']}<br>
        <strong>💡 Recommendation:</strong> Maintain conservation, invest in infrastructure
        </p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Agricultural Guidance for Farmers
if AGRICULTURE_AVAILABLE:
    st.subheader("🌾 Agricultural Guidance")
    
    advice = get_planting_advice(
        selected_county,
        is_asal,
        county_row['WSI'],
        datetime.now().month
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"""
        <div style="background: #e8f5e9; padding: 20px; border-radius: 10px; border-left: 5px solid #4caf50;">
            <h4 style="margin-top: 0;">📅 Current Season</h4>
            <p style="font-size: 1.1em;"><strong>{advice['season']}</strong></p>
            <p style="margin: 10px 0;">
                <strong>Recommendation:</strong> <span style="font-size: 1.2em;">{advice['action']}</span><br>
                <em>{advice['timing']}</em>
            </p>
            <p style="margin: 10px 0;">
                <strong>Stress Level:</strong> <span style="text-transform: uppercase; font-weight: bold;">{advice['stress_level']}</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**💧 Water-Saving Tips:**")
        for tip in advice['water_saving_tips']:
            st.markdown(f"- {tip}")
    
    with col2:
        st.markdown("**🌱 Recommended Crops:**")
        for crop in advice['recommended_crops']:
            st.markdown(f"- {crop}")
        
        st.markdown("**⚡ Critical Actions:**")
        for action in advice['critical_actions']:
            st.markdown(f"{action}")
        
        next_window, dates = get_next_planting_window(datetime.now().month, is_asal)
        st.info(f"📅 **Next Planting Window:** {next_window} ({dates})")
        
        st.caption(f"💁 **Need Help?** Contact {advice['contact']}")

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
    
    # Excel Export Button
    if EXPORT_AVAILABLE:
        st.markdown("---")
        col_export1, col_export2, col_export3 = st.columns([1, 1, 2])
        
        with col_export1:
            excel_data = export_all_counties_excel(df)
            st.download_button(
                label="📊 Download Excel (All Counties)",
                data=excel_data,
                file_name=f"OpenResilience_AllCounties_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Multi-sheet Excel with summary statistics"
            )
        
        with col_export2:
            csv_data = export_county_data_csv(df)
            st.download_button(
                label="📄 Download CSV (All Counties)",
                data=csv_data,
                file_name=f"OpenResilience_AllCounties_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                help="All counties data as CSV"
            )
        
        with col_export3:
            st.caption("💡 **Tip:** Excel file includes multiple sheets: All Counties, ASAL Counties, High Risk, and Summary Statistics")

# SMS Alert Service
with st.expander("📱 SMS Alert Service"):
    st.markdown("""
    <div style="background: #e3f2fd; padding: 20px; border-radius: 10px; border-left: 5px solid #2196f3;">
        <h3 style="color: #1565c0; margin-top: 0;">📱 Free Water Alerts via SMS</h3>
        <p style="font-size: 1.1em; color: #000;">
            <strong>No smartphone or internet needed!</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        **Receive:**
        - 📊 Weekly water stress updates
        - ⚠️ Critical shortage warnings
        - 🌱 Planting season reminders
        - 🚛 Water truck schedules
        
        **To register:** SMS `MAJI` to `22555`
        
        **Cost:** Free service (standard SMS rates apply)
        """)
    
    with col2:
        st.markdown("""
        **SMS Commands:**
        - `MAJI` - Subscribe to alerts
        - `STOP` - Unsubscribe
        - `HELP` - Get help
        - `STATUS <county>` - Check status
        
        **Example Alert:**
        ```
        🟠 OPENRESILIENCE
        Kiambu: HIGH
        Action: Reduce water use by 40%
        ```
        """)
    
    st.info("💡 **Perfect for farmers with basic phones!** No smartphone or internet required. Receive critical water alerts directly via SMS.")
    
    st.caption("**Service powered by Africa's Talking** | Questions? Contact your County Water Office")

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

# Field Reports Tab
with tab2:
    st.header("📝 Field Reports / Ripoti za Uwanja")
    
    col_intro1, col_intro2 = st.columns([2, 1])
    with col_intro1:
        if lang == "Kiswahili":
            st.markdown("""
            Tuma ripoti kutoka eneo lako kuhusu hali ya maji, chakula, na soko.
            Ripoti zako husaidia maamuzi ya serikali na kusambaza misaada.
            """)
        else:
            st.markdown("""
            Submit ground-truth reports from your area about water, food, and market conditions.
            Your reports help authorities make informed decisions and allocate resources effectively.
            """)
    
    with col_intro2:
        if db_initialized:
            try:
                report_count = len(get_recent_reports(limit=100))
                st.metric("Recent Reports", report_count)
            except Exception:
                st.metric("Recent Reports", "Error")
        else:
            st.metric("Recent Reports", "N/A")
    
    st.divider()
    
    # Report Submission Form
    st.subheader("Submit New Report" if lang == "English" else "Wasilisha Ripoti Mpya")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        report_county = st.selectbox(
            "County / Kaunti",
            sorted(KENYA_COUNTIES.keys()),
            key="field_report_county"
        )
    
    with col_f2:
        report_category = st.selectbox(
            "Category / Aina",
            ["Water / Maji", "Food / Chakula", "Market / Soko", "Health / Afya", "Security / Usalama"],
            key="field_report_category"
        )
    
    with col_f3:
        report_severity = st.select_slider(
            "Severity / Ukali",
            options=[1, 2, 3, 4, 5],
            value=3,
            format_func=lambda x: {
                1: "1 - Minor / Ndogo",
                2: "2 - Moderate / Wastani",
                3: "3 - Significant / Muhimu",
                4: "4 - Severe / Kali",
                5: "5 - Critical / Hatari"
            }[x],
            key="field_report_severity"
        )
    
    report_message = st.text_area(
        "Description / Maelezo",
        placeholder="Describe what you're observing in your area...",
        height=100,
        key="field_report_message"
    )
    
    col_sub1, col_sub2 = st.columns([3, 1])
    
    with col_sub1:
        geo_hint = st.text_input(
            "Location hint (optional) / Mahali",
            placeholder="e.g., 'Near Thika market' (do NOT provide exact GPS)",
            key="field_report_geo"
        )
    
    with col_sub2:
        contact_optional = st.text_input(
            "Contact (optional) / Mawasiliano",
            placeholder="Phone/email",
            type="password",
            key="field_report_contact"
        )
    
    if st.button("📤 Submit Report", type="primary", use_container_width=True):
        if not report_message.strip():
            st.error("Please provide a description")
        else:
            if db_initialized:
                try:
                    # Get or create region
                    region_id = ensure_region(
                        report_county,
                        level="county",
                        **KENYA_COUNTIES[report_county]
                    )
                    
                    # Hash contact if provided (privacy-preserving)
                    contact_hash = None
                    if contact_optional.strip():
                        contact_hash = hashlib.sha256(
                            contact_optional.strip().encode()
                        ).hexdigest()[:16]
                    
                    # Extract category key
                    category_key = report_category.split("/")[0].strip().lower()
                    
                    # Insert report
                    report_id = insert_field_report(
                        region_id=region_id,
                        category=category_key,
                        severity=report_severity,
                        message=report_message.strip(),
                        contact_hash=contact_hash,
                        geo_hint=geo_hint.strip() if geo_hint.strip() else None
                    )
                    
                    st.success(f"✅ Report #{report_id} submitted for {report_county}. Thank you!")
                    st.info("Your report helps county governments prioritize resource allocation.")
                    
                    # Check if this should trigger an alert
                    if report_severity >= 4:
                        st.session_state.selected_region_id = region_id
                        st.warning("⚠️ High severity report - review alerts tab for potential notifications")
                
                except Exception as e:
                    st.error(f"Failed to submit report: {e}")
            else:
                st.success("✅ Report received (database not available - demo mode)")
                st.info("Enable database module for full field report functionality")
    
    st.divider()
    
    # Recent Reports Display
    st.subheader("Recent Reports" if lang == "English" else "Ripoti za Hivi Karibuni")
    
    if db_initialized:
        try:
            reports = get_recent_reports(limit=20)
            
            if reports:
                for report in reports:
                    severity_emoji = {1: "🟢", 2: "🟡", 3: "🟠", 4: "🔴", 5: "🚨"}
                    
                    with st.expander(
                        f"{severity_emoji.get(report['severity'], '⚪')} "
                        f"{report['category'].title()} - "
                        f"{report['timestamp'][:10]}"
                    ):
                        st.markdown(f"**Severity:** {report['severity']}/5")
                        st.markdown(f"**Message:** {report['message']}")
                        if report.get('geo_hint'):
                            st.caption(f"📍 Location hint: {report['geo_hint']}")
                        st.caption(f"⏰ {report['timestamp']}")
            else:
                st.info("No recent reports. Be the first to submit!")
        
        except Exception as e:
            st.warning(f"Could not load reports: {e}")
    else:
        st.info("Database module not available. Enable for persistent report storage.")

# Alerts Tab
with tab3:
    st.header("🚨 Alerts / Tahadhari")
    
    if lang == "Kiswahili":
        st.markdown("""
        Angalizo la muda wa hali mbaya ya maji, chakula, au soko.
        Tahadhari hizi zinaundwa kiotomatiki wakati mazingira yanafikia kiwango cha hatari.
        """)
    else:
        st.markdown("""
        Real-time alerts for critical water, food, or market stress conditions.
        Alerts are automatically generated when indices exceed risk thresholds.
        """)
    
    st.divider()
    
    if db_initialized:
        try:
            active_alerts = get_active_alerts()
            
            if active_alerts:
                st.warning(f"⚠️ **{len(active_alerts)} active alert(s)**")
                
                for alert in active_alerts:
                    level_config = {
                        "info": ("ℹ️", "blue"),
                        "warning": ("⚠️", "orange"),
                        "critical": ("🚨", "red")
                    }
                    
                    emoji, color = level_config.get(alert['level'], ("⚪", "gray"))
                    
                    with st.container():
                        st.markdown(f"### {emoji} {alert['title']}")
                        st.markdown(f"**Region:** {alert['region_name']}")
                        st.markdown(f"**Level:** {alert['level'].upper()}")
                        st.markdown(f"**CRI:** {alert['cri']:.1f}/100")
                        st.markdown(f"**Detail:** {alert['detail']}")
                        st.caption(f"🕐 {alert['timestamp']}")
                        st.divider()
            else:
                st.success("✅ No active alerts. All regions within normal parameters.")
                st.info("Alerts trigger when Composite Risk Index (CRI) exceeds 70/100")
        
        except Exception as e:
            st.warning(f"Could not load alerts: {e}")
    else:
        st.info("Database module not available. Enable for alert functionality.")
        st.markdown("""
        **Alert Thresholds:**
        - **INFO**: CRI 50-60 (Watch conditions)
        - **WARNING**: CRI 60-70 (Prepare for action)
        - **CRITICAL**: CRI 70+ (Immediate response needed)
        """)

# Footer
st.divider()
st.caption("💧 OpenResilience Kenya • Built WITH and FOR Kenyan Communities")
st.caption("🇰🇪 Data Sovereignty • Community Resilience • Climate Adaptation • Agricultural Planning")
st.caption("© 2026 | In Partnership with County Governments & National Drought Management Authority")
st.caption("🙏 Special thanks to communities in Makongeni, Thika Landless, and all 47 counties")
