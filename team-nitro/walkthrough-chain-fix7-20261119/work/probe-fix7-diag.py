#!/usr/bin/env python3
"""FIX7 diagnosis probe — staged /agreement + / at 390x844 and 1920x999.
Measures load scroll position, scrollability, button visibility/hit-test,
and the Keep-reading advance. Screenshots + JSON to evidence/."""
import json, os, sys
from playwright.sync_api import sync_playwright

STAGING = "https://naya-walk-beginning-staging.nayapower.workers.dev"
OUT = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix7-20261119/evidence"
os.makedirs(OUT, exist_ok=True)

MEASURE = r"""
() => {
  const q = s => document.querySelector(s);
  const r = el => { if (!el) return null; const b = el.getBoundingClientRect();
    return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width),
            h: Math.round(b.height), top: Math.round(b.top), bottom: Math.round(b.bottom)}; };
  const vis = el => { if (!el) return false; const b = el.getBoundingClientRect();
    return b.bottom > 0 && b.top < innerHeight && b.width > 0 && b.height > 0; };
  const beat1 = q('#deckBody .letter-beat[data-beat="1"]');
  const kr1 = beat1 ? beat1.querySelector('.deck-next[data-beat="1"]') : null;
  const cs = getComputedStyle(document.documentElement);
  const bcs = getComputedStyle(document.body);
  const db = q('#deckBody');
  return {
    url: location.href, scrollY: Math.round(scrollY),
    scrollH: document.scrollingElement.scrollHeight, innerH: innerHeight, innerW: innerWidth,
    docH: document.documentElement.scrollHeight,
    htmlOverflow: cs.overflow + '/' + cs.overflowY, bodyOverflow: bcs.overflow + '/' + bcs.overflowY,
    deckSnap: db ? getComputedStyle(db).scrollSnapType : null,
    title: r(q('.deal-title')), playBtn: r(q('#playBtn')),
    beat1: r(beat1), beat1Hidden: beat1 ? beat1.hidden : null,
    beat1Nutshell: r(beat1 ? beat1.querySelector('.ib-nutshell') : null),
    kr1: r(kr1), kr1Visible: vis(kr1),
    kr1Hit: (() => { if (!kr1) return null; const b = kr1.getBoundingClientRect();
      const el = document.elementFromPoint(b.x + b.width/2, Math.min(b.y + b.height/2, innerHeight - 2));
      return el ? (el.tagName + '.' + (el.className.baseVal !== undefined ? '' : String(el.className)).slice(0,40)) : null; })(),
    beatsVisible: [...document.querySelectorAll('#deckBody .letter-beat')].filter(b => !b.hidden).length,
    beatsTotal: document.querySelectorAll('#deckBody .letter-beat').length,
    controls: r(q('#deckControls')), footLinks: r(q('.foot-links')),
    endCard: r(q('#dealAgreeBtn')),
  };
}
"""


def probe(pw, width, height, tag):
    b = pw.chromium.launch(headless=True, proxy={"server": "http://127.0.0.1:18080"})
    ctx = b.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
    pg = ctx.new_page()
    out = {"tag": tag, "viewport": [width, height]}
    try:
        pg.goto(STAGING + "/agreement", wait_until="load", timeout=60000)
        pg.wait_for_timeout(4000)
        out["load"] = pg.evaluate(MEASURE)
        pg.screenshot(path=f"{OUT}/fix7-diag-{tag}-load.png")
        # try to scroll the page by script
        pg.evaluate("window.scrollTo(0, 500)")
        pg.wait_for_timeout(1200)
        out["afterScrollTo500"] = {"scrollY": pg.evaluate("Math.round(scrollY)")}
        pg.evaluate("window.scrollTo(0, document.scrollingElement.scrollHeight)")
        pg.wait_for_timeout(1200)
        out["afterScrollToBottom"] = {"scrollY": pg.evaluate("Math.round(scrollY)")}
        pg.screenshot(path=f"{OUT}/fix7-diag-{tag}-bottom.png")
        # back to top, click Keep reading on beat 1
        pg.evaluate("window.scrollTo(0,0)")
        pg.wait_for_timeout(800)
        kr = pg.query_selector('#deckBody .letter-beat[data-beat="1"] .deck-next[data-beat="1"]')
        if kr:
            kr.click()
            pg.wait_for_timeout(2500)
            out["afterKeepReading"] = pg.evaluate(MEASURE)
            pg.screenshot(path=f"{OUT}/fix7-diag-{tag}-after-kr.png")
        else:
            out["afterKeepReading"] = "NO Keep-reading button found on beat 1"
        # welcome root: what does the front door show?
        pg.goto(STAGING + "/", wait_until="load", timeout=60000)
        pg.wait_for_timeout(3000)
        out["welcome"] = pg.evaluate(r"""() => ({
            scrollY: Math.round(scrollY), scrollH: document.scrollingElement.scrollHeight,
            innerH: innerHeight, title: document.title,
            bodyTextStart: document.body.innerText.slice(0, 400) })""")
        pg.screenshot(path=f"{OUT}/fix7-diag-{tag}-welcome.png")
    except Exception as e:
        out["error"] = repr(e)
    finally:
        ctx.close(); b.close()
    return out


def main():
    with sync_playwright() as pw:
        results = []
        results.append(probe(pw, 390, 844, "390"))
        results.append(probe(pw, 1920, 999, "1920"))
    with open(f"{OUT}/fix7-diag.json", "w") as f:
        json.dump(results, f, indent=1)
    print(json.dumps(results, indent=1)[:6000])


if __name__ == "__main__":
    main()
