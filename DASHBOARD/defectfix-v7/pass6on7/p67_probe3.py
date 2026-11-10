"""PASS-6-ON-7 probe 3 — last gaps from probe 2.
1. Hover time-series on the merged file (probe 2's C read rest shadows —
   determine whether :hover engages at all, with :hover matching + transform).
2. Scrolled-120px note + toggle check at 390/1440 in % mode (is the note
   fully visible + clickable once scrolled, as in pass-6?).
Usage: python3 p67_probe3.py -> p67c.json + shots3/
"""
import json, threading, http.server, functools, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'p67c.json')
SHOTS = os.path.join(HERE, 'shots3')
os.makedirs(SHOTS, exist_ok=True)
PORT = 18763

os.chdir(HERE)
Handler = functools.partial(http.server.SimpleHTTPRequestHandler)
httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), Handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()

SETUP = """() => {
  const now = Date.now();
  const hrs = (n) => { const a=[]; for (let i=0;i<n;i++) a.push(new Date(now - (i+1)*36e5).toISOString()); return a; };
  window._osSpine = { posts: 4, notes: 8, msgs: 5, invs: 2, clicks: 1100, joins: 0, score: 1120, saves: 1, invitesSent: 2, inviteJoins: 0, sales: 0, likes: 0, comments: 0, shares: 0, extShares: 0, memberBonus: 0, people: 4, updatedAt: now, deltas: {hour: 12, day: 120, week: 400, month: 900}, funnel: {recorded: 3, opened: 2, joined: 1, dryRun: false}, mix: {posts: 4, notes: 8, messages: 5, invites: 2, clicks: 1100, joins: 0}, mixTotal: 1119 };
  window._dashD = { noteTimes: hrs(8), postTimes: hrs(4), msgTimes: hrs(5), invTimes: hrs(2), saveTimes: hrs(1) };
  window._dashLinkT = {c: 1100, j: 0};
  window._dashClickDayMap = {};
  window._dashDataLanded = true;
  const rows = [{id:'1', name:'joinus', url:'https://nayanet.app/welcome', clicks:1100, joins:0},{id:'2', name:'alpha', url:'https://example.com/b', clicks:120, joins:3},{id:'3', name:'beta', url:'https://example.com/c', clicks:45, joins:0},{id:'4', name:'gamma', url:'https://example.com/d', clicks:20, joins:1},{id:'5', name:'delta', url:'https://example.com/e', clicks:8, joins:0}];
  const stats = []; rows.forEach(r => stats.push({link_id:r.id, clicks:r.clicks, joins:r.joins, day:'2026-11-09'}));
  window._osRenderLinks(rows, stats, null, null);
  if (typeof window.renderBoards === 'function') window.renderBoards();
  try { if (typeof window.loadPointsBoard === 'function') window.loadPointsBoard(); } catch(e){}
  return 'setup-done';
}"""

HOVER_T = """(boardIdx) => {
  const b = document.querySelectorAll('.os-world-board')[boardIdx];
  if (!b) return {error: 'no board ' + boardIdx};
  const btn = b.querySelector('.os-wb-btn');
  if (!btn) return {error: 'no btn'};
  const cs = getComputedStyle(btn);
  const hov = document.querySelector('.os-world-board .os-wb-btn:hover');
  return {board: (b.querySelector('.os-wb-id b')||{}).textContent,
    hoverMatches: hov === btn, border: cs.borderColor, shadow: cs.boxShadow,
    transform: cs.transform, filter: cs.filter, bg: cs.backgroundImage.slice(0,90)};
}"""

