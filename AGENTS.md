# AGENTS.md — WapiMaji

This file gives AI coding agents (Cursor, GitHub Copilot, Claude Code, Devin, etc.)
the context needed to work reliably in this repository.

## What this is

Water stress and drought monitoring. Data: NDMA. SMS alerts via Africa's Talking.

**Live app:** https://openresilience.streamlit.app  
**Portfolio:** https://gabrielmahia.github.io

## Structure

```
app.py              ← Main entry point (Streamlit)
pages/              ← Multi-page app sections (if present)
services/           ← Shared services (data loading, APIs)
data/               ← Seed CSV data files
.streamlit/
  config.toml       ← Theme and toolbar config
requirements.txt    ← Python dependencies
```

## Running locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Critical rules — do not change without understanding

1. **CSS dark mode**: Every custom HTML class has both `@media (prefers-color-scheme: dark)`
   AND `[data-theme="dark"]` selectors. Removing either breaks Streamlit's theme toggle.

2. **Feedback sidebar**: The sidebar contains a Google Form link and GitHub issues link.
   Do not remove — it's the only feedback channel.

3. **Data disclosures**: Apps with partial or demo data have visible `st.info`/`st.warning`
   banners. Do not remove — required for trust integrity.

4. **CITATION.cff**: Attribution and license metadata for scrapers. Do not modify.

## Mobile-first

All UI is designed mobile-first. Any new elements must:
- Use `min-height: 44px` for tap targets
- Use `font-size: 16px` minimum for body text
- Work on 3G (no heavy assets, lazy-load where possible)

## License

Apache 2.0 (civic tools) or CC-BY-NC-ND-4.0 (see LICENSE file).  
Contact: contact@aikungfu.dev

<!-- coverage-adaptive-reasoning:v2 -->

## Coverage-Adaptive Reasoning v2

For consequential research, recommendations, investigations, analogy searches, forecasting, opportunity discovery, and canon building:

- A correct ranking inside an incomplete universe is still a failed answer.
- Separate candidate generation from candidate ranking.
- Materiality-gate the search: use the minimum useful set of orthogonal retrieval routes that could change the answer.
- Before closure ask what correct answer the current search method would be structurally incapable of finding.
- Treat aliases, language/geography, era, source class, format, genealogy, taxonomy, legal identity vs operational control/economic benefit, intermediaries, schema categories, null/failure cases, and negative space as potential blind spots when material.
- Maintain leading + competing + null explanations.
- Distinguish answer confidence from coverage confidence.
- “Nothing found” is not evidence of absence when coverage is low.
- Stop when additional independent search routes no longer materially change the candidate universe, hypotheses, decision, or next test.
- When an important miss occurs, repair the retrieval architecture via MISS → SENSOR REDESIGN; do not merely append the missed example.

<!-- v2 section appended 2026-10-28 from https://github.com/gabrielmahia/nairobi-stack/blob/main/docs/COVERAGE_ADAPTIVE_REASONING.md; the rest of this file is unchanged. -->
