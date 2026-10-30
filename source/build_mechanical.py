#!/usr/bin/env python3
"""Build the v0.5 DB23 fit-prototype base, clip-on cap and loading aids.

One constructive geometry description generates editable OpenSCAD and analytic
CadQuery STEP. OpenSCAD is the printable STL route. Purchased parts remain
unmeasured reference envelopes; geometry checks do not establish print strength.
"""
from pathlib import Path
import argparse, json, math, subprocess, re, struct, collections
import cadquery as cq
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'mechanical';OUT.mkdir(exist_ok=True)
P=json.loads((ROOT/'source/design_parameters.json').read_text())
H=P['holder'];B=P['pcb'];M=P['motherboard'];C=P['cap'];J=P['pin_height_jig'];A=P['mounting'];R=P['revision']
AX=M['anchor_spacing']/2; AY=M['anchor_y']; EPS=.03
PINS=[(i*M['pin_pitch']-5.5*M['pin_pitch'],M['rear_row_y']) for i in range(12)]
PINS += [(i*M['pin_pitch']-5*M['pin_pitch'],M['front_row_y']) for i in range(11)]

def box(x0,x1,y0,y1,z0,z1):return ('box',[x0,x1,y0,y1,z0,z1])
def zc(x,y,d,z0,z1):return ('zc',[x,y,d,z0,z1])
def yc(x,z,d,y0,y1):return ('yc',[x,z,d,y0,y1])
def px(x0,x1,pts):return ('px',[x0,x1,pts])
def py(y0,y1,pts):return ('py',[y0,y1,pts])
def union(*nodes):return ('union',list(nodes))
def cut(node,*tools):return ('cut',[node,*tools])
def tx(node,x=0,y=0,z=0,rx=0):return ('tx',[node,x,y,z,rx])
def textnode(s,x,y,z,size):return ('text',[s,x,y,z,size])
def scad(n,depth=0):
 op,a=n;indent=' '*depth
 if op=='box':
  x0,x1,y0,y1,z0,z1=a;return f'{indent}translate({[x0,y0,z0]}) cube({[x1-x0,y1-y0,z1-z0]});\n'
 if op=='zc':
  x,y,d,z0,z1=a;return f'{indent}translate({[x,y,z0]}) cylinder(d={d},h={z1-z0});\n'
 if op=='yc':
  x,z,d,y0,y1=a;return f'{indent}translate({[x,y0,z]}) rotate([-90,0,0]) cylinder(d={d},h={y1-y0});\n'
 if op=='px':
  x0,x1,pts=a;return f'{indent}translate({[x0,0,0]}) rotate([90,0,90]) linear_extrude({x1-x0}) polygon({json.dumps(pts)});\n'
 if op=='py':
  y0,y1,pts=a;return f'{indent}translate({[0,y1,0]}) rotate([90,0,0]) linear_extrude({y1-y0}) polygon({json.dumps(pts)});\n'
 if op in ('union','cut'):
  return indent+('union' if op=='union' else 'difference')+'(){\n'+''.join(scad(c,depth+1) for c in a)+indent+'}\n'
 if op=='tx':
  node,x,y,z,rx=a;return f'{indent}translate({[x,y,z]}) rotate({[rx,0,0]}) {{\n'+scad(node,depth+1)+indent+'}\n'
 if op=='text':
  s,x,y,z,size=a;return f'{indent}translate({[x,y,z]}) linear_extrude(.36) text({json.dumps(s)},size={size},halign="center",valign="center",font="DejaVu Sans:style=Bold");\n'
 raise ValueError(op)
