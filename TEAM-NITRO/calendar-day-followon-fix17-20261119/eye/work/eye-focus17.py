#!/usr/bin/env python3
"""CAPTAIN'S EYE follow-up: Summary door scrolled into view + Worlds scrolled
to bottom + Change-cover band clearance, at 390, both font states.
Usage: eye-focus17.py [firefox|chromium]
"""
import json, os, sys
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROUND = os.path.dirname(HERE)
SHOTS = os.path.join(ROUND, "eye", "shots")
WHICH = sys.argv[1] if len(sys.argv) > 1 else "chromium"
TAG = f"eye-focus-{WHICH}-390"
URL = ("https://naya-proof-host.nayapower.workers.dev/?file=TEAM-NITRO/day-view-v18-fix-20261117/"
       "the-ultimate-calendar-v18-fix.staged.html&ref=calendar/day-followon-fix17-20261119"
       "&cb=f4c05109531f8b737891a43f6ea6bdcef84eddc9")

def open_day(page, d):
    page.evaluate("() => { const b = document.getElementById('backToMonth'); if (b) b.click(); }")
    page.wait_for_timeout(600)
    page.evaluate("(dd) => { const c=[...document.querySelectorAll('.cell[data-d]')].find(x=>+x.dataset.d===dd); if(c) c.click(); }", d)
    page.wait_for_timeout(2000)

def goto_slide(page, idx):
    page.evaluate("(i) => { const dots=[...document.querySelectorAll('#dayScroll .sb-dots button')]; if(dots[i]) dots[i].click(); }", idx)
    page.wait_for_timeout(2000)

