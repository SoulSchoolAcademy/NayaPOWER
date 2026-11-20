#!/usr/bin/env python3
"""Fix-4: live-CSS experiment for the certifies-line vs hero-name collision.
Loads identity paired at 390, waits for taken, then applies candidate
overrides via add_style_tag and measures name/title/line/wrapper/status.
"""
import json
from playwright.sync_api import sync_playwright
BASE = "https://naya-walk-beginning-staging.nayapower.workers.dev"
MEASURE = """() => {
  const R = el => { if (!el) return null; const r = el.getBoundingClientRect();
    return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
  const ov = (a,b) => { if (!a||!b) return 0; const x=Math.max(0,Math.min(a[2],b[2])-Math.max(a[0],b[0])); const y=Math.max(0,Math.min(a[3],b[3])-Math.max(a[1],b[1])); return Math.round(x*y); };
  const name = document.getElementById('displayName');
  const title = document.querySelector('.cert-title');
  const line = document.querySelector('.cert-certifies');
  const wrap = document.querySelector('.face-center');
  const status = document.querySelector('.alias-status');
  const head = document.querySelector('.face-head');
  const nr = R(name), tr = R(title), lr = R(line), wr = R(wrap), sr = R(status);
  return {plaque: (document.querySelector('.cert-plaque')||{}).className,
    nameRect: nr, titleRect: tr, lineRect: lr, wrapRect: wr, statusRect: sr, headRect: R(head),
    headJustify: head ? getComputedStyle(head).justifyContent : null,
    nameLineOv: ov(nr, lr), nameTitleOv: ov(nr, tr), lineTitleOv: ov(lr, tr),
    wrapStatusOv: ov(wr, sr)}; }"""
CANDIDATES = {
  "base": None,
  "c1-line13-m24": "@media (max-width:480px){ .cert-certifies{font-size:0.82rem !important; margin-top:0 !important;} .cert-plaque.taken .face-center,.cert-plaque.is-certified .face-center,.cert-plaque.has-name .face-center{margin-top:24px !important;} }",
  "c2-hide-line": "@media (max-width:480px){ .cert-plaque.taken .cert-certifies,.cert-plaque.is-certified .cert-certifies,.cert-plaque.has-name .cert-certifies{display:none !important;} }",
  "c3-line13-m20-name26": "@media (max-width:480px){ .cert-certifies{font-size:0.82rem !important; margin-top:0 !important;} .cert-name{font-size:26px !important;} .cert-plaque.taken .face-center,.cert-plaque.is-certified .face-center,.cert-plaque.has-name .face-center{margin-top:20px !important;} }",
}
with sync_playwright() as pw:
    b = pw.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    pg = ctx.new_page()
    pg.goto(BASE + "/identity.html?name=Shawn&alias=Shawn", timeout=60000)
    pg.wait_for_timeout(6000)
    for label, css in CANDIDATES.items():
        if css:
            pg.add_style_tag(content=css)
            pg.wait_for_timeout(400)
        print(label, json.dumps(pg.evaluate(MEASURE)), flush=True)
        if label == "c1-line13-m24":
            pg.screenshot(path="proof-fix4/fix4-exp-c1.png")
        if label == "c2-hide-line":
            pg.screenshot(path="proof-fix4/fix4-exp-c2.png")
    ctx.close(); b.close()
