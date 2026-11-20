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

def boxes_of(pg, text, limit=6):
    loc = pg.locator(f"text={text}")
    out = []
    for i in range(min(loc.count(), limit)):
        try:
            out.append(loc.nth(i).bounding_box(timeout=3000))
        except Exception as e:
            out.append(f"err {type(e).__name__}")
    return out

with sync_playwright() as p:
    b = p.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1920, "height": 1080})
    pg = ctx.new_page()
    pg.goto(STAGED, timeout=60000)
    pg.wait_for_timeout(4000)
    dismiss(pg)
    # open room
    ask = pg.locator("text=Ask Naya").first
    ask.scroll_into_view_if_needed(timeout=15000)
    pg.wait_for_timeout(800)
    box = ask.bounding_box(timeout=15000)
    pg.mouse.click(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
    pg.wait_for_timeout(5000)
    log("ask_room_5s", pg.locator(".naya-ask-room").count())
    log("tab_boxes_before", {"PERSONAL": boxes_of(pg, "PERSONAL"), "BUSINESS": boxes_of(pg, "BUSINESS"), "WORLD": boxes_of(pg, "WORLD")})
    # horizontal wheel over the tab strip to bring PERSONAL into view
    pg.mouse.move(960, 117)
    for _ in range(4):
        pg.mouse.wheel(-600, 0)
        pg.wait_for_timeout(400)
    log("tab_boxes_after_hwheel", {"PERSONAL": boxes_of(pg, "PERSONAL"), "BUSINESS": boxes_of(pg, "BUSINESS")})
    # vertical wheel as the checker did
    pg.mouse.move(960, 500)
    for _ in range(3):
        pg.mouse.wheel(0, 700)
        pg.wait_for_timeout(400)
    log("tab_boxes_after_vwheel", {"PERSONAL": boxes_of(pg, "PERSONAL")})
    # try tapping the 272x60 feed tab if it is now in viewport
    pers = pg.locator("text=PERSONAL")
    tapped = False
    for i in range(min(pers.count(), 10)):
        try:
            bb = pers.nth(i).bounding_box(timeout=3000)
        except Exception:
            continue
        if isinstance(bb, dict) and 0 <= bb["x"] < 1920 and 0 <= bb["y"] < 1080 and bb["width"] > 150 and bb["height"] > 40:
            log("yield_target", bb)
            pg.mouse.click(bb["x"] + bb["width"]/2, bb["y"] + bb["height"]/2)
            pg.wait_for_timeout(3000)
            log("room_after_personal_tab", pg.locator(".naya-ask-room").count())
            log("url_after_personal_tab", pg.url)
            pg.screenshot(path="eye-80-after-personal-yield-1920.png")
            tapped = True
            break
    log("yield_tapped", tapped)
    if not tapped:
        pg.screenshot(path="eye-81-yield-nottapped-1920.png")
    # --- Settings -> Go to Home Hub via the LINK ---
    pg.goto(STAGED, timeout=60000)
    pg.wait_for_timeout(4000)
    dismiss(pg)
    pg.locator("#settingsbtn").first.click(timeout=10000, force=True)
    pg.wait_for_timeout(2000)
    pg.locator("text=Home Hub & install").first.click(timeout=10000)
    pg.wait_for_timeout(1500)
    link = pg.locator('a.ph-msg[href="https://nayanet.app/hub#/hub"]').first
    log("hub_link_count", link.count())
    link.click(timeout=10000)
    pg.wait_for_timeout(5000)
    log("hub_landing_url", pg.url)
    log("hub_landing_title", pg.title())
    pg.screenshot(path="eye-82-hub-landing-1920.png")
    # --- #people via CONNECT menu ---
    pg.goto(STAGED, timeout=60000)
    pg.wait_for_timeout(4000)
    dismiss(pg)
    pg.locator('[aria-label="CONNECT — open"]').first.click(timeout=15000)
    pg.wait_for_timeout(1500)
    log("connect_menu_visible", pg.locator("#hubPlusConnect").first.is_visible(timeout=3000))
    pg.locator("#hubPlusConnect button", has_text="All connections").first.click(timeout=10000)
    pg.wait_for_timeout(3000)
    log("people_url", pg.url)
    pg.mouse.wheel(0, 800)
    pg.wait_for_timeout(15000)
    log("people_url_after_15s", pg.url)
    pg.screenshot(path="eye-83-people-1920.png")
    # --- WORLDS + ECOSYSTEM via aria-labels ---
    pg.goto(STAGED, timeout=60000)
    pg.wait_for_timeout(4000)
    dismiss(pg)
    pg.locator('[aria-label="WORLDS — open"]').first.click(timeout=15000)
    pg.wait_for_timeout(4000)
    log("worlds_url", pg.url)
    pg.go_back()
    pg.wait_for_timeout(3000)
    pg.locator('[aria-label="ECOSYSTEM — open"]').first.click(timeout=15000)
    pg.wait_for_timeout(4000)
    log("ecosystem_url", pg.url)
    b.close()
with open("work/leg1920e.json", "w") as f:
    json.dump(OUT, f, indent=1)
print("DONE-1920E")
