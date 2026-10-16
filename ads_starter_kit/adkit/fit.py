#!/usr/bin/env python3
"""Measure a rendered ad face and fail on the defects no other gate can see.

Why this exists. From .claude/skills/generate-ad-kit/SKILL.md, 26 Aug 2026:

    "On a card-based chassis, text overlap is invisible to every gate in
    check_all. A face where three table rows printed through each other passed
    simplicity (both halves), hook_rules, ad_lint C8 and creative_judge -- 3
    accept, 0 reject. Nothing in the suite measures whether two elements occupy
    the same pixels."

That kit averaged 5 render cycles on 3 ads, and the wave-1 measurement was 14.1
rebuild cycles per creative against 6.4 when hooks were settled as text first.
The residual cycles are this defect class, and the standing instruction for it
was "count characters against the measured chars-per-line before rendering",
which is a human eyeballing a budget. This measures it instead.

Six things are checked, all against the real rendered box model rather than
against source text length:

  F1  CLIPPED   an element extends past the .canvas box. The canvas sets
                overflow:hidden, so this is silently cropped in the PNG.
  F2  OVERLAP   two elements that are not ancestor/descendant occupy the same
                pixels. This is the documented invisible failure.
  F3  FLOOR     .callout or .head below 64px computed. ad_lint C8 asserts the
                same floors, but with re.search for the FIRST
                `.callout{...font-size:Npx}` in the source. A later override wins
                in the browser and is invisible to the linter -- which is exactly
                what IndependentDirector_Wave1's `tight=True` block does: it sets
                .callout to 58px and .head to 52px after the 66px/64px base
                rules, so those shipped faces are C8 violations that read as
                clean. This reads the COMPUTED value, so an override, an inline
                style or a scale factor cannot slip past it.
  F4  MISSING   no .callout or no .head on the face at all, which is the
                25 Aug 2026 silent pass -- C8 matched nothing and read as clean.
  F7  SPILL     text wider than its own box (scrollWidth > clientWidth), e.g. a
                nowrap call-out running out of its coloured band while still
                inside the canvas. F1 cannot see this. Added 17 Sep 2026.
  F8  CUT       an element clipped by the nearest ANCESTOR carrying
                overflow:hidden rather than by the canvas. Added 21 Sep 2026:
                the notify layout's `.note` is overflow:hidden, so on 3 of 19
                faces a tall content block let the card eat the CTA band's lower
                padding -- 78px tall instead of 108px, label almost on the edge.
                Inside the canvas throughout, so F1 saw nothing and the
                auto-fitter had no reason to shrink. Ramanuj caught it by eye.
NOT CHECKED, deliberately: text sitting close to the bottom edge. Considered 21 Sep 2026
after a face rendered 13px from the bottom against ~37px of designed padding. Measured on
192 Ramanuj-approved faces (GOLDEN.md list plus GOLDEN/*.png), per 1350px face: median 47px,
5th percentile 14px, and 43 of 192 (22%) under 20px. A rule firing there would condemn about
one approved face in five, so a tight bottom is a taste call, not a defect. Measure again
before adding it.
Measurement runs in the same Chrome that renders the PNG, so what is measured is
what ships. No new dependency: a probe script is appended to a copy of the page,
Chrome is run with --dump-dom, and the probe hands back base64 JSON.

    python -m adkit.fit <kit-folder>        measure every kit html/*.html
    python -m adkit.fit path/to/face.html   measure one file
"""
import base64
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

CALLOUT_FLOOR = 64.0
HEAD_FLOOR = 64.0     # ad_lint C8: .head hard-fails under 64px, target 80px
OVERLAP_TOLERANCE = 4.0     # px on each axis; kills sub-pixel and border touching
CLIP_TOLERANCE = 1.0

_CHROME_CANDIDATES = [
    os.environ.get("ADKIT_CHROME"),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
]


def find_chrome():
    for c in _CHROME_CANDIDATES:
        if c and pathlib.Path(c).exists():
            return c
    for n in ("chrome", "google-chrome", "chromium", "chromium-browser", "msedge"):
        p = shutil.which(n)
        if p:
            return p
    raise RuntimeError("no Chrome found. Set ADKIT_CHROME to the browser executable.")


