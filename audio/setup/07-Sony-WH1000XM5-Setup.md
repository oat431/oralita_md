---
title: Sony WH-1000XM5 Setup
created: 2026-09-04
updated: 2026-09-04
tags:
  - audio
  - sony
  - wh-1000xm5
  - bluetooth
  - wired
---

# Sony WH-1000XM5 Setup

## Important correction about the wired cable

Please check the exact cable you are using. The safest topology is **MX1 3.5 mm single-ended output → Sony-supplied 3.5 mm stereo cable → XM5**. The XM5 has a single 3.5 mm input; it is not a balanced headphone input. A generic passive 3.5 mm-to-4.4 mm adapter can connect the MX1's balanced amplifier to a single-ended load incorrectly. Do not use the same adapter you use for the COZOY D1 on the MX1's 4.4 mm output unless its manufacturer explicitly documents safe use from that specific balanced output to a 3.5 mm single-ended headphone input. A cable that merely fits is not proof of safe wiring.

## Your two listening paths

### Wired

Safest default:

```text
Phone or Windows
  → BGVP MX1 USB DAC/amp
  → MX1 3.5 mm single-ended output
  → Sony-supplied 3.5 mm stereo cable
  → Sony WH-1000XM5 3.5 mm input
```

For this headphone, do not pursue a 4.4 mm adapter. Use the MX1's 3.5 mm output. Specialized balanced-to-single-ended conversion products exist, but they are not a normal passive adapter category, provide no useful benefit here, and must be explicitly designed for the source. Do not use a generic adapter just because it fits.

The XM5 has a 3.5 mm stereo input. Its single 3.5 mm input does **not** become a true balanced headphone input just because the other end is 4.4 mm. In this chain, treat the connection as single-ended at the headphone. The 3.5 mm MX1 output is the preferred default for the XM5 because it is already sufficient and avoids the balanced-to-single-ended adapter risk.

### Wireless

```text
Phone or Windows
  → Bluetooth codec (LDAC/AAC/SBC)
  → XM5 internal DAC/DSP/amplifier
  → XM5 drivers
```

In wireless mode, the Sony's internal electronics drive the drivers. The MX1 is not in the signal path. The Bluetooth codec and Sony's stored/app settings matter more than the phone's USB-DAC settings.

## Recommended wired profile: clean and predictable

| Setting | Recommendation |
|---|---|
| Cable | Sony-supplied 3.5 mm cable or compatible stereo cable; fully click it into the XM5 |
| MX1 output | 3.5 mm single-ended; enough for the XM5 |
| MX1 gain | Low |
| Start volume | Minimum, then increase slowly |
| XM5 power | Off for ordinary passive wired listening; On when ANC/Ambient or Sony processing is needed |
| Windows EQ | Equalizer APO + Peace on the active MX1 endpoint, if desired |
| UAPP EQ | Use only when UAPP PEQ is the chosen DSP layer |
| Dolby/Xiaomi effects | Off for a neutral USB baseline |

Sony says the XM5 can play music with the supplied cable while powered off. Power the headset on when you want noise canceling/Ambient Sound or other powered functions. Sony specifically recommends using the supplied cable and inserting it until it clicks.

### Important wired limitation

The XM5's EQ/DSEE/Bluetooth codec settings are not the same as wireless playback when the headphone is being used passively through the analog input. Do not assume that a Sony app EQ preset or LDAC setting is active in passive wired mode. If you want predictable EQ, apply it upstream in Windows or UAPP.

### Is MX1 wired better?

It can provide a clean analog source and bypass Bluetooth compression, but the XM5 remains a powered ANC headphone with its own acoustic tuning. The MX1's additional 4.4 mm power does not automatically make the XM5 more detailed. The headphone's 3.5 mm input and internal design are the limiting interface; there is no balanced headphone path.

### Powered ON versus OFF while wired — what actually changes

| Aspect | Cable + power OFF | Cable + power ON |
|---|---|---|
| Signal path | MX1 amp drives the driver directly (passive; one amp) | Two amps in series: MX1 amp feeds the XM5's internal amp/DSP, which is the final stage driving the driver |
| ANC / Ambient | Not available | Fully available |
| Reported impedance | ~16 Ω at 1 kHz (retailer spec, unverified) | ~48 Ω at 1 kHz (retailer spec, unverified) |
| Tuning | Reviewers commonly describe passive wired as flatter/more mid-centric than the wireless sound | Closer to the headphone's designed wireless tuning |
| Sony app EQ / DSEE | Inactive | Reported to be inactive or limited in wired mode — verify per firmware: what works is ANC/Ambient; do not assume EQ applies |
| Battery | No drain | Drains (Sony rates roughly 36–40 h wired powered depending on codec/NC settings) |

Recommended test: play the same track through the MX1, toggle the XM5 power with volume held constant, and compare. Keep whichever you prefer; both are electrically safe since the source is the same MX1 3.5 mm output either way.

## Recommended wireless profile: Redmi + XM5

