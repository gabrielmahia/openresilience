# Real Data Integration Guide

## Overview

OpenResilience currently uses **demo data** for all indices. This guide explains how to integrate real satellite and ground-truth data sources for production deployment.

---

## 🛰️ **Available Real Data Sources**

### 1. **Rainfall Data** (for WSI)

#### **NASA GPM IMERG** (Primary Recommendation)
- **What**: Global Precipitation Measurement mission
- **Resolution**: 0.1° (~11 km), 30-minute intervals
- **Coverage**: Global, including all Kenya
- **API**: NASA GES DISC Data Access
- **Cost**: Free (NASA Earthdata account required)

**Access:**
```python
# NASA Earthdata API
import requests
from datetime import datetime, timedelta

def get_rainfall_data(lat, lon, start_date, end_date):
    """
    Fetch IMERG rainfall data from NASA GES DISC.
    
    Requires:
    - NASA Earthdata account: https://urs.earthdata.nasa.gov/
    - Bearer token from Earthdata Login
    """
    base_url = "https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/"
    # ... implementation
```

**Sign up:** https://urs.earthdata.nasa.gov/users/new

#### **CHIRPS** (Alternative/Supplementary)
- **What**: Climate Hazards Group InfraRed Precipitation with Station data
- **Resolution**: 0.05° (~5.5 km), daily
- **Coverage**: 50°S-50°N (includes Kenya)
- **API**: UCSB Climate Engine or direct download
- **Cost**: Free

**Access:**
```python
# CHIRPS via Climate Engine
# API: https://support.climateengine.org/article/62-api
```

---

### 2. **Soil Moisture** (for WSI)

#### **NASA SMAP** (Primary)
- **What**: Soil Moisture Active Passive mission
- **Resolution**: 9 km, 2-3 day revisit
- **Coverage**: Global
- **API**: NASA Earthdata
- **Cost**: Free

**Access:**
```python
def get_soil_moisture(lat, lon, date):
    """
    Fetch SMAP Level 3 soil moisture data.
    
    Product: SPL3SMP (SMAP L3 Radiometer Global Daily)
    """
    # Available through NASA Earthdata
```

---

### 3. **Vegetation Health** (for FSI)

#### **MODIS NDVI** (Primary)
- **What**: Moderate Resolution Imaging Spectroradiometer
- **Resolution**: 250m-1km, 16-day composite
- **Coverage**: Global
- **API**: NASA MODIS Web Service or Google Earth Engine
- **Cost**: Free

**Access via Google Earth Engine:**
```python
import ee

ee.Initialize()

def get_ndvi(region, start_date, end_date):
    """
    Calculate NDVI from MODIS Terra satellite.
    
    Product: MOD13Q1 (250m, 16-day NDVI)
    """
    collection = ee.ImageCollection('MODIS/006/MOD13Q1') \
        .filterDate(start_date, end_date) \
        .filterBounds(region)
    
    ndvi = collection.select('NDVI').mean()
    return ndvi
```

**Sign up:** https://earthengine.google.com/signup/

---

### 4. **Food Prices** (for MSI)

#### **WFP VAM** (World Food Programme)
- **What**: Vulnerability Analysis and Mapping price data
- **Coverage**: Kenya market prices for staple foods
- **API**: WFP Data API
- **Cost**: Free (registration required)

**Access:**
```python
def get_food_prices(country_code='KE'):
    """
    Fetch market prices from WFP VAM.
    
    API: https://dataviz.vam.wfp.org/
    """
    url = "https://dataviz.vam.wfp.org/API/GetMarketPrices"
    params = {
        'CountryCode': country_code,
        'format': 'json'
    }
    # ... implementation
```

**Sign up:** https://dataviz.vam.wfp.org/

#### **Kenya National Bureau of Statistics**
- **What**: Official consumer price indices
- **Coverage**: Kenya urban/rural markets
- **Access**: KNBS Open Data Portal
- **Cost**: Free

---

### 5. **Field Reports** (for FSI & CRI)

#### **SMS Gateway Integration**

**Africa's Talking** (Recommended for Kenya)
```python
import africastalking

def setup_sms_gateway():
    """
    Configure Africa's Talking for SMS field reports.
    
    Cost: ~0.80 KES per SMS
    Sign up: https://africastalking.com/
    """
    username = "your_username"
    api_key = "your_api_key"
    africastalking.initialize(username, api_key)
    
    sms = africastalking.SMS
    
    # Receive SMS
    @app.route('/sms', methods=['POST'])
    def receive_sms():
        sender = request.values.get('from')
        message = request.values.get('text')
        
        # Parse and store field report
        parse_field_report(sender, message)
```

**Integration Points:**
- Receive: SMS webhook → parse → insert_field_report()
- Send: Alerts → format → SMS API

---

## 📊 **Integration Architecture**

### **Option 1: Real-Time Adapters** (Recommended)

Create adapter modules that fetch fresh data:

```python
# src/openresilience/adapters/nasa.py
def fetch_current_rainfall(county_bounds):
    """Fetch latest IMERG data for county."""
    # Call NASA API
    # Calculate anomaly from climatology
    return rainfall_anomaly

# src/openresilience/adapters/wfp.py
def fetch_food_prices(market_id):
    """Fetch latest WFP price data."""
    # Call WFP API
    # Calculate % change from baseline
    return price_change
```

