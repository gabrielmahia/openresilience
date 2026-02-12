
# OpenResilience — Drought / Water / Food Stress Intelligence System

![License](https://img.shields.io/badge/license-CC--BY--NC--ND-red)
![Status](https://img.shields.io/badge/status-Research%20Infrastructure-blue)
![Data](https://img.shields.io/badge/data-DEMO%20%2F%20Simulated-orange)

> **⚠️ DATA STATUS:** This system currently runs on **DEMO / SIMULATED DATA**.  
> All water stress indices, forecasts, and severity scores are generated from statistical models  
> seeded with synthetic values — they do **NOT** reflect real-time satellite or ground-truth conditions.  
> **DO NOT use for operational decisions.**

## Overview
OpenResilience is a crisis-signal intelligence system designed to surface environmental and market stress indicators related to drought, water scarcity, and food insecurity.

This platform is intended as:
- Decision-support infrastructure (when connected to real data sources)
- Research tooling for resilience planning methodologies
- Coordination augmentation for community-level preparedness

**It is NOT an automated decision authority.**

## Current Data Sources (Demo Mode)
- 🔶 **Water Stress Indices**: Synthetic scoring algorithms (0-10 scale)
- 🔶 **Population Data**: Static 2019 census estimates
- 🔶 **Geographic Coverage**: All 47 Kenyan counties + 2 focus areas
- 🔶 **Forecast Models**: Simulated trend projections (not predictive)

## Roadmap to Production Data
See [docs/DATA_ADAPTERS.md](docs/DATA_ADAPTERS.md) for planned integration with:
- NASA MODIS satellite imagery (real-time drought monitoring)
- CHIRPS rainfall estimates
- FEWS NET food security alerts
- Kenya Meteorological Department feeds

## Mission
Reduce information asymmetry in environments where resource stress impacts human well-being.

## Governance Alignment
This repository operates under:

- **Ethics-first engineering**: No harm amplification, no misleading predictions
- **Harm minimization**: Clear data provenance labeling
- **Privacy-preserving data structures**: No PII collection in demo mode
- **Transparency of assumptions**: All scoring logic documented

## Risk Disclaimer
⚠️ **This is demonstration software.**  
Outputs are not validated for operational use. Any deployment in real decision-making contexts requires:
1. Connection to authoritative data sources
2. Local validation by domain experts
3. Ethical review of risk communication methods
4. Community consent for data usage

## Usage Notice
This system produces probabilistic signals — not certainties.  
All outputs must be validated locally before operational use.

## License
**Creative Commons Attribution-NonCommercial-NoDerivatives 4.0**  
See [LICENSE](LICENSE) file.

- ✅ Study, reference, and fork for personal learning
- ❌ Commercial use prohibited
- ❌ Distribution of modified versions prohibited

For collaboration inquiries: contact@aikungfu.dev

## Quick Start
```bash
pip install -r requirements.txt
streamlit run app.py
```

Visit `http://localhost:8501` to explore the demo interface.
