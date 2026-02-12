from fastapi import APIRouter
from api.db import conn

router = APIRouter()

@router.get("/top")
def top(metric: str="cri", severity_min: int=2, limit: int=200,
        min_lat: float | None=None, max_lat: float | None=None, min_lon: float | None=None, max_lon: float | None=None):
    where = "WHERE i.metric=%s AND i.severity >= %s"
    params = [metric, severity_min]
    if None not in (min_lat, max_lat, min_lon, max_lon):
        where += " AND r.lat BETWEEN %s AND %s AND r.lon BETWEEN %s AND %s"
        params += [min_lat, max_lat, min_lon, max_lon]
    q = f"""
    SELECT i.region_id, i.value, i.severity, i.confidence, i.updated_utc, r.lat, r.lon, r.admin0, r.admin1, r.admin2
    FROM indicators i
    LEFT JOIN regions r ON r.region_id = i.region_id
    {where}
    ORDER BY i.severity DESC, i.value DESC
    LIMIT %s
    """
    params.append(limit)
    with conn().cursor() as cur:
        cur.execute(q, params)
        rows = cur.fetchall()
    return [{
        "region_id": a[0], "value": a[1], "severity": a[2], "confidence": a[3],
        "updated_utc": a[4].isoformat(),
        "lat": a[5], "lon": a[6], "admin0": a[7], "admin1": a[8], "admin2": a[9]
    } for a in rows]
