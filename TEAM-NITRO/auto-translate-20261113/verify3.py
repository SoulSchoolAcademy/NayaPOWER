#!/usr/bin/env python3
"""AUTO-TRANSLATE Part 3 no-words test (fresh maker, 2026-11-13).
Hides words, keeps icons: a style rule makes all text transparent EXCEPT
the icon twins (.os-jewel), the + menu icon spans (.fc-pi-ico) and the
bottom bar (#naya-notif-bar, SVG currentColor icons). Emoji (💬✉️🌍⭐🔊🎥)
render in full colour regardless of `color`, so they stay visible; only
word-glyphs vanish. Layout untouched (no font-size/display changes).
Five steps, each by icon + position + colour alone, tap target recorded
with a screenshot. 390 first, then 1440."""
import json, sys
from playwright.sync_api import sync_playwright
URL = 'file:///home/hatch/workspace/personal-complete-wt/TEAM-NITRO/personal-page-complete-20261113/personal-complete.html'
W = int(sys.argv[1]) if len(sys.argv) > 1 else 390
WORK = '/home/hatch/workspace/team-nitro/auto-translate-20261113/'
HIDE_CSS = """
* { color: transparent !important; text-shadow: none !important; }
.os-jewel, .os-jewel * { color: var(--jc, #fff) !important; }
.fc-pi-ico { color: #fff !important; }
#naya-notif-bar, #naya-notif-bar * { color: #fff !important; }
::placeholder { color: transparent !important; }
input, textarea { color: transparent !important; }
"""
R = {'width': W}
def rect(p, sel):
    return p.evaluate("(s) => { var e=document.querySelector(s); if(!e) return null; var r=e.getBoundingClientRect(); return {x:Math.round(r.x), y:Math.round(r.y), w:Math.round(r.width), h:Math.round(r.height), visible: r.width>0 && r.height>0}; }", sel)
def vis(p, sel):
    return p.evaluate("(s) => { var e=document.querySelector(s); if(!e) return 'missing'; var r=e.getBoundingClientRect(); var cs=getComputedStyle(e); return {w:Math.round(r.width), h:Math.round(r.height), display:cs.display, visibility:cs.visibility, hidden:!!e.hidden}; }", sel)
