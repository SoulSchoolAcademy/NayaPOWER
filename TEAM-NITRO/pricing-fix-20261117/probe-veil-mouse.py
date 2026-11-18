#!/usr/bin/env python3
"""Real-mouse test of the veil: does a human click on ENTER while the veil
is up dismiss it, and does the click also land on ENTER?"""
import os
from playwright.sync_api import sync_playwright

FREE = "https://naya-pricing-free-staging.nayapower.workers.dev/free"
HERE = os.path.dirname(os.path.abspath(__file__))

with sync_playwright() as pw:
    browser = pw.chromium.launch(headless=True, proxy={"server": "http://127.0.0.1:18080"})
    ctx = browser.new_context(viewport={"width": 635, "height": 900}, device_scale_factor=1,
                              is_mobile=True, ignore_https_errors=True)
    page = ctx.new_page()
    page.goto(FREE, wait_until="load", timeout=60000)
    page.wait_for_function("!document.getElementById('installVeil').hidden", timeout=12000)
    box = page.evaluate("""() => { const b = document.getElementById('enterBtn').getBoundingClientRect();
      return {x: b.x + b.width/2, y: b.y + b.height/2}; }""")
    print("veil up; ENTER center:", box)
    # Real mouse click, as a human would do it.
    page.mouse.click(box["x"], box["y"])
    page.wait_for_timeout(600)
    s1 = page.evaluate("""() => ({veilHidden: document.getElementById('installVeil').hidden,
      status: document.getElementById('aliasStatus').textContent,
      dismissed: localStorage.getItem('nayanet_install_dismissed')})""")
    print("after 1st real click on ENTER:", s1)
    # Second click: veil is gone, ENTER must act.
    page.mouse.click(box["x"], box["y"])
    page.wait_for_timeout(600)
    s2 = page.evaluate("""() => ({veilHidden: document.getElementById('installVeil').hidden,
      status: document.getElementById('aliasStatus').textContent})""")
    print("after 2nd real click on ENTER:", s2)
    # Keyboard: type in the alias box while veil is up on a fresh load?
    # (veil dismissed already; instead check Escape path is intact via reload)
    page.screenshot(path=os.path.join(HERE, "shots-fix", "veil-mouse.png"))
    browser.close()
    print("CONCLUSION: 1st click dismisses veil:", s1["veilHidden"],
          "| 1st click also activated ENTER:", s1["status"] == "Enter alias to continue.",
          "| 2nd click activates ENTER:", s2["status"] == "Enter alias to continue.")
