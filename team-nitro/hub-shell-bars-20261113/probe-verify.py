#!/usr/bin/env python3
"""Hub Shell Bars — FULL VERIFICATION on staging (Playwright Firefox).
Fresh profile per width. 390 first, then 1440, then 360.
Start at the staged note link /s/sn2696; confirm the note landing first.
Per width: radii (computed, icon element itself), sizes, labels, gem hashes,
counts (preset localStorage mail=3, spaces=2 via init script), stack geometry,
cover rect-by-rect at max scroll (fixed-ancestor-excluded), overflow, errors.
Clicks: trio 3/3 at every width + upper row 9/9 at 1440 (fresh load each,
destination URL + title). Ask-room: one open attempt at 390.
Screenshots + proof JSON -> work dir.
"""
import hashlib
import json
from playwright.sync_api import sync_playwright

WD = "/home/hatch/workspace/team-nitro/hub-shell-bars-20261113"
STAGING = "https://naya-public-blog-staging.nayapower.workers.dev"
NOTE_URL = STAGING + "/s/sn2696"

MEASURE_JS = """() => {
  const q = s => document.querySelector(s);
  const qa = s => [...document.querySelectorAll(s)];
  const r = el => { if (!el) return null; const b = el.getBoundingClientRect();
    return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width),
            h: Math.round(b.height), top: Math.round(b.top), bottom: Math.round(b.bottom)}; };
  const cs = el => el ? getComputedStyle(el) : null;
  const txt = document.body.innerText || '';
  const out = {};
  out.url = location.href; out.title = document.title;
  out.notHere = txt.includes("That note isn't here");
  out.hook = txt.includes("Not one feed like Facebook");
  out.noteTitle = txt.includes("SN-2696");
  out.boards = document.querySelectorAll('.intel-board').length;
  const ov = document.querySelector('.naya-install-overlay');
  out.overlayShown = !!(ov && ov.classList.contains('show'));
  out.overlayVisible = !!(ov && cs(ov).display !== 'none' && ov.getBoundingClientRect().height > 50);
  const main = q('.main');
  out.mainPaddingBottom = main ? cs(main).paddingBottom : null;
  out.notifH = getComputedStyle(document.documentElement).getPropertyValue('--notif-h').trim();
  const obb = q('#obb-bar');
  out.obbBelow = obb ? (obb.style.getPropertyValue('--obb-below') || '') : null;
  out.obbBar = r(obb);
  out.obbPills = qa('#obb-bar .obb-pill').map(a => {
    const j = a.querySelector('.obb-jewel'); const jc = j ? cs(j) : null;
    const l = a.querySelector('.obb-lbl');
    return {label: l ? l.innerText : null, href: a.getAttribute('href'),
      jewelW: j ? Math.round(j.getBoundingClientRect().width) : null,
      jewelH: j ? Math.round(j.getBoundingClientRect().height) : null,
      jewelRadius: jc ? jc.borderRadius : null,
      labelVisible: l ? (cs(l).display !== 'none' && cs(l).visibility !== 'hidden' && l.getBoundingClientRect().height > 0) : false}; });
  out.activityPills = qa('#obb-bar [data-obb="activity"]').length;
  const nb = q('#naya-notif-bar');
  out.notifBars = qa('#naya-notif-bar').length;
  out.notifBar = r(nb);
  out.notifSegs = qa('#naya-notif-bar .notif-seg').map(s => {
    const t = s.querySelector('.notif-tile'); const tc = t ? cs(t) : null;
    const svg = t ? t.querySelector('svg') : null;
    const bub = s.querySelector('.notif-count');
    const lbl = s.querySelector('.notif-lbl');
    return {key: s.getAttribute('data-notif'), gem: s.getAttribute('data-gem'),
      label: lbl ? lbl.innerText : null, tileW: t ? Math.round(t.getBoundingClientRect().width) : null,
      tileH: t ? Math.round(t.getBoundingClientRect().height) : null,
      tileRadius: tc ? tc.borderRadius : null,
      svgHash: svg ? 'sha:' + Array.from(new Uint8Array(0)).length : null,
      svgOuter: svg ? svg.outerHTML : null,
      count: bub ? bub.innerText : null,
      countShown: bub ? cs(bub).display : null}; });
  const eco = q('.eco-bottombar');
  out.ecoPresent = !!eco;
  out.ecoBtns = qa('.eco-bottombar .eco-bb-btn').length;
  out.overflow0 = document.documentElement.scrollWidth - window.innerWidth;
  out.viewH = window.innerHeight; out.docH = document.documentElement.scrollHeight;
  return out;
}"""

