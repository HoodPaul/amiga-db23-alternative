# Reference motherboard fit screen

Project development: **Paul of UK Computing Limited**, **Jon of JMC Electronics** and **AI assistance through Codex**.

This is a limited comparison with the locally retained [A4000 replica KiCad board](https://github.com/Acill/A4000RevB/blob/master/Kicad/A4k-Replica-Acill.kicad_pcb). It is not a physical fit result, clearance certificate or substitute for measurements of the target motherboard. The source file is not republished here. Its exact SHA-256 and retained copper-screen findings are in [motherboard-reference-fit.json](motherboard-reference-fit.json).

## Reproducible current checks

The current saved boards and STEP files pass **70 checks**, run with:

```sh
python3 source/verify_reference_fit.py --reference-board /path/to/A4k-Replica-Acill.kicad_pcb
```

The helper requires CadQuery and the exact external source file identified by the stored SHA-256. It verifies that source hash, directly parses both saved adapter boards and rechecks their bores, J4 fillet clearances, outlines and the current base/cap STEP. Historic reference-board copper findings are retained rather than re-extracted; this limitation is explicit in the machine-readable report.

## Nominal mounting positions

The source CN450 RGB and CN352 floppy anchor line lies 0.1524 mm behind the midpoint of the source signal rows, with 44.2976 mm anchor spacing and 3.175 mm anchor drills. The sourced iComp contract uses 44.2700 mm spacing and nominal 3.20 mm motherboard drills. The replacement retains iComp centres and uses Ø3.30 mm adapter holes. Under ideal circular-hole assumptions, the reference/adapter radial allowance for a nominal M3 shank is 0.2375 mm versus about 0.1530 mm axis eccentricity; real tolerances and physical fit remain unverified. Do not enlarge or countersink the motherboard.

## Underside screw heads

The unchanged source-board screen records a bare Ø7 mm head overlapping a foreign CN450 bottom-copper trace by 0.2107 mm in plan; the nearest recorded CN352 foreign trace has only 0.0369 mm nominal gap. Mask condition and actual exposed metal are not established. The default Ø8 × 0.50 mm underside insulating washers and deliberate motherboard shell-ground wire therefore remain required. Verify actual coverage, bearing, components and chassis clearance; do not rely on bolt contact for grounding.

## Revised square end faces and neighbouring connector

The recorded CN175 mounting pad is centred at X26.797, Y5.7916, with a Ø2.3622 mm drill and Ø3.175 mm copper land. The strengthened forward ends now use one uniform outer face at X±25.60 through Y5.10. The aft local relief then reduces the outer edge to X±25.00 until Y7.50. PCB ears remain unchanged: X±25.00 at Y6.00–7.50 and X±25.60 behind it.

| Current saved shape | Gap to reference drill cylinder | Drill-cylinder intersection |
|---|---:|---:|
| Base | 0.201332 mm | 0.000000 mm³ |
| Cap | 0.201332 mm | 0.000000 mm³ |
| Adapter outline | 0.627944 mm | 0.000000 mm³ |

The closest square end corner has a signed planar gap to the copper-pad circle of approximately **-0.205068 mm**. A negative value means projected overlap with the ground land, not a proven collision or electrical contact: the printed parts are insulating and the actual lug, solder fillet and housing heights are not modelled. This is an explicit physical fit check for the target motherboard. Do not interpret a clear drill cylinder as proof of clearance to the complete neighbouring connector.

## Saved adapter-to-print alignment

For each gender, 23 guide probes, two mounting-bore probes and two conservative J4 underside-fillet probes clear the delivered base. Native tail positions match the nominal grid, both variants retain the same geometric tail set, and all 16 outline segments match the shared contract. The J4 probe is Ø2.40 mm and extends 0.75 mm below the adapter PCB. These are saved-file alignment checks, not actual solder-fillet or print-fit measurements.

The photographs identify the CN450 area but do not establish exact depth or height clearance. Record the real motherboard revision, neighbouring metal and solder geometry, fastener stack and case fit in the measurement worksheet.
