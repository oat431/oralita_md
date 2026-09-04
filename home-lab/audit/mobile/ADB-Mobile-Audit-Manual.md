---
tags: [android, adb, reference, howto, mobile]
aliases: [ADB Manual, Mobile Audit Manual]
---

# ADB Mobile Audit Manual — Redmi Note 14 Pro+ 5G

> **Created:** 2026-09-04
> **Applies to:** Xiaomi Redmi Note 14 Pro+ 5G (HyperOS), audited from SAHACHAN-LAPTOP (Windows 11)
> **Checklist:** [[Mobile-Device-Checklist]]
> **Status:** 🟢 Reference ready — platform-tools install pending (user executes manually)

---

## 1. Purpose & Trust Model

ADB (Android Debug Bridge) is the official Google tool for inspecting an Android
device over USB. It gives shell-level **read access to system properties, service
state, package lists, and permissions** — exactly the telemetry a mobile audit
needs, without root.

**Audit discipline (mirrors the PC audit conventions):**

- Every claim in an audit note is backed by real command output. No guessed statuses.
- **Read-only during audit**: `getprop`, `dumpsys`, `pm list`, `settings get`, `df`, `bmgr enabled`. No `pm uninstall`, no `pm disable`, no `settings put`, no installs — remediation only after explicit user approval.
- **Data privacy**: device identifiers (model, build, patch level, package names) go to the vault; personal content (photos, messages, app data, contacts) never leaves the phone.
- **High-risk boundary — user executes manually**: installing platform-tools, enabling/disabling USB debugging, revoking USB authorizations. Enabling USB debugging temporarily weakens the phone's posture; it stays in the user's hands.
- **Never in scope**: bootloader unlock, Mi Unlock tool, rooting, flashing, the "USB debugging (Security settings)" toggle, "Install via USB". The bootloader path also has Xiaomi's account-binding wait — irrelevant here and deliberately untouched.

## 2. Install Platform-Tools on the PC (user executes)

Google ships adb as a self-contained zip — no installer, no services, no registry changes.

