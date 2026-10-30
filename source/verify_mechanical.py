#!/usr/bin/env python3
"""Independent saved-file CAD checks for the DB23 revision 0.5 fit prototype.

Read the delivered STEP/STL files without importing the mechanical builder.
CadQuery/OpenCascade checks solid clearance and VTK independently checks meshes
and loading-jig stop surfaces. Assumed envelopes are not measured purchased parts.
"""
from pathlib import Path
import json, math
import cadquery as cq
import vtk

ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/'source/design_parameters.json').read_text())
H=P['holder'];B=P['pcb'];M=P['motherboard'];C=P['connector_sample_assumptions'];J=P['pin_height_jig'];A=P['mounting'];R=P['revision']
K=P.get('cap',{})
OUT=ROOT/'verification/mechanical-audit.json'
report={'revision':R,'scope':'Saved-file CAD only; connector, hardware and print fits remain unmeasured assumptions',
        'checks':{},'intersections_mm3':{},'meshes':{},'unsupported_screw_lengths':{}}

def check(name,condition,details=True):
    report['checks'][name]={'passed':bool(condition),'details':details}
    if not condition:raise AssertionError(f'{name}: {details}')

def box(x0,x1,y0,y1,z0,z1):return cq.Solid.makeBox(x1-x0,y1-y0,z1-z0,cq.Vector(x0,y0,z0))
def zc(x,y,d,z0,z1):return cq.Solid.makeCylinder(d/2,z1-z0,cq.Vector(x,y,z0))
def yc(x,z,d,y0,y1):return cq.Solid.makeCylinder(d/2,y1-y0,cq.Vector(x,y0,z),cq.Vector(0,1,0))
def compound(shapes):return cq.Compound.makeCompound(shapes)
def intersection(name,a,b):
    v=a.intersect(b).Volume();report['intersections_mm3'][name]=round(v,8)
    check(name,v<1e-6,round(v,8));return v

def hex_z(x,y,z,af,t,bore=0):
    rad=af/math.sqrt(3)
    pts=[(x+rad*math.cos(math.radians(a)),y+rad*math.sin(math.radians(a))) for a in range(0,360,60)]
    s=cq.Workplane('XY').polyline(pts).close().extrude(t).translate((0,0,z)).val()
    if bore:s=s.cut(zc(x,y,bore,z-.01,z+t+.01))
    return s