with sync_playwright() as pw:
    br = pw.firefox.launch()
    ctx = br.new_context(viewport={'width': W, 'height': 844})
    p = ctx.new_page()
    ce, pe = [], []
    p.on('console', lambda m: ce.append(m.text[:160]) if m.type == 'error' else None)
    p.on('pageerror', lambda e: pe.append(str(e)))
    p.goto(URL, wait_until='domcontentloaded', timeout=60000)
    p.wait_for_timeout(12000)
    p.add_style_tag(content=HIDE_CSS)
    p.wait_for_timeout(500)
    R['page_errors'] = pe
    R['console_error_count'] = len(ce)
    R['console_non_supabase'] = [c for c in ce if 'supabase' not in c.lower() and 'Cross-Origin' not in c][:10]
    R['overflow0'] = p.evaluate("({sw: document.documentElement.scrollWidth, iw: window.innerWidth})")
    # --- STEP 1 ENTER: cover + orb visible, hero row buttons visible as shapes ---
    R['step1_enter'] = {
        'cover': rect(p, '#cvr'),
        'orb': rect(p, '.ph-orb, .pc-orb, [class*="orb"]'),
        'heroBtns': p.evaluate("() => ['msgbtn','aboutbtn','myworldbtn','skillsbtn','connbtn','growthbtn','sharebtn','joinbtn'].map(id=>{var e=document.getElementById(id); var r=e?e.getBoundingClientRect():null; return {id:id, w:r?Math.round(r.width):0, h:r?Math.round(r.height):0};})"),
        'pill': rect(p, '#pointscount'),
    }
    p.screenshot(path=WORK + 'proof-%d-nowords-1-enter.png' % W)
    # --- STEP 2 FIND YOUR WORLD: spaces seg (icon-only circle) opens the left drawer ---
    R['step2_seg'] = rect(p, '.notif-seg[data-notif="spaces"]')
    p.evaluate("() => { var s=document.querySelector('.notif-seg[data-notif=\"spaces\"]'); if(s) s.click(); }")
    p.wait_for_timeout(1200)
    R['step2_drawer'] = {
        'drawerOpen': p.evaluate("() => document.getElementById('os-drawer').classList.contains('open')"),
        'worlds': p.evaluate("""() => ['personal','business','space'].map(w=>{var a=document.querySelector('#os-drawer a[href*=\"/'+w+'\"]'); if(!a) return {w:w, found:false}; var r=a.getBoundingClientRect(); var j=a.querySelector('.os-jewel'); var jr=j?j.getBoundingClientRect():null; var cs=j?getComputedStyle(j):null; return {w:w, rect:{x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height)}, jewel: !!j, jewelColor: cs?cs.getPropertyValue('--jc'):null, jewelRect: jr?{x:Math.round(jr.x),y:Math.round(jr.y),w:Math.round(jr.width),h:Math.round(jr.height)}:null};})"""),
    }
    p.screenshot(path=WORK + 'proof-%d-nowords-2-worlds.png' % W)
    # close the drawer via the backdrop (do NOT follow the world link — it navigates away)
    p.evaluate("() => { var b=document.getElementById('os-backdrop'); if(b) b.click(); }")
    p.wait_for_timeout(800)
    R['step2_closed'] = p.evaluate("() => !document.getElementById('os-drawer').classList.contains('open')")
    # --- STEP 3 READ THE FEED: the Public tab by its globe jewel ---
    p.evaluate("() => { var t=document.getElementById('mwTabNaya'); if(t) t.scrollIntoView({block:'center'}); }")
    p.wait_for_timeout(600)
    R['step3_tab'] = {'rect': rect(p, '#mwTabNaya'), 'jewel': p.evaluate("() => { var t=document.getElementById('mwTabNaya'); var j=t?t.querySelector('.os-jewel'):null; return j?{txt:j.textContent, jc:getComputedStyle(j).getPropertyValue('--jc')}:null; }")}
    p.evaluate("() => { var t=document.getElementById('mwTabNaya'); if(t) t.click(); }")
    p.wait_for_timeout(1200)
    R['step3_after'] = p.evaluate("() => { var t=document.getElementById('mwTabNaya'); return {selected: t?t.getAttribute('aria-selected'):null, active: t?t.classList.contains('active'):null}; }")
    p.screenshot(path=WORK + 'proof-%d-nowords-3-feed.png' % W)
    # back to the Personal tab so the composer + rail steps run on the home feed
    p.evaluate("() => { var t=document.getElementById('mwTabSmart'); if(t) t.click(); }")
    p.wait_for_timeout(1000)
    # --- STEP 4 MAKE A POST: plus seg opens the + menu, first item is the post (pencil icon) ---
    R['step4_plus_seg'] = rect(p, '.notif-seg[data-notif="plus"]')
    p.evaluate("() => { var s=document.querySelector('.notif-seg[data-notif=\"plus\"]'); if(s) s.click(); }")
    p.wait_for_timeout(1000)
    R['step4_menu'] = {
        'menuVisible': p.evaluate("() => { var m=document.getElementById('fcPlusMenu'); return m ? !m.hidden : 'missing'; }"),
        'items': p.evaluate("""() => [...document.querySelectorAll('.fc-plusitem')].map((b,i)=>{var r=b.getBoundingClientRect(); var ic=b.querySelector('.fc-pi-ico'); return {i:i, ico: ic?ic.textContent:null, rect:{x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height)}, visible: r.width>0};})"""),
    }
    p.screenshot(path=WORK + 'proof-%d-nowords-4-plusmenu.png' % W)
    p.evaluate("() => { var b=document.querySelectorAll('.fc-plusitem')[0]; if(b) b.click(); }")
    p.wait_for_timeout(1200)
    R['step4_after'] = {
        'composer': vis(p, '#tg-hint'),
        'composerBox': vis(p, '.tg-input, #os-note-input, textarea'),
        'menuClosed': p.evaluate("() => { var m=document.getElementById('fcPlusMenu'); return m ? !!m.hidden : null; }"),
    }
    p.screenshot(path=WORK + 'proof-%d-nowords-4-composer.png' % W)
    # --- STEP 5 TALK TO SOMEONE: first rail card's Chat button (speech-balloon icon) ---
    p.evaluate("() => { var r=document.querySelector('.pc-card'); if(r) r.scrollIntoView({block:'center'}); }")
    p.wait_for_timeout(800)
    R['step5_rail'] = {
        'card': rect(p, '.pc-card'),
        'chatBtn': p.evaluate("""() => { var b=document.querySelector('.pc-card .pc-btn[data-pc-act="chat"]'); if(!b) return null; var r=b.getBoundingClientRect(); return {rect:{x:Math.round(r.x),y:Math.round(r.y),w:Math.round(r.width),h:Math.round(r.height)}, text:(b.textContent||'').trim()}; }"""),
    }
    p.evaluate("() => { var b=document.querySelector('.pc-card .pc-btn[data-pc-act=\"chat\"]'); if(b) b.click(); }")
    p.wait_for_timeout(1500)
    R['step5_after'] = {
        'chat': vis(p, '#fcChat'),
        'picker': vis(p, '#fcPicker'),
    }
    p.screenshot(path=WORK + 'proof-%d-nowords-5-talk.png' % W)
    br.close()
json.dump(R, open(WORK + 'verify-nowords-%d.json' % W, 'w'), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
