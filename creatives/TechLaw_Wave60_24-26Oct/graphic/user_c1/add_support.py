# Adds the supporting-copy banner just above each ad's Join button, and nothing else.
# Supporting copy is the user's 16 Oct script (09: "at your own pace" changed to "live, from home",
# because the camp is live only). Run: python3 add_support.py  -> final/TL_C1_<id>.jpg
import os, glob, subprocess, html, cv2, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
COPY = {
 "01": ("#13756B", "Use your LLB to explore tech law, employment contracts and workplace compliance."),
 "02": ("#1D6FE0", "Use your degree to explore fintech regulations, financial contracts and technology law."),
 "03": ("#5B2BD6", "Use your LLB to build practical skills in software agreements, privacy policies and tech law documents."),
 "04": ("#E8590C", "Use your degree to explore commercial contracts, software agreements and compliance."),
 "05": ("#C8102E", "Use your degree to rebuild practical legal skills in contracts, privacy and technology law."),
 "06": ("#1D5FD0", "Explore practical tech law skills that can open up new directions for your legal career."),
 "07": ("#1D5FD0", "Use your Indian law degree to explore tech law skills and the opportunities open to you."),
 "08": ("#D97706", "Use your degree to learn practical contract drafting, privacy and technology law skills."),
 "09": ("#DB2777", "Refresh your legal skills and explore contracts, privacy and tech law, live from home."),
 "10": ("#9A6A1E", "Use your degree to explore practical tech law work, from drafting software contracts to reviewing privacy policies."),
}
def button_top(img):
    h, w = img.shape[:2]; b, g, r = [img[:, w // 4: 3 * w // 4, i].astype(int) for i in range(3)]
    red = ((r > 190) & (g < 90) & (b < 90)).mean(axis=1)
    rows = np.where(red[h // 2:] > 0.5)[0] + h // 2; return int(rows.min()) if len(rows) else int(h * .86)
hs = glob.glob("/opt/pw-browsers/chromium_headless_shell-*/*/headless_shell")[0]
os.makedirs(os.path.join(HERE, "final"), exist_ok=True)
for tid, (ac, txt) in COPY.items():
    src = os.path.join(HERE, "tile_%s.png" % tid)
    if not os.path.exists(src): continue
    img = cv2.imread(src); H = img.shape[0]; bt = button_top(img)
    page = ('<!doctype html><html><head><meta charset="utf-8"><style>'
            "*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;height:%dpx;overflow:hidden;position:relative;background:#fff}"
            "img{position:absolute;left:-7px;top:-4px;width:1094px}"
            ".s{position:absolute;left:64px;right:64px;bottom:%dpx;background:rgba(255,255,255,.94);border-left:10px solid %s;border-radius:22px;"
            "padding:20px 28px;box-shadow:0 12px 28px rgba(0,0,0,.22);font-family:Inter,sans-serif}"
            ".t{font-weight:700;font-size:34px;line-height:1.28;color:#151515}.f{margin-top:8px;font-weight:800;font-size:22px;letter-spacing:.08em;color:%s}"
            "</style></head><body><img src='tile_%s.png'><div class='s'><div class='t'>%s</div><div class='f'>&#8377;10 INCL. GST &nbsp;·&nbsp; REFUNDABLE &nbsp;·&nbsp; 3 LIVE EVENINGS</div></div></body></html>"
            % (H, H - bt + 22, ac, ac, tid, html.escape(txt)))
    hp = os.path.join(HERE, "p_%s.html" % tid); open(hp, "w").write(page)
    out = os.path.join(HERE, "final", "TL_C1_%s.png" % tid)
    subprocess.run([hs, "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--window-size=1080,%d" % H, "--virtual-time-budget=2000",
                    "--screenshot=" + out, "file://" + hp], check=True, capture_output=True)
    cv2.imwrite(out.replace(".png", ".jpg"), cv2.imread(out), [cv2.IMWRITE_JPEG_QUALITY, 92]); os.remove(out); os.remove(hp)
    print(tid, "button top", bt, "of", H)
