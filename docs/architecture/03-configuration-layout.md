# 03. Configuration layout

- **Status:** Accepted
- **Date:** 2026-08-21
- **Deciders:** @ByteBreach
- **Related:** [adr/05-dual-installer.md](../adr/05-dual-installer.md), [usage/04-configuration.md](../usage/04-configuration.md)

## Context

TorNet keeps its runtime state under a single user directory (`~/.tornet/`)
and ships its packaging metadata in two files. This documents where everything
lives so operators and contributors know what is safe to edit, delete, or
version-control.

## Runtime state — `~/.tornet/`

| Path | Written by | Purpose |
|------|-----------|---------|
| `~/.tornet/config.yml` | `save_config()` | Optional YAML/JSON user config loaded by `--config` (defaults to this) |
| `~/.tornet/tornet.log` | `follow_logs()` | TorNet log file; created on first `--log` if absent |
| `~/.tornet/torrc.custom` | `configure_tor_country()` | Custom Tor config with `ExitNodes`/`StrictNodes`; removed by `--restore-default` |
| `~/.tornet/current_country` | `configure_tor_country()` | Last pinned country code; read by `get_current_country()` for `--status` |

These are the only persistent side effects of a run. Deleting the whole
`~/.tornet/` directory resets TorNet to a clean state (the default Tor
configuration is restored by `restore_default_tor()`).

## Config file format

`load_config()` accepts `.yml`, `.yaml`, and `.json`. A documented example:

```yaml
default:
  interval: 60
  count: 0
  country: auto
  schedule: null

network:
  proxy_port: 9050
  dns_port: 53
  control_port: 9051

security:
  kill_switch: false
  dns_protection: true
  log_level: info

advanced:
  max_retries: 3
  timeout: 30
  verify_ssl: true
```

Loaded via `--config <path>`; falls back to `~/.tornet/config.yml` and to an
empty dict if the file is missing or unsupported. An unsupported extension
produces a warning and an empty config rather than a crash.

## Packaging — dual installer

TorNet declares the same metadata in two places (see
[ADR-05](../adr/05-dual-installer.md)):

| File | Role | Version |
|------|------|---------|
| `pyproject.toml` | Primary PEP 517 build; declares `tornet=tornet.tornet:main` | 2.0.2 |
| `setup.py` | Legacy fallback for `python setup.py ...` | 2.0.2 |
| `tornet.egg-info/` | Generated build artifact; not source of truth | — |

Both declare the same runtime dependencies: `requests`, `PySocks`, `PyYAML`,
`schedule`, `stem`. **When bumping the version or changing a dependency, edit
both files** to avoid drift.

## Project root layout

```
tornet/
├── tornet/              # the Python package
│   ├── __init__.py      # public API re-exports
│   ├── tornet.py        # CLI + all runtime mechanisms
│   ├── utils.py         # standalone cross-distro dependency checker
│   ├── banner.py        # ASCII banner
│   └── tor.exe          # Windows Tor binary shipped in-package
├── docs/                # this documentation tree
├── README.md            # project homepage (GitHub-native)
├── LICENSE              # MIT
├── pyproject.toml       # primary packaging
└── setup.py             # legacy packaging
```

## Consequences

- All persistent state is confined to `~/.tornet/`, so a "reset" is a single
  `rm -rf ~/.tornet` (or `tornet --restore-default` for just the Tor config).
- The dual installer means version/dependency edits are a two-file change.
- The in-package `tor.exe` makes the Windows build self-contained but bloats
  the wheel; it is not used on Linux.

## References

- [PEP 517](https://peps.python.org/pep-0517/) — build backend interface used by `pyproject.toml`.
- [Tor config — `ExitNodes`/`StrictNodes`](https://2019.www.torproject.org/docs/tor-manual.html.en)
