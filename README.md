# OpenResilience - Simplified Streamlit Edition

**Single-file water stress monitoring app** - Perfect for quick deployment and demos.

---

## ⚡ 5-Minute Deployment (No Downloads Required)

This is the simplified version - similar to deploying a trading bot on Streamlit Cloud.

### Step 1: Create GitHub Repository (2 minutes)

1. Go to https://github.com/new
2. Repository name: `openresilience-simple`
3. Description: "Water stress monitoring system"
4. Click "Create repository"
5. Click "uploading an existing file"
6. Drag `app.py` and `requirements.txt` into the upload area
7. Click "Commit changes"

### Step 2: Deploy to Streamlit Cloud (3 minutes)

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select repository: `openresilience-simple`
5. Main file: `app.py`
6. Click "Deploy"

**Done!** Your water stress map will be live at:  
`https://your-username-openresilience-simple-xxx.streamlit.app`

---

## Features

✅ **Global water stress map** with color-coded severity  
✅ **Active alerts** panel with filtering  
✅ **Quick jump** to regions of interest  
✅ **Field reporting** with privacy protection  
✅ **Zero infrastructure** - runs entirely on Streamlit Cloud  
✅ **Free forever** on Streamlit free tier  

---

## What This Includes

- **Interactive map** powered by Folium
- **Synthetic data generator** (demonstrates functionality)
- **Alert system** with severity filtering
- **Community reporting** with coarse geolocation
- **Educational information** about water stress monitoring

---

## What This Doesn't Include (vs Full System)

| Feature | Simplified | Full Production |
|---------|-----------|-----------------|
| Data storage | Session state (temporary) | PostgreSQL database |
| Updates | Manual refresh button | Automatic every 3 hours |
| Real NASA data | Not included | Included |
| Monitoring | None | Grafana dashboards |
| Backups | None | Automated daily |
| API | None | REST API for integration |

---

## Upgrading to Full Production

When you're ready for the full system with real NASA data:

1. **Get the full package:** Download `openresilience.zip`
2. **Follow:** ZERO_INSTALL_GUIDE.md
3. **Deploy:** Railway (API + Worker) + Streamlit (Frontend)
4. **Time:** 20 minutes
5. **Cost:** $0 (free tiers)

**The full system gives you:**
- Real NASA satellite data (IMERG + SMAP)
- Automatic updates every 3 hours
- Persistent data storage
- Health monitoring and alerts
- Production-grade architecture

---

## Local Testing (Optional)

If you want to test locally before deploying:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501

---

## Customization

### Change Update Frequency
Edit `app.py`, line ~30:
```python
# Add auto-refresh every N minutes
st_autorefresh(interval=180000)  # 3 minutes
```

### Add Real Data Sources
Replace the `generate_synthetic_data()` function with:
```python
import requests

def fetch_nasa_data():
    # Your NASA IMERG/SMAP integration here
    pass
```

### Change Map Style
Edit line ~200:
```python
tiles="CartoDB dark_matter"  # Try: "OpenStreetMap", "Stamen Terrain"
```

### Adjust Colors
Edit line ~90:
```python
rgba[wsi_data == 1] = [255, 204, 0, 160]   # Watch - Yellow
rgba[wsi_data == 2] = [255, 128, 0, 180]   # Warning - Orange
rgba[wsi_data == 3] = [255, 0, 0, 200]     # Severe - Red
```

---

## Files Included

```
openresilience-simple/
├── app.py              # Main Streamlit application (370 lines)
├── requirements.txt    # Python dependencies (5 packages)
└── README.md          # This file
```

---

## Support

- **Issues:** Create an issue on GitHub
- **Questions:** Open a discussion on GitHub
- **Email:** Contact via your repository

---

## Comparison: When to Use Which Version

### Use Simplified Version If:
- ✅ You want a quick demo
- ✅ You're testing the concept
- ✅ You have <100 users
- ✅ Manual refresh is acceptable
- ✅ You don't need data persistence

### Use Full Production If:
- ✅ You need real NASA data
- ✅ You want automatic updates
- ✅ You need monitoring and alerts
- ✅ You have >100 users
- ✅ You need API integration
- ✅ You require data backups

---

## Technical Details

**Framework:** Streamlit 1.x  
**Map Library:** Folium + Streamlit-Folium  
**Data:** Numpy for grid computation  
**Images:** Pillow for tile generation  
**Deployment:** Streamlit Cloud (free tier)  

**Performance:**
- Load time: ~2 seconds
- Refresh time: ~1 second
- Memory: ~200 MB
- Works on: Desktop, tablet, mobile

---

## License

MIT License - See full system for details

---

## What's Next

1. **Deploy this simplified version** (5 minutes)
2. **Test with synthetic data**
3. **When ready, upgrade to full production** (see ZERO_INSTALL_GUIDE.md)

**Total investment: 5 minutes to see it working**
