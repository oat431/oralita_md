---
title: Digital Audio and Hi-Res
created: 2026-09-04
tags:
  - audio
  - digital-audio
  - streaming
  - fundamentals
---

# Digital Audio and Hi-Res

## Sample rate

The sample rate is how many times per second an analog waveform is sampled. `44.1 kHz` stores up to roughly 22.05 kHz, and `48 kHz` stores up to roughly 24 kHz under the Nyquist model. Human hearing usually does not extend to 24 kHz, so a higher number is not automatically audible improvement.

For music, 44.1 kHz is normal; 48 kHz is common for video. Use the source's native rate when practical instead of forcing extreme rates such as 192/384/768 kHz.

## Bit depth

Bit depth describes the number of amplitude steps and the available theoretical dynamic range. 16-bit has approximately 96 dB theoretical dynamic range; 24-bit provides more recording/production headroom. During playback, 24-bit does not automatically make a master sound better than a good 16-bit master.

## Lossless and lossy

- **Lossless:** decoding reproduces the original digital samples, e.g. FLAC, ALAC, WAV.
- **Lossy:** removes information judged less important to reduce size, e.g. AAC, Opus, MP3.
- **Hi-Res:** commonly means greater than CD sample rate and/or bit depth, but the label says nothing about mastering quality.

A well-mastered 16/44.1 lossless file can sound better than a poorly mastered 24/192 file. Mastering and loudness often matter more than the container or sample-rate badge.

## DSD

DSD uses a different one-bit, very-high-rate encoding approach. It is not automatically more detailed or more analog-like. Many playback chains convert it to PCM for volume control or DSP.

## Bit-perfect

Bit-perfect means the player sends samples without changing them through its processing path. It can be useful for preserving the source exactly, but it is not a magical sound-quality mode. EQ, crossfeed, replay gain, and some volume operations require processing and therefore are not bit-perfect.

## TIDAL/UAPP baseline

For a clean comparison:

- choose the highest lossless tier available to your account;
- disable normalization when evaluating the original mastering;
- disable crossfade for album-transition testing;
- use normal stereo unless intentionally testing an immersive mix;
- let UAPP and the MX1 negotiate a sensible native/automatic rate.

The best format is the one that plays reliably without unnecessary conversion, dropouts, battery drain, or volume mistakes.
