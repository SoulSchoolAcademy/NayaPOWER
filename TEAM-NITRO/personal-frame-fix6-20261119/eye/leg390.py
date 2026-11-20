import json, time
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
    # dismiss install modal if present
    try:
        btn = pg.locator("#naya-install-overlay button", has_text="Not now")
        if btn.count():
            btn.first.click(timeout=10000, force=True)
            pg.wait_for_timeout(1000)
            log("modal_dismissed", True)
    except Exception as e:
        log("modal_dismiss", f"failed: {type(e).__name__}")
    log("fresh_url", pg.url)
    log("fresh_controls", pg.locator("button, a, input, [role=button]").count())
    pg.screenshot(path="eye-10-fresh-390.png")
    # --- Ask Naya button ---
    ask = pg.locator("text=Ask Naya").first
    box = ask.bounding_box(timeout=15000)
    log("ask_box", box)
    pg.mouse.click(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
    for t in (2, 5, 10):
        pg.wait_for_timeout((t - (2 if t==2 else 5 if t==5 else 10))*1000 if t>2 else 2000)
        log(f"room_at_{t}s", pg.locator(".naya-ask-room").count())
        log(f"hash_at_{t}s", pg.url.split("workers.dev/")[-1][:80])
    log("hash_after_ask", pg.url)
    pg.screenshot(path="eye-11-ask-room-390.png")
    # room bar labels: read text of the room bottom bar
    try:
        bar = pg.locator(".naya-ask-room").locator("..").inner_text(timeout=5000)
        log("room_text_snippet", bar[:400])
    except Exception as e:
        log("room_text", f"err {type(e).__name__}")
    # --- PERSONAL yield (B): room open -> tap PERSONAL feed tab ---
    # The room covers feed tabs at 390 per checker; try to find PERSONAL tab
    pers = pg.locator("text=PERSONAL").first
    try:
        pbox = pers.bounding_box(timeout=5000)
        log("personal_tab_box_while_room_open", pbox)
        if pbox:
            pg.mouse.click(pbox["x"] + pbox["width"]/2, pbox["y"] + pbox["height"]/2)
            pg.wait_for_timeout(3000)
            log("room_after_personal_tab", pg.locator(".naya-ask-room").count())
            log("url_after_personal_tab", pg.url)
            pg.screenshot(path="eye-12-after-personal-yield-390.png")
    except Exception as e:
        log("personal_tab_while_room_open", f"err {type(e).__name__}")
    # --- Back closes room (re-open first if closed) ---
    if pg.locator(".naya-ask-room").count() == 0:
        box = pg.locator("text=Ask Naya").first.bounding_box(timeout=15000)
        pg.mouse.click(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
        pg.wait_for_timeout(5000)
        log("room_reopened", pg.locator(".naya-ask-room").count())
    pg.go_back()
    pg.wait_for_timeout(3000)
    log("room_after_back", pg.locator(".naya-ask-room").count())
    log("url_after_back", pg.url)
    pg.screenshot(path="eye-13-after-back-390.png")
    # --- Back-button repaint: go WORLDS (use Go to the Hub at 390 per fix-5 eye) ---
    pg.goto(STAGED, timeout=60000)
    pg.wait_for_timeout(4000)
    try:
        btn = pg.locator("#naya-install-overlay button", has_text="Not now")
        if btn.count():
            btn.first.click(timeout=10000, force=True)
            pg.wait_for_timeout(1000)
    except Exception:
        pass
    fresh_n = pg.locator("button, a, input, [role=button]").count()
    log("back_fresh_controls", fresh_n)
    pg.screenshot(path="eye-14-back-fresh-390.png")
    hub = pg.locator("text=Go to the Hub").first
    hbox = hub.bounding_box(timeout=15000)
    log("go_hub_box", hbox)
    pg.mouse.click(hbox["x"] + hbox["width"]/2, hbox["y"] + hbox["height"]/2)
    pg.wait_for_timeout(5000)
    log("url_after_go_hub", pg.url)
    pg.go_back()
    pg.wait_for_timeout(5000)
    log("back_controls_5s", pg.locator("button, a, input, [role=button]").count())
    pg.screenshot(path="eye-15-after-back-390.png")
    pg.wait_for_timeout(10000)
    log("back_controls_15s", pg.locator("button, a, input, [role=button]").count())
    pg.screenshot(path="eye-16-after-back-15s-390.png")
    # markers visible?
    for m in ["Shawn Vibert", "Nothing here yet", "PERSONAL"]:
        log(f"marker_{m}", pg.locator(f"text={m}").first.count())
    b.close()
with open("work/leg390.json", "w") as f:
    json.dump(OUT, f, indent=1)
print("DONE-390")
