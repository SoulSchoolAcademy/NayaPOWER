#!/usr/bin/env python3
"""Focused sense check: every p.ev sw<=cw, refined overflower scan, ev183 geometry."""
import json, sys
from playwright.sync_api import sync_playwright

def scan(page, width, url):
    page.set_viewport_size({"width": width, "height": 900})
    page.goto(url, wait_until="load")
    page.wait_for_timeout(600)
    return page.evaluate("""() => {
      const iw = window.innerWidth;
      const badRect = [];
      const badScroll = [];
      document.querySelectorAll('body *').forEach(el => {
        const r = el.getBoundingClientRect();
        const cs = getComputedStyle(el);
        if (r.right > iw + 1 && r.width > 0) badRect.push({tag: el.tagName, cls: String(el.className).slice(0,30), right: Math.round(r.right), w: Math.round(r.width), text: (el.textContent||'').slice(0,60)});
        if (cs.display !== 'inline' && el.clientWidth > 0 && el.scrollWidth > el.clientWidth + 1)
          badScroll.push({tag: el.tagName, cls: String(el.className).slice(0,30), sw: el.scrollWidth, cw: el.clientWidth, text: (el.textContent||'').slice(0,60)});
      });
      const evs = [...document.querySelectorAll('p.ev')].map(e => ({sw: e.scrollWidth, cw: e.clientWidth, h: Math.round(e.getBoundingClientRect().height)})).filter(x => x.sw > x.cw + 1);
      const ev183 = [...document.querySelectorAll('p.ev')].find(e => e.textContent.includes('CLARITY-CONFIRMATION-ACT-DRAFT'));
      const r183 = ev183.getBoundingClientRect();
      return {docSW: document.documentElement.scrollWidth, iw,
              badRect: badRect.slice(0,10), nBadRect: badRect.length,
              badScroll: badScroll.slice(0,10), nBadScroll: badScroll.length,
              evOverflowing: evs, nEvOverflowing: evs.length,
              ev183: {sw: ev183.scrollWidth, cw: ev183.clientWidth, h: Math.round(r183.height), lines: Math.round(r183.height / 27)}};
    }""")

out = {}
with sync_playwright() as p:
    b = p.firefox.launch()
    pg = b.new_page()
    for label, url in (("post", "file:///home/hatch/workspace/project-intelligence/proof/index.html"),
                       ("pre", "file:///tmp/pre-fix-index.html")):
        out[label] = {}
        for w in (1440, 390, 360):
            out[label][w] = scan(pg, w, url)
    b.close()
print(json.dumps(out, indent=2))
json.dump(out, open(sys.argv[1], "w"), indent=2)
