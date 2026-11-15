#!/usr/bin/env python3
"""Fix-pass-2 browser probe (self-check pass 2): drive the staged walk from
the login page, phone first (360x800) then desktop (1440x900), on the
DEPLOYED bytes. Verifies live behaviour:
- Fix 1: 19 board portraits + 14 note photos loaded with the NEW srcs;
  eyes 14/14; signing photo is /agmt-sign2.png and bigger.
- Fix 2: the LIVE plain-text view carries 0 lines ending in a stray " i";
  the whole letter in order, ending "nayanet.app — enter."
- Fix 3: beats 57 + 63 bold sentences compute to 17px (body size);
  control beat 37 bold still 12px (unchanged by design).
- Guards re-proven: 82 clicks / 83 boards, dots, overflow 0 at both
  widths, zero page errors.
Sentence-count JS strips eye BUTTONS as well as note divs (the fix-pass
probe bug: button text counted as a sentence fragment).
Drive pattern harvested from proof-fixpass-drive.py. Screenshots to
proof-fixpass2/ (durable, next to the maker record).
"""
import json, re
from playwright.sync_api import sync_playwright

BASE = "https://naya-walk-beginning-staging.nayapower.workers.dev"
PROXY = "http://127.0.0.1:18080"
ANS = {1: "I am a test walker, here to learn and build.", 2: "music and making things",
       4: "To help people learn and earn.", 5: "Do good, share well.", 6: "Build a small bakery business.",
       7: "I bake bread for my neighbours.", 8: "Fresh bread and baking lessons.", 9: "A neighbourhood bakery.",
       10: "A warm space for bakers and neighbours."}
EXPECT_BOARDS = {"11": "/agmt-b06.png", "18": "/agmt-b04.jpg", "25": "/agmt-b09.jpg",
                 "36": "/agmt-b02.jpg", "37": "/agmt-b12.jpg", "40": "/agmt-b11.jpg",
                 "43": "/agmt-b00.jpg", "46": "/agmt-b01.jpg", "49": "/agmt-b03.jpg",
                 "52": "/agmt-b05.jpg", "55": "/agmt-b12.jpg", "58": "/agmt-b00.jpg",
                 "61": "/agmt-b01.jpg", "64": "/agmt-b02.jpg", "67": "/agmt-b03.jpg",
                 "70": "/agmt-b07.jpg", "73": "/agmt-b05.jpg", "76": "/agmt-b11.jpg",
                 "78": "/agmt-b08.jpg"}
EXPECT_NOTES = {"deal-note-collective": "/agmt-b06.png", "deal-note-land": "/agmt-b04.jpg",
                "deal-note-business": "/agmt-b11.jpg", "deal-note-deed": "/agmt-b00.jpg",
                "deal-note-cost": "/agmt-b01.jpg", "deal-note-joining": "/agmt-b03.jpg",
                "deal-note-privacy": "/agmt-b05.jpg", "deal-note-vault": "/agmt-b10.jpg",
                "deal-note-save": "/agmt-b12.jpg", "deal-note-job": "/agmt-b04.jpg",
                "deal-note-earn": "/agmt-b07.jpg", "deal-note-skeptic": "/agmt-b08.jpg",
                "deal-note-cap": "/agmt-b09.jpg", "deal-note-hold": "/agmt-b02.jpg"}


def dismiss_veil(pg):
    # PWA install veil (#installVeil, "Not now" = #installLater) pops up on
    # the identity page on a timer and intercepts pointer events (Vera's
    # fix-pass note). It is hidden at first, so a plain Playwright click
    # times out before it appears — poll for it and JS-click "Not now"
    # (the user action) until it is gone.
    for _ in range(8):
        gone = pg.evaluate("""() => {
          const v = document.getElementById('installVeil');
          if (!v || v.hidden || getComputedStyle(v).display === 'none') return true;
          const b = document.getElementById('installLater');
          if (b) b.click();
          return false;
        }""")
        if gone:
            return True
        pg.wait_for_timeout(500)
    return False


def drive_to_end(pg, alias):
    pg.goto(BASE + "/", timeout=60000)
    dismiss_veil(pg)
    pg.fill("#userName", alias)
    pg.click("#entryForm button[type='submit'], #entryForm button")
    pg.wait_for_url("**/identity.html**", timeout=60000)
    pg.fill("#aliasInput", alias)
    pg.wait_for_timeout(2500)
    dismiss_veil(pg)
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


def unfold_all(pg):
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
    return clicks


