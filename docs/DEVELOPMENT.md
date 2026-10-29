# Development and regeneration

The PCB and printed holder share `source/design_parameters.json`. Keep this file, builders, native CAD, printable outputs, previews and validation reports from the same revision together.

Before regeneration, review any manual native-CAD edits. Builders can overwrite generated files. Port deliberate edits into the source or retain a reviewed native baseline before proceeding.

## PCB

The PCB builder requires the KiCad Python `pcbnew` module. Use the Python interpreter associated with the installed KiCad version; a generic Python environment may not provide it.

```sh
python3 source/build_pcb.py --kicad-cli /path/to/kicad-cli
```

Run that command with the correct interpreter in place of `python3` if required by the installation. The `--kicad-cli` path enables the available schematic netlist, schematic PDF and board manufacturing/preview exports. Read the builder's help for the current interface.

The builder creates male and female projects and writes reports under `verification/`. Native DRC and connection-map results must be read, not inferred from a successful export. The KiCad 7 CLI does not provide a native ERC command; exported netlist equality is a separate check and must not be described as ERC.

The portable audit checks the saved boards and exported netlists without KiCad or additional Python packages:

```sh
python3 source/verify_pcb.py
```

It also checks that the saved native DRC reports are clean. It does not independently rerun KiCad DRC or establish physical fit.

## Mechanical parts

```sh
python3 source/build_mechanical.py
```

OpenSCAD performs STL generation. The builder also uses CadQuery for the analytic holder STEP and its additional geometry checks when that dependency is available. The generated OpenSCAD source remains editable, but changes made directly to it must be ported before rerunning the builder.

Keep the slicer's print orientation separate from the assembly coordinate frame. The holder STL retains its z = 0.60 mm assembly offset and should be dropped to the print bed. Shims provide that 0.60 mm gap when the printed part is assembled on the motherboard.

## Previews and drawings

The optional Python dependencies are listed in `source/requirements-previews.txt`. Native PCB colour appearance views also require Inkscape. VTK rendering needs an available X display; an Xvfb session can supply this on a headless Linux machine.

```sh
python3 source/render_previews.py
python3 source/make_pcb_appearance.py
python3 source/make_drawings.py
```

The 3D holder uses the actual printable STL. The purchased DB23 body, solder cups, jackposts and fasteners in the assembly picture use the explicitly assumed reference geometry. Do not treat reference meshes as printable functional parts. Font paths in the preview scripts use DejaVu Sans on Linux; adjust them for other operating systems.

## Change and release checks

After editing shared geometry:

1. Rebuild the affected PCB and mechanical outputs.
2. Re-run native parsing, PCB DRC, connection and geometry checks.
3. Review actual CAD alignment, especially the PCB corner notches, solder access, pin grid, nut pockets, anchor shims and fastener envelopes.
4. Update the measurement worksheet, BOM, drawings, previews, changelog and handover.
5. Record any remaining assumptions and failed or unavailable checks in the validation record.

No future repository URL, licence, physical compatibility or manufacturing approval should be invented during regeneration.

