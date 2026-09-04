---
title: UAPP Settings Reference
created: 2026-09-04
updated: 2026-09-04
tags:
  - audio
  - android
  - uapp
---

# UAPP Settings Reference

## Clean USB DAC mode

`Redmi Note 14 Pro+ 5G → UAPP custom USB driver → BGVP MX1 → COZOY D1`

- `Use USB DAC`: On
- USB volume control: use the MX1 hardware volume; if UAPP offers `None`, it is a reasonable starting choice
- Bit-perfect: `When possible`; test `On` only when no DSP/EQ is needed and playback is stable
- Android/sample-rate setting: begin with `Device Native`; test `Variable` if the phone/DAC behaves better with it
- Resampler: Off for the baseline
- UAPP EQ/DSP: Off for the baseline

## EQ mode

UAPP EQ/DSP processing and bit-perfect playback are competing goals. To use ToneBoosters PEQ or another UAPP DSP, turn bit-perfect Off. To use bit-perfect playback, turn UAPP processing Off.

## Troubleshooting

- No DAC detection: unlock the phone, reconnect the cable, accept USB permission, and keep `Use USB DAC` enabled.
- Dropouts/clicks: increase the USB buffer; only then test `USB tweak 2`.
- If UAPP cannot play a format in bit-perfect mode, use `When possible` rather than forcing `Always`.
- If you use DSD files later, leave DSD mode at its default/compatible option unless the DAC specifically requires Native DSD or DoP. Do not change this setting for Tidal PCM playback.

## Listening/streaming notes

UAPP's own USB driver is the relevant feature for an external USB DAC; the phone's internal Hi-Res driver is a different path. UAPP supports streaming services including Tidal and can route audio directly to a USB DAC.

Verify the actual output shown in UAPP while a track plays: source format, sample rate, bit depth, and active USB device. Do not assume a 24-bit/192 kHz indicator automatically sounds better than a 16-bit/44.1 kHz lossless stream.

## Hardware

- Use the supplied short USB-C cable if it is stable.
- A USB-C cable must carry data; charge-only cables will fail.
- Keep the MX1 supported so the phone port does not experience sideways force.
- The MX1's low-gain position is appropriate for the sensitive COZOY D1.
- Do not use the 3.5 mm-to-4.4 mm adapter in this chain.
