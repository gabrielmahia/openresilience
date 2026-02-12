import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple

import pandas as pd
import streamlit as st

APP_NAME = "OpenResilience Platform"
DB_PATH_DEFAULT = "openresilience.db"

@dataclass
class Scores:
    wsi: float
    fsi: float
    msi: float
    cri: float
    confidence: float

def clamp(x: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, x))

def compute_scores(
    rainfall_anom: float,        # -100..+100 (%)
    soil_moisture: float,        # 0..1
    vegetation: float,           # 0..1
    staple_price_delta: float,   # -100..+100 (%)
    market_stockouts: int,       # 0..5
    field_reports_24h: int,      # count
) -> Scores:
    # Water stress
    w = 0.55 * clamp(-rainfall_anom, 0, 100) + 0.45 * clamp((1 - soil_moisture) * 100, 0, 100)
    wsi = clamp(w)

    # Food stress
    f = 0.50 * clamp((1 - vegetation) * 100, 0, 100) + 0.30 * wsi + 0.20 * clamp(field_reports_24h * 12, 0, 100)
    fsi = clamp(f)

    # Market stress
    m = 0.70 * clamp(staple_price_delta, 0, 100) + 0.30 * clamp(market_stockouts * 20, 0, 100)
    msi = clamp(m)

    # Composite (drought-weighted)
    cri = clamp(0.45 * wsi + 0.35 * fsi + 0.20 * msi)

    aligned = 0
    aligned += 1 if rainfall_anom < -20 else 0
    aligned += 1 if soil_moisture < 0.35 else 0
    aligned += 1 if vegetation < 0.45 else 0
    aligned += 1 if field_reports_24h >= 2 else 0
    confidence = min(1.0, 0.35 + 0.15 * aligned)

    return Scores(wsi=wsi, fsi=fsi, msi=msi, cri=cri, confidence=confidence)

def risk_level(cri: float) -> str:
    if cri >= 80: return "SEVERE"
    if cri >= 60: return "HIGH"
    if cri >= 40: return "ELEVATED"
    if cri >= 20: return "WATCH"
    return "LOW"

def db_connect(db_path: str):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn

def db_init(conn: sqlite3.Connection):
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS regions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        country TEXT NOT NULL DEFAULT 'Kenya'
    );

    CREATE TABLE IF NOT EXISTS runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        region_id INTEGER NOT NULL,
        ts TEXT NOT NULL,
        rainfall_anom REAL NOT NULL,
        soil_moisture REAL NOT NULL,
        vegetation REAL NOT NULL,
        staple_price_delta REAL NOT NULL,
        market_stockouts INTEGER NOT NULL,
        field_reports_24h INTEGER NOT NULL,
        wsi REAL NOT NULL,
        fsi REAL NOT NULL,
        msi REAL NOT NULL,
        cri REAL NOT NULL,
        confidence REAL NOT NULL,
        notes TEXT,
        FOREIGN KEY(region_id) REFERENCES regions(id)
    );

    CREATE TABLE IF NOT EXISTS field_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        region_id INTEGER NOT NULL,
        ts TEXT NOT NULL,
        category TEXT NOT NULL,
        severity INTEGER NOT NULL,
        message TEXT NOT NULL,
        contact_hash TEXT,
        geo_hint TEXT,
        FOREIGN KEY(region_id) REFERENCES regions(id)
    );

    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        region_id INTEGER NOT NULL,
        ts TEXT NOT NULL,
        level TEXT NOT NULL,
        cri REAL NOT NULL,
        title TEXT NOT NULL,
        detail TEXT NOT NULL,
        acknowledged INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY(region_id) REFERENCES regions(id)
    );
    """)
    conn.commit()

def ensure_region(conn: sqlite3.Connection, name: str, country: str = "Kenya") -> int:
    cur = conn.execute("SELECT id FROM regions WHERE name = ?", (name,))
    row = cur.fetchone()
    if row:
        return int(row[0])
    conn.execute("INSERT INTO regions (name, country) VALUES (?, ?)", (name, country))
    conn.commit()
    return int(conn.execute("SELECT id FROM regions WHERE name = ?", (name,)).fetchone()[0])

def insert_run(conn: sqlite3.Connection, region_id: int, payload: Dict[str, Any], scores: Scores, notes: str = ""):
    conn.execute("""
    INSERT INTO runs (
        region_id, ts, rainfall_anom, soil_moisture, vegetation, staple_price_delta,
        market_stockouts, field_reports_24h, wsi, fsi, msi, cri, confidence, notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        region_id,
        datetime.utcnow().isoformat(timespec="seconds") + "Z",
        float(payload["rainfall_anom"]),
        float(payload["soil_moisture"]),
        float(payload["vegetation"]),
        float(payload["staple_price_delta"]),
        int(payload["market_stockouts"]),
        int(payload["field_reports_24h"]),
        float(scores.wsi), float(scores.fsi), float(scores.msi), float(scores.cri), float(scores.confidence),
        notes or ""
    ))
    conn.commit()

