#!/usr/bin/env python3
"""Render native CAD geometry and illustrative connector hardware using VTK.

The holder mesh comes from the printable OpenSCAD output. Connector rear-body,
solder cups and hardware envelopes are unmeasured references, not purchased-part
models. Run with an X display (Xvfb is sufficient for headless operation).
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
mb=P['motherboard']; pcb=P['pcb']; holder=P['holder']; con=P['connector_sample_assumptions']
REV=P['revision']

def box(x0,x1,y0,y1,z0,z1):
    return cq.Workplane('XY').box(x1-x0,y1-y0,z1-z0).translate(((x0+x1)/2,(y0+y1)/2,(z0+z1)/2)).val()
def cyl_z(x,y,z,r,h):
    return cq.Workplane('XY').workplane(offset=z).center(x,y).circle(r).extrude(h).val()
def cyl_y(x,y,z,r,h):
    return cq.Workplane('XZ',origin=(0,y,0)).center(x,z).circle(r).extrude(-h).val()
def hex_y(x,y,z,af,h,bore=0):
    rad=af/math.sqrt(3)
    pts=[(x+rad*math.cos(math.radians(a)),z+rad*math.sin(math.radians(a))) for a in range(30,360,60)]
    q=cq.Workplane('XZ',origin=(0,y,0)).polyline(pts).close().extrude(-h).val()
    if bore:q=q.cut(cyl_y(x,y-.02,z,bore/2,h+.04))
    return q
def compound(shapes): return cq.Compound.makeCompound(shapes)
def save(name,shape):
    path=MESH/(name+'.stl')
    cq.exporters.export(shape,str(path),tolerance=.035,angularTolerance=.1)
    return path
def pin_xy(n,gender='M'):
    x=(6.5-n)*mb['pin_pitch'] if n<=12 else (18-n)*mb['pin_pitch']
    if gender=='F':x=-x
    return x, mb['rear_row_y'] if n<=12 else mb['front_row_y']

def build_meshes():
    outline=pcb['outline_xy']; z=pcb['bottom_z']; t=pcb['thickness']
    board=cq.Workplane('XY').polyline(outline).close().extrude(t).translate((0,0,z)).val()
    for n in range(1,24):
        x,y=pin_xy(n);board=board.cut(cyl_z(x,y,z-.1,pcb['tail_drill']/2,t+.2))
    for x in (-pcb['shield_pad_x'],pcb['shield_pad_x']):
        board=board.cut(cyl_z(x,pcb['shield_pad_y'],z-.1,pcb['shield_pad_drill']/2,t+.2))
    paths={'pcb':save('pcb-reference',board)}
    pads=[]
    for n in range(1,24):
        x,y=pin_xy(n)
        for zz in (z-.045,z+t+.005):
            pads.append(cyl_z(x,y,zz,pcb['tail_pad_diameter']/2,.04).cut(cyl_z(x,y,zz-.01,pcb['tail_drill']/2,.06)))
        zz=z+t+.005 if n<=12 else z-.045
        pads.append(box(x-pcb['cup_pad_width']/2,x+pcb['cup_pad_width']/2,pcb['cup_pad_front_y'],pcb['cup_pad_front_y']+pcb['cup_pad_length'],zz,zz+.04))
    for x in (-pcb['shield_pad_x'],pcb['shield_pad_x']):
        for zz in (z-.045,z+t+.005):
            pads.append(cyl_z(x,pcb['shield_pad_y'],zz,pcb['shield_pad_diameter']/2,.04).cut(cyl_z(x,pcb['shield_pad_y'],zz-.01,pcb['shield_pad_drill']/2,.06)))
    paths['pads']=save('exposed-pad-reference',compound(pads))
    pins=[];halfp=holder['square_pin_size_assumed']/2
    for n in range(1,24):
        x,y=pin_xy(n);pins.append(box(x-halfp,x+halfp,y-halfp,y+halfp,holder['pin_bottom_z'],holder['pin_top_z']))
    paths['pins']=save('23-tail-pins-reference',compound(pins))
    # Flange FRONT plane is y=0; its metal thickness occupies positive y.
    flange=box(-con['flange_width']/2,con['flange_width']/2,0,con['flange_thickness'],0,con['flange_height'])
    for x in (-mb['anchor_spacing']/2,mb['anchor_spacing']/2):
        flange=flange.cut(cyl_y(x,-.02,mb['connector_centre_height'],1.65,con['flange_thickness']+.04))
    zc=mb['connector_centre_height']
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
        x,_=pin_xy(n);zz=zc+(mb['row_spacing']/2 if n<=12 else -mb['row_spacing']/2)
        contacts.append(cyl_y(x,-5.25,zz,.49,3.1))
        tube=cyl_y(x,con['rear_body_end_y'],zz,con['cup_outer_diameter']/2,con['cup_end_y']-con['rear_body_end_y'])
        tube=tube.cut(cyl_y(x,con['rear_body_end_y']-.02,zz,.47,con['cup_end_y']-con['rear_body_end_y']+.04))
        if n<=12: tube=tube.cut(box(x-1,x+1,con['rear_body_end_y']+.6,con['cup_end_y']+.1,zz,zz+1.1))
        else: tube=tube.cut(box(x-1,x+1,con['rear_body_end_y']+.6,con['cup_end_y']+.1,zz-1.1,zz))
        contacts.append(tube)
    paths['contacts']=save('23-db23-contacts-reference',compound(contacts))
    nuts=[];posts=[];anchors=[]
    for s in (-1,1):
        xx=s*mb['anchor_spacing']/2
        nuts.append(hex_y(xx,holder['nut_axis_y_assumed']-holder['nut_thickness_assumed']/2,zc,holder['nut_across_flats_assumed'],holder['nut_thickness_assumed'],3.0))
        posts.append(hex_y(xx,-4.8,zc,4.75,4.8,2.2))
        posts.append(cyl_y(xx,0,zc,1.48,4.8))
        # Low anchor head is separate from the horizontal cable jackpost.
        anchors.append(cyl_z(xx,mb['anchor_y'],-3.0,1.48,5.4))
        anchors.append(cyl_z(xx,mb['anchor_y'],2.4,2.8,2.1))
    paths['nuts']=save('m3-nuts-reference',compound(nuts))
    paths['posts']=save('short-jackposts-reference',compound(posts))
    paths['anchors']=save('anchor-bolts-reference',compound(anchors))
    return paths

COLOURS={'holder':(.40,.49,.55),'pcb':(.055,.065,.075),'pads':(.83,.64,.20),'pins':(.85,.66,.24),
         'shell':(.76,.81,.85),'insulator':(.08,.09,.105),'contacts':(.86,.68,.27),
         'nuts':(.66,.71,.75),'posts':(.74,.78,.82),'anchors':(.60,.66,.70),'keeper':(.38,.48,.54),'shim':(.43,.52,.57)}
def actor_for(path,key,offset=(0,0,0),rotate_y=0):
    reader=vtk.vtkSTLReader();reader.SetFileName(str(path));reader.Update()
    normals=vtk.vtkPolyDataNormals();normals.SetInputConnection(reader.GetOutputPort());normals.SetFeatureAngle(35)
    mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(normals.GetOutputPort())
    actor=vtk.vtkActor();actor.SetMapper(mapper);actor.SetPosition(*offset)
    if rotate_y:actor.RotateY(rotate_y)
    mat=actor.GetProperty();mat.SetColor(*COLOURS[key]);mat.SetInterpolationToPBR()
    mat.SetMetallic(.7 if key in ('shell','pads','pins','contacts','nuts','posts','anchors') else .0)
    mat.SetRoughness(.34 if key in ('shell','contacts','posts') else .68)
    return actor

FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONTB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def annotate(path,title,subtitle,notes):
    im=Image.open(path).convert('RGB');w,h=im.size
    canvas=Image.new('RGB',(w,h+170),'#ffffff');canvas.paste(im,(0,100))
    d=ImageDraw.Draw(canvas);d.rectangle((0,0,w,9),fill='#17394e')
    d.text((42,24),title,font=ImageFont.truetype(FONTB,30),fill='#17394e')
    d.text((42,65),subtitle,font=ImageFont.truetype(FONT,19),fill='#526873')
    d.rectangle((0,h+100,w,h+170),fill='#edf3f6')
    for i,n in enumerate(notes):d.text((42,h+112+i*25),n,font=ImageFont.truetype(FONT,17),fill='#354b59')
    canvas.save(path)

def render(paths,mode,name,camera=(64,72,50)):
    renderer=vtk.vtkRenderer();renderer.SetBackground(.99,.995,1);renderer.SetBackground2(.89,.93,.96);renderer.GradientBackgroundOn()
    if mode=='holder':
        renderer.AddActor(actor_for(ROOT/f'mechanical/DB23_Holder_v{REV}.stl','holder'))
    else:
        renderer.AddActor(actor_for(ROOT/f'mechanical/DB23_Holder_v{REV}.stl','holder'))
        exploded=mode=='exploded';pz=15 if exploded else 0;cy=-12 if exploded else 0
        for key in ('pcb','pads'):renderer.AddActor(actor_for(paths[key],key,(0,0,pz)))
        renderer.AddActor(actor_for(paths['pins'],'pins'))
        for key in ('shell','insulator','contacts','posts'):renderer.AddActor(actor_for(paths[key],key,(0,cy,0)))
        for key in ('nuts','anchors'):renderer.AddActor(actor_for(paths[key],key))
        shim=ROOT/f'mechanical/DB23_Anchor_Shim_Single_v{REV}.stl'
        keeper=ROOT/f'mechanical/DB23_Nut_Keeper_v{REV}.stl'
        for s in (-1,1):
            if shim.exists():renderer.AddActor(actor_for(shim,'shim',(s*mb['anchor_spacing']/2,mb['anchor_y'],0)))
            if keeper.exists():renderer.AddActor(actor_for(keeper,'keeper',(s*mb['anchor_spacing']/2,0,12.2+(18 if exploded else 0)),180))
    for position,intensity in [((35,-50,95),1.0),((-55,15,50),.7),((0,65,90),.8)]:
        light=vtk.vtkLight();light.SetPosition(*position);light.SetFocalPoint(0,5,4);light.SetIntensity(intensity);renderer.AddLight(light)
    cam=renderer.GetActiveCamera();cam.SetPosition(*camera);cam.SetFocalPoint(0,3,9 if mode=='exploded' else 4)
    cam.SetViewUp(0,0,1);cam.ParallelProjectionOn();cam.SetParallelScale(31 if mode=='exploded' else 24)
    window=vtk.vtkRenderWindow();window.SetOffScreenRendering(1);window.AddRenderer(renderer);window.SetSize(1600,1000);window.SetMultiSamples(8)
    window.Render()
    capture=vtk.vtkWindowToImageFilter();capture.SetInput(window);capture.SetInputBufferTypeToRGB();capture.ReadFrontBufferOff();capture.Update()
    writer=vtk.vtkPNGWriter();writer.SetFileName(str(OUT/name));writer.SetInputConnection(capture.GetOutputPort());writer.Write();window.Finalize()
    titles={'assembly':'DB23 replacement - assembled CAD preview','exploded':'DB23 replacement - exploded CAD preview','holder':'Printed holder - actual printable CAD geometry'}
    notes={'assembly':['Black: adapter PCB. Grey: printed holder. Gold: contacts and supported motherboard pins.',
                       'FIT PROTOTYPE v0.3. Solder-cup connector and bought hardware are unmeasured references.'],
           'exploded':['PCB and nut keepers lifted; connector moved forwards. Pins remain in the printed guide block.',
                       'Exploded offsets are illustrative. Shell bonding wires are omitted; they remain required.'],
           'holder':['23 guide bores, two captive nut pockets, original-position anchor holes and rear PCB support.',
                     'Default guide bore 0.92 mm. Print and drill the fit coupon before the complete holder.']}
    annotate(OUT/name,titles[mode],'UK Computing Limited | Revision 0.3 | Nominal dimensions in millimetres',notes[mode])

if __name__=='__main__':
    paths=build_meshes()
    render(paths,'assembly','assembly-isometric.png')
    render(paths,'exploded','assembly-exploded.png',camera=(65,78,60))
    render(paths,'holder','holder-isometric.png')
    print('Rendered assembly-isometric.png, assembly-exploded.png, holder-isometric.png')
