#!/usr/bin/env python3
"""Identify the lowest visible text leaves at max scroll (baseline staged shell).
For each width: scroll to max, list text leaves whose rect intersects the viewport
and ends below the obb-bar top, with tag/class/ancestor chain and .main membership.
"""
import json
from playwright.sync_api import sync_playwright

WD = "/home/hatch/workspace/team-nitro/hub-shell-bars-20261113"
STAGING = "https://naya-public-blog-staging.nayapower.workers.dev"

JS = """() => {
  const fixedAncestor = el => { let n = el; while (n) { const p = getComputedStyle(n).position;
    if (p === 'fixed') return true; n = n.parentElement; } return false; };
  const obb = document.querySelector('#obb-bar');
  const obbTop = obb ? obb.getBoundingClientRect().top : null;
  const notif = document.querySelector('#naya-notif-bar');
  const notifTop = notif ? notif.getBoundingClientRect().top : null;
  const chain = el => { const parts = []; let n = el;
    while (n && n !== document.body) { parts.unshift((n.tagName||'').toLowerCase() +
      (n.id ? '#'+n.id : '') + (n.className && typeof n.className === 'string' && n.className ? '.'+n.className.trim().split(/\\s+/).slice(0,3).join('.') : ''));
      n = n.parentElement; } return parts.join(' > '); };
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const hits = []; let node;
  while (node = walker.nextNode()) {
    if (!node.nodeValue || !node.nodeValue.trim()) continue;
    const el = node.parentElement; if (!el || fixedAncestor(el)) continue;
    const b = el.getBoundingClientRect();
    if (b.height <= 0) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    // visible portion intersects viewport?
    if (b.bottom <= 0 || b.top >= window.innerHeight) continue;
    hits.push({text: node.nodeValue.trim().slice(0, 50), top: Math.round(b.top),
      bottom: Math.round(b.bottom), tag: el.tagName, cls: (el.className||'').toString().slice(0,80),
      inMain: !!el.closest('.main'), chain: chain(el)});
  }
  hits.sort((a,b) => b.bottom - a.bottom);
  return {obbTop: Math.round(obbTop), notifTop: Math.round(notifTop), viewH: window.innerHeight,
          scrollY: Math.round(window.scrollY), docH: document.documentElement.scrollHeight,
          lowest5: hits.slice(0, 5),
          underBar: hits.filter(h => h.bottom > obbTop).length};
}"""

with sync_playwright() as pw:
    for w, h in [(390, 844), (1440, 900)]:
        browser = pw.firefox.launch(headless=True)
        pg = browser.new_context(viewport={"width": w, "height": h}).new_page()
        pg.goto(STAGING + "/s/sn2696", timeout=60000)
        pg.wait_for_timeout(3500)
        pg.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        pg.wait_for_timeout(1000)
        print(f"== WIDTH {w} ==")
        print(json.dumps(pg.evaluate(JS), indent=1))
        browser.close()
