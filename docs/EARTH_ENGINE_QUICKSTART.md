# Earth Engine Integration - Quick Start

## 🌍 **What You Just Got**

Your OpenResilience app now has **Google Earth Engine MODIS vegetation data** integration ready to go!

**Current Status:**
- ✅ Code integrated and deployed
- ⏳ Waiting for Earth Engine approval (1-2 days typically)
- 🔄 Falls back to demo data automatically

**When Earth Engine is approved:**
- 🌿 Real MODIS NDVI vegetation health (250m resolution)
- 📊 16-day composite for cloud-free coverage
- ✨ UI shows "Earth Engine MODIS" indicator

---

## ⚡ **Registration & Setup**

### **Step 1: Complete Earth Engine Registration** (You're here!)

Based on your screenshot, select:

**Organization Type:**
- ✅ Nonprofit/NGO (if applicable)
- ✅ Academia/Research (if university)
- ✅ Government

**Quota Tier:**
- ✅ **Community** (FREE, 150 EECU-hour limit)
- Perfect for 47 counties × 4 checks/day
- No billing account needed!

**Work Description:** (Paste this)
```
OpenResilience Kenya - Drought resilience platform for 47 counties

Using MODIS NDVI (MOD13Q1) to monitor vegetation health across Kenya 
for agricultural planning and food security early warning. Provides 
actionable intelligence to county governments, NDMA, and humanitarian 
organizations serving vulnerable communities.

Data Usage: Point extraction for 47 county centroids, updated weekly
Expected Compute: ~10 EECU-hours/month (well within Community tier)
```

**Submit** → Wait 1-2 days for approval email

---

### **Step 2: Get Service Account Credentials** (After Approval)

Once approved, you'll need service account credentials for automated access:

1. Go to: https://console.cloud.google.com/
2. Select your Earth Engine project (created during registration)
3. Go to: **IAM & Admin** → **Service Accounts**
4. Click **Create Service Account**
   - Name: `openresilience-production`
   - Description: `Automated MODIS NDVI extraction`
   - Click **Create and Continue**
5. Grant role: **Earth Engine Resource Writer**
6. Click **Done**
7. Click on the new service account
8. Go to **Keys** tab
9. Click **Add Key** → **Create new key**
10. Choose **JSON** → Click **Create**
11. Save the downloaded JSON file (keep it secure!)

---

### **Step 3: Add Credentials to Streamlit** (5 minutes)

1. Open the downloaded JSON file in a text editor
2. Copy the ENTIRE JSON content
3. Go to: https://share.streamlit.io/
4. Find "openresilience" app → **⚙️ Settings** → **Secrets**
5. Add this line:

```toml
GEE_SERVICE_ACCOUNT = '''
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...",
  "client_email": "openresilience-production@your-project.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  ...rest of JSON...
}
'''
```

6. Click **Save**
7. App will auto-restart with Earth Engine access! 🚀

---

## 📊 **What Happens Next**

### **Immediate (After Credentials Added)**

Your app will:
1. Try to fetch Earth Engine data from local cache
2. If cache empty, use demo data (same as before)
3. Show "Data Mode: Demo" in sidebar

Everything still works perfectly while you set up data collection!

### **After Running Data Collection**

Run the vegetation data updater:

```bash
# One-time manual run
python scripts/update_gee_data.py

# Or set up cron job (every 7 days - MODIS is 16-day composite)
crontab -e
# Add: 0 2 */7 * * cd /path/to/openresilience && python scripts/update_gee_data.py
```

**What this does:**
1. Authenticates with Earth Engine
2. Fetches latest MODIS NDVI for all 47 counties
3. Calculates vegetation health (0-1 scale)
4. Creates cache files in `data/gee_cache/`
5. Next app reload uses real vegetation data! 🎉

**Your sidebar will show:**
```
🌍 Using Earth Engine vegetation data for 47 counties
```

---

## 🏗️ **Combined Architecture** (NASA + Earth Engine)

```
┌─────────────────────┐
│   Streamlit App     │
│   (User Interface)  │
└──────────┬──────────┘
           │
           ▼ Reads cached data
┌──────────────────────────────────┐
│  Local Cache                     │
│  ├── data/nasa_cache/*.json      │ ← Rainfall + Soil Moisture
│  └── data/gee_cache/*.json       │ ← Vegetation Health (NDVI)
└──────────┬───────────────────────┘
           │
           ▼ Updated by background jobs
┌──────────────────────────────────┐
│  Update Scripts (Cron Jobs)      │
│  ├── update_nasa_data.py (6h)    │
│  └── update_gee_data.py (7d)     │
└──────────┬───────────────────────┘
           │
           ▼ Fetches from
┌──────────────────────────────────┐
│  Satellite Data Sources          │
│  ├── NASA AppEEARS (rainfall/soil)│
│  └── Google Earth Engine (NDVI)  │
└───────────────────────────────────┘
```

