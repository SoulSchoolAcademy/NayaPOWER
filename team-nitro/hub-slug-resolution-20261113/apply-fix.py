#!/usr/bin/env python3
"""Hub Slug Resolution — apply the chosen fix to the v2 baked shell.

Option 1 (scorecard winner) + Option 4 (rides with it, suppress variant).
Base: ~/workspace/team-nitro/hub-shell-rebake-v2-20261113/index-intel-today.html
  (v2 baked shell, 5,553,655 B, sha256 49b47e68fa987855127636d3487286046600fc03e123b84dc4aec2f302f25d52)
Output: index-intel-today.html in THIS work dir (the fixed shell).
Edit, never rebuild: two byte-exact insertions, each anchor asserted count == 1.
No live touch, no worker edit, no feed edit. STAGING ONLY.

Edit 1 — slug map in findNoteBySlug (Option 1):
  The approved public slug map, harvested verbatim from the phase-1 worker's
  PHASE1_CANDIDATE table (slug "sn-2696" -> id
  "IB-SMART-NOTE-20261112-the-infinite-smart-feeds"). Consulted FIRST, so an
  approved slug always wins; unlisted slugs fall through to the existing
  digit/full-id scans and can never resolve a note the worker would not serve.
  One line per future approved candidate; never widened by hand.
  (Considered and rejected: scanning note TITLES for snNNNN — it would resolve
  notes the publication allowlist has not approved, bypassing the gate.)

Edit 2 — install-modal bar on note landings (Option 4, suppress variant):
  maybeAuto is deferred one tick and skipped when the landing is a note route
  (hash #/smart-notes|notes|note/ or clean path /smart-notes|notes|note/).
  The one-tick deferral lets the router settle the hash from a clean note path
  before the 1600 ms auto-show timer starts; the /s/<slug> 302 already carries
  the hash. maybeAuto still runs on every other landing. The install prompt
  itself is untouched — only its auto-show on a reading landing is suppressed.
  Delay variant rejected: it would still pop over the note while reading.
"""
import hashlib
import sys

WD = "/home/hatch/workspace/team-nitro/hub-slug-resolution-20261113"
BASE = "/home/hatch/workspace/team-nitro/hub-shell-rebake-v2-20261113/index-intel-today.html"
BASE_SHA = "49b47e68fa987855127636d3487286046600fc03e123b84dc4aec2f302f25d52"
BASE_BYTES = 5553655
OUT = WD + "/index-intel-today.html"

src = open(BASE, "rb").read()
assert len(src) == BASE_BYTES, f"base size moved: {len(src)} != {BASE_BYTES} — STOP"
assert hashlib.sha256(src).hexdigest() == BASE_SHA, "base sha moved — STOP"
text = src.decode("utf-8")

# --- Edit 1 anchor: findNoteBySlug head (v2 shell line 6654-6657) ---
ANCHOR1 = (
    "  function findNoteBySlug(slug) {\n"
    "    var notes = (window.NayaFeedIntelligence && window.NayaFeedIntelligence.notes) || [];\n"
    "    var s = String(slug || '').toLowerCase();\n"
    "    if (!s) return null;\n"
)
assert text.count(ANCHOR1) == 1, f"anchor1 count {text.count(ANCHOR1)} != 1 — STOP"
INSERT1 = (
    "    /* Slug-resolution round (2026-11-13): the approved public slug map,\n"
    "       harvested verbatim from the phase-1 worker's PHASE1_CANDIDATE table\n"
    "       (slug \"sn-2696\" -> id \"IB-SMART-NOTE-20261112-the-infinite-smart-feeds\").\n"
    "       A short slug is a publication allowlist entry, not a substring of a\n"
    "       feed id: SN-2696's feed id carries no sn2696, so the digit scan below\n"
    "       can never find it. The map is consulted FIRST, so an approved slug\n"
    "       always wins; unlisted slugs still fall through to the digit/full-id\n"
    "       scans below and can never resolve a note the worker would not serve.\n"
    "       Add one line per future approved candidate; never widen it by hand. */\n"
    "    var SLUG_MAP = { 'sn-2696': 'IB-SMART-NOTE-20261112-the-infinite-smart-feeds' };\n"
    "    var snKey = s.match(/^sn-?(\\d+)$/);\n"
    "    if (snKey) {\n"
    "      var mappedId = SLUG_MAP['sn-' + String(parseInt(snKey[1], 10))];\n"
    "      if (mappedId) {\n"
    "        for (var mi = 0; mi < notes.length; mi++) {\n"
    "          if (String((notes[mi] && notes[mi].id) || '').toLowerCase() === mappedId.toLowerCase()) return notes[mi];\n"
    "        }\n"
    "      }\n"
    "    }\n"
)
text = text.replace(ANCHOR1, ANCHOR1 + INSERT1, 1)

# --- Edit 2 anchor: maybeAuto call (v2 shell line 5746) ---
ANCHOR2 = "  window.NayaInstall.maybeAuto();\n"
assert text.count(ANCHOR2) == 1, f"anchor2 count {text.count(ANCHOR2)} != 1 — STOP"
INSERT2 = (
    "  /* Slug-resolution round (2026-11-13): a note landing is a reading\n"
    "     landing — the install overlay must never cover first paint for a\n"
    "     fresh visitor who followed a note link. maybeAuto still runs on\n"
    "     every other landing. The check is deferred one tick so the router\n"
    "     below has settled the hash from a clean note path\n"
    "     (/smart-notes/<slug> served as the shell) before the 1600 ms\n"
    "     auto-show timer starts; the /s/<slug> 302 already carries the hash. */\n"
    "  setTimeout(function () {\n"
    "    var lh = String(location.hash || '');\n"
    "    var lp = String(location.pathname || '');\n"
    "    var isNoteLanding = lh.indexOf('#/smart-notes/') === 0 || lh.indexOf('#/notes/') === 0 || lh.indexOf('#/note/') === 0 || /^\\/(?:smart-notes|notes|note)\\//.test(lp);\n"
    "    if (!isNoteLanding) window.NayaInstall.maybeAuto();\n"
    "  }, 0);\n"
)
text = text.replace(ANCHOR2, INSERT2, 1)

out = text.encode("utf-8")
open(OUT, "wb").write(out)
print(f"base: {len(src)} B sha {hashlib.sha256(src).hexdigest()}")
print(f"fixed: {len(out)} B sha {hashlib.sha256(out).hexdigest()}")
print(f"delta: +{len(out) - len(src)} B")
print(f"SLUG_MAP count: {text.count(chr(39)+'sn-2696'+chr(39)+':')}")
print(f"findNoteBySlug count: {text.count('findNoteBySlug')}")
print(f"maybeAuto call sites (guarded): {text.count('window.NayaInstall.maybeAuto()')}")
print("OK fixed shell written to", OUT)
