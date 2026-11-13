#!/usr/bin/env python3
"""AUTO-TRANSLATE Part 2 (fresh maker, 2026-11-13): translation taps, CORRECT
selectors matching mw-translate.js as built: .mw-tr-pick > .mw-tr-lang
(source picker), .mw-tr-view + .mw-tr-label (labelled view), .mw-tr-orig
(Show original / Show translation toggle), .mw-tr-view.mw-tr-fail
(honest failure). The first maker's verify-b.py / verify-local.py used
.mw-tr-src / .mw-tr-showorig / .mw-tr-back / .mw-tr-err, which do not exist
in the built module — those scripts could never have clicked the picker.
This script replaces them for Part 2. 390 first."""
import json, sys
from playwright.sync_api import sync_playwright
URL = 'file:///home/hatch/workspace/personal-complete-wt/TEAM-NITRO/personal-page-complete-20261113/personal-complete.html'
W = int(sys.argv[1]) if len(sys.argv) > 1 else 390
WORK = '/home/hatch/workspace/team-nitro/auto-translate-20261113/'
R = {}

def set_lang(p, code):
    p.evaluate("(c) => { var s=document.getElementById('mw-set-lang'); s.value=c; s.dispatchEvent(new Event('change')); }", code)
    p.wait_for_timeout(1000)

def insert_stub(p, author, body):
    return p.evaluate("([a,b]) => window.fcStubInsert({k:'wall', a:a, b:b, noteType:'naya'})", [author, body])

def tap_translate_latest(p, src_label):
    """Click the Translate button on the newest stub, pick source language, wait, return view text.
    Polls for the picker (the wall can re-paint once shortly after load; a
    picker lost to a re-paint is re-opened with one more tap — attempts recorded)."""
    attempts = 0
    pick = None
    for attempt in range(2):
        attempts += 1
        p.evaluate("() => { var b=document.querySelector('[data-fc-stub] .mw-tr-btn'); if(b) b.click(); }")
        for _ in range(10):
            p.wait_for_timeout(500)
            pick = p.evaluate("""() => { var pk=document.querySelector('[data-fc-stub] .mw-tr-pick');
              return pk ? {langs:[...pk.querySelectorAll('.mw-tr-lang')].map(b=>b.textContent.trim()),
                           q:(pk.querySelector('.mw-tr-pick-q')||{}).textContent} : null; }""")
            if pick:
                break
        if pick:
            break
    p.evaluate("(s) => { var b=[...document.querySelectorAll('[data-fc-stub] .mw-tr-lang')].find(x=>x.textContent.trim()===s); if(b) b.click(); }", src_label)
    p.wait_for_timeout(10000)
    view = p.evaluate("""() => { var v=document.querySelector('[data-fc-stub] .mw-tr-view');
      return v ? v.textContent : null; }""")
    return pick, view, attempts

def view_label(p):
    return p.evaluate("""() => { var v=document.querySelector('[data-fc-stub] .mw-tr-view');
      return v ? ((v.querySelector('.mw-tr-label')||{}).textContent||'').trim() : null; }""")