with sync_playwright() as p:
    errs = []
    if WHICH == "firefox":
        browser = p.firefox.launch()
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.route("**/*fonts.g*/*", lambda route: route.abort())
        page.route("**/*gstatic.com/*", lambda route: route.abort())
    else:
        browser = p.chromium.launch(args=["--no-sandbox"], proxy={"server": "http://127.0.0.1:18080"})
        ctx = browser.new_context(viewport={"width": 390, "height": 844}, ignore_https_errors=True)
        page = ctx.new_page()
    page.on("pageerror", lambda e: errs.append(str(e)))
    page.goto(URL, wait_until="load", timeout=90000)
    page.wait_for_timeout(3000)
    print(f"=== {TAG} ===")
    # 1. Summary door scrolled into view, day 19 (and day 21, worst wisdom day stack)
    for d in (19, 21):
        open_day(page, d)
        goto_slide(page, 6)
        before = page.evaluate("""() => { const on=[...document.querySelectorAll('#dayScroll .smart-block')].find(e=>e.classList.contains('on'));
          const door=[...on.querySelectorAll('button, [role=button], a')].find(b=>/Your Journal/i.test(b.textContent));
          const cc=[...document.querySelectorAll('button')].find(b=>/Change cover/i.test(b.textContent));
          const r=(el)=>{const b=el.getBoundingClientRect(); return {top:Math.round(b.top),bottom:Math.round(b.bottom)};};
          return {door: door?r(door):null, cc: cc?r(cc):null}; }""")
        # scroll the slide's own scroll container so the door comes into view
        page.evaluate("""() => { const on=[...document.querySelectorAll('#dayScroll .smart-block')].find(e=>e.classList.contains('on'));
          const sb=on?on.querySelector('.sb-scroll'):null;
          const door=[...on.querySelectorAll('button, [role=button], a')].find(b=>/Your Journal/i.test(b.textContent));
          if (sb && door) { door.scrollIntoView({block:'center'}); } }""")
        page.wait_for_timeout(1200)
        after = page.evaluate("""() => { const on=[...document.querySelectorAll('#dayScroll .smart-block')].find(e=>e.classList.contains('on'));
          const door=[...on.querySelectorAll('button, [role=button], a')].find(b=>/Your Journal/i.test(b.textContent));
          const cc=[...document.querySelectorAll('button')].find(b=>/Change cover/i.test(b.textContent));
          const sb=on?on.querySelector('.sb-scroll'):null;
          const r=(el)=>{const b=el.getBoundingClientRect(); return {top:Math.round(b.top),bottom:Math.round(b.bottom),left:Math.round(b.left),right:Math.round(b.right)};};
          const hit=(el,frac)=>{ if(!el) return null; const b=el.getBoundingClientRect();
            const e=document.elementFromPoint(Math.round(b.x+b.width/2), Math.round(b.y+b.height*frac));
            return e?(e.tagName+'.'+String(e.className).split(' ')[0]):'NONE'; };
          const ov=(a,b)=>a&&b&&!(a.right<=b.left||b.right<=a.left||a.bottom<=b.top||b.bottom<=a.top);
          const sbr=sb?sb.getBoundingClientRect():null;
          return {door: door?r(door):null, doorText: door?door.textContent.replace(/\\s+/g,' ').trim().slice(0,40):null,
            cc: cc?r(cc):null, overlapCC: ov(r(door), r(cc)),
            hitC: hit(door,0.5), hitB: hit(door,0.92),
            scrollWin: sbr?{top:Math.round(sbr.top),bottom:Math.round(sbr.bottom)}:null,
            doorWholeInWin: door && sbr ? (door.getBoundingClientRect().top>=sbr.top-1 && door.getBoundingClientRect().bottom<=sbr.bottom+1) : null}; }""")
        print(f"day {d} Summary door: at-rest door={before['door']} cc={before['cc']} | scrolled door={after['door']} text={after['doorText']!r} overlapCC={after['overlapCC']} hitC={after['hitC']} hitB={after['hitB']} win={after['scrollWin']} wholeInWin={after['doorWholeInWin']}")
        page.screenshot(path=os.path.join(SHOTS, f"focus-{TAG}-summary-door-day{d}.png"))
    # 2. Worlds scrolled to bottom, day 19
    open_day(page, 19)
    goto_slide(page, 3)
    page.evaluate("""() => { const on=[...document.querySelectorAll('#dayScroll .smart-block')].find(e=>e.classList.contains('on'));
      const sb=on?on.querySelector('.sb-scroll'):null; if(sb) sb.scrollTop=sb.scrollHeight; }""")
    page.wait_for_timeout(1200)
    w = page.evaluate("""() => { const on=[...document.querySelectorAll('#dayScroll .smart-block')].find(e=>e.classList.contains('on'));
      const cells=[...on.querySelectorAll('.world-cell')];
      const cc=[...document.querySelectorAll('button')].find(b=>/Change cover/i.test(b.textContent));
      const sb=on?on.querySelector('.sb-scroll'):null;
      const r=(el)=>{const b=el.getBoundingClientRect(); return {top:Math.round(b.top),bottom:Math.round(b.bottom)};};
      const ov=(a,b)=>a&&b&&!(a.right<=b.left||b.right<=a.left||a.bottom<=b.top||b.bottom<=a.top);
      const sbr=sb?sb.getBoundingClientRect():null;
      return {count: cells.length, cc: cc?r(cc):null,
        cells: cells.map(c=>{ const h=c.querySelector('h3, .wl, [class*=name]'); const s=c.querySelector('p, .ws, [class*=sub]');
          return {label: h?h.textContent.trim():null, rect: r(c),
            wholeInWin: sbr?(c.getBoundingClientRect().top>=sbr.top-1 && c.getBoundingClientRect().bottom<=sbr.bottom+1):null,
            overlapsCC: ov(r(c), r(cc))}; }),
        scrollWin: sbr?{top:Math.round(sbr.top),bottom:Math.round(sbr.bottom)}:null}; }""")
    print("WORLDS scrolled-to-bottom:", json.dumps(w))
    page.screenshot(path=os.path.join(SHOTS, f"focus-{TAG}-worlds-bottom.png"))
    # 3. Change-cover band clearance, day 19, slides 1/2/4/5/6/7/8
    open_day(page, 19)
    for idx in (1, 2, 4, 5, 6, 7, 8):
        goto_slide(page, idx)
        c = page.evaluate("""() => { const on=[...document.querySelectorAll('#dayScroll .smart-block')].find(e=>e.classList.contains('on'));
          const dots=on?on.querySelector('.sb-dots'):null;
          const cc=[...document.querySelectorAll('button')].find(b=>/Change cover/i.test(b.textContent));
          const back=on.querySelector('.slide-back');
          const title=on.querySelector('h1,h2,h3,.sb-title,[class*=title]');
          const r=(el)=>{if(!el) return null; const b=el.getBoundingClientRect(); return {top:Math.round(b.top),bottom:Math.round(b.bottom),left:Math.round(b.left),right:Math.round(b.right)};};
          const ccR=r(cc);
          const backR=r(back);
          const backVisible = back ? (getComputedStyle(back).display !== 'none' && backR && backR.right > 0) : false;
          // lowest title top among visible headings in the slide
          const heads=[...on.querySelectorAll('h1,h2,h3')].map(h=>r(h)).filter(x=>x&&x.top>=0);
          const lowestTitleTop = heads.length?Math.min(...heads.map(h=>h.top)):null;
          return {slide: idx, dots: r(dots), cc: ccR, back: backR, backVisible,
            lowestTitleTop,
            dotsGap: (dots&&ccR)?ccR.top-Math.round(dots.getBoundingClientRect().bottom):null,
            titleGap: (lowestTitleTop!==null&&ccR)?lowestTitleTop-ccR.bottom:null,
            backGap: (backVisible&&ccR)?ccR.left-backR.right:null}; }""".replace("idx", str(idx)))
        print(f"slide {idx} band: dots={c['dots']} cc={c['cc']} back={c['back']} backVis={c['backVisible']} lowestTitleTop={c['lowestTitleTop']} dotsGap={c['dotsGap']} titleGap={c['titleGap']} backGap={c['backGap']}")
    print("PAGE ERRORS:", errs if errs else "NONE")
    browser.close()
print("DONE", TAG)
