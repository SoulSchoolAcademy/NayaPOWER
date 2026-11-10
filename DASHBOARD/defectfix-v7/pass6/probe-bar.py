import threading, http.server, functools, os
HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
Handler = functools.partial(http.server.SimpleHTTPRequestHandler)
httpd = http.server.ThreadingHTTPServer(('127.0.0.1', 18744), Handler)
threading.Thread(target=httpd.serve_forever, daemon=True).start()
SETUP = open('probe-after.py').read().split('SETUP = """')[1].split('"""')[0]
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.firefox.launch()
    for fname in ('dashboard-pass5-base.html', 'dashboard-pass6.html'):
        pg = b.new_page(viewport={'width': 390, 'height': 844})
        pg.goto(f'http://127.0.0.1:18744/{fname}', wait_until='load')
        pg.wait_for_timeout(2500)
        pg.evaluate("() => {" + SETUP.split("() => {",1)[1])
        pg.wait_for_timeout(2000)
        r = pg.evaluate("""() => {
          const fixed = Array.from(document.querySelectorAll('body *')).filter(el => {
            const cs = getComputedStyle(el); if (cs.position !== 'fixed') return false;
            const b = el.getBoundingClientRect(); return b.bottom >= innerHeight - 2 && b.height > 20 && b.width > 100;
          }).map(el => ({cls: el.className.toString().slice(0,60), top: Math.round(el.getBoundingClientRect().top), h: Math.round(el.getBoundingClientRect().height)}));
          const t = document.getElementById('os-pts-toggle').getBoundingClientRect();
          return {fixed, toggleTop: Math.round(t.top), toggleBottom: Math.round(t.bottom)};
        }""")
        print(fname, r)
        pg.close()
    b.close()
httpd.shutdown()
