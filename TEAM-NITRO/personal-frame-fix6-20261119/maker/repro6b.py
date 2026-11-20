"""Fix-6 repro B: capture stack trace of the NAVIGATE(/hub/feed) that follows the ask click."""
from playwright.sync_api import sync_playwright

BASE = ("https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/"
        "personal-page-complete-20261113/personal-complete.html"
        "&ref=personal/frame-round-fix5-20261119"
        "&cb=dedf0b19057b4396572d8b1963352f0744c32439&owner=flagship-personal")
EYE = "/home/hatch/workspace/team-nitro/personal-frame-fix6-20261119/maker"

INIT = r"""
window.__plog = [];
function __log(m){ try{ window.__plog.push(Date.now()%100000 + ' ' + m); var d=document.getElementById('__probeLog'); if(d) d.textContent = window.__plog.join('\n'); }catch(e){} }
(function(){
  var tries = 0;
  var t = setInterval(function(){
    tries++;
    if (window.NayaRouter && !window.NayaRouter.__wrapped) {
      var R = window.NayaRouter;
      R.__wrapped = true;
      var nav = R.navigate.bind(R);
      R.navigate = function(p){
        var st = ''; try { st = new Error('trace').stack.split('\n').slice(1,7).join(' | '); } catch(e){}
        __log('NAVIGATE(' + p + ') from hash=' + location.hash + ' STACK: ' + st);
        return nav(p);
      };
      __log('WRAPPED NayaRouter');
      clearInterval(t);
    }
    if (tries > 200) clearInterval(t);
  }, 100);
})();
document.addEventListener('DOMContentLoaded', function(){
  var d = document.createElement('pre');
  d.id = '__probeLog'; d.style.cssText = 'position:fixed;left:0;top:0;z-index:999999;background:#fff;color:#000;font-size:9px;max-height:60vh;overflow:auto;display:none';
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

def main():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = ctx.new_page()
        page.add_init_script(INIT)
        page.goto(BASE, wait_until="domcontentloaded", timeout=120000)
        page.wait_for_timeout(8000)
        dismiss_modal(page)
        ask = page.get_by_role("button", name="Ask Naya")
        bb = ask.bounding_box(timeout=8000)
        page.mouse.click(bb["x"] + bb["width"]/2, bb["y"] + bb["height"]/2)
        page.wait_for_timeout(5000)
        print("url tail:", page.url[-50:], "room:", page.locator(".naya-ask-room").count(), flush=True)
        print(page.locator("#__probeLog").inner_text(), flush=True)
        browser.close()

main()
