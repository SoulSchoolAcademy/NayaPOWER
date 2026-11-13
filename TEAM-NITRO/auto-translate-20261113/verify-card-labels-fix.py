#!/usr/bin/env python3
"""CARD-LABELS-FIX verification (maker, 2026-11-13).
Loads the FIX file (worktree, branch personal/auto-translate-card-labels-fix-20261113)
at 390: for es/fr/de — switch, open the feed, dump every fixed card label
on a rendered wall card (intelBoard), a direct-rendered SMART intelBoard
(layer heads only render there — wall notes carry no noteType, so the wall
renders the classic branch), a direct-rendered ibFeedCard, the category
bar, and the Notes-view sample noteCards; element screenshots at 390;
regression green set + one live note Translate tap; pill settles live;
pick persists across reload; overflow at 390/1440/360; first-visit es-ES.
"""
import json
from playwright.sync_api import sync_playwright

URL = 'file:///home/hatch/workspace/personal-complete-wt/TEAM-NITRO/personal-page-complete-20261113/personal-complete.html'
WORK = '/home/hatch/workspace/team-nitro/auto-translate-20261113/'

SMART_STUB = """() => window.fcStubInsert({k:'wall', a:'Shawn Vibert',
  b:'Consistency beats intensity. Show up every day, even when it is hard.',
  noteType:'smart', raw:'My own words here, word for word.',
  smart:{angles:[{b:'A child hears: keep going.'},{b:'A grandma hears: steady wins.'}],
  themes:['Focus','Calm']}})"""
NAYA_STUB = """() => window.fcStubInsert({k:'wall', a:'Shawn Vibert',
  b:'My words, beautifully formatted by Naya.', noteType:'naya'})"""

WALL_JS = """() => {
  return [...document.querySelectorAll('#os-wall-list article.intel-board')].map(function(c){
  var t = function(s){ var e=c.querySelector(s); return e ? e.textContent.replace(/\\s+/g,' ').trim() : null; };
  var ta = function(s){ var e=c.querySelector(s); return e ? e.getAttribute('aria-label') : null; };
  return {
    nutshell: t('.ib-nutshell b'),
    presenter: t('.ib-presenter span'),
    meta: t('.ib-meta span'),
    foot: t('.ib-foot span'),
    microLeft: t('.ib-microcopy .left'),
    microRight: t('.ib-microcopy .right'),
    topBtns: [...c.querySelectorAll('.board-top-actions .action')].map(function(b){ return b.textContent.replace(/\\s+/g,' ').trim(); }),
    topAria: [...c.querySelectorAll('.board-top-actions .action')].map(function(b){ return b.getAttribute('aria-label'); }),
    loveLike: [...c.querySelectorAll('.board-actions .action')].map(function(b){ return b.textContent.replace(/\\s+/g,' ').trim(); }),
    shareBtn: t('.board-actions .action[data-kind="share-intel"]'),
    starsAria: ta('.star-rating'),
    addIntelHead: t('.add-intel > b'),
    addIntelPh: (c.querySelector('.add-intel input')||{}).placeholder || null,
    addIntelAria: (c.querySelector('.add-intel input')||{}).getAttribute('aria-label') || null,
    addIntelBtn: t('.add-intel .action[data-kind="add-intel"]'),
    addIntelEmpty: t('.add-intel .intel-empty'),
  }; }); }"""

SMART_RENDER_JS = """() => {
  if(document.getElementById('mw-cardfix-probe')) document.getElementById('mw-cardfix-probe').remove();
  var host = document.createElement('div'); host.id = 'mw-cardfix-probe';
  document.body.appendChild(host);
  var note = {id:'SN-9999', title:'', subtitle:'', tone:'purple', kind:'official',
    noteType:'smart', created_at:new Date().toISOString(),
    layers:[
      {name:'In A Nutshell', color:'white', tier:'primary', body:'The nutshell body.'},
      {name:'Human Note', color:'magenta', tier:'primary', body:'Human body.'},
      {name:'Child Note', color:'sapphire', tier:'primary', body:'Child body.'},
      {name:'Grandma Note', color:'emerald', tier:'primary', body:'Grandma body.'},
      {name:'Naya Note', color:'purple', tier:'primary', body:'Naya body.'},
      {name:'Themes', color:'forest', tier:'deeper', body:'THEMES: FOCUS, CALM'},
      {name:'What It Means', color:'lime', tier:'primary', body:'Means body.'},
      {name:'Mystery Layer', color:'purple', tier:'primary', body:'Unknown head stays English.'}]};
  host.appendChild(window.ibRender(note, 0, 'collective'));
  return true; }"""

