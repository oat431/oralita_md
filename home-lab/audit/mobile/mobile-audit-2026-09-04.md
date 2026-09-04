---
tags: [mobile, android, audit, redmi]
---

# Mobile Audit — Redmi Note 14 Pro+ 5G (24115RA8EG)

> **Date:** 2026-09-04 (18:30 SEAST) · audited from SAHACHAN-LAPTOP via ADB (platform-tools 37.0.1)
> **Checklist:** [[Mobile-Device-Checklist]] · **Method:** [[ADB-Mobile-Audit-Manual]] §5
> **Status:** 🟡 Complete (adb sections) — manual on-phone checks ⏳ pending user verification, post-audit hardening ⏳ pending

## System Overview

| Field | Value | Status |
|---|---|---|
| Device | Xiaomi Redmi Note 14 Pro+ 5G (`24115RA8EG`, `amethyst_global`) | ✅ as expected |
| OS | Android **16** (SDK 36) / **HyperOS 3.0** (`OS3.0.304.0.WOPMIDC`, MIUI V816) | ✅ current major |
| Build | `BP2A.250605.031.A3`, built **2026-06-24 04:22 UTC**, `release-keys` | ✅ |
| Security patch | **2026-06-01** → **95 days old** at audit date | ⚠️ R1 |
| Verified boot / bootloader | `green` / `flash.locked=1` / `vbmeta=locked` | ✅ |
| Encryption | `encrypted` + `file` (FBE) | ✅ |
| Third-party packages | **127** (406 total incl. system) | — |
| Battery | 100 %, 35.5 °C (AC charging), health Good | ✅ |
| /data | 124 G used / 465 G (**27 %**, 341 G free) | ✅ |
| Backup manager | Enabled, active transport = Google (`com.google.android.gms/.backup.BackupTransportService`) | ✅ (coverage = manual check) |

## 1. Identity & Baseline — ✅

| Check | Result |
|---|---|
| marketname / model / device | Redmi Note 14 Pro+ 5G / `24115RA8EG` / `amethyst` |
| Fingerprint | `Redmi/amethyst_global/amethyst:16/BP2A.250605.031.A3/OS3.0.304.0.WOPMIDC:user/release-keys` |
| Build date | 2026-06-24 04:22:34 UTC (epoch 1782274954) |
| Android / SDK | 16 / 36 · `first_api_level=34` (shipped Android 14, consistent with Jan 2025 launch) |
| HyperOS | OS3.0 (code 3), incremental `OS3.0.304.0.WOPMIDC`, MIUI platform V816 |
| Timezone | Asia/Bangkok |

## 2. Security Posture — ✅ / ⚠️

| Check | Result | Status |
|---|---|---|
| `ro.secure` / `ro.debuggable` / `ro.adb.secure` | 1 / 0 / 1 | ✅ production-hardened |
| Build tags | `release-keys` | ✅ |
| Verified boot | `green`, bootloader `locked` (both boot + vbmeta) | ✅ |
| Encryption | FBE (`encrypted` / `file`) | ✅ |
| Security patch | 2026-06-01 (95 d) | ⚠️ R1 |
| `adb_enabled` | 1 (session state; hardening = R2) | ⚠️ R2 |
| Wireless debugging (`adb_wifi_enabled`) | 0 | ✅ |
| Mock location | 0 | ✅ |
| Private DNS | mode=`opportunistic`, specifier=`c9daf585.d.adguard-dns.com` | ⚠️ R3 — specifier only applies in **hostname** mode; AdGuard DoT filtering likely **not** enforced |
| Always-on VPN | none configured (no VPN apps installed) | ℹ️ |
| `stay_on_while_plugged_in` | 0 | ✅ no stray dev option |

## 3. Update Risk — ⚠️

| Check | Result | Status |
|---|---|---|
| Patch age | 95 days vs Xiaomi quarterly cadence (next quarterly due ~September 2026) | ⚠️ R1 — run Settings → Updater now, enable auto-update |
| Update policy | Shipped Android 14; now on Android 16 = 2 majors in ~19 months (healthy cadence). Provisional policy: **3 OS upgrades + 4 years security** → support into ~2029. **Provisional** — verify against Xiaomi trust page / Updater | ℹ️ recorded |

## 4. App Inventory — ✅ / ℹ️

