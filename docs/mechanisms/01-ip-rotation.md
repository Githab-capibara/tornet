# 01. IP rotation

- **Status:** Accepted
- **Date:** 2026-08-23
- **Deciders:** @ByteBreach
- **Related:** [adr/02-newnym-via-control-port.md](../adr/02-newnym-via-control-port.md), [architecture/01-system-overview.md](../architecture/01-system-overview.md)

## Context

TorNet's core promise is frequent, unattended IP changes. Rotations must be
fast enough to run every few seconds indefinitely, must not need root for
every iteration, and must survive a control port that may be unavailable.
Tor supports circuit replacement (`NEWNYM`) over its local control port, which
is far cheaper than restarting the whole `tor` process.

## Mechanism

One rotation is `change_ip()`:

1. If a specific country was requested (not `auto`), call
   `configure_tor_country()` first — pinning requires a torrc restart, see
   [country exit nodes](06-country-exitnodes.md).
2. Call `rotate_tor_ip()`:
   - connect `stem.control.Controller.from_port(port=9051)`,
   - `controller.authenticate()` (cookie-based),
   - send `Signal.NEWNYM`.
   Any exception is caught, warned about, and returns `False`.
3. On failure, fall back to `service_action("reload")`.
4. `time.sleep(2)` to let the new circuit establish.
5. Return `get_current_ip()` — via the SOCKS proxy if Tor is running,
   otherwise direct.

The repeated loop is `change_ip_repeatedly(interval_str, count, country, json_output)`:
`count == 0` loops forever, otherwise exactly `count` iterations. Each
iteration sleeps `parse_interval(interval_str)` seconds **before** rotating.

### Interval syntax (`parse_interval()`)

| Input | Meaning |
|-------|---------|
| `60` | exactly 60 seconds |
| `30-120` | uniformly random seconds per iteration (`random.randint(start, end)`) |

A malformed value exits with code 8.

## Implementation details

- Control-port path needs a readable `/run/tor/control.authcookie`
  (`debian-tor` group membership on Debian-family systems); no `sudo` involved.
- `get_ip_via_tor()` queries `https://api.ipify.org` through
  `socks5://127.0.0.1:9050`, 10 s timeout; network trouble returns `None`
  with a warning, never raises into the loop.
- The direct fetch fallback reports the **real** IP — diagnostic only.

## Testing

```bash
tornet --ip                      # baseline IP
tornet --change                  # rotate once, observe new IP
tornet --interval 30-120 --count 3   # three rotations at random gaps
```

Verify the IP actually changed between calls and that no `sudo` prompt appears
for plain rotations when the user is in the `debian-tor` group.

## Alternatives considered

- **Restart `tor` each time:** rejected — seconds of downtime per rotation and
  root required (see ADR-02).
- **Raw socket control protocol:** rejected — hand-rolled cookie auth is
  error-prone; `stem` is one small dependency.