def shape(n):
 op,a=n
 if op=='box':
  x0,x1,y0,y1,z0,z1=a;return cq.Solid.makeBox(x1-x0,y1-y0,z1-z0,cq.Vector(x0,y0,z0))
 if op=='zc':
  x,y,d,z0,z1=a;return cq.Solid.makeCylinder(d/2,z1-z0,cq.Vector(x,y,z0))
 if op=='yc':
  x,z,d,y0,y1=a;return cq.Solid.makeCylinder(d/2,y1-y0,cq.Vector(x,y0,z),cq.Vector(0,1,0))
 if op in ('px','py'):
  q0,q1,pts=a
  vec=[cq.Vector(q0,y,z) for y,z in pts] if op=='px' else[cq.Vector(x,q0,z) for x,z in pts]
  w=cq.Wire.makePolygon(vec+[vec[0]])
  return cq.Solid.extrudeLinear(w,[],cq.Vector(q1-q0,0,0) if op=='px' else cq.Vector(0,q1-q0,0))
 if op=='union':
  vals=[shape(c) for c in a];return vals[0].fuse(*vals[1:]).clean()
 if op=='cut':return shape(a[0]).cut(*[shape(c) for c in a[1:]]).clean()
 if op=='tx':
  node,x,y,z,rx=a;s=shape(node)
  if rx:s=s.rotate((0,0,0),(1,0,0),rx)
  return s.translate((x,y,z))
 raise ValueError(op)

def holder():
 hw=H['overall_width']/2;bz=H['bottom_clearance'];pb=H['pin_block_width']/2
 add=[box(-pb,pb,H['pin_block_front_y'],H['pin_block_rear_y'],bz,H['pin_block_top_z']),box(-25.6,25.6,H['rear_infill_front_y'],H['rear_y'],bz,B['bottom_z'])]
 sub=[zc(x,y,H['pin_guide_hole_diameter'],bz-EPS,H['pin_block_top_z']+EPS) for x,y in PINS]
 af=H['nut_across_flats_assumed']+H['nut_pocket_clearance'];nt=H['nut_thickness_assumed']+H['nut_pocket_clearance'];ny=H['nut_axis_y_assumed'];nz=H['nut_axis_z']
 for s in (-1,1):
  x0,x1=sorted((s*H['rail_front_inner_x'],s*hw));add.append(box(x0,x1,H['front_y'],H['rail_step_y'],bz,B['bottom_z']))
  x0,x1=sorted((s*H['rail_inner_x'],s*hw));add.append(box(x0,x1,H['rail_step_y'],H['rear_y'],bz,B['bottom_z']))
  x0,x1=sorted((s*H['tower_inner_x'],s*hw));add.append(box(x0,x1,H['front_y'],H['tower_rear_y'],bz,H['tower_top_z']))
  add.append(zc(s*AX,AY,H['foot_diameter'],H['foot_bottom_z'],B['bottom_z']))
  sub.append(zc(s*AX,AY,H['anchor_clearance_diameter'],-EPS,H['tower_top_z']+EPS))
  sub.append(yc(s*AX,nz,H['jackpost_through_diameter'],H['front_y']-EPS,H['jackpost_relief_end_y']))
  pts=[[s*AX+af/math.sqrt(3)*math.cos(math.radians(a)),nz+af/math.sqrt(3)*math.sin(math.radians(a))] for a in range(30,331,60)]
  sub.append(py(ny-nt/2,ny+nt/2,pts))
  sub.append(box(s*AX-af/2,s*AX+af/2,ny-nt/2,ny+nt/2,nz,H['tower_top_z']+EPS))
  sx=s*B['shell_bond_pad_x'];sw=H['shell_relief_width']/2
  sub.append(box(sx-sw,sx+sw,H['shell_relief_front_y'],H['shell_relief_rear_y'],H['shell_relief_floor_z'],B['bottom_z']+EPS))
  x0,x1=sorted((s*H['latch_notch_x_inner'],s*H['latch_notch_x_outer']))
  sub.append(box(x0,x1,H['latch_notch_front_y'],H['latch_notch_rear_y'],H['latch_notch_bottom_z'],H['latch_notch_top_z']))
 # Square each forward end at one continuous outer plane. This fills the
 # former rear-corner notch while retaining full-height neighbour clearance.
 for s in (-1,1):
  x0,x1=sorted((s*H['forward_end_outer_x'],s*(hw+EPS)))
  sub.append(box(x0,x1,H['front_y']-EPS,H['tower_rear_y'],-EPS,H['tower_top_z']+EPS))
 # The local outside relief now starts behind the end tower, not through it.
 for s in (-1,1):
  x0,x1=sorted((s*H['outer_relief_x'],s*(hw+EPS)))
  sub.append(box(x0,x1,H['outer_relief_front_y'],H['outer_relief_rear_y'],-EPS,H['tower_top_z']+EPS))
 gx0,gx1=H['ground_wire_groove_inner_x'],hw+EPS
 sub.append(box(gx0,gx1,AY-H['ground_wire_groove_width']/2,AY+H['ground_wire_groove_width']/2,-EPS,H['ground_wire_groove_height']))
 return cut(union(*add),*sub)

