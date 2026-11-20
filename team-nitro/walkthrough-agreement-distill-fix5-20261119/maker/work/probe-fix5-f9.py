#!/usr/bin/env python3
"""Fix-5 maker: re-prove the deck/letter F9 legs that failed on my first
driver's button-text assumption (deck/letter advance via #fpNextBtn, not
a "Next"-text button — the checker's stage_walk pattern).
One 390 context: agree via /agreement -> bridge pair -> Begin -> deck
1->37 -> Enter NayaNET -> bridge -> Read the agreement -> /agreement 1/37;
then /?stage=letter 1->37 -> I agree -> bridge.
Writes proof-fix5/fix5-f9-deck-letter.json.
"""
import json
from playwright.sync_api import sync_playwright

W = "/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work"
FIX = "http://127.0.0.1:18094"
LOG = W + "/proof-fix5/fix5-f9-deck-letter.json"

def counter(page):
    return page.evaluate("() => { const m = document.body.innerText.match(/(\\d+)\\s*\\/\\s*37/); return m ? m[0] : null; }")

def stage_walk(page, end_re, label):
    """Click #fpNextBtn until a button matching end_re is visible; return counters seen."""
    seen = []
    for i in range(42):
        vis = page.evaluate("() => !!document.querySelector('#fpNextBtn') && document.querySelector('#fpNextBtn').offsetParent!==null")
        if not vis:
            break
        if page.evaluate("() => [...document.querySelectorAll('button')].some(x=>x.offsetParent!==null && /" + end_re + "/i.test(x.innerText))"):
            break
        c = counter(page)
        if c: seen.append(c)
        page.locator("#fpNextBtn").click(timeout=6000)
        page.wait_for_timeout(450)
    c = counter(page)
    if c: seen.append(c)
    return {"label": label, "first": seen[:3], "last": seen[-3:], "count": len(seen),
            "sequential": seen == [f"{i} / 37" for i in range(1, len(seen)+1)],
            "endVisible": page.evaluate("() => [...document.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>x.innerText.trim()).filter(t=>/" + end_re + "/i.test(t))")}

def run(pw):
    out = {"label": "FIX5-F9-deck-letter", "legs": []}
    def leg(name, fn):
        try:
            out["legs"].append({"leg": name, **fn()})
        except Exception as e:
            out["legs"].append({"leg": name, "ERROR": str(e)[:500]})
            print("LEG FAIL", name, str(e)[:300], flush=True)
    b = pw.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, ignore_https_errors=True)
    page = ctx.new_page()
    errs = []
    page.on("pageerror", lambda e: errs.append(str(e)[:200]))
    page.on("console", lambda m: errs.append(m.type + ": " + m.text[:200]) if m.type == "error" else None)
    def leg_agree():
        page.goto(FIX + "/agreement", timeout=60000); page.wait_for_timeout(2000)
        for i in range(40):
            if page.evaluate("() => [...document.querySelectorAll('button')].some(x=>x.offsetParent!==null && /I agree/i.test(x.innerText))"):
                break
            page.locator("button", has_text="Next").locator("visible=true").first.click(timeout=5000)
            page.wait_for_timeout(350)
        page.locator("button", has_text="I agree").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(2500)
        return {"pair": page.evaluate("() => [...document.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>x.innerText.trim()).filter(t=>/Begin the visual story|Read the agreement/.test(t))")}
    leg("390-agree-pair", leg_agree)
    def leg_begin():
        page.locator("button", has_text="Begin the visual story").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(2500)
        return {"counter": counter(page), "url": page.url,
                "nextBtn": page.evaluate("() => { const n = document.querySelector('#fpNextBtn'); return n ? {visible: n.offsetParent!==null, text: n.innerText.trim()} : 'MISSING'; }")}
    leg("390-pair-begin-deck", leg_begin)
    def leg_deck():
        return stage_walk(page, "Enter NayaNET", "390-deck-1-37")
    leg("390-deck-1-37", leg_deck)
    def leg_deck_enter():
        page.wait_for_timeout(1500)  # fpNHold overlay clears after a short hold
        page.locator("button", has_text="Enter NayaNET").locator("visible=true").first.click(timeout=8000)
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
        return stage_walk(page, "I agree", "390-letter-1-37")
    leg("390-letter-1-37", leg_letter)
    def leg_letter_agree():
        page.wait_for_timeout(1500)
        page.locator("button", has_text="I agree").locator("visible=true").first.click(timeout=8000)
        page.wait_for_timeout(2500)
        return {"url": page.url}
    leg("390-letter-agree-bridge", leg_letter_agree)
    out["legs"].append({"leg": "390-console-errors", "errors": errs})
    b.close()
    return out

with sync_playwright() as pw:
    res = run(pw)
with open(LOG, "w") as f:
    json.dump(res, f, indent=1)
for leg in res["legs"]:
    print(json.dumps(leg)[:900], flush=True)
print("WROTE", LOG)
