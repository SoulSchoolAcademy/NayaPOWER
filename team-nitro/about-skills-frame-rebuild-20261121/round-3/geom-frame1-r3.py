# Frame-1 geometry probe — ROUND 3. Measures every vertical contributor inside
# frame 1's .frame-scroll at phone 390x844 on the round-2 build, so the
# spacing recovery can be computed exactly before any value changes.
import sys, json
from pathlib import Path
from playwright.sync_api import sync_playwright

DIR = Path(__file__).resolve().parent
R2 = DIR
FILE = 'file://' + str(DIR / 'about-skills.html')

GEOM_JS = """() => {
  const a = document.querySelector('article[data-beat="1"]');
  const sc = a.querySelector('.frame-scroll');
  const cs = getComputedStyle;
  const r = el => { if (!el) return null; const b = el.getBoundingClientRect();
    return {top: Math.round(b.top), bottom: Math.round(b.bottom), h: Math.round(b.height)}; };
  const media = document.getElementById('fpMediaFrame');
  const out = {scroller: {sh: sc.scrollHeight, ch: sc.clientHeight,
               bottom: Math.round(sc.getBoundingClientRect().bottom)},
    media: r(media),
    mediaKids: {},
    nut: r(a.querySelector('.ib-nutshell')),
    foot: r(a.querySelector('.ib-foot')),
    topbar: r(a.querySelector('.frame-topbar')),
    frameFoot: r(a.querySelector('.frame-foot')),
    styles: {}};
  if (media) for (const [k, sel] of [['title','.frame-media-title'],['audio','.frame-media-audio'],
      ['audioName','.frame-media-audio-name'],['audioState','.frame-media-audio-state'],
      ['playBtn','.play-btn'],['videoBtn','.frame-video-btn']]) {
    const el = media.querySelector(sel); if (!el) continue;
    out.mediaKids[k] = {...r(el), lines: el.getClientRects().length};
  }
  const grab = (el, props) => { if (!el) return null; const s = cs(el); const o = {};
    for (const p of props) o[p] = s.getPropertyValue(p); return o; };
  out.styles.media = grab(media, ['padding-top','padding-bottom','margin-bottom','border-top-width']);
  out.styles.title = grab(media && media.querySelector('.frame-media-title'), ['margin-bottom','line-height']);
  out.styles.audio = grab(media && media.querySelector('.frame-media-audio'), ['gap','height']);
  out.styles.audioState = grab(media && media.querySelector('.frame-media-audio-state'), ['margin-top','line-height']);
  out.styles.playBtn = grab(media && media.querySelector('.play-btn'), ['width','height']);
  out.styles.videoBtn = grab(media && media.querySelector('.frame-video-btn'), ['margin-top','padding-top','padding-bottom']);
  out.styles.nut = grab(a.querySelector('.ib-nutshell'), ['margin-top','margin-bottom','padding-top','padding-bottom']);
  out.styles.foot = grab(a.querySelector('.ib-foot'), ['margin-top','padding-top','border-top-width']);
  out.styles.scrollerKids = [...sc.children].map(c => c.className + ' ' + Math.round(c.getBoundingClientRect().height) + 'px');
  return out;
}"""

with sync_playwright() as p:
    browser = p.chromium.launch(args=['--no-sandbox', '--disable-gpu', '--force-device-scale-factor=1'],
                                proxy={'server': 'http://127.0.0.1:18080'})
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto(FILE, wait_until='load', timeout=60000)
    page.wait_for_timeout(1500)
    g = page.evaluate(GEOM_JS)
    print(json.dumps(g, indent=1))
    browser.close()
