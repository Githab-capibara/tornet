# 01. Getting Started

- **Status:** Accepted
- **Date:** 2026-08-23
- **Deciders:** @ByteBreach
- **Related:** [usage/02-command-reference.md](02-command-reference.md)
- **Authors:** @Githab-capibara

## Context

New users need a fast path from install to first IP change. This guide assumes
you are on a supported platform (Linux recommended; Windows and Android builds
are in progress). Tor must be installed on the system before TorNet can rotate
your IP.

## Prerequisites

- Python 3.6+
- `tor` binary in PATH (install via your distro's package manager, e.g.
  `apt install tor`, `dnf install tor`)
- A user account that can read the Tor control auth cookie (on Debian-family
  systems, membership in the `debian-tor` group is sufficient for routine
  rotations)

## Usage

### Install

```bash
pip install tornet==2.0.2
```

### First IP change

```bash
tornet --ip           # show your current exit IP
tornet --change       # rotate to a new IP once
```

If any dependencies are missing, run:

```bash
tornet --auto-fix
```

This installs `pip` (if absent), `requests[socks]`, and the system `tor`
package — then exits so you can re-run the command above.

## How it works

`--ip` reads your current exit IP through the Tor SOCKS proxy at
`127.0.0.1:9050` (or directly when Tor is off). `--change` rotates the circuit
by sending `NEWNYM` over the Tor control port — no restart, no `sudo` in the
common case — then reads the new IP back. For the full walkthrough, see
[IP rotation mechanism](../mechanisms/01-ip-rotation.md).

## Caveats

- Tor must be installed first (`tornet --auto-fix` or your distro's package
  manager); a fresh box needs this step before `--change` will work.
- Kill-switch operations require root (`sudo tornet --kill-switch`); plain
  rotations usually do not.
- Windows and Android builds are in progress — today the install path is the
  Linux `pip` package.

## What's next?

- Full flag reference → [Command Reference](02-command-reference.md)
- How rotation works under the hood → [IP rotation mechanism](../mechanisms/01-ip-rotation.md)
- Country pinning → [Country selection](03-country-selection.md)

## Consequences

- **Easier:** five-minute onboarding from a clean box.
- **Harder:** requires `tor` to be installed (or `--auto-fix` to run first).
- **What it leaves open:** GUI onboarding — CLI is the only path today.

## References

- [Command Reference](02-command-reference.md)
- [IP Rotation mechanism](../mechanisms/01-ip-rotation.md)
