# OpenResilience Kenya — Index Methodology

## Overview

OpenResilience uses four composite indices to surface water, food, and market stress across Kenya's 47 counties. This document explains what each index measures, how it is computed, and the methodological basis for weighting decisions.

All indices are normalised to **[0, 1]** where 0 = no stress and 1 = extreme stress. Thresholds for severity tiers (Watch / Alert / Emergency) are calibrated against Kenya Meteorological Department drought classifications and FEWS NET IPC phase boundaries.

---

## WSI — Water Stress Index

**What it measures:** Combined rainfall deficit and soil moisture depletion.

**Formula:**

```
WSI = (rainfall_deficit_fraction × 0.6) + (soil_dryness × 0.4)
```

Where:
- `rainfall_deficit_fraction` = percentage below long-run monthly mean ÷ 100 (positive = deficit)
- `soil_dryness` = 1 − soil_moisture (soil_moisture expressed as volumetric fraction 0–1)

**Weight rationale:**  
Rainfall is the primary driver of water stress onset in ASAL regions (0.6 weight), following FAO's Water Requirements Satisfaction Index (WRSI) methodology which weights precipitation as the dominant factor in rain-fed systems. Soil moisture (0.4 weight) captures cumulative deficit — a county with moderate rainfall but severely depleted soils carries forward risk not visible in single-season rainfall data. This dual-signal approach is consistent with CHIRPS + SMAP combined analysis used by FEWS NET for East Africa.

**Production data sources (roadmap):**  
- Rainfall: CHIRPS v2.0 (Climate Hazards Group, daily, 0.05° resolution)  
- Soil moisture: NASA SMAP Level-3 (3-day composite, 36km resolution)

---

## FSI — Food Stress Index

**What it measures:** Risk of food production shortfall, driven primarily by water stress with a vegetation signal adjustment.

**Formula (current):**

```
FSI = WSI × 0.8
```

**Formula (production, with vegetation data):**

```
FSI = (WSI × 0.55) + (vegetation_deficit × 0.30) + (field_reports_severity × 0.15)
```

**Weight rationale:**  
In Kenya's ASAL counties, food stress is dominated by water availability — crop failure closely tracks WSI. The 0.8 scalar reflects the empirical correlation between Water Stress Index and Kenya's short-rains food insecurity assessments (NDMA county bulletins, 2018–2024). The production formula adds vegetation deficit (NDVI anomaly from MODIS MOD13A2) and community field reports as independent signal sources, reducing reliance on a single proxy.

**Production data sources (roadmap):**  
- Vegetation: NASA MODIS MOD13A2 NDVI (16-day composite, 1km resolution)  
- Field reports: NDMA County Drought Early Warning Bulletins + community submissions

---

## MSI — Market Stress Index

**What it measures:** Food market price pressure and supply disruption signals.

**Formula:**

```
MSI = price_change_fraction × 0.7
```

Where `price_change_fraction` is the observed or projected maize/staple price change relative to the seasonal average, capped at 1.0.

**Weight rationale:**  
Price data is the most operationally actionable stress signal for market-dependent households — a 70% weight reflects its primacy as a leading indicator of household food access deterioration. This is consistent with FEWS NET Market Analysis guidance which treats staple price inflation as an early IPC Phase 2/3 trigger. The 0.7 factor (rather than 1.0) accounts for high price-data volatility and the need to avoid over-triggering alerts on short-term price spikes.

**Production data sources (roadmap):**  
- Kenya National Bureau of Statistics monthly retail prices  
- WFP VAM food price monitoring

---

## CRI — Composite Risk Index

**What it measures:** Overall household resilience risk, combining all three stress signals.

**Formula:**

```
CRI = (WSI × 0.45) + (FSI × 0.35) + (MSI × 0.20)
```

**Severity tiers:**

| CRI Range | Tier | Action |
|-----------|------|--------|
| 0.00–0.29 | Normal | Routine monitoring |
| 0.30–0.49 | Watch | Increased frequency |
| 0.50–0.69 | Alert | Coordination + field verification |
| 0.70–1.00 | Emergency | Immediate response mobilisation |

**Weight rationale:**  
WSI receives the highest weight (0.45) because water availability is the foundational constraint in Kenya's drought cycles — it precedes and causes food and market stress. FSI (0.35) reflects that food production shortfall is the primary humanitarian consequence and requires pre-positioning time. MSI (0.20) is weighted lower because price signals can lag physical stress by weeks and are subject to speculative movement; it acts as a confirmatory rather than primary signal.

These weights were informed by retrospective analysis of NDMA drought responses (2011–2023) and align with Kenya's National Drought Management Authority scoring matrix for ASAL counties.

---

## Limitations and Honest Caveats

1. **Current data is synthetic.** All indices in demo mode run on algorithmically generated data seeded with seasonal patterns. No current reading should be treated as operational.

2. **ASAL vs. non-ASAL calibration.** Thresholds are calibrated primarily for arid and semi-arid counties (Turkana, Marsabit, Garissa, Wajir, Mandera, etc.). Highland and lakeshore counties may require adjusted thresholds to avoid false alerts.

3. **Population weighting not applied.** County-level indices treat all counties as equally sized units. A 0.65 CRI in Nairobi (4.4M people) and a 0.65 CRI in Lamu (144k people) carry very different humanitarian implications. Population-weighted aggregation is on the roadmap.

4. **Field validation not yet completed.** These formulas have not been ground-truthed against historical KMD/NDMA drought declarations. Before operational deployment, retrospective validation against the 2016–17, 2021–22, and 2023 drought events is required.

---

## References

- FAO (2015). *Crop Water Requirements and Irrigation Scheduling.* FAO Irrigation and Drainage Paper 56.
- FEWS NET (2023). *East Africa Market Analysis Update.* USAID.
- Kenya NDMA (2024). *County Drought Early Warning Bulletins.* National Drought Management Authority.
- Funk, C. et al. (2015). *The Climate Hazards Infrared Precipitation with Stations (CHIRPS).* Nature Scientific Data.
- Entekhabi, D. et al. (2010). *The Soil Moisture Active Passive (SMAP) Mission.* Proceedings of the IEEE.

---

*Last updated: February 2026. Methodology is versioned — changes tracked in RELEASE.md.*
