#!/usr/bin/env python3
"""Fix-5 checker driver 2b — re-prove unfold 1->37 sequential with
change-detection, and measure the board-37 orb/photo clearance with VISIBLE
elements only (driver 2's .frame-icon/.fp-speak-face selectors hit zero-rect
hidden copies). Writes checker-log2b.json."""
import json
from playwright.sync_api import sync_playwright

CK = "/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix5-20261119/checker"
FIX = "http://127.0.0.1:18096"
LOG = CK + "/checker-log2b.json"

def counter(page):
    return page.evaluate("() => { const m = document.body.innerText.match(/(\\d+)\\s*\\/\\s*37/); return m ? m[0] : null; }")

CLEAR = r"""() => {
  const R = el => { const r = el.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]; };
  const vis = sel => [...document.querySelectorAll(sel)].filter(e => e.offsetParent !== null);
  const titles = vis('.frame-title, .ib-title').filter(e => /Congratulations/.test(e.textContent));
  const t = titles[0] || null;
  const range = document.createRange(); const byTop = {};
  if (t) { const walk = document.createTreeWalker(t, NodeFilter.SHOW_TEXT); let node;
    while ((node = walk.nextNode())) { for (let i = 0; i < node.textContent.length; i++) {
      range.setStart(node, i); range.setEnd(node, i + 1); const r = range.getBoundingClientRect();
      if (r.width > 0 && r.height > 0) { const tt = Math.round(r.top); byTop[tt] = byTop[tt] || [Math.round(r.left), tt, Math.round(r.right), Math.round(r.bottom)]; byTop[tt][0] = Math.min(byTop[tt][0], Math.round(r.left)); byTop[tt][2] = Math.max(byTop[tt][2], Math.round(r.right)); } } } }
  const lines = Object.values(byTop);
  const cands = ['.frame-icon', '.deal-beat-photo', '.fp-speak-face', '.deal-seal', '[class*=orb]', '.fp-agree-logo']
    .flatMap(sel => vis(sel).map(e => ({sel, cls: e.className.toString().slice(0, 40), rect: R(e)})))
    .filter(c => c.rect[2] > c.rect[0] && c.rect[3] > c.rect[1]);
  return {titleFont: t ? getComputedStyle(t).fontSize : null, titleRect: t ? R(t) : null,
    titleLines: lines, visibleCandidates: cands};
}"""

out = {"label": "FIX5-CHECKER-DRIVE2B", "legs": []}
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

    def leg_unfold_seq():
        page.goto(FIX + "/agreement", timeout=60000); page.wait_for_timeout(2000)
        seen = []
        prev = None
        for i in range(45):
            c = counter(page)
            if c != prev:
                seen.append(c); prev = c
            if page.evaluate("() => [...document.querySelectorAll('button')].some(x=>x.offsetParent!==null && /I agree/i.test(x.innerText))"):
                break
            # wait for the counter to change after the click
            before = counter(page)
            page.locator("button", has_text="Next").locator("visible=true").first.click(timeout=5000)
            for _ in range(20):
                page.wait_for_timeout(150)
                if counter(page) != before: break
        return {"seen": seen, "count": len(seen),
                "sequential": seen == [f"{i} / 37" for i in range(1, 38)]}
    leg("unfold-1-37-sequential", leg_unfold_seq)
    def leg_unfold_clear():
        return page.evaluate(CLEAR)
    leg("D-unfold37-clearance-visible", leg_unfold_clear)
    def leg_to_bridge():
        page.locator("button", has_text="I agree").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(2500)
        page.locator("button", has_text="Begin the visual story").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(2500)
        return {"counter": counter(page), "url": page.url}
    leg("bridge-begin-deck", leg_to_bridge)
    def leg_deck_walk():
        seen = []
        prev = None
        for i in range(45):
            c = counter(page)
            if c != prev:
                seen.append(c); prev = c
            vis = page.evaluate("() => !!document.querySelector('#fpNextBtn') && document.querySelector('#fpNextBtn').offsetParent!==null")
            if not vis: break
            txt = page.evaluate("() => document.querySelector('#fpNextBtn').innerText.trim()")
            if any(k in txt for k in ("Enter NayaNET", "I agree", "Read the Collective")): break
            page.locator("#fpNextBtn").click(timeout=6000)
            page.wait_for_timeout(450)
        return {"seenCount": len(seen), "sequential": seen == [f"{i} / 37" for i in range(1, 38)], "last": seen[-3:]}
    leg("deck-1-37-sequential", leg_deck_walk)
    def leg_deck_clear():
        return page.evaluate(CLEAR)
    leg("D-E-deck37-clearance-visible", leg_deck_clear)
    def leg_letter_walk():
        page.goto(FIX + "/?stage=letter", timeout=60000); page.wait_for_timeout(2500)
        seen = []
        prev = None
        for i in range(45):
            c = counter(page)
            if c != prev:
                seen.append(c); prev = c
            vis = page.evaluate("() => !!document.querySelector('#fpNextBtn') && document.querySelector('#fpNextBtn').offsetParent!==null")
            if not vis: break
            txt = page.evaluate("() => document.querySelector('#fpNextBtn').innerText.trim()")
            if any(k in txt for k in ("Enter NayaNET", "I agree", "Read the Collective")): break
            page.locator("#fpNextBtn").click(timeout=6000)
            page.wait_for_timeout(450)
        return {"seenCount": len(seen), "sequential": seen == [f"{i} / 37" for i in range(1, 38)], "last": seen[-3:]}
    leg("letter-1-37-sequential", leg_letter_walk)
    def leg_letter_clear():
        return page.evaluate(CLEAR)
    leg("D-E-letter37-clearance-visible", leg_letter_clear)
    out["legs"].append({"leg": "390-console-errors", "errors": errs})
    b.close()

with open(LOG, "w") as f:
    json.dump(out, f, indent=1)
for l in out["legs"]:
    print(json.dumps(l)[:1400], flush=True)
print("WROTE", LOG)
