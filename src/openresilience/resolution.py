"""
Resolution Engine for OpenResilience

Determines the geographic resolution level (ward/constituency/county)
and data quality status for display in the UI.
"""

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any


class DataMode(Enum):
    """Data source mode."""
    DEMO = "demo"
    SIMULATED = "simulated"
    LIVE = "live"
    HYBRID = "hybrid"


class Resolution(Enum):
    """Geographic resolution level."""
    WARD = "ward"
    CONSTITUENCY = "constituency"
    COUNTY = "county"
    NATIONAL = "national"


class ResolutionStatus:
    """
    Container for current system resolution status.
    
    Tracks what level of geographic detail is being used
    and what data sources are active.
    """
    
    def __init__(
        self,
        mode: DataMode = DataMode.DEMO,
        resolution: Resolution = Resolution.COUNTY,
        source: str = "Synthetic scoring algorithms",
        timestamp: Optional[datetime] = None,
        confidence: str = "demonstration",
        notes: Optional[str] = None
    ):
        self.mode = mode
        self.resolution = resolution
        self.source = source
        self.timestamp = timestamp or datetime.now()
        self.confidence = confidence
        self.notes = notes
    
    def to_dict(self) -> Dict[str, Any]:
        """Export status as dictionary for UI display."""
        return {
            "mode": self.mode.value,
            "resolution": self.resolution.value,
            "source": self.source,
            "timestamp": self.timestamp.isoformat(),
            "confidence": self.confidence,
            "notes": self.notes
        }
    
    def __str__(self) -> str:
        """Human-readable status summary."""
        return f"{self.mode.value.upper()} | {self.resolution.value.upper()} | {self.source}"


def determine_resolution(
    county: str,
    constituency: Optional[str] = None,
    ward: Optional[str] = None,
    hierarchy_available: bool = False,
    ward_data_available: bool = False
) -> Resolution:
    """
    Determine the appropriate geographic resolution based on selected area and data availability.
    
    Args:
        county: Selected county name
        constituency: Selected constituency (None if county-wide)
        ward: Selected ward (None if all wards or constituency-wide)
        hierarchy_available: Whether hierarchy data is loaded
        ward_data_available: Whether ward-level datasets exist
    
    Returns:
        Resolution level (WARD, CONSTITUENCY, COUNTY, or NATIONAL)
    """
    # If ward specified and ward data exists, use ward resolution
    if ward and ward != "All wards" and ward_data_available:
        return Resolution.WARD
    
    # If constituency specified and hierarchy available, use constituency resolution
    if constituency and constituency != "County-wide" and hierarchy_available:
        return Resolution.CONSTITUENCY
    
    # Default to county resolution
    if county:
        return Resolution.COUNTY
    
    # Fallback to national
    return Resolution.NATIONAL


def get_current_status(
    selected_county: str,
    selected_constituency: Optional[str] = None,
    selected_ward: Optional[str] = None,
    hierarchy_available: bool = False,
    ward_data_available: bool = False
) -> ResolutionStatus:
    """
    Get current system status for UI display.
    
    Args:
        selected_county: Active county selection
        selected_constituency: Active constituency (if any)
        selected_ward: Active ward (if any)
        hierarchy_available: Hierarchy data loaded
        ward_data_available: Ward-level data available
    
    Returns:
        ResolutionStatus object with current system state
    """
    resolution = determine_resolution(
        selected_county,
        selected_constituency,
        selected_ward,
        hierarchy_available,
        ward_data_available
    )
    
    # Determine data source description
    if resolution == Resolution.WARD:
        source = "Ward-level synthetic models"
        notes = "Demo data - not real-time ward measurements"
    elif resolution == Resolution.CONSTITUENCY:
        source = "Constituency aggregate models"
        notes = "Demo data - aggregated from county baseline"
    else:
        source = "County-level synthetic models"
        notes = "Demo data - not real-time satellite or ground truth"
    
    return ResolutionStatus(
        mode=DataMode.DEMO,
        resolution=resolution,
        source=source,
        confidence="demonstration",
        notes=notes
    )


# Export main classes and functions
__all__ = [
    "DataMode",
    "Resolution",
    "ResolutionStatus",
    "determine_resolution",
    "get_current_status"
]
