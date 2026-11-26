#!/usr/bin/env python3
"""R6e video + 404 follow-up (phone): does the welcome video actually PLAY
after the facade click (header status + deck current time over 12s), and
what exactly 404s on the staged /agreement load? If still paused, click the
YouTube player's own play button and sample again."""
import os, json
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://portal-frontpage-fix-20261125-r6-staging.nayapower.workers.dev"
PROXY = {"server": "http://127.0.0.1:18080"}
EXE = "/home/hatch/.cache/ms-playwright/chromium-1255/chrome-linux64/chrome"
reqs = []
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=EXE, args=["--no-sandbox"], proxy=PROXY)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, has_touch=True, is_mobile=True)
    pg = ctx.new_page()
    pg.on("response", lambda r: reqs.append((r.status, r.url)))
    pg.on("pageerror", lambda e: print("PAGEERROR:", str(e)[:200], flush=True))
    pg.goto(BASE + "/agreement", wait_until="domcontentloaded", timeout=180000)
    pg.wait_for_function("() => { const c = document.getElementById('screen-cover'); return c && c.classList.contains('active'); }", timeout=60000)
    pg.wait_for_timeout(4000)
    bad = [(s, u) for (s, u) in reqs if s >= 400]
    print("NON-2XX ON /agreement LOAD:", json.dumps(bad, indent=1), flush=True)
    def state():
        return pg.evaluate("""() => {
          const hdr = document.querySelector('.pm-status, .pm-head .status, [class*="status"]');
          const seek = document.querySelector('.deck-seekrow, .hero-seekrow');
          return { headerStatus: (document.querySelector('.pm-head')||{}).textContent ? document.querySelector('.pm-head').textContent.trim().slice(0,60) : null,
            tDur: (document.getElementById('tDur')||{}).textContent || null,
            seekText: seek ? seek.textContent.trim().replace(/\\s+/g,' ') : null,
            framePlaying: (document.getElementById('videoFrame')||{}).classList ? document.getElementById('videoFrame').classList.contains('playing') : null,
            iframe: !!document.querySelector('#videoShell iframe') };
        }""")
    print("BEFORE CLICK:", json.dumps(state()), flush=True)
    pg.locator("#videoFacade").click(timeout=10000)
    for t in (2, 6, 12):
        pg.wait_for_timeout((2 if t == 2 else 4 if t == 6 else 6) * 1000)
        print(f"AFTER CLICK +{t}s:", json.dumps(state()), flush=True)
    st = state()
    if "PAUSED" in (st["headerStatus"] or ""):
        print("STILL PAUSED — clicking the YouTube player's own play button (iframe centre)", flush=True)
        box = pg.locator("#videoShell iframe").bounding_box()
        if box:
            pg.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            for t in (3, 8):
                pg.wait_for_timeout(3000 if t == 3 else 5000)
                print(f"AFTER YT PLAY +{t}s:", json.dumps(state()), flush=True)
    pg.screenshot(path=os.path.join(HERE, "r6e-phone-video-state.png"))
    bad2 = [(s, u) for (s, u) in reqs if s >= 400]
    print("NON-2XX TOTAL:", json.dumps(bad2, indent=1), flush=True)
    b.close()
    print("VIDEO FOLLOW-UP DONE", flush=True)
