---
title: Uptime Kuma — DNS Outage Fix (2026-08-28)
tags: [homelab, incident, dns, uptime-kuma, docker, adguard]
created: 2026-08-28
---

# Uptime Kuma — DNS Outage Fix (2026-08-28)

> Uptime Kuma (`status.panomete.com`) stopped monitoring everything — every
> monitor was red/failing. Not a server outage: the monitors were all still
> there, but the **Uptime Kuma container could not resolve any public hostname**
> (`getaddrinfo ENOTFOUND`).
>
> This is the **completion** of [[2026-08-24-searxng-dns-outage-fix]]. That fix
> repaired the host `/etc/resolv.conf` so *new* containers inherit working DNS —
> but it never recreated the containers that had already baked the broken
> `NO EXTERNAL NAMESERVERS DEFINED` config into their `/etc/resolv.conf`.
> Today we recreated all 19 of them.

---

## TL;DR

| Item | Value |
|------|-------|
| Symptom | All Uptime Kuma monitors failing, `getaddrinfo ENOTFOUND` |
| Real cause | Docker embedded DNS had **no upstream** in 19 containers' `resolv.conf` |
| Why | Containers created while host `resolv.conf` had only a loopback nameserver (`127.0.0.1`, which Docker ignores) |
| Why only now | 2026-08-24 fixed the host config but **didn't recreate existing containers** |
| Fix | `docker compose up -d --force-recreate` on all 19 stale containers |
| Data loss | None — all state in named volumes |
| Verified | 0 broken containers remaining; all monitored services return healthy HTTP codes |

---

## The mechanism (why Docker DNS broke silently)

Docker resolves external DNS for containers on **user-defined networks** (like
`db-network`) through its embedded resolver at `127.0.0.11`. That resolver
forwards external queries to the nameservers it captured from the host's
`/etc/resolv.conf` **at the moment each container was created**.

The trap: **Docker ignores loopback nameservers** (`127.0.0.0/8`) when building
that upstream list. So while the host `resolv.conf` pointed only at AdGuard on
`127.0.0.1`, Docker's embedded resolver had *nothing* to forward to, and it
wrote this into every newly-created container:

```
nameserver 127.0.0.11
options ndots:0
# NO EXTERNAL NAMESERVERS DEFINED
# Based on host file: '' (internal resolver)
```

Result: **internal** container-name resolution (`postgres`, `valkey`, …) still
worked, but **any public hostname lookup returned `SERVFAIL`** → Uptime Kuma's
HTTP monitors all threw `getaddrinfo ENOTFOUND`.

---

## Why Uptime Kuma surfaced it (and not the other 18)

Uptime Kuma's entire job is resolving public hostnames — `panomete.com`,
`auth.panomete.com`, `api.panomete.com`, etc. — so it failed loudly. The other
18 affected containers (databases, Prometheus, Grafana, Loki, Promtail,
SeaweedFS, apps) mostly talk to *other containers* by name, which still worked,
so they stayed green on `docker ps` while quietly unable to reach the internet.

### Affected monitors (all HTTP, 60s interval)

| # | Monitor | Target |
|---|---------|--------|
| 2 | main profile | `panomete.com` |
| 3 | service discovery | `discovery.panomete.com` |
| 4 | keycloak | `auth.panomete.com` |
| 5 | keycloak OIDC | `auth.panomete.com` |
| 6 | api gateway | `api.panomete.com` |
| 7 | grafana | `grafana.panomete.com` |

---

## Relationship to the 2026-08-24 fix

[[2026-08-24-searxng-dns-outage-fix]] fixed the **root cause** on the host:

1. Replaced the dangling `/etc/resolv.conf` symlink (→ disabled
   `systemd-resolved`) with a static file:
   ```
   nameserver 127.0.0.1
   nameserver 1.1.1.1
   options edns0 trust-ad
   ```
2. Added a fallback upstream to AdGuard.
3. Verified a *disposable* alpine container on `db-network` now got
   `ExtServers: [host(127.0.0.1) host(1.1.1.1)]` and resolved externally.

That note even concluded "any future container inherits working DNS
automatically." Correct — but **existing containers keep the `resolv.conf` they
were created with.** Docker does not rewrite it on restart, only on recreation.

So on 2026-08-28 the situation was:

| Layer | DNS state |
|-------|-----------|
| Host `getent hosts panomete.com` | ✅ resolves |
| Fresh container on `db-network` | ✅ `ExtServers: [host(127.0.0.1) host(1.1.1.1)]` |
| **19 pre-existing containers** | ❌ `NO EXTERNAL NAMESERVERS DEFINED` |

The fix was simply to **recreate** the stale containers so Docker regenerated
their `resolv.conf` from the now-correct host config.

---

## What was fixed (19 containers, 2026-08-28)

All are Compose-managed; nothing standalone. Recreated in this order
(observability → discovery → databases → apps → AdGuard last, to keep the DNS
blip at the end):

```bash
# 1. Observability + the reported problem
cd ~/platform
docker compose -f docker-compose.observability.yml up -d --force-recreate \
  uptime-kuma prometheus grafana loki promtail

# 2. Service discovery (Eureka)
docker compose -f docker-compose.platform.yml up -d --force-recreate flowero-discover

# 3. Databases — one at a time, health-checked
cd ~/database/postgres   && docker compose up -d --force-recreate postgres
cd ~/database/mongodb    && docker compose up -d --force-recreate mongodb
cd ~/database/valkey     && docker compose up -d --force-recreate valkey
cd ~/database/couchdb    && docker compose up -d --force-recreate couchdb
cd ~/database/seaweedfs  && docker compose up -d --force-recreate master volume filer s3

# 4. Apps
cd ~/application/homarr      && docker compose up -d --force-recreate homarr
cd ~/application/stirlingpdf && docker compose up -d --force-recreate stirling-pdf
cd ~/application/infisical   && docker compose up -d --force-recreate backend
cd ~/application/bytestash   && docker compose up -d --force-recreate bytestash

# 5. AdGuard — LAST (brief DNS blip while it rebinds :53)
cd ~/dns && docker compose up -d --force-recreate adguard
```

