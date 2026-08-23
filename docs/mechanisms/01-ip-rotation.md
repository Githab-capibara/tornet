# 01. IP Rotation

- **Status:** Published
- **Date:** 2026-08-23
- **Authors:** @ByteBreach
- **Related:** [adr/02-newnym-via-control-port.md](../adr/02-newnym-via-control-port.md)

## Context

Tor exposes NEWNYM signal via control port.

## Mechanism

`rotate_tor_ip()` authenticates to 127.0.0.1:9051 with stem and sends Signal.NEWNYM. Falls back to service reload.

## Implementation details

Uses `stem.control.Controller`. Requires readable control auth cookie.

## Testing

`tornet --change` should show new IP.

## Alternatives considered

- **Restart tor:** rejected for downtime.
