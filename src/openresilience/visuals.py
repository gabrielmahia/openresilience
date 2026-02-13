"""
Visual Indicators and Mobile-Friendly UI Components

Provides simple, clear visual indicators that work for:
- Farmers with basic phones
- Low-literacy users
- Quick decision-making
"""

from typing import Tuple


def get_stress_emoji(stress_level: float) -> str:
    """
    Get emoji indicator for stress level.
    
    Args:
        stress_level: Stress value 0-1
    
    Returns:
        Emoji string
    """
    if stress_level < 0.3:
        return "🟢"  # Green - Good
    elif stress_level < 0.5:
        return "🟡"  # Yellow - Moderate
    elif stress_level < 0.7:
        return "🟠"  # Orange - High
    else:
        return "🔴"  # Red - Severe


def get_stress_text(stress_level: float, language: str = 'en') -> str:
    """
    Get text description of stress level.
    
    Args:
        stress_level: Stress value 0-1
        language: 'en' or 'sw' (Kiswahili)
    
    Returns:
        Text description
    """
    if language == 'sw':
        if stress_level < 0.3:
            return "Mazingira Nzuri"  # Good conditions
        elif stress_level < 0.5:
            return "Wastani"  # Moderate
        elif stress_level < 0.7:
            return "Hatari"  # Danger
        else:
            return "Dharura"  # Emergency
    else:
        if stress_level < 0.3:
            return "Good"
        elif stress_level < 0.5:
            return "Moderate"
        elif stress_level < 0.7:
            return "High"
        else:
            return "Severe"


def get_action_required(stress_level: float, language: str = 'en') -> Tuple[str, str]:
    """
    Get action required for given stress level.
    
    Args:
        stress_level: Stress value 0-1
        language: 'en' or 'sw'
    
    Returns:
        Tuple of (icon, action_text)
    """
    if language == 'sw':
        if stress_level < 0.3:
            return ("✅", "Endelea na shughuli za kawaida")  # Continue normal activities
        elif stress_level < 0.5:
            return ("⚡", "Punguza matumizi ya maji kwa 20%")  # Reduce water use by 20%
        elif stress_level < 0.7:
            return ("⚠️", "Punguza matumizi ya maji kwa 40%")  # Reduce water use by 40%
        else:
            return ("🚨", "DHARURA: Wasiliana na afisa wa maji")  # EMERGENCY: Contact water officer
    else:
        if stress_level < 0.3:
            return ("✅", "Continue normal activities")
        elif stress_level < 0.5:
            return ("⚡", "Reduce water use by 20%")
        elif stress_level < 0.7:
            return ("⚠️", "Reduce water use by 40%")
        else:
            return ("🚨", "EMERGENCY: Contact water officer")


def get_planting_recommendation(
    stress_level: float,
    month: int,
    is_asal: bool,
    language: str = 'en'
) -> str:
    """
    Get simple planting recommendation for farmers.
    
    Args:
        stress_level: Water stress 0-1
        month: Current month (1-12)
        is_asal: Whether in ASAL zone
        language: 'en' or 'sw'
    
    Returns:
        Simple text recommendation
    """
    # Planting seasons
    is_long_rains = 3 <= month <= 5
    is_short_rains = 10 <= month <= 12
    
    if language == 'sw':
        if stress_level > 0.7:
            return "⛔ USIPANDE - Maji si ya kutosha"  # DON'T PLANT - Not enough water
        elif is_long_rains:
            return "🌱 PANDA SASA - Msimu wa mvua ndefu"  # PLANT NOW - Long rains season
        elif is_short_rains:
            return "🌱 PANDA SASA - Msimu wa mvua fupi"  # PLANT NOW - Short rains season
        else:
            return "⏳ SUBIRI - Si msimu wa kupanda"  # WAIT - Not planting season
    else:
        if stress_level > 0.7:
            return "⛔ DON'T PLANT - Insufficient water"
        elif is_long_rains:
            return "🌱 PLANT NOW - Long rains season"
        elif is_short_rains:
            return "🌱 PLANT NOW - Short rains season"
        else:
            return "⏳ WAIT - Not planting season"


def format_phone_number(number: str) -> str:
    """
    Format phone number for SMS (Kenya format).
    
    Args:
        number: Raw phone number
    
    Returns:
        Formatted +254... number
    """
    # Remove spaces and special chars
    clean = ''.join(c for c in number if c.isdigit())
    
    # Convert 07xx to +254 7xx
    if clean.startswith('0'):
        return f"+254{clean[1:]}"
    elif clean.startswith('254'):
        return f"+{clean}"
    elif clean.startswith('7') or clean.startswith('1'):
        return f"+254{clean}"
    else:
        return clean


def get_simple_forecast(
    current_stress: float,
    forecast_1_2mo: float,
    language: str = 'en'
) -> str:
    """
    Get simple forecast message for farmers.
    
    Args:
        current_stress: Current stress level
        forecast_1_2mo: Forecasted stress in 1-2 months
        language: 'en' or 'sw'
    
    Returns:
        Simple forecast message
    """
    trend = forecast_1_2mo - current_stress
    
    if language == 'sw':
        if trend > 0.1:
            return "📉 Hali itakuwa mbaya - Jiandae"  # Conditions worsening - Prepare
        elif trend < -0.1:
            return "📈 Hali itaboreshwa"  # Conditions improving
        else:
            return "➡️ Hali itaendelea hivyo hivyo"  # Conditions stable
    else:
        if trend > 0.1:
            return "📉 Conditions worsening - Prepare"
        elif trend < -0.1:
            return "📈 Conditions improving"
        else:
            return "➡️ Conditions stable"


# Export functions
__all__ = [
    'get_stress_emoji',
    'get_stress_text',
    'get_action_required',
    'get_planting_recommendation',
    'format_phone_number',
    'get_simple_forecast'
]
