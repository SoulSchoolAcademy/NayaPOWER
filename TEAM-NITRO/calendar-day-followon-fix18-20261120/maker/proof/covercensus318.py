#!/usr/bin/env python3
"""CAL-FIX18 item 3: per-slide cover census, CORRECTED freeze.
Per slide: navigate, wait 2.5s (entrance done), pause all currently-running
animations via a.pause() only (NO global style tag -- that froze future
slide entrances at opacity 0 and faked a fullscreen cover). Then shot A
(cover on), toggle cover off, shot B. Any remaining interior diff is the
cover itself. Usage: covercensus318.py [firefox|chromium] [fonts|nofont] [390|1920]
"""
import io, os, sys
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
WHICH = sys.argv[1] if len(sys.argv) > 1 else "firefox"
FONT = sys.argv[2] if len(sys.argv) > 2 else "nofont"
W = int(sys.argv[3]) if len(sys.argv) > 3 else 1920
H = 844 if W == 390 else 999
TAG = f"{WHICH}-{FONT}-{W}"
HTML = open(os.path.join(HERE, "base-fix17.html"), encoding="utf-8").read()

def diffpx(a, b):
    d = np.array(ImageChops.difference(a, b).convert("L"))
    mask = d > 12
    return int(mask.sum()), int(mask[6:-6, 6:-6].sum())

PAUSE = """() => { let n=0;
  document.getAnimations().forEach(a => { try { if (a.playState === 'running') { a.pause(); n++; } } catch(e){} });
  return n; }"""

with sync_playwright() as p:
    errs = []
    if WHICH == "firefox":
        browser = p.firefox.launch()
        page = browser.new_page(viewport={"width": W, "height": H})
    else:
        browser = p.chromium.launch(args=["--no-sandbox"], proxy={"server": "http://127.0.0.1:18080"})
        ctx = browser.new_context(viewport={"width": W, "height": H}, ignore_https_errors=True)
        page = ctx.new_page()
    page.on("pageerror", lambda e: errs.append(str(e)))
    if FONT == "nofont":
        page.route("**/*fonts.g*/*", lambda route: route.abort())
        page.route("**/*gstatic.com/*", lambda route: route.abort())
    page.set_content(HTML, wait_until="load", timeout=60000)
    page.wait_for_timeout(3000)
    page.evaluate("() => { const b=document.getElementById('backToMonth'); if(b) b.click(); }")
    page.wait_for_timeout(600)
    page.evaluate("() => { const c=[...document.querySelectorAll('.cell[data-d]')].find(x=>+x.dataset.d===20); if(c) c.click(); }")
    page.wait_for_timeout(2000)
    clip = page.evaluate("() => { const b=document.querySelector('#dayScroll').getBoundingClientRect(); return {x:b.x,y:b.y,width:b.width,height:b.height}; }")
    print(f"=== corrected frozen cover census base {TAG} day20 ===")
    for i in range(9):
        page.evaluate("(ii) => { const dots=[...document.querySelectorAll('#dayScroll .sb-dots button')]; if(dots[ii]) dots[ii].click(); }", i)
        page.wait_for_timeout(2500)
        page.evaluate("() => { document.querySelector('#dayCoverBg').style.display=''; }")
        n = page.evaluate(PAUSE)
        page.wait_for_timeout(200)
        a = Image.open(io.BytesIO(page.screenshot(clip=clip))).convert("RGB")
        page.evaluate("() => { document.querySelector('#dayCoverBg').style.display='none'; }")
        page.wait_for_timeout(300)
        bimg = Image.open(io.BytesIO(page.screenshot(clip=clip))).convert("RGB")
        page.evaluate("() => { document.querySelector('#dayCoverBg').style.display=''; }")
        c_tot, c_in = diffpx(a, bimg)
        name = page.evaluate("() => { const on=[...document.querySelectorAll('#dayScroll .smart-block')].find(e=>e.classList.contains('on')); return on ? (on.id || on.className.split(' ')[0]) : '?'; }")
        verdict = "COVER-SHOWN" if c_in > 500 else "rim-only"
        print(f"slide {i} {name}: paused={n} cover tot={c_tot} in={c_in} | {verdict}")
    print("PAGE ERRORS:", errs if errs else "NONE")
    browser.close()
