# Engineering and AI working instructions

Read this file, [docs/AI-HANDOVER.md](docs/AI-HANDOVER.md), [source/design_parameters.json](source/design_parameters.json) and the current [validation record](docs/VALIDATION.md) before editing.

## Project purpose

Develop an affordable motherboard DB23 replacement using a genuine solder-cup DB23, a horizontal PCB, straight individual pins and a printed structural holder. Retain compatibility with existing Amiga DB23 cables. Do not substitute a different external connector standard without an explicit design decision.

## Current state

Revision 0.3 is an unmeasured fit prototype. Nominal motherboard geometry is sourced; the selected solder-cup connector, nuts, jackposts, printed fit and surrounding clearances are not verified. Never promote assumed geometry or CAD-only checks to a claim of physical compatibility or successful operation.

## Files and regeneration

- Shared dimensions and assumptions live in `source/design_parameters.json`.
- PCB projects live in `pcb/DB23M_RGB/` and `pcb/DB23F_Floppy/`.
- The mechanical builder and OpenSCAD source generate the printable trial parts.
- Keep generator changes, native files, previews, BOM and documentation consistent.
- Before regeneration, check for manual changes in native CAD. Preserve and port those edits rather than overwriting them silently.
- Keep intermediate downloads, package extracts and temporary tool configurations outside the project package.
- Record tool versions and actual command outcomes in the validation record.

## Geometry contract

All dimensions are millimetres. The x axis runs across the port, y runs inward from the flange reference plane and z runs upward from the motherboard top. In a top view, the connector faces towards negative y. Male pin 1 is at positive x; the female numbering is mirrored.

The nominal signal grid is 2.77 mm along each row, 2.84 mm between rows and 1.385 mm staggered. Pins 13–23 are on the front row at y = 8.08 mm; pins 1–12 are on the rear row at y = 10.92 mm. Original shell anchors are x = ±22.135 mm, y = 9.50 mm. Check source drawings before altering this geometry.

## Electrical requirements

- Preserve 23 separate pin-to-pin circuits; use neutral `P01`–`P23` names.
- Preserve the separate `SHIELD` circuit. Do not merge it with signal grounds by assumption.
- Video pin 13 must not be joined to video grounds 16–20 on the adapter.
- The male and female variants need independent mapping checks.
- Treat mounting straps, wire bonds and shell continuity as assembly requirements, not automatic consequences of a printed bracket.
- Run native parsing and connection checks after edits. Do not report ERC or DRC checks that the installed tool has not actually performed.

## Mechanical requirements

- Keep the signal pins supported inside the holder, with soldering access and heat clearance.
- A 0.64 mm square pin has a diagonal of approximately 0.905 mm. A 0.80 mm finished round bore does not clear it.
- Fit bores, nut pockets and printer allowances using the provided coupon and actual parts.
- Match captive nuts to the purchased jackpost's rear stem; cable-facing and rear threads can differ.
- Use the original motherboard mounting holes. Do not assume that new motherboard drilling or underside fastener clearance is acceptable.
- Preserve the 0.60 mm anchor shim/washer requirement in the height stack; do not tighten the holder across an unsupported gap.
- Locating pegs provide alignment only; the holder needs positive retention to carry insertion and extraction loads.
- Keep male/female solder-cup envelope assumptions explicit. The reference connector model is not a measured part.

## Documentation and release

Use British English. Distinguish sourced nominal dimensions, design choices, assumptions and physically tested results. Describe the design as an original replacement project developed from the supplied concept. Do not invent collaborator identities, product certifications, licences or validation results.

Revision releases must contain matching CAD, source, printable parts, preview images and reports. Keep unverified fabrication files clearly marked as fit prototypes.

