"""PASS-6-ON-PASS-7 REBASE probe (builder seat's own probes, own eyes).
Serves pass6on7/ locally; loads the MERGED file (git merge-file, 0 conflicts)
+ pass-5 control for minis A/B. Synthetic spine score 1120 / clicks 1100
(Shawn's live values) via the page's own _osRenderLinks + renderBoards.
Per width (360/390/1440) x mode (PTS/%/MONEY) x scenario (link-holder,
page-holder Business incl. saved-holder reload): orb tile-digit px + font +
text + orb diameter, note rect + overlap vs dial SVG, gauge numeral/state/
caption at 3s AND 9s, Quiet scan, Ambassador sample, minis, overflow,
console errors, fit scale. Plus per width: pass-7 boards (1 button each,
size/href/rest+hover), Reports white, notif rect at scroll 0 + click opens
Running feed + Escape, gray sweep, D1/D2/D3, D4-R1 scroll rest.
Usage: python3 p67_probe.py  -> p67.json + shots/
"""
import json, threading, http.server, functools, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'p67.json')
SHOTS = os.path.join(HERE, 'shots')
os.makedirs(SHOTS, exist_ok=True)
PORT = 18761

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

MEASURE = r"""
(mode) => {
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect();
    return {x:+b.x.toFixed(1), y:+b.y.toFixed(1), w:+b.width.toFixed(1), h:+b.height.toFixed(1),
      top:+b.top.toFixed(1), bottom:+b.bottom.toFixed(1), left:+b.left.toFixed(1), right:+b.right.toFixed(1)}; };
  const overlap = (a, b) => { if (!a || !b) return 0;
    const iw = Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left));
    const ih = Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
    return +(iw*ih).toFixed(1); };
  const vh = window.innerHeight;
  const bars = [];
  document.querySelectorAll('body *').forEach((el) => {
    const cs = getComputedStyle(el);
    if (cs.position !== 'fixed' || cs.display === 'none' || cs.visibility === 'hidden') return;
    const b = el.getBoundingClientRect();
    if (b.width < 100 || b.height < 8) return;
    if (b.bottom >= vh - 2 && b.top < vh) bars.push({cls: (el.className.baseVal !== undefined ? el.className.baseVal : el.className || '').toString().slice(0,60), id: el.id || '', rect: r(el)});
  });
  const out = {mode, scrollY: Math.round(window.scrollY),
    fitScale: (() => { const hf = document.getElementById('os-hero-fit'); if (!hf) return null;
      const m = getComputedStyle(hf).transform.match(/matrix\(([^,]+)/); return m ? +parseFloat(m[1]).toFixed(3) : null; })(),
    dial: r(document.querySelector('#tn-tacho-mount svg.tn-tacho-dial')),
    bars, orbs: [], note: null, toggle: null, gauge: null,
    quietOnPage: (document.body.innerText || '').includes('Quiet — nothing measured yet'),
    quietCount: ((document.body.innerText || '').match(/Quiet — nothing measured yet/g) || []).length,
    sample: null, overflowX: document.documentElement.scrollWidth > document.documentElement.clientWidth,
    scrollW: document.documentElement.scrollWidth, clientW: document.documentElement.clientWidth,
    maxScroll: Math.round(document.documentElement.scrollHeight - window.innerHeight),
    featuredDisplay: null};
  try { const v = window._featuredDisplay(); out.featuredDisplay = {kind: v.kind, id: v.id, marker: v.marker, name: v.name, center: v.center}; } catch(e){ out.featuredDisplay = {error: String(e)}; }
  document.querySelectorAll('#os-ld-nodes .os-ld-node').forEach((o) => {
    const n = o.querySelector('.os-ld-n');
    const lbl = o.querySelector('.os-ld-lbl');
    const cs = n ? getComputedStyle(n) : null;
    const lcs = lbl ? getComputedStyle(lbl) : null;
    const tile = n ? n.querySelector('.os-mini-tile .rd') : null;
    const tcs = tile ? getComputedStyle(tile) : null;
    out.orbs.push({key: o.getAttribute('data-node'),
      orbD: +o.getBoundingClientRect().width.toFixed(1),
      numText: n ? n.textContent.trim() : null,
      numFontPx: cs ? parseFloat(cs.fontSize) : null,
      numFamily: cs ? cs.fontFamily.slice(0,80) : null,
      numWeight: cs ? cs.fontWeight : null,
      labelText: lbl ? lbl.textContent.trim().slice(0,30) : null,
      labelFontPx: lcs ? parseFloat(lcs.fontSize) : null,
      tiled: !!n.querySelector('.os-mini-num'),
      tileDigitPx: tcs ? parseFloat(tcs.fontSize) : null,
      tileDigitFamily: tcs ? tcs.fontFamily.slice(0,80) : null});
  });
  const note = document.getElementById('os-pts-note');
  if (note) { const cs = getComputedStyle(note); const nr = r(note);
    out.note = {text: note.textContent.trim().slice(0, 200), fontPx: parseFloat(cs.fontSize),
      color: cs.color, rect: nr, visibility: cs.visibility, display: cs.display,
      visible: nr.width > 0 && nr.height > 0 && cs.visibility !== 'hidden',
      overlapDial: overlap(nr, out.dial),
      barOverlap: Math.max(0, ...bars.map(b => overlap(nr, b.rect))),
      barCoveredH: (() => { let m = 0; bars.forEach(b => { const ih = Math.max(0, Math.min(nr.bottom, b.rect.bottom) - Math.max(nr.top, b.rect.top)); const iw = Math.max(0, Math.min(nr.right, b.rect.right) - Math.max(nr.left, b.rect.left)); if (iw > 0) m = Math.max(m, ih); }); return +m.toFixed(1); })()}; }
  const tg = document.getElementById('os-pts-toggle');
  if (tg) { const tr = r(tg);
    out.toggle = {rect: tr, barOverlap: Math.max(0, ...bars.map(b => overlap(tr, b.rect))),
      barCoveredH: (() => { let m = 0; bars.forEach(b => { const ih = Math.max(0, Math.min(tr.bottom, b.rect.bottom) - Math.max(tr.top, b.rect.top)); const iw = Math.max(0, Math.min(tr.right, b.rect.right) - Math.max(tr.left, b.rect.left)); if (iw > 0) m = Math.max(m, ih); }); return +m.toFixed(1); })(),
      activeBtn: (() => { const a = tg.querySelector('.os-pts-btn.active, [aria-pressed="true"]'); return a ? a.textContent.trim() : null; })()}; }
  const tacho = document.querySelector('#tn-tacho-mount .tn-tacho');
  const numEl = document.querySelector('#tn-tacho-mount .tn-tacho-num') || document.querySelector('.tn-tacho-num');
  const cap = document.querySelector('#tn-tacho-mount .tn-tacho-cap');
  const svgnum = document.querySelector('#tn-tacho-mount .tn-tacho-svgnum');
  out.gauge = {state: tacho ? tacho.getAttribute('data-state') : null,
    target: tacho ? tacho.getAttribute('data-target') : null,
    numeral: numEl ? numEl.textContent.trim() : null,
    svgnum: svgnum ? svgnum.textContent.trim() : null,
    capText: cap ? cap.textContent.trim().slice(0,120) : null,
    capHidden: cap ? !!cap.hidden : null};
  const sl = document.querySelector('.os-feat-sample-link');
  if (sl) { out.sample = {text: sl.textContent.trim(), href: sl.getAttribute('href'), rect: r(sl),
    fontPx: parseFloat(getComputedStyle(sl).fontSize), color: getComputedStyle(sl).color}; }
  out.minis = Array.from(document.querySelectorAll('.os-sl-gauge-num, .os-sl-stat-n')).slice(0, 30).map(el => (el.textContent || '').trim().slice(0, 24));
  out.miniTiled = Array.from(document.querySelectorAll('.os-sl-gauge-num, .os-sl-stat-n')).slice(0, 30).map(el => !!el.querySelector('.os-mini-num'));
  return out;
}
"""

