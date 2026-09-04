---
title: Windows + COZOY D1 + BGVP MX1 Listening Setup
created: 2026-09-04
updated: 2026-09-04
tags:
  - audio
  - iem
  - windows
  - eq
---

# Windows + COZOY D1 + BGVP MX1 Listening Setup

## Current chain

`Windows laptop → USB BGVP MX1 → 4.4 mm output → COZOY D1`

The BGVP MX1 is detected by Windows as `USB Audio 2.0` / `Headphones (BGVP MX1)`.
The COZOY D1 is a roughly 33 Ω IEM with high sensitivity, so the MX1 has ample power; a desktop amplifier is not the logical next upgrade.

## Important 4.4 mm note

The 4.4 mm output on the MX1 is a true balanced output, but this does **not** mean every 4.4 mm cable or adapter creates a balanced circuit. Use the D1's 4.4 mm cable directly with the MX1. Do not connect a 3.5 mm single-ended source to a 4.4 mm adapter and call it balanced.

## Recommended signal path

1. Select `Headphones (BGVP MX1)` as the Windows output.
2. Keep `FxSound` bypassed for critical music listening unless intentionally comparing its effect. FxSound is installed, but its saved output target is the monitor (`1 - EK251Q P6`) and its saved preset is `Movies`, so it is not currently the clean path for the IEM.
3. Turn off Windows audio enhancements and spatial audio for a neutral baseline.
4. Use normal shared mode for general desktop use. For local files, use foobar2000 with official WASAPI output in exclusive mode if you want the player to take direct control of the DAC. Exclusive mode prevents other system audio from playing through that endpoint.
5. Leave sample-rate conversion alone unless it causes a real problem. 24-bit/48 kHz is a practical Windows default; do not chase 768 kHz as an audible upgrade.

## EQ starting point

The D1 is sensitive and does not need more gain. EQ is the upgrade that can change the sound most directly. Start with a small, reversible change rather than stacking FxSound, DTS, and another EQ.

- Use either the MX1's own 8-band PEQ (if configured through Walk Play) **or** Equalizer APO + Peace, not both at first.
- Use a preamp negative enough to avoid clipping after positive filters.
- Treat measurement-based EQ as a starting point: fit, insertion depth, tips, and personal preference can change the result.
- RAA publishes a Cozoy D1 measurement and a separate recommended-equalization page targeting Harman In-Ear 2019. The site currently rate-limits some graph requests, so use its displayed export rather than copying unverified numbers from a search snippet.

## Hardware verdict

No new DAC/amp is needed for this IEM chain. Spend first on:

- better-fitting eartips and a reliable seal;
- a comfortable, directly terminated 4.4 mm cable only if the current cable is inconvenient;
- EQ and listening comparisons;
- a different IEM only when the D1's tuning, not its amplification, is the limitation.

## Useful links

- [[02-Listening-Test-and-EQ-Workflow]]
- [[03-Desktop-Audio-Software-Options]]
