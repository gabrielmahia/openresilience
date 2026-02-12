# Architecture

Single-process Streamlit app + local SQLite store.

Tables:
- regions
- runs (signals + scores)
- field_reports (ground truth)
- alerts (conservative notifications)

Why SQLite: zero infra required for demos and pilots.
