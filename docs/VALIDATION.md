# Validation record

**PCB, assembly and mechanical revision:** 0.5  
**Date:** 30 October 2026
**State:** Fit prototype. No physical print, cable-load trial, assembled continuity test or Amiga operation has been verified.

Project development: **Paul of UK Computing Limited**, **Jon of JMC Electronics** and **AI assistance through Codex**.

The retained-0.5 review amendments square the forward end faces, fill the marked rear corners, change both PCB faces to `Amiga DB23 REV 0.5`, update project credits and lower the complete printed base underside to motherboard Z0. The two former circular feet and the 0.60 mm underside gap are removed without changing the PCB support height. The PCB copper, pad positions, holes, routing and outline remain unchanged from commit `d955061620d6cfa38a8a3d53e913e118aec0ad2e`.

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
| Actual silkscreen stroke containment | 27 items per board contained within outline; conservative minimum edge clearance 0.108035 mm; new label uses 0.70 mm text / 0.10 mm strokes |
| Native schematic ERC | Not run: KiCad 7 CLI does not expose ERC; parser/netlist checks are separate |

Reports are in `verification/*-drc.rpt`, `*-netlist.xml`, `pcb-build-summary.json`, `pcb-geometry-review.json`, `pcb-text-update.json`, `pin-map.csv` and `portable-audit.json`. The text-update report also compares non-text geometry with the pre-edit boards. Gerber and Excellon exports were regenerated from these saved revision 0.5 boards and remain under `fabrication/FIT-PROTOTYPE/`.

## Mechanical CAD

The revised base STL was regenerated with OpenSCAD and its analytic STEP with CadQuery; unchanged cap and trial-aid binaries were retained. All six delivered printable STL files passed topology checks. The independent saved-file verifier reads the delivered base, cap and jig STEP/STL files without importing the mechanical builder and passes **217 checks**.

| Delivered part | STL triangles | Closed regions | STEP |
|---|---:|---:|---|
| Solid base | 7,796 | 1 | Valid, one solid, 1,945.635 mm³ |
| Keyed cap | 220 | 1 | Valid, one solid, 978.692 mm³ |
| Pin-height jig | 1,036 | 1 | Valid, one solid, 3,008.953 mm³ |
| Hole-fit coupon | 26,384 | 1 | STL trial part |
| Clip-fit base coupon | 28 | 1 | STL trial part |
| Clip-fit cap coupon | 40 | 1 | STL trial part |

All six STL meshes have zero boundary or non-manifold edges in the recorded checks. The cap STL is exported roof-down for printing; its STEP retains assembly coordinates. The jig STEP/STL use print-bed coordinates. Apply the transforms documented in `mechanical/MECHANICAL_NOTES.txt` when assembling these shapes in CAD.

The following saved-file checks pass:

- Base, cap and seated PCB have no unintended intersection. Assumed connector flange, body, cups, mounting hardware and jackpost nuts clear the relevant printed parts.
- The joined PCB/DB23 clears the base throughout a 20 mm vertical lowering sweep, using exact prismatic sweeps and conservative cup envelopes.
- The holder minimum is Z0 and its saved STEP has one broad 359.105 mm² bottom face. The old foot parameters are absent, and representative material probes confirm the rail, pin-guide and rear-infill undersides all share that plane. All 23 guide bores are open. The assumed square pins clear the jig and cap, and independent mesh rays verify their common Z−3.20 tip stop and the jig's Z0 base-support datum.
- The default M3 × 12 mm screw, Ø8 × 0.50 mm underside insulating washer and direct top nut clear the cap. The tip is Z9.90, nut top Z9.15, nominal protrusion 0.75 mm and roof clearance above the tip 1.10 mm.
- Untrimmed 14 and 16 mm screws intersect the default cap. They are explicitly unsupported alternatives without trimming or a separately checked cover.
- The supported horizontal jackpost stem endpoint Y6.00 clears the printed passage and top mounting nuts. The printed clearance passage ends at Y6.20; this is not an unlimited stem-length allowance.
- The raised latch's conservative rearward-flex envelope clears the PCB. This checks space for assembly, not elastic strain, insertion force, retention force or fatigue.
- The recessed right-side base grounding-wire channel and dedicated J4 underside relief are present. Actual wire insulation, solder fillets and routing are not modelled as validated harnesses; they must not lift the base.
- Both forward ends have one straight outer face at X±25.60 through Y5.10. The former X25 rear-corner rebate is filled by 0.60 mm and the earlier X26 front face is trimmed by 0.40 mm to make a continuous square face. Material probes verify the filled corners and unchanged nut pockets; nominal outer wall and rear web are 0.615 and 0.80 mm. These are geometry checks, not a strength rating.

