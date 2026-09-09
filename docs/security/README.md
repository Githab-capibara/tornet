# Security

This directory contains **security-oriented documentation** for TorNet — threat models, disclosure policies, audit procedures, and defensive design decisions.

## Directory map

| File | Purpose |
|------|---------|
| [01-threat-model.md](01-threat-model.md) | Assets, adversaries, and trust boundaries for TorNet |
| [02-responsible-disclosure.md](02-responsible-disclosure.md) | How to report and triage security vulnerabilities |
| [03-audit-procedure.md](03-audit-procedure.md) | Step-by-step security audit checklist for contributors |
| [04-kill-switch-audit.md](04-kill-switch-audit.md) | Deep dive into kill switch attack surface and verification |
| [05-guard.md](05-guard.md) | Automated security guardrails: CI checks, SAST, dependency scanning |

Use [`template.md`](template.md) as the starting point for a new security document.