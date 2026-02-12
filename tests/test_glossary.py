"""
Smoke tests for water stress glossary module.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from openresilience.glossary import (
    get_stress_category,
    get_stress_interpretation,
    get_glossary_text,
    WATER_STRESS_SCALE
)


def test_stress_scale_structure():
    """Verify stress scale has expected categories."""
    assert "minimal" in WATER_STRESS_SCALE
    assert "low" in WATER_STRESS_SCALE
    assert "moderate" in WATER_STRESS_SCALE
    assert "high" in WATER_STRESS_SCALE
    assert "extreme" in WATER_STRESS_SCALE


def test_stress_category_boundaries():
    """Test stress category classification at boundaries."""
    assert get_stress_category(0.0) == "minimal"
    assert get_stress_category(1.9) == "minimal"
    assert get_stress_category(2.0) == "low"
    assert get_stress_category(3.9) == "low"
    assert get_stress_category(4.0) == "moderate"
    assert get_stress_category(5.9) == "moderate"
    assert get_stress_category(6.0) == "high"
    assert get_stress_category(7.9) == "high"
    assert get_stress_category(8.0) == "extreme"
    assert get_stress_category(10.0) == "extreme"


def test_stress_interpretation_completeness():
    """Verify all categories have interpretations."""
    categories = ["minimal", "low", "moderate", "high", "extreme"]
    
    for category in categories:
        interp = get_stress_interpretation(category)
        assert "meaning" in interp
        assert "conditions" in interp
        assert "actions" in interp
        assert "confidence" in interp
        # Verify confidence disclaimer present
        assert "demonstration" in interp["confidence"].lower()


def test_glossary_text_format():
    """Verify glossary text is non-empty markdown."""
    text = get_glossary_text()
    assert len(text) > 100
    assert "Water Stress" in text
    assert "0.0 - 2.0" in text  # Check scale table present
    assert "Demo Mode" in text or "demo" in text.lower()


def test_interpretation_trust_labeling():
    """Verify all interpretations include demo data warnings."""
    categories = ["minimal", "low", "moderate", "high", "extreme"]
    
    for category in categories:
        interp = get_stress_interpretation(category)
        confidence = interp["confidence"].lower()
        # Should mention demo/demonstration
        assert "demo" in confidence or "demonstration" in confidence
