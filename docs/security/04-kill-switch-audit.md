# 04. Kill Switch Audit

- **Status:** Accepted
- **Date:** 2026-09-10
- **Deciders:** @ByteBreach
- **Researcher:** @Githab-capibara
- **Purpose:** Deep dive into the kill switch attack surface and its verification
- **Feeds into:** [01-threat-model.md](01-threat-model.md), [adr/03-kill-switch-iptables.md](../adr/03-kill-switch-iptables.md)
- **Authors:** @Githab-capibara

## Context

The kill switch is TorNet's highest-consequence feature: a broken
`--kill-switch` either (a) fails to block traffic when the operator believes
they are protected, or (b) blocks all traffic and bricks the operator's
connectivity. It is implemented in `toggle_kill_switch()` with raw iptables
rules and requires root — see [mechanisms/02](../mechanisms/02-kill-switch.md).
This audit enumerates the specific ways the switch can fail and the checks the
code performs.

## Assessment

### Attack surface

| Failure mode | Trigger | Consequence |
|--------------|---------|-------------|
| **iptables absent** | `--kill-switch` on a host without iptables | Exit 13 with clear message; no partial rules |
| **Not root** | `--kill-switch` without elevation | Exit 14; switch refuses to run |
| **Rule-state divergence** | Kill switch toggled by external tooling | `kill_switch_active` flag differs from real iptables rules |
| **Too-broad rule** | Mis-scoped OUTPUT/INPUT policy | Blocks non-Tor traffic the operator expects to keep |
| **Stale state on exit** | Process killed before restore | iptables left in blocked/unblocked state |

### Current mitigations in code

- The switch verifies root via the same privilege check used across the CLI
  (exit 14 pathway documented in [mechanisms/14](../mechanisms/14-startup-checks.md)).
- Missing `iptables` binary is detected before rule mutation (exit 13 —
  see [usage/05-troubleshooting.md](../usage/05-troubleshooting.md#exit-codes--cli-tornet)).
- The iptables rule set is scoped to Tor's ports/socks traffic and
  restore-default is available to reverse the policy
  (see [mechanisms/02](../mechanisms/02-kill-switch.md)).

### Audit findings to verify on every audit

1. Rule set matches the documented scope (no broad DROP on all interfaces
   without documented intent).
2. Exit 13/14 ordering: the binary check and the privilege check run before
   any iptables mutation.
3. `restore_default_tor()` and the kill switch cannot both leave rules behind;
   their interplay is documented in [mechanisms/02](../mechanisms/02-kill-switch.md).
4. No path records operator traffic metadata into the log during switch
   operations beyond the documented event lines.

## Mitigation

- The operator must verify with an explicit traffic test after enabling the
  switch (external IP check through the Tor SOCKS proxy, not via
  `--kill-switch` alone).
- Any change to the kill switch logic must pass the clean-box audit step in
  [03-audit-procedure.md](03-audit-procedure.md) and update both
  [mechanisms/02](../mechanisms/02-kill-switch.md) and
  [adr/03](../adr/03-kill-switch-iptables.md) in the same commit.
- The switch state is re-verified against iptables before trust is declared
  (no cached-flag assumptions).

## References

- [mechanisms/02-kill-switch.md](../mechanisms/02-kill-switch.md)
- [adr/03-kill-switch-iptables.md](../adr/03-kill-switch-iptables.md)
- [01-threat-model.md](01-threat-model.md)
- [03-audit-procedure.md](03-audit-procedure.md)