#!/usr/bin/env python3
"""CHECKER (independent, fix-18) — my own render proof on the FETCHED fixed bytes.
Usage: check18.py [firefox|chromium] [390|1920]
Firefox = no-webfont fallback (fonts routes blocked). Chromium = fonts-loaded via
localhost forwarder 127.0.0.1:18080. 2s waits after every deck navigation.
Covers: item 1 header geometry, item 2 Hz census + wisdom, item 3 per-slide pill
census + my own pixel-diff cover-visibility census, fix-17 hold (7/7 sweep, 9/9
deck, buttons by real tap, month grid), file-picker tap test.
Screenshots -> checker/proof/shots18c/
"""
import json, os, sys
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
FIXED = open(os.path.join(HERE, "fetched-fixed.html"), encoding="utf-8").read()
SHOTS = os.path.join(HERE, "shots18c")
os.makedirs(SHOTS, exist_ok=True)
WHICH = sys.argv[1] if len(sys.argv) > 1 else "firefox"
W = int(sys.argv[2]) if len(sys.argv) > 2 else 390
H = 844 if W == 390 else 999
FONT = "nofont" if WHICH == "firefox" else "fonts"
TAG = f"{WHICH}-{FONT}-{W}"

HDR = r"""() => {
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect();
    return {x:Math.round(b.x), y:Math.round(b.y), w:Math.round(b.width), h:Math.round(b.height),
      left:Math.round(b.left), right:Math.round(b.right), top:Math.round(b.top), bottom:Math.round(b.bottom),
      cx:Math.round(b.left+b.width/2), cy:Math.round(b.top+b.height/2)}; };
  const head = document.querySelector('.official-headliner');
  const ml = document.querySelector('.hl-monthline');
  const script = ml ? ml.querySelector('.hl-script') : null;
  const nums = ml ? [...ml.querySelectorAll('.os-mini-num')] : [];
  // line count: distinct rounded tops of the monthline's text-node ranges
  let lines = null;
  if (ml) { const tops = new Set(); const walker = document.createTreeWalker(ml, NodeFilter.SHOW_TEXT);
    let n; while (n = walker.nextNode()) { if (!n.textContent.trim()) continue;
      const rg = document.createRange(); rg.selectNodeContents(n);
      for (const rc of rg.getClientRects()) tops.add(Math.round(rc.top)); }
    lines = [...tops].sort((a,b)=>a-b); }
  const vwC = Math.round(innerWidth/2);
  const mlR = r(ml), scR = r(script);
  const yearSpans = nums.length ? nums.map(r) : [];
  const dt = document.querySelector('#dayTeach');
  const center = document.querySelector('.hl-center');
  const left = document.querySelector('.hl-left');
  const stats = document.querySelector('.stats-btn');
  const timewrap = document.querySelector('.hl-timewrap');
  const back = document.getElementById('backToMonth');
  const orb = document.querySelector('.daybar .sigpiece, .sigpiece');
  const deck = document.querySelector('#dayScroll');
  return {vw: innerWidth, vwCenter: vwC,
    fonts: [...document.fonts].map(f=>f.family+':'+f.status),
    headerText: head ? head.innerText.replace(/\s+/g,' ').trim() : null,
    headerHasHz: head ? /Hz|396/.test(head.innerText) : null,
    monthlineText: ml ? ml.textContent.replace(/\s+/g,' ').trim() : null,
    monthline: mlR, monthlineCenterOff: mlR ? mlR.cx - vwC : null,
    lineTops: lines, lineCount: lines ? lines.length : null,
    nov: scR, yearFirst: yearSpans[0] || null,
    novYearGap: (scR && yearSpans[0]) ? Math.round(yearSpans[0].left - scR.right) : null,
    numSpans: nums.length, yearSpans,
    centerCol: r(center), leftCol: r(left), stats: r(stats), timewrap: r(timewrap),
    backToMonth: r(back), orb: r(orb), deck: r(deck),
    timeUnderMonth: (mlR && timewrap) ? Math.round(r(timewrap).cy - mlR.bottom) : null,
    wisdom: dt ? dt.textContent.replace(/\s+/g,' ').trim() : null,
    wisdomHz: dt ? (dt.textContent.match(/396/g)||[]).length : null,
    docScrollW: document.documentElement.scrollWidth,
    greet: (document.querySelector('#wisdomBanner .greet-hello')||{}).textContent || null};
}"""

