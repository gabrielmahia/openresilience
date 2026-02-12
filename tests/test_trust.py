"""Smoke tests for shared trust/confidence logic."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "shared"))

from or_shared.trust import confidence_from_inputs


def test_high_confidence_when_fresh_and_complete():
    assert confidence_from_inputs(missing_pct=0.0, freshness_min=5, cadence_min=10) == "high"


def test_low_confidence_when_too_much_missing():
    assert confidence_from_inputs(missing_pct=15.0, freshness_min=5, cadence_min=10) == "low"


def test_medium_confidence_when_slightly_stale():
    assert confidence_from_inputs(missing_pct=5.0, freshness_min=15, cadence_min=10) == "medium"


def test_low_confidence_when_very_stale():
    assert confidence_from_inputs(missing_pct=5.0, freshness_min=30, cadence_min=10) == "low"
