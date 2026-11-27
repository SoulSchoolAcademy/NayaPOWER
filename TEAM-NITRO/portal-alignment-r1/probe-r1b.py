#!/usr/bin/env python3
"""R1b re-probe — strip position only, both widths, staged R1."""
import json, os
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://portal-alignment-r1-staging.nayapower.workers.dev"
PROXY = {"server": "http://127.0.0.1:18080"}
EXE = "/home/hatch/.cache/ms-playwright/chromium-1255/chrome-linux64/chrome"
JS = """() => {
  const strip = document.querySelector('.fp-walk-strip');
  const sr = strip ? strip.getBoundingClientRect() : null;
  const cs = strip ? getComputedStyle(strip) : null;
  const stage = document.querySelector('section.stage').getBoundingClientRect();
  return {vw: window.innerWidth, scrollW: document.scrollingElement.scrollWidth,
    stage: {h: Math.round(stage.height)},
    strip: strip ? {text: strip.textContent.replace(/\\s+/g,' ').trim(),
      pos: cs.position, bottom: cs.bottom, whiteSpace: cs.whiteSpace,
      rect: {x: Math.round(sr.x), y: Math.round(sr.y), w: Math.round(sr.width), h: Math.round(sr.height), right: Math.round(sr.right), bottom: Math.round(sr.bottom)}} : null,
    navGrid: getComputedStyle(document.querySelector('nav.eco-inline')).display};
}"""
out = {}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    for tag, w, h in [("phone", 390, 844), ("desk", 1440, 900)]:
        pg = b.new_page(viewport={"width": w, "height": h}, proxy=PROXY)
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
        pg.goto(BASE + "/", wait_until="networkidle", timeout=90000)
        pg.wait_for_timeout(1200)
        out[tag] = pg.evaluate(JS)
        out[tag]["pageerrors"] = errs
        pg.screenshot(path=os.path.join(HERE, f"r1b-{tag}-front.png"))
        pg.close()
    b.close()
print(json.dumps(out, indent=2))
