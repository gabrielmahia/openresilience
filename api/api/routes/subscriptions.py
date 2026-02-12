from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from api.db import conn
from api.redis_client import rconn
from api.settings import Settings
from or_shared.rate_limit import token_bucket_allow
import hashlib

router = APIRouter()

class SubIn(BaseModel):
    channel: str = Field(pattern="^(sms|whatsapp|email)$")
    contact: str
    region_id: str
    severity_min: int = Field(ge=1, le=3)

def h(x: str) -> str:
    return hashlib.sha256(x.strip().lower().encode("utf-8")).hexdigest()

@router.post("")
def subscribe(su: SubIn, request: Request):
    s = Settings()
    redis = rconn()
    ip = request.client.host if request.client else "unknown"
    key = f"subs:ip:{ip}"
    cap = s.subs_per_ip_per_hour
    refill = cap / 3600.0
    if not token_bucket_allow(redis, key, capacity=cap, refill_per_sec=refill):
        raise HTTPException(status_code=429, detail="Subscription rate limit exceeded")
    now = datetime.now(timezone.utc)
    with conn().cursor() as cur:
        cur.execute(
            "INSERT INTO subscriptions(created_utc, channel, contact_hash, region_id, severity_min, active, meta) "
            "VALUES (%s,%s,%s,%s,%s,TRUE,%s)",
            (now, su.channel, h(su.contact), su.region_id, su.severity_min, "{}")
        )
    return {"ok": True}
