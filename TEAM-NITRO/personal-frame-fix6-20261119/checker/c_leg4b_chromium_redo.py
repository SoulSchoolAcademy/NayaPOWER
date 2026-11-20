# CHECKER leg 4b (REDO) — Chromium 1920: PERSONAL yield (wheel-scroll method) +
# Back return (fresh page, WORLDS locator click, wait for /space, go_back).
import subprocess, time
from playwright.sync_api import sync_playwright

URL = "https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/frame-round-fix6-20261119&cb=8fbec9580c078b97d0881f7aa20d8c92ce41d9d6&owner=flagship-personal"
OUT = "/home/hatch/workspace/team-nitro/personal-frame-fix6-20261119/checker/"
FWD = "/home/hatch/workspace/project-intelligence/proof/pi-h1-evidence/h1-proxy-forwarder.py"

def room(page): return page.locator(".naya-ask-room").count()
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

fwd = subprocess.Popen(["python3", FWD], stdout=open(OUT + "c4b-forwarder.log", "w"), stderr=subprocess.STDOUT)
print("forwarder pid:", fwd.pid, flush=True)
time.sleep(3)
try:
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, proxy={"server": "http://127.0.0.1:18080"}, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 1920, "height": 1080}, ignore_https_errors=True)

        # --- PERSONAL yield, wheel-scroll method ---
        page = ctx.new_page()
        page.goto(URL, wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(9000)
        print("modal dismissed:", dismiss_modal(page), flush=True)
        page.wait_for_timeout(3000)
        ask = page.locator('.hub-obsidian-btn[aria-label="Ask Naya"]')
        bb = ask.first.bounding_box(timeout=15000)
        page.mouse.click(bb["x"] + bb["width"]/2, bb["y"] + bb["height"]/2)
        page.wait_for_timeout(5000)
        print("chromium yield: room before PERSONAL:", room(page), "hash:", page.url.split("#")[-1], flush=True)
        page.mouse.move(960, 500)
        for _ in range(3):
            page.mouse.wheel(0, 700)
            page.wait_for_timeout(1000)
        tab = page.get_by_text("PERSONAL", exact=True)
        print("PERSONAL matches:", tab.count(), flush=True)
        for i in range(tab.count()):
            try: tb = tab.nth(i).bounding_box(timeout=4000)
            except Exception: tb = None
            print(f"  tab [{i}] box={tb}", flush=True)
            if tb and 0 <= tb["x"] <= 1900 and 0 <= tb["y"] <= 1040:
                page.mouse.click(tb["x"] + tb["width"]/2, tb["y"] + tb["height"]/2)
                print(f"tapped PERSONAL tab [{i}]", flush=True)
                break
        page.wait_for_timeout(4000)
        print(f"chromium after PERSONAL: room={room(page)} hash={page.url.split('#')[-1]}", flush=True)
        print("CHROMIUM PERSONAL YIELD:", "PASS" if room(page) == 0 and page.url.split("#")[-1] == "/hub/feed" else "FAIL", flush=True)
        page.screenshot(path=OUT + "c4b-after-personal-yield.png")
        page.close()

        # --- Back return, fresh page, maker method ---
        page = ctx.new_page()
        page.goto(URL, wait_until="domcontentloaded", timeout=180000)
        page.wait_for_timeout(9000)
        print("modal dismissed:", dismiss_modal(page), flush=True)
        page.wait_for_timeout(3000)
        fresh = controls(page)
        print(f"chromium back FRESH controls={fresh} markers={markers(page)}", flush=True)
        page.screenshot(path=OUT + "c4b-chromium-fresh.png")
        page.mouse.wheel(0, 5000); page.wait_for_timeout(1500)
        page.mouse.wheel(0, 5000); page.wait_for_timeout(3000)
        loc = page.get_by_text("WORLDS", exact=True)
        print("WORLDS count:", loc.count(), flush=True)
        loc.first.click(timeout=120000)
        print("tapped WORLDS via locator", flush=True)
        try:
            page.wait_for_url("**nayanet.app/space**", timeout=120000)
            print("landed on space:", page.url, flush=True)
            left = True
        except Exception:
            print("did NOT land on /space, url=", page.url[:140], flush=True)
            left = False
        page.wait_for_timeout(4000)
        page.go_back(timeout=60000)
        page.wait_for_timeout(6000)
        print("modal dismissed after back:", dismiss_modal(page), flush=True)
        page.wait_for_timeout(3000)
        c5 = controls(page); m5 = markers(page)
        print(f"chromium back AFTER-BACK controls={c5} markers={m5}", flush=True)
        page.screenshot(path=OUT + "c4b-chromium-after-back.png")
        page.wait_for_timeout(10000)
        c15 = controls(page); m15 = markers(page)
        print(f"chromium back AFTER-BACK-15s controls={c15} markers={m15}", flush=True)
        page.screenshot(path=OUT + "c4b-chromium-after-back-15s.png")
        print("CHROMIUM BACK RETURN:", "PASS" if left and c15 > 700 and all(m15.values()) else "FAIL/CHECK", flush=True)
        print("LEG4B DONE", flush=True)
        b.close()
finally:
    fwd.terminate()
    try: fwd.wait(timeout=10)
    except Exception: fwd.kill()
    print("forwarder killed", flush=True)
