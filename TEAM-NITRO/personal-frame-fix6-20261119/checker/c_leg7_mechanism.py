# CHECKER mechanism probe — log popstate/hashchange + room state on FIXED vs BASE
# staged bytes, Firefox 1920. Events are written into a DOM node (evaluate fails in FF).
from playwright.sync_api import sync_playwright

FIXED = "https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/frame-round-fix6-20261119&cb=8fbec9580c078b97d0881f7aa20d8c92ce41d9d6&owner=flagship-personal"
BASE = "https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/personal-complete.html&ref=personal/frame-round-fix5-20261119&cb=dedf0b19057b4396572d8b1963352f0744c32439&owner=flagship-personal"
OUT = "/home/hatch/workspace/team-nitro/personal-frame-fix6-20261119/checker/"

INIT = """
window.__ev = [];
function __logEv(kind){ try {
  var d = document.getElementById('chk-ev');
  if (d) d.textContent += kind + ' hash=' + location.hash + ' room=' + document.querySelectorAll('.naya-ask-room').length + ' t=' + Math.round(performance.now()) + '\\n';
} catch(e){} }
window.addEventListener('popstate', function(){ __logEv('POPSTATE'); });
window.addEventListener('hashchange', function(){ __logEv('HASHCHANGE'); });
document.addEventListener('DOMContentLoaded', function(){
  var d = document.createElement('div'); d.id = 'chk-ev'; d.style.display = 'none';
  document.body.appendChild(d);
});
"""

def dismiss_install(page):
    try:
        btn = page.get_by_role("button", name="Not now")
        if btn.count():
            btn.first.click(timeout=10000, force=True)
    except Exception:
        pass

def run(p, label, url):
    b = p.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1920, "height": 1080})
    page = ctx.new_page()
    page.add_init_script(INIT)
    page.goto(url, wait_until="domcontentloaded", timeout=120000)
    page.wait_for_timeout(9000)
    dismiss_install(page)
    page.wait_for_timeout(3000)
    ask = page.locator('.hub-obsidian-btn[aria-label="Ask Naya"]')
    bb = ask.first.bounding_box(timeout=15000)
    page.mouse.click(bb["x"] + bb["width"]/2, bb["y"] + bb["height"]/2)
    page.wait_for_timeout(6000)
    ev = page.locator("#chk-ev").inner_text(timeout=5000)
    print(f"===== {label} =====", flush=True)
    print(ev, flush=True)
    print(f"{label}: final room={page.locator('.naya-ask-room').count()} hash={page.url.split('#')[-1]}", flush=True)
    page.screenshot(path=OUT + f"c7-mech-{label.lower()}.png")
    b.close()

with sync_playwright() as p:
    run(p, "FIXED", FIXED)
    run(p, "BASE", BASE)
print("LEG7 DONE")
