#!/usr/bin/env python3
"""Generate the DB23 fit-prototype KiCad projects with KiCad 7 pcbnew.

Run with a Python interpreter containing pcbnew (normally system KiCad Python).
The shared design_parameters.json is authoritative for dimensions. Rebuilding
overwrites the generated pcb/ and per-project verification files.
"""
from pathlib import Path
import argparse
import csv
import json
import math
import re
import shutil
import subprocess
import sys
import uuid
import xml.etree.ElementTree as ET

import wx
APP = wx.AppConsole()
import pcbnew as k

ROOT = Path(__file__).resolve().parents[1]
PARAMS = json.loads((ROOT / 'source/design_parameters.json').read_text())
P = PARAMS['pcb']
M = PARAMS['motherboard']
REV = PARAMS['pcb_revision']
ORIGIN = (150.0, 80.0)
NAMESPACE = uuid.UUID('4c21c548-6442-4900-9bec-1ad39af09c24')
PROJECTS = [('DB23M_RGB', 'M', 'MALE RGB'), ('DB23F_Floppy', 'F', 'FEMALE FLOPPY')]


def uid(label):
    return str(uuid.uuid5(NAMESPACE, label))


def mm(v):
    return k.FromMM(v)


def pos(x, y):
    return k.VECTOR2I(mm(ORIGIN[0] + x), mm(ORIGIN[1] + y))


def xy(n, gender):
    x = (6.5 - n) * M['pin_pitch'] if n <= 12 else (18 - n) * M['pin_pitch']
    if gender == 'F':
        x = -x
    return x, M['rear_row_y'] if n <= 12 else M['front_row_y']


def nname(n):
    return f'P{n:02d}'


def line(board, start, end, layer, width=0.05):
    item = k.PCB_SHAPE()
    item.SetShape(k.SHAPE_T_SEGMENT)
    item.SetStart(pos(*start)); item.SetEnd(pos(*end))
    item.SetWidth(mm(width)); item.SetLayer(layer)
    board.Add(item)


def board_text(board, s, x, y, layer=k.F_SilkS, size=0.9, mirror=False, thickness=None):
    item = k.PCB_TEXT(board)
    item.SetText(s); item.SetPosition(pos(x, y)); item.SetLayer(layer)
    item.SetTextSize(k.VECTOR2I(mm(size), mm(size)))
    item.SetTextThickness(mm(thickness if thickness is not None else (0.12 if size < 0.9 else 0.15)))
    item.SetMirrored(mirror)
    board.Add(item)


def new_fp(board, name, ref, value, project):
    fp = k.FOOTPRINT(board)
    fp.SetReference(ref); fp.SetValue(value)
    fp.SetFPIDAsString(f'DB23_Local:{name}')
    fp.SetPosition(pos(0, 0)); fp.SetLayer(k.F_Cu)
    fp.Reference().SetVisible(False); fp.Reference().SetLayer(k.F_Fab)
    fp.Value().SetVisible(False); fp.Value().SetLayer(k.F_Fab)
    path = k.KIID_PATH()
    path.push_back(k.KIID(uid(f'{project}/{ref}')))
    fp.SetPath(path)
    return fp


def configure_rules(board):
    ds=board.GetDesignSettings()
    ds.SetBoardThickness(mm(P['thickness']));ds.SetCopperLayerCount(2)
    ds.m_MinClearance=mm(P['clearance']);ds.m_CopperEdgeClearance=mm(0.2)
    ds.m_SilkClearance=mm(0.1);ds.m_MinSilkTextHeight=mm(0.7);ds.m_MinSilkTextThickness=mm(0.1)
    ds.m_TrackMinWidth=mm(0.2);ds.m_MinThroughDrill=mm(0.3);ds.m_HoleToHoleMin=mm(0.25)
    ds.m_ViasMinSize=mm(0.6);ds.m_ViasMinAnnularWidth=mm(0.1)
    nc=ds.m_NetSettings.m_DefaultNetClass
    nc.SetTrackWidth(mm(P['track_width']));nc.SetClearance(mm(P['clearance']))