def latch(x0,x1):
 # A single 2D outline avoids coincident beam/hook CSG facets in STL export.
 return px(x0,x1,[[C['latch_front_y'],C['roof_bottom_z']+EPS],[C['latch_rear_y'],C['roof_bottom_z']+EPS],[C['latch_rear_y'],C['latch_bottom_z']],[C['latch_front_y'],C['latch_bottom_z']],[C['latch_hook_front_y'],C['latch_hook_ramp_top_z']],[C['latch_hook_front_y'],C['latch_hook_top_z']],[C['latch_front_y'],C['latch_hook_top_z']]])

def cap():
 hw=C['overall_width']/2;rb=C['roof_bottom_z'];rt=C['roof_top_z'];sk=C['skirt_bottom_z'];t=C['side_wall_thickness']
 add=[box(-hw,hw,C['front_y'],C['rear_y'],rb,rt),box(-H['tower_inner_x'],H['tower_inner_x'],C['front_y'],C['front_skirt_rear_y'],C['front_skirt_bottom_z'],rb+EPS),box(-C['rear_central_half_width'],C['rear_central_half_width'],C['rear_wall_front_y'],C['rear_y'],sk,rb+EPS)]
 sub=[]
 af=H['nut_across_flats_assumed']+H['nut_pocket_clearance']-C['tongue_clearance_total'];nt=H['nut_thickness_assumed']+H['nut_pocket_clearance']-C['tongue_clearance_total']
 for s in (-1,1):
  x0,x1=sorted((s*(hw-t),s*hw));add.append(box(x0,x1,C['side_skirt_front_y'],C['rear_y'],sk,rb+EPS))
  sub.append(box(x0-EPS,x1+EPS,C['side_nut_relief_front_y'],C['side_nut_relief_rear_y'],sk-EPS,C['mount_nut_relief_top_z']))
  x0,x1=sorted((s*C['rear_central_half_width'],s*hw));add.append(box(x0,x1,C['rear_wall_front_y'],C['rear_y'],C['mount_nut_relief_top_z'],rb+EPS))
  add.append(box(s*AX-af/2,s*AX+af/2,H['nut_axis_y_assumed']-nt/2,H['nut_axis_y_assumed']+nt/2,C['tongue_bottom_z'],rb+EPS))
  cx=s*C['latch_centre_x'];lx0,lx1=cx-C['latch_width']/2,cx+C['latch_width']/2
  add.append(latch(lx0,lx1))

 for s in(-1,1):
  x0,x1=sorted((s*H['forward_end_outer_x'],s*(hw+EPS)))
  sub.append(box(x0,x1,C['front_y']-EPS,H['tower_rear_y'],sk-EPS,rt+EPS))
  x0,x1=sorted((s*H['outer_relief_x'],s*(hw+EPS)))
  sub.append(box(x0,x1,H['outer_relief_front_y'],H['outer_relief_rear_y'],sk-EPS,rt+EPS))
 return cut(union(*add),*sub)

