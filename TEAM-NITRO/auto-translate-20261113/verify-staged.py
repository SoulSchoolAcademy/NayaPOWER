#!/usr/bin/env python3
"""AUTO-TRANSLATE staged verification (fresh maker, 2026-11-13).
Loads the STAGED page (proof host, ref personal/auto-translate-20261113,
cb = filed commit eeb5db00) at 390: errors, overflow, green set (incl. the
pill on served bytes), language switch, one live translation tap."""
import json
from playwright.sync_api import sync_playwright
URL = ('https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/personal-page-complete-20261113/'
       'personal-complete.html&ref=personal/auto-translate-20261113&cb=eeb5db00814b8bd3d12f16edc25b8ecf7e4ab791')
WORK = '/home/hatch/workspace/team-nitro/auto-translate-20261113/'
R = {'staged_url': URL}
with sync_playwright() as pw:
    br = pw.firefox.launch()
    ctx = br.new_context(viewport={'width': 390, 'height': 844})
    p = ctx.new_page()
    ce, pe = [], []
    p.on('console', lambda m: ce.append(m.text[:160]) if m.type == 'error' else None)
    p.on('pageerror', lambda e: pe.append(str(e)))
    p.goto(URL, wait_until='domcontentloaded', timeout=60000)
    p.wait_for_timeout(15000)
    R['page_errors'] = pe
    R['console_error_count'] = len(ce)
    R['console_non_supabase'] = [c for c in ce if 'supabase' not in c.lower() and 'Cross-Origin' not in c][:10]
    R['overflow0'] = p.evaluate("({sw: document.documentElement.scrollWidth, iw: window.innerWidth})")
    p.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
    p.wait_for_timeout(1500)
    R['overflow_scrolled'] = p.evaluate("({sw: document.documentElement.scrollWidth, iw: window.innerWidth})")
    p.evaluate("window.scrollTo(0,0)")
    R['green'] = p.evaluate("""() => ({
      pill: (document.getElementById('pointscount')||{}).textContent,
      tabs: [...document.querySelectorAll('.lens-tab')].map(t=>t.textContent.trim()),
      railCards: document.querySelectorAll('.pc-card').length,
      plusItems: document.querySelectorAll('.fc-plusitem').length,
      wallCards: document.querySelectorAll('#os-wall-list article.intel-board').length,
      wallEmpty: !!document.querySelector('#os-wall-list .ph-card'),
      lang: document.documentElement.lang,
    })""")
    # language switch to es on staged bytes
    p.evaluate("() => { var s=document.getElementById('mw-set-lang'); s.value='es'; s.dispatchEvent(new Event('change')); }")
    p.wait_for_timeout(1200)
    R['lang_es'] = p.evaluate("() => ({lang: document.documentElement.lang, msgbtn: (document.getElementById('msgbtn')||{}).textContent, tabPublic: (document.getElementById('mwTabNaya')||{}).textContent})")
    p.evaluate("() => { var s=document.getElementById('mw-set-lang'); s.value='en'; s.dispatchEvent(new Event('change')); }")
    p.wait_for_timeout(800)
    # one live translation tap on staged bytes
    R['stub'] = p.evaluate("() => window.fcStubInsert({k:'wall', a:'Sofía', b:'El sol sale sobre la ciudad y todo se llena de luz. Caminamos juntos por el mercado.', noteType:'naya'})")
    p.wait_for_timeout(1500)
    p.evaluate("() => { var b=document.querySelector('[data-fc-stub] .mw-tr-btn'); if(b) b.click(); }")
    p.wait_for_timeout(1000)
    R['picker'] = p.evaluate("() => !!document.querySelector('[data-fc-stub] .mw-tr-pick')")
    p.evaluate("() => { var b=[...document.querySelectorAll('[data-fc-stub] .mw-tr-lang')].find(x=>x.textContent.trim()==='Español'); if(b) b.click(); }")
    p.wait_for_timeout(12000)
    R['staged_translation'] = p.evaluate("""() => { var v=document.querySelector('[data-fc-stub] .mw-tr-view');
      return v ? v.textContent.slice(0,300) : null; }""")
    p.evaluate("() => { var c=document.querySelector('[data-fc-stub]'); if(c) c.scrollIntoView({block:'center'}); }")
    p.wait_for_timeout(500)
    p.screenshot(path=WORK + 'proof-staged-390-translated.png')
    br.close()
json.dump(R, open(WORK + 'verify-staged.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
