#!/usr/bin/env python3
"""Transform bug-verify-v3.py -> bug-verify-v4.py (identity v3, heal gate).

Fresh aliases/profiles (v3's are claimed): healwalk2 / bugowner10 / mike9 /
bugfresh3, profiles /tmp/bug4-profile-*. Fixes the v3 probe's one stale
expectation ("Mike7" -> "Mike9": the composing certificate echoes the TYPED
alias pretty-printed, so mike9 echoes "Mike9" — the page was right, the
probe's hardcoded expectation was left over from v2's mike7).

Adds the heal-gate assertions v3 never made (leg b): after typing another
identity's alias and certifying it, the stored singleton pair must be
UNTOUCHED (still mike9/Mike) and the entry page's current Jump back in must
carry the stored pair — the v2 heal wrote the certified name against the
stored alias, which would have jumped the citizen into the wrong name.
"""
import re

SRC = "/home/hatch/workspace/team-nitro/walk/end-slide-10-20261112/bug-verify-v3.py"
DST = "/home/hatch/workspace/team-nitro/walk/end-slide-10-20261112/bug-verify-v4.py"

s = open(SRC).read()

# --- docstring header ---
s = s.replace(
    '"""NEW-ACCOUNT BUG verify v3 (Shawn 22:36Z) — AFTER the fix + heal + pair rule.\nRe-run of v2 with fresh aliases/profiles: the v2 run was killed by the\nruntime restart after 1 check, and /tmp was wiped (profiles gone, v1/v2\naliases already claimed).',
    '"""NEW-ACCOUNT BUG verify v4 (Shawn 22:36Z) — AFTER the identity v3 heal gate.\nRe-run of v3 with fresh aliases/profiles: v3 passed 63/64 (its 1 fail was a\nstale probe expectation, "Mike7" left over from v2), but reading the heal\nshowed a real gap v3 never asserted: the heal wrote the certified name\nagainst the stored alias even when the certified identity was ANOTHER\none (typing bugowner9 while stored as mike8). Identity v3 gates the\nsingleton heal on the certified alias BEING the stored alias; v4 proves\nthe gate (leg b) and re-proves the heal (leg 0) + the whole bug fix.')

# --- fresh aliases / profiles / outputs ---
reps = [
    ("/tmp/bug3-profile-poison", "/tmp/bug4-profile-poison"),
    ("/tmp/bug3-profile-main", "/tmp/bug4-profile-main"),
    ("healwalk1", "healwalk2"),
    ("bugowner9", "bugowner10"),
    ("mike8", "mike9"),
    ("bugfresh2", "bugfresh3"),
    ("bug-verify-results.json", "bug-verify-results-v4.json"),
    ("bug-verify-healed.png", "bug-verify-v4-healed.png"),
    ("bug-verify-cert-mike.png", "bug-verify-v4-cert-mike.png"),
    ("bug-verify-mike-end.png", "bug-verify-v4-mike-end.png"),
    ("bug-verify-others.png", "bug-verify-v4-others.png"),
    ("bug-verify-fresh-end.png", "bug-verify-v4-fresh-end.png"),
]
for old, new in reps:
    assert old in s, f"missing pattern: {old}"
    s = s.replace(old, new)

# --- the stale v2 expectation: composing echoes the TYPED alias ---
old_check = '''    check("(a) typing the alias echoes the NEW name (Mike7)",
          st2["displayName"].strip() == "Mike7", str(st2))'''
new_check = '''    check("(a) typing the alias echoes the typed alias (Mike9)",
          st2["displayName"].strip() == "Mike9", str(st2))'''
assert old_check in s, "stale Mike7 check not found"
s = s.replace(old_check, new_check)

# --- heal-gate assertions in leg (b), right after the certify check ---
anchor = '''    check("(b) typing the old alias certifies as Bug Owner (live check is the truth)",
          st3b["displayName"].strip() == "Bug Owner" and "welcome back" in st3b["status"], str(st3b))'''
gate = anchor + '''
    # HEAL GATE (identity v3): certifying ANOTHER identity must NOT rewrite
    # the stored singleton — the entry page jumps back in on the stored pair.
    check("(b) HEAL GATE: typing another alias leaves the stored pair untouched",
          p2.evaluate("localStorage.getItem('nayanet_smart_alias')") == "mike9"
          and p2.evaluate("localStorage.getItem('nayanet_smart_name')") == "Mike",
          p2.evaluate("() => localStorage.getItem('nayanet_smart_alias') + ' / ' + localStorage.getItem('nayanet_smart_name')"))
    check("(b) HEAL GATE: the identities list still holds both correct pairs",
          p2.evaluate("() => { const l = JSON.parse(localStorage.getItem('nayanet_smart_identities') || '[]'); return l.map(x => x.alias + ':' + x.name).join(','); }") == "bugowner10:Bug Owner,mike9:Mike",
          p2.evaluate("localStorage.getItem('nayanet_smart_identities')"))'''
assert anchor in s, "leg (b) certify anchor not found"
s = s.replace(anchor, gate)

# --- current-Jump check: after the others-list check, click the CURRENT jump ---
anchor2 = '''    p2.screenshot(path=OUT + "bug-verify-v4-others.png")
    p2.locator(".returning-other").click()'''
gate2 = '''    p2.screenshot(path=OUT + "bug-verify-v4-others.png")
    # HEAL GATE (continued): the CURRENT Jump back in carries the STORED pair.
    p2.locator("#jumpBackIn").click()
    p2.wait_for_timeout(2000)
    check("(b) HEAL GATE: current Jump back in carries the stored pair (Mike/mike9)",
          "/hub?" in p2.url and "name=Mike" in p2.url and "alias=mike9" in p2.url, p2.url)
    p2.goto(BASE + "/", wait_until="networkidle")
    p2.wait_for_timeout(1200)
    p2.locator(".returning-other").click()'''
assert anchor2 in s, "others screenshot anchor not found"
s = s.replace(anchor2, gate2)

open(DST, "w").write(s)
print("wrote", DST, len(s), "bytes")