COVER_JS = """() => {
  const fixedAncestor = el => { let n = el; while (n) { const p = getComputedStyle(n).position;
    if (p === 'fixed') return true; n = n.parentElement; } return false; };
  const obb = document.querySelector('#obb-bar');
  const obbTop = obb ? obb.getBoundingClientRect().top : null;
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let lowestMain = null, node;
  while (node = walker.nextNode()) {
    if (!node.nodeValue || !node.nodeValue.trim()) continue;
    const el = node.parentElement; if (!el || fixedAncestor(el)) continue;
    if (!el.closest('.main')) continue;
    const b = el.getBoundingClientRect();
    if (b.height <= 0) continue;
    const css = getComputedStyle(el);
    if (css.visibility === 'hidden' || css.display === 'none') continue;
    if (b.bottom <= 0 || b.top >= window.innerHeight) continue;
    if (!lowestMain || b.bottom > lowestMain.bottom)
      lowestMain = {text: node.nodeValue.trim().slice(0, 60), bottom: Math.round(b.bottom), top: Math.round(b.top)};
  }
  const nb = document.querySelector('#naya-notif-bar');
  return {lowestMain, obbTop: Math.round(obbTop),
          notifTop: nb ? Math.round(nb.getBoundingClientRect().top) : null,
          obbBottom: obb ? Math.round(obb.getBoundingClientRect().bottom) : null,
          viewH: window.innerHeight, scrollY: Math.round(window.scrollY),
          maxScroll: Math.round(document.documentElement.scrollHeight - window.innerHeight)};
}"""

SNAP_JS = """() => {
  const row = document.querySelector('.obb-row');
  if (!row) return {row: null};
  row.scrollTo({left: 120, behavior: 'instant'});
  return {rowLeft: Math.round(row.getBoundingClientRect().left),
          scrollLeft: row.scrollLeft, scrollW: row.scrollWidth, clientW: row.clientWidth};
}"""

SNAP_AFTER_JS = """() => {
  const row = document.querySelector('.obb-row');
  const pills = [...document.querySelectorAll('#obb-bar .obb-pill')];
  const rl = row.getBoundingClientRect().left;
  const vis = pills.map(p => { const b = p.getBoundingClientRect();
    return {label: (p.querySelector('.obb-lbl')||{}).innerText, left: Math.round(b.left), right: Math.round(b.right)}; })
    .filter(p => p.right > rl && p.left < rl + row.clientWidth);
  return {scrollLeft: row.scrollLeft, firstVisibleLeft: vis.length ? vis[0].left : null,
          rowLeft: Math.round(rl), visible: vis.slice(0, 3)};
}"""


def click_proof(pw, width, height, selector, label):
    """Fresh load, click one bar element, record destination URL + title."""
    browser = pw.firefox.launch(headless=True)
    ctx = browser.new_context(viewport={"width": width, "height": height})
    pg = ctx.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(NOTE_URL, timeout=60000)
    pg.wait_for_timeout(3500)
    el = pg.query_selector(selector)
    if not el:
        browser.close()
        return {"label": label, "selector": selector, "found": False}
    try:
        el.scroll_into_view_if_needed(timeout=5000)
        pg.wait_for_timeout(400)
        el.click(timeout=8000)
    except Exception as e:
        browser.close()
        return {"label": label, "selector": selector, "found": True, "click_error": str(e)[:200]}
    pg.wait_for_timeout(4000)
    out = {"label": label, "selector": selector, "found": True,
           "dest_url": pg.url, "dest_title": pg.title(), "page_errors": errs}
    print(f"  click {label}: -> {out['dest_url'][:90]} | {out['dest_title'][:60]!r}")
    browser.close()
    return out


