---
title: Sony IER-EX15C Setup
created: 2026-11-17
updated: 2026-11-17
tags:
  - audio
  - sony
  - iem
  - usb-c
---

# Sony IER-EX15C Setup

## Quick verdict

The IER-EX15C is a self-contained USB-C earphone: its DAC and amplifier live inside the USB-C plug. It cannot use the BGVP MX1 or any analog output — there is no 3.5 mm plug anywhere in this chain. That is a feature, not a limitation: it is the grab-and-go, battery-free, mic-equipped daily driver your collection was missing.

```text
Redmi Note 14 Pro+ 5G / Windows PC / any USB-C device
  → USB-C digital audio
  → IER-EX15C inline DAC/amplifier (USB bus power, 5 V 25 mA)
  → 5 mm dynamic drivers
```

Role in the collection:

| Situation | Use |
|---|---|
| Noisy commute (need ANC) | [[07-Sony-WH1000XM5-Setup\|Sony WH-1000XM5]] or [[09-Xiaomi-Buds-5-Pro-Setup\|Xiaomi Buds 5 Pro]] |
| Quiet commute / calls / all-day wear, zero battery anxiety | Sony IER-EX15C (this note) |
| Desk critical listening | BGVP MX1 → COZOY D1 ([[01-Windows-IEM-Listening-Setup]]) |
| Portable critical listening | Redmi + UAPP + MX1 + COZOY D1 ([[04-Redmi-UAPP-MX1-Setup]]) |

## Published specifications

| Spec | Value | Source |
|---|---|---|
| Type | Closed, dynamic | Sony official |
| Driver | 5 mm | Sony official (some resellers list 9 mm — wrong) |
| Frequency response | 8 Hz – 22,000 Hz | Retailer-published |
| Impedance | 16 Ω (at 1 kHz) | Retailer-published |
| Sensitivity | 100 dB/mW | Retailer-published |
| Power handling | 62.5 mW (IEC) | Sony official |
| Power source | USB bus power (5 V, 25 mA) | Sony official |
| Cable | 1.2 m, USB-C plug, inline remote + mic, **non-replaceable** | Sony official |
| Mass | ~3 g per side (without cable) | Sony official |

Impedance/sensitivity matching is irrelevant here: the earphone brings its own amplifier and needs no external power. 16 Ω + 100 dB/mW only confirms it is easy to drive from the internal DAC.

## Step 1: Plug in and grant permissions

1. **Android (Redmi):** plug in, unlock the phone, accept the USB device permission dialog. It is remembered afterwards.
2. **Windows / macOS / iOS:** class-compliant USB audio — no drivers, no setup. Select it as the output device.
3. Test the inline remote: volume rocker is tactile; the playback button is stiff (known trait). The mic sits on the **left** side — also the fastest way to tell L from R (the L/R markings are tiny).

## Step 2: Chain and software

- **Redmi + UAPP:** the EX15C's internal DAC appears as a USB audio device exactly like the MX1 does. Same bit-perfect flow applies ([[05-UAPP-Settings-Reference]]).
- **HyperOS effects:** per [[home-lab/audit/mobile/ADB-Audio-Audit-Findings-2026-09-04|ADB audit]], the device→effect map is `speaker=dolby, bluetooth=misound, usb=none`. The USB path gets **no** vendor DSP, so audio reaches the EX15C clean — nothing to disable.
- **Windows:** shows as "USB Audio Device". Equalizer APO / Peace can EQ it ([[03-Desktop-Audio-Software-Options]]). Note FxSound 1.1.16.0 currently targets the EK251Q P6 monitor (Movies preset) — verify routing if output behaves oddly.

## Step 3: Fit, tips, and microphonics

- Passive isolation is weak (a known trait of this model — seals poorly against loud environments). Eartip rolling is the single biggest improvement lever ([[09-Eartips-Fit-and-Isolation]]). Verify nozzle fit with tips you already own before buying new ones.
- Cable microphonics is the main complaint in reviews: shirt-rub and wind are audible. Fix with a shirt clip and under-the-clothes routing. No ear hooks, and the cable is not replaceable (unless you solder) — treat it gently.

## Step 4: Sound and EQ

Out of the box character (SoundGuys lab + reviewer notes):

- Good tonal balance for the price; clean vocals (MDAQS 4.1/5 — Timbre 4.7, strong).
- Slight **underemphasis in parts of the treble** — can feel soft/less "sparkly".
- Bass is present and spacious but the attack is a bit soft — not a basshead tuning.
- Distortion score low (2.2 sub-score) at high output — don't crank it.

Suggested starting EQ (applied at the **source** — the internal DAC is the last stage):

```text
Baseline: flat for a few days first
If treble feels dull:  +1.5–2 dB high shelf from ~4 kHz
If bass wants more impact:  +1–2 dB low shelf at ~105 Hz
Avoid large boosts — small driver, distortion rises fast at high SPL
```

Check Wavelet/AutoEQ for an IER-EX15C preset first ([[04-Frequency-Response-and-EQ]]); if none exists, the manual shelves above are safe. Use only one EQ layer at a time.

## What NOT to buy

- **No dongle DAC** — the MX1 physically cannot connect (USB-C plug, not 3.5 mm). The internal DAC *is* the source.
- **No cable upgrades** — cable is permanently attached.
- **No balanced anything** — the entire circuit is single-ended inside one plug ([[08-4.4mm-Balanced-Audio]]).
- **No burn-in rituals** — plug in and listen.

## Troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| No sound on Android | USB permission not granted — unplug, replug, accept dialog |
| No sound in UAPP | USB audio output not selected in UAPP settings |
| One side quieter | Earwax or tip seating — 5 mm nozzles clog easily; clean and reseat |
| Call partner hears scratching | Cable microphonics — clip the cable to clothing |
| Sounds "dull" | Its slightly recessed treble + weak seal — try tips first, EQ second |

## Sources

- Sony Help Guide — Specifications (official)
- SoundGuys review, Mar 2026 — rating 7.4/10, comfort 8.5, value 8.0
- Thai market (Nov 2026): street price ≈ 488 THB via SoundProof, SS Iner, Progadget, Shopee, Lazada, NocNoc; PowerBuy carries official stock (check warranty: official vs grey import)

## Related notes

- [[09-Eartips-Fit-and-Isolation]] — seal and tip rolling
- [[04-Frequency-Response-and-EQ]] — how to EQ safely
- [[08-MX1-Output-Compatibility]] — why the MX1 has no place in this chain
- [[05-UAPP-Settings-Reference]] — bit-perfect USB playback on the Redmi
- [[03-Desktop-Audio-Software-Options]] — Windows EQ options
- [[12-Audio-Decision-Matrix]] — where this purchase sits on value
