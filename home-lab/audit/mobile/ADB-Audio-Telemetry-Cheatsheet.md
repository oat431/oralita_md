---
tags: [android, adb, audio, reference, audiophile, mobile]
---

# ADB Audio Telemetry — Cheat Sheet

> **Created:** 2026-09-04 · from the mobile-audit session (see [[mobile-audit-2026-09-04]])
> **Device:** Xiaomi Redmi Note 14 Pro+ 5G (`24115RA8EG`, `amethyst_global`) — Android 16, HyperOS 3.0.304, Snapdragon 7s Gen 3 (per spec)
> **For:** audiophile-profile session · **All commands read-only** · Outputs = Bluetooth + USB-C audio

## Prerequisites (user executes manually)

1. Phone → Developer options → USB debugging ON (may re-accept the RSA prompt if authorizations were revoked after the security audit — expected, one tap)
2. Plug into PC → verify: `"C:/Users/Admin/platform-tools/adb.exe" devices -l` → state `device`
3. **Start playback first** — codec/stream dumps are only meaningful while audio plays (or BT headphones connected / DAC plugged in)
4. Privacy boundary: capture config/telemetry only. No call logs, SMS, or personal content providers — out of scope.

## A. Bluetooth codec (headphones connected, playing)

```bash
ADB="C:/Users/Admin/platform-tools/adb.exe"; S="<serial or leave off for single device>"
"$ADB" shell dumpsys bluetooth_manager > bt.txt
grep -iE -A6 'a2dp|codec' bt.txt | head -60      # active codec, sample rate, bits per sample, LDAC quality
"$ADB" shell settings list global | grep -iE 'a2dp|ldac|aptx|codec'   # codec/quality setting keys as they exist on this build
```

Read from the dump: **active codec** (SBC/AAC/aptX*/LDAC/LC3), negotiated sample rate & bit depth, LDAC playback-quality setting. Note whether "Bluetooth audio codec" dev-option overrides are in play (user-facing toggle on some builds).

## B. Bit-perfect / resampling check (the interesting one)

```bash
"$ADB" shell dumpsys media.audio_flinger > flinger.txt
grep -iE -B2 -A12 'Output thread|HAL|sample rate|format|channel' flinger.txt | head -80
"$ADB" shell dumpsys media.audio_policy > policy.txt
```

Method: play a 44.1 kHz track, record the output thread's sample rate/format; repeat with 96 kHz hi-res track. If both show the same rate → Android is resampling (normal mixer behavior); if the rate follows the track → bit-perfect path (or app-level exclusive access). Record PCM format as 16/24/32-bit from the stream config.

## C. USB DAC path

```bash
"$ADB" shell dumpsys usb > usb.txt
"$ADB" shell dumpsys media.audio_flinger | grep -iE -A12 'usb|out' | head -60
```

Check the negotiated rate/bit depth on the USB output thread while playing hi-res content; repeat at 44.1/48/96 to map rate-switching behavior.

## D. Vendor audio stack & effects

```bash
"$ADB" shell getprop | grep -iE 'audio|dolby|dirac|aptx|ldac|hi.?res|pcm' 
"$ADB" shell pm list packages | grep -iE 'dolby|audiofx|dirac|sony|aptx'
"$ADB" shell dumpsys audio > audio.txt        # volumes, devices, ringer, sessions
```

Note: Dolby Atmos / MIUI sound-effects packages are visible here; their tuning files are **not** readable without root — expected limit, don't chase it.

## E. Glitch / drop-out investigation (if ever needed)

```bash
"$ADB" logcat -d | grep -iE 'audioflinger|a2dp|ldac|usb_audio|underrun|AudioTrack' | tail -80
```

## Known limits (no root — by design)

- Can't read vendor DSP tuning files, can't force/persist codec policy, can't change resampling behavior system-wide, can't uninstall preloads (disable only, and only on explicit approval). Root is out of scope for this device (bootloader stays locked — see [[mobile-audit-2026-09-04]]).

## Related

[[mobile-audit-2026-09-04]] · [[ADB-Mobile-Audit-Manual]] · [[Mobile-Device-Checklist]] · [[ADB-Audio-Audit-Findings-2026-09-04]]