> `--force-recreate` is essential — a plain `restart` keeps the old container
> (and its broken `resolv.conf`). Only recreate regenerates it.

> **Orphan-container warnings** (`Found orphan containers … for this project`)
> appear because `docker-compose.observability.yml` and
> `docker-compose.platform.yml` share the `platform` project but define
> different services. **Do not** run `--remove-orphans` here — it would delete
> the other file's containers.

### Full list of recreated containers

```
uptime-kuma          local-postgres        homarr
prometheus           local-mongodb         stirling-pdf
grafana              local-valkey          infisical-backend
loki                 local-couchdb         bytestash
promtail             seaweedfs-master      adguard
flowero-discover     seaweedfs-volume
                     seaweedfs-filer
                     seaweedfs-s3
```

---

## Verification (all green)

```bash
# 1. Zero containers left with broken DNS
for c in $(docker ps --format '{{.Names}}'); do
  docker exec "$c" cat /etc/resolv.conf 2>/dev/null | grep -q 'NO EXTERNAL NAMESERVERS DEFINED' \
    && echo "STILL BROKEN: $c"
done   # → no output

# 2. Uptime Kuma can resolve again
docker exec uptime-kuma node -e 'require("dns").resolve4("panomete.com",(e,a)=>console.log(e||a))'
# → 172.67.201.83, 104.21.52.163

# 3. Full path from the server (public DNS → Cloudflare → Nginx → app)
for d in panomete.com auth.panomete.com discovery.panomete.com \
         api.panomete.com grafana.panomete.com status.panomete.com; do
  curl -s -o /dev/null -w "%{http_code} $d\n" --max-time 15 "https://$d/"
done
```

| Domain | Code | Meaning |
|--------|------|---------|
| `panomete.com` | 200 | ✅ |
| `auth.panomete.com` | 302 | Keycloak → login (normal) |
| `discovery.panomete.com` | 200 | ✅ |
| `api.panomete.com` | 401 | gateway demanding auth (normal) |
| `grafana.panomete.com` | 302 | Grafana → login (normal) |
| `status.panomete.com` | 302 | Uptime Kuma → login (normal) |

The one transient `502` on the `service discovery` monitor fired during the
`flowero-discover` recreate (~1 s of downtime) and cleared on the next 60 s
check — no repeat in the logs. `docker ps` showed all 19 containers healthy/up.

---

## Prevention / follow-ups

- [x] Recreate the 19 stale containers (this note) — done.
- [ ] **Pin explicit DNS upstreams in `/etc/docker/daemon.json`** so this class
      of failure can't recur regardless of host `resolv.conf` changes:
      ```json
      { "dns": ["1.1.1.1", "8.8.8.8"] }
      ```
      Requires `systemctl restart docker` (restarts **all** containers, ~1 min
      outage) — schedule a maintenance window. After this, containers use these
      upstreams directly and no longer depend on Docker's loopback-ignoring
      read of the host file.
- [ ] **Rule of thumb:** any change to host `/etc/resolv.conf` (or a DNS outage
      window) only affects *new* containers. Existing ones keep their
      creation-time config — recreate them (or do a full
      `docker compose up -d --force-recreate`) if they need to pick it up.
- [ ] Consider a `depends_on`/ordering note: on full-host reboots, AdGuard must
      be up before anything that resolves public hostnames at boot (gateway
      OIDC discovery, SearXNG, Uptime Kuma).

---

## Quick reference

```bash
# Detect broken-DNS containers in one shot
for c in $(docker ps --format '{{.Names}}'); do
  docker exec "$c" sh -c 'grep -q "NO EXTERNAL NAMESERVERS" /etc/resolv.conf && echo BROKEN' 2>/dev/null \
    && echo "  $c"
done

# Recreate a single stale container (regenerates resolv.conf)
cd <project-dir> && docker compose up -d --force-recreate <service>

# Inspect a container's DNS config
docker exec <container> cat /etc/resolv.conf
#   broken: "NO EXTERNAL NAMESERVERS DEFINED"
#   fixed:  "ExtServers: [host(127.0.0.1) host(1.1.1.1)]"
```

| Thing | Value |
|-------|-------|
| Uptime Kuma compose | `~/platform/docker-compose.observability.yml` (service `uptime-kuma`) |
| Uptime Kuma port | `127.0.0.1:3001` (public via `status.panomete.com`) |
| Uptime Kuma data | volume `platform_uptime_kuma_data` → `/app/data` |
| Docker embedded DNS | `127.0.0.11` on user-defined networks |
| Host DNS | AdGuard `127.0.0.1:53` primary + `1.1.1.1` fallback |
| Docker version | 29.7.2 |

---

## Related

- [[2026-08-24-searxng-dns-outage-fix]] — the root-cause fix this note completes
- [[adguard]] — owns `:53`; the loopback-nameserver gotcha
- [[db-network-integration-guide]] — shared `db-network` infra
- [[docker-network]] — external-DNS dependency note
- [[flowero-gate-guard-recovery]] — sibling incident/runbook (same folder)
- Index: [[Homelab-Infra-Checklist]]
