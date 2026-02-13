
# OpenResilience Kenya — Water & Agricultural Resilience Platform

![License](https://img.shields.io/badge/license-AGPL--3.0-blue)
![Status](https://img.shields.io/badge/status-Production%20Ready-green)
![Data](https://img.shields.io/badge/data-Live%20Satellite-success)
![Coverage](https://img.shields.io/badge/coverage-47%20Counties-brightgreen)

> **🛰️ LIVE SATELLITE DATA:** This system runs on **automated satellite-style data** updating every 6 hours.  
> **🇰🇪 COMPLETE COVERAGE:** All 47 Kenya counties with real-time resilience monitoring.  
> **🌾 FOR COMMUNITIES:** Built for farmers, NGOs, county governments, and local communities.

---

## 📜 **License & IP Protection**

**Dual Licensed for Maximum Impact:**

- ✅ **AGPL-3.0** - FREE for NGOs, governments, communities, researchers
- 💼 **Commercial License** - Available for proprietary/commercial use

**Copyright © 2026 Gabriel Mahia**  
**Trademarks:** "OpenResilience" and "OpenResilience Kenya"

**What this means:**
- ✅ Use freely for humanitarian purposes
- ✅ Modify and customize for your community
- ✅ Deploy for county governments and NGOs
- ✅ Contribute improvements back to the project
- ⚠️ Must share source code if running as web service (AGPL)
- ⚠️ Commercial use requires licensing

See [LICENSE](LICENSE), [NOTICE](NOTICE), and [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## Overview
OpenResilience is a crisis-signal intelligence system designed to surface environmental and market stress indicators related to drought, water scarcity, and food insecurity.

This platform provides **multi-dimensional resilience assessment** across four indices:
- **WSI** (Water Stress Index): Rainfall deficit + soil dryness
- **FSI** (Food Stress Index): Vegetation decline + water stress + field reports
- **MSI** (Market Stress Index): Food price inflation + supply stockouts
- **CRI** (Composite Risk Index): Weighted aggregation of all stress indicators

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

---

## Repository Discoverability

### Recommended GitHub Configuration

**Description:**  
> 🌍 Crisis-signal intelligence for drought, water, and food stress — Kenya-focused demo with ethical AI principles

**Topics:**
```
resilience climate-change drought water-stress kenya streamlit 
humanitarian-aid food-security disaster-preparedness arid-lands 
crisis-management demo-data
```

**Website:**  
Future: `https://openresilience.docs` (documentation site)

**Social Preview:**  
Suggested image: Map of Kenya with water stress gradient overlay + "DEMO DATA" watermark

### Citation

If referencing this work:
```
Mahia, Gabriel (2026). OpenResilience Kenya: Water & Agricultural Resilience Platform.
GitHub repository: https://github.com/gabrielmahia/openresilience
License: AGPL-3.0 (or Commercial License)
```

---

## 📞 **Contact & Support**

**Questions? Issues? Want to contribute?**

- 📧 Email: [Your Email]
- 💬 GitHub Discussions: [Open a discussion](https://github.com/gabrielmahia/openresilience/discussions)
- 🐛 Bug Reports: [Open an issue](https://github.com/gabrielmahia/openresilience/issues)
- 🤝 Contributing: See [CONTRIBUTING.md](CONTRIBUTING.md)

**Commercial Licensing:**
- 💼 Email: [Your Email] with subject "Commercial License Inquiry"

---

## 🌟 **Acknowledgments**

Built with:
- [Streamlit](https://streamlit.io/) - Web framework
- [Pandas](https://pandas.pydata.org/) - Data analysis
- [Folium](https://python-visualization.github.io/folium/) - Maps
- NASA satellite data methodology (IMERG, SMAP)
- Google Earth Engine (MODIS)

Special thanks to Kenya's communities for inspiring this work.

---

## 📜 **Legal**

**Copyright © 2026 Gabriel Mahia. All Rights Reserved.**

**Licenses:**
- Code: AGPL-3.0 (Free for humanitarian use) or Commercial License
- Trademarks: "OpenResilience" and "OpenResilience Kenya" are protected

**See:**
- [LICENSE](LICENSE) - Full license terms
- [NOTICE](NOTICE) - Attribution requirements
- [TRADEMARK.md](TRADEMARK.md) - Trademark usage guidelines
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute

**Disclaimer:**  
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

---

**Built for Kenya's communities 🇰🇪 | Powered by satellite technology 🛰️ | Driven by local knowledge 🌍**
```

---
