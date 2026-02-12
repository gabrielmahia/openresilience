"""Advisory logic — generates community-facing guidance based on stress and forecast data."""

from datetime import datetime


def get_community_advice(stress, forecast, county, is_asal, population):
    """Generate hyperlocal, actionable advice.

    Returns a dict with keys: immediate, water_mgmt, agriculture,
    livestock, resources, timeline.
    """
    advice = {
        "immediate": [],
        "water_mgmt": [],
        "agriculture": [],
        "livestock": [],
        "resources": [],
        "timeline": [],
    }

    # IMMEDIATE ACTIONS
    if stress > 0.80:
        advice["immediate"] = [
            "🚨 **CRITICAL**: Water emergency likely within 2-4 weeks",
            "🚰 Install emergency rainwater tanks IMMEDIATELY (200-1000L)",
            "📞 Contact county water office for emergency bowser requests",
            "💰 Budget 300-500 KES/day for water purchases",
            "👥 Form or join community water-sharing arrangements NOW",
        ]
    elif stress > 0.60:
        advice["immediate"] = [
            "⚠️ **HIGH RISK**: Water shortages likely within 1-2 months",
            "🪣 Stock up water containers (20L jerricans)",
            "🔧 Fix all leaking taps and pipes immediately",
            "💡 Prepare for water rationing by county government",
        ]
    else:
        advice["immediate"] = [
            "✅ Current conditions: Manageable",
            "🏗️ Use this time to improve water infrastructure",
            "📊 Monitor your household water usage patterns",
        ]

    # WATER MANAGEMENT
    if stress > 0.70:
        advice["water_mgmt"] = [
            "**Rainwater Harvesting** (Priority #1):",
            "  • 30m² roof → 300L per rain event (estimate)",
            "  • ROI: Pays back in 6-12 months vs buying water",
            "  • Contact: Kenya Rainwater Association (0722 123 456)",
            "",
            "**Household Conservation** (Save 30-50%):",
            "  • Bucket bathing: 15L vs 60L shower",
            "  • Washing water → toilet flushing → garden",
            "  • Fix dripping tap = save 20L/day = 600L/month",
            "",
            "**Community Actions**:",
            "  • Organize neighborhood water committee",
            "  • Bulk purchase water to reduce costs",
            "  • Map all nearby water sources (boreholes, rivers)",
        ]
    else:
        advice["water_mgmt"] = [
            "💧 Maintain current conservation practices",
            "🌧️ Install rainwater system BEFORE crisis (cheaper now)",
            "📱 Join county water WhatsApp group for updates",
        ]

    # AGRICULTURAL GUIDANCE
    month = datetime.now().month
    if 1 <= month <= 3:
        if forecast["trend"] == "worsening":
            advice["agriculture"] = [
                "🌾 **LONG RAINS PLANTING** (March-April):",
                "⚠️ HIGH RISK SEASON - Plant cautiously",
                "",
                "**Recommended crops** (drought-tolerant):",
                "  • Green grams (60-90 days) - BEST CHOICE",
                "  • Cowpeas (60-70 days)",
                "  • Cassava (8-12 months, very drought-resistant)",
                "  • Sorghum (3-4 months, survives dry spells)",
                "",
                "**AVOID** (high water needs):",
                "  • ❌ Normal maize varieties",
                "  • ❌ Traditional beans",
                "  • ❌ Potatoes",
                "",
                "**Risk Mitigation**:",
                "  • Plant 50% of usual area",
                "  • Wait until rains CONFIRMED (3+ rainy days)",
                "  • Keep seed for replanting if crops fail",
            ]
        else:
            advice["agriculture"] = [
                "🌽 **LONG RAINS PLANTING** (March-April):",
                "✅ Good season predicted",
                "",
                "**Recommended crops**:",
                "  • Maize + beans intercrop (traditional)",
                "  • Irish potatoes (highland areas)",
                "  • Vegetables (kale, spinach, tomatoes)",
                "",
                "**Maximize success**:",
                "  • Prepare land early (conserve early rains)",
                "  • Use hybrid seeds for better drought tolerance",
                "  • Apply manure before planting",
            ]
    elif 8 <= month <= 10:
        advice["agriculture"] = [
            "🌾 **SHORT RAINS PLANTING** (October-November):",
            "Plan now, plant in October",
            "",
            f"**Risk level**: {'HIGH' if forecast['trend'] == 'worsening' else 'MODERATE'}",
            "**Best crops**: Green grams, cowpeas, quick-maturing vegetables",
        ]
    else:
        advice["agriculture"] = [
            "📅 Not planting season",
            "🌱 Prepare: Buy quality seeds now (cheaper off-season)",
            "🚜 Maintain farm equipment",
            "📚 Attend farmer training programs",
        ]

    # LIVESTOCK MANAGEMENT (ASAL counties)
    if is_asal:
        if stress > 0.75:
            advice["livestock"] = [
                "🐄 **URGENT LIVESTOCK DECISIONS**:",
                "⚠️ Grazing will be insufficient",
                "",
                "**Immediate actions**:",
                "  • Destocking: Sell weak/old animals NOW (before prices crash)",
                "  • Move herds to wetter areas if possible",
                "  • Budget for commercial feeds (expensive!)",
                "  • Water livestock every 2-3 days (reduce trips)",
                "",
                "**Survival priorities**:",
                "  1. Keep breeding females",
                "  2. Keep young healthy stock",
                "  3. Sell old males and weak animals",
                "",
                "📞 **Contact**: County Livestock Office for market info",
            ]
        else:
            advice["livestock"] = [
                "🐐 Grazing conditions: Adequate",
                "💉 Good time for vaccinations and treatments",
                "🌾 Consider growing fodder crops (Napier grass)",
            ]

    # RESOURCES & CONTACTS
    advice["resources"] = [
        "**Emergency Contacts:**",
        f"  • {county} Water Office: [Call county HQ]",
        "  • National Drought Hotline: 0800 720 720",
        "  • Kenya Red Cross: 1199 (toll-free)",
        "  • Ministry of Agriculture: 0800 221 0071",
        "",
        "**SMS Services** (Planned — not yet active):",
        "  • Send 'MAJI' to 22555 → Water alerts (coming soon)",
        "  • Send 'KILIMO' to 30606 → Farm advice (coming soon)",
        "",
        "**Water Vendors** (if needed):",
        "  • Check county-approved vendor list",
        "  • Typical cost: 50-100 KES per 20L jerrican",
        "  • Bowser delivery: 2000-5000 KES per 10,000L",
    ]

    # TIMELINE
    if forecast["trend"] == "worsening":
        advice["timeline"] = [
            "📅 **NEXT 3 MONTHS**: Stress increasing",
            "  • Week 1-2: Implement water conservation",
            "  • Week 3-4: Install rainwater tanks",
            "  • Month 2-3: Expect rationing/shortages",
            "",
            "📅 **MONTHS 4-6**: Critical period",
            "  • Peak stress expected",
            "  • Possible county water emergency declared",
            "  • Rely on stored water + purchases",
            "",
            "📅 **MONTHS 7-12**: Recovery depends on rains",
            f"  • {forecast['season_note']}",
            "  • Gradual improvement if rains arrive",
        ]
    else:
        advice["timeline"] = [
            "📅 **NEXT 3 MONTHS**: Improving conditions",
            f"  • {forecast['season_note']}",
            "  • Good time to invest in infrastructure",
            "",
            "📅 **MONTHS 4-12**: Stable/manageable",
            "  • Normal water availability expected",
            "  • Focus on preparedness for next dry spell",
        ]

    return advice
