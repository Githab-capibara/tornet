# 11. Scheduled rotation

- **Status:** Published
- **Date:** 2026-08-26
- **Deciders:** @ByteBreach
- **Related:** [mechanisms/01-ip-rotation.md](01-ip-rotation.md), [usage/02-command-reference.md](../usage/02-command-reference.md)

## Context

Beyond per-N-seconds intervals (`--interval`), operators want calendar-style
periods — every five minutes, hourly, daily — without computing seconds by
hand. The schedule must compose with country pinning and JSON output exactly
like the ordinary loop.

## Mechanism

`tornet --schedule SPEC [--country C] [--json]` → `run_scheduled(schedule_str)`:

1. `parse_schedule()` converts the spec to seconds:

| Spec | Computation | Seconds |
|------|-------------|---------|
| `30s` | value | 30 |
| `5m` | value × 60 | 300 |
| `2h` | value × 3600 | 7200 |
| `1d` | value × 86400 | 86400 |

   Unknown unit suffix or non-numeric value → error exit 12.
2. Logs `Scheduled IP change every <spec>`.
3. Delegates to
   `change_ip_repeatedly(str(interval), count=0, country, json_output)` —
   i.e. the **infinite** rotation loop from
   [IP rotation](01-ip-rotation.md) at a fixed period.

## Implementation details

- Schedules are always fixed-period; randomized gaps are the domain of
  `--interval 30-120`. Combining both flags: `--schedule` wins because it is
  dispatched earlier in `main()` and never falls through to the interval loop.
- The conversion result is passed back as a string, so the loop re-parses it
  as a plain integer — a deliberate reuse that keeps one sleep/rotate path.
- Country pinning and JSON output pass through untouched (`args.country`,
  `args.json`).
- Like all long runs, SIGINT/SIGQUIT teardown applies
  ([signal handling](03-signal-handling.md)).

## Testing

```bash
tornet --schedule 1m --country de --json   # rotation every 60 s, JSON lines
tornet --schedule 7x                       # expect exit code 12 usage error
```

## Alternatives considered

- **cron integration:** rejected — external dependency on crontab semantics;
  in-process scheduling keeps teardown unified.
- **`schedule` library at runtime:** listed as a dependency but the shipped
  implementation uses the hand-rolled parser; adopting the library would be a
  superseding ADR.
