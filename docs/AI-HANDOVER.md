# AI and engineering handover

**Mechanical/assembly revision:** 0.6; **PCB revision:** 0.5
**Date:** 30 October 2026
**State:** Fit prototype. Paul has trial-printed 0.5 and reported fragile lid projections and nuts within the footprint. Revision 0.6 is not yet physically tested; the full PCB/hardware stack and strength remain unmeasured. No assembled electrical operation on an Amiga has been verified.

Project development: **Paul of UK Computing Limited**, **Jon of JMC Electronics** and **AI assistance through Codex**.

## Objective and agreed direction

Make an affordable motherboard DB23 adapter using a genuine solder-cup DB23, horizontal PCB, suitable straight pins from ordinary header stock and a substantial printed base. Retain existing Amiga cables.

Revision 0.6 implements Paul's print feedback: remove the four thin lid projections and both hook legs, fill their catch recesses in the base, and simplify the lid into an optional cosmetic cover. Use a 1.60 mm roof and short 1.20 mm side/rear rim starting at Z10.30, above the nominal mounting nuts. Keep two broad locating tabs over the jackpost pockets; tiny superglue spots on the tower tops can attach the cover after inspection. Fitted jackposts must retain their nuts without it. Adhesive is not the primary cable-load attachment.

All 23 guide bores have 0.40 mm deep, 45-degree entry funnels from Z4.10 to Z4.50, opening from Ø0.92 to Ø1.72. Keep the straight bore below for pin retention. The coupon has matching funnels. Trial careful hand clearing with a pin vice and the actual pins; hot insertion has not been validated.

Paul reports that the selected nuts sit within the current print footprint. The photo does not include the PCB beneath the nut. Preserve clearance for the complete stack: PCB thickness 1.00 mm, mounting nut top Z9.15, M3 x 12 tip Z9.90. Retain the square forward tower faces at X±25.60 over Y0.65–5.10 and neighbour relief X±25.00 over Y5.10–7.50. The cap keeps the same XY envelope. Do not fill the neighbour relief merely from a nut-only photograph.

PCB files, routing, outline, fabrication exports and the legend **Amiga DB23 REV 0.5** are unchanged. Keep company names in the project credits. The broad base underside stays at Z0 and the PCB support at Z5.75. Cable loads are intended to pass from the clamped flange to the base and through-bolts. No physical load rating is established.

Do not reopen the rejected HD26/custom-cable interface without a reason or request. Keep the genuine DB23 external interface.

## Agreed assembly order

1. Solder DB23 cups to the matching PCB on both faces, and prepare covered shell-wire joints.
2. Load 23 equal-length pins into the base on the height jig; remove the jig, lower the joined PCB/DB23 from above and solder pin tops.
3. Fit the selected jackpost nuts and hex posts, checking flange bearing and rear-stem clearance.
4. Fit to the motherboard; insert screws upward, fit underside insulating washers and top nuts, solder tails and shell bonds, inspect, then optionally glue the cover to the tower tops.

The motherboard is not a forming fixture. See [ASSEMBLY.md](ASSEMBLY.md) for checks and heat precautions.

## Current files

- Shared geometry and assumptions: `source/design_parameters.json`.
- PCB projects: `pcb/DB23M_RGB/` and `pcb/DB23F_Floppy/`.
- Mechanical builder: `source/build_mechanical.py`; editable source and print files under `mechanical/` include `DB23_Holder_v0.6`, `DB23_Cap_v0.6`, pin-height jig and chamfered hole coupon. Superseded outputs and clip-fit coupons are removed.
- Native and independent checks: `verification/`, `mechanical/mechanical_validation.json` and [VALIDATION.md](VALIDATION.md).
- Assembly renders and drawing PDF: `previews/`.

Read the actual reports before quoting counts, passes or clearance claims. Native KiCad 7 ERC is not available through the installed CLI; exact netlist checks are separate. CAD geometry is not a physical fit test.

## Geometry contract

Millimetres; X across the port, Y inward from flange front Y0, Z upward from motherboard top Z0. The connector faces negative Y. Male pin 1 is at positive X; female numbering is mirrored.

Sourced nominal values: 2.77 mm row pitch, 2.84 mm row spacing and 1.385 mm stagger. Front pins 13–23 are at Y8.08; rear pins 1–12 at Y10.92. Original shell-anchor axes are X±22.135, Y9.50. Mating centreline Z6.25.

Revision 0.5 PCB: 51.20 mm overall width, Y4.00–13.00, 1.00 mm assumed thickness, underside Z5.75. Ears begin at Y6.00, reach X±25.00 until Y7.50 and then X±25.60; the local cutback clears a reference neighbouring lug. The stepped front clears the nut towers. Its new J3 mounting holes are Ø3.30 with Ø6.50 exposed lands at the original shell-anchor axes. J4 wire pads at X±18.00, Y7.00 are Ø1.20/2.40. Keep wire and solder away from the top nut-bearing lands.

The 23-pin guide nominally uses Ø0.92 bores for assumed 0.64 mm square pins and stops at Z4.50, leaving 1.25 mm beneath the PCB. The 10.70 mm pins run from Z−3.20 to Z7.50. The complete base underside now reaches Z0 as one broad, coplanar surface; the two former circular feet and loose 0.60 mm shims are absent, while the PCB remains at Z5.75. The separate jig supports this flat base and must be removed before heat. Printer, pin retention and bore fits require coupons.

