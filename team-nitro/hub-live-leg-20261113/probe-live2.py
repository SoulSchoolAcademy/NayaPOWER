#!/usr/bin/env python3
"""Live-leg bars + note proof, cold-link flow (Terra, 2026-11-13).
Per width (390, 1440, 360): fresh context -> goto the live deep link
https://nayanet.app/#/smart-notes/sn2696 -> entrance -> enter name ->
note renders. Measures bars in detail (radii, sizes, labels, gem SVGs),
install overlay at first paint + 3.5s, errors, overflow. Screenshots.
"""
import json
from playwright.sync_api import sync_playwright

MEASURE = """() => {
  const cs = (el, p) => el ? getComputedStyle(el)[p] : null;
  const pills = [...document.querySelectorAll('.obb-pill')];
  const jewels = pills.map(p => p.querySelector('.obb-jewel'));
  const segs = [...document.querySelectorAll('.notif-seg')];
  const overlay = document.querySelector('.naya-install-overlay');
  const ov = overlay ? (getComputedStyle(overlay).display !== 'none' && overlay.classList.contains('show')) : false;
  const de = document.documentElement;
  return {
    url: location.href, title: document.title,
    hasIsntHere: document.body.innerText.includes("isn't here"),
    hook: document.body.innerText.includes('Not one feed like Facebook'),
    nutshell: document.body.innerText.includes('IN A NUTSHELL'),
    sn2696: document.body.innerText.includes('SN-2696'),
    installOverlay: ov,
    overflowX: de.scrollWidth > window.innerWidth + 1,
    boards: document.querySelectorAll('.intel-board').length,
    pills: pills.length,
    jewelRadius: [...new Set(jewels.map(j => cs(j, 'borderRadius')))],
    jewelSize: [...new Set(jewels.map(j => j ? Math.round(j.getBoundingClientRect().width) : null))],
    pillLabels: pills.map(p => (p.textContent || '').trim()),
    segs: segs.length,
    segLabels: segs.map(s => (s.textContent || '').trim()),
    segRadius: [...new Set(segs.map(s => cs(s.querySelector('.notif-tile') || s.firstElementChild, 'borderRadius')))],
    segSize: [...new Set(segs.map(s => { const t = s.querySelector('.notif-tile') || s.firstElementChild; return t ? Math.round(t.getBoundingClientRect().width) : null; }))],
    gemSvg: segs.map(s => { const g = s.querySelector('svg'); return g ? g.outerHTML.length : 0; }),
    notifBar: !!document.querySelector('#naya-notif-bar'),
    obbBar: !!document.querySelector('#obb-bar'),
  };
}"""

WIDTHS = [(390, 844), (1440, 900), (360, 800)]
results = {}

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    for w, h in WIDTHS:
        errs, perrs = [], []
        ctx = browser.new_context(viewport={"width": w, "height": h})
        page = ctx.new_page()
        page.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: perrs.append(str(e)))
        r = {"width": w}
        page.goto("https://nayanet.app/#/smart-notes/sn2696", timeout=60000)
        page.wait_for_timeout(2000)
        page.screenshot(path=f"probe-live2-entrance-{w}.png")
        r["entrance_title"] = page.title()
        inp = page.locator('input[name="name"], input[placeholder*="name" i]').first
        if inp.count() == 0:
            inp = page.locator("input").first
        inp.fill("Probe Visitor")
        page.locator('button:has-text("Enter NayaNET")').first.click()
        try:
            page.wait_for_function("() => document.title.includes('SN-2696')", timeout=20000)
        except Exception:
            pass
        page.wait_for_timeout(800)
        r["note_firstpaint"] = page.evaluate(MEASURE)
        page.screenshot(path=f"probe-live2-note-{w}.png")
        page.wait_for_timeout(3500)
        m = page.evaluate(MEASURE)
        r["note_plus3_5s"] = {"installOverlay": m["installOverlay"], "title": m["title"]}
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000)
        page.screenshot(path=f"probe-live2-scrolled-{w}.png")
        r["scrolled"] = page.evaluate("({scrollW: document.documentElement.scrollWidth, innerW: window.innerWidth})")
        r["console_errors"] = errs
        r["page_errors"] = perrs
        results[str(w)] = r
        print(f"== {w} ==")
        print(json.dumps(r, indent=1))
        ctx.close()
    browser.close()

open("probe-live2-results.json", "w").write(json.dumps(results, indent=2))
print("OK probe-live2-results.json written")
