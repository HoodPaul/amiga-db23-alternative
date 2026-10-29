#!/usr/bin/env python3
"""Generate the review drawings from shared dimensions and actual CAD previews.

The vector pin templates are at 1:1. Reference hardware and the selected DB23
still require physical measurement; this PDF is not a fabrication approval.
"""
from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/'source/design_parameters.json').read_text());B=P['pcb'];M=P['motherboard'];H=P['holder'];F=P['mounting'];REV=P['revision']
FONT='/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('DSans',FONT+'DejaVuSans.ttf'));pdfmetrics.registerFont(TTFont('DSans-Bold',FONT+'DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('DSans',normal='DSans',bold='DSans-Bold')
OUT=ROOT/f'previews/DB23_Prototype_Drawings_v{REV}.pdf'
c=canvas.Canvas(str(OUT),pagesize=A4);c.setTitle(f'Amiga DB23 Replacement - Prototype Drawings v{REV}');c.setAuthor('UK Computing Limited')
NAVY=HexColor('#183b50');BLUE=HexColor('#2e6e90');INK=HexColor('#253946');GREY=HexColor('#647985');PALE=HexColor('#edf3f6');LINE=HexColor('#c6d6de');GOLD=HexColor('#b9913f')

def txt(x,y,s,size=9,bold=False,col=INK):
 c.setFillColor(col);c.setFont('DSans-Bold' if bold else 'DSans',size);c.drawString(x*mm,y*mm,s)
def line(x1,y1,x2,y2,col=LINE,w=.5):
 c.setStrokeColor(col);c.setLineWidth(w);c.line(x1*mm,y1*mm,x2*mm,y2*mm)
def para(x,y,s,width=174,size=9,leading=12):
 p=Paragraph(s,ParagraphStyle('p',fontName='DSans',fontSize=size,leading=leading,textColor=INK));_,h=p.wrap(width*mm,999);p.drawOn(c,x*mm,y*mm-h);return y-h/mm

def header(num,title,sub):
 c.setFillColor(NAVY);c.rect(0,279*mm,210*mm,18*mm,fill=1,stroke=0)
 txt(18,286,'UK COMPUTING  /  AMIGA HARDWARE',9,True,white)
 txt(18,264,title,20,True,NAVY);txt(18,256,sub,8.5,col=GREY)
 line(18,17,192,17);txt(18,11,f'29 October 2026 | Revision {REV} | Fit prototype; physical fit unverified',7,col=GREY);txt(181,11,f'{num} / 5',7,col=GREY)

def image(name,x,y,w,h):c.drawImage(str(ROOT/'previews'/name),x*mm,y*mm,width=w*mm,height=h*mm,preserveAspectRatio=True,anchor='c',mask='auto')
def table(y,rows,left=18,width=174,col2=111,step=8,size=8.4):
 for i,(a,b) in enumerate(rows):
  yy=y-i*step
  if i%2==0:c.setFillColor(PALE);c.rect(left*mm,(yy-2)*mm,width*mm,step*mm,fill=1,stroke=0)
  txt(left+3,yy,a,size);txt(col2,yy,b,size,True)

def stage(y,title,body):
 txt(18,y,title,10,True,NAVY);return para(18,y-6,body,size=8.3,leading=11.2)

header(1,'DB23 replacement assembly','Shorter mounting-ear PCB, solid printed base and black keyed clip-on cap')
image('assembly-isometric.png',18,138,174,113)
para(18,132,'The revision 0.5 assembly uses two metal screws from beneath the motherboard, through a solid base and the adapter PCB, with insulating washers below the motherboard and nuts above the adapter PCB. '
     'The cover conceals the mounting hardware and retains the jackpost nuts; it is not the primary cable-load attachment.',size=9.2,leading=13)
