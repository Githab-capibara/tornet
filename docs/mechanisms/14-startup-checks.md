# 14. startup checks

- **Status:** Accepted
- **Date:** 2026-08-26
- **Deciders:** @ByteBreach
- **Related:** [mechanisms/10-service-detection.md](10-service-detection.md), [mechanisms/04-auto-fix.md](04-auto-fix.md)

## Context

Every invocation walks a gate sequence before doing real work. Operators and
contributors need to know exactly what runs, in what order, and which exit
code each failure produces — so failures are diagnosable without reading
`main()`.

## Mechanism

Ordering inside `main()` for any command that reaches the rotation path
(single-shot commands like `--stop` dispatch earlier and skip these gates):

1. **Signal registration** — SIGINT/SIGQUIT handlers first
   ([signal handling](03-signal-handling.md)).
2. **Config load** — `load_config(args.config or ~/.tornet/config.yml)`
   ([config management](07-config-management.md)).
3. **Tor present?** — `is_tor_installed()` false → error exit 10, message
   suggests manual install or `--auto-fix`.
4. **requests importable?** — ImportError → error exit 11, message points to
   `--auto-fix`.
5. **Internet reachable?** — `check_internet_connection()` does an HTTP GET to
   `http://www.google.com` with a 5 s timeout; failure → error exit 9.
6. **Banner** — skipped entirely when `--json` is set.
7. **Environment init** — `initialize_environment()`: if Tor is not running,
   start it via `service_action("start")`; prints proxy hint
   (`127.0.0.1:9050`).
8. Settle delay — `time.sleep(5)` for bootstrap before the first rotation.

## Privilege model

| Helper | Behavior |
|--------|----------|
| `is_root()` | true iff `os.geteuid() == 0` |
| `has_sudo()` | true iff `sudo` binary exists in PATH |
| `run_cmd(cmd, use_sudo=True)` | prepends `sudo` only when not root; neither root nor sudo available → error exit 2 |

Consequences: routine NEWNYM rotations need **no privileges** (cookie auth);
service actions and package installs escalate transparently; the kill switch
additionally hard-requires root itself (exit 14).

## Implementation details

- Exit-code map for this phase: 2 (no sudo), 9 (no internet), 10 (no tor),
  11 (no requests) — each message names the remedy.
- The internet probe is plaintext HTTP to a well-known host purely as a
  connectivity canary; it is not routed through Tor.
- The 5 s settle sleep is unconditional — even an already-bootstrapped Tor
  pays it once per run.

## Testing

```bash
PATH=/usr/bin:/bin tornet --interval 60        # tor hidden -> exit 10
systemctl stop tor && tornet --interval 60     # auto-start path, then rotates
unshare -n tornet --interval 60                # offline -> exit 9
```

## Alternatives considered

- **Delegating gates to `--auto-fix` automatically:** rejected — violates the
  explicit-trigger policy of ADR-04.
- **Skipping the settle sleep when circuits exist:** possible optimization;
  requires control-port bootstrap-state queries — candidate future ADR.