BOARDS = r"""
() => {
  const out = {boards: [], graySweep: [], notif: null, reports: null, sub: null,
    whatNayaDoes: 0, drillGold: [], drillRowCount: 0};
  document.querySelectorAll('.os-world-board').forEach(b => {
    const title = b.querySelector('.os-wb-id b') ? b.querySelector('.os-wb-id b').textContent : '?';
    const ac = getComputedStyle(b).getPropertyValue('--ac').trim();
    const btns = [...b.querySelectorAll('button, a')].map(el => {
      const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
      return {tag: el.tagName, cls: el.className, text: (el.textContent||'').trim().slice(0,40),
        disabled: !!el.disabled, w: Math.round(r.width*10)/10, h: Math.round(r.height*10)/10,
        border: cs.borderColor, bg: cs.backgroundImage.slice(0,80), color: cs.color,
        shadow: cs.boxShadow.slice(0,300), href: el.getAttribute('href') || null,
        visible: r.width > 0 && r.height > 0};
    });
    out.boards.push({title, kind: b.getAttribute('data-holder-kind'), id: b.getAttribute('data-holder-id'),
      ac, featTag: !!b.querySelector('.os-wb-feat'),
      linkRows: b.querySelectorAll('.os-link-row').length, minis: b.querySelectorAll('.os-sl-gauge').length,
      btns});
  });
  const scopes = [...document.querySelectorAll('.os-world-board'), document.querySelector('#os-reports-board')].filter(Boolean);
  const seen = new Set();
  scopes.forEach(sc => {
    const walker = document.createTreeWalker(sc, NodeFilter.SHOW_TEXT);
    let n;
    while (n = walker.nextNode()) {
      const txt = (n.textContent||'').trim();
      if (!txt) continue;
      const el = n.parentElement; if (!el) continue;
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) continue;
      const cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'none') continue;
      const key = txt.slice(0,40) + '|' + cs.color + '|' + cs.fontSize;
      if (seen.has(key)) continue; seen.add(key);
      const m = cs.color.match(/rgba?\(([^)]+)\)/);
      let rgb = m ? m[1].split(',').map(Number) : [0,0,0];
      const alpha = rgb.length > 3 ? rgb[3] : 1;
      const mx = Math.max(rgb[0],rgb[1],rgb[2]), mn = Math.min(rgb[0],rgb[1],rgb[2]);
      const lum = (0.2126*rgb[0]+0.7152*rgb[1]+0.0722*rgb[2])/255;
      const isGrayish = (mx-mn) < 28 && lum > 0.22 && lum < 0.92;
      const isDimWhite = alpha < 0.85 && mx > 200;
      out.graySweep.push({text: txt.slice(0,55), color: cs.color, size: cs.fontSize, weight: cs.fontWeight,
        board: sc.id || (sc.querySelector('.os-wb-id b')||{}).textContent || '?',
        grayish: isGrayish, dimWhite: isDimWhite, lum: Math.round(lum*100)/100});
    }
  });
  const rep = document.querySelector('#os-reports-board');
  out.reports = rep ? {ps: [...rep.querySelectorAll('p')].map(p => {
    const cs = getComputedStyle(p);
    return {text: p.textContent.trim().slice(0,90), color: cs.color, size: cs.fontSize, weight: cs.fontWeight};
  })} : null;
  const nr = document.querySelector('.os-notif-row');
  if (nr) { const btn = document.querySelector('#os-notif-btn');
    const br = btn ? btn.getBoundingClientRect() : null;
    out.notif = {parentId: nr.parentElement ? nr.parentElement.id : null,
      firstChild: nr.parentElement ? nr.parentElement.firstElementChild === nr : null,
      btnRect: br ? {x: Math.round(br.x), y: Math.round(br.y), w: Math.round(br.width), h: Math.round(br.height),
        rightGap: Math.round(window.innerWidth - br.right)} : null,
      viewportW: window.innerWidth, scrollY: window.scrollY};
  }
  out.sub = (document.querySelector('.os-wb-sub')||{}).textContent || null;
  out.whatNayaDoes = (document.body.innerText.match(/What Naya Does/g) || []).length;
  out.drillGold = [...document.querySelectorAll('.os-link-row button')].filter(b => /Show on gauge/i.test(b.textContent||'')).map(el => ({text:(el.textContent||'').trim().slice(0,30), border: getComputedStyle(el).borderColor})).slice(0,8);
  out.drillRowCount = document.querySelectorAll('.os-link-row').length;
  return out;
}
"""