def jig():
 hw=J['overall_width']/2;stop=J['tip_stop_z'];top=J['support_top_z']
 add=[box(-hw,hw,J['front_y'],J['rear_y'],stop-J['floor_thickness'],stop)]
 for s in(-1,1):
  add.append(zc(s*AX,AY,J['support_foot_diameter'],stop,top))
  add.append(zc(s*AX,AY,J['locating_peg_diameter'],top-EPS,top+J['locating_peg_height']))
 return union(*add)

def coupon():
 tools=[zc(-16.8+i*4.8,5,.75+i*.05,-EPS,3+EPS) for i in range(8)]
 tools += [zc(x,y+5.4,H['pin_guide_hole_diameter'],-EPS,3+EPS) for x,y in PINS]
 add=[cut(box(-21,21,0,22,0,3),*tools)]
 add += [textnode(f'{.75+i*.05:.2f}',-16.8+i*4.8,1.7,2.99,1.3) for i in range(8)]
 add.append(textnode(f'23-PIN GRID  {H["pin_guide_hole_diameter"]}',0,20,2.99,1.65))
 return union(*add)

def clip_coupon_pair():
 # A small cross-section of the actual tower latch and matching cap, exported
 # separately. These preserve latch dimensions but omit metal nut pockets.
 x0=18.6;x1=20.8;tx0=x0;tx1=x1
 base=cut(box(tx0,tx1,2.8,5.1,.6,11),box(H['latch_notch_x_inner'],H['latch_notch_x_outer'],H['latch_notch_front_y'],H['latch_notch_rear_y'],H['latch_notch_bottom_z'],H['latch_notch_top_z']))
 cx=C['latch_centre_x'];lx0=cx-C['latch_width']/2;lx1=cx+C['latch_width']/2
 clip=union(box(tx0,tx1,2.8,6.2,11,12.2),latch(lx0,lx1))
 return tx(base,x=-tx0,y=-2.8,z=-.6),tx(tx(clip,rx=180,z=12.2),x=-tx0,y=6.2)

BASE=holder();CAP=cap();JIG=jig();CBASE,CCAP=clip_coupon_pair()
parts={'holder':BASE,'cap_assembly':CAP,'cap':tx(CAP,rx=180,z=C['print_translate_z']),'pin_height_jig':tx(JIG,z=J['print_z_offset']),'coupon':coupon(),'clip_coupon_base':CBASE,'clip_coupon_cap':CCAP}
header=f'''// DB23 v{R}: FIT PROTOTYPE. CONNECTOR AND PRINT FIT UNMEASURED.
// Generated from source/design_parameters.json by source/build_mechanical.py.
// Holder/STEP coordinates: x across, y rearward, z above motherboard top.
// Cap STL exports roof-down; cap STEP retains assembly coordinates.
// No separate foot shims: integrated feet reach Z0; body remains Z0.60.
// Choose holder, cap, cap_assembly, pin_height_jig, coupon,
// clip_coupon_base or clip_coupon_cap. Default is holder.
part="holder";
$fn=64;
'''
scad_path=OUT/f'DB23_Holder_v{R}.scad'
scad_path.write_text(header+'\n'.join('module '+name+'(){\n'+scad(node,1)+'}\n' for name,node in parts.items())+'\n'+'\n'.join(f'if(part=="{name}") {name}();' for name in parts)+'\n')

