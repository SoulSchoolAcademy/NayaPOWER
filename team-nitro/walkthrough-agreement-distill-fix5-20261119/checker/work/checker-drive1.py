#!/usr/bin/env python3
"""Fix-5 checker driver 1 — my own F geometry probe + intro activation + desktop.
BASE = fix-4 tip bytes on :18095; FIX = fix-5 bytes on :18096.
Writes checker-log.json; screenshots ck5-* in the checker dir."""
import json, time
from playwright.sync_api import sync_playwright

CK = "/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix5-20261119/checker"
BASE = "http://127.0.0.1:18095"
FIX = "http://127.0.0.1:18096"
LOG = CK + "/checker-log.json"

GEO_SWEEP = r"""() => {
  const nav = document.querySelector('#fpLegal .fp-legal-links');
  if (!nav) return {error: 'no nav'};
  const cs = getComputedStyle(nav);
  const nr = nav.getBoundingClientRect();
  const links = [...nav.querySelectorAll('a, button')].map(el => el.textContent.trim());
  const max = nav.scrollWidth - nav.clientWidth;
  const seenVP = links.map(() => null);   // fully inside viewport [0,390]
  const seenStrip = links.map(() => null); // fully inside the strip's own rect
  const positions = [0];
  for (let s = 50; s < max; s += 50) positions.push(s);
  if (max > 0) positions.push(max);
  const steps = [];
  for (const sl of positions) {
    nav.scrollLeft = sl;
    const actual = nav.scrollLeft;
    const rects = [...nav.querySelectorAll('a, button')].map(el => {
      const r = el.getBoundingClientRect();
      return {left: Math.round(r.left), right: Math.round(r.right)};
    });
    rects.forEach((rc, i) => {
      if (rc.left >= 0 && rc.right <= 390 && seenVP[i] === null) seenVP[i] = actual;
      if (rc.left >= Math.round(nr.left) && rc.right <= Math.round(nr.right) && seenStrip[i] === null) seenStrip[i] = actual;
    });
    steps.push({scrollLeft: actual, rects});
  }
  nav.scrollLeft = 0;
  const reachVP = seenVP.map((s, i) => ({link: links[i], reachable: s !== null, at: s}));
  const reachStrip = seenStrip.map((s, i) => ({link: links[i], reachable: s !== null, at: s}));
  return {
    navRect: [Math.round(nr.left), Math.round(nr.top), Math.round(nr.right), Math.round(nr.bottom)],
    scrollWidth: nav.scrollWidth, clientWidth: nav.clientWidth, maxScroll: max,
    justifyContent: cs.justifyContent, flexWrap: cs.flexWrap, overflowX: cs.overflowX,
    linkCount: links.length, links,
    reachableViewport: reachVP, unreachableViewport: reachVP.filter(r => !r.reachable).length,
    reachableStrip: reachStrip, unreachableStrip: reachStrip.filter(r => !r.reachable).length,
    at0: steps[0], atMax: steps[steps.length - 1]
  };
}"""

STAGE_STATE = r"""() => {
  const f = document.querySelector('#fpLegal');
  const n = document.querySelector('#fpLegal .fp-legal-links');
  const login = document.querySelector('#fp-login');
  return {
    bodyClass: document.body.className,
    htmlClass: document.documentElement.className,
    fpLegalDisplay: f ? getComputedStyle(f).display : 'MISSING',
    navDisplay: n ? getComputedStyle(n).display : 'MISSING',
    loginVisible: login ? login.offsetParent !== null : null,
    visibleButtons: [...document.querySelectorAll('button')].filter(x => x.offsetParent !== null)
      .map(x => (x.id ? '#' + x.id + ' ' : '') + x.innerText.trim().slice(0, 44))
  };
}"""

def walk_unfold_to_agree(page):
    for i in range(40):
        if page.evaluate("() => [...document.querySelectorAll('button')].some(x=>x.offsetParent!==null && /I agree/i.test(x.innerText))"):
            return True
        page.locator("button", has_text="Next").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(350)
    return False

def bridge_geo(page, base_url, shot_prefix):
    page.goto(base_url + "/agreement", timeout=60000)
    page.wait_for_timeout(2000)
    ok = walk_unfold_to_agree(page)
    assert ok, "never reached I agree on " + base_url
    page.locator("button", has_text="I agree").locator("visible=true").first.click(timeout=5000)
    page.wait_for_timeout(2500)
    geo = page.evaluate(GEO_SWEEP)
    page.evaluate("() => { const n = document.querySelector('#fpLegal .fp-legal-links'); if (n) n.scrollLeft = 0; }")
    page.wait_for_timeout(400)
    page.screenshot(path=CK + "/" + shot_prefix + "-s0.png")
    page.evaluate("() => { const n = document.querySelector('#fpLegal .fp-legal-links'); if (n) n.scrollLeft = n.scrollWidth; }")
    page.wait_for_timeout(400)
    page.screenshot(path=CK + "/" + shot_prefix + "-smax.png")
    return geo

