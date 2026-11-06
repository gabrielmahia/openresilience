"""
OpenResilience Core Package

Provides modular components for resilience intelligence systems.

Modules:
- scoring: Multi-index resilience scoring system
- resolution: Geographic resolution management
- agriculture: Agricultural calendar and farmer advice
- export: Data export utilities for NGOs and administrators
- visuals: Simple visual indicators for farmers
"""

from . import resolution, scoring

try:
    from . import agriculture, export, visuals
except ImportError:
    # New modules may not be available in older deployments
    pass

__version__ = "1.0.0"
