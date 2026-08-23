# 06. Stop Tor and tornet processes on SIGINT/SIGQUIT before exiting

- **Status:** Accepted
- **Date:** 2026-08-21
- **Deciders:** @ByteBreach
- **Related:** [mechanisms/10-service-detection.md](../mechanisms/10-service-detection.md)

## Context

When TorNet runs an infinite rotation loop (`--count 0`), the user interrupts
with Ctrl-C (SIGINT) or Ctrl-\ (SIGQUIT). If the process exits immediately, it
can leave a custom Tor instance running with a pinned `ExitNodes` torrc, plus
any orphaned `tornet` background work. That leftover Tor would keep routing
through a single country and is easy to forget.

## Decision

Register `signal_handler` for `SIGINT` and `SIGQUIT`. On either signal, call
`stop_services()`, which restores the default Tor configuration (removing the
custom torrc and country file), kills lingering `tor` processes, and kills
lingering `tornet` processes before exiting 0.

## Consequences

- **Easier:** interrupting a run always leaves the system in a clean state —
  no pinned exit country, no orphan Tor.
- **Harder:** Ctrl-C now has a side effect beyond "stop this process"; it also
  tears down the Tor service, which may surprise users running other Tor
  consumers.
- **Given up:** the ability to interrupt without touching Tor — by design the
  cleanup is unconditional.
- **Migration:** none; existing implementation in `signal_handler()` and
  `stop_services()`.

## Alternatives considered

- **Option A: exit immediately on interrupt.** Rejected because it leaves a
  country-pinned Tor running and accumulates orphan processes across runs.
- **Option B: only stop `tornet`, leave Tor alone.** Rejected because a
  leftover `ExitNodes {DE} StrictNodes 1` torrc silently breaks "use a random
  country" the next time the user starts Tor.
