#!/usr/bin/env python3
"""Hub 9-circle bar overflow fix (2026-11-14, maker seat).

SCORECARD (fit vs scroll), settled by first-hand repro on live /hub:
  (a) FIT: 9 pills need 578px of row at 390 (370 available) / 360 (340 avail).
      Labels drive the width (CONNECTIONS ~72px). Fitting would mean jewels
      44px -> ~28px and 9px labels -> ~6px: unreadable, a redesign, and it
      would change the bar's look. REJECTED.
  (b) SCROLL + VISIBLE AFFORDANCE: the row ALREADY scrolls (overflow-x:auto,
      scrollWidth 578, programmatic scrollLeft=200 works, snap-to-whole-pills
      lands whole). What is missing is ONLY the affordance: the scrollbar is
      hidden, there is no fade, no control, nothing that says "more". PICKED.
      Minimal, bar-only: edge fades + edge chevron buttons, driven by a
      data-obb-more attribute the row's own scroll state sets. At 1440 the
      row never overflows, so nothing shows and nothing changes.

Source: the CURRENT bake template as read first-hand (sha 4a89ed86...,
4,999,666 B). Surgical, anchored edits only — notes untouched (verified
list-identical after). Output: work/index-fixed.html (NOT the template yet).
"""
import hashlib, json, re, subprocess, sys

TPL = "/home/hatch/workspace/user/files/index-2.html"
OUT = "/home/hatch/workspace/team-nitro/hub-bar-overflow-fix-20261114/work/index-fixed.html"
WD = "/home/hatch/workspace/team-nitro/hub-bar-overflow-fix-20261114/work"
TPL_SHA = "4a89ed863fcfa05c7c0f514a5fe1aa9ce942ee7d33732c8dfe3a1d7a126a576e"

html = open(TPL, "rb").read()
assert hashlib.sha256(html).hexdigest() == TPL_SHA, "template moved - STOP"
assert html.count(b"data-obb-more") == 0 and html.count(b"obb-nav") == 0, "fix already present - STOP"
html = html.decode("utf-8")

# --- 1. HTML: chevron buttons inside the nav, after the row, before </nav> ---
a1 = ('<span class="obb-lbl">10 apps</span></a>\n</div>\n</nav>')
assert html.count(a1) == 1, f"HTML anchor != 1 ({html.count(a1)}) - STOP"
html = html.replace(a1,
    '<span class="obb-lbl">10 apps</span></a>\n</div>\n'
    '<button class="obb-nav obb-nav-l" type="button" aria-label="Show earlier apps">\u2039</button>\n'
    '<button class="obb-nav obb-nav-r" type="button" aria-label="Show more apps">\u203a</button>\n</nav>', 1)

# --- 2. CSS: fades + chevrons, appended after the phone media line ---
a2 = ('@media (max-width:640px){.obb-bar{gap:6px;padding:8px 10px calc(8px + env(safe-area-inset-bottom,0px))}'
      '.obb-row{gap:6px;scroll-padding:0 10px}.obb-pill{padding:2px 3px 0}'
      '.obb-jewel{width:44px;height:44px;flex:0 0 44px;font-size:16px}.obb-lbl{font-size:9px}}')