**Update app.py:**
```python
# Replace demo data with real data
if DATA_MODE == "live":
    rainfall_anom = fetch_current_rainfall(county_bounds)
    soil_moisture = fetch_soil_moisture(county_coords)
    vegetation = fetch_ndvi(county_bounds)
    prices = fetch_food_prices(county_market_id)
else:
    # Keep current demo data
```

---

### **Option 2: Scheduled Updates** (More Reliable)

Run data collection as cron jobs:

```bash
# Crontab: Update data every 6 hours
0 */6 * * * python scripts/update_satellite_data.py
0 8 * * * python scripts/update_market_prices.py
```

**Benefits:**
- No API rate limits during user sessions
- Faster page loads
- Cached data available offline

---

## 🚀 **Implementation Roadmap**

### **Phase 1: NASA Satellite Data** (Week 1-2)
1. Register for NASA Earthdata account
2. Create `src/openresilience/adapters/nasa.py`
3. Implement IMERG rainfall fetching
4. Implement SMAP soil moisture fetching
5. Test with 5 pilot counties
6. Deploy to staging environment

### **Phase 2: Vegetation & Market Data** (Week 3-4)
1. Set up Google Earth Engine account
2. Create `src/openresilience/adapters/gee.py`
3. Implement MODIS NDVI fetching
4. Register for WFP VAM access
5. Create `src/openresilience/adapters/wfp.py`
6. Implement price data fetching
7. Test end-to-end with real data

### **Phase 3: SMS Field Reports** (Week 5-6)
1. Sign up for Africa's Talking
2. Create `src/openresilience/adapters/sms.py`
3. Set up SMS webhook endpoint
4. Implement report parsing (expect format: "REPORT [CATEGORY] [SEVERITY] [MESSAGE]")
5. Deploy alert dispatch system
6. Pilot with 3 counties

### **Phase 4: Full Production** (Week 7-8)
1. Scale to all 47 counties
2. Set up monitoring/logging
3. Configure auto-failover to demo data
4. Document data sources in UI
5. Train county officials
6. Launch!

---

## 💰 **Cost Estimate**

### **Data Sources** (All Free!)
- NASA Earthdata: Free
- Google Earth Engine: Free (non-commercial)
- WFP VAM: Free
- KNBS: Free

### **SMS Gateway** (Africa's Talking)
- Incoming SMS: 0.80 KES (~$0.006 USD) per message
- Outgoing Alerts: 0.80 KES per recipient
- **Estimate:** 1,000 reports/month = 800 KES (~$6 USD/month)

### **Hosting** (Streamlit Cloud)
- Current tier: Free (sufficient for demo)
- Upgrade for production: $20-100/month (if needed)

**Total Monthly Cost:** ~$6-106 USD (mostly optional SMS)

---

## 🔧 **Quick Start: Add Real Rainfall Data**

Here's a minimal example to get started TODAY:

```python
# Add to app.py after imports
import os

def get_real_rainfall(lat, lon, county_name):
    """
    Fetch real IMERG rainfall for the last 30 days.
    Falls back to demo data if API fails.
    """
    try:
        # Check if NASA token exists
        nasa_token = os.getenv('NASA_EARTHDATA_TOKEN')
        if not nasa_token:
            return None  # Use demo data
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # Simplified IMERG query (implement full version later)
        url = f"https://gpm1.gesdisc.eosdis.nasa.gov/..."
        headers = {'Authorization': f'Bearer {nasa_token}'}
        
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            # Calculate anomaly
            return calculate_anomaly(data)
        else:
            return None
    
    except Exception as e:
        print(f"Failed to fetch real data: {e}")
        return None

# Update load_county_data()
@st.cache_data(ttl=3600)
def load_county_data():
    """Generate county data - use real data when available."""
    
    county_list = []
    for county, info in KENYA_COUNTIES.items():
        
        # TRY REAL DATA FIRST
        real_rainfall = get_real_rainfall(info['lat'], info['lon'], county)
        
        if real_rainfall is not None:
            rainfall_anom = real_rainfall
            st.sidebar.success(f"✅ Using real satellite data for {county}")
        else:
            # FALLBACK TO DEMO
            rainfall_anom = np.random.uniform(-55, 10)
        
        # ... rest of code unchanged
```

**Set up:**
1. Get NASA token: https://urs.earthdata.nasa.gov/
2. Add to Streamlit secrets: Settings → Secrets → `NASA_EARTHDATA_TOKEN = "your_token"`
3. Deploy!

---

## 📞 **Support Contacts**

**NASA Earthdata Help:**
- Email: support@earthdata.nasa.gov
- Forum: https://forum.earthdata.nasa.gov/

**WFP Data Support:**
- Email: wfp.vam@wfp.org

**Africa's Talking:**
- Support: https://help.africastalking.com/

**Google Earth Engine:**
- Forum: https://groups.google.com/g/google-earth-engine-developers

---

## ✅ **Next Steps**

1. **Register accounts** (NASA, WFP, GEE) - Do this today!
2. **Test API access** - Verify credentials work
3. **Choose integration approach** (real-time vs scheduled)
4. **Pilot with 1 county** - Nairobi is good starting point
5. **Iterate and scale**

**Want me to implement any of these right now?** Just say which data source to prioritize!
