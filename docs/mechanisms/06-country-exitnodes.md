# 06. Country Exit Nodes

- **Status:** Published
- **Date:** 2026-08-23
- **Authors:** @ByteBreach
- **Related:** [usage/03-country-selection.md](../usage/03-country-selection.md)

## Context

Pin exit country.

## Mechanism

`configure_tor_country` writes `ExitNodes {CC} StrictNodes 1` to `~/.tornet/torrc.custom`, restarts tor.

## Implementation details

Service action stop/start.

## Testing

IP geolocation matches country.

## Alternatives considered

- **Control port config:** not supported.
