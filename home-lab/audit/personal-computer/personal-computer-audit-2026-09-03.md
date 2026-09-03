# Personal Computer Audit — `SAHACHAN-LAPTOP`

> **Date:** 2026-09-03 (UTC+7)
> **Checklist:** [[Personal-Computer-Checklist]]
> **Status:** ✅ Healthy — all findings addressed same-day; R1–R8 closed (see §9). Incident note: [[2026-09-03-startmenu-crash-loop-fix]]
> **Scope:** Read-only audit of all essential components; changes below executed post-audit with approval

---

## System Overview

| Item | Value |
|------|-------|
| **OS** | Windows 11 Home Insider Preview (Single Language) — build 26340, **Dev Channel** (BranchName=Dev, Ring=External) |
| **OS installed** | 2026-08-02 |
| **Uptime** | 4d 1h (last boot 2026-08-30 15:03) |
| **Model** | Acer Nitro ANV15-41 (laptop, chassis: Notebook) |
| **BIOS** | INSYDE Corp. V1.51 |
| **CPU** | AMD Ryzen 5 6600H — 6C/12T, 3.3 GHz (FP7) |
| **RAM** | 32 GB DDR5-4800 (2× Kingston 16 GB) |
| **GPU** | NVIDIA RTX 3050 6GB Laptop + AMD Radeon 660M (iGPU) |
| **Disks** | Samsung MZVL2512HCJQ 512 GB NVMe (C:) + WD_BLACK SN770 1 TB NVMe (E:+F:) |
| **Battery** | AP18E7M — 100% (on AC) |
| **LAN IP** | 192.168.1.123 (Ethernet, 1 Gbps, DHCP) |
| **Tailscale IP** | 100.90.67.14 |
| **Power plan** | Acer (custom) |
| **User** | Admin (WORKGROUP) |

---

## 1. Hardware & Base Platform

| Item | Status | Notes |
|------|--------|-------|
| Motherboard/BIOS | ✅ | INSYDE V1.51 — not cross-checked against Acer latest release ⚠️ |
| CPU | ✅ | Ryzen 5 6600H, 6C/12T, reported 3.3 GHz, load 12% at sampling |
| RAM | ✅ | 31.3 GB usable, 2× Kingston 16 GB DDR5 configured @ 4800 MHz |
| GPU | ✅ | RTX 3050 6GB Laptop (NVIDIA driver 616.56) + Radeon 660M — 1920×1080, 143 Hz (NVIDIA) / 165 Hz (AMD) reported |
| Battery | ✅ | AP18E7M @ 100%, on AC — no wear data without elevation |
| Cooling/fans | ⚠️ | No thermal telemetry non-elevated; advice given: NitroSense Auto for daily, FPS cap, raised rear edge |

**Note:** Dual-GPU (dGPU + iGPU) laptop with MUX reporting — both controllers report the panel. VRAM values from WMI are capped artifacts (RTX 3050 is the 6 GB variant per model name).

---

## 2. Storage & Disk Health

| Item | Status | Notes |
|------|--------|-------|
| Samsung MZVL2512HCJQ 512 GB (C:) | ✅ | NVMe SSD, Health: **Healthy**, OK |
| WD_BLACK SN770 1 TB (E: + F:) | ✅ | NVMe SSD, Health: **Healthy**, OK |
| C: [Acer] | ✅ | 208.2 GB free / 475.4 GB — **44% free** |
| E: [game and media] | ✅ | 143.3 GB free / 430.5 GB — 33% free |
| F: [work project and app] | ✅ | 384.5 GB free / 501 GB — **77% free** (Obsidian vault lives here) |
| Wear/temperature counters | ⚠️ | Not exposed by these NVMe models via `Get-StorageReliabilityCounter`; temps captured 2026-09-03: Samsung 69 °C (warm, normal under load), WD 48 °C |
| Temp folder hygiene | ✅ | User temp 226 MB, C:\Windows\Temp 0 MB — clean |
| Pagefile | ✅ | C:\pagefile.sys (system-managed) |

No SMART/health alarms. C: holds 267 GB used (OS + apps + Steam) — healthy, no pressure.

---

## 3. Memory & Performance

