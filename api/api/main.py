from fastapi import FastAPI
from api.middleware import RateLimitMiddleware
from api.routes.health import router as health
from api.routes.runs import router as runs
from api.routes.indicators import router as indicators
from api.routes.alerts import router as alerts
from api.routes.reports import router as reports
from api.routes.subscriptions import router as subs
from api.routes.exports import router as exports
from api.routes.briefs import router as briefs

app = FastAPI(title="OpenResilience API", version="0.3.0")
app.add_middleware(RateLimitMiddleware)

app.include_router(health, prefix="/health")
app.include_router(runs, prefix="/runs")
app.include_router(indicators, prefix="/indicators")
app.include_router(alerts, prefix="/alerts")
app.include_router(reports, prefix="/reports")
app.include_router(subs, prefix="/subscriptions")
app.include_router(exports, prefix="/exports")
app.include_router(briefs, prefix="/briefs")