def insert_field_report(conn: sqlite3.Connection, region_id: int, category: str, severity: int, message: str, contact_hash: str = "", geo_hint: str = ""):
    conn.execute("""
    INSERT INTO field_reports (region_id, ts, category, severity, message, contact_hash, geo_hint)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        region_id,
        datetime.utcnow().isoformat(timespec="seconds") + "Z",
        category, int(severity), message.strip(), contact_hash.strip(), geo_hint.strip()
    ))
    conn.commit()

def insert_alert(conn: sqlite3.Connection, region_id: int, level: str, cri: float, title: str, detail: str):
    conn.execute("""
    INSERT INTO alerts (region_id, ts, level, cri, title, detail)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        region_id,
        datetime.utcnow().isoformat(timespec="seconds") + "Z",
        level, float(cri), title.strip(), detail.strip()
    ))
    conn.commit()

def latest_runs(conn: sqlite3.Connection, region_id: int, limit: int = 180) -> pd.DataFrame:
    df = pd.read_sql_query("""
        SELECT ts, rainfall_anom, soil_moisture, vegetation, staple_price_delta,
               market_stockouts, field_reports_24h, wsi, fsi, msi, cri, confidence, notes
        FROM runs WHERE region_id = ?
        ORDER BY ts DESC LIMIT ?
    """, conn, params=(region_id, limit))
    if not df.empty:
        df["ts"] = pd.to_datetime(df["ts"], errors="coerce")
        df = df.sort_values("ts")
    return df

def latest_alerts(conn: sqlite3.Connection, region_id: int, limit: int = 30) -> pd.DataFrame:
    df = pd.read_sql_query("""
        SELECT id, ts, level, cri, title, detail, acknowledged
        FROM alerts WHERE region_id = ?
        ORDER BY ts DESC LIMIT ?
    """, conn, params=(region_id, limit))
    if not df.empty:
        df["ts"] = pd.to_datetime(df["ts"], errors="coerce")
    return df

def recent_reports(conn: sqlite3.Connection, region_id: int, limit: int = 50) -> pd.DataFrame:
    df = pd.read_sql_query("""
        SELECT ts, category, severity, message, geo_hint
        FROM field_reports WHERE region_id = ?
        ORDER BY ts DESC LIMIT ?
    """, conn, params=(region_id, limit))
    if not df.empty:
        df["ts"] = pd.to_datetime(df["ts"], errors="coerce")
    return df

def count_reports_last_24h(conn: sqlite3.Connection, region_id: int) -> int:
    since = (datetime.utcnow() - timedelta(hours=24)).isoformat(timespec="seconds") + "Z"
    cur = conn.execute("SELECT COUNT(*) FROM field_reports WHERE region_id = ? AND ts >= ?", (region_id, since))
    return int(cur.fetchone()[0])

