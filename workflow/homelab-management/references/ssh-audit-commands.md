# SSH Audit Command Patterns

> Commands for remote server audits via SSH. Run in parallel batches grouped by concern.
> **Avoid `sudo`** — hangs on password prompt. Note what needs root and flag it.

## Hardware & System Info

```bash
ssh user@host "echo '=== CPU ===' && lscpu | grep -E 'Model name|Socket|Core|Thread|CPU\(s\):' && echo '=== RAM ===' && free -h && echo '=== DISK ===' && df -h && echo '=== UPTIME ===' && uptime"
```

## Docker Stack

```bash
# Versions + running containers + networks + volumes
ssh user@host "docker --version && docker compose version && docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.Image}}' && docker network ls && docker volume ls"

# Restart policies
ssh user@host "docker inspect --format '{{.Name}}: {{.HostConfig.RestartPolicy.Name}}' \$(docker ps -q)"

# Healthchecks
ssh user@host "docker inspect --format '{{.Name}}: {{json .Config.Healthcheck}}' \$(docker ps -q)"

# Publicly bound ports (bypasses reverse proxy)
ssh user@host "docker ps --format '{{.Names}}: {{.Ports}}' | grep '0.0.0.0'"

# Disk usage
ssh user@host "docker system df"
```

## Security Config

```bash
# SSH config (no sudo needed)
ssh user@host "grep -vE '^#|^$' /etc/ssh/sshd_config && cat /etc/ssh/sshd_config.d/*.conf"

# fail2ban status
ssh user@host "systemctl is-active fail2ban && systemctl status fail2ban | head -5"

# Firewall (needs root — try without sudo, note if permission denied)
ssh user@host "ufw status 2>&1"

# Open ports
ssh user@host "ss -tlnp | head -30"
```

## Reverse Proxy

```bash
# Nginx vhosts
ssh user@host "ls /etc/nginx/sites-enabled/ && for f in /etc/nginx/sites-enabled/*.conf; do echo \"--- \$f ---\"; grep server_name \$f; done"

# SSL certs
ssh user@host "ls /etc/letsencrypt/live/ 2>/dev/null"

# Specific vhost config
ssh user@host "cat /etc/nginx/sites-enabled/gateway.conf"
```

## Users & Access

```bash
ssh user@host "cat /etc/passwd | grep -E '/bin/bash|/bin/sh' | grep -v nologin && getent group sudo"
```

## Remote Access Tools

```bash
# Check for VPN/tunnel tools
ssh user@host "which tailscale 2>/dev/null; which cloudflared 2>/dev/null; which wg 2>/dev/null"
```

## Backup Status

```bash
# Crontab + systemd timers
ssh user@host "crontab -l 2>/dev/null; echo '=== ROOT CRONTAB ==='; sudo crontab -l 2>/dev/null; echo '=== TIMERS ==='; systemctl list-timers --all | head -20"

# Standard backup dirs
ssh user@host "ls -la /backup* /opt/backup* /home/user/backup* 2>/dev/null || echo 'no standard backup dirs'"
```

## Networking

```bash
ssh user@host "ip -4 addr show | grep inet && cat /etc/resolv.conf"
```

## Auto-Updates

```bash
ssh user@host "dpkg -l unattended-upgrades 2>/dev/null | tail -1 && systemctl is-active unattended-upgrades"
```

## Compose Files Discovery

```bash
ssh user@host "find /home/user -maxdepth 3 -name 'docker-compose*.yml' -o -name 'compose*.yml'"
```

## Pitfalls

- **SSH timeout**: Commands with `sudo` or `systemctl status` hang waiting for password. Break into smaller calls or use `is-active` instead of `status`.
- **Long commands**: SSH sessions timeout at ~15-20s. Keep each command focused. Run multiple in parallel.
- **Root-only info**: Note what requires root (`ufw status`, `iptables -L`) and report it as "❓ cannot verify — needs root" rather than guessing.
- **`ss -tlnp` without sudo**: Shows process names only for processes owned by the current user. Other processes show as `*`.
- **sudo over SSH**: Requires TTY. Non-interactive SSH hangs. Need NOPASSWD sudoers entry for audit workflows.
- **Windows ed25519 failure**: Windows OpenSSH 9.9's hostbound key signing fails with Ubuntu 26.04 OpenSSH 10.2. Use RSA 4096 keys instead.
- **SSH_ASKPASS stdin**: Always redirect stdin from `/dev/null` (`< /dev/null`) when using SSH_ASKPASS, otherwise SSH reads from stdin instead of calling the askpass script.
