---
title: Audio Signal Chain
created: 2026-09-04
tags:
  - audio
  - fundamentals
  - signal-chain
---

# Audio Signal Chain

## The simple model

```text
Music file/stream
  → player and decoder
  → DSP/EQ/volume processing
  → operating-system audio path
  → DAC
  → amplifier
  → cable/connector
  → IEM or headphone driver
  → ear + brain
```

Each stage has a different job. A later stage cannot repair every problem created by an earlier stage.

## Applied to your setup

```text
TIDAL inside UAPP
  → UAPP USB driver and optional DSP
  → USB-C digital connection
  → BGVP MX1 DAC
  → MX1 headphone amplifier
  → MX1 4.4 mm output
  → COZOY D1 dynamic driver
  → your ears
```

The Redmi is mainly the **source/controller** here. The MX1 performs the digital-to-analog conversion and amplification. The COZOY D1 is where the final acoustic tuning happens.

## Why this model matters

If the sound is too sharp, a larger amplifier usually does not solve it; the cause is more likely IEM tuning, fit, tips, or EQ. If there is hiss, investigate the source/amp noise floor and gain. If there are dropouts, investigate USB connection, power, buffer, and software.

## Three types of change

| Change | What it changes | Example |
|---|---|---|
| Tonal/DSP | Frequency balance or spatial presentation | EQ, Dolby Atmos, crossfeed |
| Electrical | Ability to drive the transducer cleanly | Output power, output impedance, noise |
| Acoustic/mechanical | Coupling between driver and ear | Eartips, seal, insertion depth |

For an efficient IEM such as the D1, tonal and acoustic changes are usually more relevant than adding amplifier power.

## Practical rule

Troubleshoot from left to right: source/content → software path → USB → DAC/amp → cable → fit/IEM. Change one variable at a time.
