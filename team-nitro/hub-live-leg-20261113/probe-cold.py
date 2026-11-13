#!/usr/bin/env python3
"""Cold deep-link diagnosis (Terra, 2026-11-13).
Two fresh-context loads, no login first:
  A. https://nayanet.app/#/smart-notes/sn2696  (the worker's 302 target)
  B. https://nayanet.app/hub#/smart-notes/sn2696 (the Hub shell directly)
Measure after 6s + after entering a name on A.
"""
import json
from playwright.sync_api import sync_playwright

MEASURE = """() => ({
  url: location.href,
  title: document.title,
  hasIsntHere: document.body.innerText.includes("isn't here"),
  hook: document.body.innerText.includes('Not one feed like Facebook'),
  nutshell: document.body.innerText.includes('IN A NUTSHELL'),
  sn2696: document.body.innerText.includes('SN-2696'),
  boards: document.querySelectorAll('.intel-board').length,
  pills: document.querySelectorAll('.obb-pill').length,
  segs: document.querySelectorAll('.notif-seg').length,
  bodyStart: document.body.innerText.slice(0, 200).replace(/\\n/g, ' | '),
})"""

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    # A: cold 302 target
    ctx = browser.new_context(viewport={"width": 390, "height": 844})
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("https://nayanet.app/#/smart-notes/sn2696", timeout=60000)
    pg.wait_for_timeout(6000)
    print("A cold /#/smart-notes/sn2696 @6s:", json.dumps(pg.evaluate(MEASURE), indent=1))
    print("A pageerrors:", errs)
    pg.screenshot(path="probe-cold-A-390.png")
    # enter a name on A: does the entrance preserve the note hash?
    try:
        inp = pg.locator('input[name="name"], input[placeholder*="name" i]').first
        if inp.count():
            inp.fill("Probe Visitor")
            btn = pg.locator('button:has-text("Enter NayaNET")').first
            btn.click()
            pg.wait_for_timeout(5000)
            print("A after entering name:", json.dumps(pg.evaluate(MEASURE), indent=1))
            pg.screenshot(path="probe-cold-A-entered-390.png")
    except Exception as e:
        print("A enter step error:", e)
    ctx.close()
    # B: Hub-direct
    ctx = browser.new_context(viewport={"width": 390, "height": 844})
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("https://nayanet.app/hub#/smart-notes/sn2696", timeout=60000)
    pg.wait_for_timeout(6000)
    print("B cold /hub#/smart-notes/sn2696 @6s:", json.dumps(pg.evaluate(MEASURE), indent=1))
    print("B pageerrors:", errs)
    pg.screenshot(path="probe-cold-B-390.png")
    pg.wait_for_timeout(6000)
    print("B @12s:", json.dumps(pg.evaluate(MEASURE), indent=1))
    ctx.close()
    browser.close()
print("OK cold diagnosis done")
