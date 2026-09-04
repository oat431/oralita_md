---
title: DAC Amplifier and Output Power
created: 2026-09-04
tags:
  - audio
  - dac
  - amplifier
  - fundamentals
---

# DAC, Amplifier, and Output Power

## DAC

A **DAC** (digital-to-analog converter) turns digital samples into an analog electrical waveform. The DAC chip name alone does not tell you the final sound quality; implementation, filtering, power supply, noise, distortion, and output stage matter.

## Amplifier

The headphone amplifier provides voltage and current to move the driver. A good amplifier should provide enough clean output, low noise, and low enough output impedance for the load.

More power is not automatically better. Once the amplifier is comfortably below its limits, extra power is unused headroom.

## Power and loudness

Power is commonly expressed in mW, voltage in Vrms, and loudness in dB SPL. Specifications must be compared at the same impedance and with the same sensitivity convention. `dB/V` and `dB/mW` are not interchangeable without conversion.

The RAA measurement for the COZOY D1 reports approximately 113.15 dB/mW sensitivity and 33.2 Ω average impedance. BGVP lists approximately 320 mW / 4 Vrms at 32 Ω for the MX1's 4.4 mm output. The conclusion is practical: the MX1 has ample headroom for the D1; do not use high gain to chase detail.

## Gain

Gain is how much the amplifier increases voltage. High gain does not create information. It makes the volume control reach loud levels sooner and can expose amplifier hiss or make accidental over-volume easier.

| Load situation | Sensible gain |
|---|---|
| Sensitive IEM, like D1 | Low gain |
| Average portable headphone | Low first; high only if needed |
| Difficult, insensitive headphone | High if low gain cannot reach the desired level cleanly |

## Output impedance

Output impedance is the resistance the source presents to the headphone. If an IEM's impedance changes significantly with frequency, a high source impedance can alter its frequency response. Low output impedance is normally the safe choice for multi-driver and low-impedance IEMs.

A common conservative design rule is source output impedance no more than about one-eighth of the headphone's minimum impedance. It is a rule of thumb, not a law; the actual impedance curve and audible result matter.

## Noise floor and hiss

A sensitive IEM can reveal low-level amplifier noise as hiss during silence. High gain often makes this more noticeable. If your D1 is quiet on the MX1, there is no reason to buy another amp for noise reasons.

## Apply this to your lab

```text
COZOY D1: efficient, around 33 Ω
BGVP MX1: powerful 4.4 mm dongle
Recommended: low gain, moderate volume, no extra amplifier
```

The next upgrade should be fit, EQ, or a different tuning—not a bigger amp.
