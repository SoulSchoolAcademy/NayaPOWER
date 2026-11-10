"""Probe 6: clean board-button tap retry (fresh page, no drill open).
Personal board button -> nayanet.app/personal, real mouse click."""
import json, threading, http.server, functools, os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'p67f.json')
PORT = 18766
os.chdir(HERE)
Handler = functools.partial(http.server.SimpleHTTPRequestHandler)
httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), Handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
SETUP = """() => {
  const now = Date.now();
  window._osSpine = { posts: 4, notes: 8, msgs: 5, invs: 2, clicks: 1100, joins: 0, score: 1120, saves: 1, invitesSent: 2, inviteJoins: 0, sales: 0, likes: 0, comments: 0, shares: 0, extShares: 0, memberBonus: 0, people: 4, updatedAt: now, deltas: {hour: 12, day: 120, week: 400, month: 900}, funnel: {recorded: 3, opened: 2, joined: 1, dryRun: false}, mix: {posts: 4, notes: 8, messages: 5, invites: 2, clicks: 1100, joins: 0}, mixTotal: 1119 };
  window._dashLinkT = {c: 1100, j: 0}; window._dashClickDayMap = {}; window._dashDataLanded = true;
  const rows = [{id:'1', name:'joinus', url:'https://nayanet.app/welcome', clicks:1100, joins:0},{id:'2', name:'alpha', url:'https://example.com/b', clicks:120, joins:3},{id:'3', name:'beta', url:'https://example.com/c', clicks:45, joins:0},{id:'4', name:'gamma', url:'https://example.com/d', clicks:20, joins:1},{id:'5', name:'delta', url:'https://example.com/e', clicks:8, joins:0}];
  const stats = []; rows.forEach(r => stats.push({link_id:r.id, clicks:r.clicks, joins:r.joins, day:'2026-11-09'}));
  window._osRenderLinks(rows, stats, null, null);
  if (typeof window.renderBoards === 'function') window.renderBoards();
  return 'setup-done';
}"""
results = {}
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.firefox.launch()
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto(f'http://127.0.0.1:{PORT}/dashboard-pass6on7.html', wait_until='load', timeout=60000)
    page.wait_for_timeout(2500)
    page.evaluate(SETUP); page.wait_for_timeout(1500)
    page.evaluate("() => { const b = document.querySelectorAll('.os-world-board')[1]; if (b) b.scrollIntoView({block:'center'}); }")
    page.wait_for_timeout(800)
    vis = page.evaluate("() => { const b = document.querySelectorAll('.os-world-board')[1].querySelector('.os-wb-btn'); const r = b.getBoundingClientRect(); const cs = getComputedStyle(b); return {rect: {x: r.x, y: r.y, w: r.width, h: r.height}, visible: r.width > 0 && r.height > 0, display: cs.display, visibility: cs.visibility, href: b.getAttribute('href')}; }")
    results['buttonState'] = vis
    try:
        box = page.locator('.os-world-board >> nth=1 >> .os-wb-btn').bounding_box()
        results['box'] = box
        if box:
            with page.expect_navigation(url='https://nayanet.app/personal', timeout=20000):
                page.mouse.click(box['x'] + box['width']/2, box['y'] + box['height']/2)
        results['boardTap'] = {'landed': page.url, 'title': page.title()}
    except Exception as e:
        results['boardTap'] = {'error': str(e)[:400], 'urlNow': page.url}
    print(json.dumps(results, indent=1), flush=True)
    page.close(); browser.close()
json.dump(results, open(OUT, 'w'), indent=1)
print('wrote', OUT)
