"""
Google Earth Engine Adapter for OpenResilience

Integrates MODIS vegetation indices:
- MOD13Q1: 250m resolution, 16-day NDVI composite
- MYD13Q1: Aqua satellite backup

Requires Google Earth Engine account (free for noncommercial use).
Sign up: https://earthengine.google.com/signup/
"""

import os
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# Earth Engine imports (optional - graceful fallback if unavailable)
try:
    import ee
    EE_AVAILABLE = True
except ImportError:
    EE_AVAILABLE = False
    logger.warning("Earth Engine not available (pip install earthengine-api)")


class EarthEngineAdapter:
    """
    Adapter for Google Earth Engine.
    
    Handles authentication, data extraction, and error recovery.
    """
    
    def __init__(self, service_account_key: Optional[str] = None):
        """
        Initialize Earth Engine adapter.
        
        Args:
            service_account_key: Path to service account JSON or JSON string
        """
        self.authenticated = False
        self.service_account_key = service_account_key or os.getenv('GEE_SERVICE_ACCOUNT')
        
        if EE_AVAILABLE:
            self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Earth Engine."""
        try:
            # Try service account authentication first
            if self.service_account_key:
                if os.path.isfile(self.service_account_key):
                    # File path
                    credentials = ee.ServiceAccountCredentials(
                        None, 
                        self.service_account_key
                    )
                    ee.Initialize(credentials)
                else:
                    # JSON string (from Streamlit secrets)
                    credentials_dict = json.loads(self.service_account_key)
                    credentials = ee.ServiceAccountCredentials(
                        credentials_dict['client_email'],
                        key_data=self.service_account_key
                    )
                    ee.Initialize(credentials)
                
                self.authenticated = True
                logger.info("Earth Engine authenticated (service account)")
            else:
                # Try user authentication (for local development)
                try:
                    ee.Initialize()
                    self.authenticated = True
                    logger.info("Earth Engine authenticated (user credentials)")
                except Exception:
                    # Attempt to authenticate
                    ee.Authenticate()
                    ee.Initialize()
                    self.authenticated = True
                    logger.info("Earth Engine authenticated (new user)")
        
        except Exception as e:
            logger.error(f"Earth Engine authentication failed: {e}")
            self.authenticated = False
    
    def is_available(self) -> bool:
        """Check if Earth Engine is available and authenticated."""
        return EE_AVAILABLE and self.authenticated
    
    def get_ndvi(
        self,
        lat: float,
        lon: float,
        days: int = 16
    ) -> Optional[Dict[str, Any]]:
        """
        Get NDVI (vegetation health) from MODIS.
        
        Args:
            lat: Latitude (decimal degrees)
            lon: Longitude (decimal degrees)
            days: Number of days to average (default 16 for one MODIS cycle)
        
        Returns:
            Dict with:
            - ndvi: Normalized Difference Vegetation Index (-1 to 1)
            - ndvi_scaled: Scaled to 0-1 for vegetation health
            - evi: Enhanced Vegetation Index (optional)
            - quality: Data quality flag
            Or None if fetch fails
        """
        if not self.is_available():
            return None
        
        try:
            # Create point geometry
            point = ee.Geometry.Point([lon, lat])
            
            # Date range (last 16 days by default)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # MODIS Terra 16-day NDVI (250m resolution)
            # MOD13Q1.061 - Collection 6.1
            collection = ee.ImageCollection('MODIS/061/MOD13Q1') \
                .filterDate(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')) \
                .filterBounds(point)
            
            # Get most recent image
            if collection.size().getInfo() == 0:
                logger.warning(f"No MODIS data available for {lat}, {lon}")
                return None
            
            # Use most recent composite
            image = collection.sort('system:time_start', False).first()
            
            # Extract NDVI at point (scale: 0.0001, range: -2000 to 10000)
            ndvi_raw = image.select('NDVI').reduceRegion(
                reducer=ee.Reducer.first(),
                geometry=point,
                scale=250  # 250m resolution
            ).getInfo()
            
            if 'NDVI' not in ndvi_raw:
                return None
            
            # Scale NDVI: raw / 10000 to get -0.2 to 1.0 range
            ndvi = ndvi_raw['NDVI'] / 10000.0
            
            # Scale to 0-1 for vegetation health (assuming -0.2 is bare soil, 0.8+ is healthy)
            # Clamp to reasonable range
            ndvi_health = max(0.0, min(1.0, (ndvi + 0.2) / 1.0))
            
            # Get quality flag
            quality_raw = image.select('SummaryQA').reduceRegion(
                reducer=ee.Reducer.first(),
                geometry=point,
                scale=250
            ).getInfo()
            
            quality = quality_raw.get('SummaryQA', -1)
            
            # Get timestamp
            timestamp = datetime.fromtimestamp(
                image.get('system:time_start').getInfo() / 1000
            )
            
            logger.info(f"MODIS NDVI for {lat}, {lon}: {ndvi:.3f} (health: {ndvi_health:.3f})")
            
            return {
                'ndvi': ndvi,
                'vegetation_health': ndvi_health,
                'quality': quality,
                'timestamp': timestamp.isoformat(),
                'confidence': 90 if quality == 0 else 70  # Quality 0 = good
            }
        
        except Exception as e:
            logger.error(f"Failed to fetch MODIS NDVI: {e}")
            return None
    
    def get_ndvi_bulk(
        self,
        locations: list,
        days: int = 16
    ) -> Dict[str, Optional[Dict[str, Any]]]:
        """
        Get NDVI for multiple locations efficiently.
        
        Args:
            locations: List of (county_name, lat, lon) tuples
            days: Number of days to average
        
        Returns:
            Dict mapping county_name to NDVI data
        """
        if not self.is_available():
            return {name: None for name, _, _ in locations}
        
        results = {}
        
        for county_name, lat, lon in locations:
            try:
                results[county_name] = self.get_ndvi(lat, lon, days)
            except Exception as e:
                logger.error(f"Failed to get NDVI for {county_name}: {e}")
                results[county_name] = None
        
        return results


def get_cached_vegetation_data(county_name: str) -> Optional[Dict[str, Any]]:
    """
    Read vegetation data from local cache.
    
    Cache is populated by background job or manual script.
    
    Args:
        county_name: Kenya county name
    
    Returns:
        Dict with vegetation_health (0-1), or None
    """
    try:
        cache_dir = Path("data/gee_cache")
        cache_file = cache_dir / f"{county_name.lower().replace(' ', '_')}.json"
        
        if not cache_file.exists():
            return None
        
        # Check if cache is recent (< 7 days old for MODIS 16-day product)
        file_age = datetime.now() - datetime.fromtimestamp(cache_file.stat().st_mtime)
        if file_age > timedelta(days=7):
            logger.warning(f"GEE cache for {county_name} is stale ({file_age.days} days old)")
            return None
        
        with open(cache_file, 'r') as f:
            data = json.load(f)
        
        logger.info(f"Using cached GEE data for {county_name}")
        return data
    
    except Exception as e:
        logger.error(f"Failed to read GEE cache: {e}")
        return None


def get_vegetation_health(
    county_name: str,
    lat: float,
    lon: float
) -> Optional[float]:
    """
    Get vegetation health for a county.
    
    Strategy:
    1. Check local cache first (fast, reliable)
    2. If cache miss, return None to use demo data
    3. Background job updates cache every 7 days
    
    Args:
        county_name: Kenya county name
        lat, lon: County centroid coordinates
    
    Returns:
        Vegetation health (0-1) or None
    """
    cached = get_cached_vegetation_data(county_name)
    
    if cached:
        return cached.get('vegetation_health')
    
    # No cached data - return None to use demo data
    return None


# Export public interface
__all__ = [
    'EarthEngineAdapter',
    'get_cached_vegetation_data',
    'get_vegetation_health',
]
