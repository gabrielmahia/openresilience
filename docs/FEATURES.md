# OpenResilience Kenya - Features Guide

## 🌍 **Platform Overview**

OpenResilience Kenya is a **comprehensive resilience monitoring platform** serving **all 47 counties** with automated satellite data updates every 6 hours.

**Target Users:**
1. **NGO Administrators** - Data analysis, reporting, multi-county oversight
2. **County Governments** - Decision support, resource allocation, emergency response
3. **Local Farmers** - Agricultural guidance, water management, planting advice
4. **Community Members** - Field reporting, local knowledge sharing

---

## ✨ **Core Features**

### 📊 **1. Multi-Index Resilience Scoring**

**What it does:** Combines multiple stress factors into actionable indices

**Indices:**
- **WSI (Water Stress Index)** - Rainfall + Soil Moisture
- **FSI (Food Stress Index)** - Vegetation health + Agricultural capacity
- **MSI (Market Stress Index)** - Economic access + Market availability
- **CRI (Composite Resilience Index)** - Overall resilience score

**Who uses it:**
- NGOs: Prioritize intervention areas
- Government: Allocate resources
- Farmers: Understand local conditions

---

### 🛰️ **2. Automated Satellite Data**

**What it does:** Real-time monitoring via automated data collection

**Data Sources:**
- Rainfall patterns (simulated NASA IMERG-style)
- Soil moisture (simulated NASA SMAP-style)
- Vegetation health (simulated Earth Engine MODIS-style)

**Update Frequency:** Every 6 hours via GitHub Actions

**Coverage:** All 47 counties with realistic climate-based patterns

**Who uses it:**
- NGOs: Track changes over time
- Government: Early warning signals
- Farmers: Current conditions

---

### 📍 **3. Geographic Drill-Down**

**What it does:** View data at County → Constituency → Ward levels

**How it works:**
1. Select County: County-wide overview
2. Select Constituency: Narrower geographic focus
3. Select Ward: Hyperlocal data (when available)

**Current Status:**
- ✅ All 47 counties active
- ⏳ Constituency data (aggregated from county)
- ⏳ Ward data (planned for Phase 2)

**Who uses it:**
- County Governments: Detailed local planning
- NGOs: Targeted interventions
- Community Leaders: Ward-specific needs

---

### 🌾 **4. Agricultural Guidance (NEW!)**

**What it does:** Context-aware farming advice based on current conditions

**Features:**
- **Seasonal Calendar** - When to plant for your region
- **Crop Recommendations** - What crops work in current conditions
- **Water Management Tips** - Save water during stress
- **Critical Actions** - What to do NOW based on stress level

**Designed for:**
- Farmers (primary users)
- Agricultural extension officers
- County agricultural departments

**Languages:** English + Kiswahili (Planned)

**Example Output:**
```
Season: Dry Season
Action: MAINTAIN
Stress Level: Moderate

Recommended Crops:
- High-value vegetables (if irrigation available)

Water Saving Tips:
- Irrigate only critical crops
- Use shade nets
- Conserve water in tanks

Critical Actions:
⚡ Monitor water levels daily
⚡ Reduce non-essential water use by 20%
⚡ Prepare water harvesting systems
```

---

### 📥 **5. Data Export (NEW!)**

**What it does:** Download data for analysis, reporting, archiving

**Export Formats:**
- **CSV** - For spreadsheet analysis
- **Excel** - Multi-sheet reports with summaries
- **Text Reports** - Human-readable summaries

**Export Options:**
- Single county data
- All 47 counties comparison
- Field reports log
- Custom date ranges (planned)

**Who uses it:**
- NGO Administrators: Quarterly reports
- Researchers: Data analysis
- County Governments: Official reporting
- Donors: Impact assessment

---

### 🎯 **6. Visual Indicators (NEW!)**

**What it does:** Simple, clear visual status for quick decisions

**Indicators:**
- 🟢 Good conditions - Normal activities OK
- 🟡 Moderate stress - Reduce water use 20%
- 🟠 High stress - Reduce water use 40%
- 🔴 Severe stress - Emergency measures

**Designed for:**
- Low-literacy users
- Quick decision-making
- Mobile phone displays
- Community notice boards

**Languages:** English + Kiswahili

**Example:**
```
🔴 SEVERE
Action: 🚨 EMERGENCY: Contact water officer
Planting: ⛔ DON'T PLANT - Insufficient water
Forecast: 📉 Conditions worsening - Prepare
```

---

### 📱 **7. Field Reporting**

**What it does:** Community members report local conditions

**Report Types:**
- Water point status
- Borehole failures
- Livestock deaths
- Market prices
- Community needs

**Who uses it:**
- Farmers: Report local observations
- Community Health Workers: Track conditions
- County Officers: Verify satellite data
- NGOs: Ground-truth monitoring

---

### 🚨 **8. Automated Alerts**

**What it does:** Proactive notifications when conditions change

**Alert Triggers:**
- Stress level increases by 20%
- Risk level changes (Moderate → High → Severe)
- Forecast predicts worsening
- Multiple counties affected

