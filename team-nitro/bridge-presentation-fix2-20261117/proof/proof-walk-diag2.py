#!/usr/bin/env python3
"""Diagnose the true step: which step section is visible after answering Q1,
and whether the answer persisted in localStorage. (Firefox fallback: both
Chromium builds SIGTRAP on launch in this VM as of ~23:24Z.)"""
import json
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8899"
out = {}

with sync_playwright() as p:
    br = p.firefox.launch(
        proxy={"server": "http://127.0.0.1:18080", "bypass": "127.0.0.1,localhost"})
    ctx = br.new_context(viewport={"width": 635, "height": 900})
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(BASE + "/welcome?name=Diag2&alias=diagwalk2", wait_until="load")
    pg.wait_for_timeout(6000)
    def vis_steps():
        return pg.evaluate("""() => {
          const secs = [...document.querySelectorAll('[id^="step-"]')].map(s => {
            const b = s.getBoundingClientRect();
            return {id: s.id, vis: b.height > 0, h: Math.round(b.height)};
          }).filter(x => x.vis);
          return {visibleSections: secs};
        }""")
    out["before"] = vis_steps()
    pg.click("#answer-1", timeout=3000)
    pg.keyboard.type("I am Diag2, a tester.", delay=25)
    pg.wait_for_timeout(500)
    out["typedValue"] = pg.evaluate("() => document.querySelector('#answer-1').value")
    out["lsBefore"] = pg.evaluate("() => Object.keys(localStorage)")
    pg.click("#enterBtn-1", timeout=3000)
    pg.wait_for_timeout(2000)
    out["afterEnter"] = vis_steps()
    out["lsAfter"] = pg.evaluate("() => Object.keys(localStorage).map(k => [k, (localStorage.getItem(k)||'').slice(0,200)]))")
    out["enterNote"] = pg.evaluate("""() => {
      const n = document.querySelector('#enterNote-1');
      return n ? {hidden: n.hidden, text: n.textContent.trim().slice(0,120)} : null;
    }""")
    out["errors"] = errs
    pg.screenshot(path="/tmp/fix2/proof/diag-walk2.png")
    ctx.close()
    br.close()

print(json.dumps(out, indent=1))