assert html.count(a2) == 1, f"CSS anchor != 1 ({html.count(a2)}) - STOP"
css_add = (
    '\n/* FIX 2026-11-14 (bar overflow): the row already scrolls (overflow-x:auto,\n'
    '   snap-to-whole-pills) but at phone widths nothing says there is more — the\n'
    '   scrollbar is hidden and the last pill is cut mid-label with no affordance.\n'
    '   Edge fades + edge chevrons, driven by data-obb-more on the bar (JS below):\n'
    '   "left", "right", "left right", or absent. At 1440 the row never overflows,\n'
    '   so nothing shows and nothing changes. */\n'
    '.obb-bar::before,.obb-bar::after{content:"";position:absolute;top:0;bottom:0;width:34px;pointer-events:none;opacity:0;transition:opacity .25s ease;z-index:3}\n'
    '.obb-bar::before{left:0;background:linear-gradient(90deg,rgba(3,3,5,.97),rgba(3,3,5,0))}\n'
    '.obb-bar::after{right:0;background:linear-gradient(270deg,rgba(3,3,5,.97),rgba(3,3,5,0))}\n'
    '.obb-bar[data-obb-more~="left"]::before{opacity:1}\n'
    '.obb-bar[data-obb-more~="right"]::after{opacity:1}\n'
    '.obb-nav{display:none;position:absolute;top:50%;transform:translateY(-50%);width:30px;height:30px;border-radius:50%;place-items:center;font-size:19px;line-height:1;color:#fff;background:radial-gradient(circle at 35% 30%,#2a2a32,#0a0a0e 70%);border:1px solid rgba(255,255,255,.45);box-shadow:0 0 14px rgba(255,255,255,.25),0 4px 10px rgba(0,0,0,.5);cursor:pointer;z-index:4;padding:0}\n'
    '.obb-nav-l{left:3px}\n'
    '.obb-nav-r{right:3px}\n'
    '.obb-bar[data-obb-more~="left"] .obb-nav-l{display:grid}\n'
    '.obb-bar[data-obb-more~="right"] .obb-nav-r{display:grid}\n'
    '.obb-nav:active{transform:translateY(-50%) scale(.94)}')
html = html.replace(a2, a2 + css_add, 1)

# --- 3. JS: affordance driver IIFE, after the lane script, before </script> ---
a3 = "  window.__obbLayout=obbLayout;\n})();\n</script>\n<!-- /ONE-BOTTOM-BAR -->"
assert html.count(a3) == 1, f"JS anchor != 1 ({html.count(a3)}) - STOP"
js_add = (
    '/* FIX 2026-11-14 (bar overflow affordance): the row scrolls, but nothing\n'
    '   shows it. Read the row\'s own scroll state and say so on the bar:\n'
    '   data-obb-more = "left" / "right" / "left right" / "" — the CSS above\n'
    '   shows the edge fades + chevrons only for the directions that exist.\n'
    '   A chevron tap scrolls the first not-fully-visible pill into view\n'
    '   (scrollIntoView, snap-aware — smooth, lands whole). Plain scrollBy\n'
    '   does NOT travel here: scroll-snap-stop:always stops it at the very\n'
    '   first snap point (46px), so scrollIntoView on the pill is the way.\n'
    '   No overflow (1440) -> attribute empty -> nothing shows, nothing changes. */\n'
    '(function(){\n'
    '  var bar=document.getElementById(\'obb-bar\'); if(!bar) return;\n'
    '  var row=bar.querySelector(\'.obb-row\'); if(!row) return;\n'
    '  function obbMore(){\n'
    '    var max=row.scrollWidth-row.clientWidth;\n'
    '    var sl=row.scrollLeft, m=\'\';\n'
    '    if(max>4){ if(sl>4) m+=\'left \'; if(sl<max-4) m+=\'right\'; }\n'
    '    bar.setAttribute(\'data-obb-more\', m.replace(/\\s+$/,\'\'));\n'
    '  }\n'
    '  row.addEventListener(\'scroll\', obbMore, {passive:true});\n'
    '  window.addEventListener(\'resize\', obbMore);\n'
    '  if(document.readyState===\'loading\'){ document.addEventListener(\'DOMContentLoaded\', obbMore); }\n'
    '  else { obbMore(); }\n'
    '  setTimeout(obbMore, 500); setTimeout(obbMore, 1500);\n'
    '  function obbStep(dir){\n'
    '    var rr=row.getBoundingClientRect(), pills=row.querySelectorAll(\'.obb-pill\'), t=null;\n'
    '    var i;\n'
    '    if(dir>0){ for(i=0;i<pills.length;i++){ if(pills[i].getBoundingClientRect().right>rr.right+1){ t=pills[i]; break; } } }\n'
    '    else { for(i=pills.length-1;i>=0;i--){ if(pills[i].getBoundingClientRect().left<rr.left-1){ t=pills[i]; break; } } }\n'
    '    if(t){ t.scrollIntoView({inline:\'start\', behavior:\'smooth\'}); }\n'
    '  }\n'
    '  var navs=bar.querySelectorAll(\'.obb-nav\');\n'
    '  for(var i=0;i<navs.length;i++){\n'
    '    navs[i].addEventListener(\'click\', function(){\n'
    '      obbStep(this.className.indexOf(\'obb-nav-r\')>=0 ? 1 : -1);\n'
    '    });\n'
    '  }\n'
    '})();\n')
