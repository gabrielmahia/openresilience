"""
Tests for multi-index scoring module.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from openresilience.scoring import (
    compute_resilience_scores,
    compute_water_stress,
    compute_food_stress,
    compute_market_stress,
    compute_composite_risk,
    ResilienceScores
)


def test_water_stress_calculation():
    """Test WSI calculation with known inputs."""
    # Severe drought conditions
    wsi = compute_water_stress(
        rainfall_anomaly=-50,  # 50% below normal
        soil_moisture=0.2      # Very dry
    )
    assert 60 <= wsi <= 85, f"Expected high WSI, got {wsi}"
    
    # Normal conditions
    wsi_normal = compute_water_stress(
        rainfall_anomaly=0,
        soil_moisture=0.6
    )
    assert 20 <= wsi_normal <= 45, f"Expected moderate WSI, got {wsi_normal}"


def test_food_stress_calculation():
    """Test FSI calculation."""
    # Poor food security
    fsi = compute_food_stress(
        vegetation_health=0.3,  # Poor vegetation
        water_stress=70,        # High water stress
        field_reports_24h=5     # Multiple reports
    )
    assert 60 <= fsi <= 90, f"Expected high FSI, got {fsi}"


def test_market_stress_calculation():
    """Test MSI calculation."""
    # High market stress
    msi = compute_market_stress(
        staple_price_change=40,  # 40% price increase
        market_stockouts=3       # Multiple stockouts
    )
    assert 35 <= msi <= 50, f"Expected high MSI, got {msi}"


def test_composite_risk_weighting():
    """Test CRI properly weights WSI > FSI > MSI."""
    cri = compute_composite_risk(wsi=60, fsi=40, msi=20)
    
    # Should be closer to WSI due to 0.45 weight
    assert 40 <= cri <= 50, f"Expected weighted CRI, got {cri}"
    
    # CRI should equal weighted average
    expected = 0.45 * 60 + 0.35 * 40 + 0.20 * 20
    assert abs(cri - expected) < 0.1


def test_resilience_scores_dataclass():
    """Test ResilienceScores container."""
    scores = ResilienceScores(
        wsi=50.0,
        fsi=40.0,
        msi=30.0,
        cri=45.0,
        confidence=75.0
    )
    
    assert scores.wsi == 50.0
    assert scores.cri == 45.0
    
    # Test to_dict conversion
    d = scores.to_dict()
    assert d['wsi'] == 50.0
    assert d['confidence'] == 75.0


def test_compute_resilience_scores_integration():
    """Test full scoring pipeline."""
    scores = compute_resilience_scores(
        rainfall_anomaly=-40,
        soil_moisture=0.3,
        vegetation_health=0.4,
        staple_price_change=25,
        market_stockouts=2,
        field_reports_24h=3
    )
    
    # All scores should be in valid range
    assert 0 <= scores.wsi <= 100
    assert 0 <= scores.fsi <= 100
    assert 0 <= scores.msi <= 100
    assert 0 <= scores.cri <= 100
    assert 0 <= scores.confidence <= 100
    
    # WSI should be highest given severe drought inputs
    assert scores.wsi > scores.fsi
    assert scores.wsi > scores.msi


def test_scoring_with_defaults():
    """Test scoring works with default parameters."""
    scores = compute_resilience_scores()
    
    # Should return moderate scores with defaults
    assert 0 <= scores.cri <= 100
    assert scores.confidence >= 0


def test_extreme_values_clamped():
    """Test extreme values are properly clamped."""
    scores = compute_resilience_scores(
        rainfall_anomaly=-200,  # Way beyond range
        soil_moisture=2.0,      # Invalid
        vegetation_health=-1.0, # Invalid
        staple_price_change=500,  # Extreme
        market_stockouts=20,    # Way too many
        field_reports_24h=1000  # Unrealistic
    )
    
    # All scores should still be in valid range
    assert 0 <= scores.wsi <= 100
    assert 0 <= scores.fsi <= 100
    assert 0 <= scores.msi <= 100
    assert 0 <= scores.cri <= 100
