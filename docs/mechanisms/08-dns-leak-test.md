# 08. DNS Leak Test

- **Status:** Published
- **Date:** 2026-08-23
- **Authors:** @ByteBreach
- **Related:** [usage/05-troubleshooting.md](../usage/05-troubleshooting.md)

## Context

Verify DNS goes via Tor.

## Mechanism

`dns_leak_test` fetches dnsleaktest.com via SOCKS5 proxy 127.0.0.1:9050.

## Implementation details

Uses requests proxies.

## Testing

Should return Tor exit IP.

## Alternatives considered

- **Local resolver check:** less reliable.
