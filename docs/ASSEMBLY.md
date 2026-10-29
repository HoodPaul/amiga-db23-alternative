# Trial assembly guide

Assembly and mechanical revision 0.4 uses a solid printed cradle and the unchanged revision 0.3 male RGB or female floppy PCB. The build order matters: the connector cups and any underside wiring must be soldered before the PCB is lowered into the holder.

Complete the measurement worksheet and begin with an unpowered fit trial. Check the actual connector, pins, nuts, jackposts and mounting hardware. Print the hole-fit coupon first, followed by the holder, pin-height loading jig, two required 0.60 mm anchor shims and two optional nut caps. Confirm printed hole and pocket fit before soldering. Do not use an Amiga motherboard as the pin-setting fixture.

## Part 1: join the DB23 and PCB

1. Identify the mating-face pin numbers on the actual DB23 and compare them with the chosen PCB. Male and female numbering is mirrored; use the matching variant.
2. Check the measured cup gap, overlap and rear insulator clearance. Support the connector and PCB in a heat-safe fixture, with the PCB horizontal between the cup rows. Do not force the cups apart to accommodate the assumed 1.00 mm board thickness.
3. Tack one cup on each side, check alignment and solder all 23 cups to their corresponding pads on both PCB faces. Complete these joints away from the printed holder.
4. Prepare the separate shell-ground leads or metal straps. Pre-solder any PCB underside joints that will be covered after lowering, then route them through the holder's local relief. Leave the motherboard end free for final installation. Check the actual lead insulation and solder fillets clear the plastic.
5. Inspect for cup bridges and check pin-to-pad mapping before enclosing the underside. Do not fit the jackpost nuts, hex jackposts or caps yet.

## Part 2: load the pins and lower the joined assembly

1. Select or cut 23 straight pins to the tested common length. The nominal length is 10.70 mm, extending from z = -3.20 mm to +7.50 mm in the assembly frame. Check actual motherboard thickness and solder protrusion before accepting that length. Remove the plastic carrier if recovering pins from ordinary 0.1-inch header stock.
2. Place the printed holder on its separate pin-height loading jig. Confirm it seats on the intended locating/support faces and the common pin well is unobstructed.
3. Insert each pin through the holder until its lower tip reaches the jig stop. Use controlled pressure on one pin at a time. The jig establishes equal lower projection; equal pin lengths establish equal tops. Do not force a 0.64 mm square pin into a finished 0.80 mm round bore.
4. Check the full 23-pin grid for straightness and equal height. Lift the loaded holder off the pin-height jig and support it in a separate heat-safe fixture. Recheck all upper and lower pin heights. The guide fit must retain the pins during this transfer; adjust the tested bore fit if pins slide, rather than soldering over the printed jig.
5. **Preload the two motherboard anchor bolts into their recessed seats now, before lowering the PCB.** The raised lugs surround low head seats, and the PCB partly covers the bolt heads once installed. Keep the bolts retained and their shanks clear of the work surface. The motherboard-side nuts are fitted in Part 4. This is separate from the jackpost nuts fitted in Part 3.
6. Lower the joined **PCB and DB23 together from above**, feeding all pins through their corresponding plated holes. Seat the PCB on the holder's shoulders and rear support; do not use solder to pull a misaligned PCB down. Check pre-soldered underside fillets lie within the shallow relief pockets and shell leads emerge from the PCB top.
7. Retain the PCB against its seats, tack two widely separated pin tops, check full seating and alignment again, then solder the tops of all 23 pins. The guide remains below the board with a deliberate gap for underside fillets and heat separation. Monitor for softening or movement of the print.

The height jig is a loading aid, not a soldering fixture or part of the final installation. It does not compensate for unequal pin lengths, printer error or a tilted holder.

## Part 3: fit the nuts, hex jackposts and optional caps

Before tightening the jackposts, check the actual flange-to-cradle bearing fit. The reference model leaves 0.15 mm between the assumed flange back and holder front; this is not a specified shim thickness. Measure the real gap and fit suitable firm shims/spacers if required, or adjust the cradle face. Confirm the flange bears against the cradle so inserting a monitor plug does not bend the solder cups or signal tails. Do not pull an unsupported flange across a gap by tightening the hardware.

1. Insert the two selected nuts from above into the captive pockets.
2. Fit the hex jackposts through the connector flange and thread them into the nuts. Confirm the cable-facing thread and rear mounting thread separately. The prototype assumes 4-40 UNC cable-facing threads with M3 rear stems and matching M3 nuts.
3. Check the rear stem ends and the motherboard anchor fasteners have the clearance described in the current mechanical notes. Select or trim the actual hardware only after measurement. Do not overtighten against printed material.
4. Fit the optional caps if used. Check they neither lift the nuts nor obstruct the PCB, connector or mounting tools.
5. Complete and inspect any connector-shell bond that remains accessible here. Captured nuts and printed plastic do not provide shell continuity.

## Check the complete adapter before installation

- Confirm each DB23 contact connects only to its corresponding motherboard tail, for all 23 positions.
- Check for solder bridges between adjacent cups, pads and tails. The adapter must preserve the separate `P01`–`P23` circuits.
- Check the separate shell-ground path and deliberate bonds. Keep the shell circuit separate from signal-ground assumptions; video pin 13 must not be merged with pins 16–20 on the adapter.
- Inspect solder wetting, tail straightness, equal projection, seated PCB faces and clear wire routing.
- Verify the holder, fasteners and connector support cable loads through the original shell-anchor mounting positions. Physical insertion and extraction strength remains to be tested; soldered signal tails alone are not the intended attachment.

## Part 4: attach and solder to the motherboard

1. Check the unpowered target motherboard and case for top and underside clearances. Verify the raised end supports and preloaded anchor hardware do not foul the PCB, neighbouring components or case. Confirm underside nut/tool access before installation; use a different reviewed fastener arrangement if that access is unavailable.
2. Place one required **0.60 mm shim or washer beneath each holder mounting foot**. Insert all 23 pins into the original holes without bending or forcing them. Confirm the flange aligns with the original panel opening.
3. Fit the measured underside nuts or threaded retention hardware to the preloaded anchor bolts and positively secure the holder at the original shell-retention holes. The holder has nominal 3.30 mm clearances for the referenced 3.20 mm motherboard holes; no new motherboard drilling is specified. Do not tighten across an unsupported gap or distort the print.
4. Solder the motherboard tails using a process already tested for printed-part heat tolerance. Complete the intended shell bond to the motherboard's original shell-ground points.
5. Reinspect the soldering, fastener seating, pin alignment and shell continuity. Interpret any installed isolation measurements against the target motherboard schematic: the motherboard can join grounds and other nets internally, so this does not replace the standalone adapter check.
6. After mechanical and electrical inspection, perform a controlled functional test. Record the machine, port, cable or device, fit, insertion behaviour and result in the validation record.
