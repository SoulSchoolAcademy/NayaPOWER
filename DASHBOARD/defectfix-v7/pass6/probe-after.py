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

MEASURE = r"""
(mode, scenario) => {
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect();
    return {x:+b.x.toFixed(1), y:+b.y.toFixed(1), w:+b.width.toFixed(1), h:+b.height.toFixed(1),
      top:+b.top.toFixed(1), bottom:+b.bottom.toFixed(1), left:+b.left.toFixed(1), right:+b.right.toFixed(1)}; };
  const out = {mode, scenario, heroMode: document.body.classList.contains('hero-mode'),
    constellation: r(document.getElementById('os-constellation')),
    dial: r(document.querySelector('#tn-tacho-mount svg.tn-tacho-dial')),
    mount: r(document.getElementById('tn-tacho-mount')),
    heroFitScale: (() => { const hf = document.getElementById('os-hero-fit'); const m = getComputedStyle(hf).transform.match(/matrix\(([^,]+)/); return m ? +parseFloat(m[1]).toFixed(3) : null; })(),
    orbs: [], note: null, noteOverlapDialPx: null, toggle: r(document.getElementById('os-pts-toggle')),
    gauge: null, quietOnPage: (document.body.innerText || '').includes('Quiet — nothing measured yet'),
    sample: null, featPanel: null};
  document.querySelectorAll('#os-ld-nodes .os-ld-node').forEach((o) => {
    const n = o.querySelector('.os-ld-n');
    const lbl = o.querySelector('.os-ld-lbl');
    const cs = n ? getComputedStyle(n) : null;
    const lcs = lbl ? getComputedStyle(lbl) : null;
    const nr = n ? n.getBoundingClientRect() : null;
    out.orbs.push({key: o.getAttribute('data-node'),
      orbD: +o.getBoundingClientRect().width.toFixed(1),
      orbRect: r(o),
      numText: n ? n.textContent.trim() : null,
      numFontPx: cs ? parseFloat(cs.fontSize) : null,
      numRect: r(n), numW: nr ? +nr.width.toFixed(1) : null, numH: nr ? +nr.height.toFixed(1) : null,
      numFamily: cs ? cs.fontFamily.slice(0,60) : null, numWeight: cs ? cs.fontWeight : null,
      labelText: lbl ? lbl.textContent.trim().slice(0,30) : null,
      labelFontPx: lcs ? parseFloat(lcs.fontSize) : null,
      tiled: !!n.querySelector('.os-mini-num'),
      tileCount: n ? n.querySelectorAll('.os-mini-tile').length : 0,
      tileDigitPx: (() => { const t = n ? n.querySelector('.os-mini-tile .rd') : null; return t ? parseFloat(getComputedStyle(t).fontSize) : null; })(),
      tileW: (() => { const t = n ? n.querySelector('.os-mini-tile') : null; return t ? +t.getBoundingClientRect().width.toFixed(1) : null; })()});
  });
  const note = document.getElementById('os-pts-note');
  if (note) {
    const cs = getComputedStyle(note);
    const nr = note.getBoundingClientRect();
    out.note = {text: note.textContent.trim().slice(0, 160),
      fontPx: parseFloat(cs.fontSize), color: cs.color, rect: r(note),
      visibility: cs.visibility, display: cs.display,
      visible: nr.width > 0 && nr.height > 0 && cs.visibility !== 'hidden'};
    const dr = out.dial;
    if (dr && nr.width > 0 && nr.height > 0 && cs.visibility !== 'hidden') {
      const iw = Math.max(0, Math.min(nr.right, dr.right) - Math.max(nr.left, dr.left));
      const ih = Math.max(0, Math.min(nr.bottom, dr.bottom) - Math.max(nr.top, dr.top));
      out.noteOverlapDialPx = {w:+iw.toFixed(1), h:+ih.toFixed(1), area:+(iw*ih).toFixed(1)};
    } else { out.noteOverlapDialPx = {w:0, h:0, area:0}; }
  }
  const tacho = document.querySelector('#tn-tacho-mount .tn-tacho');
  const numEl = document.querySelector('#tn-tacho-mount .tn-tacho-num') || document.querySelector('.tn-tacho-num');
  const cap = document.querySelector('#tn-tacho-mount .tn-tacho-cap');
  const svgnum = document.querySelector('#tn-tacho-mount .tn-tacho-svgnum');
  out.gauge = {state: tacho ? tacho.getAttribute('data-state') : null,
    target: tacho ? tacho.getAttribute('data-target') : null,
    numeral: numEl ? numEl.textContent.trim() : null,
    numeralFontPx: numEl ? parseFloat(getComputedStyle(numEl).fontSize) : null,
    svgnum: svgnum ? svgnum.textContent.trim() : null,
    capText: cap ? cap.textContent.trim().slice(0,120) : null,
    capHidden: cap ? !!cap.hidden : null,
    capRect: r(cap)};
  const sl = document.querySelector('.os-feat-sample-link');
  if (sl) { out.sample = {text: sl.textContent.trim(), href: sl.getAttribute('href'), rect: r(sl),
    fontPx: parseFloat(getComputedStyle(sl).fontSize), color: getComputedStyle(sl).color}; }
  const fp = document.getElementById('os-feat-panel');
  if (fp) { const mk = document.getElementById('os-feat-marker'); const nm = document.getElementById('os-feat-name');
    const sc = document.getElementById('os-feat-scope');
    out.featPanel = {marker: mk ? mk.textContent.trim() : null, name: nm ? nm.textContent.trim() : null,
      scope: sc ? sc.textContent.trim().slice(0,120) : null}; }
  out.minis = Array.from(document.querySelectorAll('.os-sl-gauge-num, .os-sl-stat-n')).slice(0, 30).map(el => ({cls: el.className.slice(0, 30), text: (el.textContent || '').trim().slice(0, 24), tiled: !!el.querySelector('.os-mini-num')}));
  out.overflowX = document.documentElement.scrollWidth > document.documentElement.clientWidth;
  out.scrollW = document.documentElement.scrollWidth; out.clientW = document.documentElement.clientWidth;
  return out;
}
"""

