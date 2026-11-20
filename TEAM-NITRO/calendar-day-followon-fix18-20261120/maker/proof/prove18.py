#!/usr/bin/env python3
"""MAKER fix-18: full render proof on FIXED bytes (fixed-fix18.html).
Firefox/Chromium, fonts/nofont, 390/1920. 2s waits after every navigation.
Measures, per slide per day: Change-cover rect + visibility, overlap vs the
weather pill, vs EVERY on-slide button, vs the nav; nav whole + clear of rim;
Smart Meet pill hit-test; buttons; month grid; 0 page errors.
Usage: prove17.py [firefox|chromium] [fonts|nofont] [390|1920]
Screenshots -> maker/proof/shots18/
"""
import json, os, sys
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
FIXED = open(os.path.join(HERE, "fixed-fix18.html"), encoding="utf-8").read()
SHOTS = os.path.join(HERE, "shots18")
os.makedirs(SHOTS, exist_ok=True)
WHICH = sys.argv[1] if len(sys.argv) > 1 else "firefox"
FONT = sys.argv[2] if len(sys.argv) > 2 else "nofont"
W = int(sys.argv[3]) if len(sys.argv) > 3 else 390
H = 844 if W == 390 else 999
TAG = f"{WHICH}-{FONT}-{W}"

WIS = r"""() => {
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect();
    return {x:Math.round(b.x), y:Math.round(b.y), w:Math.round(b.width), h:Math.round(b.height), top:Math.round(b.top), bottom:Math.round(b.bottom)}; };
  const rim = document.querySelector('.rf-rim');
  const rimLineTop = rim ? Math.round(rim.getBoundingClientRect().bottom) - 3 : null;
  const q = document.querySelector('#wisdomQuote');
  const dt = document.querySelector('#wisdomBanner .dayteach');
  const st = document.querySelector('#wisdomBanner .wq-store');
  const pill = document.querySelector('#wxBottomLeft .wx-btn');
  const ml = document.querySelector('.hl-monthline');
  const greet = document.querySelector('#wisdomBanner .greet-hello');
  const back = document.querySelector('#wisdomBanner .slide-back');
  const nav = document.querySelector('#wisdomBanner .sb-nav');
  const cc = [...document.querySelectorAll('button')].find(b=>/Change cover/i.test(b.textContent));
  const ccVis = cc ? (getComputedStyle(cc).display !== 'none' && cc.getBoundingClientRect().width > 0) : null;
  const hit = (el) => { if (!el) return null; const b = el.getBoundingClientRect();
    const e = document.elementFromPoint(Math.round(b.x + b.width/2), Math.round(b.bottom - 5));
    return e ? (e.tagName + '.' + String(e.className).split(' ')[0]) : 'NONE'; };
  const ov = (a,b) => a && b && !(a.x+a.w<=b.x || b.x+b.w<=a.x || a.y+a.h<=b.y || b.y+b.h<=a.y);
  return {day: ml ? ml.textContent.replace(/\s+/g,' ').trim() : null,
    greet: greet ? greet.textContent : null,
    fonts: [...document.fonts].map(f=>f.family+':'+f.status),
    quoteLines: q ? Math.round(q.getBoundingClientRect().height / parseFloat(getComputedStyle(q).lineHeight)) : null,
    teach: r(dt), store: r(st), pill: r(pill), nav: r(nav),
    teachHit: hit(dt), storeHit: hit(st),
    pillClear: (pill && st) ? Math.round(pill.getBoundingClientRect().top - st.getBoundingClientRect().bottom) : null,
    rimLineTop, navClear: (nav&&rimLineTop!==null)?rimLineTop-Math.round(nav.getBoundingClientRect().bottom):null,
    navWhole: nav ? (nav.getBoundingClientRect().top >= 0 && nav.getBoundingClientRect().bottom <= innerHeight) : null,
    backOverlapsHello: ov(r(back), r(greet)),
    changeCover: r(cc), ccVisible: ccVis,
    ccOverlapsWeather: ccVis ? ov(r(cc), r(pill)) : false,
    docScrollW: document.documentElement.scrollWidth};
}"""

