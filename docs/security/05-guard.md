# 05. Guard

- **Status:** Accepted
- **Date:** 2026-09-10
- **Deciders:** @ByteBreach
- **Researcher:** @Githab-capibara
- **Purpose:** Automated security guardrails: CI checks, SAST, dependency scanning
- **Feeds into:** [03-audit-procedure.md](03-audit-procedure.md), [pipeline/02](../pipeline/02-ci-gate-and-quality-tiers.md)
- **Authors:** @Githab-capibara

## Context

Manual review alone misses regressions that reappear after refactors —
especially the privilege split re-introduced in
[mechanisms/04](../mechanisms/04-auto-fix.md) and the exit-code contract in
[usage/05](../usage/05-troubleshooting.md). Guardrails make the audit
procedure ([03-audit-procedure.md](03-audit-procedure.md)) executable without
a human eyeballing every diff. This document defines which automated checks
exist today and which the project treats as mandatory before merge.

## Assessment

### Existing guardrails

| Guardrail | Scope | Where it runs |
|-----------|-------|---------------|
| **Docs build gate** | `docs/` Sphinx build via `readthedocs.yaml` | ReadTheDocs on push |
| **Exit-code contract** | `usage/05` table vs code | Every security audit |
| **Standalone checker** | `tornet/utils.py` dependency-chain validation | Audit + clean-box steps |
| **Mechanism coverage map** | Every function mapped to a mechanism doc | Review gate |

### Recommended mandatory checks (run locally per audit)

1. **SAST rule pass over `tornet/`** — flag `subprocess`/`os.system` sites,
   `eval`/`exec` usage, and unquoted shell interpolation; each finding is
   triaged against [01-threat-model.md](01-threat-model.md).
2. **Dependency scan** — check the pinned dependency set
   (`requests`, `PyYAML`, `schedule`, `stem`) against known advisories before
   tagging a release.
3. **Secrets scan** — confirm no private key material or API tokens land in
   the tree (`.gitignore` covers `build/`, `*.egg-info`).
4. **Privilege allow-list check** — assert that only `install_package` sites
   call `run_cmd(..., use_sudo=True)` and pip paths stay user-level
   (see [mechanisms/04](../mechanisms/04-auto-fix.md)).

## Mitigation

- Guardrails 1–4 are run as part of every audit procedure pass
  ([03-audit-procedure.md](03-audit-procedure.md)) and recorded with the
  findings.
- Any guardrail that fails blocks merge for that change; a passed run is a
  precondition for the L/XL quality tier
  ([pipeline/02](../pipeline/02-ci-gate-and-quality-tiers.md)).
- Results feed the advisory flow ([02-responsible-disclosure.md](02-responsible-disclosure.md))
  when they surface a live vulnerability.

## References

- [03-audit-procedure.md](03-audit-procedure.md)
- [01-threat-model.md](01-threat-model.md)
- [pipeline/02-ci-gate-and-quality-tiers.md](../pipeline/02-ci-gate-and-quality-tiers.md)
- [mechanisms/04-auto-fix.md](../mechanisms/04-auto-fix.md)