from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b = pw.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width":390,"height":844}, device_scale_factor=2)
    pg = ctx.new_page()
    pg.goto("http://127.0.0.1:18093/", timeout=60000)
    pg.wait_for_timeout(3000)
    print(pg.evaluate("""() => {
      const f = document.querySelector('#fpLegal');
      const n = document.querySelector('#fpLegal .fp-legal-links');
      const cs = el => { const c = getComputedStyle(el); return {display: c.display, vis: c.visibility}; };
      return {bodyClass: document.body.className, htmlClass: document.documentElement.className,
        fpLegal: f ? cs(f) : 'MISSING', nav: n ? cs(n) : 'MISSING',
        navRect: n ? JSON.stringify(n.getBoundingClientRect()) : null,
        stage: document.body.getAttribute('data-stage')};
    }"""))
    # scroll to bottom and re-check
    pg.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    pg.wait_for_timeout(1500)
    print(pg.evaluate("""() => {
      const n = document.querySelector('#fpLegal .fp-legal-links');
      const r = n.getBoundingClientRect();
      return {bodyClass: document.body.className, navRect: [Math.round(r.left),Math.round(r.top),Math.round(r.right),Math.round(r.bottom)], scrollW: n.scrollWidth, clientW: n.clientWidth, justify: getComputedStyle(n).justifyContent, wrap: getComputedStyle(n).flexWrap};
    }"""))
    b.close()
print("DIAG DONE")
