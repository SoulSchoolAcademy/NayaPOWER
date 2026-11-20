"""Fix-6 staged regression D (Chromium 1920 via localhost forwarder): Ask Naya button + back-button."""
from playwright.sync_api import sync_playwright

BASE = ("https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/"
        "personal-page-complete-20261113/personal-complete.html"
        "&ref=personal/frame-round-fix6-20261119"
        "&cb=8fbec9580c078b97d0881f7aa20d8c92ce41d9d6&owner=flagship-personal")
EYE = "/home/hatch/workspace/team-nitro/personal-frame-fix6-20261119/eye"
PROXY = {"server": "http://127.0.0.1:18080"}

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
        browser = p.chromium.launch(headless=True, proxy=PROXY)
        ctx = browser.new_context(viewport={"width": 1920, "height": 1080}, ignore_https_errors=True)
        page = ctx.new_page()
        page.goto(BASE, wait_until="domcontentloaded", timeout=180000)
        page.wait_for_timeout(8000)
        print("modal dismissed:", dismiss_modal(page), flush=True)
        fresh = state(page, "CHROMIUM-FRESH")
        page.screenshot(path=EYE + "/6d-chromium-fresh.png")
        # --- Ask Naya button ---
        ask = page.locator('.hub-obsidian-btn[aria-label="Ask Naya"]')
        print("hub askBtn count:", ask.count(), flush=True)
        bb = ask.first.bounding_box(timeout=8000)
        print("ask box:", bb, flush=True)
        page.mouse.click(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2)
        for t in (2, 5, 10):
            page.wait_for_timeout(2000 if t == 2 else 3000 if t == 5 else 5000)
            room = page.locator(".naya-ask-room").count()
            print(f"@ask+{t}s hash={page.url.split('#')[-1]} room={room} title={page.title()}", flush=True)
        page.screenshot(path=EYE + "/6d-chromium-ask-room.png")
        # --- yield back to feed, then back-button leg ---
        page.mouse.move(960, 500)
        for _ in range(3):
            page.mouse.wheel(0, 700)
            page.wait_for_timeout(1000)
        tab = page.get_by_text("PERSONAL", exact=True)
        for i in range(tab.count()):
            try:
                b = tab.nth(i).bounding_box(timeout=4000)
            except Exception:
                b = None
            if b and 0 <= b["x"] <= 1900 and 0 <= b["y"] <= 1040:
                page.mouse.click(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
                print(f"tapped PERSONAL tab [{i}]", flush=True)
                break
        page.wait_for_timeout(4000)
        print(f"after PERSONAL: room={page.locator('.naya-ask-room').count()} hash={page.url.split('#')[-1]}", flush=True)
        page.mouse.wheel(0, 5000)
        page.wait_for_timeout(1500)
        page.mouse.wheel(0, 5000)
        page.wait_for_timeout(1500)
        loc = page.get_by_text("WORLDS", exact=True)
        print("WORLDS count:", loc.count(), flush=True)
        loc.first.click(timeout=60000)
        print("tapped WORLDS", flush=True)
        try:
            page.wait_for_url("**nayanet.app/space**", timeout=90000)
            print("landed on space", flush=True)
        except Exception:
            print("did not land on /space, url=", page.url[:120], flush=True)
        page.wait_for_timeout(4000)
        page.go_back()
        page.wait_for_timeout(6000)
        print("modal dismissed after back:", dismiss_modal(page), flush=True)
        page.wait_for_timeout(3000)
        after = state(page, "CHROMIUM-AFTER-BACK")
        page.screenshot(path=EYE + "/6d-chromium-after-back.png")
        page.wait_for_timeout(10000)
        after15 = state(page, "CHROMIUM-AFTER-BACK-15s")
        page.screenshot(path=EYE + "/6d-chromium-after-back-15s.png")
        print(f"SUMMARY chromium fresh={fresh} after-back={after} after-15s={after15}", flush=True)
        browser.close()

main()
