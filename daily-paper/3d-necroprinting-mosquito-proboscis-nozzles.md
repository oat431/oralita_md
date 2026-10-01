---
title: "3D Necroprinting: Mosquito Mouthparts as 3D Printer Nozzles"
tags: [paper, biohybrid, 3d-printing, bioprinting, ig-nobel, applied-science]
created: 2026-10-01
source: "Puma et al.; 3D necroprinting: Leveraging biotic material as the nozzle for 3D printing; Science Advances 11(47), eadw9953, 19 Nov 2025; DOI 10.1126/sciadv.adw9953; PDF: F:/papers/3D Necroprinting.pdf"
---

# 3D Necroprinting: Mosquito Mouthparts as 3D Printer Nozzles

> *Paper: Justin Puma, Zhen Yang, Evan Johnston, et al., Jianyu Li and Changhong Cao (corresponding), McGill University with Drexel University. "3D necroprinting: Leveraging biotic material as the nozzle for 3D printing." Science Advances 11(47), eadw9953, 19 November 2025. Article pages "1 of 13" to "13 of 13" match PDF pages 1-13; PDF page 14 is the publisher cover sheet. Plain-language body first; the dense detail (mechanics, rheology, numbers, quotes) lives in the Appendix at the end.*

## What Is This Paper, In Plain Words

Yes, it is exactly what the title sounds like: a team at McGill took the mouthparts of dead female mosquitoes and used them as the nozzle of a 3D printer. And no, it is not a joke paper. It ran in Science Advances, one of the top journals in the world, and the engineering behind it is genuinely serious. This is the Ig Nobel sweet spot: a premise that makes you laugh, followed by results that make you think.

Here is the problem they attack. When a 3D printer "writes" with liquid ink (a method called direct ink writing), the fineness of your printout is limited by the fineness of the nozzle, the little tip the ink squeezes through. The best commercially available ultra-fine metal tips are around 35 micrometers wide inside (a human hair is about 70 to 100 micrometers, so these are already thin), and they cost over $80 *each*. They are also made of metal and plastic: not biodegradable, and the US alone throws away over 4 billion dispense tips a year (p. 1).

Now here is nature's answer: a female mosquito already owns a nearly perfect micro-dispensing needle. Her proboscis (the "beak" that pierces your skin) is stiff, straight, about 2 mm long, and its inner channel is only 20 to 25 micrometers wide, finer than anything you can buy off the shelf for a reasonable price. Evolution spent a few hundred million years perfecting it. The mosquitoes used were lab-reared, uninfected, and already dead (frozen stock from a research supplier), so nobody was harmed for the nozzles.

The team built a custom high-resolution printer, glued a mosquito proboscis into a standard dispense tip with UV-curing resin, and printed with it. The results:

- **Lines as fine as 18 to 28 micrometers**, about twice the resolution of the best cheap commercial tips, and comparable to or better than the $80 specialty ones (pp. 7, 9).
- They printed a **honeycomb** 600 micrometers across, a **maple leaf** (a nicely patriotic touch from a Canadian lab), and most impressively, **living scaffolds with cancer cells and red blood cells inside**. After printing, 86.1% of the cells were still alive, which shows the mosquito needle is gentle enough for bioprinting (p. 7).
- A whole nozzle costs about **80 cents** to assemble, and the mosquito itself costs under 2 cents to raise (p. 9).

Of course, a biological part has a biological breaking point, and finding it was half the science. Push too much pressure and the proboscis bursts. The team measured exactly when and why: it fails at about 60 kPa of internal pressure, and it fails in two distinct ways. Sometimes the ink dries into a plug at the tip and pressure builds up there until the wall splits (failure type 1); sometimes the ink is simply too thick and the pressure needed to push it through splits the wall near the inlet instead (failure type 2). Both produce the same signature: a crack running lengthwise along the tube. They then turned this into a simple operating chart so a user can pick an ink and a speed that will never burst the nozzle (pp. 4-7).

There is even an unexpected bonus. Because the proboscis bursts at a known pressure, it acts like a **biological fuse**: if the printer ever pushes too hard, the nozzle sacrifices itself instead of crushing the delicate cells in the ink. Metal nozzles have no such fail-safe (p. 9).