with sync_playwright() as pw:
    br = pw.firefox.launch()
    ctx = br.new_context(viewport={'width': W, 'height': 844})
    p = ctx.new_page()
    ce, pe = [], []
    p.on('console', lambda m: ce.append(m.text[:160]) if m.type == 'error' else None)
    p.on('pageerror', lambda e: pe.append(str(e)))
    p.goto(URL, wait_until='domcontentloaded', timeout=60000)
    p.wait_for_timeout(12000)
    R['page_errors'] = pe
    R['console_error_count'] = len(ce)
    R['console_non_supabase'] = [c for c in ce if 'supabase' not in c.lower() and 'Cross-Origin' not in c][:10]
    R['overflow0'] = p.evaluate("({sw: document.documentElement.scrollWidth, iw: window.innerWidth})")
    R['tr_btns_fresh_load'] = p.evaluate("() => document.querySelectorAll('.mw-tr-btn').length")
    R['wall_cards_fresh'] = p.evaluate("() => document.querySelectorAll('#os-wall-list article.intel-board').length")

    # --- ES 3-sentence note -> English (multi-sentence segmentation proof) ---
    R['stub_es'] = insert_stub(p, 'Sofía', 'El sol sale sobre la ciudad y todo se llena de luz. Caminamos juntos por el mercado, probando el pan y hablando del futuro. La vida es mejor cuando se comparte.')
    p.wait_for_timeout(1500)
    R['tr_btns_after_stub'] = p.evaluate("() => document.querySelectorAll('.mw-tr-btn').length")
    pick, view, att = tap_translate_latest(p, 'Español')
    R['es_attempts'] = att
    R['es_picker'] = pick
    R['es_to_en_view'] = view
    R['es_to_en_label'] = view_label(p)
    p.screenshot(path=WORK + 'proof-%d-translated-es.png' % W)
    # original one tap away, then back
    p.evaluate("() => { var b=document.querySelector('[data-fc-stub] .mw-tr-orig'); if(b) b.click(); }")
    p.wait_for_timeout(600)
    R['after_show_original'] = p.evaluate("""() => { var c=document.querySelector('[data-fc-stub]');
      return {collapsed: !!c.querySelector('.mw-tr-view.mw-tr-collapsed'),
              backBtn: (c.querySelector('.mw-tr-orig')||{}).textContent,
              origNut: (c.querySelector('.ib-nutshell')||{textContent:''}).textContent.slice(0,60)}; }""")
    p.evaluate("() => { var b=document.querySelector('[data-fc-stub] .mw-tr-orig'); if(b) b.click(); }")
    p.wait_for_timeout(600)
    R['after_show_translation'] = p.evaluate("() => { var c=document.querySelector('[data-fc-stub]'); return {hasView: !!c.querySelector('.mw-tr-view:not(.mw-tr-collapsed)'), label:(c.querySelector('.mw-tr-label')||{textContent:''}).textContent.trim()}; }")

    # --- FR note -> English ---
    insert_stub(p, 'Marie', 'Le matin est calme et la ville se réveille doucement. Nous buvons du café en regardant la rivière passer.')
    p.wait_for_timeout(1500)
    _, view, att = tap_translate_latest(p, 'Français')
    R['fr_attempts'] = att
    R['fr_to_en_view'] = view
    R['fr_to_en_label'] = view_label(p)
    # --- DE note -> English ---
    insert_stub(p, 'Jonas', 'Der Abend ist still und die Lichter der Stadt spiegeln sich im Fluss. Wir gehen langsam nach Hause und denken an morgen.')
    p.wait_for_timeout(1500)
    _, view, att = tap_translate_latest(p, 'Deutsch')
    R['de_attempts'] = att
    R['de_to_en_view'] = view
    R['de_to_en_label'] = view_label(p)

    # --- EN note -> ES, FR, DE (page language = target each time) ---
    en_body = 'The garden grows quiet in winter. We plant seeds in spring and watch them climb toward the sun.'
    for code, src_label, key in [('es', 'English', 'en_to_es'), ('fr', 'English', 'en_to_fr'), ('de', 'English', 'en_to_de')]:
        set_lang(p, code)
        insert_stub(p, 'Alex', en_body)
        p.wait_for_timeout(1500)
        _, view, att = tap_translate_latest(p, src_label)
        R[key + '_attempts'] = att
        R[key + '_view'] = view
        R[key + '_label'] = view_label(p)
    set_lang(p, 'en')

    # --- Naya-card attach path (synthetic faithful card: the live Naya feed
    # stays skeleton on file://, so the scan path is proven with a card in the
    # feed's own shape, labelled synthetic here) ---
    R['naya_attach'] = p.evaluate("""() => {
      var feed=document.getElementById('mwFeedNaya'); if(!feed) return 'no feed';
      var c=document.createElement('div'); c.className='ph-card'; c.setAttribute('data-synth-naya','1');
      c.innerHTML='<h3>Morning light</h3><p>General &middot; today</p><p>Le matin est calme et la ville se réveille doucement.</p>';
      feed.appendChild(c); return 'inserted'; }""")
    p.wait_for_timeout(1500)
    R['naya_tr_btns'] = p.evaluate("() => document.querySelectorAll('#mwFeedNaya .mw-tr-btn').length")
    ctx.close()

    # --- failure honesty: worker host blocked ---
    ctx2 = br.new_context(viewport={'width': W, 'height': 844})
    p2 = ctx2.new_page()
    p2.route('**naya-auto-translate-staging.nayapower.workers.dev**', lambda r: r.abort())
    pe2 = []
    p2.on('pageerror', lambda e: pe2.append(str(e)))
    p2.goto(URL, wait_until='domcontentloaded', timeout=60000)
    p2.wait_for_timeout(12000)
    insert_stub(p2, 'Luc', 'La pluie tombe sur les toits et tout devient silencieux.')
    p2.wait_for_timeout(1500)
    p2.evaluate("() => { var b=document.querySelector('[data-fc-stub] .mw-tr-btn'); if(b) b.click(); }")
    fail_pick = None
    for _ in range(10):
        p2.wait_for_timeout(500)
        fail_pick = p2.evaluate("() => !!document.querySelector('[data-fc-stub] .mw-tr-pick')")
        if fail_pick:
            break
    if not fail_pick:
        p2.evaluate("() => { var b=document.querySelector('[data-fc-stub] .mw-tr-btn'); if(b) b.click(); }")
        for _ in range(10):
            p2.wait_for_timeout(500)
            fail_pick = p2.evaluate("() => !!document.querySelector('[data-fc-stub] .mw-tr-pick')")
            if fail_pick:
                break
    R['failure_picker'] = fail_pick
    p2.evaluate("() => { var b=[...document.querySelectorAll('[data-fc-stub] .mw-tr-lang')].find(x=>x.textContent.trim()==='Français'); if(b) b.click(); }")
    # the fail view self-removes after 6s — poll fast, record first sighting
    fail_seen = None
    for _ in range(16):
        p2.wait_for_timeout(500)
        st = p2.evaluate("""() => { var c=document.querySelector('[data-fc-stub]');
          var f=c.querySelector('.mw-tr-view.mw-tr-fail');
          return {failText: f?f.textContent.trim():null, hasView: !!c.querySelector('.mw-tr-view:not(.mw-tr-fail)')}; }""")
        if st['failText'] and fail_seen is None:
            fail_seen = st
    R['failure'] = fail_seen if fail_seen else st
    R['failure_seen'] = fail_seen is not None
    R['failure_page_errors'] = pe2
    p2.screenshot(path=WORK + 'proof-%d-failure.png' % W)
    ctx2.close()
    br.close()

json.dump(R, open(WORK + 'verify-b2-%d.json' % W, 'w'), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
