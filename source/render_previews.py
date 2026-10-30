#!/usr/bin/env python3
"""Render the delivered printable CAD with explicitly assumed bought hardware.

Run with an X display (Xvfb is sufficient). Connector envelopes, screw threads
and motherboard thickness are references, not measured purchased-part models.
"""
import json, math
from pathlib import Path
import cadquery as cq
import vtk
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/'source/design_parameters.json').read_text())
OUT=ROOT/'previews'; MESH=OUT/'reference-meshes'
OUT.mkdir(exist_ok=True); MESH.mkdir(exist_ok=True)
mb=P['motherboard']; pcb=P['pcb']; holder=P['holder']; con=P['connector_sample_assumptions']; mounting=P['mounting']
REV=P['revision']

def box(x0,x1,y0,y1,z0,z1):
    return cq.Solid.makeBox(x1-x0,y1-y0,z1-z0,cq.Vector(x0,y0,z0))
def cyl_z(x,y,z,r,h):return cq.Solid.makeCylinder(r,h,cq.Vector(x,y,z))
def cyl_y(x,y,z,r,h):return cq.Solid.makeCylinder(r,h,cq.Vector(x,y,z),cq.Vector(0,1,0))
def hex_y(x,y,z,af,h,bore=0):
    rad=af/math.sqrt(3)
    pts=[cq.Vector(x+rad*math.cos(math.radians(a)),y,z+rad*math.sin(math.radians(a))) for a in range(30,360,60)]
    q=cq.Solid.extrudeLinear(cq.Wire.makePolygon(pts+[pts[0]]),[],cq.Vector(0,h,0))
    return q.cut(cyl_y(x,y-.02,z,bore/2,h+.04)) if bore else q

def hex_z(x,y,z,af,h,bore=0):
    rad=af/math.sqrt(3)
    pts=[cq.Vector(x+rad*math.cos(math.radians(a)),y+rad*math.sin(math.radians(a)),z) for a in range(0,360,60)]
    q=cq.Solid.extrudeLinear(cq.Wire.makePolygon(pts+[pts[0]]),[],cq.Vector(0,0,h))
    return q.cut(cyl_z(x,y,z-.02,bore/2,h+.04)) if bore else q

def compound(shapes):return cq.Compound.makeCompound(shapes)
def save(name,shape):
    path=MESH/(name+'.stl'); cq.exporters.export(shape,str(path),tolerance=.025,angularTolerance=.1);return path

def pin_xy(n,gender='M'):
    x=(6.5-n)*mb['pin_pitch'] if n<=12 else (18-n)*mb['pin_pitch']
    return (-x if gender=='F' else x), mb['rear_row_y'] if n<=12 else mb['front_row_y']

def pcb_holes():
    holes=[(*pin_xy(n),pcb['tail_drill'],pcb['tail_pad_diameter']) for n in range(1,24)]
    for prefix in ('shield','shell_bond'):
        for side in (-1,1):
            holes.append((side*pcb[prefix+'_pad_x'],pcb[prefix+'_pad_y'],pcb[prefix+'_pad_drill'],pcb[prefix+'_pad_diameter']))
    return holes

