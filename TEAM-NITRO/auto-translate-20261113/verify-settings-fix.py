#!/usr/bin/env python3
"""SETTINGS-FIX verification (maker, 2026-11-13).
Loads the FIX file (worktree, branch personal/auto-translate-settings-fix-20261113)
at 390: for es/fr/de — switch, open Settings, dump every panel label, element
screenshot; regression green set + one live note Translate tap; overflow at
390/1440/360; first-visit es-ES (auth card + install state at boot)."""
import json
from playwright.sync_api import sync_playwright
URL='file:///home/hatch/workspace/personal-complete-wt/TEAM-NITRO/personal-page-complete-20261113/personal-complete.html'
WORK='/home/hatch/workspace/team-nitro/auto-translate-20261113/'
PANEL_JS="""() => {
  var el=document.getElementById('settings');
  var out=[];
  el.querySelectorAll('h3, b, .os-setrow-sub, p, button, .ph-sec-t, label, a, .os-switch-cap').forEach(function(n){
    var t=(n.textContent||'').trim().replace(/\\s+/g,' ');
    if(t) out.push(t);
  });
  return out; }"""
R={'url':URL}
with sync_playwright() as pw:
    br=pw.firefox.launch()
    ctx=br.new_context(viewport={'width':390,'height':844})
    p=ctx.new_page()
    ce,pe=[],[]
    p.on('console', lambda m: ce.append(m.text[:160]) if m.type=='error' else None)
    p.on('pageerror', lambda e: pe.append(str(e)))
    p.goto(URL); p.wait_for_timeout(10000)
    R['page_errors']=pe
    R['console_error_count']=len(ce)
    R['console_non_supabase']=[c for c in ce if 'supabase' not in c.lower() and 'Cross-Origin' not in c][:10]
    R['overflow390']=p.evaluate("({sw: document.documentElement.scrollWidth, iw: window.innerWidth})")
    # open Settings once via the gear
    p.evaluate("() => document.getElementById('settingsbtn').click()")
    p.wait_for_timeout(1500)
    R['settings_open']=p.evaluate("() => document.getElementById('settings').classList.contains('on')")
    R['langs']={}
    for lang in ('es','fr','de'):
        p.evaluate("() => { var s=document.getElementById('mw-set-lang'); s.value='%s'; s.dispatchEvent(new Event('change')); }" % lang)
        p.wait_for_timeout(1200)
        texts=p.evaluate(PANEL_JS)
        slots=p.evaluate("""() => [...document.querySelectorAll('#mw-cover-slots input')].map(i=>({ph: i.getAttribute('placeholder'), al: i.getAttribute('aria-label')}))""")
        R['langs'][lang]={'lang_attr':p.evaluate("document.documentElement.lang"),'panel_texts':texts,'slots':slots}
        p.locator('#settings').screenshot(path=WORK+'fix-proof-390-settings-%s.png' % lang)
    # regression green set (back to en, then es for the chrome check)
    p.evaluate("() => { var s=document.getElementById('mw-set-lang'); s.value='es'; s.dispatchEvent(new Event('change')); }")
    p.wait_for_timeout(1200)
    R['green_es']=p.evaluate("""() => ({
      msgbtn: (document.getElementById('msgbtn')||{}).textContent,
      tabPublic: (document.getElementById('mwTabNaya')||{}).textContent,
      railHead: (document.querySelector('.pc-rail-head h3, #pcRail h3')||{}).textContent,
      railCards: document.querySelectorAll('.pc-card').length,
      plusItems: document.querySelectorAll('.fc-plusitem').length,
      segs: [...document.querySelectorAll('#naya-notif-bar [data-notif]')].map(b=>b.getAttribute('aria-label')),
    })""")
    # + menu opens, note Translate tap end to end (es note -> en page)
    p.evaluate("() => { var s=document.getElementById('mw-set-lang'); s.value='en'; s.dispatchEvent(new Event('change')); }")
    p.wait_for_timeout(800)
    R['stub']=p.evaluate("() => window.fcStubInsert({k:'wall', a:'Sofía', b:'El sol sale sobre la ciudad y todo se llena de luz. Caminamos juntos por el mercado.', noteType:'naya'})")
    p.wait_for_timeout(1500)
    p.evaluate("() => { var b=document.querySelector('[data-fc-stub] .mw-tr-btn'); if(b) b.click(); }")
    p.wait_for_timeout(1000)
    R['picker']=p.evaluate("() => !!document.querySelector('[data-fc-stub] .mw-tr-pick')")
    p.evaluate("() => { var b=[...document.querySelectorAll('[data-fc-stub] .mw-tr-lang')].find(x=>x.textContent.trim()==='Español'); if(b) b.click(); }")
    p.wait_for_timeout(12000)
    R['translation']=p.evaluate("""() => { var v=document.querySelector('[data-fc-stub] .mw-tr-view');
      return v ? v.textContent.slice(0,300) : null; }""")
    R['original_back']=p.evaluate("""() => { var b=document.querySelector('[data-fc-stub] .mw-tr-view .mw-tr-orig, [data-fc-stub] .mw-tr-showorig');
      if(!b) return null; b.click(); return true; }""")
    p.wait_for_timeout(800)
    # persistence across reload
    p.evaluate("() => { var s=document.getElementById('mw-set-lang'); s.value='de'; s.dispatchEvent(new Event('change')); }")
    p.wait_for_timeout(800)
    p.reload(); p.wait_for_timeout(8000)
    R['persist_after_reload']=p.evaluate("() => ({lang: document.documentElement.lang, stored: localStorage.getItem('mw.set.lang')})")
    # overflow at 1440 and 360
    for w in (1440,360):
        ctx2=br.new_context(viewport={'width':w,'height':900})
        q=ctx2.new_page()
        q.goto(URL); q.wait_for_timeout(9000)
        R['overflow%d'%w]=q.evaluate("({sw: document.documentElement.scrollWidth, iw: window.innerWidth})")
        q.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)"); q.wait_for_timeout(1200)
        R['overflow%d_scrolled'%w]=q.evaluate("({sw: document.documentElement.scrollWidth, iw: window.innerWidth})")
        ctx2.close()
    # first visit, locale es-ES, fresh context: auth card + install state at boot
    ctx3=br.new_context(viewport={'width':390,'height':844}, locale='es-ES')
    q3=ctx3.new_page()
    q3.goto(URL); q3.wait_for_timeout(10000)
    R['first_visit_es']=q3.evaluate("() => ({lang: document.documentElement.lang, stored: localStorage.getItem('mw.set.lang')})")
    q3.evaluate("() => document.getElementById('settingsbtn').click()")
    q3.wait_for_timeout(1500)
    R['first_visit_es']['auth_card']=q3.evaluate("""() => { var b=document.getElementById('naya-auth-btn');
      var card=b?b.parentElement:null;
      return card ? card.textContent.replace(/\\s+/g,' ').trim().slice(0,300) : null; }""")
    R['first_visit_es']['install_state']=q3.evaluate("() => (document.getElementById('os-install-state')||{}).textContent")
    R['first_visit_es']['id_line']=q3.evaluate("() => (document.getElementById('os-id-line')||{}).textContent")
    ctx3.close()
    br.close()
json.dump(R, open(WORK+'verify-settings-fix.json','w'), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
