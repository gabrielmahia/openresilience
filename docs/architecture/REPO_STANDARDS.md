# OpenResilience Repository Standards

This document defines governance, structure, and quality standards for OpenResilience and future related repositories.

## License Requirements

**Mandatory License:** Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 (CC BY-NC-ND)

### Why This License?
- **NonCommercial**: Prevents extraction/commodification of crisis intelligence
- **NoDerivatives**: Maintains ethical integrity, prevents weaponization or misrepresentation
- **Attribution**: Ensures visibility of source and methodology

### License File Format
```
Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International Public License

Copyright (c) [YEAR] [AUTHOR]

By exercising the Licensed Rights (defined below), You accept and agree to be bound by...
[Standard CC BY-NC-ND text]

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
```

## Trust and Transparency Standards

### Demo Data Disclosure
All repositories using simulated/demo data MUST:

1. **Prominent warning** in README (within first 3 sections)
2. **Badge indicators** showing data status
3. **Per-output labeling** in UI/CLI/API responses
4. **Clear roadmap** to production data integration

❌ **Prohibited:**
- Hidden demo disclaimers
- Misleading forecasts presented as authoritative
- Fake partnerships or institutional endorsements
- Simulated SMS shortcodes presented as live services

### Security Reporting

**SECURITY.md template:**
```markdown
# Security

## Reporting a Vulnerability

If you discover an error:

**DO NOT** open a public issue.

Email directly to:  
[CONTACT_EMAIL]
```

## Repository Structure

### Required Files
```
LICENSE                    # CC BY-NC-ND 4.0
README.md                  # Trust-first disclosure
SECURITY.md                # Vulnerability reporting
CONTRIBUTING.md            # Contribution guidelines
.gitignore                 # Python, data, secrets
pyproject.toml             # Package config (if applicable)
```

### Recommended Structure
```
src/
  [package]/               # Core logic as installable package
    __init__.py
    [modules].py
tests/
  test_*.py                # Smoke tests minimum
data/
  admin/                   # Static geographic/admin data
  demo/                    # Sample datasets
  real/ (gitignored)       # Production data (never committed)
docs/
  architecture/            # Design docs
  DATA_ADAPTERS.md         # Data integration roadmap
app.py                     # Main Streamlit/UI entry point (if applicable)
```

### What NOT to Commit
- Real data with PII
- API keys, credentials, secrets
- Large binary files (>5MB without LFS)
- Proprietary satellite imagery
- Unvetted external datasets

## Code Quality Standards

### Python Style
- **Formatter**: Ruff (or Black)
- **Linter**: Ruff
- **Type hints**: Encouraged for public APIs
- **Docstrings**: Required for modules, classes, public functions
- **Line length**: 100 characters

### Testing Requirements
- **Minimum**: Smoke tests for each module
- **Scope**: `src/`, `tests/`, main app file
- **Microservices**: Optional (may have separate CI)

### CI/CD
Recommended GitHub Actions workflows:
- Linting (Ruff)
- Testing (pytest)
- Security scanning (CodeQL, Dependabot)

## Documentation Standards

### README Template Sections
1. **Status badges** (license, data mode, build status)
2. **Data disclosure warning** (if demo mode)
3. **Overview** (purpose, NOT operational status)
4. **Architecture** (components and their roles)
5. **Quick start** (minimal setup instructions)
6. **Governance alignment** (ethics, privacy, transparency)
7. **Risk disclaimer** (operational use warnings)
8. **License** (explicit terms)

### DATA_ADAPTERS.md
Required if system uses demo data. Must document:
- Current data sources (with "demo/simulated" labeling)
- Planned production integrations (NASA MODIS, CHIRPS, FEWS NET, etc.)
- Data sovereignty considerations
- Validation requirements before operational use

## Ethics and Harm Prevention

### Prohibited Use Cases
- Surveillance or targeting of vulnerable populations
- Commercial exploitation of crisis intelligence
- Circumventing humanitarian coordination structures
- Creating information asymmetries that benefit powerful actors

### Required Disclosures
- Data provenance (source, recency, confidence)
- Model limitations and failure modes
- Uncertainty quantification in forecasts
- Community consent requirements for deployment

## Governance Workflow

### For New Features
1. Open issue describing use case and ethics implications
2. Review against harm scenarios
3. Implement with trust labeling
4. Document in architecture docs
5. Add tests covering trust properties

### For External Collaborators
1. Review LICENSE (NoDerivatives means no direct PRs for redistribution)
2. Collaboration requires email coordination: contact@aikungfu.dev
3. Forks for study/learning are encouraged
4. Suggest improvements via issues

## Version Control

### Branch Naming
- `main` - stable, deployable
- `claude/*` - automated professionalization work
- `feature/*` - new capabilities
- `fix/*` - bug fixes

### Commit Message Format
```
type: short description

- Bullet points for changes
- Include why, not just what
```

Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`

### Merge Policy
- All governance changes require explicit review
- License changes require repository owner approval
- Demo data must never be merged into production paths

## Future Repository Standards

Any new repositories under OpenResilience umbrella must:
1. Adopt CC BY-NC-ND license
2. Follow trust disclosure standards
3. Use src/ package structure
4. Include smoke tests
5. Document ethics implications

## Questions?

Contact: contact@aikungfu.dev
