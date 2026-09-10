# 03. Security Policy

- **Status:** Accepted
- **Date:** 2026-08-23
- **Deciders:** @ByteBreach
- **Related:** [governance/01-contributing.md](01-contributing.md)
- **Authors:** @Githab-capibara

## Context

TorNet handles network traffic and requires root for kill switch. Security issues must be reported responsibly to prevent public exposure before fixes.

## Decision

Use GitHub Security Advisories for responsible disclosure, with a 48-hour acknowledgement window and private triage before public disclosure.

## Consequences

- **Easier:** responsible disclosure process with clear timeline.
- **Harder:** maintainer must triage privately and coordinate fixes.
- **Given up:** public discussion of unpatched issues.
- **Migration:** none; this is the initial policy.

## Alternatives considered

- **Option A: public issues for security bugs.** Rejected because it exposes vulnerabilities before fixes are available.
- **Option B: email-only disclosure.** Rejected because GitHub Security Advisories provide better tooling and audit trail.