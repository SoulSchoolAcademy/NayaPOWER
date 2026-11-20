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
    log("modal", dismiss(pg))
    log("fresh_controls", pg.locator("button, a, input, [role=button]").count())
    pg.screenshot(path="eye-30-fresh-1920.png")
    # --- 1. Ask Naya x2 ---
    ask = pg.locator("text=Ask Naya").first
    ask.scroll_into_view_if_needed(timeout=15000)
    pg.wait_for_timeout(800)
    box = ask.bounding_box(timeout=15000)
    pg.mouse.click(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
    pg.wait_for_timeout(2000); log("ask1_room_2s", pg.locator(".naya-ask-room").count())
    pg.wait_for_timeout(3000); log("ask1_room_5s", pg.locator(".naya-ask-room").count())
    pg.wait_for_timeout(5000); log("ask1_room_10s", pg.locator(".naya-ask-room").count())
    log("ask1_url", pg.url)
    pg.screenshot(path="eye-31-ask-room-1920.png")
    # --- 3. PERSONAL yield (B): room open -> tap PERSONAL feed tab (wheel method) ---
    pg.mouse.move(960, 500)
    for _ in range(3):
        pg.mouse.wheel(0, 700)
        pg.wait_for_timeout(400)
    pers = pg.locator("text=PERSONAL").first
    pbox = pers.bounding_box(timeout=8000)
    log("personal_tab_box", pbox)
    if pbox:
        pg.mouse.click(pbox["x"] + pbox["width"]/2, pbox["y"] + pbox["height"]/2)
        pg.wait_for_timeout(3000)
        log("room_after_personal_tab", pg.locator(".naya-ask-room").count())
        log("url_after_personal_tab", pg.url)
        pg.screenshot(path="eye-32-after-personal-yield-1920.png")
    # --- 2. Back closes room: reopen, then Back ---
    ask = pg.locator("text=Ask Naya").first
    ask.scroll_into_view_if_needed(timeout=15000)
    pg.wait_for_timeout(800)
    box = ask.bounding_box(timeout=15000)
    pg.mouse.click(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
    pg.wait_for_timeout(5000)
    log("ask2_room_5s", pg.locator(".naya-ask-room").count())
    pg.screenshot(path="eye-33-ask-room-2nd-1920.png")
    pg.go_back()
    pg.wait_for_timeout(3000)
    log("room_after_back", pg.locator(".naya-ask-room").count())
    log("url_after_back", pg.url)
    # --- 5/6. ADD menu items at 1920 ---
    add = pg.locator('[aria-label="ADD — open"]').first
    abox = add.bounding_box(timeout=10000)
    log("add_box", abox)
    def open_menu():
        ab = pg.locator('[aria-label="ADD — open"]').first.bounding_box(timeout=10000)
        pg.mouse.click(ab["x"] + ab["width"]/2, ab["y"] + ab["height"]/2)
        pg.wait_for_timeout(1500)
    def tap_menu_item(label):
        open_menu()
        it = pg.locator("#hubPlusCreate button", has_text=label).first
        ibox = it.bounding_box(timeout=8000)
        log(f"menu_item_{label}_box", ibox)
        if ibox:
            pg.mouse.click(ibox["x"] + ibox["width"]/2, ibox["y"] + ibox["height"]/2)
            pg.wait_for_timeout(3000)
            return True
        return False
    # Message (A) — twice, fresh loads
    for attempt in (1, 2):
        if attempt == 2:
            pg.goto(STAGED, timeout=60000)
            pg.wait_for_timeout(4000)
            dismiss(pg)
        tap_menu_item("Message")
        log(f"message_attempt{attempt}_url", pg.url)
        log(f"message_attempt{attempt}_body_msg_open", pg.locator("body.msg-open").count())
        log(f"message_attempt{attempt}_msg_panel_count", pg.locator(".hub-msg-panel").count())
        try:
            log(f"message_attempt{attempt}_msg_panel_visible", pg.locator(".hub-msg-panel").first.is_visible(timeout=3000))
        except Exception as e:
            log(f"message_attempt{attempt}_msg_panel_visible", f"err {type(e).__name__}")
        log(f"message_attempt{attempt}_composer_hidden", pg.locator("#fcCreator").count())
        pg.screenshot(path=f"eye-34-after-message-{attempt}-1920.png")
    # Make a post via menu
    tap_menu_item("Make a post")
    log("post_menu_url", pg.url)
    try:
        log("post_menu_fc_hidden_attr", pg.locator("#fcCreator").get_attribute("hidden", timeout=3000))
    except Exception as e:
        log("post_menu_fc_hidden_attr", f"err {type(e).__name__}")
    log("post_menu_body_fc_open", pg.locator("body.fc-open").count())
    pg.screenshot(path="eye-35-composer-post-1920.png")
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(1500)
    # Naya note via menu
    tap_menu_item("Naya note")
    log("naya_menu_body_fc_open", pg.locator("body.fc-open").count())
    pg.screenshot(path="eye-36-composer-naya-1920.png")
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(1500)
    # Mail via menu
    tap_menu_item("Mail")
    log("mail_menu_url", pg.url)
    log("mail_menu_body_fc_open", pg.locator("body.fc-open").count())
    pg.screenshot(path="eye-37-after-mail-1920.png")
    # --- 7. Academy ---
    pg.goto(STAGED, timeout=60000)
    pg.wait_for_timeout(4000)
    dismiss(pg)
    with pg.expect_popup(timeout=15000) as pop:
        pg.locator("a[data-mw-cover='Naya Academy']").first.click(timeout=10000, force=True)
    popup = pop.value
    popup.wait_for_timeout(3000)
    log("academy_popup_url", popup.url)
    pg.screenshot(path="eye-38-academy-1920.png")
    # --- 8. #people ---
    pg.locator("text=Connections").first.scroll_into_view_if_needed(timeout=10000)
    pg.wait_for_timeout(800)
    cbox = pg.locator("text=Connections").first.bounding_box(timeout=8000)
    pg.mouse.click(cbox["x"] + cbox["width"]/2, cbox["y"] + cbox["height"]/2)
    pg.wait_for_timeout(3000)
    log("people_url", pg.url)
    pg.mouse.wheel(0, 800)
    pg.wait_for_timeout(15000)
    log("people_url_after_15s", pg.url)
    pg.screenshot(path="eye-39-people-1920.png")
    # --- 9. Settings -> Go to Home Hub ---
    pg.locator("#settingsbtn").first.click(timeout=10000, force=True)
    pg.wait_for_timeout(2000)
    log("settings_url", pg.url)
    tab = pg.locator("text=Home Hub & install").first
    tab.click(timeout=10000)
    pg.wait_for_timeout(1500)
    pg.screenshot(path="eye-40-settings-tab6-1920.png")
    link = pg.locator("text=Go to Home Hub").first
    lbox = link.bounding_box(timeout=8000)
    log("go_hub_link_box", lbox)
    if lbox:
        pg.mouse.click(lbox["x"] + lbox["width"]/2, lbox["y"] + lbox["height"]/2)
        pg.wait_for_timeout(4000)
        log("hub_landing_url", pg.url)
        pg.screenshot(path="eye-41-hub-landing-1920.png")
    b.close()
with open("work/leg1920.json", "w") as f:
    json.dump(OUT, f, indent=1)
print("DONE-1920")
