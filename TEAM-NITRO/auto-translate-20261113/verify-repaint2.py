#!/usr/bin/env python3
"""AUTO-TRANSLATE repaint-resilience proof 2 (fresh maker, 2026-11-13).
Deterministic: force the page's own repaint (window.mwPaintWallPosts — the
exact list.innerHTML rebuild that killed the picker) while a picker is open,
then again after the translation lands. PASS = picker re-opens on the fresh
node, the translation completes, and the finished view survives the second
repaint."""
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
    p.wait_for_timeout(14000)  # past the natural post-load repaint
    R['stub'] = p.evaluate("() => window.fcStubInsert({k:'wall', a:'Sofía', b:'El sol sale sobre la ciudad y todo se llena de luz. Caminamos juntos por el mercado, probando el pan y hablando del futuro. La vida es mejor cuando se comparte.', noteType:'naya'})")
    p.wait_for_timeout(1500)
    p.evaluate("() => { var b=document.querySelector('[data-fc-stub] .mw-tr-btn'); if(b) b.click(); }")
    p.wait_for_timeout(800)
    R['picker_before_repaint'] = p.evaluate("() => !!document.querySelector('[data-fc-stub] .mw-tr-pick')")
    # FORCE the page's own repaint while the picker is open
    p.evaluate("() => window.mwPaintWallPosts(window.MW_WALL_POSTS||[])")
    p.wait_for_timeout(1500)
    R['picker_after_forced_repaint'] = p.evaluate("""() => { var c=document.querySelector('[data-fc-stub]');
      return c ? !!c.querySelector('.mw-tr-pick') : 'nocard'; }""")
    R['stub_survived'] = p.evaluate("() => !!document.querySelector('[data-fc-stub]')")
    p.screenshot(path=WORK + 'proof-390-repaint-picker.png')
    # pick Español in the RESTORED picker
    p.evaluate("() => { var b=[...document.querySelectorAll('[data-fc-stub] .mw-tr-lang')].find(x=>x.textContent.trim()==='Español'); if(b) b.click(); }")
    p.wait_for_timeout(12000)
    R['view_after_translate'] = p.evaluate("""() => { var v=document.querySelector('[data-fc-stub] .mw-tr-view');
      return v ? v.textContent.slice(0,300) : null; }""")
    # FORCE a second repaint with the finished view showing
    p.evaluate("() => window.mwPaintWallPosts(window.MW_WALL_POSTS||[])")
    p.wait_for_timeout(1500)
    R['view_after_second_repaint'] = p.evaluate("""() => { var v=document.querySelector('[data-fc-stub] .mw-tr-view');
      return v ? v.textContent.slice(0,300) : null; }""")
    R['page_errors'] = pe
    p.evaluate("() => { var c=document.querySelector('[data-fc-stub]'); if(c) c.scrollIntoView(); }")
    p.wait_for_timeout(400)
    p.screenshot(path=WORK + 'proof-390-repaint-view2.png')
    br.close()
json.dump(R, open(WORK + 'verify-repaint2-390.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
