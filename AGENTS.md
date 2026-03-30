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
