#!/usr/bin/env python3
"""Fix-5 checker driver 2c — unfold 1->37 with stabilize-wait: after each click,
wait until the counter is non-null AND stable, then record. The 2b sampler
caught the counter mid-transition (nulls), which is a sampling artifact, not
a skipped board. Writes checker-log2c.json."""
import json
from playwright.sync_api import sync_playwright

CK = "/home/hatch/workspace/team-nitro/walkthrough-agreement-distill-fix5-20261119/checker"
FIX = "http://127.0.0.1:18096"
LOG = CK + "/checker-log2c.json"

def counter(page):
    return page.evaluate("() => { const m = document.body.innerText.match(/(\\d+)\\s*\\/\\s*37/); return m ? m[0] : null; }")

def stable_counter(page, timeout_ms=4000):
    last = None; stable_since = None
    import time
    t0 = time.time()
    while (time.time() - t0) * 1000 < timeout_ms:
        c = counter(page)
        if c is not None:
            if c == last:
                if stable_since is not None and (time.time() - stable_since) * 1000 >= 300:
                    return c
            else:
                last = c; stable_since = time.time()
        page.wait_for_timeout(100)
    return last

out = {"label": "FIX5-CHECKER-DRIVE2C", "legs": []}
with sync_playwright() as pw:
    b = pw.firefox.launch(headless=True)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, ignore_https_errors=True)
    page = ctx.new_page()
    errs = []
    page.on("pageerror", lambda e: errs.append(str(e)[:200]))
    page.on("console", lambda m: errs.append(m.type + ": " + m.text[:200]) if m.type == "error" else None)
    try:
        page.goto(FIX + "/agreement", timeout=60000); page.wait_for_timeout(2000)
        seen = []
        for i in range(45):
            c = stable_counter(page)
            if c and (not seen or seen[-1] != c):
                seen.append(c)
            if page.evaluate("() => [...document.querySelectorAll('button')].some(x=>x.offsetParent!==null && /I agree/i.test(x.innerText))"):
                break
            page.locator("button", has_text="Next").locator("visible=true").first.click(timeout=5000)
            page.wait_for_timeout(200)
        out["legs"].append({"leg": "unfold-1-37-stabilized", "seen": seen, "count": len(seen),
                            "sequential": seen == [f"{i} / 37" for i in range(1, 38)],
                            "errors": errs})
    except Exception as e:
        out["legs"].append({"leg": "unfold-1-37-stabilized", "ERROR": str(e)[:600]})
    b.close()
with open(LOG, "w") as f:
    json.dump(out, f, indent=1)
for l in out["legs"]:
    print(json.dumps(l)[:1500], flush=True)
print("WROTE", LOG)
