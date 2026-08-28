# 12. Status monitoring

- **Status:** Accepted
- **Date:** 2026-08-26
- **Deciders:** @ByteBreach
- **Related:** [mechanisms/10-service-detection.md](10-service-detection.md), [mechanisms/06-country-exitnodes.md](06-country-exitnodes.md)

## Context

Operators need a single read-only command answering: is Tor installed, is it
running, what exit am I on right now, and what did *I* configure? Diagnosing
"am I leaking / why is my IP wrong?" should not require five separate shell
commands.

## Mechanism

`tornet --status` → `show_status()` renders one panel by combining probes:

| Field | Source probe |
|-------|--------------|
| Tor Installed | `is_tor_installed()` — `shutil.which("tor")` |
| Tor Running | `is_tor_running()` — `pgrep -x tor`, `/proc/*/comm` fallback |
| Current IP | `get_ip_with_country()` — `https://ipapi.co/json/` through SOCKS `127.0.0.1:9050`; falls back to `get_ip_via_tor()` (ipify, no geo) |
| IP Country | geolocation fields from the same response |
| Configured Country | `get_current_country()` — reads `~/.tornet/current_country`, else `"Auto (Random)"` |
| Service Manager | `detect_service_manager()` |
| Package Manager | `detect_package_manager()` (inline `which()` variant) |
| Config File / Log File | constant paths under `~/.tornet/` |

The contrast between **Current IP Country** (what Tor actually gives you now)
and **Configured Country** (the pin state on disk) is the fastest way to spot
a stale or failed pin.

## Implementation details

- Strictly read-only: no service actions, no writes.
- All network probes carry a 10 s timeout and degrade to `Unknown` /
  red-colored output instead of failing the command.
- The panel is colored-text only; there is deliberately no `--status --json`
  variant yet — machine-readable status is future work (see
  [JSON output](13-json-output.md) for current coverage).

## Testing

```bash
tornet --status                                  # healthy system: all ✓
sudo systemctl stop tor && tornet --status       # Running ✗, IP Unknown
echo -n DE > ~/.tornet/current_country && tornet --status   # Configured: DE
```

## Alternatives considered

- **JSON-only machine output with a pretty-printer wrapper:** deferred until
  the JSON surface (13) is extended to cover status.
- **Polling daemon:** rejected — out of scope for a CLI tool; `--follow` logs
  and repeated invocations cover monitoring needs.
