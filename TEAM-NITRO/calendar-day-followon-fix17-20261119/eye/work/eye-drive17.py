#!/usr/bin/env python3
"""CAPTAIN'S EYE (independent, fix-17): own render proof on the STAGED URL.
Own driver, own measurements — nothing taken from the maker/checker numbers.
Firefox/Chromium, fonts/nofont, 390/1920. 2s waits after every deck nav.
Usage: eye-drive17.py [firefox|chromium] [fonts|nofont] [390|1920]
Screenshots -> eye/shots/ ; JSON -> eye/work/eye-<tag>.json
"""
import json, os, sys
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROUND = os.path.dirname(HERE)
SHOTS = os.path.join(ROUND, "eye", "shots")
os.makedirs(SHOTS, exist_ok=True)
WHICH = sys.argv[1] if len(sys.argv) > 1 else "firefox"
FONT = sys.argv[2] if len(sys.argv) > 2 else "nofont"
W = int(sys.argv[3]) if len(sys.argv) > 3 else 390
H = 844 if W == 390 else 999
TAG = f"eye-{WHICH}-{FONT}-{W}"
URL = ("https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/day-view-v18-fix-20261117/"
       "the-ultimate-calendar-v18-fix.staged.html&ref=calendar/day-followon-fix17-20261119"
       "&cb=f4c05109531f8b737891a43f6ea6bdcef84eddc9")

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
  const ccDisp = cc ? getComputedStyle(cc).display : null;
  const ccVis = cc ? (ccDisp !== 'none' && cc.getBoundingClientRect().width > 0) : null;
  const hit = (el, frac) => { if (!el) return null; const b = el.getBoundingClientRect();
    const e = document.elementFromPoint(Math.round(b.x + b.width/2), Math.round(b.y + b.height*frac));
    return e ? (e.tagName + '.' + String(e.className).split(' ')[0]) : 'NONE'; };
  const ov = (a,b) => a && b && !(a.x+a.w<=b.x || b.x+b.w<=a.x || a.y+a.h<=b.y || b.y+b.h<=a.y);
  const pillOneLine = pill ? (pill.scrollWidth <= pill.clientWidth + 1) : null;
  return {day: ml ? ml.textContent.replace(/\s+/g,' ').trim() : null,
    greet: greet ? greet.textContent : null,
    fonts: [...document.fonts].map(f=>f.family+':'+f.status),
    quoteFont: q ? getComputedStyle(q).fontSize : null,
    quoteLines: q ? Math.round(q.getBoundingClientRect().height / parseFloat(getComputedStyle(q).lineHeight)) : null,
    teach: r(dt), store: r(st), pill: r(pill), pillOneLine,
    nav: r(nav), teachHit: hit(dt, 0.9), storeHit: hit(st, 0.9),
    pillClear: (pill && st) ? Math.round(pill.getBoundingClientRect().top - st.getBoundingClientRect().bottom) : null,
    rimLineTop, navClear: (nav&&rimLineTop!==null)?rimLineTop-Math.round(nav.getBoundingClientRect().bottom):null,
    navWhole: nav ? (nav.getBoundingClientRect().top >= 0 && nav.getBoundingClientRect().bottom <= innerHeight) : null,
    backOverlapsHello: ov(r(back), r(greet)),
    changeCover: r(cc), ccVisible: ccVis, ccDisplay: ccDisp,
    ccOverlapsWeather: ov(r(cc), r(pill)),
    docScrollW: document.documentElement.scrollWidth};
}"""

SLIDE = r"""() => {
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect();
    return {x:Math.round(b.x), y:Math.round(b.y), w:Math.round(b.width), h:Math.round(b.height), top:Math.round(b.top), bottom:Math.round(b.bottom)}; };
  const rim = document.querySelector('.rf-rim');
  const rimLineTop = rim ? Math.round(rim.getBoundingClientRect().bottom) - 3 : null;
  const on = [...document.querySelectorAll('#dayScroll .smart-block')].find(e=>e.classList.contains('on'));
  const nav = on ? on.querySelector('.sb-nav') : null;
  const dots = on ? on.querySelector('.sb-dots') : null;
  const cc = [...document.querySelectorAll('button')].find(b=>/Change cover/i.test(b.textContent));
  const ccDisp = cc ? getComputedStyle(cc).display : null;
  const ccVis = cc ? (ccDisp !== 'none' && cc.getBoundingClientRect().width > 0) : null;
  const wx = document.querySelector('#wxBottomLeft .wx-btn');
  const ov = (a,b) => a && b && !(a.x+a.w<=b.x || b.x+b.w<=a.x || a.y+a.h<=b.y || b.y+b.h<=a.y);
  const ccr = r(cc);
  const visRect = (el) => { if (!el) return null; let b = el.getBoundingClientRect();
    let a = el.parentElement;
    while (a) { const cs = getComputedStyle(a);
      if (cs.overflow !== 'visible' || cs.overflowX !== 'visible' || cs.overflowY !== 'visible') {
        const ab = a.getBoundingClientRect();
        const x0 = Math.max(b.left, ab.left), y0 = Math.max(b.top, ab.top);
        const x1 = Math.min(b.right, ab.right), y1 = Math.min(b.bottom, ab.bottom);
        b = {left: x0, top: y0, right: x1, bottom: y1, width: x1 - x0, height: y1 - y0};
        if (b.width <= 0 || b.height <= 0) return {x: 0, y: 0, w: 0, h: 0, top: 0, bottom: 0, clipped: true};
      }
      a = a.parentElement; }
    const x0 = Math.max(b.left, 0), y0 = Math.max(b.top, 0);
    const x1 = Math.min(b.right, innerWidth), y1 = Math.min(b.bottom, innerHeight);
    return {x: Math.round(x0), y: Math.round(y0), w: Math.round(x1 - x0), h: Math.round(y1 - y0),
      top: Math.round(y0), bottom: Math.round(y1), clipped: (x1 - x0) <= 0 || (y1 - y0) <= 0}; };
  const btns = on ? [...on.querySelectorAll('button')].map(b=>({t:(b.textContent||'').trim().slice(0,18), ...r(b)})) : [];
  const ccHits = (ccVis ? btns.filter(b=>ov(b, ccr)).map(b=>b.t) : []);
  const leaves = [];
  if (on && ccVis) {
    const all = on.querySelectorAll('*');
    for (const el of all) {
      if (el.children.length) continue;
      const b = el.getBoundingClientRect();
      if (b.width <= 0 || b.height <= 0) continue;
      const vr = visRect(el);
      if (!vr || vr.w <= 0 || vr.h <= 0) continue;
      if (ov(vr, ccr)) leaves.push(el.tagName + '.' + String(el.className).split(' ')[0] + ':' + (el.textContent||'').trim().slice(0,20));
    }
  }
  const smart = on ? [...on.querySelectorAll('button')].find(b=>/Smart Meet/i.test(b.textContent)) : null;
  const hitAt = (el, frac) => { if (!el) return null; const b = el.getBoundingClientRect();
    const e = document.elementFromPoint(Math.round(b.x + b.width/2), Math.round(b.y + b.height*frac));
    return e ? (e.tagName + '.' + String(e.className).split(' ')[0]) : 'NONE'; };
  const journalDoor = on ? [...on.querySelectorAll('button, [role=button], a')].find(b=>/Your Journal/i.test(b.textContent)) : null;
  const journalVis = visRect(journalDoor);
  const journalOverlapsCCvis = (ccVis && journalVis && journalVis.w > 0) ? ov(journalVis, ccr) : false;
  const smartOneLine = smart ? (smart.scrollWidth <= smart.clientWidth + 1) : null;
  return {slide: on ? on.textContent.replace(/\s+/g,' ').trim().slice(0,28) : null,
    rimLineTop, nav: r(nav), navClear: (nav&&rimLineTop!==null)?rimLineTop-Math.round(nav.getBoundingClientRect().bottom):null,
    navWhole: nav ? (nav.getBoundingClientRect().top >= 0 && nav.getBoundingClientRect().bottom <= innerHeight) : null,
    dots: r(dots), changeCover: ccr, ccVisible: ccVis, ccDisplay: ccDisp,
    ccOverlapsWeather: ov(ccr, r(wx)), ccOverlapsSlideBtns: ccHits, ccOverlapsLeaves: leaves,
    smartMeet: r(smart), smartOneLine, smartHitC: hitAt(smart, 0.5), smartHitB: hitAt(smart, 0.92),
    journalDoor: r(journalDoor), journalVis, journalOverlapsCCvis, journalHitC: hitAt(journalDoor, 0.5),
    docScrollW: document.documentElement.scrollWidth};
}"""

def open_day(page, d):
    page.evaluate("() => { const b = document.getElementById('backToMonth'); if (b) b.click(); }")
    page.wait_for_timeout(600)
    page.evaluate("(dd) => { const c=[...document.querySelectorAll('.cell[data-d]')].find(x=>+x.dataset.d===dd); if(c) c.click(); }", d)
    page.wait_for_timeout(2000)

def goto_slide(page, idx):
    page.evaluate("(i) => { const dots=[...document.querySelectorAll('#dayScroll .sb-dots button')]; if(dots[i]) dots[i].click(); }", idx)
    page.wait_for_timeout(2000)

def next_slide(page):
    page.evaluate("""() => { const on=[...document.querySelectorAll('#dayScroll .smart-block')].find(e=>e.classList.contains('on')); const b=on?on.querySelector('.deck-next'):null; if(b) b.click(); }""")
    page.wait_for_timeout(2000)

out = {"tag": TAG, "url": URL, "sweep": [], "deck": [], "defect_days": [], "buttons": {}, "month": {}, "errors": []}
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
    page.on("console", lambda m: errs.append("console." + m.type + ": " + m.text) if m.type == "error" else None)
    if FONT == "nofont":
        page.route("**/*fonts.g*/*", lambda route: route.abort())
        page.route("**/*gstatic.com/*", lambda route: route.abort())
    page.goto(URL, wait_until="load", timeout=90000)
    page.wait_for_timeout(3000)
    print(f"=== {TAG} {W}x{H} ===")
    print("--- wisdom sweep (forced slide 0 per day) ---")
    n = 0
    for d in (15, 16, 17, 18, 19, 20, 21):
        open_day(page, d)
        goto_slide(page, 0)
        m = page.evaluate(WIS)
        ok = (m['teachHit'] == 'DIV.dayteach' and m['storeHit'] == 'DIV.wq-store'
              and m['pillOneLine'] and m['navWhole'] and m['navClear'] is not None and m['navClear'] >= 0
              and m['docScrollW'] == W and not m['backOverlapsHello']
              and (m['ccVisible'] is False if W == 390 else True) and not m['ccOverlapsWeather'])
        n += 1 if ok else 0
        out["sweep"].append({"day": d, "pass": ok, **m})
        print(f"day {d}: {'PASS' if ok else 'FAIL'} qLines={m['quoteLines']} qFont={m['quoteFont']} "
              f"teach={m['teach']['top']}-{m['teach']['bottom']} store={m['store']['top']}-{m['store']['bottom']} "
              f"pill={m['pill']['top']}-{m['pill']['bottom']} oneLine={m['pillOneLine']} pillClear={m['pillClear']} "
              f"nav={m['nav']['top']}-{m['nav']['bottom']} rimTop={m['rimLineTop']} navClear={m['navClear']} "
              f"cc={m['changeCover']['top']}-{m['changeCover']['bottom']} ccVis={m['ccVisible']} ccDisp={m['ccDisplay']} ccXwx={m['ccOverlapsWeather']} "
              f"greet={m['greet']!r} docW={m['docScrollW']}")
        page.screenshot(path=os.path.join(SHOTS, f"sweep-{TAG}-{d}.png"))
    print(f"sweep {TAG}: {n}/7 PASS")
    print("--- deck walk day 19 ---")
    open_day(page, 19)
    goto_slide(page, 0)
    n = 0
    for step in range(9):
        m = page.evaluate(SLIDE)
        ok = m['navWhole'] and m['navClear'] is not None and m['navClear'] >= 0 and m['docScrollW'] == W and not m['ccOverlapsSlideBtns'] and not m['ccOverlapsLeaves'] and not m['ccOverlapsWeather']
        if step == 5 and m['smartMeet']:
            ok = ok and m['smartHitC'] == 'BUTTON.elite-meetpill' and m['smartHitB'] == 'BUTTON.elite-meetpill' and m['smartOneLine']
        if step == 6 and m['journalDoor']:
            ok = ok and not m['journalOverlapsCCvis']
        n += 1 if ok else 0
        out["deck"].append({"step": step, "pass": ok, **m})
        print(f"slide {step} {m['slide']}: {'PASS' if ok else 'FAIL'} nav={m['nav']['top']}-{m['nav']['bottom']} clear={m['navClear']} "
              f"dots={m['dots']['top']}-{m['dots']['bottom']} cc={m['changeCover']['top']}-{m['changeCover']['bottom']} vis={m['ccVisible']} ccXwx={m['ccOverlapsWeather']} ccXbtns={m['ccOverlapsSlideBtns']} ccXleaves={m['ccOverlapsLeaves']} "
              f"smart={m['smartMeet'] and (str(m['smartMeet']['top'])+'-'+str(m['smartMeet']['bottom']))} oneLine={m['smartOneLine']} smartHitC={m['smartHitC']} smartHitB={m['smartHitB']} "
              f"journal={m['journalDoor'] and (str(m['journalDoor']['top'])+'-'+str(m['journalDoor']['bottom']))} journalVis={m['journalVis']} journalXccVis={m['journalOverlapsCCvis']} journalHit={m['journalHitC']} docW={m['docScrollW']}")
        page.screenshot(path=os.path.join(SHOTS, f"deck-{TAG}-{step}.png"))
        if step < 8:
            next_slide(page)
    print(f"deck {TAG}: {n}/9 PASS")
    if W == 390:
        print("--- per-day defect slides (Appointments 5 / Summary 6) ---")
        for d in (15, 16, 17, 18, 19, 20, 21):
            open_day(page, d)
            goto_slide(page, 5)
            a = page.evaluate(SLIDE)
            goto_slide(page, 6)
            s = page.evaluate(SLIDE)
            appt_ok = (a['smartMeet'] is not None and a['smartHitC'] == 'BUTTON.elite-meetpill'
                       and a['smartHitB'] == 'BUTTON.elite-meetpill' and a['smartOneLine']
                       and not a['ccOverlapsSlideBtns'] and not a['ccOverlapsLeaves']
                       and a['navWhole'] and a['navClear'] is not None and a['navClear'] >= 0)
            summ_ok = (s['journalDoor'] is not None and not s['journalOverlapsCCvis']
                       and not s['ccOverlapsSlideBtns'] and not s['ccOverlapsLeaves']
                       and s['navWhole'] and s['navClear'] is not None and s['navClear'] >= 0)
            out["defect_days"].append({"day": d, "appt_pass": appt_ok, "summ_pass": summ_ok,
                "smart": a['smartMeet'], "smartHitC": a['smartHitC'], "smartHitB": a['smartHitB'],
                "apptNav": a['nav'], "apptNavClear": a['navClear'],
                "journal": s['journalDoor'], "journalVis": s['journalVis'],
                "journalXcc": s['journalOverlapsCCvis'], "summNavClear": s['navClear']})
            print(f"day {d}: APPT {'PASS' if appt_ok else 'FAIL'} smart={a['smartMeet']['top']}-{a['smartMeet']['bottom']} hitC={a['smartHitC']} hitB={a['smartHitB']} oneLine={a['smartOneLine']} nav={a['nav']['top']}-{a['nav']['bottom']} clear={a['navClear']} | "
                  f"SUMM {'PASS' if summ_ok else 'FAIL'} journal={s['journalDoor']['top']}-{s['journalDoor']['bottom']} vis={s['journalVis']} xcc={s['journalOverlapsCCvis']} navClear={s['navClear']}")
    print("--- buttons + month ---")
    open_day(page, 19)
    goto_slide(page, 8)
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
    out["buttons"] = {"keep": kept, "before": ml_before, "after": ml_after, "prev": prevd, "afterPrev": ml_back}
    print(f"BUTTONS keep={kept} before={ml_before!r} after={ml_after!r} | prev={prevd} afterPrev={ml_back!r}")
    page.evaluate("() => { const b=document.getElementById('backToMonth'); if(b) b.click(); }")
    page.wait_for_timeout(1000)
    month = page.evaluate("""() => { const cells=[...document.querySelectorAll('#grid .cell, .cell')];
      const num=[...document.querySelectorAll('.cell[data-d]')];
      const blank=[...document.querySelectorAll('.cell.blank')];
      const vis=document.getElementById('screen-month') && !document.getElementById('screen-month').classList.contains('hidden');
      const row6=[...document.querySelectorAll('.cell')].slice(35,42).map(c=>({blank:c.classList.contains('blank'), d:c.dataset.d||null}));
      const row5=[...document.querySelectorAll('.cell')].slice(28,35).map(c=>({blank:c.classList.contains('blank'), d:c.dataset.d||null}));
      return {total: cells.length, numbered: num.length, blank: blank.length, monthVisible: vis,
        name:(document.getElementById('monthName')||{}).textContent, row5, row6}; }""")
    out["month"] = month
    print("MONTH:", json.dumps(month))
    page.screenshot(path=os.path.join(SHOTS, f"month-{TAG}.png"))
    out["errors"] = errs
    print("PAGE ERRORS:", errs if errs else "NONE")
    with open(os.path.join(HERE, f"eye-{TAG}.json"), "w") as f:
        json.dump(out, f, indent=1)
    browser.close()
print("DONE", TAG)