def audit(pg):
    r = {}
    r["overflow_hook"] = pg.evaluate("() => ({sw: document.body.scrollWidth, iw: window.innerWidth})")
    # fix 2 FIRST: #letterAll is only visible at the hook / while reading —
    # once all 83 boards are read the letter controls hide and the agree
    # frame shows instead. (Same reason Vera ran plain text as its own run.)
    pg.click("#letterAll")
    pg.wait_for_timeout(500)
    pg.screenshot(path="proof-fixpass2/plaintext-360.png")
    txt = pg.evaluate("() => document.getElementById('dealPlainText').textContent")
    lines = txt.split("\n")
    r["plaintext_lines"] = len(lines)
    r["plaintext_stray_i"] = [l for l in lines if l.endswith(" i")]
    r["plaintext_tail"] = txt.strip().split("\n")[-1]
    r["plaintext_head"] = txt.strip().split("\n")[:3]
    # order: every board sentence (DOM, buttons+notes stripped) appears in order in the plain text
    sents = pg.evaluate("""() => {
      const out = [];
      document.querySelectorAll('#letterBody .letter-beat').forEach(b => {
        const nuts = b.querySelector('.ib-nutshell');
        const clone = nuts.cloneNode(true);
        clone.querySelectorAll('.deal-eye-note').forEach(d => d.remove());
        clone.querySelectorAll('p').forEach(p => {
          p.querySelectorAll('button').forEach(x => x.remove());
          const t = p.textContent.replace(/\\s+/g, ' ').trim();
          if (t) out.push(t);
        });
      });
      return out;
    }""")
    flat = re.sub(r"\s+", " ", txt)
    pos, missing = 0, []
    for s in sents:
        s2 = re.sub(r"\s+", " ", s)
        i = flat.find(s2, pos)
        if i < 0:
            missing.append(s2[:60])
        else:
            pos = i + len(s2)
    r["plaintext_sentences_checked"] = len(sents)
    r["plaintext_sentences_missing"] = missing
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(300)
    r["clicks"] = unfold_all(pg)
    r["boards_visible"] = pg.evaluate("() => Array.from(document.querySelectorAll('#letterBody .letter-beat')).filter(b => !b.hidden).length")
    r["dots_on"] = pg.evaluate("() => document.querySelectorAll('#letterDots .ldot.on').length")
    r["label_end"] = pg.inner_text("#letterStepLabel")
    r["agree_visible"] = pg.evaluate("() => { const a = document.getElementById('dealAgree'); return a && !a.hidden; }")
    r["counts"] = pg.evaluate("""() => {
      const beats = Array.from(document.querySelectorAll('#letterBody .letter-beat'));
      return beats.map(b => {
        const nuts = b.querySelector('.ib-nutshell');
        const clone = nuts.cloneNode(true);
        clone.querySelectorAll('.deal-eye-note').forEach(d => d.remove());
        let n = 0;
        clone.querySelectorAll('p').forEach(p => {
          p.querySelectorAll('button').forEach(x => x.remove());
          const t = p.textContent.replace(/\\$\\d+\\.\\d+/g, 'PRICE');
          const frags = t.split(/[.!?\\u2026]+/).filter(s => s.trim());
          n += Math.max(1, frags.length);
        });
        return n;
      });
    }""")
    r["board_photos"] = pg.evaluate("""() => {
      const out = {};
      document.querySelectorAll('#letterBody .letter-beat').forEach(b => {
        const img = b.querySelector('.deal-beat-photo');
        if (img) out[b.getAttribute('data-beat')] = {src: img.getAttribute('src'), ok: img.complete && img.naturalWidth > 0, w: Math.round(img.getBoundingClientRect().width)};
      });
      return out;
    }""")
    r["board_photos_match"] = {k: (v["src"] == EXPECT_BOARDS[k]) for k, v in r["board_photos"].items()}
    r["note_photos"] = pg.evaluate("""() => {
      const out = {};
      document.querySelectorAll('.deal-eye-note').forEach(d => {
        const img = d.querySelector('.deal-quote-photo');
        if (img) out[d.id] = {src: img.getAttribute('src'), ok: img.complete && img.naturalWidth > 0};
      });
      return out;
    }""")
    r["note_photos_match"] = {k: (v["src"] == EXPECT_NOTES[k]) for k, v in r["note_photos"].items()}
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
    r["eyes_ok"] = all((not st["hidden"]) and st["inView"] for _, st in opened) and len(opened) == 14
    r["overflow_unfolded"] = pg.evaluate("() => ({sw: document.body.scrollWidth, iw: window.innerWidth})")
    r["signing"] = pg.evaluate("""() => {
      const b = document.querySelector('#letterBody .deal-beat-photo');
      const s = document.querySelector('.deal-sign-photo');
      if (!b || !s) return null;
      return {board: Math.round(b.getBoundingClientRect().width), sign: Math.round(s.getBoundingClientRect().width),
              signSrc: s.getAttribute('src'), signOk: s.complete && s.naturalWidth > 0};
    }""")
    # fix 3: computed bold sizes (beats unfolded, so styles are live)
    r["bold_sizes"] = pg.evaluate("""() => {
      const out = {};
      for (const beat of [57, 63, 37, 45]) {
        const b = document.querySelector('[data-beat="' + beat + '"] .ib-nutshell b');
        out[beat] = b ? getComputedStyle(b).fontSize + ' / ls ' + getComputedStyle(b).letterSpacing : null;
      }
      return out;
    }""")
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(300)
    return r


