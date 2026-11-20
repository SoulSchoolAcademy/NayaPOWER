#!/usr/bin/env python3
"""Diagnose the walk answer wiring: enumerate visionin textareas, Enter
buttons, and test each submit path on Q1 with state inspection."""
import json
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8899"
out = {}

with sync_playwright() as p:
    br = p.chromium.launch(
        proxy={"server": "http://127.0.0.1:18080", "bypass": "127.0.0.1,localhost"},
        args=["--no-sandbox"])
    ctx = br.new_context(viewport={"width": 635, "height": 900})
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(BASE + "/welcome?name=Diag&alias=diagwalk1", wait_until="load")
    pg.wait_for_timeout(6000)
    out["visionin"] = pg.evaluate("""() => {
      return [...document.querySelectorAll('textarea.visionin')].map((ta, i) => {
        const b = ta.getBoundingClientRect();
        const sec = ta.closest('section, [data-step], div[id^="step"], div[id^="q"]');
        return {i, id: ta.id, vis: b.height > 0 && b.width > 0,
                readonly: ta.readOnly, disabled: ta.disabled,
                x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height),
                sec: sec ? (sec.id || sec.className.slice(0,40)) : null,
                placeholder: (ta.placeholder||'').slice(0,40)};
      });
    }""")
    out["enterBtns"] = pg.evaluate("""() => {
      return [...document.querySelectorAll('.p3-enter')].filter(e => /Enter/.test(e.textContent)).map(e => {
        const b = e.getBoundingClientRect();
        return {id: e.id, vis: b.height > 0, x: Math.round(b.x), y: Math.round(b.y)};
      });
    }""")
    out["choiceTexts"] = pg.evaluate("""() => {
      return [...document.querySelectorAll('.p3-choice-text')].slice(0,6).map(ta => {
        const b = ta.getBoundingClientRect();
        return {id: ta.id, vis: b.height > 0, readonly: ta.readOnly,
                val: (ta.value||'').slice(0,30)};
      });
    }""")
    # Path A: type into the VISIBLE visionin with real keystrokes, then click #enterBtn-1
    vis = [t for t in out["visionin"] if t["vis"]]
    out["visibleVisioninCount"] = len(vis)
    if vis:
        sel = f"#{vis[0]['id']}" if vis[0]["id"] else "textarea.visionin >> visible=true"
        pg.click(sel, timeout=3000)
        pg.keyboard.type("I am Diag, a tester.", delay=30)
        pg.wait_for_timeout(600)
        out["afterType"] = pg.evaluate("""() => {
          const notes = [...document.querySelectorAll('.p3-note')].filter(n => !n.hidden).map(n => n.textContent.trim().slice(0,100));
          const ta = document.querySelector('textarea.visionin:not([hidden])');
          return {notes, q: (document.querySelector('.p3-question')||{}).textContent};
        }""")
        pg.click("#enterBtn-1", timeout=3000)
        pg.wait_for_timeout(1500)
        out["afterEnterBtn"] = pg.evaluate("() => ({q: (document.querySelector('.p3-question')||{}).textContent, body: document.body.className})")
    out["errors"] = errs
    pg.screenshot(path="/tmp/fix2/proof/diag-walk.png")
    ctx.close()
    br.close()

print(json.dumps(out, indent=1))
