#!/usr/bin/env python3
"""Minimal Chromium aliveness probe (bridge presentation round)."""
import sys
print("STEP import", flush=True)
from playwright.sync_api import sync_playwright
print("STEP launch", flush=True)
try:
    with sync_playwright() as pw:
        b = pw.chromium.launch(proxy={"server": "http://127.0.0.1:18080"},
                               args=["--ignore-certificate-errors", "--no-sandbox"])
        print("STEP launched", flush=True)
        pg = b.new_page()
        print("STEP page", flush=True)
        pg.goto("about:blank")
        print("CHROMIUM ALIVE", flush=True)
        b.close()
except BaseException as e:
    print("CHROMIUM DEAD:", type(e).__name__, str(e)[:200], flush=True)
    sys.exit(0)
