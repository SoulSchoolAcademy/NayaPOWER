"""Probe 5: D1 drill gold buttons (expand Smart Link drill, sample a
'Show on gauge' button) + one end-to-end board-button tap in the merged file
(Personal -> nayanet.app/personal)."""
import json, threading, http.server, functools, os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'p67e.json')
PORT = 18765
os.chdir(HERE)
Handler = functools.partial(http.server.SimpleHTTPRequestHandler)
httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), Handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
SETUP = """() => {
  const now = Date.now();
  window._osSpine = { posts: 4, notes: 8, msgs: 5, invs: 2, clicks: 1100, joins: 0, score: 1120, saves: 1, invitesSent: 2, inviteJoins: 0, sales: 0, likes: 0, comments: 0, shares: 0, extShares: 0, memberBonus: 0, people: 4, updatedAt: now, deltas: {hour: 12, day: 120, week: 400, month: 900}, funnel: {recorded: 3, opened: 2, joined: 1, dryRun: false}, mix: {posts: 4, notes: 8, messages: 5, invites: 2, clicks: 1100, joins: 0}, mixTotal: 1119 };
  window._dashD = { noteTimes: [], postTimes: [], msgTimes: [], invTimes: [], saveTimes: [] };
  window._dashLinkT = {c: 1100, j: 0}; window._dashClickDayMap = {}; window._dashDataLanded = true;
  const rows = [{id:'1', name:'joinus', url:'https://nayanet.app/welcome', clicks:1100, joins:0},{id:'2', name:'alpha', url:'https://example.com/b', clicks:120, joins:3},{id:'3', name:'beta', url:'https://example.com/c', clicks:45, joins:0},{id:'4', name:'gamma', url:'https://example.com/d', clicks:20, joins:1},{id:'5', name:'delta', url:'https://example.com/e', clicks:8, joins:0}];
  const stats = []; rows.forEach(r => stats.push({link_id:r.id, clicks:r.clicks, joins:r.joins, day:'2026-11-09'}));
  window._osRenderLinks(rows, stats, null, null);
  if (typeof window.renderBoards === 'function') window.renderBoards();
  return 'setup-done';
}"""
DRILL = r"""() => {
  const btns = [...document.querySelectorAll('.os-link-row button')].filter(b => /Show on gauge/i.test(b.textContent || ''));
  return {showOnGaugeCount: btns.length,
    sample: btns.slice(0, 4).map(b => { const cs = getComputedStyle(b);
      return {text: b.textContent.trim().slice(0, 30), color: cs.color, borderColor: cs.borderColor, boxShadow: cs.boxShadow.slice(0, 140)}; }),
    linkRows: document.querySelectorAll('.os-link-row').length};
}"""
def js(pg, expr):
    try: return pg.evaluate(expr)
    except Exception as e: return {"error": str(e)[:400]}
results = {}
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.firefox.launch()
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto(f'http://127.0.0.1:{PORT}/dashboard-pass6on7.html', wait_until='load', timeout=60000)
    page.wait_for_timeout(2500)
    js(page, SETUP); page.wait_for_timeout(1500)
    # expand the Smart Link drill: click "See every link" (whatever opens it)
    clicked = js(page, """() => {
      const els = [...document.querySelectorAll('button, a')];
      const t = els.find(e => /see every link/i.test(e.textContent || ''));
      if (t) { t.click(); return 'clicked: ' + t.textContent.trim().slice(0, 40); }
      return 'not-found: ' + els.map(e => (e.textContent || '').trim().slice(0, 25)).join(' | ').slice(0, 300);
    }""")
    page.wait_for_timeout(1500)
    results['drillOpen'] = clicked
    results['drill'] = js(page, DRILL)
    page.screenshot(path=os.path.join(HERE, 'shots3', 'p67e-drill-390.png'))
    # end-to-end board-button tap: Personal board -> nayanet.app/personal
    page.evaluate("() => { const b = document.querySelectorAll('.os-world-board')[1]; if (b) b.scrollIntoView({block:'center'}); }")
    page.wait_for_timeout(600)
    try:
        with page.expect_navigation(url='https://nayanet.app/personal', timeout=20000) as nav:
            page.click('.os-world-board >> nth=1 >> .os-wb-btn', timeout=5000)
        results['boardTap'] = {'landed': page.url, 'title': page.title()}
    except Exception as e:
        results['boardTap'] = {'error': str(e)[:300], 'urlNow': page.url}
    print(json.dumps(results, indent=1), flush=True)
    page.close(); browser.close()
json.dump(results, open(OUT, 'w'), indent=1)
print('wrote', OUT)
