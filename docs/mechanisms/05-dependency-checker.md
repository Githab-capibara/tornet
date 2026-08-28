# 05. Dependency checker

- **Status:** Accepted
- **Date:** 2026-08-23
- **Deciders:** @ByteBreach
- **Related:** [adr/07-cross-distro-checker.md](../adr/07-cross-distro-checker.md), [mechanisms/04-auto-fix.md](04-auto-fix.md)

## Context

Before TorNet is installed there is no CLI to fix anything. Operators need a
standalone health check that works with nothing but Python 3 present, detects
the distribution properly (not just "which binaries exist"), and can bring the
box up to spec.

## Mechanism

`tornet/utils.py` is runnable directly (`python -m tornet.utils`). Its
`main()` pipeline:

1. `check_python3()` — `python3` in PATH, else exit 8.
2. `detect_package_manager()` returns `(manager, human description)`:
   - parse `/etc/os-release` into a dict (`read_os_release()`, strips quotes);
   - pass 1: match `ID` or `ID_LIKE` against known families, confirm the
     manager binary actually exists;
   - pass 2 (fallback): first existing binary among
     apt / dnf / yum / pacman / apk / zypper;
   - neither → `(None, None)` and the run continues with `ensurepip` only.
3. `ensure_pip(pm)` — import test, else distro pip package, else `ensurepip`;
   then upgrades pip itself.
4. `ensure_requests()` — import test, else `pip install requests`, then always
   ensures `requests[socks]`.
5. `ensure_tor(pm)` — `which("tor")`, else `install_system_package(pm, "tor")`,
   verify again, else exit 7.

## Implementation details

- Distinction vs the inline helpers in `tornet.py`: `utils.py` consults
  `ID`/`ID_LIKE` from os-release (so Fedora-like derivatives resolve to dnf,
  Arch-likes to pacman, etc.) while the inline path is `which()`-only.
- Package name maps live as module-level dicts: `PIP_SYSTEM_PACKAGES`
  (`python3-pip` / `python-pip` / `py3-pip`) and `TOR_PACKAGE_NAMES`
  (all `"tor"` today).
- `run_cmd()` mirrors the main tool's sudo semantics: prepends `sudo` when not
  root, exit 2 if sudo is missing; logs every executed command to stderr.
- Exit codes: 2 (no sudo), 3 (missing required binary), 4 (ensurepip failed),
  5 (unknown package manager), 6 (cannot install tor, no manager), 7 (tor
  still missing after install), 8 (no python3).
- KeyboardInterrupt during the standalone run exits 130.

## Testing

```bash
python -m tornet.utils                 # full check on any supported distro
python -c "from tornet.utils import read_os_release as r; print(r())"
```

Verify on at least one Debian-family and one RPM-family image that the
reported manager matches `ID`/`ID_LIKE`, not merely PATH order.

## Alternatives considered

- **Delete `utils.py`, keep inline only:** rejected — weaker detection and not
  runnable pre-install (ADR-07).
- **Route runtime `--auto-fix` through this module:** deferred — couples the
  CLI to standalone `main()` exit semantics; possible future refactor.
