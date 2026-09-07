# 04. project principles

- **Status:** Accepted
- **Date:** 2026-08-24
- **Deciders:** @ByteBreach
- **Related:** [governance/01-contributing.md](01-contributing.md)

## Context

Project operates under explicit working principles to keep documentation, testing and git hygiene consistent across contributors.

## Decision

Maintain a canonical list of project principles covering documentation updates, testing, verification, GitHub usage and author attribution.

## Consequences

- **Easier:** onboarding and compliance checks become explicit.
- **Harder:** requires discipline to update principles when process changes.
- **Given up:** implicit tribal knowledge.
- **Migration:** none; this is the initial adoption.

## Alternatives considered

- **Option A: no formal principles.** Rejected because without explicit standards, documentation and testing quality drifts across contributors.
- **Option B: lengthy process document.** Rejected because concise principles are more memorable and actionable.

## Principles

1. **No laziness** — work at maximum capacity.
2. **Reconnaissance first** — always gather context before acting. Reconnaissance first, action second.
3. **Made changes? Update documentation!**
4. **Added a feature? Update documentation!**
5. **Made changes? Edit existing / write new tests!**
6. **Added a feature? Edit existing / write new tests!**
7. **Did something? Verify nothing is broken first!**
8. **Working with the system? Be maximally careful!**
9. **Working with GitHub? Use the `gh` command, it is already configured!**
10. **Making a commit? Always set the author to:**  
    Nick: `Githab-capibara`  
    Email: `rrrarrr37r@gmail.com`
11. **Writing documentation? Use the required styles:** ADR Michael Nygard format, Design Documents format, README table format, Main README with badges/hero/benchmark/diagrams.
12. **See documentation not in the required style? Fix it!**
