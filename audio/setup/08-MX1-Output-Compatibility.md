---
title: BGVP MX1 Output Compatibility
created: 2026-09-04
updated: 2026-09-04
tags:
  - audio
  - bgvp-mx1
  - balanced
  - sony
---

# BGVP MX1 Output Compatibility

## Quick answer

Use the MX1's **3.5 mm single-ended output** for the Sony WH-1000XM5. It is sufficient for this headphone and avoids an unnecessary balanced-to-single-ended adapter.

Use the MX1's **4.4 mm balanced output** for the COZOY D1 only when using the proper direct 4.4 mm IEM cable.

## Why

The WH-1000XM5 has one 3.5 mm stereo input. It is not a dual-entry balanced headphone. A 4.4 mm plug at the source does not make the XM5 balanced.

A generic passive 3.5 mm-to-4.4 mm adapter only changes connector geometry. It cannot convert an electrical single-ended signal into a balanced signal. Worse, the wiring may connect a true balanced amplifier output to a shared ground or otherwise be incompatible.

## Output matrix

| Headphone/IEM | MX1 output | Cable | Verdict |
|---|---|---|---|
| COZOY D1 | 4.4 mm balanced | Direct 4.4 mm IEM cable | Correct |
| Sony WH-1000XM5 | 3.5 mm single-ended | Sony-supplied 3.5 mm stereo cable | Recommended |
| Sony WH-1000XM5 | 4.4 mm balanced | Generic adapter | Avoid |
| Sony WH-1000XM5 | 4.4 mm source | Explicitly engineered converter | Technically possible, but no benefit here |

## MX1 output figures

BGVP's product material reports approximately:

- 4.4 mm balanced: 320 mW / 32 Ω, 4 Vrms
- 3.5 mm single-ended: 125 mW / 32 Ω, 2 Vrms

Those figures do not mean the XM5 needs the larger output. The XM5 is a powered ANC headphone and can be driven comfortably from the MX1's 3.5 mm output.

## Safety procedure

1. Stop playback.
2. Set the MX1 to low gain.
3. Set volume to minimum.
4. Connect the Sony-supplied stereo cable to the MX1 3.5 mm output.
5. Connect the other end to the XM5 until it clicks.
6. Start playback quietly and raise the level slowly.
7. If using ANC, turn the XM5 on; for passive listening, it can remain off.

## Do not confuse these terms

- **4.4 mm:** connector format.
- **Balanced:** an electrical output/input topology.
- **Single-ended:** a signal using a shared reference/ground.
- **Adapter:** may change plug shape but does not necessarily convert circuit topology.
- **Enough power:** reaches the desired level cleanly; it does not mean maximum available power.

## Related notes

- [[knowledge/08-4.4mm-Balanced-Audio]]
- [[knowledge/02-DAC-Amplifier-and-Output-Power]]
- [[setup/07-Sony-WH1000XM5-Setup]]

## Sources

- BGVP MX1: https://www.bgvp-hifi.com/product/bgvp-mx1-hi-res-usb-dac-3-5-single-ended-4-4-balanced-portable-dac/
- Sony WH-1000XM5 supplied cable guide: https://helpguide.sony.net/mdr/wh1000xm5/v1/en/contents/TP1000534744.html
- Sony WH-1000XM5 specifications: https://helpguide.sony.net/mdr/wh1000xm5/v1/en/contents/TP1000541014.html
