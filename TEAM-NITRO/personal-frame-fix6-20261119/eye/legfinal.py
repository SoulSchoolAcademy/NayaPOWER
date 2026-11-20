import json, traceback
from playwright.sync_api import sync_playwright

STAGED = "https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/frame-round-fix6-20261119&cb=8fbec9580c078b97d0881f7aa20d8c92ce41d9d6&owner=flagship-personal"
LIVE_HUB = "https://nayanet.app/hub"
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
    # ---- 1. LIVE HUB end-to-end ----
    pg = ctx.new_page()
    try:
        pg.goto(LIVE_HUB, timeout=60000)
        pg.wait_for_timeout(6000)
        log("live_modal_present", pg.locator("#naya-install-overlay").count())
        log("live_modal_dismissed", dismiss(pg))
        pg.screenshot(path="eye-90-live-hub-1920.png")
        log("live_controls", pg.locator("button, a, input, [role=button]").count())
        ask = pg.locator("text=Ask Naya").first
        try:
            abox = ask.bounding_box(timeout=15000)
            log("live_ask_box", abox)
        except Exception as e:
            log("live_ask_box", f"err {type(e).__name__}: {e}")
            abox = None
        if abox:
            pg.mouse.click(abox["x"] + abox["width"]/2, abox["y"] + abox["height"]/2)
            pg.wait_for_timeout(5000)
            log("live_room_5s", pg.locator(".naya-ask-room").count())
            log("live_url", pg.url)
            pg.screenshot(path="eye-91-live-ask-room-1920.png")
    except Exception:
        log("live_hub_error", traceback.format_exc()[-1200:])
    pg.close()
    # ---- 2. PERSONAL yield via strip drag ----
    pg = ctx.new_page()
    try:
        pg.goto(STAGED, timeout=60000)
        pg.wait_for_timeout(4000)
        dismiss(pg)
        ask = pg.locator("text=Ask Naya").first
        ask.scroll_into_view_if_needed(timeout=15000)
        pg.wait_for_timeout(800)
        box = ask.bounding_box(timeout=15000)
        pg.mouse.click(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
        pg.wait_for_timeout(5000)
        log("staged_room_5s", pg.locator(".naya-ask-room").count())
        # drag the tab strip right to bring PERSONAL into view
        pers = pg.locator("text=PERSONAL")
        bb0 = None
        for i in range(min(pers.count(), 10)):
            try:
                bb = pers.nth(i).bounding_box(timeout=3000)
            except Exception:
                continue
            if isinstance(bb, dict) and bb["width"] > 150 and bb["height"] > 40:
                bb0 = bb
                break
        log("strip_tab_box_before_drag", bb0)
        if bb0:
            pg.mouse.move(bb0["x"] + bb0["width"]/2, bb0["y"] + bb0["height"]/2)
            pg.mouse.down()
            for _ in range(10):
                pg.mouse.move(bb0["x"] + bb0["width"]/2 + 40 * (_ + 1), bb0["y"] + bb0["height"]/2)
                pg.wait_for_timeout(60)
            pg.mouse.up()
            pg.wait_for_timeout(800)
            bb1 = None
            for i in range(min(pers.count(), 10)):
                try:
                    bb = pers.nth(i).bounding_box(timeout=3000)
                except Exception:
                    continue
                if isinstance(bb, dict) and bb["width"] > 150 and bb["height"] > 40:
                    bb1 = bb
                    break
            log("strip_tab_box_after_drag", bb1)
            if isinstance(bb1, dict) and 0 <= bb1["x"] < 1920 and 0 <= bb1["y"] < 1080:
                pg.mouse.click(bb1["x"] + bb1["width"]/2, bb1["y"] + bb1["height"]/2)
                pg.wait_for_timeout(3000)
                log("room_after_personal_tab", pg.locator(".naya-ask-room").count())
                log("url_after_personal_tab", pg.url)
                pg.screenshot(path="eye-92-after-personal-yield-1920.png")
            else:
                log("yield_tap", "tab still off-viewport after drag")
                pg.screenshot(path="eye-93-yield-nottapped-1920.png")
        else:
            log("yield_tap", "no 272x60 tab found")
    except Exception:
        log("yield_error", traceback.format_exc()[-1200:])
    b.close()
with open("work/legfinal.json", "w") as f:
    json.dump(OUT, f, indent=1)
print("DONE-FINAL")
