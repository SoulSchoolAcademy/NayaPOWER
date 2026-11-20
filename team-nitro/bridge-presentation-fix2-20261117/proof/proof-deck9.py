#!/usr/bin/env python3
"""Deck drive to beat 9 via #fpNextBtn + deckBack at beat 9."""
import json
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8899"
out = {}

with sync_playwright() as p:
    br = p.chromium.launch(
        proxy={"server": "http://127.0.0.1:18080", "bypass": "127.0.0.1,localhost"},
        args=["--no-sandbox"])
    ctx = br.new_context(viewport={"width": 1920, "height": 900})
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(BASE + "/?stage=deck", wait_until="load")
    pg.wait_for_timeout(5000)
    steps = []
    for i in range(8):
        pg.click("#fpNextBtn", timeout=5000)
        pg.wait_for_timeout(1100)
        st = pg.evaluate("""() => {
          const vis = [...document.querySelectorAll('#deckBody article[data-beat]')].filter(a => a.getBoundingClientRect().height > 0).map(a => a.getAttribute('data-beat'));
          return {deck: window.__fpStage ? window.__fpStage.state.deck : null, visibleBeats: vis,
                  nextLabel: document.querySelector('#fpNextBtn').textContent.trim()};
        }""")
        steps.append(st)
    out["steps"] = steps
    out["errors"] = errs
    beat9 = pg.evaluate("""() => {
      const art = document.querySelector('#deckBody article[data-beat="9"]');
      const img = art ? art.querySelector('figure.lb-showcase img') : null;
      const b = img ? img.getBoundingClientRect() : null;
      return {artVisible: art ? art.getBoundingClientRect().height > 0 : false,
              imgSrc: img ? img.getAttribute('src').slice(0, 130) : null,
              imgRect: b ? {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height)} : null,
              nextBtn2Visible: !!document.querySelector('#fpNextBtn2') && !document.querySelector('#fpNextBtn2').hidden,
              nextBtn2Text: document.querySelector('#fpNextBtn2') ? document.querySelector('#fpNextBtn2').textContent.trim() : null};
    }""")
    out["beat9"] = beat9
    pg.screenshot(path="/tmp/fix2/proof/w4-1920-deck9c.png")
    back = pg.locator("#fpDeckBack")
    out["deckBackAt9"] = {"hidden": back.is_hidden()}
    back.click(timeout=5000)
    pg.wait_for_timeout(1500)
    out["afterBack"] = pg.evaluate("() => document.querySelector('#fpAgreement').className")
    pg.screenshot(path="/tmp/fix2/proof/deckback-1920-bridge9.png")
    ctx.close()
    br.close()

print(json.dumps(out, indent=1))
with open("/tmp/fix2/proof/results4.json", "w") as f:
    json.dump(out, f, indent=1)
