---
tags: [android, xiaomi, hyperos, rom, migration, redmi-note-14-pro]
---

# Redmi Note 14 Pro+ 5G — Migration Note: Global DC → Global XM ROM

> **Created:** 2026-09-04
> **Decision at time of writing:** 🟢 **STAY on Global DC** (deliberate choice — see Why below). This note exists so the migration path is documented *if* that decision ever changes (e.g. DC patches lag main Global by months — then it becomes a security decision, not a preference).
> **Device context:** [[mobile-audit-2026-09-04]] · [[ADB-Mobile-Audit-Manual]]

## 1. Background — what "DC" actually is

The phone shipped with build `OS3.0.304.0.WOPMIDC`. Decoded:

| Fragment | Meaning |
|---|---|
| `OS3.0.304.0` | HyperOS 3.0, build 304 (June 2026 patch level, same as main Global's 304) |
| `WOPM` | Device/board code for amethyst (Redmi Note 14 Pro+ 5G global hardware) |
| `DC` | **Region branch "Global DC"** — an official Xiaomi distribution variant |
| (comparison) | `XM` = main "Global" branch, `ID` = Indonesia, `RU` = Russia, etc. |

**Verified facts (2026-09-04):** Xiaomi's ROM database (hyperosfirmware.com/model/amethyst, which indexes official Xiaomi CDN packages) lists `OS3.0.304.0.WOPMIDC` as region **"Global DC"** — an officially shipped branch, alongside `WOPMIXM` "Global". The phone's own trust chain proves authenticity regardless of label: Verified Boot **green**, bootloader **locked**, `release-keys` (audit evidence). "DC" is *not* custom/repacked/modified firmware — it is stock, just a different regional distribution branch with its own (slower) OTA cadence.

## 2. State snapshot (recorded 2026-09-04, before any migration)

| Field | Value |
|---|---|
| Model / device | `24115RA8EG` / `amethyst_global` |
| Current build | `OS3.0.304.0.WOPMIDC` (built 2026-06-24) |
| Security patch | 2026-06-01 |
| Bootloader | **locked** (re-locking = default state; migration = unlock → flash → re-lock) |
| Target build if migrated | `OS3.0.306.0.WOPMIXM` (main Global, 2 build-points ahead; fastboot package confirmed available) |

## 3. Why staying on DC (the decision)

- DC is official, Xiaomi-signed, OTA-supported — switching buys **slightly earlier OTAs**, nothing else visible day-to-day
- The switch **costs**: Mi-unlock waiting period, full data wipe (twice: unlock wipes, flash wipes), re-setup of the entire phone, re-audit
- Warranty/service nuance: TH service centers may treat region-mismatched units differently even when fully owned
- Trigger to revisit: DC patch level visibly trailing main Global by ~2+ quarters

## 4. Migration runbook (only if decision changes)

**Everything in this section is user-executed manually. No step is automated from the PC — bootloader work is explicitly out of the assistant's high-risk boundary (same class as SSH keys / firewall rules).**

### Phase 0 — prerequisites (all mandatory)

| # | Step | Notes |
|---|---|---|
| 0.1 | **Full backup** — Google One, Mi Cloud, photos/videos off-device, 2FA authenticator apps exported | Unlock **wipes the phone**. There is no graceful path. |
| 0.2 | Know the **Mi account password** | Anti-theft lock bites at post-flash setup if forgotten |
| 0.3 | SIM PIN + screen lock credentials known | Needed after wipe |
| 0.4 | PC: platform-tools installed (`C:\Users\Admin\platform-tools\`), good USB data cable, phone ≥ 60 % charge | Same tooling as the audit |
| 0.5 | Download **fastboot ROM** `amethyst` Global `OS3.0.306.0.WOPMIXM` (or newest XM available) | Index: <https://hyperosfirmware.com/model/amethyst> → Fastboot ROM → the `OS3.0.306.0.WOPMIXM` package (official Xiaomi CDN). ~4–6 GB tgz. Verify size/checksum before flashing. |
| 0.6 | **Mi Flash tool** (official Xiaomi flash utility) | Obtain from Xiaomi official channels (mi.com / Xiaomi Community); avoid third-party tool mirrors |

### Phase 1 — bootloader unlock (user executes)

| # | Step | Notes |
|---|---|---|
| 1.1 | Phone: Mi account signed in + SIM inserted | HyperOS gate — required |
| 1.2 | Developer options → **Mi Unlock status** → bind account | Follow in-app permission steps |
| 1.3 | PC: run **Mi Unlock Tool**, sign in same account, request unlock | HyperOS era: application + **waiting period (days)** applies; account quota ≈ 4 devices/year |
| 1.4 | After wait: unlock in tool → **phone wipes** | Bootloader now unlocked; AVB state turns orange — expected, temporary |
| 1.5 | Restore nothing yet; re-enable USB debugging, replug | Prepare for flash |

### Phase 2 — flash XM Global fastboot ROM (user executes)

| # | Step | Notes |
|---|---|---|
| 2.1 | Bootloader → fastboot mode | `adb reboot bootloader` (from PC, phone connected) or Power+Vol− |
| 2.2 | Extract ROM tgz; Mi Flash → select folder → **"clean all"** (NOT "clean all and lock", NOT "save user data") | Cross-region flash; "save user data" is the classic brick-maker on cross-branch flashes |
| 2.3 | Flash, wait for success, phone reboots to fresh XM Global setup | Do **not** interrupt USB/power during flash — interrupted fastboot flash is the #1 brick cause |
| 2.4 | First boot: sign in Mi account, SIM, basic setup only — **do not restore data yet** | Verify the ROM is good before trusting it with data |

### Phase 3 — verify, then re-lock (user executes, assistant verifies via adb)

| # | Step | Notes |
|---|---|---|
| 3.1 | Verify via adb (read-only): `ro.build.fingerprint` ends `WOPMIXM`, patch level current, `ro.boot.verifiedbootstate=orange`, `flash.locked=0` | Expected intermediate state |
| 3.2 | Confirm OTAs arrive normally (Updater shows XM channel) | Confirms region switch took |
| 3.3 | **Re-lock bootloader**: fastboot mode → `fastboot flashing lock` (or Mi Flash "clean all and lock" on a *re-flash*, never on cross-region first flash) | Only after days of stable XM usage; re-lock returns AVB to green |
| 3.4 | Full re-audit (adb command map in [[ADB-Mobile-Audit-Manual]] §5): expect green/locked, `WOPMIXM` build, fresh patch | Audit note documents the new baseline |

### Rollback path (if XM misbehaves)

Same procedure in reverse: fastboot-flash the **DC** package (`OS3.0.304.0.WOPMIDC` listed in the same ROM database) while bootloader is still unlocked → re-lock. Do **not** flash a build older than the current security patch level (rollback protection on vbmeta can refuse downgrades — check patch dates before choosing a package).

## 5. Risks & gotchas (honest list)

| Risk | Reality |
|---|---|
| Hard brick | Rare on this device with correct package + "clean all", but real — interrupted flash or wrong device package is the usual cause |
| Waiting period | Mi Unlock wait is Xiaomi-controlled and non-negotiable; plan around days, not minutes |
| Double wipe | Unlock wipes AND flash wipes — budget setup time twice |
| Anti-rollback | Never downgrade security-patch level across branches |
| Warranty/service | Region-mismatched unit may complicate TH service-center handling even when fully owned |
| Account lockout | Forgotten Mi account password = recovery hell after wipe |

## Related

[[mobile-audit-2026-09-04]] · [[ADB-Mobile-Audit-Manual]] · [[Mobile-Device-Checklist]]
