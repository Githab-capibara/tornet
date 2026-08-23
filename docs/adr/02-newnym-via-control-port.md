# 02. Rotate IPs via the Tor control port instead of restarting the service

- **Status:** Accepted
- **Date:** 2026-08-21
- **Deciders:** @ByteBreach
- **Related:** [mechanisms/01-ip-rotation.md](../mechanisms/01-ip-rotation.md)

## Context

Tor exposes two ways to force a new exit IP: send the `NEWNYM` signal over the
control port, or restart the whole `tor` process. Restarting is simple and
works with any privilege model, but it tears down all circuits, re-runs
bootstrap, and adds several seconds of downtime per rotation. TorNet rotates
IPs frequently (`--interval 30`, `--count 0` for infinite), so per-rotation
downtime compounds.

The control port (`127.0.0.1:9051`) accepts `NEWNYM`, which requests a clean
circuit without restarting the process. On Debian-based systems the
`debian-tor` group can read `/run/tor/control.authcookie`, so an unprivileged
user in that group can authenticate directly — no `sudo` required.

## Decision

Rotate IPs by authenticating to the Tor control port with `stem` and sending
`NEWNYM`. Fall back to `service_action("reload")` only if the control-port
path fails. Do not escalate to `sudo` for routine rotations.

## Consequences

- **Easier:** sub-second rotations with no process restart; no root needed for
  the common case.
- **Harder:** requires the `stem` library and a readable control auth cookie;
  on locked-down systems the fallback path still needs privileges.
- **Given up:** the simplicity of "restart and forget" — the code now carries a
  primary path and a fallback.
- **Migration:** none; this is the existing implementation in
  `rotate_tor_ip()` / `change_ip()`.

## Alternatives considered

- **Option A: always `service tor reload`.** Rejected because it is slower,
  tears down circuits, and still needs root on most distros, gaining nothing
  over the control-port path.
- **Option B: raw socket to port 9051 instead of `stem`.** Rejected because
  hand-rolling cookie authentication and the control protocol is error-prone
  and gains only a single dependency removal.
