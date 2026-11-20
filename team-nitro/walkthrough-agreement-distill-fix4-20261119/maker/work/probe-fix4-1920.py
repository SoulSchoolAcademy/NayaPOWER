#!/usr/bin/env python3
"""Fix-4b: 1920 spot regression — identity paired + name-only + door hold."""
import json
from playwright.sync_api import sync_playwright
BASE = "https://naya-walk-beginning-staging.nayapower.workers.dev"
with sync_playwright() as pw:
    b = pw.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1920, "height": 1080})
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.goto(BASE + "/identity.html?name=Shawn&alias=Shawn", timeout=60000)
    pg.wait_for_timeout(6000)
    print("1920-paired", json.dumps(pg.evaluate("""() => {
      const R = el => { if (!el) return null; const r = el.getBoundingClientRect();
        return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
      const ov = (a,b) => { if (!a||!b) return 0; const x=Math.max(0,Math.min(a[2],b[2])-Math.max(a[0],b[0])); const y=Math.max(0,Math.min(a[3],b[3])-Math.max(a[1],b[1])); return Math.round(x*y); };
      const name = document.getElementById('displayName');
      const title = document.querySelector('.cert-title');
      const line = document.querySelector('.cert-certifies');
      return {input: document.getElementById('aliasInput').value, hero: name.textContent,
        dataText: name.getAttribute('data-text'), plaque: document.querySelector('.cert-plaque').className,
        nameRect: R(name), titleRect: R(title), lineDisplay: getComputedStyle(line).display,
        nameTitleOv: ov(R(name), R(title)), nameLineOv: ov(R(name), R(line))}; }""")), flush=True)
    pg.goto(BASE + "/identity.html?name=Shawn", timeout=60000)
    pg.wait_for_timeout(4000)
    print("1920-name-only", json.dumps(pg.evaluate("() => { const n = document.getElementById('displayName'); const i = document.getElementById('aliasInput'); return {input: i.value, hero: n.textContent, hidden: n.hidden}; }")), flush=True)
    ctx.close()
    ctx = b.new_context(viewport={"width": 1920, "height": 1080})
    pg = ctx.new_page()
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.goto(BASE + "/welcome?name=FixFour&alias=fix4door7x", timeout=60000)
    pg.wait_for_timeout(4000)
    pg.wait_for_timeout(10000)
    print("1920-door-hold", pg.evaluate("() => [...document.querySelectorAll('.p3-step')].filter(s => !s.hidden).map(s => s.id)"), flush=True)
    pg.locator("#doorContinue").click(timeout=6000)
    pg.wait_for_timeout(1200)
    print("1920-door-continue", pg.evaluate("() => [...document.querySelectorAll('.p3-step')].filter(s => !s.hidden).map(s => s.id)"), flush=True)
    ctx.close(); b.close()
    print("1920 console errors:", len(errs), errs[:3])
