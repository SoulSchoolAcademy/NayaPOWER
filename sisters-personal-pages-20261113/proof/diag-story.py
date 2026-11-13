from playwright.sync_api import sync_playwright
JS = """() => {
  const heads = [...document.querySelectorAll('.ib-layer-head b')].map(b => b.textContent.trim());
  return {
    heads: heads.slice(0, 8),
    mshipKind: window.MSHIP_PAGE_KIND,
    pageAlias: window.PAGE_ALIAS,
    storyB: (() => { const els=[...document.querySelectorAll('b')].filter(b=>/story/i.test(b.textContent)); return els.map(e=>e.textContent.trim()); })(),
  };
}"""
with sync_playwright() as pw:
    br = pw.firefox.launch()
    for label, url in [("STAGED biz", "http://127.0.0.1:8901/pages/sophia/sophias-lessons"),
                       ("LIVE biz", "https://nayanet.app/business")]:
        ctx = br.new_context(viewport={"width": 1440, "height": 900})
        pg = ctx.new_page()
        pg.goto(url, wait_until="domcontentloaded")
        pg.wait_for_selector("#pname", timeout=20000)
        pg.wait_for_timeout(6000)
        print(f"--- {label} (before About) ---")
        print("MSHIP_PAGE_KIND:", pg.evaluate("window.MSHIP_PAGE_KIND"), "| PAGE_ALIAS:", pg.evaluate("window.PAGE_ALIAS"))
        pg.locator(".up-act", has_text="About").first.click()
        pg.wait_for_timeout(1500)
        print("after About 1.5s:", pg.evaluate(JS))
        pg.wait_for_timeout(5000)
        print("after About 6.5s:", pg.evaluate(JS))
        ctx.close()
    br.close()
print("DIAG DONE")
