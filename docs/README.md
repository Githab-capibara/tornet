# TorNet Documentation

This is the canonical documentation index for **TorNet** — a privacy-focused
Python CLI that automates IP address rotation through the Tor network.

TorNet is documented as GitHub-native Markdown. There is no separate Sphinx
site; every guide lives in this `docs/` tree and renders directly on GitHub.

## Start here

New to TorNet? These links get you running in under five minutes.

| Goal | Link |
|------|------|
| Install and run your first IP change | [Installation guide](#) |
| Every CLI flag at a glance | [CLI options](#) |
| How TorNet rotates your IP | [IP rotation](#) |
| Why the code is shaped this way | [Record Architecture Decisions](adr/01-record-architecture-decisions.md) |
| How to contribute | [Contributing](governance/01-contributing.md) |

## Directory map

| Directory | Purpose |
|-----------|---------|
| [`adr/`](adr/) | Architecture Decision Records (Michael Nygard format) |
| [`architecture/`](architecture/) | System structure, Tor integration, configuration layout |
| [`usage/`](usage/) | Installation, commands, country selection, troubleshooting |
| [`mechanisms/`](mechanisms/) | Deep dives into each runtime mechanism |
| [`governance/`](governance/) | Contributing, code of conduct, security policy |

## Key entry points

- **Operators** → [usage/README.md](usage/README.md), [usage/README.md](usage/README.md)
- **Contributors** → [governance/01-contributing.md](governance/01-contributing.md), [architecture/01-system-overview.md](architecture/01-system-overview.md)
- **Maintainers** → [adr/README.md](adr/README.md) (decision log), [adr/05-dual-installer.md](adr/05-dual-installer.md)
- **Security review** → [mechanisms/README.md](mechanisms/README.md), [governance/README.md](governance/README.md)

## Governance

- [Contributing Guide](governance/01-contributing.md)
- [Code of Conduct](#)
- [Security Policy](#)
- [License (MIT)](../LICENSE)

## Conventions

- Documentation is **English only**.
- Every document carries a two-digit number prefix (`01-`, `02-`); numbering
  restarts at `01` inside each subdirectory.
- File names are lowercase kebab-case, e.g. `07-cross-distro-checker.md`.
- New documents start from the [template](template.md).
- Each subdirectory has its own `README.md` describing its contents.
