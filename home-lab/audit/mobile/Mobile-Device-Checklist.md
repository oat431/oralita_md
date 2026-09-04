---
tags: [mobile, android, moc, checklist]
---

# Mobile Device Checklist

Audit index for the user's Android phone — **Xiaomi Redmi Note 14 Pro+ 5G (24115RA8EG, HyperOS)** — audited from SAHACHAN-LAPTOP via ADB. Mirrors the [[Personal-Computer-Checklist]] conventions: dated snapshot notes, real command output as evidence, findings tracked as R# rows with outcomes.

> **Tooling prerequisite:** platform-tools installed at `C:\Users\Admin\platform-tools\` + phone-side USB debugging — see [[ADB-Mobile-Audit-Manual]] (install and USB-debugging enablement are **user-executed manually**, high-risk boundary).

## Audit Log

| Date | Note | Focus |
|---|---|---|
| 2026-09-04 | [[ADB-Mobile-Audit-Manual]] | Reference manual + tooling prerequisite created; first audit pending |
| 2026-09-04 | [[mobile-audit-2026-09-04]] | Full first audit (adb sections complete): 10 findings R1–R10; manual on-phone checks + hardening pending |
| 2026-09-04 | [[ADB-Audio-Telemetry-Cheatsheet]] | Audio telemetry reference for audiophile-profile session (BT codec, bit-perfect check, USB DAC) |

## Standing Checklist

Numbered sections, each audited per the command map in [[ADB-Mobile-Audit-Manual]] §5 (adb) and §8 (manual on-phone checks).

| # | Section | Method | Status (2026-09-04) |
|---|---|---|---|
| 1 | Identity & baseline (model, HyperOS/Android, build fingerprint) | adb `getprop` | ✅ Android 16 / HyperOS 3.0.304, as expected |
| 2 | Security posture (patch date, verified boot, bootloader lock, encryption, private DNS, adb state) | adb `getprop` + `settings get` | ⚠️ R1 patch 95 d · R2 adb on · R3 private DNS opportunistic |
| 3 | Update risk (patch age vs Xiaomi quarterly cadence, confirmed update policy) | adb + web/Xiaomi trust page | ⚠️ R1 September quarterly due |
| 4 | App inventory (third-party packages, installer attribution, Xiaomi ad/analytics packages) | adb `pm list` | ⚠️ R4 one sideload; R7 ad stack optional; else clean |
| 5 | Runtime permissions review (dangerous grants per app) | adb `dumpsys package` | ⚠️ R5 majorcineplex background location · R6 four broader-than-purpose apps |
| 6 | Battery & thermal health | adb `dumpsys battery` / `thermalservice` | ✅ 35.5 °C charging, no throttling |
| 7 | Storage pressure (/data free) | adb `df` / `diskstats` | ✅ 27 % used, 341 G free |
| 8 | Backup & recovery (bmgr state + manual Google One/Drive coverage) | adb `bmgr` + on-phone | ✅ enabled, Google transport active · coverage ⏳ manual |
| 9 | Manual on-phone checks (screen lock/biometrics, Play Protect, Find Device, SIM PIN, permission manager, auto-update, unknown VPN) | on-phone (manual) | ⏳ pending user verification |
| 10 | Findings & recommendations (R# table, severity, owner, outcome) | synthesized | ✅ R1–R10 recorded in [[mobile-audit-2026-09-04]] |
| 11 | Post-audit hardening (USB debugging off / authorizations revoked — user executes) | adb verify + on-phone | ⏳ pending |

## Boundaries

- **Audit = read-only.** Remediation (`pm disable/uninstall`, `settings put`) only after explicit user approval, recorded in the dated note.
- **User executes manually:** platform-tools install, USB debugging toggle, USB-debugging revocation, any credential/key-material action.
- **Never in scope:** bootloader unlock, rooting, flashing, "USB debugging (Security settings)", "Install via USB".
- **Privacy:** device metadata to vault; personal content (photos, messages, app data) never leaves the phone.

## Related

[[ADB-Mobile-Audit-Manual]] · [[Personal-Computer-Checklist]] · `home-lab/audit/personal-computer/`
