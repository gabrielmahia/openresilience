"""
Geographic Hierarchy Management for Kenya

Loads and provides access to county → constituency → ward administrative structure.
Handles incomplete datasets gracefully with fallback behavior.
Supports optional ward centroid data for mapping.
"""

import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class GeoHierarchy:
    """
    Manages Kenya's administrative hierarchy data.
    
    Provides safe access to county → constituency → ward relationships
    with graceful degradation when data is incomplete.
    """
    
    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize hierarchy loader.
        
        Args:
            data_path: Path to ke_admin_hierarchy.json. If None, uses default location.
        """
        if data_path is None:
            # Default to data/admin/ relative to repository root
            data_path = Path(__file__).parent.parent.parent / "data" / "admin" / "ke_admin_hierarchy.json"
        
        self.data_path = Path(data_path)
        self.hierarchy = {}
        self.loaded = False
        self._load()
        
        # Optional ward centroids
        self.centroids_path = self.data_path.parent / "ke_ward_centroids.csv"
        self.ward_centroids = None
        self._load_centroids()
    
    def _load_centroids(self):
        """Load optional ward centroid data."""
        if not self.centroids_path.exists():
            return
        
        try:
            self.ward_centroids = pd.read_csv(self.centroids_path)
        except:
            self.ward_centroids = None
    
    def get_ward_centroid(
        self, 
        county: str, 
        constituency: Optional[str] = None, 
        ward: Optional[str] = None,
        county_fallback: Optional[Tuple[float, float]] = None
    ) -> Optional[Tuple[float, float]]:
        """
        Get centroid coordinates for a ward, with fallback to county centroid.
        
        Args:
            county: County name
            constituency: Constituency name (optional)
            ward: Ward name (optional)
            county_fallback: (lat, lon) tuple to use if ward data unavailable
        
        Returns:
            (latitude, longitude) tuple, or None if not found
        """
        if self.ward_centroids is None:
            return county_fallback
        
        # Try to find ward centroid
        if ward and constituency:
            match = self.ward_centroids[
                (self.ward_centroids['county'] == county) &
                (self.ward_centroids['constituency'] == constituency) &
                (self.ward_centroids['ward'] == ward)
            ]
            
            if not match.empty:
                row = match.iloc[0]
                return (float(row['latitude']), float(row['longitude']))
        
        # Fallback to county centroid
        return county_fallback
    
    def _load(self):
        """Load hierarchy data from JSON file."""
        if not self.data_path.exists():
            # Graceful fallback - no error, just empty hierarchy
            self.loaded = False
            return
        
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.hierarchy = data.get('counties', {})
                self.loaded = True
        except (json.JSONDecodeError, IOError):
            # Silent fallback on malformed data
            self.loaded = False
    
    def is_available(self) -> bool:
        """Check if hierarchy data is loaded and available."""
        return self.loaded and len(self.hierarchy) > 0
    
    def get_counties(self) -> List[str]:
        """
        Get list of counties with hierarchy data.
        
        Returns:
            List of county names, or empty list if data unavailable
        """
        if not self.loaded:
            return []
        return sorted(self.hierarchy.keys())
    
    def get_constituencies(self, county: str) -> List[str]:
        """
        Get constituencies within a county.
        
        Args:
            county: County name
        
        Returns:
            List of constituency names, or empty list if county not found
        """
        if not self.loaded or county not in self.hierarchy:
            return []
        
        constituencies = self.hierarchy[county].get('constituencies', {})
        return sorted(constituencies.keys())
    
    def get_wards(self, county: str, constituency: str) -> List[str]:
        """
        Get wards within a constituency.
        
        Args:
            county: County name
            constituency: Constituency name
        
        Returns:
            List of ward names, or empty list if not found
        """
        if not self.loaded or county not in self.hierarchy:
            return []
        
        constituencies = self.hierarchy[county].get('constituencies', {})
        if constituency not in constituencies:
            return []
        
        wards = constituencies[constituency].get('wards', [])
        return sorted(wards) if isinstance(wards, list) else []
    
    def get_coverage_summary(self) -> Dict[str, int]:
        """
        Get summary of data coverage.
        
        Returns:
            Dictionary with counts: counties, constituencies, wards
        """
        if not self.loaded:
            return {"counties": 0, "constituencies": 0, "wards": 0}
        
        constituency_count = 0
        ward_count = 0
        
        for county_data in self.hierarchy.values():
            constituencies = county_data.get('constituencies', {})
            constituency_count += len(constituencies)
            
            for const_data in constituencies.values():
                wards = const_data.get('wards', [])
                ward_count += len(wards) if isinstance(wards, list) else 0
        
        return {
            "counties": len(self.hierarchy),
            "constituencies": constituency_count,
            "wards": ward_count
        }


def load_hierarchy(data_path: Optional[str] = None) -> GeoHierarchy:
    """
    Convenience function to load geographic hierarchy.
    
    Args:
        data_path: Optional custom path to hierarchy JSON
    
    Returns:
        GeoHierarchy instance (may be empty if data unavailable)
    """
    return GeoHierarchy(data_path)


# Export main classes and functions
__all__ = ["GeoHierarchy", "load_hierarchy"]
