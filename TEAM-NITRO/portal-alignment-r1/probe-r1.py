#!/usr/bin/env python3
"""ALIGNMENT R1 probe — staged R1 only. Labels visible at rest (both widths),
phone 3x3 grid, strip present, no horizontal overflow, single-tap navigates,
name entry -> /identity.html on the same host, console/pageerror log.
Chromium 1255 via the localhost forwarder (127.0.0.1:18080)."""
import json, os
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://portal-alignment-r1-staging.nayapower.workers.dev"
PROXY = {"server": "http://127.0.0.1:18080"}
EXE = "/home/hatch/.cache/ms-playwright/chromium-1255/chrome-linux64/chrome"
LOG = {"errors": [], "failed_requests": [], "requestfailed": [], "checks": {}}

def hook(page, tag):
    page.on("console", lambda m: LOG["errors"].append(f"{tag} console.{m.type}: {m.text[:200]}") if m.type == "error" else None)
    page.on("pageerror", lambda e: LOG["errors"].append(f"{tag} pageerror: {str(e)[:200]}"))
    page.on("response", lambda r: LOG["failed_requests"].append(f"{tag} {r.status} {r.url[:140]}") if r.status >= 400 else None)
    page.on("requestfailed", lambda r: LOG["requestfailed"].append(f"{tag} {r.failure} {r.url[:140]}") if r.url.startswith("http") else None)

NAV_JS = """() => {
  const nav = document.querySelector('nav.eco-inline');
  const items = [...document.querySelectorAll('nav.eco-inline > a')];
  const cs = nav ? getComputedStyle(nav) : null;
  const strip = document.querySelector('.fp-walk-strip');
  const sr = strip ? strip.getBoundingClientRect() : null;
  return {
    vw: window.innerWidth, scrollW: document.scrollingElement.scrollWidth,
    nav: nav ? {display: cs.display, gridCols: cs.gridTemplateColumns, flexWrap: cs.flexWrap,
      rect: (r => ({x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)}))(nav.getBoundingClientRect())} : null,
    items: items.map((a, i) => {
      const r = a.getBoundingClientRect();
      const tip = a.querySelector('.eco-tip');
      const tcs = tip ? getComputedStyle(tip) : null;
      const tr = tip ? tip.getBoundingClientRect() : null;
      return {i, label: a.getAttribute('aria-label'), tipText: tip ? tip.textContent.trim() : null,
        tipOpacity: tcs ? tcs.opacity : null, tipFont: tcs ? tcs.fontSize : null,
        rect: {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)},
        tipRect: tr ? {x: Math.round(tr.x), y: Math.round(tr.y), w: Math.round(tr.width), h: Math.round(tr.height), right: Math.round(tr.right)} : null};
    }),
    strip: strip ? {text: strip.textContent.replace(/\\s+/g,' ').trim(),
      links: [...strip.querySelectorAll('a')].map(a => a.getAttribute('href')),
      rect: {x: Math.round(sr.x), y: Math.round(sr.y), w: Math.round(sr.width), h: Math.round(sr.height), right: Math.round(sr.right)}} : null
  };
}"""

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=EXE, args=["--no-sandbox"])
    for tag, w, h in [("phone", 390, 844), ("desk", 1440, 900)]:
        pg = b.new_page(viewport={"width": w, "height": h}, proxy=PROXY, has_touch=(tag == "phone"))
        hook(pg, tag)
        pg.goto(BASE + "/", wait_until="networkidle", timeout=90000)
        pg.wait_for_timeout(1500)
        data = pg.evaluate(NAV_JS)
        LOG["checks"][tag] = data
        pg.screenshot(path=os.path.join(HERE, f"r1-{tag}-front.png"))
        # single tap/click on Innovations (index 2): must navigate on FIRST tap now.
        # Links are target=_blank, so the tap opens a popup, not a same-page nav.
        if tag == "phone":
            with pg.expect_popup(timeout=30000) as pop:
                pg.locator("nav.eco-inline > a").nth(2).tap()
            LOG["checks"]["phone_tap_innovations_url"] = pop.value.url
            pop.value.close()
        else:
            with pg.expect_popup(timeout=30000) as pop:
                pg.locator("nav.eco-inline > a").nth(2).click()
            LOG["checks"]["desk_click_innovations_url"] = pop.value.url
            pop.value.close()
        with open(os.path.join(HERE, "r1-probe-log.json"), "w") as f:
            json.dump(LOG, f, indent=2)
        pg.close()
    # name entry -> certificate on the same host
    pg = b.new_page(viewport={"width": 390, "height": 844}, proxy=PROXY)
    hook(pg, "name")
    pg.goto(BASE + "/", wait_until="networkidle", timeout=90000)
    pg.wait_for_timeout(1000)
    pg.fill("#userName", "R1 Check")
    with pg.expect_navigation(timeout=30000):
        pg.click(".enter")
    LOG["checks"]["name_entry_url"] = pg.url
    pg.screenshot(path=os.path.join(HERE, "r1-phone-cert.png"))
    pg.close()
    b.close()

with open(os.path.join(HERE, "r1-probe-log.json"), "w") as f:
    json.dump(LOG, f, indent=2)
print(json.dumps(LOG["checks"], indent=2)[:6000])
print("ERRORS:", json.dumps(LOG["errors"], indent=2)[:2000])
print("FAILED_REQ:", json.dumps(LOG["failed_requests"], indent=2)[:2000])
