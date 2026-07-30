# Ubuntu 26.04 "resolute" Compatibility Notes

> Codename: `resolute` (released 2026)
> Kernel: 7.0.0

## Cloudflare cloudflared

**Problem**: Cloudflare's apt repo (`pkg.cloudflare.com/cloudflared`) does NOT have packages for `resolute`.

**Fix**: Install the binary directly from GitHub releases:
```bash
curl -fsSL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /tmp/cloudflared
sudo install -m 755 /tmp/cloudflared /usr/local/bin/cloudflared
rm /tmp/cloudflared
```

## Docker

Docker's apt repo DOES support `resolute` (as of 2026-07). Standard install works, but watch for escaping issues in SSH commands when writing the repo line.

**Safe pattern** — compute variables server-side:
```bash
ssh user@server "
ARCH=\$(dpkg --print-architecture)
CODENAME=\$(. /etc/os-release && echo \$VERSION_CODENAME)
echo \"deb [arch=\$ARCH signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \$CODENAME stable\" | sudo tee /etc/apt/sources.list.d/docker.list
"
```

## OpenSSH 10.2p1

Ubuntu 26.04 ships OpenSSH 10.2p1. Known incompatibility with Windows OpenSSH 9.9p2 ed25519 hostbound keys. Use RSA keys for automation (see `ssh-automation-windows.md`).

## Systemd

- SSH service is `ssh.service` (not `sshd.service`), triggered by `ssh.socket`
- `sshd -T` may return empty output without sudo — use `sudo sshd -T` for effective config dump
