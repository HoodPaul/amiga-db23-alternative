#!/usr/bin/env python3
"""Read-only portable audit of the saved KiCad boards and exported netlists.

No KiCad installation or pip dependencies are needed. This complements the
native DRC reports; it is not an ERC or physical fit/continuity test.
"""
from pathlib import Path
import json
import math
import re
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
PARAMS=json.loads((ROOT/'source/design_parameters.json').read_text())
P=PARAMS['pcb'];M=PARAMS['motherboard']
ORIGIN=(150.0,80.0)
CHECKS=0


def check(condition, message):
    global CHECKS
    CHECKS+=1
    if not condition:raise AssertionError(message)


def parse(text):
    tokens=re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',text)
    stack=[];root=None
    for token in tokens:
        if token=='(':
            n=[]
            if stack:stack[-1].append(n)
            else:
                if root is not None:raise AssertionError('Multiple S-expression roots')
                root=n
            stack.append(n)
        elif token==')':
            if not stack:raise AssertionError('Unmatched close parenthesis')
            stack.pop()
        else:
            if not stack:raise AssertionError('Token outside root')
            stack[-1].append(json.loads(token) if token.startswith('"') else token)
    if stack:raise AssertionError('Unclosed S-expression')
    return root


def children(node,name):return [n for n in node if isinstance(n,list) and n and n[0]==name]
def child(node,name):return next((n for n in node if isinstance(n,list) and n and n[0]==name),None)
def almost(a,b):return abs(float(a)-float(b))<0.000002
def pair(node,name):return tuple(map(float,child(node,name)[1:3]))


