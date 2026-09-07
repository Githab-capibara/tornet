# 05. troubleshooting

- **Status:** Accepted
- **Date:** 2026-08-23
- **Deciders:** @ByteBreach
- **Related:** [usage/01-getting-started.md](01-getting-started.md), [mechanisms/14-startup-checks.md](../mechanisms/14-startup-checks.md)

## Context

Common errors need fast resolution paths. Every non-zero exit code carries a
message pointing at the remedy — this document collects them in one place so
operators do not need to read `main()` to diagnose a failure.

## Exit codes

| Code | Meaning | Remedy |
|------|---------|--------|
| 1 | Generic error | Check the error message above |
| 2 | No sudo, not root | Run as root or install sudo |
| 3 | No service manager found | Install `systemd` or `sysvinit-utils` |
| 4 | No package manager found | Install dependencies manually |
| 5–7 | pip/install failures | See `--auto-fix` output; install manually |
| 8 | `python3` not in PATH | Install Python 3.6+ |
| 9 | No internet connectivity | Fix network; check VPN/firewall rules |
| 10 | `tor` not installed | `sudo apt install tor` or run `tornet --auto-fix` |
| 11 | `requests` not importable | `pip install requests requests[socks]` |
| 12 | Bad schedule syntax | Use one of `30s`, `5m`, `2h`, `1d` |
| 13 | Interrupted (standalone checker) | Normal on Ctrl-C |
| 14 | Kill switch needs root | `sudo tornet --kill-switch` |
| 15 | Log file unreadable | Check permissions on `~/.tornet/tornet.log` |

## Permission denied (kill switch)

```bash
sudo tornet --kill-switch
```

The kill switch requires root because it manipulates iptables rules. Running
without sudo exits with code 14.

## Tor not starting

```bash
which tor                          # verify binary is in PATH
sudo systemctl start tor           # systemd
# or
sudo service tor start             # SysV init
```

If Tor refuses to start, check its logs:

```bash
sudo journalctl -u tor --no-pager -n 30
```

## Dependencies missing

```bash
tornet --auto-fix
python3 -c "import requests, socks"   # verify requests[socks] installed
tor --version                         # verify tor binary
```

If `--auto-fix` itself fails, run the steps manually using your distro's
package manager (see [dependency checker mechanism](../mechanisms/05-dependency-checker.md)).

## Connection issues

```bash
curl -s https://api.ipify.org          # direct IP (should NOT be your real IP when Tor is active)
curl --socks5 127.0.0.1:9050 https://api.ipify.org   # through Tor
tornet --dns-leak-test                 # verify DNS routes through Tor
```

If the direct fetch shows your real IP but the SOCKS fetch shows a Tor exit,
your application is leaking DNS — configure your browser or client to use the
SOCKS proxy (see [Firefox setup in README](../../README.md)).

## Stale country pin

```bash
cat ~/.tornet/current_country   # what country is pinned?
cat ~/.tornet/torrc.custom      # the actual torrc snippet
tornet --restore-default        # clear pin and restart stock Tor
```

If `--country de` shows Germany but `--status` reports a different country,
Tor may have failed to apply `StrictNodes`. Check the Tor log for "circuit
construction failed" messages.

## Consequences

- Easier: self-service recovery without reading source code.
- Harder: maintenance of examples across distros.

## References

- [Getting Started](01-getting-started.md)
- [Startup checks mechanism](../mechanisms/14-startup-checks.md)
- [Dependency checker mechanism](../mechanisms/05-dependency-checker.md)