def build_meshes():
    z=pcb['bottom_z']; t=pcb['thickness']
    board=cq.Workplane('XY').polyline(pcb['outline_xy']).close().extrude(t).translate((0,0,z)).val()
    holes=pcb_holes()
    for x,y,drill,_ in holes:board=board.cut(cyl_z(x,y,z-.1,drill/2,t+.2))
    paths={'pcb':save('pcb-reference',board)}
    pads=[]
    for x,y,drill,dia in holes:
        for zz in (z-.045,z+t+.005):
            pads.append(cyl_z(x,y,zz,dia/2,.04).cut(cyl_z(x,y,zz-.01,drill/2,.06)))
    for n in range(1,24):
        x,_=pin_xy(n); zz=z+t+.005 if n<=12 else z-.045
        pads.append(box(x-pcb['cup_pad_width']/2,x+pcb['cup_pad_width']/2,pcb['cup_pad_front_y'],pcb['cup_pad_front_y']+pcb['cup_pad_length'],zz,zz+.04))
    paths['pads']=save('exposed-pad-reference',compound(pads))
    half=holder['square_pin_size_assumed']/2
    paths['pins']=save('23-tail-pins-reference',compound([box(x-half,x+half,y-half,y+half,holder['pin_bottom_z'],holder['pin_top_z']) for x,y in [pin_xy(n) for n in range(1,24)]]))
    zc=mb['connector_centre_height']
    flange=box(-con['flange_width']/2,con['flange_width']/2,0,con['flange_thickness'],0,con['flange_height'])
    for side in (-1,1):flange=flange.cut(cyl_y(side*mb['anchor_spacing']/2,-.02,zc,1.65,con['flange_thickness']+.04))
    outer=[(-18.095,zc+4.125),(18.095,zc+4.125),(16.9,zc-4.125),(-16.9,zc-4.125)]
    inner=[(-17.45,zc+3.50),(17.45,zc+3.50),(16.35,zc-3.50),(-16.35,zc-3.50)]
    shell=cq.Workplane('XZ').polyline(outer).close().extrude(con['front_shell_depth']).val()
    shell=shell.cut(cq.Workplane('XZ',origin=(0,.02,0)).polyline(inner).close().extrude(con['front_shell_depth']+.04).val())
    paths['shell']=save('db23-metal-reference',compound([flange,shell]))
    body=box(-con['rear_body_width']/2,con['rear_body_width']/2,con['flange_thickness'],con['rear_body_end_y'],zc-con['rear_body_height']/2,zc+con['rear_body_height']/2)
    frontins=cq.Workplane('XZ',origin=(0,-.7,0)).polyline(inner).close().extrude(1.5).val()
    paths['insulator']=save('db23-insulator-reference',compound([body,frontins]))
    contacts=[]
    for n in range(1,24):
        x,_=pin_xy(n); zz=zc+(mb['row_spacing']/2 if n<=12 else -mb['row_spacing']/2)
        contacts.append(cyl_y(x,-5.25,zz,.49,3.1))
        tube=cyl_y(x,con['rear_body_end_y'],zz,con['cup_outer_diameter']/2,con['cup_end_y']-con['rear_body_end_y'])
        tube=tube.cut(cyl_y(x,con['rear_body_end_y']-.02,zz,.47,con['cup_end_y']-con['rear_body_end_y']+.04))
        if n<=12:tube=tube.cut(box(x-1,x+1,con['rear_body_end_y']+.6,con['cup_end_y']+.1,zz,zz+1.1))
        else:tube=tube.cut(box(x-1,x+1,con['rear_body_end_y']+.6,con['cup_end_y']+.1,zz-1.1,zz))
        contacts.append(tube)
    paths['contacts']=save('23-db23-contacts-reference',compound(contacts))
    nuts=[];posts=[];bolts=[];washers=[];top_nuts=[];under_washers=[]
    uwt=mounting['underside_washer_thickness_assumed']
    seat=-mb['thickness_assumed']-uwt; wt=mounting['washer_thickness_assumed']; washer_z=z+t
    for side in (-1,1):
        xx=side*mb['anchor_spacing']/2; yy=mb['anchor_y']
        nuts.append(hex_y(xx,holder['nut_axis_y_assumed']-holder['nut_thickness_assumed']/2,zc,holder['nut_across_flats_assumed'],holder['nut_thickness_assumed'],3.0))
        posts.append(hex_y(xx,-4.8,zc,4.75,4.8,2.2))
        posts.append(cyl_y(xx,0,zc,1.48,holder.get('jackpost_reference_stem_end_y',4.8)))
        # Nominal under-head length. Neither thread geometry nor drive recess is a fit specification.
        shaft=cyl_z(xx,yy,seat,1.48,mounting['screw_length_under_head'])
        hh=mounting['head_height_assumed']; head=cyl_z(xx,yy,seat-hh,mounting['head_diameter_assumed']/2,hh)
        head=head.cut(box(xx-.35,xx+.35,yy-1.5,yy+1.5,seat-hh-.01,seat-hh+.32)).cut(box(xx-1.5,xx+1.5,yy-.35,yy+.35,seat-hh-.01,seat-hh+.32))
        bolts.append(compound([shaft,head]))
        if wt>0: washers.append(cyl_z(xx,yy,washer_z,mounting['washer_diameter_assumed']/2,wt).cut(cyl_z(xx,yy,washer_z-.01,1.6,wt+.02)))
        under_washers.append(cyl_z(xx,yy,seat,mounting['underside_washer_diameter_assumed']/2,uwt).cut(cyl_z(xx,yy,seat-.01,mounting['underside_washer_bore_assumed']/2,uwt+.02)))
        top_nuts.append(hex_z(xx,yy,washer_z+wt,mounting['nut_across_flats_assumed'],mounting['nut_height_assumed'],3.0))
    paths['nuts']=save('jackpost-nuts-reference',compound(nuts)); paths['posts']=save('jackposts-reference',compound(posts))
    paths['anchors']=save('upward-M3x12-screws-reference',compound(bolts))
    if washers:paths['washers']=save('top-washers-reference',compound(washers))
    else:(MESH/'top-washers-reference.stl').unlink(missing_ok=True)
    paths['insulating_washers']=save('underside-insulating-washers-reference',compound(under_washers))
    paths['top_nuts']=save('top-mounting-nuts-reference',compound(top_nuts))
    return paths

