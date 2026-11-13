#!/usr/bin/env python3
"""Local render probe for the edited Q2 walk file (NOT a staged proof).

Serves walk-beginning-fixed.html over localhost, loads it in Playwright
Firefox at 1440/390/360, forces #step-2 visible (the real walk from the
login page needs the staging worker + backend — that leg is owed after
deploy), and measures: heading verbatim + wrap, overflow, console errors,
hint texts, all four eye pop-ups (2-A, 2-B, 2-C, 2-custom), "2 of 10".
Screenshots to the work dir for eye-check. Prints a JSON summary.
"""
import json
import subprocess
import sys
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

D = "/home/hatch/workspace/team-nitro/walk-q2-whats-your-thing-20261113"
PORT = 8931


class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=D, **k)

    def log_message(self, *a):
        pass


srv = ThreadingHTTPServer(("127.0.0.1", PORT), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()

from playwright.sync_api import sync_playwright

SHOW_Q2 = """
() => {
  document.querySelectorAll('.p3-step').forEach(s => { s.hidden = true; });
  const q2 = document.getElementById('step-2');
  q2.hidden = false;
  return {
    heading: q2.querySelector('.p3-question').textContent,
    progress: q2.querySelector('.p3-progress').textContent,
    choices: [...q2.querySelectorAll('.p3-choice-text')].map(t => t.value),
    hints: [...q2.querySelectorAll('#hintRow-2 .p3-tip')].map(t => t.textContent),
    answerEmpty: q2.querySelector('#answer-2').value === ''
  };
}
"""

EYE_JS = """
(code) => {
  document.querySelector('[data-eye="' + code + '"]').click();
  const m = document.getElementById('choiceModal');
  const vis = m && !m.hidden;
  const txt = vis ? m.innerText : '';
  const close = document.getElementById('choiceClose') || m.querySelector('button');
  if (close) close.click();
  return {visible: vis, text: txt};
}
"""

results = {}
with sync_playwright() as p:
    b = p.firefox.launch()
    for label, w, h in [("1440", 1440, 900), ("390", 390, 844), ("360", 360, 740)]:
        errors = []
        pg = b.new_page(viewport={"width": w, "height": h})
        pg.on("console", lambda m: errors.append(m.type + ": " + m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errors.append("pageerror: " + str(e)))
        pg.goto(f"http://127.0.0.1:{PORT}/walk-beginning-fixed.html", wait_until="load")
        pg.wait_for_timeout(1200)
        info = pg.evaluate(SHOW_Q2)
        pg.wait_for_timeout(300)
        m = pg.evaluate("""() => {
          const q = document.querySelector('#step-2 .p3-question');
          const r = q.getBoundingClientRect();
          return {
            headingBox: {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)},
            headingLines: Math.round(r.height / parseFloat(getComputedStyle(q).lineHeight)),
            headingFont: getComputedStyle(q).fontSize,
            docScrollW: document.documentElement.scrollWidth,
            winW: window.innerWidth,
            overflowX: document.documentElement.scrollWidth > window.innerWidth,
            q2ScrollW: document.getElementById('step-2').scrollWidth
          };
        }""")
        eyes = {}
        for code in ["2-A", "2-B", "2-C", "2-custom"]:
            eyes[code] = pg.evaluate(EYE_JS, code)
            pg.wait_for_timeout(200)
        pg.screenshot(path=f"{D}/q2-{label}.png", full_page=False)
        pg.screenshot(path=f"{D}/q2-{label}-full.png", full_page=True)
        results[label] = {"info": info, "measure": m, "eyes": eyes,
                          "consoleErrors": errors}
        pg.close()
    b.close()

srv.shutdown()
print(json.dumps(results, indent=1, ensure_ascii=False))
