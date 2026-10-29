# Trial assembly guide

Revision 0.5 uses the matching male RGB or female floppy PCB, a solid printed base and a keyed clip-on cap. Two M3 screws pass **upwards from beneath the motherboard**, through the base and plated PCB mounting lands, with insulating washers beneath the heads and nuts directly on the top J3 lands. The cap is fitted last.

Complete the [measurement worksheet](MEASUREMENTS.md) before accepting the geometry. Print the hole coupon first, then trial the base, cap and pin-height jig with the actual pins and hardware. Begin with an unpowered fit check; an Amiga motherboard is not a pin-setting fixture.

## Part 1: join the DB23 and PCB

1. Identify the actual DB23 pin numbers and use the matching PCB. Male and female numbering is mirrored.
2. Check the measured cup gap, overlap, rear insulator and flange position. Support the connector and PCB in a heat-safe fixture. Do not force the cups apart to accommodate the assumed 1.00 mm PCB.
3. Tack one cup on each side, check alignment and solder all 23 cups to their corresponding top and bottom pads. Complete this work away from the print.
4. Prepare the connector-shell bond and the required motherboard shell-ground wire at the dedicated J4 pads. Keep wire and solder off the J3 mounting lands, where the mounting nuts must seat flat. Pre-solder any covered underside joints and route the wire through the intended local relief, clear of signal pins.
5. Inspect both faces for bridges and confirm contact-to-pad mapping before the underside becomes enclosed. Leave the cap off.

## Part 2: load the pins and lower the joined assembly

1. Select or cut 23 straight pins to equal tested lengths. The nominal 10.70 mm length spans Z−3.20 to Z+7.50. Actual motherboard thickness, solder protrusion and clearance determine the final length. Remove the plastic carrier if recovering pins from ordinary 0.1-inch header stock.
2. Seat the base on its separate pin-height loading jig. Check the support faces, locating features and common pin-tip stop are clean.
3. Push each pin gently through its guide until the lower tip reaches the stop. The stop establishes equal lower projection; equal pin lengths establish equal tops. Do not force an assumed 0.64 mm square pin through a finished Ø0.80 mm bore.
4. Check the full grid, lift the loaded base off the jig and place it in a heat-safe support with room for the projecting tails. Recheck all heights. The tested guide fit must retain the pins during transfer.
5. Lower the joined **PCB and DB23 together from above**, feeding the pins through their plated holes. Seat the PCB flat on its support faces and mounting bosses. Verify J4 underside fillets and the shell wire lie in their reliefs.
6. Tack two widely separated pin tops, recheck seating and solder all 23 top joints. The guide remains below the PCB with a deliberate fillet and heat gap. Check the print has not softened or shifted.

The jig is a loading aid. Remove it before soldering; it is not part of the installed assembly. The old recessed anchor-bolt preloading step and loose mounting shims do not apply to revision 0.5.

## Part 3: fit the jackpost nuts and hex posts

1. Load the selected nuts into their top-loading pockets.
2. Fit the hex jackposts through the connector flange and into the nuts. Check the cable-facing and rear mounting threads separately. Prototype defaults assume 4-40 UNC at the cable and M3 rear stems with matching nuts.
3. Check the full rear stem projection against the current passage limit and the upward mounting screw axes. The passage ends at Y6.20 and the conservative stem end limit is Y≤6.00 from the flange datum. An extended passage does not make every stem length compatible.
4. Confirm the flange bears firmly on the printed cradle when secured. The illustrative flange and cradle have an unmeasured nominal gap; measure the actual fit and use a firm spacer or revise the bearing face if required. Do not pull a gap closed by bending cups, PCB joints or tails.
5. Check the separate shell bond. Leave the cap off for mounting and inspection.

## Check the complete adapter before installation

- Verify each DB23 contact connects only to its matching motherboard tail, for all 23 positions.
- Check for bridges between adjacent cups, pads and tails, and retain the separate `P01`–`P23` circuits.
- Confirm J3 mounting lands and J4 shell-bond pads share the separate `SHIELD` circuit, without joining it to any signal pin.
- Inspect solder wetting, straight tails, equal projection, flat seating and wire clearance.
- Print the matched clip-fit coupons and trial the cap without forcing it. Check latch engagement and release, nut retention and room above the selected mounting hardware. Remove it for installation.

## Part 4: mount, solder and fit the cap

1. With the base removed, pre-tack the required board-ground wire to the selected original motherboard shell-ground pad. The right foot has an outward wire groove; check the actual wire and fillet fit. Inspect the target motherboard's original mounting holes and surrounding ground pads, including both sides. Check neighbouring components, front corner reliefs, rear-panel alignment and underside/chassis space for the assumed Ø7 × 1 mm screw heads plus Ø8 × 0.50 mm insulating washers. The assumed head bottoms are Z−3.10. Reference-layout checks do not prove the user's board revision fits. No motherboard drilling or countersinking is specified.
2. Lower all 23 pins into their original holes without bending or forcing them. Seat the integral mounting feet on their intended bearing points. **Do not fit the old 0.60 mm loose shims:** their thickness is now incorporated in the base.
3. Fit the selected insulating washer beneath each screw head and insert the two M3 screws upward from beneath the motherboard, through the printed bores and J3 PCB mounting holes. Fit the nuts directly on the top J3 lands. Keep each mounting ear flat on its supporting boss and tighten only sufficiently to secure the assembly without bowing the PCB or distorting the print.
4. Verify the complete height stack and thread engagement. Default assumptions are M3 × 12 mm, an underside 0.50 mm insulating washer and a 2.40 mm top nut. The top nut has no default washer. Adding one, or using 14/16 mm screws, requires a separately checked stack and cover or trimming as appropriate. Optional rigid compression stops must match the measured support height and chosen base variant.
5. Solder the motherboard tails with a process already checked for printed-part heat tolerance. Complete the required J4 wire bond to the motherboard's original shell-ground pad, routing it in the base's intended foot relief so it is not pinched. Retain the separate bond to the DB23 metal shell. The default insulating washers prevent reliance on bolt-head contact; verify both deliberate bonds.
6. Inspect all joints, fastener seating, pin alignment and shell continuity. Installed isolation measurements must be interpreted against the motherboard schematic; the motherboard can join nets internally.
7. Fit the keyed clip-on cap after the mounting nuts, jackposts, solder joints and wire routing pass inspection. It retains the jackpost nuts and covers the top hardware; the through-bolts and solid base carry the intended cable loads.
8. Perform and record the controlled functional trial only after these checks. Record motherboard revision, port, cable/device, insertion behaviour and result in [VALIDATION.md](VALIDATION.md).
