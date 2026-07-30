# SSH on Windows (Git Bash / MINGW64) — Pitfalls & Workarounds

## Ed25519 Key with Passphrase Fails Silently

**Symptom:** `ssh -vvv` shows "Server accepts key" then "we did not send a packet, disable method" → Permission denied.

**Root cause:** Windows OpenSSH client (MINGW64) fails to sign with passphrase-protected ed25519 keys in non-interactive mode. The hostbound key extension (`publickey-hostbound-v00@openssh.com`) signing step silently fails.

**Fix:** Generate a separate automation key without passphrase:
```bash
ssh-keygen -t ed25519 -C "automation" -f ~/.ssh/id_homelab -N ""
```
Keep your passphrase-protected key for personal use. Use the no-passphrase key for scripts, cron, and agent automation.

**Alternative:** RSA keys work fine with passphrases on Windows:
```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa_automation -N ""
```

## SSH_ASKPASS for Scripted Password Auth

When you need to SSH with a password from a script (e.g., initial setup before keys are deployed):

```bash
cat > /tmp/ssh_pass.sh << 'SCRIPT'
#!/bin/bash
echo 'your-password'
SCRIPT
chmod +x /tmp/ssh_pass.sh

# Use it
SSH_ASKPASS=/tmp/ssh_pass.sh SSH_ASKPASS_REQUIRE=force DISPLAY=:0 \
  ssh -o StrictHostKeyChecking=no user@host "command" < /dev/null
```

⚠️ `< /dev/null` is required to prevent SSH from reading stdin.
⚠️ Clean up `/tmp/ssh_pass.sh` after use — it contains the password in plaintext.

## No sshpass on MINGW64

`sshpass` is not available in Git Bash/MSYS2. The SSH_ASKPASS trick above is the workaround. Don't waste time looking for `sshpass`, `expect`, or `pacman` in this environment.

## paramiko (Python SSH) on Windows

Installing paramiko on MSYS2 Python requires Rust (bcrypt dependency). Either:
- Use the SSH_ASKPASS approach instead
- Install via `python3 -m pip install --break-system-packages paramiko` on systems with Rust available
- Use the Hermes venv Python if paramiko is pre-installed there
