"""Fix-6 staged regression E4 (Firefox 390, is_mobile): (1) Back closes the Ask room at 390;
(2) back-button return via 'Go to the Hub' from a FRESH page (fix-5 phone_back3 method)."""
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

def markers(page):
    t = page.locator("body").inner_text()
    return {
        "controls": page.locator("button, a, input, select").count(),
        "quote": "NayaNET" in t,
        "name": "Shawn Vibert" in t,
        "empty": "Nothing here yet." in t,
    }

def main():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        # --- (1) Back closes the Ask room at 390 ---
        ctx = browser.new_context(viewport={"width": 390, "height": 844},
                                  is_mobile=True, has_touch=True)
        page = ctx.new_page()
        page.goto(BASE, wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(9000)
        dismiss_modal(page)
        page.wait_for_timeout(3000)
        ask = page.locator('.hub-obsidian-btn[aria-label="Ask Naya"]')
        for step in range(8):
            bb = ask.first.bounding_box(timeout=3000)
            if bb and 0 <= bb["y"] <= 800:
                page.mouse.click(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2)
                break
            page.mouse.move(195, 400)
            page.mouse.wheel(0, 400)
            page.wait_for_timeout(1000)
        page.wait_for_timeout(5000)
        print(f"(1) room open: {page.locator('.naya-ask-room').count()} hash={page.url.split('#')[-1] if '#' in page.url else '(none)'}", flush=True)
        page.go_back()
        page.wait_for_timeout(5000)
        print(f"(1) after browser Back: room={page.locator('.naya-ask-room').count()} hash={page.url.split('#')[-1] if '#' in page.url else '(none)'} markers={markers(page)}", flush=True)
        page.screenshot(path=EYE + "/6e4-phone-room-back.png")
        ctx.close()

        # --- (2) back-button return via 'Go to the Hub' from fresh ---
        ctx = browser.new_context(viewport={"width": 390, "height": 844},
                                  is_mobile=True, has_touch=True)
        page = ctx.new_page()
        page.goto(BASE, wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(9000)
        dismiss_modal(page)
        page.wait_for_timeout(3000)
        print("(2) fresh 390:", markers(page), flush=True)
        go = page.get_by_text("Go to the Hub", exact=False)
        print("(2) 'Go to the Hub' matches:", go.count(), flush=True)
        tapped = False
        for step in range(6):
            for i in range(go.count()):
                try:
                    bb = go.nth(i).bounding_box(timeout=3000)
                except Exception:
                    bb = None
                print(f"  step {step} hub btn [{i}] box={bb}", flush=True)
                if bb and 0 <= bb["y"] <= 800:
                    page.mouse.click(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2)
                    print("(2) tapped Go to the Hub", flush=True)
                    tapped = True
                    break
            if tapped:
                break
            page.mouse.move(195, 400)
            page.mouse.wheel(0, 400)
            page.wait_for_timeout(1000)
        if tapped:
            try:
                page.wait_for_url("**nayanet.app/hub**", timeout=60000)
                print("(2) HUB LANDING:", page.url, flush=True)
            except Exception:
                print("(2) no hub landing; url=", page.url[:110], flush=True)
            page.wait_for_timeout(3000)
            page.go_back()
            page.wait_for_timeout(5000)
            print("(2) after Back 390 @5s:", markers(page), flush=True)
            page.screenshot(path=EYE + "/6e4-phone-after-back.png")
            page.wait_for_timeout(10000)
            print("(2) after Back 390 @15s:", markers(page), flush=True)
            page.screenshot(path=EYE + "/6e4-phone-after-back-15s.png")
        else:
            print("(2) Go to the Hub never became tappable at 390", flush=True)
        browser.close()

main()
