# CHECKER leg 6b (REDO) — Settings → "Go to Home Hub →" link itself (anchor whose
# text is exactly that), via the tab's locator click.
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
    gear = page.locator("#settingsbtn")
    print("gear count:", gear.count(), flush=True)
    gear.first.click(timeout=10000)
    page.wait_for_timeout(3000)
    print("after gear hash:", page.url.split("#")[-1], flush=True)
    page.screenshot(path=OUT + "c6b-settings.png")
    tab = page.get_by_role("button", name="Home Hub & install")
    print("tab count:", tab.count(), flush=True)
    tab.first.click(timeout=10000)
    page.wait_for_timeout(3000)
    page.screenshot(path=OUT + "c6b-settings-tab6.png")
    link = page.locator("a", has_text="Go to Home Hub")
    print("Go-to-Home-Hub anchors:", link.count(), flush=True)
    for i in range(link.count()):
        try:
            bb = link.nth(i).bounding_box(timeout=3000)
            print(f"  link[{i}] href={link.nth(i).get_attribute('href')} box={bb}", flush=True)
        except Exception as e:
            print(f"  link[{i}] no box:", str(e)[:80], flush=True)
    # click the one whose text is the link (not the off-canvas twin)
    clicked = False
    for i in range(link.count()):
        try:
            bb = link.nth(i).bounding_box(timeout=5000)
        except Exception:
            bb = None
        if bb and bb["x"] >= 0 and bb["width"] > 0:
            page.mouse.click(bb["x"] + bb["width"]/2, bb["y"] + bb["height"]/2)
            print(f"clicked link[{i}] at ({bb['x']:.0f},{bb['y']:.0f})", flush=True)
            clicked = True
            break
    if not clicked:
        print("no clickable Go-to-Home-Hub link found", flush=True)
    try:
        page.wait_for_url("**nayanet.app/hub**", timeout=30000)
        print("HUB LANDING:", page.url, flush=True)
    except Exception:
        print("did not land on hub; url=", page.url[:140], flush=True)
    page.wait_for_timeout(3000)
    page.screenshot(path=OUT + "c6b-hub-landing.png")
    print("SETTINGS→HUB:", "PASS" if page.url.startswith("https://nayanet.app/hub") else "FAIL", flush=True)
    print("LEG6B DONE", flush=True)
    b.close()
