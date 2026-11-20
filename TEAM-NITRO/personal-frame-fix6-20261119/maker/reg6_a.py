"""Fix-6 staged regression A (Firefox 1920): Ask Naya button (2 taps), PERSONAL yield,
#people hold, Settings -> Home Hub. Adapted from fix-5 eye regression_e/k."""
from playwright.sync_api import sync_playwright

BASE = ("https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/"
        "personal-page-complete-20261113/personal-complete.html"
        "&ref=personal/frame-round-fix6-20261119"
        "&cb=8fbec9580c078b97d0881f7aa20d8c92ce41d9d6&owner=flagship-personal")
EYE = "/home/hatch/workspace/team-nitro/personal-frame-fix6-20261119/eye"

def dismiss_modal(page):
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

def center_click(page, loc, label, timeout=8000):
    try:
        bb = loc.bounding_box(timeout=timeout)
    except Exception as e:
        print(f"{label}: no box: {str(e)[:120]}", flush=True)
        return False
    if not bb:
        print(f"{label}: empty box", flush=True)
        return False
    print(f"{label}: clicking center ({bb['x']+bb['width']/2:.0f}, {bb['y']+bb['height']/2:.0f})", flush=True)
    page.mouse.click(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2)
    return True

def main():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = ctx.new_page()
        page.goto(BASE, wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(8000)
        print("modal dismissed:", dismiss_modal(page), flush=True)

        # --- 1. Ask Naya button: two real taps ---
        ask = page.get_by_role("button", name="Ask Naya")
        print("ask button count:", ask.count(), flush=True)
        center_click(page, ask, "Ask Naya tap 1")
        for t in (2, 5, 10):
            page.wait_for_timeout(2000 if t == 2 else 3000 if t == 5 else 5000)
            print(f"@tap1+{t}s hash={page.url.split('#')[-1]} room={page.locator('.naya-ask-room').count()} title={page.title()}", flush=True)
        page.screenshot(path=EYE + "/6a-ask-room.png")
        center_click(page, ask, "Ask Naya tap 2")
        page.wait_for_timeout(5000)
        print(f"@tap2+5s hash={page.url.split('#')[-1]} room={page.locator('.naya-ask-room').count()}", flush=True)
        page.screenshot(path=EYE + "/6a-ask-room-2nd.png")

        # --- 2. PERSONAL yield via feed tab (scroll to tabs first) ---
        page.mouse.move(960, 500)
        for _ in range(3):
            page.mouse.wheel(0, 700)
            page.wait_for_timeout(1000)
        tab = page.get_by_text("PERSONAL", exact=True)
        print("PERSONAL matches:", tab.count(), flush=True)
        tapped = False
        for i in range(tab.count()):
            try:
                b = tab.nth(i).bounding_box(timeout=4000)
            except Exception:
                b = None
            print(f"  tab [{i}] box={b}", flush=True)
            if b and 0 <= b["x"] <= 1900 and 0 <= b["y"] <= 1040:
                page.mouse.click(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
                print(f"tapped PERSONAL tab [{i}]", flush=True)
                tapped = True
                break
        page.wait_for_timeout(4000)
        print(f"after PERSONAL: room={page.locator('.naya-ask-room').count()} hash={page.url.split('#')[-1]}", flush=True)
        page.screenshot(path=EYE + "/6a-after-personal-yield.png")

        # --- 3. #people hold ---
        conn = page.get_by_role("button", name="Connections")
        print("connections button count:", conn.count(), flush=True)
        if conn.count():
            center_click(page, conn, "Connections profile button")
            page.wait_for_timeout(4000)
            print("after Connections hash:", page.url.split('#')[-1], flush=True)
            page.mouse.wheel(0, 800)
            page.wait_for_timeout(15000)
            print("after scroll + 15s hash:", page.url.split('#')[-1], flush=True)
            page.screenshot(path=EYE + "/6a-people-hash.png")

        # --- 4. Settings -> Home Hub & install tab -> link ---
        gear = page.locator("#settingsbtn")
        print("settingsbtn count:", gear.count(), flush=True)
        if gear.count():
            center_click(page, gear, "Settings gear #settingsbtn")
            page.wait_for_timeout(4000)
            print("after gear hash:", page.url.split('#')[-1], flush=True)
            tab6 = page.get_by_role("button", name="Home Hub & install")
            print("tab6 count:", tab6.count(), flush=True)
            if tab6.count():
                try:
                    tab6.click(timeout=10000)
                    print("tab6 clicked via locator", flush=True)
                except Exception as e:
                    print("tab6 click failed:", str(e)[:150], flush=True)
                page.wait_for_timeout(3000)
                page.screenshot(path=EYE + "/6a-settings-tab6.png")
                link = page.locator("a[href='https://nayanet.app/hub#/hub']")
                print("home-hub link count:", link.count(), flush=True)
                if link.count():
                    center_click(page, link.first, "Go to Home Hub link")
                    try:
                        page.wait_for_url("**nayanet.app/hub**", timeout=30000)
                        print("HUB LANDING:", page.url, flush=True)
                    except Exception:
                        print("did not land on hub; url=", page.url[:120], flush=True)
                    page.wait_for_timeout(3000)
                    page.screenshot(path=EYE + "/6a-hub-landing.png")
        browser.close()

main()
