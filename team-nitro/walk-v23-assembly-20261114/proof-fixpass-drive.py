#!/usr/bin/env python3
"""Fix-pass browser probe (self-check pass 2): drive the staged walk from
the login page, phone first (360x800) then desktop (1440x900), on the
DEPLOYED bytes. Verifies live behaviour: 82 clicks / 83 boards, dots,
board 58/59/60 sentences from the rendered DOM, §4 faced boards' images
loaded + distinct + non-adjacent, eye notes open with the new photos,
overflow 0 at both widths, signing ratio, zero page errors.
Drive pattern harvested from ~/workspace/vera-proof/vera-drive.py.
Screenshots to proof-fixpass/ (durable, next to the maker record).
"""
import json, re, sys
from playwright.sync_api import sync_playwright

BASE = "https://naya-walk-beginning-staging.nayapower.workers.dev"
PROXY = "http://127.0.0.1:18080"
ANS = {1: "I am a test walker, here to learn and build.", 2: "music and making things",
       4: "To help people learn and earn.", 5: "Do good, share well.", 6: "Build a small bakery business.",
       7: "I bake bread for my neighbours.", 8: "Fresh bread and baking lessons.", 9: "A neighbourhood bakery.",
       10: "A warm space for bakers and neighbours."}


def drive_to_end(pg, alias):
    pg.goto(BASE + "/", timeout=60000)
    pg.fill("#userName", alias)
    pg.click("#entryForm button[type='submit'], #entryForm button")
    pg.wait_for_url("**/identity.html**", timeout=60000)
    pg.fill("#aliasInput", alias)
    pg.wait_for_timeout(2500)
    pg.click("#enterBtn")
    pg.wait_for_function("() => location.pathname === '/welcome' && document.readyState === 'complete'", timeout=120000)
    pg.fill("#answer-1", ANS[1]); pg.click("#enterBtn-1")
    pg.wait_for_selector("#step-2:visible", timeout=15000)
    pg.fill("#answer-2", ANS[2]); pg.click("#enterBtn-2")
    pg.wait_for_selector("#step-3:visible", timeout=15000)
    pg.locator('[data-edit="3-B"]').click(); pg.wait_for_timeout(300)
    pg.fill("#choice-3-B", "A world where everyone can learn, earn and belong.")
    pg.click("#enterBtn-3")
    pg.wait_for_selector("#step-4:visible", timeout=15000)
    for n in range(4, 11):
        pg.fill(f"#answer-{n}", ANS[n]); pg.click(f"#enterBtn-{n}")
        pg.wait_for_selector(f"#step-{n+1}:visible", timeout=15000)
    for n in (11, 12, 13):
        pg.locator(f"#step-{n} [data-act='yes']").click()
        nxt = f"#step-{n+1}" if n < 13 else "#step-14"
        pg.wait_for_selector(nxt + ":visible", timeout=15000)
    pg.fill("#answer-14", "Tokyo, Japan"); pg.click("#enterBtn-14")
    pg.wait_for_selector("#step-names:visible", timeout=15000)
    pg.fill("#name-personal", "Personal"); pg.fill("#name-business", "Business"); pg.fill("#name-space", "Space")
    pg.click("#enterBtn-15")
    pg.wait_for_selector("#step-end:not([hidden])", timeout=60000)


