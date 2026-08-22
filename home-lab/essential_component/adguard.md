# AdGuard Home

> DNS server + network-wide ad blocking.
> Last updated: 2026-07-20

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
https://1.1.1.1/dns-query
https://dns.google/dns-query
```

## Notes

- DNS port 53 is bound to `0.0.0.0` (open for LAN devices)
- Web UI is bound to `127.0.0.1` (access via Nginx or Tailscale)
- Replaces paid AdGuard DNS service
- `systemd-resolved` was disabled to free port 53
