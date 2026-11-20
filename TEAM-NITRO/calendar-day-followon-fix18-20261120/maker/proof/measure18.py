#!/usr/bin/env python3
"""CAL-FIX18: measure BASE header geometry (fix17 bytes) — monthline
centeredness, November<->2026 gap, header Hz census, wisdom line.
Usage: measure18.py [base|fixed] [firefox|chromium] [fonts|nofont] [390|1920]
"""
import json, os, sys
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
WHICH_FILE = sys.argv[1] if len(sys.argv) > 1 else "base"
WHICH = sys.argv[2] if len(sys.argv) > 2 else "firefox"
FONT = sys.argv[3] if len(sys.argv) > 3 else "nofont"
W = int(sys.argv[4]) if len(sys.argv) > 4 else 390
H = 844 if W == 390 else 999
TAG = f"{WHICH_FILE}-{WHICH}-{FONT}-{W}"
SRC = os.path.join(HERE, "base-fix17.html" if WHICH_FILE == "base" else "fixed-fix18.html")
HTML = open(SRC, encoding="utf-8").read()
SHOTS = os.path.join(HERE, "shots18")
os.makedirs(SHOTS, exist_ok=True)

MEAS = r"""() => {
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect();
    return {x:Math.round(b.x), y:Math.round(b.y), w:Math.round(b.width), h:Math.round(b.height),
      left:Math.round(b.left), right:Math.round(b.right), top:Math.round(b.top), bottom:Math.round(b.bottom),
      cx:Math.round(b.left + b.width/2), cy:Math.round(b.top + b.height/2)}; };
  const head = document.querySelector('.official-headliner');
  const ml = document.querySelector('.hl-monthline');
  const script = ml ? ml.querySelector('.hl-script') : null;
  const nums = ml ? [...ml.querySelectorAll('.os-mini-num.daynum')] : [];
  const center = document.querySelector('.hl-center');
  const left = document.querySelector('.hl-left');
  const stats = document.querySelector('.stats-btn');
  const timewrap = document.querySelector('.hl-timewrap');
  const back = document.getElementById('backToMonth');
  const orb = document.querySelector('.daybar .sigpiece, .sigpiece');
  const dt = document.querySelector('#dayTeach');
  const mlR = r(ml), scR = r(script);
  const yearR = nums.length ? r(nums[0]) : null;
  const hzR = nums.length > 1 ? r(nums[1]) : null;
  const vwC = Math.round(innerWidth / 2);
  return {
    vw: innerWidth, vh: innerHeight, vwCenter: vwC,
    fonts: [...document.fonts].map(f=>f.family+':'+f.status),
    headerText: head ? head.innerText.replace(/\s+/g,' ').trim() : null,
    headerHTMLHasHz: head ? /Hz/.test(head.innerHTML) : null,
    monthlineText: ml ? ml.textContent.replace(/\s+/g,' ').trim() : null,
    monthline: mlR,
    monthlineCenterOff: mlR ? mlR.cx - vwC : null,
    nov: scR, year: yearR, hzTiles: hzR,
    novYearGap: (scR && yearR) ? Math.round(yearR.left - scR.right) : null,
    numSpans: nums.length,
    center: r(center), left: r(left), stats: r(stats), timewrap: r(timewrap),
    backToMonth: r(back), orb: r(orb),
    wisdom: dt ? dt.textContent.replace(/\s+/g,' ').trim() : null,
    wisdomHzCount: dt ? (dt.textContent.match(/396/g)||[]).length : null,
    docScrollW: document.documentElement.scrollWidth,
    pageErrors: window.__errs || []
  };
}"""

def open_day(page, d):
    page.evaluate("() => { const b = document.getElementById('backToMonth'); if (b) b.click(); }")
    page.wait_for_timeout(600)
    page.evaluate("(dd) => { const c=[...document.querySelectorAll('.cell[data-d]')].find(x=>+x.dataset.d===dd); if(c) c.click(); }", d)
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
    m = page.evaluate(MEAS)
    m["pageErrors"] = errs
    print(f"=== {TAG} ===")
    print(json.dumps(m, indent=1))
    page.screenshot(path=os.path.join(SHOTS, f"header-{TAG}.png"),
                    clip={"x": 0, "y": 0, "width": W, "height": 320})
    page.screenshot(path=os.path.join(SHOTS, f"full-{TAG}.png"))
    browser.close()
