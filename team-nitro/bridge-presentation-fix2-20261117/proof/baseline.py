#!/usr/bin/env python3
"""Baseline live geometry probe on the STAGED worker (presentation bytes).
Loads ?stage=bridge at 1920/635/390, dumps rects for D3/D4 + pageerrors.
Usage: python3 baseline.py [width]  (default all three)"""
import json, sys, time
from playwright.sync_api import sync_playwright

BASE = "https://naya-walk-beginning-staging.nayapower.workers.dev"
WIDTHS = [int(x) for x in sys.argv[1:]] or [1920, 635, 390]

JS = r"""
() => {
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect();
    return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height),
            right: Math.round(b.right), bottom: Math.round(b.bottom)}; };
  const q = (s) => document.querySelector(s);
  const qa = (s) => Array.from(document.querySelectorAll(s));
  const cs = (el, p) => el ? getComputedStyle(el)[p] : null;
  const head = q('.fp-agree-head');
  return {
    view: (document.querySelector('#fpAgreement')||{}).className,
    bodyClass: document.body.className,
    head: r(head),
    headPos: head ? cs(head, 'position') : null,
    kicker: r(q('.fp-agree-kicker')),
    title: r(q('.fp-agree-title')),
    sub: r(q('.fp-agree-sub')),
    logo: r(q('.fp-agree-logo')),
    corners: r(q('.fp-bridge-corners')),
    emblems: qa('.fp-bridge-emblem').map(e => ({cls: e.className, rect: r(e), disp: cs(e,'display')})),
    legal: r(q('#fpLegal')),
    legalLinks: r(q('#fpLegal .fp-legal-links')),
    legalDisp: q('#fpLegal') ? cs(q('#fpLegal'), 'position') + '/' + cs(q('#fpLegal'), 'display') : null,
    barB: r(q('#fpStageBarB')),
    barBBottom: q('#fpStageBarB') ? cs(q('#fpStageBarB'), 'bottom') : null,
    barT: r(q('#fpStageBarT')),
    bridge: r(q('#fpBridge')),
    agreePadBottom: q('#fpAgreement') ? cs(q('#fpAgreement'), 'paddingBottom') : null,
    continues: qa('#fpBridge .fp-bridge-more').map(e => ({id: e.id, hidden: e.hidden, rect: r(e)})),
    vw: innerWidth, vh: innerHeight,
    errors: (window.__errs || [])
  };
}
"""

with sync_playwright() as p:
    b = p.chromium.launch(proxy={"server": "http://127.0.0.1:18080"}, args=["--no-sandbox"])
    for w in WIDTHS:
        pg = b.new_page(viewport={"width": w, "height": 900})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.evaluate("window.__errs = []; window.addEventListener('error', e => window.__errs.push(String(e.message)))")
        pg.goto(BASE + "/?stage=bridge", wait_until="load", timeout=60000)
        pg.wait_for_timeout(6000)
        pg.evaluate("window.__errs = window.__errs || []")
        d = pg.evaluate(JS)
        d["pageerrors"] = errs
        print("===== WIDTH %d =====" % w)
        print(json.dumps(d, indent=1))
        pg.screenshot(path="/tmp/fix2/base-%d-bridge-top.png" % w)
        pg.close()
    b.close()
