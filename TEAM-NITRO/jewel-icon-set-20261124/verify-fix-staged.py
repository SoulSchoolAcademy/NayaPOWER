#!/usr/bin/env python3
"""Fix-round STAGED render probe — renders the proof-host link itself
(the ?file=/ref=/cb= URL from the filing receipt), Chromium via the
127.0.0.1:18080 forwarder, phone 390x844 + desktop 1280x800.
This is the check round 1 skipped: bytes-only verification is not a
render. Screenshots are lane evidence (maker/fix-staged-*.png)."""
import json
from playwright.sync_api import sync_playwright

URL = ("https://naya-proof-host.nayapower.workers.dev/"
       "?file=TEAM-NITRO/jewel-icon-set-20261124/showcase.html"
       "&ref=62b19dcb83eee5782ca920c0ea60f58cda99fa97"
       "&cb=09896daf092ced1a7a45803962366a085757ff5e&t=1795050600")
OUT = "/home/hatch/workspace/team-nitro/jewel-icon-set-20261124/maker"
errors, failed = [], []

with sync_playwright() as p:
    browser = p.chromium.launch(proxy={"server": "http://127.0.0.1:18080",
                                       "bypass": "127.0.0.1,localhost"},
                                args=["--no-sandbox"])
    page = browser.new_page(viewport={"width": 390, "height": 844},
                            device_scale_factor=3, is_mobile=True,
                            has_touch=True, ignore_https_errors=True)
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("requestfailed", lambda r: failed.append(f"{r.url} :: {r.failure}"))
    page.on("response", lambda r: failed.append(f"{r.url} :: HTTP {r.status}") if r.status >= 400 else None)
    page.goto(URL, wait_until="networkidle", timeout=90000)
    page.wait_for_timeout(1500)
    svgs = page.evaluate("""() => [...document.querySelectorAll('svg')].map(s => {
      const r = s.getBoundingClientRect();
      return {w: Math.round(r.width), h: Math.round(r.height)}; })""")
    print("STAGED inline SVGs:", len(svgs), "zero-size:", [s for s in svgs if s["w"] == 0])
    print("STAGED img tags (must be 0):", page.evaluate("() => document.querySelectorAll('img').length"))
    bar = page.evaluate("""() => {
      const bar = document.querySelector('.bar');
      const cells = [...document.querySelectorAll('.bar .cell')].map(c => {
        const r = c.getBoundingClientRect();
        const svg = c.querySelector('svg');
        const rim = svg.querySelector('circle[stroke-opacity=".85"]');
        return {label: c.querySelector('.lbl').textContent,
                top: Math.round(r.top), rim: rim ? rim.getAttribute('stroke') : '?'};
      });
      return {wrap: getComputedStyle(bar).flexWrap,
              scrollW: bar.scrollWidth, clientW: bar.clientWidth, cells};
    }""")
    print("STAGED BAR phone:", json.dumps(bar))
    emoji = page.evaluate("""() => [...document.querySelectorAll('.grid')[1].querySelectorAll('svg')].map(s => {
        const h = s.outerHTML;
        return {orbit: !!s.querySelector('.jwl-orbit'), disc: h.includes('disc)'),
                gemorb: h.includes('gemorb'), crown: h.includes('48,4 54,10 48,16 42,10')};
      })""")
    print("STAGED EMOJI all orbit+disc+crown, no gemorb:",
          all(e["orbit"] and e["disc"] and e["crown"] and not e["gemorb"] for e in emoji),
          f"({len(emoji)} checked)")
    page.screenshot(path=f"{OUT}/fix-staged-phone-top.png", timeout=60000)
    for name, sel, nth in [("bar", ".bar", 0), ("emoji", ".grid", 1),
                           ("core", ".grid", 0), ("thread", ".thread", 0)]:
        el = page.locator(sel).nth(nth)
        el.scroll_into_view_if_needed(); page.wait_for_timeout(400)
        el.screenshot(path=f"{OUT}/fix-staged-phone-{name}.png", timeout=60000)
    print("STAGED phone errors:", errors)
    print("STAGED phone failed:", failed)
    page.close()

    page3 = browser.new_page(viewport={"width": 1280, "height": 800},
                             device_scale_factor=2, ignore_https_errors=True)
    page3.on("pageerror", lambda e: errors.append("desktop: " + str(e)))
    page3.on("response", lambda r: failed.append(f"desktop: {r.url} :: HTTP {r.status}") if r.status >= 400 else None)
    page3.goto(URL, wait_until="networkidle", timeout=90000)
    page3.wait_for_timeout(1000)
    bar_d = page3.evaluate("""() => {
      const cells = [...document.querySelectorAll('.bar .cell')].map(c => {
        const r = c.getBoundingClientRect();
        return {label: c.querySelector('.lbl').textContent, top: Math.round(r.top),
                lblDisplay: getComputedStyle(c.querySelector('.lbl')).display}; });
      return {wrap: getComputedStyle(document.querySelector('.bar')).flexWrap, cells}; }""")
    print("STAGED BAR desktop:", json.dumps(bar_d))
    page3.screenshot(path=f"{OUT}/fix-staged-desktop-top.png", timeout=60000)
    for name, sel, nth in [("bar", ".bar", 0), ("emoji", ".grid", 1)]:
        el = page3.locator(sel).nth(nth)
        el.scroll_into_view_if_needed(); page3.wait_for_timeout(300)
        el.screenshot(path=f"{OUT}/fix-staged-desktop-{name}.png", timeout=60000)
    print("ALL errors:", errors)
    print("ALL failed:", failed)
    page3.close()
    browser.close()
print("DONE-STAGED")
