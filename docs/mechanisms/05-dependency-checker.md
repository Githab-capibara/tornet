# 05. Dependency Checker

- **Status:** Published
- **Date:** 2026-08-23
- **Deciders:** @ByteBreach
- **Related:** [adr/07-cross-distro-checker.md](../adr/07-cross-distro-checker.md)

## Context

Detect package manager across distros.

## Mechanism

`tornet/utils.py` reads `/etc/os-release`, maps ID/ID_LIKE to package manager.

## Implementation details

Standalone runnable via `python -m tornet.utils`.

## Testing

Run on multiple distros.

## Alternatives considered

- **Inline only:** rejected weaker detection.
