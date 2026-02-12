from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from api.db import conn
from api.redis_client import rconn
from api.settings import Settings
from or_shared.rate_limit import token_bucket_allow
import hashlib

router = APIRouter()

class ReportIn(BaseModel):
    lat: float
    lon: float
    report_type: str = Field(pattern="^(borehole|well|river|tap|market|health|other)$")
    status: str = Field(pattern="^(ok|low|dry|inaccessible|crowded|price_spike)$")
    notes: str | None = None
    source_hint: str | None = None
    region_id: str | None = None

def coarse_geohash(lat: float, lon: float, precision_deg: float = 0.05) -> str:
    lat_r = round(lat / precision_deg) * precision_deg
    lon_r = round(lon / precision_deg) * precision_deg
    key = f"{lat_r:.2f},{lon_r:.2f}"
    return hashlib.sha1(key.encode("utf-8")).hexdigest()[:10]

@router.post("")
def create(r: ReportIn, request: Request):
    s = Settings()
    redis = rconn()
    ip = request.client.host if request.client else "unknown"
    key = f"reports:ip:{ip}"
    cap = s.reports_per_ip_per_hour
    refill = cap / 3600.0
    if not token_bucket_allow(redis, key, capacity=cap, refill_per_sec=refill):
        raise HTTPException(status_code=429, detail="Report rate limit exceeded")
    now = datetime.now(timezone.utc)
    gh = coarse_geohash(r.lat, r.lon)
    with conn().cursor() as cur:
        cur.execute(
            "INSERT INTO field_reports(created_utc, region_id, coarse_geohash, lat, lon, report_type, status, notes, source_hint, trust_score) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (now, r.region_id, gh, r.lat, r.lon, r.report_type, r.status, r.notes, r.source_hint, 0.5)
        )
    return {"ok": True, "created_utc": now.isoformat(), "coarse_geohash": gh}
