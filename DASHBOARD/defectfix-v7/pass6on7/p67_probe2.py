"""PASS-6-ON-7 probe 2 — follow-ups from probe 1.
A: money-first on a FRESH load (merged vs pass6 vs pass7) — is money mode
   broken in the merged file, or was probe 1's late money click past the
   sandbox stale-ledger timer?
B: fit-scale / visual orb size / minis A/B across pass5, pass6, pass7, merged.
C: hover/rest with the arg bug fixed (probe 1 passed no board index).
D: page-holder (saved Business) fresh load per mode — gauge live in each mode?
Usage: python3 p67_probe2.py -> p67b.json + shots2/
"""
import json, threading, http.server, functools, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'p67b.json')
SHOTS = os.path.join(HERE, 'shots2')
os.makedirs(SHOTS, exist_ok=True)
PORT = 18762

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

GAUGE = r"""() => {
  const tacho = document.querySelector('#tn-tacho-mount .tn-tacho');
  const numEl = document.querySelector('#tn-tacho-mount .tn-tacho-num') || document.querySelector('.tn-tacho-num');
  const cap = document.querySelector('#tn-tacho-mount .tn-tacho-cap');
  let fd = null; try { const v = window._featuredDisplay(); fd = {kind: v.kind, id: v.id, marker: v.marker, name: v.name, center: v.center}; } catch(e){ fd = {error: String(e)}; }
  return {state: tacho ? tacho.getAttribute('data-state') : null,
    numeral: numEl ? numEl.textContent.trim() : null,
    capText: cap ? cap.textContent.trim().slice(0,120) : null,
    quietOnPage: (document.body.innerText || '').includes('Quiet — nothing measured yet'),
    spineStale: (typeof window._osSpineStale !== 'undefined') ? window._osSpineStale : null,
    fd};
}"""

FIT = r"""() => {
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect();
    return {x:+b.x.toFixed(1), y:+b.y.toFixed(1), w:+b.width.toFixed(1), h:+b.height.toFixed(1), top:+b.top.toFixed(1), bottom:+b.bottom.toFixed(1)}; };
  const hf = document.getElementById('os-hero-fit');
  let fit = null;
  if (hf) { const m = getComputedStyle(hf).transform.match(/matrix\(([^,]+)/); fit = m ? +parseFloat(m[1]).toFixed(3) : 'none'; }
  const bar = document.getElementById('os-bottom3');
  const note = document.getElementById('os-pts-note');
  const tg = document.getElementById('os-pts-toggle');
  const orbs = [];
  document.querySelectorAll('#os-ld-nodes .os-ld-node').forEach((o) => {
    const n = o.querySelector('.os-ld-n');
    const tile = n ? n.querySelector('.os-mini-tile .rd') : null;
    const tr = tile ? tile.getBoundingClientRect() : null;
    orbs.push({key: o.getAttribute('data-node'), orbD: +o.getBoundingClientRect().width.toFixed(1),
      numText: n ? n.textContent.trim() : null,
      tileDigitPx: tile ? parseFloat(getComputedStyle(tile).fontSize) : null,
      tileDigitVisualH: tr ? +tr.height.toFixed(1) : null, tiled: !!n.querySelector('.os-mini-num')});
  });
  return {fit, barTop: bar ? +bar.getBoundingClientRect().top.toFixed(1) : null,
    note: note ? {rect: r(note), visibility: getComputedStyle(note).visibility, text: note.textContent.trim().slice(0,80)} : null,
    toggle: tg ? {rect: r(tg)} : null, orbs,
    minis: Array.from(document.querySelectorAll('.os-sl-gauge-num, .os-sl-stat-n')).slice(0, 30).map(el => (el.textContent || '').trim().slice(0, 24)),
    overflowX: document.documentElement.scrollWidth > document.documentElement.clientWidth};
}"""

HOVER = """(boardIdx) => {
  const b = document.querySelectorAll('.os-world-board')[boardIdx];
  if (!b) return {error: 'no board ' + boardIdx};
  const btn = b.querySelector('.os-wb-btn');
  if (!btn) return {error: 'no btn'};
  const cs = getComputedStyle(btn);
  return {board: (b.querySelector('.os-wb-id b')||{}).textContent, ac: getComputedStyle(b).getPropertyValue('--ac').trim(),
    border: cs.borderColor, shadow: cs.boxShadow, bg: cs.backgroundImage.slice(0,90)};
}"""

def js(pg, expr, arg=None):
    try: return pg.evaluate(expr, arg) if arg is not None else pg.evaluate(expr)
    except Exception as e: return {"error": str(e)[:400]}

results = {}
def save(): json.dump(results, open(OUT, 'w'), indent=1)

from playwright.sync_api import sync_playwright
FILES = {'pass5': 'dashboard-pass5-blob.html', 'pass6': 'dashboard-pass6-blob.html',
         'pass7': 'dashboard-pass7-blob.html', 'merged': 'dashboard-pass6on7.html'}
