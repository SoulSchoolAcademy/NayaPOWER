"""Probe 4: bar + note geometry across scroll positions (% mode, merged)."""
import json, threading, http.server, functools, os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'p67d.json')
SHOTS = os.path.join(HERE, 'shots3')
PORT = 18764
os.chdir(HERE)
Handler = functools.partial(http.server.SimpleHTTPRequestHandler)
httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), Handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
SETUP = """() => {
  const now = Date.now();
  const hrs = (n) => { const a=[]; for (let i=0;i<n;i++) a.push(new Date(now - (i+1)*36e5).toISOString()); return a; };
  window._osSpine = { posts: 4, notes: 8, msgs: 5, invs: 2, clicks: 1100, joins: 0, score: 1120, saves: 1, invitesSent: 2, inviteJoins: 0, sales: 0, likes: 0, comments: 0, shares: 0, extShares: 0, memberBonus: 0, people: 4, updatedAt: now, deltas: {hour: 12, day: 120, week: 400, month: 900}, funnel: {recorded: 3, opened: 2, joined: 1, dryRun: false}, mix: {posts: 4, notes: 8, messages: 5, invites: 2, clicks: 1100, joins: 0}, mixTotal: 1119 };
  window._dashD = { noteTimes: hrs(8), postTimes: hrs(4), msgTimes: hrs(5), invTimes: hrs(2), saveTimes: hrs(1) };
  window._dashLinkT = {c: 1100, j: 0}; window._dashClickDayMap = {}; window._dashDataLanded = true;
  const rows = [{id:'1', name:'joinus', url:'https://nayanet.app/welcome', clicks:1100, joins:0},{id:'2', name:'alpha', url:'https://example.com/b', clicks:120, joins:3},{id:'3', name:'beta', url:'https://example.com/c', clicks:45, joins:0},{id:'4', name:'gamma', url:'https://example.com/d', clicks:20, joins:1},{id:'5', name:'delta', url:'https://example.com/e', clicks:8, joins:0}];
  const stats = []; rows.forEach(r => stats.push({link_id:r.id, clicks:r.clicks, joins:r.joins, day:'2026-11-09'}));
  window._osRenderLinks(rows, stats, null, null);
  if (typeof window.renderBoards === 'function') window.renderBoards();
  return 'setup-done';
}"""
GEOM = r"""() => {
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect();
    return {x:+b.x.toFixed(1), y:+b.y.toFixed(1), w:+b.width.toFixed(1), h:+b.height.toFixed(1), top:+b.top.toFixed(1), bottom:+b.bottom.toFixed(1)}; };
  const bar = document.getElementById('os-bottom3');
  const note = document.getElementById('os-pts-note');
  const tg = document.getElementById('os-pts-toggle');
  const br = bar ? r(bar) : null, nr = note ? r(note) : null, tr = tg ? r(tg) : null;
  const ov = (a) => { if (!a || !br) return 0;
    const iw = Math.max(0, Math.min(a.x + a.w, br.x + br.w) - Math.max(a.x, br.x));
    const ih = Math.max(0, Math.min(a.bottom, br.bottom) - Math.max(a.top, br.top));
    return +(iw*ih).toFixed(1); };
  const hitAt = (rect) => { if (!rect) return null;
    const el = document.elementFromPoint(rect.x + rect.w/2, rect.y + rect.h/2);
    return el ? (el.id || (el.className.baseVal !== undefined ? el.className.baseVal : el.className || '').toString().slice(0,40) || el.tagName) : null; };
  return {scrollY: Math.round(window.scrollY), vh: window.innerHeight,
    bar: br ? {rect: br, position: getComputedStyle(bar).position, display: getComputedStyle(bar).display} : null,
    note: nr ? {rect: nr, visibility: getComputedStyle(note).visibility, text: note.textContent.trim().slice(0,60), barOverlap: ov(nr), hitCenter: hitAt(nr)} : null,
    toggle: tr ? {rect: tr, barOverlap: ov(tr), hitCenter: hitAt(tr)} : null};
}"""
def js(pg, expr):
    try: return pg.evaluate(expr)
    except Exception as e: return {"error": str(e)[:400]}
results = {}
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.firefox.launch()
    for width in (390, 1440):
        page = browser.new_page(viewport={'width': width, 'height': 844})
        page.goto(f'http://127.0.0.1:{PORT}/dashboard-pass6on7.html', wait_until='load', timeout=60000)
        page.wait_for_timeout(2500)
        js(page, SETUP); page.wait_for_timeout(1500)
        page.evaluate("() => { const b = document.querySelector('.os-pts-btn[data-mode=\"pct\"]'); if (b) b.click(); }")
        page.wait_for_timeout(3000)
        rows = {}
        for sy in (0, 60, 120, 300):
            page.evaluate(f"window.scrollTo(0,{sy})"); page.wait_for_timeout(700)
            rows[f'scroll{sy}'] = js(page, GEOM)
        page.evaluate("() => { const n = document.getElementById('os-pts-note'); if (n) n.scrollIntoView({block:'center'}); }")
        page.wait_for_timeout(700)
        rows['noteIntoView'] = js(page, GEOM)
        page.screenshot(path=os.path.join(SHOTS, f'p67d-note-inview-{width}.png'))
        results[f'merged-{width}'] = rows
        print('done', width, flush=True)
        page.close()
    browser.close()
json.dump(results, open(OUT, 'w'), indent=1)
print('wrote', OUT)
