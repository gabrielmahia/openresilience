# OpenResilience (ALL-OUT) • Drought / Water / Food Stress System (v0.3)

This is a **full-stack, safety-first crisis intelligence + coordination system** built for drought, water scarcity, and famine risk.

## Architecture
- `db` Postgres: indicators, alerts, reports, subscriptions, prices
- `api` FastAPI: read/write endpoints + PDF briefs + export
- `worker` computes WSI/FSI/MSI/CRI + generates alerts (adapter-driven)
- `notifier` pushes alerts to subscriptions (provider adapters: mock/Twilio/Africa's Talking stubs)
- `ui` Streamlit: Situation • Water • Food • Markets • Logistics • Alerts • Reports • Briefs • Admin
- `docs` threat model, safety policy, data integrity rules

## Safety defaults
- No public high-resolution water-point map by default.
- Field reports stored as **coarse geohash** + optional admin region.
- Alerts always include **timestamp + confidence + provenance + assumptions**.
- Rate-limiting on inbound reports/subscriptions to reduce abuse.

## Run
```bash
cp .env.example .env
docker compose up --build
```

Open:
- UI: http://localhost:8501
- API: http://localhost:8000/docs