| Item | Status | Notes |
|------|--------|-------|
| Memory headroom | ✅ | 14.5 GB free / 31.3 GB (54% used) at audit time |
| Top consumers | ✅ | msedge (~1.5 GB total), dwm 770 MB, explorer 521 MB, Hermes 509 MB, MsMpEng 450 MB, Discord 435 MB |
| CPU sample | ✅ | 64–67% during audit run — active-workload snapshot, not a sustained load |
| Pagefile | ✅ | Present; no low-memory events in log |

---

## 4. Networking & Connectivity

| Item | Status | Notes |
|------|--------|-------|
| Ethernet (Realtek 1 Gbps) | ✅ | Up — 192.168.1.123, GW 192.168.1.1 |
| Wi-Fi (MediaTek MT7921) | ⚠️ | Disconnected (on Ethernet) |
| USB-Ethernet (ASIX) | ⚠️ | Disconnected |
| DNS | ✅ | AdGuard public 94.140.14.49/.59 (final). Tested homelab AdGuard 192.168.1.121 as primary — it answers `0.0.0.0` (blocked) for google.com → reverted; see R5 |
| Gateway ping | ✅ | 192.168.1.1 reachable |
| Internet | ✅ | 1.1.1.1 reachable |
| Homelab (Tailscale) | ✅ | 100.73.143.25 reachable — direct peer |
| Tailscale | ✅ | v1.102.2, this node = 100.90.67.14 |
| cloudflared | ✅ | Client v2025.8.1 installed locally |

---

## 5. Security

| Item | Status | Notes |
|------|--------|-------|
| Windows Defender | ✅ | AV enabled, real-time on, tamper protection on |
| Defender signatures | ✅ | v1.459.17.0, updated 2026-09-03 04:10 |
| Last quick scan | ✅ | 3 days ago |
| Firewall | ✅ | All 3 profiles enabled; defaults not overridden |
| UAC | ✅ | Enabled (LUA=1), default prompt level (5) |
| Windows updates | ✅ | KB5124043/4042/2776/0708 through 08-22; no pending reboot |
| BitLocker / device encryption | ✅ | **ON — C:/E:/F: all Protection On, 100% FullyEncrypted** (user enabled 2026-09-03, verified elevated; C: XTS-AES 128 with TPM + recovery-key protectors) |
| Insider channel | ⚠️ | **Dev Channel build 26340** — preview software by design |

---

## 6. Software & Toolchain

| Component | Status | Detail |
|-----------|--------|--------|
| Git | ✅ | 2.49.0 |
| GitHub CLI | ✅ | 2.98.0 |
| Node.js | ✅ | v22.23.2 (via **nvm4w**, C:\nvm4w\nodejs) |
| Python (python.org) | ✅ | 3.12.10 — py launcher default, `PIPX_DEFAULT_PYTHON` pinned here |
| Python on PATH | ✅ | Fixed 2026-09-03: HKCU PATH reordered (Python312 + Scripts + Launcher before msys2) + `python3.exe` shim added → fresh cmd/PowerShell resolve native 3.12.10. MSYS2 terminals still prepend their own bins (by design) |
| pipx / uv | ✅ | pipx 1.17.2 (scoop), uv 0.12.9 |
| Go | ✅ | go1.25.3 windows/amd64 |
| Java | ✅ | **GraalVM JDK 25 LTS** (C:\Program Files\graalvm-25) |
| Docker Desktop | ✅ | 4.86.0 — engine verified working (server 29.7.2); local images/containers intact. **WSL2 backend required on Home.** Bundled kubectl v1.36.1 |
| WSL2 | ✅ | Platform only (`--no-distribution`, no Ubuntu) — docker-desktop distro Running |
| PowerShell | ✅ | 7.6.5 (+ Windows PowerShell 5.1) |
| Tailscale | ✅ | 1.102.2, service Auto/Running |
| Package managers | ✅ | scoop (pipx only), winget 1.30.110-preview |
| Obsidian | ✅ | 1.12.4 (vault on F:) |
| Data tools | ✅ | MongoDB Compass 1.49.14, DBeaver 26.1.4, Postman 12.15.6 |
| Microsoft 365 | ✅ | en-us, 16.0.20326 |
| VS Code | ❌ | Not installed |
| Zed | ✅ | 1.17.2 native installer — DeepSeek (predictions + agent) + OpenClaw ACP configured; CLI on PATH |
| 7-Zip / VLC / fzf | ✅ | 26.02 / 3.0.23 / 0.74.3 — installed 2026-09-03 |
| gsudo / Everything | ✅ | 2.6.1 / 1.4.1.1032 — installed 2026-09-03 (user) |
| Other | ✅ | Edge, Discord, Steam, Logitech G HUB, NVIDIA App |

