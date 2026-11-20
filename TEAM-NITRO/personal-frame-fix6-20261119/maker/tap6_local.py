"""Fix-6 LOCAL pre-file test: tap Ask Naya on the locally served fixed bytes (Firefox 1920)."""
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:18091/personal-complete-fix6.html"
EYE = "/home/hatch/workspace/team-nitro/personal-frame-fix6-20261119/maker"

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

def main():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = ctx.new_page()
        page.goto(BASE, wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(8000)
        print("modal dismissed:", dismiss_modal(page), flush=True)
        ask = page.get_by_role("button", name="Ask Naya")
        print("ask button count:", ask.count(), flush=True)
        bb = ask.bounding_box(timeout=8000)
        print("ask box:", bb, flush=True)
        page.mouse.click(bb["x"] + bb["width"]/2, bb["y"] + bb["height"]/2)
        for t in (2, 5, 10):
            page.wait_for_timeout(2000 if t == 2 else 3000 if t == 5 else 5000)
            room = page.locator(".naya-ask-room").count()
            print(f"@{t}s hash={page.url.split('#')[-1] if '#' in page.url else '(none)'} room={room} title={page.title()}", flush=True)
        page.screenshot(path=EYE + "/L6-ask-room-open.png")
        # PERSONAL yield: tap bottom-bar PERSONAL while room open
        per = page.get_by_text("PERSONAL", exact=True)
        tapped = False
        for i in range(per.count()):
            try:
                b = per.nth(i).bounding_box(timeout=5000)
            except Exception:
                b = None
            if b and b["y"] > 900:
                page.mouse.click(b["x"] + b["width"]/2, b["y"] + b["height"]/2)
                print("tapped bottom-bar PERSONAL", flush=True)
                tapped = True
                break
        if not tapped:
            print("PERSONAL bottom-bar tile NOT tapped", flush=True)
        page.wait_for_timeout(4000)
        print(f"after PERSONAL hash={page.url.split('#')[-1] if '#' in page.url else '(none)'} room={page.locator('.naya-ask-room').count()}", flush=True)
        page.screenshot(path=EYE + "/L6-after-personal-yield.png")
        browser.close()

main()
