#!/usr/bin/env python3
"""Apply the points-round edits to the Personal bytes (maker seat).

Inputs (read-only, never written):
  - ~/workspace/team-nitro/space-business-mirror-personal-20261112/personal-live.html
    (sha 992ab18c29315e7654f45c36eb43e30aadfc2ea5642394bbd9884f21617e3f50)
  - ~/workspace/team-nitro/page-audit-remeasure-20261112/personal-hero-fix.html
    (hero-fix <style> block, harvested byte-identical)
  - ~/workspace/team-nitro/page-audit-remeasure-20261112/personal-rooms-plus-fixed.html
    (template source for the clone builder; pill applied to a lane-local copy)

Outputs (this lane dir):
  - personal-points.html — live Personal + pill + wiring + hero-fix block
  - rooms-points.html  — rooms template source + pill + wiring (clone builder input)

Edits (each asserted by exact count):
  E1 pill markup — harvested verbatim from smart-skills-page.html lines
     2082-2086, inserted directly after #pname inside the name flex row.
     ONE permitted change: initial #pointscount content 0 -> … (the page's
     own loading glyph; the Skills 0 is a placeholder with no writer).
  E2 wiring — in loadPointsBoard's charts IIFE, immediately after the donut
     render (same tick the donut's total lands): set #pointscount to the same
     `total`, formatted with toLocaleString(). Guarded on window._dashD so a
     pre-data render leaves the … loading glyph instead of a false 0.
  E3 hero-fix — the 23-line <style id="hero-fix-20261112"> block, byte-identical
     from the audit file, inserted before </body> (the block the clones
     already carry; this is what lines the three heroes up at phone widths).
     Personal-points only — the rooms fix stays clone-only (pre-existing
     divergence, named in the record, not introduced here).
"""
import hashlib, os, re, sys

LANE = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.expanduser("~/workspace/team-nitro/space-business-mirror-personal-20261112")
AUDIT = os.path.expanduser("~/workspace/team-nitro/page-audit-remeasure-20261112")

def sha(b): return hashlib.sha256(b).hexdigest()
def read(p): return open(p, "rb").read()

LIVE_SHA = "992ab18c29315e7654f45c36eb43e30aadfc2ea5642394bbd9884f21617e3f50"

PILL = ('      <div class="ph-points" id="pointsdisplay" title="Your Naya points">\n'
        '        <span class="ph-points-star">✦</span>\n'
        '        <span id="pointscount">…</span>\n'
        '        <span class="ph-points-label">pts</span>\n'
        '      </div>\n')

WIRING = ('        /* POINTS PILL (2026-11-13): the hero pill beside the name (#pointscount)\n'
          '           shows this same total — the same tick the donut\'s total lands, so the\n'
          '           pill and the donut can never disagree in one session. Guarded on\n'
          '           window._dashD: before the live rows land the pill keeps its loading\n'
          '           glyph (…) instead of printing a false 0. */\n'
          '        try{ var _pc = document.getElementById(\'pointscount\');\n'
          '          if (_pc && window._dashD) _pc.textContent = total.toLocaleString(); }catch(_){}\n')

PNAME_ANCHOR = '      <div class="ph-nm" id="pname" title="Click to edit">Shawn Vibert</div>\n'
DONUT_ANCHOR = ("          donutWrap.innerHTML = '<div style=\"color:rgba(255,255,255,.4);font-size:14px;padding:40px;\">Earn points to see your breakdown</div>';\n"
                "        }\n")

def apply_pill_and_wiring(text, label):
    assert text.count(PNAME_ANCHOR) == 1, f"{label}: pname anchor count {text.count(PNAME_ANCHOR)}"
    assert 'id="pointsdisplay"' not in text, f"{label}: pill already present"
    text = text.replace(PNAME_ANCHOR, PNAME_ANCHOR + PILL, 1)
    assert text.count(DONUT_ANCHOR) == 1, f"{label}: donut anchor count {text.count(DONUT_ANCHOR)}"
    assert "POINTS PILL (2026-11-13)" not in text, f"{label}: wiring already present"
    text = text.replace(DONUT_ANCHOR, DONUT_ANCHOR + WIRING, 1)
    return text

