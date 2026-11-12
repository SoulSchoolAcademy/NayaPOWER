#!/usr/bin/env python3
"""NEW-ACCOUNT BUG repro (Shawn 22:36Z) — BEFORE any fix.
Returning-browser context (persistent Firefox profile): claim a stored
identity first (bugowner7, full walk so the reveal exists), then, in the
SAME browser, enter a NEW name (Mike) + Create a new account, and record
what the certificate shows. Defect = certificate shows the OLD profile
(name, welcome back, Nº, no alias field) instead of the new name.
Writes bug-repro-*.png + bug-repro-results.json into the work dir.
"""
import json
import subprocess
import time
from playwright.sync_api import sync_playwright

BASE = "https://naya-walk-beginning-staging.nayapower.workers.dev"
OUT = "/home/hatch/workspace/team-nitro/walk-s2-box-pages-20261112/"
PROFILE = "/tmp/bug-profile-bugowner7"
R = {"pass": [], "fail": [], "notes": []}

def dump():
    R["notes"] = [f"pass={len(R['pass'])} fail={len(R['fail'])}"]
    json.dump(R, open(OUT + "bug-repro-results.json", "w"), indent=2)

def check(name, ok, detail=""):
    (R["pass"] if ok else R["fail"]).append(name + (" :: " + str(detail) if detail else ""))
    try:
        dump()
    except Exception:
        pass

def dismiss_veil(pg):
    try:
        pg.wait_for_selector("#installLater:visible", timeout=8000)
        pg.locator("#installLater").click()
        pg.wait_for_timeout(500)
        return True
    except Exception:
        return False

ANS = {
    1: "I am a baker from the valley, growing food for my neighbours.",
    2: "I am into growing food and sharing the harvest.",
    3: "A street where every garden feeds a family.",
    4: "To turn ten front gardens into food gardens this year.",
    5: "Grow a little every day.",
    6: "To own a small farm and teach children to grow food.",
    7: "I grow vegetables and sell boxes of fresh food each week.",
    8: "A weekly box of fresh vegetables, picked the same morning.",
    9: "I am building a market garden. The goal is fifty weekly boxes.",
    10: "A garden room for growers and cooks, where we swap seeds and recipes.",
}

