# Validation record

**Mechanical/assembly revision:** 0.6. **PCB revision:** 0.5.
**Date:** 30 October 2026. **State:** Fit prototype; revision 0.6 is not yet physically printed or tested.

Project development: **Paul of UK Computing Limited**, **Jon of JMC Electronics** and **AI assistance through Codex**.

## Physical observations and scope

Paul trial-printed revision 0.5, reported delicate/missing lid features and marked four thin projections for removal. He reported that the nuts fit within the print footprint. The supplied photo shows a nut on the base without the PCB beneath it. This observation does not measure the full PCB/fastener stack, clearances, strength or electrical operation. The 0.6 geometry responds to that feedback; no new physical pass is claimed.

The update removes four thin cover projections and two hook legs, fills the base catch recesses, thickens the cover roof to 1.60 mm and replaces the deep side features with a short 1.20 mm rim above the mounting nuts. Two broad locating tabs remain. The optional cover can be attached with tiny glue spots on the tower tops after inspection. All 23 pin guides gain a 0.40 mm deep, 45° entry funnel, Ø1.72 at the mouth above the straight Ø0.92 bore. The hole-fit coupon includes matching entry geometry. Old mechanical outputs and clip coupons are removed.

## Electrical CAD

The complete `pcb/` and `fabrication/` directories remain byte-for-byte identical to main commit `c59b0faba1f23329de7d6f23b2fcd576300d418a`. The PCB legend remains `Amiga DB23 REV 0.5` on both faces. The saved-file portable audit was rerun and passed **648 checks**, 324 per variant.

Both saved boards contain 50 pads, 24 nets, 26 track segments and no vias: 23 independent `P01`–`P23` circuits and a separate four-pad `SHIELD` circuit. Saved schematic netlists agree with their boards. The retained KiCad 7.0.11 native DRC reports show zero violations, zero unconnected pads and zero footprint errors for both boards. Native KiCad DRC was not rerun for this mechanical-only change; the CLI is unavailable in this runtime. Native schematic ERC has not been run.

The retained silkscreen check contains all 27 text items per board within the outline, with conservative minimum edge clearance 0.108035 mm. Native reports, netlists, text/geometry reviews, `pin-map.csv` and the refreshed `portable-audit.json` remain under `verification/`. No new electrical performance result is inferred.

## Mechanical CAD

A full OpenSCAD/CadQuery build generated all four STL parts and three STEP solids. The independent saved-file verifier reads those delivered exports without importing the builder and passed **273 checks**. All three STEP files are valid single solids. All four STL files are connected, closed meshes in the topology checks.

| Part | STL triangles | Connected regions | Boundary/non-manifold edges | STEP volume |
|---|---:|---:|---:|---:|
| Base | 13,652 | 1 | 0 | 1,939.706 mm³ |
| Optional cover | 132 | 1 | 0 | 1,150.640 mm³ |
| Pin-height jig | 1,036 | 1 | 0 | 3,008.953 mm³ |
| Hole-fit coupon | 34,320 | 1 | 0 | STL trial only |

The saved-file checks establish:

- The four thin cover projections and both hook legs are absent. Both base catches are filled with material. The broad keys and tower-top glue bearing are present; the upper rim follows the neighbour relief.
- All 23 guide bores remain open. Analytic STEP probes confirm the shallow taper and preserved lower guide; independent STL rays confirm each funnel midsection at Z4.30 has radius 0.66 mm.
- The base has one broad, coplanar Z0 bottom face of 359.104525 mm², with no projecting feet. PCB support stays at Z5.75, guide top Z4.50 and nominal fillet/heat gap 1.25 mm.
- The base, cover, PCB, assumed connector body/cups and selected hardware envelopes have no unintended overlap. A 20 mm vertical sweep clears the joined PCB/DB23 insertion path; nut loading paths also clear.
- M3 × 12 mm screws and rotation-independent envelopes of the top nuts clear the cover. With the assumed PCB and under-head washer, nut top is Z9.15, screw tip Z9.90 and roof underside Z11.00. Roof clearance is 1.10 mm and thread projection above the nut is 0.75 mm.
- Untrimmed 14/16 mm screws intersect this cover, as recorded in `mechanical-audit.json`; they are unsupported without a separately checked change. Under-head insulating washers remain required.
- The horizontal jackpost stem clears the passage through Y6.20 when its end is Y≤6.00. A lifted-nut envelope intersects the fitted stem, supporting the intended nut retention without the cover. Threads, torque and physical retention remain untested.
- J4 underside fillet reliefs and the recessed right-side grounding-wire route are preserved. Actual solder and wire must fit without lifting the base.
- The cap STL's roof-down transform restores its STEP bounds. The jig's independent STL rays confirm all 23 stops at Z−3.20, support pads at Z0 and locator tops at Z1.20.

