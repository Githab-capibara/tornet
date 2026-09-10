# 03. Agent Orchestration

- **Status:** Accepted
- **Date:** 2026-09-10
- **Deciders:** @ByteBreach
- **Related:** [01-engagement-workflow.md](01-engagement-workflow.md), [04-workflow-deep-dive.md](04-workflow-deep-dive.md)
- **Authors:** @Githab-capibara

## Context

Maintenance of TorNet is increasingly delegated to AI coding agents. An
undisciplined agent can silently mutate `tornet/tornet.py` without updating
the corresponding mechanism doc, or rewrite `README.md` licensing claims, or
close an issue without a commit. The project codifies the agent contract in
`AGENTS.md` at the repository root; this document explains how that contract
is orchestrated on multi-step tasks.

## Process

Agent runs follow a fixed pipeline of principles (all defined in
`AGENTS.md`):

1. **Recon first, act second.** Every task starts with reading the affected
   code and docs before any edit.
2. **Docs parity.** Any change to behavior or features must be mirrored in
   `docs/` in the same commit; doc-only drift is a review failure.
3. **Test parity.** Any change to behavior or features must add or adapt a
   test in the same commit.
4. **Self-verification.** After any change, the agent must confirm nothing
   broke — run the affected path, not just a syntax check.
5. **Style discipline.** Documentation follows the mandated ADR/README styles
   (Michael Nygard for ADRs, table-driven READMEs) — an agent that produces
   off-style docs must fix them (rule 12).
6. **Accountability.** GitHub interactions go through `gh`; commits are
   authored as `Githab-capibara <rrrarrr37r@gmail.com>`.

## Implementation details

- `AGENTS.md` is the machine-readable contract: rules 1–12 are mandatory, not
  advisory; rule 7 ("work at maximum", "recon first") is the entry point for
  every session.
- Multi-step tasks are decomposed into a TODO list first, then executed
  sequentially with a status update per item.
- The docs tree in `docs/` is the ground truth for mechanism coverage:
  every function in `tornet/tornet.py` and `tornet/utils.py` is expected to
  appear in exactly one mechanism document.

## Testing

- Assign an agent a feature flag addition and verify the resulting commit
  contains: code change + mechanism doc update + test update, in one commit.
- Assign an agent a pure documentation task and verify it edits only `docs/`
  and never touches `tornet/`.

## References

- Repository root `AGENTS.md` (the contract itself)
- [01-engagement-workflow.md](01-engagement-workflow.md)
- [04-workflow-deep-dive.md](04-workflow-deep-dive.md)