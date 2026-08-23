# Architecture Decision Records

This directory contains the **Architecture Decision Records** (ADRs) for
TorNet — short, numbered, append-only documents that capture non-obvious
architectural decisions, their context, and their consequences.

## When to write one

Write an ADR when the answer to "why is the code shaped this way?" needs to
be available to a future maintainer (human or AI) who was not in the room when
the decision was made. Concretely:

- A trade-off between two viable designs where the loser is not obviously bad
  (e.g. rotating IPs via the Tor control port vs. restarting the service).
- A constraint that the code relies on but does not test (e.g. the assumption
  that the `debian-tor` group can read the control auth cookie).
- A reversal of a previous decision — the old ADR is marked `Superseded` and
  the new one explains why.
- A policy that governs how the project is operated (e.g. the dual
  `setup.py` + `pyproject.toml` packaging, the runtime auto-fix behavior).

Do **not** write an ADR for:

- Decisions that are obvious from reading the code.
- Bug fixes that do not change architecture.
- Style or formatting decisions (the project's lint config is the source of
  truth).
- Feature scoping (open an issue).

## Format

Each ADR follows the [Michael Nygard format](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions):

1. **Title** — short, imperative, present tense.
2. **Status** — `Proposed` / `Accepted` / `Deprecated` / `Superseded by ADR-NN`.
3. **Context** — the forces at play; what makes this decision non-obvious.
4. **Decision** — what we are doing.
5. **Consequences** — what becomes easier, what becomes harder, what is given up.
6. **Alternatives considered** — the designs that lost, with one sentence each
   on why.

Use [`template.md`](template.md) as the starting point.

## Lifecycle

- Numbered sequentially, two digits, never renumbered: `01-...`, `02-...`. The
  number is allocated when the PR opens; if your draft PR sits for a while and
  another ADR lands first, renumber yours.
- File name kebab-case, derived from the title: `07-cross-distro-checker.md`.
- Append-only. To change a decision, write a new ADR that supersedes the old
  one; do not edit the old one except to flip its `Status` to
  `Superseded by ADR-NN`.

## Contents

| Document | Purpose |
|----------|---------|
| [01-record-architecture-decisions.md](01-record-architecture-decisions.md) | Record architecture decisions |
| [02-newnym-via-control-port.md](02-newnym-via-control-port.md) | Rotate IPs via Tor control port |
| [03-kill-switch-iptables.md](03-kill-switch-iptables.md) | Implement kill switch as iptables chain |
| [04-runtime-auto-fix.md](04-runtime-auto-fix.md) | Install dependencies at runtime |
| [05-dual-installer.md](05-dual-installer.md) | Ship both setup.py and pyproject.toml |
| [06-signal-cleanup.md](06-signal-cleanup.md) | Stop processes on signals |
| [07-cross-distro-checker.md](07-cross-distro-checker.md) | Cross-distribution dependency checker |


## Index

| # | Title | Status |
|---|-------|--------|
| [01](01-record-architecture-decisions.md) | Record architecture decisions | Accepted |
| [02](02-newnym-via-control-port.md) | Rotate IPs via the Tor control port instead of restarting the service | Accepted |
| [03](03-kill-switch-iptables.md) | Implement the kill switch as an iptables chain named TORNET-KILLSWITCH | Accepted |
| [04](04-runtime-auto-fix.md) | Install missing dependencies at runtime behind an explicit `--auto-fix` flag | Accepted |
| [05](05-dual-installer.md) | Ship both `setup.py` and `pyproject.toml` as install sources | Accepted |
| [06](06-signal-cleanup.md) | Stop Tor and tornet processes on SIGINT/SIGQUIT before exiting | Accepted |
| [07](07-cross-distro-checker.md) | Keep a standalone cross-distribution dependency checker in `utils.py` | Accepted |

Keep this index in sync when you land a new ADR.
