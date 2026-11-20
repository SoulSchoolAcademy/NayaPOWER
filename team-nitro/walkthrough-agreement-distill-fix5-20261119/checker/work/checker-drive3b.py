#!/usr/bin/env python3
"""Fix-5 checker driver 3b — staged re-run with full diagnostics: record URL,
body classes, counter, and #fpLegal presence at each step; longer waits.
Writes checker-log3b.json."""
import json
from playwright.sync_api import sync_playwright

CK = "/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix5-20261119/checker"
STAGE = "https://naya-walk-beginning-staging.nayapower.workers.dev"
LOG = CK + "/checker-log3b.json"

GEO_SWEEP = r"""() => {
  const nav = document.querySelector('#fpLegal .fp-legal-links');
  if (!nav) return {error: 'no nav'};
  const cs = getComputedStyle(nav);
  const links = [...nav.querySelectorAll('a, button')].map(el => el.textContent.trim());
  const max = nav.scrollWidth - nav.clientWidth;
  const seen = links.map(() => null);
  const positions = [0];
  for (let s = 100; s < max; s += 100) positions.push(s);
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
  return {scrollWidth: nav.scrollWidth, clientWidth: nav.clientWidth, maxScroll: max,
    justifyContent: cs.justifyContent, linkCount: links.length,
    unreachable: reach.filter(r => !r.reachable).length, reachable: reach, at0First3: at0.slice(0, 3)};
}"""

out = {"label": "FIX5-CHECKER-DRIVE3B-STAGED", "legs": []}
with sync_playwright() as pw:
    b = pw.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, ignore_https_errors=True)
    page = ctx.new_page()
    errs = []
    page.on("pageerror", lambda e: errs.append(str(e)[:200]))
    page.on("console", lambda m: errs.append(m.type + ": " + m.text[:200]) if m.type == "error" else None)
    try:
        page.goto(STAGE + "/agreement", timeout=60000); page.wait_for_timeout(4000)
        diag0 = page.evaluate("() => ({url: location.href, title: document.title.slice(0,60), counter: (document.body.innerText.match(/(\\d+)\\s*\\/\\s*37/)||[])[0] || null, fpLegal: !!document.querySelector('#fpLegal'), bodyClass: document.body.className})")
        for i in range(40):
            if page.evaluate("() => [...document.querySelectorAll('button')].some(x=>x.offsetParent!==null && /I agree/i.test(x.innerText))"): break
            page.locator("button", has_text="Next").locator("visible=true").first.click(timeout=8000)
            page.wait_for_timeout(500)
        diag1 = page.evaluate("() => ({url: location.href, counter: (document.body.innerText.match(/(\\d+)\\s*\\/\\s*37/)||[])[0] || null, agreeVisible: [...document.querySelectorAll('button')].some(x=>x.offsetParent!==null && /I agree/i.test(x.innerText))})")
        page.locator("button", has_text="I agree").locator("visible=true").first.click(timeout=8000)
        page.wait_for_timeout(5000)
        diag2 = page.evaluate("() => ({url: location.href, bodyClass: document.body.className, fpLegal: !!document.querySelector('#fpLegal'), nav: !!document.querySelector('#fpLegal .fp-legal-links'), fpLegalDisplay: (() => { const f = document.querySelector('#fpLegal'); return f ? getComputedStyle(f).display : 'MISSING'; })()})")
        geo = page.evaluate(GEO_SWEEP)
        if "error" not in geo:
            page.evaluate("() => { const n = document.querySelector('#fpLegal .fp-legal-links'); if (n) n.scrollLeft = 0; }")
            page.wait_for_timeout(400)
            page.screenshot(path=CK + "/ck5-staged-bridge-s0.png")
        out["legs"].append({"leg": "staged-bridge-diag", "atLoad": diag0, "at37": diag1,
                            "afterAgree": diag2, "geo": geo, "consoleErrors": errs})
    except Exception as e:
        out["legs"].append({"leg": "staged-bridge-diag", "ERROR": str(e)[:600]})
    b.close()
with open(LOG, "w") as f:
    json.dump(out, f, indent=1)
for l in out["legs"]:
    print(json.dumps(l)[:1800], flush=True)
print("WROTE", LOG)
