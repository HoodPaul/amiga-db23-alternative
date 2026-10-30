# AI and engineering handover

**PCB, assembly and mechanical revision:** 0.5  
**Date:** 29 October 2026  
**State:** Fit prototype. Connector sample, hardware, print fit and physical insertion strength are unmeasured. No assembled electrical operation on an Amiga has been verified.

Project development: **Paul of UK Computing Limited**, **Jon of JMC Electronics** and **AI assistance through Codex**.

## Objective and agreed direction

Make an affordable motherboard DB23 replacement using a genuine solder-cup DB23, horizontal PCB, straight pins recovered from ordinary header stock if suitable, and a substantial printed base. Retain existing Amiga cables.

Paul reviewed the earlier print for strength and assembly. Revision 0.4 filled the rear and raised its rails. He then proposed a stronger and simpler mounting stack: two metal screws **upwards from beneath the motherboard**, through a solid base and the adapter PCB, with nuts above and insulating washers beneath the heads. Revision 0.5 implements that direction with a shorter PCB, mounting ears and a keyed black clip-on cap. The PCB legend is **Amiga DB23 REV 0.5** on both faces; company names belong in the project credits rather than the silkscreen. Do not restore the old top-access screw-head recesses, separate 0.60 mm shims or printed expanding motherboard pegs.

The retained-revision 0.5 review squares the forward tower outer faces to X±25.60 over Y0.65–5.10, filling 0.60 mm at the former rear-corner rebates and moving the remaining X±25.00 neighbour relief to Y5.10–7.50 behind the towers. The cap matches this front profile. The adapter PCB outline, signal mapping and hardware stack are unchanged; its legend is `Amiga DB23 REV 0.5`.

The cap retains jackpost nuts and conceals hardware. It is fitted last. Cable loads are intended to pass from the clamped DB23 flange into the solid base and positive through-bolt attachment, with broad support under PCB mounting ears. No load rating is established.

Do not reopen the rejected HD26/custom-cable interface without a reason or request. Keep the genuine DB23 external interface.

## Agreed assembly order

1. Solder DB23 cups to the matching PCB on both faces, and prepare covered shell-wire joints.
2. Load 23 equal-length pins into the base on the height jig; remove the jig, lower the joined PCB/DB23 from above and solder pin tops.
3. Fit the selected jackpost nuts and hex posts, checking flange bearing and rear-stem clearance.
4. Fit to the motherboard; insert screws upward, fit underside insulating washers and top nuts, solder tails and shell bonds, inspect, then fit the keyed cap.

The motherboard is not a forming fixture. See [ASSEMBLY.md](ASSEMBLY.md) for checks and heat precautions.

## Current files

- Shared geometry and assumptions: `source/design_parameters.json`.
- PCB projects: `pcb/DB23M_RGB/` and `pcb/DB23F_Floppy/`.
- Mechanical builder: `source/build_mechanical.py`; editable source and print files under `mechanical/` include `DB23_Holder_v0.5`, `DB23_Cap_v0.5`, pin-height jig, hole coupon and two clip-fit coupons.
- Native and independent checks: `verification/`, `mechanical/mechanical_validation.json` and [VALIDATION.md](VALIDATION.md).
- Assembly renders and drawing PDF: `previews/`.

Read the actual reports before quoting counts, passes or clearance claims. Native KiCad 7 ERC is not available through the installed CLI; exact netlist checks are separate. CAD geometry is not a physical fit test.

## Geometry contract

Millimetres; X across the port, Y inward from flange front Y0, Z upward from motherboard top Z0. The connector faces negative Y. Male pin 1 is at positive X; female numbering is mirrored.

Sourced nominal values: 2.77 mm row pitch, 2.84 mm row spacing and 1.385 mm stagger. Front pins 13–23 are at Y8.08; rear pins 1–12 at Y10.92. Original shell-anchor axes are X±22.135, Y9.50. Mating centreline Z6.25.

