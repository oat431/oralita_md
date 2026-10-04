# Router DNS Setup — Huawei ONT (AIS Fibre)

> Complete walkthrough: point every home device at the homelab AdGuard (`192.168.1.121`)
> for network-wide ad blocking, and close the IPv6 DNS leak.
> Router: Huawei ONT (AIS) · Admin: `http://192.168.1.1`
> Last updated: 2026-10-04

---

## Goal

Every device on the home Wi-Fi/LAN resolves DNS through **AdGuard Home** (`192.168.1.121`) → ads/trackers blocked network-wide. Devices that respect router settings get it automatically; no per-device config needed.

---

## Part 0 — Before you start

| Item | Value |
|------|-------|
| Router UI | `http://192.168.1.1` |
| Login password | On the ONT sticker (or ask AIS support; advanced menus may need the `telecomadmin` account) |
| AdGuard (homelab) | `192.168.1.121` — IPv4 DNS :53 · IPv6: `2405:9800:b500:9736:692:26ff:fe01:ecaf` :53 |
| AdGuard v6 serving | Enabled 2026-10-04 (see [[2026-10-04-adguard-blocking-audit]]) |

---

## Part 1 — IPv4 DHCP DNS ✅ (the main step)

This is what makes **every device** use AdGuard automatically.

1. Browse to `http://192.168.1.1` and log in.
2. Navigate:

   ```
   Basic Setup → LAN → DHCP Server Configuration
   ```

   *(menu names vary slightly by firmware — look for "DHCP Server" under LAN)*

3. Set:

   | Field | Value | 
   | ------- | ------- |
   | **Primary DNS Server** | `192.168.1.121` |
   | **Secondary DNS Server** | `1.1.1.1` *(availability fallback — optional; leave blank for strict filtering only)* |

4. **Save / Apply.**
5. If the fields already show `192.168.1.121` → nothing to change, just confirm and move on.

> **Existing devices** keep their old DNS until their lease renews / they reconnect. Toggle Wi-Fi on phones to pick it up immediately.

---

## Part 2 — IPv6 DNS leak (RDNSS / DHCPv6) ✅ DONE 2026-10-04

**The problem:** the ONT advertised **AIS IPv6 DNS servers** (RDNSS: `2405:9800:a:1::10`, `2405:9800:a:2::26`). IPv6-capable devices (Windows, Android, iOS, macOS) *prefer* IPv6 DNS → they bypassed AdGuard.

**Applied fix — path used on this ONT:**

```
LAN → IPv6 LAN Configuration (DHCPv6 Server Configuration page)
  DNS Source on the LAN Side:  [ WAN port / DNS agent ]  →  [ Static configuration ]
  Preferred DNS (IPv6):  2405:9800:b500:9736:692:26ff:fe01:ecaf   (homelab AdGuard)
  Spare DNS (IPv6):      2606:4700:4700::1111                     (Cloudflare — availability fallback)
  (Enable Route Advertisement + Enable DHCPv6 Server both stay ON)
```

**Verified (2026-10-04, live packet capture on the server):**
- Router's **DHCPv6 advertisement** now carries: `DNS-server 2405:9800:b500:9736:692:26ff:fe01:ecaf` + `2606:4700:4700::1111` ✅
- **Devices observed querying the homelab over IPv6** (fresh captures): the PC, `.126`, `.128` — they could only learn this DNS from the router ✅
- AdGuard serves v6: `dig @2405:...ecaf doubleclick.net` → `0.0.0.0` (blocked) ✅

> **Maintenance note:** the homelab IPv6 is a *dynamic AIS prefix*. If AIS ever rotates the `/64`, update: (1) router Preferred DNS, (2) the `ufw` v6 rule (`2405:9800:b500:9736::/64`), (3) the PC's static v6 DNS. Devices fall back to IPv4 AdGuard meanwhile — still filtered.
>
> **Strictness option:** the Cloudflare spare means a device *may* race a query to Cloudflare if the homelab is slow (rare). To be 100% strict, clear the Spare field — trade: pure-homelab DNS has no independent backup (devices then fall back to IPv4 AdGuard anyway).

### Original options (kept for reference)

<details><summary>Option A/B details (if firmware menus differ)</summary>

### Option A — Remove DNS from the IPv6 advertisement (simplest)

Look under (names vary):

```
LAN → IPv6 LAN Configuration     or
WAN → IPv6 settings              or
Advanced → IPv6
```

- Turn **off** the "DNS advertisement" / clear the IPv6 DNS server fields.
- Effect: devices fall back to the IPv4 DHCP DNS (= AdGuard). ✅

### Option B — Set IPv6 DNS (RDNSS) to the homelab

In the same IPv6 settings area, set the IPv6 DNS server to:

```
2405:9800:b500:9736:692:26ff:fe01:ecaf
```

- Effect: v6-capable devices query AdGuard over IPv6. ✅
- ⚠️ **Caveat:** this is a *dynamic AIS prefix*. If AIS ever rotates the `/64`, the address breaks → devices fall back to IPv4 (still filtered), but revisit this + the server UFW rule.

</details>

### If the firmware hides both (AIS-locked ONT)

Options, in order of practicality:
1. Log in as `telecomadmin` (AIS superadmin) — more menus appear.
2. Ask AIS support to disable "IPv6 DNS advertisement" on the ONT.
3. Accept partial leak: v6-preferring devices hop between AIS DNS (unfiltered) and AdGuard (filtered). For critical devices, set **per-SSID static DNS** (see [[adguard]] — never set static DNS globally, and remember it only applies at home).

---

## Part 3 — Verify

1. **Reconnect a phone** to the Wi-Fi (toggle Wi-Fi off/on).
2. On the phone, try loading a known ad domain in the browser — it should **not load** (e.g. `doubleclick.net` shows an error page).
   - Quick check: `https://adblock-tester.com` — higher score = more blocked.
3. **Server-side check (ask the AI devops assistant):** it reads AdGuard's query log to confirm the device appears with blocked queries.
4. Cross-check one device that was previously bypassing (e.g. an Android phone — look for `mtalk.google.com`-type blocks from its IP in the query log).

---

## Rollback

- Set Primary/Secondary DNS back to `Automatic` (or `1.1.1.1`), save.
- IPv6 options: restore AIS DNS or re-enable advertisement.

---

## Known limitations (expected, not bugs)

- **Mobile data / away Wi-Fi**: home DNS doesn't apply — normal.
- **Hardcoded DNS devices** (some IoT, Chromecast etc. use `8.8.8.8` internally): bypass anything the router says.
- **Android Private DNS / browser DoH** enabled on a device: bypasses router DNS. (Check: Android → Settings → Network → Private DNS = Off/Automatic hostname from provider.)
- Devices with same-subnet collisions elsewhere (e.g. another `192.168.1.x` network with a device at `.121`) only matter if static DNS is set **globally** — never do that on roaming devices; per-SSID only.

---

## Related

- [[adguard]] — AdGuard Home component notes + the resolv.conf gotcha
- [[2026-10-04-adguard-blocking-audit]] — the audit that led here (blocking was fine; coverage was the issue)
- [[2026-08-24-searxng-dns-outage-fix]] — DNS incident history
