#!/usr/bin/env python3
"""Independent saved-file geometry checks for the DB23 mechanical fit prototype.

Reads the delivered STEP/STL, rather than importing the geometry builder. Tests
clearance and the proposed assembly paths against explicitly assumed envelopes.
Requires CadQuery and VTK; this does not test printed strength or physical fit.
"""
from pathlib import Path
import json, math
import cadquery as cq
import vtk

ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/'source/design_parameters.json').read_text())
H=P['holder']; B=P['pcb']; M=P['motherboard']; C=P['connector_sample_assumptions']; J=P['pin_height_jig']; R=P['revision']
OUT=ROOT/'verification/mechanical-audit.json'
report={'revision':R,'scope':'Saved-file CAD only; connector/hardware envelopes are unmeasured assumptions','checks':{},'intersections_mm3':{},'meshes':{}}

def check(name, condition, details=True):
    report['checks'][name]={'passed':bool(condition),'details':details}
    if not condition: raise AssertionError(f'{name}: {details}')

def box(x0,x1,y0,y1,z0,z1):
    return cq.Solid.makeBox(x1-x0,y1-y0,z1-z0,cq.Vector(x0,y0,z0))
def zc(x,y,d,z0,z1):
    return cq.Solid.makeCylinder(d/2,z1-z0,cq.Vector(x,y,z0))
def yc(x,z,d,y0,y1):
    return cq.Solid.makeCylinder(d/2,y1-y0,cq.Vector(x,y0,z),cq.Vector(0,1,0))
def compound(shapes): return cq.Compound.makeCompound(shapes)
def pcb(sweep=0):
    return cq.Workplane('XY').polyline(B['outline_xy']).close().extrude(B['thickness']+sweep).translate((0,0,B['bottom_z'])).val()
def intersection(name,a,b):
    vol=a.intersect(b).Volume(); report['intersections_mm3'][name]=round(vol,8)
    check(name,vol<1e-6,round(vol,8)); return vol

holder=cq.importers.importStep(str(ROOT/f'mechanical/DB23_Holder_v{R}.step')).val()
check('holder_STEP_valid_one_solid',holder.isValid() and len(holder.Solids())==1)
report['holder_volume_mm3']=round(holder.Volume(),6)
zc0=M['connector_centre_height']
flange=box(-C['flange_width']/2,C['flange_width']/2,0,C['flange_thickness'],0,C['flange_height'])
body=box(-C['rear_body_width']/2,C['rear_body_width']/2,C['flange_thickness'],C['rear_body_end_y'],zc0-C['rear_body_height']/2,zc0+C['rear_body_height']/2)
pins=[];cups=[];cup_sweep_boxes=[]
for n in range(1,24):
    x=(6.5-n)*M['pin_pitch'] if n<=12 else(18-n)*M['pin_pitch']
    y=M['rear_row_y'] if n<=12 else M['front_row_y']; pins.append((x,y))
    zz=zc0+(M['row_spacing']/2 if n<=12 else-M['row_spacing']/2)
    cups.append(yc(x,zz,C['cup_outer_diameter'],C['rear_body_end_y'],C['cup_end_y']))
    rad=C['cup_outer_diameter']/2
    cup_sweep_boxes.append(box(x-rad,x+rad,C['rear_body_end_y'],C['cup_end_y'],zz-rad,zz+rad+20))
intersection('holder_notched_PCB',holder,pcb())
intersection('holder_assumed_flange',holder,flange)
intersection('holder_assumed_rear_body',holder,body)
intersection('holder_all_assumed_full_cup_envelopes',holder,compound(cups))
# Exact linear sweep for prism bodies; conservative bounding-box sweeps for cups.
# Each covers every intermediate vertical offset from final position to +20 mm.
intersection('holder_PCB_vertical_lowering_sweep_20mm',holder,pcb(20))
intersection('holder_flange_vertical_lowering_sweep_20mm',holder,box(-C['flange_width']/2,C['flange_width']/2,0,C['flange_thickness'],0,C['flange_height']+20))
intersection('holder_body_vertical_lowering_sweep_20mm',holder,box(-C['rear_body_width']/2,C['rear_body_width']/2,C['flange_thickness'],C['rear_body_end_y'],zc0-C['rear_body_height']/2,zc0+C['rear_body_height']/2+20))
intersection('holder_conservative_cup_vertical_lowering_sweep_20mm',holder,compound(cup_sweep_boxes))
# Nut top-loading: vertically swept hex is a six-vertex prism with its top extended.
# Convex hull of both hex end positions gives an exact translational sweep section.

def hull(pts):
    pts=sorted(set(pts))
    def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    low=[]
    for p in pts:
        while len(low)>=2 and cross(low[-2],low[-1],p)<=0:low.pop()
        low.append(p)
    up=[]
    for p in reversed(pts):
        while len(up)>=2 and cross(up[-2],up[-1],p)<=0:up.pop()
        up.append(p)
    return low[:-1]+up[:-1]

def nutshape(ax,sweep=0):
    rad=H['nut_across_flats_assumed']/math.sqrt(3)
    pts=[(ax+rad*math.cos(math.radians(a)),H['nut_axis_z']+rad*math.sin(math.radians(a))+dz) for a in range(30,331,60) for dz in (0,sweep)]
    coords=hull(pts);y=H['nut_axis_y_assumed']-H['nut_thickness_assumed']/2
    vs=[cq.Vector(x,y,z) for x,z in coords]
    wire=cq.Wire.makePolygon(vs+[vs[0]])
    return cq.Solid.extrudeLinear(wire,[],cq.Vector(0,H['nut_thickness_assumed'],0))