def courtyard(fp,x0,y0,x1,y1):
    """Contact-group service envelope; complete connector housing is in MCAD."""
    points=[(x0,y0),(x1,y0),(x1,y1),(x0,y1)]
    for a,b in zip(points,points[1:]+points[:1]):
        item=k.FP_SHAPE(fp);item.SetShape(k.SHAPE_T_SEGMENT);item.SetLayer(k.F_CrtYd);item.SetWidth(mm(0.05))
        item.SetStart0(k.VECTOR2I(mm(a[0]),mm(a[1])));item.SetEnd0(k.VECTOR2I(mm(b[0]),mm(b[1])))
        item.SetStart(pos(*a));item.SetEnd(pos(*b));fp.Add(item)


def round_courtyard(fp,x,y,radius):
    """Circular keep-out envelope avoids a square corner overstating round hardware."""
    item=k.FP_SHAPE(fp);item.SetShape(k.SHAPE_T_CIRCLE)
    item.SetLayer(k.F_CrtYd);item.SetWidth(mm(0.05))
    item.SetStart0(k.VECTOR2I(mm(x),mm(y)))
    item.SetEnd0(k.VECTOR2I(mm(x+radius),mm(y)))
    item.SetStart(pos(x,y));item.SetEnd(pos(x+radius,y));fp.Add(item)


def add_pad(fp, n, x, y, net, side=None, drill=None, size=None):
    pad = k.PAD(fp)
    pad.SetNumber(str(n)); pad.SetPos0(k.VECTOR2I(mm(x),mm(y))); pad.SetPosition(pos(x, y))
    if side is None:
        pad.SetAttribute(k.PAD_ATTRIB_PTH)
        pad.SetShape(k.PAD_SHAPE_RECT if str(n) == '1' and fp.GetReference() == 'J2' else k.PAD_SHAPE_CIRCLE)
        dia = size or P['tail_pad_diameter']
        pad.SetSize(k.VECTOR2I(mm(dia), mm(dia)))
        hole = drill or P['tail_drill']
        pad.SetDrillSize(k.VECTOR2I(mm(hole), mm(hole)))
        layers=k.LSET.AllCuMask();layers.AddLayer(k.F_Mask);layers.AddLayer(k.B_Mask)
        pad.SetLayerSet(layers)
    else:
        pad.SetAttribute(k.PAD_ATTRIB_SMD)
        pad.SetShape(k.PAD_SHAPE_ROUNDRECT)
        pad.SetSize(k.VECTOR2I(mm(P['cup_pad_width']), mm(P['cup_pad_length'])))
        pad.SetRoundRectRadiusRatio(0.20)
        # Hand-soldered cups; no paste apertures/stencil are specified.
        layers=k.LSET(side);layers.AddLayer(k.F_Mask if side == k.F_Cu else k.B_Mask)
        pad.SetLayerSet(layers)
    pad.SetNet(net)
    fp.Add(pad)
    return pad


def track(board, start, end, layer, net, width=None):
    t = k.PCB_TRACK(board)
    t.SetStart(pos(*start)); t.SetEnd(pos(*end)); t.SetLayer(layer)
    t.SetWidth(mm(width or P['track_width'])); t.SetNet(net)
    board.Add(t)


def symbol_definition(name, side, count):
    x, ang = (7.62, 180) if side == 'R' else (-7.62, 0)
    h = -2.54 * (count - 1)
    o = [f'(symbol "DB23_Local:{name}" (pin_names (offset 1.016) hide) (in_bom yes) (on_board yes)',
         ' (property "Reference" "J" (at 0 5.08 0) (effects (font (size 1.27 1.27))))',
         f' (property "Value" "{name}" (at 0 3.048 0) (effects (font (size 1.27 1.27))))',
         ' (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))',
         ' (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))',
         f' (symbol "{name}_0_1" (rectangle (start -5.08 1.27) (end 5.08 {h-1.27:.3f}) (stroke (width 0.254) (type default)) (fill (type background))))',
         f' (symbol "{name}_1_1"']
    for n in range(1, count + 1):
        o.append(f' (pin passive line (at {x} {-2.54*(n-1):.3f} {ang}) (length 2.54) (name "{n}" (effects (font (size 1.27 1.27)))) (number "{n}" (effects (font (size 1.27 1.27)))))')
    o += [' )', ')']
    return '\n'.join(o)


