def confidence_from_inputs(missing_pct, freshness_min, cadence_min):
    if missing_pct >= 10.0:
        return 'low'
    if freshness_min <= cadence_min:
        return 'high'
    if freshness_min <= cadence_min * 2:
        return 'medium'
    return 'low'
