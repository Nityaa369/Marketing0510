#!/usr/bin/env python3
"""Google sizes of the SAME 10 creative images used in the Meta kit. Nothing on the ad is changed:
only resized. Where the shape differs, the whole ad is kept on a colour wash made from its own edge pixels."""
import glob, os
from PIL import Image, ImageFilter
Z='/tmp/claude-0/-home-user-Marketing0510/54fb68af-29ff-5f82-8df2-53b8e402c4c0/scratchpad/imgs/Images for tech law /'
def zf(k): return [f for f in glob.glob(Z+'*.png') if os.path.basename(f).startswith(k)][0]
SRC={'01':zf('Legal Minds '),'02':zf('Fintech Law'),'03':'/tmp/claude-0/-home-user-Marketing0510/54fb68af-29ff-5f82-8df2-53b8e402c4c0/images/4.webp','04':zf('From Busines'),'05':zf('Return to La'),'06':zf('New City, Ne'),'07':zf('Global Legal'),'08':zf('Tech Law Boo'),'09':zf('Flexible Leg'),'10':zf('Reignite You')}
NAME={'01':'hr','02':'banking','03':'content','04':'sales_ops','05':'back_from_break','06':'moved_city','07':'abroad','08':'bpo_back_office','09':'returning','10':'left_firm'}
SIZES=[('landscape',1200,628),('square',1200,1200),('portrait',960,1200)]
def canvas(im,W,H):
    if abs(im.width/im.height-W/H)<0.02: return im.resize((W,H),Image.LANCZOS)
    s=min(W/im.width,H/im.height); fg=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    c=Image.new('RGB',(W,H)); x=(W-fg.width)//2; y=(H-fg.height)//2
    if y>0:
        c.paste(fg.crop((0,0,fg.width,3)).resize((fg.width,y+1)),(x,0)); c.paste(fg.crop((0,fg.height-3,fg.width,fg.height)).resize((fg.width,H-y-fg.height+1)),(x,y+fg.height-1))
    if x>0:
        c.paste(fg.crop((0,0,3,fg.height)).resize((x+1,fg.height)),(0,y)); c.paste(fg.crop((fg.width-3,0,fg.width,fg.height)).resize((x+1,fg.height)),(x+fg.width-1,y))
    c=c.filter(ImageFilter.GaussianBlur(14)); c.paste(fg,(x,y)); return c
for n,f in SRC.items():
    im=Image.open(f).convert('RGB')
    for tag,W,H in SIZES:
        canvas(im,W,H).save(f'{tag}_{W}x{H}/tlc1_{n}_{NAME[n]}_{tag}_{W}x{H}.jpg',quality=88,optimize=True,progressive=True)
print('done')