def audit(project,gender):
    start=CHECKS
    board=parse((ROOT/'pcb'/project/f'{project}.kicad_pcb').read_text())
    check(board[0]=='kicad_pcb',f'{project}: wrong file type')
    check(int(child(board,'version')[1])==20221018,f'{project}: expected native KiCad7 PCB format')
    check(almost(child(child(board,'general'),'thickness')[1],P['thickness']),f'{project}: thickness')
    netnames={n[1]:n[2] for n in children(board,'net')}
    check(set(netnames.values())=={''}|{f'/P{n:02d}' for n in range(1,24)}|{'/SHIELD'},f'{project}: net set')
    fps={child(fp,'fp_text')[2]:fp for fp in children(board,'footprint')}
    check(set(fps)=={'J1','J2','J3','J4'},f'{project}: footprint references')
    pads={ref:{n[1]:n for n in children(fp,'pad')} for ref,fp in fps.items()}
    check([len(pads[r]) for r in ('J1','J2','J3','J4')]==[23,23,2,2],f'{project}: pad counts')
    for ref,fp in fps.items():
        check(pair(fp,'at')==ORIGIN,f'{project}: unexpected footprint translation')
    tracks=children(board,'segment')
    check(len(tracks)==26,f'{project}: track count')
    check(not children(board,'via'),f'{project}: expected no vias')
    check(not children(board,'zone'),f'{project}: no copper pours joining contacts')
    cup_y=P['cup_pad_front_y']+P['cup_pad_length']/2
    for n in range(1,24):
        nn=str(n);name=f'/P{n:02d}'
        x=(6.5-n)*M['pin_pitch'] if n<=12 else (18-n)*M['pin_pitch']
        if gender=='F':x=-x
        y=M['rear_row_y'] if n<=12 else M['front_row_y']
        a,z=pads['J1'][nn],pads['J2'][nn]
        check(all(almost(v,w) for v,w in zip(pair(a,'at'),(x,cup_y))),f'{project}: cup {n} position')
        check(all(almost(v,w) for v,w in zip(pair(z,'at'),(x,y))),f'{project}: tail {n} position')
        check(child(a,'net')[2]==child(z,'net')[2]==name,f'{project}: pin {n} net mismatch')
        check(a[2]=='smd' and z[2]=='thru_hole',f'{project}: pin {n} types')
        check(almost(child(z,'drill')[1],P['tail_drill']),f'{project}: pin {n} drill')
        check(pair(z,'size')==(P['tail_pad_diameter'],P['tail_pad_diameter']),f'{project}: pin {n} pad size')
        check(pair(a,'size')==(P['cup_pad_width'],P['cup_pad_length']),f'{project}: pin {n} cup size')
        layer='F.Cu' if n<=12 else 'B.Cu'
        check(child(a,'layers')[1:]==[layer,('F.Mask' if n<=12 else 'B.Mask')],f'{project}: pin {n} cup layers')
        routed=[t for t in tracks if netnames[child(t,'net')[1]]==name]
        check(len(routed)==1,f'{project}: pin {n} route count')
        t=routed[0]
        check(child(t,'layer')[1]==layer and almost(child(t,'width')[1],P['track_width']),f'{project}: pin {n} route layer/width')
        ends=[pair(t,'start'),pair(t,'end')]
        expected=[(ORIGIN[0]+x,ORIGIN[1]+cup_y),(ORIGIN[0]+x,ORIGIN[1]+y)]
        check(all(math.dist(v,w)<0.000002 for v,w in zip(ends,expected)),f'{project}: pin {n} route endpoints')
        all_nodes=[(ref,pad[1]) for ref,fp in fps.items() for pad in children(fp,'pad') if child(pad,'net')[2]==name]
        check(sorted(all_nodes)==[('J1',nn),('J2',nn)],f'{project}: pin {n} merged/extra nodes')
    for n,x in [('1',-P['shield_pad_x']),('2',P['shield_pad_x'])]:
        pad=pads['J3'][n]
        check(pair(pad,'at')==(x,P['shield_pad_y']),f'{project}: shield {n} position')
        check(child(pad,'net')[2]=='/SHIELD',f'{project}: shield {n} net')
        check(almost(abs(x),M['anchor_spacing']/2) and almost(P['shield_pad_y'],M['anchor_y']),f'{project}: mounting hole {n} original motherboard alignment')
        check(pad[2]=='thru_hole' and almost(child(pad,'drill')[1],P['shield_pad_drill']),f'{project}: mounting hole {n} type and drill')
        check(pair(pad,'size')==(P['shield_pad_diameter'],P['shield_pad_diameter']),f'{project}: mounting land {n} size')
    for n,x in [('1',-P['shell_bond_pad_x']),('2',P['shell_bond_pad_x'])]:
        pad=pads['J4'][n]
        check(pair(pad,'at')==(x,P['shell_bond_pad_y']),f'{project}: shell bond {n} position')
        check(child(pad,'net')[2]=='/SHIELD',f'{project}: shell bond {n} net')
        check(pad[2]=='thru_hole' and almost(child(pad,'drill')[1],P['shell_bond_pad_drill']),f'{project}: shell bond {n} type and drill')
        check(pair(pad,'size')==(P['shell_bond_pad_diameter'],P['shell_bond_pad_diameter']),f'{project}: shell bond land {n} size')
    shield_tracks=[t for t in tracks if netnames[child(t,'net')[1]]=='/SHIELD']
    check(len(shield_tracks)==3,f'{project}: shield route count')
    actual_shield={(child(t,'layer')[1],pair(t,'start'),pair(t,'end'),float(child(t,'width')[1])) for t in shield_tracks}
    expected_shield={('B.Cu',(ORIGIN[0]-P['shield_pad_x'],ORIGIN[1]+P['shield_track_y']),
                     (ORIGIN[0]+P['shield_pad_x'],ORIGIN[1]+P['shield_track_y']),P['shield_track_width'])}
    for side in(-1,1):
        expected_shield.add(('F.Cu',(ORIGIN[0]+side*P['shell_bond_pad_x'],ORIGIN[1]+P['shell_bond_pad_y']),
                            (ORIGIN[0]+side*P['shield_pad_x'],ORIGIN[1]+P['shield_pad_y']),P['shield_track_width']))
    check(actual_shield==expected_shield,f'{project}: SHIELD route geometry/layers/width')
    row_gap=min(P['shield_track_y']-M['front_row_y'],M['rear_row_y']-P['shield_track_y'])-P['tail_pad_diameter']/2-P['shield_track_width']/2
    check(row_gap>=P['clearance'],f'{project}: SHIELD crossbar clears both signal-pad rows')
    outline=P['outline_xy']
    edges=[s for s in children(board,'gr_line') if child(s,'layer')[1]=='Edge.Cuts']
    check(len(edges)==len(outline),f'{project}: outline segment count')
    actual={tuple(sorted([pair(s,'start'),pair(s,'end')])) for s in edges}
    expected={tuple(sorted([(ORIGIN[0]+a[0],ORIGIN[1]+a[1]),(ORIGIN[0]+b[0],ORIGIN[1]+b[1])])) for a,b in zip(outline,outline[1:]+outline[:1])}
    check(actual==expected,f'{project}: outline geometry')
    xml=ET.parse(ROOT/'verification'/f'{project}-netlist.xml')
    exported={n.attrib['name']:{(v.attrib['ref'],v.attrib['pin']) for v in n.findall('node')} for n in xml.findall('./nets/net')}
    expected={f'/P{n:02d}':{('J1',str(n)),('J2',str(n))} for n in range(1,24)}
    expected['/SHIELD']={('J3','1'),('J3','2'),('J4','1'),('J4','2')}
    check(exported==expected,f'{project}: schematic exported topology')
    for comp in xml.findall('./components/comp'):
        ref=comp.attrib['ref']
        check(comp.findtext('footprint')==fps[ref][1],f'{project}: {ref} footprint identifier')
        check(child(fps[ref],'path')[1]=='/'+comp.findtext('tstamps'),f'{project}: {ref} schematic UUID link')
    drc=(ROOT/'verification'/f'{project}-drc.rpt').read_text()
    for s in ('Found 0 DRC violations','Found 0 unconnected pads','Found 0 Footprint errors'):
        check(s in drc,f'{project}: native DRC not clean: {s}')
    return {'status':'PASS','design_checks':CHECKS-start,'signal_nets':23,'shield_nets':1,'pads':50,'tracks':26,'vias':0,'mounting_holes_at_original_shell_anchors':True,'shield_crossbar_minimum_row_clearance_mm':round(row_gap,3),'native_drc_violations':0,'native_unconnected_pads':0,'native_footprint_errors':0}


def main():
    result={name:audit(name,g) for name,g in [('DB23M_RGB','M'),('DB23F_Floppy','F')]}
    print(json.dumps({'revision':PARAMS.get('pcb_revision',PARAMS['revision']),'design_checks':CHECKS,'projects':result},indent=2))


if __name__=='__main__':main()
