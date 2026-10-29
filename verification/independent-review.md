# Independent geometry review, revision 0.5

Reviewed 29 October 2026. **Fit prototype using unmeasured solder-cup connector, hardware and printed-fit assumptions.** Both electrical PCB variants are now revision 0.5.

The delivered STEP and STL files were examined with `python3 source/verify_mechanical.py`. The audit reads saved files without importing the mechanical builder and passes **176 checks**. Detailed results are in [mechanical-audit.json](mechanical-audit.json). CadQuery/OpenCascade supplies solid intersections; VTK independently checks STL topology, print transforms and loading-jig stop surfaces. A separate [native-board/reference comparison](motherboard-reference-fit.md) records **68 checks** against the saved male/female KiCad boards and delivered base STEP.

## Solid base and shorter PCB

The holder STEP is valid and contains one solid of **1,787.389466 mm³**. It retains a maximum **52.00 mm width**, ends at **Y13.00**, and supports the adapter PCB underside at **Z5.75**. Two integral feet reach the motherboard datum at **Z0**. The remainder retains nominal **Z0.60** underside clearance; there are no separate anchor shims.

The new PCB has a 16-vertex outline, **51.20 mm maximum width**, front **Y4.00** and rear **Y13.00**. Its mounting ears align with the nominal original shell-anchor positions, **X±22.135, Y9.50**. Its own J3 drills are **3.30 mm**, distinct from the **3.20 mm nominal motherboard** drawing value. No original motherboard hole enlargement is specified. Dedicated J4 shell-bond holes are **X±18.00, Y7.00**.

The PCB outer ears are relieved to X±25.00 from Y6.00–7.50. Matching base and cap reliefs reduce their outer edges to X±25.00 from Y4.40–7.50. These avoid the unrelieved rectangular projection over the neighbouring CN175 mounting-lug region in the separate reference model. That model's actual lug, solder fillet, component housing and chassis dimensions remain unverified; see the restricted scope below.

The 23-pin guide top remains **Z4.50**, providing **1.25 mm nominal clearance** beneath the PCB. All 23 delivered guide bores are open, and the assumed square pin envelopes clear the base. J4 underside reliefs clear conservative **Ø2.40 × 0.75 mm** fillet envelopes and their complete 20 mm vertical lowering sweeps. These assumed fillets do not replace inspection of actual solder joints.

## Joined DB23/PCB assembly path

The saved base has **zero intersection volume** with the PCB, assumed flange, assumed rear connector body and all 23 full solder-cup outer-cylinder envelopes. The PCB model uses the final outline and all signal, mounting and J4 drills.

The path of the already joined DB23 and PCB was checked from the seated position to **20 mm above it**. Exact prismatic sweeps were used for the PCB, flange and rear body; conservative bounding-box sweeps were used for the cups. Every swept envelope has **0 mm³** intersection with the base. Both jackpost nuts also clear the base and already-seated PCB over exact **15 mm vertical loading sweeps**. This supports the documented top-loading assembly order within the stated assumptions.

The assumed flange back at Y0.50 and holder front at Y0.65 retain a nominal **0.15 mm gap**. Actual bearing and clamping need measurement and a suitable measured spacer or revised face where necessary. Cable load must reach the base and mounting bolts without forcing the solder cups or signal pins to close an unverified gap.

## Upward mounting screws and insulation

The saved geometry clears nominal **M3 × 12 mm under-head** mounting screws, **Ø7.00 × 1.00 mm** heads and the specified underside insulating washers, **Ø8.00 / Ø3.20 × 0.50 mm**. The default top nut bears directly on the supported PCB mounting land; no top washer is included.

| Stack item | Assumed thickness |
|---|---:|
| Insulating washer beneath motherboard | 0.50 mm |
| Motherboard | 1.60 mm |
| Motherboard top to adapter PCB underside | 5.75 mm |
| Adapter PCB | 1.00 mm |
| Top washer, default | 0.00 mm |
| M3 nut | 2.40 mm |
| **Under-head seat to nut top** | **11.25 mm** |

The default 12 mm screw tip is at **Z9.90**, the nut top at **Z9.15**, leaving **0.75 mm nominal thread projection**. Head plus insulation projects **1.50 mm below the motherboard underside**, with its bottom at Z−3.10. Actual board thickness, hardware tolerances, nut engagement and chassis clearance require checking.

Solid tests give zero intersection between the default fasteners, base, PCB and seated cap. Material probes confirm PCB support and the integral feet around the mounting axes. The right foot intentionally has a ground-wire exit through part of its outboard side; it is not an uninterrupted bearing annulus. The nominal mounting bores are clear through the saved base STEP.

**Untrimmed longer screws are unsupported by this cap:**

