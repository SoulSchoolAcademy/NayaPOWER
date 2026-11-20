import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    for name in ("firefox", "chromium"):
        try:
            b = p.firefox.launch() if name=="firefox" else p.chromium.launch(args=["--no-sandbox"], proxy={"server":"http://127.0.0.1:18080"})
            pg = b.new_page(viewport={"width":390,"height":844})
            pg.set_content("<h1>hi</h1>", wait_until="load")
            print(name, "OK", pg.evaluate("() => document.title"))
            b.close()
        except Exception as e:
            print(name, "DEAD:", str(e)[:300])
