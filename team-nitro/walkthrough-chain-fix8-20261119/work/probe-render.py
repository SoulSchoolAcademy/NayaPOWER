#!/usr/bin/env python3
"""FIX8 render probe (python playwright): staged /agreement at 1920x999
via the h1 forwarder proxy. Screenshots at 1.5/5.5/9.5s + live DOM state.
No sign-in, no submit/agree — navigation clicks only."""
import json, sys
from playwright.sync_api import sync_playwright

OUT = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix8-20261119/work/"
URL = "https://naya-walk-beginning-staging.nayapower.workers.dev/agreement"
STATE_JS = r"""
() => {
  const q = (s) => document.querySelector(s);
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height), display: cs.display, opacity: cs.opacity}; };
  const beats = [...document.querySelectorAll('#deckBody .letter-beat')];
  const cur = beats.findIndex(b => b.classList.contains('frame-now'));
  const curBeat = beats[cur];
  const rows = beats.slice(0, 4).map((b, i) => {
    const row = b.querySelector('.frame-btnrow');
    const btns = row ? [...row.querySelectorAll('button')].map(x => ({t: x.textContent.trim(), hidden: x.hidden, disp: getComputedStyle(x).display})) : null;
    const foot = b.querySelector('.frame-foot');
    const seal = b.querySelector('.frame-red-n');
    return {i, btns, footRect: r(foot), seal: seal ? r(seal) : null};
  });
  const topbar = curBeat ? curBeat.querySelector('.frame-topbar') : null;
  const face = curBeat ? curBeat.querySelector('.frame-face') : null;
  const sc = curBeat ? curBeat.querySelector('.frame-scroll') : null;
  const main = q('main.p3-deal-unfold');
  const cs = main ? getComputedStyle(main) : null;
  return {
    title: document.title,
    mainRect: r(main), mainPad: cs ? {t: cs.paddingTop, b: cs.paddingBottom, l: cs.paddingLeft, r: cs.paddingRight} : null,
    deckBodyRect: r(q('#deckBody')),
    frameLayer: r(q('.naya-frame')),
    cur, beatsTotal: beats.length,
    topbarRect: r(topbar),
    face: face ? {src: face.src.slice(0, 130), complete: face.complete, nw: face.naturalWidth} : null,
    scrollRect: r(sc), scrollH: sc ? sc.scrollHeight : null,
    firstPara: curBeat ? (curBeat.querySelector('.ib-nutshell p') || {}).textContent : null,
    rows,
    playBtn: (() => { const p = q('#playBtn'); return p ? {rect: r(p), hidden: p.hidden} : null; })(),
    playTip: (() => { const p = q('#playTip'); return p ? p.textContent : null; })(),
    dots: (() => { const d = q('#deckControls'); return d ? r(d) : null; })(),
    footLinks: (() => { const f = q('.foot-links'); return f ? r(f) : null; })(),
    headerRects: {steplabel: r(q('.letter-steplabel')), h1: r(q('.deal-title')), sub: r(q('.deck-sub')), playWrap: r(q('.play-wrap')), playNote: r(q('.play-note'))},
    scrollY: window.scrollY, docH: document.documentElement.scrollHeight, innerH: window.innerHeight,
  };
}
"""

def main():
    errors, failed = [], []
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"],
                              proxy={"server": "http://127.0.0.1:18080"})
        pg = b.new_page(viewport={"width": 1920, "height": 999})
        pg.on("pageerror", lambda e: errors.append("PAGEERROR: " + str(e)[:200]))
        pg.on("console", lambda m: errors.append("CONSOLE: " + m.text[:200]) if m.type == "error" else None)
        pg.on("requestfailed", lambda r: failed.append(r.url[:160] + " :: " + str(r.failure)))
        pg.on("response", lambda r: failed.append(str(r.status) + " " + r.url[:160]) if r.status >= 400 else None)
        pg.goto(URL, wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_timeout(1500)
        pg.screenshot(path=OUT + "probe-agree-t1.png")
        print("=== STATE t+1.5s ==="); print(json.dumps(pg.evaluate(STATE_JS), indent=1))
        pg.wait_for_timeout(4000)
        pg.screenshot(path=OUT + "probe-agree-t5.png")
        print("=== STATE t+5.5s ==="); print(json.dumps(pg.evaluate(STATE_JS), indent=1))
        pg.wait_for_timeout(4000)
        pg.screenshot(path=OUT + "probe-agree-t9.png")
        print("=== STATE t+9.5s ==="); print(json.dumps(pg.evaluate(STATE_JS), indent=1))
        print("=== ERRORS ==="); print("\n".join(errors) or "(none)")
        print("=== FAILED REQUESTS (first 25) ==="); print("\n".join(failed[:25]) or "(none)")
        b.close()

if __name__ == "__main__":
    main()
