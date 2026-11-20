import json
from playwright.sync_api import sync_playwright

STAGED = "https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/frame-round-fix6-20261119&cb=8fbec9580c078b97d0881f7aa20d8c92ce41d9d6&owner=flagship-personal"
OUT = {}
def log(k, v):
    OUT[k] = v
    print(k, "=", json.dumps(v), flush=True)

def dismiss(pg):
    try:
        btn = pg.locator("#naya-install-overlay button", has_text="Not now")
        if btn.count():
            btn.first.click(timeout=10000, force=True)
            pg.wait_for_timeout(1000)
            return True
    except Exception:
        pass
    return False

with sync_playwright() as p:
    b = p.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1920, "height": 1080})
    pg = ctx.new_page()
    pg.goto(STAGED, timeout=60000)
    pg.wait_for_timeout(4000)
    dismiss(pg)
    # --- (B) PERSONAL yield: open room, wheel-scroll FIRST, then tap tab as-is ---
    ask = pg.locator("text=Ask Naya").first
    ask.scroll_into_view_if_needed(timeout=15000)
    pg.wait_for_timeout(800)
    box = ask.bounding_box(timeout=15000)
    pg.mouse.click(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
    pg.wait_for_timeout(5000)
    log("ask_room_5s", pg.locator(".naya-ask-room").count())
    pg.mouse.move(960, 500)
    for _ in range(3):
        pg.mouse.wheel(0, 700)
        pg.wait_for_timeout(400)
    pers_all = pg.locator("text=PERSONAL")
    boxes = []
    for i in range(min(pers_all.count(), 10)):
        try:
            boxes.append(pers_all.nth(i).bounding_box(timeout=3000))
        except Exception as e:
            boxes.append(f"err {type(e).__name__}")
    log("personal_boxes_after_wheel", boxes)
    # the feed tab is ~272 wide x 60 high; pick one in viewport
    target = None
    for bb in boxes:
        if isinstance(bb, dict) and 0 <= bb["x"] < 1920 and 0 <= bb["y"] < 1080 and bb["width"] > 150:
            target = bb
            break
    log("yield_target", target)
    if target:
        pg.mouse.click(target["x"] + target["width"]/2, target["y"] + target["height"]/2)
        pg.wait_for_timeout(3000)
        log("room_after_personal_tab", pg.locator(".naya-ask-room").count())
        log("url_after_personal_tab", pg.url)
        pg.screenshot(path="eye-60-after-personal-yield-1920.png")
    # --- (A) Message: scroll bar into view, open menu, tap Message ---
    for attempt in (1, 2):
        if attempt == 2:
            pg.goto(STAGED, timeout=60000)
            pg.wait_for_timeout(4000)
            dismiss(pg)
        # scroll page to bottom so the bar is in view
        for _ in range(6):
            pg.mouse.wheel(0, 2000)
            pg.wait_for_timeout(300)
        add = pg.locator('[aria-label="ADD — open"]').first
        abox = add.bounding_box(timeout=10000)
        log(f"message{attempt}_add_box", abox)
        # locator click auto-scrolls into view
        add.click(timeout=10000)
        pg.wait_for_timeout(1500)
        log(f"message{attempt}_menu_visible", pg.locator("#hubPlusCreate").first.is_visible(timeout=3000))
        pg.screenshot(path=f"eye-61-create-menu-{attempt}-1920.png")
        it = pg.locator("#hubPlusCreate button", has_text="Message").first
        ibox = it.bounding_box(timeout=8000)
        log(f"message{attempt}_item_box", ibox)
        it.click(timeout=10000)
        pg.wait_for_timeout(3000)
        log(f"message{attempt}_url", pg.url)
        log(f"message{attempt}_body_msg_open", pg.locator("body.msg-open").count())
        log(f"message{attempt}_msg_panel_count", pg.locator(".hub-msg-panel").count())
        try:
            log(f"message{attempt}_msg_panel_visible", pg.locator(".hub-msg-panel").first.is_visible(timeout=3000))
        except Exception as e:
            log(f"message{attempt}_msg_panel_visible", f"err {type(e).__name__}")
        pg.screenshot(path=f"eye-62-after-message-{attempt}-1920.png")
    # --- Settings -> Go to Home Hub: popup check ---
    pg.goto(STAGED, timeout=60000)
    pg.wait_for_timeout(4000)
    dismiss(pg)
    pg.locator("#settingsbtn").first.click(timeout=10000, force=True)
    pg.wait_for_timeout(2000)
    pg.locator("text=Home Hub & install").first.click(timeout=10000)
    pg.wait_for_timeout(1500)
    pages_before = len(ctx.pages)
    log("pages_before_hub_click", pages_before)
    try:
        with pg.expect_popup(timeout=8000) as pop:
            pg.locator("text=Go to Home Hub").first.click(timeout=10000)
        popup = pop.value
        popup.wait_for_timeout(3000)
        log("hub_popup_url", popup.url)
        log("hub_popup_title", popup.title())
    except Exception as e:
        log("hub_popup", f"none: {type(e).__name__}")
        pg.wait_for_timeout(2000)
        log("hub_url_after_click", pg.url)
        log("pages_after_click", len(ctx.pages))
    pg.screenshot(path="eye-63-hub-landing-1920.png")
    b.close()
with open("work/leg1920c.json", "w") as f:
    json.dump(OUT, f, indent=1)
print("DONE-1920C")
