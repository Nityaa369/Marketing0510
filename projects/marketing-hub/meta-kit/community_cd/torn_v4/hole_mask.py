"""Find the torn hole in the template: inside a loose outline, everything that is not the
neutral-white torn fringe, connected to the centre, holes filled, edges softened."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage

t = np.asarray(Image.open("src/template_01.webp").convert("RGB")).astype(int)
H, W = t.shape[:2]
loose = Image.new("L", (W, H), 0)
ImageDraw.Draw(loose).polygon([(110, 130), (300, 40), (560, 80), (820, 40), (960, 120), (1012, 330), (995, 560),
                               (1002, 700), (900, 742), (130, 742), (58, 560), (70, 330)], fill=255)
loose = np.asarray(loose) > 0
mx, mn = t.max(axis=2), t.min(axis=2)
fringe = (mn > 165) & ((mx - mn) < 48)
cand = loose & ~fringe
lab, _ = ndimage.label(cand)
m = lab == lab[400, 512]
m = ndimage.binary_closing(m, iterations=3)
m = ndimage.binary_fill_holes(m)
m = ndimage.binary_opening(m, iterations=2)
alpha = Image.fromarray((m * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(1.0))
alpha.save("src/hole_mask.png")
ys, xs = np.where(m)
print("hole bbox", xs.min(), xs.max(), ys.min(), ys.max())
v = t.copy(); v[m] = (v[m] * 0.35 + np.array([255, 0, 0]) * 0.65).astype(int)
Image.fromarray(v.astype("uint8")).resize((512, 768)).save("/tmp/claude-0/-home-user-Marketing0510/6893ab34-d546-5f8f-9637-69ed00ee7533/scratchpad/mask_vis.jpg")
