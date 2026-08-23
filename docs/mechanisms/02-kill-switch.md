# 02. Kill Switch

- **Status:** Published
- **Date:** 2026-08-23
- **Deciders:** @ByteBreach
- **Related:** [adr/03-kill-switch-iptables.md](../adr/03-kill-switch-iptables.md)

## Context

Prevent IP leaks when Tor circuit drops.

## Mechanism

Create iptables chain TORNET-KILLSWITCH, jump from OUTPUT, allow loopback/private and TCP 9050, drop rest. Toggle by chain existence.

## Implementation details

`toggle_kill_switch()` uses iptables. Linux only, requires root.

## Testing

Enable → non-Tor traffic blocked.

## Alternatives considered

- **Append rules:** rejected for fragility.
