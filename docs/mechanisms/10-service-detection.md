# 10. Service Detection

- **Status:** Published
- **Date:** 2026-08-23
- **Authors:** @ByteBreach
- **Related:** [architecture/02-tor-integration.md](../architecture/02-tor-integration.md)

## Context

Start/stop Tor via systemd or service.

## Mechanism

`detect_service_manager` checks for systemctl or service, `service_action` runs start/stop/reload.

## Implementation details

Runs with sudo.

## Testing

`tornet --status` shows running.

## Alternatives considered

- **Hardcode systemctl:** less portable.