| Step | Action | Detail |
|---|---|---|
| 1 | Download official zip | Release notes page: <https://developer.android.com/tools/releases/platform-tools> — take the Windows link from there. Direct link as of **2026-09-04**: `https://dl.google.com/android/repository/platform-tools_r37.0.1-win.zip` (**37.0.1, July 2026** — verified live, HTTP 206). If a direct link 404s, the version moved on: use the release-notes page. |
| 2 | Verify provenance | File should be signed by Google LLC (Properties → Digital Signatures). Only use the `dl.google.com` domain — never third-party "adb download" mirrors. |
| 3 | Extract | To `C:\Users\Admin\platform-tools\` (so `adb.exe` sits at `C:\Users\Admin\platform-tools\adb.exe`). |
| 4 | PATH (optional) | Add the folder to the user PATH for convenience, or just call the full path from any shell. |
| 5 | Verify | `adb version` → expect `Android Debug Bridge version 1.0.41`, `Version 37.0.1-<hash>`. |
| 6 | Uninstall anytime | Delete the folder. Nothing else to clean up. |

Firewall: outbound HTTPS only for the download; adb itself is local USB (and localhost for forward/reverse ports) — no inbound exposure.

## 3. Phone-Side Preparation (HyperOS)

All steps on the phone; Xiaomi gates some toggles behind account/SIM presence.

| Step | On the phone | Notes |
|---|---|---|
| 1 | Settings → About phone → Specifications → tap **OS version** 7× | Toast: "You are now a developer". Developer options now exist under Additional settings. |
| 2 | Settings → Additional settings → Developer options → **USB debugging** ON | Xiaomi gate: HyperOS may demand a **Mi account sign-in and/or a SIM card** before the toggle works (anti-tamper measure). If the toggle is greyed or a popup demands account/SIM — that is the reason, not a defect. |
| 3 | Leave OFF: "USB debugging (Security settings)", "Install via USB", "OEM unlocking" | None are needed for a read-only audit. Each one widens the attack surface for no benefit here. |
| 4 | Connect USB cable → watch for the **RSA fingerprint dialog** | Tick **"Always allow from this computer"**, then Allow. The Allow button often has a ~10 s countdown before it activates — normal HyperOS behavior, not a hang. |
| 5 | Verify from the PC | `adb devices -l` → the phone must list with state **`device`**. |

**Authorization states (`adb devices`):**

| State | Meaning | Fix |
|---|---|---|
| `device` | Authorized and ready | — |
| `unauthorized` | RSA dialog not (yet) accepted | Unlock phone, accept the prompt (replug if no prompt appears) |
| `offline` | Stale daemon/connection | Replug; `adb kill-server && adb devices` |
| *(empty)* | Not seen at all | Cable/driver — see §4 |

Cable note: many USB cables are charge-only. If the device list stays empty, try a known data-capable cable before suspecting drivers.

## 4. Troubleshooting (Windows + Xiaomi Quirks)

| Symptom | Likely cause | Fix |
|---|---|---|
| `'adb' is not recognized` | Not on PATH | Call full path `C:\Users\Admin\platform-tools\adb.exe` or fix PATH |
| `adb devices` empty | Charge-only cable / bad port / driver | Try another cable + port; check Device Manager for "ADB Device" under Android Phone; Windows usually auto-installs via Windows Update |
| `unauthorized` | RSA not accepted | Accept dialog on phone; or Developer options → Revoke USB debugging authorizations, then replug and re-accept |
| `offline` / flapping | Daemon mismatch | `adb kill-server && adb start-server && adb devices` |
| Multiple serials listed | Other devices/emuators | Target one: `adb -s <serial> <command>` |
| `INSTALL_FAILED_USER_RESTRICTED` / "Install via USB" popup | Appears only when *installing* APKs (MIUI/HyperOS protection) | An audit never installs anything — if you see this popup, cancel it. It must not appear during the audit. |
| `getprop` returns empty for a key | Property renamed in this HyperOS build | Record it as unrecorded/n.a. in the note; do not invent values |

## 5. Audit Command Map (read-only)

All commands run as `adb shell <command>` (or `adb shell` into an interactive shell). "Expected" values are grounded expectations for this device — record what you actually see, never assume.

| # | Section | Command(s) | Shows / expected |
|---|---|---|---|
| 1 | Identity | `getprop ro.product.marketname; getprop ro.product.model; getprop ro.product.device; getprop ro.build.fingerprint; getprop ro.build.display.id; getprop ro.build.date.utc` | Marketing name (e.g. REDMI NOTE 14 PRO+ 5G); model code (global variant is expected as `24115RA8EG` — record as-is if different); build fingerprint; build timestamp |
| 2 | OS version | `getprop ro.build.version.release; getprop ro.mi.os.version.name; getprop ro.mi.os.version.incremental; getprop ro.build.version.security_patch` | Android version; HyperOS version; **security patch date** (core SLI of the audit) |
| 3 | Boot security | `getprop ro.boot.verifiedbootstate; getprop ro.boot.flash.locked; getprop ro.boot.vbmeta.device_state` | `green` + `1` + `locked` = bootloader locked, Verified Boot intact |
| 4 | Encryption | `getprop ro.crypto.state; getprop ro.crypto.type` | Expected `encrypted` + `file` (File-Based Encryption) |
| 5 | ADB & DNS posture | `settings get global adb_enabled; settings get global private_dns_mode; settings get global private_dns_specifier` | `adb_enabled` = 1 during audit (0 after hardening); private DNS: `off` = finding, `opportunistic` = ok, `hostname` = strict |
| 6 | App inventory | `pm list packages -3 | sort` (count: `pm list packages -3 | wc -l`); `pm list packages -3 -i`; `pm list packages -s | wc -l` | All third-party packages; installer attribution (may be `null` on newer builds — record as n.a.); system package count |
| 7 | Xiaomi ad/analytics packages | `pm list packages | grep -iE 'msa|miui.system|analytics|aduard|tracker'` | e.g. `com.miui.msa.global` (MIUI System Ads), `com.google.android.apps.tachyon`-style carriers bloat — presence is default Xiaomi behavior, noted not condemned; removal needs explicit approval |
| 8 | Runtime permissions | per-app: `dumpsys package <pkg> | grep -A20 'runtime permissions'` | Scripted pass over all `-3` packages; summarized to vault (raw dump never pasted) |
| 9 | Battery | `dumpsys battery` | Level %, `temperature` (tenths of °C — 421 = 42.1 °C), charge counter, USB input |
| 10 | Thermal | `dumpsys thermalservice` (fallback: `dumpsys thermal`) | Current temperatures + throttling status; may be restricted on some builds |
| 11 | Storage | `dumpsys diskstats; df -h /data` | Free bytes on /data, usage pressure |
| 12 | Backup | `bmgr enabled` | `Backup Manager currently enabled/disabled` — transport state; Google One config itself is a manual check (§8) |
| 13 | Screen/time | `settings get global screen_off_timeout; getprop persist.sys.timezone` | Basic hygiene |

## 6. Interpretation Thresholds

What converts an observation into a numbered finding (R#):

| Observation | Severity | Rationale |
|---|---|---|
| Security patch older than ~90 days at audit date | ⚠️ High | Xiaomi ships quarterly patches on this tier; a stale patch = known-CVE exposure window |
| `verifiedbootstate` ≠ `green` / bootloader unlocked | ❌ Critical | Verified Boot disabled = tampered trust chain (would also mean the device is rooted — re-scope the audit) |
| `ro.crypto.state` ≠ `encrypted` | ❌ Critical | Stolen phone = readable data |
| Private DNS `off` | ⚠️ Medium | Plain-text DNS; recommend `dns.google` or `one.one.one.one` (user decision) |
| Battery temp > 45 °C at idle | ⚠️ High | Thermal/battery health issue — investigate before it becomes hardware damage |
| /data free < 10 % | ⚠️ Medium | Update installs and app performance degrade |
| `bmgr` disabled with no Google One backup verified | ⚠️ High | Single point of failure: lost/broken phone = lost data |
| Xiaomi ad/analytics packages present | 🟡 Low/Info | Default on Xiaomi; document, removal optional with approval |
| `adb_enabled` still 1 after audit | ⚠️ Medium | Hardening step missed (see §7) |

## 7. After the Audit — Hardening (user executes manually)

| Step | Action | Why |
|---|---|---|
| 1 | Developer options → **USB debugging OFF** (or at minimum **Revoke USB debugging authorizations**) | Any PC with the "always allow" grant could drive the phone. Off = surface closed. |
| 2 | If keeping debugging for future audits: revoke authorizations after each session and re-accept on next use | Trust is re-established deliberately, not left stale |
| 3 | Verify: replug phone, `adb devices` → empty or `unauthorized` | Real confirmation, not assumption |
| 4 | Decide and record: Developer options kept ON (convenience for quarterly audits) vs OFF (maximal closure) | Trade-off recorded in the audit note |

## 8. What ADB Cannot See — Manual On-Phone Checklist

Verified by eye on the phone during the audit, recorded in the note:

| Check | Where (HyperOS) | Looking for |
|---|---|---|
| Screen lock + biometrics | Settings → Passwords & security | Lock set (PIN ≥ 6 / password), fingerprints active, lockdown option known |
| Play Protect | Play Store → Profile → Play Protect | Scanning ON, last scan recent |
| Find Device | Settings → Mi Account / Google Find Hub | Reachable if lost — both stores considered |
| SIM PIN | Settings → SIM cards | PIN on (protects against SIM-swap-on-theft) |
| Google One / Drive backup | Settings → Google → Backup | Photos, contacts, SMS coverage; last successful backup date |
| Permission manager | Settings → Privacy → Permission manager | Camera/mic/location granted to apps that don't need them |
| Play Store auto-update | Play Store → Settings | Auto-update ON (patch delivery path) |
| VPN / unknown profiles | Settings → VPN | Nothing unknown |

## 9. Update-Policy Context (recorded 2026-09-04)

- Released globally **January 2025**; shipped with Android 14 / HyperOS 1.0.
- Community-reported policy: **3 major Android upgrades + 4 years of security patches** (→ security support into ~2029). Treat as provisional: verify against Settings → Updater and Xiaomi's official security-update page (`trust.mi.com/misrc/updates/phone`) during the first audit, and record the confirmed numbers in [[Mobile-Device-Checklist]].

## Appendix A — Dated Audit Note Template

```markdown
# Mobile Audit — Redmi Note 14 Pro+ 5G (24115RA8EG)

