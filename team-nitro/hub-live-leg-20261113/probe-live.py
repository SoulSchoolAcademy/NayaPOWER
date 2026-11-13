#!/usr/bin/env python3
"""Live-leg walked-entrance probe (Terra, 2026-11-13).
Start at the LIVE login page, enter as a fresh visitor, follow the LIVE
deep link /s/sn2696 by real anchor click. Widths: 390 first, then 1440,
then 360. Fresh context per width. Shape modeled on the slug round's
probe-walked-entrance.py (page.evaluate strings work on this Firefox).
Outputs: probe-live-results.json + probe-live-*.png in this work dir.
"""
import json

from playwright.sync_api import sync_playwright

MEASURE = """() => {
  const cs = (el, p) => el ? getComputedStyle(el)[p] : null;
  const pills = [...document.querySelectorAll('.obb-pill')];
  const jewels = pills.map(p => p.querySelector('.obb-jewel'));
  const segs = [...document.querySelectorAll('.notif-seg')];
  const overlay = document.querySelector('.naya-install-overlay');
  const ovVisible = overlay ? (getComputedStyle(overlay).display !== 'none' && overlay.classList.contains('show')) : false;
  const de = document.documentElement;
  return {
    url: location.href,
    title: document.title,
    bodyTextHasIsntHere: document.body.innerText.includes("isn't here"),
    hook: document.body.innerText.includes('Not one feed like Facebook'),
    nutshell: document.body.innerText.includes('IN A NUTSHELL'),
    sn2696Title: document.body.innerText.includes('SN-2696'),
    installOverlay: ovVisible,
    overflowX: de.scrollWidth > window.innerWidth + 1,
    scrollW: de.scrollWidth, innerW: window.innerWidth,
    intelBoards: document.querySelectorAll('.intel-board').length,
    pills: pills.length,
    jewelRadius: jewels.map(j => cs(j, 'borderRadius')),
    jewelSize: jewels.map(j => j ? Math.round(j.getBoundingClientRect().width) : null),
    pillLabels: pills.map(p => (p.textContent || '').trim().slice(0, 20)),
    segs: segs.length,
    segLabels: segs.map(s => (s.textContent || '').trim().slice(0, 20)),
    segRadius: segs.map(s => cs(s.querySelector('.notif-tile') || s.firstElementChild, 'borderRadius')),
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
        page.goto("https://nayanet.app/", timeout=60000)
        page.wait_for_timeout(1500)
        page.screenshot(path=f"probe-live-entrance-{w}.png")
        r["entrance_title"] = page.title()
        r["entrance_text"] = (page.evaluate("document.body.innerText.slice(0,300)") or "").replace("\n", " | ")
        name_input = page.locator('input[name="name"], input[placeholder*="name" i]').first
        if name_input.count() == 0:
            name_input = page.locator("input").first
        name_input.fill("Probe Visitor")
        enter = page.locator('button:has-text("Enter NayaNET")').first
        if enter.count() == 0:
            enter = page.locator('button[type="submit"]').first
        enter.click()
        try:
            page.wait_for_url("**#/hub", timeout=15000)
        except Exception:
            pass
        page.wait_for_timeout(1500)
        r["after_enter_url"] = page.url
        r["after_enter_title"] = page.title()
        page.evaluate("""(href) => {
          const a = document.createElement('a');
          a.href = href; a.textContent = 'probe link'; a.id = 'probe-link';
          document.body.appendChild(a); a.click();
        }""", "https://nayanet.app/s/sn2696")
        try:
            page.wait_for_url("**#/smart-notes/sn2696", timeout=20000)
        except Exception:
            pass
        page.wait_for_timeout(2500)
        r["note"] = page.evaluate(MEASURE)
        page.screenshot(path=f"probe-live-note-{w}.png")
        page.wait_for_timeout(1500)
        r["note_plus3s_overlay"] = page.evaluate("() => { const o = document.querySelector('.naya-install-overlay'); return o ? (getComputedStyle(o).display !== 'none' && o.classList.contains('show')) : false; }")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1200)
        page.screenshot(path=f"probe-live-scrolled-{w}.png")
        r["scrolled"] = page.evaluate("({scrollW: document.documentElement.scrollWidth, innerW: window.innerWidth})")
        page.evaluate("window.scrollTo(0, 0)")
        r["console_errors"] = errs
        r["page_errors_note"] = perrs
        errs2, perrs2 = [], []
        page2 = ctx.new_page()
        page2.on("console", lambda m: errs2.append(m.text) if m.type == "error" else None)
        page2.on("pageerror", lambda e: perrs2.append(str(e)))
        page2.goto("https://nayanet.app/hub/feed", timeout=60000)
        page2.wait_for_timeout(2500)
        r["hub_feed"] = page2.evaluate("({url: location.href, title: document.title, overflowX: document.documentElement.scrollWidth > window.innerWidth + 1})")
        r["console_errors_feed"] = errs2
        r["page_errors_feed"] = perrs2
        page2.screenshot(path=f"probe-live-feed-{w}.png")
        results[str(w)] = r
        print(f"== {w} ==")
        print(json.dumps(r, indent=1)[:3200])
        ctx.close()
    browser.close()

open("probe-live-results.json", "w").write(json.dumps(results, indent=2))
print("OK probe-live-results.json written")