def desk_geo(page, base_url):
    page.goto(base_url + "/?stage=bridge", timeout=60000)
    page.wait_for_timeout(2500)
    return page.evaluate(r"""() => {
      const nav = document.querySelector('#fpLegal .fp-legal-links');
      if (!nav) return {error: 'no nav'};
      const cs = getComputedStyle(nav);
      const r = nav.getBoundingClientRect();
      const links = [...nav.querySelectorAll('a, button')].map(el => {
        const b = el.getBoundingClientRect();
        return {t: el.textContent.trim(), left: Math.round(b.left), right: Math.round(b.right)};
      });
      return {navRect: [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)],
        scrollWidth: nav.scrollWidth, clientWidth: nav.clientWidth,
        justifyContent: cs.justifyContent, flexWrap: cs.flexWrap, links};
    }""")

out = {"label": "FIX5-CHECKER-DRIVE1", "legs": []}
def leg(name, fn):
    try:
        out["legs"].append({"leg": name, **fn()})
    except Exception as e:
        out["legs"].append({"leg": name, "ERROR": str(e)[:600]})
        print("LEG FAIL", name, str(e)[:300], flush=True)

with sync_playwright() as pw:
    # ---- intro activation on FIX5, real citizen path: login name form -> Enter ----
    b = pw.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, ignore_https_errors=True)
    page = ctx.new_page()
    errs = []
    page.on("pageerror", lambda e: errs.append(str(e)[:200]))
    page.on("console", lambda m: errs.append(m.type + ": " + m.text[:200]) if m.type == "error" else None)
    def leg_intro_cold():
        page.goto(FIX + "/", timeout=60000); page.wait_for_timeout(3000)
        return {"cold": page.evaluate(STAGE_STATE)}
    leg("intro-cold-load", leg_intro_cold)
    def leg_intro_enter():
        page.locator("#userName").fill("Checker Five")
        page.locator("#entryForm button.enter").click(timeout=6000)
        page.wait_for_timeout(3000)
        st = page.evaluate(STAGE_STATE)
        geo = page.evaluate(GEO_SWEEP)
        page.evaluate("() => { const n = document.querySelector('#fpLegal .fp-legal-links'); if (n) n.scrollLeft = 0; }")
        page.wait_for_timeout(400)
        page.screenshot(path=CK + "/ck5-intro-s0.png")
        page.evaluate("() => { const n = document.querySelector('#fpLegal .fp-legal-links'); if (n) n.scrollLeft = n.scrollWidth; }")
        page.wait_for_timeout(400)
        page.screenshot(path=CK + "/ck5-intro-smax.png")
        return {"afterEnter": st, "geo": geo, "consoleErrors": errs}
    leg("intro-after-enter", leg_intro_enter)
    def leg_intro_param():
        page.goto(FIX + "/?stage=intro", timeout=60000); page.wait_for_timeout(3000)
        return page.evaluate(STAGE_STATE)
    leg("intro-param-stage-intro", leg_intro_param)
    b.close()

    # ---- bridge F: BASE then FIX, same harness ----
    for label, base_url, prefix in (("BASE", BASE, "ck5-base-F-bridge"), ("FIX5", FIX, "ck5-fix-F-bridge")):
        b = pw.firefox.launch(headless=True)
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, ignore_https_errors=True)
        page = ctx.new_page()
        errs2 = []
        page.on("pageerror", lambda e: errs2.append(str(e)[:200]))
        page.on("console", lambda m: errs2.append(m.type + ": " + m.text[:200]) if m.type == "error" else None)
        def mk_geo(bu=base_url, sp=prefix, e2=errs2):
            def f():
                g = bridge_geo(page, bu, sp)
                g["consoleErrors"] = e2
                return g
            return f
        leg(label + "-bridge-footer-geo", mk_geo())
        b.close()

    # ---- desktop 1920: FIX5 and BASE ----
    for label, base_url in (("FIX5", FIX), ("BASE", BASE)):
        b = pw.firefox.launch(headless=True)
        ctx = b.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=1, ignore_https_errors=True)
        page = ctx.new_page()
        errs3 = []
        page.on("pageerror", lambda e: errs3.append(str(e)[:200]))
        page.on("console", lambda m: errs3.append(m.type + ": " + m.text[:200]) if m.type == "error" else None)
        def mk_desk(bu=base_url, e3=errs3):
            def f():
                g = desk_geo(page, bu)
                g["consoleErrors"] = e3
                return g
            return f
        leg(label + "-desktop-1920-bridge-geo", mk_desk())
        if label == "FIX5":
            page.screenshot(path=CK + "/ck5-1920-bridge.png")
        b.close()

with open(LOG, "w") as f:
    json.dump(out, f, indent=1)
for l in out["legs"]:
    print(json.dumps(l)[:1400], flush=True)
print("WROTE", LOG)
