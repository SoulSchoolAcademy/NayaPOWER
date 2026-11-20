# CHECKER leg 6c (REDO) — Settings → tab 7 via raw mouse click at the tab centre,
# verify "Step 7 of 7" text, then click the "Go to Home Hub →" link (height>40 match).
from playwright.sync_api import sync_playwright

URL = "https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/frame-round-fix6-20261119&cb=8fbec9580c078b97d0881f7aa20d8c92ce41d9d6&owner=flagship-personal"
OUT = "/home/hatch/workspace/team-nitro/personal-frame-fix6-20261119/checker/"

def dismiss_install(page):
    for _ in range(10):
        try:
            if page.locator("#naya-install-overlay.show").count() == 0:
                return True
            try:
                page.get_by_text("Not now", exact=True).click(timeout=10000)
            except Exception:
                page.get_by_text("Not now", exact=True).click(timeout=5000, force=True)
        except Exception:
            pass
        page.wait_for_timeout(1000)
    return page.locator("#naya-install-overlay.show").count() == 0

with sync_playwright() as p:
    b = p.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1920, "height": 1080})
    page = ctx.new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(9000)
    print("modal dismissed:", dismiss_install(page), flush=True)
    page.wait_for_timeout(3000)
    page.locator("#settingsbtn").click(timeout=15000)
    page.wait_for_timeout(5000)
    print("after gear hash:", page.url.split("#")[-1], flush=True)
    tab = page.get_by_role("button", name="Home Hub & install")
    print("tab count:", tab.count(), flush=True)
    for attempt in range(3):
        bb = tab.first.bounding_box(timeout=15000)
        print(f"tab box attempt {attempt}: {bb}", flush=True)
        page.mouse.click(bb["x"] + bb["width"]/2, bb["y"] + bb["height"]/2)
        page.wait_for_timeout(3000)
        step = page.get_by_text("Step 7 of 7", exact=False).count()
        print(f"after tab click {attempt}: 'Step 7 of 7' matches={step}", flush=True)
        if step:
            break
    page.screenshot(path=OUT + "c6c-settings-tab6.png")
    txt = page.get_by_text("Go to Home Hub", exact=False)
    print("text matches:", txt.count(), flush=True)
    clicked = False
    for i in range(txt.count()):
        try: lb = txt.nth(i).bounding_box(timeout=4000)
        except Exception: lb = None
        print(f"  text [{i}] box={lb}", flush=True)
        if lb and lb["height"] > 40 and 0 <= lb["x"] <= 1800 and 0 <= lb["y"] <= 1040:
            page.mouse.click(lb["x"] + lb["width"]/2, lb["y"] + lb["height"]/2)
            print(f"mouse-clicked text [{i}] at ({lb['x']+lb['width']/2:.0f},{lb['y']+lb['height']/2:.0f})", flush=True)
            clicked = True
            break
    print("clicked:", clicked, flush=True)
    try:
        page.wait_for_url("**nayanet.app/hub**", timeout=30000)
        print("HUB LANDING:", page.url, flush=True)
    except Exception:
        print("did not land on hub; url=", page.url[:140], flush=True)
    page.wait_for_timeout(3000)
    page.screenshot(path=OUT + "c6c-hub-landing.png")
    print("SETTINGS→HUB:", "PASS" if page.url.startswith("https://nayanet.app/hub") else "FAIL", flush=True)
    print("LEG6C DONE", flush=True)
    b.close()
