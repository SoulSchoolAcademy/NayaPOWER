#!/usr/bin/env python3
"""Apply Dashboard PASS-6 edits to dashboard-pass6.html (edit of pass-5 base).
Every replacement is asserted to match exactly once; the script aborts otherwise.
Edits:
 1. Orb number: same font, 28px -> 52px desktop, 40px phone (ultimate override).
 2. Phone orbs bigger: ldLayoutNodes nd mobile 64/66 -> 96, gap 40 -> 32.
 3. #os-pts-note: moved in-flow before the toggle; flow CSS, white 15px,
    slot always reserved (min-height), visibility toggled (never display:none).
 4. _refreshPtsNote: hidden <-> visibility.
 5. readSpine: featured-page noData falls back to the live world spine.
 6. paintRest quiet branch: the Quiet caption never renders (setCap('')).
 7. Ambassador sample link added to #os-feat-panel (+ CSS).
 8. ORB TILES desktop: .os-mini-num.orbnum tiles 16px/13px digit -> 26px/24px.
 9. ORB TILES phone: 11px/10px digit -> 20px/18px digit.
10. miniConvert: re-tile the CURRENT displayed value (fixes the % clobber:
    "44%" at +50ms reverted to "280" at +200ms by the debounced re-tile).
"""
import sys

P = 'dashboard-pass6.html'
s = open(P, encoding='utf-8').read()
orig = s

def rep(old, new, name):
    global s
    n = s.count(old)
    assert n == 1, f'{name}: matched {n}x (want exactly 1)'
    s = s.replace(old, new)
    print(f'ok {name}')

# 1a. Orb number desktop 28 -> 52, same font (family/weight/glow untouched).
rep(
  "  /* 2026-11-02 — Shawn: 75% size (28px), perfectly centered, minimal elegant glow */\n  font-size:28px !important;",
  "  /* PASS-6 2026-11-10 — Shawn's eye: the orb numbers are too small to read. SAME font as before (it looks good) — only the size grows, 28px -> 52px, so the number is the hero of the orb. The widest honest content (a flipped full number like \"3 937\", ~128px at 52px) still fits the 135px desktop orb. Phone size rides in the media query below. */\n  font-size:52px !important;",
  'orb-number-52px')

# 1b. Phone media query right after the .os-ld-lbl override rule.
rep(
  "  font-size:9px !important;\n  letter-spacing:.08em !important;\n  text-shadow:\n    0 1px 0 rgba(0,0,0,.9),\n    0 2px 6px rgba(0,0,0,.7),\n    0 0 14px var(--nc) !important;\n}",
  "  font-size:9px !important;\n  letter-spacing:.08em !important;\n  text-shadow:\n    0 1px 0 rgba(0,0,0,.9),\n    0 2px 6px rgba(0,0,0,.7),\n    0 0 14px var(--nc) !important;\n}\n/* PASS-6 2026-11-10 — phone orbs: SAME font, 40px. A 52px number cannot fit a phone orb (the widest content \"3 937\" is ~99px at 40px vs the 96px phone orb); 40px is the biggest size that fits the harvested orb. The orbs grow with it (ldLayoutNodes nd 64 -> 96). */\n@media (max-width:768px){\n  html body .os-constellation .os-ld-nodes button.os-ld-node span.os-ld-n{\n    font-size:40px !important;\n  }\n}",
  'orb-number-phone-40px')

# 2a. Phone orb diameter 64/66 -> 96.
rep(
  "  var nd = isMobile ? (isHero ? 66 : 64) : (isHero ? 160 : 135); /* FIX 6 — PHONE ORBIT CLEARANCE",
  "  var nd = isMobile ? 96 : (isHero ? 160 : 135); /* PASS-6 2026-11-10: phone orbs 64/66 -> 96 — the 40px number needs the room (widest content ~99px). Desktop untouched (160/135 already hold the 52px number). FIX 6 — PHONE ORBIT CLEARANCE",
  'phone-orb-96')

# 2b. Phone orbit gap 40 -> 32 (buys back some gauge room for the bigger orbs).
rep(
  "  var gap = isMobile ? 40 : 48; /* PASS-3 (ninth): phones get a 40px gap",
  "  var gap = isMobile ? 32 : 48; /* PASS-6 2026-11-10: phones 40 -> 32 — the bigger orbs (nd 96) eat orbit room, so the gap gives 8px back to the gauge. Desktop keeps 48px. PASS-3 (ninth): phones get a 40px gap",
  'phone-gap-32')

