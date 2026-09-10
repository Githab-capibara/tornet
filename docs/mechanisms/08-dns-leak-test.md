# 08. DNS Leak Test

- **Status:** Accepted
- **Date:** 2026-08-23
- **Deciders:** @ByteBreach
- **Related:** [usage/05-troubleshooting.md](../usage/05-troubleshooting.md), [architecture/02-tor-integration.md](../architecture/02-tor-integration.md)
- **Authors:** @Githab-capibara

## Context

The classic leak scenario: traffic rides Tor but DNS resolution escapes to the
ISP resolver, exposing every domain visited. Operators need an in-tool check
that the Tor SOCKS path actually carries requests end-to-end.

## Mechanism

`tornet --dns-leak-test` → `dns_leak_test()` fetches three well-known
leak-check sites through the Tor SOCKS5 proxy:

| Test URL | Purpose |
|----------|---------|
| `https://dnsleaktest.com` | dedicated leak test service |
| `https://ipleak.net` | combined IP+DNS+WebRTC checks |
| `https://www.dnsleaktest.com` | canonical host variant |

For each URL it issues `requests.get(url, proxies=..., timeout=10)` with:

```python
proxies = {
    'http':  'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050',
}
```

HTTP 200 prints "Accessible via Tor ✓"; any non-200 or exception prints
"✗". A closing hint advises running the browser-level test at
dnsleaktest.com while proxied through Tor.

## Implementation details

- Requires `requests[socks]` (PySocks); a plain `requests` install raises on
  the `socks5://` scheme — `--auto-fix` installs the extra.
- The check proves HTTPS-through-SOCKS works; it does **not** by itself prove
  that your browser's resolver uses Tor. For resolver-level proof, open the
  standard/extended test at dnsleaktest.com in a browser configured per the
  root README (SOCKS v5 + "Proxy DNS when using SOCKS v5").
- Failures print per-URL and never abort the run.

## Testing

With Tor running:

```bash
tornet --dns-leak-test        # expect three ✓ lines
sudo systemctl stop tor && tornet --dns-leak-test   # expect ✗ lines
```

Then the browser test above for full resolver verification.

## Alternatives considered

- **Querying a wildcard subdomain and sniffing the authoritative server:**
  rejected — requires controlling a domain; overkill for a CLI self-check.
- **Comparing system-resolver answers vs Tor-side answers locally:**
  rejected — less reliable signal than the established public services.
