"""Fix-6 staged regression C (Firefox 1920): composer landings 6/6 on FRESH loads + Academy popup.
Fresh context per suffix (hash-only goto never re-runs boot)."""
from playwright.sync_api import sync_playwright

BASE = ("https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/"
        "personal-page-complete-20261113/personal-complete.html"
        "&ref=personal/frame-round-fix6-20261119"
        "&cb=8fbec9580c078b97d0881f7aa20d8c92ce41d9d6&owner=flagship-personal")
EYE = "/home/hatch/workspace/team-nitro/personal-frame-fix6-20261119/eye"

def dismiss_modal(page):
    for _ in range(10):
        try:
            if page.locator("#naya-install-overlay.show").count() == 0:
                return True
            try:
                page.get_by_text("Not now", exact=True).click(timeout=10000)
            except Exception:
                page.get_by_text("Not now", exact=True).click(timeout=5000, force=True)
        except Exception:
            pass
        page.wait_for_timeout(1000)
    return page.locator("#naya-install-overlay.show").count() == 0

def composer_open(page):
    # fix-5 eye: check hidden attr + body.fc-open, not is_visible()
    try:
        hidden = page.locator("#fcCreator").get_attribute("hidden")
    except Exception:
        hidden = "?"
    try:
        fc = page.evaluate("document.body.classList.contains('fc-open')") if False else "?"
    except Exception:
        fc = "?"
    return hidden, fc

def main():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        cases = [
            ("#home/composer", True, "Naya note"),
            ("#home/post", True, "Make a post"),
            ("#home/naya", True, "Naya note"),
            ("#home/smart", True, "Smart note"),
            ("#home", False, None),
            ("#about", False, None),
        ]
        for i, (suffix, expect_open, mode) in enumerate(cases):
            ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
            page = ctx.new_page()
            page.goto(BASE + suffix, wait_until="domcontentloaded", timeout=120000)
            page.wait_for_timeout(5000)
            dismiss_modal(page)
            page.wait_for_timeout(2000)
            creator = page.locator("#fcCreator")
            hidden = creator.get_attribute("hidden") if creator.count() else "ABSENT"
            body_cls = page.locator("body").get_attribute("class") or ""
            fc_open = "fc-open" in body_cls
            mode_text = ""
            if fc_open:
                try:
                    mode_text = page.locator("#fcCreator").inner_text()[:120].replace("\n", " | ")
                except Exception:
                    mode_text = "?"
            ok = (fc_open == expect_open)
            print(f"[{suffix}] open={fc_open} hidden={hidden} expect={expect_open} {'PASS' if ok else 'FAIL'} mode~{mode_text[:80]}", flush=True)
            page.screenshot(path=EYE + f"/6c-composer-{i}.png")
            ctx.close()
        # Academy popup (fresh context)
        ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = ctx.new_page()
        page.goto(BASE, wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(8000)
        dismiss_modal(page)
        pill = page.locator("a[data-mw-cover='Naya Academy']")
        print("academy pill count:", pill.count(), flush=True)
        if pill.count():
            bb = pill.bounding_box(timeout=8000)
            print("academy pill box:", bb, flush=True)
            try:
                with page.expect_popup(timeout=15000) as pop:
                    page.mouse.click(bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2)
                new_page = pop.value
                new_page.wait_for_timeout(4000)
                print("ACADEMY POPUP URL:", new_page.url, flush=True)
                new_page.screenshot(path=EYE + "/6c-academy-popup.png")
                new_page.close()
            except Exception as e:
                print("ACADEMY popup FAILED:", str(e)[:200], flush=True)
                print("pages in ctx:", [pg.url[:80] for pg in ctx.pages], flush=True)
        print("main page still staged:", "naya-proof-host" in page.url, flush=True)
        browser.close()

main()