table(104,[('Adapter PCB overall width / depth','51.20 / 9.00 mm (Y4.00-13.00)'),('PCB thickness / underside height','1.00 mm / Z5.75 mm assumed'),('Printed base width / rear position','52.00 mm / Y13.00 mm'),('Printed cap width / rear position','52.00 mm / Y13.20 mm'),('Original shell mounting centres','44.27 mm; Y9.50 mm')])
para(18,58,'<b>OEM comparison:</b> iComp\'s original-equivalent drawing has a 50.27 mm width and 12.50 mm depth behind the flange datum. '
     'The present printed envelope is 52.00 mm wide and reaches Y13.20: +0.865 mm per side and +0.70 mm at the rear. '
     'The signal-hole pattern and nominal mating centreline are retained.',size=8.5,leading=11.5)
para(18,34,'<b>Fit prototype:</b> purchased connector, printed fit, clamping, underside clearance and cable-load strength remain unverified. '
     'The DB23 body, cups and bought hardware in the views are explicitly assumed reference shapes.',size=8,leading=10.5)
c.showPage()

header(2,'The two printed parts','A solid base carries the PCB; a keyed cover clips onto the front towers')
image('base-and-cap.png',18,143,174,108)
para(18,137,'The base has continuous end supports and integrated feet at the original mounting positions. No separate 0.60 mm shims are used in this revision. '
     'Its 23-pin guide remains below the adapter PCB, leaving the nominal 1.25 mm solder-fillet and heat gap. J4 reliefs clear covered underside joints.',size=8.8,leading=12)
image('pin-height-jig.png',18,49,98,70)
txt(121,112,'Load the pins first',10,True,NAVY)
para(121,105,'Print the hole-fit coupon and clip-fit pair before the full parts. The trial guide diameter is 0.92 mm for assumed 0.64 mm square pins; their diagonal is 0.905 mm. '
     'A finished 0.80 mm bore does not clear them.<br/><br/>Use the separate loading jig to set the lower tips. Equal 10.70 mm pins span Z-3.20 to Z7.50. '
     'Remove the jig before soldering and check that the base retains the pins.',width=71,size=8.3,leading=11.2)
para(18,42,'<b>Printing:</b> the base, cap, jig and hole coupon are trial parts. Follow the mechanical notes for print orientations and cap assembly transforms. '
     'The cap\'s flexible latches, nut tongues and keyed surfaces need an actual print-fit trial; material, soldering heat and long-term strength have not been validated.',size=8.2,leading=11)
c.showPage()

header(3,'Assembly in four parts','The DB23 and PCB stay joined; upward mounting screws are fitted during installation')
image('assembly-exploded.png',18,133,174,117)
stage(124,'Part 1 - Join the DB23 and PCB',
      'Identify the matching male or female pin numbers. Solder both rows of cups to the PCB away from the printed base. '
      'Prepare the shell bond at the dedicated J4 pads and finish any covered underside joints.')
stage(99,'Part 2 - Load pins, then lower the joined assembly',
      'Load equal-length pins into the base using the height jig. Remove the jig, retain the pins in a heat-safe fixture and lower the complete DB23 + PCB from above. '
      'Seat the PCB fully, then solder all 23 pin tops.')
stage(73,'Part 3 - Fit the jackpost hardware',
      'Insert the jackpost nuts and fit the hex posts through the connector flange. Check actual flange bearing, nut fit and rear stem projection. '
      'Leave the decorative cap off while fitting and checking the mounting hardware.')
stage(48,'Part 4 - Mount, solder, check, then cap',
      'Check all 23 circuits off the motherboard. Pre-tack the motherboard shell-pad lead with the base removed, then route it through the foot groove. Install screws upwards from below, with insulating washers below the motherboard and nuts on the PCB mounting pads. '
      'Secure the supported stack, solder the motherboard tails and complete the shell bond. Inspect and test before clipping the cover on last.')
c.showPage()

