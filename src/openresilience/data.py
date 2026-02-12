"""Data loading and forecast generation — pure logic, no Streamlit dependency."""

import numpy as np
import pandas as pd
from datetime import datetime

from .constants import KENYA_COUNTIES


def load_county_data():
    """Generate water stress data for all 47 counties.

    Returns a pandas DataFrame with columns: County, Lat, Lon, Population,
    ASAL, Current_Stress, Severity.
    """
    np.random.seed(42)

    county_list = []
    for county, info in KENYA_COUNTIES.items():
        if info["arid"]:
            base_stress = np.random.uniform(0.65, 0.95)
        else:
            base_stress = np.random.uniform(0.25, 0.60)

        month = datetime.now().month
        if 3 <= month <= 5 or 10 <= month <= 12:
            stress = max(0.1, base_stress - 0.15)
        else:
            stress = min(0.98, base_stress + 0.10)

        county_list.append(
            {
                "County": county,
                "Lat": info["lat"],
                "Lon": info["lon"],
                "Population": info["pop"],
                "ASAL": "Yes" if info["arid"] else "No",
                "Current_Stress": stress,
                "Severity": 3 if stress > 0.80 else 2 if stress > 0.60 else 1 if stress > 0.40 else 0,
            }
        )

    return pd.DataFrame(county_list)


def generate_forecast(county_name, current_stress, is_asal):
    """Generate actionable short, mid, long-term forecast.

    Returns a dict with keys: short, medium, long, trend, trend_emoji,
    season_note, confidence.
    """
    month = datetime.now().month

    if 3 <= month <= 5:
        short_trend = -0.08
        season_note = "Long rains season approaching"
    elif 6 <= month <= 9:
        short_trend = 0.06
        season_note = "Dry season - stress increasing"
    elif 10 <= month <= 12:
        short_trend = -0.05
        season_note = "Short rains season active"
    else:
        short_trend = 0.08
        season_note = "Peak dry season"

    if is_asal:
        short_trend *= 1.5

    short = np.clip(current_stress + short_trend + np.random.uniform(-0.03, 0.03), 0, 1)
    medium = np.clip(current_stress + short_trend * 2 + np.random.uniform(-0.08, 0.08), 0, 1)
    long_val = np.clip(current_stress + short_trend * 3 + np.random.uniform(-0.12, 0.12), 0, 1)

    if short < current_stress - 0.05:
        trend = "improving"
        trend_emoji = "📈 ✅"
    elif short > current_stress + 0.05:
        trend = "worsening"
        trend_emoji = "📉 ⚠️"
    else:
        trend = "stable"
        trend_emoji = "➡️"

    return {
        "short": short,
        "medium": medium,
        "long": long_val,
        "trend": trend,
        "trend_emoji": trend_emoji,
        "season_note": season_note,
        "confidence": "Simulated (demo data)" if not is_asal else "Simulated (demo data)",
    }
