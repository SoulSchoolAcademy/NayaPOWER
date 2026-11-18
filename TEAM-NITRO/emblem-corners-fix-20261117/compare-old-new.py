#!/usr/bin/env python3
"""Compare render: OLD (emblem placement tip, fbe04202) vs NEW (corners fix)
at 390x844 and 635x390, served from MEMORY on localhost (no disk, no staging
overwrite). Screenshots: compare-old-<w>.png / compare-new-<w>.png.
No alias typed, no claim made."""
import importlib.util
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
sys.path.insert(0, os.path.expanduser("~/workspace/ninaya/integration"))

CURDIR = os.path.expanduser("~/workspace/team-nitro/pricing-certificate-current-20261117")
FIXDIR = os.path.expanduser("~/workspace/team-nitro/pricing-certificate-fix-20261117")
PREVDIR = os.path.expanduser("~/workspace/team-nitro/emblem-placement-20261117")
HERE = os.path.expanduser("~/workspace/team-nitro/emblem-corners-fix-20261117")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_cur = load("certcurrent", os.path.join(CURDIR, "build-certificate.py"))
_fixmod = load("certfix", os.path.join(FIXDIR, "build-fix.py"))
_emb = load("embcert", os.path.join(PREVDIR, "build-emblem-certificate.py"))
_fix = load("cornersfix", os.path.join(HERE, "build-emblem-corners-fix.py"))

walk_pf, entry_pf = _cur.regen_pricing_fix_tip()
h = _cur.harvest_identity()
base_entry = _cur.apply_certificate(entry_pf, h)
fix_entry = _fixmod.apply_fix(base_entry, h)
b64 = _emb.emblem_b64()
old_entry = _emb.apply_emblem(fix_entry, b64)
new_entry = _fix.apply_corners_fix(old_entry, b64)
print(f"old {len(old_entry.encode())} B, new {len(new_entry.encode())} B")

PAGES = {"/old": old_entry.encode(), "/new": new_entry.encode()}


class H(BaseHTTPRequestHandler):
    def do_GET(self):
        body = PAGES.get(self.path)
        if body is None:
            self.send_response(404); self.end_headers(); return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass


srv = ThreadingHTTPServer(("127.0.0.1", 8901), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for width, height in [(390, 844), (635, 390)]:
        for tag, path in [("old", "/old"), ("new", "/new")]:
            ctx = browser.new_context(viewport={"width": width, "height": height})
            pg = ctx.new_page()
            pg.goto(f"http://127.0.0.1:8901{path}", wait_until="networkidle")
            pg.wait_for_timeout(1200)
            # Scroll the plaque to the bottom, so the bottom corners are in view.
            pg.evaluate("""() => {
              const pl = document.querySelector('#certPlaque');
              if (pl) pl.scrollTop = pl.scrollHeight;
            }""")
            pg.wait_for_timeout(600)
            pg.screenshot(path=os.path.join(HERE, f"compare-{tag}-{width}-bottom.png"))
            print(f"compare-{tag}-{width}-bottom.png", flush=True)
            ctx.close()
    browser.close()
srv.shutdown()
print("COMPARE OK")