# 3. Move #os-pts-note in-flow BEFORE the toggle (was absolute after it).
rep(
  "<div class=\"os-pts-toggle\" id=\"os-pts-toggle\">\n  <button class=\"os-pts-btn active\" data-mode=\"pts\">PTS</button>\n  <button class=\"os-pts-btn\" data-mode=\"pct\">%</button>\n  <button class=\"os-pts-btn\" data-mode=\"money\">MONEY</button>\n</div>\n<div class=\"os-pts-note\" id=\"os-pts-note\" hidden></div>",
  "<!-- PASS-6 2026-11-10: the note lives HERE now — in flow under the gauge, above the mode bar. It was absolute bottom:64px after the toggle, anchored to hero-fit's stale-short box, and landed across the gauge face on desktop. In flow it cannot overlap the gauge: it sits below the whole constellation. -->\n<div class=\"os-pts-note\" id=\"os-pts-note\"></div>\n<div class=\"os-pts-toggle\" id=\"os-pts-toggle\">\n  <button class=\"os-pts-btn active\" data-mode=\"pts\">PTS</button>\n  <button class=\"os-pts-btn\" data-mode=\"pct\">%</button>\n  <button class=\"os-pts-btn\" data-mode=\"money\">MONEY</button>\n</div>",
  'note-moved-in-flow')

# 3b. Note CSS: flow, white 15px, slot always reserved, hidden by visibility.
rep(
  ".os-pts-note{font-size:12px;color:rgba(255,255,255,.65);text-align:center;margin:0;max-width:560px;line-height:1.45;padding:0 16px;position:absolute;left:50%;bottom:64px;transform:translateX(-50%);width:max-content;max-width:90%;z-index:100;} /* FIX 5 FIX 4: rides above the pinned mode bar. 2026-11-08: the bar is taller now (big coloured toggle) — the note rides 64px up. */",
  ".os-pts-note{font-size:15px;color:#fff;text-align:center;margin:10px auto 0;max-width:560px;line-height:1.5;padding:0 16px;min-height:45px;visibility:hidden;} /* PASS-6 2026-11-10: in-flow caption under the gauge, above the mode bar — white, bigger, readable. The slot is ALWAYS reserved (min-height 45px = two lines) so the fit scale never jumps when the note appears in % / MONEY mode; _refreshPtsNote toggles visibility, never display. The old absolute bottom:64px is gone: it anchored to hero-fit's stale-short box and sat across the gauge face. */",
  'note-css-flow')

# 4. _refreshPtsNote: hidden -> visibility (slot stays reserved).
rep(
  "          n.textContent = 'Money: your score as dollars — the gauge wraps every $500.';\n          n.hidden = false; return;",
  "          n.textContent = 'Money: your score as dollars — the gauge wraps every $500.';\n          n.style.visibility = 'visible'; return;",
  'note-js-money')
rep(
  "        if (window._dashPctMode !== true){ n.hidden = true; return; }",
  "        if (window._dashPctMode !== true){ n.style.visibility = 'hidden'; return; }",
  'note-js-pts')
rep(
  "        if (!names.length){ n.hidden = true; return; }\n        n.textContent = 'Counts stay counts: ' + names.join(', ') + ' — numbers, not points.';\n        n.hidden = false;",
  "        if (!names.length){ n.style.visibility = 'hidden'; return; }\n        n.textContent = 'Counts stay counts: ' + names.join(', ') + ' — numbers, not points.';\n        n.style.visibility = 'visible';",
  'note-js-pct')

