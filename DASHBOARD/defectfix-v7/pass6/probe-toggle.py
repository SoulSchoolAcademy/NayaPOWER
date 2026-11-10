import json, threading, http.server, functools, os
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
Handler = functools.partial(http.server.SimpleHTTPRequestHandler)
httpd = http.server.ThreadingHTTPServer(('127.0.0.1', 18743), Handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
SETUP = open('probe-after.py').read().split('SETUP = """')[1].split('"""')[0]
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.firefox.launch()
    # 1. feat-block click sequence on pass-6
    pg = b.new_page(viewport={'width': 390, 'height': 844})
    pg.goto('http://127.0.0.1:18743/dashboard-pass6.html', wait_until='load')
    pg.wait_for_timeout(2500)
    pg.evaluate("() => {" + SETUP.split("() => {",1)[1])
    pg.wait_for_timeout(1500)
    pg.evaluate("document.querySelector('.os-pts-btn[data-mode=\"money\"]').click()")
    pg.wait_for_timeout(1000)
    print('after money click:', pg.evaluate("() => ({mode: window._dashMode, active: document.querySelector('.os-pts-btn.active').dataset.mode})"))
    pg.evaluate("() => { document.querySelector('.os-pts-btn[data-mode=\"pts\"]').click(); }")
    pg.wait_for_timeout(700)
    print('after feat-block pts click:', pg.evaluate("() => ({mode: window._dashMode, active: document.querySelector('.os-pts-btn.active').dataset.mode})"))
    pg.close()
    # 2. toggle rect at scroll-0, pass-5 base vs pass-6, 390 + 1440
    for fname in ('dashboard-pass5-base.html', 'dashboard-pass6.html'):
        for width, height in ((390, 844), (1440, 900)):
            pg = b.new_page(viewport={'width': width, 'height': height})
            pg.goto(f'http://127.0.0.1:18743/{fname}', wait_until='load')
            pg.wait_for_timeout(2500)
            pg.evaluate("() => {" + SETUP.split("() => {",1)[1])
            pg.wait_for_timeout(2500)
            r = pg.evaluate("""() => {
              const t = document.getElementById('os-pts-toggle').getBoundingClientRect();
              const bar = document.querySelector('.os-bottom-bar, .os-nav-bottom, [class*="bottom-bar"]');
              const br = bar ? bar.getBoundingClientRect() : null;
              return {toggleTop: Math.round(t.top), toggleBottom: Math.round(t.bottom), vh: innerHeight,
                      barTop: br ? Math.round(br.top) : null, toggleVisible: t.bottom <= innerHeight};
            }""")
            print(fname, width, r)
            pg.close()
    b.close()
httpd.shutdown()