## Hardware assumptions

The default motherboard mounting screw is M3 × 12 mm measured under the head, with a user-listed Ø7 mm, approximately 1 mm thick head. Underside insulating washers are assumed Ø8 × 0.50 mm; top nuts 5.50 mm AF × 2.40 mm high bear directly on the supported J3 lands. There is no default top washer. These are not measured purchase specifications.

With assumed motherboard thickness 1.60 mm, the under-head stack through the nut is `0.50 + 1.60 + 5.75 + 1.00 + 2.40 = 11.25 mm`; a 12 mm screw projects 0.75 mm past the nut and ends at Z9.90. The assumed head bottom is Z−3.10, 1.50 mm beneath the assumed motherboard underside. Ø8 underside washers span 52.27 mm across the pair, slightly wider than the 52.00 mm prints. Adding a top washer consumes the spare thread and requires a separate stack review. Fourteen and sixteen millimetre screws are alternatives only after trimming or checking a different cap. Verify full thread engagement, all bearing surfaces and underside pad/trace/chassis clearance. Do not drill or countersink the motherboard.

Cable-facing jackposts require the original-compatible 4-40 UNC thread. Prototype rear stems/nuts are M3, AF5.50/thickness2.40 with fit allowances. HARTING 09670009924 is a candidate thread arrangement, not a drop-in or frozen part. The rear-stem passage ends at Y6.20; the conservative permitted stem end is Y≤6.00 from the flange datum. It clears the top mounting nut as well as the bolt. Do not describe clearance as unlimited.

Keep the flange-to-cradle bearing check. The illustrative flange is unmeasured; any actual gap needs an appropriate firm spacer or revised bearing face, without bending cups or tails to close it. Optional compression stops must match the actual support height and chosen base variant.

## Electrical decisions

Every `P01`–`P23` circuit stays independent and pin-for-pin. The four J3/J4 pads share `SHIELD`, separate from every signal position. Never join video pin 13 to video grounds 16–20 by assumption.

A deliberate DB23 metal-shell bond is required. The default under-head washers are insulating. Require a deliberate J4-to-motherboard original shell-ground-pad wire as well as the connector-shell bond; do not rely on bolt or shank contact. Pre-tack that wire on the motherboard with the base removed, then route it out through the recessed right-side base channel (X24 outward, Y9.50 ±0.60, Z0–1.00) and up to J4. Plastic and solder mask are insulating. Verify both bonds and confirm the wire does not lift the flat base.

The board remains passive. It is not a scan-rate converter, floppy converter or protection circuit.

## Remaining engineering work

1. Obtain and measure each male/female solder-cup part, pins, nuts, jackposts and mounting hardware.
2. Complete [MEASUREMENTS.md](MEASUREMENTS.md) for the intended motherboard revision and case.
3. Trial the hole/cap fits and soldering heat behaviour using actual print settings.
4. Check the flat base bearing surface, PCB-ear support, local front-corner reliefs, optional-cover seating and adhesive access, underside washers/heads, all screw lengths, both shell bonds and neighbouring components. Reference A4000 layout checks are not proof of fit on the user's actual board revision.
5. Update shared parameters and regenerate coordinated CAD, previews and reports as needed.
6. Assemble, inspect and record an unpowered prototype before controlled functional and insertion/extraction trials.

Canonical repository: [HoodPaul/amiga-db23-alternative](https://github.com/HoodPaul/amiga-db23-alternative), default branch `main`. No project-wide licence or production release has been selected.


## Universal PCB prototype — ordered 30 October 2026

**Use the universal PCB at your own risk.** A separate [universal prototype package](../pcb/DB23_Universal_Prototype/README.md) now includes editable PCB, Gerbers/drills, preview, checks and order records. It retains the existing physical routing, adds VIDEO 1 / FLOPPY 1 markings on both faces, removes other numbers and uses round signal pads. Internal numbering remains the VIDEO reference; actual connector orientation and continuity must be checked.

Paul confirmed ordering 30 boards from JLCPCB on 30 October 2026: two-layer FR-4, 1.00 mm, 1 oz, black mask, white silkscreen, ENIG. Receipt, physical fit and functional operation remain unverified. Native KiCad 10.0.7 DRC reports zero errors/unconnected items and four missing-library warnings; exact checks confirm 23 separate signal connections. This is a standalone board snapshot, not a new coordinated PCB revision or a replacement for the two existing variants.


### Hardware order update — 30 October 2026

Paul confirmed **30 PCBs** (correcting the earlier 20), **100 M3 × 12 mm screws with 7 mm heads**, **100 M3 304 stainless nuts**, and **40 strips of 1×40 L11.5 headers** (nominally 1,600 pins). See [the order details](../pcb/DB23_Universal_Prototype/ORDER_RECORD_2026-10-30.md). The selected 11.5 mm pins are intended to be used untrimmed after carrier removal; nominal protrusion above the PCB is 1.55 mm and roof clearance 2.70 mm with the existing jig. Actual dimensions and fit are unverified; main CAD still models 10.70 mm pins. Earlier quoted prices apply to the original 20-board screenshot, not the final 30-board order.
