#!/usr/bin/env python3
"""Fix-5 maker: prove defect F fixed on FIX5 bytes at 390x844 + F9 spot-check.
Same legs as the first attempt, but every leg is try/except-wrapped and
the log is written even if a leg fails. Door Continue is #doorContinue
(text "Continue to the walk"); the walk leg uses a fresh test alias.
Writes proof-fix5/fix5-verify.json.
"""
import json
from playwright.sync_api import sync_playwright

W = "/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work"
FIX = "http://127.0.0.1:18094"
LOG = W + "/proof-fix5/fix5-verify.json"

GEO_SWEEP = r"""() => {
  const nav = document.querySelector('#fpLegal .fp-legal-links');
  if (!nav) return {error: 'no nav'};
  const cs = getComputedStyle(nav);
  const navRect = nav.getBoundingClientRect();
  const links = [...nav.querySelectorAll('a, button')].map(el => el.textContent.trim());
  const max = nav.scrollWidth - nav.clientWidth;
  const seen = links.map(() => null);
  const positions = [0];
  for (let s = 100; s < max; s += 100) positions.push(s);
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
    linkCount: links.length, links, reachable,
    unreachableCount: reachable.filter(r => !r.reachable).length,
    at0: steps[0], atMax: steps[steps.length-1]
  };
}"""

DESK_GEO = r"""() => {
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
}"""

def counter(page):
    return page.evaluate("() => { const m = document.body.innerText.match(/(\\d+)\\s*\\/\\s*37/); return m ? m[0] : null; }")

def walk_to_end(page, end_re):
    seen = []
    for i in range(40):
        c = counter(page)
        if c: seen.append(c)
        if page.evaluate("() => [...document.querySelectorAll('button')].some(x=>x.offsetParent!==null && /" + end_re + "/i.test(x.innerText))"):
            break
        page.locator("button", has_text="Next").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(350)
    return seen