def seed_demo(conn: sqlite3.Connection, region_id: int):
    insert_field_report(conn, region_id, "water", 3, "Borehole queue increasing; intermittent supply reported.", geo_hint="coarse: ward-level")
    insert_field_report(conn, region_id, "market", 2, "Maize flour price up ~10% at local kiosks.", geo_hint="coarse: neighborhood")
    insert_field_report(conn, region_id, "food", 4, "Livestock body condition worsening in nearby pastoral areas.", geo_hint="coarse: county-level")

    now = datetime.utcnow()
    for i in range(30, 0, -1):
        ts = now - timedelta(days=i)
        payload = {
            "rainfall_anom": -10 - (i % 7) * 2,
            "soil_moisture": max(0.15, 0.55 - i * 0.01),
            "vegetation": max(0.20, 0.65 - i * 0.012),
            "staple_price_delta": max(0.0, (i % 10) * 2.0),
            "market_stockouts": (i % 3),
            "field_reports_24h": 0
        }
        scores = compute_scores(**payload)
        conn.execute("""
        INSERT INTO runs (
            region_id, ts, rainfall_anom, soil_moisture, vegetation, staple_price_delta,
            market_stockouts, field_reports_24h, wsi, fsi, msi, cri, confidence, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            region_id,
            ts.isoformat(timespec="seconds") + "Z",
            payload["rainfall_anom"], payload["soil_moisture"], payload["vegetation"], payload["staple_price_delta"],
            payload["market_stockouts"], payload["field_reports_24h"],
            scores.wsi, scores.fsi, scores.msi, scores.cri, scores.confidence,
            "demo"
        ))
    conn.commit()

def set_page():
    st.set_page_config(page_title=APP_NAME, page_icon="🛰️", layout="wide", initial_sidebar_state="expanded")

def disclaimer():
    st.info(
        "Signals, not certainties. Validate locally before acting. Avoid sharing precise resource locations publicly.",
        icon="ℹ️"
    )

def sidebar_controls(conn: sqlite3.Connection) -> Tuple[int, str, str]:
    st.sidebar.title("OpenResilience")
    st.sidebar.caption("Drought • Water • Food Stress Intelligence")

    db_path = st.sidebar.text_input("Database", value=st.session_state.get("db_path", DB_PATH_DEFAULT),
                                    help="SQLite DB file path (local).")
    if db_path != st.session_state.get("db_path", DB_PATH_DEFAULT):
        st.session_state["db_path"] = db_path
        st.rerun()

    st.sidebar.divider()
    country = st.sidebar.text_input("Country", value="Kenya")
    region_name = st.sidebar.text_input("Region", value="Nairobi / Westlands")
    region_id = ensure_region(conn, region_name, country)

    st.sidebar.divider()
    st.sidebar.subheader("Quick Actions")
    if st.sidebar.button("Seed Demo Data", use_container_width=True):
        seed_demo(conn, region_id)
        st.sidebar.success("Seeded demo runs + sample reports.")

    return region_id, region_name, country

def render_kpis(df: pd.DataFrame):
    if df.empty:
        st.warning("No runs yet. Use 'Seed Demo Data' or create a run.", icon="⚠️")
        return
    last = df.iloc[-1]
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("WATER (WSI)", f"{last['wsi']:.0f}/100")
    c2.metric("FOOD (FSI)", f"{last['fsi']:.0f}/100")
    c3.metric("MARKET (MSI)", f"{last['msi']:.0f}/100")
    c4.metric("COMPOSITE (CRI)", f"{last['cri']:.0f}/100", delta=risk_level(float(last["cri"])))
    c5.metric("Confidence", f"{last['confidence']:.2f}")

def chart_scores(df: pd.DataFrame):
    if df.empty:
        return
    plot_df = df[["ts", "wsi", "fsi", "msi", "cri"]].set_index("ts")
    st.line_chart(plot_df)

def alerts_logic(conn: sqlite3.Connection, region_id: int, df: pd.DataFrame):
    if df.empty:
        return
    last = df.iloc[-1]
    level = risk_level(float(last["cri"]))
    if level in ("HIGH", "SEVERE"):
        adf = latest_alerts(conn, region_id, limit=1)
        should = True
        if not adf.empty:
            a = adf.iloc[0]
            ts = a["ts"].to_pydatetime() if pd.notnull(a["ts"]) else datetime.utcnow()
            if (datetime.utcnow() - ts) < timedelta(hours=24) and a["level"] == level:
                should = False
        if should:
            insert_alert(
                conn, region_id,
                level=level, cri=float(last["cri"]),
                title=f"{level} drought/food-stress signal detected",
                detail=(
                    f"CRI={float(last['cri']):.1f}, WSI={float(last['wsi']):.1f}, "
                    f"FSI={float(last['fsi']):.1f}, MSI={float(last['msi']):.1f}. "
                    "Treat as a signal; confirm with local authorities and ground checks."
                ),
            )

def tab_situation(conn: sqlite3.Connection, region_id: int):
    st.header("Situation Overview")
    disclaimer()
    df = latest_runs(conn, region_id, limit=180)
    render_kpis(df)
    st.subheader("Trend")
    chart_scores(df)
    alerts_logic(conn, region_id, df)
    st.subheader("Latest Alerts")
    adf = latest_alerts(conn, region_id, limit=20)
    if adf.empty:
        st.write("No active alerts.")
    else:
        st.dataframe(adf, use_container_width=True)

def tab_create_run(conn: sqlite3.Connection, region_id: int):
    st.header("Create / Update Run")
    disclaimer()
    reports_24h = count_reports_last_24h(conn, region_id)

    c1, c2, c3 = st.columns(3)
    with c1:
        rainfall_anom = st.slider("Rainfall anomaly (%)", -100, 100, -15, help="Negative = below normal rainfall.")
        soil = st.slider("Soil moisture (0–1)", 0.0, 1.0, 0.35, step=0.01)
    with c2:
        veg = st.slider("Vegetation index (0–1)", 0.0, 1.0, 0.45, step=0.01)
        price_delta = st.slider("Staple price delta (%)", -100, 100, 12, help="Percent vs baseline.")
    with c3:
        stockouts = st.slider("Market stockouts (0–5)", 0, 5, 1)
        st.metric("Field reports (last 24h)", reports_24h)

    payload = dict(
        rainfall_anom=rainfall_anom,
        soil_moisture=soil,
        vegetation=veg,
        staple_price_delta=price_delta,
        market_stockouts=stockouts,
        field_reports_24h=reports_24h,
    )
    scores = compute_scores(**payload)

    st.write("### Computed Scores")
    sc1, sc2, sc3, sc4, sc5 = st.columns(5)
    sc1.metric("WSI", f"{scores.wsi:.0f}")
    sc2.metric("FSI", f"{scores.fsi:.0f}")
    sc3.metric("MSI", f"{scores.msi:.0f}")
    sc4.metric("CRI", f"{scores.cri:.0f}", delta=risk_level(scores.cri))
    sc5.metric("Confidence", f"{scores.confidence:.2f}")

    notes = st.text_area("Notes (optional)", value="")
    if st.button("Save Run", type="primary"):
        insert_run(conn, region_id, payload, scores, notes=notes)
        st.success("Saved. Navigate to Situation to view trends/alerts.")
        st.rerun()

def tab_field_reports(conn: sqlite3.Connection, region_id: int):
    st.header("Field Reports")
    disclaimer()

    with st.form("report_form", clear_on_submit=True):
        col1, col2 = st.columns([1, 2])
        with col1:
            category = st.selectbox("Category", ["water", "food", "market", "health", "security", "other"])
            severity = st.slider("Severity (1–5)", 1, 5, 3)
        with col2:
            message = st.text_area("Report", placeholder="Describe observable conditions. Avoid exact coordinates.")
            geo_hint = st.text_input("Geo hint (coarse)", value="coarse: ward/county/neighborhood")
        contact_hash = st.text_input("Contact hash (optional)", value="",
                                     help="Store a hashed identifier if needed — not raw phone/email.")
        submitted = st.form_submit_button("Submit report")
        if submitted:
            if not message.strip():
                st.error("Report text required.")
            else:
                insert_field_report(conn, region_id, category, severity, message,
                                   contact_hash=contact_hash, geo_hint=geo_hint)
                st.success("Report submitted.")
                st.rerun()

    st.subheader("Recent Reports")
    rdf = recent_reports(conn, region_id, limit=50)
    if rdf.empty:
        st.write("No reports yet.")
    else:
        st.dataframe(rdf, use_container_width=True)

def tab_exports(conn: sqlite3.Connection, region_id: int):
    st.header("Exports")
    disclaimer()

    df = latest_runs(conn, region_id, limit=1000)
    adf = latest_alerts(conn, region_id, limit=1000)
    rdf = recent_reports(conn, region_id, limit=1000)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button("Download runs.csv", df.to_csv(index=False).encode("utf-8"), file_name="runs.csv")
    with c2:
        st.download_button("Download alerts.csv", adf.to_csv(index=False).encode("utf-8"), file_name="alerts.csv")
    with c3:
        st.download_button("Download reports.csv", rdf.to_csv(index=False).encode("utf-8"), file_name="reports.csv")

def tab_admin(conn: sqlite3.Connection, region_id: int, region_name: str, country: str):
    st.header("Admin")
    st.caption("Local SQLite storage by default. Designed to run anywhere without extra infrastructure.")
    st.write(f"**Active region:** {region_name} ({country})")

    st.subheader("Database")
    if st.button("Reset DB (danger)", type="secondary"):
        conn.executescript("""
        DROP TABLE IF EXISTS alerts;
        DROP TABLE IF EXISTS field_reports;
        DROP TABLE IF EXISTS runs;
        DROP TABLE IF EXISTS regions;
        """)
        conn.commit()
        db_init(conn)
        ensure_region(conn, region_name, country)
        st.success("Database reset.")
        st.rerun()

def main():
    set_page()
    db_path = st.session_state.get("db_path", DB_PATH_DEFAULT)
    conn = db_connect(db_path)
    db_init(conn)

    region_id, region_name, country = sidebar_controls(conn)

    tabs = st.tabs(["Situation", "Create Run", "Field Reports", "Exports", "Admin"])
    with tabs[0]:
        tab_situation(conn, region_id)
    with tabs[1]:
        tab_create_run(conn, region_id)
    with tabs[2]:
        tab_field_reports(conn, region_id)
    with tabs[3]:
        tab_exports(conn, region_id)
    with tabs[4]:
        tab_admin(conn, region_id, region_name, country)

if __name__ == "__main__":
    main()
