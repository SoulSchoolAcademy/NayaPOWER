#!/usr/bin/env python3
"""SETTINGS-FIX verification pass 2 (maker, 2026-11-13) — the auth card.
For es/fr/de: switch, open Settings, read the Account h3 span (must be
translated AND the info button must still be inside the h3), the info
button aria-label, open the info panel and read its text. Plus first-visit
es-ES boot (card created in Spanish, panel decorated in Spanish)."""
import json
from playwright.sync_api import sync_playwright
URL='file:///home/hatch/workspace/personal-complete-wt/TEAM-NITRO/personal-page-complete-20261113/personal-complete.html'
WORK='/home/hatch/workspace/team-nitro/auto-translate-20261113/'
AUTH_JS="""() => {
  var b=document.getElementById('naya-auth-btn');
  if(!b) return null;
  var card=b.parentElement, h3=card.querySelector('h3');
  return {
    h3_text: h3 ? h3.textContent.trim() : null,
    h3_span: h3 && h3.querySelector('span') ? h3.querySelector('span').textContent : null,
    info_btn_present: !!card.querySelector('.os-info-btn'),
    info_aria: (card.querySelector('.os-info-btn')||{}).getAttribute ? card.querySelector('.os-info-btn').getAttribute('aria-label') : null,
    panel_text: (card.querySelector('.os-info-panel')||{}).textContent || null,
    panel_marked: !!(card.querySelector('.os-info-panel')||{}).getAttribute && card.querySelector('.os-info-panel').getAttribute('data-mw-tr'),
    btn_text: b.textContent,
  }; }"""
R={}
with sync_playwright() as pw:
    br=pw.firefox.launch()
    ctx=br.new_context(viewport={'width':390,'height':844})
    p=ctx.new_page()
    pe=[]; p.on('pageerror', lambda e: pe.append(str(e)))
    p.goto(URL); p.wait_for_timeout(10000)
    R['page_errors']=pe
    p.evaluate("() => document.getElementById('settingsbtn').click()")
    p.wait_for_timeout(1500)
    R['langs']={}
    for lang in ('es','fr','de'):
        p.evaluate("() => { var s=document.getElementById('mw-set-lang'); s.value='%s'; s.dispatchEvent(new Event('change')); }" % lang)
        p.wait_for_timeout(1200)
        # open the info panel
        p.evaluate("() => { var b=document.querySelector('#settings .os-info-btn'); if(b) b.click(); }")
        p.wait_for_timeout(600)
        R['langs'][lang]=p.evaluate(AUTH_JS)
        p.evaluate("() => { var b=document.querySelector('#settings .os-info-btn'); if(b) b.click(); }")
        p.wait_for_timeout(400)
    # first visit es-ES
    ctx3=br.new_context(viewport={'width':390,'height':844}, locale='es-ES')
    q3=ctx3.new_page()
    q3.goto(URL); q3.wait_for_timeout(10000)
    q3.evaluate("() => document.getElementById('settingsbtn').click()")
    q3.wait_for_timeout(1500)
    q3.evaluate("() => { var b=document.querySelector('#settings .os-info-btn'); if(b) b.click(); }")
    q3.wait_for_timeout(600)
    R['first_visit_es']=q3.evaluate(AUTH_JS)
    R['first_visit_es']['lang']=q3.evaluate("document.documentElement.lang")
    ctx3.close()
    br.close()
json.dump(R, open(WORK+'verify-settings-fix2.json','w'), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