def run(pw):
    out = {"label": "FIX5", "legs": []}
    def leg(name, fn):
        try:
            out["legs"].append({"leg": name, **fn()})
        except Exception as e:
            out["legs"].append({"leg": name, "ERROR": str(e)[:500]})
            print("LEG FAIL", name, str(e)[:300], flush=True)

    # ---- 390: bridge footer geometry + screenshots ----
    b = pw.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, ignore_https_errors=True)
    page = ctx.new_page()
    errs = []
    page.on("pageerror", lambda e: errs.append(str(e)[:200]))
    page.on("console", lambda m: errs.append(m.type + ": " + m.text[:200]) if m.type == "error" else None)
    def leg1():
        page.goto(FIX + "/agreement", timeout=60000); page.wait_for_timeout(2000)
        walk_to_end(page, "I agree")
        page.locator("button", has_text="I agree").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(2500)
        bridge = page.evaluate(GEO_SWEEP)
        page.evaluate("() => { const n = document.querySelector('#fpLegal .fp-legal-links'); if (n) n.scrollLeft = 0; }")
        page.wait_for_timeout(400)
        page.screenshot(path=W + "/proof-fix5/fix5-bridge-s0.png")
        page.evaluate("() => { const n = document.querySelector('#fpLegal .fp-legal-links'); if (n) n.scrollLeft = n.scrollWidth; }")
        page.wait_for_timeout(400)
        page.screenshot(path=W + "/proof-fix5/fix5-bridge-smax.png")
        page.screenshot(path=W + "/proof-fix5/fix5-bridge-full.png")
        bridge["consoleErrors"] = errs
        return bridge
    leg("390-bridge-footer-geo", leg1)
    b.close()

    # ---- 390: F9 spot-check in one context ----
    b = pw.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, ignore_https_errors=True)
    page = ctx.new_page()
    errs2 = []
    page.on("pageerror", lambda e: errs2.append(str(e)[:200]))
    page.on("console", lambda m: errs2.append(m.type + ": " + m.text[:200]) if m.type == "error" else None)
    def leg_ident():
        page.goto(FIX + "/identity.html?name=Shawn&alias=Shawn", timeout=60000); page.wait_for_timeout(2500)
        return page.evaluate("() => { const inp = document.querySelector('input'); const hero = document.querySelector('#displayName'); return {input: inp ? inp.value : null, hero: hero ? hero.textContent.trim() : null, heroVisible: hero ? hero.offsetParent !== null : null}; }")
    leg("390-identity-paired", leg_ident)
    def leg_door():
        page.goto(FIX + "/welcome?name=Fix5%20Walk&alias=fix5walktest1", timeout=60000); page.wait_for_timeout(2000)
        steps0 = page.evaluate("() => [...document.querySelectorAll('[id^=step-]')].filter(e=>e.offsetParent!==null).map(e=>e.id)")
        page.wait_for_timeout(10000)
        steps10 = page.evaluate("() => [...document.querySelectorAll('[id^=step-]')].filter(e=>e.offsetParent!==null).map(e=>e.id)")
        return {"at0": steps0, "at10s": steps10, "held": steps0 == steps10}
    leg("390-door-10s-hold", leg_door)
    def leg_cont():
        page.locator("#doorContinue").click(timeout=6000)
        page.wait_for_timeout(1500)
        return {"visibleSteps": page.evaluate("() => [...document.querySelectorAll('[id^=step-]')].filter(e=>e.offsetParent!==null).map(e=>e.id)")}
    leg("390-door-continue", leg_cont)
    def leg_unfold():
        page.goto(FIX + "/agreement", timeout=60000); page.wait_for_timeout(2000)
        seen = walk_to_end(page, "I agree")
        return {"first": seen[:3], "last": seen[-3:], "count": len(seen),
                "sequential": seen == [f"{i} / 37" for i in range(1, len(seen)+1)]}
    leg("390-unfold-1-37", leg_unfold)
    def leg_agree_pair():
        page.locator("button", has_text="I agree").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(2500)
        return {"pair": page.evaluate("() => [...document.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>x.innerText.trim()).filter(t=>/Begin the visual story|Read the agreement/.test(t))")}
    leg("390-bridge-pair-after-agree", leg_agree_pair)
    def leg_begin():
        page.locator("button", has_text="Begin the visual story").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(2500)
        return {"counter": counter(page), "url": page.url}
    leg("390-pair-begin-deck", leg_begin)
    def leg_deck():
        seen = walk_to_end(page, "Enter NayaNET")
        return {"first": seen[:3], "last": seen[-3:], "count": len(seen),
                "sequential": seen == [f"{i} / 37" for i in range(1, len(seen)+1)]}
    leg("390-deck-1-37", leg_deck)
    def leg_deck_enter():
        page.locator("button", has_text="Enter NayaNET").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(2500)
        return {"url": page.url,
            "pair": page.evaluate("() => [...document.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>x.innerText.trim()).filter(t=>/Begin the visual story|Read the agreement/.test(t))")}
    leg("390-deck-enter-bridge", leg_deck_enter)
    def leg_read():
        page.locator("button", has_text="Read the agreement").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(2500)
        return {"counter": counter(page), "url": page.url}
    leg("390-pair-read-agreement", leg_read)
    def leg_letter():
        page.goto(FIX + "/?stage=letter", timeout=60000); page.wait_for_timeout(2500)
        seen = walk_to_end(page, "I agree")
        return {"first": seen[:3], "last": seen[-3:], "count": len(seen),
                "sequential": seen == [f"{i} / 37" for i in range(1, len(seen)+1)]}
    leg("390-letter-1-37", leg_letter)
    def leg_letter_agree():
        page.locator("button", has_text="I agree").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(2500)
        return {"url": page.url}
    leg("390-letter-agree-bridge", leg_letter_agree)
    out["legs"].append({"leg": "390-f9-console-errors", "errors": errs2})
    b.close()

    # ---- 1920 desktop ----
    b = pw.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=1, ignore_https_errors=True)
    page = ctx.new_page()
    errs3 = []
    page.on("pageerror", lambda e: errs3.append(str(e)[:200]))
    page.on("console", lambda m: errs3.append(m.type + ": " + m.text[:200]) if m.type == "error" else None)
    def leg_desk_geo():
        page.goto(FIX + "/?stage=bridge", timeout=60000); page.wait_for_timeout(2500)
        d = page.evaluate(DESK_GEO)
        page.screenshot(path=W + "/proof-fix5/fix5-1920-bridge.png")
        return d
    leg("1920-bridge-footer-geo", leg_desk_geo)
    def leg_desk_ident():
        page.goto(FIX + "/identity.html?name=Shawn&alias=Shawn", timeout=60000); page.wait_for_timeout(2500)
        return page.evaluate("() => { const inp = document.querySelector('input'); const hero = document.querySelector('#displayName'); const r = hero ? hero.getBoundingClientRect() : null; return {input: inp ? inp.value : null, hero: hero ? hero.textContent.trim() : null, heroRect: r ? [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)] : null}; }")
    leg("1920-identity-paired", leg_desk_ident)
    def leg_desk_unfold():
        page.goto(FIX + "/agreement", timeout=60000); page.wait_for_timeout(2000)
        walk_to_end(page, "I agree")
        t = page.evaluate("() => { const el = [...document.querySelectorAll('.frame-title, .ib-title')].find(e=>e.offsetParent!==null && /Congratulations/.test(e.textContent)); if (!el) return null; const r = el.getBoundingClientRect(); return {font: getComputedStyle(el).fontSize, rect: [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]}; }")
        page.screenshot(path=W + "/proof-fix5/fix5-1920-unfold37.png")
        return t or {"ERROR": "no Congratulations title found"}
    leg("1920-unfold-board37", leg_desk_unfold)
    out["legs"].append({"leg": "1920-console-errors", "errors": errs3})
    b.close()
    return out

with sync_playwright() as pw:
    try:
        res = run(pw)
    except Exception as e:
        res = {"label": "FIX5", "legs": [], "RUN_ERROR": str(e)[:500]}
        print("RUN ERROR", str(e)[:500], flush=True)
with open(LOG, "w") as f:
    json.dump(res, f, indent=1)
for leg in res["legs"]:
    print(json.dumps(leg)[:1100], flush=True)
print("WROTE", LOG)
