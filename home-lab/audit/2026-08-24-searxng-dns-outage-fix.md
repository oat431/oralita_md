---
tags: [homelab, incident, dns, searxng, adguard]
---

# Deployment Log — 2026-08-24

## Incident: SearXNG returning zero search results

**Symptom:** `searxng_web_search` (via MCP) returned "No results found" for every query, including trivial ones. `/search?format=json` showed all engines (bing, duckduckgo, google, google cse, mojeek, wikipedia, yandex) in `unresponsive_engines` with `"HTTP connection error"`.

## Root Cause — two compounding bugs

### Bug 1: `db-network` containers had zero external DNS

The host's `/etc/resolv.conf` was a **dangling symlink** → `../run/systemd/resolve/stub-resolv.conf`, but `systemd-resolved` is disabled on this host (intentionally — see [[adguard]], it needs port 53 free for AdGuard). Nothing regenerated the stub file, so the symlink target didn't exist.

Docker reads the host's resolver config when a container joins a **user-defined network** (like `db-network`) to seed that container's embedded DNS forwarder (`127.0.0.11`). With no usable host config, it wrote:

```
# NO EXTERNAL NAMESERVERS DEFINED
```

into every `db-network` container's `/etc/resolv.conf` — internal container-name resolution (`postgres`, `valkey`, etc.) still worked fine, but **any external hostname lookup failed silently**. This affects every container on `db-network`, not just SearXNG — it just happened to surface here first because SearXNG is the only one making outbound HTTP calls to arbitrary external hosts.

### Bug 2: AdGuard's only upstream was failing

Independently, AdGuard's `upstream_dns` had a single entry (`https://dns10.quad9.net/dns-query`) with no fallback. Its logs showed repeated:

```
dnsproxy: exchange failed upstream=https://dns10.quad9.net:443/dns-query ... err="exchanging: ... unexpected EOF"
```

So even after fixing Bug 1, anything resolving through AdGuard as its DNS server was still one flaky upstream away from failing LAN-wide.

**Red herring during diagnosis:** testing with `dig www.google.com @127.0.0.1` kept returning `0.0.0.0` even after both bugs were fixed. That's not a bug — AdGuard's query log showed a real filter rule match (`||google.com^`, FilterListID `1787523486`, `IsFiltered: true`). Intentional block, unrelated to this incident. Test with a neutral domain (`example.com`, `www.bing.com`) instead of `google.com` when diagnosing DNS on this LAN.

## Fixes Applied

**1. SearXNG — explicit DNS in compose (defense in depth):**

`~/application/searxng/docker-compose.yml`, service `core`:
```yaml
    dns:
      - 1.1.1.1
      - 9.9.9.9
```
Backup: `docker-compose.yml.bak-predns-20260824`. Applied with `docker compose up -d` (recreates the container).

**2. AdGuard — added fallback upstream:**

`AdGuardHome.yaml` (`dns_adguard-conf` volume), `upstream_dns`:
```yaml
upstream_dns:
  - https://dns10.quad9.net/dns-query
  - https://dns.cloudflare.com/dns-query   # added
```
Backup: `AdGuardHome.yaml.bak-20260824`. Applied with `docker restart adguard`.

**3. Host — replaced the dangling `/etc/resolv.conf` symlink with a static file (the actual root-cause fix):**

```
# Static resolv.conf — systemd-resolved is intentionally disabled so AdGuard
# (Docker container, bound to 0.0.0.0:53) owns port 53 on this host.
# AdGuard is primary; 1.1.1.1 is a fallback if the container is ever down
# (e.g. very early boot before Docker starts).
nameserver 127.0.0.1
nameserver 1.1.1.1
options edns0 trust-ad
```
Backup: `/etc/resolv.conf.bak-symlink-20260824` (the old symlink itself, preserved with `cp -P`).

`systemd-networkd` (netplan/DHCP) manages the interface on this host but does not write `/etc/resolv.conf` directly — only `systemd-resolved` does that, and it's disabled — so this static file is stable across reboots/`netplan apply`.

## Verification

- `docker exec searxng-core cat /etc/resolv.conf` → real `ExtServers: [1.1.1.1 9.9.9.9]`, resolves `www.bing.com` correctly.
- `dig www.bing.com @127.0.0.1` (AdGuard direct) → real answers, no errors.
- **Root-cause check:** spun up a disposable `alpine` container on `db-network` with no per-service DNS override — it now shows `ExtServers: [host(127.0.0.1) host(1.1.1.1)]` and resolves externally. Confirms *any future container* on `db-network` inherits working DNS automatically; the SearXNG-specific override is now redundant but left in place as a resilience layer.
- `curl http://127.0.0.1:7004/search?q=obsidian&format=json` → 41 results, `unresponsive_engines: []`.
- `searxng_web_search` MCP tool → confirmed working end-to-end from Claude Code.

## Takeaway for New Server Setup

If you self-host AdGuard on the same box as your Docker apps (standard pattern here — see [[adguard]]):

1. Disabling `systemd-resolved` to free port 53 for AdGuard is correct.
2. **But you must then manually replace `/etc/resolv.conf` with a static file** (`nameserver 127.0.0.1` + a public fallback) — nothing else will do it for you, and the default dangling symlink silently breaks external DNS for every container on every user-defined Docker network.
3. Give AdGuard **at least two** `upstream_dns` entries — a single upstream is a silent single point of failure for the whole LAN's DNS.
4. When diagnosing "is DNS broken," don't test with `google.com` on this LAN — it's intentionally filtered. Use a neutral domain.

## Related

- [[adguard]] — updated with the resolv.conf gotcha and current upstream config
- [[docker-network]] — updated with the external-DNS dependency note
- [[db-network-integration-guide]] — original migration that put SearXNG on `db-network`
- Index: [[Homelab-Infra-Checklist]]
