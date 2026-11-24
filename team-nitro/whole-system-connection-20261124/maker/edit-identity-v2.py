#!/usr/bin/env python3
"""Whole-system connection round — IDENTITY fix v2 (checker FAIL -> fix).

Input: maker/identity.html (v1 output, sha edb926dd). Output: same file,
in place. Every edit asserts its anchor; a failed assert stops the build.

Fixes (checker verdict 2026-11-24, items 61/70):
 6. Taken message: #aliasStatus "already claimed" was near-white
    rgb(242,242,246) at 14.08px — the base rule "taken stays honest
    silver-white" — and the green #hubNote + "This is me" button sat at
    y950 on a 900px viewport, entirely below the fold. Fix: the taken
    status goes GREEN (#2fe89e) + bigger (19px, weight 800), and the note
    scrolls into view (block:'center') the moment it appears, so the green
    note and the "This is me" button are IN VIEW on phone and desktop.
"""
import hashlib
import re

P = "/home/hatch/workspace/team-nitro/whole-system-connection-20261124/maker/identity.html"

text = open(P, encoding="utf-8", errors="ignore").read()
print("v2 input:", len(text.encode("utf-8")), hashlib.sha256(text.encode("utf-8")).hexdigest()[:12])
assert hashlib.sha256(text.encode("utf-8")).hexdigest().startswith("edb926dd"), "v1 base moved"


def replace_once(s, old, new, name):
    assert s.count(old) == 1, f"{name}: anchor count {s.count(old)} != 1: {old[:90]!r}"
    return s.replace(old, new, 1)


# ---------------------------------------------------------------- F6 taken status: GREEN + bigger
old = "#hubNote.fp-taken-green{color:#2fe89e !important;font-size:19px !important;font-weight:800;text-align:center}"
new = (old + "\n"
       "/* WHOLE-SYSTEM CONNECTION 2026-11-24 v2 (items 61/70): \"already claimed\"\n"
       "   goes GREEN + bigger + unmissable. The base rule kept it silver-white\n"
       "   at 14.08px — the fail. The green note below already carries the\n"
       "   detail; this line is the unmissable headline. */\n"
       ".alias-status[data-state=\"taken\"]{color:#2fe89e !important;font-size:19px !important;font-weight:800 !important;text-shadow:0 0 14px rgba(47,232,158,.35)}")
text = replace_once(text, old, new, "taken-green-bigger")

# ---------------------------------------------------------------- F6 taken note: scroll into view when it appears
old = "          note.appendChild(_tim);\n          return;"
new = ("          note.appendChild(_tim);\n"
       "          /* WHOLE-SYSTEM CONNECTION 2026-11-24 v2 (items 61/70): the green\n"
       "             note + \"This is me\" sat below the fold (y950 on a 900 viewport).\n"
       "             Bring them into view the moment they appear. */\n"
       "          try { note.scrollIntoView({block:'center'}); } catch(e){}\n"
       "          return;")
text = replace_once(text, old, new, "taken-note-into-view")

# ---------------------------------------------------------------- verify
assert '.alias-status[data-state="taken"]{color:#2fe89e !important;font-size:19px !important' in text
assert "note.scrollIntoView({block:'center'})" in text
assert "WALKTHROUGH_URL = '/?walk=1'" in text
assert "fpThisIsMe" in text
open(P, "w", encoding="utf-8").write(text)
b = len(text.encode("utf-8"))
print("V2 written:", P, b, "sha:", hashlib.sha256(text.encode("utf-8")).hexdigest()[:12])
scripts = re.findall(r"<script>(.*?)</script>", text, re.S)
print("script blocks:", len(scripts))
for i, sc in enumerate(scripts):
    open(f"/tmp/wsc-id2-{i}.js", "w").write(sc)
