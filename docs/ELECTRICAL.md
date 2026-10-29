# Electrical notes

## Passive pin-to-pin circuit

The RGB and floppy adapters follow the same rule: DB23 contact n connects to motherboard tail n for positions 1–23. Each `P01`–`P23` circuit remains distinct from the others in the bare adapter.

The PCB does not reinterpret the port, omit specialised contacts, regulate power, buffer signals or alter timing. Keeping all positions avoids depending on a reduced-function cable or one motherboard's unused contacts.

RGB and floppy have different pin functions. Male and female numbering is mirrored; use the matching variant and actual connector numbering. Do not infer a connection from another interface's pin labels.

## Video ground distinction

Commodore's A4000 documentation distinguishes the clock-related return on video pin 13 from video grounds 16–20. The adapter does not join those contacts. Independent `Pxx` circuits preserve that distinction without assuming another motherboard's return arrangement.

## Mounting and shell circuit

Revision 0.5 gives `SHIELD` four pads, isolated from all 23 signal positions:

| Reference | Function | Nominal coordinates |
|---|---|---|
| J3 pads 1 and 2 | Plated mounting lands for upward screws and top nuts | X±22.135, Y9.50 mm |
| J4 pads 1 and 2 | Dedicated shell-bond wire points, clear of nut-bearing surfaces | X±18.00, Y7.00 mm |

J3 and J4 share `SHIELD`. The PCB does not connect this circuit to any `Pxx` position. Provide a deliberate wire or metal connection from the DB23 metal shell to J4, and a separate J4 wire to the original motherboard shell-ground pad. Keep solder and wire out from beneath the J3 top nuts so they seat flat.

The default mounting screws use insulating washers beneath their heads. Mounting-bolt contact is therefore not the specified motherboard grounding path, even if incidental shank contact occurs. The separate J4-to-motherboard pad wire is required. Printed plastic, solder mask and captured nuts do not establish a bond. Confirm the actual motherboard's shell-ground arrangement and check both deliberate shell connections after assembly.

## Power and routing

Some video and floppy positions carry supply rails. Neutral net names do not imply they may be bridged or exchanged. Signal tracks are nominally 0.50 mm; the separate shell route is nominally 0.60 mm. No continuous-current, voltage-drop or thermal qualification has been performed. Retain the motherboard's original protections and limits.

This assembly does not convert video scan rates or make a drive compatible with the floppy port. Any conversion or interface electronics remain separate.

## Validation scope

The connection audit must prove all 23 mappings for each variant, no merged signal nets and the separate four-pad shell topology. Native parsing and DRC provide additional saved-file checks. They do not establish contact resistance, solder quality, shielding, fit or hardware grounding.

See [VALIDATION.md](VALIDATION.md) for actual results and [SOURCES.md](SOURCES.md) for primary references.