SCROLL_CHECK = r"""() => {
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect();
    return {x:+b.x.toFixed(1), y:+b.y.toFixed(1), w:+b.width.toFixed(1), h:+b.height.toFixed(1), top:+b.top.toFixed(1), bottom:+b.bottom.toFixed(1)}; };
  const bar = document.getElementById('os-bottom3');
  const br = bar ? bar.getBoundingClientRect() : null;
  const note = document.getElementById('os-pts-note');
  const tg = document.getElementById('os-pts-toggle');
  const nr = note ? r(note) : null, tr = tg ? r(tg) : null;
  const ov = (a) => { if (!a || !br) return 0;
    const iw = Math.max(0, Math.min(a.right ?? a.x + a.w, br.right) - Math.max(a.left ?? a.x, br.left));
    const ih = Math.max(0, Math.min(a.bottom, br.bottom) - Math.max(a.top, br.top));
    return +(iw*ih).toFixed(1); };
  const hitAt = (rect) => { if (!rect) return null;
    const el = document.elementFromPoint(rect.x + rect.w/2, rect.y + rect.h/2);
    return el ? (el.id || el.className.toString().slice(0,40) || el.tagName) : null; };
  return {scrollY: Math.round(window.scrollY), barTop: br ? +br.top.toFixed(1) : null,
    note: nr ? {rect: nr, visibility: getComputedStyle(note).visibility, text: note.textContent.trim().slice(0,60),
      barOverlap: ov(nr), hitCenter: hitAt(nr)} : null,
    toggle: tr ? {rect: tr, barOverlap: ov(tr), hitCenter: hitAt(tr)} : null};
}"""

def js(pg, expr, arg=None):
    try: return pg.evaluate(expr, arg) if arg is not None else pg.evaluate(expr)
    except Exception as e: return {"error": str(e)[:400]}

results = {}
def save(): json.dump(results, open(OUT, 'w'), indent=1)

from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.firefox.launch()
    for width in (390, 1440):
        page = browser.new_page(viewport={'width': width, 'height': 844})
        errs = []
        page.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        page.on('pageerror', lambda e: errs.append(str(e)))
        page.goto(f'http://127.0.0.1:{PORT}/dashboard-pass6on7.html', wait_until='load', timeout=60000)
        page.wait_for_timeout(2500)
        js(page, SETUP); page.wait_for_timeout(1500)
        # hover time-series, boards 0 and 2
        series = {}
        for i in (0, 2):
            page.evaluate(f"() => {{ const b = document.querySelectorAll('.os-world-board')[{i}]; if (b) b.scrollIntoView({{block:'center'}}); }}")
            page.wait_for_timeout(500)
            box = page.locator('.os-world-board >> nth=%d >> .os-wb-btn' % i).bounding_box()
            samples = []
            if box:
                page.mouse.move(box['x'] + box['width']/2, box['y'] + box['height']/2, steps=5)
                for wait in (500, 500, 600, 1000):
                    page.wait_for_timeout(wait)
                    samples.append(js(page, HOVER_T, i))
            else:
                samples.append({'error': 'no box'})
            series[f'board{i}'] = samples
        # scrolled-120 note + toggle in % mode
        page.evaluate("() => { const b = document.querySelector('.os-pts-btn[data-mode=\"pct\"]'); if (b) b.click(); }")
        page.wait_for_timeout(3000)
        page.evaluate("window.scrollTo(0,120)")
        page.wait_for_timeout(600)
        sc120 = js(page, SCROLL_CHECK)
        page.screenshot(path=os.path.join(SHOTS, f'p67c-scrolled120-pct-{width}.png'))
        # toggle clickable after scroll? click MONEY from scrolled position
        page.evaluate("() => { const b = document.querySelector('.os-pts-btn[data-mode=\"money\"]'); if (b) b.click(); }")
        page.wait_for_timeout(3000)
        money = js(page, "() => { const t = document.querySelector('#tn-tacho-mount .tn-tacho'); const n = document.querySelector('#tn-tacho-mount .tn-tacho-num'); return {state: t ? t.getAttribute('data-state') : null, numeral: n ? n.textContent.trim() : null}; }")
        results[f'merged-{width}'] = {'hoverSeries': series, 'scrolled120pct': sc120,
            'moneyAfterScrollClick': money, 'consoleErrors': errs}
        save(); print('done', width, flush=True); page.close()
    browser.close()
save()
print('wrote', OUT)
