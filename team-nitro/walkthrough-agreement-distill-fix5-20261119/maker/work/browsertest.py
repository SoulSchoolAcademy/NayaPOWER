from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    try:
        b = pw.firefox.launch(headless=True)
        pg = b.new_page(viewport={"width":390,"height":844})
        pg.goto("about:blank")
        print("FIREFOX ALIVE", pg.evaluate("() => 1+1"))
        b.close()
    except Exception as e:
        print("FIREFOX DEAD", str(e)[:300])
