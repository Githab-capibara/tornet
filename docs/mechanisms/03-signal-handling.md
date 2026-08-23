# 03. Signal Handling

- **Status:** Published
- **Date:** 2026-08-23
- **Deciders:** @ByteBreach
- **Related:** [adr/06-signal-cleanup.md](../adr/06-signal-cleanup.md)

## Context

Infinite loops need clean exit.

## Mechanism

Register SIGINT/SIGQUIT to `signal_handler`, which calls `stop_services()`: restore default Tor config, pkill tor and tornet.

## Implementation details

Uses `signal.signal`.

## Testing

Ctrl-C leaves no pinned torrc.

## Alternatives considered

- **Exit immediately:** rejected leaves orphans.
