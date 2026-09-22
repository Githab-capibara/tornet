# 01. Threat Model

- **Status:** Accepted
- **Date:** 2026-09-10
- **Deciders:** @ByteBreach
- **Researcher:** @Githab-capibara
- **Purpose:** Define assets, adversaries, and trust boundaries for TorNet
- **Feeds into:** [04-kill-switch-audit.md](04-kill-switch-audit.md), [03-audit-procedure.md](03-audit-procedure.md), [governance/03-security-policy.md](../governance/03-security-policy.md)
- **Authors:** @Githab-capibara

## Context

TorNet is a privileged Tor controller: it manages the Tor daemon, rewrites
`torrc` files, toggles an iptables kill switch, and — when run as root —
executes package-manager commands. Operators rely on it to keep their real IP
hidden. The threat model must therefore cover both classical software
attackers (rooted processes, malicious packages) and the specific privacy
adversary Tor protects against (network observers, exit-node snoopers).

## Assessment

### Assets

| Asset | Description | Impact if compromised |
|-------|-------------|----------------------|
| **Operator IP** | Real source IP hidden behind Tor circuits | Deanonymization |
| **torrc.custom** | Country pin + exit-node policy written to `~/.tornet/` | Circuit pinning bypass, traffic leak |
| **Kill switch state** | iptables rules toggle via `toggle_kill_switch()` | Traffic routed outside Tor |
| **Config file** | `~/.tornet/config.yaml` (API keys, options) | Operator fingerprinting |
| **Log file** | `~/.tornet/tornet.log` — timestamps, exit codes | Behavioral metadata |
| **IP geolocation** | Lookup responses from ip-api.com / ipapi.co | Operator IP disclosure to third party |

### Adversaries

| Adversary | Capability | Target |
|-----------|-----------|--------|
| **Network observer** | Passive monitoring of operator link | Correlation of pre/post-change traffic |
| **Exit-node operator** | Sees decrypted circuit egress (unless TLS) | Content sniffing, IP-to-account mapping |
| **Malicious package** | Compromised pip/distro dependency | Execution in the operator's session |
| **Local attacker** | Access to the operator's user account or `~/.tornet/` | Config/log/custom-torrc tampering |
| **Geolocation API** | ip-api.com / ipapi.co operator | IP/behavioral fingerprinting |

### Trust boundaries

1. **Operator ↔ Tor control port.** 9050/9051 speak the Tor control protocol;
   the control port is the root of circuit-switching trust.
2. **Operator ↔ iptables.** The kill switch blindly trusts the local kernel;
   user-space state (`kill_switch_active`) can diverge from actual rules.
3. **CLI ↔ package manager.** `run_cmd(..., use_sudo=True)` elevates
   commands; a compromised `tor`/pip package inherits root.
4. **CLI ↔ external APIs.** IP geolocation calls run over SOCKS/Tor for
   status; the `--ip` path queries an external HTTP API directly.

## Mitigation

- Geolocation and status endpoints are treated as untrusted input; a failed
  lookup degrades to the raw IP instead of failing the whole command
  (see [mechanisms/15](../mechanisms/15-ip-geolocation.md)).
- The standalone checker (`python -m tornet.utils`) validates the dependency
  chain before the main CLI ever executes privileged paths
  (see [adr/07](../adr/07-cross-distro-checker.md)).
- Kill-switch state is verified against iptables before every toggle
  (see [04-kill-switch-audit.md](04-kill-switch-audit.md)).
- Config and log files live under `~/.tornet/` with operator-owned
  permissions; logs never record the real IP (see
  [mechanisms/09](../mechanisms/09-log-management.md)).

## References

- [governance/03-security-policy.md](../governance/03-security-policy.md)
- [04-kill-switch-audit.md](04-kill-switch-audit.md)
- [03-audit-procedure.md](03-audit-procedure.md)
- [mechanisms/02-kill-switch.md](../mechanisms/02-kill-switch.md)