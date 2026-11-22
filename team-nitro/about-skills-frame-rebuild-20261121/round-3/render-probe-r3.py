# Render probe, ROUND 3 — About + Skills frame rebuild (15 frames).
# Loads the local built file in Chromium (via the localhost forwarding proxy so
# proof-host images can load), walks all 15 frames with the page's own Next
# buttons, measures each frame's .frame-scroll fit + frame bottom vs viewport,
# screenshots every frame. Usage: python3 render-probe-r2.py [phone|desktop]
import sys, json, time
from pathlib import Path
from playwright.sync_api import sync_playwright

DIR = Path(__file__).resolve().parent
FILE = 'file://' + str(DIR / 'about-skills.html')
MODE = sys.argv[1] if len(sys.argv) > 1 else 'phone'
VP = {'width': 1920, 'height': 999} if MODE == 'desktop' else {'width': 390, 'height': 844}

MEASURE_JS = """() => {
  const arts = [...document.querySelectorAll('article[data-beat]')];
  const vis = arts.find(a => a.offsetParent !== null && getComputedStyle(a).display !== 'none');
  if (!vis) return {visible: null};
  const sc = vis.querySelector('.frame-scroll');
  const r = vis.getBoundingClientRect();
  const kind = (vis.querySelector('.ib-kind') || {}).textContent || '';
  const title = (vis.querySelector('.ib-title') || {}).textContent || '';
  const nut = vis.querySelector('.ib-nutshell');
  const nutR = nut ? nut.getBoundingClientRect() : null;
  const nextBtn = [...vis.querySelectorAll('.deck-next')].find(b => !b.hidden && getComputedStyle(b).display !== 'none');
  const nbR = nextBtn ? nextBtn.getBoundingClientRect() : null;
  const foot = vis.querySelector('.ib-foot');
  const footR = foot ? foot.getBoundingClientRect() : null;
  const frame = document.querySelector('.naya-frame');
  const fr = frame ? frame.getBoundingClientRect() : null;
  // what sits at the centre of the next button — is the frame overlay covering it?
  let coverAtBtn = null;
  if (nbR) { const el = document.elementFromPoint(nbR.left + nbR.width/2, nbR.top + nbR.height/2); coverAtBtn = el ? (el.className && el.className.toString().slice(0,40)) : null; }
  return {
    visible: vis.getAttribute('data-beat'),
    kind: kind.trim(), title: title.trim().slice(0, 48),
    frameTop: Math.round(r.top), frameH: Math.round(r.height), frameBottom: Math.round(r.bottom),
    vw: window.innerWidth, vh: window.innerHeight,
    nutBottom: nutR ? Math.round(nutR.bottom) : null,
    footBottom: footR ? Math.round(footR.bottom) : null,
    nextBtn: nbR ? {top: Math.round(nbR.top), bottom: Math.round(nbR.bottom), cover: coverAtBtn} : null,
    frameOverlay: fr ? {top: Math.round(fr.top), bottom: Math.round(fr.bottom)} : null,
    scroll: sc ? {sh: sc.scrollHeight, ch: sc.clientHeight, sw: sc.scrollWidth, cw: sc.clientWidth,
                  vOverflow: sc.scrollHeight - sc.clientHeight, hOverflow: sc.scrollWidth - sc.clientWidth} : null,
    pill: (document.querySelector('.af-prog-num') || {}).textContent ? document.querySelector('.af-prog-num').textContent.trim() : null,
  };
}"""

CLICK_NEXT_JS = """() => {
  const arts = [...document.querySelectorAll('article[data-beat]')];
  const vis = arts.find(a => a.offsetParent !== null && getComputedStyle(a).display !== 'none');
  if (!vis) return false;
  const btns = [...vis.querySelectorAll('.deck-next')].filter(b => !b.hidden && getComputedStyle(b).display !== 'none');
  const fwd = btns.find(b => /Keep reading|See my skills/.test(b.textContent)) || btns.find(b => /^\\s*Next/.test(b.textContent));
  if (fwd) { fwd.click(); return true; } return false;
}"""

FONTS_JS = """() => {
  const c = document.createElement('canvas').getContext('2d');
  c.font = '25px Marcellus'; const wM = c.measureText('About Sean').width;
  c.font = '25px serif'; const wS = c.measureText('About Sean').width;
  return {marcellusLoaded: document.fonts.check('25px Marcellus'),
          outfitLoaded: document.fonts.check('16px Outfit'),
          wMarcellus: Math.round(wM*10)/10, wSerif: Math.round(wS*10)/10,
          pill: (document.querySelector('.af-prog-num') || {}).textContent || null,
          articles: document.querySelectorAll('article[data-beat]').length,
          errors: window.__errs || 0};
}"""

with sync_playwright() as p:
    browser = p.chromium.launch(args=['--no-sandbox', '--disable-gpu', '--force-device-scale-factor=1'],
                                proxy={'server': 'http://127.0.0.1:18080'})
    page = browser.new_page(viewport=VP)
    errs = []
    page.on('pageerror', lambda e: errs.append(str(e)[:200]))
    page.on('console', lambda m: errs.append(m.text[:200]) if m.type == 'error' else None)
    page.goto(FILE, wait_until='load', timeout=60000)
    page.wait_for_timeout(1500)
    print('FONTS:', page.evaluate(FONTS_JS))
    results = []
    for pos in range(1, 16):
        m = page.evaluate(MEASURE_JS)
        results.append((pos, m))
        page.screenshot(path=str(DIR / f'r3-shot-{MODE}-{pos:02d}.png'))
        if pos < 15:
            if not page.evaluate(CLICK_NEXT_JS):
                print(f'frame {pos}: NO NEXT BUTTON — stopped'); break
            page.wait_for_timeout(450)
    for pos, r in results:
        s = r.get('scroll')
        if s:
            print(f"pos {pos:2d} beat={r['visible']} pill={r['pill']!r} kind={r['kind']!r} "
                  f"vOver={s['vOverflow']} hOver={s['hOverflow']} (sh {s['sh']}/ch {s['ch']}) "
                  f"frameBottom={r['frameBottom']}/{r['vh']} nutBottom={r['nutBottom']} footBottom={r['footBottom']} next={r['nextBtn']}")
        else:
            print(f"pos {pos:2d} beat={r['visible']} NO .frame-scroll")
    bad = [pos for pos, r in results if r.get('scroll') and (r['scroll']['vOverflow'] > 0 or r['scroll']['hOverflow'] > 0)]
    print('OVERFLOWING FRAMES:', ','.join(map(str, bad)) if bad else 'none')
    print('PAGEERRORS:', errs if errs else 'none')
    json.dump(results, open(str(DIR / f'r3-measure-{MODE}.json'), 'w'), indent=1)
    browser.close()
