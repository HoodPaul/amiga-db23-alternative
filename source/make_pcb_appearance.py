#!/usr/bin/env python3
"""Colour native KiCad SVG plots as black-mask/white-silk/ENIG appearance views.

No CAD geometry is modified. Tracks under the mask are hidden by recolouring;
mask openings and native silk paths keep their exported positions and shapes.
Requires Inkscape to rasterise the SVG output.
"""
from pathlib import Path
import re,subprocess,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'previews'
SVG='{http://www.w3.org/2000/svg}'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONTB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
for side,name in [('F','top'),('B','bottom')]:
 root=ET.parse(OUT/'native'/f'DB23M_RGB-{side}.svg').getroot()
 edges=[]
 for el in root.iter():
  style=el.attrib.get('style','')
  if '#D0D2CD' in style:
   for path in el.findall(SVG+'path'):
    coords=re.findall(r'[-+]?\d*\.?\d+',path.attrib.get('d',''))
    if len(coords)==4:edges.extend([(float(coords[0]),float(coords[1])),(float(coords[2]),float(coords[3]))])
 if not edges:raise RuntimeError('No native edge coordinates')
 xmin=min(x for x,y in edges);xmax=max(x for x,y in edges);ymin=min(y for x,y in edges);ymax=max(y for x,y in edges)
 xo=(xmin+xmax)/2;yo=ymin-4.0
 points=[(-18,4),(18,4),(18,5.5),(20,5.5),(20,16),(-20,16),(-20,5.5),(-18,5.5)]
 bg=ET.Element(SVG+'polygon',{'points':' '.join(f'{xo+x},{yo+y}' for x,y in points),'fill':'#171b1e'})
 root.insert(2,bg)
 # Native bottom SVG ordering can draw copper after mask openings. Remove copper
 # paths entirely because the intended finished mask covers those tracks.
 for parent in list(root.iter()):
  for child in list(parent):
   st=child.attrib.get('style','')
   if '#C83434' in st or '#4D7FC4' in st:parent.remove(child)
 for el in root.iter():
  st=el.attrib.get('style','')
  mask=('#D864FF' in st or '#02FFEE' in st)
  for old,new in [('#C83434','#171b1e'),('#4D7FC4','#171b1e'),('#D864FF','#d8b449'),('#02FFEE','#d8b449'),('#F2EDA1','#ffffff'),('#E8B2A7','#ffffff'),('#D0D2CD','#647079')]:st=st.replace(old,new)
  if mask:st=re.sub(r'(fill|stroke)-opacity:[^;]+',lambda m:m.group(1)+'-opacity:1.0',st)
  if st:el.attrib['style']=st
 root.attrib['viewBox']=f'{xmin-.6} {ymin-.6} {xmax-xmin+1.2} {ymax-ymin+1.2}'
 root.attrib['width']='164.8mm';root.attrib['height']='52.8mm'
 svg=OUT/f'pcb-male-{name}-appearance.svg';png=OUT/f'pcb-male-{name}.png'
 ET.ElementTree(root).write(svg,encoding='utf-8',xml_declaration=True)
 subprocess.run(['inkscape',str(svg),'--export-type=png',f'--export-filename={png}','--export-width=1800','--export-background=white','--export-background-opacity=1'],check=True,stdout=subprocess.DEVNULL)
 im=Image.open(png).convert('RGB');canvas=Image.new('RGB',(1800,im.height+135),'white');canvas.paste(im,(0,80));d=ImageDraw.Draw(canvas)
 d.rectangle((0,0,1800,7),fill='#183b50');d.text((34,22),f'DB23M RGB - {name} appearance',font=ImageFont.truetype(FONTB,29),fill='#183b50')
 d.text((34,im.height+91),'Native KiCad geometry; proposed black solder mask, white silkscreen and gold exposed pads.',font=ImageFont.truetype(FONT,18),fill='#526873')
 canvas.save(png)
 print(png)
