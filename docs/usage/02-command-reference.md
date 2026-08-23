# 02. Command Reference

- **Status:** Published
- **Date:** 2026-08-23
- **Deciders:** @ByteBreach
- **Related:** [usage/01-getting-started.md](01-getting-started.md)

## Context

All CLI flags need a single reference.

## Body

| Flag | Purpose |
|------|---------|
| `--ip` | Display current IP |
| `--change` | Change IP once |
| `--interval` | Seconds between changes |
| `--count` | Number of changes, 0 = infinite |
| `--country` | Pin exit country |
| `--kill-switch` | Toggle kill switch |
| `--auto-fix` | Install missing dependencies |
| `--status` | Show status |
| `--dns-leak-test` | Test DNS leaks |
| `--log` | Show logs |

## Consequences

- Easier: discoverability.
- Harder: keep in sync with code.

## References

- [Getting Started](01-getting-started.md)
