import os, requests
import pandas as pd
import streamlit as st

API_BASE = os.environ.get("API_BASE","http://api:8000")
st.set_page_config(page_title="OpenResilience • Drought/Water/Food", layout="wide")
st.title("OpenResilience • Drought / Water / Food Stress System (ALL-OUT)")
st.caption("Signals, not certainties. Verify locally. Designed for low bandwidth, mobile-first, and messaging-first access.")

def get_json(url, params=None, timeout=15):
    r = requests.get(url, params=params, timeout=timeout)
    r.raise_for_status()
    return r.json()

@st.cache_data(ttl=60)
def latest_run():
    return get_json(f"{API_BASE}/runs/latest")

@st.cache_data(ttl=60)
def top(metric, sev_min, bbox):
    params = {"metric": metric, "severity_min": sev_min, "limit": 500}
    if bbox: params.update(bbox)
    return get_json(f"{API_BASE}/indicators/top", params=params)

@st.cache_data(ttl=60)
def alerts(sev_min, bbox):
    params = {"severity_min": sev_min, "limit": 300}
    if bbox: params.update(bbox)
    return get_json(f"{API_BASE}/alerts/latest", params=params)

st.sidebar.header("Filters")
sev_min = st.sidebar.selectbox("Alert threshold", [1,2,3], index=1)
metric = st.sidebar.selectbox("Rank by", ["cri","wsi","fsi","msi"], index=0)
use_bbox = st.sidebar.checkbox("Filter by bounding box (lat/lon)", value=False)
bbox = None
if use_bbox:
    bbox = {
        "min_lat": st.sidebar.number_input("min_lat", value=-5.0),
        "max_lat": st.sidebar.number_input("max_lat", value=5.0),
        "min_lon": st.sidebar.number_input("min_lon", value=30.0),
        "max_lon": st.sidebar.number_input("max_lon", value=45.0),
    }

tabs = st.tabs(["Situation","Water","Food","Markets","Logistics","Alerts","Reports","Briefs","Admin"])

with tabs[0]:
    st.subheader("Situation Overview")
    try:
        run = latest_run()
        st.success(f"Latest run: {run['run_time_utc']} • Adapter: {run['adapter']} • Version: {run['version']}")
        if run.get("notes"): st.caption(run["notes"])
        df = pd.DataFrame(top(metric, sev_min, bbox))
        if df.empty: st.info("No regions above threshold.")
        else:
            df["value"] = df["value"].astype(float).round(2)
            st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"API error: {e}")

with tabs[1]:
    st.subheader("Water Stress (WSI)")
    st.write("WSI blends rainfall anomaly + soil moisture proxy + drought persistence proxy. Replace proxies with real adapters for production.")
    try:
        st.dataframe(pd.DataFrame(top("wsi", sev_min, bbox)), use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(e)

with tabs[2]:
    st.subheader("Food Stress (FSI)")
    st.write("FSI uses vegetation stress proxy + persistence + rainfall proxy. Add market + nutrition signals for better famine early warning.")
    try:
        st.dataframe(pd.DataFrame(top("fsi", sev_min, bbox)), use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(e)

with tabs[3]:
    st.subheader("Markets (MSI)")
    st.info("MSI placeholder = 0 until prices are ingested. DB + API already include prices table. Add a loader to activate.")

with tabs[4]:
    st.subheader("Logistics")
    st.markdown("""In drought/famine logistics, the constraints are:
- water trucking routes + queue discipline
- storage buffers (tank capacity, household storage)
- fuel availability + road conditions + security
- time-to-failure (days until storage empty)

This repo is structured to add a logistics adapter without redesign.
""")

with tabs[5]:
    st.subheader("Alerts")
    try:
        payload = alerts(sev_min, bbox)
        arr = payload.get("alerts", [])
        if not arr:
            st.info("No alerts at this threshold.")
        for a in arr[:120]:
            st.markdown(f"### {a['title']} (S{a['severity']})")
            st.caption(f"Region: {a['region_id']} • {a['domain']} • {a['created_utc']} • Conf: {a.get('details',{}).get('confidence','n/a')}")
            st.write(a["message"])
            st.json(a.get("details",{}), expanded=False)
            st.divider()
    except Exception as e:
        st.error(e)

with tabs[6]:
    st.subheader("Field Reports (Privacy-safe)")
    st.warning("Do not publish precise resource coordinates publicly in active crisis/conflict areas. Reports are coarsened by default.")
    with st.form("report"):
        c1,c2,c3 = st.columns(3)
        lat = c1.number_input("Latitude", value=-1.29)
        lon = c2.number_input("Longitude", value=36.82)
        region_id = c3.text_input("region_id (optional)", value="")
        r_type = st.selectbox("Type", ["borehole","well","river","tap","market","health","other"])
        status = st.selectbox("Status", ["ok","low","dry","inaccessible","crowded","price_spike"])
        notes = st.text_area("Notes", "")
        src = st.text_input("Source hint (optional)", "")
        ok = st.form_submit_button("Submit")
        if ok:
            try:
                resp = requests.post(f"{API_BASE}/reports", json={
                    "lat": lat, "lon": lon, "region_id": region_id or None,
                    "report_type": r_type, "status": status,
                    "notes": notes or None, "source_hint": src or None
                }, timeout=20).json()
                st.success(f"Submitted. Coarse hash: {resp['coarse_geohash']}")
            except Exception as e:
                st.error(f"Submit failed: {e}")

with tabs[7]:
    st.subheader("Briefs (PDF)")
    rid = st.text_input("Region ID", value="grid_0p25_lat_-1.25_lon_36.75")
    st.markdown(f"[Open brief PDF]({API_BASE}/briefs/region/{rid}.pdf)")

with tabs[8]:
    st.subheader("Admin")
    st.markdown(f"Exports:  
- {API_BASE}/exports/alerts.csv  
- {API_BASE}/exports/indicators.csv?metric=cri")
    st.caption("Notifier is enabled; MSG_PROVIDER=mock prints sends to logs.")
