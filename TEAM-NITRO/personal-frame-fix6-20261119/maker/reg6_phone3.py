"""Fix-6 staged regression E3 (Firefox 390, is_mobile): PERSONAL yield at 390, then
back via 'Go to the Hub' from the yielded feed."""
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
        ctx = browser.new_context(viewport={"width": 390, "height": 844},
                                  is_mobile=True, has_touch=True)
        page = ctx.new_page()
        page.goto(BASE, wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(9000)
        dismiss_modal(page)
        page.wait_for_timeout(3000)
        print("fresh 390:", markers(page), flush=True)
        # open room via Ask (scroll into view first)
        ask = page.locator('.hub-obsidian-btn[aria-label="Ask Naya"]')
        for step in range(8):
            bb = ask.first.bounding_box(timeout=3000)
            if bb and 0 <= bb["y"] <= 800:
                page.mouse.click(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2)
                print(f"tapped Ask Naya 390 at step {step}", flush=True)
                break
            page.mouse.move(195, 400)
            page.mouse.wheel(0, 400)
            page.wait_for_timeout(1000)
        page.wait_for_timeout(5000)
        print(f"room open: {page.locator('.naya-ask-room').count()} hash={page.url.split('#')[-1] if '#' in page.url else '(none)'}", flush=True)
        # hunt the PERSONAL feed tab: small scroll steps, probe box each step
        tab = page.get_by_text("PERSONAL", exact=True)
        print("PERSONAL matches:", tab.count(), flush=True)
        tapped = False
        for step in range(12):
            for i in range(tab.count()):
                try:
                    b = tab.nth(i).bounding_box(timeout=3000)
                except Exception:
                    b = None
                print(f"  yield step {step} tab [{i}] box={b}", flush=True)
                if b and 0 <= b["x"] <= 380 and 0 <= b["y"] <= 820:
                    page.mouse.click(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
                    print(f"tapped PERSONAL tab [{i}] at step {step}", flush=True)
                    tapped = True
                    break
            if tapped:
                break
            page.mouse.move(195, 400)
            page.mouse.wheel(0, 300)
            page.wait_for_timeout(800)
        page.wait_for_timeout(4000)
        print(f"after PERSONAL (390): room={page.locator('.naya-ask-room').count()} hash={page.url.split('#')[-1] if '#' in page.url else '(none)'}", flush=True)
        page.screenshot(path=EYE + "/6e3-phone-yield.png")
        # back leg from the yielded feed
        if page.locator(".naya-ask-room").count() == 0:
            page.keyboard.press("Home")
            page.wait_for_timeout(2000)
            go = page.get_by_text("Go to the Hub", exact=False)
            print("'Go to the Hub' matches:", go.count(), flush=True)
            hit = False
            for step in range(8):
                for i in range(go.count()):
                    try:
                        b = go.nth(i).bounding_box(timeout=3000)
                    except Exception:
                        b = None
                    print(f"  hub step {step} [{i}] box={b}", flush=True)
                    if b and 0 <= b["y"] <= 800 and 0 <= b["x"] <= 380:
                        page.mouse.click(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
                        print(f"tapped Go to the Hub [{i}] at step {step}", flush=True)
                        hit = True
                        break
                if hit:
                    break
                page.mouse.move(195, 400)
                page.mouse.wheel(0, 400)
                page.wait_for_timeout(1000)
            if hit:
                try:
                    page.wait_for_url("**nayanet.app/hub**", timeout=60000)
                    print("HUB LANDING:", page.url, flush=True)
                except Exception:
                    print("no hub landing; url=", page.url[:110], flush=True)
                page.wait_for_timeout(3000)
                page.go_back()
                page.wait_for_timeout(5000)
                print("after Back 390 @5s:", markers(page), flush=True)
                page.screenshot(path=EYE + "/6e3-phone-after-back.png")
                page.wait_for_timeout(10000)
                print("after Back 390 @15s:", markers(page), flush=True)
                page.screenshot(path=EYE + "/6e3-phone-after-back-15s.png")
        browser.close()

main()
