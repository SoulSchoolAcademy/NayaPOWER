#!/usr/bin/env python3
"""FIX9 geometry probe (2026-11-19): measure the three gaps on the STAGED
fix-8 bytes before editing anything. Viewport 1920x999, VM Chromium via
the h1 forwarder. Navigation clicks only; no agree, no sign-in.
Measures: frame-1 reading window vs media board vs first paragraph
(F1); per-frame foot contents incl. seal (F7); final-frame row + dots
(F3). Screenshots to maker/work/proof/."""
import json, subprocess
from playwright.sync_api import sync_playwright

OUT = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix9-20261119/maker/work/proof/"
WRITER = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix9-20261119/maker/work/writer9.js"
BASE = "https://naya-walk-beginning-staging.nayapower.workers.dev"


def shot(pg, name):
    """Screenshot bytes stay in memory (python file writes EPERM in this
    window); the node stdin-writer lands them on disk, sha-verified."""
    data = pg.screenshot()
    r = subprocess.run(["node", WRITER, OUT + name, "6"], input=data,
                       capture_output=True, timeout=60)
    print("shot %s: %d B rc=%d %s" % (name, len(data), r.returncode,
          r.stderr.decode("utf-8", "replace").strip().splitlines()[-1] if r.stderr else ""), flush=True)

GEOM_JS = r"""
() => {
  const q = (s) => document.querySelector(s);
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height), display: cs.display}; };
  const beats = [...document.querySelectorAll('#deckBody .letter-beat')];
  const cur = beats.findIndex(b => b.classList.contains('frame-now'));
  const cb = beats[cur];
  const sc = cb ? cb.querySelector('.frame-scroll') : null;
  const foot = cb ? cb.querySelector('.frame-foot') : null;
  const row = cb ? cb.querySelector('.frame-btnrow') : null;
  const media = q('#fpMediaFrame');
  const kids = sc ? [...sc.children].map(el => ({tag: el.tagName, cls: (el.className||'').toString().slice(0,40),
    id: el.id || '', offTop: el.offsetTop, rect: r(el),
    text: (el.textContent||'').trim().slice(0,60)})) : null;
  // first paragraph element inside the scroll window (after the media board)
  const paras = sc ? [...sc.querySelectorAll('p')] : [];
  const p0 = paras.find(p => !p.closest('#fpMediaFrame'));
  const p0cs = p0 ? getComputedStyle(p0) : null;
  // how much of p0 is inside the scroll window's visible rect?
  let p0vis = null;
  if (p0 && sc) {
    const pr = p0.getBoundingClientRect(), sr = sc.getBoundingClientRect();
    const top = Math.max(pr.top, sr.top), bot = Math.min(pr.bottom, sr.bottom);
    p0vis = {linesTotal: Math.round(pr.height / parseFloat(p0cs.lineHeight)),
             visPx: Math.max(0, Math.round(bot - top)),
             visLines: Math.max(0, (bot - top) / parseFloat(p0cs.lineHeight))};
  }
  return {
    cur, beatsTotal: beats.length,
    title: cb ? (cb.querySelector('.frame-title')||{}).textContent : null,
    deckRect: r(q('#deckBody')),
    topbarRect: cb ? r(cb.querySelector('.frame-topbar')) : null,
    scrollRect: r(sc), scrollH: sc ? sc.scrollHeight : null, scrollTop: sc ? sc.scrollTop : null,
    scrollPadTop: sc ? getComputedStyle(sc).paddingTop : null,
    footRect: r(foot),
    seal: cb ? r(cb.querySelector('.frame-red-n')) : null,
    sealCount: cb ? cb.querySelectorAll('.frame-red-n').length : 0,
    btns: row ? [...row.querySelectorAll('button')].map(x => ({t: x.textContent.trim(), id: x.id||'',
      cls: (x.className||'').slice(0,40), hidden: x.hidden, disabled: x.disabled,
      disp: getComputedStyle(x).display, rect: r(x)})) : null,
    media: media ? {rect: r(media), marginBottom: getComputedStyle(media).marginBottom,
      title: r(media.querySelector('.frame-media-title')),
      audioRow: r(media.querySelector('.frame-media-audio')),
      orb: r(media.querySelector('.play-btn')),
      videoBtn: r(media.querySelector('#fpAnthemVideoBtn'))} : null,
    firstPara: p0 ? {offTop: p0.offsetTop, rect: r(p0), lineHeight: p0cs.lineHeight,
      fontSize: p0cs.fontSize, marginTop: p0cs.marginTop, marginBottom: p0cs.marginBottom,
      text: p0.textContent.trim().slice(0,80), vis: p0vis} : null,
    scKids: kids ? kids.slice(0, 8) : null,
    dealSeal: (() => { const s = q('#dealSeal'); return s ? {hidden: s.hidden, disp: getComputedStyle(s).display} : null; })(),
    dots: (() => { const d = [...document.querySelectorAll('#deckDots .ldot')];
      return {count: d.length, ariaHidden: (q('#deckDots')||{}).getAttribute ? q('#deckDots').getAttribute('aria-hidden') : null,
        firstRect: d[0] ? r(d[0]) : null, cursor: d[0] ? getComputedStyle(d[0]).cursor : null}; })(),
    deckControlsRect: r(q('#deckControls')),
    audioEl: !!document.querySelector('audio'),
    pageHasMp3: document.documentElement.outerHTML.includes('agreement-naya-voice'),
  };
}
"""

