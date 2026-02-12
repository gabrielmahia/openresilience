import numpy as np
from or_shared.scoring import sev_from_thresholds, composite_max

def rain_anomaly(obs, typ, eps=1e-6):
    return (obs - typ) / np.maximum(typ, eps)

def compute_scores(obs_rain, typ_rain, soil_pct, ndvi_anom, persistence_weeks):
    anom = rain_anomaly(obs_rain, typ_rain)
    dryness = np.clip(-anom, 0, 2)
    rain_sev = sev_from_thresholds(dryness, 0.15, 0.30, 0.50, True)
    soil_sev = sev_from_thresholds(soil_pct, 0.30, 0.20, 0.10, False)
    veg_sev  = sev_from_thresholds(np.clip(-ndvi_anom,0,2), 0.10, 0.20, 0.30, True)
    pers_sev = sev_from_thresholds(persistence_weeks.astype(float), 2, 4, 6, True)
    wsi = composite_max(rain_sev, soil_sev, pers_sev)
    fsi = composite_max(veg_sev, pers_sev, rain_sev)
    msi = np.zeros_like(wsi)
    cri = composite_max(wsi, fsi, msi)
    return anom, soil_pct, ndvi_anom, persistence_weeks, wsi, fsi, msi, cri
