---
title: ADB Audio Audit — Findings (2026-09-04)
created: 2026-09-04
updated: 2026-09-04
tags:
  - android
  - adb
  - audio
  - audit
  - audiophile
  - mobile
---

# ADB Audio Audit — Live Telemetry Findings

> **Session:** 2026-09-04 (evening) · audiophile-profile · read-only + wireless ADB bridge
> **Device:** Xiaomi Redmi Note 14 Pro+ 5G (`24115RA8EG`, `amethyst_global`) — Android 16, SDK 36
> **Audit method:** [[ADB-Audio-Telemetry-Cheatsheet]] — dumpsys + getprop + settings; **no root**

## ★ Key finding: the vendor DSP map (answers Dolby/Xiaomi Sound once and for all)

```
Device -> Effect map: {speaker=dolby, bluetooth_device=misound, usb_device=none}
```

Read live from `dumpsys audio`. This is the phone's actual effect-attachment table:

| Output path | Attached vendor effect | Meaning for listening |
|---|---|---|
| Speaker | `dolby` | Built-in speaker = Dolby-processed (Dolby codec HAL `dolbycodec2` running) |
| Bluetooth | `misound` (Xiaomi Sound / MiSound app `com.miui.misound`) | **BT buds/headphones pass through Xiaomi Sound effects** |
| **USB device** | **`none`** | **The BGVP MX1 USB path has ZERO vendor DSP attached** |

### Consequence
- **MX1 / COZOY D1 / XM5-wired over USB → clean, uncolored by HyperOS.** Confirmed from the device itself, not just theory.
- **Xiaomi Buds 5 Pro / XM5 over Bluetooth → Xiaomi Sound (`misound`) is the effect in play.** This is the toggle that actually matters when testing BT sound; Dolby is not attached to BT.
- So: UAPP + MX1 = true neutral baseline. BT = vendor tuning already baked in unless Xiaomi Sound is off.

## Codec capability: aptX Lossless is disabled platform-wide

```
SUPPORT_APTX_LOSSLESS=false        (global setting)
```

- Buds 5 Pro are aptX Lossless-capable hardware, but **this build reports the capability OFF**.
- Expected BT negotiation: **aptX Adaptive / AAC** (or SBC fallback) — *not* aptX Lossless.
- Optional (needs discussion + user approval, reversible): try `adb shell settings put global SUPPORT_APTX_LOSSLESS true`, then re-check negotiation. Not done yet.

## Audio hardware/software stack observed

| Item | Finding |
|---|---|
| MMAP audio policy | `aaudio.mmap_policy=2`, `aaudio.mmap_exclusive_policy=2` → direct/exclusive audio enabled at platform level |
| Direct PCM profile | supports 8–192 kHz PCM-16 / 8_24, up to 352.8/384 kHz at 24-bit — hi-res capable output threads exist |
| Mixer baseline | all active mixer output threads = **48 kHz** (shared Android path resamples to 48k) |
| Spatializer | status close; effect map above; `DAP_offload` effect Enabled+Active; MiSound Disabled+Active (registered, not boosting) |
| Dolby HAL | `dolbycodec2`, `vendor-dolby-media-c2-hal-1-0` running (video/Atmos path) |
| LHDC | `miui_bluetooth_lhdc_whitelist_cache=14:6c:27:05:37:04;` → OpenWear Stereo whitelisted for LHDC |
| Per-device codec stores | `STORE_DEVICE_CODEC` has entries (e.g. `14:6C:27:05:37:04:19`, `B0:A3:F2:FA:50:47:7`) — per-device stored codec prefs exist; live mapping needs capture while connected |
| Audio packages | UAPP `com.extreamsd.usbaudioplayerpro`, TIDAL `com.aspiro.tidal`, Sony Sound Connect `com.sony.songpal.mdr` installed |
| HyperOS background audio | "AudioHardening" log shows UAPP background playback would be muted (full/partial) → lock UAPP in recents + allow unrestricted battery |

## Bluetooth state at audit time

- Adapter ON (`State: ON`), A2DP offload enabled.
- Bonded devices include: **WH-1000XM5**, **Xiaomi Buds 5 Pro**, Xiaomi OpenWear Stereo (battery 94/84/79), Watch S4, Smart Band 9 Pro, JQVITEK swimfree buds.
- At capture time no A2DP stream was active (all state machines Disconnected, `mActiveDevice: null`) — codec capture needs a live connection.

## USB state at audit time

- Phone was in **MTP mode, screen locked, no USB-audio device attached** (ADB cable occupied the port).
- → Wired ADB blocks the MX1 test. Solution applied below.

## Wireless ADB bridge (enabled this session)

```text
Phone IP : 192.168.1.129
Port     : 5555
Status   : TCP/IP mode ON — USB port now free for the MX1

Connect from PC:
adb connect 192.168.1.129:5555
adb devices -l          # expect c0c80c60 (USB) + 192.168.1.129:5555 (wireless)

Re-enable after phone reboot (USB required once):
adb tcpip 5555
```

Raw dumps from this session (PC): `C:\Users\Admin\AppData\Local\Temp\phone-audio\`
→ `audio.txt` · `bt.txt` · `usb.txt` · `policy.txt` · `flinger.txt`

## Pending live tests (to finish when back)

### Test 1 — USB DAC bit-perfect path (MX1)
1. Unplug phone from PC (wireless ADB keeps working).
2. Plug **BGVP MX1** into USB-C.
3. Open **UAPP**, play a TIDAL track (44.1 kHz is fine; a 96 kHz track later to compare).
4. Re-capture: `dumpsys audio` (usb output thread rate), `dumpsys media.audio_flinger`, and if readable `/proc/asound/...` hw_params.
5. Compare reported rate vs track rate → prove bit-perfect/no-resample on USB path.

### Test 2 — Bluetooth codec negotiation
1. Connect **Xiaomi Buds 5 Pro** (or WH-1000XM5).
2. Play music (any app).
3. Capture `dumpsys bluetooth_manager` → read actual negotiated codec (SBC/AAC/aptX Adaptive/LDAC/LHDC) + rate.
4. Check `STORE_DEVICE_CODEC` value → confirm which codec the Buds/XM5 use per-device.
5. Re-run after `SUPPORT_APTX_LOSSLESS` discussion if user wants the experiment.

### Test 3 — (optional) Xiaomi Sound on/off A/B over BT
- With Buds playing, toggle `com.miui.misound` effect in settings / Spatializer state, re-read effect map to show `misound` attach/detach, and level-match listen.

## Notes / caveats
- HyperOS masks BT MACs in dumps (`XX:XX:XX:XX:xx:xx`); name-matching used the Fast Pair metadata instead.
- No root → vendor DSP tuning files not readable; per policy, root stays out of scope.
- `charging_sounds_enabled=0`, `sync_parent_sounds=1` observed (not audio-path relevant).
- Every command used was read-only except `adb tcpip 5555` (wireless bridge — reversible via reboot or `adb usb`).

## Related
[[ADB-Audio-Telemetry-Cheatsheet]] · [[mobile-audit-2026-09-04]] · [[../audio/setup/04-Redmi-UAPP-MX1-Setup]] · [[../audio/setup/06-HyperOS-Audio-Effects]] · [[../audio/setup/09-Xiaomi-Buds-5-Pro-Setup]]