SMART_DUMP_JS = """() => {
  var c = document.querySelector('#mw-cardfix-probe article.intel-board');
  if(!c) return null;
  return {
    nutshell: (c.querySelector('.ib-nutshell b')||{}).textContent,
    heads: [...c.querySelectorAll('.ib-layer-head b')].map(function(b){ return b.textContent; }),
    foot: (c.querySelector('.ib-foot span')||{}).textContent,
  }; }"""

FEEDCARD_JS = """() => {
  if(document.getElementById('mw-cardfix-feed')) document.getElementById('mw-cardfix-feed').remove();
  var host = document.createElement('div'); host.id = 'mw-cardfix-feed';
  document.body.appendChild(host);
  var post = {id:'t1', author:'Shawn Vibert', iso:new Date().toISOString(),
    pinned:true, mine:true, noteType:'smart', title:'Test post', body:'Body text.',
    raw:'Raw words here.', themes:['Focus'],
    layers:[{head:'Detail', body:'Detail body.'},{head:'Human Note', body:'Human body.'}],
    likes:3, liked:false, comments:[], rating:{t:9,c:2}, myStars:4,
    noteId:'SN-0001', truth:'Verified', area:'personal'};
  host.innerHTML = window.ibFeedCard(post, {canPin:true});
  var c = host.querySelector('.ib-card');
  var t = function(s){ var e=c.querySelector(s); return e ? e.textContent.replace(/\\s+/g,' ').trim() : null; };
  return {
    kind: t('.ib-kind'),
    owner: t('.ib-identity span span'),
    nutshell: t('.ib-nutshell-label'),
    heads: [...c.querySelectorAll('.ib-layer-head')].map(function(s){ return s.textContent.replace(/\\s+/g,' ').trim(); }),
    rawSummary: t('.ib-rawdetails summary'),
    distilled: t('.ib-microcopy span'),
    share: t('[data-ib-share]'),
    saveList: t('[data-ib-save]'),
    pin: t('[data-ib-pin]'),
    space: t('[data-ib-grow-space]'),
    biz: t('[data-ib-grow-biz]'),
    commentBtn: t('[data-ib-cmt-toggle]'),
    commentPh: (c.querySelector('.ib-cmt-in')||{}).placeholder || null,
    send: t('[data-ib-cmt-send]'),
    micro: t('.ib-microcopy'),
  }; }"""

CATBAR_JS = """() => {
  var h = window.ibCatBarHTML(null);
  var d = document.createElement('div'); d.innerHTML = h;
  return [...d.querySelectorAll('button')].map(function(b){ return b.textContent.trim(); }); }"""

NOTES_RENDER_JS = """() => {
  if(typeof window.noteCard !== 'function') return 'NO_NOTECARD_FN';
  if(document.getElementById('mw-cardfix-notes')) document.getElementById('mw-cardfix-notes').remove();
  var host = document.createElement('div'); host.id = 'mw-cardfix-notes';
  document.body.appendChild(host);
  host.innerHTML = '<div class="ph-grid">'
    + window.noteCard({id:'sample-0', t:'The Power of Showing Up', b:'Consistency beats intensity.', c:'#2fe89e', sample:true, i:0})
    + window.noteCard({id:'r123', t:'A real note', b:'Body of a real note.', c:'#a06bff', at:new Date().toISOString(), sample:false, i:1})
    + '</div>';
  return 'RENDERED'; }"""
NOTES_DUMP_JS = """() => {
  var out = {sample: null, real: null};
  var cards = [...document.querySelectorAll('#mw-cardfix-notes .ph-card')];
  if(cards[0]) out.sample = {
    presenter: (cards[0].querySelector('.ib-presenter span')||{}).textContent || null,
    nutshell: (cards[0].querySelector('.ph-nutshell')||{}).textContent || null,
    saveBtn: (cards[0].querySelector('[data-os-save]')||{}).textContent || null,
    listBtn: (cards[0].querySelector('[data-os-listfile]')||{}).textContent || null,
  };
  if(cards[1]) out.real = {
    presenter: (cards[1].querySelector('.ib-presenter span')||{}).textContent || null,
    nutshell: (cards[1].querySelector('.ph-nutshell')||{}).textContent || null,
    saveBtn: (cards[1].querySelector('[data-os-save]')||{}).textContent || null,
    listBtn: (cards[1].querySelector('[data-os-listfile]')||{}).textContent || null,
    inLine: (cards[1].querySelector('.os-sl-in')||{}).textContent || null,
  };
  return out; }"""

