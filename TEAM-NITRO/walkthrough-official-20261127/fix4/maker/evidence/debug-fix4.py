# FIX4 debug — cascade city state + failing request URLs + end-screen state.
from playwright.sync_api import sync_playwright
BASE = "https://official-walkthrough-staging.nayapower.workers.dev"
with sync_playwright() as pw:
    b = pw.chromium.launch(proxy={"server": "http://127.0.0.1:18080"})
    ctxP = b.new_context(viewport={"width": 390, "height": 844}, ignore_https_errors=True)
    pp = ctxP.new_page()
    bad = []
    pp.on("response", lambda r: bad.append((r.status, r.url)) if r.status >= 400 else None)
    pp.on("pageerror", lambda e: print("PAGEERROR", str(e), flush=True))
    pp.add_init_script("""
      localStorage.setItem('nayanet_smart_alias', 'shawn');
      localStorage.setItem('nayanet_smart_name', 'Shawn');
      localStorage.setItem('nayanet_smart_identities', JSON.stringify([{alias:'shawn',name:'Shawn'},{alias:'friend',name:'Friend'}]));
    """)
    pp.goto(BASE + "/?walk=1&name=Shawn&alias=shawn", wait_until="domcontentloaded", timeout=120000)
    pp.wait_for_timeout(2000)
    pp.select_option('[data-fid="country"]', "canada")
    pp.wait_for_timeout(400)
    print("after country:", pp.evaluate("() => ({provHidden: document.querySelector('[data-fid=\"province\"]').closest('.bd-field').classList.contains('bd-cascade-hidden'), provOpts: [...document.querySelectorAll('[data-fid=\"province\"] option')].map(o => o.value)})"), flush=True)
    pp.select_option('[data-fid="province"]', "ontario")
    pp.wait_for_timeout(800)
    print("after province:", pp.evaluate("() => { const c = document.querySelector('[data-fid=\"city\"]'); const w = c.closest('.bd-field'); return {provVal: document.querySelector('[data-fid=\"province\"]').value, cityHidden: w.classList.contains('bd-cascade-hidden'), cityMode: w.getAttribute('data-cascade-mode'), cityOpts: [...c.options].map(o => o.text + '=' + o.value)}; }"), flush=True)
    # Drive to the end, then dump end state + failing requests.
    for _ in range(30):
        if pp.evaluate("() => document.getElementById('bdSingle').hidden"): break
        pp.click("#fpWalkNext", force=True)
        pp.wait_for_timeout(300)
    pp.wait_for_timeout(2000)
    print("end:", pp.evaluate("() => ({singleHidden: document.getElementById('bdSingle').hidden, endHidden: document.getElementById('bdEndPhone').hidden, failLine: (document.getElementById('fpWalkFailLine') || {}).hidden, readyLine: (document.getElementById('fpWalkReadyLine') || {}).hidden, failText: (document.getElementById('fpWalkFailLine') || {}).textContent})"), flush=True)
    print("bad responses:", bad, flush=True)
    b.close()
print("DEBUG DONE")
