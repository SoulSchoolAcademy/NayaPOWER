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
    # --- (B) PERSONAL yield via BOTTOM-BAR tile (fix-4 checker's exact path) ---
    ask = pg.locator("text=Ask Naya").first
    ask.scroll_into_view_if_needed(timeout=15000)
    pg.wait_for_timeout(800)
    box = ask.bounding_box(timeout=15000)
    pg.mouse.click(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
    pg.wait_for_timeout(5000)
    log("ask_room_5s", pg.locator(".naya-ask-room").count())
    log("ask_url", pg.url)
    pg.locator('[aria-label="PERSONAL — open"]').first.click(timeout=15000)
    pg.wait_for_timeout(3000)
    log("room_after_personal_tile", pg.locator(".naya-ask-room").count())
    log("url_after_personal_tile", pg.url)
    pg.screenshot(path="eye-70-after-personal-yield-1920.png")
    # tap PERSONAL tile again -> URL normalises to #home (fix-4 checker item 151)
    pg.locator('[aria-label="PERSONAL — open"]').first.click(timeout=15000)
    pg.wait_for_timeout(3000)
    log("url_after_personal_tile_2nd", pg.url)
    # --- Settings -> Go to Home Hub via the LINK (a.ph-msg), not the heading ---
    pg.locator("#settingsbtn").first.click(timeout=10000, force=True)
    pg.wait_for_timeout(2000)
    log("settings_url", pg.url)
    pg.locator("text=Home Hub & install").first.click(timeout=10000)
    pg.wait_for_timeout(1500)
    link = pg.locator('a.ph-msg[href="https://nayanet.app/hub#/hub"]').first
    log("hub_link_count", link.count())
    lbox = link.bounding_box(timeout=8000)
    log("hub_link_box", lbox)
    link.click(timeout=10000)
    pg.wait_for_timeout(5000)
    log("hub_landing_url", pg.url)
    log("hub_landing_title", pg.title())
    pg.screenshot(path="eye-71-hub-landing-1920.png")
    # --- #people via CONNECT menu -> All connections ---
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
    pg.screenshot(path="eye-72-people-1920.png")
    # --- bottom-bar destinations: WORLDS + ECOSYSTEM via aria-labels ---
    pg.goto(STAGED, timeout=60000)
    pg.wait_for_timeout(4000)
    dismiss(pg)
    pg.locator('[aria-label="WORLDS — open"]').first.click(timeout=15000)
    pg.wait_for_timeout(4000)
    log("worlds_url", pg.url)
    pg.go_back()
    pg.wait_for_timeout(3000)
    log("back_after_worlds_url", pg.url)
    pg.locator('[aria-label="ECOSYSTEM — open"]').first.click(timeout=15000)
    pg.wait_for_timeout(4000)
    log("ecosystem_url", pg.url)
    b.close()
with open("work/leg1920d.json", "w") as f:
    json.dump(OUT, f, indent=1)
print("DONE-1920D")