## Why You Should Care

1. **It reframes "biohybrid" engineering.** Most biohybrid work uses living tissue (muscle-powered robots, spider-leg grippers from the same "necrobotics" lineage this paper's name comes from). This paper shows that *dead* biological parts can be manufacturing components: cheap, consistent, biodegradable, and in some specs better than engineered equivalents.
2. **The selection method is reusable.** They did not just grab a mosquito; they surveyed every dispensing structure in nature (stingers, fangs, harpoons, claws, four kinds of proboscis, plant xylem), scored them against engineering criteria (curvature, stiffness, inner diameter, length), and the mosquito won on points (pp. 2-3). That is a template for any "nature already solved this" problem.
3. **The failure analysis is the real engineering.** Quantifying burst pressure, identifying the two failure modes, and deriving an operating window from a fluid-flow model is what separates this from a stunt. The appendix below has the full mechanics.
4. **It is honest about limits.** Glass-pulled nozzles still print finer (under 1 micrometer) and withstand far more pressure; the proboscis has a shelf life (9 days at room temperature, but a year frozen); and the authors list exactly what they did not control. No overselling.

---

# Appendix: The Dense Details

> *Everything below is the reference layer: numbers, mechanics, rheology, and quotes, page-cited to the article ("p. N" = both article page N of 13 and PDF page N).*

## A. The Problem in Numbers (p. 1)

- Over 4 billion dispense tips used annually in the US alone (breakdown in Supplementary Materials); conventional tips are metal/plastic, nonbiodegradable.
- Finest commercial metal tip: 36-gauge (36G), ~35 micrometers inner diameter, over $80 USD per tip (NanoFil Needles, World Precision Instruments). Plastic tips stop at 30G (~150 micrometers inner diameter).
- Micro dispense tips (diameter <100 micrometers) are needed for microelectronic fabrication, pharmaceutical injection, 3D bioprinting, and direct ink writing (DIW).

## B. Nozzle Selection: The Survey (pp. 2-3)

Two categories of biological micro dispense tips: **fluid depositing** (stingers of bees/wasps/scorpions, snake fangs, centipede forcipules, cone-snail harpoons) and **fluid withdrawing** (plant xylem vessels; insect proboscides in four types: flexed under head, retracted into head, flexed in front of head, coiled).

DIW-nozzle criteria: minimal curvature, high stiffness and strength (minimal compliance during extrusion), small inner diameter (resolution), manageable length (manipulable but not so long that backpressure risks failure). Candidates shortlisted from the Ashby-style chart: proboscides of mosquitos, assassin bugs, bed bugs, aphids, sandflies, tsetse flies.

**Why the female mosquito proboscis won:**
- Nearly zero curvature (stiff and straight; pierces epidermis and infiltrates blood vessels despite being soft polymeric material)
- Inner diameter 20-25 micrometers average: smaller than the minimum diameter of commercial metal and plastic tips
- Length ~2 mm: manipulable, adjustable during fabrication to tune backpressure
- Stiffness ~200 MPa: comparable to common plastics
- Strength (measured here for the first time): burst pressure ~708 kPa hoop-stress equivalent (below)
- Anatomy: core-shell structure; labium is the shell (discarded), the fascicle (labrum + hypopharynx stylets) forms a single sealed hollow tube
- Accessibility: widely available, easy to rear, global (p. 3)
- Species used: Aedes aegypti (Fig. 1B highlight; supplied frozen, uninfected, from BEI Resources, strain Black Eye Liverpool NR-48920)

Comparison context: glass-pulled tips reach <1 micrometer diameter but are hard to fabricate and extremely brittle (p. 3).

## C. Printer Design and Nozzle Integration (p. 3)

Custom DIW printer: high-resolution motion stage, piston-driven extruder with micrometer-level dispensing, synchronized via Arduino microcontroller and DC signal switch. Design-phase modeling: power-law process window, validated with COMSOL simulations using a Herschel-Bulkley inelastic flow model. Integration: the proboscis is bonded with UV-curable resin into a 30G Luer-Lock engineered dispense tip through an SLA-printed concentricity adapter, giving a continuous fluid path syringe → dispense tip → proboscis → substrate. Methods detail (p. 10): mosquitoes sterilized by 80% ethanol dips; labium detached and discarded; resin applied via toothpick with the outlet oriented downward to keep the channel clear; cured 10 s under a 3-W 395-nm UV flashlight while rotating; both ends cut with a razor blade. Engineered tips are reusable: soak in acetone, blow out with compressed air.

## D. Mechanical Failure: Two Modes and the Numbers (pp. 4-7)

**Burst test.** Custom rig: syringe + 30-psi pressure transducer + dispense tip + proboscis filled with deionized water, outlet sealed with two-part epoxy (cured 10 min to 90%), plunger displaced at 0.0167 mm/s (quasistatic), pressure recorded to rupture. Average burst pressure across tests: **59.7 kPa** (Fig. 3E). Internal pressure vs time shows a peak at the moment of failure (Fig. 3D).

**Thin-walled pressure vessel model.** Imaging showed inner diameter more than 10x wall thickness, justifying the thin-wall idealization; assumptions: isotropic material, small strains. Stresses: longitudinal sigma_zz = Pd/4t, hoop sigma_theta_theta = Pd/2t. With internal diameter 23.6 micrometers and wall thickness 0.96 micrometers, at failure: sigma_zz = 354 kPa, sigma_theta_theta = **708 kPa**. Hoop stress dominates and the observed axial crack is perpendicular to it: failure is governed by circumferential principal stress. The paper claims first-ever quantification of the proboscis strength at ~708 kPa, well below common metals and plastics used in engineered tips (p. 6).

**Fracture-mechanics cross-check.** For assumed initial crack lengths 2a = 8 and 12 micrometers, critical stress intensity factors K_IC = 4.35 and 7.04 kPa m^1/2, close to reported chitin hydrogel values (~10 kPa m^1/2), consistent with the chitinized labrum/hypopharynx joined by a less-chitinized membrane (p. 6).

**Type 1 failure: clog-induced overpressure at the tip** (pp. 5-6). Shear-thinning ink accumulating at the outlet loses shear stress; storage modulus dominates loss modulus (solid-phase behavior); the plug blocks flow; by Herschel-Bulkley, pressure builds at the outlet; hoop stress concentrates at imperfections; microfractures initiate, propagate, coalesce. Occasional, observed mid-air extrusion of Cellink Start.

**Type 2 failure: uniform overpressure from high-viscosity flow demands** (p. 6). High apparent viscosity means high backpressure to maintain velocity; pressure drops steadily inlet → outlet, so the inlet wall sees sigma_theta_theta(inlet) >= sigma_theta_theta(critical) first: consistent rupture near the inlet. Observed with Pluronic F-127 at high extrusion rate.

**Operating guideline (Fig. 3I).** Herschel-Bulkley model (Eq. 3) relates ink velocity to pressure drop, length, inner radius, yield stress tau_y, consistency coefficient k, flow behavior index n (0 < n < 1 shear-thinning). For 40% (w/v) Pluronic F-127 (k = 375 Pa·s^n, n = 0.05, tau_y = 310 Pa): maximum allowable ink velocity ~0.015 mm/s (15 micrometers/s). Additional ink-screening rule: surface tension plus operating parameters must yield an Ohnesorge number greater than 10 for continuous filaments.

## E. Process Window: Draw Ratio (p. 7)

Balance ink extrusion speed v_ink against nozzle movement speed v_nozzle via the draw ratio r = v_ink / v_nozzle:

| Regime | Condition | Behavior |
|---|---|---|
| Overextrusion | r > 1 | Nonuniform continuous lines; type 1 failure risk (Bernoulli pressure buildup at outlet; gushing or rupture) |
| Good extrusion | 0.25 < r <= 1 | Continuous, uniform lines; line width approaches the 20-30 micrometer proboscis inner diameter |
| Underextrusion | r <= 0.25 | Broken filaments; excessive stretching from velocity contrast fractures the ink |

Experimental failure strain of 40% (w/v) Pluronic F-127: 3000%.

**Resolution achieved:** ~20 micrometers printing resolution, ~250% finer than the ~50 micrometer inner diameter of a standard 34G tip (the smallest commonly used commercial tip per the authors); comparable specialty 36G tips (~35 micrometer ID, ~40 micrometer resolution) cost ~$80 each (p. 7).

## F. Demonstrations (pp. 7-9)

1. **Honeycomb** (Fig. 4B): ~600 x 600 x 310 micrometers, Pluronic F-127; SEM shows ~22 micrometer printed line width and high interlayer fidelity.
2. **Maple leaf** (Fig. 4C): 900 x 870 x 310 micrometers; printed lines ~18 micrometers, the finest in the paper.
3. **Cell-laden grid scaffold** (Fig. 4D): 600 x 600 x 310 micrometers, 28-micrometer lines, Pluronic F-127 with B16 murine melanoma cancer cells; separate RBC demo with bovine red blood cells (~2 billion cells/ml estimated in print). Post-printing cell viability **86.1% ± 2.1% (n = 3)**: sufficient resistance to shear-stress-induced rupture during extrusion.

Printing parameters for all demos (p. 11): print speed 20 micrometers/s, ink speed ~14 micrometers/s (r ≈ 0.7), layer height 15-20 micrometers (20 ± 3 micrometer nominal), on 75 x 25 x 1 mm glass slides, ambient 20-30 degrees C and 30-70% relative humidity.

**Extras:** picoliter-scale drug-delivery demonstration with hydrogel carrier into pig skin (uptake and redeposition; elasticity/compliance reduce substrate damage vs rigid nozzles, p. 9). The defined burst pressure acts as a biological "fuse" passively limiting extrusion force and protecting shear-sensitive cell-laden bioinks, "an intrinsic safeguard not found in synthetic micronozzles" (p. 9). Surface-defect simulation (cavity/crevice defects modeled from SEM): outlet velocity difference vs perfect surface only 0.1% (0.02 micrometers/s), friction impact negligible (p. 9).

## G. Comparison, Lifespan, Robustness (p. 9)

**vs glass-pulled tips (the only resolution competitor, <1 micrometer lines):** glass wins resolution and pressure tolerance (theoretical burst ~20,800 kPa) but loses on fragility (extreme brittleness, vibration sensitivity), consistency (multivariable pull process: heating temperature, pulling force/speed, delay, environment, plus stock variability; mosquito proboscides show 11% inner-diameter error and 16.5% wall-thickness error and need nearly no quality control), cost (~$26 per pre-pulled glass pipette vs ~$0.8 assembly per bio tip; mosquito rearing <$0.02 each), and biodegradability (glass: none).

**Lifespan (10 tips tested):** minimum 9 days at ambient storage; 30% failure rate after 14 days; at -20 degrees C, functional after a full year of aging.

**Environmental robustness:** repeated printing tests across 20-30 degrees C and 30-70% RH held structural shape and mechanical performance; extreme conditions suspected to cause catastrophic failure, boundaries unexplored.

**Other candidate bio-tips named:** assassin bug, bed bug, tsetse fly, sandfly, and aphid proboscides (aphids offer <1 micrometer internal diameter, i.e., a possible sub-micrometer bio-nozzle).

## H. Materials and Methods Highlights (pp. 10-12)

- Rheology: Anton Paar MCR 302, 25-mm aluminum parallel plate, 1-mm gap; frequency sweeps 0.01-1000 Hz; stress sweeps 0.1-1000 Pa at 1 Hz; ~25 degrees C.
- Inks: Cellink Start (polyethylene oxide training bioink; centrifuged 1000 RPM 30 s); 40% (w/v) Pluronic F-127 sacrificial temperature-sensitive bioink (stored 4 degrees C, equilibrated 10 min); cell inks per section F with Pluronic F-127 MW 12,600 g/mol at 35 wt% (cancer cells) and 29 wt% (RBC); viability ink 29% (w/v) F127 in Live/Dead PBS, 0.22-micrometer filtered, 5 x 10^6 cells/ml; drug-delivery ink 4% (w/v) low-MW alginate (90 kDa) in DMEM.
- Viability assay: prints covered with DMEM, incubated 37 degrees C / 5% CO2 for 6 h, imaged on EVOS M5000.
- SEM: Hitachi SU3400; prints flash-frozen in liquid N2, freeze-dried 2-3 days, sputter-coated 4-nm platinum.
- Confocal: ZEISS LSM 800; B16 z-stacks over 30 micrometers at 10 micrometer steps, max-intensity projections in ImageJ; RBC at 10x/20x/63x.
- Motion control: AeroScript (Aerotech gantry) plus G-code; ink speed calibrated by matching z-stage speed until filament neither thinned/fractured nor bent/flowed out of plane.
- Sterilization: ethanol-based deemed sufficient for bioprinting research; ethylene oxide, low-dose ionizing radiation, hydrogen peroxide vapor suggested for biomedical use.

## I. Limitations Stated by the Authors (pp. 9-10)

- Biological samples only partially screened (species and gender controlled; age and other variables unmonitored); a systematic study of species/gender/age variation is proposed future work.
- Biological components degrade with time, unlike synthetic parts; lifespan must be managed (see G).
- Extreme environmental boundaries unexplored.
- Engineered dispense tips still used as carriers in the current assembly (reusable custom adapters proposed to eliminate them, p. 3).

## J. Practitioner Takeaways

1. **Nature's parts have datasheets now.** If you design with biological components, this paper's method (survey → criteria scoring → burst testing → failure-mode mapping → operating window) is a complete playbook for qualifying them.
2. **Characterize failure before capability.** The most reusable content is not the prints but Fig. 3: two failure modes, one stress model, one operating chart. Any soft-matter extrusion system benefits from the same treatment.
3. **The draw ratio r = v_ink/v_nozzle is the single knob** for extrusion quality: keep 0.25 < r <= 1; the paper's demo ran at r ≈ 0.7.
4. **Hoop stress governs thin biological tubes:** sigma = Pd/2t with d ~ 23.6 micrometers and t ~ 0.96 micrometers gives a 708 kPa material-strength estimate from a 59.7 kPa burst measurement; axial cracks are the fingerprint of hoop failure.
5. **A known breaking point is a feature:** design bio-components as fuses where downstream contents (cells) are more valuable than the part.
6. **Cold storage is the shelf-life answer:** -20 degrees C extends a 9-day ambient lifespan to over a year, which is what makes bio-tips practical inventory rather than fresh produce.

## K. Memorable Quotes

> "Here we report '3D necroprinting,' a biohybrid manufacturing technique that repurposes female mosquito proboscides as high-resolution 3D printing nozzles." (p. 1, abstract)

> "To our knowledge, this is the first report to quantify the female mosquito proboscis's strength at approximately 708 kPa, well below the reported material strengths of common metals and plastics used in engineered dispense tips." (p. 6)

> "the proboscis exhibits a defined burst pressure that passively limits extrusion forces, acting as a biological 'fuse' to protect sensitive cell-laden bioinks from shear-induced damage, an intrinsic safeguard not found in synthetic micronozzles" (p. 9)

> "Repurposing dispensing structures from uninfected, laboratory grown, deceased organisms represents a new avenue for engineering applications" (p. 1)

> "the female mosquito proboscis requires nearly no quality control due to their minimal structural variability and consistent fabrication process executed by natural procedures" (p. 9)

## Related

- Source PDF: `F:/papers/3D Necroprinting.pdf`
- Article online (external): `https://www.science.org/doi/10.1126/sciadv.adw9953` (open access, CC BY-NC)
- The named lineage: necrobotics (spider-leg microgrippers, Yap et al., Advanced Science 2022) and the group's earlier biohybrid mosquito-stinger AFM probe (Ljubich et al., J. Vis. Exp. 2024)

---

*Summary written 2026-10-01 in the plain-language body + dense appendix format. Page numbers are the article's "N of 13" pagination, identical to PDF pages 1-13; PDF page 14 is the publisher cover sheet. Quotes are verbatim; everything else is own-words paraphrase. References (pp. 12-13) and Supplementary Materials (figs. S1-S20, tables S1-S4, movies S1-S7) are not summarized beyond what the article text states about them. The Ig Nobel framing and hair-width comparison in the body are external context, not from the paper.*
