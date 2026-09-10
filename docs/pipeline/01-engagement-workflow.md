# 01. Engagement Workflow

- **Status:** Accepted
- **Date:** 2026-09-10
- **Deciders:** @ByteBreach
- **Related:** [02-ci-gate-and-quality-tiers.md](02-ci-gate-and-quality-tiers.md), [03-agent-orchestration.md](03-agent-orchestration.md), [adr/01-record-architecture-decisions.md](../adr/01-record-architecture-decisions.md)
- **Authors:** @Githab-capibara

## Context

TorNet is a single-operator project maintained through GitHub. Contributions
arrive as issues, feature requests, and pull requests. The project keeps a
small, change-averse surface: every PR must stay consistent with the ADR set,
the documentation hierarchy in `docs/`, and the dual-installer packaging in
[adr/05-dual-installer.md](../adr/05-dual-installer.md). Without a written
workflow, "quick fixes" drift out of scope and documentation rot sets in.

## Process

1. **Issue intake.**
   - Bug reports must include the failing command, exit code, and `tornet --version`.
   - Feature requests must state the rotation/reliability problem they solve.
2. **Triage against ADRs.**
   - If the change touches routing, install, signal handling, or packaging,
     it must be reflected in the relevant ADR before code review (see
     [adr/01-record-architecture-decisions.md](../adr/01-record-architecture-decisions.md)).
3. **Branch, change, verify.**
   - A feature branch is opened from `main`.
   - Every code change ships with a docs update and a test update
     (repository rules, enforced in review).
4. **Pull request.**
   - Reference the issue and the affected ADRs.
   - Summary must list: code path changed, doc files touched, test files touched.
5. **Merge.**
   - Merged only when the docs build passes and the quality tiers in
     [02-ci-gate-and-quality-tiers.md](02-ci-gate-and-quality-tiers.md) are met.

## Implementation details

- GitHub CLI (`gh`) is the sanctioned way to interact with the remote —
  issues, PRs, checks.
- Commits are authored as `Githab-capibara <rrrarrr37r@gmail.com>`.
- The `main` branch is the single source of truth; releases are tagged from it.
- Documentation changes are never committed separately from the code they
  describe; the review gate rejects doc-less code changes.

## Testing

- Contributor: open a PR, confirm the ReadTheDocs preview builds, and confirm
  `python -m pytest` (when tests exist for the affected module) is green.
- Maintainer: verify the PR touches `docs/` and `tests/` for every source
  change reported in the summary.

## References

- [adr/01-record-architecture-decisions.md](../adr/01-record-architecture-decisions.md)
- [02-ci-gate-and-quality-tiers.md](02-ci-gate-and-quality-tiers.md)
- [04-workflow-deep-dive.md](04-workflow-deep-dive.md)