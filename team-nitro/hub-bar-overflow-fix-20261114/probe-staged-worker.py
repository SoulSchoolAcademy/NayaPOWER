#!/usr/bin/env python3
"""Staged proof: walk the PROOF-HOST staged link (fixed bytes, sha 7d25f591)
at 390/360/1440 — cold link (#/smart-notes/sn2696) + Hub-direct.
Bar affordance + chevron reachability, gems, note route, feed, modal timing,
0 console/page errors. Screenshots read by eye after.
"""
import json
from playwright.sync_api import sync_playwright

BASE = "https://naya-public-blog-staging.nayapower.workers.dev/hub"
OUT = "/home/hatch/workspace/team-nitro/hub-bar-overflow-fix-20261114/work/"

MEASURE = """() => {
  const bar = document.querySelector('nav.obb-bar');
  const row = document.querySelector('.obb-row');
  const cs = (el, p, pe) => getComputedStyle(el, pe || null)[p];
  const pills = [...document.querySelectorAll('.obb-pill')].map(p => {
    const r = p.getBoundingClientRect();
    return {label: p.getAttribute('aria-label'), left: Math.round(r.left), right: Math.round(r.right),
            jewel: Math.round(p.querySelector('.obb-jewel').getBoundingClientRect().width),
            visible: r.left >= 0 && r.right <= innerWidth};
  });
  const navL = bar.querySelector('.obb-nav-l'), navR = bar.querySelector('.obb-nav-r');
  const gems = [...document.querySelectorAll('.notif-lbl')].filter(e =>
    ['Personal','Business','Thing'].includes((e.textContent||'').trim())
  ).map(lbl => { const par = lbl.parentElement;
    const ico = par ? par.querySelector('svg, .notif-ico, [class*=ico]') : null;
    const r = ico ? ico.getBoundingClientRect() : lbl.getBoundingClientRect();
    const svg = par ? par.querySelector('svg') : null;
    return {label: lbl.textContent.trim(), w: Math.round(r.width), h: Math.round(r.height),
            radius: ico ? cs(ico, 'borderRadius') : '-', svgLen: svg ? svg.outerHTML.length : 0}; });
  const modal = [...document.querySelectorAll('.naya-install-overlay')].map(o => o.className);
  const noteTitle = (document.querySelector('h1,h2') || {}).textContent || '';
  return {vw: innerWidth, title: document.title, more: bar.getAttribute('data-obb-more'),
    row: {scrollWidth: row.scrollWidth, clientWidth: row.clientWidth, scrollLeft: Math.round(row.scrollLeft)},
    fade: {before: cs(bar, 'opacity', '::before'), after: cs(bar, 'opacity', '::after')},
    navL: cs(navL, 'display'), navR: cs(navR, 'display'),
    pills, gems, modal,
    note: {title: noteTitle.slice(0, 80), sn2696: document.body.innerText.includes('SN-2696'),
           hook: document.body.innerText.includes('The Infinite Smart Feeds'),
           nutshell: document.body.innerText.includes('IN A NUTSHELL')},
    feedCards: document.querySelectorAll('[class*=note-card i], [data-note-id]').length};
}"""

SETTLE = """() => new Promise(res => {
  let last = -1, stable = 0;
  const row = document.querySelector('.obb-row');
  const iv = setInterval(() => {
    const sl = Math.round(row.scrollLeft);
    if (sl === last) { stable++; if (stable >= 3) { clearInterval(iv); res(sl); } }
    else { stable = 0; last = sl; }
  }, 200);
  setTimeout(() => { clearInterval(iv); res(Math.round(row.scrollLeft)); }, 6000);
})"""

results = {}
with sync_playwright() as pw:
    b = pw.firefox.launch()
    for width in (390, 360, 1440):
        h = 844 if width < 1000 else 900
        for flow, url in (("cold", BASE + "#/smart-notes/sn2696"), ("direct", BASE)):
            ctx = b.new_context(viewport={"width": width, "height": h},
                                has_touch=True, is_mobile=width < 1000)
            pg = ctx.new_page()
            errs = []
            pg.on("pageerror", lambda e: errs.append(f"pageerror:{str(e)[:100]}"))
            pg.on("console", lambda m: errs.append(f"console:{m.type}:{m.text[:100]}") if m.type == "error" else None)
            pg.goto(url, wait_until="domcontentloaded")
            pg.wait_for_timeout(4000)
            modal_settled = pg.evaluate("() => { const o=document.querySelector('.naya-install-overlay'); return o ? o.className : 'none'; }")
            pg.wait_for_timeout(2500)
            modal_6s = pg.evaluate("() => { const o=document.querySelector('.naya-install-overlay'); return o ? o.className : 'none'; }")
            # visitor dismisses the Install modal via its own "Not now" button (probe action)
            pg.evaluate("() => { const l=document.querySelector('.naya-install-later'); if(l) l.click(); }")
            pg.wait_for_timeout(800)
            m0 = pg.evaluate(MEASURE)
            tag = f"staged-w-{width}-{flow}"
            pg.screenshot(path=f"{OUT}{tag}-w-rest.png")
            clicked = False
            if m0["navR"] != "none":
                pg.click(".obb-nav-r")
                pg.evaluate(SETTLE)
                pg.wait_for_timeout(500)
                clicked = True
            m1 = pg.evaluate(MEASURE)
            pg.screenshot(path=f"{OUT}{tag}-w-scrolled.png")
            if clicked and m1["navL"] != "none":
                pg.click(".obb-nav-l")
                pg.evaluate(SETTLE)
                pg.wait_for_timeout(500)
            m2 = pg.evaluate(MEASURE)
            results[f"{width}-{flow}"] = {"rest": m0, "after_right": m1, "after_left": m2,
                                          "errors": errs, "modal_settled_4s": modal_settled,
                                          "modal_6s": modal_6s}
            print(f"== {width} {flow}: title={m0['title']!r} more={m0['more']!r} navR={m0['navR']} navL={m0['navL']} fade={m0['fade']} SL={m0['row']['scrollLeft']}")
            print(f"   pills rest: {[(p['label'], p['left'], p['right'], p['visible']) for p in m0['pills']]}")
            if clicked:
                print(f"   after R: SL={m1['row']['scrollLeft']} more={m1['more']!r} visible={[p['label'] for p in m1['pills'] if p['visible']]}")
                print(f"   after L: SL={m2['row']['scrollLeft']} more={m2['more']!r}")
            print(f"   gems: {m0['gems']} note: {m0['note']} feedCards: {m0['feedCards']} errors: {errs}")
            print(f"   modal 4s: {modal_settled} | 6s: {modal_6s}")
            ctx.close()
    b.close()
json.dump(results, open(OUT + "probe-staged-worker.json", "w"), indent=1)
print("STAGED-WORKER PROBE DONE")
