# Independent geometry review, v0.3

Reviewed 29 October 2026. Status: **fit prototype using an unmeasured solder-cup connector envelope**.

## Footprint and electrical mapping

The two saved PCB outlines match the shared notched outline. Both 23-pin tail footprint coordinate sets match the holder's 23 guide bores exactly. With the connector facing upwards in a top-of-motherboard view, male pin 1 is at the right of the rear row; female pin 1 is at the left. Pins 13–23 form the front row.

The nominal grid is 2.77 mm along each row, 2.84 mm between rows and 1.385 mm staggered. Anchor centres are X = ±22.135 mm, Y = 9.50 mm, with 3.30 mm holder clearance holes. These holder holes are distinct from the manufacturer's nominal 3.20 mm motherboard anchor holes.

Independent parsing of both exported schematic XML netlists confirms J1 pin *n* connects only to J2 pin *n* for all 23 pins. The two shield strap pads share their own separate net. The supplied native KiCad reports show zero DRC violations, unconnected pads and footprint errors for each board. ERC was not run.

## Mechanical checks

CadQuery/OpenCascade reports a valid holder STEP with one solid. Solid intersections with the holder returned **0 mm³** for each of the following: the notched PCB, assumed rear connector body, assumed flange at Y = 0–0.50 mm, all 23 assumed solder cups and both nominal 5.50 mm AF × 2.40 mm nuts.

The rear PCB ledge supports the specified underside height Z = 5.75 mm. With the 1.00 mm PCB, its mid-plane is Z = 6.25 mm. Relevant nominal clearances are:

| Relationship | Clearance |
|---|---:|
| Assumed flange rear to holder front | 0.15 mm |
| Assumed connector body to inner tower, each side | 0.20 mm |
| Assumed cup ends to pin-guide block | 0.10 mm |
| PCB side edge to lateral stop, each side | 0.25 mm |
| Nut pocket, across flats and thickness | 0.20 mm total in each dimension |

The holder bottom is Z = 0.60 mm. Both 0.60 mm anchor shims are required to support the mounting bosses at the intended height. Omitting them changes the installed geometry when the anchors are tightened.

## Independent STL topology checks

VTK feature-edge and connectivity checks were run on the actual exported STL files.

| Part | Triangles | Boundary/non-manifold edges | Connected regions |
|---|---:|---:|---:|
| Holder | 8,268 | 0 | 1 |
| Hole-fit coupon | 23,488 | 0 | 1 |
| Nut keeper | 28 | 0 | 1 |
| Anchor shim pair | 1,024 | 0 | 2, intentional |
| Single anchor shim | 512 | 0 | 1 |

These checks support closed, connected printable geometry as tabulated. They do not establish physical fit, print accuracy, strength, thermal performance or compatibility with a purchased connector. The 0.92 mm nominal guide bore is only 0.0149 mm larger than the diagonal of a 0.64 mm square pin; the coupon and actual printed parts must determine the finished clearance. Connector, fastener and motherboard measurements remain required before production release.