HOVER = r"""
(boardIdx) => {
  const b = document.querySelectorAll('.os-world-board')[boardIdx];
  if (!b) return {error: 'no board ' + boardIdx};
  const btn = b.querySelector('.os-wb-btn');
  if (!btn) return {error: 'no btn'};
  const cs = getComputedStyle(btn);
  return {board: (b.querySelector('.os-wb-id b')||{}).textContent, ac: getComputedStyle(b).getPropertyValue('--ac').trim(),
    border: cs.borderColor, shadow: cs.boxShadow, bg: cs.backgroundImage.slice(0,90)};
}
"""

D4R1 = r"""() => { const de = document.documentElement; window.scrollTo(0, de.scrollHeight - window.innerHeight); return {maxScroll: Math.round(de.scrollHeight - window.innerHeight), at: Math.round(window.scrollY)}; }"""
D4R1_REST = r"""() => { const de = document.documentElement; return {scrollY: Math.round(window.scrollY), maxScroll: Math.round(de.scrollHeight - window.innerHeight)}; }"""

def js(pg, expr):
    try: return pg.evaluate(expr)
    except Exception as e: return {"error": str(e)[:400]}

results = {}
def save():
    json.dump(results, open(OUT, 'w'), indent=1)

from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.firefox.launch()
    # --- pass-5 control: minis at 390 + 1440 (PTS only) ---
    for width in (390, 1440):
        page = browser.new_page(viewport={'width': width, 'height': 844})
        errs = []
        page.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        page.on('pageerror', lambda e: errs.append(str(e)))
        page.goto(f'http://127.0.0.1:{PORT}/dashboard-pass5-blob.html', wait_until='load', timeout=60000)
        page.wait_for_timeout(2500)
        js(page, SETUP); page.wait_for_timeout(2500)
        m = js(page, MEASURE)
        results[f'pass5ctl-{width}'] = {'minis': m.get('minis'), 'miniTiled': m.get('miniTiled'),
            'orbs': m.get('orbs'), 'consoleErrors': errs}
        save(); print('done pass5ctl', width, flush=True); page.close()
    # --- merged file ---
    for width in (390, 1440, 360):
        page = browser.new_page(viewport={'width': width, 'height': 844})
        errs = []
        page.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        page.on('pageerror', lambda e: errs.append(str(e)))
        page.goto(f'http://127.0.0.1:{PORT}/dashboard-pass6on7.html', wait_until='load', timeout=60000)
        page.wait_for_timeout(2500)
        js(page, SETUP); page.wait_for_timeout(2500)
        data = {'modes': {}, 'consoleErrors': errs}
        for mode in ('pts', 'pct', 'money'):
            page.evaluate(f"() => {{ const b = document.querySelector('.os-pts-btn[data-mode=\"{mode}\"]'); if (b) b.click(); }}")
            page.wait_for_timeout(3000)
            m3 = js(page, MEASURE)
            page.wait_for_timeout(6000)
            m9 = js(page, MEASURE)
            m3['gaugeAt9s'] = m9['gauge']; m3['fitScaleAt9s'] = m9['fitScale']
            m3['noteAt9s'] = m9['note']; m3['toggleAt9s'] = m9['toggle']
            data['modes'][mode] = m3
            page.evaluate("window.scrollTo(0,0)"); page.wait_for_timeout(400)
            page.screenshot(path=os.path.join(SHOTS, f'p67-hero-{width}-{mode}.png'))
        # boards / notif / gray (link-holder state, PTS)
        page.evaluate("() => { const b = document.querySelector('.os-pts-btn[data-mode=\"pts\"]'); if (b) b.click(); }")
        page.wait_for_timeout(1500)
        b = js(page, BOARDS)
        b['consoleErrors'] = errs
        # hover each board button (real mouse, 1.5s settle at 1440 per v7 lesson)
        b['hovers'] = []
        for i in range(4):
            try:
                box = page.locator('.os-world-board >> nth=%d >> .os-wb-btn' % i).bounding_box()
                if box:
                    page.mouse.move(box['x'] + box['width']/2, box['y'] + box['height']/2, steps=5)
                    page.wait_for_timeout(1600)
                    b['hovers'].append(js(page, HOVER))
                else: b['hovers'].append({'error': 'no box'})
            except Exception as e: b['hovers'].append({'error': str(e)})
        page.mouse.move(5, 5, steps=3); page.wait_for_timeout(400)
        b['rests'] = [js(page, HOVER) for i in range(4)]
        # notif click
        try:
            page.evaluate("() => { window.scrollTo(0,0); }"); page.wait_for_timeout(300)
            page.click('#os-notif-btn', timeout=5000); page.wait_for_timeout(700)
            b['notifClick'] = js(page, "() => ({feedOpen: document.body.classList.contains('os-feed-open'), boardVisible: !!document.querySelector('#os-feed-board') && getComputedStyle(document.querySelector('#os-feed-board')).display !== 'none', feedText: (document.querySelector('#os-feed-board')||{}).textContent ? document.querySelector('#os-feed-board').textContent.slice(0,200) : null})")
            page.screenshot(path=os.path.join(SHOTS, f'p67-notif-{width}.png'))
            page.keyboard.press('Escape'); page.wait_for_timeout(300)
            b['notifAfterEsc'] = js(page, "() => document.body.classList.contains('os-feed-open')")
        except Exception as e: b['notifClick'] = {'error': str(e)}
        # sample link click (new tab)
        try:
            page.evaluate("() => { const f = document.getElementById('os-feat-panel'); if (f) f.scrollIntoView({block:'center'}); }")
            page.wait_for_timeout(800)
            page.screenshot(path=os.path.join(SHOTS, f'p67-feat-{width}.png'))
            with page.expect_popup(timeout=10000) as pop:
                page.click('.os-feat-sample-link', timeout=5000)
            np = pop.value
            np.wait_for_load_state('domcontentloaded', timeout=20000)
            b['sampleClick'] = {'url': np.url, 'title': np.title()}
            np.close()
        except Exception as e: b['sampleClick'] = {'error': str(e)[:300]}
        # boards + reports screenshots
        by = js(page, "() => { const b = document.querySelector('.os-world-board'); return b ? Math.round(b.getBoundingClientRect().top + window.scrollY) : 0; }")
        page.evaluate(f"() => window.scrollTo(0, {max(by-20,0)})"); page.wait_for_timeout(300)
        page.screenshot(path=os.path.join(SHOTS, f'p67-boards-{width}.png'))
        ry = js(page, "() => { const b = document.querySelector('#os-reports-board'); return b ? Math.round(b.getBoundingClientRect().top + window.scrollY) : 0; }")
        page.evaluate(f"() => window.scrollTo(0, {max(ry-20,0)})"); page.wait_for_timeout(300)
        page.screenshot(path=os.path.join(SHOTS, f'p67-reports-{width}.png'))
        # D4-R1
        page.evaluate("window.scrollTo(0,0)"); page.wait_for_timeout(500)
        d = js(page, D4R1); page.wait_for_timeout(5000)
        rest = js(page, D4R1_REST)
        b['d4r1'] = {'scrolled': d, 'rest5s': rest}
        data['boards'] = b
        # --- page-holder scenario: saved Business holder (Shawn's persisted state) ---
        page.evaluate("() => { localStorage.setItem('os-featured-holder', JSON.stringify({kind:'page', id:'business', label:'Business'})); return 'saved'; }")
        page.reload(wait_until='load', timeout=60000); page.wait_for_timeout(2500)
        js(page, SETUP); page.wait_for_timeout(2500)
        ph = {'modes': {}}
        for mode in ('pts', 'pct', 'money'):
            page.evaluate(f"() => {{ const b = document.querySelector('.os-pts-btn[data-mode=\"{mode}\"]'); if (b) b.click(); }}")
            page.wait_for_timeout(3000)
            m3 = js(page, MEASURE)
            page.wait_for_timeout(6000)
            m9 = js(page, MEASURE)
            m3['gaugeAt9s'] = m9['gauge']
            ph['modes'][mode] = m3
            page.evaluate("window.scrollTo(0,0)"); page.wait_for_timeout(400)
        ph['savedHolderSurvives'] = js(page, "() => localStorage.getItem('os-featured-holder')")
        data['pageHolder'] = ph
        page.evaluate("() => { const b = document.querySelector('.os-pts-btn[data-mode=\"pts\"]'); if (b) b.click(); }")
        page.wait_for_timeout(9000)
        page.screenshot(path=os.path.join(SHOTS, f'p67-pageholder-{width}-pts.png'))
        data['consoleErrors'] = errs
        results[f'merged-{width}'] = data
        save(); print('done merged', width, flush=True); page.close()
    browser.close()
save()
print('wrote', OUT)
