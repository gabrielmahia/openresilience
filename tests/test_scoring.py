"""Smoke tests for shared scoring logic."""

import os
import sys

import numpy as np

# Allow importing or_shared from the shared directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "shared"))

from or_shared.scoring import composite_max, sev_from_thresholds


def test_sev_from_thresholds_higher_worse():
    x = np.array([0.0, 0.15, 0.30, 0.50, 0.80])
    result = sev_from_thresholds(x, 0.15, 0.30, 0.50, higher_worse=True)
    assert list(result) == [0, 1, 2, 3, 3]


def test_sev_from_thresholds_lower_worse():
    x = np.array([0.50, 0.30, 0.20, 0.10, 0.05])
    result = sev_from_thresholds(x, 0.30, 0.20, 0.10, higher_worse=False)
    assert list(result) == [0, 0, 1, 2, 3]


def test_composite_max_takes_element_wise_max():
    a = np.array([0, 1, 2, 0], dtype=np.uint8)
    b = np.array([1, 0, 1, 3], dtype=np.uint8)
    result = composite_max(a, b)
    assert list(result) == [1, 1, 2, 3]