PILL = r"""() => {
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect();
    return {x:Math.round(b.x), y:Math.round(b.y), w:Math.round(b.width), h:Math.round(b.height),
      top:Math.round(b.top), bottom:Math.round(b.bottom), left:Math.round(b.left), right:Math.round(b.right)}; };
  const on = [...document.querySelectorAll('#dayScroll .smart-block')].find(e=>e.classList.contains('on'));
  const cc = [...document.querySelectorAll('button')].find(b=>/Change cover/i.test(b.textContent));
  const disp = cc ? getComputedStyle(cc).display : null;
  const vis = cc ? (disp !== 'none' && cc.getBoundingClientRect().width > 0 && cc.getBoundingClientRect().height > 0) : false;
  let hit = null;
  if (cc && vis) { const b = cc.getBoundingClientRect();
    const e = document.elementFromPoint(Math.round(b.x+b.width/2), Math.round(b.y+b.height/2));
    hit = e ? (e.tagName+'.'+String(e.className).split(' ')[0]+':'+(e.textContent||'').trim().slice(0,14)) : 'NONE'; }
  const nav = on ? on.querySelector('.sb-nav') : null;
  const rim = document.querySelector('.rf-rim');
  const rimTop = rim ? Math.round(rim.getBoundingClientRect().bottom) - 3 : null;
  return {slide: on ? on.textContent.replace(/\s+/g,' ').trim().slice(0,30) : null,
    slideIdx: on ? [...document.querySelectorAll('#dayScroll .smart-block')].indexOf(on) : -1,
    pill: r(cc), pillDisplay: disp, pillVisible: vis, pillHit: hit,
    nav: r(nav), navWhole: nav ? (nav.getBoundingClientRect().top>=0 && nav.getBoundingClientRect().bottom<=innerHeight) : null,
    navClear: (nav && rimTop!==null) ? rimTop - Math.round(nav.getBoundingClientRect().bottom) : null,
    docScrollW: document.documentElement.scrollWidth};
}"""

WIS = r"""() => {
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect();
    return {x:Math.round(b.x), y:Math.round(b.y), w:Math.round(b.width), h:Math.round(b.height), top:Math.round(b.top), bottom:Math.round(b.bottom)}; };
  const rim = document.querySelector('.rf-rim');
  const rimTop = rim ? Math.round(rim.getBoundingClientRect().bottom) - 3 : null;
  const q = document.querySelector('#wisdomQuote');
  const dt = document.querySelector('#wisdomBanner .dayteach');
  const st = document.querySelector('#wisdomBanner .wq-store');
  const pill = document.querySelector('#wxBottomLeft .wx-btn');
  const nav = document.querySelector('#wisdomBanner .sb-nav');
  const greet = document.querySelector('#wisdomBanner .greet-hello');
  const back = document.querySelector('#wisdomBanner .slide-back');
  const cc = [...document.querySelectorAll('button')].find(b=>/Change cover/i.test(b.textContent));
  const ccDisp = cc ? getComputedStyle(cc).display : null;
  const ccVis = cc ? (ccDisp !== 'none' && cc.getBoundingClientRect().width > 0) : null;
  const hit = (el, frac) => { if (!el) return null; const b = el.getBoundingClientRect();
    const e = document.elementFromPoint(Math.round(b.x+b.width/2), Math.round(b.y+b.height*frac));
    return e ? (e.tagName+'.'+String(e.className).split(' ')[0]) : 'NONE'; };
  const ov = (a,b) => a && b && !(a.x+a.w<=b.x || b.x+b.w<=a.x || a.y+a.h<=b.y || b.y+b.h<=a.y);
  return {fonts: [...document.fonts].map(f=>f.family+':'+f.status),
    teachHit: hit(dt,0.9), storeHit: hit(st,0.9),
    pillClear: (pill&&st) ? Math.round(pill.getBoundingClientRect().top - st.getBoundingClientRect().bottom) : null,
    navWhole: nav ? (nav.getBoundingClientRect().top>=0 && nav.getBoundingClientRect().bottom<=innerHeight) : null,
    navClear: (nav&&rimTop!==null) ? rimTop-Math.round(nav.getBoundingClientRect().bottom) : null,
    nav: r(nav), teach: r(dt), store: r(st), pill: r(pill),
    backOverlapsHello: ov(r(back), r(greet)),
    ccVisible: ccVis, ccDisplay: ccDisp, cc: r(cc),
    ccOverlapsWeather: ov(r(cc), r(pill)),
    greet: greet ? greet.textContent : null, docScrollW: document.documentElement.scrollWidth};
}"""

def open_day(page, d):
    page.evaluate("() => { const b = document.getElementById('backToMonth'); if (b) b.click(); }")
    page.wait_for_timeout(600)
    page.evaluate("(dd) => { const c=[...document.querySelectorAll('.cell[data-d]')].find(x=>+x.dataset.d===dd); if(c) c.click(); }", d)
    page.wait_for_timeout(2000)

