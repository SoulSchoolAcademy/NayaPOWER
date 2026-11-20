# CHECKER leg 5c — phone 390: Back return via Go to the Hub (partial-match + stepped
# wheel scroll, fix-5 eye phone_back3 pattern), Academy popup, composer.
from playwright.sync_api import sync_playwright

URL = "https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/frame-round-fix6-20261119&cb=8fbec9580c078b97d0881f7aa20d8c92ce41d9d6&owner=flagship-personal"
OUT = "/home/hatch/workspace/team-nitro/personal-frame-fix6-20261119/checker/"

def dismiss_install(page):
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
    t = page.locator("body").inner_text(timeout=5000)
    return {"controls": page.locator("button, a, input, [role=button]").count(),
            "quote": "NayaNET" in t, "name": "Shawn Vibert" in t, "empty": "Nothing here yet." in t}
def raw_tap(page, locator):
    box = locator.bounding_box(timeout=15000)
    assert box, "no box"
    page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)

with sync_playwright() as p:
    b = p.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)

    # --- Back return via Go to the Hub (fresh page) ---
    page = ctx.new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(9000)
    print("modal dismissed:", dismiss_install(page), flush=True)
    page.wait_for_timeout(3000)
    print("phone back fresh:", markers(page), flush=True)
    page.screenshot(path=OUT + "c5c-phone-fresh.png")
    btn = page.get_by_text("Go to the Hub", exact=False)
    print("Go to the Hub (partial) matches:", btn.count(), flush=True)
    tapped = False
    for step in range(8):
        for i in range(btn.count()):
            try: bb = btn.nth(i).bounding_box(timeout=3000)
            except Exception: bb = None
            print(f"  step {step} hub btn [{i}] box={bb}", flush=True)
            if bb and 0 <= bb["y"] <= 800:
                page.mouse.click(bb["x"] + bb["width"]/2, bb["y"] + bb["height"]/2)
                print("tapped Go to the Hub", flush=True)
                tapped = True
                break
        if tapped: break
        page.mouse.move(195, 400)
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(1000)
    if tapped:
        try:
            page.wait_for_url("**nayanet.app/hub**", timeout=30000)
            print("HUB LANDING:", page.url, flush=True)
        except Exception:
            print("no hub landing; url=", page.url[:110], flush=True)
        page.wait_for_timeout(3000)
        page.go_back(timeout=60000)
        page.wait_for_timeout(5000)
        print("phone after Back @5s:", markers(page), flush=True)
        page.screenshot(path=OUT + "c5c-phone-after-back.png")
        page.wait_for_timeout(10000)
        m15 = markers(page)
        print("phone after Back @15s:", m15, flush=True)
        page.screenshot(path=OUT + "c5c-phone-after-back-15s.png")
        print("PHONE BACK RETURN:", "PASS" if m15["controls"] > 650 and m15["quote"] and m15["name"] and m15["empty"] else "FAIL/CHECK", flush=True)
    else:
        print("PHONE BACK RETURN: Go to the Hub never became tappable at 390", flush=True)
    page.close()

    # --- Academy popup at 390 ---
    page2 = ctx.new_page()
    page2.goto(URL, wait_until="domcontentloaded", timeout=120000)
    page2.wait_for_timeout(9000); dismiss_install(page2); page2.wait_for_timeout(2000)
    pill = page2.locator("a[data-mw-cover='Naya Academy']")
    print("phone academy pill count:", pill.count(), flush=True)
    with ctx.expect_page(timeout=15000) as pop:
        raw_tap(page2, pill.first)
    popup = pop.value
    popup.wait_for_timeout(5000)
    print("phone academy popup url:", popup.url, flush=True)
    page2.screenshot(path=OUT + "c5c-phone-academy-popup.png")
    print("PHONE ACADEMY:", "PASS" if popup.url == "https://nayanet.groovepages.com/academy" else "FAIL", flush=True)
    page2.close()

    # --- Composer at 390 (fresh load) ---
    page3 = ctx.new_page()
    page3.goto(URL + "#home/composer", wait_until="domcontentloaded", timeout=120000)
    page3.wait_for_timeout(9000); dismiss_install(page3); page3.wait_for_timeout(5000)
    fc = page3.locator("#fcCreator")
    hidden = fc.get_attribute("hidden") if fc.count() else "NO-ELEMENT"
    body_cls = page3.locator("body").get_attribute("class") or ""
    open_state = (hidden is None) and ("fc-open" in body_cls)
    print(f"phone composer: open={open_state} hidden={hidden!r}", flush=True)
    page3.screenshot(path=OUT + "c5c-phone-composer.png")
    print("PHONE COMPOSER:", "PASS" if open_state else "FAIL", flush=True)
    print("LEG5C DONE", flush=True)
    b.close()
