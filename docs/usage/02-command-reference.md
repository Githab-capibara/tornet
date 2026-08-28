# 02. Command reference

- **Status:** Accepted
- **Date:** 2026-08-23
- **Deciders:** @ByteBreach
- **Related:** [usage/01-getting-started.md](01-getting-started.md), [mechanisms/README.md](../mechanisms/README.md)

## Context

All CLI flags need a single reference. TorNet's `argparse` parser in
`tornet/tornet.py` (`main()`) defines **18 flags**; this document mirrors them
exactly, grouped the same way as the root README (basic vs advanced).

## Body

### Basic commands

| Flag | Type / default | Purpose |
|------|----------------|---------|
| `--ip` | flag | Display current IP address and exit |
| `--change` | flag | Change IP once and exit |
| `--interval` | str, default `60` | Seconds between changes, or a random range like `30-120` |
| `--count` | int, default `10` | Number of changes; `0` = infinite loop |
| `--stop` | flag | Stop all Tor services and tornet processes (`stop_services()`) |
| `--version` | flag | Print version (`2.0.2`) and exit |

### Advanced commands

| Flag | Type / default | Purpose |
|------|----------------|---------|
| `--status` | flag | Show system status panel (`show_status()`) |
| `--country CODE` | str | Pin exit country (`us`, `de`, ...); `auto` = random (default) |
| `--schedule SPEC` | str | Fixed schedule like `30s`, `5m`, `2h`, `1d` |
| `--dns-leak-test` | flag | Test leak-check URLs through the Tor SOCKS proxy |
| `--kill-switch` | flag | Toggle the iptables kill switch (root required) |
| `--log` | flag | Print the log file contents |
| `--follow` | flag | Follow the log file live (use with `--log`) |
| `--json` | flag | Emit machine-readable JSON instead of colored text |
| `--config FILE` | str | Use a custom YAML/JSON config file |
| `--auto-fix` | flag | Install missing dependencies (pip, requests, tor) |
| `--list-countries` | flag | List available exit-country codes |
| `--restore-default` | flag | Remove custom torrc/country files and restart stock Tor |

### Dispatch order

`main()` handles flags in a fixed order and returns after the first match:
`--stop` → `--restore-default` → `--list-countries` → `--status` → `--ip` →
`--change` → `--dns-leak-test` → `--kill-switch` → `--log` → `--schedule` →
`--auto-fix`. Only if none matched does it fall through to the rotation loop
(`--interval` + `--count`), which first verifies tor is installed, `requests`
is importable, and internet is reachable.

### Interval and schedule syntax

- `--interval 60` — exactly 60 seconds between changes.
- `--interval 30-120` — uniformly random seconds per iteration
  (`parse_interval()` → `random.randint(start, end)`).
- `--schedule 5m` — fixed period; unit suffixes: `s`, `m`, `h`, `d`
  (`parse_schedule()` multiplies to seconds).

## Consequences

- **Easier:** every capability discoverable from one table.
- **Harder:** must be kept in sync with `argparse` definitions in `main()`.

## References

- [Getting started](01-getting-started.md)
- [Scheduled rotation mechanism](../mechanisms/11-scheduled-rotation.md)
- [JSON output mechanism](../mechanisms/13-json-output.md)
