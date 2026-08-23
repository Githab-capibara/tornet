# 05. Troubleshooting

- **Status:** Published
- **Date:** 2026-08-23
- **Deciders:** @ByteBreach
- **Related:** [usage/01-getting-started.md](01-getting-started.md)

## Context

Common errors need fast resolution paths.

## Body

### Permission denied

Run kill switch with sudo: `sudo tornet --kill-switch`

### Tor not starting

```bash
which tor
sudo systemctl start tor
```

### Dependencies missing

```bash
tornet --auto-fix
```

## Consequences

- Easier: self-service.
- Harder: maintenance of examples.

## References

- [Getting Started](01-getting-started.md)
