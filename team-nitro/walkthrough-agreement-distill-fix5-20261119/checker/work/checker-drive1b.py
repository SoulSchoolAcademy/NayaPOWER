#!/usr/bin/env python3
"""Fix-5 checker driver 1b — intro activation, attempt 2.
Path: cold `/` -> fill name -> Enter (lands on /welcome) -> click #enterBtn.
If that lands the intro stage, sweep the intro strip. Fallback: diagnostic
window.__fpStage.enter() on a cold `/` load (labelled as diagnostic, not the
citizen flow) so the intro rule is still geometry-probed through the real render.
Writes checker-log-intro.json."""
import json
from playwright.sync_api import sync_playwright

CK = "/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix5-20261119/checker"
FIX = "http://127.0.0.1:18096"
LOG = CK + "/checker-log-intro.json"

GEO_SWEEP = r"""() => {
  const nav = document.querySelector('#fpLegal .fp-legal-links');
  if (!nav) return {error: 'no nav'};
  const cs = getComputedStyle(nav);
  const nr = nav.getBoundingClientRect();
  const links = [...nav.querySelectorAll('a, button')].map(el => el.textContent.trim());
  const max = nav.scrollWidth - nav.clientWidth;
  const seen = links.map(() => null);
  const positions = [0];
  for (let s = 50; s < max; s += 50) positions.push(s);
  if (max > 0) positions.push(max);
  for (const sl of positions) {
    nav.scrollLeft = sl;
    const actual = nav.scrollLeft;
    [...nav.querySelectorAll('a, button')].forEach((el, i) => {
      const r = el.getBoundingClientRect();
      if (r.left >= 0 && r.right <= 390 && seen[i] === null) seen[i] = actual;
    });
  }
  nav.scrollLeft = 0;
  const reach = seen.map((s, i) => ({link: links[i], reachable: s !== null, at: s}));
  const at0 = [...nav.querySelectorAll('a, button')].map(el => { const r = el.getBoundingClientRect(); return {left: Math.round(r.left), right: Math.round(r.right)}; });
  nav.scrollLeft = max;
  const atMax = [...nav.querySelectorAll('a, button')].map(el => { const r = el.getBoundingClientRect(); return {left: Math.round(r.left), right: Math.round(r.right)}; });
  nav.scrollLeft = 0;
  return {navRect: [Math.round(nr.left), Math.round(nr.top), Math.round(nr.right), Math.round(nr.bottom)],
    scrollWidth: nav.scrollWidth, clientWidth: nav.clientWidth, maxScroll: max,
    justifyContent: cs.justifyContent, flexWrap: cs.flexWrap, overflowX: cs.overflowX,
    linkCount: links.length, links, reachable: reach,
    unreachable: reach.filter(r => !r.reachable).length, at0, atMax};
}"""

STATE = r"""() => {
  const f = document.querySelector('#fpLegal');
  return {url: location.href, bodyClass: document.body.className,
    fpLegalDisplay: f ? getComputedStyle(f).display : 'MISSING',
    visibleButtons: [...document.querySelectorAll('button')].filter(x => x.offsetParent !== null)
      .map(x => (x.id ? '#' + x.id + ' ' : '') + x.innerText.trim().slice(0, 44))};
}"""

out = {"label": "FIX5-CHECKER-INTRO-1B", "legs": []}
def leg(name, fn):
    try:
        out["legs"].append({"leg": name, **fn()})
    except Exception as e:
        out["legs"].append({"leg": name, "ERROR": str(e)[:600]})
        print("LEG FAIL", name, str(e)[:300], flush=True)

with sync_playwright() as pw:
    b = pw.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, ignore_https_errors=True)
    page = ctx.new_page()
    errs = []
    page.on("pageerror", lambda e: errs.append(str(e)[:200]))
    page.on("console", lambda m: errs.append(m.type + ": " + m.text[:200]) if m.type == "error" else None)
    def leg_path():
        page.goto(FIX + "/", timeout=60000); page.wait_for_timeout(3000)
        page.locator("#userName").fill("Checker Five")
        page.locator("#entryForm button.enter").click(timeout=6000)
        page.wait_for_timeout(3000)
        after_login = page.evaluate(STATE)
        # click the walk page's ENTER button
        page.locator("#enterBtn").click(timeout=6000)
        page.wait_for_timeout(3000)
        after_enter_btn = page.evaluate(STATE)
        geo = page.evaluate(GEO_SWEEP)
        if "error" not in geo:
            page.evaluate("() => { const n = document.querySelector('#fpLegal .fp-legal-links'); if (n) n.scrollLeft = 0; }")
            page.wait_for_timeout(400)
            page.screenshot(path=CK + "/ck5-intro-real-s0.png")
            page.evaluate("() => { const n = document.querySelector('#fpLegal .fp-legal-links'); if (n) n.scrollLeft = n.scrollWidth; }")
            page.wait_for_timeout(400)
            page.screenshot(path=CK + "/ck5-intro-real-smax.png")
        return {"afterLoginEnter": after_login, "afterWalkEnterBtn": after_enter_btn,
                "geo": geo, "consoleErrors": errs}
    leg("intro-via-walk-enterBtn", leg_path)
    b.close()

    # ---- diagnostic fallback: cold `/`, call the exposed stage enter() ----
    b = pw.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, ignore_https_errors=True)
    page = ctx.new_page()
    errs2 = []
    page.on("pageerror", lambda e: errs2.append(str(e)[:200]))
    page.on("console", lambda m: errs2.append(m.type + ": " + m.text[:200]) if m.type == "error" else None)
    def leg_diag():
        page.goto(FIX + "/", timeout=60000); page.wait_for_timeout(3000)
        has = page.evaluate("() => !!window.__fpStage && typeof window.__fpStage.enter === 'function'")
        page.evaluate("() => window.__fpStage.enter()")
        page.wait_for_timeout(3000)
        st = page.evaluate(STATE)
        geo = page.evaluate(GEO_SWEEP)
        if "error" not in geo:
            page.evaluate("() => { const n = document.querySelector('#fpLegal .fp-legal-links'); if (n) n.scrollLeft = 0; }")
            page.wait_for_timeout(400)
            page.screenshot(path=CK + "/ck5-intro-diag-s0.png")
            page.evaluate("() => { const n = document.querySelector('#fpLegal .fp-legal-links'); if (n) n.scrollLeft = n.scrollWidth; }")
            page.wait_for_timeout(400)
            page.screenshot(path=CK + "/ck5-intro-diag-smax.png")
        return {"fpStageExposed": has, "afterDiagEnter": st, "geo": geo, "consoleErrors": errs2}
    leg("intro-diagnostic-enter", leg_diag)
    b.close()

with open(LOG, "w") as f:
    json.dump(out, f, indent=1)
for l in out["legs"]:
    print(json.dumps(l)[:1600], flush=True)
print("WROTE", LOG)
