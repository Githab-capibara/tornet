# 15. IP Geolocation

- **Status:** Accepted
- **Date:** 2026-08-27
- **Deciders:** @ByteBreach
- **Related:** [mechanisms/12-status-monitoring.md](12-status-monitoring.md), [architecture/01-system-overview.md](../architecture/01-system-overview.md)
- **Authors:** @Githab-capibara

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

This helper is used **only** by the `--ip --json` surface in `main()`:
the JSON payload is enriched with the returned fields when their
`status == "success"`. It is **not** used by `--status` — that panel reads
`get_ip_with_country()` instead (see [status monitoring](12-status-monitoring.md)).

### `get_country_name(country_code)`

Maps a two-letter ISO code (e.g. `US`, `RU`, `DE`) to a display name using a
built-in `country_map` dict. Unknown codes fall back to the uppercased code
itself, so the UI never shows a blank. At the time of writing the map holds
33 entries (US, GB, DE, FR, CA, AU, JP, CN, IN, BR, RU, KR, IT, ES, NL, SE,
CH, NO, DK, FI, PL, TR, MX, ZA, EG, NG, KE, SG, HK, TW, IL, AE, SA).

### `list_countries()`

Prints the built-in `countries` dict (code → name) — the list shown by
`tornet --list-countries`, **22 entries** (US, GB, DE, FR, CA, AU, JP, NL,
SE, CH, NO, DK, FI, RU, CN, IN, BR, MX, ZA, SG, HK, TW), plus the `AUTO`
entry that stands for the random-country default.

> ⚠️ **Caveat:** `countries` (used by `list_countries()`) and `country_map`
> (used by `get_country_name()`) are **two separate dictionaries** in
> `tornet/tornet.py`. They overlap but are not identical — e.g. `IT`/`ES`
> exist in `country_map` but not in `countries`. Keep both in sync when adding
> or removing a country; a future refactor should unify them.

> ⚠️ **Validation caveat:** the `--country` argument is **not validated**
> against either dictionary. `configure_tor_country()` writes whatever
> two-letter code it receives into `torrc.custom`
> (`ExitNodes {ZZ}` / `StrictNodes 1`). An unknown code is not rejected
> upfront — Tor simply fails to satisfy the pin, so verify with
> `tornet --status` after pinning an unusual code.

## Implementation details

- The ip-api.com call is unauthenticated and rate-limited (free tier ~45 req/min);
  callers must not invoke it inside a tight loop.
- `get_ip_info` failure is silent by design — geolocation is diagnostic, never
  on the critical rotation path.
- The country map is static and embedded; changing supported countries means
  editing the map in `tornet/tornet.py`, not a config file.

## Testing

```bash
tornet --ip --json         # JSON enriched with ip-api.com fields when reachable
tornet --status            # shows IP Country / country name from get_ip_with_country (ipapi.co)
tornet --list-countries    # prints the 22-code countries dict + AUTO
tornet --country us        # pins US; get_country_name renders "United States" in status
```

Notes on the current behavior:

- `--status` geolocation comes from `get_ip_with_country()` (`https://ipapi.co/json/`),
  **not** from `get_ip_info()`; the latter is only reachable via `--ip --json`.
- An unknown `--country ZZ` is **not rejected** by the CLI: TorNet writes
  `ExitNodes {ZZ}` and lets Tor fail to satisfy the pin. Confirm the pin
  outcome with `tornet --status` rather than assuming validation.
- `tornet --status` still prints the raw IP when the geolocation API is
  unreachable — geolocation is never on the critical path.

## Alternatives considered

- **Bundle a local GeoIP database (MaxMind).** Rejected — adds a large data
  file and an update dependency for a diagnostic feature.
- **Hardcode country names only where needed.** Rejected — duplicates the map
  across functions; a single `list_countries()` keeps it consistent.
