# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| main    | Yes       |

## Reporting a Vulnerability

**DO NOT** open a public GitHub issue for security vulnerabilities.

Instead, email: **contact@aikungfu.dev**

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact assessment
- Suggested fix (if any)

## Response Timeline

| Action | Timeframe |
|--------|-----------|
| Acknowledgement | 48 hours |
| Initial assessment | 5 business days |
| Fix or mitigation plan | 15 business days |
| Public disclosure (coordinated) | After fix is deployed |

## Scope

The following are in scope:
- API endpoint vulnerabilities (injection, auth bypass, rate-limit bypass)
- Data leakage of personally identifiable information
- Geolocation precision leaks in community reports
- Notification system abuse (subscription spam, message injection)
- Docker/infrastructure misconfigurations in provided compose files

The following are out of scope:
- Vulnerabilities in upstream dependencies (report to the upstream project)
- Denial-of-service against demo/development deployments
- Social engineering attacks

## Responsible Disclosure

We follow coordinated disclosure. We will credit reporters in release notes unless anonymity is requested.
