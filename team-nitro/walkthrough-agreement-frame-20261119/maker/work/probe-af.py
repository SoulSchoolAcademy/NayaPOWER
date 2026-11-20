#!/usr/bin/env python3
"""AGREEMENT-FRAME render verification (2026-11-19): the staged AF bytes
at 1920x999 and 390x844, VM Chromium via the h1 forwarder. Proves, on the
live staged bytes: 24 boards (was 47), no dots row, frame hugs edges
(corners + rims present), light inside (frameLightAF), Naya's photo
top-right, buttons in the foot at the bottom not blocking, first words
visible at load, seal on frames, Back on the final frame, agree never
clicked (#dealSeal stays hidden), deck view framed at both widths.
Screenshots land via the node stdin-writer (python file writes EPERM)."""
import json, subprocess
from playwright.sync_api import sync_playwright

OUT = "/home/hatch/workspace/team-nitro/walkthrough-agreement-frame-20261119/maker/work/proof/"
WRITER = "/home/hatch/workspace/team-nitro/walkthrough-agreement-frame-20261119/maker/work/writer9.js"
BASE = "https://naya-walk-beginning-staging.nayapower.workers.dev"

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
  const topbar = cb ? cb.querySelector('.frame-topbar') : null;
  const face = cb ? cb.querySelector('.frame-face') : null;
  const title = cb ? cb.querySelector('.frame-title') : null;
  const media = q('#fpMediaFrame');
  const paras = sc ? [...sc.querySelectorAll('p')] : [];
  const p0 = paras.find(p => !p.closest('#fpMediaFrame'));
  let p0vis = null;
  if (p0 && sc) {
    const pr = p0.getBoundingClientRect(), sr = sc.getBoundingClientRect();
    const top = Math.max(pr.top, sr.top), bot = Math.min(pr.bottom, sr.bottom);
    const lh = parseFloat(getComputedStyle(p0).lineHeight);
    p0vis = {visPx: Math.max(0, Math.round(bot - top)), visLines: Math.round(((Math.max(0, bot - top)) / lh) * 10) / 10};
  }
  const light = q('.frame-light');
  const corners = [...document.querySelectorAll('.af-corner')].map(r);
  const sealEl = cb ? cb.querySelector('.frame-red-n') : null;
  const stage = q('.p3-deal-unfold');
  return {
    afStyle: document.documentElement.getAttribute('data-af-style'),
    fpFrameAF: !!q('#fpFrameAF'), fpFrame9: !!q('#fpFrame9'),
    beatsTotal: beats.length, cur,
    title: title ? title.textContent : null,
    titleRect: r(title), faceRect: r(face),
    faceRightOfTitle: face && title ? (face.getBoundingClientRect().x > title.getBoundingClientRect().x) : null,
    faceSize: face ? Math.round(face.getBoundingClientRect().width) : null,
    stageRect: r(stage),
    scrollRect: r(sc), scrollH: sc ? sc.scrollHeight : null,
    scrollClientH: sc ? sc.clientHeight : null,
    footRect: r(foot), rowRect: r(row),
    footBottomVsViewport: foot ? Math.round(window.innerHeight - foot.getBoundingClientRect().bottom) : null,
    btns: row ? [...row.querySelectorAll('button')].map(x => ({t: x.textContent.trim(), hidden: x.hidden, disabled: x.disabled})) : null,
    media: media ? {rect: r(media)} : null,
    firstPara: p0 ? {text: p0.textContent.trim().slice(0,50), vis: p0vis} : null,
    dots: [...document.querySelectorAll('#deckDots .ldot')].length,
    dotsBox: !!q('#deckDots'),
    corners: corners.length, cornerRects: corners,
    lightAnim: light ? getComputedStyle(light).animationName : null,
    seal: sealEl ? {w: Math.round(sealEl.getBoundingClientRect().width), disp: getComputedStyle(sealEl).display} : null,
    sealCount: cb ? cb.querySelectorAll('.frame-red-n').length : 0,
    dealSeal: (() => { const s = q('#dealSeal'); return s ? {hidden: s.hidden, disp: getComputedStyle(s).display} : null; })(),
    audioEl: !!document.querySelector('audio'),
    pageHasMp3: document.documentElement.outerHTML.includes('agreement-naya-voice'),
    boardRect: cb ? r(cb) : null,
  };
}
"""

DECK_JS = r"""
() => {
  const q = (s) => document.querySelector(s);
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height), display: cs.display}; };
  const vis = [...document.querySelectorAll('#deckBody .letter-beat')].filter(b => b.offsetParent !== null);
  const first = vis[0];
  const show = first ? first.querySelector('.lb-showcase img') : null;
  return {
    deckOn: document.body.classList.contains('af-deck-on'),
    fpDeckAF: !!q('#fpDeckAF'),
    deckFrame: !!q('.af-deck-frame'),
    deckCorners: [...document.querySelectorAll('.af-deck-frame .af-corner')].length,
    deckLight: !!q('.af-deck-light'),
    dots: [...document.querySelectorAll('#deckDots .ldot')].length,
    visibleBeats: vis.length,
    firstTitle: first ? (first.querySelector('.ib-title')||{}).textContent : null,
    firstRect: r(first),
    showcaseRect: show ? r(show) : null,
    showcaseOrder: show ? getComputedStyle(show.closest('.lb-showcase')).order : null,
    stageOn: document.body.classList.contains('fp-stage-on'),
  };
}
"""


def show(label, obj):
    print("=== " + label + " ===")
    print(json.dumps(obj, indent=1))


def shot(pg, name):
    data = pg.screenshot()
    r = subprocess.run(["node", WRITER, OUT + name, "6"], input=data,
                       capture_output=True, timeout=60)
    print("shot %s: %d B rc=%d" % (name, len(data), r.returncode), flush=True)


with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"], proxy={"server": "http://127.0.0.1:18080"})
    # ---- DESKTOP 1920: unfold ----
    pg = b.new_page(viewport={"width": 1920, "height": 999})
    errs, failed = [], []
    pg.on("pageerror", lambda e: errs.append("PAGEERROR: " + str(e)[:200]))
    pg.on("response", lambda r: failed.append(str(r.status) + " " + r.url[:150]) if r.status >= 400 else None)
    pg.on("requestfailed", lambda r: failed.append(r.url[:150] + " :: " + str(r.failure)))
    pg.goto(BASE + "/agreement", wait_until="domcontentloaded", timeout=60000)
    pg.wait_for_timeout(2500)
    shot(pg, "af-f1-desktop.png")
    s = pg.evaluate(GEOM_JS); show("AF desktop frame1", s)
    print("AF-D1 boards=%s (need 24) dots=%s (need 0) corners=%s (need 4) light=%s (need frameLightAF) style=%s" % (
        s["beatsTotal"], s["dots"], s["corners"], s["lightAnim"], s["afStyle"]))
    print("AF-D1 faceRight=%s faceSize=%s firstParaVis=%s footGapBottom=%s btns=%s" % (
        s["faceRightOfTitle"], s["faceSize"], (s["firstPara"] or {}).get("vis"),
        s["footBottomVsViewport"], [x["t"] for x in (s["btns"] or [])]))
    # Walk to board 2 (Next) and board 24 (Keep reading x22), then final
    pg.click("#deckBody .letter-beat.frame-now .frame-btnrow .frame-next")
    pg.wait_for_timeout(400)
    s2 = pg.evaluate(GEOM_JS)
    print("AF-D2 board2: cur=%s title=%s sealCount=%s" % (s2["cur"], s2["title"], s2["sealCount"]))
    shot(pg, "af-f2-desktop.png")
    for _ in range(21):
        pg.click("#deckBody .letter-beat.frame-now .frame-btnrow .frame-next")
        pg.wait_for_timeout(150)
    s3 = pg.evaluate(GEOM_JS); show("AF desktop final board", s3)
    print("AF-D24 final: cur=%s btns=%s dealSeal=%s" % (s3["cur"], [x["t"] for x in (s3["btns"] or [])], s3["dealSeal"]))
    shot(pg, "af-final-desktop.png")
    pg.click("#deckBody .letter-beat.frame-now .frame-btnrow .deck-back")
    pg.wait_for_timeout(500)
    print("AF-D24 Back click: cur=%s (need 22)" % pg.evaluate(GEOM_JS)["cur"])
    print("AF-D pageerrors=%s failedReqs=%s" % (errs, [f for f in failed if "fonts.g" not in f][:5]))
    pg.close()
    # ---- DESKTOP 1920: deck (?stage=deck) ----
    pg = b.new_page(viewport={"width": 1920, "height": 999})
    pg.on("pageerror", lambda e: errs.append("DECK PAGEERROR: " + str(e)[:200]))
    pg.goto(BASE + "/?stage=deck", wait_until="domcontentloaded", timeout=60000)
    pg.wait_for_timeout(2500)
    d = pg.evaluate(DECK_JS); show("AF desktop deck", d)
    shot(pg, "af-deck-desktop.png")
    pg.close()
    # ---- MOBILE 390: unfold ----
    pg = b.new_page(viewport={"width": 390, "height": 844})
    pg.goto(BASE + "/agreement", wait_until="domcontentloaded", timeout=60000)
    pg.wait_for_timeout(2500)
    shot(pg, "af-f1-mobile.png")
    s = pg.evaluate(GEOM_JS); show("AF mobile frame1", s)
    print("AF-M1 boards=%s dots=%s corners=%s style=%s faceSize=%s firstParaVis=%s btns=%s" % (
        s["beatsTotal"], s["dots"], s["corners"], s["afStyle"], s["faceSize"],
        (s["firstPara"] or {}).get("vis"), [x["t"] for x in (s["btns"] or [])]))
    pg.click("#deckBody .letter-beat.frame-now .frame-btnrow .frame-next")
    pg.wait_for_timeout(400)
    shot(pg, "af-f2-mobile.png")
    print("AF-M2 board2 cur=%s title=%s" % (pg.evaluate(GEOM_JS)["cur"], pg.evaluate(GEOM_JS)["title"]))
    pg.close()
    # ---- MOBILE 390: deck ----
    pg = b.new_page(viewport={"width": 390, "height": 844})
    pg.goto(BASE + "/?stage=deck", wait_until="domcontentloaded", timeout=60000)
    pg.wait_for_timeout(2500)
    d = pg.evaluate(DECK_JS); show("AF mobile deck", d)
    shot(pg, "af-deck-mobile.png")
    pg.close()
    b.close()
print("PROBE DONE")