def schematic(project, gender):
    root = uid(f'{project}/root')
    defs = [('Cups23', 'R', 23), ('Motherboard23', 'L', 23), ('MountingShield', 'R', 2), ('ShellBond', 'R', 2)]
    o = [f'(kicad_sch (version 20230121) (generator eeschema)',
         f' (uuid {root}) (paper "A4")',
         f' (title_block (title "{project} DB23 replacement") (date "{PARAMS["date"]}") (rev "{REV}") (company "Amiga DB23") (comment 1 "FIT PROTOTYPE - measure selected solder-cup DB23 before manufacture") (comment 2 "Paul of UK Computing Limited; Jon of JMC Electronics; AI assistance through Codex"))',
         ' (lib_symbols']
    o.extend(symbol_definition(*d) for d in defs)
    o.append(' )')

    def add_symbol(name, ref, x, y, count):
        inst = uid(f'{project}/{ref}')
        value = {'J1': f'DB23{gender} SOLDER CUPS', 'J2': 'MOTHERBOARD PINS', 'J3': 'M3 MOUNTING / SHIELD', 'J4': 'DB23 SHELL WIRE BOND'}[ref]
        o.extend([f' (symbol (lib_id "DB23_Local:{name}") (at {x} {y} 0) (unit 1) (in_bom yes) (on_board yes)',
                  f' (uuid {inst})',
                  f' (property "Reference" "{ref}" (at {x} {y-6.35} 0) (effects (font (size 1.27 1.27))))',
                  f' (property "Value" "{value}" (at {x} {y-3.81} 0) (effects (font (size 1.27 1.27))))',
                  f' (property "Footprint" "DB23_Local:{name}_{gender}" (at {x} {y} 0) (effects (font (size 1.27 1.27)) hide))',
                  f' (property "Datasheet" "" (at {x} {y} 0) (effects (font (size 1.27 1.27)) hide))'])
        for n in range(1, count+1):
            o.append(f' (pin "{n}" (uuid {uid(f"{project}/{ref}/pin{n}")}))')
        o.append(f' (instances (project "{project}" (path "/{root}" (reference "{ref}") (unit 1)))))')

    add_symbol('Cups23', 'J1', 60, 40, 23)
    add_symbol('Motherboard23', 'J2', 160, 40, 23)
    add_symbol('MountingShield', 'J3', 60, 120, 2)
    add_symbol('ShellBond', 'J4', 60, 140, 2)
    for n in range(1, 24):
        yy = 40 + 2.54*(n-1)
        o.append(f' (wire (pts (xy 67.62 {yy:.3f}) (xy 152.38 {yy:.3f})) (stroke (width 0) (type default)) (uuid {uid(f"{project}/wire{n}")}))')
        o.append(f' (label "{nname(n)}" (at 105 {yy:.3f} 0) (effects (font (size 1.27 1.27)) (justify left bottom)) (uuid {uid(f"{project}/label{n}")}))')
    for ref,y0 in [('J3',120),('J4',140)]:
        for n in (1, 2):
            yy = y0+2.54*(n-1)
            o.append(f' (wire (pts (xy 67.62 {yy:.3f}) (xy 77.62 {yy:.3f})) (stroke (width 0) (type default)) (uuid {uid(f"{project}/{ref}/shieldwire{n}")}))')
            o.append(f' (label "SHIELD" (at 77.62 {yy} 0) (effects (font (size 1.27 1.27)) (justify left bottom)) (uuid {uid(f"{project}/{ref}/shieldlabel{n}")}))')
    note = 'Passive pin-for-pin replacement. J1 pin n connects only to J2 pin n.\\nJ3 pads are M3 mounting lands on SHIELD, aligned to the original motherboard shell anchors.\\nJ4 is a dedicated shell-wire bond: solder away from the mounting nut and washer bearing faces.\\nProvide a deliberate connector-shell bond and verify hardware continuity to motherboard shell ground.\\nNo video ground pins, pin 13, or supply rails are joined by this board.\\nJ1 solder cups: 1-12 on F.Cu, 13-23 on B.Cu. Actual connector fit remains unverified.'
    o.append(f' (text "{note}" (at 85 122 0) (effects (font (size 1.27 1.27)) (justify left top)) (uuid {uid(f"{project}/notes")}))')
    o.append(' (sheet_instances (path "/" (page "1")))')
    o.append(')')
    return '\n'.join(o)+'\n'


