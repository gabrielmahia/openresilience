#!/usr/bin/env python3
"""
Automated Satellite-Style Data Generator

Generates realistic, dynamic data that simulates satellite patterns.
Updates automatically every 6 hours via GitHub Actions.

This provides immediate functionality while real APIs are being debugged.
Data patterns are based on:
- Kenya climate zones
- Seasonal rainfall patterns
- Regional vegetation cycles
- ASAL vs non-ASAL characteristics
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime, timedelta
import random
import math

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Kenya counties with characteristics
KENYA_COUNTIES = {
    "Nairobi": {"lat": -1.286389, "lon": 36.817223, "arid": False, "altitude": 1795},
    "Kiambu": {"lat": -1.171, "lon": 36.835, "arid": False, "altitude": 1800},
    "Nakuru": {"lat": -0.303, "lon": 36.080, "arid": False, "altitude": 1850},
    "Mombasa": {"lat": -4.043, "lon": 39.658, "arid": False, "altitude": 17},
    "Kisumu": {"lat": -0.091702, "lon": 34.767956, "arid": False, "altitude": 1131},
    "Turkana": {"lat": 3.312, "lon": 35.564, "arid": True, "altitude": 400},
    "Marsabit": {"lat": 2.334, "lon": 37.988, "arid": True, "altitude": 1345},
    "Mandera": {"lat": 3.563, "lon": 41.167, "arid": True, "altitude": 231},
    "Wajir": {"lat": 1.747, "lon": 40.057, "arid": True, "altitude": 244},
    "Garissa": {"lat": -0.463, "lon": 39.662, "arid": True, "altitude": 147},
}


def get_seasonal_factor(month: int) -> dict:
    """
    Get seasonal factors for Kenya climate.
    
    Kenya has two rainy seasons:
    - Long rains: March-May
    - Short rains: October-December
    
    Returns dict with rainfall, vegetation, and drought factors.
    """
    # Long rains (March-May)
    if 3 <= month <= 5:
        return {
            'rainfall_bonus': 30,
            'vegetation_bonus': 0.20,
            'drought_factor': 0.5
        }
    # Short rains (October-December)
    elif 10 <= month <= 12:
        return {
            'rainfall_bonus': 20,
            'vegetation_bonus': 0.15,
            'drought_factor': 0.7
        }
    # Dry season (Jan-Feb, June-Sept)
    else:
        return {
            'rainfall_bonus': -15,
            'vegetation_bonus': -0.10,
            'drought_factor': 1.3
        }


def generate_rainfall_anomaly(county_info: dict, seasonal: dict) -> float:
    """
    Generate realistic rainfall anomaly (% from normal).
    
    Based on:
    - ASAL vs non-ASAL
    - Seasonal patterns
    - Random variation (simulates weather variability)
    """
    base = -40 if county_info['arid'] else -10
    variation = random.uniform(-20, 20)
    seasonal_adj = seasonal['rainfall_bonus']
    
    # Add some persistence (25% correlation with "previous" value)
    seed = hash(county_info['lat'] + county_info['lon']) % 100
    trend = (seed - 50) * 0.3
    
    anomaly = base + variation + seasonal_adj + trend
    return max(-80, min(50, anomaly))  # Clamp to reasonable range


def generate_soil_moisture(rainfall_anomaly: float, county_info: dict, seasonal: dict) -> float:
    """
    Generate soil moisture (0-1 scale).
    
    Correlated with rainfall but with lag and regional differences.
    """
    # Base moisture from rainfall (with lag effect)
    rainfall_effect = (rainfall_anomaly + 50) / 100  # Convert -50 to +50 -> 0 to 1
    
    # ASAL areas have lower moisture retention
    retention = 0.6 if county_info['arid'] else 0.85
    
    # Coastal areas (Mombasa) have different patterns
    coastal_bonus = 0.10 if county_info['altitude'] < 100 else 0.0
    
    moisture = rainfall_effect * retention + coastal_bonus
    moisture += random.uniform(-0.05, 0.05)  # Small random variation
    
    return max(0.0, min(1.0, moisture))


def generate_vegetation_health(soil_moisture: float, county_info: dict, seasonal: dict) -> float:
    """
    Generate vegetation health / NDVI (0-1 scale).
    
    Correlated with soil moisture but with seasonal vegetation cycles.
    """
    # Base health from soil moisture
    base_health = soil_moisture * 0.8
    
    # Seasonal vegetation factor
    base_health += seasonal['vegetation_bonus']
    
    # ASAL areas have sparse vegetation even when conditions are good
    if county_info['arid']:
        base_health *= 0.7
    
    # Add altitude effect (higher = more vegetation in Kenya highlands)
    if county_info['altitude'] > 1500:
        base_health += 0.10
    
    # Random variation
    base_health += random.uniform(-0.08, 0.08)
    
    return max(0.0, min(1.0, base_health))


def generate_all_counties_data():
    """Generate data for all counties and save to cache."""
    logger.info("Starting automated data generation...")
    
    now = datetime.now()
    month = now.month
    seasonal = get_seasonal_factor(month)
    
    logger.info(f"Current month: {month}, Season: {seasonal}")
    
    # Create cache directories
    nasa_cache_dir = Path("data/nasa_cache")
    gee_cache_dir = Path("data/gee_cache")
    nasa_cache_dir.mkdir(parents=True, exist_ok=True)
    gee_cache_dir.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    
    for county_name, county_info in KENYA_COUNTIES.items():
        try:
            logger.info(f"Generating data for {county_name}...")
            
            # Generate correlated data
            rainfall_anom = generate_rainfall_anomaly(county_info, seasonal)
            soil_moisture = generate_soil_moisture(rainfall_anom, county_info, seasonal)
            vegetation = generate_vegetation_health(soil_moisture, county_info, seasonal)
            
            # NASA cache (rainfall + soil moisture)
            nasa_data = {
                'county': county_name,
                'lat': county_info['lat'],
                'lon': county_info['lon'],
                'timestamp': now.isoformat(),
                'rainfall_anomaly': round(rainfall_anom, 2),
                'soil_moisture': round(soil_moisture, 3),
                'data_source': 'simulated_realistic',
                'note': 'Realistic simulation based on Kenya climate patterns'
            }
            
            nasa_file = nasa_cache_dir / f"{county_name.lower().replace(' ', '_')}.json"
            with open(nasa_file, 'w') as f:
                json.dump(nasa_data, f, indent=2)
            
            # Earth Engine cache (vegetation)
            gee_data = {
                'county': county_name,
                'lat': county_info['lat'],
                'lon': county_info['lon'],
                'timestamp': now.isoformat(),
                'vegetation_health': round(vegetation, 3),
                'ndvi': round((vegetation * 0.8) - 0.1, 3),  # Convert to NDVI scale
                'quality': 0 if vegetation > 0.3 else 1,
                'confidence': 85,
                'data_source': 'simulated_realistic',
                'note': 'Realistic NDVI simulation based on regional patterns'
            }
            
            gee_file = gee_cache_dir / f"{county_name.lower().replace(' ', '_')}.json"
            with open(gee_file, 'w') as f:
                json.dump(gee_data, f, indent=2)
            
            logger.info(f"  ✓ {county_name}: rainfall={rainfall_anom:.1f}%, soil={soil_moisture:.2f}, veg={vegetation:.2f}")
            success_count += 1
            
        except Exception as e:
            logger.error(f"Failed to generate data for {county_name}: {e}")
    
    logger.info(f"\n{'='*60}")
    logger.info(f"Data generation complete: {success_count}/{len(KENYA_COUNTIES)} counties")
    logger.info(f"NASA cache: {nasa_cache_dir}")
    logger.info(f"GEE cache: {gee_cache_dir}")
    logger.info(f"{'='*60}\n")
    
    if success_count == 0:
        logger.error("No data generated - check errors above")
        sys.exit(1)


if __name__ == "__main__":
    generate_all_counties_data()
