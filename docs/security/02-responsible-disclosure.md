# 02. Responsible Disclosure

- **Status:** Accepted
- **Date:** 2026-09-10
- **Deciders:** @ByteBreach
- **Researcher:** @Githab-capibara
- **Purpose:** Define how security vulnerabilities are reported and triaged
- **Feeds into:** [governance/03-security-policy.md](../governance/03-security-policy.md)
- **Authors:** @Githab-capibara

## Context

TorNet is exposed to two classes of reporters: privacy researchers who sit
behind Tor and operators who discovered a leak in their own traffic. Both need
a private, auditable channel; public issue reports of a live vulnerability
would weaponize unpatched bugs. The governance policy
([governance/03-security-policy.md](../governance/03-security-policy.md))
already commits to GitHub Security Advisories — this document turns that
commitment into a runnable procedure.

## Assessment

The reporting surface includes:

1. **GitHub Security Advisories** — the sanctioned private channel.
2. **Public issues** — must be redirected to the advisory flow if they carry
   exploit detail.
3. **Direct contact with the maintainer** — accepted for reporters who cannot
   open a draft advisory, but the advisory is still created for the audit
   trail.

Risk to avoid: a vuln reported publicly before the advisory exists → hostile
parties learn the attack before a fix ships.

## Mitigation

### Reporter path

1. Reporter opens a **draft GitHub Security Advisory** (private by default)
   with the vulnerable command, environment, and impact.
2. Alternatively, opens a public issue with **no exploit detail** and asks for
   a private channel; maintainer moves the conversation to an advisory.

### Maintainer path

1. **Acknowledge within 48 hours** of the advisory being filed.
2. Triage against the threat model ([01-threat-model.md](01-threat-model.md)):
   classify as S/M/L/XL blast radius per
   [pipeline/02](../pipeline/02-ci-gate-and-quality-tiers.md).
3. Fix in a private branch; document the change in the relevant mechanism doc
   and ADR before merge.
4. **Coordination window:** publish the fix before public disclosure; the
   advisory credits the reporter and records the timeline.
5. After the fix ships, the advisory is made public with the PR reference.

### Non-negotiable rules

- No public disclosure before the fix branch exists.
- No commit message references CVE/advisory before publication.
- Reporter identity is shared only with their consent.

## References

- [governance/03-security-policy.md](../governance/03-security-policy.md)
- [01-threat-model.md](01-threat-model.md)
- [03-audit-procedure.md](03-audit-procedure.md)