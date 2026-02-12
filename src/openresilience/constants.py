"""Geographic and demographic constants for all 47 Kenyan counties
and special focus areas."""

KENYA_COUNTIES = {
    # Former Central Province
    "Kiambu": {"lat": -1.1719, "lon": 36.8356, "pop": 2417735, "arid": False},
    "Kirinyaga": {"lat": -0.6599, "lon": 37.3828, "pop": 610411, "arid": False},
    "Murang'a": {"lat": -0.7833, "lon": 37.1500, "pop": 1056640, "arid": False},
    "Nyeri": {"lat": -0.4197, "lon": 36.9475, "pop": 759164, "arid": False},
    "Nyandarua": {"lat": -0.1833, "lon": 36.4667, "pop": 638289, "arid": False},

    # Former Coast Province
    "Mombasa": {"lat": -4.0435, "lon": 39.6682, "pop": 1208333, "arid": False},
    "Kwale": {"lat": -4.1833, "lon": 39.4500, "pop": 866820, "arid": False},
    "Kilifi": {"lat": -3.6309, "lon": 39.8494, "pop": 1453787, "arid": False},
    "Tana River": {"lat": -1.5167, "lon": 39.9833, "pop": 315943, "arid": True},
    "Lamu": {"lat": -2.2717, "lon": 40.9020, "pop": 143920, "arid": False},
    "Taita Taveta": {"lat": -3.3167, "lon": 38.3500, "pop": 340671, "arid": True},

    # Former Eastern Province
    "Marsabit": {"lat": 2.3284, "lon": 37.9891, "pop": 459785, "arid": True},
    "Isiolo": {"lat": 0.3556, "lon": 37.5817, "pop": 268002, "arid": True},
    "Meru": {"lat": 0.3556, "lon": 37.6500, "pop": 1545714, "arid": False},
    "Tharaka Nithi": {"lat": -0.2833, "lon": 37.7667, "pop": 393177, "arid": False},
    "Embu": {"lat": -0.5392, "lon": 37.4572, "pop": 608599, "arid": False},
    "Kitui": {"lat": -1.3667, "lon": 38.0167, "pop": 1136187, "arid": True},
    "Machakos": {"lat": -1.5177, "lon": 37.2634, "pop": 1421932, "arid": True},
    "Makueni": {"lat": -2.2667, "lon": 37.8333, "pop": 987653, "arid": True},

    # Nairobi (Capital)
    "Nairobi": {"lat": -1.2921, "lon": 36.8219, "pop": 4397073, "arid": False},

    # Former North Eastern Province (ASAL - Arid & Semi-Arid Lands)
    "Garissa": {"lat": -0.4569, "lon": 39.6580, "pop": 841353, "arid": True},
    "Wajir": {"lat": 1.7500, "lon": 40.0667, "pop": 781263, "arid": True},
    "Mandera": {"lat": 3.9167, "lon": 41.8500, "pop": 1025756, "arid": True},

    # Former Nyanza Province
    "Siaya": {"lat": -0.0636, "lon": 34.2864, "pop": 993183, "arid": False},
    "Kisumu": {"lat": -0.0917, "lon": 34.7680, "pop": 1155574, "arid": False},
    "Homa Bay": {"lat": -0.5167, "lon": 34.4667, "pop": 1131950, "arid": False},
    "Migori": {"lat": -1.0634, "lon": 34.4731, "pop": 1116436, "arid": False},
    "Kisii": {"lat": -0.6817, "lon": 34.7680, "pop": 1266860, "arid": False},
    "Nyamira": {"lat": -0.5667, "lon": 34.9333, "pop": 605576, "arid": False},

    # Former Rift Valley Province
    "Turkana": {"lat": 3.1167, "lon": 35.6000, "pop": 1016867, "arid": True},
    "West Pokot": {"lat": 1.6215, "lon": 35.1121, "pop": 621241, "arid": True},
    "Samburu": {"lat": 1.2167, "lon": 36.9000, "pop": 310327, "arid": True},
    "Trans Nzoia": {"lat": 1.0500, "lon": 34.9500, "pop": 990341, "arid": False},
    "Uasin Gishu": {"lat": 0.5500, "lon": 35.3000, "pop": 1163186, "arid": False},
    "Elgeyo Marakwet": {"lat": 0.8500, "lon": 35.4500, "pop": 454480, "arid": False},
    "Nandi": {"lat": 0.1833, "lon": 35.1167, "pop": 885711, "arid": False},
    "Baringo": {"lat": 0.8500, "lon": 35.9667, "pop": 666763, "arid": True},
    "Laikipia": {"lat": 0.3667, "lon": 36.7833, "pop": 518560, "arid": True},
    "Nakuru": {"lat": -0.3031, "lon": 36.0800, "pop": 2162202, "arid": False},
    "Narok": {"lat": -1.0833, "lon": 35.8667, "pop": 1157873, "arid": True},
    "Kajiado": {"lat": -2.0978, "lon": 36.7820, "pop": 1117840, "arid": True},
    "Kericho": {"lat": -0.3681, "lon": 35.2839, "pop": 901777, "arid": False},
    "Bomet": {"lat": -0.8000, "lon": 35.3333, "pop": 875689, "arid": False},

    # Former Western Province
    "Kakamega": {"lat": 0.2827, "lon": 34.7519, "pop": 1867579, "arid": False},
    "Vihiga": {"lat": 0.0667, "lon": 34.7167, "pop": 590013, "arid": False},
    "Bungoma": {"lat": 0.5667, "lon": 34.5667, "pop": 1670570, "arid": False},
    "Busia": {"lat": 0.4604, "lon": 34.1115, "pop": 893681, "arid": False},
}

SPECIAL_AREAS = {
    "Makongeni (Thika)": {
        "lat": -1.0332, "lon": 37.0893,
        "type": "Informal Settlement",
        "county": "Kiambu",
        "challenges": ["Unreliable piped water", "Expensive water kiosks", "No rainwater harvesting"],
        "population": 15000,
    },
    "Thika Landless": {
        "lat": -1.0419, "lon": 37.0977,
        "type": "Landless Community",
        "county": "Kiambu",
        "challenges": ["No land for wells", "Dependent on vendors", "High water costs"],
        "population": 8000,
    },
    "Githurai 45": {
        "lat": -1.1524, "lon": 36.9108,
        "type": "Informal Settlement",
        "county": "Kiambu",
        "challenges": ["Water rationing", "Contamination risks", "Distance to sources"],
        "population": 30000,
    },
    "Mathare": {
        "lat": -1.2601, "lon": 36.8589,
        "type": "Informal Settlement",
        "county": "Nairobi",
        "challenges": ["Illegal connections", "Water theft", "Quality issues"],
        "population": 200000,
    },
}
