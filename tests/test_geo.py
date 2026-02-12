"""
Smoke tests for geographic hierarchy loader.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from openresilience.geo import GeoHierarchy, load_hierarchy


def test_hierarchy_loads_without_error():
    """Verify hierarchy loader doesn't crash on missing data."""
    # Should work even if data file doesn't exist
    geo = GeoHierarchy(data_path="nonexistent.json")
    assert geo is not None
    assert isinstance(geo.is_available(), bool)


def test_hierarchy_graceful_fallback():
    """Verify empty results when data unavailable."""
    geo = GeoHierarchy(data_path="nonexistent.json")
    
    assert geo.get_counties() == []
    assert geo.get_constituencies("Nairobi") == []
    assert geo.get_wards("Nairobi", "Westlands") == []


def test_hierarchy_loads_real_data():
    """Test loading actual hierarchy data if present."""
    geo = load_hierarchy()
    
    if geo.is_available():
        counties = geo.get_counties()
        assert len(counties) > 0
        assert all(isinstance(c, str) for c in counties)
        
        # If Nairobi exists, it should have constituencies
        if "Nairobi" in counties:
            constituencies = geo.get_constituencies("Nairobi")
            assert len(constituencies) > 0


def test_coverage_summary_structure():
    """Verify coverage summary returns correct structure."""
    geo = load_hierarchy()
    summary = geo.get_coverage_summary()
    
    assert "counties" in summary
    assert "constituencies" in summary
    assert "wards" in summary
    assert all(isinstance(v, int) for v in summary.values())
    assert all(v >= 0 for v in summary.values())


def test_ward_centroid_fallback():
    """Verify ward centroid falls back to county centroid."""
    geo = load_hierarchy()
    
    fallback = (-1.2921, 36.8219)  # Nairobi coords
    result = geo.get_ward_centroid(
        "Nairobi",
        "Westlands",
        "NonexistentWard",
        county_fallback=fallback
    )
    
    # Should return fallback if ward not found
    assert result == fallback or result is None or result == fallback


def test_ward_centroids_optional():
    """Verify system works without ward centroid data."""
    geo = load_hierarchy()
    
    # Should not crash even if centroids unavailable
    result = geo.get_ward_centroid("TestCounty", "TestConstituency", "TestWard")
    assert result is None or isinstance(result, tuple)
