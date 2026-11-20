"""Fix-6 staged regression E (Firefox 390x844): Ask Naya button, back via 'Go to the Hub',
Academy popup, composer #home/composer. Adapted from fix-5 eye phone_leg.py."""
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

def state(page, label):
    controls = page.locator("button, a, input, [role=button]").count()
    markers = {}
    for name, sel in [
        ("quote", "text=NayaNET — create, learn and grow together"),
        ("empty-state", "text=Nothing here yet."),
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
        ctx = browser.new_context(viewport={"width": 390, "height": 844})
        page = ctx.new_page()
        page.goto(BASE, wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(8000)
        print("modal dismissed:", dismiss_modal(page), flush=True)
        fresh = state(page, "390-FRESH")
        page.screenshot(path=EYE + "/6e-phone-fresh.png")

        # --- 1. Ask Naya button at 390 ---
        ask = page.locator('.hub-obsidian-btn[aria-label="Ask Naya"]')
        print("hub askBtn count (390):", ask.count(), flush=True)
        try:
            bb = ask.first.bounding_box(timeout=8000)
            print("ask box (390):", bb, flush=True)
            page.mouse.click(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2)
        except Exception as e:
            print("ask tap failed:", str(e)[:150], flush=True)
        for t in (2, 5, 10):
            page.wait_for_timeout(2000 if t == 2 else 3000 if t == 5 else 5000)
            print(f"@ask+{t}s hash={page.url.split('#')[-1]} room={page.locator('.naya-ask-room').count()} title={page.title()}", flush=True)
        page.screenshot(path=EYE + "/6e-phone-ask-room.png")
        # yield back to feed via PERSONAL tab (scroll to tabs)
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
        print(f"after PERSONAL (390): room={page.locator('.naya-ask-room').count()} hash={page.url.split('#')[-1]}", flush=True)

        # --- 2. Back via 'Go to the Hub' ---
        page.keyboard.press("Home")
        page.wait_for_timeout(2000)
        go = page.get_by_text("Go to the Hub", exact=True)
        print("'Go to the Hub' count:", go.count(), flush=True)
        tapped = False
        for i in range(go.count()):
            try:
                b = go.nth(i).bounding_box(timeout=4000)
            except Exception:
                b = None
            print(f"  go [{i}] box={b}", flush=True)
            if b and 0 <= b["y"] <= 820:
                page.mouse.click(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
                print(f"tapped Go to the Hub [{i}]", flush=True)
                tapped = True
                break
        if not tapped:
            # scroll down to reveal the profile buttons, then retry
            for _ in range(4):
                page.mouse.wheel(0, 600)
                page.wait_for_timeout(800)
            for i in range(go.count()):
                try:
                    b = go.nth(i).bounding_box(timeout=4000)
                except Exception:
                    b = None
                if b and 0 <= b["y"] <= 820:
                    page.mouse.click(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
                    print(f"tapped Go to the Hub [{i}] after scroll", flush=True)
                    tapped = True
                    break
        try:
            page.wait_for_url("**nayanet.app/hub**", timeout=60000)
            print("landed on live hub", flush=True)
        except Exception:
            print("did not land on live hub; url=", page.url[:120], flush=True)
        page.wait_for_timeout(4000)
        page.go_back()
        page.wait_for_timeout(5000)
        print("modal dismissed after back:", dismiss_modal(page), flush=True)
        page.wait_for_timeout(3000)
        after = state(page, "390-AFTER-BACK")
        page.screenshot(path=EYE + "/6e-phone-after-back.png")
        page.wait_for_timeout(10000)
        after15 = state(page, "390-AFTER-BACK-15s")
        page.screenshot(path=EYE + "/6e-phone-after-back-15s.png")
        print(f"SUMMARY phone-back fresh={fresh} after-back={after} after-15s={after15}", flush=True)

        # --- 3. Academy popup at 390 ---
        pill = page.locator("a[data-mw-cover='Naya Academy']")
        print("academy pill count (390):", pill.count(), flush=True)
        if pill.count():
            bb = pill.bounding_box(timeout=8000)
            print("academy pill box (390):", bb, flush=True)
            try:
                with page.expect_popup(timeout=15000) as pop:
                    page.mouse.click(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2)
                new_page = pop.value
                new_page.wait_for_timeout(4000)
                print("ACADEMY POPUP URL (390):", new_page.url, flush=True)
                new_page.screenshot(path=EYE + "/6e-phone-academy-popup.png")
                new_page.close()
            except Exception as e:
                print("ACADEMY popup FAILED (390):", str(e)[:200], flush=True)
        print("main page still staged:", "naya-proof-host" in page.url, flush=True)

        # --- 4. Composer at 390 (fresh load) ---
        ctx2 = browser.new_context(viewport={"width": 390, "height": 844})
        page2 = ctx2.new_page()
        page2.goto(BASE + "#home/composer", wait_until="domcontentloaded", timeout=120000)
        page2.wait_for_timeout(5000)
        dismiss_modal(page2)
        page2.wait_for_timeout(2000)
        body_cls = page2.locator("body").get_attribute("class") or ""
        fc_open = "fc-open" in body_cls
        print(f"[390 #home/composer] open={fc_open}", flush=True)
        page2.screenshot(path=EYE + "/6e-phone-composer.png")
        browser.close()

main()
