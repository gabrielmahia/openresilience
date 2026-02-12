CREATE TABLE IF NOT EXISTS runs (
  id BIGSERIAL PRIMARY KEY,
  run_id TEXT NOT NULL UNIQUE,
  run_time_utc TIMESTAMP NOT NULL,
  version TEXT NOT NULL,
  adapter TEXT NOT NULL,
  notes TEXT
);

CREATE TABLE IF NOT EXISTS regions (
  id BIGSERIAL PRIMARY KEY,
  region_id TEXT NOT NULL UNIQUE,
  region_name TEXT,
  level TEXT NOT NULL,
  lat REAL,
  lon REAL,
  admin0 TEXT,
  admin1 TEXT,
  admin2 TEXT,
  meta JSONB
);

CREATE TABLE IF NOT EXISTS indicators (
  id BIGSERIAL PRIMARY KEY,
  run_id BIGINT NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
  region_id TEXT NOT NULL,
  metric TEXT NOT NULL,
  value REAL NOT NULL,
  severity INT NOT NULL CHECK (severity BETWEEN 0 AND 3),
  confidence TEXT NOT NULL CHECK (confidence IN ('high','medium','low')),
  provenance JSONB NOT NULL,
  updated_utc TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS alerts (
  id BIGSERIAL PRIMARY KEY,
  run_id BIGINT NOT NULL REFERENCES runs(id) ON DELETE CASCADE,
  region_id TEXT NOT NULL,
  domain TEXT NOT NULL,
  severity INT NOT NULL CHECK (severity BETWEEN 1 AND 3),
  title TEXT NOT NULL,
  message TEXT NOT NULL,
  details JSONB NOT NULL,
  valid_start_utc TIMESTAMP NOT NULL,
  valid_end_utc TIMESTAMP NOT NULL,
  created_utc TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS prices (
  id BIGSERIAL PRIMARY KEY,
  region_id TEXT NOT NULL,
  commodity TEXT NOT NULL,
  price REAL NOT NULL,
  currency TEXT NOT NULL,
  unit TEXT NOT NULL,
  source TEXT NOT NULL,
  observed_utc TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS field_reports (
  id BIGSERIAL PRIMARY KEY,
  created_utc TIMESTAMP NOT NULL,
  region_id TEXT,
  coarse_geohash TEXT NOT NULL,
  lat REAL NOT NULL,
  lon REAL NOT NULL,
  report_type TEXT NOT NULL,
  status TEXT NOT NULL,
  notes TEXT,
  source_hint TEXT,
  trust_score REAL NOT NULL DEFAULT 0.5
);

CREATE TABLE IF NOT EXISTS subscriptions (
  id BIGSERIAL PRIMARY KEY,
  created_utc TIMESTAMP NOT NULL,
  channel TEXT NOT NULL,
  contact_hash TEXT NOT NULL,
  region_id TEXT NOT NULL,
  severity_min INT NOT NULL CHECK (severity_min BETWEEN 1 AND 3),
  active BOOLEAN NOT NULL DEFAULT TRUE,
  last_sent_utc TIMESTAMP,
  meta JSONB
);

CREATE TABLE IF NOT EXISTS audit_log (
  id BIGSERIAL PRIMARY KEY,
  created_utc TIMESTAMP NOT NULL,
  actor TEXT,
  action TEXT NOT NULL,
  detail JSONB
);
