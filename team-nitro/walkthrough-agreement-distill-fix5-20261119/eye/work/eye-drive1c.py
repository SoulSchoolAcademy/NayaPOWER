#!/usr/bin/env python3
"""Captain's eye fix-5 — drive 1c: bridge strip re-run at 390 with a real wait for
#fpLegal (drive 1b hit 'no nav' because the bridge stage JS had not rendered it
within 2500ms on the remote host). Writes eye-log1c.json."""
import json, time
from playwright.sync_api import sync_playwright

BASE = "https://naya-walk-beginning-staging.nayapower.workers.dev"
EYE = "/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix5-20261119/eye"
LOGP = EYE + "/eye-log1c.json"

GEO_SWEEP = r"""() => {
  const nav = document.querySelector('#fpLegal .fp-legal-links');
  if (!nav) return {error: 'no nav'};
  const cs = getComputedStyle(nav);
  const nr = nav.getBoundingClientRect();
  const links = [...nav.querySelectorAll('a, button')].map(el => el.textContent.trim());
  const max = nav.scrollWidth - nav.clientWidth;
  const seenVP = links.map(() => null);
  const seenStrip = links.map(() => null);
  const positions = [0];
  for (let s = 50; s < max; s += 50) positions.push(s);
  if (max > 0) positions.push(max);
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
  }
  nav.scrollLeft = 0;
  const reachVP = seenVP.map((s, i) => ({link: links[i], reachable: s !== null, at: s}));
  const reachStrip = seenStrip.map((s, i) => ({link: links[i], reachable: s !== null, at: s}));
  return {navRect: [Math.round(nr.left), Math.round(nr.top), Math.round(nr.right), Math.round(nr.bottom)],
    scrollWidth: nav.scrollWidth, clientWidth: nav.clientWidth, maxScroll: max,
    justifyContent: cs.justifyContent, flexWrap: cs.flexWrap, overflowX: cs.overflowX,
    linkCount: links.length, links,
    reachableViewport: reachVP, unreachableViewport: reachVP.filter(r => !r.reachable).length,
    reachableStrip: reachStrip, unreachableStrip: reachStrip.filter(r => !r.reachable).length};
}"""

def counter(page):
    return page.evaluate("() => { const m = document.body.innerText.match(/(\\d+)\\s*\\/\\s*37/); return m ? m[0] : null; }")

def settle_counter(page, timeout=3000):
    end = time.time() + timeout / 1000
    last = None; stable = 0
    while time.time() < end:
        c = counter(page)
        if c is not None and c == last:
            stable += 1
            if stable >= 2: return c
        else:
            stable = 0
        last = c
        page.wait_for_timeout(120)
    return last

out = {"label": "EYE-FIX5-BRIDGE-RERUN-390", "legs": []}
with sync_playwright() as pw:
    b = pw.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, ignore_https_errors=True)
    page = ctx.new_page()
    errs = []
    page.on("pageerror", lambda e: errs.append("pageerror: " + str(e)[:200]))
    page.on("console", lambda m: errs.append("console." + m.type + ": " + m.text[:200]) if m.type == "error" else None)
    try:
        page.goto(BASE + "/agreement", timeout=60000); page.wait_for_timeout(2000)
        seen = []
        for i in range(45):
            c = settle_counter(page)
            if c and (not seen or seen[-1] != c): seen.append(c)
            if page.evaluate("() => [...document.querySelectorAll('button')].some(x=>x.offsetParent!==null && /I agree/i.test(x.innerText))"): break
            page.locator("button", has_text="Next").locator("visible=true").first.click(timeout=5000)
            page.wait_for_timeout(350)
        out["legs"].append({"leg": "unfold-1-37", "seenCount": len(seen), "first": seen[:2], "last": seen[-2:],
                            "sequential": seen == [f"{n} / 37" for n in range(1, len(seen) + 1)]})
        page.locator("button", has_text="I agree").locator("visible=true").first.click(timeout=5000)
        t0 = time.time()
        page.wait_for_selector("#fpLegal .fp-legal-links", state="attached", timeout=15000)
        waited = round(time.time() - t0, 1)
        page.wait_for_timeout(800)
        geo = page.evaluate(GEO_SWEEP)
        page.evaluate("() => { const n = document.querySelector('#fpLegal .fp-legal-links'); if (n) n.scrollLeft = 0; }")
        page.wait_for_timeout(400)
        page.screenshot(path=EYE + "/eye-26-bridge-s0.png")
        page.evaluate("() => { const n = document.querySelector('#fpLegal .fp-legal-links'); if (n) n.scrollLeft = n.scrollWidth; }")
        page.wait_for_timeout(400)
        page.screenshot(path=EYE + "/eye-27-bridge-smax.png")
        out["legs"].append({"leg": "F-bridge-real-tap-rerun", "url": page.url,
                            "waitForNavSeconds": waited, "F-bridge": geo})
    except Exception as e:
        out["legs"].append({"leg": "bridge-rerun", "ERROR": str(e)[:600]})
    out["legs"].append({"leg": "390-console-errors-drive1c", "errors": errs})
    b.close()

with open(LOGP, "w") as f:
    json.dump(out, f, indent=1)
print("WROTE", LOGP)
for l in out["legs"]:
    print(json.dumps(l)[:1200], flush=True)