def project_config(project):
    return {
      'meta': {'filename': f'{project}.kicad_pro', 'version': 1},
      'board': {'design_settings': {'rules': {
        'min_clearance': 0.2, 'min_track_width': 0.2,
        'min_via_diameter': 0.6, 'min_through_hole_diameter': 0.3,
        'min_hole_to_hole': 0.25, 'min_copper_edge_clearance': 0.2,
        'min_silk_clearance': 0.1, 'min_text_height': 0.7,
        'min_text_thickness': 0.1
      }}},
      'net_settings': {'meta': {'version': 3}, 'classes': [{
        'name': 'Default', 'clearance': 0.2, 'track_width': 0.5,
        'via_diameter': 0.6, 'via_drill': 0.3,
        'microvia_diameter': 0.3, 'microvia_drill': 0.1,
        'diff_pair_width': 0.2, 'diff_pair_gap': 0.25, 'diff_pair_via_gap': 0.25
      }]}
    }


def build(project, gender, label):
    dest = ROOT / 'pcb' / project
    library = dest / 'DB23_Local.pretty'
    library.mkdir(parents=True, exist_ok=True)
    for legacy in library.glob('ShieldStraps_*.kicad_mod'):
        legacy.unlink()
    (dest/f'{project}.kicad_pro').write_text(json.dumps(project_config(project), indent=2)+'\n')
    (dest/f'{project}.kicad_sch').write_text(schematic(project, gender))
    definitions = '\n'.join(symbol_definition(*d).replace('"DB23_Local:', '"') for d in [('Cups23','R',23),('Motherboard23','L',23),('MountingShield','R',2),('ShellBond','R',2)])
    (dest/'DB23_Local.kicad_sym').write_text('(kicad_symbol_lib (version 20220914) (generator kicad_symbol_editor)\n'+definitions+'\n)\n')
    (dest/'fp-lib-table').write_text('(fp_lib_table\n  (lib (name "DB23_Local")(type "KiCad")(uri "${KIPRJMOD}/DB23_Local.pretty")(options "")(descr "Project-local DB23 fit prototype"))\n)\n')
    (dest/'sym-lib-table').write_text('(sym_lib_table\n  (lib (name "DB23_Local")(type "KiCad")(uri "${KIPRJMOD}/DB23_Local.kicad_sym")(options "")(descr "Project-local passive connectors"))\n)\n')
    board = k.BOARD()
    board.SetFileName(str(dest/f'{project}.kicad_pcb'))
    configure_rules(board)
    net = {}
    for n in range(1, 24):
        net[n] = k.NETINFO_ITEM(board, '/'+nname(n)); board.Add(net[n])
    shield = k.NETINFO_ITEM(board, '/SHIELD'); board.Add(shield)
    cups = new_fp(board, f'Cups23_{gender}', 'J1', f'DB23{gender} solder cups', project)
    cups.SetAttributes(k.FP_SMD)
    tails = new_fp(board, f'Motherboard23_{gender}', 'J2', 'Pins to motherboard', project)
    tails.SetAttributes(k.FP_THROUGH_HOLE)
    straps = new_fp(board, f'MountingShield_{gender}', 'J3', 'M3 mounting / shield', project)
    straps.SetAttributes(k.FP_THROUGH_HOLE)
    bonds = new_fp(board, f'ShellBond_{gender}', 'J4', 'DB23 shell wire bond', project)
    bonds.SetAttributes(k.FP_THROUGH_HOLE)
    cup_y = P['cup_pad_front_y'] + P['cup_pad_length']/2
    for n in range(1, 24):
        x, y = xy(n, gender)
        layer = k.F_Cu if n<=12 else k.B_Cu
        add_pad(cups, n, x, cup_y, net[n], side=layer)
        add_pad(tails, n, x, y, net[n])
        track(board, (x,cup_y), (x,y), layer, net[n])
        # Labels between the two motherboard rows avoid cup and PTH mask.
        board_text(board, str(n), x, 9.50, k.F_SilkS if n<=12 else k.B_SilkS, 0.8, n>12)
    for n, x in [(1,-P['shield_pad_x']), (2,P['shield_pad_x'])]:
        add_pad(straps,n,x,P['shield_pad_y'],shield,drill=P['shield_pad_drill'],size=P['shield_pad_diameter'])
    for n,x in [(1,-P['shell_bond_pad_x']),(2,P['shell_bond_pad_x'])]:
        add_pad(bonds,n,x,P['shell_bond_pad_y'],shield,drill=P['shell_bond_pad_drill'],size=P['shell_bond_pad_diameter'])
        round_courtyard(bonds,x,P['shell_bond_pad_y'],P['shell_bond_pad_diameter']/2+.05)
    courtyard(cups,-16.2,4.05,16.2,6.95)
    courtyard(tails,-16.2,7.10,16.2,11.90)
    mounting_radius = P['shield_pad_diameter']/2
    for x in (-P['shield_pad_x'],P['shield_pad_x']):
        round_courtyard(straps,x,P['shield_pad_y'],mounting_radius)
    for fp in (cups,tails,straps,bonds):
        board.Add(fp)
        # Library copies are saved with their own relative contact coordinates.
        clone = fp.Duplicate()
        clone.SetPosition(k.VECTOR2I(0,0)); clone.SetReference('REF**')
        clone.ClearAllNets()
        k.FootprintSave(str(library), clone)
    # Between the two PTH rows: 1.42 - 0.85 - 0.30 = 0.27 mm
    # clearance to either row's copper, with the SHIELD route on B.Cu.
    track(board,(-P['shield_pad_x'],P['shield_track_y']),
          (P['shield_pad_x'],P['shield_track_y']),k.B_Cu,shield,P['shield_track_width'])
    for side in (-1,1):
        track(board,(side*P['shell_bond_pad_x'],P['shell_bond_pad_y']),
              (side*P['shield_pad_x'],P['shield_pad_y']),k.F_Cu,shield,P['shield_track_width'])
    points=P['outline_xy']
    for a,b in zip(points,points[1:]+points[:1]):line(board,a,b,k.Edge_Cuts)
    # Mixed-case descenders need a smaller label in the unchanged rear strip.
    board_text(board,f'Amiga DB23 REV {REV}',0,12.29,k.F_SilkS,0.7,thickness=0.1)
    board_text(board,f'Amiga DB23 REV {REV}',0,12.29,k.B_SilkS,0.7,True,thickness=0.1)
    board_text(board,'S',-18.0,10.4,k.F_SilkS,0.8)
    board_text(board,'S',18.0,10.4,k.F_SilkS,0.8)
    board_text(board,'FLANGE REFERENCE y=0; NOMINAL CONTACT C/L z=6.25; FIT PROTOTYPE',0,-2.0,k.Dwgs_User,1.0)
    line(board,(-M['anchor_spacing']/2,0),(M['anchor_spacing']/2,0),k.Dwgs_User,0.15)
    k.SaveBoard(str(dest/f'{project}.kicad_pcb'), board)
    return dest


