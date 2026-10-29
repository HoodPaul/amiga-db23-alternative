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
OUT=ROOT/'previews/DB23_Prototype_Drawings_v0.3.pdf'
c=canvas.Canvas(str(OUT),pagesize=A4);c.setTitle('Amiga DB23 Replacement - Prototype Drawings v0.3');c.setAuthor('UK Computing Limited')
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
 line(18,17,192,17);txt(18,11,'29 October 2026 | Revision 0.3 | Fit prototype; physical fit unverified',7,col=GREY)
 txt(181,11,f'{num} / 3',7,col=GREY)
def image(name,x,y,w,h):c.drawImage(str(ROOT/'previews'/name),x*mm,y*mm,width=w*mm,height=h*mm,preserveAspectRatio=True,anchor='c',mask='auto')
def table(y,rows):
 for i,(a,b) in enumerate(rows):
  yy=y-i*8
  if i%2==0:c.setFillColor(PALE);c.rect(18*mm,(yy-2)*mm,174*mm,8*mm,fill=1,stroke=0)
  txt(21,yy,a,8.4);txt(111,yy,b,8.4,True)

header(1,'DB23 replacement assembly','Genuine DB23 solder-cup connector + two-layer PCB + printed pin-support holder')
image('assembly-isometric.png',18,124,174,127)
para(18,118,'A common printed holder supports 23 individual motherboard pins and the connector flange. '
     'Separate male RGB and female floppy PCBs retain the original Amiga cable interface. '
     'The 3D views use an illustrative, unmeasured solder-cup connector and fastener geometry.',size=9.2,leading=13)
table(91,[('PCB outline','40.00 x 12.00 mm, notched front'),('PCB thickness / underside height','1.00 mm / 5.75 mm assumed'),
          ('Holder width / rear position','52.00 mm / Y15.60 mm'),('Motherboard pin grid','2.77 pitch; 2.84 row spacing'),
          ('Shell anchor centres','44.27 mm; Y9.50 mm')])
para(18,44,'<b>Prototype status:</b> both boards pass native KiCad PCB DRC and exact connection checks. '
     'The holder is a closed printable solid. These checks do not establish fit, strength or soldering '
     'heat performance with the purchased parts. Complete the measurement worksheet before PCB manufacture.',size=8.4,leading=11.5)
c.showPage()

header(2,'Exploded view and assembly','PCB and nut retainers lifted; connector moved forwards for visibility')
image('assembly-exploded.png',18,124,174,127)
txt(18,115,'Parts per connector assembly',11,True,NAVY)
table(105,[('Solder-cup connector','1 DB23 male OR female'),('PCB and straight pins','1 matching PCB +23 pins'),
           ('Printed parts','1 holder; 2 shims; 2 optional caps'),('Cable jackposts and captive nuts','2 each; M3 rear / 4-40 front'),
           ('Motherboard anchors and shell bond','2 anchor sets; separate shield bond')])
txt(18,58,'Build order',11,True,NAVY)
para(18,52,'1. Measure the connector and pins; print the hole-fit coupon.<br/>'
     '2. Print and trial-fit the holder, nuts and mandatory 0.60 mm anchor shims.<br/>'
     '3. Set the 23 pin lengths and solder the PCB/DB23 using a heat-safe support.<br/>'
     '4. Check the complete unpowered assembly, shell bond and all 23 connections.',size=8.5,leading=11.7)
c.showPage()

header(3,'Fit references and measurements','Full-size pin templates below: print at 100% / Actual size, with no page scaling')
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
