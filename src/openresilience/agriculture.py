"""
Agricultural Calendar and Advice for Kenyan Farmers

Provides context-aware planting advice, crop recommendations,
and water management guidance based on:
- Current water stress levels
- Seasonal patterns
- County/region characteristics
- ASAL vs non-ASAL zones
"""

from datetime import datetime
from typing import Dict, List, Tuple


def get_season_name(month: int) -> str:
    """Get Kenya season name for given month."""
    if 3 <= month <= 5:
        return "Long Rains (Masika)"
    elif 6 <= month <= 9:
        return "Dry Season"
    elif 10 <= month <= 12:
        return "Short Rains (Vuli)"
    else:
        return "Short Dry Season"


def get_planting_advice(
    county_name: str,
    is_asal: bool,
    water_stress: float,
    month: int
) -> Dict[str, any]:
    """
    Get comprehensive planting advice for farmers.
    
    Args:
        county_name: Kenya county name
        is_asal: Whether county is in ASAL zone
        water_stress: Current water stress index (0-1)
        month: Current month (1-12)
    
    Returns:
        Dict with planting recommendations, crops, and water advice
    """
    season = get_season_name(month)
    
    # Determine stress level
    if water_stress < 0.3:
        stress_level = "low"
    elif water_stress < 0.6:
        stress_level = "moderate"
    else:
        stress_level = "high"
    
    # Base recommendations by season
    if 3 <= month <= 5:  # Long rains
        action = "PLANT" if water_stress < 0.7 else "WAIT"
        timing = "Now is planting season" if water_stress < 0.7 else "Delay planting until rains improve"
        
        if is_asal:
            recommended_crops = ["Sorghum", "Millet", "Cowpeas", "Green grams", "Pigeon peas"]
            water_saving = ["Use drought-tolerant varieties", "Plant in basins to capture water", "Mulch heavily"]
        else:
            recommended_crops = ["Maize", "Beans", "Potatoes", "Vegetables", "Kale (Sukuma wiki)"]
            water_saving = ["Plant early to maximize rain", "Use organic mulch", "Practice crop rotation"]
    
    elif 10 <= month <= 12:  # Short rains
        action = "PLANT" if water_stress < 0.7 else "WAIT"
        timing = "Short rains planting window" if water_stress < 0.7 else "Wait for better rainfall"
        
        if is_asal:
            recommended_crops = ["Fast-maturing sorghum", "Green grams", "Cowpeas"]
            water_saving = ["Choose 60-day varieties", "Plant densely to shade soil", "Harvest rainwater"]
        else:
            recommended_crops = ["Short-season maize", "Beans", "Tomatoes", "Onions"]
            water_saving = ["Use improved varieties", "Apply mulch", "Plant cover crops"]
    
    else:  # Dry seasons
        action = "MAINTAIN"
        timing = "Dry season - focus on water conservation"
        
        if is_asal:
            recommended_crops = ["Irrigated vegetables (if water available)", "Fodder crops for livestock"]
            water_saving = ["Drip irrigation essential", "Harvest any available water", "Reduce crop area"]
        else:
            recommended_crops = ["High-value vegetables (if irrigation available)"]
            water_saving = ["Irrigate only critical crops", "Use shade nets", "Conserve water in tanks"]
    
    # Critical actions by stress level
    if stress_level == "high":
        critical_actions = [
            "⚠️ CRITICAL: Reduce irrigation by 30-50%",
            "⚠️ Prioritize drinking water over irrigation",
            "⚠️ Consider drought-resistant crops only",
            "⚠️ Contact county agricultural officer for support"
        ]
    elif stress_level == "moderate":
        critical_actions = [
            "⚡ Monitor water levels daily",
            "⚡ Reduce non-essential water use by 20%",
            "⚡ Prepare water harvesting systems",
            "⚡ Check weather forecasts regularly"
        ]
    else:
        critical_actions = [
            "✅ Normal water management practices OK",
            "✅ Good time to prepare fields",
            "✅ Ensure water storage is ready",
            "✅ Plan crop rotation"
        ]
    
    return {
        'season': season,
        'action': action,
        'timing': timing,
        'stress_level': stress_level,
        'recommended_crops': recommended_crops,
        'water_saving_tips': water_saving,
        'critical_actions': critical_actions,
        'contact': f"{county_name} County Agricultural Office"
    }


def get_next_planting_window(month: int, is_asal: bool) -> Tuple[str, str]:
    """
    Get next planting window information.
    
    Returns:
        Tuple of (window_name, date_range)
    """
    if month < 3:
        return ("Long Rains", "March 15 - April 30")
    elif 3 <= month <= 5:
        return ("Short Rains", "October 15 - November 30")
    elif month < 10:
        return ("Short Rains", "October 15 - November 30")
    elif 10 <= month <= 12:
        return ("Long Rains", "March 15 - April 30 (next year)")
    else:
        return ("Long Rains", "March 15 - April 30")


def get_crop_calendar(is_asal: bool) -> Dict[str, List[Tuple[str, str]]]:
    """
    Get full year crop calendar.
    
    Returns:
        Dict mapping crop name to list of (month, activity) tuples
    """
    if is_asal:
        return {
            "Sorghum": [
                ("March", "Plant"),
                ("May", "Weed"),
                ("July", "Harvest"),
                ("October", "Plant (short season)"),
                ("December", "Harvest")
            ],
            "Millet": [
                ("March", "Plant"),
                ("June", "Harvest"),
                ("October", "Plant"),
                ("December", "Harvest")
            ],
            "Green Grams": [
                ("March", "Plant"),
                ("May", "Harvest"),
                ("October", "Plant"),
                ("December", "Harvest")
            ]
        }
    else:
        return {
            "Maize": [
                ("March", "Plant long rains crop"),
                ("April", "First weeding"),
                ("May", "Top dressing"),
                ("August", "Harvest"),
                ("October", "Plant short rains crop"),
                ("January", "Harvest")
            ],
            "Beans": [
                ("March", "Plant with maize"),
                ("June", "Harvest"),
                ("October", "Plant short season"),
                ("December", "Harvest")
            ],
            "Vegetables": [
                ("Year-round", "Plant with irrigation"),
                ("Continuous", "Harvest every 2-3 months")
            ]
        }


# Export functions
__all__ = [
    'get_planting_advice',
    'get_next_planting_window',
    'get_crop_calendar',
    'get_season_name'
]
