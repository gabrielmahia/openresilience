"""
Water Stress Glossary and Interpretation Framework

Provides definitions, interpretation scales, and recommended actions
for water stress indicators used in OpenResilience.
"""

from typing import Dict, Tuple

# Water Stress Index Scale (0-10)
WATER_STRESS_SCALE = {
    "minimal": (0.0, 2.0),
    "low": (2.0, 4.0),
    "moderate": (4.0, 6.0),
    "high": (6.0, 8.0),
    "extreme": (8.0, 10.0),
}


def get_stress_category(stress_value: float) -> str:
    """
    Categorize a water stress value into human-readable category.
    
    Args:
        stress_value: Numeric stress index (0-10 scale)
    
    Returns:
        Category name: minimal, low, moderate, high, extreme
    """
    if stress_value < 2.0:
        return "minimal"
    elif stress_value < 4.0:
        return "low"
    elif stress_value < 6.0:
        return "moderate"
    elif stress_value < 8.0:
        return "high"
    else:
        return "extreme"


def get_stress_interpretation(category: str) -> Dict[str, str]:
    """
    Get interpretation and recommended actions for a stress category.
    
    Args:
        category: Stress category (minimal, low, moderate, high, extreme)
    
    Returns:
        Dictionary with interpretation and recommended actions
    """
    interpretations = {
        "minimal": {
            "meaning": "Water resources are adequate for current demand. Normal operational conditions.",
            "conditions": "Sufficient rainfall, aquifer recharge normal, surface water bodies at healthy levels.",
            "actions": "Continue routine monitoring. Maintain conservation awareness programs.",
            "confidence": "This is a demonstration value. Real water stress requires satellite and ground data."
        },
        "low": {
            "meaning": "Slight pressure on water resources. Early awareness phase.",
            "conditions": "Below-average rainfall or increased demand. Some reduction in water availability.",
            "actions": "Increase monitoring frequency. Prepare conservation messaging. Review contingency plans.",
            "confidence": "This is a demonstration value. Real water stress requires satellite and ground data."
        },
        "moderate": {
            "meaning": "Noticeable water stress. Active management required.",
            "conditions": "Prolonged dry period or significantly increased demand. Reservoirs/aquifers declining.",
            "actions": "Implement voluntary conservation measures. Activate community awareness campaigns. Assess vulnerable populations.",
            "confidence": "This is a demonstration value. Real water stress requires satellite and ground data."
        },
        "high": {
            "meaning": "Significant water scarcity. Intervention necessary.",
            "conditions": "Severe drought conditions or major supply disruption. Critical infrastructure at risk.",
            "actions": "Enforce mandatory restrictions. Deploy emergency water supplies. Prioritize human/livestock needs. Coordinate with regional authorities.",
            "confidence": "This is a demonstration value. Real water stress requires satellite and ground data."
        },
        "extreme": {
            "meaning": "Critical water emergency. Immediate action essential.",
            "conditions": "Catastrophic drought or system failure. Widespread shortages imminent.",
            "actions": "Activate crisis response protocols. Emergency water rationing. Humanitarian assistance coordination. Evacuate vulnerable areas if necessary.",
            "confidence": "This is a demonstration value. Real water stress requires satellite and ground data."
        }
    }
    
    return interpretations.get(category, interpretations["moderate"])


def get_glossary_text() -> str:
    """
    Return full glossary text for UI display.
    
    Returns:
        Markdown-formatted glossary content
    """
    return """
### Water Stress Index — Definition

**Water Stress** measures the imbalance between water supply and demand in a region.

#### What This Index Represents

The Water Stress Index (0-10 scale) integrates:
- **Rainfall patterns**: Deviation from historical norms
- **Surface water availability**: Reservoir and river levels
- **Groundwater status**: Aquifer recharge rates
- **Demand pressure**: Population, agriculture, industrial use
- **Seasonal factors**: Dry season vs wet season dynamics

#### Interpretation Scale

| Score Range | Category | Meaning |
|-------------|----------|---------|
| 0.0 - 2.0 | Minimal | Adequate water resources |
| 2.0 - 4.0 | Low | Slight pressure, early awareness |
| 4.0 - 6.0 | Moderate | Noticeable stress, active management |
| 6.0 - 8.0 | High | Significant scarcity, intervention needed |
| 8.0 - 10.0 | Extreme | Critical emergency, immediate action |

#### Important Limitations

⚠️ **In Demo Mode:**
- Values are **simulated** from statistical models
- They do **NOT** reflect real-time satellite or ground measurements
- Scores are for **demonstration purposes only**

📡 **For Production Use:**
- Requires integration with NASA MODIS, CHIRPS, FEWS NET
- Needs ground-truth calibration from local monitoring stations
- Must be validated by hydrological experts

#### Recommended Actions by Category

**Minimal (0-2):** Routine monitoring, conservation awareness  
**Low (2-4):** Increase monitoring, prepare conservation messaging  
**Moderate (4-6):** Voluntary conservation, community campaigns  
**High (6-8):** Mandatory restrictions, emergency supplies  
**Extreme (8-10):** Crisis protocols, humanitarian coordination

#### Data Sovereignty Note

Water stress assessments have political implications. Always:
- Disclose data sources and methodologies
- Involve local communities in interpretation
- Respect indigenous water knowledge systems
- Coordinate with national/regional authorities before public communication
"""


# Export glossary constants
__all__ = [
    "WATER_STRESS_SCALE",
    "get_stress_category",
    "get_stress_interpretation",
    "get_glossary_text",
]