header(4,'Upward screw mounting stack','Nominal dimensions only; the actual motherboard, washer and nut must be measured')
uwt=F['underside_washer_thickness_assumed'];seat=-M['thickness_assumed']-uwt;pcb_top=B['bottom_z']+B['thickness'];washer_top=pcb_top+F['washer_thickness_assumed'];nut_top=washer_top+F['nut_height_assumed'];tip=seat+F['screw_length_under_head']
cap_under=P.get('cap',{}).get('roof_bottom_z',11.0)
table(243,[('Motherboard thickness assumed',f"{M['thickness_assumed']:.2f} mm"),('Motherboard top to PCB underside',f"{B['bottom_z']:.2f} mm"),('Adapter PCB thickness',f"{B['thickness']:.2f} mm"),('Underside insulating washer',f"{uwt:.2f} mm"),('Nut height; no top washer',f"{F['nut_height_assumed']:.2f} mm"),('Total under head to top of nut',f'{nut_top-seat:.2f} mm')])
# Enlarged local section: the vertical scale is explicit and does not alter the 1:1 pin templates.
scale=4.2;cx=61;z0=139
Y=lambda z:z0+z*scale

def rect(x0,x1,z1,z2,fill):
 c.setFillColor(fill);c.setStrokeColor(INK);c.setLineWidth(.35);c.rect(x0*mm,Y(z1)*mm,(x1-x0)*mm,(z2-z1)*scale*mm,fill=1,stroke=1)
# Split surfaces around the clearance bore leave the shaft visible.
for a,b in ((cx-22,cx-7),(cx+7,cx+22)):
 rect(a,b,-M['thickness_assumed'],0,HexColor('#73967b'));rect(a,b,0,B['bottom_z'],HexColor('#56616a'));rect(a,b,B['bottom_z'],pcb_top,HexColor('#273947'))
rect(cx-F['underside_washer_diameter_assumed']/2*scale,cx+F['underside_washer_diameter_assumed']/2*scale,seat,-M['thickness_assumed'],HexColor('#9eabb4'))
rect(cx-F['head_diameter_assumed']/2*scale,cx+F['head_diameter_assumed']/2*scale,seat-F['head_height_assumed'],seat,HexColor('#c0c9cf'))
rect(cx-1.5*scale,cx+1.5*scale,seat,tip,HexColor('#b8c1c7'))
if F['washer_thickness_assumed']>0:rect(cx-3*scale,cx+3*scale,pcb_top,washer_top,HexColor('#d4dce1'))
rect(cx-F['nut_across_flats_assumed']/2*scale,cx+F['nut_across_flats_assumed']/2*scale,washer_top,nut_top,HexColor('#aebbc3'))
rect(cx-22,cx+22,cap_under,cap_under+1.2,HexColor('#394650'))
for z,label in [(cap_under+.6,'Clip-on cap roof'),(tip,f'M3 x 12 tip: Z{tip:.2f}'),(nut_top-.6,'Nut directly on PCB pad'),(3,'Solid base / supported PCB'),(-.4,'Motherboard'),(seat-.6,'Head + insulating washer')]:
 line(cx+22,Y(z),116,Y(z),GREY,.4);txt(119,Y(z)-1,label,7.8)
txt(25,124,'Local section enlarged; geometry simplified',7.4,col=GREY)
txt(18,112,'Length selection',11,True,NAVY)
table(101,[('Screw length below head','Projection past nut / tip height'),('12.00 mm - default',f'{12-(nut_top-seat):.2f} mm / Z{12+seat:.2f}'),('14.00 mm',f'{14-(nut_top-seat):.2f} mm / Z{14+seat:.2f}'),('16.00 mm',f'{16-(nut_top-seat):.2f} mm / Z{16+seat:.2f}')],size=8.2)
para(18,64,'<b>Cap clearance:</b> the default 12 mm screw ends at Z9.90, below the nominal roof underside at Z11.00. '
     'Untrimmed 14 mm and 16 mm screws project into the cover envelope and are not default-compatible. '
     'Changing the insulating washer, nut, board thickness or cap geometry requires rechecking the complete stack.',size=8.4,leading=11.4)
para(18,38,'<b>Original holes only:</b> the 7 mm head sits over an 8 mm insulating washer. Allow 1.50 mm total projection below the motherboard. Verify chassis and copper clearance; the shell bond remains a separate wire connection. '
     'The washer pair spans 52.27 mm: 0.135 mm beyond each side of the 52 mm print. Do not countersink the motherboard. Wire routing and actual chassis clearance still need a fit check.',size=8,leading=10.5)
