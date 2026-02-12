from fastapi import APIRouter, HTTPException
from api.db import conn

router = APIRouter()

@router.get("/latest")
def latest(severity_min: int=2, limit: int=200,
           min_lat: float | None=None, max_lat: float | None=None, min_lon: float | None=None, max_lon: float | None=None):
    with conn().cursor() as cur:
        cur.execute("SELECT id, run_id, run_time_utc FROM runs ORDER BY run_time_utc DESC LIMIT 1")
        run = cur.fetchone()
        if not run:
            raise HTTPException(status_code=404, detail="No runs yet")
        run_db_id = run[0]
        where = "WHERE a.run_id=%s AND a.severity >= %s"
        params = [run_db_id, severity_min]
        if None not in (min_lat, max_lat, min_lon, max_lon):
            where += " AND r.lat BETWEEN %s AND %s AND r.lon BETWEEN %s AND %s"
            params += [min_lat, max_lat, min_lon, max_lon]
        q = f"""
        SELECT a.region_id, a.domain, a.severity, a.title, a.message, a.details,
               a.valid_start_utc, a.valid_end_utc, a.created_utc,
               r.lat, r.lon, r.admin0, r.admin1, r.admin2
        FROM alerts a
        LEFT JOIN regions r ON r.region_id = a.region_id
        {where}
        ORDER BY a.severity DESC, a.created_utc DESC
        LIMIT %s
        """
        params.append(limit)
        cur.execute(q, params)
        rows = cur.fetchall()
    return {
        "run_id": run[1],
        "alerts": [{
            "region_id": r[0], "domain": r[1], "severity": r[2],
            "title": r[3], "message": r[4], "details": r[5],
            "valid_start_utc": r[6].isoformat(), "valid_end_utc": r[7].isoformat(),
            "created_utc": r[8].isoformat(),
            "lat": r[9], "lon": r[10], "admin0": r[11], "admin1": r[12], "admin2": r[13]
        } for r in rows]
    }
