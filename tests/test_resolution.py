"""
Smoke tests for resolution engine.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from openresilience.resolution import (
    DataMode,
    Resolution,
    ResolutionStatus,
    determine_resolution,
    get_current_status
)


def test_enums_exist():
    """Verify enums are properly defined."""
    assert DataMode.DEMO.value == "demo"
    assert DataMode.LIVE.value == "live"
    
    assert Resolution.WARD.value == "ward"
    assert Resolution.CONSTITUENCY.value == "constituency"
    assert Resolution.COUNTY.value == "county"
    assert Resolution.NATIONAL.value == "national"


def test_resolution_status_creation():
    """Verify ResolutionStatus can be created."""
    status = ResolutionStatus()
    
    assert status.mode == DataMode.DEMO
    assert status.resolution == Resolution.COUNTY
    assert isinstance(status.timestamp, datetime)
    assert status.confidence == "demonstration"


def test_resolution_status_to_dict():
    """Verify status can be exported as dictionary."""
    status = ResolutionStatus()
    d = status.to_dict()
    
    assert "mode" in d
    assert "resolution" in d
    assert "source" in d
    assert "timestamp" in d
    assert "confidence" in d


def test_determine_resolution_county_default():
    """Test county-level resolution as default."""
    res = determine_resolution("Nairobi")
    assert res == Resolution.COUNTY


def test_determine_resolution_constituency():
    """Test constituency resolution when specified."""
    res = determine_resolution(
        "Nairobi",
        constituency="Westlands",
        hierarchy_available=True
    )
    assert res == Resolution.CONSTITUENCY


def test_determine_resolution_ward():
    """Test ward resolution when data available."""
    res = determine_resolution(
        "Nairobi",
        constituency="Westlands",
        ward="Kitisuru",
        hierarchy_available=True,
        ward_data_available=True
    )
    assert res == Resolution.WARD


def test_determine_resolution_fallback():
    """Test resolution falls back appropriately."""
    # Ward specified but no data -> should fall back
    res = determine_resolution(
        "Nairobi",
        constituency="Westlands",
        ward="Kitisuru",
        hierarchy_available=False,
        ward_data_available=False
    )
    assert res in [Resolution.COUNTY, Resolution.CONSTITUENCY]


def test_get_current_status_smoke():
    """Verify get_current_status doesn't crash."""
    status = get_current_status("Nairobi")
    
    assert isinstance(status, ResolutionStatus)
    assert status.mode == DataMode.DEMO
    assert status.resolution in [r for r in Resolution]
    assert len(status.source) > 0


def test_status_includes_demo_warning():
    """Verify status includes demo data warnings."""
    status = get_current_status("Nairobi")
    
    assert status.notes is not None
    assert "demo" in status.notes.lower() or "Demo" in status.notes
