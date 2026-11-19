#!/usr/bin/env python3
"""FIX8 probe 2: staged / (welcome home) at 1920x999 — where are the
entrance + nav, where does the page sit, what hides them. Screenshots
+ rects. No sign-in, no clicks that submit."""
import json
from playwright.sync_api import sync_playwright

OUT = "/home/hatch/workspace/team-nitro/walkthrough-chain-fix8-20261119/work/"
URL = "https://naya-walk-beginning-staging.nayapower.workers.dev/"
JS = r"""
() => {
  const q = (s) => document.querySelector(s);
  const r = (el) => { if (!el) return null; const b = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    return {x: Math.round(b.x), y: Math.round(b.y), w: Math.round(b.width), h: Math.round(b.height), display: cs.display, opacity: cs.opacity, vis: cs.visibility}; };
  const nav = q('nav.eco-inline');
  const dots = [...document.querySelectorAll('nav.eco-inline a')].map(a => ({t: a.getAttribute('title'), rect: r(a)}));
  return {
    scrollY: Math.round(window.scrollY), docH: document.documentElement.scrollHeight, innerH: window.innerHeight,
    hash: location.hash, href: location.href,
    nav: r(nav), navDots: dots.slice(0, 3), navCount: dots.length,
    stage: r(q('section.stage')), portal: r(q('.portal')), content: r(q('.content')),
    presence: r(q('#presence')), enterBtn: r(q('button.enter')),
    returning: r(q('#returningView')), jumpBackIn: r(q('#jumpBackIn')),
    agreement: r(q('#fpAgreement')), agreeTitle: (() => { const e = q('.fp-agree-title'); return e ? e.textContent.trim().slice(0, 80) : null; })(),
    loginLink: (() => { const els = [...document.querySelectorAll('a,button')].filter(e => /login/i.test(e.textContent || '')); return els.slice(0,3).map(e => ({t: (e.textContent||'').trim().slice(0,30), rect: r(e)})); })(),
    bodyOverflow: getComputedStyle(document.body).overflow,
    ls: (() => { try { return {stage: localStorage.getItem('nayanet_fp_stage'), agreed: localStorage.getItem('nayanet_fp_agreed')}; } catch(e) { return 'n/a'; } })(),
  };
}
"""

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox", "--disable-gpu"], proxy={"server": "http://127.0.0.1:18080"})
    pg = b.new_page(viewport={"width": 1920, "height": 999})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)[:200]))
    pg.goto(URL, wait_until="domcontentloaded", timeout=60000)
    pg.wait_for_timeout(2500)
    pg.screenshot(path=OUT + "probe-home-t2.png")
    print("=== HOME t+2.5s ==="); print(json.dumps(pg.evaluate(JS), indent=1))
    pg.wait_for_timeout(4000)
    pg.screenshot(path=OUT + "probe-home-t6.png")
    print("=== HOME t+6.5s ==="); print(json.dumps(pg.evaluate(JS), indent=1))
    print("ERRORS:", errs or "(none)")
    b.close()
