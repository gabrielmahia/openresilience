from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from api.db import conn
import csv, io

router = APIRouter()

@router.get("/alerts.csv", response_class=PlainTextResponse)
def alerts_csv(limit: int=5000):
    with conn().cursor() as cur:
        cur.execute("SELECT run_id, region_id, domain, severity, title, message, created_utc FROM alerts ORDER BY created_utc DESC LIMIT %s", (limit,))
        rows = cur.fetchall()
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["run_db_id","region_id","domain","severity","title","message","created_utc"])
    w.writerows(rows)
    return out.getvalue()

@router.get("/indicators.csv", response_class=PlainTextResponse)
def indicators_csv(metric: str="cri", limit: int=20000):
    with conn().cursor() as cur:
        cur.execute(
            "SELECT run_id, region_id, metric, value, severity, confidence, updated_utc FROM indicators "
            "WHERE metric=%s ORDER BY severity DESC, updated_utc DESC LIMIT %s",
            (metric, limit)
        )
        rows = cur.fetchall()
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["run_db_id","region_id","metric","value","severity","confidence","updated_utc"])
    w.writerows(rows)
    return out.getvalue()
