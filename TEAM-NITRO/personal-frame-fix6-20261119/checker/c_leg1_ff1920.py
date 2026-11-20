# CHECKER leg 1 — Firefox 1920: Ask Naya bullseye (2 taps), PERSONAL yield, #people, Academy.
import sys, time
from playwright.sync_api import sync_playwright

URL = "https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/frame-round-fix6-20261119&cb=8fbec9580c078b97d0881f7aa20d8c92ce41d9d6&owner=flagship-personal"
OUT = "/home/hatch/workspace/team-nitro/personal-frame-fix6-20261119/checker/"

def room(page): return page.locator(".naya-ask-room").count()
def dismiss_install(page):
    try:
        btn = page.get_by_role("button", name="Not now")
        if btn.count():
            btn.first.click(timeout=10000, force=True)
            print("install modal dismissed", flush=True)
    except Exception as e:
        print("install dismiss:", str(e)[:120], flush=True)

def raw_tap(page, locator):
    box = locator.bounding_box(timeout=15000)
    assert box, "no box"
    page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    print("tapped at", round(box["x"] + box["width"]/2, 1), round(box["y"] + box["height"]/2, 1), flush=True)

with sync_playwright() as p:
    b = p.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1920, "height": 1080})
    page = ctx.new_page()
    page.goto(URL, timeout=120000)
    page.wait_for_timeout(8000)
    dismiss_install(page)
    page.wait_for_timeout(3000)
    print("loaded title:", page.title(), "url:", page.url, "room:", room(page), flush=True)
    page.screenshot(path=OUT + "c1-fresh.png")

    # --- Bullseye: Ask Naya button ---
    ask = page.locator('.hub-obsidian-btn[aria-label="Ask Naya"]')
    print("ask btn count:", ask.count(), flush=True)
    raw_tap(page, ask.first)
    for t in (2, 5, 10):
        page.wait_for_timeout(t * 1000 if t == 2 else (t - 2) * 1000 if t == 5 else 5000)
        print(f"after tap1 t+{t}s room={room(page)} url={page.url} title={page.title()}", flush=True)
    page.screenshot(path=OUT + "c1-ask-room.png")
    # second tap (button may be behind room; use locator again)
    try:
        raw_tap(page, ask.first)
        page.wait_for_timeout(5000)
        print(f"after tap2 t+5s room={room(page)} url={page.url}", flush=True)
    except Exception as e:
        print("tap2 skipped:", str(e)[:150], "room still:", room(page), flush=True)
    page.screenshot(path=OUT + "c1-ask-room-2nd.png")

    # --- PERSONAL feed tab yield ---
    personal = page.get_by_role("tab", name="PERSONAL")
    print("PERSONAL tab count:", personal.count(), flush=True)
    if personal.count():
        try:
            personal.first.click(timeout=10000)
        except Exception:
            raw_tap(page, personal.first)
        page.wait_for_timeout(3000)
        print(f"after PERSONAL tab: room={room(page)} url={page.url}", flush=True)
        page.screenshot(path=OUT + "c1-after-personal-yield.png")
    else:
        # fallback: any button/link named PERSONAL
        alt = page.locator("text=PERSONAL").first
        print("PERSONAL text count:", page.locator("text=PERSONAL").count(), flush=True)

    # --- Connections #people hold ---
    conn = page.get_by_role("button", name="Connections")
    print("Connections btn count:", conn.count(), flush=True)
    if conn.count():
        try:
            conn.first.click(timeout=10000)
        except Exception:
            raw_tap(page, conn.first)
        page.wait_for_timeout(3000)
        print("after Connections url:", page.url, flush=True)
        page.mouse.wheel(0, 800)
        page.wait_for_timeout(15000)
        print("after scroll+15s url:", page.url, flush=True)
        page.screenshot(path=OUT + "c1-people-hash.png")

    # --- Academy cover pill (fresh page to avoid state) ---
    page2 = ctx.new_page()
    page2.goto(URL, timeout=120000)
    page2.wait_for_timeout(8000)
    dismiss_install(page2)
    page2.wait_for_timeout(2000)
    pill = page2.locator("a[data-mw-cover='Naya Academy']")
    print("academy pill count:", pill.count(), flush=True)
    with ctx.expect_page(timeout=15000) as pop:
        raw_tap(page2, pill.first)
    popup = pop.value
    popup.wait_for_timeout(5000)
    print("academy popup url:", popup.url, flush=True)
    page2.screenshot(path=OUT + "c1-academy-popup.png")
    print("LEG1 DONE", flush=True)
    b.close()