with sync_playwright() as pw:
    ctx = pw.firefox.launch_persistent_context(
        PROFILE, viewport={"width": 1440, "height": 900})
    pg = ctx.new_page()
    errs, perrs = [], []
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: perrs.append(str(e)))

    # ---- STEP 1: claim the stored identity in this profile ----
    pg.goto(BASE + "/", wait_until="networkidle")
    pg.wait_for_timeout(1000)
    check("repro setup: fresh entry dial (one input)", pg.locator("input").count() == 1)
    pg.fill("#userName", "Bug Owner")
    pg.locator("button.enter[type='submit']").click()
    pg.wait_for_url("**/identity.html**", timeout=15000)
    check("repro setup: entry lands on certificate", True, pg.url)
    dismiss_veil(pg)
    pg.fill("#aliasInput", "bugowner7")
    pg.locator("#enterBtn").click()
    try:
        pg.wait_for_url("**/welcome**", timeout=25000)
        check("repro setup: claim lands on the walk", True, pg.url)
    except Exception as e:
        check("repro setup: claim lands on the walk", False, f"{pg.url} :: {str(e)[:120]}")
        pg.screenshot(path=OUT + "bug-repro-claim-stuck.png")
        raise SystemExit(1)
    pg.wait_for_timeout(1200)
    check("repro setup: Q1 shown", pg.locator("#step-1").is_visible())
    for n in range(1, 11):
        pg.fill(f"#answer-{n}", ANS[n])
        pg.click(f"#enterBtn-{n}")
        nxt = f"#step-{n+1}" if n < 10 else "#step-names"
        pg.wait_for_selector(nxt + ":visible", timeout=9000)
    check("repro setup: ten answers walked", True)
    pg.fill("#name-business", "Bug Bakery")
    pg.fill("#name-space", "Bug Garden")
    pg.wait_for_timeout(300)
    pg.click("#enterBtn-11")
    pg.wait_for_selector("text=Done — here are your pages.", timeout=25000)
    check("repro setup: building done (reveal exists)", True)
    pg.click("#buildGo")
    pg.wait_for_selector("#step-end:visible", timeout=9000)
    check("repro setup: stored citizen reaches the end slide", pg.locator("#step-end").is_visible())
    stored = pg.evaluate("JSON.stringify({alias: localStorage.getItem('nayanet_smart_alias'), name: localStorage.getItem('nayanet_smart_name'), key: !!localStorage.getItem('nayanet_vault_key')})")
    check("repro setup: stored identity in this browser", True, stored)
    pg.screenshot(path=OUT + "bug-repro-stored-end.png")

    # ---- STEP 2: the returning-browser new-account path ----
    pg.goto(BASE + "/", wait_until="networkidle")
    pg.wait_for_timeout(1200)
    check("repro: returning view shown (stored profile present)",
          pg.locator("#returningView").is_visible() and pg.locator("#entryForm").is_hidden())
    pg.screenshot(path=OUT + "bug-repro-returning.png")
    pg.locator("#newAccountLine").click()
    pg.wait_for_timeout(500)
    check("repro: Create a new account reveals the dial",
          pg.locator("#entryForm").is_visible() and pg.locator("#returningView").is_hidden())
    pg.fill("#userName", "Mike")
    pg.locator("button.enter[type='submit']").click()
    try:
        pg.wait_for_url("**/identity.html**", timeout=15000)
    except Exception as e:
        check("repro: new name lands on certificate", False, f"{pg.url} :: {str(e)[:120]}")
        raise SystemExit(1)
    pg.wait_for_timeout(2500)  # let the silent restore answer
    dismiss_veil(pg)
    pg.wait_for_timeout(1500)
    url = pg.url
    cert = pg.evaluate("""() => {
      const q = s => { const el = document.querySelector(s); return el ? el.innerText : 'MISSING:' + s; };
      const vis = s => { const el = document.querySelector(s); if (!el) return 'MISSING'; const cs = getComputedStyle(el); return cs.display === 'none' || el.hidden ? 'hidden' : 'visible'; };
      return {
        url: location.href,
        displayName: q('#displayName'),
        status: q('#aliasStatus'),
        certNo: q('#certNoValue'),
        link: q('#displayLink'),
        plaqueCertified: (document.querySelector('#certPlaque') || {classList:{contains:()=>false}}).classList.contains('is-certified'),
        aliasFieldWrapper: vis('.alias-field-wrapper'),
        aliasInputVisible: vis('#aliasInput'),
        aliasInputValue: (document.querySelector('#aliasInput') || {}).value,
      };
    }""")
    print("CERT STATE:", json.dumps(cert, indent=2))
    check("repro: certificate URL carries the new name whole",
          "name=Mike" in url, url)
    pg.screenshot(path=OUT + "bug-repro-cert-shows-old.png")
    # THE DEFECT: old profile painted, no alias field
    check("DEFECT reproduced: certificate shows the OLD name, not Mike",
          cert["displayName"].strip() == "Bug Owner", str(cert))
    check("DEFECT reproduced: status says welcome back (old profile)",
          "welcome back" in cert["status"], cert["status"])
    check("DEFECT reproduced: old certificate number painted",
          cert["certNo"].strip() != "", cert["certNo"])
    check("DEFECT reproduced: NO alias field to fill in",
          cert["aliasFieldWrapper"] == "hidden" or cert["aliasInputVisible"] == "hidden", str(cert))
    # Enter with the empty alias jumps straight to the old citizen's end slide
    pg.locator("#enterBtn").click()
    try:
        pg.wait_for_url("**/welcome**", timeout=15000)
    except Exception:
        pass
    pg.wait_for_timeout(1500)
    check("DEFECT reproduced: Enter jumps straight to the end slide (no ten questions)",
          pg.locator("#step-end").is_visible(), pg.url)
    pg.screenshot(path=OUT + "bug-repro-end-slide-jump.png")
    check("repro console errors", len(errs) == 0, f"{len(errs)}: {errs[:3]}")
    check("repro pageerrors", len(perrs) == 0, f"{len(perrs)}: {perrs[:3]}")
    ctx.close()

R["notes"] = [f"pass={len(R['pass'])} fail={len(R['fail'])}"]
json.dump(R, open(OUT + "bug-repro-results.json", "w"), indent=2)
print(f"PASS {len(R['pass'])} / FAIL {len(R['fail'])}")
for f in R["fail"]:
    print("FAIL:", f)
for p_ in R["pass"]:
    print("PASS:", p_)
