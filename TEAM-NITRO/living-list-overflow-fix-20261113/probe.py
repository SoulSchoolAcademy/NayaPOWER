#!/usr/bin/env python3
"""Measure overflow / errors / counts on the staged Living List render."""
import json, sys
from playwright.sync_api import sync_playwright

URL = "file:///home/hatch/workspace/project-intelligence/proof/index.html"
OUT = sys.argv[1]
SHOTDIR = sys.argv[2]

def measure(page, width):
    page.set_viewport_size({"width": width, "height": 900})
    page.goto(URL, wait_until="load")
    page.wait_for_timeout(800)
    res = {}
    for pos in ("start", "end"):
        if pos == "end":
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(500)
        else:
            page.evaluate("window.scrollTo(0,0)")
            page.wait_for_timeout(300)
        m = page.evaluate("""() => {
          const de = document.documentElement;
          const bad = [];
          document.querySelectorAll('*').forEach(el => {
            const r = el.getBoundingClientRect();
            if (r.width > window.innerWidth + 1 || el.scrollWidth > el.clientWidth + 1) {
              bad.push({tag: el.tagName, cls: el.className && el.className.baseVal !== undefined ? '' : String(el.className).slice(0,40),
                        sw: el.scrollWidth, cw: el.clientWidth, w: Math.round(r.width),
                        text: (el.textContent||'').slice(0,80)});
            }
          });
          return {scrollWidth: de.scrollWidth, innerWidth: window.innerWidth,
                  scrollHeight: de.scrollHeight, overflowers: bad.slice(0,12), nOverflowers: bad.length};
        }""")
        res[pos] = m
        page.screenshot(path=f"{SHOTDIR}/{width}-{pos}.png")
    return res

with sync_playwright() as p:
    browser = p.firefox.launch()
    page = browser.new_page()
    console, pageerr, failed = [], [], []
    page.on("console", lambda m: console.append(f"{m.type}: {m.text}") if m.type in ("error","warning") else None)
    page.on("pageerror", lambda e: pageerr.append(str(e)))
    page.on("requestfailed", lambda r: failed.append(f"{r.url} {r.failure}"))
    page.on("response", lambda r: failed.append(f"{r.url} HTTP {r.status}") if r.status >= 400 else None)
    out = {}
    for w in (1440, 390, 360):
        out[w] = measure(page, w)
    counts = page.evaluate("""() => {
      const s = document.querySelector('.subline');
      const ev183 = [...document.querySelectorAll('p.ev')].find(e => e.textContent.includes('CLARITY-CONFIRMATION-ACT-DRAFT'));
      return {subline: s ? s.textContent.trim().slice(0,200) : null,
              ev183: ev183 ? {sw: ev183.scrollWidth, cw: ev183.clientWidth} : null,
              nEv: document.querySelectorAll('p.ev').length};
    }""")
    out["counts"] = counts
    out["console_errors"] = console
    out["page_errors"] = pageerr
    out["failed_requests"] = failed
    browser.close()

json.dump(out, open(OUT, "w"), indent=2)
print(json.dumps(out, indent=2))