def show(label, obj):
    print("=== " + label + " ===")
    print(json.dumps(obj, indent=1))

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"], proxy={"server": "http://127.0.0.1:18080"})
    pg = b.new_page(viewport={"width": 1920, "height": 999})
    errs, failed = [], []
    pg.on("pageerror", lambda e: errs.append("PAGEERROR: " + str(e)[:200]))
    pg.on("response", lambda r: failed.append(str(r.status) + " " + r.url[:150]) if r.status >= 400 else None)
    pg.on("requestfailed", lambda r: failed.append(r.url[:150] + " :: " + str(r.failure)))

    pg.goto(BASE + "/agreement", wait_until="domcontentloaded", timeout=60000)
    pg.wait_for_timeout(2000)
    shot(pg, "fx9-base-f1.png")
    show("BASE frame1", pg.evaluate(GEOM_JS))

    # frame 2 (one Next) — foot contents without seal?
    pg.click("#deckBody .letter-beat.frame-now .frame-btnrow .frame-next")
    pg.wait_for_timeout(700)
    show("BASE frame2", pg.evaluate(GEOM_JS))
    shot(pg, "fx9-base-f2.png")

    # walk to the final frame (cur 46)
    for n in range(44):
        pg.click("#deckBody .letter-beat.frame-now .frame-btnrow .frame-next")
        pg.wait_for_timeout(120)
    pg.wait_for_timeout(700)
    show("BASE final frame", pg.evaluate(GEOM_JS))
    shot(pg, "fx9-base-final.png")
    # dots: click dot 23 (index 22) — display-only?
    pg.evaluate("() => { const d = document.querySelectorAll('#deckDots .ldot'); if (d[22]) d[22].click(); }")
    pg.wait_for_timeout(500)
    s = pg.evaluate(GEOM_JS)
    print("AFTER dot-23 click: cur=%s (46 = dots display-only)" % s["cur"])
    # Back from final via 'read the whole agreement at once' — the only way back today
    pg.click("#deckAll")
    pg.wait_for_timeout(500)
    print("AFTER read-it-all click: cur=%s" % pg.evaluate(GEOM_JS)["cur"])
    print("ERRORS:", errs or "(none)")
    print("FAILED REQ:", failed[:10] or "(none)")
    b.close()
print("GEOMETRY PROBE DONE")
