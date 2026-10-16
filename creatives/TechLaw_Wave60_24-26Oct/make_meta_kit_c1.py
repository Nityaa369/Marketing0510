# Builds the C1 Meta kit: 9:16 (1080x1920) and 4:5 (1080x1350) versions of each ad, the upload
# sheet (CSV), and META_KIT.md. Images: FSRCNN x4 upscale (OpenCV, local, free), no content change.
# 4:5 keeps the whole ad (no crop) on a blurred backdrop of itself. Run: python3 make_meta_kit_c1.py
import os, csv, cv2, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, "graphic", "c1_final_v4"); OUT = os.path.join(HERE, "meta_kit_c1")
sr = cv2.dnn_superres.DnnSuperResImpl_create(); sr.readModel("/tmp/claude-0/sr/FSRCNN_x4.pb"); sr.setModel("fsrcnn", 4)
os.makedirs(os.path.join(OUT, "9x16"), exist_ok=True); os.makedirs(os.path.join(OUT, "4x5"), exist_ok=True)
for n in range(1, 11):
    nn = "%02d" % n; im = cv2.imread(os.path.join(SRC, "TL_C1_%s.jpg" % nn))
    up = sr.upsample(im); h = round(up.shape[0] * 1080 / up.shape[1])
    v = cv2.resize(up, (1080, h), interpolation=cv2.INTER_AREA)
    top = max(0, (h - 1920) // 2); v = v[top:top + 1920] if h >= 1920 else cv2.copyMakeBorder(v, 0, 1920 - h, 0, 0, cv2.BORDER_REPLICATE)
    cv2.imwrite(os.path.join(OUT, "9x16", "TL_C1_%s_9x16.jpg" % nn), v, [cv2.IMWRITE_JPEG_QUALITY, 92])
    fw = round(1080 * 1350 / 1920); fg = cv2.resize(v, (fw, 1350), interpolation=cv2.INTER_AREA)
    bg = cv2.GaussianBlur(cv2.resize(v[300:1620], (1080, 1350)), (0, 0), 28); bg = (bg * 0.82).astype(np.uint8)
    x = (1080 - fw) // 2; bg[:, x:x + fw] = fg
    cv2.imwrite(os.path.join(OUT, "4x5", "TL_C1_%s_4x5.jpg" % nn), bg, [cv2.IMWRITE_JPEG_QUALITY, 92])
    print(nn, "ok", flush=True)
