# Reference motherboard fit screen

This is a limited two-dimensional comparison with the locally retained [A4000 replica KiCad board](https://github.com/Acill/A4000RevB/blob/master/Kicad/A4k-Replica-Acill.kicad_pcb). It is not a physical fit result, a clearance certificate or a substitute for measurements of the target motherboard.

The exact source SHA-256, native format version, pad/track locations and numeric results are recorded in [motherboard-reference-fit.json](motherboard-reference-fit.json). The source file is not included in this project. Component bodies, solder fillets, actual screw dimensions, solder-mask condition and chassis surfaces are outside this screen.

## Nominal mounting positions

The reference CN450 RGB and CN352 floppy signal-hole sets closely follow the iComp nominal grid. There are small differences consistent with legacy unit conversion or motherboard revision differences. In particular, the reference anchor line is 0.1524 mm behind the midpoint of its two signal rows, whereas the iComp drawing places it at that midpoint. The reference anchor spacing is 44.2976 mm rather than 44.2700 mm, and its anchor drill is 3.175 mm rather than the 3.20 mm nominal drawing value.

The replacement retains the sourced iComp hole centres. Its own J3 mounting drills are 3.30 mm, providing clearance for nominal M3 shanks without changing the original motherboard. Under ideal circular-hole assumptions, combined radial allowance from the reference motherboard and adapter holes is 0.2375 mm, compared with approximately 0.1530 mm centre mismatch after registering the signal rows. This simple allowance does not include screw, drilling, print or assembly tolerances; actual fit must be checked.

## Underside screw heads

The user's proposed head is approximately 7 mm in diameter and 1 mm high. A bare 7 mm metal disc at the reference CN450 left anchor overlaps the plan projection of a foreign bottom-copper `-M450` trace by 0.2107 mm. At the reference CN352 left anchor, the nominal gap to a foreign bottom trace is only 0.0369 mm. These are copper projections; this screen does not establish which areas are exposed or safely insulated by solder mask.

For comparison, a 6 mm head leaves approximately 0.2893 mm clearance to the nearest CN450 foreign trace in this reference model. That is not approval of a different screw or universal fit.

Revision 0.5 therefore requires a separate insulating washer beneath the motherboard for the retained 7 mm head arrangement. Verify the washer dimensions and dielectric coverage, head bearing, underside component clearance and chassis clearance on the real machine. The insulating washer means that a reliable shell-ground connection must be provided deliberately, rather than assumed through the mounting screw's bearing face.

## Neighbouring connector

On the reference CN450 right side, CN175 mounting pad 7 is centred at approximately X+26.797, Y5.7916 in the replacement's assembly frame. Its copper land is 3.175 mm in diameter and its drill is 2.3622 mm. An unrelieved 52 mm rectangular base projection would overlap that neighbouring hole/lug region.

The delivered adapter PCB has a 16-vertex outline, with outer ears locally reduced to X±25.00 from Y6.00 to Y7.50. The base and cap have a matching local reduction to X±25.00 from Y4.40 to Y7.50, while retaining the full 52 mm width elsewhere. The local boundary comparison gives:

| Shape | Closest boundary point | Gap to reference drill circle | Gap to reference copper-pad circle |
|---|---|---:|---:|
| Adapter PCB | X25.00, Y6.00 | 0.627944 mm | 0.221544 mm |
| Base/cap outer polyline | X26.00, Y4.40 | 0.422571 mm | 0.016171 mm |

The base/cap's closest feature is the front corner of the relief, not the X25 straight segment. The copper-pad projection has very little gap at that corner. These are local plan-outline distances only; no actual neighbouring metal-lug, solder-fillet or connector-housing height is modelled. Their physical clearance remains unverified.

An independent check against the final delivered base and cap STEP solids confirms zero intersection with a vertical cylinder having the reference drill's 2.3622 mm diameter. Their minimum distance to that cylinder is 0.422571 mm. The corresponding final adapter-outline solid has zero intersection and 0.627944 mm minimum distance. These cylinder checks use the drill circle as a reference envelope, not a measured neighbouring component body.

## Saved adapter-to-print alignment

The final native KiCad files for both adapter genders were parsed directly, independently of the builders. Sixty-eight checks passed across the final native boards, delivered STEP clearances and neighbouring reference-cylinder comparison. They confirm:

- All 23 signal-hole centres in each board are unchanged from revision 0.4, with maximum centre movement of 0.000000 mm. The male and female variants retain the same geometric hole set with their own numbering.
- The new mounting holes are at X±22.135, Y9.500, with 3.30 mm adapter drills. The dedicated J4 shell-bond holes are at X±18.000, Y7.000, with 1.20 mm drills.
- Each saved board's 16 outline segments match the shared final relieved outline, and its footprint origin offset is correctly converted to assembly coordinates.
- All 23 guide-clearance probes, both mounting-bore probes and both J4 nominal underside-fillet envelopes return zero base intersection for each board.

The J4 probes are 2.4 mm diameter and extend 0.75 mm beneath the adapter PCB. These results demonstrate saved-file alignment and nominal clearance only. They do not establish actual solder-fillet shape, hole finishing, printer accuracy or pin retention.

The photographs are useful for identifying the CN450 area and nearby parts. They do not establish exact depth or height clearance by themselves. Keep the original motherboard unmodified and record the actual target revision and hardware in the measurement worksheet.
