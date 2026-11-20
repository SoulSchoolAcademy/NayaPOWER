#!/usr/bin/env python3
"""Fix-5 maker: reproduce defect F on BASE bytes at 390x844.
Geometry probe: for the footer strip (#fpLegal .fp-legal-links) sweep
scrollLeft across its full range and record every one of the 12 links'
rects at each step. A link is REACHABLE iff at some scrollLeft its rect
lies inside the page viewport: left >= 0 and right <= 390.
Probes both states that carry a nowrap rule: intro (load /) and bridge
(/agreement -> tap through -> I agree -> bridge).
Screenshots: strip at scrollLeft 0 and at max scroll, per state.
Usage: python3 probe-fix5-base.py  (writes proof-base/fix5-base.json)
"""
import json, sys, time
from playwright.sync_api import sync_playwright

W = "/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work"
BASE = "http://127.0.0.1:18093"
LOG = W + "/proof-base/fix5-base.json"

GEO_SWEEP = r"""() => {
  const nav = document.querySelector('#fpLegal .fp-legal-links');
  if (!nav) return {error: 'no nav'};
  const cs = getComputedStyle(nav);
  const navRect = nav.getBoundingClientRect();
  const links = [...nav.querySelectorAll('a, button')].map(el => el.textContent.trim());
  const max = nav.scrollWidth - nav.clientWidth;
  const steps = [];
  const seen = links.map(() => null);
  const positions = [0];
  for (let s = 100; s < max; s += 100) positions.push(s);
  if (max > 0) positions.push(max);
  for (const sl of positions) {
    nav.scrollLeft = sl;
    const actual = nav.scrollLeft;
    const rects = [...nav.querySelectorAll('a, button')].map(el => {
      const r = el.getBoundingClientRect();
      return {left: Math.round(r.left), right: Math.round(r.right), top: Math.round(r.top), bottom: Math.round(r.bottom)};
    });
    rects.forEach((rc, i) => {
      if (rc.left >= 0 && rc.right <= 390 && seen[i] === null) seen[i] = actual;
    });
    steps.push({scrollLeft: actual, rects});
  }
  nav.scrollLeft = 0;
  const reachable = seen.map((s, i) => ({link: links[i], reachable: s !== null, atScrollLeft: s}));
  return {
    navRect: [Math.round(navRect.left), Math.round(navRect.top), Math.round(navRect.right), Math.round(navRect.bottom)],
    scrollWidth: nav.scrollWidth, clientWidth: nav.clientWidth, maxScroll: max,
    justifyContent: cs.justifyContent, flexWrap: cs.flexWrap, overflowX: cs.overflowX,
    display: cs.display, linkCount: links.length, links,
    reachable, unreachableCount: reachable.filter(r => !r.reachable).length,
    at0: steps[0], atMax: steps[steps.length-1]
  };
}"""

def shot_strip(page, path, sl):
    page.evaluate(f"() => {{ const n = document.querySelector('#fpLegal .fp-legal-links'); if (n) n.scrollLeft = {sl}; }}")
    page.wait_for_timeout(400)
    page.screenshot(path=path)

def run(pw, label):
    out = {"label": label, "steps": []}
    b = pw.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, ignore_https_errors=True)
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)[:200]))
    page.on("console", lambda m: errors.append(m.type + ": " + m.text[:200]) if m.type == "error" else None)
    try:
        # --- intro state: load / ---
        page.goto(BASE + "/", timeout=60000)
        page.wait_for_timeout(2500)
        intro = page.evaluate(GEO_SWEEP)
        out["steps"].append({"state": "intro", **intro})
        shot_strip(page, W + f"/proof-base/fix5-base-intro-s0.png", 0)
        if intro.get("maxScroll"):
            shot_strip(page, W + f"/proof-base/fix5-base-intro-smax.png", intro["maxScroll"])
        # --- bridge state: /agreement -> tap to 37 -> I agree ---
        page.goto(BASE + "/agreement", timeout=60000)
        page.wait_for_timeout(2000)
        for i in range(40):
            if page.evaluate("() => [...document.querySelectorAll('button')].some(x=>x.offsetParent!==null && /I agree/i.test(x.innerText))"):
                break
            page.locator("button", has_text="Next").locator("visible=true").first.click(timeout=5000)
            page.wait_for_timeout(400)
        page.locator("button", has_text="I agree").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(2500)
        bridge = page.evaluate(GEO_SWEEP)
        out["steps"].append({"state": "bridge", **bridge})
        shot_strip(page, W + "/proof-base/fix5-base-bridge-s0.png", 0)
        if bridge.get("maxScroll"):
            shot_strip(page, W + "/proof-base/fix5-base-bridge-smax.png", bridge["maxScroll"])
        page.screenshot(path=W + "/proof-base/fix5-base-bridge-full.png")
        out["consoleErrors"] = errors
    finally:
        b.close()
    return out

with sync_playwright() as pw:
    res = run(pw, "BASE")
with open(LOG, "w") as f:
    json.dump(res, f, indent=1)
for st in res["steps"]:
    print(st["state"], "links:", st.get("linkCount"), "scrollWidth:", st.get("scrollWidth"),
          "clientWidth:", st.get("clientWidth"), "maxScroll:", st.get("maxScroll"),
          "justify:", st.get("justifyContent"), "wrap:", st.get("flexWrap"))
    for r in st.get("reachable", []):
        print("   ", r["link"], "reachable:", r["reachable"], "at:", r["atScrollLeft"])
    print("    at0 rects:", [(r["link"] if False else "") for r in []] or
          [(l, a["left"], a["right"]) for l, a in zip(st["links"], st["at0"]["rects"])])
    print("    atMax rects:", [(l, a["left"], a["right"]) for l, a in zip(st["links"], st["atMax"]["rects"])])
print("consoleErrors:", res.get("consoleErrors"))
print("WROTE", LOG)