for side in (-1,1):
    ax=side*M['anchor_spacing']/2; ay=M['anchor_y']
    intersection(f'holder_nut_{side}',holder,nutshape(ax))
    intersection(f'holder_nut_top_loading_sweep_{side}',holder,nutshape(ax,15))
    intersection(f'PCB_nut_top_loading_sweep_{side}',pcb(),nutshape(ax,15))
    # Maximum allowed head/washer stack, not just the narrower illustration.
    head=zc(ax,ay,H['anchor_head_max_diameter'],H['anchor_head_seat_z'],H['anchor_head_seat_z']+H['anchor_head_max_height'])
    intersection(f'holder_max_anchor_head_{side}',holder,head)
    intersection(f'PCB_max_anchor_head_{side}',pcb(),head)
    # A straight Ø4 driver centred on the screw axis clears the board edge.
    intersection(f'PCB_4mm_anchor_driver_{side}',pcb(),zc(ax,ay,4,H['anchor_head_seat_z'],20))
    # Check the pocket is open outboard at a height above the bearing floor.
    p=cq.Vector(side*(H['overall_width']/2-.05),ay,H['anchor_head_seat_z']+.2)
    check(f'anchor_pocket_open_outboard_{side}',not holder.isInside(p))
    # Material remains at the inward web and both fore/aft cheeks.
    for label,xx,yy,zz in [('inner_web',side*18.0,ay,5.0),('front_cheek',ax,5.7,4.0),('rear_cheek',ax,13.3,4.0),('bearing_floor',ax+side*2.4,ay,1.5)]:
        check(f'anchor_material_{side}_{label}',holder.isInside(cq.Vector(xx,yy,zz)),[xx,yy,zz])
# All through bores must be empty; probe slightly inside the nominal cylinder.
for i,(x,y) in enumerate(pins,1):
    intersection(f'guide_bore_{i:02d}',holder,zc(x,y,H['pin_guide_hole_diameter']-.002,H['bottom_clearance']-.01,H['pin_block_top_z']+.01))
for xx in (0,-10,10):
    check(f'rear_infill_material_X{xx}',holder.isInside(cq.Vector(xx,13.25,5.0)))
# Actual delivered STL topology and vertical intersections, independently via VTK.
def mesh(path):
    rd=vtk.vtkSTLReader();rd.SetFileName(str(path));rd.Update(); data=rd.GetOutput()
    edges=vtk.vtkFeatureEdges();edges.SetInputData(data);edges.BoundaryEdgesOn();edges.NonManifoldEdgesOn();edges.FeatureEdgesOff();edges.ManifoldEdgesOff();edges.Update()
    conn=vtk.vtkPolyDataConnectivityFilter();conn.SetInputData(data);conn.SetExtractionModeToAllRegions();conn.Update()
    stat={'triangles':data.GetNumberOfPolys(),'boundary_or_nonmanifold_edges':edges.GetOutput().GetNumberOfCells(),'regions':conn.GetNumberOfExtractedRegions()}
    report['meshes'][path.name]=stat
    check('mesh_'+path.stem,stat['boundary_or_nonmanifold_edges']==0 and stat['regions']==(2 if 'Anchor_Shims_' in path.name else 1),stat)
    return data

for path in sorted((ROOT/'mechanical').glob('*.stl')):mesh(path)
jig_path=ROOT/f'mechanical/DB23_Pin_Height_Jig_v{R}.stl'
jig_data=mesh(jig_path)
jig=cq.importers.importStep(str(ROOT/f'mechanical/DB23_Pin_Height_Jig_v{R}.step')).val().translate((0,0,-J['print_z_offset']))
check('jig_STEP_valid_one_solid',jig.isValid() and len(jig.Solids())==1)
intersection('jig_holder_at_loading_position',jig,holder)
half=H['square_pin_size_assumed']/2
for i,(x,y) in enumerate(pins,1):
    intersection(f'jig_square_pin_{i:02d}',jig,box(x-half,x+half,y-half,y+half,H['pin_bottom_z'],H['pin_top_z']))
obb=vtk.vtkOBBTree();obb.SetDataSet(jig_data);obb.BuildLocator()
def vertical_hits(x,y):
    pts=vtk.vtkPoints();obb.IntersectWithLine((x,y,-1),(x,y,30),pts,None)
    return sorted(set(round(pts.GetPoint(i)[2]-J['print_z_offset'],4) for i in range(pts.GetNumberOfPoints())))
for i,(x,y) in enumerate(pins,1):
    hits=vertical_hits(x,y)
    check(f'jig_tip_stop_{i:02d}',len(hits)==2 and abs(hits[-1]-H['pin_bottom_z'])<.001,hits)
for side in(-1,1):
    hits=vertical_hits(side*24.5,5)
    check(f'jig_holder_support_{side}',len(hits)==2 and abs(hits[-1]-H['bottom_clearance'])<.001,hits)
    hits=vertical_hits(side*M['anchor_spacing']/2,M['anchor_y'])
    check(f'jig_peg_top_{side}',len(hits)==2 and abs(hits[-1]-(J['support_top_z']+J['locating_peg_height']))<.001,hits)
check('pin_length_matches_top_and_bottom_datums',abs((H['pin_top_z']-H['pin_bottom_z'])-10.7)<1e-6)
check('fillet_heat_gap_nominal',B['bottom_z']-H['pin_block_top_z']>=1.25,B['bottom_z']-H['pin_block_top_z'])
report['checks_passed']=sum(v['passed'] for v in report['checks'].values())
OUT.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'checks_passed':report['checks_passed'],'holder_volume_mm3':report['holder_volume_mm3'],'meshes':report['meshes'],'report':str(OUT)},indent=2))
