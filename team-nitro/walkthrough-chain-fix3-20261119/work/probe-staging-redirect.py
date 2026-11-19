import json
from playwright.sync_api import sync_playwright
with sync_playwright() as pw:
    b = pw.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1920, "height": 999})
    p = ctx.new_page()
    p.goto("https://naya-walk-beginning-staging.nayapower.workers.dev/identity.html", wait_until="load", timeout=60000)
    p.wait_for_timeout(2000)
    p.fill("#aliasInput", "fix3redirect")
    p.wait_for_timeout(1800)
    print("before ENTER:", p.evaluate("() => ({status: document.querySelector('#aliasStatus') ? document.querySelector('#aliasStatus').textContent.trim() : null})"))
    p.query_selector("button:has-text('ENTER')").click()
    p.wait_for_timeout(5000)
    print("after ENTER:", p.evaluate("""() => ({url: location.href,
      bodyStart: document.body.innerText.slice(0, 200),
      lsName: (() => { try { return localStorage.getItem('nayanet_smart_name'); } catch(e){ return 'ERR'; } })()})"""))
    b.close()