| Check | Result | Status |
|---|---|---|
| Total packages | 406 system + 127 third-party | ✅ lean count |
| Installer attribution (dumpsys, authoritative) | **109** Play Store · **10** Xiaomi GetApps (`com.xiaomi.mipicks`) · **1** sideloaded (`com.parallelc.micts` v2.4, installed 2025-09-09) · **1** Facebook App Manager auto-install (`com.facebook.katana` via `com.facebook.system`) · **6** no installer — all Xiaomi ROM built-ins (calculator, compass, screenrecorder, scanner, Mi Remote, WPS Office lite; firstInstall 2024-11-06 = ROM ship or epoch) | ⚠️ R4 (the 1 sideload) |
| Xiaomi ad/analytics stack | `com.miui.msa.global` + `com.miui.analytics` present — default on global ROM | ℹ️ R7 optional removal |
| Disabled packages | `com.google.android.devicelockcontroller`, `com.payjoy.access` (financing agent, disabled), `com.google.android.gms.supervision`, `com.android.virtualization.terminal` | ℹ️ noted, appears intentional |

## 5. Runtime Permissions — ⚠️

79 of 127 third-party apps hold ≥ 1 dangerous permission. Notable grant patterns:

| App | Grants | Assessment | Status |
|---|---|---|---|
| `com.xiaomi.wearable` | READ_CALL_LOG, READ_SMS, SEND_SMS, READ_PHONE_STATE, RECORD_AUDIO, **BACKGROUND location**, contacts, media | Broad but functional for call/SMS-on-watch **if** the wearable is still in use; revoke/uninstall if retired | ⚠️ R8 |
| `gogolook.callgogolook2` (Whoscall) | CALL_PHONE, READ_CALL_LOG, READ_SMS, RECEIVE_MMS/SMS, READ_CONTACTS, READ_PHONE_STATE | The app's core feature (caller ID) — acceptable by design | ℹ️ |
| `com.hlpth.majorcineplex` | **ACCESS_BACKGROUND_LOCATION** + fine | Cinema app has no background-location use case | ⚠️ R5 → revoke to While-in-use |
| `com.miui.weather2` | **ACCESS_BACKGROUND_LOCATION** | Auto-refresh convenience; foreground-only is defensible | 🟡 R6 |
| `com.liuzh.deviceinfo` | READ_PHONE_STATE + fine location | Device-info utility — grant set broader than purpose | 🟡 R6 |
| `com.deepstash` | READ_CONTACTS | Reading app — contacts not obviously needed | 🟡 R6 |
| `photo.hd.video.beauty.camera` | fine location + camera + mic | Location grant questionable for a camera app | 🟡 R6 |
| `com.miui.notes` / `com.miui.mediaeditor` / `com.android.soundrecorder` | MANAGE_EXTERNAL_STORAGE | Xiaomi built-ins — broad but stock | ℹ️ |
| `com.scb.phone`, banking QR apps | fine location + CAMERA (+ some READ_CONTACTS) | Anti-fraud device-check / payee features — normal for TH banking | ℹ️ |
| `com.microsoft.teams`, `com.discord`, `jp.naver.line.android`, `org.telegram.messenger`, `com.instagram.android` | camera/mic/media (+ call-log for dialer features) | Comm apps — expected shape | ℹ️ |
| No user app | MANAGE_EXTERNAL_STORAGE, BODY_SENSORS, READ_CALL_LOG (outside Whoscall/wearable/Telegram) | — | ✅ no red-flag grants |

## 6. Battery & Thermal — ✅

| Check | Result | Status |
|---|---|---|
| Level / charging | 100 %, AC powered (Max charging current 1450 mA @ 5000 mV), Li-poly | ✅ |
| Battery temp | 35.5 °C while charging (sensors show 32.7–35.6 °C) | ✅ well under 45 °C threshold |
| Health / voltage | health=2 (Good), 4415 mV, charge counter 4654 mAh | ✅ |
| Skin temp | 38.6 °C max | ✅ |
| CPU / GPU | 50–58 °C during dump burst (SoC diode 68 °C instantaneous) — **no throttling** (`mStatus=0` all sensors) | ✅ |

## 7. Storage — ✅

| Check | Result | Status |
|---|---|---|
| /data | 124 G / 465 G used → **341 G free (73 %)** | ✅ far above the 10 % floor |
| Composition | Apps 28.4 GB · **App cache 28.6 GB** · Photos 8.8 GB · Videos 0.9 GB · Audio 0.1 GB | ℹ️ R9 cache optional cleanup |
| Observation | `diskstats` reports System-Free 0 K (system partition headroom) — normal for dynamic-partition devices post-OTA; not user-facing | ℹ️ |

