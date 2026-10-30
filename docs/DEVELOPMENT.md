# Development and regeneration

PCB, assembly and mechanical revision 0.5 share `source/design_parameters.json`. This revision changes the board outline, mounting lands, shell-wire pads, routing and printed hardware. Do not reuse revision 0.3 manufacturing files or revision 0.4 mounting instructions with it.

Review manual native-CAD edits before running builders. Port deliberate edits into the source or preserve a reviewed baseline before overwriting files. Keep shared parameters, builders, native CAD, prints, previews and validation together.

## PCB

The builder needs the KiCad Python `pcbnew` module. Use the interpreter associated with KiCad; an ordinary Python installation may not include it.

```sh
python3 source/build_pcb.py --kicad-cli /path/to/kicad-cli
```

Substitute the correct interpreter where required. The CLI path enables the available netlist, schematic PDF, board manufacturing and preview exports. Read the builder help for its current interface.

Native DRC and mapping results must be inspected, not inferred from export success. KiCad 7 CLI does not expose ERC; exact exported-netlist checks are separate.

The portable saved-file audit needs only Python's standard library:

```sh
python3 source/verify_pcb.py
```

It checks the saved boards, exported netlists and clean native DRC reports. It does not rerun KiCad DRC or establish physical fit.

## Mechanical parts

```sh
python3 source/build_mechanical.py
python3 source/verify_mechanical.py
```

The mechanical builder requires both OpenSCAD and CadQuery. OpenSCAD generates printable STL parts from the shared geometry; CadQuery exports analytic STEP and performs solid checks. The independent mechanical verifier also requires VTK and reads saved STEP/STL rather than importing the builder. Read the actual validation record for its scope and results.

The complete base underside reaches motherboard Z0 as a coplanar bearing and print surface, replacing both the old loose shims and the two former circular feet. The pin guide remains raised for clearance. Keep print-bed and assembly transforms distinct, particularly the cap and loading jig. Consult `mechanical/MECHANICAL_NOTES.txt` for generated part names and orientations.

## Previews and drawings

The Python dependencies for the mechanical build, audit, previews and PDF are listed in `source/requirements-previews.txt`; OpenSCAD is a separate application. Native PCB appearance views also need Inkscape. VTK rendering requires an available X display; Xvfb can provide this on headless Linux.

```sh
python3 source/render_previews.py
python3 source/make_pcb_appearance.py
python3 source/make_drawings.py
```

The printed geometry is the actual delivered STL. Bought DB23 bodies, cups, pins and fasteners are explicitly assumed reference envelopes; their preview meshes are not functional print files. Font paths use DejaVu Sans on Linux and may need adjustment elsewhere.

## Coordinated change checks

1. Rebuild affected native and mechanical outputs after parameter changes.
2. Re-run native parsing, DRC, exact connections and saved-geometry checks.
3. Review the PCB ears, J3 nut-bearing lands, J4/base wire channel, underside insulating washers, all 23 pin bores, flat base bearing, cap keys/latches and both fastener directions together.
4. Check default and alternative screw-length envelopes explicitly; do not treat a longer jackpost passage as unlimited clearance.
5. Update assembly, measurements, BOM, previews, drawings, changelog and handover.
6. Record actual commands, versions, failed/unavailable checks and outstanding assumptions.

Do not invent licences, physical compatibility, component measurements or manufacture approval during regeneration.
