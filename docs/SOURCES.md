# Sources and assumptions

## Primary connector geometry

- [iComp DB23 connector documentation](https://wiki.icomp.de/wiki/DB23_connector).
- [iComp male right-angle DB23 drawing](https://wiki.icomp.de/w/images/2/2a/DB23_male_iComp.pdf).
- [iComp female right-angle DB23 drawing](https://wiki.icomp.de/w/images/2/24/DB23_female_iComp.pdf).

iComp identifies these as replacements matching the original Commodore/Foxconn parts. The drawings support the nominal motherboard contact pitch, stagger, mounting-hole positions, flange references and centreline height used in this project.

They describe **right-angle motherboard connectors**. They do not establish rear-insulator dimensions, cup gap or cup length for a different solder-cup connector. Those values remain explicitly assumed in revision 0.4 until the selected parts are measured.

## Interface information

- [Commodore A4000 User's Guide](https://www.retromaniek.pl/wp-content/uploads/2019/04/Commodore-Amiga-4000-User-Guide.pdf), Appendix B, VIDEO and FLOPPY ports.

The adapter preserves separate pin positions rather than relying on reduced-function pin assignments. The manual is used for the distinction between video pin 13 and video grounds 16–20, and for the presence of power contacts. Model-specific functions and unused positions should be checked against the intended board.

## D-sub mounting hardware

- [HARTING manufacturer catalogue hosted by Farnell](https://www.farnell.com/datasheets/1853417.pdf), female screw-lock thread options.

Cable-facing and rear mounting threads can differ. The purchased jackpost and matching captive nut, rather than the generic description “D-sub screw”, must determine the pocket and thread specification.

## Practical straddle-PCB precedent

- [Dale King: Amiga Buffered VGA Adaptor](https://github.com/daleking/Amiga_to_VGA_Buffered).

This is evidence that a solder-cup DB23 can accommodate a straddle PCB. It does not validate this holder, PCB thickness, motherboard-tail assembly or any arbitrary solder-cup part.

## Project basis and assumptions

The starting concept is Paul's supplied `DB23_Straddle_Adapter_v0.1.zip`. Revision 0.3 retains the genuine DB23 interface and horizontal straddle arrangement while developing a smaller PCB and a structural printed pin guide. Revision 0.4 develops the holder into a solid cradle and adds a pin-height loading jig, following Paul's assembly review.

Current assumed values include the solder-cup connector rear envelope, 1.00 mm PCB thickness, nut dimensions, pin dimensions and length, printed-hole compensation, material and retention hardware. The authoritative list is `source/design_parameters.json`; measurements should replace assumptions in future revisions.

