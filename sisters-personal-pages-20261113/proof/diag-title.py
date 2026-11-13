from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    br = pw.firefox.launch()
    for label, url in [("STAGED biz", "http://127.0.0.1:8901/pages/sophia/sophias-lessons"),
                       ("STAGED space", "http://127.0.0.1:8901/pages/sophia/the-learning-circle"),
                       ("STAGED personal", "http://127.0.0.1:8901/pages/sophia/sophia")]:
        ctx = br.new_context(viewport={"width": 1440, "height": 900})
        pg = ctx.new_page()
        pg.goto(url, wait_until="domcontentloaded")
        pg.wait_for_selector("#pname", timeout=20000)
        pg.wait_for_timeout(6000)
        print(label, "| os-story-title:", repr(pg.locator("#os-story-title").inner_text()), "| kind:", pg.evaluate("window.MSHIP_PAGE_KIND"))
        ctx.close()
    br.close()
print("DIAG DONE")