---

## 7. Services & Startup

| Service | Status | Start | Note |
|---------|--------|-------|------|
| Tailscale | ✅ Running | Automatic | Mesh VPN active |
| WinDefend | ✅ Running | Automatic | Defender engine |
| WSearch | ✅ Running | Automatic | Timeouts resolved after reboot (F2) |
| Spooler | ✅ Running | Automatic | Print spooler |
| com.docker.service | ⚠️ Stopped | Manual | Starts with Docker Desktop app |
| ssh-agent | ❌ Disabled | Disabled | Deliberate |
| wuauserv | Stopped | Manual | Normal (UsoSvc orchestrates) |

---

## 8. Event Log — Findings (last 7 days)

| # | Severity | Event | Finding |
|---|----------|-------|---------|
| F1 | ✅ Resolved | Application Error 1000 — `StartMenuExperienceHost.exe`, faulting module `StartDocked.dll` (0xc000027b) | Start menu crash loop — root cause: wedged AppX pipeline; **resolved by reboot** (0 crashes since) → [[2026-09-03-startmenu-crash-loop-fix]] |
| F2 | ✅ Resolved | SCM 7011 | WSearch transaction timeouts — **0 since reboot** |
| F3 | 🟢 | DCOM 10001 / 10016 / 10010 | Permission + activation noise (standard Windows chatter) |
| F4 | 🟢 | NDIS 10317 — Wi-Fi Direct Virtual Adapter power transition | Wi-Fi power-state glitch; Wi-Fi unused |
| F5 | 🟢 | winsrvext 100 — Steam webhelper + AcerQAAgent delaying shutdown ~5 s | Cosmetic |
| F6 | ✅ | No Kernel-Power 41, no WHEA, no disk errors | No power/BSOD/hardware fault events in window |

---

## 9. Findings & Recommendations

| # | Sev | Action | Priority |
|---|-----|--------|----------|
| R1 | ✅ Resolved | Start menu crash loop — reboot cleared the wedged AppX pipeline; 0 crashes since boot (16:52) | Medium |
| R2 | ✅ Resolved | Search indexer timeouts — 0 WSearch timeouts since reboot | Low |
| R3 | ✅ Done | Elevated pass completed 2026-09-03 — BitLocker/Device Encryption was OFF on all volumes (enabled since → R8 ✅); NVMe temps: Samsung 69 °C ⚠️ warm, WD 48 °C ✅ | Low |
| R4 | ✅ Done | **PATH hygiene** — HKCU PATH reordered 2026-09-03: Python312 + Scripts + Launcher before msys2; `python3.exe` shim added. Fresh cmd/PowerShell resolve native 3.12.10. Backups: `%TEMP%\PATH-backup-*.txt` | Low |
| R5 | ✅ Settled | **DNS** — homelab AdGuard blocks google.com **intentionally** (your choice, server-side). Laptop stays on AdGuard public (94.140.14.49/.59) by design — no impact on PC usage. If you ever want homelab custom rules *without* the Google block: AdGuard per-client settings, then re-point (1 command) | Low |
| R6 | ✅ Done | Acer Jumpstart + User Experience Improvement Program Service uninstalled (msiexec, verified). Optional: disable AcerQAAgent startup entry | Optional |
| R7 | ✅ | C: at 44% free — healthy; no action | — |
| R8 | ✅ Done (user) | **Disk encryption ON — verified elevated:** C:/E:/F: all Protection On, 100% FullyEncrypted. C: XTS-AES 128, TPM + numerical-password protectors. ⚠️ Reminder: confirm recovery key saved (MS account; E:/F: via `manage-bde -protectors -get`) | Medium |

---

## Related

- [[Personal-Computer-Checklist]] — index of PC audits
- [[2026-09-03-startmenu-crash-loop-fix]] — Start menu incident note
- [[Homelab-Infra-Checklist]] — homelab server audits (192.168.1.121 / 100.73.143.25)
- [[home-lab-apps]] — app/port registry
- [[home-lab-installation]] — server setup guides
