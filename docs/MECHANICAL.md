# Mechanical design and print notes

## Solid base and keyed cap

Revision 0.5 uses a solid printed base, a short PCB with mounting ears and two upward metal mounting screws. The separate keyed cap retains the port-jackpost nuts and covers the upper fasteners. Broad supported parts and positive bolts provide the intended load path; no physical strength or print lifetime is established.

The base supports the DB23 flange, the 23-pin guide and the PCB mounting ears. Its integral feet contact the motherboard at the original shell-anchor positions. **The old separate 0.60 mm anchor shims are not used:** that height is incorporated in the feet while preserving the PCB underside at Z5.75.

The PCB and connector are soldered together first, then lowered onto the loaded base from above. The cap is fitted after mounting, soldering and inspection. It does not obstruct the top mounting nuts during installation.

## Coordinates and envelope

All dimensions are millimetres. X runs across the port; positive Y runs inward from flange front Y0; positive Z rises from motherboard top Z0. The connector faces negative Y. Male and female share the same geometric pin set with mirrored numbering.

| Reference | Nominal value |
|---|---|
| PCB overall width / front / rear | 51.20 mm / Y4.00 / Y13.00 |
| Base width / rear | 52.00 mm / Y13.00 |
| Cap width / rear / roof | 52.00 mm / Y13.20 / Z11.00–12.20 |
| Maximum nominal underside washer span | 52.27 mm across both Ø8 washers |
| Head and washer projection beneath motherboard underside | 1.50 mm, assuming 1.00 + 0.50 mm |
| PCB thickness / underside | 1.00 mm / Z5.75 |
| PCB mounting-ear sides | X±25.00 at Y6.00–7.50; X±25.60 behind Y7.50 |
| Original anchor axes | X±22.135, Y9.50 |
| Front / rear signal rows | Y8.08 / Y10.92 |
| Signal pitch / row spacing / stagger | 2.77 / 2.84 / 1.385 |
| Nominal mating centreline | Z6.25 |
| Pin guide top | Z4.50 |
| Guide-to-PCB underside gap | 1.25 mm |

The PCB rear has moved from Y16.00 to Y13.00, 0.50 mm behind the OEM reference rear at Y12.50. The cap reaches Y13.20, 0.70 mm behind that OEM reference. The two Ø8 underside washers span 52.27 mm, slightly wider than the 52.00 mm prints; do not treat the whole assembly as a 52 mm rectangular envelope. Actual wire emerging from the foot and side window also needs clearance. The outer assembly still needs checking with the target motherboard and case: matching the original holes does not establish the same external envelope. Photos around CN450 identify a useful region to inspect, but are not dimensional fit evidence. Use the shared parameters for current base/cap extents and the drawing PDF for views.

The front PCB steps clear the nut towers and assumed connector envelope. Following the marked review, each forward tower now has a flat outer face at X±25.60 from Y0.65 to Y5.10. This adds 0.60 mm at the former rear-corner rebate and trims the formerly wider front by 0.40 mm, removing the stepped thin corner. The matching cap has the same forward profile. The nominal outer nut-pocket wall is 0.615 mm and the rear web 0.80 mm; actual print strength still needs testing.

The remaining neighbour relief is X±25.00 from Y5.10 to Y7.50, behind the towers. The aft base/cap retain their 52.00 mm maximum width. The adapter PCB outline is unchanged by this end-wall amendment. Verify the actual neighbouring lug, fillet and housing: reference-CAD clearance is not a physical fit result. Preserve this shaped outline when changing the ears or shortening the board.

## Mounting stack

Screws pass upward from under the motherboard, through the solid base and J3 holes, with insulating washers under the heads and nuts above the PCB. Each mounting ear must sit flat on its boss before tightening. Do not use nut force to pull a tilted PCB down or close a gap. No motherboard drilling or countersinking is specified.

The default stack is:

| Part | Assumed height |
|---|---:|
| Underside insulating washer | 0.50 mm |
| Motherboard | 1.60 mm |
| Motherboard top to PCB underside | 5.75 mm |
| Adapter PCB | 1.00 mm |
| Top nut | 2.40 mm |
| Total beneath screw head to nut top | 11.25 mm |

The default M3 × 12 mm under-head screw ends at Z9.90 and projects about 0.75 mm beyond the assumed nut. Washer and nut dimensions are not measured. Fourteen and sixteen millimetre screws end at Z11.90 and Z13.90 respectively, and are not automatically compatible with the default cap. Trim only after determining the actual stack or use an independently checked cover.

User-listed screw heads are Ø7 mm and approximately 1 mm thick. Fit default Ø8 × 0.50 mm insulating washers beneath them. The heads then extend to nominal Z−3.10, which is 1.50 mm below the underside of the assumed 1.60 mm motherboard. Check both motherboard faces, nearby tracks/components and chassis space; the reference A4000 layout is not a physical fit result for the user's board. Top nuts seat directly on supported J3 lands. Solder wires to J4, clear of the nut seats. An optional top washer consumes the 0.75 mm spare thread and requires a separate stack review.

Tightening behaviour, plastic compression, creep and long-term preload have not been tested. Optional rigid compression stops can be developed if needed, but must match the measured support height and selected base bore; they are not an unspecified drop-in part. Do not bow the 1.00 mm PCB or crush the print.

## Pins and loading jig

