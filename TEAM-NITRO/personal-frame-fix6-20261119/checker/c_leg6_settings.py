# CHECKER leg 6 — Settings → "Go to Home Hub →" (Firefox 1920).
from playwright.sync_api import sync_playwright

URL = "https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/frame-round-fix6-20261119&cb=8fbec9580c078b97d0881f7aa20d8c92ce41d9d6&owner=flagship-personal"
OUT = "/home/hatch/workspace/team-nitro/personal-frame-fix6-20261119/checker/"

def dismiss_install(page):
    try:
        btn = page.get_by_role("button", name="Not now")
        if btn.count():
            btn.first.click(timeout=10000, force=True)
    except Exception as e:
        print("install dismiss:", str(e)[:100], flush=True)

with sync_playwright() as p:
    b = p.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1920, "height": 1080})
    page = ctx.new_page()
    page.goto(URL, timeout=120000)
    page.wait_for_timeout(9000); dismiss_install(page); page.wait_for_timeout(3000)
    gear = page.locator("#settingsbtn")
    print("gear count:", gear.count(), flush=True)
    gear.first.click(timeout=10000)
    page.wait_for_timeout(3000)
    print("after gear hash:", page.url.split("#")[-1], flush=True)
    page.screenshot(path=OUT + "c6-settings.png")
    tab = page.get_by_text("Home Hub & install", exact=True)
    print("tab count:", tab.count(), flush=True)
    tab.first.click(timeout=10000)
    page.wait_for_timeout(2000)
    page.screenshot(path=OUT + "c6-settings-tab6.png")
    link = page.get_by_text("Go to Home Hub", exact=False)
    print("Go-to-Home-Hub matches:", link.count(), flush=True)
    # the link is an <a>; prefer an anchor whose href contains nayanet.app/hub
    anchor = page.locator("a[href*='nayanet.app/hub']")
    print("hub anchors:", anchor.count(), flush=True)
    for i in range(anchor.count()):
        try:
            print(f"  anchor[{i}] href={anchor.nth(i).get_attribute('href')} text={anchor.nth(i).inner_text()[:60]!r}", flush=True)
        except Exception as e:
            print(f"  anchor[{i}] unreadable:", str(e)[:80], flush=True)
    # click the anchor inside the settings view (visible one)
    clicked = False
    for i in range(anchor.count()):
        try:
            box = anchor.nth(i).bounding_box(timeout=5000)
            if box and box["x"] >= 0 and box["width"] > 0:
                page.mouse.click(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
                clicked = True
                print(f"clicked anchor[{i}] at", round(box["x"], 1), round(box["y"], 1), flush=True)
                break
        except Exception as e:
            print(f"anchor[{i}] click failed:", str(e)[:100], flush=True)
    page.wait_for_timeout(8000)
    print("after Home Hub click url:", page.url, flush=True)
    page.screenshot(path=OUT + "c6-hub-landing.png")
    print("SETTINGS→HUB:", "PASS" if page.url.startswith("https://nayanet.app/hub") else "FAIL", flush=True)
    print("LEG6 DONE", flush=True)
    b.close()
