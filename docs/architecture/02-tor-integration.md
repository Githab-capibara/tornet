# 02. Tor Integration

- **Status:** Accepted
- **Date:** 2026-08-21
- **Deciders:** @ByteBreach
- **Related:** [adr/02-newnym-via-control-port.md](../adr/02-newnym-via-control-port.md), [mechanisms/06-country-exitnodes.md](../mechanisms/06-country-exitnodes.md)
- **Authors:** @Githab-capibara

## Context

TorNet is fundamentally a thin controller around a local Tor instance. Two
local endpoints matter: the SOCKS proxy that application traffic flows through,
and the control port that TorNet uses to request new circuits and pin exit
countries.

## SOCKS proxy — 127.0.0.1:9050

All TorNet IP lookups and leak tests route through Tor's SOCKS5 proxy:

```python
proxies = {
    'http':  'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050',
}
```

- `get_ip_via_tor()` fetches the current exit IP from `https://api.ipify.org`
  through this proxy.
- `get_ip_with_country()` enriches it via `https://ipapi.co/json/`.
- `dns_leak_test()` hits leak-test URLs through the proxy to confirm they
  resolve over Tor.

When Tor is **not** running, `get_ip_direct()` falls back to a direct fetch —
this reports the user's real IP and is used only for the `--ip` diagnostic,
never for confirming a rotation.

## Control port — 127.0.0.1:9051

IP rotation uses the control port, not a service restart (see
[ADR-02](../adr/02-newnym-via-control-port.md)):

```python
from stem.control import Controller
from stem import Signal
with Controller.from_port(port=9051) as controller:
    controller.authenticate()
    controller.signal(Signal.NEWNYM)
```

Authentication is cookie-based. On Debian-based systems, membership in the
`debian-tor` group makes `/run/tor/control.authcookie` group-readable, so
routine rotations need no `sudo`. If the control-port path fails, TorNet falls
back to `service_action("reload")`.

## Country exit nodes

`configure_tor_country(country_code)` writes a custom torrc:

```
ExitNodes {DE}
StrictNodes 1
```

then restarts Tor with that torrc (`tor -f ~/.tornet/torrc.custom --RunAsDaemon 1`)
and records the choice in `~/.tornet/current_country`. `StrictNodes 1` forces
Tor to use only the listed exit countries; without it, Tor may ignore the
constraint when it cannot satisfy it. See
[country exit nodes mechanism](../mechanisms/06-country-exitnodes.md).

## Service management

`detect_service_manager()` returns `systemctl` (when `/run/systemd/system`
exists) or `service`, and `service_action(action)` runs the corresponding
`systemctl <action> tor` / `service tor <action>`. These are used to start,
stop, reload, and restart Tor.

## Browser configuration

TorNet does not configure the browser; the user must point their browser at the
SOCKS proxy. The README documents the Firefox manual-proxy setup
(`127.0.0.1:9050`, SOCKS v5, "Proxy DNS when using SOCKS v5").

## Consequences

- Two ports matter: **9050** (SOCKS, application traffic) and **9051**
  (control, rotation + country).
- A pinned exit country only takes effect after a Tor (re)start with the custom
  torrc — `NEWNYM` alone does not change the exit country.
- The direct-IP fallback exists only as a diagnostic; it never confirms a
  rotation and should not be relied on under the threat model.

## References

- [Tor config docs — ExitNodes / StrictNodes](https://2019.www.torproject.org/docs/tor-manual.html.en)
- [stem `Controller`](https://stem.torproject.org/api/control.html) — control-port client.
