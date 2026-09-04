---
title: Listening Test and EQ Workflow
created: 2026-09-04
tags:
  - audio
  - eq
  - listening
---

# Listening Test and EQ Workflow

## A/B method

1. Set a comfortable volume with EQ off.
2. Change only one thing at a time.
3. Match loudness as closely as possible; louder almost always sounds "better" at first.
4. Use familiar tracks with vocals, bass, cymbals, and dense mixes.
5. Keep the setting that remains better after several short comparisons—not the one that merely sounds more exciting for 30 seconds.

## Safe EQ rules

- Use a negative preamp when adding positive gain.
- Prefer gentle cuts to large boosts.
- If sibilance or fatigue is the problem, try a narrow cut around the offending region rather than reducing all treble.
- If bass is thin, check seal and tips before boosting bass.
- If a preset sounds worse, disable it. There is no obligation to follow a target curve.

## Suggested first experiments for COZOY D1

These are listening experiments, not a claimed measurement correction:

- `Neutral baseline`: EQ off.
- `Less bright`: a gentle high-shelf cut, approximately -2 dB above 6–8 kHz.
- `More warmth`: a gentle low-shelf boost, approximately +1.5 dB below 150 Hz, with a negative preamp.
- `Relaxed`: combine both small changes.

Compare each against the baseline. Stop if the change makes vocals dull, bass muddy, or detail less clear.

## Install route on Windows

For system-wide EQ, install Equalizer APO first and then Peace as its user interface. During Equalizer APO configuration, select `Headphones (BGVP MX1)`. If playback is unaffected after installation, reopen the configurator and verify that the MX1 endpoint is checked; some Windows driver paths require reinstalling the APO for the endpoint.

For local-file playback, foobar2000 plus its official WASAPI output component is an alternative that can use exclusive mode. This is useful for a clean playback path, not because exclusive mode magically improves frequency response.
