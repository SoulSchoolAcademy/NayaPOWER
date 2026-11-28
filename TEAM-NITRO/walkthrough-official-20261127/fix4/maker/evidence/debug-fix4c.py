# FIX4 debug 3 — capture-phase spy: province value + city mode BEFORE/AFTER
# the page's own change handlers run, on the country change.
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
      window.__spy = [];
      const fe = document.querySelector('#bdSingle .bd-fields');
      const snap = (tag) => {
        const prov = document.querySelector('[data-fid="province"]');
        const city = document.querySelector('[data-fid="city"]');
        window.__spy.push(tag + ' provVal=' + (prov ? prov.value : 'NONE') + ' provOpts=' + (prov ? prov.options.length : 0) + ' cityMode=' + (city ? city.closest('.bd-field').getAttribute('data-cascade-mode') : 'NONE') + ' cityOpts=' + (city ? city.options.length : 0));
      };
      fe.addEventListener('change', () => snap('CAPTURE-change'), true);
      fe.addEventListener('change', () => snap('BUBBLE-change'), false);
      fe.addEventListener('input', () => snap('CAPTURE-input'), true);
      // Re-implement parentValue from the live QUESTIONS + DOM.
      window.__pv = (fid) => {
        const step = window.QUESTIONS[0];
        const byId = {}; step.fields.forEach(f => byId[f.id] = f);
        const pf = byId[fid]; if (!pf) return 'NOFIELD';
        const sel = fe.querySelector('[data-fid="' + fid + '"]');
        if (!sel) return 'NOSEL';
        if (pf.cascadeFrom) {
          const wrap = sel.closest('.bd-field');
          const mode = wrap ? wrap.getAttribute('data-cascade-mode') : 'select';
          const o = fe.querySelector('[data-fid="' + fid + '-other"]');
          if (mode === 'text') return 'TEXTMODE:' + (o ? o.value : '?');
          if (sel.value === '__other') return 'OTHER:' + (o ? o.value : '?');
          return 'VAL:' + sel.value;
        }
        return 'PLAIN:' + sel.value;
      };
    }""")
    pp.select_option('[data-fid="country"]', "canada")
    pp.wait_for_timeout(400)
    print("spy:", pp.evaluate("() => window.__spy"), flush=True)
    print("pv(province) now:", pp.evaluate("() => window.__pv('province')"), flush=True)
    print("city map keys:", pp.evaluate("() => Object.keys(window.QUESTIONS[0].fields.find(f => f.id === 'city').cascadeMap)"), flush=True)
    print("live field ids:", pp.evaluate("() => window.QUESTIONS[0].fields.map(f => f.id)"), flush=True)
    b.close()
print("DEBUG3 DONE")
