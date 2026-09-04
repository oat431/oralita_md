---
title: Frequency Response and EQ
created: 2026-09-04
updated: 2026-09-04
tags:
  - audio
  - eq
  - frequency-response
  - fundamentals
---

# Frequency Response and EQ

## Frequency response

Frequency response (FR) shows how loud different frequencies are relative to one another. It mostly describes **tonal balance**: bass, mids, treble, warmth, brightness, and perceived clarity.

FR does not directly measure soundstage, detail, musicality, or build quality. A graph also cannot perfectly predict your result because ear shape, insertion depth, eartips, and the measurement rig matter.

## EQ

An equalizer changes the level of selected frequency regions. It can correct a broad tonal imbalance or create a personal sound. EQ cannot fix a broken driver, poor seal, distortion, or a badly fitting shell.

### Common filter types

| Filter | Use |
|---|---|
| Peak/peaking | Cut or boost around a center frequency |
| Low shelf | Change bass below a transition frequency |
| High shelf | Change treble above a transition frequency |
| Low-pass/high-pass | Remove frequencies above/below a cutoff; use carefully |

### EQ vocabulary

- **Frequency:** where the filter is centered, measured in Hz.
- **Gain:** how much to cut or boost, measured in dB.
- **Q:** filter width. Higher Q = narrower; lower Q = wider.
- **Preamp:** overall level reduction before EQ, used to prevent digital clipping.
- **Clipping:** the waveform runs out of headroom and distorts.

## Safe workflow

1. Start with EQ off.
2. Identify one problem: too bright, too thin, too warm, too recessed.
3. Make a small change, usually 1–3 dB.
4. Reduce preamp when any filter boosts a region.
5. Match volume before comparing.
6. Test several familiar tracks.
7. Keep the change only if it remains better after the novelty disappears.

## Target curves

A target curve is a preferred reference shape, not an objective law. Harman In-Ear is a useful starting point, but many listeners prefer less bass, more treble, or another target. Measurement services may use different couplers and compensation standards; do not copy settings across rigs without checking the measurement source.

## D1 experiments

These are preference experiments, not a certified correction for every D1 unit:

| Goal | Starting experiment |
|---|---|
| Less treble fatigue | High-shelf cut around 6–8 kHz, about -1.5 to -2 dB |
| Slightly more warmth | Low-shelf boost below about 150 Hz, about +1 to +1.5 dB |
| Preserve headroom | Negative preamp at least as large as the biggest positive boost |

Check the seal before bass EQ. If the IEM is leaking, no reasonable bass filter can fully replace a proper fit.

## EQ tools in your setup

- Windows: Equalizer APO + Peace, applied to `Headphones (BGVP MX1)`.
- Android/UAPP: UAPP ToneBoosters PEQ, with bit-perfect Off while EQ is active.
- MX1: its built-in PEQ, if configured through the supported Walk Play app.

Use one EQ location at a time so the final result remains understandable.
