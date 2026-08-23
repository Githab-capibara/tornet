# 09. Log Management

- **Status:** Published
- **Date:** 2026-08-23
- **Authors:** @ByteBreach
- **Related:** [usage/02-command-reference.md](../usage/02-command-reference.md)

## Context

Users need visibility.

## Mechanism

`follow_logs` reads `~/.tornet/tornet.log`, supports follow mode.

## Implementation details

Creates log dir if missing.

## Testing

`tornet --log --follow` streams.

## Alternatives considered

- **stdout only:** no persistence.
