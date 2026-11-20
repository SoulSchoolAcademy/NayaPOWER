import json
from playwright.sync_api import sync_playwright

STAGED = "https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/frame-round-fix6-20261119&cb=8fbec9580c078b97d0881f7aa20d8c92ce41d9d6&owner=flagship-personal"
OUT = {}
def log(k, v):
    OUT[k] = v
    print(k, "=", json.dumps(v), flush=True)

with sync_playwright() as p:
    b = p.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    pg = ctx.new_page()
    pg.goto(STAGED, timeout=60000)
    pg.wait_for_timeout(4000)
    try:
        btn = pg.locator("#naya-install-overlay button", has_text="Not now")
        if btn.count():
            btn.first.click(timeout=10000, force=True)
            pg.wait_for_timeout(1000)
            log("modal_dismissed", True)
    except Exception as e:
        log("modal_dismiss", f"failed: {type(e).__name__}")
    # --- Ask Naya button: scroll into view first (checker c_leg5 method) ---
    ask = pg.locator("text=Ask Naya").first
    ask.scroll_into_view_if_needed(timeout=15000)
    pg.wait_for_timeout(1000)
    box = ask.bounding_box(timeout=15000)
    log("ask_box_after_scroll", box)
    pg.screenshot(path="eye-20-before-ask-390.png")
    pg.mouse.click(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
    pg.wait_for_timeout(2000)
    log("room_at_2s", pg.locator(".naya-ask-room").count())
    log("url_at_2s", pg.url)
    pg.wait_for_timeout(3000)
    log("room_at_5s", pg.locator(".naya-ask-room").count())
    pg.wait_for_timeout(5000)
    log("room_at_10s", pg.locator(".naya-ask-room").count())
    log("url_at_10s", pg.url)
    pg.screenshot(path="eye-21-ask-room-390.png")
    # room bar labels at 390 — read the room bar text
    try:
        room = pg.locator(".naya-ask-room").first
        log("room_text", room.inner_text(timeout=5000)[:500])
    except Exception as e:
        log("room_text", f"err {type(e).__name__}")
    # scroll the room to see bottom bar
    pg.mouse.wheel(0, 600)
    pg.wait_for_timeout(1000)
    pg.screenshot(path="eye-22-room-scrolled-390.png")
    # --- Back closes room at 390 ---
    pg.go_back()
    pg.wait_for_timeout(3000)
    log("room_after_back", pg.locator(".naya-ask-room").count())
    log("url_after_back", pg.url)
    pg.screenshot(path="eye-23-after-back-390.png")
    # --- ADD menu -> Message (A) at 390 ---
    pg.goto(STAGED, timeout=60000)
    pg.wait_for_timeout(4000)
    try:
        btn = pg.locator("#naya-install-overlay button", has_text="Not now")
        if btn.count():
            btn.first.click(timeout=10000, force=True)
            pg.wait_for_timeout(1000)
    except Exception:
        pass
    # bottom bar ADD: scroll to bottom of page to reveal bar
    pg.mouse.wheel(0, 5000)
    pg.wait_for_timeout(1500)
    pg.screenshot(path="eye-24-bottom-bar-390.png")
    add = pg.locator("text=ADD").first
    try:
        abox = add.bounding_box(timeout=8000)
        log("add_box", abox)
        if abox:
            pg.mouse.click(abox["x"] + abox["width"]/2, abox["y"] + abox["height"]/2)
            pg.wait_for_timeout(2000)
            pg.screenshot(path="eye-25-create-menu-390.png")
            msg = pg.locator("text=Message").first
            mbox = msg.bounding_box(timeout=8000)
            log("message_item_box", mbox)
            if mbox:
                pg.mouse.click(mbox["x"] + mbox["width"]/2, mbox["y"] + mbox["height"]/2)
                pg.wait_for_timeout(3000)
                log("url_after_message_tap", pg.url)
                log("composer_open_after_message", pg.locator("#fcCreator").count())
                try:
                    log("fc_hidden", pg.locator("#fcCreator").get_attribute("hidden", timeout=3000))
                except Exception as e:
                    log("fc_hidden", f"err {type(e).__name__}")
                log("body_fc_open", pg.locator("body.fc-open").count())
                pg.screenshot(path="eye-26-after-message-390.png")
    except Exception as e:
        log("add_menu", f"err {type(e).__name__}: {e}")
    b.close()
with open("work/leg390b.json", "w") as f:
    json.dump(OUT, f, indent=1)
print("DONE-390B")
