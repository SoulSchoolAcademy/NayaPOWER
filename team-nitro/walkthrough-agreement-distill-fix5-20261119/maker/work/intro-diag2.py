from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b = pw.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width":390,"height":844}, device_scale_factor=2)
    pg = ctx.new_page()
    for url in ["http://127.0.0.1:18093/?stage=intro", "http://127.0.0.1:18093/?stage=bridge"]:
        pg.goto(url, timeout=60000)
        pg.wait_for_timeout(3000)
        print(url, pg.evaluate("""() => {
          const n = document.querySelector('#fpLegal .fp-legal-links');
          const r = n.getBoundingClientRect();
          return {bodyClass: document.body.className, navRect: [Math.round(r.left),Math.round(r.top),Math.round(r.right),Math.round(r.bottom)], scrollW: n.scrollWidth, clientW: n.clientWidth, justify: getComputedStyle(n).justifyContent, wrap: getComputedStyle(n).flexWrap, fpLegalDisplay: getComputedStyle(document.querySelector('#fpLegal')).display};
        }"""))
    b.close()
print("DIAG2 DONE")
