# AI and engineering handover

**Revision:** 0.3  
**Date:** 29 October 2026  
**State:** Fit prototype. Connector sample and printed fit have not been measured. No assembled hardware or Amiga operation has been verified.

## Objective and agreed design

Make an affordable replacement for the original motherboard-mounted DB23 using available solder-cup connectors. Retain the normal DB23 external interface.

Paul's proposed assembly is a horizontal PCB similar to his supplied starting files, with shorter wings and a printed holder. The holder supports the connector, captures its port-jackpost nuts, sets the PCB height and guides all 23 straight motherboard pins in a substantial block. The pins can be recovered individually from ordinary 0.1-inch header stock, but must be positioned on the original 2.77 mm grid.

Do not reopen the HD26/custom-cable alternative without a reason or request. It added a new external interface while retaining the adapter construction work and was rejected as offering little improvement over the supplied draft.

## Current files

- Shared geometry: `source/design_parameters.json`.
- RGB PCB: `pcb/DB23M_RGB/DB23M_RGB.kicad_pro`.
- Floppy PCB: `pcb/DB23F_Floppy/DB23F_Floppy.kicad_pro`.
- Mechanical builder: `source/build_mechanical.py`.
- Mechanical source: `mechanical/DB23_Holder_v0.3.scad`.
- Printable holder, hole coupon and optional nut keeper: `mechanical/`.
- Check reports: `verification/`; actual results are summarised in `docs/VALIDATION.md`.

## Recorded CAD validation

Both KiCad 7.0.11 native DRC reports contain zero violations, zero unconnected pads and zero footprint errors. The portable audit passes 610 checks across both variants, including the exact exported schematic netlist. Native ERC was not run. The holder STL is closed and one component; STEP is valid and one solid; all 23 bores are unobstructed. The independent collision review passes against the explicitly assumed connector envelope, nominal nuts and notched PCB. See `verification/independent-review.md`; none of these results establishes physical fit.

## Fixed nominal geometry

The motherboard grid is from iComp's replacement drawings: 2.77 mm along-row pitch, 2.84 mm row spacing, 1.385 mm stagger; pins 13–23 at y = 8.08 mm and pins 1–12 at y = 10.92 mm. The shell-anchor centres are x = ±22.135 mm, y = 9.50 mm. The nominal mating centreline is z = 6.25 mm.

The reference frame is millimetres, x across the port, y inward from the flange front reference plane and z above the motherboard top. Male pin 1 is at positive x in this top view; female numbering is mirrored.

## Assumed geometry and hardware

The PCB is 40 × 12 × 1.00 mm overall, spanning y = 4.00–16.00 mm with its lower face at z = 5.75 mm. Two 2.00 × 1.50 mm front-corner notches clear the nut towers; preserve them. The 1.00 mm thickness and front edge position depend on the actual solder-cup connector and are not frozen production dimensions.

The printed holder is nominally 52 mm wide. Pin guide bores are 0.92 mm for assumed 0.64 mm square pins. Their diagonal is approximately 0.905 mm, so Paul's proposed 0.8 mm drill is a possible pilot or trial size, not a finished clearance bore for those square pins. Printer and pin fit must be established with the coupon.

Jackposts need 4-40 UNC at the cable-facing thread. Prototype defaults use M3 rear stems and M3 captive nuts, with assumed 5.50 mm across flats and 2.40 mm nut thickness, plus clearance. HARTING 09670009924 is a candidate, not a frozen BOM part. Other rear stems exist; the actual purchased hardware must match the pockets. Do not specify M3.5 by assumption.

Original-position motherboard retention is required. The holder's 3.30 mm fastener clearances do not authorise enlarging the original nominal 3.20 mm motherboard holes. The holder bottom is z = 0.60 mm, so two 0.60 mm anchor shims or washers are required under its mounting feet before tightening; do not pull an unsupported gap closed. Fastener length, underside clearance and chassis contact require physical checks.

## Electrical decisions

Each of the 23 positions remains an independent pin-to-pin circuit. PCB nets are named `P01`–`P23` instead of model-dependent signal names. The separate `SHIELD` path needs real wire or metal bonding. The printed holder does not provide grounding. Video pin 13 must remain separate from video grounds 16–20 on the adapter.

The board is passive. It does not alter video scan rates or floppy signalling and is not a video converter, drive adapter or protection circuit.

## Next engineering work

1. Select and obtain the male and female solder-cup DB23 parts, jackposts, nuts and pins.
2. Complete `docs/MEASUREMENTS.md` separately for both connector genders and the intended motherboard.
3. Print the hole coupon and test the pins, nut fit and soldering heat strategy.
4. Update shared parameters, regenerate coordinated files and compare diffs.
5. Trial-print the holder, dry-fit the assembly and verify mating face position, mounting, PCB/cup interference and case clearance.
6. Re-run native and independent connection checks. Record exact reports and versions.
7. Assemble and electrically inspect a prototype before a powered Amiga test.

The canonical repository is [HoodPaul/amiga-db23-alternative](https://github.com/HoodPaul/amiga-db23-alternative), with `main` as its default branch. This is the initial revision 0.3 prototype upload. No project-wide licence or production release has been selected.

