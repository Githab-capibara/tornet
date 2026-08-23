# 07. Keep a standalone cross-distribution dependency checker in `utils.py`

- **Status:** Accepted
- **Date:** 2026-08-21
- **Deciders:** @ByteBreach
- **Related:** [mechanisms/04-auto-fix.md](../mechanisms/04-auto-fix.md), [mechanisms/05-dependency-checker.md](../mechanisms/05-dependency-checker.md), [adr/04-runtime-auto-fix.md](04-runtime-auto-fix.md)

## Context

`tornet/tornet.py` already contains `detect_package_manager()`,
`install_package()`, `ensure_pip()`, `ensure_requests()`, and `ensure_tor()`
inline — enough to satisfy the `--auto-fix` path. A second, parallel
implementation exists in `tornet/utils.py` that reads `/etc/os-release` for
distro detection, maps package managers to human-readable descriptions, and
exposes a `main()` that can be run directly
(`python -m tornet.utils`).

Carrying two implementations of the same logic risks drift, but `utils.py` is
more thorough (it consults `ID`/`ID_LIKE` from `os-release`, not just `which`)
and is runnable standalone before `tornet` itself is installed.

## Decision

Keep `tornet/utils.py` as a standalone, runnable dependency checker that can
bootstrap a box before `tornet` is importable. It is the authoritative
detection logic; `tornet.py`'s inline `ensure_*` helpers remain a thinner
runtime convenience for the `--auto-fix` path.

## Consequences

- **Easier:** a pre-install health check that works without importing the full
  CLI; richer distro detection than the inline path.
- **Harder:** two code paths doing similar work; any change to the package
  matrix must be mirrored in both files or the standalone checker drifts.
- **Given up:** a single source of truth for dependency logic.
- **Migration:** none; both files already coexist. Future work could have
  `tornet.py` delegate to `utils.py`, but that is out of scope here.

## Alternatives considered

- **Option A: delete `utils.py` and rely only on `tornet.py`.** Rejected
  because the inline detection is weaker and not runnable before install.
- **Option B: delete the inline helpers and route `--auto-fix` through
  `utils.py`.** Rejected because it couples a runtime command to the
  standalone module's `main()` exit semantics, and would require a larger
  refactor than this documentation pass.