---

## 🧪 **Testing**

### **Test 1: Verify Credentials Work**

```python
from openresilience.adapters.earthengine import EarthEngineAdapter

adapter = EarthEngineAdapter()
print(f"Earth Engine available: {adapter.is_available()}")
```

Expected output:
```
Earth Engine authentication successful
Earth Engine available: True
```

### **Test 2: Fetch Test NDVI**

```bash
python scripts/update_gee_data.py
```

Expected output:
```
2026-02-12 16:30:00 - INFO - Starting Earth Engine data update...
2026-02-12 16:30:01 - INFO - Earth Engine authentication successful
2026-02-12 16:30:02 - INFO - Fetching NDVI for Nairobi...
2026-02-12 16:30:05 - INFO - Cached NDVI for Nairobi: 0.673
...
2026-02-12 16:31:00 - INFO - Update complete: 47/47 counties
```

### **Test 3: Verify App Shows Real Data**

1. Refresh your Streamlit app
2. Check sidebar for: "🌍 Using Earth Engine vegetation data"
3. Click different counties
4. Data status should show satellite source

---

## 🎯 **Data Quality**

**MODIS NDVI (MOD13Q1):**
- Resolution: 250 meters
- Temporal: 16-day composite (cloud-free)
- Range: -0.2 (bare soil) to 0.9+ (dense vegetation)
- Quality: High (NASA Tier 1 product)

**For Kenya:**
- Works perfectly for agricultural monitoring
- Detects drought stress early (before crop failure)
- Reliable even in arid regions (ASAL counties)

---

## 💰 **Cost**

**Earth Engine:** **FREE** (Community tier)

**Compute Budget:**
- Your quota: 150 EECU-hours/month
- Estimated usage: ~10 EECU-hours/month
- **You're using <7% of your quota!** 🎉

---

## 🔧 **Troubleshooting**

### **"Earth Engine not available"**

**Fix:** 
1. Check Earth Engine registration was approved
2. Verify service account was created
3. Confirm JSON credentials are in Streamlit secrets

### **"Authentication failed"**

**Check:**
- JSON formatting is correct (use triple quotes)
- Service account has "Earth Engine Resource Writer" role
- Project is registered for Earth Engine

### **"No MODIS data available"**

**This can happen if:**
- Location is outside MODIS coverage (unlikely for Kenya)
- Recent cloud cover (MODIS picks best 16-day window)
- Temporary Earth Engine service issue

**Solution:** App automatically falls back to demo data

### **"Still showing Demo mode"**

**This means:**
- Credentials configured ✅
- But cache empty (haven't run data updater yet)
- App safely using demo data ✅

**To get real data:**
```bash
python scripts/update_gee_data.py
```

---

## 🎊 **Combined Data Sources**

### **When Both NASA + Earth Engine Active:**

**Sidebar shows:**
```
🛰️ Using NASA satellite data for 47 counties
🌍 Using Earth Engine vegetation data for 47 counties
```

**Data status shows:**
```
🛰️ Satellite Data: NASA (rainfall, soil) + GEE (vegetation)
```

**You get:**
- ✅ Real rainfall from NASA IMERG
- ✅ Real soil moisture from NASA SMAP  
- ✅ Real vegetation health from MODIS NDVI
- ✅ Comprehensive resilience assessment!

---

## 📅 **Timeline**

### **Day 1 (Today):**
- ✅ Code deployed
- ⏳ Waiting for Earth Engine approval

### **Day 2-3:**
- 📧 Receive Earth Engine approval email
- 🔑 Create service account
- ⚙️ Add credentials to Streamlit

### **Day 4:**
- ▶️ Run data updater
- ✨ See real vegetation data!

### **Week 2:**
- 📊 Set up automated weekly updates
- 🎯 Monitor data quality
- 📈 Compare with ground observations

---

## 🆘 **Need Help?**

**Earth Engine Support:**
- Forum: https://groups.google.com/g/google-earth-engine-developers
- Docs: https://developers.google.com/earth-engine

**Service Account Issues:**
- Guide: https://developers.google.com/earth-engine/guides/service_account

**OpenResilience Issues:**
- GitHub: https://github.com/gabrielmahia/openresilience/issues

---

## ✨ **Next Steps**

1. **Complete registration** (select Community tier, submit)
2. **Wait for approval** (1-2 days, check email)
3. **Create service account** (5 minutes after approval)
4. **Add credentials to Streamlit** (copy-paste JSON)
5. **Watch your app use real satellite vegetation data!** 🌿

Your app is already deployed with Earth Engine integration. Just complete the registration and add credentials when approved!

**The best part?** Everything still works perfectly with demo data while you wait. Your users see no disruption. 🌍✨
