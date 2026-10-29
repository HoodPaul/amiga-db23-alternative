# Mechanical design and print notes

## Arrangement

The PCB sits horizontally between the solder-cup rows. Its signal tails pass down through a printed guide block to the original motherboard holes. Revision 0.4 replaces the low side rails and rear opening with raised end supports and a continuous rear infill, joined to the pin guide as one substantial printed cradle. The end supports and rear infill reach the PCB seating plane at z = 5.75 mm. The pin guide itself stops at z = 4.50 mm, leaving a 1.25 mm gap beneath the PCB for fillets and heat separation. Front side clearances preserve the assumed connector-body and solder-cup envelope.

The holder must be positively attached at the original shell retention positions. A close fit or locating peg alone is not the intended means of resisting cable insertion, extraction or overturning force.

Check that the actual connector flange bears firmly against the cradle when the jackposts are secured. The illustrative flange back is at y = 0.50 mm and the cradle front at y = 0.65 mm, leaving a nominal 0.15 mm gap. This is an unmeasured clearance, not an established bearing fit. Measure the real gap and, if needed, fit firm bearing shims or spacers of the measured thickness, or revise the cradle contact face. Do not specify 0.15 mm as a fixed shim thickness. The fitted arrangement must transfer monitor-plug insertion force from the flange into the cradle and its motherboard anchors without bending the solder cups, PCB joints or signal tails. Check that clamping does not shift the mating face or obstruct the contacts, and record the fit before load testing.

## Shared reference frame

All dimensions are millimetres. The flange front reference plane is y = 0; positive y points into the machine. The illustrative metal flange occupies y = 0–0.50 mm, and the holder starts behind it at y = 0.65 mm. The motherboard top is z = 0. The PCB occupies x = ±20 mm, y = 4–16 mm and z = 5.75–6.75 mm. The mating centreline is nominally z = 6.25 mm.

The PCB has two 2.00 × 1.50 mm front-corner notches to clear the nut towers. A plain rectangular 40 × 12 mm board would interfere with the holder. Preserve these clearances when editing the outline.

Pins 13–23 form the front row at y = 8.08 mm. Pins 1–12 form the rear row at y = 10.92 mm. Both variants use the same geometric hole set, with mirrored numbering. Original shell anchors are x = ±22.135 mm, y = 9.50 mm.

## Pins and hole fit

The holder uses 0.92 mm nominal guide bores as a trial value for assumed 0.64 mm square pins. The square diagonal is `0.64 × sqrt(2) = 0.9051 mm`. Printed hole size, corner contact and interference are process-dependent; the nominal CAD bore is not a guaranteed press fit.

Print the hole coupon first. Record the pin section, as-printed bore, drilled or reamed diameter and resulting fit. A 0.80 mm drill can serve for a pilot or smaller round pins, but cannot produce clearance for the assumed square pin. Do not force pins through an undersized holder or motherboard hole.

The nominal pin extends from z = -3.20 mm to +7.50 mm, a 10.70 mm length. This assumes a 1.60 mm motherboard and leaves about 1.60 mm below its underside. Actual motherboard thickness, pin length, case clearance and required soldering protrusion determine the final cut length.

The pin block ends below the adapter PCB to leave fillet and heat clearance. The rear is filled from y = 12.50 mm to 15.60 mm up to the PCB seating plane. Two local J3 underside-filleting pockets remain: x = ±18.00 mm with 4.40 mm width, y = 11.80–14.80 mm, and floor z = 4.50 mm. These are shallow top recesses, not the former through openings. Pre-solder covered underside joints before lowering the PCB and route shell leads from its top. Check actual fillets and insulation against the recesses. Do not fill the guide gap with adhesive or extend the block against solder fillets without checking access and temperature behaviour.

### Pin-height loading jig

The separate [pin-height jig](../mechanical/DB23_Pin_Height_Jig_v0.4.stl) supports the holder at z = 0.60 mm and provides a common lower-tip stop at z = -3.20 mm. Short nominal 2.90 mm loose locating pegs use the holder's anchor holes during loading. Equal 10.70 mm pins then reach z = +7.50 mm; the jig does not correct unequal pin lengths or pin-tip geometry. Its open common well accommodates the pin grid without requiring another set of tight guide holes.

