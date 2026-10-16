# 60 distinct palettes: dark accent (white text passes contrast), light tint background.
# Distinct = CIELAB dE >= 12 on the accent, or on the (accent, background) pair.
import colorsys, math, itertools
def srgb_to_lab(rgb):
    def lin(c):
        c/=255; return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
    r,g,b=[lin(c) for c in rgb]
    x=(0.4124*r+0.3576*g+0.1805*b)/0.95047; y=(0.2126*r+0.7152*g+0.0722*b); z=(0.0193*r+0.1192*g+0.9505*b)/1.08883
    f=lambda t: t**(1/3) if t>0.008856 else 7.787*t+16/116
    return (116*f(y)-16, 500*(f(x)-f(y)), 200*(f(y)-f(z)))
def de(a,b): return math.dist(srgb_to_lab(a),srgb_to_lab(b))
def lum(rgb):
    def lin(c):
        c/=255; return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
    r,g,b=[lin(c) for c in rgb]; return 0.2126*r+0.7152*g+0.0722*b
def contrast(a,b):
    la,lb=sorted([lum(a),lum(b)],reverse=True); return (la+0.05)/(lb+0.05)
def hx(rgb): return '#%02X%02X%02X'%rgb
def build(n=60):
    out=[]
    cands=[]
    for L in (0.20,0.26,0.32,0.38,0.42):
        for h in range(0,360,6):
            for s in (0.45,0.65,0.85):
                rgb=tuple(int(round(c*255)) for c in colorsys.hls_to_rgb(h/360,L,s))
                if contrast(rgb,(255,255,255))>=4.6: cands.append((h,L,s,rgb))
    for h,L,s,rgb in cands:
        if all(de(rgb,o[1])>=12 for o in out):
            bg=tuple(int(round(c*255)) for c in colorsys.hls_to_rgb(h/360,0.93,0.45))
            hi=tuple(int(round(c*255)) for c in colorsys.hls_to_rgb(h/360,0.85,0.6))
            out.append((hx(rgb),rgb,hx(bg),hx(hi)))
        if len(out)==n: break
    return out
if __name__=="__main__":
    p=build(); print(len(p))
    m=min(de(a[1],b[1]) for a,b in itertools.combinations(p,2)); print("min dE accent",round(m,1))
