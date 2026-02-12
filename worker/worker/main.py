from datetime import timedelta, timezone
from worker.settings import Settings
from worker.db import conn
from worker.adapters.synthetic import load_synthetic
from worker.logic import compute_scores
from or_shared.timeutils import utcnow, iso_z
from or_shared.trust import confidence_from_inputs

def region_id_for_cell(lat_center, lon_center, step):
    return f"grid_{str(step).replace('.','p')}_lat_{lat_center:.2f}_lon_{lon_center:.2f}"

def cell_center(i, j, shape, step_deg):
    h, w = shape
    lat = 90 - (i + 0.5) * (180 / h)
    lon = -180 + (j + 0.5) * (360 / w)
    lat_c = (int(lat / step_deg) * step_deg) + step_deg/2
    lon_c = (int(lon / step_deg) * step_deg) + step_deg/2
    return lat_c, lon_c

def run_once():
    s = Settings()
    now = utcnow()
    run_id = iso_z(now)
    obs_rain, typ_rain, soil_pct, ndvi_anom, persistence = load_synthetic()
    notes = "synthetic adapter (offline demo). Replace with real adapters."
    anom, soil, ndvi, pers, wsi, fsi, msi, cri = compute_scores(obs_rain, typ_rain, soil_pct, ndvi_anom, persistence)
    confidence = confidence_from_inputs(0.0, 0, 180)
    valid_start = (now - timedelta(days=30)).astimezone(timezone.utc)
    valid_end = now.astimezone(timezone.utc)
    with conn().cursor() as cur:
        cur.execute("INSERT INTO runs(run_id, run_time_utc, version, adapter, notes) VALUES (%s,%s,%s,%s,%s) RETURNING id",
                    (run_id, now, s.version, s.adapter, notes))
        run_db_id = int(cur.fetchone()[0])
        h, w = cri.shape
        step = s.grid_step_deg
        prov = {"adapter": s.adapter, "assumption": "proxy thresholds", "run_id": run_id}
        for i in range(h):
            for j in range(w):
                lat_c, lon_c = cell_center(i, j, (h, w), step)
                rid = region_id_for_cell(lat_c, lon_c, step)
                cur.execute("INSERT INTO regions(region_id, region_name, level, lat, lon, meta) VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT (region_id) DO NOTHING",
                            (rid, None, "grid", lat_c, lon_c, "{}"))
                def ins(metric, val, sev):
                    cur.execute("INSERT INTO indicators(run_id, region_id, metric, value, severity, confidence, provenance, updated_utc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                                (run_db_id, rid, metric, float(val), int(sev), confidence, prov, now))
                ins("rain_anom", anom[i,j], 0); ins("soil_pct", soil[i,j], 0); ins("ndvi_anom", ndvi[i,j], 0); ins("persistence_wk", pers[i,j], 0)
                ins("wsi", wsi[i,j], wsi[i,j]); ins("fsi", fsi[i,j], fsi[i,j]); ins("msi", msi[i,j], msi[i,j]); ins("cri", cri[i,j], cri[i,j])
                sev = int(cri[i,j])
                if sev >= 2:
                    title = "Crisis risk elevated" if sev == 2 else "Crisis risk severe"
                    msg = "Composite drought/water/food stress signals elevated. Verify locally; prioritize vulnerable groups. Avoid rumor-based movements."
                    details = {"cri": sev, "wsi": int(wsi[i,j]), "fsi": int(fsi[i,j]), "msi": int(msi[i,j]), "confidence": confidence}
                    cur.execute("INSERT INTO alerts(run_id, region_id, domain, severity, title, message, details, valid_start_utc, valid_end_utc, created_utc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                (run_db_id, rid, "composite", sev, title, msg, details, valid_start, valid_end, now))
    print(f"OK run_id={run_id}")

if __name__ == "__main__":
    run_once()