def audit_board(path, project, gender):
    b=k.LoadBoard(str(path))
    errors=[]; rows=[]
    fps={fp.GetReference():fp for fp in b.GetFootprints()}
    assert set(fps)=={'J1','J2','J3','J4'},set(fps)
    for n in range(1,24):
        a=fps['J1'].FindPadByNumber(str(n)); z=fps['J2'].FindPadByNumber(str(n))
        x,y=xy(n,gender)
        assert a and z
        assert a.GetNetname()==z.GetNetname()=='/'+nname(n)
        assert a.GetNetCode()==z.GetNetCode()
        actual=(k.ToMM(z.GetPosition().x)-ORIGIN[0],k.ToMM(z.GetPosition().y)-ORIGIN[1])
        assert math.dist(actual,(x,y))<0.000002,(n,actual,(x,y))
        nodes=[(fp.GetReference(),p.GetNumber()) for fp in fps.values() for p in fp.Pads() if p.GetNetname()=='/'+nname(n)]
        assert sorted(nodes)==[('J1',str(n)),('J2',str(n))],(n,nodes)
        rows.append([project,n,'/'+nname(n),'J1',n,'J2',n,round(x,6),y,'F.Cu' if n<=12 else 'B.Cu'])
    assert len(list(b.GetTracks()))==26
    assert sum(len(list(f.Pads())) for f in fps.values())==50
    assert abs(k.ToMM(b.GetDesignSettings().GetBoardThickness())-P['thickness'])<0.000001
    assert {p.GetNetname() for p in fps['J3'].Pads()}=={'/SHIELD'}
    assert {p.GetNetname() for p in fps['J4'].Pads()}=={'/SHIELD'}
    assert len({fps['J2'].FindPadByNumber(str(n)).GetNetCode() for n in range(1,24)})==23
    return rows


