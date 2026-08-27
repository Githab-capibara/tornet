# 04. Auto fix

- **Status:** Published
- **Date:** 2026-08-23
- **Deciders:** @ByteBreach
- **Related:** [adr/04-runtime-auto-fix.md](../adr/04-runtime-auto-fix.md), [mechanisms/05-dependency-checker.md](05-dependency-checker.md)

## Context

TorNet depends on the Python packages `requests` (+SOCKS extras), `PyYAML`,
`schedule`, `stem`, and the system `tor` binary. Fresh-box installs frequently
hit `ImportError` or "tor not found" on first run. Silent installs behind the
user's back are a security hazard, so recovery must be an explicit opt-in.

## Mechanism

`tornet --auto-fix` → `auto_fix()`, which runs three steps in order:

1. `ensure_pip()`:
   - test `import pip`;
   - if missing, try `python -m ensurepip --upgrade`;
   - if that fails, install the distro pip package via
     `install_package()` — `python3-pip` (apt/dnf/yum/zypper),
     `python-pip` (pacman), `py3-pip` (apk).
2. `ensure_requests()`:
   - test `import requests`;
   - if missing, ensure pip, then
     `pip install requests requests[socks]`.
3. `ensure_tor()`:
   - `shutil.which("tor")`; if absent, `install_package("tor")`.

Every step exits with a dedicated code on failure (5/6/7) telling the user to
install manually.

## Implementation details

- Package-manager detection is `detect_package_manager()` — first binary found
  among apt/dnf/yum/pacman/apk/zypper; none → exit 4.
- All installs run through `run_cmd(..., use_sudo=True)`; if not root and no
  `sudo` binary exists → exit 2.
- Regular commands never auto-install. Missing tor → exit 10, missing
  `requests` → exit 11, both messages point at `--auto-fix`. This is the
  deliberate "explicit trigger only" policy from ADR-04.
- A more thorough standalone variant of the same logic lives in
  [mechanisms/05-dependency-checker.md](05-dependency-checker.md) and can bootstrap before TorNet is even
  installed.

## Testing

On a clean container without `tor`:

```bash
tornet --auto-fix        # installs pip/requests/tor per detected distro
tor --version            # expect a version string
python3 -c "import requests, socks"   # expect success
```

Also verify a normal command still refuses to install anything when
dependencies are missing (exit 10/11, no package-manager side effects).

## Alternatives considered

- **Auto-install on every run:** rejected — silent privileged mutation is a
  security anti-pattern.
- **Hard-fail with no recovery path:** rejected — the six-distro matrix makes
  manual recovery painful for non-expert users.
