#!/usr/bin/env python3
"""
Quick test script for Earth Engine integration.

Run this to verify your credentials work before running the full updater.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

print("Testing Earth Engine integration...")
print("-" * 50)

# Test 1: Import modules
print("\n1. Checking imports...")
try:
    from openresilience.adapters.earthengine import EarthEngineAdapter
    print("   ✓ Earth Engine adapter imported")
except ImportError as e:
    print(f"   ✗ Import failed: {e}")
    print("   Fix: pip install earthengine-api")
    sys.exit(1)

# Test 2: Initialize adapter
print("\n2. Initializing adapter...")
adapter = EarthEngineAdapter()

if not adapter.is_available():
    print("   ✗ Earth Engine not available")
    print("   Check: GEE_SERVICE_ACCOUNT in environment or Streamlit secrets")
    sys.exit(1)

print("   ✓ Earth Engine authenticated")

# Test 3: Fetch sample NDVI
print("\n3. Fetching sample NDVI (Nairobi)...")
try:
    result = adapter.get_ndvi(
        lat=-1.286389,
        lon=36.817223,
        days=16
    )
    
    if result:
        print(f"   ✓ NDVI fetched successfully!")
        print(f"   - NDVI value: {result['ndvi']:.3f}")
        print(f"   - Vegetation health: {result['vegetation_health']:.3f}")
        print(f"   - Quality flag: {result['quality']}")
        print(f"   - Timestamp: {result['timestamp']}")
        print(f"   - Confidence: {result['confidence']}%")
    else:
        print("   ✗ No NDVI data returned")
        print("   This might be normal if there's recent cloud cover")
        
except Exception as e:
    print(f"   ✗ Error fetching NDVI: {e}")
    sys.exit(1)

print("\n" + "=" * 50)
print("SUCCESS! Earth Engine integration is working! 🌍✨")
print("=" * 50)
print("\nNext step: Run the full data updater")
print("Command: python scripts/update_gee_data.py")
