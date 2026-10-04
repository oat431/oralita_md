---
tags: [homelab, audit, adguard, dns, ipv6]
---

# AdGuard Home — Blocking Audit (2026-10-04)

**Question:** "AdGuard seems to not block anything in block list — audit that?"

**Verdict:** AdGuard itself is **healthy and blocking aggressively** (5.4M rules, actively blocking on every device that uses it). The perception comes from **DNS coverage gaps** — the user's own PC (and any IPv6-preferring device) **never queries AdGuard at all**.

---

## Evidence 1 — AdGuard is working (server side)

| Check | Result |
|-------|--------|
| Container | `adguard` up 5 weeks, stable |
| Filter lists | **50 lists, all enabled** (HaGeZi, OISD, Steven Black, Thai lists…) |
| Rules loaded | **5,399,945 rules** in `work/data/filters/*.txt` (~111 MB) |
| Lists updated | Fresh — daily refresh working (last: Oct 4 ~02:18 ICT) |
| Upstreams | Quad9 + Cloudflare DoH (2 upstreams, from the 2026-08-24 fix) |
| DNSSEC | Enabled; rate limit 20; blocking mode default (0.0.0.0 / ::) |

**Live block test (server + LAN):**

```
$ nslookup doubleclick.net 192.168.1.121
Name: doubleclick.net
Addresses: ::            ← BLOCKED (homelab AdGuard)
           0.0.0.0

$ nslookup doubleclick.net 2405:9800:a:1::10   (AIS ISP DNS)
Name: doubleclick.net
Addresses: 2404:6800:4016:80e::200e   ← NOT blocked (ISP)
           142.250.204.206
```

**Query log stats (last ~6h, 8,714 queries parsed):**

| Client | Queries | Blocked | % |
|--------|---------|---------|---|
| 192.168.1.128 | 345 | 343 | **99.4%** |
| 192.168.1.103 | 288 | 244 | **84.7%** |
| 192.168.1.106 | 240 | 178 | 74.2% |
| 192.168.1.104 | 228 | 228 | **100%** |
| 192.168.1.129 | 12 | 3 | 25% |
| (host/docker) | 7,595 | 25 | 0.3% (internal domains) |

→ **1,022 blocked in 6 hours.** Devices that use AdGuard are filtered heavily (high % = ad SDKs retry-looping on blocked domains — normal).

---

## Evidence 2 — Why the user sees "no blocking"

### The user's PC (192.168.1.123) does NOT use AdGuard

| Check | Finding |
|-------|---------|
| System resolver | **AIS ISP DNS** (`nsc01.awn.co.th`, `2405:9800:a:1::10`) — 5/5 samples |
| Adapter static IPv4 DNS | `94.140.14.49 / .59` = AdGuard **public** DNS service (stale config, NOT the homelab) |
| Adapter IPv6 DNS | From router RA/RDNSS: `2405:9800:a:1::10`, `2405:9800:a:2::26` (AIS) |
| Windows behavior | **Prefers IPv6 DNS** when IPv6 connectivity exists → AIS wins over the static IPv4 entries |
| PC in AdGuard query log | **Absent** — its queries never reach the homelab |

**Proof:** `doubleclick.net` on the PC → real Google IPs (unfiltered). Via homelab AdGuard → `::` / `0.0.0.0` (blocked).

### The IPv6 DNS gap (affects ALL IPv6-preferring devices)

1. Router advertises **AIS IPv6 DNS** via RA/RDNSS.
2. Windows/Android/iOS prefer IPv6 DNS servers.
3. Homelab AdGuard **only listens on IPv4** (`bind_hosts: ['0.0.0.0']`, docker publishes `0.0.0.0:53` — no `[::]:53`).
→ Every device with working IPv6 can silently bypass filtering via IPv6.

### Also noted

- **Router DHCP IPv4 DNS is already correct**: hands out `192.168.1.121` (homelab) + `1.1.1.1` — that's why several LAN devices DO use AdGuard.
- **`user_rules` is empty** — no custom block rules exist. If custom rules were expected, re-add them.
- **"No Google" list is active** — blocks `www.google.com` etc. by design (keep or remove as desired).
- Query log file is 698 MB (`querylog.json`) — growing large; consider reviewing retention settings sometime.

---

## Fix Options

