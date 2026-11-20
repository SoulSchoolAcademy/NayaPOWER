#!/usr/bin/env python3
"""Decisive §8 READ test: trace the letter-button click and /agreement load."""
import json
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8899"
out = {}

with sync_playwright() as p:
    br = p.chromium.launch(
        proxy={"server": "http://127.0.0.1:18080", "bypass": "127.0.0.1,localhost"},
        args=["--no-sandbox"])

    # (1) direct /agreement load
    ctx = br.new_context(viewport={"width": 1920, "height": 900})
    pg = ctx.new_page()
    navs = []
    pg.on("framenavigated", lambda f: navs.append(f.url) if f == pg.main_frame else None)
    reqs = []
    pg.on("request", lambda r: reqs.append(r.url[:110]))
    pg.on("response", lambda r: reqs.append(f"RESP {r.status} {r.url[:100]}"))
    pg.goto(BASE + "/agreement", wait_until="load")
    pg.wait_for_timeout(4000)
    out["direct_agreement"] = {"url": pg.url, "title": pg.evaluate("() => document.title"),
                               "navs": navs,
                               "h1": pg.evaluate("() => { const h = document.querySelector('h1'); return h ? h.textContent.slice(0,80) : null; }")}
    pg.screenshot(path="/tmp/fix2/proof/s8-direct-agreement.png")
    ctx.close()

    # (2) letter-button click with full tracing
    ctx = br.new_context(viewport={"width": 1920, "height": 900})
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    navs2 = []
    pg.on("framenavigated", lambda f: navs2.append(f.url) if f == pg.main_frame else None)
    reqs2 = []
    pg.on("request", lambda r: reqs2.append(r.url[:110]))
    pg.goto(BASE + "/?stage=bridge", wait_until="load")
    pg.wait_for_timeout(5000)
    out["view_at_load"] = pg.evaluate("() => window.__fpStage ? window.__fpStage.state.view : 'NO-STATE'")
    for btn in ("#fpBridgeMore1", "#fpBridgeMore2", "#fpBridgeMore3", "#fpBridgeMore4"):
        pg.click(btn, timeout=3000)
        pg.wait_for_timeout(900)
    pg.evaluate("document.querySelector('#fpBridge').scrollTop = 999999")
    pg.wait_for_timeout(800)
    out["view_before_letter_click"] = pg.evaluate("() => window.__fpStage ? window.__fpStage.state.view : 'NO-STATE'")
    out["letter_btn"] = pg.evaluate("""() => { const b = document.querySelector('#fpBridgeLetter');
      const r = b.getBoundingClientRect(); return {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height), hidden: b.hidden}; }""")
    # click via DOM .click() so no hit-target ambiguity, and log what happens
    pg.evaluate("document.querySelector('#fpBridgeLetter').click()")
    for _ in range(20):
        pg.wait_for_timeout(500)
        if "/agreement" in pg.url or "proof-host" in pg.url:
            break
    pg.wait_for_timeout(2000)
    out["after_dom_click"] = {"url": pg.url, "title": pg.evaluate("() => document.title"),
                              "navs": navs2, "errors": errs,
                              "reqs_tail": reqs2[-8:]}
    pg.screenshot(path="/tmp/fix2/proof/s8-after-domclick.png")
    ctx.close()
    br.close()

print(json.dumps(out, indent=1))
with open("/tmp/fix2/proof/results3.json", "w") as f:
    json.dump(out, f, indent=1)
