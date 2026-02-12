#!/usr/bin/env python3
"""
Background NASA Data Updater

Fetches satellite data for all Kenya counties and caches locally.
Run as cron job every 6 hours:
    0 */6 * * * python scripts/update_nasa_data.py

Requires:
- NASA_EARTHDATA_USERNAME
- NASA_EARTHDATA_PASSWORD
Set in environment or .env file.
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from openresilience.adapters.appeears import NASAAppEEARSClient

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
    # Add all 47 counties here for production
}


def calculate_rainfall_anomaly(rainfall_data: list) -> float:
    """
    Calculate rainfall anomaly from time series.
    
    Args:
        rainfall_data: List of daily rainfall values (mm)
    
    Returns:
        Anomaly as percentage (-100 to +100)
    """
    if not rainfall_data:
        return 0.0
    
    # Calculate 30-day total
    total_rainfall = sum(rainfall_data)
    
    # Kenya climatology: ~50mm/month average (varies by region)
    # This should be region-specific in production
    expected_rainfall = 50.0
    
    # Calculate anomaly
    anomaly = ((total_rainfall - expected_rainfall) / expected_rainfall) * 100
    
    # Clamp to reasonable range
    return max(-100, min(100, anomaly))


def calculate_soil_moisture_average(soil_data: list) -> float:
    """
    Calculate average soil moisture from time series.
    
    Args:
        soil_data: List of soil moisture values (0-1)
    
    Returns:
        Average soil moisture (0-1)
    """
    if not soil_data:
        return 0.5
    
    # Filter out invalid values
    valid_data = [v for v in soil_data if 0 <= v <= 1]
    
    if not valid_data:
        return 0.5
    
    return sum(valid_data) / len(valid_data)


def fetch_and_cache_county_data(
    client: NASAAppEEARSClient,
    county_name: str,
    lat: float,
    lon: float
) -> bool:
    """
    Fetch NASA data for a county and cache it.
    
    Args:
        client: Authenticated NASA client
        county_name: County name
        lat, lon: County coordinates
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Date range: last 30 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')
        
        # Products to request
        products = [
            'GPM_3IMERGDL_06_precipitation',  # IMERG Daily
            'SPL3SMP_E_005_soil_moisture'      # SMAP Enhanced
        ]
        
        logger.info(f"Submitting request for {county_name}...")
        
        # Submit request
        task_id = client.submit_point_request(
            lat, lon, start_str, end_str, products
        )
        
        if not task_id:
            logger.error(f"Failed to submit request for {county_name}")
            return False
        
        logger.info(f"Task submitted: {task_id}")
        
        # NOTE: AppEEARS is asynchronous
        # Task takes 5-30 minutes to complete
        # For production: Store task_id, check status later, download when ready
        
        # For immediate deployment: Use demo data while tasks process
        # Placeholder cache entry
        cache_data = {
            'county': county_name,
            'lat': lat,
            'lon': lon,
            'timestamp': datetime.now().isoformat(),
            'task_id': task_id,
            'status': 'pending',
            'rainfall_anomaly': None,  # Will be populated when task completes
            'soil_moisture': None,
            'note': 'Real NASA data processing - using demo until ready'
        }
        
        # Save to cache
        cache_dir = Path("data/nasa_cache")
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        cache_file = cache_dir / f"{county_name.lower().replace(' ', '_')}.json"
        
        with open(cache_file, 'w') as f:
            json.dump(cache_data, f, indent=2)
        
        logger.info(f"Cached placeholder for {county_name}")
        return True
    
    except Exception as e:
        logger.error(f"Failed to fetch data for {county_name}: {e}")
        return False


def main():
    """Main execution: Update NASA data for all counties."""
    logger.info("Starting NASA data update...")
    
    # Initialize client
    client = NASAAppEEARSClient()
    
    if not client.is_available():
        logger.error("NASA credentials not configured!")
        logger.error("Set NASA_EARTHDATA_USERNAME and NASA_EARTHDATA_PASSWORD")
        sys.exit(1)
    
    # Authenticate
    if not client.authenticate():
        logger.error("NASA authentication failed!")
        sys.exit(1)
    
    logger.info("NASA authentication successful")
    
    # Process each county
    success_count = 0
    for county_name, coords in KENYA_COUNTIES.items():
        if fetch_and_cache_county_data(
            client, county_name, coords['lat'], coords['lon']
        ):
            success_count += 1
    
    logger.info(f"Update complete: {success_count}/{len(KENYA_COUNTIES)} counties")
    
    # Note: This is Phase 1 - submits requests
    # Phase 2: Run separate script to check task status and download results
    # Phase 3: Parse downloaded data and update cache with actual values


if __name__ == "__main__":
    main()
