# Tailscale Setup — Full Workflow

> Zero-config mesh VPN for remote access. No port forwarding, works behind CGNAT.

## Prerequisites

- Tailscale account (free for personal use, login with Google/GitHub/etc)
- First device registered (creates the tailnet)

## 1. Install on server

```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

## 2. Authenticate

```bash
sudo tailscale up
```

Outputs a browser URL. User logs in with their Tailscale account. Server joins the tailnet.

**Note:** The command blocks until auth completes. If running over SSH, it will timeout — the user must visit the URL while tailscale waits.

## 3. Enable on boot

```bash
sudo systemctl enable tailscaled
```

## 4. Verify

```bash
tailscale status   # shows all devices on the tailnet
tailscale ip       # shows this device's Tailscale IP (100.x.x.x)
```

## Key Facts

- **Tailscale IPs are stable** — assigned per device, never change (reboot, ISP change, location change)
- **Each tailnet is isolated** — your 100.x.x.x has no conflict with anyone else's
- **MagicDNS** — devices can reach each other by hostname (e.g., `ssh flowero@flowero`)
- **Free tier** — 100 devices, 3 users, personal use

## Adding a New Device

1. Install Tailscale on the device
2. Log in with the same account
3. Device appears in `tailscale status` with its own 100.x.x.x IP
4. SSH/access services via Tailscale IP

## SSH Access Pattern

Since Cloudflare Tunnel only handles HTTP/HTTPS, SSH goes through Tailscale:

```
Device (on tailnet) → Tailscale IP (100.x.x.x) → SSH (port 22)
```

For a friendly hostname, either:
- Use Tailscale MagicDNS: `ssh flowero@flowero`
- Create a DNS A record: `remote.example.com` → `100.x.x.x` (DNS only, not proxied)
- Use SSH config alias in `~/.ssh/config`

## DNS Record for SSH Alias

In Cloudflare, create:

| Type | Name | Value | Proxy |
|------|------|-------|-------|
| A | `remote` | `100.x.x.x` | DNS only (gray cloud) ⚠️ |

**Must be DNS only** — if proxied (orange cloud), Cloudflare handles it as HTTP/HTTPS, which breaks SSH.

## Common Mistake: Sharing Private Keys

Each device gets its OWN key pair. Never copy `id_homelab` to another device.

| Device | Private key | Public key goes to |
|--------|------------|-------------------|
| Your PC | `id_homelab` (stays here) | → server's `authorized_keys` |
| Friend laptop | `id_friend` (stays there) | → server's `authorized_keys` |
| Tablet | `id_tablet` (stays there) | → server's `authorized_keys` |

To revoke a device: remove its public key from `authorized_keys`.
