# Saved-file mechanical review, revision 0.6

**PCB revision 0.5 is unchanged.** Reviewed 30 October 2026 using the delivered STEP/STL exports, separately from the mechanical builder. This is a CAD review, not an independent human certification or physical fit test.

Project development: **Paul of UK Computing Limited**, **Jon of JMC Electronics** and **AI assistance through Codex**.

`python3 source/verify_mechanical.py` passes **273 checks**. CadQuery/OpenCascade reads saved STEP solids and VTK reads the delivered STL files. Detailed probe, intersection and mesh results are in [mechanical-audit.json](mechanical-audit.json).

## Simplified cover and base

The 1.60 mm roof spans Z11.00–12.60. The short 1.20 mm side/rear rim starts at Z10.30; the front skirt starts at Z10.20. Two broad locating tabs extend to Z9.90. Saved-solid probes confirm the four old thin corner projections and two hook/beam features are absent, both old catch recesses are filled in the base, the upper rim is present, and the tabs/tower-top bearing remain.

The cover is optional and can be secured with tiny glue spots on the tower tops after inspection. The fitted horizontal stems block nominal upward nut escape in the envelope check. Actual threaded retention, glue strength and serviceability are not established by that geometric test.

## Pin entries and retained geometry

Each of the 23 guides opens from Ø0.92 at Z4.10 to Ø1.72 at Z4.50, a 0.40 mm deep 45° funnel. STEP probes check three taper heights and retained lower material. Independent STL rays check both edges of each funnel at Z4.30, radius 0.66 mm within 0.003 mm. The lower guide remains straight; all bores are open. Actual pin grip, hand drilling and heated insertion remain untested.

Base STEP volume is **1,939.705637 mm³**; cover volume is **1,150.640000 mm³**. The broad Z0 underside retains one 359.104525 mm² bottom face. PCB support stays at Z5.75 and guide top Z4.50, giving 1.25 mm nominal fillet/heat space. The forward tower faces remain X±25.60 over Y0.65–5.10; neighbour relief remains X±25.00 over Y5.10–7.50. Nut pockets and shell-wire relief are retained.

## Assembly and mounting hardware

The base clears the seated PCB, assumed DB23 flange/body and all 23 cup envelopes. The complete joined assembly clears a 20 mm vertical insertion sweep; jackpost-nut loading sweeps clear. Assumed square pins clear the cover and loading jig.

The default M3 × 12 mm mounting screw uses an assumed Ø7 × 1 mm head, Ø8 × 0.50 mm insulating washer under the motherboard, 1.60 mm motherboard, 5.75 mm base support height, 1.00 mm PCB and 2.40 mm top nut without a top washer. The under-head stack is 11.25 mm, tip Z9.90, nut top Z9.15, thread projection 0.75 mm and roof clearance 1.10 mm. All default hardware envelopes clear the cover, including enclosing cylinders for any top-nut rotation.

| Under-head length | Tip Z | Cover intersection per screw |
|---|---:|---:|
| 12 mm, default | 9.90 mm | 0 mm³ |
| 14 mm, unsupported untrimmed | 11.90 mm | 6.361725 mm³ |
| 16 mm, unsupported untrimmed | 13.90 mm | 11.309734 mm³ |

The maximum checked horizontal jackpost stem ends at Y6.00; its passage ends at Y6.20. It clears the base, PCB and top mounting nuts. Arbitrary longer stems are not qualified. Actual flange bearing, torque and compression need a trial.

Keep deliberate J4 bonds to both the DB23 metal shell and original motherboard shell-ground pad. The recessed right-side channel has a clear core in the saved model; actual wire/solder must not lift the base. Insulated screw heads are not the grounding path.

## Print files and loading jig

| Part | STL triangles | Connected regions | Boundary/non-manifold edges | STEP volume |
|---|---:|---:|---:|---:|
| Base | 13,652 | 1 | 0 | 1,939.706 mm³ |
| Optional cover | 132 | 1 | 0 | 1,150.640 mm³ |
| Pin-height jig | 1,036 | 1 | 0 | 3,008.953 mm³ |
| Hole-fit coupon | 34,320 | 1 | 0 | STL trial only |

Restore the cap STL by rotating 180° around X and translating +12.60 mm in Z. Its restored bounds agree with STEP within 0.002 mm. Restore jig STEP/STL by translating −6.20 mm in Z. Independent ray checks verify 23 lower-tip stops at Z−3.20, base support at Z0 and locator tops Z1.20. Equal 10.70 mm pins then place tops at Z7.50; remove the jig before soldering and verify retention after transfer.

## Reference and physical limits

The [reference-board comparison](motherboard-reference-fit.md) passes 70 checks, retaining gaps of 0.201332 mm for base/cover and 0.627944 mm for the PCB to the nominal neighbour drill cylinder. Copper-pad projection overlaps about 0.205068 mm; actual lug, solder and housing are not represented by a drill cylinder. Under-head insulation remains required by the retained reference copper screen.

Paul's physical feedback concerns revision 0.5 only: delicate lid features and a nut within the printed footprint, shown without the PCB underneath. Revision 0.6 remains unprinted. These checks do not establish real fit, print accuracy, adhesive performance, pin retention, hot insertion, soldering heat tolerance, clamping torque, chassis fit, cable strength or Amiga operation.
