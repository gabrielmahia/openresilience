from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from api.db import conn
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

router = APIRouter()

def get_latest_metrics(region_id: str):
    with conn().cursor() as cur:
        cur.execute("SELECT id FROM runs ORDER BY run_time_utc DESC LIMIT 1")
        run = cur.fetchone()
        if not run:
            raise HTTPException(status_code=404, detail="No runs")
        cur.execute(
            "SELECT metric, value, severity, confidence, updated_utc FROM indicators "
            "WHERE region_id=%s AND metric IN ('wsi','fsi','msi','cri') ORDER BY updated_utc DESC",
            (region_id,)
        )
        ind = cur.fetchall()
        cur.execute(
            "SELECT domain, severity, title, message, created_utc FROM alerts "
            "WHERE region_id=%s ORDER BY created_utc DESC LIMIT 10",
            (region_id,)
        )
        alerts = cur.fetchall()
        cur.execute("SELECT lat, lon, admin0, admin1, admin2 FROM regions WHERE region_id=%s", (region_id,))
        reg = cur.fetchone()
    return reg, ind, alerts

@router.get("/region/{region_id}.pdf")
def region_pdf(region_id: str):
    reg, ind, alerts = get_latest_metrics(region_id)
    if not reg:
        raise HTTPException(status_code=404, detail="Unknown region")
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    w, h = letter
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, h-72, "OpenResilience • Region Brief")
    c.setFont("Helvetica", 10)
    c.drawString(72, h-90, f"Region: {region_id}")
    c.drawString(72, h-105, f"Lat/Lon: {reg[0]:.2f}, {reg[1]:.2f}  Admin: {reg[2] or ''} / {reg[3] or ''} / {reg[4] or ''}")
    y = h-135
    c.setFont("Helvetica-Bold", 12)
    c.drawString(72, y, "Latest Metrics")
    y -= 16
    c.setFont("Helvetica", 10)
    for m,v,sev,conf,ts in ind[:20]:
        c.drawString(72, y, f"{m.upper()}  value={v:.2f}  severity={sev}  conf={conf}  updated={ts.isoformat()}")
        y -= 12
        if y < 120:
            c.showPage(); y = h-72
    c.setFont("Helvetica-Bold", 12)
    c.drawString(72, y, "Recent Alerts")
    y -= 16
    c.setFont("Helvetica", 10)
    for d,sev,title,msg,ts in alerts:
        c.drawString(72, y, f"[{d}] S{sev} {title} ({ts.isoformat()})")
        y -= 12
        for line in (msg[:240], msg[240:480]):
            if line:
                c.drawString(92, y, line)
                y -= 12
        y -= 4
        if y < 120:
            c.showPage(); y = h-72
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(72, 72, "Disclaimer: probabilistic signals. Verify locally. Do not use as sole basis for travel or enforcement.")
    c.save()
    return Response(content=buf.getvalue(), media_type="application/pdf")
