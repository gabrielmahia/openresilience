from datetime import datetime, timezone

def utcnow():
    return datetime.now(timezone.utc)

def iso_z(dt):
    return dt.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