Glue strength, filament behaviour, bore compensation, hot insertion, soldering heat, clamping torque, cable forces and fatigue are outside these CAD checks. Read [the saved-file review](../verification/independent-review.md) and machine-readable reports for scope.

## Reference motherboard layout

The reference helper passed **70 checks** against both saved adapter boards and current STEP exports. It reverified the external A4000 replica board's SHA-256 and current adapter-to-print alignment. Historic copper-screen findings are retained rather than re-extracted; this limited scope is stated in the [reference report](../verification/motherboard-reference-fit.md).

The base and cover retain a nominal 0.201332 mm gap to the neighbouring connector's reference drill cylinder; the unchanged PCB outline has 0.627944 mm. The square corner overlaps the reference ground land in plan by about 0.205068 mm. A drill cylinder is not a measured lug, solder fillet or housing, so this does not establish physical clearance. The original motherboard holes must not be enlarged.

The recorded bare Ø7 mm screw-head projection overlaps unrelated copper in the reference layout. Keep the Ø8 × 0.50 mm underside insulating washers and deliberate J4-to-motherboard shell-ground wire, independently of mounting-bolt contact. Washers span 52.27 mm overall, slightly wider than the 52 mm print. Actual case, component and wire clearance still require measurement.

## Reproduction and visual review

Commands run successfully from the repository root:

```sh
python3 source/build_mechanical.py
python3 source/verify_mechanical.py
python3 source/verify_pcb.py
python3 source/verify_reference_fit.py --reference-board /path/to/a4000-replica.kicad_pcb
python3 source/render_previews.py
python3 source/make_drawings.py
python3 -m py_compile source/*.py
```

Rendering ran under a locally extracted Xvfb server, started in the same process environment with `DISPLAY=127.0.0.1:104`. The normal headless invocation is `xvfb-run -a python3 source/render_previews.py`. An initial audit started before the STEP exports existed; it was rerun successfully after the build. Initial display setup attempts failed; the final six views rendered successfully. Tool versions are recorded in `verification/tool-versions.json`.

All six assembly/part previews and all five rendered A4 drawing pages were visually inspected. They show delivered print geometry; bought-part reference meshes remain illustrative and unchanged. The PDF's pin templates retain their 1:1 vector scale and 50 mm scale check. The five-page drawing pack is mechanical revision 0.6 with PCB revision 0.5.

The revision audit records repository integrity, relative-link checks and BOM parsing. The SHA-256 manifest covers current repository file bytes and excludes itself; it is an integrity record, not additional engineering validation.

## Next physical trial

Print the chamfered hole coupon first, record layer height/material/nozzle, and establish pin fit and hand-clearing allowance. Print the new base and roof-down cover. Dry-fit using the PCB beneath the top nuts, measure full thread engagement and check the cover without forcing it. Verify jackpost-nut retention with the cover absent. Complete soldering, continuity, isolation and wire inspections before optional glue attachment. Record results in [MEASUREMENTS.md](MEASUREMENTS.md).

Purchased connector dimensions, flange bearing, neighbour/chassis clearance, insertion strength, print heat behaviour, adhesive durability and controlled Amiga operation remain unverified.
