#!/usr/bin/env python3
"""AUTO-TRANSLATE repaint-resilience proof (fresh maker, 2026-11-13).
The wall repaints once after load when the live rows land (mwPaintWallPosts
list.innerHTML) — a tap made before that repaint must survive it.
Flow: load, insert an ES stub EARLY (3s), tap Translate, pick Español,
then poll the picker + the finished view every 500ms for 25s across the
repaint. PASS = the view is present at the end AND was present in the last
polls, with the picker re-appearing if the repaint hit mid-pick. Records
the repaint moment (wall childList swap) and any gap."""
import json
from playwright.sync_api import sync_playwright
URL = 'file:///home/hatch/workspace/personal-complete-wt/TEAM-NITRO/personal-page-complete-20261113/personal-complete.html'
WORK = '/home/hatch/workspace/team-nitro/auto-translate-20261113/'
R = {}
with sync_playwright() as pw:
    br = pw.firefox.launch()
    ctx = br.new_context(viewport={'width': 390, 'height': 844})
    p = ctx.new_page()
    pe = []
    p.on('pageerror', lambda e: pe.append(str(e)))
    p.goto(URL, wait_until='domcontentloaded', timeout=60000)
    p.wait_for_timeout(3000)
    p.evaluate("""() => {
      window.__t0=Date.now(); window.__repaints=[];
      var list=document.getElementById('os-wall-list');
      new MutationObserver(function(ms){ ms.forEach(function(m){
        if(m.target===list && m.removedNodes.length) window.__repaints.push(Date.now()-window.__t0);
      }); }).observe(list,{childList:true});
    }""")
    R['stub'] = p.evaluate("() => window.fcStubInsert({k:'wall', a:'Sofía', b:'El sol sale sobre la ciudad y todo se llena de luz. Caminamos juntos por el mercado, probando el pan y hablando del futuro. La vida es mejor cuando se comparte.', noteType:'naya'})")
    p.wait_for_timeout(800)
    p.evaluate("() => { var b=document.querySelector('[data-fc-stub] .mw-tr-btn'); if(b) b.click(); }")
    p.wait_for_timeout(700)
    R['picker_after_tap'] = p.evaluate("() => !!document.querySelector('[data-fc-stub] .mw-tr-pick')")
    p.evaluate("() => { var b=[...document.querySelectorAll('[data-fc-stub] .mw-tr-lang')].find(x=>x.textContent.trim()==='Español'); if(b) b.click(); }")
    hist = []
    for i in range(50):
        p.wait_for_timeout(500)
        hist.append(p.evaluate("""() => { var c=document.querySelector('[data-fc-stub]');
          if(!c) return 'nocard';
          var v=c.querySelector('.mw-tr-view:not(.mw-tr-collapsed)');
          var pk=!!c.querySelector('.mw-tr-pick');
          return (v?'V':'-')+(pk?'P':'-'); }"""))
    R['timeline_500ms_x50'] = ''.join(hist)
    R['view_at_end'] = p.evaluate("""() => { var v=document.querySelector('[data-fc-stub] .mw-tr-view');
      return v ? v.textContent.slice(0,200) : null; }""")
    R['repaints_ms_after_stub'] = p.evaluate("() => window.__repaints")
    R['page_errors'] = pe
    p.evaluate("() => { var c=document.querySelector('[data-fc-stub]'); if(c) c.scrollIntoView(); }")
    p.wait_for_timeout(400)
    p.screenshot(path=WORK + 'proof-390-repaint-view.png')
    br.close()
json.dump(R, open(WORK + 'verify-repaint-390.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