html = html.replace(a3, "  window.__obbLayout=obbLayout;\n})();\n" + js_add + "</script>\n<!-- /ONE-BOTTOM-BAR -->", 1)

out = html.encode("utf-8")
open(OUT, "wb").write(out)
print(f"fixed shell: {len(out)} B sha256 {hashlib.sha256(out).hexdigest()}")

# --- verify: markers, notes list-identical, node --check, CSS brace gate ---
def count(b, m): return b.count(m)
for m, want in [(b"findNoteBySlug", 4), (b"SLUG_MAP", 2), (b"smart-notes/:slug", 7),
                (b'src="/js/naya-search.js"', 1), (b'src="js/naya-search.js"', 0),
                (b"data-obb-more", 7), (b"obb-nav", 12)]:
    got = count(out, m)
    print(f"  {m.decode():28s} {got} (want {want})")
    assert got == want, f"{m}: {got} != {want} - STOP"
for sn in (b"SN-2782", b"SN-2696"):
    assert sn in out, f"{sn} missing - STOP"
    print(f"  {sn.decode():28s} present ({count(out, sn)}x)")

live_notes = json.load(open(WD + "/live-notes-extract.json", encoding="utf-8"))
m = re.search(rb"const NOTES = (\[.*?\])\.concat\(NOTES_BASE\);", out, flags=re.DOTALL)
assert m, "NOTES anchor lost - STOP"
assert json.loads(m.group(1)) == live_notes, "notes NOT list-identical - STOP"
print("  notes parsed back: 200, list-identical to the extract")

# node --check on every inline <script> block in the fixed shell (notes block + obb block)
blocks = re.findall(rb"<script>(.*?)</script>", out, flags=re.DOTALL)
print(f"  inline script blocks: {len(blocks)}")
for i, blk in enumerate(blocks):
    p = f"/tmp/hub_fix_script_{i}.js"
    open(p, "wb").write(blk)
    chk = subprocess.run(["node", "--check", p], capture_output=True, text=True, timeout=30)
    assert chk.returncode == 0, f"node --check block {i} FAILED: {chk.stderr[:300]}"
print("  node --check on all inline script blocks: PASS")

sys.path.insert(0, "/home/hatch/workspace/factory-pipeline")
import deploy as dep
assert dep.css_brace_check(out.decode("utf-8"), OUT), "CSS brace check FAILED - STOP"
print("  CSS brace check: PASS")

# diff scope: changed/added lines must all sit in the obb block region
old_lines = open(TPL, encoding="utf-8").read().split("\n")
new_lines = html.split("\n")
import difflib
changed = [i for i, (a, b) in enumerate(zip(old_lines, new_lines)) if a != b]
added = len(new_lines) - len(old_lines)
print(f"  lines: {len(old_lines)} -> {len(new_lines)} (+{added}); first changed line {changed[0]+1 if changed else '-'}")
assert all(9720 <= i + 1 <= 9860 for i in changed), f"change outside obb region: {changed[:5]} - STOP"
print("  diff scope: all edits inside the one-bottom-bar block (lines 9721-9830) - PASS")
print(f"OK wrote {OUT}")