def js(pg, expr):
    try: return pg.evaluate(expr)
    except Exception as e: return {"error": str(e)[:400]}

results = {}
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.firefox.launch()
    for scenario in ('link', 'page'):
        for width, height in ((390, 844), (1440, 900), (360, 800)):
            errors = []
            page = browser.new_page(viewport={'width': width, 'height': height})
            if scenario == 'page':
                page.add_init_script("try { localStorage.setItem('os-featured-holder', JSON.stringify({kind:'page', id:'business', label:'Business'})); } catch(e){}")
            page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(URL, wait_until='load', timeout=60000)
            page.wait_for_timeout(2500)
            js(page, SETUP)
            page.wait_for_timeout(2500)
            n = js(page, "() => document.querySelectorAll('#os-ld-nodes .os-ld-node').length")
            data = {'orbCount': n, 'modes': {}, 'consoleErrors': errors}
            for mode in ('pts', 'pct', 'money'):
                try:
                    page.evaluate(f"() => {{ const b = document.querySelector('.os-pts-btn[data-mode=\"{mode}\"]'); if (b) b.click(); }}")
                except Exception as e:
                    data.setdefault('clickErrors', {})[mode] = str(e)[:200]
                page.wait_for_timeout(3000)
                m = js(page, MEASURE)
                m['mode'] = mode
                data['modes'][mode] = m
                page.evaluate("window.scrollTo(0,0)")
                page.wait_for_timeout(400)
                page.screenshot(path=os.path.join(OUTDIR, f'p6-hero-{scenario}-{width}-{mode}.png'))
            # feat panel screenshot at 390 + 1440, link scenario, pts mode
            if scenario == 'link' and width in (390, 1440):
                page.evaluate("() => { document.querySelector('.os-pts-btn[data-mode=\"pts\"]').click(); }")
                page.wait_for_timeout(700)
                page.evaluate("() => { const f = document.getElementById('os-feat-panel'); if (f) f.scrollIntoView({block:'center'}); }")
                page.wait_for_timeout(800)
                page.screenshot(path=os.path.join(OUTDIR, f'p6-feat-{width}.png'))
            data['consoleErrors'] = errors
            results[f'{scenario}-{width}'] = data
            json.dump(results, open(os.path.join(OUTDIR, 'after.json'), 'w'), indent=1)
            print('done', scenario, width, 'orbs', n, flush=True)
            page.close()
    browser.close()
json.dump(results, open(os.path.join(OUTDIR, 'after.json'), 'w'), indent=1)
print('wrote', os.path.join(OUTDIR, 'after.json'))
