# Render probe, CLONE ROUND 2 — About + Skills (live-agreement clone).
# Loads the local built file in Chromium (via the localhost forwarding proxy),
# walks cover -> 15 slides -> 10 legal deals / 15 frames with the page's own
# buttons, measures overflow + visibility, screenshots each screen.
# Usage: python3 render-probe-clone2.py [phone|desktop]
import sys, json
from pathlib import Path
from playwright.sync_api import sync_playwright

DIR = Path(__file__).resolve().parent
BUILT = Path('/home/hatch/workspace/nayapower-about-clone2/team-nitro/about-skills-frame-rebuild-20261121/about-skills.html')
FILE = 'file://' + str(BUILT)
MODE = sys.argv[1] if len(sys.argv) > 1 else 'phone'
VP = {'width': 1920, 'height': 999} if MODE == 'desktop' else {'width': 390, 'height': 844}

STATE_JS = """() => {
  const active = [...document.querySelectorAll('section.screen')].find(s => s.classList.contains('active'));
  const q = (sel) => document.querySelector(sel);
  const vis = (el) => el && el.offsetParent !== null;
  const slide = {
    station: (q('#slideStation') || {}).textContent || null,
    boardScript: (q('#slideBoards .b-script') || {}).textContent || null,
    boardText: (q('#slideBoards p') || {}).textContent || null,
    imgOk: (() => { const im = q('#slideImg'); return im ? (im.naturalWidth > 0) : null; })(),
  };
  const legal = (() => {
    const panel = [...document.querySelectorAll('.fp-legal-page')].find(p => !p.hidden);
    if (!panel) return null;
    const beats = [...panel.querySelectorAll('[data-legal-beat]')];
    const shown = beats.filter(b => !b.hidden);
    return { deal: panel.id, title: (panel.querySelector('.deal-title') || {}).textContent,
      beats: beats.length, shown: shown.length,
      shownTitles: shown.map(b => (b.querySelector('.ib-title') || {}).textContent),
      dots: panel.querySelectorAll('.ldot').length,
      nextVisible: (() => { const n = panel.querySelector('[data-legal-next]'); return n ? !n.hidden : null; })() };
  })();
  return {
    activeScreen: active ? active.id : null,
    title: document.title,
    tbTitle: (q('#tbTitle') || {}).textContent || null,
    ticker: (q('#tickA') || {}).textContent || null,
    deckStatus: (q('#deckStatus') || {}).textContent || null,
    startVisible: vis(q('#btnStart')),
    hOverflow: document.documentElement.scrollWidth - window.innerWidth,
    vOverflow: document.documentElement.scrollHeight - window.innerHeight,
    errors: window.__errs || 0,
    slide, legal,
  };
}"""

with sync_playwright() as p:
    browser = p.chromium.launch(args=['--no-sandbox', '--disable-gpu', '--force-device-scale-factor=1'],
                                proxy={'server': 'http://127.0.0.1:18080'})
    page = browser.new_page(viewport=VP)
    errs = []
    page.on('pageerror', lambda e: errs.append('PAGEERROR: ' + str(e)[:200]))
    page.on('console', lambda m: errs.append('CONSOLE-ERROR: ' + m.text[:200]) if m.type == 'error' else None)
    page.goto(FILE, wait_until='load', timeout=90000)
    page.wait_for_timeout(1500)
    out = []
    st = page.evaluate(STATE_JS)
    out.append(('cover', st))
    print('COVER:', json.dumps(st))
    page.screenshot(path=str(DIR / f'c2-shot-{MODE}-cover.png'))
    # cover -> slide 0
    page.click('#btnStart')
    page.wait_for_timeout(600)
    for i in range(15):
        st = page.evaluate(STATE_JS)
        out.append((f'slide-{i+1}', st))
        print(f"SLIDE {i+1}: station={st['slide']['station']!r} imgOk={st['slide']['imgOk']} hOver={st['hOverflow']} board={str(st['slide']['boardScript'])[:40]!r}")
        page.screenshot(path=str(DIR / f'c2-shot-{MODE}-slide-{i+1:02d}.png'))
        if i < 14:
            page.click('#btnForward')
            page.wait_for_timeout(450)
    # last slide forward -> where?
    page.click('#btnForward')
    page.wait_for_timeout(600)
    st = page.evaluate(STATE_JS)
    out.append(('after-last-slide', st))
    print('AFTER LAST SLIDE FORWARD:', json.dumps(st))
    page.screenshot(path=str(DIR / f'c2-shot-{MODE}-after-last.png'))
    # legal: walk the 10 deals via the footer buttons
    links = page.query_selector_all('.fp-legal-link')
    print('footer links:', len(links))
    for li, link in enumerate(links):
        link.click()
        page.wait_for_timeout(500)
        st = page.evaluate(STATE_JS)
        lg = st['legal']
        print(f"DEAL {li+1}: {lg['deal']} title={lg['title']!r} beats={lg['beats']} shown={lg['shown']} dots={lg['dots']} shownTitles={lg['shownTitles']}")
        page.screenshot(path=str(DIR / f'c2-shot-{MODE}-deal-{li+1:02d}.png'))
        # walk beats with Keep reading
        steps = 0
        while steps < 5:
            nxt = page.query_selector('.fp-legal-page:not([hidden]) [data-legal-next]')
            if not nxt or not nxt.is_visible():
                break
            nxt.click()
            page.wait_for_timeout(400)
            steps += 1
            st2 = page.evaluate(STATE_JS)
            print(f"   +next {steps}: shown={st2['legal']['shown']} titles={st2['legal']['shownTitles']}")
        out.append((f'deal-{li+1}', st))
    print('ERRORS:', errs if errs else 'none')
    json.dump(out, open(str(DIR / f'c2-measure-{MODE}.json'), 'w'), indent=1)
    browser.close()
