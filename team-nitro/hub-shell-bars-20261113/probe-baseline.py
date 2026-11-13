#!/usr/bin/env python3
"""Hub Shell Bars — BASELINE probe (pre-edit staged shell, slug round's bytes).
Playwright Firefox, fresh profile per width. 390 first, then 1440, then 360.
Start at the staged note link /s/sn2696; confirm the note landing, then measure
the bars as they stand: which fixed bars are visible, their rects, computed
.main padding, --notif-h / --obb-below, and the lowest text rect at max scroll
(fixed-ancestor-excluded). Screenshots -> work dir.
"""
import json
from playwright.sync_api import sync_playwright

WD = "/home/hatch/workspace/team-nitro/hub-shell-bars-20261113"
STAGING = "https://naya-public-blog-staging.nayapower.workers.dev"

MEASURE_JS = """() => {
  const q = s => document.querySelector(s);
  const qa = s => [...document.querySelectorAll(s)];
  const r = el => { if (!el) return null; const b = el.getBoundingClientRect();
    return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width),
            h: Math.round(b.height), top: Math.round(b.top), bottom: Math.round(b.bottom)}; };
  const cs = el => el ? getComputedStyle(el) : null;
  const fixedAncestor = el => { let n = el; while (n) { const p = getComputedStyle(n).position;
    if (p === 'fixed') return true; n = n.parentElement; } return false; };
  const out = {};
  out.url = location.href; out.title = document.title;
  const txt = document.body.innerText || '';
  out.notHere = txt.includes("That note isn't here");
  out.hook = txt.includes("Not one feed like Facebook");
  out.noteTitle = txt.includes("SN-2696");
  const main = q('.main');
  out.mainPaddingBottom = main ? cs(main).paddingBottom : null;
  out.notifH = getComputedStyle(document.documentElement).getPropertyValue('--notif-h').trim();
  out.obbBelow = getComputedStyle(document.documentElement).getPropertyValue('--obb-below').trim();
  out.bodyClasses = document.body.className;
  // bars
  const obb = q('#obb-bar');
  out.obbBar = r(obb);
  out.obbBarVisible = !!(obb && cs(obb).display !== 'none' && cs(obb).visibility !== 'hidden');
  out.obbPills = qa('#obb-bar .obb-pill').map(a => {
    const j = a.querySelector('.obb-jewel'); const jc = j ? cs(j) : null;
    return {label: (a.querySelector('.obb-lbl')||{}).innerText || a.getAttribute('aria-label'),
      href: a.getAttribute('href'), jewel: r(j),
      jewelRadius: jc ? jc.borderRadius : null, jewelW: j ? Math.round(j.getBoundingClientRect().width) : null}; });
  const nb = q('#naya-notif-bar');
  out.notifBar = r(nb);
  out.notifBarVisible = !!(nb && cs(nb).display !== 'none');
  out.notifSegs = qa('#naya-notif-bar .notif-seg').map(s => {
    const t = s.querySelector('.notif-tile'); const tc = t ? cs(t) : null;
    return {key: s.getAttribute('data-notif'), label: (s.querySelector('.notif-lbl')||{}).innerText || null,
      tile: r(t), tileRadius: tc ? tc.borderRadius : null,
      count: (s.querySelector('.notif-count')||{}).innerText || null,
      countShown: s.querySelector('.notif-count') ? cs(s.querySelector('.notif-count')).display : null}; });
  const eco = q('.eco-bottombar');
  out.ecoBar = r(eco);
  out.ecoVisible = !!(eco && cs(eco).display !== 'none' && cs(eco).visibility !== 'hidden' && eco.getBoundingClientRect().height > 0);
  out.ecoBtns = qa('.eco-bottombar .eco-bb-btn').length;
  const ico = q('.eco-bottombar .eco-bb-ico');
  out.ecoIco = r(ico); out.ecoIcoRadius = ico ? cs(ico).borderRadius : null;
  out.overflow = document.documentElement.scrollWidth - window.innerWidth;
  out.viewH = window.innerHeight;
  out.docH = document.documentElement.scrollHeight;
  return out;
}"""

COVER_JS = """() => {
  const fixedAncestor = el => { let n = el; while (n) { const p = getComputedStyle(n).position;
    if (p === 'fixed') return true; n = n.parentElement; } return false; };
  // lowest visible text leaf in the flow (not inside a fixed ancestor)
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let lowest = null, node;
  while (node = walker.nextNode()) {
    if (!node.nodeValue || !node.nodeValue.trim()) continue;
    const el = node.parentElement; if (!el || fixedAncestor(el)) continue;
    const b = el.getBoundingClientRect();
    if (b.height <= 0 || b.bottom <= 0) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    if (!lowest || b.bottom > lowest.bottom) lowest = {text: node.nodeValue.trim().slice(0, 60), bottom: Math.round(b.bottom), top: Math.round(b.top)};
  }
  const bars = ['#naya-notif-bar', '.eco-bottombar', '#obb-bar'].map(s => {
    const el = document.querySelector(s); if (!el) return {sel: s, top: null};
    return {sel: s, top: Math.round(el.getBoundingClientRect().top), h: Math.round(el.getBoundingClientRect().height)}; });
  return {lowest, bars, viewH: window.innerHeight, scrollY: Math.round(window.scrollY),
          maxScroll: Math.round(document.documentElement.scrollHeight - window.innerHeight)};
}"""

def run_width(pw, width, height):
    print(f"== WIDTH {width} ==")
    browser = pw.firefox.launch(headless=True)
    ctx = browser.new_context(viewport={"width": width, "height": height})
    pg = ctx.new_page()
    console_errors, page_errors = [], []
    pg.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: page_errors.append(str(e)))
    pg.goto(STAGING + "/s/sn2696", timeout=60000)
    pg.wait_for_timeout(4000)
    d = pg.evaluate(MEASURE_JS)
    d["console_errors"] = console_errors
    d["page_errors"] = page_errors
    print(json.dumps(d, indent=1))
    pg.screenshot(path=f"{WD}/baseline-note-{width}.png")
    # bar crop: bottom 260px
    pg.screenshot(path=f"{WD}/baseline-bars-{width}.png",
                  clip={"x": 0, "y": max(0, d["viewH"] - 280), "width": width, "height": min(280, d["viewH"])})
    # max scroll cover
    pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    pg.wait_for_timeout(1200)
    cover = pg.evaluate(COVER_JS)
    print("COVER @max-scroll:", json.dumps(cover))
    d["cover_max_scroll"] = cover
    pg.screenshot(path=f"{WD}/baseline-scrolled-{width}.png")
    pg.evaluate("window.scrollTo(0,0)")
    browser.close()
    return d

results = {}
with sync_playwright() as pw:
    for w, h in [(390, 844), (1440, 900), (360, 800)]:
        results[w] = run_width(pw, w, h)
json.dump(results, open(f"{WD}/baseline-results.json", "w"), indent=1)
print("WROTE baseline-results.json")
