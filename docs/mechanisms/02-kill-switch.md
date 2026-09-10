# 02. Kill Switch

- **Status:** Accepted
- **Date:** 2026-08-23
- **Deciders:** @ByteBreach
- **Related:** [adr/03-kill-switch-iptables.md](../adr/03-kill-switch-iptables.md), [architecture/01-system-overview.md](../architecture/01-system-overview.md)
- **Authors:** @Githab-capibara

## Context

If the Tor circuit drops while traffic keeps flowing outside Tor, the real IP
leaks. A kill switch blocks everything that does not go through Tor, and must
be toggleable on demand and cleanly removable — without clobbering rules the
user already has.

## Mechanism

`tornet --kill-switch` calls `toggle_kill_switch()`, an idempotent toggle:

**State detection:** `iptables -L`; if the output contains
`TORNET-KILLSWITCH`, the switch is ON → disable path. Otherwise enable path.

**Enable** (chain created, then jumped to from `OUTPUT`):

```
iptables -N TORNET-KILLSWITCH
iptables -A TORNET-KILLSWITCH -d 127.0.0.1/8     -j ACCEPT
iptables -A TORNET-KILLSWITCH -d 192.168.0.0/16  -j ACCEPT
iptables -A TORNET-KILLSWITCH -d 172.16.0.0/12   -j ACCEPT
iptables -A TORNET-KILLSWITCH -d 10.0.0.0/8      -j ACCEPT
iptables -A TORNET-KILLSWITCH -p tcp --dport 9050 -j ACCEPT
iptables -A TORNET-KILLSWITCH -j DROP
iptables -A OUTPUT -j TORNET-KILLSWITCH
```

Result: loopback, RFC 1918 private ranges, and TCP to the Tor SOCKS port
(9050) pass; everything else outbound drops.

**Disable** (exact reverse):

```
iptables -D OUTPUT -j TORNET-KILLSWITCH   # remove the jump
iptables -F TORNET-KILLSWITCH             # flush the chain
iptables -X TORNET-KILLSWITCH             # delete the chain
```

## Implementation details

- Guards, in order: `shutil.which("iptables")` missing → exit 13;
  not running as root (`os.geteuid() != 0`) → exit 14.
- Commands run with `use_sudo=False` — root is already required, so no
  `sudo` prefix is added.
- Linux-only by construction; Windows/Android builds have no kill switch.
- The named chain makes state auditable: `iptables -L TORNET-KILLSWITCH`.

## Testing

1. `sudo tornet --kill-switch` → expect "Kill switch enabled".
2. `curl https://api.ipify.org` → must hang/fail (blocked);
   `curl --socks5 127.0.0.1:9050 https://api.ipify.org` → works.
3. `sudo tornet --kill-switch` again → disabled; ordinary traffic restored.
4. Re-run twice in either state — no duplicated rules, no leftovers.

## Alternatives considered

- **Append DROP rules directly to `OUTPUT`:** rejected — hard to find/remove,
  risks leaving the host firewalled shut.
- **nftables:** rejected — less universal on the older distros TorNet targets.
