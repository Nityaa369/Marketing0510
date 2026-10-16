# Cuts the user's 10-ad board (5x2) into tiles, removes the board's tile number, upscales x4 with
# EDSR (OpenCV dnn_superres, free, local) and resizes to 1080 wide. Run: python3 slice_upscale.py board.webp [ids]
import sys, cv2, numpy as np, time
board = cv2.imread(sys.argv[1]); only = set(sys.argv[2:])
cols = [(0, 314), (322, 615), (623, 919), (928, 1226), (1235, 1535)]; rows = [(0, 511), (520, 997)]
sr = cv2.dnn_superres.DnnSuperResImpl_create(); sr.readModel("/tmp/claude-0/sr/EDSR_x4.pb"); sr.setModel("edsr", 4)
n = 0
for r, (y0, y1) in enumerate(rows):
    for c, (x0, x1) in enumerate(cols):
        n += 1; tid = "%02d" % n
        if only and tid not in only: continue
        t = board[y0:y1 + 1, x0:x1 + 1].copy()
        mask = np.zeros(t.shape[:2], np.uint8); mask[8:40, 6:48] = 255  # the "01".."10" board label
        t = cv2.inpaint(t, mask, 5, cv2.INPAINT_TELEA)
        s = time.time(); up = sr.upsample(t)
        out = cv2.resize(up, (1080, round(up.shape[0] * 1080 / up.shape[1])), interpolation=cv2.INTER_AREA)
        cv2.imwrite("tile_%s.png" % tid, out); print(tid, t.shape, "->", out.shape, "%.1fs" % (time.time() - s), flush=True)
