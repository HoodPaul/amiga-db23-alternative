# Prototype fabrication notes

## Release state

Revision 0.3 is a fit prototype. It is intended for measurement, trial printing and unpowered assembly review before a PCB order. The selected solder-cup connector and fastening hardware have not been measured, so native CAD or clean DRC alone does not make this a production release.

## Proposed PCB settings

| Setting | Current value |
|---|---|
| Variant | Male RGB or female floppy, as required |
| Layers | Two |
| Outline | 40.00 × 12.00 mm overall, with two 2.00 × 1.50 mm front-corner notches |
| Finished thickness | 1.00 mm assumed; confirm from cup gap |
| Copper | 1 oz proposed |
| Mask / silkscreen | Black / white proposed |
| Surface finish | ENIG preferred; manufacturer order choice |
| Minimum signal track / clearance | 0.50 / 0.20 mm nominal |
| Tail finished drill / pad | 1.04 / 1.70 mm |
| Shell strap finished drill / pad | 1.20 / 2.40 mm |

The solder-cup pads are hand-soldered to both sides of the board. Confirm the actual overlap, cup spacing and PCB edge position. Do not order an assembly stencil or claim an SMT assembly process without reviewing the intended population method.

If manufacturing exports are generated, keep them in a folder clearly labelled `FIT-PROTOTYPE`, with matching checks and revision information. Regenerate and recheck them after any coordinate, thickness, footprint or routing change.

## Printed-part preparation

Start with the hole-fit coupon and the actual pins. Confirm usable bore size and the drilling or reaming process. Then check nut pockets with the purchased hardware before committing to the full holder.

The holder model's nominal 52 mm width must clear adjacent ports, motherboard components and casework. Its 0.60 mm bottom clearance requires two matching anchor shims or washers beneath the mounting feet before tightening. Check its underside and the retention fasteners against the motherboard and chassis. No new motherboard drilling is specified.

No printer, material, process or strength has been qualified. Retain the editable source and measured fit settings with the printed parts so future builders can reproduce the result.

## Before a release or order

Complete the connector and hardware measurements, dry fit the holder and PCB, run the current native and independent checks, and record results. Keep the generated design, printed files, previews and reports from the same parameter revision together.

