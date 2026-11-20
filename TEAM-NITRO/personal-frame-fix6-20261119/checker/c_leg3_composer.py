# CHECKER leg 3 — composer landings 6/6 on FRESH loads (Firefox 1920).
# Fresh context per suffix; composer judged by hidden attr + body.fc-open (is_visible false-negatives).
from playwright.sync_api import sync_playwright

BASE = "https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/frame-round-fix6-20261119&cb=8fbec9580c078b97d0881f7aa20d8c92ce41d9d6&owner=flagship-personal"
OUT = "/home/hatch/workspace/team-nitro/personal-frame-fix6-20261119/checker/"
SUFFIXES = ["#home/composer", "#home/post", "#home/naya", "#home/smart", "#home", "#about"]

def dismiss_install(page):
    try:
        btn = page.get_by_role("button", name="Not now")
        if btn.count():
            btn.first.click(timeout=10000, force=True)
    except Exception:
        pass

with sync_playwright() as p:
    b = p.firefox.launch(headless=True)
    results = {}
    for i, suf in enumerate(SUFFIXES):
        ctx = b.new_context(viewport={"width": 1920, "height": 1080})
        page = ctx.new_page()
        page.add_init_script("window.__c6log=[]; window.addEventListener('hashchange',()=>window.__c6log.push(location.hash));")
        page.goto(BASE + suf, timeout=120000)
        page.wait_for_timeout(8000)
        dismiss_install(page)
        page.wait_for_timeout(5000)
        fc = page.locator("#fcCreator")
        hidden = fc.get_attribute("hidden") if fc.count() else "NO-ELEMENT"
        body_cls = page.locator("body").get_attribute("class") or ""
        open_state = (hidden is None) and ("fc-open" in body_cls)
        # mode label text if open
        mode = ""
        try:
            mode = page.locator("#fcCreator").inner_text(timeout=3000)[:120].replace("\n", " | ")
        except Exception:
            mode = "(no text read)"
        print(f"{suf}: open={open_state} hidden={hidden!r} fc-open={'fc-open' in body_cls} :: {mode}", flush=True)
        results[suf] = open_state
        page.screenshot(path=OUT + f"c3-composer-{i}.png")
        ctx.close()
    expect_open = {"#home/composer", "#home/post", "#home/naya", "#home/smart"}
    ok = all(results[s] for s in expect_open) and not results["#home"] and not results["#about"]
    print("COMPOSER 6/6:", "PASS" if ok else "FAIL", results, flush=True)
    print("LEG3 DONE", flush=True)
    b.close()