c.showPage()

header(5,'Pin templates and fit worksheet','Print this page at 100% / Actual size with no page scaling')
txt(18,244,'Motherboard top view; connector faces the top of the page',9.7,True,NAVY)
txt(18,238,'Signal holes and shell anchors retain the original nominal grid. J4 belongs to the adapter only.',7.7,col=GREY)

def fp(cx,top,gender):
 def xy(x,y):return((cx+x)*mm,(top-y)*mm)
 c.setStrokeColor(GREY);c.setLineWidth(.4);c.line(*xy(-25.135,0),*xy(25.135,0));txt(cx-25.5,top+3,gender+' / '+('RGB' if gender=='MALE' else 'FLOPPY'),8,True,NAVY)
 path=c.beginPath();path.moveTo(*xy(*B['outline_xy'][0]))
 for pt in B['outline_xy'][1:]:path.lineTo(*xy(*pt))
 path.close();c.setStrokeColor(BLUE);c.drawPath(path,stroke=1,fill=0)
 for n in range(1,24):
  x=(6.5-n)*M['pin_pitch'] if n<=12 else (18-n)*M['pin_pitch']
  if gender=='FEMALE':x=-x
  y=M['rear_row_y'] if n<=12 else M['front_row_y'];xx,yy=xy(x,y);c.setStrokeColor(INK);c.circle(xx,yy,M['signal_hole_reference']/2*mm,stroke=1,fill=0)
  if n in(1,12,13,23):c.setFont('DSans',5);c.setFillColor(INK);c.drawCentredString(xx,yy+(-3.0*mm if n<=12 else 1.7*mm),str(n))
 for side in(-1,1):
  xx,yy=xy(side*M['anchor_spacing']/2,M['anchor_y']);c.setStrokeColor(INK);c.circle(xx,yy,M['anchor_hole_reference']/2*mm,stroke=1,fill=0)
  xx,yy=xy(side*B['shell_bond_pad_x'],B['shell_bond_pad_y']);c.setStrokeColor(BLUE);c.circle(xx,yy,B['shell_bond_pad_drill']/2*mm,stroke=1,fill=0)
 txt(cx-25.5,top-20,'Blue: adapter outline and J4 holes',6.4,col=BLUE)
fp(53,225,'MALE');fp(151,225,'FEMALE')
line(18,190,68,190,INK,.8);line(18,188.5,18,191.5,INK,.8);line(68,188.5,68,191.5,INK,.8);txt(73,188.8,'50.00 mm scale check',8,True)
txt(18,177,'Measure before fabrication or final assembly',11,True,NAVY)
rows=[('Purchased DB23 part / gender','____________________________'),('Cup gap / cup length / body depth','____________________________'),('Actual motherboard / PCB thickness','____________________________'),('Pin section / finished bore / retention','____________________________'),('Jackpost rear thread / stem projection','____________________________'),('Nut AF / thickness / pocket fit','____________________________'),('Upward screw / washer / nut stack','____________________________'),('Head bearing / underside chassis gap','____________________________'),('Cap latch fit / removal / tip clearance','____________________________'),('Shell bond / clamping / insertion trial','____________________________')]
table(165,rows)
para(18,73,'<b>Coordinate system:</b> X runs across the connector; Y points inward from the flange front plane; Z is measured upward from the motherboard top. '
     'Male pin 1 is at positive X in this top view; female numbering is mirrored. The pin pitch is 2.77 mm, row spacing 2.84 mm and row stagger 1.385 mm.',size=8.5,leading=11.5)
para(18,48,'<b>Sources:</b> original nominal connector grid and envelope: iComp DB23 replacement drawings. All selected design choices and unmeasured envelopes are in source/design_parameters.json. '
     'See docs/VALIDATION.md for actual saved-file checks and the physical work still outstanding.',size=8.2,leading=11)
c.save();print(OUT)
