#!/usr/bin/env python3
"""Generate the prototype review PDF from shared geometry and CAD previews."""
from pathlib import Path
import json,math
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor,white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

ROOT=Path(__file__).resolve().parents[1]
P=json.loads((ROOT/'source/design_parameters.json').read_text());B=P['pcb'];M=P['motherboard'];H=P['holder']
FONT='/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('DSans',FONT+'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DSans-Bold',FONT+'DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('DSans',normal='DSans',bold='DSans-Bold')
REV=P['revision']
OUT=ROOT/f'previews/DB23_Prototype_Drawings_v{REV}.pdf'
c=canvas.Canvas(str(OUT),pagesize=A4);c.setTitle(f'Amiga DB23 Replacement - Prototype Drawings v{REV}');c.setAuthor('UK Computing Limited')
NAVY=HexColor('#183b50');BLUE=HexColor('#2e6e90');INK=HexColor('#253946');GREY=HexColor('#647985');PALE=HexColor('#edf3f6');LINE=HexColor('#c6d6de')

def txt(x,y,s,size=9,bold=False,col=INK):
 c.setFillColor(col);c.setFont('DSans-Bold' if bold else 'DSans',size);c.drawString(x*mm,y*mm,s)
def line(x1,y1,x2,y2,col=LINE,w=.5):
 c.setStrokeColor(col);c.setLineWidth(w);c.line(x1*mm,y1*mm,x2*mm,y2*mm)
def para(x,y,s,width=174,size=9,leading=12):
 p=Paragraph(s,ParagraphStyle('p',fontName='DSans',fontSize=size,leading=leading,textColor=INK));_,h=p.wrap(width*mm,999)
 p.drawOn(c,x*mm,y*mm-h);return y-h/mm
def header(num,title,sub):
 c.setFillColor(NAVY);c.rect(0,279*mm,210*mm,18*mm,fill=1,stroke=0)
 txt(18,286,'UK COMPUTING  /  AMIGA HARDWARE',9,True,white)
 txt(18,264,title,20,True,NAVY);txt(18,256,sub,8.6,col=GREY)
 line(18,17,192,17);txt(18,11,f'29 October 2026 | Holder revision {REV} | Fit prototype; physical fit unverified',7,col=GREY)
 txt(181,11,f'{num} / 4',7,col=GREY)
def image(name,x,y,w,h):c.drawImage(str(ROOT/'previews'/name),x*mm,y*mm,width=w*mm,height=h*mm,preserveAspectRatio=True,anchor='c',mask='auto')
def table(y,rows):
 for i,(a,b) in enumerate(rows):
  yy=y-i*8
  if i%2==0:c.setFillColor(PALE);c.rect(18*mm,(yy-2)*mm,174*mm,8*mm,fill=1,stroke=0)
  txt(21,yy,a,8.4);txt(111,yy,b,8.4,True)

header(1,'DB23 replacement assembly','Solid one-piece cradle + solder-cup DB23 + original 23-pin motherboard interface')
image('assembly-isometric.png',18,135,174,116)
para(18,129,'The revised cradle carries the connector flange, 23-pin guide and PCB supports in one continuous part. '
     'Raised end lugs and a filled rear replace the low rails and rear opening of revision 0.3. '
     'The male RGB and female floppy PCBs retain electrical revision 0.3.',size=9.2,leading=13)
table(101,[('PCB outline','40.00 x 12.00 mm, notched front'),('PCB thickness / underside height','1.00 mm / Z5.75 mm assumed'),
          ('Holder width / rear position','52.00 mm / Y15.60 mm'),('Motherboard pin grid','2.77 pitch; 2.84 row spacing'),
          ('Original shell anchor centres','44.27 mm; Y9.50 mm')])
para(18,52,'<b>Prototype status:</b> the views use an unmeasured solder-cup connector and hardware envelope. '
     'The larger section is a geometric reinforcement; insertion strength, print fit and soldering heat '
     'performance still require trials with the selected parts. The PCB and all 23 circuits are unchanged.',size=8.5,leading=11.7)
c.showPage()

header(2,'The solid cradle and loading jig','The printed structure stays assembled; the loading jig is removed before soldering')
image('holder-isometric.png',18,139,174,111)
txt(18,132,'Continuous support around the pin guide',11,True,NAVY)
para(18,125,'The side lugs rise to the PCB support plane at Z5.75 mm, and rear infill closes the old opening. '
     'The pin-guide top remains at Z4.50 mm, leaving a 1.25 mm underside gap at the tail joints. '
     'Local shield-wire relief and access to the original mounting holes are retained.',size=9,leading=12)
image('pin-height-jig.png',18,39,98,70)
txt(121,100,'Set all 23 pins together',10,True,NAVY)
para(121,93,'Support the holder in the separate jig. Push equal-length pins gently down to the common lower stop. '
     'The default 10.70 mm pin spans Z-3.20 to Z7.50 mm.<br/><br/>'
     'Remove the jig vertically, then lower the soldered DB23 + PCB onto the pins and solder the top joints.',width=71,size=8.5,leading=11.5)
para(18,35,'<b>Mounting:</b> retain both 0.60 mm anchor shims beneath the cradle feet. The raised lugs retain '
     'recessed anchor-head seats at Z2.40 mm. Preload their bolts before lowering the PCB. The jig is a loading tool, not a heat-safe soldering fixture.',size=8,leading=10.5)
