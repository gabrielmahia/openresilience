"""
Practical NASA Data Integration

Uses NASA AppEEARS API for reliable, cached satellite data access.
Simpler than OpenDAP, works with standard HTTP requests.

Setup:
1. Get NASA Earthdata account: https://urs.earthdata.nasa.gov/
2. Set NASA_EARTHDATA_USERNAME and NASA_EARTHDATA_PASSWORD in secrets
3. Data updates every 6 hours via background job (optional)

For immediate deployment, includes fallback to demo data.
"""

import os
import requests
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class NASAAppEEARSClient:
    """
    Client for NASA AppEEARS API.
    
    AppEEARS (Application for Extracting and Exploring Analysis Ready Samples)
    is a simpler alternative to OpenDAP for point-based extractions.
    
    API Docs: https://appeears.earthdatacloud.nasa.gov/api/
    """
    
    BASE_URL = "https://appeears.earthdatacloud.nasa.gov/api"
    
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        self.username = username or os.getenv('NASA_EARTHDATA_USERNAME')
        self.password = password or os.getenv('NASA_EARTHDATA_PASSWORD')
        self.token = None
        self.session = requests.Session()
    
    def authenticate(self) -> bool:
        """Get authentication token."""
        if not self.username or not self.password:
            return False
        
        try:
            response = self.session.post(
                f"{self.BASE_URL}/login",
                auth=(self.username, self.password),
                timeout=10
            )
            
            if response.status_code == 200:
                self.token = response.json().get('token')
                self.session.headers.update({'Authorization': f'Bearer {self.token}'})
                return True
            
            return False
        
        except Exception as e:
            logger.error(f"NASA authentication failed: {e}")
            return False
    
    def is_available(self) -> bool:
        """Check if credentials are configured."""
        return bool(self.username and self.password)
    
    def submit_point_request(
        self,
        lat: float,
        lon: float,
        start_date: str,
        end_date: str,
        products: list
    ) -> Optional[str]:
        """
        Submit a point extraction request.
        
        Args:
            lat, lon: Coordinates
            start_date, end_date: Format 'YYYY-MM-DD'
            products: List of product layers (e.g., ['GPM_3IMERGDL_06_precipitation'])
        
        Returns:
            Task ID or None
        """
        if not self.token:
            if not self.authenticate():
                return None
        
        try:
            task_data = {
                'task_type': 'point',
                'task_name': f'OpenResilience_{lat}_{lon}_{datetime.now().strftime("%Y%m%d")}',
                'params': {
                    'dates': [{'startDate': start_date, 'endDate': end_date}],
                    'layers': [{'product': p} for p in products],
                    'coordinates': [{'latitude': lat, 'longitude': lon, 'id': 'point1'}]
                }
            }
            
            response = self.session.post(
                f"{self.BASE_URL}/task",
                json=task_data,
                timeout=30
            )
            
            if response.status_code == 202:
                return response.json().get('task_id')
            
            logger.warning(f"Point request failed: {response.status_code}")
            return None
        
        except Exception as e:
            logger.error(f"Failed to submit point request: {e}")
            return None


def get_cached_nasa_data(county_name: str) -> Optional[Dict[str, Any]]:
    """
    Read NASA data from local cache.
    
    Cache is populated by background job or manual script.
    Falls back to None if cache doesn't exist.
    
    Args:
        county_name: Kenya county name
    
    Returns:
        Dict with rainfall_anomaly, soil_moisture, etc., or None
    """
    try:
        cache_dir = Path("data/nasa_cache")
        cache_file = cache_dir / f"{county_name.lower().replace(' ', '_')}.json"
        
        if not cache_file.exists():
            return None
        
        # Check if cache is recent (< 24 hours old)
        file_age = datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)
        if file_age > timedelta(hours=24):
            logger.warning(f"NASA cache for {county_name} is stale ({file_age.days} days old)")
            return None
        
        with open(cache_file, 'r') as f:
            data = json.load(f)
        
        logger.info(f"Using cached NASA data for {county_name}")
        return data
    
    except Exception as e:
        logger.error(f"Failed to read NASA cache: {e}")
        return None


def get_nasa_data_for_county(
    county_name: str,
    lat: float,
    lon: float
) -> Tuple[Optional[float], Optional[float]]:
    """
    Get NASA satellite data for a county.
    
    Strategy:
    1. Check local cache first (fast, reliable)
    2. If cache miss, return None to use demo data
    3. Background job updates cache every 6 hours
    
    Args:
        county_name: Kenya county name
        lat, lon: County centroid coordinates
    
    Returns:
        (rainfall_anomaly, soil_moisture) or (None, None)
    """
    cached = get_cached_nasa_data(county_name)
    
    if cached:
        return (
            cached.get('rainfall_anomaly'),
            cached.get('soil_moisture')
        )
    
    # No cached data - return None to use demo data
    # Production: Background service ensures cache is always populated
    return None, None


# Export public interface
__all__ = [
    'NASAAppEEARSClient',
    'get_cached_nasa_data',
    'get_nasa_data_for_county',
]
