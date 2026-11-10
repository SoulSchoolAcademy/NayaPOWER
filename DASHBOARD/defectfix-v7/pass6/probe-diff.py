"""Compare minis + gauge landing: pass-5 base vs pass-6 file. Minis must be identical;
orb tile digits must differ (24/18 vs 13/10). Gauge numeral tracked to 10s."""
import json, threading, http.server, functools, os
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
Handler = functools.partial(http.server.SimpleHTTPRequestHandler)
httpd = http.server.ThreadingHTTPServer(('127.0.0.1', 18742), Handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
SETUP = open('probe-after.py').read().split('SETUP = """')[1].split('"""')[0]
DUMP = r"""() => {
  const minis = Array.from(document.querySelectorAll('.os-sl-gauge-num, .os-sl-stat-n')).map(el => (el.textContent||'').trim());
  const orbs = Array.from(document.querySelectorAll('#os-ld-nodes .os-ld-node .os-ld-n')).map(n => {
    const t = n.querySelector('.os-mini-tile .rd');
    return {text:(n.textContent||'').trim(), digit: t ? parseFloat(getComputedStyle(t).fontSize) : null, tiled: !!n.querySelector('.os-mini-num')};
  });
  const g = document.querySelector('#tn-tacho-mount .tn-tacho-num');
  const tacho = document.querySelector('#tn-tacho-mount .tn-tacho');
  return {minis, orbs, numeral: g ? g.textContent.trim() : null, state: tacho ? tacho.getAttribute('data-state') : null};
}"""
from playwright.sync_api import sync_playwright
out = {}
with sync_playwright() as p:
    b = p.firefox.launch()
    for fname in ('dashboard-pass5-base.html', 'dashboard-pass6.html'):
        for width, height in ((1440, 900), (390, 844)):
            pg = b.new_page(viewport={'width': width, 'height': height})
            pg.goto(f'http://127.0.0.1:18742/{fname}', wait_until='load')
            pg.wait_for_timeout(2500)
            pg.evaluate("() => {" + SETUP.split("() => {",1)[1])
            pg.wait_for_timeout(1500)
            # gauge landing track: pts mode, read every 2s to 10s
            pg.evaluate("document.querySelector('.os-pts-btn[data-mode=\"pts\"]').click()")
            track = []
            for i in range(5):
                pg.wait_for_timeout(2000)
                track.append(pg.evaluate("() => { const g = document.querySelector('#tn-tacho-mount .tn-tacho-num'); return g ? g.textContent.trim() : null; }"))
            d = pg.evaluate(DUMP)
            d['gaugeTrackPts'] = track
            out[f'{fname}-{width}'] = d
            print(fname, width, 'numeral track:', track, 'orb0:', d['orbs'][0], flush=True)
            pg.close()
    b.close()
json.dump(out, open('diff-check.json','w'), indent=1)
# diff the minis
base = out['dashboard-pass5-base.html-1440']['minis']
new = out['dashboard-pass6.html-1440']['minis']
print('minis 1440 identical:', base == new, 'count:', len(base), len(new))
if base != new:
    for i,(a,c) in enumerate(zip(base,new)):
        if a!=c: print('  mini', i, repr(a), '->', repr(c))
base = out['dashboard-pass5-base.html-390']['minis']
new = out['dashboard-pass6.html-390']['minis']
print('minis 390 identical:', base == new)
httpd.shutdown()
