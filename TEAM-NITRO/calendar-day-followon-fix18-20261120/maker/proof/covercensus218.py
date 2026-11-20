#!/usr/bin/env python3
"""CAL-FIX18 item 3: 1920 cover census with animations FROZEN, so the only
difference between cover-on and cover-off shots is the cover itself.
Also samples pixel colors in the empty deck region on slide 1.
Usage: covercensus218.py [firefox|chromium] [fonts|nofont] [390|1920]
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

FREEZE = """() => {
  document.getAnimations().forEach(a => { try { a.pause(); } catch(e){} });
  const st = document.createElement('style');
  st.textContent = '*{animation-play-state:paused!important;transition:none!important}';
  document.head.appendChild(st);
  return document.getAnimations().length;
}"""

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
    print(f"=== frozen cover census base {TAG} day20 ===")
    clip = page.evaluate("() => { const b=document.querySelector('#dayScroll').getBoundingClientRect(); return {x:b.x,y:b.y,width:b.width,height:b.height}; }")
    for i in range(9):
        page.evaluate("(ii) => { const dots=[...document.querySelectorAll('#dayScroll .sb-dots button')]; if(dots[ii]) dots[ii].click(); }", i)
        page.wait_for_timeout(2500)
        n = page.evaluate(FREEZE)
        page.evaluate("() => { document.querySelector('#dayCoverBg').style.display=''; }")
        page.wait_for_timeout(300)
        a = Image.open(io.BytesIO(page.screenshot(clip=clip))).convert("RGB")
        page.evaluate("() => { document.querySelector('#dayCoverBg').style.display='none'; }")
        page.wait_for_timeout(300)
        bimg = Image.open(io.BytesIO(page.screenshot(clip=clip))).convert("RGB")
        page.evaluate("() => { document.querySelector('#dayCoverBg').style.display=''; }")
        c_tot, c_in = diffpx(a, bimg)
        name = page.evaluate("() => { const on=[...document.querySelectorAll('#dayScroll .smart-block')].find(e=>e.classList.contains('on')); return on ? (on.id || on.className.split(' ')[0]) : '?'; }")
        verdict = "COVER-SHOWN" if c_in > 500 else "rim-only"
        print(f"slide {i} {name}: frozen-anims={n} cover tot={c_tot} in={c_in} | {verdict}")
        if i == 1:
            arr = np.array(a)
            # sample the empty region above the notifications panel (clip coords)
            pts = [(100, 40), (850, 40), (1600, 40), (100, 100), (850, 100), (1600, 100), (850, 150)]
            print("  slide1 empty-region ON colors:", [tuple(arr[y, x].tolist()) for x, y in pts])
            arr2 = np.array(bimg)
            print("  slide1 empty-region OFF colors:", [tuple(arr2[y, x].tolist()) for x, y in pts])
    print("PAGE ERRORS:", errs if errs else "NONE")
    browser.close()
