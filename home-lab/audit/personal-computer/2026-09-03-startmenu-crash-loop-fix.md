# Start Menu Crash Loop Fix — 2026-09-03

> **Machine:** SAHACHAN-LAPTOP (Acer Nitro ANV15-41) — Windows 11 Home Insider Preview Dev, build 26340
> **Status:** 🔴 Diagnosed — **fix pending reboot** (user reboots manually)
> **Related:** [[personal-computer-audit-2026-09-03]] (F1/R1), [[Personal-Computer-Checklist]]

---

## Symptom

StartMenuExperienceHost.exe crash loop — Event 1000 (Application Error), every ~2–4 minutes:

```
Faulting application name: StartMenuExperienceHost.exe, version: 10.0.26100.8951
Faulting module name: StartDocked.dll, version: 10.0.26100.9233
Exception code: 0xc000027b   (stowed exception — XAML/WinUI state failure)
```

**38 crashes in 14 days, ALL on 2026-09-03** — first at **11:44:48**, none in the 13 days before.

## Evidence & Timeline (2026-09-03)

| Time | Event |
|------|-------|
| 10:52–11:50 | AppX deployment churn: license-manager errors (0x800703f0, Todos/Store), cleanup loop failing 0x5 on stale packages every 6 min |
| **11:44:48** | First Start menu crash (crash onset) |
| 11:50 | Status updates: ScreenSketch 11.2607.21.0, StartExperiencesApp 1.380.2.0 |
| 12:01 | `Get-AppxPackage \| ConvertTo-Json` (user diagnostic) **hangs — process still alive 4.5 h later** (PID 38224); WU scan finds 0 updates; StartExperiencesApp 1.380.2.0 flagged `REGISTRATION_REQUIRED_BLOCKING`, then updated → 1.398.0.0; ScreenSketch updated 21.0 → 22.0; NearbyShare removed |
| 12:11 | Trust-label validation wave (Teams, Edge, Paint, Photos, OneDrive, Office) |
| **14:25** | AppX: ScreenSketch register op **hung and cancelled** (event 678) |
| **15:21** | AppX: StartExperiencesApp register op **hung and cancelled**; Zed removed (Remove-AppxPackage process still alive, PID 61636) |
| **16:31:32** | My `Reset-AppxPackage` (non-elevated attempt) **queued a Remove op on StartMenuExperienceHost itself** — never completed; blocks every subsequent AppX op (Store updates will fail until cleared) |

## Root Cause (hypothesis, high confidence)

**AppX deployment pipeline (AppXSvc / AppXDeploymentServer) wedged since ~12:01–14:25**, in the middle of inbox-app servicing churn. Version skew on disk confirms a partially-serviced Start host: exe @ 10.0.26100.8951, StartDocked.dll @ 10.0.26100.9233. The crashing host renders against inconsistent registration → stowed exception loop. All further AppX operations (register/reset/remove) hang behind the stuck queue — including the reset I queued at 16:31.

## Actions Attempted (before diagnosis)

| Attempt | Result |
|---------|--------|
| Clear Start host cache (`LocalState` → backup at `%TEMP%\startmenu-LocalState-backup-20260903-163637`) | ❌ crashes continued (2 more within 4 min) |
| `Reset-AppxPackage` (non-elevated) | ❌ hung → queued stuck Remove op (16:31:32) |
| `Add-AppxPackage -Register` Start host + experiences (non-elevated) | ❌ hung behind stuck queue |

## Recommended Fix (after user reboots)

A reboot clears the wedged service state; the queued Start-package reset replays cleanly.

1. **Reboot** (Start → Power → Restart, or `shutdown /r /t 0`).
2. After login, verify no new crashes:
   ```powershell
   Get-WinEvent -FilterHashtable @{LogName='Application'; ProviderName='Application Error'; StartTime=(Get-Date).AddMinutes(-10)} |
     Where-Object { $_.Message -match 'StartMenuExperienceHost' } | Measure-Object
   ```
   Expect count **0**.
3. Confirm the queued reset completed (AppX log shows no stuck Remove):
   ```powershell
   Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-AppXDeploymentServer/Operational'} -MaxEvents 20 |
     Format-Table TimeCreated, Id, Message -AutoSize
   ```
4. If crashes persist → run elevated (admin PowerShell):
   ```powershell
   Get-AppxPackage Microsoft.Windows.StartMenuExperienceHost | Reset-AppxPackage
   Get-AppxPackage Microsoft.StartExperiencesApp      | Reset-AppxPackage
   ```
5. If still crashing → system file repair (admin, slow):
   ```powershell
   DISM /Online /Cleanup-Image /RestoreHealth
   sfc /scannow
   ```
6. If still crashing → latest Insider Dev flight (Settings → Windows Update) — the file skew (8951/9233) may only be resolved by the next build; report via Feedback Hub.

## Side Notes

- Until the reboot, **Store app installs/updates will hang or fail** (stuck deployment queue) — expected.
- Stray hung processes to confirm gone after reboot: `powershell` PIDs 38224, 61636, 58108 (all pre-reboot).
- Backups created during this session (safe to delete after reboot confirms fix):
  `%TEMP%\startmenu-LocalState-backup-20260903-163637`
