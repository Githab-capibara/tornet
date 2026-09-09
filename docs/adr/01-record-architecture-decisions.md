# 01. record architecture decisions

- **Status:** Accepted
- **Date:** 2026-08-21
- **Deciders:** @ByteBreach
- **Related:** —

## Context

TorNet has accumulated non-obvious design choices: rotating IPs through the
Tor control port instead of restarting the service, building the kill switch as
a dedicated iptables chain, installing dependencies at runtime, and shipping a
dual installer. None of these are self-evident from reading the code alone. A
future contributor reading `rotate_tor_ip()` can see *what* it does, but not
*why* the alternative of reloading the tor service was rejected.

## Decision

Keep Architecture Decision Records (ADRs) in [`docs/adr/`](.) following the
Michael Nygard format. Each ADR is a short, numbered, append-only document
capturing context, decision, consequences, and rejected alternatives.

## Consequences

- **Easier:** future maintainers can reconstruct the reasoning behind a design
  without digging through git history or guessing.
- **Harder:** every non-trivial architectural change now requires an ADR PR.
- **Given up:** the ability to silently reverse a decision — reversals must be
  recorded as a superseding ADR.
- **Migration:** none. Existing decisions are back-filled as ADRs 02–07.

## Alternatives considered

- **Option A: inline comments only.** Rejected because comments explain *how*,
  not *why*, and they rot alongside the code instead of being reviewed as
  first-class artifacts.
- **Option B: a single `DESIGN.md`.** Rejected because one file grows
  unbounded and loses the append-only, one-decision-per-document property that
  makes ADRs scannable.
