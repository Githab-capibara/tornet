# 03. Country Selection

- **Status:** Published
- **Date:** 2026-08-23
- **Authors:** @ByteBreach
- **Related:** [architecture/02-tor-integration.md](../architecture/02-tor-integration.md)

## Context

Users want specific exit countries.

## Body

Use `--country US` to pin exit nodes.

List available:

```bash
tornet --list-countries
```

Tor configuration is written to `~/.tornet/torrc.custom` with `ExitNodes {CC} StrictNodes 1`.

## Consequences

- Easier: geo-specific routing.
- Harder: some countries unreliable.

## References

- [Tor Integration](architecture/02-tor-integration.md)