PROBE = """
<script>
(function(){
function __run(){
  function box(e){var r=e.getBoundingClientRect();
    return {x:r.left,y:r.top,w:r.width,h:r.height,r:r.right,b:r.bottom};}
  var c=document.querySelector('.canvas')||document.body;
  var cb=box(c);
  var all=[].slice.call(c.querySelectorAll('*'));
  var items=[];
  all.forEach(function(e,i){
    if(e.tagName==='SCRIPT'||e.tagName==='STYLE')return;
    var b=box(e);
    var cs0=getComputedStyle(e);
    if(cs0.display==='none'||cs0.visibility==='hidden')return;
    if(b.w<=0||b.h<=0)return;
    var txt=(e.textContent||'').replace(/\\s+/g,' ').trim();
    var kidsWithText=[].slice.call(e.children).some(function(k){
      return (k.textContent||'').trim().length>0;});
    var isLeaf=(txt.length>0&&!kidsWithText)||e.tagName==='IMG';
    var cs=getComputedStyle(e);
    var cls=(e.className&&e.className.baseVal!==undefined)
      ?e.className.baseVal:String(e.className||'');
    items.push({tag:e.tagName,cls:cls,leaf:isLeaf,
      fs:parseFloat(cs.fontSize)||0,text:txt.slice(0,60),box:b,node:e});
  });
  var TOL=4.0, CTOL=1.0;
  var clipped=[];
  items.forEach(function(it){
    if(!it.leaf)return;
    var b=it.box;
    if(b.b>cb.b+CTOL||b.y<cb.y-CTOL||b.r>cb.r+CTOL||b.x<cb.x-CTOL)
      clipped.push({cls:it.cls,tag:it.tag,text:it.text,
        over_bottom:Math.round(b.b-cb.b),over_right:Math.round(b.r-cb.r)});
  });
  // F7. Text wider than its OWN box. F1 only compares leaves with the canvas, and
  // an element holding styled children (a <span class='keep'>) is not a leaf, so
  // a nowrap call-out whose words ran past the right edge of its coloured band,
  // while staying inside the canvas, passed clean (17 Sep 2026, search layout).
  var spill=[];
  items.forEach(function(it){
    var e=it.node, cs=getComputedStyle(e);
    if(!it.text||e.clientWidth<=0)return;
    if(cs.display.indexOf('inline')===0&&cs.display!=='inline-block')return;
    if(cs.overflowX!=='visible')return;
    var over=e.scrollWidth-e.clientWidth;
    if(over>CTOL+1)spill.push({cls:it.cls,tag:it.tag,text:it.text,over:Math.round(over)});
  });
  var leaves=items.filter(function(it){return it.leaf;});
  var overlaps=[];
  for(var a=0;a<leaves.length;a++){
    for(var d=a+1;d<leaves.length;d++){
      var A=leaves[a],B=leaves[d];
      if(A.node.contains(B.node)||B.node.contains(A.node))continue;
      // An element inside a declared overlay sits ON the thing beneath it by
      // design. Added 23 Sep 2026: the three GOLDEN arbitration faces
      // (mh01_corridor, mh02_office, mh03_chamber) are all a photograph with a
      // speech bubble over it, and F2 called that an overlap defect. Only a
      // class actually named `overlay` or `bubble` is exempt, so an accidental
      // collision between two body elements still fires.
      if(A.node.closest('.bubble,.overlay')||B.node.closest('.bubble,.overlay'))continue;
      var ox=Math.min(A.box.r,B.box.r)-Math.max(A.box.x,B.box.x);
      var oy=Math.min(A.box.b,B.box.b)-Math.max(A.box.y,B.box.y);
      if(ox>TOL&&oy>TOL)
        overlaps.push({a:(A.cls||A.tag),b:(B.cls||B.tag),
          ax:A.text,bx:B.text,px:Math.round(ox)+'x'+Math.round(oy)});
    }
  }
  function firstFont(sel){var e=c.querySelector(sel);
    return e?parseFloat(getComputedStyle(e).fontSize):null;}
  // F8. Clipped by an ANCESTOR, not by the canvas. F1 compares each leaf with
  // the canvas box, so an element cut off by a nearer ancestor that carries
  // overflow:hidden sits comfortably inside the canvas and passes clean. Found
  // 21 Sep 2026 on the notify layout: `.note` is overflow:hidden inside a fixed
  // canvas, so on three of nineteen faces a tall content block pushed the CTA
  // band down and the card ate its lower padding. The band rendered 78px instead
  // of 108px and the label sat almost on the bottom edge. Ramanuj saw it on the
  // faces; fit.check reported clean at scale 1.00, so the auto-fitter had no
  // reason to shrink anything. Same family as F7, one level up.
  var cut=[];
  items.forEach(function(it){
    var e=it.node;
    for(var p=e.parentElement;p&&p!==c.parentElement;p=p.parentElement){
      var ps=getComputedStyle(p);
      if(ps.overflow==='visible'&&ps.overflowY==='visible')continue;
      var pb=box(p);
      var b=it.box;
      // the clip edge is the ancestor's padding box; border sits outside it
      var bw=parseFloat(ps.borderBottomWidth)||0;
      var over=b.b-(pb.b-bw);
      if(over>CTOL+1){
        cut.push({cls:it.cls,tag:it.tag,text:it.text,
                  anc:(p.className&&p.className.baseVal!==undefined)
                      ?p.className.baseVal:String(p.className||p.tagName),
                  over:Math.round(over)});
      }
      break;   // nearest clipping ancestor only
    }
  });
  // F6. The probe and the screenshot are two SEPARATE Chrome runs. If an image
  // has not decoded when the probe measures, its box is zero and the page looks
  // like it fits, while the screenshot run loads it and pushes the footer off
  // the canvas. That is a gate reporting clean on a face that ships cut, which
  // is the one failure mode check_all.py exists to prevent.
  var imgs=[].slice.call(c.querySelectorAll('img')).map(function(im){
    return {complete:!!im.complete,nh:im.naturalHeight||0,
            h:Math.round(box(im).h)};});
  var out={canvas:{w:Math.round(cb.w),h:Math.round(cb.h)},
    scroll:{sh:c.scrollHeight,ch:c.clientHeight},
    callout_fs:firstFont('.callout'),head_fs:firstFont('.head'),
    clipped:clipped,spill:spill.slice(0,20),overlaps:overlaps.slice(0,20),
    cut:cut.slice(0,20),
    imgs:imgs,leaves:leaves.length};
  var d=document.createElement('div');
  d.id='__adkit_fit';
  d.textContent=btoa(unescape(encodeURIComponent(JSON.stringify(out))));
  document.body.appendChild(d);
}
// Images decode asynchronously. Measuring before they land is what made every
// photo-led face measure as fitting no matter how tall its hero was.
if(document.readyState==='complete'){__run();}
else{window.addEventListener('load',__run);}
})();
</script>
"""