def audit_silk(board):
    """Use actual stroke geometry, not KiCad's padded generic text box.

    The latter includes extra line-height space and can extend beyond the
    board even when the physical strokes remain within it.
    """
    polygon=P['outline_xy']
    def inside(point):
        x,y=point; result=False
        for a,b in zip(polygon,polygon[1:]+polygon[:1]):
            if (a[1]>y)!=(b[1]>y) and x<(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]:
                result=not result
        return result
    def distance_to_edge(point,a,b):
        dx,dy=b[0]-a[0],b[1]-a[1]
        t=max(0,min(1,((point[0]-a[0])*dx+(point[1]-a[1])*dy)/(dx*dx+dy*dy)))
        return math.dist(point,(a[0]+t*dx,a[1]+t*dy))
    records=[]
    for text in board.GetDrawings():
        if not isinstance(text,k.PCB_TEXT) or text.GetLayer() not in(k.F_SilkS,k.B_SilkS):continue
        shape=text.GetEffectiveTextShape();rect=shape.BBox()
        x0,x1=k.ToMM(rect.GetLeft())-ORIGIN[0],k.ToMM(rect.GetRight())-ORIGIN[0]
        y0,y1=k.ToMM(rect.GetTop())-ORIGIN[1],k.ToMM(rect.GetBottom())-ORIGIN[1]
        corners=[(x0,y0),(x1,y0),(x1,y1),(x0,y1)]
        assert all(inside(pt) for pt in corners),(text.GetText(),corners)
        clearance=min(distance_to_edge(pt,a,b) for pt in corners for a,b in zip(polygon,polygon[1:]+polygon[:1]))
        records.append({'text':text.GetText(),'layer':text.GetLayerName(),
                        'actual_stroke_bounds_mm':[round(x0,6),round(y0,6),round(x1,6),round(y1,6)],
                        'conservative_edge_clearance_mm':round(clearance,6)})
    return {'text_items_checked':len(records),'all_actual_strokes_within_outline':True,
            'minimum_conservative_edge_clearance_mm':min(x['conservative_edge_clearance_mm'] for x in records),
            'items':records}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kicad-cli', default=shutil.which('kicad-cli'), help='KiCad CLI for schematic/plot exports; optional')
    args=parser.parse_args()
    verification=ROOT/'verification';verification.mkdir(exist_ok=True)
    allrows=[]
    results={}
    geometry={}
    for project,gender,label in PROJECTS:
        dest=build(project,gender,label)
        # Reload the saved files: checks concern what a recipient opens.
        allrows.extend(audit_board(dest/f'{project}.kicad_pcb',project,gender))
        b=k.LoadBoard(str(dest/f'{project}.kicad_pcb'))
        geometry[project]=audit_silk(b)
        configure_rules(b)
        rpt=verification/f'{project}-drc.rpt'
        ok=k.WriteDRCReport(b,str(rpt),k.EDA_UNITS_MILLIMETRES,True)
        report=rpt.read_text()
        drc=int(re.search(r'Found (\d+) DRC violations',report).group(1))
        unconnected=int(re.search(r'Found (\d+) unconnected pads',report).group(1))
        footprint_errors=int(re.search(r'Found (\d+) Footprint errors',report).group(1))
        results[project]={'saved_board_reloaded':True,'mapping_assertions_passed':True,'native_drc_report_written':bool(ok),'drc_violations':drc,'unconnected_pads':unconnected,'footprint_errors':footprint_errors,'report':str(rpt.relative_to(ROOT))}
        if args.kicad_cli:
            sch=dest/f'{project}.kicad_sch'
            netlist=verification/f'{project}-netlist.xml'
            subprocess.run([args.kicad_cli,'sch','export','netlist','--format','kicadxml','-o',str(netlist),str(sch)],check=True)
            subprocess.run([args.kicad_cli,'sch','export','pdf','-o',str(verification/f'{project}-schematic.pdf'),str(sch)],check=True)
            xml=ET.parse(netlist)
            exported={n.attrib['name']:{(v.attrib['ref'],v.attrib['pin']) for v in n.findall('node')} for n in xml.findall('./nets/net')}
            expected={'/'+nname(n):{('J1',str(n)),('J2',str(n))} for n in range(1,24)}
            expected['/SHIELD']={('J3','1'),('J3','2'),('J4','1'),('J4','2')}
            assert exported==expected, (project,exported)
            results[project]['native_schematic_netlist_matches_board']=True
            results[project]['native_erc']='Not run: KiCad 7 CLI does not expose ERC; parser and exact exported netlist were checked instead.'
            out=ROOT/'fabrication'/'FIT-PROTOTYPE'/project
            out.mkdir(parents=True,exist_ok=True)
            if drc==unconnected==footprint_errors==0:
                pcb=dest/f'{project}.kicad_pcb'
                subprocess.run([args.kicad_cli,'pcb','export','gerbers','--layers','F.Cu,B.Cu,F.Mask,B.Mask,F.SilkS,B.SilkS,Edge.Cuts','--subtract-soldermask','-o',str(out)+'/',str(pcb)],check=True)
                subprocess.run([args.kicad_cli,'pcb','export','drill','--format','excellon','--excellon-units','mm','--excellon-separate-th','-o',str(out)+'/',str(pcb)],check=True)
                plot=ROOT/'previews'/'native';plot.mkdir(parents=True,exist_ok=True)
                for side in ('F','B'):
                    command=[args.kicad_cli,'pcb','export','svg','--layers',f'{side}.Cu,{side}.Mask,{side}.SilkS,Edge.Cuts','--page-size-mode','2','--exclude-drawing-sheet','-o',str(plot/f'{project}-{side}.svg'),str(pcb)]
                    if side=='B':command.insert(-1,'--mirror')
                    subprocess.run(command,check=True)
            # Native CLI normalises projects using its session defaults. Restore
            # the documented editable project rules after those exports.
            (dest/f'{project}.kicad_pro').write_text(json.dumps(project_config(project),indent=2)+'\n')
            for cache in dest.glob('*.kicad_prl'):cache.unlink()
        print(project,'generated, loaded and audited; DRC report:',rpt)
    with (verification/'pin-map.csv').open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['project','amiga_pin','net','cup_reference','cup_pad','tail_reference','tail_pad','x_mm','y_mm','routed_layer']);writer.writerows(allrows)
    (verification/'pcb-build-summary.json').write_text(json.dumps({'tool_version':k.GetBuildVersion(),'revision':PARAMS['revision'],'results':results},indent=2)+'\n')
    (verification/'pcb-geometry-review.json').write_text(json.dumps({'tool_version':k.GetBuildVersion(),'revision':REV,'projects':geometry},indent=2)+'\n')


if __name__=='__main__':main()
