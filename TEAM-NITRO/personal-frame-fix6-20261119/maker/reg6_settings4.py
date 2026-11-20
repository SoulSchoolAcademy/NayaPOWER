"""Fix-6 staged regression: Settings -> tab 7 -> debug all 'Go to Home Hub' matches, click the in-view one."""
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

def main():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = ctx.new_page()
        page.goto(BASE, wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(8000)
        dismiss_modal(page)
        page.locator("#settingsbtn").click(timeout=15000)
        page.wait_for_timeout(4000)
        page.get_by_role("button", name="Home Hub & install").click(timeout=15000)
        page.wait_for_timeout(3000)
        txt = page.get_by_text("Go to Home Hub", exact=False)
        print("text matches:", txt.count(), flush=True)
        for i in range(txt.count()):
            try:
                lb = txt.nth(i).bounding_box(timeout=4000)
            except Exception as e:
                lb = f"ERR {str(e)[:80]}"
            try:
                tag = txt.nth(i).evaluate("el => el.tagName + '#' + (el.id||'') + '.' + (el.className||'').toString().slice(0,40)") if False else "?"
            except Exception:
                tag = "?"
            print(f"  text [{i}] box={lb}", flush=True)
        page.screenshot(path=EYE + "/6s4-settings-tab6.png")
        # click the in-view one by mouse
        clicked = False
        for i in range(txt.count()):
            try:
                lb = txt.nth(i).bounding_box(timeout=4000)
            except Exception:
                lb = None
            if lb and lb["height"] > 40 and 0 <= lb["x"] <= 1800 and 0 <= lb["y"] <= 1040:
                page.mouse.click(lb["x"] + lb["width"] / 2, lb["y"] + lb["height"] / 2)
                print(f"mouse-clicked text [{i}] at ({lb['x']+lb['width']/2:.0f},{lb['y']+lb['height']/2:.0f})", flush=True)
                clicked = True
                break
        print("clicked:", clicked, flush=True)
        try:
            page.wait_for_url("**nayanet.app/hub**", timeout=30000)
            print("HUB LANDING:", page.url, flush=True)
        except Exception:
            print("did not land on hub; url=", page.url[:120], flush=True)
        page.wait_for_timeout(3000)
        page.screenshot(path=EYE + "/6s4-hub-landing.png")
        browser.close()

main()
