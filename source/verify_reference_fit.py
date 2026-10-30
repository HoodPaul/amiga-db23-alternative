#!/usr/bin/env python3
"""Recheck saved adapter/print alignment against recorded reference geometry.

The original reference-board copper findings remain in the JSON record. This
script verifies that exact source file's hash, parses both saved adapter boards,
and rechecks the current STEP and outline against the recorded CN175 drill
coordinate. It does not re-extract the historic copper/track screen or establish
physical component, solder-fillet or chassis clearance. Requires CadQuery.
"""
from pathlib import Path
import argparse, hashlib, json, math
import cadquery as cq
import verify_pcb as native

ROOT=Path(__file__).resolve().parents[1]
PARAMS=json.loads((ROOT/'source/design_parameters.json').read_text())
B=PARAMS['pcb'];H=PARAMS['holder'];M=PARAMS['motherboard'];R=PARAMS['revision']
RECORD=ROOT/'verification/motherboard-reference-fit.json'
record=json.loads(RECORD.read_text())
checks={}

def check(name,ok,details=True):
    checks[name]={'passed':bool(ok),'details':details}
    if not ok:raise AssertionError(f'{name}: {details}')

def zc(x,y,d,z0,z1):return cq.Solid.makeCylinder(d/2,z1-z0,cq.Vector(x,y,z0))
def zero(a,b):return a.intersect(b).Volume()
def qpair(v):return tuple(round(float(a),6) for a in v)
def native_pair(node,name):return tuple(map(float,native.child(node,name)[1:3]))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--reference-board',type=Path,default=ROOT.parent/'a4000-replica.kicad_pcb',help='Exact external reference board identified by the stored SHA-256')
    args=ap.parse_args()
    if not args.reference_board.is_file():raise FileNotFoundError('Supply the external reference file with --reference-board; its stored SHA-256 must match.')
    digest=sha(args.reference_board)
    check('reference_source_SHA256_unchanged',digest==record['source_sha256'],digest)
    holder=cq.importers.importStep(str(ROOT/f'mechanical/DB23_Holder_v{R}.step')).val()
    cap=cq.importers.importStep(str(ROOT/f'mechanical/DB23_Cap_v{R}.step')).val()
    neighbour=record['neighbour_projection'];nx,ny=neighbour['centre_assembly_xy_mm'];dd=neighbour['drill_diameter_mm'];pd=neighbour['copper_pad_diameter_mm']
    cyl=zc(nx,ny,dd,-1,20);pad_cyl=zc(nx,ny,pd,-1,20)
    steps={};projects={};sets=[]
    for label,s in [('base',holder),('cap',cap)]:
        check(label+'_STEP_valid_one_solid',s.isValid() and len(s.Solids())==1)
        v=zero(s,cyl);gap=s.distance(cyl);pad_gap=s.distance(pad_cyl);pad_overlap=zero(s,pad_cyl)
        check(label+'_reference_drill_cylinder_clear',v<1e-6,v)
        check(label+'_positive_reference_drill_gap',gap>0,gap)
        steps[label]={'intersection_with_reference_drill_cylinder_mm3':round(v,8),'minimum_distance_to_reference_drill_cylinder_mm':round(gap,6),'intersection_with_reference_copper_pad_cylinder_mm3':round(pad_overlap,8),'minimum_distance_to_reference_copper_pad_cylinder_mm':round(pad_gap,6)}
    z=B['bottom_z'];t=B['thickness']
    outline=cq.Workplane('XY').polyline(B['outline_xy']).close().extrude(t).translate((0,0,z)).val()
    outline_v=zero(outline,cyl);outline_gap=outline.distance(cyl);outline_pad_gap=outline.distance(pad_cyl)
    for project,gender in [('DB23M_RGB','M'),('DB23F_Floppy','F')]:
        pcb_path=ROOT/'pcb'/project/f'{project}.kicad_pcb';board=native.parse(pcb_path.read_text())
        fps={native.child(fp,'fp_text')[2]:fp for fp in native.children(board,'footprint')}
        origin=(150.0,80.0)
        check(project+'_origin_and_thickness',all(native_pair(f,'at')==origin for f in fps.values()) and abs(float(native.child(native.child(board,'general'),'thickness')[1])-t)<1e-6)
        pads={ref:{p[1]:p for p in native.children(fp,'pad')} for ref,fp in fps.items()}
        edges=[s for s in native.children(board,'gr_line') if native.child(s,'layer')[1]=='Edge.Cuts']
        actual={tuple(sorted([qpair((p[0]-origin[0],p[1]-origin[1])) for p in [native_pair(e,'start'),native_pair(e,'end')]])) for e in edges}
        expected={tuple(sorted([qpair(a),qpair(b)])) for a,b in zip(B['outline_xy'],B['outline_xy'][1:]+B['outline_xy'][:1])}
        check(project+'_native_outline_matches_contract',actual==expected and len(edges)==len(expected))
        positions=[];all_grid=True;max_bore=0
        for n in range(1,24):
            p=pads['J2'][str(n)];x,y=native_pair(p,'at');positions.append(qpair((x,y)))
            ex=(6.5-n)*M['pin_pitch'] if n<=12 else(18-n)*M['pin_pitch']
            if gender=='F':ex=-ex
            ey=M['rear_row_y'] if n<=12 else M['front_row_y']
            all_grid=all_grid and math.dist((x,y),(ex,ey))<2e-6 and abs(float(native.child(p,'drill')[1])-B['tail_drill'])<1e-6
            v=zero(holder,zc(x,y,H['pin_guide_hole_diameter']-.002,H['bottom_clearance']-.01,H['pin_block_top_z']+.01));max_bore=max(max_bore,v)
            check(project+f'_native_tail_guide_{n:02d}',v<1e-6,round(v,9))
        check(project+'_all_native_tails_match_nominal_grid',all_grid)
        sets.append(set(positions));mounts=[];max_mount=0
        for n,side in [('1',-1),('2',1)]:
            p=pads['J3'][n];x,y=native_pair(p,'at');mounts.append([x,y]);v=zero(holder,zc(x,y,B['shield_pad_drill']-.002,-.01,z+.01));max_mount=max(max_mount,v)
            check(project+f'_native_mount_{n}',math.dist((x,y),(side*M['anchor_spacing']/2,M['anchor_y']))<2e-6 and abs(float(native.child(p,'drill')[1])-B['shield_pad_drill'])<1e-6 and v<1e-6,round(v,9))
        bonds=[];max_fillet=0
        for n,side in [('1',-1),('2',1)]:
            p=pads['J4'][n];x,y=native_pair(p,'at');bonds.append([x,y]);v=zero(holder,zc(x,y,B['shell_bond_pad_diameter'],z-.75,z));max_fillet=max(max_fillet,v)
            check(project+f'_native_J4_fillet_{n}',math.dist((x,y),(side*B['shell_bond_pad_x'],B['shell_bond_pad_y']))<2e-6 and abs(float(native.child(p,'drill')[1])-B['shell_bond_pad_drill'])<1e-6 and v<1e-6,round(v,9))
        check(project+'_outline_reference_drill_clear',outline_v<1e-6 and outline_gap>0,{'overlap_mm3':round(outline_v,9),'gap_mm':round(outline_gap,6)})
        projects[project]={'signal_guides_checked_from_saved_native_centres':23,'all_native_tail_positions_match_nominal_grid':all_grid,'max_bore_probe_intersection_mm3':round(max_bore,9),'signal_drill_mm':B['tail_drill'],'mount_bores_checked_from_saved_native_centres':2,'mounting_xy_mm':mounts,'adapter_mount_drill_mm':B['shield_pad_drill'],'max_mount_probe_intersection_mm3':round(max_mount,9),'J4_fillets_checked_from_saved_native_centres':2,'J4_xy_mm':bonds,'J4_drill_mm':B['shell_bond_pad_drill'],'J4_fillet_probe_envelope':'Diameter2.4mm,0.75mm belowPCBunderside','max_J4_probe_intersection_mm3':round(max_fillet,9),'outline_vertices':len(edges),'outline_matches_shared_parameters':True,'footprint_to_assembly_origin_verified_mm':list(origin),'native_PCB_SHA256':sha(pcb_path)}
    check('both_variants_same_geometric_tail_set',sets[0]==sets[1])
    steps['adapter_outline_solid']={'intersection_with_reference_drill_cylinder_mm3':round(outline_v,9),'minimum_distance_to_reference_drill_cylinder_mm':round(outline_gap,6),'minimum_distance_to_reference_copper_pad_cylinder_mm':round(outline_pad_gap,6)}
    neighbour['note']='Current saved STEP/outline check against the recorded CN175 drill and copper-pad cylinders; no actual metal lug, solder fillet or housing height is modelled. Copper-pad cylinder overlap is recorded separately and is not a physical collision result.'
    neighbour['adapter_outline_vertices']=len(B['outline_xy'])
    neighbour['actual_delivered_STEP_and_adapter_outline_checks']=steps
    # Remove obsolete literal-polyline results when the design uses a different boundary.
    for key in list(neighbour):
        if key.startswith('base_cap_') or key in ('adapter_nearest_outline_point_mm','adapter_gap_to_reference_drill_circle_mm','adapter_gap_to_reference_copper_pad_circle_mm'):neighbour.pop(key)
    record['native_adapter_to_print_alignment']={'status':'PASS','checks_passed':len(checks),'both_variants_same_geometric_tail_set':True,'scope':'Current saved native adapter boards and delivered STEP, plus source-file hash verification. Recorded historic copper-screen results are retained without re-extraction. Nominal drill cylinders are not measured component bodies.','projects':projects,'checks':checks,'checker':'source/verify_reference_fit.py','source_SHA256_reverified':True,'reviewed_STEP_SHA256':{name:sha(ROOT/f'mechanical/{name}_v{R}.step') for name in ('DB23_Holder','DB23_Cap')}}
    RECORD.write_text(json.dumps(record,indent=2)+'\n')
    xend=H.get('forward_end_outer_x',H['overall_width']/2)
    gap=steps['base']['minimum_distance_to_reference_drill_cylinder_mm'];cap_gap=steps['cap']['minimum_distance_to_reference_drill_cylinder_mm']
    # The signed planar pad gap at the nearest square front corner explains why
    # a passing drill envelope still cannot certify the neighbouring solder area.
    cy=H.get('outer_relief_front_y',5.1)
    signed_pad_gap=math.hypot(nx-xend,ny-cy)-pd/2
    md=f'''# Reference motherboard fit screen\n\nProject development: **Paul of UK Computing Limited**, **Jon of JMC Electronics** and **AI assistance through Codex**.\n\nThis is a limited comparison with the locally retained [A4000 replica KiCad board]({record['source_url']}). It is not a physical fit result, clearance certificate or substitute for measurements of the target motherboard. The source file is not republished here. Its exact SHA-256 and retained copper-screen findings are in [motherboard-reference-fit.json](motherboard-reference-fit.json).\n\n## Reproducible current checks\n\nThe current saved boards and STEP files pass **{len(checks)} checks**, run with:\n\n```sh\npython3 source/verify_reference_fit.py --reference-board /path/to/A4k-Replica-Acill.kicad_pcb\n```\n\nThe helper requires CadQuery and the exact external source file identified by the stored SHA-256. It verifies that source hash, directly parses both saved adapter boards and rechecks their bores, J4 fillet clearances, outlines and the current base/cap STEP. Historic reference-board copper findings are retained rather than re-extracted; this limitation is explicit in the machine-readable report.\n\n## Nominal mounting positions\n\nThe source CN450 RGB and CN352 floppy anchor line lies 0.1524 mm behind the midpoint of the source signal rows, with 44.2976 mm anchor spacing and 3.175 mm anchor drills. The sourced iComp contract uses 44.2700 mm spacing and nominal 3.20 mm motherboard drills. The replacement retains iComp centres and uses Ø3.30 mm adapter holes. Under ideal circular-hole assumptions, the reference/adapter radial allowance for a nominal M3 shank is 0.2375 mm versus about 0.1530 mm axis eccentricity; real tolerances and physical fit remain unverified. Do not enlarge or countersink the motherboard.\n\n## Underside screw heads\n\nThe unchanged source-board screen records a bare Ø7 mm head overlapping a foreign CN450 bottom-copper trace by 0.2107 mm in plan; the nearest recorded CN352 foreign trace has only 0.0369 mm nominal gap. Mask condition and actual exposed metal are not established. The default Ø8 × 0.50 mm underside insulating washers and deliberate motherboard shell-ground wire therefore remain required. Verify actual coverage, bearing, components and chassis clearance; do not rely on bolt contact for grounding.\n\n## Revised square end faces and neighbouring connector\n\nThe recorded CN175 mounting pad is centred at X26.797, Y5.7916, with a Ø2.3622 mm drill and Ø3.175 mm copper land. The strengthened forward ends now use one uniform outer face at X±25.60 through Y5.10. The aft local relief then reduces the outer edge to X±25.00 until Y7.50. PCB ears remain unchanged: X±25.00 at Y6.00–7.50 and X±25.60 behind it.\n\n| Current saved shape | Gap to reference drill cylinder | Drill-cylinder intersection |\n|---|---:|---:|\n| Base | {gap:.6f} mm | {steps['base']['intersection_with_reference_drill_cylinder_mm3']:.6f} mm³ |\n| Cap | {cap_gap:.6f} mm | {steps['cap']['intersection_with_reference_drill_cylinder_mm3']:.6f} mm³ |\n| Adapter outline | {outline_gap:.6f} mm | {outline_v:.6f} mm³ |\n\nThe closest square end corner has a signed planar gap to the copper-pad circle of approximately **{signed_pad_gap:.6f} mm**. A negative value means projected overlap with the ground land, not a proven collision or electrical contact: the printed parts are insulating and the actual lug, solder fillet and housing heights are not modelled. This is an explicit physical fit check for the target motherboard. Do not interpret a clear drill cylinder as proof of clearance to the complete neighbouring connector.\n\n## Saved adapter-to-print alignment\n\nFor each gender, 23 guide probes, two mounting-bore probes and two conservative J4 underside-fillet probes clear the delivered base. Native tail positions match the nominal grid, both variants retain the same geometric tail set, and all 16 outline segments match the shared contract. The J4 probe is Ø2.40 mm and extends 0.75 mm below the adapter PCB. These are saved-file alignment checks, not actual solder-fillet or print-fit measurements.\n\nThe photographs identify the CN450 area but do not establish exact depth or height clearance. Record the real motherboard revision, neighbouring metal and solder geometry, fastener stack and case fit in the measurement worksheet.\n'''
    (ROOT/'verification/motherboard-reference-fit.md').write_text(md)
    print(json.dumps({'checks_passed':len(checks),'neighbour_gaps_mm':{'base':gap,'cap':cap_gap,'adapter':round(outline_gap,6)},'report':str(RECORD)},indent=2))

if __name__=='__main__':main()
