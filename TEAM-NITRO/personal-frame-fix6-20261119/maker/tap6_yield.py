"""Fix-6 LOCAL: open room via Ask Naya button, scroll to PERSONAL feed tab, tap -> must yield."""
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
        dismiss_modal(page)
        ask = page.get_by_role("button", name="Ask Naya")
        bb = ask.bounding_box(timeout=8000)
        page.mouse.click(bb["x"] + bb["width"]/2, bb["y"] + bb["height"]/2)
        page.wait_for_timeout(4000)
        print("room open via button:", page.locator(".naya-ask-room").count(), "hash:", page.url.split('#')[-1], flush=True)
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
                page.mouse.click(b["x"] + b["width"]/2, b["y"] + b["height"]/2)
                print(f"tapped PERSONAL tab [{i}]", flush=True)
                tapped = True
                break
        if not tapped:
            print("no in-view PERSONAL tab", flush=True)
        page.wait_for_timeout(4000)
        print("after PERSONAL tab: room=", page.locator(".naya-ask-room").count(), "hash:", page.url.split('#')[-1], flush=True)
        page.screenshot(path=EYE + "/L6-yield-after-tab.png")
        browser.close()

main()
