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
    # --- Back repaint 1920 ---
    log("back_fresh_controls", pg.locator("button, a, input, [role=button]").count())
    pg.screenshot(path="eye-50-back-fresh-1920.png")
    worlds = pg.locator("text=WORLDS").first
    worlds.scroll_into_view_if_needed(timeout=10000)
    pg.wait_for_timeout(800)
    wbox = worlds.bounding_box(timeout=8000)
    log("worlds_box", wbox)
    pg.mouse.click(wbox["x"] + wbox["width"]/2, wbox["y"] + wbox["height"]/2)
    pg.wait_for_timeout(5000)
    log("url_after_worlds", pg.url)
    pg.go_back()
    pg.wait_for_timeout(5000)
    log("back_controls_5s", pg.locator("button, a, input, [role=button]").count())
    pg.screenshot(path="eye-51-after-back-1920.png")
    pg.wait_for_timeout(10000)
    log("back_controls_15s", pg.locator("button, a, input, [role=button]").count())
    for m in ["Shawn Vibert", "Nothing here yet", "PERSONAL"]:
        log(f"marker_{m}", pg.locator(f"text={m}").first.count())
    # --- Ask + PERSONAL yield with enumeration ---
    ask = pg.locator("text=Ask Naya").first
    ask.scroll_into_view_if_needed(timeout=15000)
    pg.wait_for_timeout(800)
    box = ask.bounding_box(timeout=15000)
    pg.mouse.click(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
    pg.wait_for_timeout(5000)
    log("ask_room_5s", pg.locator(".naya-ask-room").count())
    log("ask_url", pg.url)
    # enumerate PERSONAL matches
    pers_all = pg.locator("text=PERSONAL")
    n = pers_all.count()
    log("personal_matches", n)
    boxes = []
    for i in range(min(n, 8)):
        try:
            bb = pers_all.nth(i).bounding_box(timeout=3000)
            boxes.append(bb)
        except Exception as e:
            boxes.append(f"err {type(e).__name__}")
    log("personal_boxes", boxes)
    # pick the feed-tab one: in viewport, y in [800,1080]
    target = None
    for bb in boxes:
        if isinstance(bb, dict) and 0 <= bb["x"] < 1920 and 800 <= bb["y"] < 1080:
            target = bb
            break
    if not target:
        # scroll the page so the tab row comes into view, re-enumerate
        pg.mouse.move(960, 500)
        for _ in range(3):
            pg.mouse.wheel(0, 700)
            pg.wait_for_timeout(400)
        boxes2 = []
        for i in range(min(pers_all.count(), 8)):
            try:
                boxes2.append(pers_all.nth(i).bounding_box(timeout=3000))
            except Exception as e:
                boxes2.append(f"err {type(e).__name__}")
        log("personal_boxes_after_wheel", boxes2)
        for bb in boxes2:
            if isinstance(bb, dict) and 0 <= bb["x"] < 1920 and 800 <= bb["y"] < 1080:
                target = bb
                break
    log("personal_yield_target", target)
    if target:
        pg.mouse.click(target["x"] + target["width"]/2, target["y"] + target["height"]/2)
        pg.wait_for_timeout(3000)
        log("room_after_personal_tab", pg.locator(".naya-ask-room").count())
        log("url_after_personal_tab", pg.url)
        pg.screenshot(path="eye-52-after-personal-yield-1920.png")
    # --- ADD menu: handle collapsed bar first ---
    pg.goto(STAGED, timeout=60000)
    pg.wait_for_timeout(4000)
    dismiss(pg)
    show = pg.locator("text=Show the bottom bar").first
    if show.count():
        try:
            sbox = show.bounding_box(timeout=5000)
            log("show_bar_box", sbox)
            if sbox:
                pg.mouse.click(sbox["x"] + sbox["width"]/2, sbox["y"] + sbox["height"]/2)
                pg.wait_for_timeout(1500)
                log("clicked_show_bar", True)
        except Exception as e:
            log("show_bar", f"err {type(e).__name__}")
    else:
        log("show_bar_present", False)
    add = pg.locator('[aria-label="ADD — open"]').first
    abox = add.bounding_box(timeout=10000)
    log("add_box_after_show", abox)
    pg.screenshot(path="eye-53-bottom-bar-1920.png")
    def open_menu():
        ab = pg.locator('[aria-label="ADD — open"]').first.bounding_box(timeout=10000)
        pg.mouse.click(ab["x"] + ab["width"]/2, ab["y"] + ab["height"]/2)
        pg.wait_for_timeout(1500)
        log("menu_visible", pg.locator("#hubPlusCreate").first.is_visible(timeout=3000))
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
    for attempt in (1, 2):
        if attempt == 2:
            pg.goto(STAGED, timeout=60000)
            pg.wait_for_timeout(4000)
            dismiss(pg)
            show = pg.locator("text=Show the bottom bar").first
            if show.count():
                try:
                    sbox = show.bounding_box(timeout=5000)
                    if sbox:
                        pg.mouse.click(sbox["x"] + sbox["width"]/2, sbox["y"] + sbox["height"]/2)
                        pg.wait_for_timeout(1500)
                except Exception:
                    pass
        tap_menu_item("Message")
        log(f"message{attempt}_url", pg.url)
        log(f"message{attempt}_body_msg_open", pg.locator("body.msg-open").count())
        log(f"message{attempt}_msg_panel_count", pg.locator(".hub-msg-panel").count())
        try:
            log(f"message{attempt}_msg_panel_visible", pg.locator(".hub-msg-panel").first.is_visible(timeout=3000))
        except Exception as e:
            log(f"message{attempt}_msg_panel_visible", f"err {type(e).__name__}")
        pg.screenshot(path=f"eye-54-after-message-{attempt}-1920.png")
    tap_menu_item("Make a post")
    log("post_body_fc_open", pg.locator("body.fc-open").count())
    try:
        log("post_fc_hidden", pg.locator("#fcCreator").get_attribute("hidden", timeout=3000))
    except Exception as e:
        log("post_fc_hidden", f"err {type(e).__name__}")
    pg.screenshot(path="eye-55-composer-post-1920.png")
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(1500)
    tap_menu_item("Naya note")
    log("naya_body_fc_open", pg.locator("body.fc-open").count())
    pg.screenshot(path="eye-56-composer-naya-1920.png")
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(1500)
    tap_menu_item("Mail")
    log("mail_url", pg.url)
    log("mail_body_fc_open", pg.locator("body.fc-open").count())
    pg.screenshot(path="eye-57-after-mail-1920.png")
    # --- #people via CONNECT menu -> All connections (robust path) + profile button attempt ---
    pg.goto(STAGED, timeout=60000)
    pg.wait_for_timeout(4000)
    dismiss(pg)
    show = pg.locator("text=Show the bottom bar").first
    if show.count():
        try:
            sbox = show.bounding_box(timeout=5000)
            if sbox:
                pg.mouse.click(sbox["x"] + sbox["width"]/2, sbox["y"] + sbox["height"]/2)
                pg.wait_for_timeout(1500)
        except Exception:
            pass
    conn = pg.locator('[aria-label="CONNECT — open"]').first
    if conn.count() == 0:
        conn = pg.locator("text=CONNECT").first
    try:
        cbox = conn.bounding_box(timeout=8000)
        log("connect_box", cbox)
        if cbox:
            pg.mouse.click(cbox["x"] + cbox["width"]/2, cbox["y"] + cbox["height"]/2)
            pg.wait_for_timeout(1500)
            allc = pg.locator("#hubPlusConnect button", has_text="All connections").first
            acbox = allc.bounding_box(timeout=8000)
            log("all_connections_box", acbox)
            if acbox:
                pg.mouse.click(acbox["x"] + acbox["width"]/2, acbox["y"] + acbox["height"]/2)
                pg.wait_for_timeout(3000)
                log("people_url_via_connect", pg.url)
    except Exception as e:
        log("connect_menu", f"err {type(e).__name__}: {e}")
    pg.mouse.wheel(0, 800)
    pg.wait_for_timeout(15000)
    log("people_url_after_15s", pg.url)
    pg.screenshot(path="eye-58-people-1920.png")
    # --- Settings -> Go to Home Hub with LOCATOR click ---
    pg.locator("#settingsbtn").first.click(timeout=10000, force=True)
    pg.wait_for_timeout(2000)
    log("settings_url", pg.url)
    pg.locator("text=Home Hub & install").first.click(timeout=10000)
    pg.wait_for_timeout(1500)
    pg.locator("text=Go to Home Hub").first.click(timeout=10000)
    pg.wait_for_timeout(4000)
    log("hub_landing_url_locator_click", pg.url)
    pg.screenshot(path="eye-59-hub-landing-1920.png")
    b.close()
with open("work/leg1920b.json", "w") as f:
    json.dump(OUT, f, indent=1)
print("DONE-1920B")
