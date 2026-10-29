# Amiga DB23 Video and Floppy Replacement

A low-cost replacement assembly for the motherboard-mounted **DB23 RGB video and external floppy connectors** used on the Amiga. It combines a genuine solder-cup DB23, a small horizontal PCB and a printed holder with a supported 23-pin motherboard interface. Current revision: **0.3**.

Project development: **Paul of UK Computing Limited**, with **AI assistance through Codex**. The design develops Paul's supplied straddle-PCB concept and the proposal to support ordinary loose header pins in a printed block.

Repository: [HoodPaul/amiga-db23-alternative](https://github.com/HoodPaul/amiga-db23-alternative).

**Status, 29 October 2026: fit prototype. The chosen solder-cup connector, jackposts, nuts and printer tolerances have not been measured. No physical fit, assembled connector or operation in an Amiga has been verified.** The editable files and trial-print parts are intended to make those checks possible. This is not a production release.

For engineering or AI work, start with [AGENTS.md](AGENTS.md), the [current handover](docs/AI-HANDOVER.md) and the [documentation index](docs/README.md).

![Assembly view](previews/assembly-isometric.png)
![Exploded assembly](previews/assembly-exploded.png)

These views are rendered from the coordinated prototype CAD. The DB23 reference body and solder cups are illustrative, unmeasured envelopes; their appearance is not evidence that a purchased connector fits. Further views and the [prototype drawing PDF](previews/DB23_Prototype_Drawings_v0.3.pdf) are in [previews/](previews/).

## How it works

The DB23's solder cups straddle the front edge of the PCB. The upper contact row solders to the top copper; the lower row solders to the bottom copper. Separate straight pins connect the PCB to the original motherboard holes.

The printed holder supports the connector flange, captures its jackpost nuts and guides the 23 straight pins. Its shoulders set the PCB height. Mounting fasteners through the original shell retention holes provide the mechanical attachment; the signal pins are not intended to support cable insertion loads.

The existing Amiga cable interface remains DB23. No replacement cable standard is introduced.

## PCB variants and editable files

Open either project with **KiCad 7.0 or newer**:

| Variant | Editable project | Connector on the Amiga |
|---|---|---|
| RGB video | [DB23M_RGB.kicad_pro](pcb/DB23M_RGB/DB23M_RGB.kicad_pro) | Male DB23 solder-cup connector |
| External floppy | [DB23F_Floppy.kicad_pro](pcb/DB23F_Floppy/DB23F_Floppy.kicad_pro) | Female DB23 solder-cup connector |

Project-local symbols and footprints are included. Male and female pin numbering is mirrored; use the matching PCB rather than turning one variant over.

| Property | Revision 0.3 |
|---|---|
| PCB outline | **40.00 × 12.00 mm overall**, with front-corner clearance notches |
| Copper layers | **Two** |
| PCB thickness | **1.00 mm assumed**, to be selected from the measured solder-cup gap |
| Appearance | Black mask, white silkscreen and ENIG exposed pads proposed |
| Signal tracks / nominal clearance | **0.50 / 0.20 mm** |
| Motherboard-tail drill / pad diameter | **1.04 / 1.70 mm** |
| Along-row pitch / row spacing / stagger | **2.77 / 2.84 / 1.385 mm** |
| Front signal row | Pins **13–23**, 8.08 mm inward from the flange reference plane |
| Rear signal row | Pins **1–12**, 10.92 mm inward from the flange reference plane |
| Original shell mounting centres | **44.27 mm**, on the 9.50 mm line |
| Nominal connector centreline | **6.25 mm** above the motherboard top |

Motherboard values are nominal dimensions from the [iComp replacement drawings](docs/SOURCES.md). They are not a measurement of the intended motherboard. The solder-cup connector envelope and PCB depth remain assumptions.

## Printed holder and pin fit

Editable [OpenSCAD source](mechanical/DB23_Holder_v0.3.scad), a [holder STL](mechanical/DB23_Holder_v0.3.stl), an analytic [holder STEP](mechanical/DB23_Holder_v0.3.step), a [hole-fit coupon](mechanical/DB23_Hole_Fit_Coupon_v0.3.stl) and an optional [nut keeper STL](mechanical/DB23_Nut_Keeper_v0.3.stl) are provided. Print two keepers if that option is used. The holder sits 0.60 mm above the motherboard; **two matching 0.60 mm anchor shims or washers are required beneath its mounting feet before tightening**. The [shim-pair STL](mechanical/DB23_Anchor_Shims_v0.3.stl) contains both supports.

The nominal holder is **52 mm wide** and uses **0.92 mm guide bores** for the assumed 0.64 mm square pins. Print the coupon before the full holder. A 0.64 mm square pin measures approximately **0.905 mm across its corners**, so a finished 0.80 mm round bore is too small. The usable printed or drilled diameter must be established with the actual pins and printer.

Choose jackposts with the required **4-40 UNC cable-facing thread**, then match the captive nuts to their actual rear mounting stems. Prototype defaults use **M3 rear stems and M3 nuts**, with assumed 5.50 mm across flats and 2.40 mm nut thickness. HARTING 09670009924 is a candidate thread arrangement, not a drop-in or frozen purchase item: stem length must clear the anchor bolts. M3.5 has not been specified. All pockets and fastener lengths need a fit test.

See the [mechanical notes](docs/MECHANICAL.md), [measurement worksheet](docs/MEASUREMENTS.md) and [assembly guide](docs/ASSEMBLY.md).

## Electrical arrangement

Both PCBs pass **all 23 positions individually, pin n to pin n**. Neutral net names `P01`–`P23` avoid implying that the same pin has the same function on video and floppy ports. There are no buffers, converters, protection components or changes to the Amiga interface.

The shell connection is a separate `SHIELD` circuit. It requires deliberate metal or wire bonding to the connector shell and the motherboard's original shell-ground point. Printed plastic and captive nut pockets provide no electrical grounding. The PCB does not join video pin 13 to pins 16–20.

See [electrical notes](docs/ELECTRICAL.md) and the [BOM](BOM.csv).

## Validation and prototype manufacture

Both saved boards pass native KiCad 7.0.11 DRC with **zero violations, zero unconnected pads and zero footprint errors**. The portable saved-file audit passes **610 checks** across the male and female projects. The holder STL is one closed component and the STEP is one valid solid, with all 23 guide bores open. An independent CAD review found no intersections with the explicitly assumed connector, nuts and notched PCB. Native schematic ERC was not run; parser and exact exported netlist checks are recorded separately.

The scope and actual reports are recorded in [validation](docs/VALIDATION.md). These checks establish consistency of the saved files. They do not establish solder-cup compatibility, printer accuracy, physical fit, strength or reliable operation.

Before ordering a PCB, complete the [measurements](docs/MEASUREMENTS.md), print the fit coupon and holder, and check the unpowered assembly against the target motherboard and case. Any generated manufacturing files remain **fit-prototype files**, not approval to manufacture an unmeasured design.

Run the portable saved-file audit from the project root; it needs Python 3 without additional packages:

```sh
python3 source/verify_pcb.py
```

See the [development workflow](docs/DEVELOPMENT.md) before changing parameters or regenerating files.

## Project contents

| Path | Purpose |
|---|---|
| [pcb/](pcb/) | Male RGB and female floppy KiCad projects with local libraries |
| [mechanical/](mechanical/) | Editable holder and printable trial parts |
| [previews/](previews/) | Assembly and PCB appearance views |
| [docs/](docs/) | Assembly, measurements, sources and AI handover |
| [source/](source/) | Shared parameters and reproducible design builders |
| [verification/](verification/) | Native reports and connection checks |
| [BOM.csv](BOM.csv) | Parts and purchasing requirements for one assembly |
| [CHANGELOG.md](CHANGELOG.md) | Revision history |
| [NOTICE.md](NOTICE.md) | Project and third-party notices |

