# 03. Country selection

- **Status:** Published
- **Date:** 2026-08-23
- **Deciders:** @ByteBreach
- **Related:** [architecture/02-tor-integration.md](../architecture/02-tor-integration.md), [mechanisms/06-country-exitnodes.md](../mechanisms/06-country-exitnodes.md)

## Context

Users frequently want their exit traffic to originate from a specific country
— for geo-restricted content, compliance testing, or privacy strategy. TorNet
supports this via the `--country` flag, which pins the exit node to a
two-letter ISO 3166-1 alpha-2 country code.

## Usage

```bash
# Pin exit to Germany
tornet --country de

# List every supported country code
tornet --list-countries

# Reset to random exit country
tornet --restore-default
```

## How it works

`--country` writes a custom torrc snippet to `~/.tornet/torrc.custom`:

```
ExitNodes {DE}
StrictNodes 1
```

`StrictNodes 1` is mandatory — without it Tor treats `ExitNodes` as a soft
preference and may ignore it when no suitable relay exists. With it, Tor
refuses to build a circuit that does not use an exit node in the listed
country, making the pin enforceable.

TorNet then restarts the Tor service with the custom config and records the
choice in `~/.tornet/current_country`. See
[country exit nodes mechanism](../mechanisms/06-country-exitnodes.md) for the
full implementation.

## Caveats

- Not all countries have reliable exit nodes. Some will appear in
  `--list-countries` but yield no circuit.
- Pinning forces a full Tor restart; the first rotation after setting a country
  costs a complete circuit rebuild.
- `auto` (the default) means "use any available exit" — no config file is
  written and no restart occurs.

## Consequences

- Easier: geo-specific routing with a single flag.
- Harder: some countries are unreliable; pinning adds latency on first rotation.

## References

- [Tor integration](../architecture/02-tor-integration.md)
- [Country exit nodes mechanism](../mechanisms/06-country-exitnodes.md)
