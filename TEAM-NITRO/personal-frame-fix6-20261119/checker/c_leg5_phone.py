# CHECKER leg 5 — phone 390 (Firefox is_mobile): Ask room, Back closes room,
# Back return via Go to the Hub, Academy popup, composer, layout.
from playwright.sync_api import sync_playwright

URL = "https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/frame-round-fix6-20261119&cb=8fbec9580c078b97d0881f7aa20d8c92ce41d9d6&owner=flagship-personal"
OUT = "/home/hatch/workspace/team-nitro/personal-frame-fix6-20261119/checker/"

def room(page): return page.locator(".naya-ask-room").count()
def controls(page): return page.locator("body *").count()
def dismiss_install(page):
    try:
        btn = page.get_by_role("button", name="Not now")
        if btn.count():
            btn.first.click(timeout=10000, force=True)
    except Exception as e:
        print("install dismiss:", str(e)[:100], flush=True)
def raw_tap(page, locator):
    box = locator.bounding_box(timeout=15000)
    assert box, "no box"
    page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)

with sync_playwright() as p:
    b = p.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)

    # --- Ask room at 390 ---
    page = ctx.new_page()
    page.goto(URL, timeout=120000)
    page.wait_for_timeout(9000); dismiss_install(page); page.wait_for_timeout(3000)
    page.screenshot(path=OUT + "c5-phone-fresh.png")
    ask = page.locator('.hub-obsidian-btn[aria-label="Ask Naya"]')
    print("phone ask btn count:", ask.count(), flush=True)
    ask.first.scroll_into_view_if_needed(timeout=8000)
    page.wait_for_timeout(1000)
    raw_tap(page, ask.first)
    for t in (2, 5, 10):
        page.wait_for_timeout(2000 if t == 2 else 3000 if t == 5 else 5000)
        print(f"phone ask t+{t}s room={room(page)} hash={page.url.split('#')[-1]}", flush=True)
    page.screenshot(path=OUT + "c5-phone-ask-room.png")
    # Back closes the room
    page.go_back(timeout=30000)
    page.wait_for_timeout(4000)
    print(f"phone Back from room: room={room(page)} hash={page.url.split('#')[-1]}", flush=True)
    page.screenshot(path=OUT + "c5-phone-room-back.png")
    print("PHONE BACK-CLOSES-ROOM:", "PASS" if room(page) == 0 and page.url.split("#")[-1] == "/hub/feed" else "FAIL", flush=True)

    # --- Back return via Go to the Hub ---
    g = page.get_by_text("Go to the Hub", exact=True).first
    g.scroll_into_view_if_needed(timeout=8000)
    raw_tap(page, g)
    page.wait_for_timeout(8000)
    print("phone after Go-to-Hub url:", page.url, flush=True)
    page.go_back(timeout=60000)
    page.wait_for_timeout(5000)
    c5 = controls(page)
    page.screenshot(path=OUT + "c5-phone-after-back.png")
    page.wait_for_timeout(10000)
    c15 = controls(page)
    print(f"phone back return: @5s={c5} @15s={c15} url={page.url}", flush=True)
    page.screenshot(path=OUT + "c5-phone-after-back-15s.png")
    print("PHONE BACK RETURN:", "PASS" if c15 > 650 else "CHECK", flush=True)

    # --- Academy popup at 390 ---
    page2 = ctx.new_page()
    page2.goto(URL, timeout=120000)
    page2.wait_for_timeout(9000); dismiss_install(page2); page2.wait_for_timeout(2000)
    pill = page2.locator("a[data-mw-cover='Naya Academy']")
    print("phone academy pill count:", pill.count(), flush=True)
    with ctx.expect_page(timeout=15000) as pop:
        raw_tap(page2, pill.first)
    popup = pop.value
    popup.wait_for_timeout(5000)
    print("phone academy popup url:", popup.url, flush=True)
    page2.screenshot(path=OUT + "c5-phone-academy-popup.png")
    print("PHONE ACADEMY:", "PASS" if popup.url == "https://nayanet.groovepages.com/academy" else "FAIL", flush=True)

    # --- Composer at 390 (fresh load) ---
    page3 = ctx.new_page()
    page3.goto(URL + "#home/composer", timeout=120000)
    page3.wait_for_timeout(9000); dismiss_install(page3); page3.wait_for_timeout(5000)
    fc = page3.locator("#fcCreator")
    hidden = fc.get_attribute("hidden") if fc.count() else "NO-ELEMENT"
    body_cls = page3.locator("body").get_attribute("class") or ""
    open_state = (hidden is None) and ("fc-open" in body_cls)
    print(f"phone composer: open={open_state} hidden={hidden!r}", flush=True)
    page3.screenshot(path=OUT + "c5-phone-composer.png")
    print("PHONE COMPOSER:", "PASS" if open_state else "FAIL", flush=True)
    print("LEG5 DONE", flush=True)
    b.close()
