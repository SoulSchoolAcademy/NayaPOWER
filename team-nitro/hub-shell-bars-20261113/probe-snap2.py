#!/usr/bin/env python3
"""Snap check, corrected criterion: the snap target is the SNAPPORT start
(row left + scroll-padding-left, 10px phone / 12px desktop), not the row edge.
After a scroll settles, some pill's left must equal the snapport start (+/-1px)
and that pill must be whole; pills left of it may only peek by <= the padding.
Also: all 9 reachable — scroll to max, the last pill (10 APPS) fully visible.
Staged fixed shell, 390 + 360 + 1440.
"""
import json
from playwright.sync_api import sync_playwright

WD = "/home/hatch/workspace/team-nitro/hub-shell-bars-20261113"
STAGING = "https://naya-public-blog-staging.nayapower.workers.dev"

READ = """() => {
  const row = document.querySelector('.obb-row');
  const cs = getComputedStyle(row);
  const padL = parseFloat(cs.scrollPaddingLeft) || 0;
  const rl = row.getBoundingClientRect().left;
  const rr = row.getBoundingClientRect().right;
  const snapStart = rl + padL;
  const pills = [...document.querySelectorAll('#obb-bar .obb-pill')].map(p => {
    const b = p.getBoundingClientRect();
    return {label: (p.querySelector('.obb-lbl')||{}).innerText, left: Math.round(b.left),
      right: Math.round(b.right), w: Math.round(b.width)}; });
  const atSnap = pills.filter(p => Math.abs(p.left - snapStart) <= 1);
  const halfSliced = pills.filter(p => {
    const visL = Math.max(p.left, rl), visR = Math.min(p.right, rr);
    const vis = Math.max(0, visR - visL);
    return vis > 12 && vis < p.w - 1; });
  return {scrollLeft: Math.round(row.scrollLeft * 100) / 100, rowLeft: Math.round(rl),
    padL, snapStart: Math.round(snapStart), atSnap,
    halfSliced, pills};
}"""


def check(pg, tag):
    pg.wait_for_timeout(1500)
    d = pg.evaluate(READ)
    ok = len(d["atSnap"]) == 1 and not d["halfSliced"]
    print(f"  [{tag}] scrollLeft={d['scrollLeft']} snapStart={d['snapStart']} "
          f"atSnap={[p['label'] for p in d['atSnap']]} halfSliced={[p['label'] for p in d['halfSliced']]} -> {'PASS' if ok else 'FAIL'}")
    return ok


with sync_playwright() as pw:
    for w, h in [(390, 844), (360, 800), (1440, 900)]:
        print(f"== WIDTH {w} ==")
        browser = pw.firefox.launch(headless=True)
        pg = browser.new_context(viewport={"width": w, "height": h}).new_page()
        pg.goto(STAGING + "/s/sn2696", timeout=60000)
        pg.wait_for_timeout(3500)
        # settle at rest
        print("  rest:", json.dumps(pg.evaluate(READ)["atSnap"]))
        # wheel scroll
        box = pg.query_selector("#obb-bar").bounding_box()
        pg.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        pg.mouse.wheel(120, 0)
        check(pg, "wheel-120")
        # smooth programmatic scroll mid-row
        pg.evaluate("document.querySelector('.obb-row').scrollTo({left: 200, behavior: 'smooth'})")
        check(pg, "smooth-200")
        # scroll to max: last pill reachable + whole
        pg.evaluate("document.querySelector('.obb-row').scrollTo({left: 9999, behavior: 'smooth'})")
        pg.wait_for_timeout(1500)
        d = pg.evaluate(READ)
        last = d["pills"][-1]
        print(f"  [max] last={last} rowRight={d['rowLeft'] + 0} -> whole={last['right'] <= d['rowLeft'] + pg.evaluate('document.querySelector(\".obb-row\").clientWidth')}")
        browser.close()
print("DONE")
