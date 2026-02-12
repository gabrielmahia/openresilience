"""
Database Persistence Layer for OpenResilience

SQLite-based storage for:
- Regions (counties/constituencies/wards)
- Scoring runs (historical index calculations)
- Field reports (ground truth from communities)
- Alerts (threshold-based notifications)

Design: Local-first, zero-infrastructure, portable
"""

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple


DEFAULT_DB_PATH = "openresilience.db"


@contextmanager
def get_connection(db_path: str = DEFAULT_DB_PATH):
    """
    Context manager for database connections.
    
    Args:
        db_path: Path to SQLite database file
    
    Yields:
        sqlite3.Connection object
    
    Example:
        with get_connection() as conn:
            conn.execute("SELECT * FROM regions")
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enable dict-like access
    try:
        yield conn
    finally:
        conn.close()


def init_database(db_path: str = DEFAULT_DB_PATH) -> None:
    """
    Initialize database schema if it doesn't exist.
    
    Creates tables for regions, runs, field_reports, and alerts.
    Safe to call multiple times (idempotent).
    
    Args:
        db_path: Path to SQLite database file
    """
    with get_connection(db_path) as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS regions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            level TEXT NOT NULL DEFAULT 'county',
            parent_id INTEGER,
            country TEXT NOT NULL DEFAULT 'Kenya',
            latitude REAL,
            longitude REAL,
            population INTEGER,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(parent_id) REFERENCES regions(id)
        );
        
        CREATE INDEX IF NOT EXISTS idx_regions_name ON regions(name);
        CREATE INDEX IF NOT EXISTS idx_regions_level ON regions(level);
        
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            
            -- Input signals
            rainfall_anomaly REAL NOT NULL,
            soil_moisture REAL NOT NULL,
            vegetation_health REAL NOT NULL,
            staple_price_change REAL NOT NULL,
            market_stockouts INTEGER NOT NULL,
            field_reports_24h INTEGER NOT NULL,
            
            -- Computed indices
            wsi REAL NOT NULL,
            fsi REAL NOT NULL,
            msi REAL NOT NULL,
            cri REAL NOT NULL,
            confidence REAL NOT NULL,
            
            -- Metadata
            notes TEXT,
            data_mode TEXT NOT NULL DEFAULT 'demo',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY(region_id) REFERENCES regions(id)
        );
        
        CREATE INDEX IF NOT EXISTS idx_runs_region_time ON runs(region_id, timestamp);
        CREATE INDEX IF NOT EXISTS idx_runs_cri ON runs(cri);
        
        CREATE TABLE IF NOT EXISTS field_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            
            category TEXT NOT NULL,
            severity INTEGER NOT NULL,
            message TEXT NOT NULL,
            
            -- Privacy-preserving identifiers
            contact_hash TEXT,
            geo_hint TEXT,
            
            -- Verification
            verified INTEGER NOT NULL DEFAULT 0,
            verified_at TEXT,
            verified_by TEXT,
            
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY(region_id) REFERENCES regions(id)
        );
        
        CREATE INDEX IF NOT EXISTS idx_reports_region_time ON field_reports(region_id, timestamp);
        CREATE INDEX IF NOT EXISTS idx_reports_category ON field_reports(category);
        
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            
            level TEXT NOT NULL,
            cri REAL NOT NULL,
            title TEXT NOT NULL,
            detail TEXT NOT NULL,
            
            -- Response tracking
            acknowledged INTEGER NOT NULL DEFAULT 0,
            acknowledged_at TEXT,
            acknowledged_by TEXT,
            
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY(region_id) REFERENCES regions(id)
        );
        
        CREATE INDEX IF NOT EXISTS idx_alerts_region_time ON alerts(region_id, timestamp);
        CREATE INDEX IF NOT EXISTS idx_alerts_level ON alerts(level);
        CREATE INDEX IF NOT EXISTS idx_alerts_ack ON alerts(acknowledged);
        """)
        conn.commit()


def ensure_region(
    region_name: str,
    level: str = "county",
    parent_id: Optional[int] = None,
    country: str = "Kenya",
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    population: Optional[int] = None,
    db_path: str = DEFAULT_DB_PATH
) -> int:
    """
    Ensure a region exists in the database, creating if necessary.
    
    Args:
        region_name: Name of the region
        level: Geographic level (county, constituency, ward, national)
        parent_id: ID of parent region (for hierarchical structure)
        country: Country name
        latitude: Centroid latitude
        longitude: Centroid longitude
        population: Population estimate
        db_path: Database file path
    
    Returns:
        Region ID (integer)
    """
    with get_connection(db_path) as conn:
        # Check if exists
        cur = conn.execute(
            "SELECT id FROM regions WHERE name = ? AND level = ?",
            (region_name, level)
        )
        row = cur.fetchone()
        
        if row:
            return int(row["id"])
        
        # Create new region
        conn.execute(
            """INSERT INTO regions 
               (name, level, parent_id, country, latitude, longitude, population)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (region_name, level, parent_id, country, latitude, longitude, population)
        )
        conn.commit()
        
        # Return new ID
        cur = conn.execute(
            "SELECT id FROM regions WHERE name = ? AND level = ?",
            (region_name, level)
        )
        return int(cur.fetchone()["id"])


def insert_run(
    region_id: int,
    scores: Dict[str, float],
    signals: Dict[str, Any],
    timestamp: Optional[str] = None,
    notes: str = "",
    data_mode: str = "demo",
    db_path: str = DEFAULT_DB_PATH
) -> int:
    """
    Record a scoring run in the database.
    
    Args:
        region_id: Region identifier
        scores: Dict with wsi, fsi, msi, cri, confidence
        signals: Dict with input signal values
        timestamp: ISO timestamp (defaults to now)
        notes: Optional notes about this run
        data_mode: Data source mode (demo, simulated, live, hybrid)
        db_path: Database file path
    
    Returns:
        Run ID (integer)
    """
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    
    with get_connection(db_path) as conn:
        cur = conn.execute(
            """INSERT INTO runs (
                region_id, timestamp,
                rainfall_anomaly, soil_moisture, vegetation_health,
                staple_price_change, market_stockouts, field_reports_24h,
                wsi, fsi, msi, cri, confidence,
                notes, data_mode
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                region_id, timestamp,
                signals.get("rainfall_anomaly", 0.0),
                signals.get("soil_moisture", 0.5),
                signals.get("vegetation_health", 0.7),
                signals.get("staple_price_change", 0.0),
                signals.get("market_stockouts", 0),
                signals.get("field_reports_24h", 0),
                scores["wsi"], scores["fsi"], scores["msi"],
                scores["cri"], scores["confidence"],
                notes, data_mode
            )
        )
        conn.commit()
        return cur.lastrowid