def measure(html_path, chrome=None):
    """Render `html_path` headless and return the probe's report dict.

    Raises RuntimeError if the probe did not run -- it never returns a
    clean-looking empty result, because "the gate did not run" reading as a pass
    is the exact failure check_all.py exists to stop.
    """
    html_path = pathlib.Path(html_path).resolve()
    src = html_path.read_text(encoding="utf-8", errors="replace")
    if "</body>" in src:
        probed = src.replace("</body>", PROBE + "</body>", 1)
    else:
        probed = src + PROBE
    tmp = html_path.with_name("__fit_" + html_path.name)
    tmp.write_text(probed, encoding="utf-8")
    try:
        p = subprocess.run(
            [chrome or find_chrome(), "--headless=new", "--disable-gpu",
             "--hide-scrollbars", "--virtual-time-budget=3000",
             "--force-device-scale-factor=1", "--dump-dom", tmp.resolve().as_uri()],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=120)
        dom = p.stdout or ""
        m = re.search(r'id="__adkit_fit"[^>]*>([A-Za-z0-9+/=\s]+)<', dom)
        if not m:
            raise RuntimeError(
                "fit probe did not run on %s (Chrome returned %d bytes of DOM). "
                "That is an ERROR, not a pass." % (html_path.name, len(dom)))
        return json.loads(base64.b64decode(m.group(1).strip()).decode("utf-8"))
    finally:
        try:
            tmp.unlink()
        except OSError:
            pass