def hull(pts):
    pts=sorted(set(pts))
    def cross(o,a,b):return(a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[]
    for p in pts:
        while len(lo)>=2 and cross(lo[-2],lo[-1],p)<=0:lo.pop()
        lo.append(p)
    hi=[]
    for p in reversed(pts):
        while len(hi)>=2 and cross(hi[-2],hi[-1],p)<=0:hi.pop()
        hi.append(p)
    return lo[:-1]+hi[:-1]

def jack_nut(x,sweep=0):
    rad=H['nut_across_flats_assumed']/math.sqrt(3)
    pts=[(x+rad*math.cos(math.radians(a)),H['nut_axis_z']+rad*math.sin(math.radians(a))+dz)
         for a in range(30,331,60) for dz in(0,sweep)]
    y=H['nut_axis_y_assumed']-H['nut_thickness_assumed']/2
    vs=[cq.Vector(xx,y,zz) for xx,zz in hull(pts)]
    s=cq.Solid.extrudeLinear(cq.Wire.makePolygon(vs+[vs[0]]),[],cq.Vector(0,H['nut_thickness_assumed'],0))
    if not sweep:s=s.cut(yc(x,H['nut_axis_z'],3,y-.01,y+H['nut_thickness_assumed']+.01))
    return s

pins=[]
for n in range(1,24):
    x=(6.5-n)*M['pin_pitch'] if n<=12 else(18-n)*M['pin_pitch']
    y=M['rear_row_y'] if n<=12 else M['front_row_y'];pins.append((x,y))
mounts=[(s*M['anchor_spacing']/2,M['anchor_y']) for s in(-1,1)]
bonds=[(s*B['shell_bond_pad_x'],B['shell_bond_pad_y']) for s in(-1,1)]

def pcb(sweep=0):
    z=B['bottom_z'];t=B['thickness']+sweep
    s=cq.Workplane('XY').polyline(B['outline_xy']).close().extrude(t).translate((0,0,z)).val()
    cutters=[zc(x,y,B['tail_drill'],z-.01,z+t+.01) for x,y in pins]
    cutters.extend(zc(x,y,B['shield_pad_drill'],z-.01,z+t+.01) for x,y in mounts)
    cutters.extend(zc(x,y,B['shell_bond_pad_drill'],z-.01,z+t+.01) for x,y in bonds)
    return s.cut(*cutters)

holder=cq.importers.importStep(str(ROOT/f'mechanical/DB23_Holder_v{R}.step')).val()
cap=cq.importers.importStep(str(ROOT/f'mechanical/DB23_Cap_v{R}.step')).val()
for name,s in [('holder',holder),('cap',cap)]:
    check(name+'_STEP_valid_one_solid',s.isValid() and len(s.Solids())==1)
    report[name+'_volume_mm3']=round(s.Volume(),6)
    bb=s.BoundingBox();report[name+'_assembly_bounds']=[bb.xmin,bb.xmax,bb.ymin,bb.ymax,bb.zmin,bb.zmax]
# Review amendment: both marked forward end faces must be one flat plane.
# Probe the delivered solids rather than importing/reusing the construction tree.
# The rear-corner samples were voids in the preceding stepped end shape.
end_x=H['forward_end_outer_x']
pocket_outer_x=M['anchor_spacing']/2+(H['nut_across_flats_assumed']+H['nut_pocket_clearance'])/2
pocket_rear_y=H['nut_axis_y_assumed']+(H['nut_thickness_assumed']+H['nut_pocket_clearance'])/2
report['squared_end_review']={
    'forward_outer_plane_abs_X':end_x,
    'forward_end_Y_range':[H['front_y'],H['tower_rear_y']],
    'rear_corner_fill_outward_from_previous_X25_mm':end_x-25.0,
    'front_face_trim_inward_from_previous_X26_mm':26.0-end_x,
    'outer_wall_to_nut_loading_slot_mm':end_x-pocket_outer_x,
    'rear_web_behind_nut_pocket_mm':H['tower_rear_y']-pocket_rear_y,
    'note':'Geometric section dimensions and material probes only; no physical strength or fatigue result.'}
for side in(-1,1):
    for i,y in enumerate((H['front_y']+.15,2.9,H['tower_rear_y']-.20),1):
        for name,obj,z in [('base',holder,9.0),('cap',cap,K['roof_bottom_z']+.50)]:
            inside=cq.Vector(side*(end_x-.05),y,z)
            outside=cq.Vector(side*(end_x+.05),y,z)
            check(f'square_end_{name}_{side}_{i}_inside_face',obj.isInside(inside),inside.toTuple())
            check(f'square_end_{name}_{side}_{i}_outside_face',not obj.isInside(outside),outside.toTuple())
    for i,y in enumerate((4.60,5.00),1):
        p=cq.Vector(side*25.30,y,8.50)
        check(f'filled_marked_rear_corner_{side}_{i}',holder.isInside(p),p.toTuple())
    p=cq.Vector(side*25.30,4.90,1.00)
    check(f'filled_lower_end_corner_{side}',holder.isInside(p),p.toTuple())
board=pcb();zc0=M['connector_centre_height'];pcb_top=B['bottom_z']+B['thickness']
flange=box(-C['flange_width']/2,C['flange_width']/2,0,C['flange_thickness'],0,C['flange_height'])
body=box(-C['rear_body_width']/2,C['rear_body_width']/2,C['flange_thickness'],C['rear_body_end_y'],zc0-C['rear_body_height']/2,zc0+C['rear_body_height']/2)
cups=[];cup_sweep=[];squares=[]
for n,(x,y) in enumerate(pins,1):
    zz=zc0+(M['row_spacing']/2 if n<=12 else-M['row_spacing']/2)
    cups.append(yc(x,zz,C['cup_outer_diameter'],C['rear_body_end_y'],C['cup_end_y']))
    rad=C['cup_outer_diameter']/2
    cup_sweep.append(box(x-rad,x+rad,C['rear_body_end_y'],C['cup_end_y'],zz-rad,zz+rad+20))
    half=H['square_pin_size_assumed']/2
    squares.append(box(x-half,x+half,y-half,y+half,H['pin_bottom_z'],H['pin_top_z']))
for name,obj in [('PCB',board),('assumed_flange',flange),('assumed_rear_body',body),('assumed_full_cup_envelopes',compound(cups)),('all_square_pins',compound(squares))]:
    intersection('holder_'+name,holder,obj)
    intersection('cap_'+name,cap,obj)
intersection('holder_cap_seated',holder,cap)
intersection('holder_PCB_exact_vertical_sweep_20mm',holder,pcb(20))
intersection('holder_flange_exact_vertical_sweep_20mm',holder,box(-C['flange_width']/2,C['flange_width']/2,0,C['flange_thickness'],0,C['flange_height']+20))
intersection('holder_body_exact_vertical_sweep_20mm',holder,box(-C['rear_body_width']/2,C['rear_body_width']/2,C['flange_thickness'],C['rear_body_end_y'],zc0-C['rear_body_height']/2,zc0+C['rear_body_height']/2+20))
intersection('holder_cup_conservative_vertical_sweep_20mm',holder,compound(cup_sweep))
# The motherboard here is a nominal planar envelope, not a component model.
mb=box(-30,30,0,16,-M['thickness_assumed'],0)
mb=mb.cut(*(zc(x,y,M['anchor_hole_reference'],-M['thickness_assumed']-.01,.01) for x,y in mounts))
intersection('holder_nominal_motherboard_plane',holder,mb)
hb=holder.BoundingBox()
check('flat_base_minimum_Z',abs(hb.zmin)<1e-6,hb.zmin)
bottom_faces=[f for f in holder.Faces() if abs(f.Center().z)<1e-6 and f.normalAt().z<-.99]
bottom_area=sum(f.Area() for f in bottom_faces)
check('flat_base_single_broad_bottom_face',len(bottom_faces)==1 and bottom_area>350,
      {'faces':len(bottom_faces),'area_mm2':round(bottom_area,6)})
check('projecting_mounting_feet_removed',H['bottom_clearance']==0 and 'foot_diameter' not in H and 'foot_bottom_z' not in H,
      {'bottom_clearance':H['bottom_clearance'],'foot_diameter_present':'foot_diameter' in H,'foot_bottom_z_present':'foot_bottom_z' in H})
# Representative points in each underside region must all have material just
# above the same Z0 plane. Open connector and wire-channel regions are omitted.
flat_base_samples=[(-24,2),(24,2),(-20,8),(20,8),(0,9.5),(-20,12.5),(0,12.5),(20,12.5)]
for i,(x,y) in enumerate(flat_base_samples,1):
    check(f'flat_base_bearing_sample_{i:02d}',holder.isInside(cq.Vector(x,y,.05)),[x,y,.05])
for i,(x,y) in enumerate(pins,1):
    intersection(f'guide_bore_{i:02d}',holder,zc(x,y,H['pin_guide_hole_diameter']-.002,H['bottom_clearance']-.01,H['pin_block_top_z']+.01))
# PTH bond fillets are deliberately conservative small cylinders; actual joints
# and the lead routing need a physical check before seating the subassembly.
for i,(x,y) in enumerate(bonds,1):
    fillet=zc(x,y,B['shell_bond_pad_diameter'],B['bottom_z']-.75,B['bottom_z'])
    intersection(f'holder_J4_underfillet_{i}',holder,fillet)
    intersection(f'holder_J4_underfillet_exact_vertical_sweep_{i}',holder,zc(x,y,B['shell_bond_pad_diameter'],B['bottom_z']-.75,B['bottom_z']+20))
    intersection(f'cap_J4_top_lead_clearance_{i}',cap,zc(x,y,2.0,pcb_top,pcb_top+2.0))
# Metal fasteners: nominal shanks, flat head, washer and vertical nut.
wash_z=pcb_top;nut_z=wash_z+A['washer_thickness_assumed'];nut_top=nut_z+A['nut_height_assumed']
ins_t=A['underside_washer_thickness_assumed'];head_seat_z=-M['thickness_assumed']-ins_t
report['mounting_stack_mm']={'motherboard':M['thickness_assumed'],'flat_base_to_PCB_underside':B['bottom_z'],
    'PCB':B['thickness'],'underside_insulating_washer':ins_t,'top_washer':A['washer_thickness_assumed'],'nut':A['nut_height_assumed'],
    'under_head_to_nut_top':M['thickness_assumed']+ins_t+nut_top,'default_screw_tip_Z':A['screw_length_under_head']+head_seat_z,
    'default_protrusion_above_nut':A['screw_length_under_head']+head_seat_z-nut_top,
    'head_bottom_Z':head_seat_z-A['head_height_assumed'],
    'projection_below_motherboard_underside':ins_t+A['head_height_assumed']}
for side,(x,y) in zip((-1,1),mounts):
    shank=zc(x,y,3,head_seat_z,A['screw_length_under_head']+head_seat_z)
    head=zc(x,y,A['head_diameter_assumed'],head_seat_z-A['head_height_assumed'],head_seat_z)
    insulator=zc(x,y,A['underside_washer_diameter_assumed'],head_seat_z,-M['thickness_assumed']).cut(zc(x,y,A['underside_washer_bore_assumed'],head_seat_z-.01,-M['thickness_assumed']+.01))
    washer=(zc(x,y,A['washer_diameter_assumed'],wash_z,nut_z).cut(zc(x,y,3.2,wash_z-.01,nut_z+.01)) if A['washer_thickness_assumed']>0 else None)
    nut=hex_z(x,y,nut_z,A['nut_across_flats_assumed'],A['nut_height_assumed'],3)
    nut_rotation_envelope=zc(x,y,2*A['nut_across_flats_assumed']/math.sqrt(3),nut_z,nut_top).cut(zc(x,y,3,nut_z-.01,nut_top+.01))
    jack=jack_nut(x)
    for objname,obj in [('M3_shank',shank),('M3_head',head),('underside_insulator',insulator),('top_washer',washer),('top_nut',nut),('jackpost_nut',jack)]:
        if obj is None:continue
        intersection(f'holder_{objname}_{side}',holder,obj)
        intersection(f'cap_{objname}_{side}',cap,obj)
        intersection(f'PCB_{objname}_{side}',board,obj)
    intersection(f'motherboard_M3_shank_{side}',mb,shank)
    intersection(f'motherboard_M3_head_{side}',mb,head)
    intersection(f'motherboard_underside_insulator_{side}',mb,insulator)
    check(f'head_supported_by_insulator_OD_{side}',A['underside_washer_diameter_assumed']>=A['head_diameter_assumed'],{'head_OD':A['head_diameter_assumed'],'insulator_OD':A['underside_washer_diameter_assumed']})
    intersection(f'jackpost_nut_top_loading_holder_{side}',holder,jack_nut(x,15))
    intersection(f'jackpost_nut_top_loading_PCB_{side}',board,jack_nut(x,15))
    # Four support directions through the full-height, flat-base mounting rail.
    for angle in(0,90,180,270):
        xx=x+2.4*math.cos(math.radians(angle));yy=y+2.4*math.sin(math.radians(angle))
        for label,z in [('flat_base_bearing',.10),('PCB_support',B['bottom_z']-.1)]:
            # The right rail intentionally contains one outboard ground-wire channel.
            in_ground_groove=(side==1 and angle==0 and label=='flat_base_bearing')
            if not in_ground_groove:check(f'{label}_{side}_{angle}',holder.isInside(cq.Vector(xx,yy,z)),[xx,yy,z])
    intersection(f'holder_mounting_bore_{side}',holder,zc(x,y,A['holder_bore_diameter']-.002,-.01,B['bottom_z']+.01))
    # Full end-to-end horizontal clearance tunnel and chosen maximum stem.
    passage_end=H['jackpost_relief_end_y']
    stem_end=H['jackpost_stem_max_end_y']
    stem=yc(x,H['nut_axis_z'],3,0,stem_end)
    intersection(f'holder_jackpost_stem_to_max_end_{side}',holder,stem)
    intersection(f'cap_jackpost_stem_to_max_end_{side}',cap,stem)
    intersection(f'PCB_jackpost_stem_to_max_end_{side}',board,stem)
    if washer is not None:intersection(f'top_washer_jackpost_stem_{side}',washer,stem)
    intersection(f'top_nut_jackpost_stem_{side}',nut,stem)
    intersection(f'cap_top_nut_all_rotations_envelope_{side}',cap,nut_rotation_envelope)
    intersection(f'top_nut_all_rotations_jackpost_stem_{side}',nut_rotation_envelope,stem)
    intersection(f'vertical_shank_jackpost_stem_{side}',shank,stem)
    check(f'jackpost_passage_extends_beyond_stem_{side}',passage_end>=stem_end,{'passage_end_Y':passage_end,'maximum_stem_end_Y':stem_end})
    for length in A['alternative_lengths']:
        tip=length+head_seat_z;s=zc(x,y,3,head_seat_z,tip)
        v=s.intersect(cap).Volume()
        report['unsupported_screw_lengths'].setdefault(str(length),{'tip_Z':tip,'cap_overlap_mm3':[]})['cap_overlap_mm3'].append(round(v,6))
# The right base-channel exit is a deliberate insulated grounding-wire route.
# Check a small core passes from the mounting axis out through the side.
right_x=M['anchor_spacing']/2
wire_core=box(right_x+1.9,H['overall_width']/2+.01,M['anchor_y']-.35,M['anchor_y']+.35,.02,.75)
intersection('right_base_ground_wire_exit_core',holder,wire_core)
# A conservative clip bending envelope checks room to flex without striking the PCB.
# It does not establish allowable material strain or fatigue life.
flex=max(0,H['tower_rear_y']-K['latch_hook_front_y'])+.05
report['clip_geometry']={'rearward_tip_motion_for_0_05mm_clearance':flex,
    'hook_bite_nominal':H['tower_rear_y']-K['latch_hook_front_y'],
    'XY_gap_to_PCB_ear_front_at_max_flex':B['mounting_ear_front_y']-K['latch_rear_y']-flex,
    'vertical_gap_latch_bottom_above_PCB':K['latch_bottom_z']-pcb_top,
    'note':'A negative XY gap is permitted only where the raised latch has vertical clearance; the solid-envelope check below is authoritative.'}
for side in(-1,1):
    cx=side*K['latch_centre_x']; w=K['latch_width']/2
    flexbox=box(cx-w,cx+w,K['latch_front_y'],K['latch_rear_y']+flex,K['latch_bottom_z'],K['roof_bottom_z'])
    intersection(f'PCB_conservative_clip_flex_envelope_{side}',board,flexbox)
    hook_probe=cq.Vector(cx,(K['latch_hook_front_y']+H['tower_rear_y'])/2,(K['latch_hook_ramp_top_z']+K['latch_hook_top_z'])/2)
    check(f'actual_cap_retaining_hook_material_{side}',cap.isInside(hook_probe),hook_probe.toTuple())
    check(f'actual_base_relief_at_seated_hook_{side}',not holder.isInside(hook_probe),hook_probe.toTuple())
    catch_probe=cq.Vector(hook_probe.x,hook_probe.y,H['latch_notch_top_z']+.15)
    check(f'actual_base_retaining_ceiling_{side}',holder.isInside(catch_probe),catch_probe.toTuple())
    beam_probe=cq.Vector(cx,(K['latch_front_y']+K['latch_rear_y'])/2,9)
    check(f'actual_cap_flex_beam_material_{side}',cap.isInside(beam_probe),beam_probe.toTuple())
    key_probe=cq.Vector(side*M['anchor_spacing']/2,H['nut_axis_y_assumed'],(K['tongue_bottom_z']+K['roof_bottom_z'])/2)
    check(f'actual_cap_nut_retaining_key_{side}',cap.isInside(key_probe),key_probe.toTuple())
check('clip_hook_has_positive_retention_bite',report['clip_geometry']['hook_bite_nominal']>0,report['clip_geometry'])
check('M3_default_length_full_nut_engagement',report['mounting_stack_mm']['default_protrusion_above_nut']>=.5,report['mounting_stack_mm'])
# Delivered STL topology, including separate printable cap orientation.
def mesh(path):
    rd=vtk.vtkSTLReader();rd.SetFileName(str(path));rd.Update();data=rd.GetOutput()
    e=vtk.vtkFeatureEdges();e.SetInputData(data);e.BoundaryEdgesOn();e.NonManifoldEdgesOn();e.FeatureEdgesOff();e.ManifoldEdgesOff();e.Update()
    conn=vtk.vtkPolyDataConnectivityFilter();conn.SetInputData(data);conn.SetExtractionModeToAllRegions();conn.Update()
    st={'triangles':data.GetNumberOfPolys(),'boundary_or_nonmanifold_edges':e.GetOutput().GetNumberOfCells(),'regions':conn.GetNumberOfExtractedRegions(),'bounds':list(data.GetBounds())}
    report['meshes'][path.name]=st
    check('mesh_'+path.stem,st['boundary_or_nonmanifold_edges']==0 and st['regions']==1,st)
    return data
meshes={p.name:mesh(p) for p in sorted((ROOT/'mechanical').glob(f'*v{R}.stl'))}
capdata=meshes[f'DB23_Cap_v{R}.stl']
# Print transform is R_x(180) plus a Z translation by the roof top; it is self-inverse.
roof_top=K.get('roof_top_z',12.2)
pts=[capdata.GetPoint(i) for i in range(capdata.GetNumberOfPoints())]
restored=[(x,-y,roof_top-z) for x,y,z in pts]
bb=cap.BoundingBox();expect=(bb.xmin,bb.xmax,bb.ymin,bb.ymax,bb.zmin,bb.zmax)
actual=tuple(v for axis in range(3) for v in(min(p[axis] for p in restored),max(p[axis] for p in restored)))
check('cap_print_STL_restores_STEP_assembly_bounds',max(abs(a-b) for a,b in zip(actual,expect))<.002,{'STL_restored':actual,'STEP':expect})
jigdata=meshes[f'DB23_Pin_Height_Jig_v{R}.stl']
jig=cq.importers.importStep(str(ROOT/f'mechanical/DB23_Pin_Height_Jig_v{R}.step')).val().translate((0,0,-J['print_z_offset']))
check('jig_STEP_valid_one_solid',jig.isValid() and len(jig.Solids())==1)
intersection('jig_holder_loading_position',jig,holder)
intersection('jig_all_square_pins',jig,compound(squares))
obb=vtk.vtkOBBTree();obb.SetDataSet(jigdata);obb.BuildLocator()
def vertical_hits(x,y):
    pts=vtk.vtkPoints();obb.IntersectWithLine((x,y,-1),(x,y,30),pts,None)
    return sorted(set(round(pts.GetPoint(i)[2]-J['print_z_offset'],4) for i in range(pts.GetNumberOfPoints())))
for i,(x,y) in enumerate(pins,1):
    hits=vertical_hits(x,y);check(f'jig_tip_stop_{i:02d}',len(hits)==2 and abs(hits[-1]-H['pin_bottom_z'])<.001,hits)
for side,(x,y) in zip((-1,1),mounts):
    # Offset from the locator to sample the annular flat-base support pad, not its peg.
    hits=vertical_hits(x,y+2.4)
    check(f'jig_flat_base_support_{side}',len(hits)==2 and abs(hits[-1])<.001,hits)
    hits=vertical_hits(x,y)
    check(f'jig_locator_top_{side}',len(hits)==2 and abs(hits[-1]-(J['support_top_z']+J['locating_peg_height']))<.001,hits)
check('pin_length_matches_datums',abs((H['pin_top_z']-H['pin_bottom_z'])-10.7)<1e-6)
check('guide_to_PCB_fillet_heat_gap',B['bottom_z']-H['pin_block_top_z']>=1.25,B['bottom_z']-H['pin_block_top_z'])
report['checks_passed']=sum(c['passed'] for c in report['checks'].values())
OUT.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'checks_passed':report['checks_passed'],'holder_volume_mm3':report['holder_volume_mm3'],'cap_volume_mm3':report['cap_volume_mm3'],'unsupported_screw_lengths':report['unsupported_screw_lengths'],'report':str(OUT)},indent=2))
