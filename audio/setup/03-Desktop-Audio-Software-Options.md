---
title: Desktop Audio Software Options
created: 2026-09-04
tags:
  - audio
  - windows
  - software
---

# Desktop Audio Software Options

## Recommendation order

### 1. Equalizer APO + Peace

Best starting point for Windows-wide parametric EQ. Equalizer APO provides the audio processing layer; Peace provides a practical interface, presets, and filters. Select the BGVP MX1 endpoint during setup.

Official references:

- https://sourceforge.net/projects/equalizerapo/
- https://sourceforge.net/projects/peace-equalizer-apo-extension/

### 2. foobar2000 + WASAPI output

A good local-library player. The official WASAPI component offers exclusive-mode output and bit-exact output, while muting other audio on that endpoint during playback. Use this for a clean local-file path; it is not a replacement for EQ.

- https://www.foobar2000.org/
- https://www.foobar2000.org/components/view/foo_out_wasapi

### 3. FxSound

Already installed on the laptop (`1.1.16.0`). It can be useful for a quick, fun effect, but do not stack its Movies/effects processing on top of another EQ when evaluating the D1. The current saved configuration targets the monitor endpoint rather than BGVP MX1.

### 4. AutoEq

AutoEq generates equalizer settings from headphone measurements; it is not itself the live Windows audio processor. It is useful when a supported model has a trustworthy measurement, but the COZOY D1 does not appear to have a ready-made standard AutoEq preset in the search results checked on 2026-09-04.

- https://autoeq.app/

## Avoid for this goal

- exotic USB cables, audiophile fuses, and cable burn-in;
- buying another DAC/amp before checking fit and EQ;
- enabling several sound enhancers at the same time;
- treating a 4.4 mm adapter as a balanced circuit.
