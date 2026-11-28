# FIX4 debug 2 — watch the city wrap flip: what sets mode=text, and when?
from playwright.sync_api import sync_playwright
BASE = "https://official-walkthrough-staging.nayapower.workers.dev"
with sync_playwright() as pw:
    b = pw.chromium.launch(proxy={"server": "http://127.0.0.1:18080"})
    ctxP = b.new_context(viewport={"width": 390, "height": 844}, ignore_https_errors=True)
    pp = ctxP.new_page()
    pp.add_init_script("""
      localStorage.setItem('nayanet_smart_alias', 'shawn');
      localStorage.setItem('nayanet_smart_name', 'Shawn');
      localStorage.setItem('nayanet_smart_identities', JSON.stringify([{alias:'shawn',name:'Shawn'},{alias:'friend',name:'Friend'}]));
    """)
    pp.goto(BASE + "/?walk=1&name=Shawn&alias=shawn", wait_until="domcontentloaded", timeout=120000)
    pp.wait_for_timeout(2000)
    pp.evaluate("""() => {
      window.__log = [];
      const cw = document.querySelector('[data-fid="city"]').closest('.bd-field');
      const pw2 = document.querySelector('[data-fid="province"]').closest('.bd-field');
      const obs = new MutationObserver((muts) => {
        muts.forEach(m => window.__log.push(performance.now().toFixed(0) + 'ms ' + (m.target === cw ? 'CITY' : 'PROV') + ' ' + m.attributeName + '=' + m.target.getAttribute(m.attributeName)));
      });
      obs.observe(cw, {attributes: true});
      obs.observe(pw2, {attributes: true});
      window.__cw = cw; window.__pw = pw2;
    }""")
    pp.select_option('[data-fid="country"]', "canada")
    pp.wait_for_timeout(400)
    print("after country:", pp.evaluate("() => ({log: window.__log, cityMode: window.__cw.getAttribute('data-cascade-mode'), provMode: window.__pw.getAttribute('data-cascade-mode')})"), flush=True)
    pp.evaluate("() => { window.__log = []; }")
    pp.select_option('[data-fid="province"]', "ontario")
    for ms in (50, 150, 400):
        pp.wait_for_timeout(ms if ms == 50 else ms - 50 if ms == 150 else 250)
        print(f"after province +{ms}ms:", pp.evaluate("() => ({log: window.__log, cityMode: window.__cw.getAttribute('data-cascade-mode'), cityHidden: window.__cw.classList.contains('bd-cascade-hidden'), cityOpts: [...document.querySelector('[data-fid=city]').options].map(o => o.value), provVal: document.querySelector('[data-fid=province]').value, provMode: window.__pw.getAttribute('data-cascade-mode'), answers: JSON.parse(localStorage.getItem('naya_welcome_right_v1') || '{}').answers})"), flush=True)
    b.close()
print("DEBUG2 DONE")
