# 07. Config Management

- **Status:** Published
- **Date:** 2026-08-23
- **Authors:** @ByteBreach
- **Related:** [architecture/03-configuration-layout.md](../architecture/03-configuration-layout.md)

## Context

Persist user settings.

## Mechanism

`load_config`/`save_config` handle YAML/JSON in `~/.tornet/config.yml`.

## Implementation details

Uses PyYAML.

## Testing

Config loads on start.

## Alternatives considered

- **INI:** less expressive.
