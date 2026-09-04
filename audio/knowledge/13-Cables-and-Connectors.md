---
title: Cables and Connectors
created: 2026-09-04
updated: 2026-09-04
tags:
  - audio
  - cables
  - fundamentals
  - myth-busting
---

# Cables and Connectors

## Plain-English answer

For audio, a cable has only four jobs:

1. **Conduct** — carry the signal with as little added resistance as possible.
2. **Insulate and shield** — keep the signal separated and reduce hum/noise pickup.
3. **Connect reliably** — stay plugged in, no intermittent channel dropouts.
4. **Be physically livable** — flexible, right length, comfortable, durable.

Everything else sold as "cable science" at extreme prices is usually outside the range where audio cables can actually do anything.

## What a cable physically can and cannot change

A passive audio cable is made of resistors (conductor), capacitors, and inductors — all **linear** components. Linear components cannot:

- add harmonics or "warmth";
- add detail or micro-dynamics;
- change the musical character;
- "burn in" into a different sound.

They can only attenuate a tiny bit and filter a tiny bit. At audio frequencies with short cables and normal loads, both effects are extremely small.

## The numbers behind this

### Digital cables (USB, optical, coax)

Digital links either transmit the data or they do not. There is no partial "better sounding."

| Stream | Data rate | % of USB 2.0 (480 Mbps) capacity |
|---|---|---|
| CD 44.1 kHz / 16-bit | 1.41 Mbps | 0.29% |
| 96 kHz / 24-bit | 4.61 Mbps | 0.96% |
| 384 kHz / 32-bit | 24.58 Mbps | 5.12% |

The DAC regenerates the clock from the incoming data. Any "cleaner electricity" claim about a USB cable is not how a digital receiver works. A good USB cable is one that does not disconnect.

### Resistance (the only measurable analog effect)

Copper resistivity: about 1.68×10⁻⁸ Ω·m. A 1.2 m one-way cable (2.4 m loop) gives roughly:

| Conductor | Loop resistance | Effect into a 32 Ω load |
|---|---|---|
| 32 AWG (thin IEM strand) | ~0.32 Ω | about -0.08 dB |
| 24 AWG (typical headphone cable) | ~0.05 Ω | about -0.013 dB |
| 18 AWG (very thick cable) | ~0.012 Ω | about -0.003 dB |

Two important facts:

- These losses are **flat across the whole audio band**, so they do not change tone — only level, and by an inaudible amount.
- Any change that is even slightly audible can be undone with the volume knob.

### Skin effect

Copper's skin depth at 20 kHz is about 0.46 mm. An IEM's 32 AWG strand is about 0.40 mm in diameter — already smaller than the skin depth, so skin-effect loss does not meaningfully exist at audio frequencies. This is why the "litz / skin-effect" marketing argument mostly applies to RF, not audio.

### Capacitance and inductance

A meter of typical cable adds roughly 50–150 pF capacitance. At 20 kHz that is an impedance of tens of thousands of ohms, which means it barely interacts with a 32 Ω headphone load. Cable capacitance matters for long microphone lines and phono runs — not for a 1.2 m headphone cable.

## Purity, "vacuum" copper, and exotic metals

| Claim | Reality |
|---|---|
| 4N/6N/7N/8N copper sounds better | Conductivity difference between common purity grades is far below one percent; the resistance change in a short cable is a few milliohms |
| OFC (oxygen-free copper) | No meaningful audible effect in a short headphone cable |
| "Vacuum"/cryogenic/UFPC processing | No established mechanism that changes audible behavior in a linear conductor at line level |
| Silver is more conductive | True — about 5–6% better than copper — and therefore irrelevant against a 32 Ω load |
| Gold connectors | Gold resists tarnish, which is a genuine and worthwhile benefit at the connector. Gold is a worse conductor than copper, so gold-plating the conductor itself makes no sense |
| Palladium, rhodium, "space alloy" | Sold on rarity and price, not measured benefit |
| Directional cables | Not a real phenomenon in a symmetric linear conductor |
| Cable burn-in | The most likely change is your ears adapting — that part is real, but it is not the cable |
| Magnetic/quantum/diamond "treatment" boxes and clips | No plausible mechanism; placebo plus markup |
| Audiophile USB with "cleaner power" | Digital data is data; if it errors, you get dropouts, not a nicer tone |
| Balanced power conditioning for headphone rigs | Usually unnecessary for modern switch-mode DAC dongles |
| Faraday/shielded cable with bad termination | Can genuinely make things worse |

## Where cable money does buy something real

| Purchase | Real value | Notes |
|---|---|---|
| Gold-plated or rhodium-plated **connector** surfaces | Medium | Prevents tarnish → prevents crackle and intermittent contact |
| Good strain relief at the plug | Medium | Most cable failures happen at the connector |
| Correct, secure MMCX/2-pin/3.5/4.4 termination | **High** | A loose MMCX causes channel dropouts |
| Soft, light, flexible jacket | Medium | Comfort, less microphonics, less port torque |
| Right-angle or short USB-C for a pocket dongle | Medium | Reduces mechanical stress on the phone port |
| Braid/sleeve that resists tangling | Low–medium | Daily convenience |
| A replacement cable when yours is damaged | **High** | The obvious one |
| 4.4 mm balanced termination for a source that truly has balanced outputs | Conditional | Connector changes power/separation possibilities, not "magic" |
| Exotic conductor metal for sound | Very low | See resistance table above |
| Cable priced above ~฿2,000 for headphones | Very low | You are buying build quality or brand, not measurable audio performance |
| A passive 3.5-to-4.4mm adapter as a "balanced upgrade" | Zero, plus risk | A connector is not a circuit; wrong wiring can load an output incorrectly |

## The practical test before buying a cable

Answer in writing:

```text
What is wrong now?
   e.g. one channel cuts out, jacket is splitting, too stiff, too short, plug bent, connector tarnished/crackling

Would the replacement fix exactly that?
   Yes → buy the cheapest cable that fixes it and feels comfortable

Is my only reason "it might sound more detailed"?
   Then do a blind test: swap without telling yourself which is which, at matched volume.
   If you cannot identify it reliably, do not spend the money.
```

## Applied to your lab

```text
Phone/Windows → USB-C → BGVP MX1
   Use any short, data-capable, well-made USB-C cable. This link is digital: it either works or it does not.

MX1 4.4 mm → COZOY D1
   Keep a direct, correctly wired 4.4 mm IEM cable with good strain relief and secure 2-pin/MMCX connections.
   Cable choice here should be about fit, weight, and connector reliability.

MX1 3.5 mm → Sony WH-1000XM5
   Sony's supplied 3.5 mm cable is appropriate. It is a short single-ended link; a premium version cannot improve it.

Xiaomi Buds 5 Pro
   No cable exists in the chain. There is nothing to upgrade.
```

## Verdict

A cable is a mechanical part you touch every day, so quality matters — for durability, comfort, and reliable contact. It is not a tuning device.

> Spend on fit, tips, and a well-terminating replacement cable. Never spend on a claim you cannot hear in a level-matched blind test.

## Related notes

- [[knowledge/08-4.4mm-Balanced-Audio]]
- [[knowledge/12-Audio-Decision-Matrix]]
- [[knowledge/01-Audio-Signal-Chain]]
- [[knowledge/11-Listening-and-A-B-Testing]]
- [[setup/08-MX1-Output-Compatibility]]
