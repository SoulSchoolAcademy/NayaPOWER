#!/usr/bin/env python3
"""FIX8 follow-up probe: exact rects on /agreement frame 1 + what the
first Next click actually does (phase? advance? nothing?). Compact output."""
import json
from playwright.sync_api import sync_playwright

OUT = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix8-20261119/work/"
BASE = "https://naya-walk-beginning-staging.nayapower.workers.dev"
JS = r"""
() => {
  const q = (s) => document.querySelector(s);
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect();
    return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height)}; };
  const beats = [...document.querySelectorAll('#deckBody .letter-beat')];
  const cur = beats.findIndex(b => b.classList.contains('frame-now'));
  const cb = beats[cur];
  const sc = cb ? cb.querySelector('.frame-scroll') : null;
  const foot = cb ? cb.querySelector('.frame-foot') : null;
  const row = cb ? cb.querySelector('.frame-btnrow') : null;
  const showcase = cb ? cb.querySelector('.lb-showcase') : null;
  return {
    cur, vh: window.innerHeight,
    main: r(q('main.p3-deal-unfold')),
    deck: r(q('#deckBody')),
    beat: cb ? r(cb) : null,
    beatCls: cb ? cb.className : null,
    topbar: cb ? r(cb.querySelector('.frame-topbar')) : null,
    scroll: r(sc), scrollH: sc ? sc.scrollHeight : null, scrollTop: sc ? sc.scrollTop : null,
    media: r(q('#fpMediaFrame')),
    foot: r(foot), seal: cb ? r(cb.querySelector('.frame-red-n')) : null,
    row: r(row),
    btns: row ? [...row.querySelectorAll('button')].map(x => ({t: x.textContent.trim(), ...r(x)})) : null,
    showcase: showcase ? {cls: showcase.className, ...r(showcase)} : null,
    dots: r(q('#deckControls')), footLinks: r(q('.foot-links')),
    frame: r(q('.naya-frame')),
  };
}
"""
with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"], proxy={"server": "http://127.0.0.1:18080"})
    pg = b.new_page(viewport={"width": 1920, "height": 999})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:150]))
    pg.goto(BASE + "/agreement", wait_until="domcontentloaded", timeout=60000)
    pg.wait_for_timeout(2500)
    print("T0 " + json.dumps(pg.evaluate(JS)))
    pg.click("#deckBody .letter-beat.frame-now .frame-btnrow .frame-next")
    pg.wait_for_timeout(700)
    print("N1 " + json.dumps(pg.evaluate(JS)))
    pg.screenshot(path=OUT + "verify-after-next1.png")
    pg.click("#deckBody .letter-beat.frame-now .frame-btnrow .frame-next")
    pg.wait_for_timeout(700)
    print("N2 " + json.dumps(pg.evaluate(JS)))
    print("ERRORS:", errs or "(none)")
    b.close()
print("FOLLOWUP DONE")
