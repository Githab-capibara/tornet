# 06. Country exit nodes

- **Status:** Published
- **Date:** 2026-08-23
- **Deciders:** @ByteBreach
- **Related:** [usage/03-country-selection.md](../usage/03-country-selection.md), [architecture/02-tor-integration.md](../architecture/02-tor-integration.md)

## Context

Users want exits from a specific country. Tor supports this via `ExitNodes` +
`StrictNodes` in torrc, but it requires a config file and a Tor restart —
`NEWNYM` alone changes circuits, never the exit-country policy.

## Mechanism

`tornet --country de` stores the choice and reconfigures Tor via
`configure_tor_country(country_code)`:

1. Ensure `~/.tornet/` exists.
2. Write `~/.tornet/torrc.custom`:
   ```
   ExitNodes {DE}
   StrictNodes 1
   ```
3. Write the uppercase code to `~/.tornet/current_country` (state marker).
4. `service_action("stop")`, wait 1 s.
5. Launch a user-owned daemonized instance with the custom config:
   `tor -f ~/.tornet/torrc.custom --RunAsDaemon 1`; on nonzero return, log
   "Starting Tor with custom configuration..." and wait 3 s for bootstrap.

Reading state back: `get_current_country()` returns the file contents or
`"Auto (Random)"` when no pin is active.

Restoring stock behavior: `restore_default_tor()` deletes both files, then
stops and restarts the service — used by `--restore-default`, `--stop`, and
signal cleanup ([signal handling](03-signal-handling.md)).

## Implementation details

- `StrictNodes 1` is mandatory: without it Tor treats `ExitNodes` as a
  preference and silently ignores the constraint when unsatisfied.
- The custom instance runs unprivileged (`use_sudo=False`) under the invoking
  user's account — distinct from the system service instance.
- Country codes are uppercased before use; `auto` never reaches this function
  (`change_ip()` filters it).
- Because pinning restarts Tor, the first rotation after `--country` costs a
  full circuit rebuild; subsequent rotations are plain NEWNYM within the
  pinned country pool.

## Testing

```bash
sudo tornet --country jp
cat ~/.tornet/current_country          # expect JP
cat ~/.tornet/torrc.custom             # expect ExitNodes {JP} + StrictNodes 1
tornet --status                        # IP country should be Japan
tornet --restore-default               # files removed, stock tor restarted
```

## Alternatives considered

- **Control-port SETCONF for ExitNodes:** viable in principle, but the current
  implementation predates it and torrc-restart also covers the daemon
  lifecycle; revisit as a superseding ADR if adopted.
- **Per-circuit node selection in code:** rejected — duplicates what torrc
  already expresses.
