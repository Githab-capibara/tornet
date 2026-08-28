# 01. System overview

- **Status:** Accepted
- **Date:** 2026-08-21
- **Deciders:** @ByteBreach
- **Related:** [mechanisms/01-ip-rotation.md](../mechanisms/01-ip-rotation.md), [adr/02-newnym-via-control-port.md](../adr/02-newnym-via-control-port.md)

## Context

TorNet is a single-process Python CLI with no daemon of its own; it drives an
external `tor` process and speaks to it over local sockets. This document maps
the components and the main data flow so contributors know where a given
behavior lives.

## Components

| Component | File | Responsibility |
|-----------|------|----------------|
| CLI entry point | `tornet/tornet.py` (`main`) | Parse args, dispatch to handlers, set up signal handlers |
| Banner | `tornet/banner.py` | ASCII art header |
| Public API | `tornet/__init__.py` | Re-exports the user-facing functions |
| Standalone checker | `tornet/utils.py` | Pre-install dependency bootstrap, runnable as a module |
| Packager (modern) | `pyproject.toml` | PEP 517 build metadata, declares the `tornet` console script |
| Packager (legacy) | `setup.py` | Fallback install path for old pip/setuptools |
| Tor binary | external | The SOCKS proxy and control port TorNet drives |

## Data flow

```
User CLI ──▶ main() ──▶ initialize_environment()
                            │
                            ├─ service_action("start")  ──▶ tor (systemd/service)
                            │
                   change_ip_repeatedly()
                            │
              ┌─────────────┴──────────────┐
              ▼                            ▼
   rotate_tor_ip()                configure_tor_country()
   (stem NEWNYM on 9051)          (writes torrc.custom)
              │                            │
              └─────────────┬──────────────┘
                            ▼
                   get_current_ip()
                   (socks5 127.0.0.1:9050 ──▶ api.ipify.org)
```

1. `main()` parses flags and routes to a handler (`--ip`, `--change`,
   `--status`, the rotation loop, etc.).
2. For rotation, `initialize_environment()` ensures Tor is running, then
   `change_ip_repeatedly()` loops: sleep → `change_ip()` → print IP.
3. `change_ip()` optionally pins a country via `configure_tor_country()`, then
   asks Tor for a new circuit with `rotate_tor_ip()`, falling back to a service
   reload.
4. The new IP is read back through the SOCKS proxy to confirm the rotation.

## The rotation loop

`change_ip_repeatedly(interval_str, count, country, json_output)`:

- `count == 0` → infinite loop until `KeyboardInterrupt`.
- `count > 0` → exactly `count` iterations.
- `interval_str` is parsed by `parse_interval()` — a fixed number of seconds
  or a `"min-max"` range that is re-rolled each iteration.
- Each iteration prints the IP (human-readable or `--json`).

## Consequences

- TorNet is stateless across runs except for files under `~/.tornet/` (see
  [configuration layout](03-configuration-layout.md)).
- There is no background daemon; a rotation loop only runs while the CLI
  process is alive, and SIGINT tears it down cleanly (see
  [ADR-06](../adr/06-signal-cleanup.md)).
- All network egress for IP checks and DNS-leak tests goes through the Tor
  SOCKS proxy at `127.0.0.1:9050`, never directly, when Tor is running.

## References

- [Tor control port spec](https://gitweb.torproject.org/torspec.git/tree/control-spec.txt) — `NEWNYM` and authentication.
- [stem documentation](https://stem.torproject.org/) — the controller library TorNet uses.
