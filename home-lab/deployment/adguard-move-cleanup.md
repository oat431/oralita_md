# AdGuard / DNS Move-Out Cleanup Guide

> Relocating: dismantle the AdGuard DNS setup cleanly, leave the AIS router functional
> for the house owner, and keep everything needed to rebuild at the new place.
> Written: 2026-10-12 (relocation) · Server: homelab (moves with you) · Router: stays

---

## TL;DR — Can you just `docker compose down`?

**No.** Three things point at the homelab's IP; two of them would break *other people*:

| # | Thing | If left un-reverted |
|---|-------|---------------------|
| 1 | **Router** (stays here!) | 🔴 **Whole house loses DNS** the moment your server leaves — all devices lose internet until someone fixes the router |
| 2 | **Your PC** (static DNS) | 🟡 Works-ish but slow/broken-ish everywhere you go (dead `192.168.1.121` + dead IPv6 address) |
| 3 | **Server** (`docker compose down`) | ✅ Just stop it — but do it LAST, after 1 & 2 |

**Order of operations on moving day: ① Router → ② PC → ③ Server down → ④ Move.**

---

## ① Router — revert to normal (do this FIRST)

The router belongs to the house. Revert the two DNS settings we changed, so it goes back to using the ISP's DNS like a normal AIS setup.

### 1a. DHCPv4 DNS (Basic Setup → LAN → DHCP Server Configuration)

| Field | Current (ours) | Set back to |
|-------|---------------|-------------|
| Primary DNS Server | `192.168.1.121` | **empty / Auto** (= ISP default) |
| Secondary DNS Server | `1.1.1.1` | **empty / Auto** |

*If the UI requires values, clear them or set `192.168.1.1` (the ONT itself — it forwards to ISP).*

### 1b. DHCPv6 DNS (LAN → IPv6 LAN Configuration / DHCPv6 Server Configuration)

| Field | Current (ours) | Set back to |
|-------|---------------|-------------|
| DNS Source on the LAN Side | `Static configuration` | **`DNS agent`** |
| Preferred DNS (IPv6) | `2405:9800:b500:9736:692:26ff:fe01:ecaf` | *(clears when switching)* |
| Spare DNS (IPv6) | `2606:4700:4700::1111` | *(clears)* |

Leave `Enable Route Advertisement` + `Enable DHCPv6 Server` **checked** (original state).

**Apply.** Then optionally reboot the ONT (or wait for lease renewals) so all house devices refresh to ISP DNS.

> 💡 **Before reverting, screenshot both pages** — so rebuilding at the new place is trivial (or just use [[router-dns-setup]]).
>
> 💡 If you ever set a custom **router admin password**, hand it to the house owner or reset to the sticker default before leaving.

### Quick sanity check after revert
On any house device: browse anything → works (internet OK). `nslookup doubleclick.net` on a PC → returns real IPs (no more blocking — that's expected now).

---

## ② Your PC — remove static DNS (needs admin)

We set static DNS on the Ethernet adapter. Reset to automatic (works on any network afterwards):

```bat
netsh interface ipv4 set dnsservers name="Ethernet" source=dhcp
netsh interface ipv6 set dnsservers name="Ethernet" source=dhcp
ipconfig /flushdns
```

*(or GUI: Network Connections → Ethernet → Properties → IPv4/IPv6 → "Obtain DNS server address automatically")*

**Optional:** the Wi-Fi adapter has an old static entry (`94.140.14.14`, `94.140.15.15` = AdGuard's *public* DNS — works anywhere, but if you want "factory normal", set it to automatic too):

```bat
netsh interface ipv4 set dnsservers name="Wi-Fi" source=dhcp
```

**Nothing to do:** tablet — it uses AdGuard's public DNS (`4c952a3a.d.adguard-dns.com`), independent of the homelab, works worldwide. Tailscale adapter — no DNS config needed.

---

## ③ Server — stop AdGuard (do it LAST, on moving day)

### 3a. Backup the AdGuard config first (30 seconds)

```bash
# On the server
mkdir -p ~/backups
sudo cp /var/lib/docker/volumes/dns_adguard-conf/_data/AdGuardHome.yaml ~/backups/AdGuardHome.yaml.$(date +%F)
# Optional: also save the rule-count sanity values for reference
```

### 3b. Stop the stack (keeps config + data for redeploy)

```bash
cd ~/dns
docker compose down          # NOT `down -v` — that would DELETE the config volumes
```

Volumes `dns_adguard-conf` + `dns_adguard-work` stay intact → at the new place it's just `docker compose up -d`.

### 3c. Optional — remove the stale UFW v6 rule (references the OLD network prefix)

```bash
sudo ufw status numbered | grep 53        # find the rule numbers, then:
sudo ufw delete allow from 2405:9800:b500:9736::/64 to any port 53 proto udp
sudo ufw delete allow from 2405:9800:b500:9736::/64 to any port 53 proto tcp
```

*Keep a note: at the new place you'll re-add this with the **new** prefix* — otherwise v6 DNS from LAN silently times out (the exact bug from 2026-10-04).

### 3d. Host DNS state — keep as-is (recommended)

- `systemd-resolved` stays disabled; `/etc/resolv.conf` stays `127.0.0.1` + `1.1.1.1`.
- With AdGuard down, `127.0.0.1:53` = instant connection-refused → falls to `1.1.1.1` → the server still resolves fine. Docker containers unaffected.
- If you **never** plan to run AdGuard again: re-enable systemd-resolved and restore the resolv.conf symlink instead (see [[adguard]] for that dance — keep the static file otherwise).

### 3e. Shut down & unplug

```bash
sudo shutdown -h now
```

---

## ④ At the new place — rebuild checklist

1. Plug in, boot, network up (server auto-joins DHCP)
2. `cd ~/dns && docker compose up -d` → AdGuard back on :53
3. Router (new house): point DHCP DNS → the server's **new** LAN IP ([[router-dns-setup]] Part 1)
4. IPv6: update RDNSS/DHCPv6 DNS to the server's **new** IPv6 + update the UFW rule prefix (new ISP prefix!)
5. Set your PC's static DNS again (or leave automatic and do it via the router only — now that the router handles it, per-device statics are optional)
6. Optional: verify with the packet-capture method (see [[2026-10-04-adguard-blocking-audit]])

---

## What keeps working / what doesn't

| Thing | After move |
|-------|-----------|
| `adguard.panomete.com` (Nginx + CF tunnel) | Returns 502 while AdGuard is down; works again after redeploy |
| Uptime Kuma / other monitors | Unaffected (they don't depend on AdGuard unless you pointed them at it) |
| House devices | Back to ISP DNS after router revert — nothing else needed |
| Your PC elsewhere | Normal automatic DNS everywhere |
| Tablet | Always worked (public AdGuard DNS) |

---

## Related

- [[router-dns-setup]] — the full "how to re-wire the router" walkthrough
- [[2026-10-04-adguard-blocking-audit]] — the audit + verification methods
- [[adguard]] — component notes (resolv.conf gotcha etc.)
