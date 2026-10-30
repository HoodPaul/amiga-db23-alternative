# Changelog

## 0.6 mechanics / 0.5 PCB - 30 October 2026

- Simplify the optional cover following Paul's revision 0.5 print feedback: remove the four thin projections and both hook legs, fill the base catch recesses, and use a 1.60 mm roof with a short 1.20 mm rim above the mounting hardware. Retain two broad locating tabs and allow tiny glue spots on the tower tops.
- Add 0.40 mm deep, 45-degree entry funnels to all 23 pin guides and the hole-fit coupon. Preserve the straight Ø0.92 retaining bores below each Ø1.72 guide mouth.
- Preserve square forward tower corners, nut pockets, the PCB support height, neighbour relief, original mounting axes and flat base. Record the observed nut fit separately from the unmeasured full PCB stack.
- Remove superseded mechanical outputs and obsolete clip-fit coupons. Regenerate STL, STEP, OpenSCAD, previews, drawings and geometry reports.
- Keep both revision 0.5 PCB projects and manufacturing exports byte-for-byte unchanged. Revision 0.6 remains an unprinted fit prototype.

## Repository documentation - 30 October 2026

- Give the three revision 0.5 amendment commits descriptive engineering titles and update the audit baseline reference to the corresponding commit. The file contents at each renamed commit are unchanged.
- Use Amiga DB23 Video and Floppy Adapter as the README title and describe the current assembly directly.
- Align the BOM and handover with the current flat base, recessed ground-wire channel and loading jig support.
- Retain revision 0.5, existing file names, project credits and fit-prototype status. CAD geometry and manufacturing files are unchanged.

## 0.5 review amendments - 29-30 October 2026

- On 30 October, removed the two circular mounting feet and lowered the complete base underside from Z0.60 to motherboard Z0, creating one broad, coplanar bearing and print surface without changing the PCB support height.
- Squared the forward tower sides and matching cap to X±25.60, adding 0.60 mm at the marked rear-corner rebates and placing the remaining neighbour relief behind the towers.
- Changed both PCB faces to `Amiga DB23 REV 0.5`, retaining the same revision number.
- Updated the project credits to Paul of UK Computing Limited, Jon of JMC Electronics and AI assistance through Codex.

## 0.5 - 29 October 2026

- Replaced recessed top-loaded anchor bolts with M3 screws upward from beneath the motherboard, through the base and PCB ears, with underside insulating washers and nuts directly on top.
- Moved and enlarged J3 into plated mounting lands at the original shell-anchor axes; added separate J4 shell-wire pads clear of nut seats.
- Shortened both male and female PCBs from rear Y16.00 to Y13.00, with mounting ears and coordinated shell routing.
- Replaced loose anchor shims with integral mounting feet and removed old screw-head recesses.
- Added a keyed clip-on cap retaining the jackpost nuts and covering top hardware; default M3 × 12 mm mounting screws and cap fit remain unmeasured.
- Extended rear jackpost-stem clearance with a finite hardware limit.
- Updated assembly, measurements, BOM, source, native CAD, printable trials, previews and validation records.
- Retained fit-prototype status; no physical strength, print heat or Amiga operation test is claimed.

## 0.4 - 29 October 2026

- Raised the printed end supports and closed the rear opening to form a more substantial continuous cradle around the pin guide.
- Preserved the guide-to-PCB gap and local solder/wire relief rather than trapping underside joints in plastic.
- Added a separate pin-height loading jig for equal pin projection before soldering.
- Documented Paul's four-part assembly order: solder connector to PCB; load pins and lower the joined assembly; fit nuts, hex jackposts and optional caps; attach and solder to the motherboard.
- Retained the unchanged male and female PCB designs, netlists and fabrication data at PCB revision 0.3.
- Kept the design as an unmeasured fit prototype. Added material and CAD checks do not establish cable insertion strength or printed-part heat tolerance.

## 0.3 - 29 October 2026

- Developed the supplied horizontal straddle-PCB concept into coordinated male RGB and female floppy variants.
- Narrowed the PCB to a nominal 40 × 12 mm, leaving the shell mounting area to the printed holder.
- Added a structural printed holder with a 23-pin guide block, PCB height shoulders, captive nut pockets and original-position mounting provisions.
- Added a pin-hole fit coupon and adjustable mechanical source.
- Used the sourced original connector grid and separate, neutral pin-to-pin circuits.
- Added measurement, assembly, electrical, development and validation documentation.
- Retained the status of an unmeasured fit prototype. No physical test or production approval is recorded.

## 0.2 - 29 October 2026

- Design review established nominal motherboard dimensions from manufacturer drawings.
- Compared horizontal and vertical PCB approaches and identified connector-specific measurements still required.
- Produced the separate design review and paper fit templates.

## 0.1 - Supplied starting concept

- Horizontal PCB placed between the two rows of a solder-cup DB23.
- Separate male video and female floppy projects.
- Straight pins connecting the adapter to the original motherboard footprint.



## Universal PCB prototype — ordered 30 October 2026

**Use the universal PCB at your own risk.** A separate [universal prototype package](pcb/DB23_Universal_Prototype/README.md) now includes editable PCB, Gerbers/drills, preview, checks and order records. It retains the existing physical routing, adds VIDEO 1 / FLOPPY 1 markings on both faces, removes other numbers and uses round signal pads. Internal numbering remains the VIDEO reference; actual connector orientation and continuity must be checked.

Paul confirmed ordering 30 boards from JLCPCB on 30 October 2026: two-layer FR-4, 1.00 mm, 1 oz, black mask, white silkscreen, ENIG. Receipt, physical fit and functional operation remain unverified. Native KiCad 10.0.7 DRC reports zero errors/unconnected items and four missing-library warnings; exact checks confirm 23 separate signal connections. This is a standalone board snapshot, not a new coordinated PCB revision or a replacement for the two existing variants.


### Hardware order update — 30 October 2026

Paul confirmed **30 PCBs** (correcting the earlier 20), **100 M3 × 12 mm screws with 7 mm heads**, **100 M3 304 stainless nuts**, and **40 strips of 1×40 L11.5 headers** (nominally 1,600 pins). See [the order details](pcb/DB23_Universal_Prototype/ORDER_RECORD_2026-10-30.md). The selected 11.5 mm pins are intended to be used untrimmed after carrier removal; nominal protrusion above the PCB is 1.55 mm and roof clearance 2.70 mm with the existing jig. Actual dimensions and fit are unverified; main CAD still models 10.70 mm pins. Earlier quoted prices apply to the original 20-board screenshot, not the final 30-board order.
