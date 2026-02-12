
# OpenResilience — Drought / Water / Food Stress Intelligence System

![License](https://img.shields.io/badge/license-Apache--2.0-blue)
![Status](https://img.shields.io/badge/status-Research%20Infrastructure-blue)
![Data](https://img.shields.io/badge/data-DEMO%20%2F%20Simulated-orange)

> **Data Status:** This system currently runs on **simulated demonstration data**.
> All stress indices, forecasts, and severity scores are generated from statistical
> models seeded with synthetic values — they do **not** reflect real-time conditions.
> See [Data Adapters](docs/DATA_ADAPTERS.md) for the roadmap to NASA satellite integration.

## Overview
OpenResilience is a crisis-signal intelligence system designed to surface environmental and market stress indicators related to drought, water scarcity, and food insecurity.

This platform is intended as:
- Decision-support infrastructure
- Research tooling
- Coordination augmentation

It is NOT an automated decision authority.

## Mission
Reduce information asymmetry in environments where resource stress impacts human well-being.

## Architecture

| Component | Purpose | Status |
|-----------|---------|--------|
| `app.py` | Community Streamlit dashboard (Kenya, 47 counties) | Demo data |
| `api/` | FastAPI REST service (indicators, alerts, exports) | Functional |
| `worker/` | Background data pipeline (scoring, indexing) | Synthetic adapter only |
| `notifier/` | SMS/WhatsApp alert dispatch | Stubs (Twilio, Africa's Talking) |
| `shared/` | Pure scoring and trust logic | Tested |

## Quick Start

```bash
# Standalone demo (no Docker required)
pip install -r requirements.txt
streamlit run app.py

# Full microservice stack
docker compose up --build
```

## Governance Alignment
This repository operates under:

- Ethics-first engineering
- Harm minimization
- Privacy-preserving data structures
- Transparency of assumptions

## Usage Notice
This system produces probabilistic signals — not certainties.
All outputs must be validated locally before operational use.

## License
Apache License 2.0 — See [LICENSE](LICENSE).
