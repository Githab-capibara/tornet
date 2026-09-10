# 02. CI Gate and Quality Tiers

- **Status:** Accepted
- **Date:** 2026-09-10
- **Deciders:** @ByteBreach
- **Related:** [01-engagement-workflow.md](01-engagement-workflow.md), [adr/07-cross-distro-checker.md](../adr/07-cross-distro-checker.md)
- **Authors:** @Githab-capibara

## Context

TorNet is a POSIX CLI whose installed surface spans six package managers and
three Python runtimes. A merged PR that breaks `--change` for one distro is
only discovered by users weeks later. The project needs a cheap, honest gate:
it cannot afford a full VM matrix per push, so it selects checks by blast
radius.

## Process

Blast radius is the set of users affected by a broken change:

| Radius | Example change | Gate required |
|--------|----------------|---------------|
| **S** — single path | Help text, banner, log wording | Local run of the touched command |
| **M** — one subsystem | Rotation loop, status panel, JSON output | Local run + manual smoke of `--status`, `--change --json` |
| **L** — install/signals | `--auto-fix`, kill switch, signal handling | `python -m tornet.utils` checker + clean-container test |
| **XL** — packaging/distro | Installers, cross-distro checker | Full ADR review + checker matrix per [adr/07](../adr/07-cross-distro-checker.md) |

Every PR goes through the automatic gate first, then the tier-by-radius review:

1. **Automatic gate (CI).**
   - ReadTheDocs build of `docs/` (configuration in `readthedocs.yaml`,
     `docs/conf.py`) must pass — a broken docs build blocks merge.
   - Python syntax/lint pass over `tornet/*.py` (compile check).
2. **Tiered review.**
   - S/M changes: reviewed together with their docs diff.
   - L/XL changes: additionally gated by the standalone checker
     (`python -m tornet.utils`) which bootstraps a peer review of the
     dependency chain.

## Implementation details

- The CI surface today is intentionally minimal: a Sphinx docs build on
  ReadTheDocs (`readthedocs.yaml`) plus local verification. There is no
  GitHub Actions workflow — see [04-workflow-deep-dive.md](04-workflow-deep-dive.md)
  for what the gate consists of on the maintainer side.
- Quality tiers map to the ADR set: routing changes must touch
  [adr/02](../adr/02-newnym-via-control-port.md), kill switch
  [adr/03](../adr/03-kill-switch-iptables.md), auto-fix
  [adr/04](../adr/04-runtime-auto-fix.md), packaging
  [adr/05](../adr/05-dual-installer.md), signals
  [adr/06](../adr/06-signal-cleanup.md), cross-distro
  [adr/07](../adr/07-cross-distro-checker.md).

## Testing

- Push a branch with a deliberately broken docs link; the ReadTheDocs build
  must fail before merge is possible.
- For an XL-radius change, run
  `python -m tornet.utils` on a clean container and confirm the checker
  reports exit 0 plus a valid package-manager/tor baseline.

## References

- [01-engagement-workflow.md](01-engagement-workflow.md)
- [04-workflow-deep-dive.md](04-workflow-deep-dive.md)
- [adr/07-cross-distro-checker.md](../adr/07-cross-distro-checker.md)