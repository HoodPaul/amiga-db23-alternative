# Electrical notes

## Passive pin-to-pin circuit

The RGB and floppy adapters use the same rule: DB23 contact n connects to motherboard tail n for positions 1–23. Each net is named `P01`–`P23`, and remains distinct from the others in the adapter.

The PCB does not reinterpret the port, omit specialised contacts, regulate power, buffer signals or change timing. It retains contacts that may be unused on a particular motherboard so the mechanical replacement does not depend on a reduced-function cable.

RGB and floppy have different pin functions. Male and female numbering is mirrored. Do not use a pin-function label from one interface to infer a connection on the other. The selected motherboard schematic and actual connector numbering remain the assembly references.

## Video ground distinction

Commodore's A4000 documentation distinguishes the clock-related return on video pin 13 from the video grounds on pins 16–20. The adapter must not join those contacts together. Keeping each `Pxx` net separate preserves that distinction without assuming how another model's motherboard implements its returns.

## Shell circuit

The `SHIELD` circuit joins the two shell strap pads and is isolated from all 23 `Pxx` circuits in the bare adapter PCB. The assembly requires a real wire or metal connection from the DB23 shell to the original motherboard shell-ground points. Confirm the chosen bonding arrangement against the target board.

The plastic holder, captive nut pockets and PCB support shoulders provide no electrical bond. A metal fixing also provides no guaranteed bond unless it contacts the intended conductive surfaces.

## Power and routing

Some video and floppy contacts carry supply rails. The neutral net names do not mean those contacts are safe to bridge or interchangeable. The design uses short nominal 0.50 mm tracks, but no continuous-current, voltage-drop or thermal qualification has been performed. Retain the motherboard's original protections and interface limits.

Adding this connector assembly does not make a display accept the Amiga's video scan rates and does not make a drive compatible with the floppy port. Any external conversion or interface electronics remain separate.

## Validation scope

The connection audit must prove all 23 mappings independently for both PCB variants, confirm that no pin nets are merged, and check the independent shell path. Native parsing and PCB DRC establish additional saved-file consistency. Those checks do not establish contact resistance, soldering quality, shielding or physical fit.

See [VALIDATION.md](VALIDATION.md) for actual results and [SOURCES.md](SOURCES.md) for the primary references.

