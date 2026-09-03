# Personal Computer Audit — `SAHACHAN-LAPTOP`

> **Date:** 2026-09-03 (UTC+7)
> **Checklist:** [[Personal-Computer-Checklist]]
> **Status:** ✅ Healthy — 2 open 🟡 findings (Start menu crash loop, Search indexer timeouts), no 🔴 issues
> **Scope:** Read-only audit of all essential components; no changes made

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
| Cooling/fans | ⚠️ | No thermal telemetry available non-elevated (not audited) |

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
| Wear/temperature counters | ⚠️ | `Get-StorageReliabilityCounter` returned nothing non-elevated — rerun once as admin for wear % + power-on hours |
| Temp folder hygiene | ✅ | User temp 226 MB, C:\Windows\Temp 0 MB — clean |
| Pagefile | ✅ | C:\pagefile.sys (system-managed; allocation not reported non-elevated) |

No SMART/health alarms. C: holds 267 GB used (OS + apps + Steam) — healthy, no pressure.

---

## 3. Memory & Performance

| Item | Status | Notes |
|------|--------|-------|
| Memory headroom | ✅ | 14.5 GB free / 31.3 GB (54% used) at audit time |
| Top consumers | ✅ | msedge (~1.5 GB total), dwm 770 MB, explorer 521 MB, Hermes 509 MB, MsMpEng 450 MB, Discord 435 MB |
| CPU sample | ✅ | 64–67% during audit run — active-workload snapshot (Edge + Discord + audit), not a sustained load |
| Pagefile | ✅ | Present; no low-memory events in log |

---

## 4. Networking & Connectivity

| Item | Status | Notes |
|------|--------|-------|
| Ethernet (Realtek 1 Gbps) | ✅ | Up — 192.168.1.123, GW 192.168.1.1 |
| Wi-Fi (MediaTek MT7921) | ⚠️ | Disconnected (on Ethernet) |
| USB-Ethernet (ASIX) | ⚠️ | Disconnected |
| DNS | ⚠️ | 94.140.14.49 / 94.140.14.59 = **AdGuard DNS public (filtering)** — laptop does NOT use homelab AdGuard (192.168.1.121); likely intentional, verify |
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
| Firewall | ✅ | All 3 profiles enabled; inbound/outbound defaults not overridden (Windows default = block inbound unless allowed) |
| UAC | ✅ | Enabled (LUA=1), default prompt level (5) |
| Windows updates | ✅ | KB5124043/4042/2776/0708 installed through 08-22; no pending reboot (CBS/WU flags clean) |
| BitLocker / device encryption | ⚠️ | Not queryable non-elevated — verify once with admin (`manage-bde -status`) |
| Insider channel | ⚠️ | **Dev Channel build 26340** — preview software by design; expect occasional shell/app instability (see §8) |

---

## 6. Software & Toolchain

| Component | Status | Detail |
|-----------|--------|--------|
| Git | ✅ | 2.49.0 |
| GitHub CLI | ✅ | 2.98.0 |
| Node.js | ✅ | v22.23.2 (via **nvm4w**, C:\nvm4w\nodejs) — registry MSI entry 22.14.0 is stale/secondary |
| Python (python.org) | ✅ | 3.12.10 — py launcher default, `PIPX_DEFAULT_PYTHON` pinned here (2026-09-03 fix) |
| Python on PATH | ⚠️ | `python` → Hermes venv 3.11.15, `python3` → **MSYS2 GCC 3.12.7** (ucrt64 before Python312 in PATH) — MSYS2 builds unsupported by uv/pipx; fixed for pipx via env var, PATH order still a footgun |
| pipx / uv | ✅ | pipx 1.17.2 (scoop), uv 0.12.9 |
| Go | ✅ | go1.25.3 windows/amd64 |
| Java | ✅ | **GraalVM JDK 25 LTS** (C:\Program Files\graalvm-25) |
| Docker Desktop | ⚠️ | 4.86.0 installed; **engine stopped** (com.docker.service Manual — app not running; normal when unused). Bundled kubectl v1.36.1 |
| PowerShell | ✅ | 7.6.5 (+ Windows PowerShell 5.1) |
| Tailscale | ✅ | 1.102.2, service Auto/Running |
| Package managers | ✅ | scoop (pipx only), winget 1.30.110-preview |
| Obsidian | ✅ | 1.12.4 (vault on F:) |
| Data tools | ✅ | MongoDB Compass 1.49.14, DBeaver 26.1.4, Postman 12.15.6 |
| Microsoft 365 | ✅ | en-us, 16.0.20326 |
| VS Code | ❌ | Not installed (no other IDE detected either) |
| Other | ✅ | Edge, Discord, Steam, Logitech G HUB, NVIDIA App, Acer bloat agents (AcerQAAgent) |

