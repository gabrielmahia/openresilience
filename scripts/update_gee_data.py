#!/usr/bin/env python3
"""
Background Google Earth Engine Data Updater

Fetches MODIS NDVI vegetation data for all Kenya counties.
Run as cron job every 7 days (MODIS is 16-day composite):
    0 2 */7 * * python scripts/update_gee_data.py

Requires:
- GEE_SERVICE_ACCOUNT (JSON string or file path)
- Or: User authentication (for local development)

Install: pip install earthengine-api
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from openresilience.adapters.earthengine import EarthEngineAdapter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Kenya counties with centroids
KENYA_COUNTIES = {
    "Nairobi": {"lat": -1.286389, "lon": 36.817223},
    "Kiambu": {"lat": -1.171, "lon": 36.835},
    "Nakuru": {"lat": -0.303, "lon": 36.080},
    "Mombasa": {"lat": -4.043, "lon": 39.658},
    "Kisumu": {"lat": -0.091702, "lon": 34.767956},
    "Turkana": {"lat": 3.312, "lon": 35.564},
    "Marsabit": {"lat": 2.334, "lon": 37.988},
    "Mandera": {"lat": 3.563, "lon": 41.167},
    "Wajir": {"lat": 1.747, "lon": 40.057},
    "Garissa": {"lat": -0.463, "lon": 39.662},
    # Add all 47 counties for production
}


def fetch_and_cache_county_vegetation(
    adapter: EarthEngineAdapter,
    county_name: str,
    lat: float,
    lon: float
) -> bool:
    """
    Fetch NDVI data for a county and cache it.
    
    Args:
        adapter: Authenticated Earth Engine adapter
        county_name: County name
        lat, lon: County coordinates
    
    Returns:
        True if successful, False otherwise
    """
    try:
        logger.info(f"Fetching NDVI for {county_name}...")
        
        # Fetch NDVI data
        ndvi_data = adapter.get_ndvi(lat, lon, days=16)
        
        if not ndvi_data:
            logger.error(f"No NDVI data available for {county_name}")
            return False
        
        # Prepare cache data
        cache_data = {
            'county': county_name,
            'lat': lat,
            'lon': lon,
            'timestamp': datetime.now().isoformat(),
            'vegetation_health': ndvi_data['vegetation_health'],
            'ndvi': ndvi_data['ndvi'],
            'quality': ndvi_data['quality'],
            'modis_timestamp': ndvi_data['timestamp'],
            'confidence': ndvi_data['confidence']
        }
        
        # Save to cache
        cache_dir = Path("data/gee_cache")
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        cache_file = cache_dir / f"{county_name.lower().replace(' ', '_')}.json"
        
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)
        
        logger.info(f"Cached NDVI for {county_name}: {ndvi_data['vegetation_health']:.3f}")
        return True
    
    except Exception as e:
        logger.error(f"Failed to fetch data for {county_name}: {e}")
        return False


def main():
    """Main execution: Update Earth Engine data for all counties."""
    logger.info("Starting Earth Engine data update...")
    
    # Initialize adapter
    adapter = EarthEngineAdapter()
    
    if not adapter.is_available():
        logger.error("Earth Engine not available!")
        logger.error("Install: pip install earthengine-api")
        logger.error("Authenticate: Set GEE_SERVICE_ACCOUNT or run ee.Authenticate()")
        sys.exit(1)
    
    logger.info("Earth Engine authentication successful")
    
    # Process each county
    success_count = 0
    for county_name, coords in KENYA_COUNTIES.items():
        if fetch_and_cache_county_vegetation(
            adapter, county_name, coords['lat'], coords['lon']
        ):
            success_count += 1
    
    logger.info(f"Update complete: {success_count}/{len(KENYA_COUNTIES)} counties")
    
    if success_count == 0:
        logger.error("No data collected - check Earth Engine authentication")
        sys.exit(1)


if __name__ == "__main__":
    main()
