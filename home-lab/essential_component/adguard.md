# AdGuard Home

> DNS server + network-wide ad blocking.
> Last updated: 2026-08-24

---

## Setup

**Compose:** Custom (manually created)

| Item | Value |
|------|-------|
| Image | `adguard/adguardhome:latest` |
| Container | `adguard` |
| Web UI | `127.0.0.1:7000` (mapped from 3000) |
| DNS | `0.0.0.0:53` (open for LAN) |

## Access

| Method | URL |
|--------|-----|
| Public | `https://adguard.panomete.com` |
| Tailscale | `http://100.73.143.25:7000` |

## Router Config

Set router's **Primary DNS** to `192.168.1.121` (LAN IP). All devices on the network get ad blocking automatically.

Location: **Basic Setup → LAN → DHCP Server Configuration → Primary DNS Server**

## Upstream DNS

```
https://dns10.quad9.net/dns-query
https://dns.cloudflare.com/dns-query
```

⚠️ **Always keep at least two upstreams.** A single upstream is a silent LAN-wide single point of failure — see the 2026-08-24 incident below, where Quad9 alone started failing with `unexpected EOF` and every DNS query on the network broke with no fallback.

## Notes

- DNS port 53 is bound to `0.0.0.0` (open for LAN devices)
- Web UI is bound to `127.0.0.1` (access via Nginx or Tailscale)
- Replaces paid AdGuard DNS service
- `systemd-resolved` was disabled to free port 53

## ⚠️ Host DNS Gotcha (new server setup — do this immediately after disabling systemd-resolved)

Disabling `systemd-resolved` frees port 53 for AdGuard, but it also means **nothing manages `/etc/resolv.conf` anymore**. By default it's a symlink to `systemd-resolved`'s stub file, which no longer exists once the service is disabled — the symlink dangles.

**Consequence:** Docker seeds each new container's embedded DNS forwarder from the *host's* resolver config when that container joins a user-defined network (e.g. `db-network`). With a dangling `/etc/resolv.conf`, Docker finds nothing to forward to, and every such container silently gets **zero external DNS** — internal container-name resolution (`postgres`, `valkey`, ...) still works, but any outbound HTTP call to an external host fails. This is exactly what broke SearXNG on 2026-08-24 ([[2026-08-24-searxng-dns-outage-fix]]) — and it would hit *any* app added to `db-network` the same way, not just SearXNG.

**Fix — do this right after disabling `systemd-resolved` on a new box:**

```bash
sudo cp -P /etc/resolv.conf /etc/resolv.conf.bak   # keep the old symlink just in case
sudo rm /etc/resolv.conf
sudo bash -c 'cat > /etc/resolv.conf <<EOF
nameserver 127.0.0.1
nameserver 1.1.1.1
options edns0 trust-ad
EOF'
```

Points at AdGuard itself first (self-hosted ad-blocking DNS, the whole point of running it), with `1.1.1.1` as a fallback if the AdGuard container is ever down (e.g. very early boot before Docker starts).

This survives reboots on this host because networking is managed by `systemd-networkd` (via netplan/DHCP), which does **not** write `/etc/resolv.conf` directly — only `systemd-resolved` does that, and it's disabled. If a future server uses NetworkManager instead, check whether it manages `/etc/resolv.conf` before assuming a static file will stick.

**Verify:** run a throwaway container on the shared network and confirm it inherits real DNS, don't just check the app you're actively debugging:
```bash
docker run --rm --network db-network alpine:latest cat /etc/resolv.conf
# should show: # ExtServers: [host(127.0.0.1) host(1.1.1.1)]
```
