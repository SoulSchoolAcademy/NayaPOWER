#!/usr/bin/env python3
"""Fix-5 maker: F9 deck/letter end legs, third attempt with the checker's
exact click_next_or_end pattern: at board 37 #fpNextBtn BECOMES the end
button; wait for the #fpNHold overlay to clear, then click #fpNextBtn
itself (fall back to a stage-bar button). After the deck end click an
end card may offer a second "Enter NayaNET" button — tap it too.
Writes proof-fix5/fix5-f9-deck-letter3.json.
"""
import json, time
from playwright.sync_api import sync_playwright

W = "/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix5-20261119/maker/work"
FIX = "http://127.0.0.1:18094"
LOG = W + "/proof-fix5/fix5-f9-deck-letter3.json"

def counter(page):
    return page.evaluate("() => { const m = document.body.innerText.match(/(\\d+)\\s*\\/\\s*37/); return m ? m[0] : null; }")

def bridge_pair(page):
    return page.evaluate("() => [...document.querySelectorAll('button')].filter(x=>x.offsetParent!==null).map(x=>x.innerText.trim()).filter(t=>/Begin the visual story|Read the agreement/.test(t))")

def click_next_or_end(page):
    btn = page.locator("#fpNextBtn")
    txt = page.evaluate("() => { const b=document.querySelector('#fpNextBtn'); return b ? b.innerText.trim() : ''; }")
    is_end = any(k in txt for k in ("Enter NayaNET", "I agree", "Read the Collective"))
    hold_cleared = None
    if is_end:
        hold_cleared = False
        for _ in range(30):
            hold = page.evaluate("() => { const h=document.querySelector('#fpNHold'); return h ? (!h.hidden && h.offsetParent!==null) : false; }")
            if not hold:
                hold_cleared = True
                break
            page.wait_for_timeout(500)
    try:
        btn.click(timeout=6000)
        return {"via": "fpNextBtn", "btnText": txt, "holdCleared": hold_cleared}
    except Exception:
        btns = page.evaluate("() => [...document.querySelectorAll('#fpStageBarB button, #fpStageBarT button')].filter(x=>x.offsetParent!==null).map(x=>({id:x.id, t:x.innerText.trim().slice(0,40)}))")
        for bb in btns:
            if bb["id"] not in ("fpDeckBack", "fpStageExit"):
                page.locator("#" + bb["id"]).click(timeout=6000)
                return {"via": "stagebar:" + bb["id"], "btnText": txt, "holdCleared": hold_cleared}
        raise

def stage_walk(page, label):
    counters = []
    for i in range(42):
        counters.append(counter(page))
        vis = page.evaluate("() => !!document.querySelector('#fpNextBtn') && document.querySelector('#fpNextBtn').offsetParent!==null")
        if not vis:
            break
        txt = page.evaluate("() => document.querySelector('#fpNextBtn').innerText.trim()")
        if any(k in txt for k in ("Enter NayaNET", "I agree", "Read the Collective")):
            break
        page.locator("#fpNextBtn").click(timeout=6000)
        page.wait_for_timeout(450)
    counters = [c for c in counters if c]
    return {"label": label, "first": counters[:3], "last": counters[-3:], "count": len(counters),
            "sequential": counters == [f"{i} / 37" for i in range(1, len(counters)+1)],
            "nextBtnAtEnd": page.evaluate("() => { const b=document.querySelector('#fpNextBtn'); return b ? b.innerText.trim() : null; }")}

def run(pw):
    out = {"label": "FIX5-F9-deck-letter-3", "legs": []}
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
        return {"counter": counter(page), "url": page.url}
    leg("390-pair-begin-deck", leg_begin)
    def leg_deck():
        return stage_walk(page, "390-deck-1-37")
    leg("390-deck-1-37", leg_deck)
    def leg_deck_end():
        r = click_next_or_end(page)
        page.wait_for_timeout(3000)
        second = None
        try:
            loc = page.locator("button", has_text="Enter NayaNET").locator("visible=true").first
            loc.wait_for(state="visible", timeout=5000)
            loc.scroll_into_view_if_needed(timeout=5000)
            loc.click(timeout=5000)
            page.wait_for_timeout(3000)
            second = "tapped-second-enter"
        except Exception as e:
            second = "no-second-enter: " + str(e)[:120]
        return {"endClick": r, "secondEnter": second, "url": page.url, "pair": bridge_pair(page)}
    leg("390-deck-enter-bridge", leg_deck_end)
    def leg_read():
        page.locator("button", has_text="Read the agreement").locator("visible=true").first.click(timeout=5000)
        page.wait_for_timeout(2500)
        return {"counter": counter(page), "url": page.url}
    leg("390-pair-read-agreement", leg_read)
    def leg_letter():
        page.goto(FIX + "/?stage=letter", timeout=60000); page.wait_for_timeout(2500)
        return stage_walk(page, "390-letter-1-37")
    leg("390-letter-1-37", leg_letter)
    def leg_letter_end():
        r = click_next_or_end(page)
        page.wait_for_timeout(3000)
        return {"endClick": r, "url": page.url, "pair": bridge_pair(page),
                "agreedMarker": page.evaluate("() => /AGREED/.test(document.body.innerText)")}
    leg("390-letter-agree-bridge", leg_letter_end)
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