def goto_slide(page, i):
    page.evaluate("(ii) => { const dots=[...document.querySelectorAll('#dayScroll .sb-dots button')]; if(dots[ii]) dots[ii].click(); }", i)
    page.wait_for_timeout(2000)

def pause_anims(page):
    page.evaluate("() => { document.getAnimations().forEach(a => a.pause()); }")
    page.wait_for_timeout(150)

def deck_rect(page):
    return page.evaluate("() => { const e=document.querySelector('#dayScroll'); const b=e.getBoundingClientRect(); return {x:b.x,y:b.y,w:b.width,h:b.height}; }")

def count_changed(a_path, b_path, inset=6):
    from PIL import Image
    import math
    a = Image.open(a_path).convert("RGB")
    b = Image.open(b_path).convert("RGB")
    w, h = a.size
    assert b.size == (w, h), f"size mismatch {a.size} vs {b.size}"
    pa, pb = a.load(), b.load()
    changed = 0
    for y in range(inset, h - inset):
        for x in range(inset, w - inset):
            r1, g1, bl1 = pa[x, y]; r2, g2, bl2 = pb[x, y]
            if abs(r1-r2) + abs(g1-g2) + abs(bl1-bl2) > 60:
                changed += 1
    return changed

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

    # --- Item 1 + 2: header on day 20 ---
    open_day(page, 20)
    m = page.evaluate(HDR)
    m["pageErrors"] = errs
    print("HEADER:", json.dumps(m, indent=1))
    page.screenshot(path=os.path.join(SHOTS, f"header-{TAG}.png"), clip={"x": 0, "y": 0, "width": W, "height": 340})
    page.screenshot(path=os.path.join(SHOTS, f"full-{TAG}-day20.png"))

    # --- Item 3a: per-slide pill census (day 20) ---
    print("--- pill census (day 20) ---")
    for i in range(9):
        goto_slide(page, i)
        c = page.evaluate(PILL)
        print(f"slide {i}: vis={c['pillVisible']} disp={c['pillDisplay']} pill={c['pill']} hit={c['pillHit']} nav={c['nav']['top'] if c['nav'] else None}-{c['nav']['bottom'] if c['nav'] else None} navClear={c['navClear']} navWhole={c['navWhole']} docW={c['docScrollW']}")
        page.screenshot(path=os.path.join(SHOTS, f"census-{TAG}-{i}.png"))

    # --- Item 3b: my own cover-visibility census (pixel diff, drift baseline) ---
    print("--- cover visibility (pixel diff, interior >6px inset, drift baseline) ---")
    for i in range(9):
        goto_slide(page, i)
        pause_anims(page)
        dr = deck_rect(page)
        clip = {"x": dr["x"], "y": dr["y"], "width": dr["w"], "height": dr["h"]}
        on1 = os.path.join(SHOTS, f"cv-{TAG}-{i}-on1.png")
        on2 = os.path.join(SHOTS, f"cv-{TAG}-{i}-on2.png")
        off = os.path.join(SHOTS, f"cv-{TAG}-{i}-off.png")
        page.screenshot(path=on1, clip=clip)
        page.wait_for_timeout(300)
        page.screenshot(path=on2, clip=clip)
        page.evaluate("() => { const c=document.querySelector('#dayCoverBg'); if(c) c.style.display='none'; }")
        page.wait_for_timeout(300)
        page.screenshot(path=off, clip=clip)
        page.evaluate("() => { const c=document.querySelector('#dayCoverBg'); if(c) c.style.display=''; }")
        drift = count_changed(on1, on2)
        vis = count_changed(on1, off)
        print(f"slide {i}: coverChangedPx={vis} driftPx={drift} deck={dr['w']}x{dr['h']}")

    # --- Fix-17 hold: 7-day wisdom sweep ---
    print("--- sweep 15..21 ---")
    n = 0
    for d in (15, 16, 17, 18, 19, 20, 21):
        open_day(page, d)
        goto_slide(page, 0)  # day re-opens on last-viewed slide; force wisdom
        s = page.evaluate(WIS)
        ok = (s['teachHit'] == 'DIV.dayteach' and s['storeHit'] == 'DIV.wq-store'
              and s['pillClear'] is not None and s['pillClear'] >= 4
              and s['navWhole'] and s['navClear'] is not None and s['navClear'] >= 0
              and s['docScrollW'] == W and not s['backOverlapsHello']
              and (s['ccVisible'] is False if W == 390 else True) and not s['ccOverlapsWeather'])
        n += 1 if ok else 0
        print(f"day {d}: {'PASS' if ok else 'FAIL'} teachHit={s['teachHit']} storeHit={s['storeHit']} pillClear={s['pillClear']} nav={s['nav']['top']}-{s['nav']['bottom']} navClear={s['navClear']} ccVis={s['ccVisible']} cc={s['cc']['top'] if s['cc'] else None}-{s['cc']['bottom'] if s['cc'] else None} ccXwx={s['ccOverlapsWeather']} greet={s['greet']!r} docW={s['docScrollW']}")
    print(f"sweep {TAG}: {n}/7 PASS")

    # --- Fix-17 hold: 9-slide deck ---
    print("--- deck (day 19) ---")
    open_day(page, 19)
    n = 0
    for i in range(9):
        goto_slide(page, i)
        c = page.evaluate(PILL)
        ok = c['navWhole'] and c['navClear'] is not None and c['navClear'] >= 0 and c['docScrollW'] == W
        n += 1 if ok else 0
        print(f"slide {i}: {'PASS' if ok else 'FAIL'} nav={c['nav']['top']}-{c['nav']['bottom']} navClear={c['navClear']} navWhole={c['navWhole']} ccVis={c['pillVisible']} docW={c['docScrollW']}")
    print(f"deck {TAG}: {n}/9 PASS")

    # --- Buttons by real tap ---
    open_day(page, 19)
    goto_slide(page, 8)
    def head_txt():
        return page.evaluate("() => document.querySelector('.official-headliner').innerText.replace(/\\s+/g,' ').trim()")
    ml_before = page.evaluate("() => document.querySelector('.hl-monthline').textContent.replace(/\\s+/g,' ').trim()")
    hd_before = head_txt()
    kept = page.evaluate("""() => { const on=[...document.querySelectorAll('#dayScroll .smart-block')].find(e=>e.classList.contains('on'));
      const k=[...on.querySelectorAll('.sb-nav button')].find(b=>/Keep reading/i.test(b.textContent));
      if(!k) return 'NO-KEEP'; k.click(); return 'CLICKED'; }""")
    page.wait_for_timeout(2000)
    ml_after = page.evaluate("() => document.querySelector('.hl-monthline').textContent.replace(/\\s+/g,' ').trim()")
    hd_after = head_txt()
    prevd = page.evaluate("""() => { const on=[...document.querySelectorAll('#dayScroll .smart-block')].find(e=>e.classList.contains('on'));
      const btns=[...on.querySelectorAll('.sb-nav button')]; if(!btns.length) return 'NO-BTNS';
      btns[0].click(); return 'CLICKED:'+btns[0].textContent.trim(); }""")
    page.wait_for_timeout(2000)
    ml_back = page.evaluate("() => document.querySelector('.hl-monthline').textContent.replace(/\\s+/g,' ').trim()")
    hd_back = head_txt()
    print(f"BUTTONS keep={kept} before={ml_before!r} hdBefore={hd_before!r} after={ml_after!r} hdAfter={hd_after!r} | prev={prevd} afterPrev={ml_back!r} hdBack={hd_back!r}")
    page.evaluate("() => { const b=document.getElementById('backToMonth'); if(b) b.click(); }")
    page.wait_for_timeout(1000)
    month = page.evaluate("""() => { const cells=[...document.querySelectorAll('.cell')];
      const num=[...document.querySelectorAll('.cell[data-d]')];
      const blank=[...document.querySelectorAll('.cell.blank')];
      const vis=document.getElementById('screen-month') && !document.getElementById('screen-month').classList.contains('hidden');
      const row6=[...document.querySelectorAll('.cell')].slice(35,42).map(c=>({blank:c.classList.contains('blank'), d:c.dataset.d||null}));
      return {total: cells.length, numbered: num.length, blank: blank.length, monthVisible: vis,
        name:(document.getElementById('monthName')||{}).textContent, row6}; }""")
    print("MONTH:", json.dumps(month))
    page.screenshot(path=os.path.join(SHOTS, f"month-{TAG}.png"))

    # --- File-picker tap test (only where pill is visible) ---
    for (slide, label) in [(0, "Wisdom"), (3, "Worlds")]:
        open_day(page, 20)
        goto_slide(page, slide)
        vis = page.evaluate("() => { const cc=[...document.querySelectorAll('button')].find(b=>/Change cover/i.test(b.textContent)); return cc && getComputedStyle(cc).display!=='none' && cc.getBoundingClientRect().width>0; }")
        if vis:
            try:
                with page.expect_file_chooser(timeout=5000) as fc:
                    page.evaluate("() => { const cc=[...document.querySelectorAll('button')].find(b=>/Change cover/i.test(b.textContent)); cc.click(); }")
                print(f"TAP {label} {W}: file picker OPENED")
            except Exception as e:
                print(f"TAP {label} {W}: picker did NOT open: {str(e)[:120]}")
        else:
            print(f"TAP {label} {W}: pill hidden, not clickable (expected at 390 Wisdom)")
    print("PAGEERRORS:", errs)
    browser.close()
