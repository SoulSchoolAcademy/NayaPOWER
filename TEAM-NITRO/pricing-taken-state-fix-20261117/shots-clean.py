import os
from playwright.sync_api import sync_playwright
HERE=os.path.dirname(os.path.abspath(__file__)); SD=os.path.join(HERE,"shots-after2")
FREE="https://naya-pricing-free-staging.nayapower.workers.dev/free"
ALIAS="alexanderchristopherbennett"
def settle(page):
    try:
        if page.evaluate("!document.getElementById('installVeil').hidden"):
            page.click("#installLater", timeout=3000); page.wait_for_timeout(400); return True
    except Exception: pass
    return False
with sync_playwright() as pw:
    # 635 scrolled, veil dismissed right before the shot
    b=pw.chromium.launch(headless=True, proxy={"server":"http://127.0.0.1:18080"})
    ctx=b.new_context(viewport={"width":635,"height":349}, ignore_https_errors=True)
    p=ctx.new_page(); p.goto(FREE, wait_until="load", timeout=60000); p.wait_for_timeout(1500)
    settle(p); p.fill("#aliasInput", ALIAS)
    p.wait_for_function("document.getElementById('aliasStatus').getAttribute('data-state')==='taken'", timeout=15000)
    p.wait_for_timeout(800); settle(p)
    p.mouse.move(317,174)
    for _ in range(4): p.mouse.wheel(0,400); p.wait_for_timeout(250)
    settle(p)
    m=p.evaluate("()=>({enter:document.getElementById('enterBtn').getBoundingClientRect().toJSON(), winY:window.scrollY, plaqueTop:document.getElementById('certPlaque').scrollTop})")
    print("635 scrolled:", m)
    p.screenshot(path=os.path.join(SD,"taken-long-635x349-scrolled-clean.png"))
    b.close()
    # 1440 load, veil dismissed right before the shot
    b=pw.chromium.launch(headless=True, proxy={"server":"http://127.0.0.1:18080"})
    ctx=b.new_context(viewport={"width":1440,"height":900}, ignore_https_errors=True)
    p=ctx.new_page(); p.goto(FREE, wait_until="load", timeout=60000); p.wait_for_timeout(1500)
    settle(p); p.fill("#aliasInput", ALIAS)
    p.wait_for_function("document.getElementById('aliasStatus').getAttribute('data-state')==='taken'", timeout=15000)
    p.wait_for_timeout(800); settle(p)
    p.screenshot(path=os.path.join(SD,"taken-long-1440x900-load-clean.png"))
    print("1440 load shot saved")
    b.close()
