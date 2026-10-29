# Validation record

**PCB, assembly and mechanical revision:** 0.5  
**Date:** 29 October 2026  
**State:** Fit prototype. No physical print, cable-load trial, assembled continuity test or Amiga operation has been verified.

## Electrical CAD

Both revised PCB projects were generated, saved, reloaded and checked using KiCad 7.0.11. Their exported schematic netlists agree exactly with the saved boards. Each board contains 50 pads, 24 nets, 26 track segments and no vias: 23 independent signal circuits and a separate four-pad SHIELD circuit.

| Check | Result |
|---|---|
| Native PCB DRC, male RGB | Zero violations, zero unconnected pads, zero footprint errors |
| Native PCB DRC, female floppy | Zero violations, zero unconnected pads, zero footprint errors |
| Portable saved-file audit | 648 checks passed, 324 per variant |
| Mounting holes | J3 at nominal original anchors, Ø3.30 mm adapter drill / Ø6.50 mm land |
| Dedicated shell-wire pads | J4, separate from nut-bearing mounting lands |
| Between-row SHIELD crossbar | Nominal minimum clearance to row pads: 0.27 mm |
| Actual silkscreen stroke containment | 27 items per board contained within outline; conservative minimum edge clearance 0.176145 mm |
| Native schematic ERC | Not run: KiCad 7 CLI does not expose ERC; parser/netlist checks are separate |

Reports are in `verification/*-drc.rpt`, `*-netlist.xml`, `pcb-build-summary.json`, `pcb-geometry-review.json`, `pin-map.csv` and `portable-audit.json`. Gerber and Excellon exports were regenerated from these saved revision 0.5 boards and remain under `fabrication/FIT-PROTOTYPE/`.

## Mechanical CAD

OpenSCAD generated the six printable STL files. CadQuery generated analytic base, cap and jig STEP files. The independent saved-file verifier reads the delivered STEP/STL without importing the mechanical builder and passes **176 checks**.

| Delivered part | STL triangles | Closed regions | STEP |
|---|---:|---:|---|
| Solid base | 8,324 | 1 | Valid, one solid, 1,787.389 mm³ |
| Keyed cap | 220 | 1 | Valid, one solid, 981.284 mm³ |
| Pin-height jig | 1,036 | 1 | Valid, one solid, 3,008.953 mm³ |
| Hole-fit coupon | 26,384 | 1 | STL trial part |
| Clip-fit base coupon | 28 | 1 | STL trial part |
| Clip-fit cap coupon | 40 | 1 | STL trial part |

All six STL meshes have zero boundary or non-manifold edges in the recorded checks. The cap STL is exported roof-down for printing; its STEP retains assembly coordinates. The jig STEP/STL use print-bed coordinates. Apply the transforms documented in `mechanical/MECHANICAL_NOTES.txt` when assembling these shapes in CAD.

The following saved-file checks pass:

- Base, cap and seated PCB have no unintended intersection. Assumed connector flange, body, cups, mounting hardware and jackpost nuts clear the relevant printed parts.
- The joined PCB/DB23 clears the base throughout a 20 mm vertical lowering sweep, using exact prismatic sweeps and conservative cup envelopes.
- All 23 guide bores are open. The assumed square pins clear the jig and cap, and independent mesh rays verify their common Z−3.20 tip stop and the Z0 foot-support datum.
- The default M3 × 12 mm screw, Ø8 × 0.50 mm underside insulating washer and direct top nut clear the cap. The tip is Z9.90, nut top Z9.15, nominal protrusion 0.75 mm and roof clearance above the tip 1.10 mm.
- Untrimmed 14 and 16 mm screws intersect the default cap. They are explicitly unsupported alternatives without trimming or a separately checked cover.
- The supported horizontal jackpost stem endpoint Y6.00 clears the printed passage and top mounting nuts. The printed clearance passage ends at Y6.20; this is not an unlimited stem-length allowance.
- The raised latch's conservative rearward-flex envelope clears the PCB. This checks space for assembly, not elastic strain, insertion force, retention force or fatigue.
- The foot grounding-wire exit and dedicated J4 underside relief are present. Actual wire insulation, solder fillets and routing are not modelled as validated harnesses.

See `mechanical/mechanical_validation.json`, `verification/mechanical-audit.json` and `verification/independent-review.md` for detailed results.

## Reference motherboard layout

A limited two-dimensional cross-check and independent board-to-mechanical alignment audit pass 68 checks. They used the local A4000 replica layout identified by source URL and SHA-256 in `verification/motherboard-reference-fit.json`. It is a reference CAD layout, not a measurement of the user's motherboard or chassis.

Its legacy mounting axes differ slightly from the iComp nominal grid. The adapter retains the iComp coordinate contract and uses Ø3.30 mm clearance holes; no enlargement of the motherboard holes is specified. The reference check also found that a bare Ø7 mm underside screw head overlaps a foreign copper track in plan. The default therefore requires an underside insulating washer and a deliberate J4-to-motherboard shell-ground wire, independently of screw contact.

A nearby connector lug motivated the local front-corner reliefs in the PCB, base and cap. The final nominal clearance to that reference drill envelope is about 0.423 mm for the base/cap and 0.628 mm for the adapter outline. The projected copper-pad gap at the closest printed corner is only about 0.016 mm, so actual metal, solder fillet and housing clearance still needs checking. The comparison and its limitations are recorded in `verification/motherboard-reference-fit.md`. Component heights, metal lug shape, exposed copper, washer compression, actual board thickness and chassis clearance remain unverified. The Ø8 washers span 52.27 mm overall; the printed parts are 52.00 mm wide. Side-exiting wires can extend beyond these bounds.

## Visual and reproducibility checks

The six coordinated renders show the black cap fitted, cap removed, joined PCB/DB23 exploded, the actual base, base/cap and loading jig. All six previews and all five A4 drawing pages were visually inspected. The printable clip-fit coupons are provided separately. Reference meshes under `previews/reference-meshes/` represent unmeasured bought parts and are not functional print files.

Commands used from the project root include:

```sh
python3 source/build_mechanical.py
python3 source/verify_mechanical.py
python3 source/verify_pcb.py
python3 source/render_previews.py
python3 source/make_drawings.py
```

The PCB builder was run with KiCad's Python interpreter and its CLI path. VTK rendering used an Xvfb display. Tool versions are recorded in `verification/tool-versions.json`; the source and dependency notes are in `docs/DEVELOPMENT.md`.

## Physical checks still required

- Purchased male/female solder-cup connector dimensions, cup gap and flange bearing.
- Actual mounting holes, motherboard thickness, pad condition, neighbouring components and underside chassis clearance.
- Printed guide, jig, nut pocket and clip fit, including pin retention after jig removal.
- Soldering heat effects, support removal, material strength, creep, cable insertion/extraction loads and latch fatigue.
- Insulating washer coverage and the complete fastener stack with the chosen hardware.
- Ground-wire fillets, routing and independent shell continuity; all 23 circuit continuity and isolation checks before installation.
- Controlled video and external-floppy trials on identified Amiga hardware.

The recorded results establish consistency and clearance within their stated CAD assumptions. They do not establish physical fit, long-term strength, electrical operation or production readiness.