> **Date:** YYYY-MM-DD
> **Checklist:** [[Mobile-Device-Checklist]]
> **Status:** ✅ Complete / 🟡 Follow-up (n open findings)

## System Overview
| Field | Value |
|---|---|
| HyperOS / Android | ... |
| Security patch | ... (age: N days) |
| Verified boot / crypto | green, locked / encrypted, file |
| Third-party packages | N (installer-known: N) |
| Battery temp / level | ... |
| /data free | ... |

## 1. Identity & Baseline — ✅
| Check | Result | Status |
|---|---|---|

## 2. Security Posture — ✅/⚠️/❌
...

## Findings & Recommendations
| R# | Severity | Finding | Recommendation | Owner | Outcome |
|---|---|---|---|---|---|
| R1 | ⚠️ | ... | ... | user (manual) | |

## Manual On-Phone Checks
| Check | Result | Status |
|---|---|---|

## Related
[[Mobile-Device-Checklist]] · [[ADB-Mobile-Audit-Manual]]
```

## Appendix B — Command Cheat Sheet (in audit order)

```bash
ADB="C:/Users/Admin/platform-tools/adb.exe"
"$ADB" devices -l                          # state must be 'device'
"$ADB" shell getprop ro.product.marketname
"$ADB" shell getprop ro.product.model
"$ADB" shell getprop ro.product.device
"$ADB" shell getprop ro.build.fingerprint
"$ADB" shell getprop ro.build.display.id
"$ADB" shell getprop ro.build.date.utc
"$ADB" shell getprop ro.build.version.release
"$ADB" shell getprop ro.mi.os.version.name
"$ADB" shell getprop ro.build.version.security_patch
"$ADB" shell getprop ro.boot.verifiedbootstate
"$ADB" shell getprop ro.boot.flash.locked
"$ADB" shell getprop ro.crypto.state
"$ADB" shell getprop ro.crypto.type
"$ADB" shell settings get global adb_enabled
"$ADB" shell settings get global private_dns_mode
"$ADB" shell settings get global private_dns_specifier
"$ADB" shell 'pm list packages -3 | wc -l'
"$ADB" shell 'pm list packages -3 | sort'
"$ADB" shell 'pm list packages | grep -iE "msa|analytics|ads"'
"$ADB" shell dumpsys battery
"$ADB" shell dumpsys thermalservice
"$ADB" shell df -h /data
"$ADB" shell bmgr enabled
```

## Related

[[Mobile-Device-Checklist]] · [[Personal-Computer-Checklist]] · `home-lab/audit/personal-computer/`
