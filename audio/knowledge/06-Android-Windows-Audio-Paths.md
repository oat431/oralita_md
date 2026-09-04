---
title: Android and Windows Audio Paths
created: 2026-09-04
tags:
  - audio
  - android
  - windows
  - uapp
  - fundamentals
---

# Android and Windows Audio Paths

## Why the path matters

The same DAC can sound different—or appear not to respond to an EQ—because different software paths are being used. A player may pass audio through the operating-system mixer, or it may open the USB device more directly.

## Shared/system path

```text
App → operating-system mixer → system effects → USB/device output
```

This is convenient and lets multiple apps share audio. It may also apply system volume, sample-rate conversion, vendor EQ, spatial effects, or other processing.

## Direct/exclusive path

```text
App → direct USB driver/device → DAC
```

A direct path gives the player more control over sample rate and processing. It can bypass system-wide EQ and phone effects. This is why an Android equalizer app may have no effect on UAPP's direct USB output.

## Android and UAPP

Android detects compatible USB digital-audio peripherals and routes audio according to audio-policy rules. Android 11 and later also allow manufacturers to automatically attach effects when a device is selected for playback. The actual path depends on the phone firmware, app, permissions, and selected output.

UAPP's custom USB driver is intended to communicate with supported USB DACs directly. For your MX1, treat UAPP as the owner of the USB route when its USB DAC mode is active.

## Windows shared and exclusive modes

- **Shared mode:** Windows Audio Engine mixes applications and may resample to the selected device format.
- **Exclusive/WASAPI mode:** a compatible player can take exclusive control of the endpoint, reducing interference from other apps and system processing.
- **Equalizer APO:** system-level processing applied to selected Windows endpoints; it is not an Android/UAPP solution.

## Bit-perfect versus DSP

| Goal | Appropriate path |
|---|---|
| Preserve samples unchanged | Direct/exclusive + bit-perfect, DSP off |
| Use EQ or crossfeed | Player DSP/PEQ, bit-perfect off |
| Use Windows-wide EQ | Equalizer APO + Peace on the correct endpoint |
| Use phone vendor effects | System path, only if the app/output actually goes through it |

Do not assume the label proves the route. Verify the selected device and use an obvious A/B test.

## Troubleshooting by symptom

| Symptom | First checks |
|---|---|
| EQ app does nothing | Check whether the player bypasses the system path |
| Sample rate is unexpected | Check player mode, source rate, and device negotiation |
| Dropouts | USB cable, phone power, UAPP buffer, device compatibility |
| Hiss | Low gain, volume control, DAC noise floor, IEM sensitivity |
| Dolby/Xiaomi toggle has no audible effect | Direct USB path may be bypassing system effects |

## Recommended UAPP baseline

```text
Use USB DAC: On
Bit-perfect: When possible
UAPP EQ/DSP: Off
Resampler: Off initially
Sample rate: Device Native/Automatic
MX1 gain: Low
```
