# SSH Automation from Windows (MINGW64/Git Bash)

## Problem: Password-based SSH from automation

Git Bash on Windows can't use `sshpass` (not available in MINGW64). SSH in non-interactive mode won't read password from stdin.

## Solution: SSH_ASKPASS trick

```bash
# 1. Create password script
cat > /tmp/ssh_pass.sh << 'SCRIPT'
#!/bin/bash
echo 'YOUR_PASSWORD'
SCRIPT
chmod +x /tmp/ssh_pass.sh

# 2. Use with SSH
export SSH_ASKPASS="/tmp/ssh_pass.sh"
export SSH_ASKPASS_REQUIRE="force"
export DISPLAY=":0"
ssh -o StrictHostKeyChecking=no user@server "command"
```

- `SSH_ASKPASS` — script that echoes the password
- `SSH_ASKPASS_REQUIRE=force` — always use ASKPASS (don't check for terminal)
- `DISPLAY=:0` — required for SSH_ASKPASS to trigger (even without X11)
- `< /dev/null` — detach from stdin so ASKPASS is used instead

## Problem: Ed25519 key auth fails on Windows

OpenSSH 9.9p2 (Git Bash) + OpenSSH 10.2p1 (Ubuntu 26.04) = signing failure with `publickey-hostbound-v00@openssh.com` extension.

**Debug output:**
```
debug1: Server accepts key: ...explicit
debug3: sign_and_send_pubkey: using publickey-hostbound-v00@openssh.com
debug2: we did not send a packet, disable method
```

**Root cause**: The hostbound key signing fails silently on Windows SSH client.

## Solution: Use RSA key for automation

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_homelab -N ""
```

RSA keys work fine. Ed25519 keys with passphrase also fail (can't sign non-interactively). Use unpassphrased RSA for server automation, keep passphrase-protected ed25519 for daily use.

## Problem: sudo over SSH needs a terminal

```
sudo: A terminal is required to authenticate
```

## Solution: NOPASSWD sudoers drop-in

```bash
echo 'user ALL=(ALL) NOPASSWD:ALL' | sudo tee /etc/sudoers.d/user
```

Run this on the server during initial setup. `sudo -S` (pipe password) is blocked by security tooling — don't try it.

## Paramiko alternative (Python)

If `sshpass` and `SSH_ASKPASS` don't work, Python's `paramiko` library can handle password auth:

```python
import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('server', username='user', password='pass')
stdin, stdout, stderr = client.exec_command('command')
```

**Caveat**: `bcrypt` (paramiko dependency) requires Rust compiler. Install with `pip install paramiko` on systems with Rust, or use pre-built wheels.
