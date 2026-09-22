# 04. Configuration

- **Status:** Accepted
- **Date:** 2026-08-23
- **Deciders:** @ByteBreach
- **Related:** [architecture/03-configuration-layout.md](../architecture/03-configuration-layout.md)
- **Authors:** @Githab-capibara

## Context

TorNet supports YAML and JSON config files so operators can repeat runs without
retyping flags. The default config path is `~/.tornet/config.yml`; use
`--config <path>` to load an alternate file.

## Prerequisites

- Python 3.6+ and the `tornet` CLI installed (see
  [Getting Started](01-getting-started.md)).
- A YAML (`.yml`/`.yaml`) or JSON config file, or none at all — the default
  path `~/.tornet/config.yml` is loaded when `--config` is not given.

## Config file format

Both `.yml` / `.yaml` and `.json` are accepted. Keys map directly to CLI flags:

```yaml
default:
  interval: 60        # seconds between rotations; also accepts ranges like 30-120
  count: 0            # 0 = infinite loop; N = run N times
  country: auto       # ISO 3166 code (us, de, jp) or "auto" for random
  schedule: null      # fixed period like "5m", "1h", "1d"; mutually exclusive with interval

network:
  proxy_port: 9050    # Tor SOCKS proxy port
  dns_port: 53        # DNS port (used by leak test)
  control_port: 9051  # Tor control port

security:
  kill_switch: false  # enable iptables kill switch on every run
  dns_protection: true
  log_level: info     # one of: debug, info, warning, error

advanced:
  max_retries: 3      # retries on rotation failure
  timeout: 30         # seconds before a network call is abandoned
  verify_ssl: true    # verify TLS certificates (required for ip-api.com)
```

Loaded via `--config <path>`; falls back to `~/.tornet/config.yml` and to an
empty dict if the file is missing. An unsupported extension produces a warning
and an empty config rather than a crash. An unsupported key is silently ignored.

## Current limitation

Today `config` is loaded into `main()` but CLI flags take precedence — config
keys are wired for future merge, not for current override. Treat keys as
forward-compatible until flag merging lands.

## How it works

`load_config()` sniffs the file extension, not the content: `.yml`/`.yaml`
go through `yaml.safe_load()` (which prevents arbitrary object construction
from untrusted files), `.json` through `json.load()`, anything else warns and
returns an empty config. A missing or malformed file degrades to a warning
instead of a traceback — see
[config management mechanism](../mechanisms/07-config-management.md).

## Caveats

- Unsupported extensions and malformed YAML/JSON produce warnings, not errors,
  so a silently-ignored misconfiguration is possible.
- CLI flags currently win over config values; do not rely on config keys to
  override a flag yet.
- `save_config()` writes incrementally by extension (YAML with
  `default_flow_style=False`, JSON with `indent=2`) and warns on failure.

## Consequences

- **Easier:** repeatable runs without remembering every flag.
- **Harder:** format validation is minimal; malformed YAML/JSON produces warnings,
  not errors, so silent misconfiguration is possible.

## References

- [Configuration layout](../architecture/03-configuration-layout.md)
- [Config management mechanism](../mechanisms/07-config-management.md)