def audit(pg, tag):
    r = {}
    r["overflow_hook"] = pg.evaluate("() => ({sw: document.body.scrollWidth, iw: window.innerWidth})")
    r["title"] = pg.inner_text("h1.deal-title")
    r["dots"] = pg.evaluate("() => document.querySelectorAll('#letterDots .ldot').length")
    r["label0"] = pg.inner_text("#letterStepLabel")
    # keep-reading through the whole letter
    clicks = 0
    while True:
        vis = pg.evaluate("() => { const c = document.getElementById('letterControls'); return c && !c.hidden && getComputedStyle(c).display !== 'none'; }")
        if not vis:
            break
        pg.click("#letterNext")
        clicks += 1
        pg.wait_for_timeout(120)
        if clicks > 120:
            break
    r["clicks"] = clicks
    r["boards_visible"] = pg.evaluate("() => Array.from(document.querySelectorAll('#letterBody .letter-beat')).filter(b => !b.hidden).length")
    r["dots_on"] = pg.evaluate("() => document.querySelectorAll('#letterDots .ldot.on').length")
    r["label_end"] = pg.inner_text("#letterStepLabel")
    r["agree_visible"] = pg.evaluate("() => { const a = document.getElementById('dealAgree'); return a && !a.hidden; }")
    # sentence counts from the rendered DOM (per-p method, JS mirror of the file audit)
    r["counts"] = pg.evaluate("""() => {
      const beats = Array.from(document.querySelectorAll('#letterBody .letter-beat'));
      return beats.map(b => {
        const nuts = b.querySelector('.ib-nutshell');
        const clone = nuts.cloneNode(true);
        clone.querySelectorAll('.deal-eye-note').forEach(d => d.remove());
        let n = 0;
        clone.querySelectorAll('p').forEach(p => {
          const t = p.textContent.replace(/\\$\\d+\\.\\d+/g, 'PRICE');
          const frags = t.split(/[.!?\\u2026]+/).filter(s => s.trim());
          n += Math.max(1, frags.length);
        });
        return n;
      });
    }""")
    # board portraits: rendered src + loaded?
    r["board_photos"] = pg.evaluate("""() => {
      const out = {};
      document.querySelectorAll('#letterBody .letter-beat').forEach(b => {
        const img = b.querySelector('.deal-beat-photo');
        if (img) out[b.getAttribute('data-beat')] = {src: img.getAttribute('src'), ok: img.complete && img.naturalWidth > 0, w: img.getBoundingClientRect().width};
      });
      return out;
    }""")
    # note photos
    r["note_photos"] = pg.evaluate("""() => {
      const out = {};
      document.querySelectorAll('.deal-eye-note').forEach(d => {
        const img = d.querySelector('.deal-quote-photo');
        if (img) out[d.id] = {src: img.getAttribute('src'), ok: img.complete && img.naturalWidth > 0};
      });
      return out;
    }""")
    # eyes: open each, check note appears below eye, then close
    eyes = pg.evaluate("() => Array.from(document.querySelectorAll('.deal-eye')).map(e => e.getAttribute('data-note'))")
    opened = []
    for nid in eyes:
        pg.evaluate(f"""() => {{ document.querySelector('.deal-eye[data-note="{nid}"]').scrollIntoView({{block:'center'}}); }}""")
        pg.click(f".deal-eye[data-note=\"{nid}\"]")
        pg.wait_for_timeout(150)
        st = pg.evaluate(f"""() => {{ const d = document.getElementById('{nid}'); const e = document.querySelector('.deal-eye[data-note="{nid}"]');
          const r = d.getBoundingClientRect(), er = e.getBoundingClientRect();
          return {{hidden: d.hidden, top: Math.round(r.top), eyeBottom: Math.round(er.bottom), inView: r.top >= 0 && r.top < window.innerHeight}}; }}""")
        opened.append((nid, st))
        pg.click(f".deal-eye[data-note=\"{nid}\"]")
        pg.wait_for_timeout(80)
    r["eyes"] = opened
    r["overflow_unfolded"] = pg.evaluate("() => ({sw: document.body.scrollWidth, iw: window.innerWidth})")
    # signing ratio
    r["signing"] = pg.evaluate("""() => {
      const b = document.querySelector('#letterBody .deal-beat-photo');
      const s = document.querySelector('.deal-sign-photo');
      if (!b || !s) return null;
      return {board: Math.round(b.getBoundingClientRect().width), sign: Math.round(s.getBoundingClientRect().width)};
    }""")
    return r


def main():
    out = {}
    with sync_playwright() as p:
        br = p.chromium.launch(proxy={"server": PROXY}, args=["--no-sandbox"])
        errors = []
        pg = br.new_page(viewport={"width": 360, "height": 800})
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.on("console", lambda m: errors.append("console." + m.type + ": " + m.text) if m.type == "error" else None)
        drive_to_end(pg, "fixpass360a")
        pg.screenshot(path="proof-fixpass/hook-360.png")
        r360 = audit(pg, "360")
        out["360"] = r360
        out["360_errors"] = errors
        # faced §4 board + open note screenshots at 360
        pg.evaluate("() => { const b = document.querySelector('[data-beat=\"55\"]'); b.scrollIntoView({block:'center'}); }")
        pg.wait_for_timeout(400)
        pg.screenshot(path="proof-fixpass/board55-b12-360.png")
        pg.evaluate("() => { const b = document.querySelector('[data-beat=\"58\"]'); b.scrollIntoView({block:'center'}); }")
        pg.wait_for_timeout(400)
        pg.screenshot(path="proof-fixpass/board58-360.png")
        pg.click(".deal-eye[data-note=\"deal-note-deed\"]")
        pg.wait_for_timeout(300)
        pg.evaluate("() => { document.getElementById('deal-note-deed').scrollIntoView({block:'center'}); }")
        pg.wait_for_timeout(300)
        pg.screenshot(path="proof-fixpass/note-deed-b00-360.png")
        pg.close()
        # desktop 1440: overflow + clicks only (fresh alias)
        errors2 = []
        pg2 = br.new_page(viewport={"width": 1440, "height": 900})
        pg2.on("pageerror", lambda e: errors2.append(str(e)))
        drive_to_end(pg2, "fixpass1440a")
        r14 = {"overflow_hook": pg2.evaluate("() => ({sw: document.body.scrollWidth, iw: window.innerWidth})")}
        clicks = 0
        while pg2.evaluate("() => { const c = document.getElementById('letterControls'); return c && !c.hidden; }"):
            pg2.click("#letterNext"); clicks += 1; pg2.wait_for_timeout(60)
            if clicks > 120:
                break
        r14["clicks"] = clicks
        r14["boards_visible"] = pg2.evaluate("() => Array.from(document.querySelectorAll('#letterBody .letter-beat')).filter(b => !b.hidden).length")
        r14["overflow_unfolded"] = pg2.evaluate("() => ({sw: document.body.scrollWidth, iw: window.innerWidth})")
        r14["signing"] = pg2.evaluate("() => { const b = document.querySelector('#letterBody .deal-beat-photo'); const s = document.querySelector('.deal-sign-photo'); return b && s ? {board: Math.round(b.getBoundingClientRect().width), sign: Math.round(s.getBoundingClientRect().width)} : null; }")
        out["1440"] = r14
        out["1440_errors"] = errors2
        br.close()
    print(json.dumps(out, indent=1))
    with open("proof-fixpass/probe-360-1440.json", "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
