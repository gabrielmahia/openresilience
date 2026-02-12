CREATE INDEX IF NOT EXISTS idx_regions_latlon ON regions(lat, lon);
CREATE INDEX IF NOT EXISTS idx_indicators_region_metric ON indicators(region_id, metric, updated_utc DESC);
CREATE INDEX IF NOT EXISTS idx_alerts_recent ON alerts(created_utc DESC);
CREATE INDEX IF NOT EXISTS idx_reports_recent ON field_reports(created_utc DESC);
CREATE INDEX IF NOT EXISTS idx_subs_active ON subscriptions(active, region_id);