See `mechanical/mechanical_validation.json`, `verification/mechanical-audit.json` and `verification/independent-review.md` for detailed results.

## Reference motherboard layout

A limited reference and independent board-to-mechanical alignment audit passes 70 current checks, reproducible with `source/verify_reference_fit.py`. It verifies the local A4000 replica layout's SHA-256, directly parses both adapter boards and checks the saved STEP and outlines. The earlier source-board copper findings are retained rather than re-extracted; this scope is explicit in `verification/motherboard-reference-fit.json`. It is a reference CAD layout, not a measurement of the user's motherboard or chassis.

Its legacy mounting axes differ slightly from the iComp nominal grid. The adapter retains the iComp coordinate contract and uses Ø3.30 mm clearance holes; no enlargement of the motherboard holes is specified. The reference check also found that a bare Ø7 mm underside screw head overlaps a foreign copper track in plan. The default therefore requires an underside insulating washer and a deliberate J4-to-motherboard shell-ground wire, independently of screw contact.

A nearby connector lug motivated the remaining relief behind the squared end towers. The updated nominal clearance to its reference drill envelope is about 0.201 mm for the base/cap and 0.628 mm for the unchanged adapter outline, with zero drill-cylinder intersection. The square printed corner overlaps the ground land in plan by about 0.205 mm; this is not a verified physical collision or electrical contact because actual metal, solder-fillet and housing heights are unknown. It requires a physical clearance check. The comparison and its limitations are recorded in `verification/motherboard-reference-fit.md`. Component heights, metal lug shape, exposed copper, washer compression, actual board thickness and chassis clearance remain unverified. The Ø8 washers span 52.27 mm overall; the printed parts remain 52.00 mm at their widest aft section. Side-exiting wires can extend beyond these bounds.

## Visual and reproducibility checks

The six coordinated renders show the black cap fitted, cap removed, joined PCB/DB23 exploded, the actual base, base/cap and loading jig. All six previews and all five A4 drawing pages were visually inspected. The printable clip-fit coupons are provided separately. Reference meshes under `previews/reference-meshes/` represent unmeasured bought parts and are not functional print files.

Commands used from the project root include:

```sh
python3 source/build_mechanical.py
python3 source/verify_mechanical.py
python3 source/verify_pcb.py
python3 source/verify_reference_fit.py --reference-board /path/to/A4k-Replica-Acill.kicad_pcb
python3 source/render_previews.py
python3 source/make_drawings.py
```

The reference helper requires the exact external board identified by its stored hash; that file is not included in the project. The PCB builder was run with KiCad's Python interpreter and its CLI path. This flat-base rebuild used the pinned Windows libraries and portable OpenSCAD recorded in `verification/tool-versions.json`; the source and dependency notes are in `docs/DEVELOPMENT.md`.

## Physical checks still required

- Purchased male/female solder-cup connector dimensions, cup gap and flange bearing.
- Actual mounting holes, motherboard thickness, pad condition, neighbouring components and underside chassis clearance.
- Printed guide, jig, nut pocket and clip fit, including pin retention after jig removal.
- Soldering heat effects, support removal, material strength, creep, cable insertion/extraction loads and latch fatigue.
- Insulating washer coverage and the complete fastener stack with the chosen hardware.
- Ground-wire fillets, routing and independent shell continuity; all 23 circuit continuity and isolation checks before installation.
- Controlled video and external-floppy trials on identified Amiga hardware.

The recorded results establish consistency and clearance within their stated CAD assumptions. They do not establish physical fit, long-term strength, electrical operation or production readiness.