### A. Server — enable IPv6 DNS in AdGuard *(I can do)*
- `AdGuardHome.yaml`: `bind_hosts: ['0.0.0.0', '::']`
- `~/dns/compose.yml`: add `"[::]:53:53/tcp"` + `"[::]:53:53/udp"` publishes
- Result: AdGuard answers DNS on IPv6 too (e.g. `2405:9800:b500:9736:692:26ff:fe01:ecaf`).

### B. Router — fix the IPv6 DNS advertisement *(user's territory)*
- **Option B1 (simplest):** remove DNS entries from the router's RA/RDNSS → devices fall back to IPv4 DHCP DNS = `192.168.1.121` (already correct).
- **Option B2:** advertise the homelab's IPv6 as the RDNSS DNS (requires A first). Note: ISP prefix is dynamic — may need re-checking after ISP/router changes.

### C. PC — fix the stale DNS config *(I can do)*
- Set Ethernet IPv4 DNS static → `192.168.1.121` (or reset to DHCP).
- Set Ethernet IPv6 DNS static → homelab IPv6 (requires A first), so AIS's RA-learned DNS no longer wins.
- Until B or A+C are done, the PC keeps bypassing.

---

## Fix Status (applied 2026-10-04)

### ✅ Applied

**A — AdGuard IPv6 listening enabled:**
- `AdGuardHome.yaml`: `bind_hosts` now `['0.0.0.0', '::']` (backup: `AdGuardHome.yaml.bak-v6-20261004`)
- `~/dns/compose.yml`: added `[::]:53:53/tcp` + `[::]:53:53/udp` publishes (backup: `compose.yml.bak-v6-20261004`)
- Verified server-side: v6 queries answered (`doubleclick.net` → `0.0.0.0`, `example.com` → resolves)

**C — PC (192.168.1.123) DNS updated:**
- IPv4 static: `192.168.1.121` (homelab) + `1.1.1.1` fallback
- IPv6 static: `2405:9800:b500:9736:692:26ff:fe01:ecaf` (homelab)
- **Verified: blocking now works at system level** — `ads.doubleclick.net`, `googlesyndication.com`, `adservice.google.com` → `::` / `0.0.0.0`; `example.com` resolves.

### ✅ UFW rule applied (user, 2026-10-04)

```
53/udp ALLOW 2405:9800:b500:9736::/64  # LAN DNS v6
53/tcp ALLOW 2405:9800:b500:9736::/64  # LAN DNS v6
```

**Final end-to-end verification (all pass):**
| Test | Result |
|------|--------|
| TCP/53 reachability from PC (v6) | ✅ True (was False) |
| `nslookup doubleclick.net` via v6 AdGuard | ✅ `::` / `0.0.0.0` (blocked) |
| System resolver: `ads.doubleclick.net` | ✅ `::` / `0.0.0.0` (blocked) |
| System resolver: `cdn.jsdelivr.net` | ✅ real IPs (not over-blocked) |
| Cold lookup latency | ✅ 0.41s |
| PC in AdGuard query log | ✅ `192.168.1.123: 4/4 blocked (100%)` |

### ✅ Router work — DONE (user, 2026-10-04)

The router's `DHCPv6 Server Configuration → DNS Source on the LAN Side` was changed from `WAN port` (AIS pass-through) to **`Static configuration`**:
- Preferred DNS (IPv6): `2405:9800:b500:9736:692:26ff:fe01:ecaf` (homelab)
- Spare DNS (IPv6): `2606:4700:4700::1111` (Cloudflare fallback)

**Verified via live packet capture (server, 2026-10-04):**
- Router's DHCPv6 advertisement now carries the homelab IPv6 as DNS-server ✅
- LAN devices observed querying the homelab over IPv6: PC, `.126`, `.128` ✅

→ Full DNS coverage: every standard-configured device on the LAN now resolves through AdGuard (v4 via DHCP, v6 via router advertisement). See [[router-dns-setup]] for the reusable walkthrough.

**Note:** homelab IPv6 is a dynamic AIS prefix — revisit router + UFW + PC static DNS if AIS ever renumbers.

## Recommended Sequence

1. **A** (server IPv6 listening) — ✅ done
2. **C** (PC static DNS) — ✅ done
3. **UFW v6:53 rule** — ✅ done (all verified)
4. **B1/B2** (router RA DNS) — remaining (covers all other devices)

## Related

- [[2026-08-24-searxng-dns-outage-fix]] — DNS incident (AdGuard upstream + resolv.conf)
- [[adguard]] — AdGuard component notes
- Index: [[Homelab-Infra-Checklist]]