1. Install/update Sony | Sound Connect.
2. Pair the XM5 with the Redmi directly.
3. In Sound Connect, select **Priority on sound quality**.
4. Confirm that the active codec is **LDAC** if the Redmi firmware, Bluetooth connection, and multipoint state allow it.
5. If LDAC causes dropouts, switch back to stable connection quality or use AAC/SBC reliably.
6. Turn off multipoint while evaluating maximum wireless quality; two-device operation can impose compatibility/codec trade-offs.
7. Disable Speak-to-Chat unless you use it.
8. Disable Adaptive Sound Control if you want a fixed, repeatable ANC setting.
9. Set ANC/Ambient manually for the environment.
10. Use the Sony EQ only in wireless mode, and save one clear preset rather than stacking another EQ in the phone/player.

Sony documents SBC, AAC, and LDAC support for the XM5. Sony's help guide says **Priority on sound quality** is the correct mode when sound quality is the priority, while stable connection is preferable if interruptions occur. LDAC is lossy even though it can carry more data than conventional Bluetooth codecs; it is not identical to a wired bit-perfect connection.

## Wireless Sound Connect starting point

For a neutral starting point:

```text
Equalizer: Off or Flat
DSEE Extreme: Off initially
Adaptive Sound Control: Off
Speak-to-Chat: Off
Multipoint: Off while testing
Sound quality mode: Priority on sound quality
ANC: On when commuting; Ambient only when you need awareness
360 Reality Audio: Off unless deliberately testing supported content
```

DSEE Extreme is a preference feature, not a fidelity requirement. Sony notes that DSEE Extreme may be disabled during LDAC playback depending on the playback device. Therefore, do not chase both settings as if both must be active.

## Wireless EQ suggestion

First listen to Flat for several days. If you want a warmer, less sharp balance, try a small change in the Sony app, such as:

```text
Clear Bass: -1
400 Hz: 0
1 kHz: 0
2.5 kHz: +1
6.3 kHz: -1
16 kHz: -1
```

This is a listening experiment, not a measurement-derived correction. If you apply a positive band, reduce overall level if the app offers a preamp/volume control, and compare at matched loudness. Use only this Sony EQ while testing; do not simultaneously enable UAPP PEQ, phone EQ, and Windows EQ.

### TIDAL/UAPP routing

### UAPP to XM5 through MX1

```text
UAPP/TIDAL → UAPP USB driver → MX1 3.5 mm output → Sony cable → XM5
```

Use the same clean UAPP profile as the D1, but with the XM5 at low gain and very careful volume control. The XM5 is receiving a single-ended signal; the MX1's 4.4 mm label is not relevant when using the recommended 3.5 mm path.

### TIDAL directly to XM5 over Bluetooth

```text
TIDAL/native app or UAPP → Android Bluetooth stack → LDAC → XM5
```

The MX1 is not used. UAPP USB settings such as bit-perfect USB mode, USB buffer, and device-native USB sample rate do not configure this Bluetooth path. If UAPP's TIDAL integration does not expose the Android Bluetooth route correctly, use the native TIDAL app for the wireless XM5 path.

## Windows routing

### Wired XM5 through MX1

Select the physical endpoint:

```text
Headphones (BGVP MX1)
```

Use Equalizer APO + Peace only if you want Windows-wide EQ. Bypass FxSound/DTS/spatial effects for the neutral baseline. If a virtual endpoint such as FxSound Speakers is selected, the MX1 may not be receiving the path you intended.

### Wireless XM5

Select the XM5 Bluetooth **stereo/music** endpoint, not a hands-free/call endpoint. Hands-free mode uses a low-bandwidth microphone profile and is not appropriate for music quality. Disable unused microphone applications while listening if Windows switches profiles unexpectedly.

## Which mode should you use?

| Situation | Best starting path |
|---|---|
| Commute/travel | Wireless + ANC + LDAC if stable |
| Need maximum convenience | Wireless + AAC/LDAC |
| Airplane/known RF restrictions | Wired + XM5 powered on + ANC |
| Critical desk listening | Wired through MX1, EQ upstream if wanted |
| Phone battery conservation | Wired passive, XM5 powered off; no ANC |
| Testing source/DSP | Wired through MX1 with all effects off |

## Do not buy yet

- Do not buy a new amplifier for the XM5.
- Do not buy a “balanced” cable expecting the XM5 to become balanced.
- Do not use the same generic 3.5 mm-to-4.4 mm adapter used with the D1 on the MX1's balanced output. Use the MX1's 3.5 mm output instead; it is sufficient for the XM5. A direct-looking plug shape does not prove safe wiring.
- Do not force LDAC if the connection skips.
- Do not stack Sony EQ, UAPP PEQ, phone EQ, Windows EQ, FxSound, and Dolby effects.

## Sources

- Sony WH-1000XM5 supplied cable guide: https://helpguide.sony.net/mdr/wh1000xm5/v1/en/contents/TP1000534744.html
- Sony XM5 noise-canceling/cable guide: https://helpguide.sony.net/mdr/wh1000xm5/v1/en/contents/TP1000534715.html
- Sony XM5 specifications: https://helpguide.sony.net/mdr/wh1000xm5/v1/en/contents/TP1000541014.html
- Sony supported codecs: https://helpguide.sony.net/mdr/wh1000xm5/v1/en/contents/TP1000534600.html
- Sony sound-quality mode: https://helpguide.sony.net/mdr/wh1000xm5/v1/en/contents/TP1000534501.html
- Sony DSEE Extreme: https://helpguide.sony.net/mdr/wh1000xm5/v1/en/contents/TP1000539063.html
- Sony Sound Connect app: https://www.sony.com/electronics/support/software/00269130
