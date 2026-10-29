# Validation record

**Assembly and mechanical revision:** 0.4  
**Retained PCB revision:** 0.3  
**Date:** 29 October 2026  
**State:** Fit prototype; no physical assembly, cable-load trial or Amiga operation verified.

## Saved-file and CAD checks

Revision 0.4 raises the side rails and surrounding mounting lugs, fills the rear opening and adds a separate pin-height loading jig. The pin guide remains below the PCB for solder-fillet and heat clearance. Local anchor-head pockets retain recessed bearing seats and open outwards to avoid thin outer lips.

| Check | Recorded result |
|---|---|
| Retained native PCB, fabrication and native plot files | 42 files compared byte for byte with the revision 0.3 baseline; no changes |
| Portable saved-board and schematic-netlist audit | Re-run for this assembly revision: 610 checks passed across both variants |
| Native KiCad 7.0.11 PCB DRC | Retained revision 0.3 reports: each board has zero violations, zero unconnected pads and zero footprint errors; DRC was not repeated for unchanged boards |
| Native schematic ERC | Not run; KiCad 7 CLI does not expose ERC. Parser and exported-netlist checks are separate |
| OpenSCAD STL export | Passed for holder, coupon, nut keeper, shim pair, single shim and loading jig |
| Holder mesh | 8,052 triangles; one connected region; zero boundary or non-manifold edges |
| Loading jig mesh | 556 triangles; one connected region; zero boundary or non-manifold edges |
| Other printable meshes | Coupon, keeper and single shim each closed and one region; shim pair has two intended regions |
| Holder STEP | Valid, one solid, 2,227.066 mm³; all 23 guide bores open |
| Loading jig STEP | Valid, one solid, 4,222.032 mm³; no overlap with the holder or any of the 23 assumed square pins |
| Independent saved-file mechanical audit | 117 checks passed, reading delivered STEP/STL without importing the builder |
| Joined PCB/DB23 lowering path | No holder intersection throughout a 20 mm vertical sweep of the PCB, assumed flange/body and conservative cup envelopes |
| Nut fitting after PCB seating | Both 15 mm top-loading nut sweeps clear the holder and already-seated PCB |
| Recessed anchor hardware | Maximum Ø6.00 × 3.00 mm head/washer envelopes clear holder and PCB; centred Ø4.00 mm driver clears PCB; outboard pockets are open |
| Jig height datums | Independent mesh ray checks confirm all 23 lower-tip stops at Z−3.20, holder support at Z0.60 and locating-peg tops at Z1.80 |
| Coordinated visual review | Five CAD preview images and all four pages of the revised A4 drawing PDF inspected |

The mechanical builder was run as `python3 source/build_mechanical.py`. The independent audit was run as `python3 source/verify_mechanical.py`; it needs CadQuery and VTK. The portable electrical audit was run as `python3 source/verify_pcb.py`; it needs only Python's standard library. Tool versions remain recorded in `verification/tool-versions.json`.

The reports are `mechanical/mechanical_validation.json`, `verification/mechanical-audit.json`, `verification/independent-review.md`, `verification/portable-audit.json` and `verification/revision-0.4-audit.json`. Native revision 0.3 reports and exports remain under `verification/` and `fabrication/FIT-PROTOTYPE/`.

Each PCB retains 48 pads, 24 nets, 26 track segments and no vias. All 23 signal positions remain separate, with a distinct shell circuit. No PCB order or physical print has been placed.

## Scope of the geometry checks

All connector body, cup and bought-hardware envelopes remain explicitly assumed. The lowering-path checks use exact sweeps for prismatic parts and conservative bounding sweeps for the cups. They establish clearance only against those assumed shapes. The rear infill has shallow top reliefs for pre-soldered J3 fillets; it does not provide underside soldering access after the PCB is seated.

The raised lug surfaces are at Z5.75, but anchor-head seats remain at Z2.40, keeping the permitted head top at or below Z5.40. Preload these bolts before lowering the joined PCB/DB23. The separate height jig must be removed first. The two 0.60 mm mounting shims remain required.

The jig sets equal lower-tip projection only when the holder seats correctly. Equal top heights additionally depend on equal pin lengths, and the tested guide fit must retain the pins when the jig is removed. These are physical assembly checks.

Reference meshes under `previews/reference-meshes/` are for illustration, not functional printed replacements. Printable trial parts are under `mechanical/`.

## Physical checks not performed

- Measurement of purchased solder-cup connectors, pins, nuts and jackposts.
- Printer bore, nut pocket, keeper and jig fit, including retention of loaded pins after transfer.
- Flange bearing against the cradle after clamping, and any measured spacer needed to carry cable loads without bending solder cups or signal tails.
- Soldering heat effects, printed material strength, layer adhesion, creep and cable insertion/extraction loads.
- Motherboard, neighbouring component and case fit, including underside anchor nuts and tool access.
- Assembled continuity, contact resistance and shell bonding.
- Functional video or external floppy testing on an Amiga.

More material and closed CAD geometry are not a measured strength rating. The saved-file checks do not establish physical fit, print accuracy, thermal performance or universal compatibility across Amiga models.
