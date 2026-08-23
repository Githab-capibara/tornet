# 05. Ship both `setup.py` and `pyproject.toml` as install sources

- **Status:** Accepted
- **Date:** 2026-08-21
- **Deciders:** @ByteBreach
- **Related:** [architecture/03-configuration-layout.md](../architecture/03-configuration-layout.md)

## Context

TorNet declares the same metadata (name, version, dependencies, entry point,
classifiers) in both `pyproject.toml` and `setup.py`. Modern Python packaging
has converged on `pyproject.toml` with a PEP 517 backend, but some older tooling
and install environments still invoke `python setup.py ...` directly and ignore
`pyproject.toml`.

## Decision

Keep both files as sources of truth. `pyproject.toml` is the primary, PEP 517
install path (`pip install .`); `setup.py` remains as a fallback for legacy
invocation. Both declare `2.0.2` and the same `tornet=tornet.tornet:main`
console script.

## Consequences

- **Easier:** maximum install compatibility across old and new pip/setuptools.
- **Harder:** version bumps and dependency changes must be applied in two
  places — drift between the files is a real risk.
- **Given up:** the cleanliness of a single declarative source.
- **Migration:** none; this is the current state. If legacy `setup.py` support
  is ever dropped, that should land as a superseding ADR.

## Alternatives considered

- **Option A: `pyproject.toml` only.** Rejected at this time because it would
  break users on very old pip versions that TorNet's `python_requires>=3.6`
  audience may still run.
- **Option B: `setup.py` only.** Rejected because it forgoes the modern build
  backend declaration and PEP 517 isolation.
