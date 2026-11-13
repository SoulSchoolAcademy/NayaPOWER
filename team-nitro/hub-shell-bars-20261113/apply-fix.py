#!/usr/bin/env python3
"""Hub Shell Bars — apply the bar edits to the working copy (edit, never rebuild).
Base: the slug-round fixed shell (5,555,559 B, sha 727abfd1... — asserted).
Harvest is EXTRACTED from the sources at apply time, never retyped:
  trio CSS + gem ICONS + SEGS + segment-creation lines come from
  ~/workspace/team-nitro/bottom-icons-ultimate-trio-20261113/hub-fixed.html
  (the bottom-icons Hub leg, checker PASS 8/10).
Upper-row circles are composed from this shell's own .eco-bb-ico
(lines 308-357: 46px desktop / 44px phone, border-radius:50%).
Every edit asserts its anchor count == 1 and aborts on any move.
The note and the slug fix (SLUG_MAP + maybeAuto guard) are never touched:
verified present-and-unchanged after the edits.
Usage: apply-fix.py
"""
import hashlib
import sys

WD = "/home/hatch/workspace/team-nitro/hub-shell-bars-20261113"
PATH = WD + "/index-intel-today.html"
HUBFIXED = "/home/hatch/workspace/team-nitro/bottom-icons-ultimate-trio-20261113/hub-fixed.html"
BASE_SHA = "727abfd1a96469fa27bceaefd027e0810a8b5577b410f67647fdb47b4f68cd24"

data = open(PATH, "rb").read()
assert hashlib.sha256(data).hexdigest() == BASE_SHA, "working copy moved — STOP"
text = data.decode("utf-8")
lines = text.split("\n")
print(f"base ok: {len(data)} B sha {BASE_SHA[:12]}... lines={len(lines)}")

hub = open(HUBFIXED, encoding="utf-8").read().split("\n")

def find_line(pred, where, label):
    hits = [i for i, l in enumerate(where) if pred(l)]
    assert len(hits) == 1, f"{label}: found {len(hits)} (need 1)"
    return hits[0]

def find_all(pred, where, label):
    hits = [i for i, l in enumerate(where) if pred(l)]
    assert hits, f"{label}: found none"
    return hits

# ---- HARVEST EXTRACTION (verbatim from the bottom-icons Hub leg) ----
# Trio CSS: the BOTTOM ICONS comment block through the phone @media block,
# ending just before the eco-dock comment.
tri_start = find_line(lambda l: l.startswith("/* ——— BOTTOM ICONS 2026-11-13: the trio tiles ARE"), hub, "trio css start")
tri_end = find_line(lambda l: l.startswith("/* The eco dock rides above the notifications bar"), hub, "trio css end")
trio_css = "\n".join(hub[tri_start:tri_end]).rstrip("\n")
assert ".notif-tile {" in trio_css and "border-radius: 50%;" in trio_css
assert "width: 38px; height: 38px;" in trio_css and "width: 27px; height: 27px;" in trio_css
assert "16px" not in trio_css.split(".notif-tile {")[1].split("}")[0], "trio tile still square?"
print(f"harvest trio css: {len(trio_css)} chars, {trio_css.count(chr(10))+1} lines")

# Gem ICONS: the three SVG lines in the leg's ICONS object.
icon_lines = [hub[i] for i in find_all(
    lambda l: l.strip().startswith(("personal: '<svg", "business: '<svg", "thing: '<svg")), hub, "gem icons")]
assert len(icon_lines) == 3, f"gem icons: {len(icon_lines)}"
assert icon_lines[0].strip().startswith("personal:") and icon_lines[1].strip().startswith("business:")
assert icon_lines[2].strip().startswith("thing:")
assert "rgba(160,107,255" in icon_lines[0] and "rgba(47,232,158" in icon_lines[1]
print("harvest gem icons: 3 lines (amethyst / emerald / diamond)")

# SEGS line.
segs_line = hub[find_line(lambda l: l.strip().startswith("var SEGS = [['personal'"), hub, "segs")].strip()
assert "'amethyst'" in segs_line and "'emerald'" in segs_line and "'diamond'" in segs_line
assert "space" not in segs_line.lower().replace("spaces", ""), "third segment labelled space?"
print(f"harvest segs: {segs_line[:80]}...")

# Segment-creation lines (id / data-notif+data-gem / --nc / aria-label / innerHTML).
seg_id = find_line(lambda l: l.strip().startswith("b.id = 'seg'"), hub, "seg id line")
seg_block = hub[seg_id:seg_id + 5]
assert seg_block[1].strip().startswith("b.setAttribute('data-notif'") and "data-gem" in seg_block[1]
assert "activity — open" in seg_block[3] and "notif-lbl" in seg_block[4]
print("harvest seg creation: 5 lines")

def replace_once(old, new, label):
    global text, lines
    n = text.count(old)
    assert n == 1, f"{label}: anchor count {n} (need 1)"
    text = text.replace(old, new)
    lines = text.split("\n")
    print(f"edit {label}: ok")