def check_common(text, label):
    assert text.count('id="pointsdisplay"') == 1, f"{label}: pointsdisplay count"
    assert text.count('id="pointscount"') == 1, f"{label}: pointscount element count"
    assert text.count("getElementById('pointscount')") == 1, f"{label}: wiring writer count"
    assert '<span id="pointscount">0</span>' not in text, f"{label}: placeholder 0 present"
    assert '<span id="pointscount">…</span>' in text, f"{label}: loading glyph missing"
    assert text.count("pointscount") == 4, f"{label}: pointscount occurrences {text.count('pointscount')} (want CSS + element + writer + wiring comment)"
    assert text.count("#pointscount") == 2, f"{label}: #pointscount occurrences (want CSS selector + wiring comment)"
    # no second points display: the pill is the only pointsdisplay on the page
    assert text.count("pointsdisplay") == 1, f"{label}: pointsdisplay occurrences"

def main():
    live_b = read(os.path.join(SRC_DIR, "personal-live.html"))
    assert sha(live_b) == LIVE_SHA, f"live base sha moved: {sha(live_b)}"
    live = live_b.decode("utf-8")
    hero = read(os.path.join(AUDIT, "personal-hero-fix.html")).decode("utf-8", "replace")
    m = re.search(r'<style id="hero-fix-20261112">.*?</style>', hero, re.S)
    assert m, "hero block not found in hero-fix file"
    hero_block = m.group(0)
    assert hero_block.count("\n") + 1 == 23, f"hero block lines {hero_block.count(chr(10))+1}"
    assert 'id="hero-fix-20261112"' not in live, "hero block already in live Personal"

    # --- personal-points.html: live + pill + wiring + hero-fix ---
    personal = apply_pill_and_wiring(live, "personal")
    idx = personal.rfind("</body>")
    assert idx > 0
    personal = personal[:idx] + hero_block + "\n" + personal[idx:]
    assert personal.count('id="hero-fix-20261112"') == 1
    check_common(personal, "personal-points")
    p_path = os.path.join(LANE, "personal-points.html")
    open(p_path, "w", encoding="utf-8").write(personal)
    print("personal-points.html sha:", sha(personal.encode("utf-8")), "bytes:", len(personal.encode("utf-8")))

    # --- rooms-points.html: rooms template source + pill + wiring (no hero block here;
    #     the clone builder appends the hero block, exactly as build-clone.py does) ---
    rooms_b = read(os.path.join(AUDIT, "personal-rooms-plus-fixed.html"))
    rooms_sha = sha(rooms_b)
    print("rooms source sha (audit file, untouched):", rooms_sha, "bytes:", len(rooms_b))
    rooms = rooms_b.decode("utf-8")
    assert 'id="hero-fix-20261112"' not in rooms, "hero block already in rooms file"
    rooms = apply_pill_and_wiring(rooms, "rooms")
    check_common(rooms, "rooms-points")
    r_path = os.path.join(LANE, "rooms-points.html")
    open(r_path, "w", encoding="utf-8").write(rooms)
    print("rooms-points.html sha:", sha(rooms.encode("utf-8")), "bytes:", len(rooms.encode("utf-8")))

    # --- diff audit: personal-points vs live = pill + wiring + hero block, nothing else ---
    import difflib
    def ops(a, b):
        return [(t, i1, i2, j1, j2) for t, i1, i2, j1, j2 in
                difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if t != "equal"]
    for t, i1, i2, j1, j2 in ops(live.splitlines(), personal.splitlines()):
        seg = "\n".join(personal.splitlines()[j1:j2])
        ok = ("ph-points" in seg or "POINTS PILL" in seg or "pointscount" in seg
              or "hero-fix-20261112" in seg or "HERO OVERLAP FIX" in seg)
        print(f"personal-vs-live {t} lines {j1}:{j2} ok={ok}")
        assert ok, f"unexpected personal-vs-live hunk: {seg[:300]}"
    rooms_src = rooms_b.decode("utf-8")
    for t, i1, i2, j1, j2 in ops(rooms_src.splitlines(), rooms.splitlines()):
        seg = "\n".join(rooms.splitlines()[j1:j2])
        ok = ("ph-points" in seg or "POINTS PILL" in seg or "pointscount" in seg)
        print(f"rooms-points-vs-rooms {t} lines {j1}:{j2} ok={ok}")
        assert ok, f"unexpected rooms-points hunk: {seg[:300]}"
    print("EDITS OK")

if __name__ == "__main__":
    main()
