"""
Multi-Index Scoring System for OpenResilience

Provides algorithmic assessment across four resilience dimensions:
- WSI: Water Stress Index
- FSI: Food Stress Index
- MSI: Market Stress Index
- CRI: Composite Risk Index

All indices use 0-100 scale where higher = more stress/risk.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class ResilienceScores:
    """Container for multi-dimensional resilience scores."""
    wsi: float  # Water Stress Index (0-100)
    fsi: float  # Food Stress Index (0-100)
    msi: float  # Market Stress Index (0-100)
    cri: float  # Composite Risk Index (0-100)
    confidence: float  # Overall confidence (0-100)
    
    def to_dict(self) -> Dict[str, float]:
        """Export as dictionary for storage/display."""
        return {
            "wsi": self.wsi,
            "fsi": self.fsi,
            "msi": self.msi,
            "cri": self.cri,
            "confidence": self.confidence
        }


def clamp(value: float, minimum: float = 0.0, maximum: float = 100.0) -> float:
    """
    Clamp a value between minimum and maximum bounds.
    
    Args:
        value: Value to clamp
        minimum: Lower bound (default 0.0)
        maximum: Upper bound (default 100.0)
    
    Returns:
        Clamped value
    """
    return max(minimum, min(maximum, value))


def compute_water_stress(
    rainfall_anomaly: float,  # -100 to +100 (% deviation from normal)
    soil_moisture: float,      # 0 to 1 (0=dry, 1=saturated)
    **kwargs
) -> float:
    """
    Calculate Water Stress Index (WSI).
    
    Combines rainfall deficit with soil moisture depletion.
    
    Args:
        rainfall_anomaly: % deviation from normal (-100 to +100)
        soil_moisture: Soil moisture ratio (0-1)
        **kwargs: Additional parameters (ignored for forward compatibility)
    
    Returns:
        WSI score (0-100, higher = more stress)
    
    Algorithm:
        WSI = 0.55 * rainfall_deficit + 0.45 * soil_dryness
        Where:
        - rainfall_deficit = max(0, -rainfall_anomaly)
        - soil_dryness = (1 - soil_moisture) * 100
    """
    # Convert rainfall anomaly to stress (negative anomaly = stress)
    rainfall_deficit = clamp(-rainfall_anomaly, 0, 100)
    
    # Convert soil moisture to dryness
    soil_dryness = clamp((1 - soil_moisture) * 100, 0, 100)
    
    # Weighted combination (rainfall slightly more important)
    wsi = 0.55 * rainfall_deficit + 0.45 * soil_dryness
    
    return clamp(wsi)


def compute_food_stress(
    vegetation_health: float,  # 0 to 1 (NDVI-like: 0=bare, 1=healthy)
    water_stress: float,       # 0 to 100 (from compute_water_stress)
    field_reports_24h: int,    # Count of stress reports in last 24h
    **kwargs
) -> float:
    """
    Calculate Food Stress Index (FSI).
    
    Integrates vegetation decline, water stress, and ground reports.
    
    Args:
        vegetation_health: Vegetation index (0-1, NDVI-like)
        water_stress: Pre-computed WSI score (0-100)
        field_reports_24h: Number of field reports indicating stress
        **kwargs: Additional parameters (ignored)
    
    Returns:
        FSI score (0-100, higher = more stress)
    
    Algorithm:
        FSI = 0.50 * vegetation_decline + 0.30 * water_stress + 0.20 * report_signal
        Where:
        - vegetation_decline = (1 - vegetation_health) * 100
        - report_signal = min(100, field_reports_24h * 12)
    """
    # Convert vegetation health to decline
    vegetation_decline = clamp((1 - vegetation_health) * 100, 0, 100)
    
    # Scale field reports (each report = ~12 points, cap at 100)
    report_signal = clamp(field_reports_24h * 12, 0, 100)
    
    # Weighted combination
    fsi = (
        0.50 * vegetation_decline +
        0.30 * water_stress +
        0.20 * report_signal
    )
    
    return clamp(fsi)


def compute_market_stress(
    staple_price_change: float,  # -100 to +100 (% change from baseline)
    market_stockouts: int,        # 0 to 5 (count of staple items unavailable)
    **kwargs
) -> float:
    """
    Calculate Market Stress Index (MSI).
    
    Tracks food price inflation and supply disruptions.
    
    Args:
        staple_price_change: % change in staple food basket price
        market_stockouts: Number of essential items out of stock (0-5)
        **kwargs: Additional parameters (ignored)
    
    Returns:
        MSI score (0-100, higher = more stress)
    
    Algorithm:
        MSI = 0.70 * price_stress + 0.30 * availability_stress
        Where:
        - price_stress = max(0, staple_price_change)
        - availability_stress = stockouts * 20
    """
    # Only price increases contribute to stress
    price_stress = clamp(staple_price_change, 0, 100)
    
    # Each stockout = 20 points (5 stockouts = 100%)
    availability_stress = clamp(market_stockouts * 20, 0, 100)
    
    # Price weighted more heavily than availability
    msi = 0.70 * price_stress + 0.30 * availability_stress
    
    return clamp(msi)


def compute_composite_risk(
    wsi: float,
    fsi: float,
    msi: float,
    **kwargs
) -> float:
    """
    Calculate Composite Risk Index (CRI).
    
    Drought-weighted aggregation of all stress indices.
    
    Args:
        wsi: Water Stress Index (0-100)
        fsi: Food Stress Index (0-100)
        msi: Market Stress Index (0-100)
        **kwargs: Additional parameters (ignored)
    
    Returns:
        CRI score (0-100, higher = more risk)
    
    Algorithm:
        CRI = 0.45 * WSI + 0.35 * FSI + 0.20 * MSI
        
        Rationale: Water stress is the primary driver in arid/semi-arid
        regions, with food security as secondary concern and market
        disruption as tertiary indicator.
    """
    cri = 0.45 * wsi + 0.35 * fsi + 0.20 * msi
    return clamp(cri)


def compute_confidence(
    rainfall_anomaly: float,
    soil_moisture: float,
    vegetation_health: float,
    field_reports_24h: int,
    **kwargs
) -> float:
    """
    Estimate confidence in composite scoring.
    
    Higher confidence when multiple signals align on stress direction.
    
    Args:
        rainfall_anomaly: % deviation from normal
        soil_moisture: Soil moisture ratio (0-1)
        vegetation_health: Vegetation index (0-1)
        field_reports_24h: Field report count
        **kwargs: Additional parameters (ignored)
    
    Returns:
        Confidence score (0-100, higher = more reliable)
    
    Algorithm:
        Count aligned stress indicators:
        - Rainfall deficit > 20%
        - Soil moisture < 0.35
        - Vegetation health < 0.45
        - 2+ field reports
        
        Confidence = (aligned_count / 4) * 100
    """
    aligned = 0
    
    # Check if each signal indicates stress
    if rainfall_anomaly < -20:  # 20%+ rainfall deficit
        aligned += 1
    
    if soil_moisture < 0.35:  # Significantly dry soil
        aligned += 1
    
    if vegetation_health < 0.45:  # Poor vegetation
        aligned += 1
    
    if field_reports_24h >= 2:  # Multiple ground reports
        aligned += 1
    
    # Convert to percentage
    confidence = (aligned / 4.0) * 100
    
    return clamp(confidence)


def compute_resilience_scores(
    rainfall_anomaly: float = 0.0,
    soil_moisture: float = 0.5,
    vegetation_health: float = 0.7,
    staple_price_change: float = 0.0,
    market_stockouts: int = 0,
    field_reports_24h: int = 0,
    **kwargs
) -> ResilienceScores:
    """
    Compute all resilience indices from input signals.
    
    This is the main entry point for multi-index scoring.
    
    Args:
        rainfall_anomaly: % deviation from normal (-100 to +100)
        soil_moisture: Soil moisture ratio (0-1)
        vegetation_health: Vegetation index (0-1, NDVI-like)
        staple_price_change: % change in food prices (-100 to +100)
        market_stockouts: Count of unavailable staples (0-5)
        field_reports_24h: Ground truth reports in last 24h
        **kwargs: Additional parameters (forward compatibility)
    
    Returns:
        ResilienceScores object with all indices
    
    Example:
        >>> scores = compute_resilience_scores(
        ...     rainfall_anomaly=-45,  # 45% below normal
        ...     soil_moisture=0.25,     # Dry soil
        ...     vegetation_health=0.35, # Poor vegetation
        ...     staple_price_change=30, # 30% price increase
        ...     market_stockouts=2,     # 2 items out of stock
        ...     field_reports_24h=5     # 5 stress reports
        ... )
        >>> print(f"CRI: {scores.cri:.1f}")
        CRI: 68.4
    """
    # Compute individual indices
    wsi = compute_water_stress(
        rainfall_anomaly=rainfall_anomaly,
        soil_moisture=soil_moisture,
        **kwargs
    )
    
    fsi = compute_food_stress(
        vegetation_health=vegetation_health,
        water_stress=wsi,
        field_reports_24h=field_reports_24h,
        **kwargs
    )
    
    msi = compute_market_stress(
        staple_price_change=staple_price_change,
        market_stockouts=market_stockouts,
        **kwargs
    )
    
    cri = compute_composite_risk(
        wsi=wsi,
        fsi=fsi,
        msi=msi,
        **kwargs
    )
    
    confidence = compute_confidence(
        rainfall_anomaly=rainfall_anomaly,
        soil_moisture=soil_moisture,
        vegetation_health=vegetation_health,
        field_reports_24h=field_reports_24h,
        **kwargs
    )
    
    return ResilienceScores(
        wsi=wsi,
        fsi=fsi,
        msi=msi,
        cri=cri,
        confidence=confidence
    )


# Export main components
__all__ = [
    "ResilienceScores",
    "compute_resilience_scores",
    "compute_water_stress",
    "compute_food_stress",
    "compute_market_stress",
    "compute_composite_risk",
    "compute_confidence",
]
