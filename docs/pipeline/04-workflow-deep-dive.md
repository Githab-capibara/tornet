# 04. Workflow Deep Dive

- **Status:** Accepted
- **Date:** 2026-09-10
- **Deciders:** @ByteBreach
- **Related:** [01-engagement-workflow.md](01-engagement-workflow.md), [02-ci-gate-and-quality-tiers.md](02-ci-gate-and-quality-tiers.md), [03-agent-orchestration.md](03-agent-orchestration.md)
- **Authors:** @Githab-capibara

## Context

The high-level engagement workflow (document 01) and the quality tiers
(document 02) describe *what* must happen. This document walks through a
concrete contribution end to end with exact commands and decision points, so a
contributor or agent can follow it mechanically.

## Process

### Stage 1 — Issue → branch

```bash
gh issue list --state open          # pick or file an issue
gh issue view <N>                   # confirm scope: command, exit code, version
git checkout -b fix/<slug>          # branch from main
```

Decision point: does the change touch routing, install, signals, or
packaging? If yes, re-read the matching ADR first
(`docs/adr/02…07`); the PR must note the ADR already covers it.

### Stage 2 — Change + docs + tests (one commit)

```bash
vim tornet/tornet.py                # the actual change
vim docs/mechanisms/NN-*.md         # doc parity (rule: docs with code)
vim tests/NN-*.py                   # test parity (rule: tests with code)
```

Rule of thumb: if a mechanism doc already exists for the touched function,
edit it in the same commit; if no doc exists, create one numbered at the end
of the folder.

### Stage 3 — Self-verification

```bash
python -m py_compile tornet/tornet.py tornet/utils.py
tornet --status                     # smoke the touched path
python -m tornet.utils              # standalone checker baseline
python -m pytest                    # when tests exist for the module
```

### Stage 4 — Local docs build

```bash
python -m sphinx -b html docs /tmp/tornet-docs   # must pass clean
```

ReadTheDocs runs the same build on push; a failing docs build blocks merge
(see document 02).

### Stage 5 — PR and merge

```bash
git commit -m "fix/<slug>: <what changed>"
# author: Githab-capibara <rrrarrr37r@gmail.com>
git push -u origin fix/<slug>
gh pr create --title "…" --body "…"   # references issue + ADRs
gh pr view --web                       # check the docs build status
gh pr merge --squash                   # only after gate is green
```

## Implementation details

- Merge is squash-only to keep `main` linear and bisectable.
- The commit body must list the three touched surfaces: code, docs, tests.
- Any off-style documentation spotted during review is fixed in the same PR
  (repository rule 12: "docs not in the required style? fix it").
- The standalone checker (`python -m tornet.utils`) is the tie-breaker for
  install/dependency disputes — it is intentionally independent of the main
  CLI.

## Testing

Follow Stage 3–4 verbatim on a branch that touches `tornet/tornet.py` and
confirm: compile check passes, smoke command runs, standalone checker exits 0,
local Sphinx build finishes without warnings.

## References

- [01-engagement-workflow.md](01-engagement-workflow.md)
- [02-ci-gate-and-quality-tiers.md](02-ci-gate-and-quality-tiers.md)
- [03-agent-orchestration.md](03-agent-orchestration.md)
- [`docs/mechanisms/`](../mechanisms/README.md) — per-function ground truth