#!/usr/bin/env python3
"""Baseline hero measurement (pre-edit) for the points round.
Measures #pname, #ptag, #cvrbtn, .ph-cover, .ph-head bounding boxes at
390/1440/360 on the three BASE files (personal-live, space-clone,
business-clone) via file:// URLs, plus overflow + console errors.
Usage: python3 probe-baseline.py [firefox|chromium]
Writes probe-baseline-<browser>.json + screenshots into this dir.
"""
import json, os, sys
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.expanduser("~/workspace/team-nitro/space-business-mirror-personal-20261112")
FILES = {
    "personal": os.path.join(BASE, "personal-live.html"),
    "space": os.path.join(BASE, "space-clone.html"),
    "business": os.path.join(BASE, "business-clone.html"),
}
WIDTHS = [390, 1440, 360]
SELS = ["#pname", "#pointsdisplay", "#ptag", "#cvrbtn", ".ph-cover", ".ph-head", "#cvr"]
JS = """
() => {
  const out = {};
  for (const s of %s) {
    const el = document.querySelector(s);
    if (!el) { out[s] = null; continue; }
    const r = el.getBoundingClientRect();
    out[s] = {x: +r.x.toFixed(1), y: +r.y.toFixed(1), w: +r.width.toFixed(1),
              h: +r.height.toFixed(1), top: +r.top.toFixed(1),
              bottom: +r.bottom.toFixed(1), left: +r.left.toFixed(1),
              right: +r.right.toFixed(1)};
  }
  out._doc = {scrollW: document.documentElement.scrollWidth,
              clientW: document.documentElement.clientWidth,
              scrollH: document.documentElement.scrollHeight,
              innerW: window.innerWidth};
  out._pillText = (document.querySelector('#pointscount')||{}).textContent ?? null;
  out._donutTotal = (document.querySelector('#os-dash-total')||{}).textContent ?? null;
  out._bigNum = (document.querySelector('#os-se-val')||{}).textContent ?? null;
  return out;
}
""" % json.dumps(SELS)

def boxes_overlap(a, b):
    if not a or not b: return None
    return not (a["right"] <= b["left"] or b["right"] <= a["left"]
                or a["bottom"] <= b["top"] or b["bottom"] <= a["top"])

def main():
    browser_name = sys.argv[1] if len(sys.argv) > 1 else "firefox"
    results = {"browser": browser_name, "pages": {}}
    with sync_playwright() as p:
        browser = getattr(p, browser_name).launch()
        for page_name, path in FILES.items():
            results["pages"][page_name] = {}
            for w in WIDTHS:
                ctx = browser.new_context(viewport={"width": w, "height": 844})
                page = ctx.new_page()
                errors = []
                page.on("console", lambda m: errors.append(f"{m.type}: {m.text}") if m.type == "error" else None)
                page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
                page.goto("file://" + path, wait_until="load", timeout=60000)
                page.wait_for_timeout(4000)
                top = page.evaluate(JS)
                # scrolled-to-end measurement: overflow + bottom shot
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(800)
                end = page.evaluate(JS)
                page.screenshot(path=os.path.join(HERE, f"baseline-{browser_name}-{page_name}-{w}-top.png"))
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(400)
                page.screenshot(path=os.path.join(HERE, f"baseline-{browser_name}-{page_name}-{w}-end.png"))
                page.evaluate("window.scrollTo(0,0)")
                pname, cvr = top.get("#pname"), top.get("#cvrbtn")
                results["pages"][page_name][str(w)] = {
                    "top": top, "end": end,
                    "overflow_px": max(0, top["_doc"]["scrollW"] - top["_doc"]["clientW"]),
                    "cvrbtn_intersects_pname": boxes_overlap(pname, cvr),
                    "console_errors": errors[:20],
                    "console_error_count": len(errors),
                }
                ctx.close()
        browser.close()
    out = os.path.join(HERE, f"probe-baseline-{browser_name}.json")
    with open(out, "w") as f:
        json.dump(results, f, indent=1)
    print("wrote", out)
    for pn, widths in results["pages"].items():
        for w, r in widths.items():
            t = r["top"]
            print(f"{pn} {w}: pname={t.get('#pname')} pill={t.get('#pointsdisplay')} "
                  f"ptag={t.get('#ptag')} cvrbtn={t.get('#cvrbtn')} cover={t.get('.ph-cover')} "
                  f"overflow={r['overflow_px']} cvrXname={r['cvrbtn_intersects_pname']} "
                  f"errs={r['console_error_count']}")

if __name__ == "__main__":
    main()
