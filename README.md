# OpenResilience Platform 🛰️
**Drought • Water • Food Stress Intelligence**

![License](https://img.shields.io/badge/license-CC%20BY--NC--ND-red)

## What this is
OpenResilience is a **decision-support** dashboard that turns fragmented signals into interpretable indices:

- **WSI** Water Stress Index
- **FSI** Food Stress Index
- **MSI** Market Stress Index
- **CRI** Composite Risk Index

**Signals, not certainties:** validate locally before acting. Avoid sharing precise resource locations publicly.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## First run (recommended)
Open the sidebar and click **Seed Demo Data** to populate sample runs + reports.

## Storage
Default storage is **SQLite** (`openresilience.db`) so the system runs anywhere without extra infrastructure.
For multi-user production deployments, migrate to Postgres and add authentication.

## License
CC BY-NC-ND 4.0. See LICENSE.
