# Independent geometry review, v0.4

Reviewed 29 October 2026. **Fit prototype using unmeasured solder-cup connector and hardware envelopes.** The electrical PCBs remain revision 0.3.

The saved STEP and STL files were examined independently of the mechanical builder using `python3 source/verify_mechanical.py`. The saved-file audit passes **117 checks**; detailed outcomes are in [mechanical-audit.json](mechanical-audit.json). CadQuery/OpenCascade provides solid intersections and VTK provides independent STL topology and ray intersections. This review does not import the builder or treat its own success message as proof.

## Raised supports and closed rear structure

The holder STEP is valid and contains one solid, with volume **2,227.065988 mm³**. Its external width remains **52.00 mm**. The end rails now reach the PCB underside plane, **Z5.75**, while the 23-pin guide block remains at **Z4.50**. The former rear opening is filled from **Y12.50 to Y15.60**, up to Z5.75. Two local shield-pad reliefs retain a **3.90 mm** solid floor; they are shallow top recesses rather than access holes through the holder.

Raised rails are stepped outwards to X±18.60 ahead of Y7.10 so they clear the assumed connector rear body. Behind the solder cups, the inner rail edges return to X±17.25 and join the pin block and rear infill. Material probes confirm the inner web, front and rear cheeks, and bearing floor at both original anchor positions. These establish the presence of continuous material, not a load rating or a stress analysis.

## Static fit and assembly paths

Intersections between the actual holder STEP and each of the following return **0 mm³**:

- The shared notched PCB outline at its specified installed height.
- The assumed flange and rear connector body.
- All 23 assumed solder-cup outer envelopes, treated conservatively as full cylinders.
- Both nominal captive nuts.
- Both maximum permitted anchor head and upper washer envelopes, **Ø6.00 × 3.00 mm**, on their recessed seats.

The vertical lowering path of the already joined **PCB and DB23** was checked for every offset from its seated position to **20 mm above it**. The PCB, flange and rear-body sweeps are exact extruded prisms; cup sweeps use conservative solid bounding boxes. All four swept envelopes have **0 mm³** holder intersection. This supports the proposed top-loading sequence within the stated nominal envelopes. It does not check a purchased connector, solder fillet shape, flexible shield wiring, tool handling or pin retention during assembly.

Each nut's **15 mm vertical top-loading sweep** also has 0 mm³ intersection with both the holder and the already seated PCB. Nuts can therefore be loaded after the PCB and DB23 are seated, before fitting jackposts and optional caps, for the assumed nut dimensions.

## Anchor pockets and positive retention

Simply placing anchor heads on the raised Z5.75 surface would collide with the PCB: a Ø6 mm head at X±22.135 reaches inboard to X±19.135, while the board extends to X±20. The revision retains **Z2.40 recessed bearing seats**, giving a maximum head top of **Z5.40** and **0.35 mm nominal clearance below the PCB**.

Each head pocket is **Ø6.40 mm and open outboard**. This removes the thin outer lip that a closed circular counterbore would leave within the unchanged 52 mm width. Both pockets are unobstructed outboard; material remains at their inner webs, fore and aft cheeks, and floors. A straight **Ø4 mm** driver envelope centred on either anchor axis clears the PCB. Actual fastener, driver, washer and underside access require measurement.

Preload the anchor bolts after withdrawing the pin-height jig and before lowering the PCB and DB23. Final motherboard attachment uses the verified underside retention arrangement. Place the required **0.60 mm shims or washers beneath both holder feet** before tightening. The raised outer surfaces do not remove this height-stack requirement. Cable load must pass through a properly clamped connector flange, holder and positive motherboard attachment. The assumed 0.15 mm flange-to-holder gap needs a real bearing and clamping check; solder joints and signal pins must not be forced to close an unverified gap.

## Pin support and height jig

All **23 guide bores** are open through the saved holder STEP. The nominal gap from the guide-block top to PCB underside is **1.25 mm**. This preserves space for underside solder fillets and thermal separation; neither actual fillet clearance nor soldering temperature has been tested.

The loading-jig STEP is valid and contains one solid. Restoring its assembly offset of **−6.20 mm** gives 0 mm³ overlap with the holder and with all 23 assumed square pins. Independent VTK rays through the delivered jig STL confirm:

| Datum | Actual saved geometry |
|---|---:|
| All 23 lower pin-tip stops | Z−3.20 mm |
| Holder support surfaces | Z+0.60 mm |
| Both locating-peg tops | Z+1.80 mm |
| Assumed equal pin length | 10.70 mm |
| Corresponding upper pin tips | Z+7.50 mm |

The jig sets the common lower-tip level when the holder is seated on its supports and the stop is clean and flat. Equal upper-tip heights additionally require measured equal-length pins. The jig is for loading and must be removed before soldering and before inserting the anchor bolts. The guide fit must hold the pins at their set height after jig removal, while loading the bolts and lowering the PCB. Nominal CAD clearance does not establish that retention.

A 0.64 mm square pin has a 0.9051 mm diagonal. The nominal Ø0.92 mm guide is only 0.0149 mm larger across that diagonal; printer compensation and the supplied hole coupon must determine the actual fit. A finished Ø0.80 mm round hole does not clear the assumed square pin.

## Independent STL topology checks

VTK boundary-edge, non-manifold-edge and connected-region checks on the delivered files give:

| Part | Triangles | Boundary/non-manifold edges | Connected regions |
|---|---:|---:|---:|
| Holder | 8,052 | 0 | 1 |
| Hole-fit coupon | 23,488 | 0 | 1 |
| Nut keeper | 28 | 0 | 1 |
| Anchor shim pair | 1,024 | 0 | 2, intentional |
| Single anchor shim | 512 | 0 | 1 |
| Pin-height loading jig | 556 | 0 | 1 |

These checks establish closed printable geometry and the CAD clearances stated above. They do not establish physical fit, print accuracy, pin retention, strength under monitor insertion or extraction, heat tolerance, shell continuity, case fit or operation on an Amiga. The new material arrangement is a geometric strengthening proposal awaiting physical tests.