def mesh_stats(path):
    """Read STL, validate manifold edges and report connected components/volume."""
    data=path.read_bytes()
    count=struct.unpack('<I',data[80:84])[0] if len(data)>=84 else 0
    tris=[]
    if len(data)==84+50*count:
        for i in range(count):
            vals=struct.unpack('<12fH',data[84+i*50:134+i*50])
            tris.append([tuple(round(q,5) for q in vals[j:j+3]) for j in (3,6,9)])
    else:
        vs=[tuple(round(float(q),5) for q in v) for v in re.findall(rb'vertex\s+([\-+.0-9eE]+)\s+([\-+.0-9eE]+)\s+([\-+.0-9eE]+)',data)]
        tris=[vs[i:i+3] for i in range(0,len(vs),3)]
    edges=collections.Counter()
    graph=collections.defaultdict(set)
    volume=0
    for tri in tris:
        a,b,c=tri
        volume+=(a[0]*(b[1]*c[2]-b[2]*c[1])+a[1]*(b[2]*c[0]-b[0]*c[2])+a[2]*(b[0]*c[1]-b[1]*c[0]))/6
        for v,w in ((a,b),(b,c),(c,a)):
            edges[tuple(sorted((v,w)))]+=1; graph[v].add(w);graph[w].add(v)
    unseen=set(graph); components=0
    while unseen:
        components+=1; todo=[unseen.pop()]
        while todo:
            for w in graph[todo.pop()]:
                if w in unseen: unseen.remove(w);todo.append(w)
    bad=sum(n!=2 for n in edges.values())
    pts=list(graph)
    return dict(triangles=len(tris),nonmanifold_edges=bad,components=components,
                volume_mm3=round(volume,3),
                bounds=[[min(p[i] for p in pts),max(p[i] for p in pts)] for i in range(3)])


stems={'holder':'DB23_Holder','cap':'DB23_Cap','pin_height_jig':'DB23_Pin_Height_Jig','coupon':'DB23_Hole_Fit_Coupon','clip_coupon_base':'DB23_Clip_Fit_Base','clip_coupon_cap':'DB23_Clip_Fit_Cap'}
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--parts',nargs='+',choices=tuple(stems),help='Export only these STL parts; existing other STL files are still topology-checked. Default: all parts.')
args=parser.parse_args()
selected=set(args.parts or stems)
results={'revision':R,'status':'FIT PROTOTYPE; all physical fits and strengths untested'}
for name,stem in stems.items():
 target=OUT/f'{stem}_v{R}.stl'
 if name in selected:
  run=subprocess.run(['openscad','--export-format','binstl','-o',str(target),'-D',f'part="{name}"',str(scad_path)],capture_output=True,text=True,check=True)
 elif not target.exists():
  raise RuntimeError(f'Unselected part has no existing STL: {target.name}; run a full build first')
 st=mesh_stats(target)
 if st['nonmanifold_edges'] or st['components']!=1 or st['volume_mm3']<=0:raise RuntimeError(f'Invalid mesh {target.name}: {st}')
 results[target.name]=st
 print('STL',target.name,st,flush=True)

base=shape(BASE);cap_s=shape(CAP);jig_s=shape(JIG)
for name,s in [('DB23_Holder',base),('DB23_Cap',cap_s),('DB23_Pin_Height_Jig',jig_s.translate((0,0,J['print_z_offset'])))]:
 if not s.isValid() or len(s.Solids())!=1:raise RuntimeError(f'{name}: invalid/disconnected STEP')
 target=OUT/f'{name}_v{R}.step';cq.exporters.export(s,str(target))
 results[target.name]={'valid':True,'solids':len(s.Solids()),'volume_mm3':round(s.Volume(),3),'coordinates':'print bed' if name=='DB23_Pin_Height_Jig' else 'assembly'}

def vol(a,b):return round(a.intersect(b).Volume(),9)
def chk(name,value):
 if value>1e-5:raise RuntimeError(f'{name}: overlap {value} mm3')
 return value
pcb=cq.Workplane('XY').polyline(B['outline_xy']).close().extrude(B['thickness']).translate((0,0,B['bottom_z'])).val()
for s in(-1,1):
 pcb=pcb.cut(shape(zc(s*AX,AY,B['shield_pad_drill'],B['bottom_z']-.01,B['bottom_z']+B['thickness']+.01)))
 for x,y in PINS:pcb=pcb.cut(shape(zc(x,y,B['tail_drill'],B['bottom_z']-.01,B['bottom_z']+B['thickness']+.01)))