def _safe(s):
    """ASCII-safe. A Windows console is cp1252, and check_all.py's own docstring
    records the judge crashing with a UnicodeEncodeError before printing its
    verdict, "which looks exactly like a clean run if you are not reading
    closely". A findings printer must never be able to do that."""
    return str(s).encode("ascii", "replace").decode("ascii")


def findings(report):
    """Turn a probe report into a list of finding strings. Empty means clean."""
    out = []
    if report.get("callout_fs") is None:
        out.append("F4 MISSING  no .callout on the face -- ad_lint C8 cannot see it, "
                   "so its 64px floor is not being applied")
    elif report["callout_fs"] < CALLOUT_FLOOR:
        out.append("F3 FLOOR    .callout computed %.0fpx, floor %.0fpx"
                   % (report["callout_fs"], CALLOUT_FLOOR))
    if report.get("head_fs") is None:
        out.append("F4 MISSING  no .head on the face -- C8 cannot see it")
    elif report["head_fs"] < HEAD_FLOOR:
        out.append("F3 FLOOR    .head computed %.0fpx, floor %.0fpx"
                   % (report["head_fs"], HEAD_FLOOR))
    for c in report.get("clipped", []):
        over = max(c.get("over_bottom", 0), c.get("over_right", 0))
        out.append("F1 CLIPPED  .%s runs %dpx past the canvas: %r"
                   % (_safe(c.get("cls") or c.get("tag")), over,
                      _safe(c.get("text", "")[:48])))
    for c in report.get("cut", []):
        out.append("F8 CUT      .%s is clipped %dpx by .%s (overflow:hidden), "
                   "not by the canvas: %r"
                   % (_safe(c.get("cls") or c.get("tag")), c.get("over", 0),
                      _safe(c.get("anc", "")), _safe(c.get("text", "")[:48])))
    for c in report.get("spill", []):
        out.append("F7 SPILL    .%s text runs %dpx past its own box: %r"
                   % (_safe(c.get("cls") or c.get("tag")), c.get("over", 0),
                      _safe(c.get("text", "")[:48])))
    for i, im in enumerate(report.get("imgs", [])):
        if not im.get("complete") or not im.get("nh"):
            out.append("F6 UNMEASURED  image %d had not loaded when the page was "
                       "measured, so its height counted as zero and this run "
                       "proves nothing about whether the face fits" % (i + 1))
    for o in report.get("overlaps", []):
        out.append("F2 OVERLAP  .%s and .%s share %s px: %r / %r"
                   % (_safe(o["a"]), _safe(o["b"]), o["px"],
                      _safe(o["ax"][:32]), _safe(o["bx"][:32])))
    return out


def check(html_path, chrome=None):
    return findings(measure(html_path, chrome))


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    if len(argv) < 2:
        print(__doc__)
        return 2
    target = pathlib.Path(argv[1])
    if target.is_dir():
        files = sorted((target / "html").glob("*.html")) or sorted(target.glob("*.html"))
    else:
        files = [target]
    files = [f for f in files if not f.name.startswith("__fit_")]
    if not files:
        print("ERROR: no html to measure under %s. A gate that saw zero files is "
              "not a pass." % target)
        return 2
    chrome = find_chrome()
    bad = 0
    for f in files:
        try:
            fs = check(f, chrome)
        except Exception as e:                    # noqa: BLE001 - reported, never hidden
            print("  %-42s ERROR   %s" % (f.name, e))
            bad += 1
            continue
        if fs:
            bad += 1
            print("  %-42s FINDINGS" % f.name)
            for line in fs:
                print("      " + line)
        else:
            print("  %-42s clean" % f.name)
    print("\n  %d file(s) measured, %d with findings." % (len(files), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
