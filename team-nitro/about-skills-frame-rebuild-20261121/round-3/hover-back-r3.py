# Hover + Back probe — ROUND 3. Hover every changed object (frame-1 media
# board + its buttons, the nutshell, the foot buttons) and confirm the lift;
# then tap Back and confirm the pill steps back. Chromium via proxy.
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

DIR = Path(__file__).resolve().parent
FILE = 'file://' + str(DIR / 'about-skills.html')

HOVER_JS = """(sel) => {
  const el = document.querySelector(sel);
  if (!el) return null;
  const b = el.getBoundingClientRect();
  return {cls: el.className.toString().slice(0,60),
          transform: getComputedStyle(el).transform,
          opacity: getComputedStyle(el).opacity,
          boxShadow: (getComputedStyle(el).boxShadow || '').slice(0,80)};
}"""

with sync_playwright() as p:
    browser = p.chromium.launch(args=['--no-sandbox', '--disable-gpu', '--force-device-scale-factor=1'],
                                proxy={'server': 'http://127.0.0.1:18080'})
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto(FILE, wait_until='load', timeout=60000)
    page.wait_for_timeout(1500)
    targets = [
        ('media board', '#fpMediaFrame'),
        ('media play orb', '#fpMediaFrame .play-btn'),
        ('media video btn', '#fpAnthemVideoBtn'),
        ('nutshell', 'article[data-beat="1"] .ib-nutshell'),
        ('Keep reading', 'article[data-beat="1"] .letter-next'),
    ]
    for name, sel in targets:
        before = page.evaluate(HOVER_JS, sel)
        el = page.query_selector(sel)
        box = el.bounding_box()
        page.mouse.move(box['x'] + box['width']/2, box['y'] + box['height']/2)
        page.wait_for_timeout(500)
        after = page.evaluate(HOVER_JS, sel)
        print(f"{name}: before transform={before['transform']} opacity={before['opacity']} | after transform={after['transform']} opacity={after['opacity']} | moved={before['transform'] != after['transform'] or before['opacity'] != after['opacity']}")
        page.mouse.move(195, 20)
        page.wait_for_timeout(300)
    # Back navigation: forward twice, back once
    page.evaluate("""() => { [...document.querySelectorAll('article[data-beat="1"] .deck-next')].find(b => /Keep reading/.test(b.textContent)).click(); }""")
    page.wait_for_timeout(450)
    page.evaluate("""() => { [...document.querySelectorAll('article[data-beat="2"] .deck-next')].find(b => /Keep reading/.test(b.textContent)).click(); }""")
    page.wait_for_timeout(450)
    pill3 = page.query_selector('.af-prog-num').text_content()
    page.evaluate("""() => { [...document.querySelectorAll('article[data-beat="3"] .deck-back')][0].click(); }""")
    page.wait_for_timeout(450)
    pill2 = page.query_selector('.af-prog-num').text_content()
    vis = page.evaluate("""() => { const a=[...document.querySelectorAll('article[data-beat]')].find(x=>x.offsetParent!==null); return a ? a.getAttribute('data-beat') : null; }""")
    print('pill after 2x fwd:', repr(pill3), '| pill after Back:', repr(pill2), '| visible beat:', vis)
    browser.close()