Revision 0.5 PCB: 51.20 mm overall width, Y4.00–13.00, 1.00 mm assumed thickness, underside Z5.75. Ears begin at Y6.00, reach X±25.00 until Y7.50 and then X±25.60; the local cutback clears a reference neighbouring lug. The stepped front clears the nut towers. Its new J3 mounting holes are Ø3.30 with Ø6.50 exposed lands at the original shell-anchor axes. J4 wire pads at X±18.00, Y7.00 are Ø1.20/2.40. Keep wire and solder away from the top nut-bearing lands.

The 23-pin guide nominally uses Ø0.92 bores for assumed 0.64 mm square pins and stops at Z4.50, leaving 1.25 mm beneath the PCB. The 10.70 mm pins run from Z−3.20 to Z7.50. The base's integral mounting feet reach Z0, incorporating the former 0.60 mm shims without raising the PCB. The separate jig must accommodate these feet and be removed before heat. Printer, pin retention and bore fits require coupons.

## Hardware assumptions

The default motherboard mounting screw is M3 × 12 mm measured under the head, with a user-listed Ø7 mm, approximately 1 mm thick head. Underside insulating washers are assumed Ø8 × 0.50 mm; top nuts 5.50 mm AF × 2.40 mm high bear directly on the supported J3 lands. There is no default top washer. These are not measured purchase specifications.

With assumed motherboard thickness 1.60 mm, the under-head stack through the nut is `0.50 + 1.60 + 5.75 + 1.00 + 2.40 = 11.25 mm`; a 12 mm screw projects 0.75 mm past the nut and ends at Z9.90. The assumed head bottom is Z−3.10, 1.50 mm beneath the assumed motherboard underside. Ø8 underside washers span 52.27 mm across the pair, slightly wider than the 52.00 mm prints. Adding a top washer consumes the spare thread and requires a separate stack review. Fourteen and sixteen millimetre screws are alternatives only after trimming or checking a different cap. Verify full thread engagement, all bearing surfaces and underside pad/trace/chassis clearance. Do not drill or countersink the motherboard.

Cable-facing jackposts require the original-compatible 4-40 UNC thread. Prototype rear stems/nuts are M3, AF5.50/thickness2.40 with fit allowances. HARTING 09670009924 is a candidate thread arrangement, not a drop-in or frozen part. The rear-stem passage ends at Y6.20; the conservative permitted stem end is Y≤6.00 from the flange datum. It clears the top mounting nut as well as the bolt. Do not describe clearance as unlimited.

Keep the flange-to-cradle bearing check. The illustrative flange is unmeasured; any actual gap needs an appropriate firm spacer or revised bearing face, without bending cups or tails to close it. Optional compression stops must match the actual support height and chosen base variant.

## Electrical decisions

Every `P01`–`P23` circuit stays independent and pin-for-pin. The four J3/J4 pads share `SHIELD`, separate from every signal position. Never join video pin 13 to video grounds 16–20 by assumption.

A deliberate DB23 metal-shell bond is required. The default under-head washers are insulating. Require a deliberate J4-to-motherboard original shell-ground-pad wire as well as the connector-shell bond; do not rely on bolt or shank contact. Pre-tack that wire on the motherboard with the base removed, then route it out through the right foot groove (X24 outward, Y9.50 ±0.60, Z0–1.00) and up to J4. Plastic and solder mask are insulating. Verify both bonds.

The board remains passive. It is not a scan-rate converter, floppy converter or protection circuit.

## Remaining engineering work

1. Obtain and measure each male/female solder-cup part, pins, nuts, jackposts and mounting hardware.
2. Complete [MEASUREMENTS.md](MEASUREMENTS.md) for the intended motherboard revision and case.
3. Trial the hole/cap fits and soldering heat behaviour using actual print settings.
4. Check base feet, PCB-ear support, local front-corner reliefs, cap removal, underside washers/heads, all screw lengths, both shell bonds and neighbouring components. Reference A4000 layout checks are not proof of fit on the user's actual board revision.
5. Update shared parameters and regenerate coordinated CAD, previews and reports as needed.
6. Assemble, inspect and record an unpowered prototype before controlled functional and insertion/extraction trials.

Canonical repository: [HoodPaul/amiga-db23-alternative](https://github.com/HoodPaul/amiga-db23-alternative), default branch `main`. No project-wide licence or production release has been selected.