# 5. readSpine: featured-page noData falls back to the live world spine.
rep(
  "      if (_fd.noData) return { state:'quiet', score:null, s:_ss }; /* FIXB 2026-11-07 (Fix 5): a featured page has no numbers — the gauge shows its quiet face, never the world spine. */",
  "      if (_fd.noData){ /* PASS-6 2026-11-10: a featured page has no numbers of its own — but the page holds live world numbers, so the gauge shows the world's live number, never the quiet face. Quiet while the world is live was the wrong state (Shawn's eye 05:15Z: a dash in the gauge center + 'Quiet' caption on a page full of live numbers). Only when the world spine itself has no finite score does the gauge stay quiet. Supersedes FIXB 2026-11-07 (Fix 5) for the live-world case. */\n        var _wsp = (typeof window !== 'undefined') ? window._osSpine : null;\n        var _wsc = _wsp ? spineGet(_wsp, 'score') : undefined;\n        if (typeof _wsc === 'number' && isFinite(_wsc)) return { state:'live', score:_wsc, s:_wsp };\n        return { state:'quiet', score:null, s:_ss };\n      }",
  'readspine-fallback')

# 6. The Quiet caption never renders.
rep(
  "      } else if (state === 'quiet'){\n        setCap('Quiet — nothing measured yet.');",
  "      } else if (state === 'quiet'){\n        /* PASS-6 2026-11-10: the Quiet caption never renders — it told a page full of live numbers that nothing was measured. The gauge shows the live number whenever one exists (readSpine falls back to the world spine); this branch survives only for a ledger that answered empty with no live number anywhere, and it shows no caption at all. */\n        setCap('');",
  'quiet-caption-gone')

# 7. Ambassador sample link on the headliner board.
rep(
  "<div class=\"os-feat-top\"><span class=\"os-feat-marker\" id=\"os-feat-marker\"></span><span class=\"os-feat-name\" id=\"os-feat-name\"></span></div>",
  "<div class=\"os-feat-top\"><span class=\"os-feat-marker\" id=\"os-feat-marker\"></span><span class=\"os-feat-name\" id=\"os-feat-name\"></span></div>\n<!-- PASS-6 2026-11-10: the Ambassador sample — the real ambassador link as it actually looks, harvested live from sb-api smart_links (owner flagship-personal, first link, name joinus, 2026-11-10). Short address nayanet.app/joinus, clickable to the real link. -->\n<div class=\"os-feat-sample\"><span class=\"os-feat-sample-tag\">Sample</span><a class=\"os-feat-sample-link\" href=\"https://nayanet.app/joinus\" target=\"_blank\" rel=\"noopener\">nayanet.app/joinus ↗</a></div>",
  'ambassador-sample-html')

# 7b. Sample CSS after .os-feat-scope.
rep(
  ".os-feat-scope{ margin:8px 0 0; }",
  ".os-feat-scope{ margin:8px 0 0; }\n/* PASS-6 2026-11-10 — the Ambassador sample: the real link as a real object (obsidian chip, purple headliner glow, same elite-button DNA as the mode buttons). */\n.os-feat-sample{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:12px 0 2px;}\n.os-feat-sample-tag{font-size:10px;font-weight:800;letter-spacing:.18em;color:#a06bff;text-transform:uppercase;}\n.os-feat-sample-link{display:inline-flex;align-items:center;gap:8px;padding:10px 18px;border-radius:999px;background:linear-gradient(180deg,#17171f,#0a0a0f);border:1.5px solid rgba(255,255,255,.5);color:#fff;font-size:17px;font-weight:800;text-decoration:none;box-shadow:inset 0 1.5px 0 rgba(255,255,255,.4),inset 0 -4px 8px rgba(0,0,0,.5),0 0 18px rgba(160,107,255,.5),0 8px 18px rgba(0,0,0,.5);}\n.os-feat-sample-link:hover{transform:translateY(-2px);}",
  'ambassador-sample-css')

