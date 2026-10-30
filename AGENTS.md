# Engineering and AI working instructions

Read this file, [docs/AI-HANDOVER.md](docs/AI-HANDOVER.md), [source/design_parameters.json](source/design_parameters.json) and the current [validation record](docs/VALIDATION.md) before editing.

## Project purpose

Develop an affordable motherboard DB23 replacement using a genuine solder-cup DB23, a horizontal PCB, straight individual pins and a printed structural base. Retain compatibility with existing Amiga DB23 cables. Do not substitute a different external connector standard without an explicit design decision.

## Current state

PCB, assembly and mechanical revision 0.5 is an unmeasured fit prototype. Nominal motherboard geometry is sourced; the selected solder-cup connector, hardware, printed fit and surrounding clearances are not verified. Never turn assumed geometry or CAD-only checks into a claim of physical compatibility or successful operation.

## Files and regeneration

- Shared dimensions and assumptions live in `source/design_parameters.json`.
- PCB projects live in `pcb/DB23M_RGB/` and `pcb/DB23F_Floppy/`.
- Keep builders, native CAD, printable parts, previews, BOM and documentation consistent.
- Before regeneration, check for manual native-CAD changes. Preserve and port deliberate edits rather than overwriting them silently.
- Keep downloads, package extracts and temporary tool configuration outside the project.
- Record actual commands, tool versions and outcomes in the validation record.

## Geometry contract

All dimensions are millimetres. X runs across the port, Y inward from the flange front plane and Z upward from the motherboard top. The connector faces negative Y. Male pin 1 is at positive X in a motherboard top view; female numbering is mirrored.

The nominal signal grid is 2.77 mm along each row, 2.84 mm between rows and 1.385 mm staggered. Pins 13–23 are at Y8.08; pins 1–12 are at Y10.92. Original shell anchors are X±22.135, Y9.50. Check source drawings before changing this geometry.

## Electrical requirements

- Preserve 23 separate pin-to-pin circuits, `P01`–`P23`, for both variants.
- Keep `SHIELD` distinct from all signal positions. Do not join video pin 13 to video grounds 16–20.
- J3 contains the two plated mounting lands at the original shell-anchor axes. J4 provides separate shell-bond wire pads, clear of the top nut-bearing surfaces.
- A deliberate J4 bond to the DB23 shell and a separate J4-to-motherboard shell-ground-pad wire are required. Do not rely on mounting-bolt contact; the default under-head washers are insulating. Plastic is not a grounding path.
- Run native parsing, DRC and exact connection checks after PCB edits. Do not claim an unavailable or unperformed ERC.

## Mechanical requirements

- Revision 0.5 uses screws upward from beneath the motherboard through the solid printed base and adapter PCB, with nuts above the PCB and insulating washers beneath the heads.
- Preserve the squared forward tower outer faces at X±25.60, Y0.65–5.10 and the matching cap profile. The remaining X±25.00 neighbour relief begins behind the towers at Y5.10; do not restore the former full-height rebates through the end walls.
- Preserve flat support immediately beneath each PCB mounting ear. Do not tighten across a gap or bow the PCB.
- The mounting feet now reach Z0 and incorporate the former 0.60 mm shims. Do not add the obsolete loose anchor shims to this height stack.
- Keep the PCB underside at Z5.75 and the connector centreline at Z6.25 unless a measured connector change requires a coordinated revision.
- The separate keyed cap retains jackpost nuts and covers hardware. The base and through-bolts provide the intended structural attachment; do not rely on cap latches for cable loads.
- Use only the original motherboard holes. Do not countersink or enlarge the motherboard to fit fasteners. Verify head, pad, underside and chassis clearances.
- The default mounting screw is M3 × 12 mm under-head length, with an assumed Ø7 × 1 mm head. Use Ø8 × 0.50 mm insulating washers under the heads, nuts directly on the supported top lands, and no default top washers. Actual parts are not measured. Longer screws or added top washers require a separately checked stack and cap envelope.
- Preserve the extended rear-stem clearance behind the jackpost nuts: passage to Y6.20, permitted stem end Y≤6.00. Long jackposts must clear the upward mounting hardware.
- Assemble DB23 and PCB first. Load equal-length pins with the height jig, remove the jig, lower the joined assembly and solder pin tops. Fit port hardware, attach to the motherboard, solder and inspect, then fit the cap last.
- Keep signal pins supported with solder and heat clearance. A 0.64 mm square pin has about a 0.905 mm diagonal; a finished Ø0.80 bore does not clear it.
- Establish bore, nut, latch and jig fits using coupons and the actual printer. No printed material or insertion strength is qualified.

## Documentation and release

Use British English. Separate sourced nominal values, design choices, assumptions and physically tested results. Describe an original replacement project developed from Paul's supplied concept. Project credits are **Paul of UK Computing Limited**, **Jon of JMC Electronics** and **AI assistance through Codex**. Preserve the PCB legend `Amiga DB23 REV 0.5`; keep company names in the documentation credits. Do not invent licences, collaborators, certifications or validation results.

Keep releases coordinated across source, native CAD, prints, previews and reports. Manufacturing exports remain clearly labelled fit prototypes until measurements and physical checks establish otherwise.
