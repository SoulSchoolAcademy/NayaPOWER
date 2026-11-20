"""Fix-6 staged regression: Settings gear (locator click, auto scroll-into-view)
-> 'Home Hub & install' tab (locator click) -> 'Go to Home Hub' link."""
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
        print("modal dismissed:", dismiss_modal(page), flush=True)
        gear = page.locator("#settingsbtn")
        print("settingsbtn count:", gear.count(), flush=True)
        try:
            gear.click(timeout=15000)
            print("gear clicked via locator", flush=True)
        except Exception as e:
            print("gear locator click failed:", str(e)[:200], flush=True)
        page.wait_for_timeout(4000)
        print("after gear hash:", page.url.split('#')[-1], flush=True)
        page.screenshot(path=EYE + "/6s-settings.png")
        tab6 = page.get_by_role("button", name="Home Hub & install")
        print("tab6 count:", tab6.count(), flush=True)
        if tab6.count():
            try:
                tab6.click(timeout=15000)
                print("tab6 clicked via locator", flush=True)
            except Exception as e:
                print("tab6 click failed:", str(e)[:200], flush=True)
            page.wait_for_timeout(3000)
            page.screenshot(path=EYE + "/6s-settings-tab6.png")
            link = page.locator("a[href='https://nayanet.app/hub#/hub']")
            print("home-hub link count:", link.count(), flush=True)
            if link.count():
                try:
                    link.first.click(timeout=15000)
                    print("home-hub link clicked via locator", flush=True)
                except Exception as e:
                    print("link click failed:", str(e)[:200], flush=True)
                try:
                    page.wait_for_url("**nayanet.app/hub**", timeout=30000)
                    print("HUB LANDING:", page.url, flush=True)
                except Exception:
                    print("did not land on hub; url=", page.url[:120], flush=True)
                page.wait_for_timeout(3000)
                page.screenshot(path=EYE + "/6s-hub-landing.png")
        browser.close()

main()
