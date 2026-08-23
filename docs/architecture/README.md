# Architecture

This directory documents the **structure** of TorNet: what the components are,
how they fit together, and where state lives on disk. It is the "how the system
is built" companion to [`mechanisms/`](../mechanisms/) ("how each feature works")
and [`adr/`](../adr/) ("why the decisions were made").

## Contents

| Document | Purpose |
|----------|---------|
| [01-system-overview.md](01-system-overview.md) | Components, data flow, and the rotation loop |
| [02-tor-integration.md](02-tor-integration.md) | SOCKS proxy, control port, and country exit nodes |
| [03-configuration-layout.md](03-configuration-layout.md) | `~/.tornet/` layout, config files, and the dual installer |

Use [`template.md`](template.md) as the starting point for a new architecture
document.
