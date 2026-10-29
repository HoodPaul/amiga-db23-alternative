# Trial assembly guide

This is a fit-prototype workflow. Complete the measurement worksheet and use the matching male RGB or female floppy PCB. Start with an unpowered mechanical trial; do not use an Amiga motherboard as the pin-forming or soldering fixture.

## 1. Confirm the parts and trial fit

1. Record the solder-cup connector, pins, jackposts and nuts in the measurement worksheet.
2. Check the solder-cup gap, opening direction, PCB overlap and insulator depth against the PCB. Change the parameters if required; do not force the cups apart to compensate for an unverified board thickness.
3. Print the hole-fit coupon. Establish a snug but serviceable pin fit using the actual printer and pins.
4. Print the holder and, if used, two nut keepers. Print the supplied shim pair or prepare two 0.60 mm anchor washers. Drop the holder to the slicer's bed; the source STL retains its assembly z offset. Remove supports and debris. Verify nut retention, pin access and the available soldering clearances.
5. Dry-fit the connector and PCB. Confirm the flange position and centreline height. Check that no solder cup overlaps or touches a motherboard tail of another pin.

## 2. Assemble the adapter off the motherboard

1. Identify the mating-face pin numbers on the actual DB23 and compare them with the chosen PCB. The male and female variants are mirrored.
2. Support the solder-cup connector and PCB in a suitable jig. Tack one cup on each side, confirm alignment, then complete the cup joints. Keep heat away from printed material where practical.
3. Cut or select 23 straight pins to the tested length. Remove the old header carrier if recovering pins from a 0.1-inch strip.
4. Load the pins into the printed guide or a separate trial jig. Set both upper and lower protrusion consistently. Check for straightness before placing the PCB over them.
5. Seat the PCB on its height shoulders. Tack two widely separated tail pins, recheck seating and then solder all 23 tail joints. Verify the printed guide is not softening or distorting during the operation.
6. Fit the connector hardware and nut keepers as applicable. Check the jackpost stems stop before the anchor-bolt space; the default frame requires their ends at y ≤ 5.50 mm from the flange reference. Do not overtighten fasteners against the printed holder.
7. Provide the intended shell-ground wire or metal bonds. Keep wiring clear of the cups and signal pins.

If the preferred soldering sequence cannot be completed without overheating or blocking access, stop and adjust the holder or jig arrangement before proceeding.

## 3. Inspect and check electrically

Perform these checks on the adapter before it is connected to a motherboard:

- Confirm each DB23 contact connects only to its corresponding motherboard tail, for all 23 positions.
- Check for bridges between adjacent cups, pads and tails.
- Check that the independent `P01`–`P23` circuits have not been joined together by the adapter.
- Check the separate shell path and intended ground bonds.
- Inspect solder wetting, tail straightness and exposed pin length.

The motherboard can join some signal grounds and other nets internally. An isolation result measured after installation does not replace the standalone adapter check and should be interpreted against the target schematic.

## 4. Fit to the target machine

1. Check the unpowered motherboard and case for clearance, including the underside retention hardware.
2. Insert all pins without bending or forcing them. Confirm the connector flange aligns with the original rear-panel opening and cable plug.
3. Place one 0.60 mm shim or washer beneath each holder mounting foot, then secure it through the original shell retention positions using the verified fastener stack. For the default model, the head plus upper washers must fit within 3.00 mm height and 6.00 mm diameter. Do not tighten across an unsupported gap. No new motherboard holes are part of this design.
4. Solder the motherboard tails with an assembly process that has been checked for printed-part heat tolerance.
5. Reinspect soldering and confirm the original shell-ground connection.
6. Only after inspection and electrical checks should a controlled functional test be performed. Record the machine, port, attached device and outcome in the validation record.