COLOURS={'holder':(.075,.085,.095),'cap':(.055,.065,.075),'pcb':(.035,.045,.055),'pads':(.83,.64,.20),'pins':(.85,.66,.24),'shell':(.76,.81,.85),'insulator':(.06,.07,.08),'contacts':(.86,.68,.27),'nuts':(.66,.71,.75),'posts':(.74,.78,.82),'anchors':(.60,.66,.70),'washers':(.66,.71,.75),'top_nuts':(.66,.71,.75),'jig':(.66,.38,.17),'insulating_washers':(.45,.47,.49)}
METAL={'shell','pads','pins','contacts','nuts','posts','anchors','washers','top_nuts'}
def actor_for(path,key,offset=(0,0,0),rotation=(0,0,0),colour=None):
    reader=vtk.vtkSTLReader();reader.SetFileName(str(path));reader.Update()
    normals=vtk.vtkPolyDataNormals();normals.SetInputConnection(reader.GetOutputPort());normals.SetFeatureAngle(35)
    mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(normals.GetOutputPort())
    actor=vtk.vtkActor();actor.SetMapper(mapper);actor.SetPosition(*offset)
    actor.SetOrientation(*rotation)
    mat=actor.GetProperty();mat.SetColor(*(colour or COLOURS[key]))
    if key in METAL:
        # Direct-light Phong keeps silver reference hardware readable without
        # an external HDR environment, which would otherwise render it black.
        mat.SetInterpolationToPhong();mat.SetAmbient(.18);mat.SetDiffuse(.75);mat.SetSpecular(.45);mat.SetSpecularPower(36)
    else:
        mat.SetInterpolationToPBR();mat.SetMetallic(0);mat.SetRoughness(.64)
    return actor

CREDITS='Paul of UK Computing Limited | Jon of JMC Electronics | AI assistance through Codex'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';FONTB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def annotate(path,title,notes):
    im=Image.open(path).convert('RGB');w,h=im.size
    canvas=Image.new('RGB',(w,h+194),'white');canvas.paste(im,(0,124));d=ImageDraw.Draw(canvas)
    d.rectangle((0,0,w,9),fill='#17394e');d.text((42,24),title,font=ImageFont.truetype(FONTB,30),fill='#17394e')
    d.text((42,65),CREDITS,font=ImageFont.truetype(FONT,18),fill='#526873')
    d.text((42,95),f'Revision {REV} | CAD fit prototype',font=ImageFont.truetype(FONT,15),fill='#526873')
    d.rectangle((0,h+124,w,h+194),fill='#edf3f6')
    for i,n in enumerate(notes):d.text((42,h+136+i*25),n,font=ImageFont.truetype(FONT,17),fill='#354b59')
    canvas.save(path)

def cap_actor(offset=(0,0,0),colour=None):
    cap=P['cap']
    # Inverse of roof-down STL transform R_x(180) + Z(roof_top).
    pos=[0,0,cap['print_translate_z']];rot=[cap['print_rotate_x_degrees'],0,0]
    return actor_for(ROOT/f'mechanical/DB23_Cap_v{REV}.stl','cap',tuple(pos[i]+offset[i] for i in range(3)),tuple(rot),colour)

