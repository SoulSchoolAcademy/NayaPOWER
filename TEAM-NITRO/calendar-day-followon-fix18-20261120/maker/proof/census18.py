#!/usr/bin/env python3
"""CAL-FIX18 item 3: per-slide COVER census on BASE bytes.
For each of the 9 deck slides: is #coverImg actually visible anywhere
inside the #dayScroll viewport? Grid-sample elementFromPoint over the
scroll rect; count hits whose top element is #coverImg/#dayCoverBg.
Usage: census18.py [firefox|chromium] [fonts|nofont] [390|1920]
"""
import json, os, sys
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

CENSUS = r"""() => {
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect();
    return {x:Math.round(b.x), y:Math.round(b.y), w:Math.round(b.width), h:Math.round(b.height)}; };
  const ds = document.querySelector('#dayScroll');
  const on = [...document.querySelectorAll('#dayScroll .smart-block')].find(e=>e.classList.contains('on'));
  const cc = [...document.querySelectorAll('button')].find(b=>/Change cover/i.test(b.textContent));
  const ccVis = cc ? (getComputedStyle(cc).display !== 'none' && cc.getBoundingClientRect().width > 0) : null;
  const cover = document.querySelector('#coverImg');
  const coverBg = document.querySelector('#dayCoverBg');
  const dsR = ds.getBoundingClientRect();
  const ccR = cc ? cc.getBoundingClientRect() : null;
  const step = innerWidth <= 560 ? 30 : 48;
  let total = 0, coverHits = 0, pillHits = 0;
  const hitKinds = {};
  for (let y = Math.ceil(dsR.top) + 8; y < dsR.bottom - 4; y += step) {
    for (let x = Math.ceil(dsR.left) + 8; x < dsR.right - 4; x += step) {
      if (ccR && x >= ccR.left && x <= ccR.right && y >= ccR.top && y <= ccR.bottom) { pillHits++; continue; }
      const e = document.elementFromPoint(x, y);
      total++;
      if (!e) continue;
      const k = (e.id === 'coverImg' || e.id === 'dayCoverBg') ? 'COVER'
        : (e.tagName + '.' + String(e.className).split(' ')[0]);
      hitKinds[k] = (hitKinds[k] || 0) + 1;
      if (k === 'COVER') coverHits++;
    }
  }
  const cs = on ? getComputedStyle(on) : null;
  return {slide: on ? (on.id || on.className) : null,
    slideText: on ? on.textContent.replace(/\s+/g,' ').trim().slice(0,40) : null,
    slideBg: cs ? cs.backgroundColor : null, slideBgImg: cs ? cs.backgroundImage.slice(0,60) : null,
    slideRect: r(on), scrollRect: r(ds),
    coverRect: r(cover), coverVisible: cover ? (getComputedStyle(cover).display !== 'none' && cover.getBoundingClientRect().width > 0) : null,
    coverNatural: cover ? {nw: cover.naturalWidth, nh: cover.naturalHeight, complete: cover.complete, src: (cover.currentSrc||cover.src||'').slice(-60)} : null,
    samples: total, coverHits, pillHits,
    coverFrac: total ? +(coverHits/total).toFixed(3) : null,
    topHits: Object.entries(hitKinds).sort((a,b)=>b[1]-a[1]).slice(0,6),
    pillVisible: ccVis, pillRect: r(cc),
    docScrollW: document.documentElement.scrollWidth};
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
    print(f"=== census base {TAG} ===")
    for i in range(9):
        goto_slide(page, i)
        m = page.evaluate(CENSUS)
        print(f"slide {i}: {m['slide']} | {m['slideText']!r} | bg={m['slideBg']} | "
              f"samples={m['samples']} coverHits={m['coverHits']} frac={m['coverFrac']} "
              f"pillVis={m['pillVisible']} pill={m['pillRect']} | top={m['topHits']} | docW={m['docScrollW']}")
        page.screenshot(path=os.path.join(SHOTS, f"census-{TAG}-{i}.png"))
    print("cover natural:", page.evaluate("() => { const c=document.querySelector('#coverImg'); return c ? {nw:c.naturalWidth, nh:c.naturalHeight, complete:c.complete} : null; }"))
    print("PAGE ERRORS:", errs if errs else "NONE")
    browser.close()