c.showPage()

header(3,'Assembly in four parts','The soldered DB23 and PCB are lowered together, then the port hardware is fitted')
image('assembly-exploded.png',18,131,174,119)
def stage(y,title,body):
 txt(18,y,title,10,True,NAVY)
 return para(18,y-6,body,size=8.4,leading=11.2)
stage(122,'Part 1 - DB23 + PCB',
      'Identify the matching male or female pin numbers. Solder both rows of cups to the PCB away from the printed cradle. '
      'Prepare any underside shield joints or leads before access is restricted.')
stage(99,'Part 2 - Pins + cradle, then lower the joined assembly',
      'Load the 23 pins using the height jig. Remove the jig and preload the recessed motherboard anchor bolts. '
      'Lower the completed DB23 + PCB from above, seat it on the supports, then solder all 23 top pin joints.')
stage(75,'Part 3 - Nuts, hex jackposts and optional caps',
      'Drop the nuts into the top-loading pockets, fit the matching jackposts through the DB23 flange and add the optional caps. '
      'Check stem, anchor-head and tool clearances; do not overtighten the printed pockets.')
stage(51,'Part 4 - Attach and solder to the motherboard',
      'First check all 23 circuits and the separate shell bond on the standalone assembly. Fit the two 0.60 mm shims and '
      'positively secure the original mounting holes, then solder the motherboard tails and complete the shell connection.')
c.showPage()

header(4,'Fit references and measurements','Full-size pin templates below: print at 100% / Actual size, with no page scaling')
txt(18,244,'Motherboard top view; flange faces the top of the page',10,True,NAVY)
txt(18,238,'Pin 1 is mirrored between variants. PCB corner notches clear the printed nut towers.',8,col=GREY)
def fp(cx,top,gender):
 def xy(x,y):return((cx+x)*mm,(top-y)*mm)
 c.setStrokeColor(GREY);c.setLineWidth(.45);c.line(*xy(-25.135,0),*xy(25.135,0))
 txt(cx-25,top+3,gender+' / '+('RGB' if gender=='MALE' else 'FLOPPY'),8,True,NAVY)
 # Actual notched PCB outline in the same front-flange datum.
 path=c.beginPath();path.moveTo(*xy(*B['outline_xy'][0]))
 for pt in B['outline_xy'][1:]:path.lineTo(*xy(*pt))
 path.close();c.setStrokeColor(BLUE);c.drawPath(path,stroke=1,fill=0)
 for n in range(1,24):
  x=(6.5-n)*M['pin_pitch'] if n<=12 else(18-n)*M['pin_pitch']
  if gender=='FEMALE':x=-x
  y=M['rear_row_y'] if n<=12 else M['front_row_y'];xx,yy=xy(x,y)
  c.setStrokeColor(INK);c.circle(xx,yy,M['signal_hole_reference']/2*mm,stroke=1,fill=0)
  if n in(1,12,13,23):
   c.setFont('DSans',5);c.setFillColor(INK);c.drawCentredString(xx,yy+(-3.1*mm if n<=12 else 2.0*mm),str(n))
 for x in(-22.135,22.135):
  xx,yy=xy(x,9.5);c.circle(xx,yy,1.6*mm,stroke=1,fill=0)
 txt(cx-25,top-22,'Blue outline: actual adapter PCB',6.6,col=BLUE)
fp(53,225,'MALE');fp(151,225,'FEMALE')
line(18,190,68,190,INK,.8);line(18,188.5,18,191.5,INK,.8);line(68,188.5,68,191.5,INK,.8);txt(73,188.8,'50.00 mm scale check',8,True)

txt(18,177,'Pin-hole test coupon',11,True,NAVY)
para(18,171,'The supplied STL includes trial bores from 0.75 to 1.10 mm and the complete 23-hole pattern. '
     'A 0.64 mm square pin has a 0.905 mm diagonal: 0.80 mm is not a finished clearance bore. '
     'Start with the coupon and actual pins; determine the required drilled or reamed fit.',size=9,leading=12)
txt(18,145,'Measure before freezing the PCB and holder',11,True,NAVY)
rows=[('Purchased DB23 part number / gender','____________________________'),
      ('Gap between cups / usable cup length','____________________________'),
      ('Flange to rear body / cup-end depth','____________________________'),
      ('Actual pin section / finished guide bore','____________________________'),
      ('Jackpost rear thread / stem projection','____________________________'),
      ('Nut AF / thickness / pocket fit','____________________________'),
      ('Target motherboard / case clearance','____________________________')]
table(134,rows)
para(18,68,'<b>Datum:</b> Y0 is the flange front plane; assumed flange metal spans Y0-0.50. '
     'The holder begins Y0.65. Its bottom is Z0.60 above the motherboard; the two 0.60 mm '
     'anchor shims preserve the intended height. Jackpost stems and anchor bolt heads must '
     'clear one another. See mechanical/MECHANICAL_NOTES.txt for the nominal envelopes.',size=8.4,leading=11.5)
para(18,43,'<b>Sources:</b> original connector grid and reference geometry: iComp DB23 replacement drawings. '
     'All solder-cup, nut, printer and fastener assumptions are recorded in source/design_parameters.json. '
     'Native electrical and mesh reports are in verification/ and mechanical/.',size=8,leading=11)
c.save();print(OUT)
