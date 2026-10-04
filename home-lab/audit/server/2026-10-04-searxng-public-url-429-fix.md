---
tags: [homelab, incident, searxng, rate-limit, cloudflare]
---

# Incident Log — 2026-10-04

## SearXNG "refuses to respond" — public URL returning 429 to AI/API clients

**Symptom:** AI agents reported SearXNG "refusing to respond" to searches. Reproduced: any request to `https://search.panomete.com` from a non-browser client returned **HTTP 429 Too Many Requests**:
- `curl` default UA → 429
- Python urllib / AI tools / MCP clients → 429
- `format=json` API calls → 429
- Browser (Chrome UA) → **200** (masks the problem during casual testing)

The Tailscale path (`http://100.73.143.25:7004`) worked fine — which is why the Hermes AI profiles (all pointing at the Tailscale URL) were mostly unaffected, but anything using the public URL was refused.

## Root Cause

SearXNG's bot-detection limiter extracted the **true client IP** from `X-Forwarded-For` (the proxy chain Cloudflare → cloudflared → Nginx is trusted via `real_ip: x_for: 1` + the limiter's trusted_proxies). That public IP is never in the passlist — nor can it be — so every public-URL visitor got the full bot-protection treatment:

1. **`http_user_agent` check** — blocks non-browser User-Agents outright (curl/python/AI tools → 429)
2. **`API_WINDOW` limit** — `format=json` requests capped at **4 per hour** (API_MAX=4, hardcoded constant)
3. Additional `http_accept` / `http_sec_fetch` checks treated API-style headers as suspicious

Diagnosis path: Nginx debug endpoint showed the XFF chain (`REMOTE=127.0.0.1, XFF=<client public IPv6>`); comparison tests by User-Agent isolated the checks. The limiter's block messages are logged at **DEBUG** level (invisible), which is why the fresh 429s never appeared in `docker logs`.

## Fixes Applied

**1. Disabled the limiter** (`~/application/searxng/core-config/settings.yml`):

```yaml
server:
  limiter: false   # was: true
```

Rationale: this is a **private instance** (Tailscale + Cloudflare tunnel + `noindex` headers). SearXNG's docs recommend the limiter only for public instances; the bot checks were only hurting legitimate AI/API clients. Backup: `settings.yml.bak-limiter-20261004`.

**2. Disabled DuckDuckGo engines** (every request from this IP had been CAPTCHA'd for days — 17 CAPTCHAs in 24h, pure noise):

```yaml
  - name: duckduckgo
    disabled: true
  - name: duckduckgo images   # + news, videos
    disabled: true
```

Applied with `docker compose restart`.

## Verification (all real, post-fix)

| Test | Result |
|------|--------|
| Public URL, curl default UA | HTTP **200** (was 429) |
| Public URL, JSON search | **40 results, 1.35s, zero unresponsive engines** |
| Tailscale direct, JSON search | 36 results, 1.5s |
| MCP tool call (`mcp-searxng` v2.5.0, real stdio session) | **OK, 0.7s** |

## Takeaways

1. **For private instances, keep `limiter: false`.** The limiter is designed for public instances; behind a tunnel/Cloudflare it mostly produces false positives on legitimate API clients.
2. **Browser-UA testing hides these bugs** — always test with the client UA an AI actually uses (`curl` or the tool's own UA), not just a browser.
3. **Limiter blocks log at DEBUG level** — when puzzling over 429s, remember to check with `limiter: false` comparison or enable debug logging; the "PASS" (passlist) messages are WARNING level and visible, blocks are not.
4. **Passlist can't whitelist "the internet"** — if the service is meant to serve API clients through a public URL, per-IP bot protection and API-client usage are fundamentally at odds.

## Related

- [[2026-08-24-searxng-dns-outage-fix]] — previous SearXNG incident (DNS)
- [[db-network-integration-guide]] — how SearXNG was put on `db-network`
- Index: [[Homelab-Infra-Checklist]]
