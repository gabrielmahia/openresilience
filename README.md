# 💧 WapiMaji — Water & Drought Intelligence Kenya

> **Wapi Maji?** /wɑːpi mɑːdʒi/ — *Kiswahili*: "Where is the water?"

**Water & food stress intelligence for Kenya's 47 counties.**  
Built for farmers, NGOs, county governments, and community leaders.

[![Live App](https://img.shields.io/badge/Live%20App-wapimaji.streamlit.app-FF4B4B?logo=streamlit)](https://wapimaji.streamlit.app/)
[![Live Data](https://img.shields.io/badge/Live%20Data-Open-Meteo%20%C2%B7%20NDMA-00b4d8)](#openresilience)
[![License](https://img.shields.io/badge/license-AGPL--3.0-blue)](LICENSE)
[![Status](https://img.shields.io/badge/status-Demo%20Data-orange)](docs/INDEX_METHODOLOGY.md)
[![Coverage](https://img.shields.io/badge/coverage-47%20Counties-brightgreen)](https://wapimaji.streamlit.app/)
[![SMS](https://img.shields.io/badge/SMS-Africa's%20Talking-green)](QUICKSTART_SMS.md)

> 🔶 **DEMO MODE** — Current data is synthetic. Indices are computed from real formulas against generated inputs. [Index methodology](docs/INDEX_METHODOLOGY.md) is documented and production data adapters are underway.

**[→ Open the live platform](https://wapimaji.streamlit.app/)**

---

## What it does

OpenResilience surfaces four stress indices updated per monitoring cycle:

| Index | Measures | Key inputs |
|-------|----------|------------|
| **WSI** — Water Stress | Rainfall deficit + soil dryness | CHIRPS rainfall, SMAP soil moisture |
| **FSI** — Food Stress | Crop production risk | WSI + NDVI vegetation anomaly + field reports |
| **MSI** — Market Stress | Staple food price pressure | Maize price change vs seasonal average |
| **CRI** — Composite Risk | Overall household resilience risk | Weighted combination of WSI/FSI/MSI |

[→ Full index methodology, weights, and data sources](docs/INDEX_METHODOLOGY.md)

---

## SMS alerts reach farmers without smartphones

The platform sends **bilingual SMS alerts** (English + Kiswahili) via Africa's Talking to any mobile phone — including basic feature phones with no data plan. County coordinators subscribe farmers; alerts trigger automatically when CRI crosses Watch/Alert/Emergency thresholds.

```
[OpenResilience] Turkana Alert:
Water stress HIGH (WSI 0.74).
Plant sorghum only if rains confirmed.
Nafaka: panda mtama tu ukiwa na uhakika wa mvua.
```

[→ SMS setup guide](QUICKSTART_SMS.md) · [→ Africa's Talking integration](STREAMLIT_SMS_SETUP.md)

---

## Architecture

```
app.py                          ← Streamlit UI (farmer + NGO views)
src/openresilience/             ← Core scoring, agriculture, export
  adapters/                     ← NASA IMERG, SMAP, Earth Engine connectors
api/                            ← FastAPI REST layer for programmatic access
notifier/                       ← SMS/WhatsApp alert worker
worker/                         ← Scheduled data refresh jobs
shared/or_shared/               ← Shared scoring, trust labeling, rate limiting
data/                           ← County baseline data, seed files
migrations/                     ← Database schema versioning
```

The architecture is production-ready: separate API, worker, and notifier services with Docker Compose orchestration. The current bottleneck is connecting real satellite data sources — not the infrastructure.

---

## Roadmap to live data

See [docs/DATA_ADAPTERS.md](docs/DATA_ADAPTERS.md) for full integration plan.

**Highest-impact next step:** CHIRPS rainfall data for one county (API is free, no signup required). One real county transforms the narrative from demo to operational pilot.

| Source | Status | Priority |
|--------|--------|----------|
| CHIRPS rainfall | Adapter written, pending activation | 🔴 High |
| NASA SMAP soil moisture | Adapter written | 🔴 High |
| NDMA field reports | Integration designed | 🟡 Medium |
| WFP price data | Planned | 🟡 Medium |
| Google Earth Engine NDVI | Adapter written | 🟢 Lower |

---

## Quick start

```bash
pip install -r requirements.txt
streamlit run app.py
```

For SMS setup: [QUICKSTART_SMS.md](QUICKSTART_SMS.md)  
For deployment: [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

---

## Governance

This repository operates under strict ethics-first principles:

- 🔶 **DEMO vs REAL** — All synthetic data is clearly labelled. No demo output is presented as operational.
- 📐 **Documented methodology** — Index weights and formulas are explained and referenced ([INDEX_METHODOLOGY.md](docs/INDEX_METHODOLOGY.md)).
- 🔒 **No PII collection** — Community data is anonymised at source; no personal information is stored in demo mode.
- ⚠️ **Not a decision authority** — This is decision-support infrastructure. All outputs require local validation before operational use.

See also: [ETHICS.md](ETHICS.md) · [DATA_POLICY.md](DATA_POLICY.md) · [GOVERNANCE.md](GOVERNANCE.md) · [SECURITY.md](SECURITY.md)

---

## License

**AGPL-3.0** — Free for NGOs, county governments, researchers, and community organisations.  
Requires source sharing if deployed as a public web service (AGPL §13).  
For commercial licensing: [contact@aikungfu.dev](mailto:contact@aikungfu.dev) with subject "OpenResilience Commercial License"

See [LICENSE](LICENSE) and [NOTICE](NOTICE).

---

## Citation

```
Mahia, Gabriel (2026). OpenResilience Kenya: Water & Food Stress Intelligence Platform.
GitHub: https://github.com/gabrielmahia/openresilience · License: AGPL-3.0
```

---

**Built for Kenya's communities 🇰🇪 · Powered by satellite methodology 🛰️ · Driven by local knowledge 🌍**
