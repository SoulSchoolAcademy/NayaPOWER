#!/usr/bin/env python3
"""CAL-FIX18 item 3: is the cover VISIBLE on each slide? Ground truth:
screenshot the #dayScroll rect with #dayCoverBg shown, then with it
display:none. Identical pixels => the cover contributes nothing visible
on that slide. Usage: covervis18.py [firefox|chromium] [fonts|nofont] [390|1920]
"""
import hashlib, os, sys
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
WHICH = sys.argv[1] if len(sys.argv) > 1 else "firefox"
FONT = sys.argv[2] if len(sys.argv) > 2 else "nofont"
W = int(sys.argv[3]) if len(sys.argv) > 3 else 1920
H = 844 if W == 390 else 999
TAG = f"{WHICH}-{FONT}-{W}"
HTML = open(os.path.join(HERE, "base-fix17.html"), encoding="utf-8").read()
SHOTS = os.path.join(HERE, "shots18")
os.makedirs(SHOTS, exist_ok=True)

INFO = r"""() => {
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect();
    return {x:Math.round(b.x), y:Math.round(b.y), w:Math.round(b.width), h:Math.round(b.height)}; };
  const ds = document.querySelector('#dayScroll');
  const on = [...document.querySelectorAll('#dayScroll .smart-block')].find(e=>e.classList.contains('on'));
  const bg = document.querySelector('#dayCoverBg');
  const img = document.querySelector('#coverImg');
  const cs = (el) => { if (!el) return null; const c = getComputedStyle(el);
    return {bg: c.backgroundColor, bgImg: c.backgroundImage.slice(0,80), op: c.opacity}; };
  return {slide: on ? (on.id || on.className) : null,
    scrollRect: r(ds), coverRect: r(bg), coverImgRect: r(img),
    coverBgStyle: cs(bg), coverImgStyle: cs(img),
    scrollStyle: cs(ds), slideStyle: cs(on),
    catStyle: on ? cs(on.querySelector('section.cat, .cat')) : null,
    sbScrollStyle: on ? cs(on.querySelector('.sb-scroll')) : null,
    dayScrollBg: getComputedStyle(document.querySelector('.day-scroll')).backgroundColor};
}"""

def open_day(page, d):
    page.evaluate("() => { const b = document.getElementById('backToMonth'); if (b) b.click(); }")
    page.wait_for_timeout(600)
    page.evaluate("(dd) => { const c=[...document.querySelectorAll('.cell[data-d]')].find(x=>+x.dataset.d===dd); if(c) c.click(); }", d)
    page.wait_for_timeout(2000)

def goto_slide(page, i):
    page.evaluate("(ii) => { const dots=[...document.querySelectorAll('#dayScroll .sb-dots button')]; if(dots[ii]) dots[ii].click(); }", i)
    page.wait_for_timeout(2000)

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
    open_day(page, 20)
    print(f"=== cover-visibility base {TAG} ===")
    for i in range(9):
        goto_slide(page, i)
        info = page.evaluate(INFO)
        clip = info["scrollRect"]
        clip = {"x": clip["x"], "y": clip["y"], "width": clip["w"], "height": clip["h"]}
        page.evaluate("() => { document.querySelector('#dayCoverBg').style.display=''; }")
        page.wait_for_timeout(300)
        a = page.screenshot(clip=clip)
        page.evaluate("() => { document.querySelector('#dayCoverBg').style.display='none'; }")
        page.wait_for_timeout(300)
        b = page.screenshot(clip=clip)
        page.evaluate("() => { document.querySelector('#dayCoverBg').style.display=''; }")
        ha, hb = hashlib.sha256(a).hexdigest()[:12], hashlib.sha256(b).hexdigest()[:12]
        same = (ha == hb)
        print(f"slide {i}: {info['slide']} | coverVISIBLE={not same} (on={ha} off={hb}) | "
              f"scroll={info['scrollStyle']} slide={info['slideStyle']} cat={info['catStyle']} sbScroll={info['sbScrollStyle']}")
        if not same:
            open(os.path.join(SHOTS, f"cv-{TAG}-{i}-on.png"), "wb").write(a)
            open(os.path.join(SHOTS, f"cv-{TAG}-{i}-off.png"), "wb").write(b)
    print("PAGE ERRORS:", errs if errs else "NONE")
    browser.close()