def get_recent_runs(
    region_id: int,
    limit: int = 10,
    db_path: str = DEFAULT_DB_PATH
) -> List[Dict[str, Any]]:
    """
    Retrieve recent scoring runs for a region.
    
    Args:
        region_id: Region identifier
        limit: Maximum number of runs to return
        db_path: Database file path
    
    Returns:
        List of run dictionaries
    """
    with get_connection(db_path) as conn:
        cur = conn.execute(
            """SELECT * FROM runs 
               WHERE region_id = ? 
               ORDER BY timestamp DESC 
               LIMIT ?""",
            (region_id, limit)
        )
        return [dict(row) for row in cur.fetchall()]


def insert_field_report(
    region_id: int,
    category: str,
    severity: int,
    message: str,
    contact_hash: Optional[str] = None,
    geo_hint: Optional[str] = None,
    timestamp: Optional[str] = None,
    db_path: str = DEFAULT_DB_PATH
) -> int:
    """
    Record a field report from community.
    
    Args:
        region_id: Region identifier
        category: Report category (water, food, market, health, security)
        severity: Severity rating (1-5, 5=critical)
        message: Free-text description
        contact_hash: Privacy-preserving contact identifier
        geo_hint: Coarse location hint (not precise coordinates)
        timestamp: ISO timestamp (defaults to now)
        db_path: Database file path
    
    Returns:
        Report ID (integer)
    """
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    
    with get_connection(db_path) as conn:
        cur = conn.execute(
            """INSERT INTO field_reports (
                region_id, timestamp, category, severity, message,
                contact_hash, geo_hint
            ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (region_id, timestamp, category, severity, message,
             contact_hash, geo_hint)
        )
        conn.commit()
        return cur.lastrowid


def get_recent_reports(
    region_id: Optional[int] = None,
    category: Optional[str] = None,
    limit: int = 50,
    db_path: str = DEFAULT_DB_PATH
) -> List[Dict[str, Any]]:
    """
    Retrieve recent field reports.
    
    Args:
        region_id: Optional region filter
        category: Optional category filter
        limit: Maximum number of reports
        db_path: Database file path
    
    Returns:
        List of report dictionaries
    """
    with get_connection(db_path) as conn:
        query = "SELECT * FROM field_reports WHERE 1=1"
        params = []
        
        if region_id is not None:
            query += " AND region_id = ?"
            params.append(region_id)
        
        if category is not None:
            query += " AND category = ?"
            params.append(category)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cur = conn.execute(query, params)
        return [dict(row) for row in cur.fetchall()]


def create_alert(
    region_id: int,
    level: str,
    cri: float,
    title: str,
    detail: str,
    timestamp: Optional[str] = None,
    db_path: str = DEFAULT_DB_PATH
) -> int:
    """
    Create a new alert for a region.
    
    Args:
        region_id: Region identifier
        level: Alert level (info, warning, critical)
        cri: Composite risk index that triggered alert
        title: Brief alert title
        detail: Detailed alert message
        timestamp: ISO timestamp (defaults to now)
        db_path: Database file path
    
    Returns:
        Alert ID (integer)
    """
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    
    with get_connection(db_path) as conn:
        cur = conn.execute(
            """INSERT INTO alerts (
                region_id, timestamp, level, cri, title, detail
            ) VALUES (?, ?, ?, ?, ?, ?)""",
            (region_id, timestamp, level, cri, title, detail)
        )
        conn.commit()
        return cur.lastrowid


def get_active_alerts(
    region_id: Optional[int] = None,
    db_path: str = DEFAULT_DB_PATH
) -> List[Dict[str, Any]]:
    """
    Retrieve unacknowledged alerts.
    
    Args:
        region_id: Optional region filter
        db_path: Database file path
    
    Returns:
        List of alert dictionaries
    """
    with get_connection(db_path) as conn:
        query = """SELECT a.*, r.name as region_name
                   FROM alerts a
                   JOIN regions r ON a.region_id = r.id
                   WHERE a.acknowledged = 0"""
        params = []
        
        if region_id is not None:
            query += " AND a.region_id = ?"
            params.append(region_id)
        
        query += " ORDER BY a.timestamp DESC"
        
        cur = conn.execute(query, params)
        return [dict(row) for row in cur.fetchall()]


# Export main functions
__all__ = [
    "init_database",
    "get_connection",
    "ensure_region",
    "insert_run",
    "get_recent_runs",
    "insert_field_report",
    "get_recent_reports",
    "create_alert",
    "get_active_alerts",
    "DEFAULT_DB_PATH",
]
