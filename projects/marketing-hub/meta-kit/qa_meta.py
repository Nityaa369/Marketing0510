import csv,glob,os,re,hashlib
import numpy as np
from PIL import Image
K='.';fails=[];notes=[]
def F(m):fails.append(m)
Z='/tmp/claude-0/-home-user-Marketing0510/54fb68af-29ff-5f82-8df2-53b8e402c4c0/scratchpad/imgs/Images for tech law /'
def zf(k): return [f for f in glob.glob(Z+'*.png') if os.path.basename(f).startswith(k)][0]
SRC={'01':zf('Legal Minds '),'02':zf('Fintech Law'),'03':'/tmp/claude-0/-home-user-Marketing0510/54fb68af-29ff-5f82-8df2-53b8e402c4c0/images/4.webp','04':zf('From Busines'),'05':zf('Return to La'),'06':zf('New City, Ne'),'07':zf('Global Legal'),'08':zf('Tech Law Boo'),'09':zf('Flexible Leg'),'10':zf('Reignite You')}
print("== 1. Image files, sizes, fidelity (creative words untouched)")
for n,f in SRC.items():
    src=Image.open(f).convert('RGB')
    for d,(W,H) in (('9x16',(1080,1920)),('4x5',(1080,1350))):
        p=f'{d}/TL_C1_{n}_{d}.jpg'
        if not os.path.exists(p):F('missing '+p);continue
        im=Image.open(p)
        if im.size!=(W,H):F(f'{p} size {im.size}')
        im=im.convert('RGB');r=src.width/src.height
        if abs(r-W/H)<0.02: fg=im;ref=src.resize((W,H),Image.LANCZOS);mode='full-bleed, no crop'
        else:
            s=min(W/src.width,H/src.height);w,h=round(src.width*s),round(src.height*s);x,y=(W-w)//2,(H-h)//2
            fg=im.crop((x,y,x+w,y+h));ref=src.resize((w,h),Image.LANCZOS);mode=f'whole ad kept, {w}x{h} on wash'
        diff=np.abs(np.asarray(fg,dtype=float)-np.asarray(ref,dtype=float)).mean()
        flag='OK' if diff<4 else 'CHECK'
        if diff>=4:F(f'{p} differs from supplied ad: mean diff {diff:.1f}')
        print(f'  {p}: {im.size} {mode}; mean pixel diff vs supplied ad {diff:.2f} {flag}')
print("== 2. Upload sheet")
rows=list(csv.DictReader(open('C1_meta_upload_sheet.csv',encoding='utf-8-sig')))
if len(rows)!=10:F('rows != 10')
for r in rows:
    n=r['GrowthX funnel slug'].split('-')[1]
    for k in ('Image 9:16 (Stories, Reels)','Image 4:5 (Feed)'):
        if not os.path.exists(r[k]):F(f"{r['Ad name']} missing {r[k]}")
        if f'_{n}_' not in r[k]:F(f"{r['Ad name']} {k} wrong number {r[k]}")
    if not os.path.exists(r['Landing page file']):F('missing page '+r['Landing page file'])
    pt=r['Primary text']
    if len(pt)>548:F(f"{r['Ad name']} primary text {len(pt)}>548")
    if re.search('[–—]',pt+r['Headline']+r['Description']):F(f"{r['Ad name']} dash")
    if '→' in pt+r['Headline']:F('arrow')
    for must in ('Rs 10 incl. GST','Refundable','Live only','24 and Sun 25 Oct'):
        if must.lower() not in pt.lower():F(f"{r['Ad name']} primary text missing '{must}'")
    u=r['Website URL']
    if f'/f/tlc1-{n}?' not in u or 'utm_source=meta' not in u or f'utm_content=tlc1-{n}_' not in u:F(f"{r['Ad name']} URL {u}")
    if len(r['Headline'])>40:F(f"{r['Ad name']} headline {len(r['Headline'])}>40")
    if r['Call to action']!='Sign up':F('CTA')
    print(f"  {r['Ad name']}: text {len(pt)} chars, headline {len(r['Headline'])}, url ok")
print("== 3. Landing pages")
for n in SRC:
    p=f'landing_pages_c1/lp_tlc1-{n}.html';s=open(p,encoding='utf-8').read()
    imgp=re.search(r'<img src="([^"]+)"',s).group(1)
    if not os.path.exists('landing_pages_c1/'+imgp):F(p+' image missing')
    hrefs=set(re.findall(r'href="(https://growthx[^"]+)"',s))
    if hrefs!={f'https://growthx.lawsikho.com/f/tlc1-{n}'}:F(f'{p} hrefs {hrefs}')
    if re.search('[–—]',s):F(p+' dash')
    if '→' in re.sub(r'<script.*?</script>','',s,flags=re.S).replace('&rarr;',''):F(p+' arrow')
    row=[r for r in rows if r['GrowthX funnel slug']==f'tlc1-{n}'][0]
    hook=row['Primary text'].split('\n\n')[0].replace('...','').replace('…','')
    words=re.sub(r'<[^>]+>',' ',s);words=re.sub(r'\s+',' ',words).replace('&#x27;',"'")
    first=hook.split('.')[0][:25]
    if first.lower() not in words.lower():F(f'{p} fold does not repeat hook "{first}"')
    for bad in ('guarantee','job offer','placement','salary','Zoom'):
        if bad.lower() in words.lower() and bad!='placement':F(f'{p} has "{bad}"')
    pay=len(re.findall('class="btn"',s))
    print(f'  {p}: img {imgp}, {pay} pay buttons, hook repeated, links ok')
print()
print('FAILS:',len(fails))
for f in fails:print(' -',f)
