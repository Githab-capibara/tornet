# 10. Service detection

- **Status:** Published
- **Date:** 2026-08-23
- **Deciders:** @ByteBreach
- **Related:** [architecture/02-tor-integration.md](../architecture/02-tor-integration.md), [adr/06-signal-cleanup.md](../adr/06-signal-cleanup.md)

## Context

TorNet drives an external Tor rather than embedding one. Every lifecycle
action (start before a run, reload fallback on failed NEWNYM, stop/restart on
country pinning, teardown at exit) must work across systemd and SysV-init
distros without hardcoding either.

## Mechanism

**Which manager?** `detect_service_manager()`:

| Condition | Returns |
|-----------|---------|
| `systemctl` in PATH **and** `/run/systemd/system` exists | `systemctl` |
| else `service` binary in PATH | `service` |
| neither | `None` |

The `/run/systemd/system` check prevents false positives where the binary
exists but systemd is not PID 1 (containers, WSL1).

**Acting:** `service_action(action)` builds
`["systemctl", action, "tor"]` or `["service", "tor", action]`, runs it via
`run_cmd(..., use_sudo=True, check=False)`; a nonzero return warns with stderr
instead of raising. Manager `None` → error exit 3.

**Process-level checks:**

- `is_tor_installed()` — `shutil.which("tor")`.
- `is_tor_running()` — `pgrep -x tor`; if pgrep is missing, scans
  `/proc/<pid>/comm` for the exact name `tor`.

`initialize_environment()` starts the service when not running and reminds the
user to point clients at `127.0.0.1:9050`.

## Implementation details

- Privilege escalation is centralized in `run_cmd()`: prepends `sudo` when
  euid ≠ 0; no sudo binary → exit 2.
- `check=False` everywhere here: service units may legitimately be named
  differently (e.g. `tor@default`) — failures degrade to warnings so the
  control-port rotation path still gets its chance.
- Used by: rotation fallback (`reload`), country pinning (`stop` +
  user-daemon), restore/cleanup (`stop`, `start`),
  [startup checks](14-startup-checks.md).

## Testing

```bash
tornet --status                       # Service Manager line shows systemctl/service/Unknown
sudo systemctl stop tor && tornet --ip    # direct-IP path proves running-detection works
```

On a SysV-only container verify the `service` branch is selected.

## Alternatives considered

- **Hardcode `systemctl`:** rejected — breaks Debian 8-era and Alpine images.
- **D-Bus org.freedesktop.systemd1 directly:** rejected — heavy dependency for
  two verbs.
