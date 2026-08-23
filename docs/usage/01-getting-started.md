# 01. Getting Started

- **Status:** Published
- **Date:** 2026-08-23
- **Authors:** @ByteBreach
- **Related:** [usage/02-command-reference.md](02-command-reference.md)

## Context

New users need a fast path from install to first IP change.

## Body

### Install

```bash
pip install tornet==2.0.2
```

### First IP change

```bash
tornet --ip
tornet --change
```

### Auto-fix missing deps

```bash
tornet --auto-fix
```

## Consequences

- Easier: 5 minute onboarding.
- Harder: requires Tor installed.
- What it leaves open: GUI onboarding.

## References

- [Command Reference](02-command-reference.md)
