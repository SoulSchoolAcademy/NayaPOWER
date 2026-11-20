# CHECKER leg 4 — Chromium 1920 via localhost forwarder: Ask Naya + Back return + PERSONAL yield.
import subprocess, time, os, signal
from playwright.sync_api import sync_playwright

URL = "https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/frame-round-fix6-20261119&cb=8fbec9580c078b97d0881f7aa20d8c92ce41d9d6&owner=flagship-personal"
OUT = "/home/hatch/workspace/team-nitro/personal-frame-fix6-20261119/checker/"
FWD = "/home/hatch/workspace/project-intelligence/proof/pi-h1-evidence/h1-proxy-forwarder.py"

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

fwd = subprocess.Popen(["python3", FWD], stdout=open(OUT + "c4-forwarder.log", "w"), stderr=subprocess.STDOUT)
print("forwarder pid:", fwd.pid, flush=True)
time.sleep(3)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, proxy={"server": "http://127.0.0.1:18080"}, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 1920, "height": 1080}, ignore_https_errors=True)
        page = ctx.new_page()
        page.goto(URL, timeout=120000)
        page.wait_for_timeout(9000)
        dismiss_install(page)
        page.wait_for_timeout(3000)
        print("chromium loaded title:", page.title(), "room:", room(page), flush=True)
        page.screenshot(path=OUT + "c4-chromium-fresh.png")
        # Ask Naya
        ask = page.locator('.hub-obsidian-btn[aria-label="Ask Naya"]')
        print("ask btn count:", ask.count(), flush=True)
        raw_tap(page, ask.first)
        for t in (2, 5, 10):
            page.wait_for_timeout(2000 if t == 2 else 3000 if t == 5 else 5000)
            print(f"chromium ask t+{t}s room={room(page)} url={page.url.split('#')[-1]} title={page.title()}", flush=True)
        page.screenshot(path=OUT + "c4-chromium-ask-room.png")
        # PERSONAL yield
        tabs = page.get_by_text("PERSONAL", exact=True)
        yielded = False
        for i in range(tabs.count()):
            try:
                tabs.nth(i).scroll_into_view_if_needed(timeout=5000)
                raw_tap(page, tabs.nth(i))
                page.wait_for_timeout(3000)
                print(f"  PERSONAL [{i}]: room={room(page)} hash={page.url.split('#')[-1]}", flush=True)
                if room(page) == 0 and page.url.split("#")[-1] == "/hub/feed":
                    yielded = True
                    break
            except Exception as e:
                print(f"  PERSONAL [{i}] tap failed:", str(e)[:100], flush=True)
        print("CHROMIUM PERSONAL YIELD:", "PASS" if yielded else "FAIL", flush=True)
        page.screenshot(path=OUT + "c4-after-personal-yield.png")
        # Back return
        fresh = controls(page)
        print("chromium back: fresh controls=", fresh, flush=True)
        try:
            w = page.get_by_text("WORLDS", exact=True).first
            w.scroll_into_view_if_needed(timeout=8000)
            raw_tap(page, w)
            page.wait_for_timeout(6000)
            print("chromium back: after WORLDS url=", page.url, flush=True)
        except Exception as e:
            print("chromium WORLDS tap failed:", str(e)[:120], flush=True)
            g = page.get_by_text("Go to the Hub", exact=True).first
            g.scroll_into_view_if_needed(timeout=8000)
            raw_tap(page, g)
            page.wait_for_timeout(6000)
            print("chromium back: after Go-to-Hub url=", page.url, flush=True)
        page.go_back(timeout=60000)
        page.wait_for_timeout(5000)
        c5 = controls(page)
        page.screenshot(path=OUT + "c4-chromium-after-back.png")
        page.wait_for_timeout(10000)
        c15 = controls(page)
        print(f"chromium back: @5s={c5} @15s={c15}", flush=True)
        page.screenshot(path=OUT + "c4-chromium-after-back-15s.png")
        print("CHROMIUM BACK:", "PASS" if c15 > 700 else "CHECK", flush=True)
        print("LEG4 DONE", flush=True)
        b.close()
finally:
    fwd.terminate()
    try: fwd.wait(timeout=10)
    except Exception: fwd.kill()
    print("forwarder killed", flush=True)
