import os, time
from datetime import datetime, timezone, timedelta
from notifier.db import conn
from notifier.providers import get_provider

def format_alert(a):
    return f"[{a['domain'].upper()} S{a['severity']}] {a['title']} • {a['region_id']}"

def loop():
    provider = get_provider()
    interval = int(os.environ.get("NOTIFY_INTERVAL_SEC","120"))
    while True:
        try:
            with conn().cursor() as cur:
                cur.execute("SELECT id FROM runs ORDER BY run_time_utc DESC LIMIT 1")
                run = cur.fetchone()
                if not run:
                    time.sleep(interval); continue
                run_db_id = run[0]
                cur.execute(
                    "SELECT region_id, domain, severity, title, created_utc FROM alerts "
                    "WHERE run_id=%s AND created_utc >= (NOW() AT TIME ZONE 'UTC') - INTERVAL '2 hours' "
                    "ORDER BY created_utc DESC LIMIT 200",
                    (run_db_id,)
                )
                alerts = [{"region_id": r[0], "domain": r[1], "severity": r[2], "title": r[3], "created_utc": r[4]} for r in cur.fetchall()]
                cur.execute("SELECT id, channel, contact_hash, region_id, severity_min, last_sent_utc FROM subscriptions WHERE active=TRUE")
                subs = cur.fetchall()
                now = datetime.now(timezone.utc)
                for sid, channel, chash, region_id, sev_min, last_sent in subs:
                    matching = [a for a in alerts if a["region_id"] == region_id and a["severity"] >= sev_min]
                    if not matching:
                        continue
                    if last_sent and (now - last_sent) < timedelta(seconds=interval*2):
                        continue
                    try:
                        provider.send(chash, channel, format_alert(matching[0]))
                        cur.execute("UPDATE subscriptions SET last_sent_utc=%s WHERE id=%s", (now, sid))
                    except Exception:
                        pass
        except Exception:
            pass
        time.sleep(interval)

if __name__ == "__main__":
    loop()
