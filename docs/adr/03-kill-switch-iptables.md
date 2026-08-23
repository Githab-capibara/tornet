# 03. Implement the kill switch as an iptables chain named TORNET-KILLSWITCH

- **Status:** Accepted
- **Date:** 2026-08-21
- **Deciders:** @ByteBreach
- **Related:** [mechanisms/02-kill-switch.md](../mechanisms/02-kill-switch.md)

## Context

A kill switch must block all non-Tor traffic so that a dropped circuit does
not leak the real IP. TorNet needs to enable and disable this on demand via
`--kill-switch`, and it must coexist with a user's existing firewall rules
without clobbering them.

iptables rules added directly to `OUTPUT` are hard to find and remove later;
an opaque "did we already enable it?" state leads to double-application or
leftover rules after uninstall.

## Decision

Use a dedicated, named iptables chain — `TORNET-KILLSWITCH` — that is created
on enable, jumped to from `OUTPUT`, and flushed plus deleted on disable. The
chain allows loopback, RFC 1918 private ranges, and TCP to port 9050 (the Tor
SOCKS proxy), then drops everything else. Toggle detection checks for the
chain's existence by name.

## Consequences

- **Easier:** idempotent toggle by name; clean teardown (`-F` then `-X`); the
  kill switch is visible and auditable with `iptables -L TORNET-KILLSWITCH`.
- **Harder:** requires `iptables` and root; the chain is Linux-only, so the
  kill switch does not exist on Windows/Android builds.
- **Given up:** a generic "block all" that would not need a custom chain —
  but that loses clean toggle/teardown.
- **Migration:** none; existing implementation in `toggle_kill_switch()`.

## Alternatives considered

- **Option A: append DROP rules directly to `OUTPUT`.** Rejected because
  finding and removing them later is fragile and risks leaving the host
  firewalled shut.
- **Option B: use `nftables`.** Rejected because it is less universally
  available across the older distros TorNet targets and would double the
  maintenance surface.
