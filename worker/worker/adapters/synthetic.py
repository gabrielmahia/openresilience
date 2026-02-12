import numpy as np
def load_synthetic(shape=(120, 240), seed=7):
    rng = np.random.default_rng(seed)
    lat = np.linspace(90, -90, shape[0])[:, None]
    typical_rain = 30 * np.exp(-(lat/35)**2) + 5
    typical_rain = typical_rain + rng.normal(0, 1.0, size=shape)
    typical_rain = np.clip(typical_rain, 1, None)
    observed_rain = typical_rain * (0.7 + 0.6 * rng.random(shape))
    for _ in range(8):
        r0 = rng.integers(10, shape[0]-10)
        c0 = rng.integers(10, shape[1]-10)
        observed_rain[r0-6:r0+6, c0-12:c0+12] *= rng.uniform(0.05, 0.30)
    soil_pct = rng.random(shape)
    ndvi_anom = rng.normal(0, 0.15, size=shape)
    persistence = rng.integers(0, 9, size=shape)
    return observed_rain, typical_rain, soil_pct, ndvi_anom, persistence
