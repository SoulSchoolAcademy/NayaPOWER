#!/usr/bin/env python3
"""Measure the 'NayaNET - The Deck' caption vs the sign photo on deck board 37."""
import json
from playwright.sync_api import sync_playwright
BASE = "https://naya-walk-beginning-staging.nayapower.workers.dev"
JS = """() => {
  const R = el => { if (!el) return null; const r = el.getBoundingClientRect();
    return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
  const ov = (a,b) => { if (!a||!b) return 0; const x=Math.max(0,Math.min(a[2],b[2])-Math.max(a[0],b[0])); const y=Math.max(0,Math.min(a[3],b[3])-Math.max(a[1],b[1])); return Math.round(x*y); };
  const board = document.querySelector('#fpAgreement.fp-now') || document.querySelector('.fp-now');
  const photo = board ? board.querySelector('.deal-sign-photo') : null;
  const frame = board ? board.querySelector('.deal-sign-frame') : null;
  const cap = [...document.querySelectorAll('body *')].filter(e => e.children.length === 0 && (e.textContent||'').includes('The Deck')).map(e => ({tag: e.tagName, cls: (typeof e.className==='string'?e.className:'').slice(0,60), rect: R(e), text: (e.textContent||'').trim().slice(0,40)}));
  const pr = R(photo);
  return {frameRect: R(frame), photoRect: pr, frameClass: frame ? frame.className.slice(0,80) : null,
    photoStyle: photo ? getComputedStyle(photo).cssText.slice(0,0) : null,
    photoHeight: photo ? getComputedStyle(photo).height : null,
    frameHeight: frame ? getComputedStyle(frame).height : null,
    frameOverflow: frame ? getComputedStyle(frame).overflow : null,
    captions: cap.map(c => ({...c, photoOverlap: ov(R(document.querySelector('.deal-sign-photo')), c.rect)})),
    boardScrollH: board ? board.scrollHeight : null, boardClientH: board ? board.clientHeight : null};
}"""
with sync_playwright() as pw:
    b = pw.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    pg = ctx.new_page()
    pg.goto(BASE + "/?stage=deck", timeout=60000)
    pg.wait_for_timeout(2500)
    for i in range(45):
        c = pg.evaluate("() => { const m = document.body.innerText.match(/(\\d+)\\s*\\/\\s*37/); return m ? m[0] : null; }")
        if c and c.startswith("37"): break
        pg.locator("#fpNextBtn").click(timeout=6000); pg.wait_for_timeout(500)
    print(json.dumps(pg.evaluate(JS), indent=1)[:2000], flush=True)
    ctx.close(); b.close()
