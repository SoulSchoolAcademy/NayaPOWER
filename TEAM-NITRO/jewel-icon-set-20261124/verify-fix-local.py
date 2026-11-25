#!/usr/bin/env python3
"""Fix-round local render probe — renders maker/showcase.html from a local
server (same files, sha-verified) in Chromium via the 127.0.0.1:18080
forwarder, phone 390x844 + desktop 1280x800. Checks every checker item
that can be checked locally before filing; the STAGED link gets its own
probe after filing (verify-fix-staged.py)."""
import json
import time
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8932/showcase.html"
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
    page.goto(URL, wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(1200)

    # 1. every inline SVG renders (bbox > 0) — the staged page must show icons
    svgs = page.evaluate("""() => [...document.querySelectorAll('svg')].map(s => {
      const r = s.getBoundingClientRect();
      return {w: Math.round(r.width), h: Math.round(r.height)}; })""")
    print("LOCAL inline SVGs:", len(svgs), "zero-size:", [s for s in svgs if s["w"] == 0])
    print("LOCAL img tags (must be 0):", page.evaluate("() => document.querySelectorAll('img').length"))

    # 2. bottom bar — one row, colours baked, labels hidden at phone
    bar = page.evaluate("""() => {
      const bar = document.querySelector('.bar');
      const cells = [...document.querySelectorAll('.bar .cell')].map(c => {
        const r = c.getBoundingClientRect();
        const svg = c.querySelector('svg');
        const rim = svg.querySelector('circle[stroke-opacity=".85"]');
        const gem = [...svg.querySelectorAll('linearGradient')].find(g => g.id.endsWith('gem'));
        const mid = gem ? gem.querySelectorAll('stop')[1].getAttribute('stop-color') : '?';
        return {label: c.querySelector('.lbl').textContent,
                top: Math.round(r.top), left: Math.round(r.left),
                rim: rim ? rim.getAttribute('stroke') : '?', gemMid: mid,
                lblDisplay: getComputedStyle(c.querySelector('.lbl')).display};
      });
      return {wrap: getComputedStyle(bar).flexWrap,
              scrollW: bar.scrollWidth, clientW: bar.clientWidth,
              scrollH: bar.scrollHeight, clientH: bar.clientHeight,
              cells};
    }""")
    print("BAR:", json.dumps(bar, indent=1))

    # 3. emoji construction audit — orbit + obsidian disc + crown, no gemorb
    emoji = page.evaluate("""() => [...document.querySelectorAll('.grid')[1].querySelectorAll('svg')].map(s => {
        const h = s.outerHTML;
        return {orbit: !!s.querySelector('.jwl-orbit'),
                disc: h.includes('disc)'), gemorb: h.includes('gemorb'),
                crown: h.includes('48,4 54,10 48,16 42,10')};
      })""")
    print("EMOJI audit (12):", emoji)
    print("EMOJI all orbit+disc+crown, no gemorb:",
          all(e["orbit"] and e["disc"] and e["crown"] and not e["gemorb"] for e in emoji))

    # 4. think bubble geometry from the live DOM
    think = page.evaluate("""() => {
      const svg = [...document.querySelectorAll('.grid')][1].querySelectorAll('svg')[4];
      const cs = [...svg.querySelectorAll('circle')].map(c => ({
        cx: +c.getAttribute('cx'), cy: +c.getAttribute('cy'),
        r: +c.getAttribute('r')}));
      return cs.map(c => ({...c, dist: Math.round(Math.hypot(c.cx - 48, c.cy - 48) * 10) / 10,
                           edge: Math.round((Math.hypot(c.cx - 48, c.cy - 48) + c.r) * 10) / 10}));
    }""")
    print("THINK circles (edge must be < 35.5):", think)

    # wow mouth is an open oval now, not the r=4.8 dot
    print("WOW mouth ellipse rx5.5:", page.evaluate(
        """() => [...document.querySelectorAll('.grid')][1].querySelectorAll('svg')[3]
             .outerHTML.includes('rx=\\"5.5\\"')"""))

    # hover / press on the touch contract
    jwl = page.locator(".jwl").first
    jwl.scroll_into_view_if_needed(); page.wait_for_timeout(300)
    print("JWL before:", jwl.evaluate("el => getComputedStyle(el).transform"))
    jwl.hover(); page.wait_for_timeout(500)
    print("JWL hover: ", jwl.evaluate("el => getComputedStyle(el).transform"))
    box = jwl.bounding_box()
    page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    page.mouse.down(); page.wait_for_timeout(200)
    print("JWL press: ", jwl.evaluate("el => getComputedStyle(el).transform"))
    page.mouse.up()

    # orbit turns (first inline svg's orbit group)
    def angle():
        return page.evaluate("""() => {
          const g = document.querySelector('.jwl-orbit');
          const m = new DOMMatrixReadOnly(getComputedStyle(g).transform);
          return Math.round(Math.atan2(m.b, m.a) * 180 / Math.PI * 100) / 100; }""")
    a1 = angle(); t1 = time.time(); time.sleep(6); a2 = angle()
    print(f"ORBIT mail inline: {a1}deg -> {a2}deg over {time.time()-t1:.1f}s (120s => ~18deg)")

    page.screenshot(path=f"{OUT}/fix-local-phone-full.png", full_page=True)
    page.screenshot(path=f"{OUT}/fix-local-phone-top.png")
    for name, sel, nth in [("core", ".grid", 0), ("bar", ".bar", 0),
                           ("thread", ".thread", 0), ("ladder", ".ladder", 0),
                           ("emoji", ".grid", 1)]:
        el = page.locator(sel).nth(nth)
        el.scroll_into_view_if_needed(); page.wait_for_timeout(400)
        el.screenshot(path=f"{OUT}/fix-local-phone-{name}.png")
    # think tile close-up + emoji-sm ladder
    think_tile = page.locator(".grid").nth(1).locator(".tile").nth(4)
    think_tile.scroll_into_view_if_needed(); page.wait_for_timeout(300)
    think_tile.screenshot(path=f"{OUT}/fix-local-phone-think.png")
    print("LOCAL phone errors:", errors)
    print("LOCAL phone failed:", failed)
    page.close()

    page3 = browser.new_page(viewport={"width": 1280, "height": 800},
                             device_scale_factor=2, ignore_https_errors=True)
    page3.on("pageerror", lambda e: errors.append("desktop: " + str(e)))
    page3.on("response", lambda r: failed.append(f"desktop: {r.url} :: HTTP {r.status}") if r.status >= 400 else None)
    page3.goto(URL, wait_until="networkidle", timeout=60000)
    page3.wait_for_timeout(1000)
    bar_d = page3.evaluate("""() => {
      const cells = [...document.querySelectorAll('.bar .cell')].map(c => {
        const r = c.getBoundingClientRect();
        return {label: c.querySelector('.lbl').textContent, top: Math.round(r.top),
                lblDisplay: getComputedStyle(c.querySelector('.lbl')).display}; });
      const bar = document.querySelector('.bar');
      return {wrap: getComputedStyle(bar).flexWrap, cells}; }""")
    print("BAR desktop:", json.dumps(bar_d))
    page3.screenshot(path=f"{OUT}/fix-local-desktop-full.png", full_page=True)
    page3.screenshot(path=f"{OUT}/fix-local-desktop-top.png")
    for name, sel, nth in [("bar", ".bar", 0), ("emoji", ".grid", 1)]:
        el = page3.locator(sel).nth(nth)
        el.scroll_into_view_if_needed(); page3.wait_for_timeout(300)
        el.screenshot(path=f"{OUT}/fix-local-desktop-{name}.png")
    print("ALL errors:", errors)
    print("ALL failed:", failed)
    page3.close()
    browser.close()
print("DONE-LOCAL")
