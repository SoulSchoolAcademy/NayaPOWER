#!/usr/bin/env python3
"""Re-check: does welcome-0.jpg error again on a fresh deck load?"""
from playwright.sync_api import sync_playwright
errs = []
with sync_playwright() as pw:
    b = pw.firefox.launch(headless=True)
    for url in ["/?stage=deck", "/?stage=letter", "/agreement"]:
        ctx = b.new_context(viewport={"width": 390, "height": 844})
        pg = ctx.new_page()
        pg.on("console", lambda m: errs.append((url, m.type, m.text[:160])) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append((url, "pageerror", str(e)[:160])))
        pg.goto("https://naya-walk-beginning-staging.nayapower.workers.dev" + url, timeout=60000)
        pg.wait_for_timeout(8000)
        # check the welcome-0 img element state
        st = pg.evaluate("""() => { const im = [...document.querySelectorAll('img')].find(i => (i.src||'').includes('welcome-0.jpg')); return im ? {complete: im.complete, naturalWidth: im.naturalWidth} : 'not-in-dom'; }""")
        print(url, "img:", st, flush=True)
        ctx.close()
    b.close()
print("console errors:", len(errs))
for e in errs: print(e)