def shot(pg, beat, path):
    pg.evaluate(f"""() => {{ const b = document.querySelector('[data-beat="{beat}"]'); if (b) b.scrollIntoView({{block:'center'}}); }}""")
    pg.wait_for_timeout(400)
    pg.screenshot(path=path)


def main():
    out = {}
    with sync_playwright() as p:
        br = p.chromium.launch(proxy={"server": PROXY}, args=["--no-sandbox"])
        errors = []
        pg = br.new_page(viewport={"width": 360, "height": 800})
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.on("console", lambda m: errors.append("console." + m.type + ": " + m.text) if m.type == "error" else None)
        drive_to_end(pg, "fixpass2360d")
        pg.screenshot(path="proof-fixpass2/hook-360.png")
        r360 = audit(pg)
        out["360"] = r360
        out["360_errors"] = errors
        shot(pg, 37, "proof-fixpass2/board37-b12-360.png")
        shot(pg, 58, "proof-fixpass2/board58-b00-360.png")
        shot(pg, 64, "proof-fixpass2/board64-b02-360.png")
        shot(pg, 73, "proof-fixpass2/board73-b05-360.png")
        shot(pg, 57, "proof-fixpass2/board57-bold-360.png")
        shot(pg, 63, "proof-fixpass2/board63-bold-360.png")
        pg.evaluate("() => { document.querySelector('.deal-eye[data-note=\"deal-note-land\"]').scrollIntoView({block:'center'}); }")
        pg.click(".deal-eye[data-note=\"deal-note-land\"]")
        pg.wait_for_timeout(300)
        pg.evaluate("() => { document.getElementById('deal-note-land').scrollIntoView({block:'center'}); }")
        pg.wait_for_timeout(300)
        pg.screenshot(path="proof-fixpass2/note-land-b04-360.png")
        pg.evaluate("() => { document.querySelector('.deal-sign-photo').scrollIntoView({block:'center'}); }")
        pg.wait_for_timeout(400)
        pg.screenshot(path="proof-fixpass2/signing-360.png")
        pg.close()
        errors2 = []
        pg2 = br.new_page(viewport={"width": 1440, "height": 900})
        pg2.on("pageerror", lambda e: errors2.append(str(e)))
        pg2.on("console", lambda m: errors2.append("console." + m.type + ": " + m.text) if m.type == "error" else None)
        drive_to_end(pg2, "fixpass21440a")
        r14 = {"overflow_hook": pg2.evaluate("() => ({sw: document.body.scrollWidth, iw: window.innerWidth})")}
        # plain text first (hook state — #letterAll hides after the full read)
        pg2.click("#letterAll")
        pg2.wait_for_timeout(500)
        txt = pg2.evaluate("() => document.getElementById('dealPlainText').textContent")
        lines = txt.split("\n")
        r14["plaintext_stray_i"] = [l for l in lines if l.endswith(" i")]
        r14["plaintext_tail"] = txt.strip().split("\n")[-1]
        pg2.keyboard.press("Escape")
        pg2.wait_for_timeout(300)
        r14["clicks"] = unfold_all(pg2)
        r14["boards_visible"] = pg2.evaluate("() => Array.from(document.querySelectorAll('#letterBody .letter-beat')).filter(b => !b.hidden).length")
        r14["overflow_unfolded"] = pg2.evaluate("() => ({sw: document.body.scrollWidth, iw: window.innerWidth})")
        r14["signing"] = pg2.evaluate("""() => { const b = document.querySelector('#letterBody .deal-beat-photo'); const s = document.querySelector('.deal-sign-photo'); return b && s ? {board: Math.round(b.getBoundingClientRect().width), sign: Math.round(s.getBoundingClientRect().width), signSrc: s.getAttribute('src'), signOk: s.complete && s.naturalWidth > 0} : null; }""")
        r14["bold_sizes"] = pg2.evaluate("""() => { const out = {}; for (const beat of [57, 63, 37]) { const b = document.querySelector('[data-beat="' + beat + '"] .ib-nutshell b'); out[beat] = b ? getComputedStyle(b).fontSize : null; } return out; }""")
        out["1440"] = r14
        out["1440_errors"] = errors2
        br.close()
    print(json.dumps(out, indent=1))
    with open("proof-fixpass2/probe-360-1440.json", "w") as f:
        json.dump(out, f, indent=1)


if __name__ == "__main__":
    main()
