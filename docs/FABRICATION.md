# Prototype fabrication notes

## Release state

Mechanical/assembly revision 0.6 with unchanged PCB revision 0.5 is a fit prototype for measurement, trial printing and unpowered assembly review. The selected solder-cup connector and fasteners have not been measured. Native CAD and clean DRC do not establish production readiness.

## Proposed PCB settings

| Setting | Current value |
|---|---|
| Variant | Male RGB or female floppy, as required |
| Layers | Two |
| Overall board envelope | 51.20 × 9.00 mm, Y4.00–13.00, with stepped front and mounting ears |
| Finished thickness | 1.00 mm assumed; confirm from the measured cup gap |
| Copper | 1 oz proposed |
| Mask / silkscreen | Black / white proposed |
| Legend, both faces | `Amiga DB23 REV 0.5`; nominal 0.70 mm text height / 0.10 mm stroke |
| Surface finish | ENIG preferred; order choice |
| Signal track / clearance | 0.50 / 0.20 mm nominal |
| Tail finished drill / pad | 1.04 / 1.70 mm |
| J3 mounting finished drill / pad | 3.30 / 6.50 mm |
| J4 shell-wire finished drill / pad | 1.20 / 2.40 mm |

Check that the selected fabricator can reproduce the small 0.70 mm legend and 0.10 mm strokes legibly. The saved-file containment result is recorded in the validation report; printed readability has not been tested.

The J3 lands need exposed, flat bearing surfaces for the top nuts. Keep shell-wire solder on J4 and clear of those bearing surfaces. Cup pads are hand-soldered on both PCB faces; confirm overlap, gap and edge position. No assembly stencil or reflow process is specified.

Keep manufacturing exports under `fabrication/FIT-PROTOTYPE/`, with matching reports and revision information. Regenerate and recheck after any outline, coordinate, thickness, footprint or routing change.

## Printed-part preparation

Start with the hole-fit coupon and actual pins. Establish the nominal bore and any drilling or reaming allowance. The guide entries and coupon have 0.40 mm deep, 45° funnels. Trial nut pockets, the optional cover and jig fit using the actual printer and hardware before assembling the full unit. Hand clearing with a pin vice needs a retention check; hot pressing remains unvalidated.

The solid base uses one broad, coplanar underside at motherboard Z0. **Do not add the old separate 0.60 mm mounting shims or restore the two circular feet.** Check the complete bearing area against actual shell-ground pads, solder joints and neighbouring components. Verify space for the base, cap, rear wire route and underside fastener heads. No new motherboard drilling or countersinking is part of the design. Reference A4000 layout checks identified nearby underside copper; the insulating washers and local front-corner reliefs do not establish clearance on every board revision.

The default mounting hardware is M3 × 12 mm under-head length, with user-listed Ø7 mm, approximately 1 mm thick heads. The default under-head insulating washers are assumed Ø8 × 0.50 mm and the top nuts bear directly on supported J3 lands. Washer, nut and board thicknesses are assumed; measure the real stack before accepting thread engagement and cap clearance. The resulting nominal head bottom is Z−3.10. A top washer is not included and requires a separate stack check. Fourteen or sixteen millimetre screws require trimming or a separately checked cover.

The cap STL is roof-down for printing; the base has a broad, flat Z0 print face and can be placed directly on the bed without the former 0.60 mm underside bridge. Read the mechanical notes for transforms and the 1.60 mm roof / short 1.20 mm rim. No material, printer process, strength or thermal performance has been qualified. The optional cover conceals hardware and can be glued to the tower tops after inspection; fitted jackposts must retain their nuts with the cover absent; the base and through-bolts provide the intended cable-force path. Verify that path with the actual flange, hardware, print orientation and motherboard before relying on it.

## Before an order or release

Measure the connector and hardware, dry-fit the coordinated parts, run native and independent checks, and record outcomes. Keep the actual print settings and measured dimensions with the source so the result can be reproduced.
