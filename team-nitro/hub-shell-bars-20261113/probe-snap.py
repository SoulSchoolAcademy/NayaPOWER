#!/usr/bin/env python3
"""Snap experiment: does the upper row snap to whole circles after a scroll settles?
Tests (at 390, staged fixed shell): (a) smooth programmatic scrollTo(120),
(b) real mouse-wheel scroll over the row. Each followed by 1.5s settle, then
the leftmost visible pill is measured. Comparison: the same procedure on the
locally-served BASE file (pre-edit pills) to tell a real regression from a
probe artifact.
"""
import json
import threading
import http.server
import functools
from playwright.sync_api import sync_playwright

WD = "/home/hatch/workspace/team-nitro/hub-shell-bars-20261113"
STAGING = "https://naya-public-blog-staging.nayapower.workers.dev"

SNAP_READ = """() => {
  const row = document.querySelector('.obb-row');
  const pills = [...document.querySelectorAll('#obb-bar .obb-pill')];
  const rl = row.getBoundingClientRect().left;
  const vis = pills.map(p => { const b = p.getBoundingClientRect();
    return {label: (p.querySelector('.obb-lbl')||{}).innerText, left: Math.round(b.left), right: Math.round(b.right)}; })
    .filter(p => p.right > rl && p.left < rl + row.clientWidth);
  return {scrollLeft: Math.round(row.scrollLeft * 100) / 100, rowLeft: Math.round(rl),
          first: vis.length ? vis[0] : null, nVisible: vis.length};
}"""


def serve_base():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory="/home/hatch/workspace/team-nitro/hub-slug-resolution-20261113")
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 8901), handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd


def trial(pg, how):
    if how == "smooth":
        pg.evaluate("document.querySelector('.obb-row').scrollTo({left: 120, behavior: 'smooth'})")
    elif how == "instant":
        pg.evaluate("document.querySelector('.obb-row').scrollTo({left: 120, behavior: 'instant'})")
    elif how == "wheel":
        box = pg.query_selector("#obb-bar").bounding_box()
        pg.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
        pg.mouse.wheel(120, 0)
    pg.wait_for_timeout(1500)
    return pg.evaluate(SNAP_READ)


def run_on(pw, url, tag):
    print(f"== {tag}: {url} ==")
    browser = pw.firefox.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 390, "height": 844})
    pg = ctx.new_page()
    pg.goto(url, timeout=60000)
    pg.wait_for_timeout(3500)
    for how in ["smooth", "wheel", "instant"]:
        pg.evaluate("document.querySelector('.obb-row').scrollTo({left: 0, behavior: 'instant'})")
        pg.wait_for_timeout(800)
        r = trial(pg, how)
        whole = r["first"] and r["first"]["left"] >= r["rowLeft"] - 1
        print(f"  {how}: scrollLeft={r['scrollLeft']} first={r['first']} whole={whole}")
    browser.close()


with sync_playwright() as pw:
    run_on(pw, STAGING + "/s/sn2696", "STAGED-FIXED")
    httpd = serve_base()
    try:
        run_on(pw, "http://127.0.0.1:8901/index-intel-today.html#/smart-notes/sn2696", "LOCAL-BASE")
    finally:
        httpd.shutdown()
print("DONE")