# 8. ORB TILES — the real enlargement. The orb digits are NOT plain text in
# .os-ld-n: they are .os-mini-num.orbnum TILES (A-star/B-star law), and the
# tile rules capped the digits at 13px desktop / 10px phone — that is why
# Shawn's eye saw tiny numbers even after the .os-ld-n font grew to 52px
# (probe 2026-11-10: tiles "1 1 0 0" ~10px tall inside 73px orbs). Same font
# (inherit, weight 900) — only the tile sizes grow. Desktop orb is 135px:
# "1100" = 4x26px tiles + 3x3px gaps = 113px, fits with room at the bezel.
rep(
  ".os-mini-num.orbnum{gap:2px;}\n.os-mini-num.orbnum .os-mini-tile{width:16px;border-radius:4px;border-width:1px;}\n.os-mini-num.orbnum .os-mini-tile .cap{height:3px;}\n.os-mini-num.orbnum .os-mini-tile .rd{height:15px;line-height:15px;font-size:13px;}\n.os-mini-num.orbnum .os-mini-tile.dot{width:7px;}\n.os-mini-num.orbnum .os-mini-tile.dot .rd{height:15px;padding-bottom:2px;}\n.os-mini-num.orbnum .os-mini-tile.pct{width:18px;}\n.os-mini-num.orbnum .os-mini-gap{width:6px;}",
  "/* PASS-6 2026-11-10 — ORB TILES ENLARGED: the digits were 13px tiles inside a 135px orb (Shawn: 'too small to read'). Same tile font, grown: 24px digits, 26px tiles. */\n.os-mini-num.orbnum{gap:3px;}\n.os-mini-num.orbnum .os-mini-tile{width:26px;border-radius:5px;border-width:1px;}\n.os-mini-num.orbnum .os-mini-tile .cap{height:4px;}\n.os-mini-num.orbnum .os-mini-tile .rd{height:26px;line-height:26px;font-size:24px;}\n.os-mini-num.orbnum .os-mini-tile.dot{width:12px;}\n.os-mini-num.orbnum .os-mini-tile.dot .rd{height:26px;padding-bottom:3px;}\n.os-mini-num.orbnum .os-mini-tile.pct{width:28px;}\n.os-mini-num.orbnum .os-mini-gap{width:8px;}",
  'orbnum-tiles-desktop')

# 9. ORB TILES on phones (orb 96px): "1100" = 4x20px + 3x2px gaps = 86px.
rep(
  "@media (max-width:768px){\n  .os-mini-num.orbnum .os-mini-tile{width:11px;}\n  .os-mini-num.orbnum .os-mini-tile .cap{height:2px;}\n  .os-mini-num.orbnum .os-mini-tile .rd{height:11px;line-height:11px;font-size:10px;}\n  .os-mini-num.orbnum .os-mini-tile.pct{width:13px;}\n}",
  "@media (max-width:768px){\n  .os-mini-num.orbnum{gap:2px;}\n  .os-mini-num.orbnum .os-mini-tile{width:20px;}\n  .os-mini-num.orbnum .os-mini-tile .cap{height:3px;}\n  .os-mini-num.orbnum .os-mini-tile .rd{height:19px;line-height:19px;font-size:18px;}\n  .os-mini-num.orbnum .os-mini-tile.dot{width:9px;}\n  .os-mini-num.orbnum .os-mini-tile.pct{width:22px;}\n}",
  'orbnum-tiles-phone')

# 10. miniConvert: the % clobber. The mode flip wrote "44%" into the orb, and
# the debounced re-tile (150ms) re-rendered it from the stored POINTS back to
# "280" — probe 2026-11-10: "44%" at +50ms, "280" at +200ms, unit already "%".
# The flip handler already wrote the new value; the tiler must re-tile the
# CURRENT displayed value and fall back to stored points only when the
# current text is not a tileable number. Behaviour-preserving for every other
# tile (boards, drills, minis): their current text is always tileable, so
# they re-tile identically.
rep(
  "    if (tiled){\n      /* already tiled — a mode flip re-renders from the stored points\n         (the % is not invertible to points, so the points are stored) */\n      if (typeof el._osMiniPts !== 'number') return;\n      raw = el._osMiniPts;\n    } else {",
  "    if (tiled){\n      /* PASS-6 2026-11-10 — re-tile the CURRENT displayed value. The mode flip already wrote it ('44%' / '$1 100' / '280'); re-rendering blindly from the stored points CLOBBERED the % back to points 150ms after every flip. Only fall back to the stored points when the current text is not a tileable number (the % is not invertible to points, so the points are stored for exactly that case). */\n      var cur = (el.textContent || '').trim();\n      if (/^[$]?[0-9][0-9 ]*(\\.[0-9]+)?%?$/.test(cur)) raw = cur;\n      else if (typeof el._osMiniPts === 'number') raw = el._osMiniPts;\n      else return;\n    } else {",
  'miniconvert-no-clobber')

assert s != orig
open(P, 'w', encoding='utf-8').write(s)
print(f'wrote {P}: {len(orig)} -> {len(s)} bytes (+{len(s)-len(orig)})')
