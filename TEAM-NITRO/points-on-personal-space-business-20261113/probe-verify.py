#!/usr/bin/env python3
"""Verification probe for the points round (post-edit).
Firefox, file:// local copies of personal-points.html, space-points.html,
business-points.html. At 390/1440/360: bounding boxes, pill row relationship,
#pname top-edge equality across pages, #cvrbtn intersection, overflow,
console errors, screenshots top + end, pill hover computed-style delta.
Writes probe-verify-firefox.json + proof-*.png into this dir.
"""
import json, os, sys
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = {
    "personal": os.path.join(HERE, "personal-points.html"),
    "space": os.path.join(HERE, "space-points.html"),
    "business": os.path.join(HERE, "business-points.html"),
}
WIDTHS = [390, 1440, 360]
SELS = ["#pname", "#pointsdisplay", "#pointscount", "#ptag", "#cvrbtn", ".ph-cover", ".ph-head"]
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
  out._pillCount = document.querySelectorAll('#pointsdisplay').length;
  out._donutWrap = !!document.getElementById('os-donut-wrap');
  out._ringWrap = !!document.getElementById('os-ring-wrap');
  return out;
}
""" % json.dumps(SELS)

def overlap(a, b):
    if not a or not b: return None
    return not (a["right"] <= b["left"] or b["right"] <= a["left"]
                or a["bottom"] <= b["top"] or b["bottom"] <= a["top"])

def main():
    results = {"browser": "firefox", "pages": {}}
    with sync_playwright() as p:
        browser = p.firefox.launch()
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
                # hover check H5: computed box-shadow of the pill before/after hover
                hover = page.evaluate("""() => {
                  const el = document.querySelector('#pointsdisplay');
                  if (!el) return null;
                  const cs = getComputedStyle(el);
                  return {before: cs.boxShadow, transformBefore: cs.transform};
                }""")
                try:
                    page.hover("#pointsdisplay", timeout=5000)
                    page.wait_for_timeout(500)
                    hover_after = page.evaluate("""() => {
                      const el = document.querySelector('#pointsdisplay');
                      const cs = getComputedStyle(el);
                      return {after: cs.boxShadow, transformAfter: cs.transform};
                    }""")
                    hover.update(hover_after)
                except Exception as e:
                    hover["hover_error"] = str(e)
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(800)
                end = page.evaluate(JS)
                page.evaluate("window.scrollTo(0,0)")
                page.wait_for_timeout(300)
                page.screenshot(path=os.path.join(HERE, f"proof-firefox-{page_name}-{w}-top.png"))
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                page.wait_for_timeout(400)
                page.screenshot(path=os.path.join(HERE, f"proof-firefox-{page_name}-{w}-end.png"))
                page.evaluate("window.scrollTo(0,0)")
                pname, pill = top.get("#pname"), top.get("#pointsdisplay")
                same_row = None
                gap = None
                if pname and pill:
                    same_row = abs(pill["top"] - pname["top"]) < 8 or (pill["top"] >= pname["top"] and pill["bottom"] <= pname["bottom"] + 8)
                    gap = round(pill["left"] - pname["right"], 1)
                results["pages"][page_name][str(w)] = {
                    "top": top, "end": end, "hover": hover,
                    "pill_present": pill is not None,
                    "pill_same_row_as_name": same_row,
                    "pill_gap_px": gap,
                    "pill_immediately_right": (same_row is True and gap == 14.0),
                    "overflow_px": max(0, top["_doc"]["scrollW"] - top["_doc"]["clientW"]),
                    "cvrbtn_intersects_pname": overlap(pname, top.get("#cvrbtn")),
                    "console_errors": errors[:20],
                    "console_error_count": len(errors),
                }
                ctx.close()
        browser.close()
    # cross-page pname top-edge equality
    results["pname_top_spread"] = {}
    for w in WIDTHS:
        tops = {pn: results["pages"][pn][str(w)]["top"]["#pname"]["top"]
                for pn in FILES if results["pages"][pn][str(w)]["top"].get("#pname")}
        results["pname_top_spread"][str(w)] = {
            "tops": tops,
            "spread_px": round(max(tops.values()) - min(tops.values()), 1) if tops else None,
        }
    out = os.path.join(HERE, "probe-verify-firefox.json")
    with open(out, "w") as f:
        json.dump(results, f, indent=1)
    print("wrote", out)
    for pn, widths in results["pages"].items():
        for w, r in widths.items():
            t = r["top"]
            print(f"{pn} {w}: pname_y={t['#pname']['top']} pill={t.get('#pointsdisplay')} "
                  f"same_row={r['pill_same_row_as_name']} gap={r['pill_gap_px']} "
                  f"pname_x={t['#pname']['x']} ptag_y={t['#ptag']['top']} "
                  f"cvrXname={r['cvrbtn_intersects_pname']} overflow={r['overflow_px']} "
                  f"pillText={t['_pillText']!r} donutWrap={t['_donutWrap']} errs={r['console_error_count']}")
    print("pname top spread:", json.dumps(results["pname_top_spread"]))

if __name__ == "__main__":
    main()