The jig is exported on the print bed at z = 0; its assembly placement is a -6.20 mm z translation. Remove it after loading, before preloading anchor bolts, lowering the PCB or applying soldering heat. Recheck that the guide fit retains the pins and their heights after transfer to a heat-safe support. The jig is not installed on the motherboard.

## Nuts and jackposts

The DB23 screw-lock interface needs the correct cable-facing thread. Original-style hardware uses 4-40 UNC there. The purchased jackpost's rear mounting stem may use a different thread. Choose the hardware before selecting the captive nut and pocket size.

Current pocket assumptions are for M3 nuts: 5.50 mm across flats and 2.40 mm nut thickness, with clearance. HARTING 09670009924, with an M3 male rear stem and 4-40 UNC cable-facing female thread, is a candidate jackpost. These are not frozen purchase specifications. Check that the keeper, nut and jackpost do not contact the PCB, cups, neighbouring connectors or chassis.

For the default frame, the nut pocket occupies y = 1.70–4.30 mm, centred at y = 3.00 mm, and the jackpost rear stem must end at y ≤ 5.50 mm from the flange front reference, preferably around 4.80 mm. A long stem can collide with the motherboard anchor bolt. Select or trim the stem only after measuring the actual flange and hardware; an 8 mm jackpost is not a specified drop-in part.

The original mounting-hole positions are retained in the holder. Its nominal 3.30 mm clearance bore is larger than the referenced 3.20 mm motherboard hole; this is an allowance in the printed part only, not an instruction to drill the motherboard.

The holder bottom is z = 0.60 mm above the motherboard top. Place one **0.60 mm shim or washer under each anchor foot** before tightening. These supports are part of the height stack; tightening without them would pull the feet down across a gap and change alignment or strain the assembly.

The end lugs now reach z = 5.75 mm, but the anchor-head seats remain recessed at z = 2.40 mm. Nominal 6.40 mm counterbores open towards the outer ends, avoiding a thin unsupported outer lip. The default head plus any upper washer stack must be no taller than 3.00 mm and no wider than 6.00 mm, keeping its top at or below z = 5.40 mm beneath the assumed PCB lower face. A raised head on the lug top would collide with the PCB edge.

Preload the two anchor bolts after removing the pin-height jig and **before lowering the joined PCB/DB23**, because the PCB partly covers their heads. Fit their motherboard-side nuts during final installation. Confirm underside nut and tool access, bolt retention during assembly, and the complete stack against the actual motherboard and chassis. The recessed heads are distinct from the cable jackposts and their captive nuts.

## Printing and assembly temperature

Print only the coupon and trial parts until geometry is confirmed. Select material and print orientation from actual mechanical and soldering trials. No material, layer height, thermal rating or retention force has been validated by this project.

Place the holder's broad planar bottom on the print bed. Its STL retains the assembly-coordinate bottom at z = 0.60 mm, so use the slicer's drop-to-bed function. The coupon and shims already sit at z = 0. The keeper STL is exported cap-face down for printing; its print orientation differs from its assembly orientation. The [mechanical notes](../mechanical/MECHANICAL_NOTES.txt) give the assembly transforms and support guidance.

The [shim-pair STL](../mechanical/DB23_Anchor_Shims_v0.4.stl) deliberately contains two separate printable shims. Alternatively, print the [single-shim STL](../mechanical/DB23_Anchor_Shim_Single_v0.4.stl) twice. The holder, coupon and individual keeper are each intended to be one connected part.

Keep support removal and drilling debris out of the electrical assembly. The holder is not specified as reflow-rated. Soldering heat can travel along the pins and soften a printed guide even when the iron does not touch it. Assemble or solder away from the holder where practical, test the actual process on the coupon, and avoid unnecessary heat dwell.

## Shell grounding

Printed material is insulating. Capturing a nut does not by itself connect the connector shell to motherboard shield ground. Provide deliberate wire or metal bonds and inspect their continuity after mechanical assembly. Keep this circuit distinct from assumptions about the 23 signal contacts.

## Regeneration

Run from the project root:

```sh
python3 source/build_mechanical.py
```

The builder reads `source/design_parameters.json` and produces the OpenSCAD source and printable parts. OpenSCAD is required for STL export; any optional STEP export requires the additional CAD dependencies identified by the builder. Keep the source and all generated outputs together after parameter changes.

