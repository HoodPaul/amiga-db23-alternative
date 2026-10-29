# Mechanical design and print notes

## Arrangement

The PCB sits horizontally between the solder-cup rows. Its signal tails pass down through a printed guide block to the original motherboard holes. The holder's front cradle supports the DB23 flange and nut pockets; side and rear structure links this cradle to the pin block and PCB shoulders.

The holder must be positively attached at the original shell retention positions. A close fit or locating peg alone is not the intended means of resisting cable insertion, extraction or overturning force.

## Shared reference frame

All dimensions are millimetres. The flange front reference plane is y = 0; positive y points into the machine. The illustrative metal flange occupies y = 0–0.50 mm, and the holder starts behind it at y = 0.65 mm. The motherboard top is z = 0. The PCB occupies x = ±20 mm, y = 4–16 mm and z = 5.75–6.75 mm. The mating centreline is nominally z = 6.25 mm.

The PCB has two 2.00 × 1.50 mm front-corner notches to clear the nut towers. A plain rectangular 40 × 12 mm board would interfere with the holder. Preserve these clearances when editing the outline.

Pins 13–23 form the front row at y = 8.08 mm. Pins 1–12 form the rear row at y = 10.92 mm. Both variants use the same geometric hole set, with mirrored numbering. Original shell anchors are x = ±22.135 mm, y = 9.50 mm.

## Pins and hole fit

The holder uses 0.92 mm nominal guide bores as a trial value for assumed 0.64 mm square pins. The square diagonal is `0.64 × sqrt(2) = 0.9051 mm`. Printed hole size, corner contact and interference are process-dependent; the nominal CAD bore is not a guaranteed press fit.

Print the hole coupon first. Record the pin section, as-printed bore, drilled or reamed diameter and resulting fit. A 0.80 mm drill can serve for a pilot or smaller round pins, but cannot produce clearance for the assumed square pin. Do not force pins through an undersized holder or motherboard hole.

The nominal pin extends from z = -3.20 mm to +7.50 mm, a 10.70 mm length. This assumes a 1.60 mm motherboard and leaves about 1.60 mm below its underside. Actual motherboard thickness, pin length, case clearance and required soldering protrusion determine the final cut length.

The pin block ends below the adapter PCB to leave solder access and heat separation. Do not fill this gap with adhesive or extend the block against solder fillets without checking access and temperature behaviour.

## Nuts and jackposts

The DB23 screw-lock interface needs the correct cable-facing thread. Original-style hardware uses 4-40 UNC there. The purchased jackpost's rear mounting stem may use a different thread. Choose the hardware before selecting the captive nut and pocket size.

Current pocket assumptions are for M3 nuts: 5.50 mm across flats and 2.40 mm nut thickness, with clearance. HARTING 09670009924, with an M3 male rear stem and 4-40 UNC cable-facing female thread, is a candidate jackpost. These are not frozen purchase specifications. Check that the keeper, nut and jackpost do not contact the PCB, cups, neighbouring connectors or chassis.

For the default frame, the nut pocket occupies y = 1.70–4.30 mm, centred at y = 3.00 mm, and the jackpost rear stem must end at y ≤ 5.50 mm from the flange front reference, preferably around 4.80 mm. A long stem can collide with the motherboard anchor bolt. Select or trim the stem only after measuring the actual flange and hardware; an 8 mm jackpost is not a specified drop-in part.

The original mounting-hole positions are retained in the holder. Its nominal 3.30 mm clearance bore is larger than the referenced 3.20 mm motherboard hole; this is an allowance in the printed part only, not an instruction to drill the motherboard.

The holder bottom is z = 0.60 mm above the motherboard top. Place one **0.60 mm shim or washer under each anchor foot** before tightening. These supports are part of the height stack; tightening without them would pull the feet down across a gap and change alignment or strain the assembly.

The anchor bosses are 2.40 mm high in assembly coordinates. The default model allows a bolt head and any upper washer stack no taller than 3.00 mm and no wider than 6.00 mm. That keeps its top at or below z = 5.40 mm, below the assumed PCB lower face. Verify the complete fastener stack, including the underside of the motherboard.

## Printing and assembly temperature

Print only the coupon and trial parts until geometry is confirmed. Select material and print orientation from actual mechanical and soldering trials. No material, layer height, thermal rating or retention force has been validated by this project.

Place the holder's broad planar bottom on the print bed. Its STL retains the assembly-coordinate bottom at z = 0.60 mm, so use the slicer's drop-to-bed function. The coupon and shims already sit at z = 0. The keeper STL is exported cap-face down for printing; its print orientation differs from its assembly orientation. The [mechanical notes](../mechanical/MECHANICAL_NOTES.txt) give the assembly transforms and support guidance.

The [shim-pair STL](../mechanical/DB23_Anchor_Shims_v0.3.stl) deliberately contains two separate printable shims. Alternatively, print the [single-shim STL](../mechanical/DB23_Anchor_Shim_Single_v0.3.stl) twice. The holder, coupon and individual keeper are each intended to be one connected part.

Keep support removal and drilling debris out of the electrical assembly. The holder is not specified as reflow-rated. Soldering heat can travel along the pins and soften a printed guide even when the iron does not touch it. Assemble or solder away from the holder where practical, test the actual process on the coupon, and avoid unnecessary heat dwell.

## Shell grounding

Printed material is insulating. Capturing a nut does not by itself connect the connector shell to motherboard shield ground. Provide deliberate wire or metal bonds and inspect their continuity after mechanical assembly. Keep this circuit distinct from assumptions about the 23 signal contacts.

## Regeneration

Run from the project root:

```sh
python3 source/build_mechanical.py
```

The builder reads `source/design_parameters.json` and produces the OpenSCAD source and printable parts. OpenSCAD is required for STL export; any optional STEP export requires the additional CAD dependencies identified by the builder. Keep the source and all generated outputs together after parameter changes.

