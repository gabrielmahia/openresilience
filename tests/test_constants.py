"""Smoke tests for geographic constants integrity."""

from openresilience.constants import KENYA_COUNTIES, SPECIAL_AREAS


def test_all_47_counties_present():
    assert len(KENYA_COUNTIES) == 47


def test_county_coordinates_in_valid_range():
    for name, info in KENYA_COUNTIES.items():
        assert -5.0 <= info["lat"] <= 5.0, f"{name} lat out of Kenya range"
        assert 33.0 <= info["lon"] <= 42.0, f"{name} lon out of Kenya range"


def test_county_population_positive():
    for name, info in KENYA_COUNTIES.items():
        assert info["pop"] > 0, f"{name} has non-positive population"


def test_special_areas_reference_valid_counties():
    for area_name, area in SPECIAL_AREAS.items():
        assert area["county"] in KENYA_COUNTIES, f"{area_name} references unknown county {area['county']}"


def test_special_areas_have_required_fields():
    for area_name, area in SPECIAL_AREAS.items():
        assert "lat" in area
        assert "lon" in area
        assert "type" in area
        assert "challenges" in area
        assert "population" in area
        assert area["population"] > 0