R = {'url': URL}
with sync_playwright() as pw:
    br = pw.firefox.launch()
    ctx = br.new_context(viewport={'width': 390, 'height': 844})
    p = ctx.new_page()
    ce, pe = [], []
    p.on('console', lambda m: ce.append(m.text[:160]) if m.type == 'error' else None)
    p.on('pageerror', lambda e: pe.append(str(e)))
    p.goto(URL)
    p.wait_for_timeout(10000)
    R['page_errors'] = pe
    R['console_error_count'] = len(ce)
    R['console_non_supabase'] = [c for c in ce if 'supabase' not in c.lower() and 'Cross-Origin' not in c][:10]
    R['overflow390'] = p.evaluate("({sw: document.documentElement.scrollWidth, iw: window.innerWidth})")
    R['pill'] = p.evaluate("() => (document.querySelector('.ph-points-label')||{}).textContent")
    # stubs on the wall (classic branch) + direct SMART render + feed card
    R['stub_smart'] = p.evaluate(SMART_STUB)
    R['stub_naya'] = p.evaluate(NAYA_STUB)
    p.wait_for_timeout(1500)
    R['wall_cards'] = p.evaluate("() => document.querySelectorAll('#os-wall-list article.intel-board').length")
    R['langs'] = {}
    for lang in ('es', 'fr', 'de'):
        p.evaluate("() => { var s=document.getElementById('mw-set-lang'); s.value='%s'; s.dispatchEvent(new Event('change')); }" % lang)
        p.wait_for_timeout(1200)
        p.evaluate(SMART_RENDER_JS)
        p.evaluate(FEEDCARD_JS)
        p.wait_for_timeout(400)
        R['langs'][lang] = {
            'lang_attr': p.evaluate("document.documentElement.lang"),
            'wall': p.evaluate(WALL_JS),
            'smart': p.evaluate(SMART_DUMP_JS),
            'feedcard': p.evaluate(FEEDCARD_JS),
            'catbar': p.evaluate(CATBAR_JS),
        }
        card = p.locator('#os-wall-list article.intel-board').first
        card.screenshot(path=WORK + 'fix-proof-390-card-%s.png' % lang)
    # switch-resilience: back to en, then to es on the SAME page, no reload
    p.evaluate("() => { var s=document.getElementById('mw-set-lang'); s.value='en'; s.dispatchEvent(new Event('change')); }")
    p.wait_for_timeout(1000)
    R['switch_back_en'] = p.evaluate(WALL_JS)
    p.evaluate("() => { var s=document.getElementById('mw-set-lang'); s.value='es'; s.dispatchEvent(new Event('change')); }")
    p.wait_for_timeout(1000)
    R['switch_to_es'] = p.evaluate(WALL_JS)
    # Notes view sample cards (es) — direct noteCard render: the Notes view
    # itself does not open in this file:// context (sb undeclared, pre-existing)
    R['notes_render'] = p.evaluate(NOTES_RENDER_JS)
    p.wait_for_timeout(800)
    R['notes_cards_es'] = p.evaluate(NOTES_DUMP_JS)
    # regression green set (back to en first for the English baselines, then es)
    p.evaluate("() => { var s=document.getElementById('mw-set-lang'); s.value='es'; s.dispatchEvent(new Event('change')); }")
    p.wait_for_timeout(1200)
    R['green_es'] = p.evaluate("""() => ({
      msgbtn: (document.getElementById('msgbtn')||{}).textContent,
      tabPublic: (document.getElementById('mwTabNaya')||{}).textContent,
      railHead: (document.querySelector('.pc-rail-head h3, #pcRail h3')||{}).textContent,
      railCards: document.querySelectorAll('.pc-card').length,
      plusItems: document.querySelectorAll('.fc-plusitem').length,
      segs: [...document.querySelectorAll('#naya-notif-bar [data-notif]')].map(b=>b.getAttribute('aria-label')),
    })""")
    # Settings panel still switches
    p.evaluate("() => document.getElementById('settingsbtn').click()")
    p.wait_for_timeout(1200)
    R['settings_es'] = p.evaluate("""() => [...document.querySelectorAll('#settings h3')].map(function(h){ return h.textContent.trim(); })""")
    p.evaluate("() => document.getElementById('settingsbtn').click()")
    p.wait_for_timeout(800)
    # note Translate tap end to end (es note -> en page)
    p.evaluate("() => { var s=document.getElementById('mw-set-lang'); s.value='en'; s.dispatchEvent(new Event('change')); }")
    p.wait_for_timeout(800)
    R['notes_cards_en'] = p.evaluate(NOTES_DUMP_JS)
    R['stub'] = p.evaluate("() => window.fcStubInsert({k:'wall', a:'Sofía', b:'El sol sale sobre la ciudad y todo se llena de luz. Caminamos juntos por el mercado.', noteType:'naya'})")
    p.wait_for_timeout(1500)
    p.evaluate("() => { var b=document.querySelector('[data-fc-stub] .mw-tr-btn'); if(b) b.click(); }")
    p.wait_for_timeout(1000)
    R['picker'] = p.evaluate("() => !!document.querySelector('[data-fc-stub] .mw-tr-pick')")
    p.evaluate("() => { var b=[...document.querySelectorAll('[data-fc-stub] .mw-tr-lang')].find(x=>x.textContent.trim()==='Español'); if(b) b.click(); }")
    p.wait_for_timeout(12000)
    R['translation'] = p.evaluate("""() => { var v=document.querySelector('[data-fc-stub] .mw-tr-view');
      return v ? v.textContent.slice(0,300) : null; }""")
    R['original_back'] = p.evaluate("""() => { var b=document.querySelector('[data-fc-stub] .mw-tr-view .mw-tr-orig, [data-fc-stub] .mw-tr-showorig');
      if(!b) return null; b.click(); return true; }""")
    p.wait_for_timeout(800)
    # persistence across reload
    p.evaluate("() => { var s=document.getElementById('mw-set-lang'); s.value='de'; s.dispatchEvent(new Event('change')); }")
    p.wait_for_timeout(800)
    p.reload()
    p.wait_for_timeout(8000)
    R['persist_after_reload'] = p.evaluate("() => ({lang: document.documentElement.lang, stored: localStorage.getItem('mw.set.lang')})")
    # overflow at 1440 and 360
    for w in (1440, 360):
        ctx2 = br.new_context(viewport={'width': w, 'height': 900})
        q = ctx2.new_page()
        q.goto(URL)
        q.wait_for_timeout(9000)
        R['overflow%d' % w] = q.evaluate("({sw: document.documentElement.scrollWidth, iw: window.innerWidth})")
        if w == 1440:
            q.evaluate("() => { var s=document.getElementById('mw-set-lang'); s.value='es'; s.dispatchEvent(new Event('change')); }")
            q.wait_for_timeout(1200)
            R['overflow1440_es'] = q.evaluate("({sw: document.documentElement.scrollWidth, iw: window.innerWidth})")
            q.evaluate(SMART_STUB)
            q.wait_for_timeout(1200)
            q.locator('#os-wall-list article.intel-board').first.screenshot(path=WORK + 'fix-proof-1440-card-es.png')
    # first-visit es-ES (fresh profile, browser locale es-ES, no stored pick)
    ctx3 = br.new_context(viewport={'width': 390, 'height': 844}, locale='es-ES')
    f = ctx3.new_page()
    f.goto(URL)
    f.wait_for_timeout(10000)
    R['first_visit'] = {
        'lang': f.evaluate("document.documentElement.lang"),
        'stored': f.evaluate("() => localStorage.getItem('mw.set.lang')"),
        'stub': f.evaluate(SMART_STUB),
    }
    f.wait_for_timeout(1200)
    R['first_visit']['wall'] = f.evaluate(WALL_JS)
    f.locator('#os-wall-list article.intel-board').first.screenshot(path=WORK + 'fix-proof-390-card-first-es.png')
    br.close()
json.dump(R, open(WORK + 'verify-card-labels-fix.json', 'w'), indent=1, ensure_ascii=False)
print(json.dumps({k: R[k] for k in ('page_errors', 'console_error_count', 'console_non_supabase', 'overflow390', 'overflow1440', 'overflow360', 'overflow1440_es', 'wall_cards', 'stub_smart', 'stub_naya', 'persist_after_reload')}, indent=1))
