# 15. IP geolocation

- **Status:** Accepted
- **Date:** 2026-08-27
- **Deciders:** @ByteBreach
- **Related:** [mechanisms/12-status-monitoring.md](12-status-monitoring.md), [architecture/01-system-overview.md](../architecture/01-system-overview.md)

## Context

When TorNet reports an IP (baseline, after a rotation, or via `--status`), the
operator benefits from knowing *where* that IP is. Tor exit traffic also needs
a human-readable country name and a supported-country list for the
`--country` pinning feature. These are three small helpers rather than one
mechanism, but together they form the geolocation surface of the tool and are
easy to get wrong (third-party API downtime, inconsistent country parsing).

## Mechanism

### `get_ip_info(ip)`

Performs a best-effort geolocation lookup against the public
`http://ip-api.com/json/{ip}` endpoint (5 s timeout). On a `200` response it
returns the parsed JSON (country, region, city, ISP, lat/lon, …); on any error
or non-200 it returns `None` and the caller degrades gracefully (shows the raw
IP only). No exception escapes this function.

### `get_country_name(country_code)`

Maps a two-letter ISO code (e.g. `US`, `RU`, `DE`) to a display name using a
built-in `country_map` dict. Unknown codes fall back to the uppercased code
itself, so the UI never shows a blank.

### `list_countries()`

Returns the same `country_map` (code → name) that `get_country_name` consults.
This is the single source of truth for which exit countries TorNet can pin and
for the validation of the `--country` argument.

## Implementation details

- The ip-api.com call is unauthenticated and rate-limited (free tier ~45 req/min);
  callers must not invoke it inside a tight loop.
- `get_ip_info` failure is silent by design — geolocation is diagnostic, never
  on the critical rotation path.
- The country map is static and embedded; changing supported countries means
  editing the map in `tornet/tornet.py`, not a config file.

## Testing

```bash
tornet --status          # shows IP Country / geolocation fields from get_ip_info
tornet --country US      # validates against list_countries(); get_country_name renders "United States"
```

Confirm that an unknown `--country ZZ` is rejected before any rotation starts,
and that `--status` still prints an IP when ip-api.com is unreachable.

## Alternatives considered

- **Bundle a local GeoIP database (MaxMind).** Rejected — adds a large data
  file and an update dependency for a diagnostic feature.
- **Hardcode country names only where needed.** Rejected — duplicates the map
  across functions; a single `list_countries()` keeps it consistent.
