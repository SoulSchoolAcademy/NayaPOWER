#!/usr/bin/env python3
"""Fix-5 maker: re-prove deck/letter F9 legs, corrected driver.
Deck/letter advance via #fpNextBtn whose OWN text becomes the end label
("Enter NayaNET ->" / "I agree") at the last board — the end button is
visible-but-covered from the start, so checking any-button visibility
breaks the walk at 1/37. The end click waits for the #fpNHold overlay
to clear first.
Writes proof-fix5/fix5-f9-deck-letter2.json.
"""
import json
from playwright.sync_api import sync_playwright

W = "/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work"
FIX = "http://127.0.0.1:18094"
LOG = W + "/proof-fix5/fix5-f9-deck-letter2.json"

def counter(page):
    return page.evaluate("() => { const m = document.body.innerText.match(/(\\d+)\\s*\\/\\s*37/); return m ? m[0] : null; }")

def next_label(page):
    return page.evaluate("() => { const n = document.querySelector('#fpNextBtn'); return n ? n.innerText.trim() : null; }")

def stage_walk(page, end_re, label):
    seen = []
    for i in range(45):
        lbl = next_label(page)
        c = counter(page)
        if c: seen.append(c)
        if lbl and __import__("re").search(end_re, lbl, __import__("re").I):
            break
        if not lbl:
            break
        page.locator("#fpNextBtn").click(timeout=6000)
        page.wait_for_timeout(450)
    return {"label": label, "first": seen[:3], "last": seen[-3:], "count": len(seen),
            "sequential": seen == [f"{i} / 37" for i in range(1, len(seen)+1)],
            "nextBtnAtEnd": next_label(page)}

def bridge_pair(page):
    return page.evaluate("() => [...document.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>x.innerText.trim()).filter(t=>/Begin the visual story|Read the agreement/.test(t))")

def hold_state(page):
    return page.evaluate("() => { const h = document.querySelector('#fpNHold'); if (!h) return 'NO-HOLD-ELEMENT'; const r = h.getBoundingClientRect(); const cs = getComputedStyle(h); return {visible: h.offsetParent!==null, display: cs.display, rect: [Math.round(r.left), Math.round(r.top), Math.round(r.right), Math.round(r.bottom)]}; }")

def run(pw):
    out = {"label": "FIX5-F9-deck-letter-2", "legs": []}
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
        return {"pair": bridge_pair(page)}
    leg("390-agree-pair", leg_agree)
    def leg_begin():
        page.locator("button", has_text="Begin the visual story").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(2500)
        return {"counter": counter(page), "url": page.url, "nextBtn": next_label(page)}
    leg("390-pair-begin-deck", leg_begin)
    def leg_deck():
        return stage_walk(page, "Enter NayaNET", "390-deck-1-37")
    leg("390-deck-1-37", leg_deck)
    def leg_deck_enter():
        h0 = hold_state(page)
        page.wait_for_timeout(4000)
        h1 = hold_state(page)
        page.locator("button", has_text="Enter NayaNET").locator("visible=true").first.click(timeout=8000)
        page.wait_for_timeout(2500)
        return {"url": page.url, "holdBefore": h0, "holdAfterWait": h1, "pair": bridge_pair(page)}
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
        page.wait_for_timeout(4000)
        page.locator("button", has_text="I agree").locator("visible=true").first.click(timeout=8000)
        page.wait_for_timeout(2500)
        return {"url": page.url, "pair": bridge_pair(page),
                "agreedMarker": page.evaluate("() => /AGREED/.test(document.body.innerText)")}
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
