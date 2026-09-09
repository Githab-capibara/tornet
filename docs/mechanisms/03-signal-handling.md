# 03. signal handling

- **Status:** Accepted
- **Date:** 2026-08-23
- **Deciders:** @ByteBreach
- **Related:** [adr/06-signal-cleanup.md](../adr/06-signal-cleanup.md), [mechanisms/10-service-detection.md](../mechanisms/10-service-detection.md)

## Context

Rotation runs are long-lived (`--count 0` loops forever). Users interrupt with
Ctrl-C (SIGINT) or Ctrl-\ (SIGQUIT). An immediate exit would leave a
country-pinned custom Tor instance running plus orphaned `tornet` processes,
silently breaking "random country" behavior on the next start.

## Mechanism

`main()` registers one handler before anything else:

```python
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGQUIT, signal_handler)
```

On either signal, `signal_handler()` runs `stop_services()`, which:

1. Calls `restore_default_tor()` — deletes `~/.tornet/torrc.custom` and
   `~/.tornet/current_country`, stops the service, waits 1 s, starts it again
   stock, waits 2 s.
2. `pkill -f tor` — kills lingering Tor processes started outside the service
   manager (e.g. the user-daemon launched with a custom torrc).
3. `pkill -f tornet` — kills lingering TorNet processes.
4. Prints "Program terminated by user." and exits 0.

## Implementation details

- Registration happens first in `main()`, so even early Ctrl-C during startup
  is handled.
- `pkill` failures are swallowed (`check=False`) — cleanup is best-effort and
  must not crash the handler.
- Because SIGINT now tears down Tor, users running other Tor consumers on the
  same box will notice their Tor stopped too — accepted trade-off (ADR-06).
- The infinite loop also catches `KeyboardInterrupt` inside
  `change_ip_repeatedly()` and breaks out cleanly; the signal handler remains
  the backstop that performs the teardown.

## Testing

```bash
sudo tornet --country de --interval 60 --count 0 &
# wait for one rotation, then:
kill -INT <pid>          # or press Ctrl-C in foreground
ls ~/.tornet/            # torrc.custom and current_country must be gone
pgrep -x tor || echo "tor stopped"
```

Expect: exit message, no pinned torrc left, no orphan tor/tornet processes.

## Alternatives considered

- **Exit immediately on interrupt:** rejected — leaves a country-pinned Tor
  running and accumulates orphans.
- **Stop only `tornet`, leave Tor alone:** rejected — leftover
  `ExitNodes {DE} StrictNodes 1` torrc silently breaks random-country mode.