checks={'base_PCB_overlap_mm3':chk('base PCB',vol(base,pcb)),'cap_base_overlap_mm3':chk('cap base',vol(cap_s,base)),'cap_PCB_overlap_mm3':chk('cap PCB',vol(cap_s,pcb)),'jig_base_overlap_mm3':chk('jig base',vol(jig_s,base))}
for i,(x,y) in enumerate(PINS,1):
 bore=shape(zc(x,y,H['pin_guide_hole_diameter']-.002,H['bottom_clearance']-.01,H['pin_block_top_z']+.01))
 chk('guide bore',vol(base,bore))
 pin=shape(box(x-H['square_pin_size_assumed']/2,x+H['square_pin_size_assumed']/2,y-H['square_pin_size_assumed']/2,y+H['square_pin_size_assumed']/2,H['pin_bottom_z'],H['pin_top_z']))
 chk('pin in jig',vol(jig_s,pin));chk('pin under cap',vol(cap_s,pin))
checks['guide_bores_open']=23;checks['pins_clear_jig_and_cap']=23
washer_bot=B['bottom_z']+B['thickness'];nut_bot=washer_bot+A['washer_thickness_assumed'];nut_top=nut_bot+A['nut_height_assumed'];tip=A['screw_length_under_head']-M['thickness_assumed']-A['underside_washer_thickness_assumed']
for side in(-1,1):
 ax=side*AX
 screw=shape(zc(ax,AY,3,-M['thickness_assumed'],tip))
 washer=shape(cut(zc(ax,AY,A['washer_diameter_assumed'],washer_bot,nut_bot),zc(ax,AY,A['washer_bore_assumed'],washer_bot-.01,nut_bot+.01))) if A['washer_thickness_assumed']>0 else None
 # Rotation-independent cylindrical envelope of M3 hex nut corners.
 outer_nut=shape(cut(zc(ax,AY,A['nut_across_flats_assumed']*2/math.sqrt(3),nut_bot,nut_top),zc(ax,AY,3,nut_bot-.01,nut_top+.01)))
 for label,s in [('screw',screw),('washer',washer),('nut_envelope',outer_nut)]:
  if s is not None:checks[f'cap_{label}_{side}_overlap_mm3']=chk('cap hardware',vol(cap_s,s))
 stem=shape(yc(ax,H['nut_axis_z'],3,0,H['jackpost_stem_max_end_y']))
 checks[f'stem_mounting_nut_{side}_overlap_mm3']=chk('stem versus nut',vol(stem,outer_nut))
 if washer is not None:checks[f'stem_mounting_washer_{side}_overlap_mm3']=chk('stem versus washer',vol(stem,washer))
 checks[f'stem_base_{side}_overlap_mm3']=chk('stem versus base',vol(stem,base))
checks.update(screw_tip_z=tip,nut_top_z=nut_top,default_screw_protrusion_above_nut=tip-nut_top,cap_roof_clearance_above_tip=C['roof_bottom_z']-tip,guide_fillet_gap=B['bottom_z']-H['pin_block_top_z'],integrated_foot_bottom_z=H['foot_bottom_z'],main_body_bottom_z=H['bottom_clearance'],jackpost_stem_max_end_y=H['jackpost_stem_max_end_y'],jackpost_relief_end_y=H['jackpost_relief_end_y'],cap_latch_engagement_y=H['tower_rear_y']-C['latch_hook_front_y'],latch_minimum_assembly_deflection_estimate=H['tower_rear_y']-C['latch_hook_front_y']+.1,latch_elastic_strength_tested=False,cap_print_transform={'rotate_x_degrees':180,'translate_z':C['print_translate_z']},jig_print_offset_z=J['print_z_offset'])
results['structural_checks']=checks
(OUT/'mechanical_validation.json').write_text(json.dumps(results,indent=2)+'\n')
# Remove obsolete mechanical revision names only after a complete successful build.
for old in OUT.glob('*_v0.[34].*'):old.unlink()
print(json.dumps(results,indent=2))