# ---- EDIT 1 — remove the Activity pill (markup) ----
ACT = ('  <a class="obb-pill" data-obb="activity" data-b3="activity" href="https://nayanet.app/#/hub/feed" '
       'style="--obb:#a06bff" aria-label="Activity" title="Activity"><span class="obb-jewel" aria-hidden="true">◈</span>'
       '<span class="obb-lbl">Activity</span><span class="obb-badge os-b3-badge" id="os-b3-badge" hidden></span></a>\n')
replace_once(ACT, "", "1 activity pill removed")
assert text.count('data-obb="activity"') == 0 and text.count("os-b3-badge") == 0

# ---- EDIT 2 — upper-row circles (obb CSS, lines 9705-9711) ----
old_start = find_line(lambda l: l.startswith(".obb-pill{flex:0 0 auto;scroll-snap-align:start"), lines, "obb css start")
old_end = find_line(lambda l: l.startswith("@media (max-width:640px){.obb-bar{"), lines, "obb css end")
assert old_end - old_start == 6, f"obb css slice is {old_end - old_start} lines, expected 6"
new_obb = """/* SHELL BARS 2026-11-13 — the upper row is round black circles. .obb-pill is
   now the transparent column button and .obb-jewel IS the circle, harvested
   from this shell's own .eco-bb-ico (lines 308-357): 46px desktop / 44px
   phone, border-radius:50%, obsidian radial gradient, own-color rest glow
   via --obb. The visible .obb-lbl rides under the icon, unchanged. The
   Activity pill is gone with its badge rule deleted) — one door
   per destination. Hover/focus lift lands on the jewel, as on .eco-bb-btn. */
.obb-pill{flex:0 0 auto;scroll-snap-align:start;scroll-snap-stop:always;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;min-width:0;padding:2px 4px 0;background:none;border:none;box-shadow:none;text-decoration:none;color:#fff;cursor:pointer;position:relative}
.obb-pill:hover .obb-jewel,.obb-pill:focus-visible .obb-jewel{transform:translateY(-3px) scale(1.08);border-color:var(--obb);color:var(--obb);text-shadow:0 0 6px var(--obb);box-shadow:inset 0 1px rgba(255,255,255,.2),0 0 24px color-mix(in srgb,var(--obb) 55%,transparent),0 6px 16px rgba(0,0,0,.5)}
.obb-pill:focus-visible{outline:none}
.obb-pill:active .obb-jewel{transform:scale(1.02)}
.obb-jewel{width:46px;height:46px;flex:0 0 46px;border-radius:50%;display:grid;place-items:center;font-size:18px;color:#fff;background:radial-gradient(circle at 35% 30%,#2a2a32,#0a0a0e 70%);border:1px solid rgba(255,255,255,.3);box-shadow:inset 0 1px rgba(255,255,255,.15),0 0 14px rgba(255,255,255,.1),0 4px 10px rgba(0,0,0,.4),0 0 14px -2px var(--obb);transition:all .22s cubic-bezier(.16,.84,.22,1)}
.obb-lbl{font-size:10.5px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#fff;white-space:nowrap;line-height:1}
@media (max-width:640px){.obb-bar{gap:6px;padding:8px 10px calc(8px + env(safe-area-inset-bottom,0px))}.obb-row{gap:6px;scroll-padding:0 10px}.obb-pill{padding:2px 3px 0}.obb-jewel{width:44px;height:44px;flex:0 0 44px;font-size:16px}.obb-lbl{font-size:9px}}"""
lines[old_start:old_end + 1] = new_obb.split("\n")
text = "\n".join(lines)
lines = text.split("\n")
print("edit 2 upper-row circles: ok")
assert text.count(".obb-badge") == 0, "obb-badge survived"
assert "gap:4px;min-width:0;padding:2px 4px 0;background:none;border:none;box-shadow:none" in text, "new pill rule missing"
assert "border-radius:50%;display:grid;place-items:center;font-size:18px" in text, "new jewel rule missing"

# ---- EDIT 3 — trio CSS transplant (gate tile, verbatim) ----
t_start = find_line(lambda l: l == ".notif-tile {", lines, "trio css start")
h_start = find_line(lambda l: l.startswith(".notif-seg.has-news .notif-tile {"), lines, "has-news start")
h_end = h_start
while lines[h_end].strip() != "}":
    h_end += 1
header = ("/* SHELL BARS 2026-11-13 — trio transplanted VERBATIM from the bottom-icons "
          "Hub leg (hub-fixed.html); the BOTTOM ICONS comment below is the leg's own. */")
lines[t_start:h_end + 1] = (header + "\n" + trio_css).split("\n")
text = "\n".join(lines)
lines = text.split("\n")
print("edit 3 trio css transplant: ok")
assert "border-radius: 16px" not in text.split(".notif-tile {")[1].split(".notif-count")[0]

