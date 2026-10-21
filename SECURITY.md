# Security Policy

## Supported versions

The project currently supports the latest `main` branch and the most recent published release on PyPI.

| Version | Supported |
| --- | --- |
| Latest release | Yes |
| `main` branch | Yes |
| Older releases | Security fixes are evaluated case by case |

## Reporting a vulnerability

Please do not open a public GitHub issue for a security vulnerability.

Instead, use GitHub's private vulnerability reporting flow:

1. Open the repository on GitHub.
2. Go to the Security tab.
3. Click "Report a vulnerability".
4. Submit the issue privately so the maintainers can investigate before public disclosure.

If private reporting is not available in the repository settings, contact the maintainer through the GitHub profile linked to this project and request a secure channel for the report.

Please include:

- affected version or branch
- reproduction steps or proof of concept
- affected files or package names
- business or security impact
- suggested remediation or patch, if known

## Response expectations

We aim to acknowledge valid reports within 5 business days and to coordinate a fix and responsible disclosure timeline with the reporter.

## Disclosure policy

Once a fix is prepared and validated, we will:

- publish a release with the security fix
- document the affected versions and fixed versions
- disclose the issue in a GitHub Security Advisory when appropriate
- coordinate with relevant ecosystems and vulnerability databases, including CVE assignment through the appropriate GitHub/CNA process when the issue meets the required criteria

## Security automation

This repository enables automated dependency monitoring and static security analysis through:

- GitHub Dependabot for Python and GitHub Actions updates
- GitHub CodeQL analysis for the Python codebase
- private vulnerability reporting in the GitHub Security tab

This helps keep the project aligned with secure development practices and supports responsible disclosure and advisory creation when a real vulnerability is confirmed.
