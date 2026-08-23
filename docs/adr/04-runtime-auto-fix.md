# 04. Install missing dependencies at runtime behind an explicit `--auto-fix` flag

- **Status:** Accepted
- **Date:** 2026-08-21
- **Deciders:** @ByteBreach
- **Related:** [mechanisms/04-auto-fix.md](../mechanisms/04-auto-fix.md), [adr/07-cross-distro-checker.md](07-cross-distro-checker.md)

## Context

TorNet depends on `requests`, `PySocks`, `PyYAML`, `schedule`, and `stem`, plus
the system `tor` binary. Users frequently install TorNet with `pip` on a fresh
box and hit `ImportError` or "tor not found" on first run. Hard-failing there
creates a poor first experience, but silently installing system packages and
pip dependencies behind the user's back is a security and reproducibility
hazard.

## Decision

Provide an explicit `tornet --auto-fix` command that, when invoked, installs
pip if missing, then `requests` (+ `requests[socks]`), then the `tor` system
package via the detected package manager. Regular commands never auto-install
anything; they only fail with a message pointing to `--auto-fix`.

## Consequences

- **Easier:** one command recovers a broken install without the user needing
  to know which dependency is missing.
- **Harder:** auto-fix runs package-manager commands with `sudo`, which is a
  privileged, side-effectful operation the user must consciously trigger.
- **Given up:** "just works" zero-config installation — by design, installs
  require an opt-in.
- **Migration:** none; existing implementation in `auto_fix()` and the
  `ensure_*` helpers.

## Alternatives considered

- **Option A: auto-install on every run.** Rejected because silent `sudo` and
  package-manager mutation is a security anti-pattern and breaks reproducible
  environments.
- **Option B: hard-fail only, no auto-fix.** Rejected because the
  cross-distro install matrix (apt/dnf/yum/pacman/apk/zypper) makes manual
  recovery painful for non-expert users.