# ---- EDIT 4 — eco-offset fallback follows the new trio height (both sites) ----
n79 = text.count("var(--notif-h, 79px)")
assert n79 == 2, f"eco fallback sites: {n79} (need 2)"
eco_rule = find_line(lambda l: l.startswith("body.has-notif .eco-bottombar {"), lines, "eco rule")
lines.insert(eco_rule, "/* SHELL BARS 2026-11-13: fallback follows the new trio height (85px desktop per the bottom-icons round); syncStack measures the live row — the fallback is pre-init only. */")
text = "\n".join(lines)
text = text.replace("var(--notif-h, 79px)", "var(--notif-h, 85px)")
lines = text.split("\n")
print("edit 4 eco fallback 79 -> 85 (2 sites): ok")

# ---- EDIT 5a — counts() re-keyed to the worlds ----
replace_once(
    "      return { mail: this.get('mail'), activity: unread, spaces: this.get('spaces') };",
    "      return { personal: unread, business: this.get('mail'), thing: this.get('spaces') };",
    "5a counts re-keyed")
# Storage keys keep their names (the Hub writes nayanet.notif.mail / .spaces);
# only the segments are re-keyed. Personal reads ActivityLog unread, as before.

# ---- EDIT 5b — tap(k): worlds by full URL ----
t_start = find_line(lambda l: l.strip() == "tap(k) {", lines, "tap start")
t_end = t_start
while lines[t_end].strip() != "},":
    t_end += 1
new_tap = """    tap(k) {
      /* SHELL BARS 2026-11-13 — ULTIMATE TRIO (bottom-icons Hub leg): tap opens
         the WORLD by full URL — the worlds are top-level pages, and the 9-pill
         row navigates by full URL too, so no router path is invented here. The
         count for that world clears on tap, as the channels' counts did before. */
      if (k === 'personal') { try { this.set('seen.activity', ActivityLog.read().length); } catch (e) {} window.location.href = 'https://nayanet.app/personal'; }
      else if (k === 'business') { this.set('mail', 0); window.location.href = 'https://nayanet.app/business'; }
      else if (k === 'thing') { this.set('spaces', 0); window.location.href = 'https://nayanet.app/space'; }
      this.refresh();
    },"""
lines[t_start:t_end + 1] = new_tap.split("\n")
text = "\n".join(lines)
lines = text.split("\n")
print("edit 5b tap re-keyed: ok")
assert text.count("NayaRouter.navigate('/hub/mail')") == 0
assert text.count("NayaRouter.navigate('/hub/feed-activity')") == 0
assert text.count("NayaRouter.navigate('/hub/spaces')") == 0

# ---- EDIT 5c — gem ICONS (verbatim extraction) ----
i_start = find_line(lambda l: l.strip() == "var ICONS = {", lines, "icons start")
assert lines[i_start + 1].strip().startswith("mail: '<svg")
assert lines[i_start + 2].strip().startswith("activity: '<svg")
assert lines[i_start + 3].strip().startswith("spaces: '<svg")
lines[i_start + 1:i_start + 4] = icon_lines
text = "\n".join(lines)
lines = text.split("\n")
print("edit 5c gem icons: ok")

# ---- EDIT 5d — SEGS (verbatim extraction) ----
old_segs = "      var SEGS = [['mail', 'MAIL', '#3fb8ff'], ['activity', 'ACTIVITY', '#2fe89e'], ['spaces', 'SPACES', '#ffbf3d']];"
replace_once(old_segs, "      " + segs_line, "5d segs re-keyed")

# ---- EDIT 5e — segment creation (verbatim extraction) ----
s_start = find_line(lambda l: l.strip().startswith("b.setAttribute('data-notif'"), lines, "seg create start")
assert lines[s_start + 1].strip().startswith("b.setAttribute('aria-label', s[1] + ' — open');")
assert lines[s_start + 2].strip().startswith("b.setAttribute('title', s[1]);")
assert lines[s_start + 3].strip().startswith("b.innerHTML = '<span class=\"notif-tile\">'")
lines[s_start:s_start + 4] = seg_block
text = "\n".join(lines)
print("edit 5e seg creation: ok")

# ---- POST-EDIT GUARDS: the note + the slug fix survive untouched ----
assert text.count("SLUG_MAP") == 2, "SLUG_MAP moved!"
assert "var isNoteLanding" in text and "if (!isNoteLanding) window.NayaInstall.maybeAuto();" in text
assert "'sn-2696': 'IB-SMART-NOTE-20261112-the-infinite-smart-feeds'" in text
assert text.count("data-obb=") == 9, f"upper doors: {text.count('data-obb=')} (need 9)"
assert text.count("notif-seg") >= 3
assert "MAIL" not in text.split("var SEGS")[1].split("];")[0], "old SEGS survived?"
out = text.encode("utf-8")
open(PATH, "wb").write(out)
print(f"WROTE {PATH}: {len(out)} B sha256 {hashlib.sha256(out).hexdigest()}")
print(f"delta vs base: {len(out) - len(data):+d} B")