---

## 7. Services & Startup

| Service | Status | Start | Note |
|---------|--------|-------|------|
| Tailscale | ✅ Running | Automatic | Mesh VPN active |
| WinDefend | ✅ Running | Automatic | Defender engine |
| WSearch | ✅ Running | Automatic | ⚠️ see §8 — transaction timeouts |
| Spooler | ✅ Running | Automatic | Print spooler |
| com.docker.service | ⚠️ Stopped | Manual | Docker Desktop not running |
| ssh-agent | ❌ Disabled | Disabled | Deliberate — no SSH agent service |
| wuauserv | Stopped | Manual | Normal (UsoSvc orchestrates) |

---

## 8. Event Log — Findings (last 7 days)

| # | Severity | Event | Finding |
|---|----------|-------|---------|
| F1 | 🟡 | Application Error 1000 — `StartMenuExperienceHost.exe`, faulting module `StartDocked.dll` | **Start menu crash loop** — dozens of crashes today (16:21 back to 15:22+, plus earlier). Classic Insider-Dev shell instability. Annoyance only; no data risk |
| F2 | 🟡 | SCM 7011 | **WSearch service timeout** (30 s transaction) × 6 today (11:51–14:02) — Search indexer stalling; may cause sluggish search |
| F3 | 🟢 | DCOM 10001 / 10016 / 10010 | Permission + activation noise (standard Windows chatter, elevated on Insider) |
| F4 | 🟢 | NDIS 10317 — Wi-Fi Direct Virtual Adapter power transition | Wi-Fi power-state glitch; Wi-Fi unused (Ethernet) |
| F5 | 🟢 | winsrvext 100 — Steam webhelper + AcerQAAgent delaying shutdown ~5 s | Cosmetic; Acer QA agent adds shutdown delay |
| F6 | ✅ | No Kernel-Power 41, no WHEA, no disk errors | No power/BSOD/hardware fault events in window |

---

## 9. Findings & Recommendations

| # | Sev | Action | Priority |
|---|-----|--------|----------|
| R1 | 🟡 | **Start menu crash loop (F1)** — apply latest Insider update if available; if it persists: restart `explorer.exe`, then `Get-AppxPackage Microsoft.Windows.StartMenuExperienceHost \| Reset-AppxPackage`; report via Feedback Hub (Dev Channel = expected instability) | Medium |
| R2 | 🟡 | **Search indexer timeouts (F2)** — if search feels slow, rebuild index (Settings → Privacy & Security → Searching Windows → Advanced). Re-check next audit | Low |
| R3 | 🟢 | **One elevated pass to close gaps:** `manage-bde -status` (BitLocker/device encryption) + `Get-PhysicalDisk \| Get-StorageReliabilityCounter` (NVMe wear/temperature) | Low |
| R4 | 🟢 | **PATH hygiene** — msys2/ucrt64 sits before Python312 → `python3` = MSYS2 GCC build; uv/pipx reject it (fixed via `PIPX_DEFAULT_PYTHON` 2026-09-03). Optional: move `AppData\Local\Programs\Python\Python312` ahead of MSYS2, or keep as-is with awareness | Low |
| R5 | 🟢 | **DNS consistency** — laptop resolves via AdGuard public (94.140.14.49/.59), not homelab AdGuard Home (192.168.1.121). If homelab filtering/custom rules should apply here, point DNS at 192.168.1.121 (or keep public AdGuard for roaming — both are ad-filtering) | Low |
| R6 | 🟢 | **Acer bloat (AcerQAAgent)** — optional: disable startup to cut ~5 s shutdown delay | Optional |
| R7 | ✅ | C: at 44% free — healthy; no cleanup required. No action | — |

---

## Related

- [[Personal-Computer-Checklist]] — index of PC audits
- [[Homelab-Infra-Checklist]] — homelab server audits (192.168.1.121 / 100.73.143.25)
- [[home-lab-apps]] — app/port registry
- [[home-lab-installation]] — server setup guides
