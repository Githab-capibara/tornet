# 13. JSON Output

- **Status:** Accepted
- **Date:** 2026-08-26
- **Deciders:** @ByteBreach
- **Related:** [usage/02-command-reference.md](../usage/02-command-reference.md), [mechanisms/01-ip-rotation.md](01-ip-rotation.md)
- **Authors:** @Githab-capibara

## Context

Wrappers and automation need stable, parseable lines instead of ANSI-colored
prose. Every result-bearing command should be scriptable without regex
scraping.

## Mechanism

`tornet ... --json` switches three surfaces from text to one-line JSON:

**`--ip --json`** — enriched lookup:

```json
{"ip": "185.x.x.x"}
```

plus, when `http://ip-api.com/json/<ip>` answers with `status == "success"`,
its fields (country, city, isp, ...) are merged into the same object.

**`--change --json`** — success:

```json
{"action": "ip_change", "timestamp": 1724700000.0, "ip": "51.x.x.x"}
```

failure:

```json
{"action": "ip_change", "timestamp": 1724700000.0, "error": "Failed to change IP"}
```

**Rotation loop** (`--interval/--count/--schedule` with `--json`) — one object
per successful rotation, printed after each iteration:

```json
{"timestamp": 1724700000.0, "ip": "91.x.x.x"}                  // count == 0 (infinite)
{"timestamp": 1724700000.0, "ip": "199.x.x.x", "count": 3}     // finite runs add 1-based counter
```

## Implementation details

- In a default run the ASCII banner is printed **only** when `--json` is off,
  so piped stdout stays pure JSON.
- `timestamp` values are `time.time()` epoch floats — sort-safe across lines.
- Failed rotations print nothing in loop mode (only successes emit objects);
  `--change` is the only surface with an explicit error object.
- Warnings/errors from helpers remain colored stderr/stdout text — they are
  not part of the JSON contract yet.
- Not covered by `--json` today: `--status`, `--list-countries`,
  `--dns-leak-test`, kill switch, log views. Extension points are noted in
  [12-status-monitoring](12-status-monitoring.md).

## Testing

```bash
tornet --change --json | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['action']=='ip_change' and 'ip' in d"
tornet --interval 5 --count 2 --json | wc -l     # expect exactly 2 JSON lines
tornet --ip --json | jq .country                 # merged ip-api field
```

## Alternatives considered

- **A `--output-format {text,json}` subcommand family:** rejected for now —
  one boolean flag covers every currently supported surface.
- **NDJSON envelope with event types:** premature; revisit when status and
  diagnostics gain JSON support.
