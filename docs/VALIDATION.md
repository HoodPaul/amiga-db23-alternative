# Validation record

**Revision:** 0.3  
**State:** Fit prototype; no physical assembly or Amiga operation verified.

## Generated-file checks

The actual saved files were checked on 29 October 2026. Reports live in `verification/`, with mechanical export results in `mechanical/mechanical_validation.json`. The independent review is `verification/independent-review.md`.

| Check | Recorded result |
|---|---|
| Male RGB native KiCad parse and netlist export | Passed with KiCad 7.0.11; schematic, saved board and footprint links agree |
| Female floppy native KiCad parse and netlist export | Passed with KiCad 7.0.11; schematic, saved board and footprint links agree |
| Native PCB DRC for both variants | Each: zero violations, zero unconnected pads, zero footprint errors |
| Independent 23-pin mapping and no-net-merge check | Passed; 610 portable saved-file checks across both projects |
| Native schematic ERC | Not run: KiCad 7 CLI does not expose ERC; parser/netlist checks are separate |
| OpenSCAD STL export | Passed for holder, coupon, keeper and both shim exports |
| Holder mesh | 8,268 triangles; one region; zero boundary or non-manifold edges |
| Coupon, keeper and single shim | Each closed and one region; shim-pair export has two intended regions |
| Analytic holder STEP | Valid; one solid; all 23 guide bores unobstructed |
| Assumed-part collision review | Zero holder intersection volume with the notched PCB, assumed connector flange/body/cups and both nuts |
| Coordinated preview review | Assembled, exploded and holder CAD renders inspected; three-page PDF and native PCB appearance plots inspected |

Each PCB contains 48 pads, 24 nets, 26 track segments and no vias. Native Gerber and Excellon exports are retained only under `fabrication/FIT-PROTOTYPE/`. No PCB order or print has been placed.

The 3D connector, pins and bought hardware are reference envelopes. Their generated STL files under `previews/reference-meshes/` are for rendering only, not printable functional replacements. Actual printable parts are under `mechanical/`.

## Physical checks not performed

- Measurement of purchased solder-cup connectors, pins, nuts and jackposts.
- Printer bore, nut pocket and keeper fit.
- Soldering heat effects on the chosen printed material.
- Motherboard, neighbouring component and case fit.
- Strength under cable insertion, extraction and normal handling.
- Assembled continuity, contact resistance and shell bonding.
- Functional video or external floppy testing on an Amiga.

CAD checks establish consistency only within their stated scope. They do not replace these physical checks or establish universal compatibility across Amiga models.

