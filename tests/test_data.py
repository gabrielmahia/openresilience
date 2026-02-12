"""Smoke tests for extracted data loading and forecast generation."""

from openresilience.data import generate_forecast, load_county_data


def test_load_county_data_returns_47_counties():
    df = load_county_data()
    assert len(df) == 47
    assert "County" in df.columns
    assert "Current_Stress" in df.columns
    assert "Severity" in df.columns


def test_load_county_data_stress_values_in_range():
    df = load_county_data()
    assert (df["Current_Stress"] >= 0).all()
    assert (df["Current_Stress"] <= 1).all()


def test_generate_forecast_returns_expected_keys():
    result = generate_forecast("Nairobi", 0.5, False)
    expected_keys = {"short", "medium", "long", "trend", "trend_emoji", "season_note", "confidence"}
    assert set(result.keys()) == expected_keys


def test_generate_forecast_values_clipped():
    result = generate_forecast("Turkana", 0.95, True)
    assert 0 <= result["short"] <= 1
    assert 0 <= result["medium"] <= 1
    assert 0 <= result["long"] <= 1
