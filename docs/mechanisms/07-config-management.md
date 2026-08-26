# 07. Config management

- **Status:** Published
- **Date:** 2026-08-23
- **Deciders:** @ByteBreach
- **Related:** [architecture/03-configuration-layout.md](../architecture/03-configuration-layout.md), [usage/04-configuration.md](../usage/04-configuration.md)

## Context

Operators need repeatable runs without retyping flags, and a place where
runtime state (custom torrc, current country) lives predictably. TorNet keeps
all of it under `~/.tornet/` and accepts both YAML and JSON.

## Mechanism

**Loading** — `load_config(config_file)`:

1. File missing → return `{}` (no error).
2. Extension `.yml` / `.yaml` → `yaml.safe_load()` (empty file → `{}`).
3. Extension `.json` → `json.load()`.
4. Any other extension → warning, `{}`.
5. Any parse exception → warning with the reason, `{}` — never crashes the CLI.

`main()` resolves the path as `args.config or CONFIG_FILE`
(`~/.tornet/config.yml`) on every invocation.

**Saving** — `save_config(config_file, config)` creates parent directories,
then dumps by extension: `yaml.dump(..., default_flow_style=False)` or
`json.dump(..., indent=2)`; failures warn instead of raising.

## Implementation details

- Format selection is extension-based only — content sniffing is not
  attempted.
- `yaml.safe_load` (not `load`) prevents arbitrary object construction from
  untrusted config files.
- Honest caveat: today `config` is loaded into `main()` but CLI flags are not
  yet merged from it — the loader is wired for availability and future use;
  flags remain the single source of behavior. Treat config keys as
  forward-compatible until flag merging lands.
- Runtime state files written by other mechanisms in the same directory:
  `torrc.custom`, `current_country` (see
  [country exit nodes](06-country-exitnodes.md)) and `tornet.log`
  ([log management](09-log-management.md)).

## Testing

```bash
printf 'interval: 30\ncount: 2\n' > /tmp/t.yml
tornet --config /tmp/t.yml --status          # loads without error
printf '{"bad": yaml' > /tmp/bad.yml
tornet --config /tmp/bad.yml --status        # warning, continues
```

Expect no traceback in either case.

## Alternatives considered

- **INI via configparser:** rejected — no nesting, two formats would become
  three.
- **TOML:** rejected — stdlib support (`tomllib`) is read-only pre-3.13, and
  TorNet targets 3.6+.
