from fastapi import APIRouter, HTTPException
from api.db import conn
router = APIRouter()

@router.get("/latest")
def latest():
    with conn().cursor() as cur:
        cur.execute("SELECT id, run_id, run_time_utc, version, adapter, notes FROM runs ORDER BY run_time_utc DESC LIMIT 1")
        r = cur.fetchone()
    if not r:
        raise HTTPException(status_code=404, detail="No runs yet")
    return {"id": r[0], "run_id": r[1], "run_time_utc": r[2].isoformat(), "version": r[3], "adapter": r[4], "notes": r[5]}
