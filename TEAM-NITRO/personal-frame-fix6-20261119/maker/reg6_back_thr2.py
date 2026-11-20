"""Fix-6 staged regression B2 (Firefox 1920, throttled): WORLDS via raw mouse click at box centre."""
import time
from playwright.sync_api import sync_playwright

BASE = ("https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/"
        "personal-page-complete-20261113/personal-complete.html"
        "&ref=personal/frame-round-fix6-20261119"
        "&cb=8fbec9580c078b97d0881f7aa20d8c92ce41d9d6&owner=flagship-personal")
EYE = "/home/hatch/workspace/team-nitro/personal-frame-fix6-20261119/eye"

def dismiss_modal(page):
    for _ in range(25):
        try:
            if page.locator("#naya-install-overlay.show").count() == 0:
                return True
            page.get_by_text("Not now", exact=True).click(timeout=2000)
        except Exception:
            pass
        page.wait_for_timeout(1000)
    return page.locator("#naya-install-overlay.show").count() == 0

def state(page, label):
    controls = page.locator("button, a, input, [role=button]").count()
    markers = {}
    for name, sel in [
        ("quote", "text=NayaNET — create, learn and grow together"),
        ("tabs-personal", "text=PERSONAL"),
        ("empty-state", "text=Nothing here yet."),
        ("ask-naya", "text=Ask Naya"),
        ("profile-name", "text=Shawn Vibert"),
    ]:
        try:
            markers[name] = page.locator(sel).first.is_visible()
        except Exception:
            markers[name] = "ERR"
    print(f"[{label}] controls={controls} markers={markers}", flush=True)
    return controls

def main():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = ctx.new_page()
        def slow(route):
            time.sleep(0.25)
            route.continue_()
        page.route("**/*", slow)
        t0 = time.time()
        page.goto(BASE, wait_until="domcontentloaded", timeout=180000)
        print(f"throttled domcontentloaded in {time.time()-t0:.1f}s", flush=True)
        page.wait_for_timeout(8000)
        print("modal dismissed:", dismiss_modal(page), flush=True)
        page.wait_for_timeout(3000)
        fresh = state(page, "THROTTLED-FRESH")
        page.screenshot(path=EYE + "/6b2-throttled-fresh.png")
        page.mouse.wheel(0, 5000)
        page.wait_for_timeout(1500)
        page.mouse.wheel(0, 5000)
        page.wait_for_timeout(1500)
        loc = page.get_by_text("WORLDS", exact=True)
        loc.first.click(timeout=120000)
        print("tapped WORLDS via locator (120s timeout)", flush=True)
        try:
            page.wait_for_url("**nayanet.app/space**", timeout=120000)
            print("landed on space", flush=True)
        except Exception:
            print("did not land on /space, url=", page.url[:120], flush=True)
        page.wait_for_timeout(4000)
        page.go_back()
        page.wait_for_timeout(6000)
        print("modal dismissed after back:", dismiss_modal(page), flush=True)
        page.wait_for_timeout(3000)
        after = state(page, "THROTTLED-AFTER-BACK")
        page.screenshot(path=EYE + "/6b2-throttled-after-back.png")
        page.wait_for_timeout(10000)
        after15 = state(page, "THROTTLED-AFTER-BACK-15s")
        page.screenshot(path=EYE + "/6b2-throttled-after-back-15s.png")
        print(f"SUMMARY throttled fresh={fresh} after-back={after} after-15s={after15}", flush=True)
        browser.close()

main()