The default guide bore is nominally Ø0.92 mm for assumed 0.64 mm square pins. The pin diagonal is `0.64 × sqrt(2) = 0.9051 mm`. Nominal CAD clearance is not a guaranteed printed press fit. A finished Ø0.80 mm hole is too small for those pins.

Print the hole-fit coupon first. Record pin shape, actual bore, any drill/reamer diameter and retention after soldering trials. The base must hold the pins at their set height when the jig is removed and while the PCB is lowered.

Nominal equal pin length is 10.70 mm, from Z−3.20 to Z7.50. With an assumed 1.60 mm motherboard this leaves about 1.60 mm below its underside. Confirm actual board thickness, solder protrusion and chassis clearance.

The separate jig supports the new integral feet and provides a common lower-tip stop. Equal lower projection requires a seated base and clean flat stop; equal upper heights additionally require equal pin lengths. Remove the jig vertically before soldering, then recheck the guide grip and all heights. Do not use the motherboard as the fixture.

The guide top remains 1.25 mm below the PCB for fillets and heat separation. Local J4 reliefs clear pre-soldered wire joints. Keep the actual fillet and insulation envelope within those recesses and away from signal pins; this is not underside soldering access after seating.

## Jackposts, nuts and flange bearing

Cable-facing jackpost sockets require 4-40 UNC. Their rear mounting stems can use a different thread. The prototype assumes M3 rear stems and nuts, 5.50 mm across flats and 2.40 mm thick, plus fit allowance. Match the actual parts. HARTING 09670009924 is a candidate thread arrangement, not a frozen drop-in part; M3.5 has not been specified.

The cap's retaining tongues close the top-loading jackpost nut pockets. The solid base locates those nuts; do not rely on a decorative latch as the main cable-load attachment.

The rear-stem passage ends at **Y6.20**, with a conservative permitted stem end **Y≤6.00 from the flange datum**. This limit clears the top motherboard mounting nut, not just the vertical bolt shank. Check actual projection, not only the advertised jackpost length; an 8 mm stem is not an assumed drop-in part.

The illustrative connector flange occupies Y0–0.50 and the base starts Y0.65, leaving an unmeasured 0.15 mm reference gap. Check real flange bearing when tightening the jackposts. If needed, use firm spacers selected from the measured gap or revise the bearing face. Do not bend solder cups, PCB joints or tails to pull a gap closed. The flange must transfer cable forces into the base and its mounting attachment.

## Printing, cap fit and temperature

Read `mechanical/MECHANICAL_NOTES.txt` for the complete generated notes. Delivered print trials are:

| File | Use and orientation |
|---|---|
| `DB23_Holder_v0.5.stl` / `.step` | Solid base in assembly coordinates; integral feet at Z0, main underside at Z0.60 |
| `DB23_Cap_v0.5.stl` | Cap already roof-down for printing |
| `DB23_Cap_v0.5.step` | Cap in assembly coordinates |
| `DB23_Pin_Height_Jig_v0.5.stl` / `.step` | Jig on the print bed; translate Z−6.20 for assembly placement |
| `DB23_Hole_Fit_Coupon_v0.5.stl` | Guide-hole trials before the base |
| `DB23_Clip_Fit_Base_v0.5.stl` and `DB23_Clip_Fit_Cap_v0.5.stl` | Matched latch-fit trial before full-size cap |

To restore the cap STL to assembly coordinates, rotate 180° about X, then translate Z+12.20. The base has a stepped underside: printing it on its Z0 feet leaves the main body 0.60 mm above the bed. Use local underside support or a bridging process proven on a trial; do not assume that broad region prints unsupported. The roof-down cap avoids a broad ceiling bridge, but small latch-hook overhangs still need a print trial.

The base, cap and individual jig are intended as connected parts. Reference meshes under `previews/reference-meshes/` illustrate bought components and are not functional print files.

Black print colour is proposed for a discreet appearance. No material, nozzle, process, layer direction or thermal capability has been qualified. The clip coupon has nominal 0.60 mm thick, 1.40 mm wide latch features. Trial the nut pockets, keys, latch travel and release with the actual printer before using the cap; material, fatigue life and latch strength are unvalidated. Do not force a cap that interferes with fasteners or pulls the PCB out of its seats.

Remove support and drilling debris before electrical assembly. The print is not specified as reflow-rated. Soldering heat can soften a guide through the pins even without direct iron contact. Complete cup joints away from the print, keep heat dwell controlled and test the real process on trial parts.

## Shell grounding and regeneration

J3 mounting lands and J4 wire pads share the isolated `SHIELD` circuit. Bond the DB23 metal shell deliberately to J4. A separate wire from J4 to the motherboard's original shell-ground pad is required. The right mounting foot has an outward groove beginning at X24.00, centred on Y9.50, nominally 1.20 mm wide and 1.00 mm high. Pre-tack the motherboard pad wire with the base removed, route it outward through this groove and up to J4, and verify the actual wire/fillet envelope does not lift the foot or become pinched. Do not rely on mounting-bolt contact: the default under-head washers are insulating. Plastic does not provide grounding. Check both deliberate bonds after final mechanical assembly.

From the project root:

```sh
python3 source/build_mechanical.py
python3 source/verify_mechanical.py
```

Keep the shared JSON, editable source, generated STL/STEP, PCB and reports coordinated. Refer to [VALIDATION.md](VALIDATION.md) for actual command results and limits.