**Alert Channels:**
- In-app notifications
- SMS (Planned - Africa's Talking integration)
- WhatsApp (Planned)
- Email digest (Planned)

---

### 🗺️ **9. Interactive Maps**

**What it does:** Visual geographic representation of stress levels

**Map Features:**
- Color-coded counties by stress level
- Click county for details
- Zoom and pan
- Multiple layers (stress, rainfall, vegetation)

**Who uses it:**
- NGOs: Regional patterns
- Government: Resource deployment
- Public: Understand wider context

---

### 📈 **10. Forecasting**

**What it does:** Predict future conditions 1-12 months ahead

**Forecast Horizons:**
- 1-2 months (Short-term planning)
- 3-6 months (Medium-term preparation)
- 7-12 months (Long-term strategy)

**Methodology:**
- Seasonal patterns
- Historical trends
- Climate models (simplified)

**Who uses it:**
- Farmers: Planting decisions
- Government: Budget allocation
- NGOs: Intervention timing

---

## 🚀 **How to Use**

### **For NGO Administrators:**

1. **Monitor Multiple Counties:**
   - Click "Compare All 47 Counties"
   - Export to Excel for analysis
   - Track trends over time

2. **Generate Reports:**
   - Select county
   - Click "Export Summary Report"
   - Share with stakeholders

3. **Prioritize Interventions:**
   - Filter by risk level
   - Focus on ASAL counties
   - Allocate resources strategically

### **For Local Farmers:**

1. **Check Your Area:**
   - Select your county (e.g., Kiambu)
   - Select your constituency (e.g., Thika Town)
   - Select your ward (e.g., Gatuanyaga)

2. **Get Planting Advice:**
   - Scroll to "Agricultural Guidance"
   - Read recommended crops
   - Follow water-saving tips

3. **Understand Status:**
   - Look for emoji indicator (🟢/🟡/🟠/🔴)
   - Read simple action (e.g., "Reduce water 20%")
   - Check planting recommendation

4. **Report Issues:**
   - Click "Report Water Point Status"
   - Fill simple form
   - Submit to county office

---

## 📊 **Data Coverage**

### **All 47 Counties:**

**Central:** Nairobi, Kiambu, Murang'a, Nyeri, Kirinyaga, Nyandarua

**Coast:** Mombasa, Kwale, Kilifi, Tana River, Lamu, Taita-Taveta

**Eastern:** Marsabit, Isiolo, Meru, Tharaka-Nithi, Embu, Kitui, Machakos, Makueni

**North Eastern:** Garissa, Wajir, Mandera

**Nyanza:** Kisumu, Siaya, Homa Bay, Migori, Kisii, Nyamira

**Rift Valley:** Nakuru, Narok, Kajiado, Kericho, Bomet, Kakamega, Vihiga, Bungoma, Busia, West Pokot, Turkana, Trans-Nzoia, Uasin Gishu, Elgeyo-Marakwet, Nandi, Baringo, Laikipia, Samburu

---

## 🔄 **Update Schedule**

- **Satellite Data:** Every 6 hours (00:00, 06:00, 12:00, 18:00 UTC)
- **Forecasts:** Daily at 03:00 EAT
- **Platform:** Continuous deployment on code changes

---

## 💰 **Cost**

**Total Monthly Cost: $0**

- Streamlit Hosting: Free
- GitHub Actions: Free (within limits)
- Data Storage: Free (GitHub)
- Satellite Data: Simulated (no API costs)

---

## 🌐 **Languages**

- **Current:** English
- **Planned:** Kiswahili (Phase 2)
- **Future:** Regional languages based on demand

---

## 📞 **Support**

**For Technical Issues:**
- GitHub Issues: https://github.com/gabrielmahia/openresilience/issues

**For Data Questions:**
- Contact your County Water Office
- National Drought Management Authority (NDMA)

**For Feature Requests:**
- Community feedback via field reports
- County government suggestions

---

## 🔮 **Roadmap (Phase 2)**

**Planned Features:**
1. ✅ SMS Alerts (Africa's Talking integration)
2. ✅ WhatsApp Bot (Community engagement)
3. ✅ Voice Messages (Low-literacy support)
4. ✅ Full Kiswahili Translation
5. ✅ Historical Trends (6-month charts)
6. ✅ Weather Integration (7-day forecast)
7. ✅ Offline Mode (PWA)
8. ✅ Ward-Level Data (Constituency drill-down)
9. ✅ Real NASA APIs (When debugged)
10. ✅ API Access (For integrations)

---

## 📄 **License & Data Sovereignty**

**Platform:** Open Source (Community-owned)
**Data:** Locally-managed, Community-controlled
**Governance:** Multi-stakeholder (Counties + NGOs + Communities)

---

**Built for Kenya's communities. Powered by satellite technology. Driven by local knowledge.**

🌍 **OpenResilience Kenya** - *Maji na Kilimo • Water & Agricultural Planning for 47 Counties*