SLIDE = r"""() => {
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect();
    return {x:Math.round(b.x), y:Math.round(b.y), w:Math.round(b.width), h:Math.round(b.height), top:Math.round(b.top), bottom:Math.round(b.bottom)}; };
  const rim = document.querySelector('.rf-rim');
  const rimLineTop = rim ? Math.round(rim.getBoundingClientRect().bottom) - 3 : null;
  const on = [...document.querySelectorAll('#dayScroll .smart-block')].find(e=>e.classList.contains('on'));
  const nav = on ? on.querySelector('.sb-nav') : null;
  const cc = [...document.querySelectorAll('button')].find(b=>/Change cover/i.test(b.textContent));
  const ccVis = cc ? (getComputedStyle(cc).display !== 'none' && cc.getBoundingClientRect().width > 0) : null;
  const wx = document.querySelector('#wxBottomLeft .wx-btn');
  const wxVis = wx ? (getComputedStyle(wx).display !== 'none' && wx.getBoundingClientRect().width > 0) : null;
  const ov = (a,b) => a && b && !(a.x+a.w<=b.x || b.x+b.w<=a.x || a.y+a.h<=b.y || b.y+b.h<=a.y);
  const btns = on ? [...on.querySelectorAll('button')].map(b=>({t:(b.textContent||'').trim().slice(0,18), ...r(b)})) : [];
  const ccHits = (ccVis ? btns.filter(b=>ov(b, r(cc))).map(b=>b.t) : []);
  const ccHitCenter = ccVis ? (()=>{ const b = cc.getBoundingClientRect();
    const e = document.elementFromPoint(Math.round(b.x+b.width/2), Math.round(b.y+b.height/2));
    return e ? (e.tagName+'.'+String(e.className).split(' ')[0]+':'+(e.textContent||'').trim().slice(0,20)) : 'NONE'; })() : null;
  const smart = on ? [...on.querySelectorAll('button')].find(b=>/Smart Meet/i.test(b.textContent)) : null;
  const smartHit = smart ? (()=>{ const b = smart.getBoundingClientRect();
    const e = document.elementFromPoint(Math.round(b.x+b.width/2), Math.round(b.y+b.height/2));
    return e ? (e.tagName+'.'+String(e.className).split(' ')[0]+':'+(e.textContent||'').trim().slice(0,20)) : 'NONE'; })() : null;
  const smartHitBot = smart ? (()=>{ const b = smart.getBoundingClientRect();
    const e = document.elementFromPoint(Math.round(b.x+b.width/2), Math.round(b.y+b.height*0.9));
    return e ? (e.tagName+'.'+String(e.className).split(' ')[0]+':'+(e.textContent||'').trim().slice(0,20)) : 'NONE'; })() : null;
  return {slide: on ? on.textContent.replace(/\\s+/g,' ').trim().slice(0,28) : null,
    rimLineTop, nav: r(nav), navClear: (nav&&rimLineTop!==null)?rimLineTop-Math.round(nav.getBoundingClientRect().bottom):null,
    navWhole: nav ? (nav.getBoundingClientRect().top >= 0 && nav.getBoundingClientRect().bottom <= innerHeight) : null,
    changeCover: r(cc), ccVisible: ccVis, ccHitCenter,
    ccOverlapsWeather: (ccVis && wxVis) ? ov(r(cc), r(wx)) : false,
    ccOverlapsSlideBtns: ccHits,
    smartMeet: r(smart), smartHit, smartHitBot,
    docScrollW: document.documentElement.scrollWidth};
}"""

def open_day(page, d):
    page.evaluate("() => { const b = document.getElementById('backToMonth'); if (b) b.click(); }")
    page.wait_for_timeout(600)
    page.evaluate("(dd) => { const c=[...document.querySelectorAll('.cell[data-d]')].find(x=>+x.dataset.d===dd); if(c) c.click(); }", d)
    page.wait_for_timeout(2000)

def next_slide(page):
    page.evaluate("""() => { const on=[...document.querySelectorAll('#dayScroll .smart-block')].find(e=>e.classList.contains('on')); const b=on?on.querySelector('.deck-next'):null; if(b) b.click(); }""")
    page.wait_for_timeout(2000)

