#!/usr/bin/env python3
"""Phase A: load, errors, overflow, green set, language switch + persistence + first-visit."""
import json, sys
from playwright.sync_api import sync_playwright
URL = 'file:///home/hatch/workspace/personal-complete-wt/TEAM-NITRO/personal-page-complete-20261113/personal-complete.html'
W = int(sys.argv[1]) if len(sys.argv) > 1 else 390
def overflow(p):
    return p.evaluate("({sw: document.documentElement.scrollWidth, iw: window.innerWidth})")
def lang_state(p):
    return p.evaluate("""() => ({
      lang: document.documentElement.lang,
      msgbtn: (document.getElementById('msgbtn')||{}).textContent,
      skillsbtn: (document.getElementById('skillsbtn')||{}).textContent,
      tabPublic: (document.getElementById('mwTabNaya')||{}).textContent,
      feedline: (document.querySelector('.pc-feedline')||{}).textContent,
      railHead: (document.querySelector('.pc-rail-head h3')||{}).textContent,
      railChat: (document.querySelector('.pc-btn[data-pc-act="chat"]')||{}).textContent,
      railMail: (document.querySelector('.pc-btn[data-pc-act="mail"]')||{}).textContent,
      segTop: (document.querySelector('#mw-seg-strip [data-v="top"]')||{}).textContent,
      segAny: (document.querySelector('#mw-seg-match [data-v="0"]')||{}).textContent,
      segFeed: (document.querySelector('#mw-seg-feedtab [data-v="smart"]')||{}).textContent,
      picker: (document.getElementById('mw-set-lang')||{}).value,
      stored: localStorage.getItem('mw.set.lang'),
    })""")
R = {}
with sync_playwright() as pw:
    br = pw.firefox.launch()
    ctx = br.new_context(viewport={'width': W, 'height': 844})
    p = ctx.new_page()
    ce, pe = [], []
    p.on('console', lambda m: ce.append(m.text) if m.type == 'error' else None)
    p.on('pageerror', lambda e: pe.append(str(e)))
    p.goto(URL); p.wait_for_timeout(10000)
    R['page_errors'] = pe
    R['console_error_count'] = len(ce)
    R['console_non_supabase'] = [c for c in ce if 'supabase' not in c.lower() and 'Cross-Origin' not in c][:10]
    R['overflow0'] = overflow(p)
    p.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)"); p.wait_for_timeout(1200)
    R['overflow_scrolled'] = overflow(p)
    p.evaluate("window.scrollTo(0,0)")
    R['lang_en'] = lang_state(p)
    R['green'] = p.evaluate("""() => ({
      pill: (document.getElementById('pointscount')||{}).textContent,
      tabs: [...document.querySelectorAll('.lens-tab')].map(t=>t.textContent.trim()),
      railCards: document.querySelectorAll('.pc-card').length,
      plusItems: document.querySelectorAll('.fc-plusitem').length,
      segs: [...document.querySelectorAll('#naya-notif-bar [data-notif]')].map(b=>b.getAttribute('data-notif')),
      segAria: [...document.querySelectorAll('#naya-notif-bar [data-notif]')].map(b=>b.getAttribute('aria-label')),
      wallCards: document.querySelectorAll('#os-wall-list .intel-board, #os-wall-list .ph-card').length,
      trBtns: document.querySelectorAll('.mw-tr-btn').length,
    })""")
    for code in ['es', 'fr', 'de']:
        p.evaluate("(c) => { var s=document.getElementById('mw-set-lang'); s.value=c; s.dispatchEvent(new Event('change')); }", code)
        p.wait_for_timeout(1000)
        R['lang_' + code] = lang_state(p)
    p.reload(); p.wait_for_timeout(10000)
    R['lang_de_after_reload'] = lang_state(p)
    p.screenshot(path='proof-%d-de-chrome.png' % W)
    p.evaluate("() => { var s=document.getElementById('mw-set-lang'); s.value='es'; s.dispatchEvent(new Event('change')); }")
    p.wait_for_timeout(1000)
    p.screenshot(path='proof-%d-es-chrome.png' % W)
    ctx.close()
    # first-visit defaults, one context at a time
    for loc, tag in [('es-ES', 'es'), ('ja-JP', 'ja')]:
        c2 = br.new_context(viewport={'width': W, 'height': 844}, locale=loc)
        q = c2.new_page()
        q.goto(URL); q.wait_for_timeout(10000)
        R['first_visit_' + tag] = q.evaluate("() => ({ navLang: navigator.language, lang: document.documentElement.lang, msgbtn: (document.getElementById('msgbtn')||{}).textContent, stored: localStorage.getItem('mw.set.lang') })")
        c2.close()
    br.close()
json.dump(R, open('verify-a-%d.json' % W, 'w'), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
