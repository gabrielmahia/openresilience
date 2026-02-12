"""
Tests for database persistence layer.
"""

import sys
import tempfile
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from openresilience.database import (
    init_database,
    ensure_region,
    insert_run,
    get_recent_runs,
    insert_field_report,
    get_recent_reports,
    create_alert,
    get_active_alerts
)


def test_database_initialization():
    """Test database schema creation."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    # Should create without error
    init_database(db_path)
    
    # Should be idempotent (safe to call multiple times)
    init_database(db_path)
    
    Path(db_path).unlink()  # Cleanup


def test_ensure_region():
    """Test region creation and retrieval."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    init_database(db_path)
    
    # Create new region
    region_id = ensure_region("Nairobi", level="county", db_path=db_path)
    assert region_id > 0
    
    # Retrieving again should return same ID
    region_id2 = ensure_region("Nairobi", level="county", db_path=db_path)
    assert region_id == region_id2
    
    Path(db_path).unlink()


def test_insert_and_retrieve_runs():
    """Test scoring run storage and retrieval."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    init_database(db_path)
    region_id = ensure_region("Kiambu", db_path=db_path)
    
    # Insert run
    scores = {"wsi": 50.0, "fsi": 40.0, "msi": 30.0, "cri": 45.0, "confidence": 75.0}
    signals = {
        "rainfall_anomaly": -30,
        "soil_moisture": 0.5,
        "vegetation_health": 0.6,
        "staple_price_change": 15,
        "market_stockouts": 1,
        "field_reports_24h": 2
    }
    
    run_id = insert_run(region_id, scores, signals, db_path=db_path)
    assert run_id > 0
    
    # Retrieve runs
    runs = get_recent_runs(region_id, db_path=db_path)
    assert len(runs) == 1
    assert runs[0]['wsi'] == 50.0
    assert runs[0]['cri'] == 45.0
    
    Path(db_path).unlink()


def test_field_reports():
    """Test field report submission and retrieval."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    init_database(db_path)
    region_id = ensure_region("Mombasa", db_path=db_path)
    
    # Insert report
    report_id = insert_field_report(
        region_id=region_id,
        category="water",
        severity=4,
        message="Borehole dry since yesterday",
        geo_hint="Near market",
        db_path=db_path
    )
    assert report_id > 0
    
    # Retrieve reports
    reports = get_recent_reports(region_id=region_id, db_path=db_path)
    assert len(reports) == 1
    assert reports[0]['category'] == "water"
    assert reports[0]['severity'] == 4
    
    # Filter by category
    water_reports = get_recent_reports(category="water", db_path=db_path)
    assert len(water_reports) >= 1
    
    Path(db_path).unlink()


def test_alerts():
    """Test alert creation and retrieval."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    init_database(db_path)
    region_id = ensure_region("Turkana", db_path=db_path)
    
    # Create alert
    alert_id = create_alert(
        region_id=region_id,
        level="warning",
        cri=65.0,
        title="Elevated water stress",
        detail="CRI exceeded 60/100 threshold",
        db_path=db_path
    )
    assert alert_id > 0
    
    # Retrieve active alerts
    alerts = get_active_alerts(db_path=db_path)
    assert len(alerts) >= 1
    assert alerts[0]['level'] == "warning"
    
    # Filter by region
    region_alerts = get_active_alerts(region_id=region_id, db_path=db_path)
    assert len(region_alerts) >= 1
    
    Path(db_path).unlink()


def test_hierarchical_regions():
    """Test parent-child region relationships."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    init_database(db_path)
    
    # Create county
    county_id = ensure_region("Nairobi", level="county", db_path=db_path)
    
    # Create constituency under county
    const_id = ensure_region(
        "Westlands",
        level="constituency",
        parent_id=county_id,
        db_path=db_path
    )
    
    assert const_id > county_id  # Different IDs
    assert const_id > 0
    
    Path(db_path).unlink()


def test_database_persistence():
    """Test data persists across connections."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        db_path = tmp.name
    
    # First connection: create and insert
    init_database(db_path)
    region_id = ensure_region("Kisumu", db_path=db_path)
    
    scores = {"wsi": 30.0, "fsi": 25.0, "msi": 20.0, "cri": 28.0, "confidence": 60.0}
    signals = {"rainfall_anomaly": -15, "soil_moisture": 0.6, "vegetation_health": 0.7,
               "staple_price_change": 10, "market_stockouts": 0, "field_reports_24h": 1}
    insert_run(region_id, scores, signals, db_path=db_path)
    
    # Second "connection": retrieve without re-initializing
    runs = get_recent_runs(region_id, db_path=db_path)
    assert len(runs) == 1
    assert runs[0]['cri'] == 28.0
    
    Path(db_path).unlink()
