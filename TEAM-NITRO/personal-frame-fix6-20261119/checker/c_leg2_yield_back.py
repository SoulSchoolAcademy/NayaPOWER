# CHECKER leg 2 — Firefox 1920: PERSONAL yield + Back return repaint (normal + throttled).
import sys
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
def markers(page):
    out = {}
    for name, sel in [("quote", "text=NayaNET — create, learn and grow together"),
                      ("personal", "text=PERSONAL"), ("empty", "text=Nothing here yet."),
                      ("ask", "text=Ask Naya"), ("name", "text=Shawn Vibert")]:
        try: out[name] = page.locator(sel).first.is_visible(timeout=2000)
        except Exception: out[name] = False
    return out

with sync_playwright() as p:
    b = p.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1920, "height": 1080})

    # --- PERSONAL yield ---
    page = ctx.new_page()
    page.goto(URL, timeout=120000)
    page.wait_for_timeout(8000); dismiss_install(page); page.wait_for_timeout(3000)
    ask = page.locator('.hub-obsidian-btn[aria-label="Ask Naya"]')
    raw_tap(page, ask.first)
    page.wait_for_timeout(5000)
    print("yield test: room before PERSONAL:", room(page), "hash:", page.url.split("#")[-1], flush=True)
    tabs = page.get_by_text("PERSONAL", exact=True)
    print("PERSONAL exact matches:", tabs.count(), flush=True)
    yielded = False
    for i in range(tabs.count()):
        try:
            tabs.nth(i).scroll_into_view_if_needed(timeout=5000)
            raw_tap(page, tabs.nth(i))
            page.wait_for_timeout(3000)
            print(f"  tapped PERSONAL [{i}]: room={room(page)} hash={page.url.split('#')[-1]}", flush=True)
            if room(page) == 0 and page.url.split("#")[-1] == "/hub/feed":
                yielded = True
                break
        except Exception as e:
            print(f"  PERSONAL [{i}] tap failed:", str(e)[:120], flush=True)
    print("PERSONAL YIELD:", "PASS" if yielded else "FAIL", flush=True)
    page.screenshot(path=OUT + "c2-after-personal-yield.png")
    page.close()

    # --- Back return, normal + throttled ---
    for label, throttle in [("normal", False), ("throttled", True)]:
        page = ctx.new_page()
        if throttle:
            page.route("**/*", lambda route: (page.wait_for_timeout(250), route.continue_()))
        page.goto(URL, timeout=180000)
        page.wait_for_timeout(9000); dismiss_install(page); page.wait_for_timeout(3000)
        fresh = controls(page)
        print(f"back {label}: fresh controls={fresh}", flush=True)
        page.screenshot(path=OUT + f"c2-back-{label}-fresh.png")
        # leave via WORLDS tile; fall back to Go to the Hub link
        left = False
        try:
            w = page.get_by_text("WORLDS", exact=True).first
            w.scroll_into_view_if_needed(timeout=8000)
            raw_tap(page, w)
            page.wait_for_timeout(6000)
            print(f"back {label}: after WORLDS url={page.url}", flush=True)
            left = True
        except Exception as e:
            print(f"back {label}: WORLDS tap failed:", str(e)[:120], flush=True)
        if not left:
            try:
                g = page.get_by_text("Go to the Hub", exact=True).first
                g.scroll_into_view_if_needed(timeout=8000)
                raw_tap(page, g)
                page.wait_for_timeout(6000)
                print(f"back {label}: after Go-to-Hub url={page.url}", flush=True)
            except Exception as e:
                print(f"back {label}: Go-to-Hub tap failed:", str(e)[:120], flush=True)
        page.go_back(timeout=60000)
        page.wait_for_timeout(5000)
        c5 = controls(page)
        m5 = markers(page)
        page.screenshot(path=OUT + f"c2-back-{label}-after-back.png")
        page.wait_for_timeout(10000)
        c15 = controls(page)
        m15 = markers(page)
        print(f"back {label}: @5s controls={c5} markers={m5} url={page.url}", flush=True)
        print(f"back {label}: @15s controls={c15} markers={m15}", flush=True)
        page.screenshot(path=OUT + f"c2-back-{label}-after-back-15s.png")
        print(f"back {label}: {'PASS' if c15 > 700 and all(m15.values()) else 'CHECK'}", flush=True)
        page.close()
    print("LEG2 DONE", flush=True)
    b.close()
