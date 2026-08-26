# Mechanisms

This directory contains **deep dives** into TorNet runtime mechanisms — how each feature works under the hood.

## Contents

| Guide | Purpose |
|-------|---------|
| [01-ip-rotation.md](01-ip-rotation.md) | Tor control port IP rotation mechanism |
| [02-kill-switch.md](02-kill-switch.md) | iptables kill switch implementation |
| [03-signal-handling.md](03-signal-handling.md) | Process cleanup on signals |
| [04-auto-fix.md](04-auto-fix.md) | Runtime dependency auto-install |
| [05-dependency-checker.md](05-dependency-checker.md) | Cross-distro package manager detection |
| [06-country-exitnodes.md](06-country-exitnodes.md) | Exit country pinning via torrc |
| [07-config-management.md](07-config-management.md) | YAML/JSON config load/save |
| [08-dns-leak-test.md](08-dns-leak-test.md) | DNS leak testing via Tor SOCKS |
| [09-log-management.md](09-log-management.md) | Log file follow and display |
| [10-service-detection.md](10-service-detection.md) | Tor service start/stop detection |
| [11-scheduled-rotation.md](11-scheduled-rotation.md) | Fixed-period scheduling (`30s`/`5m`/`2h`/`1d`) |
| [12-status-monitoring.md](12-status-monitoring.md) | `--status` panel probes and fields |
| [13-json-output.md](13-json-output.md) | `--json` machine-readable output contracts |
| [14-startup-checks.md](14-startup-checks.md) | Gate sequence, exit codes, and privilege model |

Use [`template.md`](template.md) as the starting point for a new mechanism document.
