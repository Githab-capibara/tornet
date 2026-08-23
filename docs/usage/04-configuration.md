# 04. Configuration

- **Status:** Published
- **Date:** 2026-08-23
- **Deciders:** @ByteBreach
- **Related:** [architecture/03-configuration-layout.md](../architecture/03-configuration-layout.md)

## Context

TorNet supports YAML/JSON config files.

## Body

Config file path: `~/.tornet/config.yml`

Example:

```yaml
interval: 60
count: 10
country: us
```

Load with `--config custom.yml`.

## Consequences

- Easier: repeatable runs.
- Harder: format validation.

## References

- [Configuration Layout](architecture/03-configuration-layout.md)