| Under-head length | Tip Z | Cap intersection per screw |
|---|---:|---:|
| 14.00 mm | 11.90 mm | 6.361725 mm³ |
| 16.00 mm | 13.90 mm | 8.482300 mm³ |

These intersections are recorded as unsupported hardware options, not silently treated as passing designs. Trim to a measured suitable length or revise and re-check the cap. Adding an optional top washer also needs a fresh engagement check.

The separate motherboard reference screen found a bare Ø7 mm head overlapping a foreign bottom-copper track in plan at one CN450 anchor. Revision 0.5 therefore requires the insulating washers. The audit checks their nominal geometric coverage, not actual dielectric quality, solder-mask condition or hardware fit. Do not rely on the insulated screw-head bearing face to provide grounding.

## Jackpost threads and deliberate ground bonds

The horizontal clearance passage extends to **Y6.20**. The tested maximum M3 jackpost stem end is **Y6.00**, measured from the flange reference, with **Y4.80 preferred**. Saved-base, PCB, cap, vertical mounting shank and top-nut intersections with that stem envelope are all zero. Conservative circular envelopes enclosing every rotation of the top nuts also clear both the cap and maximum stem. An arbitrary longer jackpost is not a drop-in part; the top mounting hardware still limits the available space.

The dedicated J4 points leave the mounting-nut lands clear for flat seating. Small top-lead clearance probes clear the cap. A continuous rectangular core probe passes through the right foot's outboard grounding-wire exit. Actual insulated-wire diameter and solder-fillets must fit without lifting the foot. Pre-tack the motherboard shell-ground lead with the base removed, route it through the exit and make the deliberate J4/shell bonds. No continuity or contact-resistance test has been performed.

## Clip-on cap

The cap STEP is valid, one solid of **981.284000 mm³**, with roof underside **Z11.00**, roof top **Z12.20**, and rear **Y13.20**. It has zero seated overlap with the base, PCB, assumed connector, 23 square pins, default mounting hardware and captive jackpost nuts. Actual STEP material probes confirm both retaining hooks, their relieved seated positions, the base catch ceilings and the nut-retaining keys.

The inboard latches have **0.20 mm nominal retaining bite**. A conservative **0.25 mm rearward-motion envelope** gives 0.05 mm tip clearance at the tower rear. That envelope clears the PCB because the latch bottoms are at **Z7.20**, **0.45 mm above the PCB top**. It may overlap the PCB's plan projection, but has zero three-dimensional intersection. These checks do not calculate material strain, insertion force, fatigue or creep. Print the two clip-fit trial parts before committing to the complete cap, and do not force a tight print.

The cap STL is exported roof-down: rotate 180° around X and translate +12.20 mm in Z to restore its assembly position. Applying that inverse transform to the actual STL bounds agrees with the STEP bounds within 0.002 mm. The cap is a cosmetic cover and jackpost-nut retainer; it is not the primary cable-load attachment.

## Pin-height loading jig

The jig STEP is valid and one solid. Restoring its print offset by translating **−6.20 mm in Z** gives no overlap with the base or any of the 23 assumed square pins. Independent VTK ray intersections with the delivered STL confirm all **23 lower-tip stops at Z−3.20**, foot supports at **Z0.00**, and locator tops at **Z1.20**.

Equal **10.70 mm** pins then have upper tips at **Z7.50**. Equal lower projection depends on clean stops and seated feet; equal tops also require equal pin lengths. The tested guide fit must retain the pins after removing the jig. Remove the jig before soldering.

## Independent STL topology

| Delivered printable part | Triangles | Boundary/non-manifold edges | Connected regions |
|---|---:|---:|---:|
| Base | 8,324 | 0 | 1 |
| Cap, roof-down | 220 | 0 | 1 |
| Pin-height jig | 1,036 | 0 | 1 |
| Hole-fit coupon | 26,384 | 0 | 1 |
| Clip-fit base trial | 28 | 0 | 1 |
| Clip-fit cap trial | 40 | 0 | 1 |

## Reference-board and physical limits

The separate [reference comparison](motherboard-reference-fit.md) records exact source identity and its limited two-dimensional/cylinder checks. It found small mounting-coordinate differences from the sourced iComp nominal pattern. The final base and cap clear a cylinder having the neighbouring CN175 reference drill diameter by **0.422571 mm**; the adapter outline clears it by **0.627944 mm**. That cylinder is not a measured metal lug or housing, and the base/cap corner is only **0.016171 mm** from the copper-pad circle in plan. Physical neighbouring-part clearance remains unverified.

These saved-file checks establish the CAD consistency stated here. They do not establish purchased-part compatibility, printing accuracy, latch life, pin retention, soldering heat tolerance, clamping torque, cable insertion strength, electrical continuity, chassis fit or operation on an Amiga. The target motherboard and actual hardware must be measured and trial-fitted before a production release.