## 8. Backup & Recovery — ✅ (coverage pending manual check)

| Check | Result | Status |
|---|---|---|
| Backup Manager | **Enabled** | ✅ |
| Transports | Active = `com.google.android.gms/.backup.BackupTransportService` (Google); also D2D + local available | ✅ |
| Google One coverage (photos/contacts/SMS, last successful run) | adb cannot see — manual check required | ⏳ manual |

## 9. Manual On-Phone Checks — ⏳ PENDING

To be verified by user per [[ADB-Mobile-Audit-Manual]] §8: screen lock + biometrics · Play Protect · Find Device (Mi + Google) · SIM PIN · Google backup coverage · Permission manager spot-check · Play auto-update · unknown VPN profiles.

| Check | Result | Status |
|---|---|---|
| Screen lock + biometrics | ⏳ | ⏳ |
| Play Protect | ⏳ | ⏳ |
| Find Device | ⏳ | ⏳ |
| SIM PIN | ⏳ | ⏳ |
| Google backup coverage | ⏳ | ⏳ |
| Play auto-update | ⏳ | ⏳ |
| Unknown VPN profiles | none visible via adb (no VPN packages) | ✅ adb-side |

## 10. Findings & Recommendations

| R# | Severity | Finding | Recommendation | Owner | Outcome |
|---|---|---|---|---|---|
| R1 | ⚠️ Med-High | Security patch 2026-06-01 is 95 days old; September quarterly due now | Settings → Updater → check & install; enable auto-update; confirm policy years on `trust.mi.com/misrc/updates/phone` | user (manual) | |
| R2 | ⚠️ Medium | USB debugging enabled + this PC holds an "always allow" grant | After audit closes: Developer options → USB debugging **OFF** (or Revoke USB debugging authorizations); verify with `adb devices` → empty/unauthorized | user (manual) | |
| R3 | ⚠️ Medium | Private DNS specifier set (AdGuard DoT) but mode=`opportunistic` → AdGuard filtering likely NOT enforced | Settings → Connection & sharing → Private DNS → select **Private DNS provider hostname** → `c9daf585.d.adguard-dns.com` | user (manual) | |
| R4 | ⚠️ Medium | Only sideloaded app: `com.parallelc.micts` v2.4 (2025-09-09), no dangerous perms granted | Confirm source/trust; uninstall if unused | user (manual) | |
| R5 | ⚠️ Medium | `com.hlpth.majorcineplex` holds ACCESS_BACKGROUND_LOCATION | Settings → Apps → Major Cineplex → Location → **While using the app** | user (manual) | |
| R6 | 🟡 Low | Broader-than-purpose grants: `com.liuzh.deviceinfo` (phone state+location), `com.deepstash` (contacts), `photo.hd.video.beauty.camera` (location), `com.miui.weather2` (background location) | Permission manager → revoke each non-essential grant | user (manual) | |
| R7 | 🟡 Low | Xiaomi ad/analytics stack (`com.miui.msa.global`, `com.miui.analytics`) present — global-ROM default | Optional disable via adb — **only on explicit approval**, separate remediation session | me (on approval) | |
| R8 | 🟡 Low | `com.xiaomi.wearable` broad grants (SMS stack + call log + background location) | If wearable retired → uninstall; else keep (functional for watch calls/SMS) | user (manual) | |
| R9 | ℹ️ Info | 28.6 GB app cache on 341 GB free | No action needed; optional cache cleanup | user | |
| R10 | ℹ️ Info | `com.payjoy.access` (device-financing agent) disabled | Confirm this is intentional; no action if so | user | |

## 11. Post-Audit Hardening — ⏳ pending

Per [[ADB-Mobile-Audit-Manual]] §7, executed by user after manual checks complete: USB debugging off / authorizations revoked → verified from PC (`adb devices` shows nothing). Developer-options policy (keep for quarterly audits vs close fully) recorded after decision.

## Evidence

Raw outputs captured to PC scratch (`%LOCALAPPDATA%\Temp\mobile-audit\`, transient): `props.txt`, `settings.txt`, `battery.txt`, `thermal.txt`, `diskstats.txt`, `packages3.txt` (127), `packages3_inst.txt`, `dumpsys_package.txt` (8.4 MB), `perm_analysis.json` (parsed grants). All values above are verbatim from those captures — none assumed.

## Related

[[Mobile-Device-Checklist]] · [[ADB-Mobile-Audit-Manual]] · [[Personal-Computer-Checklist]]
