import json
from playwright.sync_api import sync_playwright
URL = "https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/membership-rebuild-20261119/membership-rebuild.html&ref=membership/rebuild-fix8-20261119&cb=b13c17104a188e3b53bbbe77483fd4805afc29f2"
with sync_playwright() as p:
    b = p.firefox.launch(headless=True, executable_path="/home/hatch/.cache/ms-playwright/firefox-1555/firefox/firefox")
    pg = b.new_page(viewport={"width":1920,"height":1080})
    errs=[]
    pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
    pg.goto(URL, wait_until="load", timeout=90000)
    pg.wait_for_timeout(4000)
    try:
        r = pg.evaluate("() => ({title: document.title, h: document.documentElement.scrollHeight, bars: [...document.querySelectorAll('.notif-bar')].map(e=>({id:e.id, disp:getComputedStyle(e).display}))})")
        print("EVALUATE OK:", json.dumps(r))
    except Exception as e:
        print("EVALUATE FAILED:", str(e)[:300])
    pg.screenshot(path="00-smoke-desktop.png")
    print("ERRORS:", errs[:5])
    b.close()
print("SMOKE DONE")