def run_width(pw, width, height, do_clicks):
    print(f"== WIDTH {width} ==")
    browser = pw.firefox.launch(headless=True)
    ctx = browser.new_context(viewport={"width": width, "height": height})
    # preset counts BEFORE page scripts run
    ctx.add_init_script("try { localStorage.setItem('nayanet.notif.mail', '3'); "
                        "localStorage.setItem('nayanet.notif.spaces', '2'); } catch (e) {}")
    pg = ctx.new_page()
    console_errors, page_errors = [], []
    pg.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: page_errors.append(str(e)))
    pg.goto(NOTE_URL, timeout=60000)
    pg.wait_for_timeout(4000)
    d = pg.evaluate(MEASURE_JS)
    # gem hashes in python (outerHTML -> sha256)
    for s in d["notifSegs"]:
        o = s.pop("svgOuter", None)
        s["svgSha"] = hashlib.sha256((o or "").encode()).hexdigest()[:12] if o else None
        s.pop("svgHash", None)
    d["console_errors"] = console_errors
    d["page_errors"] = page_errors
    print(f"  note: title={d['title']!r} notHere={d['notHere']} hook={d['hook']} boards={d['boards']} overlay={d['overlayShown']}/{d['overlayVisible']}")
    print(f"  mainPad={d['mainPaddingBottom']} notifH={d['notifH']} obbBelow={d['obbBelow']!r} ecoPresent={d['ecoPresent']}")
    print(f"  obbBar={d['obbBar']} pills={len(d['obbPills'])} activityPills={d['activityPills']}")
    print(f"  jewels={[(p['label'], p['jewelW'], p['jewelRadius'], p['labelVisible']) for p in d['obbPills']]}")
    print(f"  notifBars={d['notifBars']} notifBar={d['notifBar']}")
    print(f"  segs={[(s['key'], s['label'], s['tileW'], s['tileRadius'], s['count'], s['countShown'], s['svgSha']) for s in d['notifSegs']]}")
    print(f"  overflow0={d['overflow0']} console={console_errors} page={page_errors}")
    pg.screenshot(path=f"{WD}/verify-note-{width}.png")
    pg.screenshot(path=f"{WD}/verify-bars-{width}.png",
                  clip={"x": 0, "y": max(0, d["viewH"] - 300), "width": width, "height": min(300, d["viewH"])})
    # snap: scroll the upper row, let it settle, check leftmost circle whole
    snap0 = pg.evaluate(SNAP_JS)
    pg.wait_for_timeout(700)
    snap1 = pg.evaluate(SNAP_AFTER_JS)
    d["snap"] = {"before": snap0, "after": snap1}
    print(f"  snap: {snap1}")
    # max scroll cover
    pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    pg.wait_for_timeout(1200)
    cover = pg.evaluate(COVER_JS)
    d["cover_max_scroll"] = cover
    print(f"  cover: {cover}")
    d["overflow_scrolled"] = pg.evaluate("document.documentElement.scrollWidth - window.innerWidth")
    pg.screenshot(path=f"{WD}/verify-scrolled-{width}.png")
    # ask-room attempt (390 only)
    if width == 390:
        pg.evaluate("window.scrollTo(0,0)")
        pg.wait_for_timeout(500)
        ask = pg.evaluate("""() => {
          const cands = [...document.querySelectorAll('button, a')].filter(e => {
            const t = (e.innerText || '').toLowerCase();
            return t.includes('ask naya') || t === 'ask';
          }).filter(e => { const b = e.getBoundingClientRect();
            return b.height > 0 && getComputedStyle(e).visibility !== 'hidden'; });
          return cands.map(e => ({tag: e.tagName, text: (e.innerText||'').slice(0,40),
            cls: (e.className||'').toString().slice(0,60)})); }""")
        d["ask_candidates"] = ask
        print(f"  ask candidates: {ask}")
        if ask:
            try:
                pg.evaluate("""() => { const c = [...document.querySelectorAll('button, a')].find(e =>
                  (e.innerText || '').toLowerCase().includes('ask naya'));
                  if (c) c.click(); }""")
                pg.wait_for_timeout(2500)
                d["ask_room"] = pg.evaluate("""() => { const room = document.querySelector('.naya-ask-room');
                  if (!room) return {present: false};
                  const nb = document.querySelector('#naya-notif-bar');
                  const obb = document.querySelector('#obb-bar');
                  return {present: true, roomRect: (() => { const b = room.getBoundingClientRect();
                    return {top: Math.round(b.top), h: Math.round(b.height)}; })(),
                    notifBottom: nb ? Math.round(nb.getBoundingClientRect().bottom) : null,
                    notifTop: nb ? Math.round(nb.getBoundingClientRect().top) : null,
                    obbTop: obb ? Math.round(obb.getBoundingClientRect().top) : null,
                    viewH: window.innerHeight}; }""")
                print(f"  ask room: {d['ask_room']}")
                pg.screenshot(path=f"{WD}/verify-askroom-{width}.png")
            except Exception as e:
                d["ask_room_error"] = str(e)[:200]
    browser.close()
    # clicks (fresh load each)
    if do_clicks:
        d["trio_clicks"] = [
            click_proof(pw, width, height, "#segPersonal", "Personal"),
            click_proof(pw, width, height, "#segBusiness", "Business"),
            click_proof(pw, width, height, "#segThing", "Thing"),
        ]
    return d


results = {}
with sync_playwright() as pw:
    results["390"] = run_width(pw, 390, 844, do_clicks=True)
    results["1440"] = run_width(pw, 1440, 900, do_clicks=True)
    results["360"] = run_width(pw, 360, 800, do_clicks=True)
    # upper-row 9/9 at 1440 (fresh load each)
    upper = []
    for i, label in enumerate(["Mail", "Dashboard", "Business", "Space", "Growth",
                               "Connections", "Smart Lists", "Reports", "10 apps"]):
        sel = f"#obb-bar .obb-pill >> nth={i}"
        upper.append(click_proof(pw, 1440, 900, sel, label))
    results["upper_clicks_1440"] = upper
json.dump(results, open(f"{WD}/verify-results.json", "w"), indent=1)
print("WROTE verify-results.json")
