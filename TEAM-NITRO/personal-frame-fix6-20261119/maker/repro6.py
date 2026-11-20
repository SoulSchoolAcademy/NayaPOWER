"""Fix-6 repro: instrument hash changes + Router calls, tap Ask Naya, log what happens."""
from playwright.sync_api import sync_playwright

BASE = ("https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/"
        "personal-page-complete-20261113/personal-complete.html"
        "&ref=personal/frame-round-fix5-20261119"
        "&cb=dedf0b19057b4396572d8b1963352f0744c32439&owner=flagship-personal")
EYE = "/home/hatch/workspace/team-nitro/personal-frame-fix6-20261119/maker"

INIT = r"""
window.__plog = [];
function __log(m){ try{ window.__plog.push(Date.now()%100000 + ' ' + m); var d=document.getElementById('__probeLog'); if(d) d.textContent = window.__plog.join('\n'); }catch(e){} }
window.addEventListener('hashchange', function(){ __log('HASHCHANGE -> ' + location.hash); });
(function(){
  var tries = 0;
  var t = setInterval(function(){
    tries++;
    if (window.NayaRouter && !window.NayaRouter.__wrapped) {
      var R = window.NayaRouter;
      R.__wrapped = true;
      var nav = R.navigate.bind(R);
      R.navigate = function(p){ __log('NAVIGATE(' + p + ') from hash=' + location.hash); return nav(p); };
      var ren = R.render.bind(R);
      R.render = function(){ __log('RENDER() hash=' + location.hash); var v = ren(); __log('RENDERED hash=' + location.hash + ' room=' + document.querySelectorAll('.naya-ask-room').length + ' title=' + document.title); return v; };
      __log('WRAPPED NayaRouter');
      clearInterval(t);
    }
    if (tries > 200) clearInterval(t);
  }, 100);
})();
document.addEventListener('DOMContentLoaded', function(){
  var d = document.createElement('pre');
  d.id = '__probeLog'; d.style.cssText = 'position:fixed;left:0;top:0;z-index:999999;background:#fff;color:#000;font-size:9px;max-height:40vh;overflow:auto;display:none';
  document.body.appendChild(d);
});
"""

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

def plog(page):
    try:
        return page.locator("#__probeLog").inner_text()
    except Exception as e:
        return f"<plog unreadable: {e}>"

def main():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = ctx.new_page()
        page.add_init_script(INIT)
        page.goto(BASE, wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(8000)
        print("modal dismissed:", dismiss_modal(page), flush=True)
        print("hash at start:", page.url.split('?file=')[0][-40:], "| hash:", page.evaluate("location.hash") if False else "(skip)", flush=True)
        ask = page.get_by_role("button", name="Ask Naya")
        print("ask button count:", ask.count(), flush=True)
        bb = ask.bounding_box(timeout=8000)
        print("ask box:", bb, flush=True)
        page.mouse.click(bb["x"] + bb["width"]/2, bb["y"] + bb["height"]/2)
        for t in (2, 5, 10):
            page.wait_for_timeout(t*1000 if t==2 else (t-2)*1000 if t==5 else 5000)
            room = page.locator(".naya-ask-room").count()
            print(f"@{t}s url tail={page.url[-60:]} room={room}", flush=True)
        page.screenshot(path=EYE + "/r6-ask-after-click.png")
        print("---- PLOG ----", flush=True)
        print(plog(page), flush=True)
        # second click
        bb2 = ask.bounding_box(timeout=8000)
        if bb2:
            page.mouse.click(bb2["x"] + bb2["width"]/2, bb2["y"] + bb2["height"]/2)
            page.wait_for_timeout(5000)
            print("after 2nd click url tail:", page.url[-60:], "room:", page.locator(".naya-ask-room").count(), flush=True)
            print("---- PLOG2 ----", flush=True)
            print(plog(page), flush=True)
        browser.close()

main()
