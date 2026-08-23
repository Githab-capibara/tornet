# 03. Security Policy

- **Status:** Published
- **Date:** 2026-08-23
- **Deciders:** @ByteBreach
- **Related:** [governance/01-contributing.md](01-contributing.md)

## Context

TorNet handles network traffic and requires root for kill switch. Security issues must be reported responsibly to prevent public exposure before fixes.

## Body

### Supported Versions

Only the latest released version is actively supported for security updates.

### Reporting a Vulnerability

Please do NOT open a public issue. Email security disclosures to the maintainer via GitHub Security Advisories.

Include:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix if known

### Response Timeline

- Acknowledgement within 48 hours
- Initial assessment within 7 days
- Fix release as soon as feasible

## Consequences

- Easier: responsible disclosure process.
- Harder: maintainer must triage privately.
- Given up: public discussion of unpatched issues.

## References

- [GitHub Security Advisories](https://docs.github.com/en/code-security)