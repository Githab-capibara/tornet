# 03. Audit Procedure

- **Status:** Accepted
- **Date:** 2026-09-10
- **Deciders:** @ByteBreach
- **Researcher:** @Githab-capibara
- **Purpose:** Step-by-step security audit checklist for contributors and reviewers
- **Feeds into:** [04-kill-switch-audit.md](04-kill-switch-audit.md), [05-guard.md](05-guard.md)
- **Authors:** @Githab-capibara

## Context

A security audit must be repeatable. Without a checklist, audits degrade into
"read the diff and hope", which misses the classes of bugs TorNet is prone to:
privilege escalation via `run_cmd`, iptables state divergence, and unvalidated
external-input written into `torrc`. This procedure gives every reviewer the
same concrete steps, tied to the actual code locations documented in
`docs/mechanisms/`.

## Assessment

Audit focus areas, mapped to code and docs:

| Area | Code entry point | Doc anchor |
|------|------------------|------------|
| Privileged command execution | `run_cmd`, `install_package` | [mechanisms/14](../mechanisms/14-startup-checks.md) |
| Kill switch consistency | `toggle_kill_switch` | [mechanisms/02](../mechanisms/02-kill-switch.md) |
| Tor control-port safety | `rotate_tor_ip`, `configure_tor_country` | [mechanisms/01](../mechanisms/01-ip-rotation.md), [mechanisms/06](../mechanisms/06-country-exitnodes.md) |
| Config/API-key handling | `load_config` | [mechanisms/07](../mechanisms/07-config-management.md) |
| Log/secret hygiene | `log`, `follow_logs` | [mechanisms/09](../mechanisms/09-log-management.md) |
| External-input trust | `--country`, `--ip`, JSON output | [mechanisms/15](../mechanisms/15-ip-geolocation.md) |
| Dependency chain | `tornet/utils.py` | [mechanisms/05](../mechanisms/05-dependency-checker.md) |

## Mitigation

Run the checklist in order:

1. **Diff review.** Every change is read with the corresponding mechanism doc
   open; any doc/code mismatch is a finding (see
   [pipeline/02](../pipeline/02-ci-gate-and-quality-tiers.md)).
2. **Privilege review.** Confirm every `run_cmd(..., use_sudo=True)` site is
   on the allow-list of system installs and that pip/user-level installs stay
   unprivileged (see [mechanisms/04](../mechanisms/04-auto-fix.md)).
3. **Input review.** Confirm `--country`, `--schedule`, and `--interval` are
   constrained to the shapes the code asserts; document any place where an
   arbitrary string reaches a config file.
4. **State review.** Verify kill-switch state is re-read from iptables, not
   assumed from a cached flag (see [04-kill-switch-audit.md](04-kill-switch-audit.md)).
5. **Secret hygiene.** Confirm logs never contain the real IP or API keys.
6. **Dependency review.** Run the standalone checker
   (`python -m tornet.utils`) and eyeball `pip`/distro resolution
   (see [mechanisms/05](../mechanisms/05-dependency-checker.md)).
7. **Clean-box run.** On a fresh container, exercise `--change`, `--kill-switch`,
   `--status`, `--auto-fix` and confirm exit codes match
   [usage/05](../usage/05-troubleshooting.md).
8. **Report.** Findings are recorded in the security directory as filed
   assessments or referenced from the advisory flow
   ([02-responsible-disclosure.md](02-responsible-disclosure.md)).

## References

- [01-threat-model.md](01-threat-model.md)
- [04-kill-switch-audit.md](04-kill-switch-audit.md)
- [05-guard.md](05-guard.md)
- [usage/05-troubleshooting.md](../usage/05-troubleshooting.md)