with sync_playwright() as p:
    errs = []
    if WHICH == "firefox":
        browser = p.firefox.launch()
        page = browser.new_page(viewport={"width": W, "height": H})
    else:
        browser = p.chromium.launch(args=["--no-sandbox"], proxy={"server": "http://127.0.0.1:18080"})
        ctx = browser.new_context(viewport={"width": W, "height": H}, ignore_https_errors=True)
        page = ctx.new_page()
    page.on("pageerror", lambda e: errs.append(str(e)))
    if FONT == "nofont":
        page.route("**/*fonts.g*/*", lambda route: route.abort())
        page.route("**/*gstatic.com/*", lambda route: route.abort())
    page.set_content(FIXED, wait_until="load", timeout=60000)
    page.wait_for_timeout(3000)
    print(f"=== {TAG} {W}x{H} ===")
    print("--- sweep (wisdom, 7 days) ---")
    n = 0
    for d in (15, 16, 17, 18, 19, 20, 21):
        open_day(page, d)
        m = page.evaluate(WIS)
        ok = (m['teachHit'] == 'DIV.dayteach' and m['storeHit'] == 'DIV.wq-store'
              and m['pillClear'] is not None and m['pillClear'] >= 4
              and m['navWhole'] and m['navClear'] is not None and m['navClear'] >= 0
              and m['docScrollW'] == W and not m['backOverlapsHello']
              and not m['ccOverlapsWeather'])
        n += 1 if ok else 0
        print(f"day {d}: {'PASS' if ok else 'FAIL'} qLines={m['quoteLines']} fonts={m['fonts']} "
              f"teach={m['teach']['top']}-{m['teach']['bottom']} store={m['store']['top']}-{m['store']['bottom']} "
              f"pill={m['pill']['top']}-{m['pill']['bottom']} pillClear={m['pillClear']} "
              f"nav={m['nav']['top']}-{m['nav']['bottom']} rimTop={m['rimLineTop']} navClear={m['navClear']} "
              f"ccVis={m['ccVisible']} cc={m['changeCover']['top']}-{m['changeCover']['bottom']} ccXwx={m['ccOverlapsWeather']} "
              f"greet={m['greet']!r} docW={m['docScrollW']}")
        page.screenshot(path=os.path.join(SHOTS, f"sweep-{TAG}-{d}.png"))
    print(f"sweep {TAG}: {n}/7 PASS")
    print("--- deck (day 19, 9 slides) ---")
    open_day(page, 19)
    n = 0
    for step in range(9):
        m = page.evaluate(SLIDE)
        ok = (m['navWhole'] and m['navClear'] is not None and m['navClear'] >= 0
              and m['docScrollW'] == W and not m['ccOverlapsWeather'] and not m['ccOverlapsSlideBtns'])
        n += 1 if ok else 0
        print(f"slide {step} {m['slide']}: {'PASS' if ok else 'FAIL'} nav={m['nav']['top']}-{m['nav']['bottom']} clear={m['navClear']} "
              f"ccVis={m['ccVisible']} cc={m['changeCover']['top']}-{m['changeCover']['bottom']} ccHit={m['ccHitCenter']} "
              f"ccXwx={m['ccOverlapsWeather']} ccXbtns={m['ccOverlapsSlideBtns']} "
              f"smart={m['smartMeet'] and (str(m['smartMeet']['top'])+'-'+str(m['smartMeet']['bottom']))} smartHit={m['smartHit']}/{m['smartHitBot']} docW={m['docScrollW']}")
        page.screenshot(path=os.path.join(SHOTS, f"deck-{TAG}-{step}.png"))
        if step < 8:
            next_slide(page)
    print(f"deck {TAG}: {n}/9 PASS")
    # --- buttons ---
    open_day(page, 19)
    page.evaluate("""() => { const dots=[...document.querySelectorAll('#dayScroll .sb-dots button')]; if(dots[8]) dots[8].click(); }""")
    page.wait_for_timeout(2000)
    ml_before = page.evaluate("() => { const ml=document.querySelector('.hl-monthline'); return ml?ml.textContent.replace(/\\s+/g,' ').trim():null; }")
    kept = page.evaluate("""() => { const on=[...document.querySelectorAll('#dayScroll .smart-block')].find(e=>e.classList.contains('on'));
      const k=[...on.querySelectorAll('.sb-nav button')].find(b=>/Keep reading/i.test(b.textContent));
      if(!k) return 'NO-KEEP'; k.click(); return 'CLICKED'; }""")
    page.wait_for_timeout(2000)
    ml_after = page.evaluate("() => { const ml=document.querySelector('.hl-monthline'); return ml?ml.textContent.replace(/\\s+/g,' ').trim():null; }")
    prevd = page.evaluate("""() => { const on=[...document.querySelectorAll('#dayScroll .smart-block')].find(e=>e.classList.contains('on'));
      const btns=[...on.querySelectorAll('.sb-nav button')]; if(!btns.length) return 'NO-BTNS';
      btns[0].click(); return 'CLICKED:'+btns[0].textContent.trim(); }""")
    page.wait_for_timeout(2000)
    ml_back = page.evaluate("() => { const ml=document.querySelector('.hl-monthline'); return ml?ml.textContent.replace(/\\s+/g,' ').trim():null; }")
    print(f"BUTTONS keep={kept} before={ml_before!r} after={ml_after!r} | prev={prevd} afterPrev={ml_back!r}")
    page.evaluate("() => { const b=document.getElementById('backToMonth'); if(b) b.click(); }")
    page.wait_for_timeout(1000)
    month = page.evaluate("""() => { const cells=[...document.querySelectorAll('#grid .cell, .cell')];
      const num=[...document.querySelectorAll('.cell[data-d]')];
      const blank=[...document.querySelectorAll('.cell.blank')];
      const row6=[...document.querySelectorAll('.cell')].slice(35,42).map(c=>({blank:c.classList.contains('blank'), d:c.dataset.d||null}));
      return {total: cells.length, numbered: num.length, blank: blank.length,
        name:(document.getElementById('monthName')||{}).textContent, row6}; }""")
    print("MONTH:", json.dumps(month))
    page.screenshot(path=os.path.join(SHOTS, f"month-{TAG}.png"))
    print("PAGE ERRORS:", errs if errs else "NONE")
    browser.close()