def render(paths,mode,name,camera=(64,72,50)):
    ren=vtk.vtkRenderer();ren.SetBackground(.99,.995,1);ren.SetBackground2(.89,.93,.96);ren.GradientBackgroundOn()
    exploded=mode=='exploded'; detail=mode in ('holder','parts')
    ren.AddActor(actor_for(ROOT/f'mechanical/DB23_Holder_v{REV}.stl','holder',colour=(.36,.43,.47) if detail else None))
    if mode=='jig':
        ren.AddActor(actor_for(ROOT/f'mechanical/DB23_Pin_Height_Jig_v{REV}.stl','jig',(0,0,-P['pin_height_jig']['print_z_offset'])))
        ren.AddActor(actor_for(paths['pins'],'pins'))
    elif mode=='parts':
        ren.AddActor(actor_for(ROOT/f'mechanical/DB23_Cap_v{REV}.stl','cap',(0,28,0),colour=(.29,.36,.41)))
    elif mode!='holder':
        pz=17 if exploded else 0
        for key in ('pcb','pads','shell','insulator','contacts'):ren.AddActor(actor_for(paths[key],key,(0,0,pz)))
        ren.AddActor(actor_for(paths['pins'],'pins'))
        ren.AddActor(actor_for(paths['posts'],'posts',(0,-9 if exploded else 0,pz)))
        ren.AddActor(actor_for(paths['nuts'],'nuts',(0,0,29 if exploded else 0)))
        ren.AddActor(actor_for(paths['anchors'],'anchors',(0,0,-8 if exploded else 0)))
        ren.AddActor(actor_for(paths['insulating_washers'],'insulating_washers',(0,0,-8 if exploded else 0)))
        for key in ('washers','top_nuts'):
            if key in paths:ren.AddActor(actor_for(paths[key],key,(0,0,28 if exploded else 0)))
        if mode in ('assembly','exploded'):ren.AddActor(cap_actor((0,0,42 if exploded else 0)))
    for position,intensity in [((35,-50,95),1.0),((-55,15,50),.7),((0,65,90),.8)]:
        light=vtk.vtkLight();light.SetPosition(*position);light.SetFocalPoint(0,5,4);light.SetIntensity(intensity);ren.AddLight(light)
    cam=ren.GetActiveCamera();cam.SetPosition(*camera);cam.SetFocalPoint(0,12 if mode=='parts' else 4,22 if exploded else 4)
    cam.SetViewUp(0,0,1);cam.ParallelProjectionOn();cam.SetParallelScale(46 if exploded else 28 if mode=='parts' else 24)
    win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.AddRenderer(ren);win.SetSize(1600,1000);win.SetMultiSamples(8);win.Render()
    cap=vtk.vtkWindowToImageFilter();cap.SetInput(win);cap.SetInputBufferTypeToRGB();cap.ReadFrontBufferOff();cap.Update()
    writer=vtk.vtkPNGWriter();writer.SetFileName(str(OUT/name));writer.SetInputConnection(cap.GetOutputPort());writer.Write();win.Finalize()
    titles={'assembly':'DB23 replacement - black clip-on cap fitted','open':'DB23 replacement - cap removed for inspection','exploded':'Assembly - joined DB23 and PCB, upward screws, clip-on cap','holder':'Solid base - flat motherboard bearing surface','parts':'Printed base and keyed clip-on cap','jig':'Pin loading - removable common-height jig'}
    notes={'assembly':['A solid base and two upward M3 screws provide the intended mounting; the cap retains jackpost nuts.', 'Unmeasured DB23 and bought-hardware reference shapes. Shell bonding wires are omitted.'],
      'open':['The large PCB mounting pads align with the original motherboard anchor holes; J4 provides shell-bond pads.', 'M3 x 12 mm screws; insulating washers below the motherboard and nuts directly on the PCB mounting pads.'],
      'exploded':['The DB23 and PCB move together. Two screws enter from below the motherboard; fit the cover last.', 'Offsets show part relationships, not a required insertion direction for every component.'],
      'holder':['The broad underside is coplanar at Z0 while the PCB support plane remains at Z5.75.', 'All 23 pins remain guided below the PCB. Strength, print fit and soldering heat still require physical trials.'],
      'parts':['Actual printable geometry: base at its assembly position, cap in its roof-down print orientation.', 'Keyed contact faces locate the cover; flexible latches and nut-retaining tongues need a print-fit trial.'],
      'jig':['Load equal-length pins against the lower-tip stop, then remove the jig before soldering.', 'The jig is a loading aid and is not fitted to the motherboard. Test pin retention after transfer.']}
    annotate(OUT/name,titles[mode],notes[mode])

if __name__=='__main__':
    paths=build_meshes()
    for mode,name,camera in [('assembly','assembly-isometric.png',(64,-72,50)),('open','assembly-cap-removed.png',(64,72,60)),('exploded','assembly-exploded.png',(65,84,67)),('holder','holder-isometric.png',(64,72,65)),('parts','base-and-cap.png',(68,82,67)),('jig','pin-height-jig.png',(64,72,60))]:render(paths,mode,name,camera)
    print('Rendered six coordinated revision '+REV+' CAD views')
