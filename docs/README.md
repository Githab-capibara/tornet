# TorNet Documentation

Canonical documentation index for **TorNet** — privacy-focused CLI for automated IP rotation via Tor.

All docs are GitHub-native Markdown in this `docs/` tree.

## Start here

| Guide | Purpose |
|-------|---------|
| [Getting Started](usage/01-getting-started.md) | First engagement in ~5 minutes |
| [Command Reference](usage/02-command-reference.md) | All CLI flags at a glance |
| [IP Rotation](mechanisms/01-ip-rotation.md) | How TorNet rotates your IP |
| [Architecture Overview](architecture/01-system-overview.md) | System structure and data flow |
| [Contributing](governance/01-contributing.md) | How to contribute |
| [ADR Index](adr/README.md) | Architecture decisions index |

## Directory map

| Directory | Purpose |
|-----------|---------|
| [`adr/`](adr/) | Architecture Decision Records, Michael Nygard format |
| [`architecture/`](architecture/) | System structure, Tor integration, configuration layout |
| [`governance/`](governance/) | Contributing, code of conduct, security policy, project principles |
| [`mechanisms/`](mechanisms/) | Runtime mechanisms deep dives |
| [`usage/`](usage/) | Operator guides: install, commands, troubleshooting |

## Key entry points

- **Operators** → [Usage README](usage/README.md) → [Getting Started](usage/01-getting-started.md)
- **Contributors** → [Contributing](governance/01-contributing.md) → [Architecture Overview](architecture/01-system-overview.md)
- **Maintainers** → [ADR Index](adr/README.md) → [Dual Installer ADR](adr/05-dual-installer.md)
- **Security review** → [Mechanisms README](mechanisms/README.md) → [Kill Switch](mechanisms/02-kill-switch.md)
- **Architecture** → [Architecture README](architecture/README.md) → [System Overview](architecture/01-system-overview.md)
- **Benchmarks** → [Benchmark Results](architecture/benchmark.svg)
- **Diagrams** → [Architecture Overview](architecture/overview.svg)

## Governance

- [Contributing Guide](governance/01-contributing.md)
- [Code of Conduct](governance/02-code-of-conduct.md)
- [Security Policy](governance/03-security-policy.md)
- [Project Principles](governance/04-project-principles.md)
- [License MIT](../LICENSE)
