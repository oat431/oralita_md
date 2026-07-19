# 04 — Fail2ban

> Ban IPs after repeated failed login attempts.

---

## Step 1: Install and enable

```bash
sudo apt update && sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

---

## Step 2: Verify

```bash
sudo fail2ban-client status sshd
```

**Why:** Even with key-only auth, fail2ban protects against brute-force scanners hitting your SSH port. It monitors logs and bans offending IPs via iptables.
