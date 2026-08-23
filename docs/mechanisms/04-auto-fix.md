# 04. Auto Fix

- **Status:** Published
- **Date:** 2026-08-23
- **Authors:** @ByteBreach
- **Related:** [adr/04-runtime-auto-fix.md](../adr/04-runtime-auto-fix.md)

## Context

Users miss dependencies.

## Mechanism

`tornet --auto-fix` runs `ensure_pip`, `ensure_requests`, `ensure_tor`.

## Implementation details

Detects package manager, runs install commands with sudo.

## Testing

Run on clean box.

## Alternatives considered

- **Auto-install silently:** rejected security.