with sync_playwright() as p:
    browser = p.firefox.launch()
    # --- A: money-first fresh load ---
    for tag in ('merged', 'pass6', 'pass7'):
        for width in (390, 1440):
            page = browser.new_page(viewport={'width': width, 'height': 844})
            errs = []
            page.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
            page.on('pageerror', lambda e: errs.append(str(e)))
            page.goto(f'http://127.0.0.1:{PORT}/{FILES[tag]}', wait_until='load', timeout=60000)
            page.wait_for_timeout(2000)
            js(page, SETUP); page.wait_for_timeout(1000)
            page.evaluate("() => { const b = document.querySelector('.os-pts-btn[data-mode=\"money\"]'); if (b) b.click(); }")
            samples = []
            for wait in (1, 2, 3, 3):
                page.wait_for_timeout(wait * 1000)
                samples.append(js(page, GAUGE))
            page.screenshot(path=os.path.join(SHOTS, f'p67b-moneyfirst-{tag}-{width}.png'))
            # then pts, for the control
            page.evaluate("() => { const b = document.querySelector('.os-pts-btn[data-mode=\"pts\"]'); if (b) b.click(); }")
            page.wait_for_timeout(9000)
            pts9 = js(page, GAUGE)
            results[f'A-moneyfirst-{tag}-{width}'] = {'moneySamples': samples, 'ptsAfter9s': pts9, 'consoleErrors': errs}
            save(); print('done A', tag, width, flush=True); page.close()
    # --- B: fit / visual orbs / minis A/B, PTS ---
    for tag in ('pass5', 'pass6', 'pass7', 'merged'):
        for width in (390, 1440):
            page = browser.new_page(viewport={'width': width, 'height': 844})
            errs = []
            page.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
            page.on('pageerror', lambda e: errs.append(str(e)))
            page.goto(f'http://127.0.0.1:{PORT}/{FILES[tag]}', wait_until='load', timeout=60000)
            page.wait_for_timeout(2500)
            js(page, SETUP); page.wait_for_timeout(2500)
            f = js(page, FIT)
            # click % to also capture the note rect + visibility in % mode
            page.evaluate("() => { const b = document.querySelector('.os-pts-btn[data-mode=\"pct\"]'); if (b) b.click(); }")
            page.wait_for_timeout(3000)
            f_pct = js(page, FIT)
            page.screenshot(path=os.path.join(SHOTS, f'p67b-hero-pct-{tag}-{width}.png'))
            results[f'B-fit-{tag}-{width}'] = {'pts': f, 'pct': f_pct, 'consoleErrors': errs}
            save(); print('done B', tag, width, flush=True); page.close()
    # --- C: hover/rest fixed ---
    for width in (390, 1440):
        page = browser.new_page(viewport={'width': width, 'height': 844})
        errs = []
        page.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        page.on('pageerror', lambda e: errs.append(str(e)))
        page.goto(f'http://127.0.0.1:{PORT}/{FILES["merged"]}', wait_until='load', timeout=60000)
        page.wait_for_timeout(2500)
        js(page, SETUP); page.wait_for_timeout(1500)
        page.evaluate("window.scrollTo(0,0)"); page.wait_for_timeout(400)
        hovers, rests = [], []
        for i in range(4):
            try:
                box = page.locator('.os-world-board >> nth=%d >> .os-wb-btn' % i).bounding_box()
                if box:
                    page.mouse.move(box['x'] + box['width']/2, box['y'] + box['height']/2, steps=5)
                    page.wait_for_timeout(1600)
                    hovers.append(js(page, HOVER, i))
                else: hovers.append({'error': 'no box'})
            except Exception as e: hovers.append({'error': str(e)})
        page.mouse.move(5, 5, steps=3); page.wait_for_timeout(400)
        for i in range(4): rests.append(js(page, HOVER, i))
        results[f'C-hover-merged-{width}'] = {'hovers': hovers, 'rests': rests, 'consoleErrors': errs}
        save(); print('done C', width, flush=True); page.close()
    # --- D: page-holder fresh load per mode ---
    for mode in ('pts', 'pct', 'money'):
        for width in (390, 1440):
            page = browser.new_page(viewport={'width': width, 'height': 844})
            errs = []
            page.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
            page.on('pageerror', lambda e: errs.append(str(e)))
            page.goto(f'http://127.0.0.1:{PORT}/{FILES["merged"]}', wait_until='load', timeout=60000)
            page.evaluate("() => { localStorage.setItem('os-featured-holder', JSON.stringify({kind:'page', id:'business', label:'Business'})); return 'saved'; }")
            page.reload(wait_until='load', timeout=60000); page.wait_for_timeout(2000)
            js(page, SETUP); page.wait_for_timeout(1000)
            page.evaluate(f"() => {{ const b = document.querySelector('.os-pts-btn[data-mode=\"{mode}\"]'); if (b) b.click(); }}")
            s3 = None; s9 = None
            page.wait_for_timeout(3000); s3 = js(page, GAUGE)
            page.wait_for_timeout(6000); s9 = js(page, GAUGE)
            page.screenshot(path=os.path.join(SHOTS, f'p67b-pageholder-{mode}-{width}.png'))
            results[f'D-page-{mode}-{width}'] = {'at3s': s3, 'at9s': s9, 'consoleErrors': errs}
            save(); print('done D', mode, width, flush=True); page.close()
    browser.close()
save()
print('wrote', OUT)
