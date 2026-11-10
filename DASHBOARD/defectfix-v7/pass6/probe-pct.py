"""PASS-6 BUILDER after-probe: measure dashboard-pass6.html, same method as baseline.
Scenarios: default link holder + page holder (localStorage, reproduces Shawn's
Quiet state). Synthetic spine + synthetic LEDGER so orbs show real numbers
(1.1K / 0 / 280 / 50 / 100 / 0 / 0 / 0 / 5 — Shawn's live values).
Per width/mode/scenario: orb font+rect+text, note rect/visibility/overlap vs dial,
gauge-center numeral + data-state + caption, Quiet scan, ambassador sample,
overflow, console errors. Screenshots hero + feat panel.
Usage: python3 probe-after.py
"""
import json, threading, http.server, functools, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, 'after')
os.makedirs(OUTDIR, exist_ok=True)
PORT = 18741

os.chdir(HERE)
Handler = functools.partial(http.server.SimpleHTTPRequestHandler)
httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), Handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
URL = f'http://127.0.0.1:{PORT}/dashboard-pass6.html'

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

def main():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.firefox.launch()
        pg = b.new_page(viewport={"width":1440,"height":900})
        errs = []
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(URL, wait_until="load")
        pg.wait_for_timeout(2500)
        pg.evaluate(SETUP)
        pg.wait_for_timeout(500)
        print("landed after setup:", pg.evaluate("window._dashDataLanded"), flush=True)
        print("notes orb before click:", pg.evaluate("document.querySelectorAll('.os-ld-n')[2].textContent"), flush=True)
        pg.evaluate("document.querySelector('.os-pts-btn[data-mode=\"pct\"]').click()")
        last = 0
        for t in (50, 200, 800, 2000):
            pg.wait_for_timeout(t - last); last = t
            r = pg.evaluate("""() => {
              const n = document.querySelectorAll('.os-ld-n')[2];
              const s = document.querySelectorAll('.os-ld-n')[0];
              return {landed: window._dashDataLanded, notes: n ? n.textContent : null,
                      notesHTML: n ? n.innerHTML.slice(0,160) : null,
                      sales: s ? s.textContent : null, pts: n ? n._osMiniPts : null,
                      unit: (document.querySelectorAll('.os-ld-node .os-ld-unit')[2]||{}).textContent};
            }""")
            print(f"+{t}ms:", json.dumps(r), flush=True)
        print("console errors:", errs, flush=True)
        b.close()
    httpd.shutdown()
main()
