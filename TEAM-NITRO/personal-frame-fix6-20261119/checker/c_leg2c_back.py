# CHECKER leg 2c — Back return redo: WORLDS via locator click with 120 s timeout,
# fallback raw mouse click after scrolling back to top (bar refolds on scroll).
import time
from playwright.sync_api import sync_playwright

URL = "https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/frame-round-fix6-20261119&cb=8fbec9580c078b97d0881f7aa20d8c92ce41d9d6&owner=flagship-personal"
OUT = "/home/hatch/workspace/team-nitro/personal-frame-fix6-20261119/checker/"

def controls(page): return page.locator("button, a, input, [role=button]").count()
def dismiss_modal(page):
    for _ in range(25):
        try:
            if page.locator("#naya-install-overlay.show").count() == 0:
                return True
            page.get_by_text("Not now", exact=True).click(timeout=2000)
        except Exception:
            pass
        page.wait_for_timeout(1000)
    return page.locator("#naya-install-overlay.show").count() == 0
def markers(page):
    out = {}
    for name, sel in [("quote", "text=NayaNET — create, learn and grow together"),
                      ("personal", "text=PERSONAL"), ("empty", "text=Nothing here yet."),
                      ("ask", "text=Ask Naya"), ("name", "text=Shawn Vibert")]:
        try: out[name] = page.locator(sel).first.is_visible(timeout=2000)
        except Exception: out[name] = False
    return out

def leave_via_worlds(page, tag):
    loc = page.get_by_text("WORLDS", exact=True)
    print(f"[{tag}] WORLDS count:", loc.count(), flush=True)
    try:
        loc.first.click(timeout=120000)
        print(f"[{tag}] tapped WORLDS via locator", flush=True)
    except Exception as e:
        print(f"[{tag}] locator click timed out, fallback raw click:", str(e)[:100], flush=True)
        page.mouse.move(960, 500)
        page.mouse.wheel(0, -10000)
        page.wait_for_timeout(4000)
        bb = loc.first.bounding_box(timeout=15000)
        print(f"[{tag}] WORLDS box after scroll-top: {bb}", flush=True)
        page.mouse.click(bb["x"] + bb["width"]/2, bb["y"] + bb["height"]/2)
        print(f"[{tag}] tapped WORLDS via raw click", flush=True)
    try:
        page.wait_for_url("**nayanet.app/space**", timeout=120000)
        print(f"[{tag}] landed on space: {page.url}", flush=True)
        return True
    except Exception:
        print(f"[{tag}] did NOT land on /space, url={page.url[:140]}", flush=True)
        return False

with sync_playwright() as p:
    b = p.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1920, "height": 1080})
    for tag, throttled in [("normal", False), ("throttled", True)]:
        page = ctx.new_page()
        if throttled:
            def slow(route):
                time.sleep(0.25)
                route.continue_()
            page.route("**/*", slow)
        page.goto(URL, wait_until="domcontentloaded", timeout=180000)
        page.wait_for_timeout(8000)
        print(f"[{tag}] modal dismissed:", dismiss_modal(page), flush=True)
        page.wait_for_timeout(3000)
        fresh = controls(page)
        print(f"[{tag}] FRESH controls={fresh} markers={markers(page)}", flush=True)
        page.screenshot(path=OUT + f"c2c-back-{tag}-fresh.png")
        page.mouse.wheel(0, 5000); page.wait_for_timeout(1500)
        page.mouse.wheel(0, 5000); page.wait_for_timeout(3000)
        left = leave_via_worlds(page, tag)
        page.wait_for_timeout(4000)
        page.go_back(timeout=60000)
        page.wait_for_timeout(6000)
        print(f"[{tag}] modal dismissed after back:", dismiss_modal(page), flush=True)
        page.wait_for_timeout(3000)
        c5 = controls(page); m5 = markers(page)
        print(f"[{tag}] AFTER-BACK controls={c5} markers={m5} url={page.url[:120]}", flush=True)
        page.screenshot(path=OUT + f"c2c-back-{tag}-after-back.png")
        page.wait_for_timeout(10000)
        c15 = controls(page); m15 = markers(page)
        print(f"[{tag}] AFTER-BACK-15s controls={c15} markers={m15}", flush=True)
        page.screenshot(path=OUT + f"c2c-back-{tag}-after-back-15s.png")
        print(f"[{tag}] BACK RETURN:", "PASS" if left and c15 > 700 and all(m15.values()) else "FAIL/CHECK", flush=True)
        page.close()
    print("LEG2C DONE", flush=True)
    b.close()
