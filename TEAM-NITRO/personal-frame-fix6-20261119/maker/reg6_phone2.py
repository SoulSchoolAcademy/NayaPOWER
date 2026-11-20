"""Fix-6 staged regression E2 (Firefox 390, is_mobile): Ask Naya button (scroll into view),
back via 'Go to the Hub' (scroll into view). Adapted from fix-5 eye phone_back3.py."""
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

def scroll_tap(page, loc, label, max_steps=8):
    """Scroll in steps until a match is in view, then mouse-click its centre."""
    for step in range(max_steps):
        for i in range(loc.count()):
            try:
                bb = loc.nth(i).bounding_box(timeout=3000)
            except Exception:
                bb = None
            print(f"  {label} step {step} [{i}] box={bb}", flush=True)
            if bb and 0 <= bb["y"] <= 800 and 0 <= bb["x"] <= 380:
                page.mouse.click(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2)
                print(f"tapped {label} [{i}]", flush=True)
                return True
        page.mouse.move(195, 400)
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(1000)
    print(f"{label} never became tappable at 390", flush=True)
    return False

def main():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 390, "height": 844},
                                  is_mobile=True, has_touch=True)
        page = ctx.new_page()
        page.goto(BASE, wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(9000)
        dismiss_modal(page)
        page.wait_for_timeout(3000)
        print("fresh 390:", markers(page), flush=True)
        page.screenshot(path=EYE + "/6e2-phone-fresh.png")

        # --- 1. Ask Naya button at 390 ---
        ask = page.locator('.hub-obsidian-btn[aria-label="Ask Naya"]')
        print("hub askBtn count (390):", ask.count(), flush=True)
        if scroll_tap(page, ask, "Ask Naya 390"):
            for t in (2, 5, 10):
                page.wait_for_timeout(2000 if t == 2 else 3000 if t == 5 else 5000)
                h = page.url.split('#')[-1] if '#' in page.url else '(no hash)'
                print(f"@ask+{t}s hash={h} room={page.locator('.naya-ask-room').count()} title={page.title()}", flush=True)
            page.screenshot(path=EYE + "/6e2-phone-ask-room.png")
            # yield via room bottom-bar HOME tile (lands on live portal) is NOT the
            # PERSONAL yield; use the PERSONAL feed tab instead: scroll to tabs.
            page.mouse.move(195, 400)
            for _ in range(3):
                page.mouse.wheel(0, 700)
                page.wait_for_timeout(1000)
            tab = page.get_by_text("PERSONAL", exact=True)
            print("PERSONAL matches (390):", tab.count(), flush=True)
            for i in range(tab.count()):
                try:
                    b = tab.nth(i).bounding_box(timeout=4000)
                except Exception:
                    b = None
                print(f"  tab [{i}] box={b}", flush=True)
                if b and 0 <= b["x"] <= 380 and 0 <= b["y"] <= 820:
                    page.mouse.click(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
                    print(f"tapped PERSONAL tab [{i}] (390)", flush=True)
                    break
            page.wait_for_timeout(4000)
            h = page.url.split('#')[-1] if '#' in page.url else '(no hash)'
            print(f"after PERSONAL (390): room={page.locator('.naya-ask-room').count()} hash={h}", flush=True)

        # --- 2. Back via 'Go to the Hub' at 390 ---
        page.keyboard.press("Home")
        page.wait_for_timeout(2000)
        go = page.get_by_text("Go to the Hub", exact=False)
        print("'Go to the Hub' (partial) matches:", go.count(), flush=True)
        if scroll_tap(page, go, "Go to the Hub 390"):
            try:
                page.wait_for_url("**nayanet.app/hub**", timeout=60000)
                print("HUB LANDING:", page.url, flush=True)
            except Exception:
                print("no hub landing; url=", page.url[:110], flush=True)
            page.wait_for_timeout(3000)
            page.go_back()
            page.wait_for_timeout(5000)
            print("after Back 390 @5s:", markers(page), flush=True)
            page.screenshot(path=EYE + "/6e2-phone-after-back.png")
            page.wait_for_timeout(10000)
            print("after Back 390 @15s:", markers(page), flush=True)
            page.screenshot(path=EYE + "/6e2-phone-after-back-15s.png")
        browser.close()

main()
