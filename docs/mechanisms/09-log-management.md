# 09. log management

- **Status:** Accepted
- **Date:** 2026-08-23
- **Deciders:** @ByteBreach
- **Related:** [usage/02-command-reference.md](../usage/02-command-reference.md), [architecture/03-configuration-layout.md](../architecture/03-configuration-layout.md)

## Context

Operators need to inspect what TorNet did after the fact, and to tail activity
live during long rotation runs. The log location must be stable:
`~/.tornet/tornet.log` (`LOG_FILE`).

## Mechanism

`tornet --log [--follow]` → `follow_logs(follow)`:

1. `os.makedirs(~/.tornet, exist_ok=True)`.
2. If `LOG_FILE` does not exist, create it with a header line:
   `TorNet Log File - Created <timestamp>`.
3. **Follow mode** (`--log --follow`): classic `tail -f` semantics — open the
   file, `seek(0, 2)` (jump to EOF), then loop `readline()` / print /
   `sleep(0.1)`; `KeyboardInterrupt` exits the loop cleanly.
4. **Plain mode** (`--log`): read and print the whole file; empty file prints
   "Log file is empty"; unreadable file exits with code 15.

## Implementation details

- Honest caveat: runtime output currently goes to stdout via the colored
  `log()/error()/warning()/info()` helpers and is **not** mirrored into
  `LOG_FILE`; today the tool itself only creates the header line. Treat
  `--log` as the viewer for anything written there (by future mirroring or by
  external tooling), and rely on stdout for current run output.
- Follow-mode poll interval is 100 ms — negligible CPU, no inotify dependency,
  works on any POSIX filesystem.
- The follow loop never re-opens the file; log rotation underneath it would
  require restarting `--log --follow`.

## Testing

```bash
tornet --log                    # expect header line (first run)
tornet --log --follow &         # start tail
echo "test" >> ~/.tornet/tornet.log   # line appears within ~0.1 s
kill %1                         # Ctrl-C also exits follow cleanly
```

## Alternatives considered

- **stdout only:** rejected — nothing persists between runs.
- **Python `logging` with RotatingFileHandler:** the right long-term fix for
  the stdout-mirroring caveat above; deferred until a release can migrate the
  print-based helpers.
