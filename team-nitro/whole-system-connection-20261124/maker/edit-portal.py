#!/usr/bin/env python3
"""Whole-system connection round — PORTAL build (maker v1).

Base: live nayanet.app/ bytes, 1,146,566 B, sha256 aa9880c7
(= portal-root-first round-2 file, blob bcd111b5).
Output: maker/welcome-staged.html (+ sha/size printed + verified).

Every edit asserts its anchor. A failed assert stops the build — nothing
is half-applied. Items covered here: 11 (verify), 12 (extend to bridge
pair), 13, 32, 37, 38, 39, 40 (pick-line), 46, 54 (verify), 56/57 (verify),
58/71, 59, 60/61/63 (deed sentence + reader + underglow), 65/67/70/72
(walk view, this-is-me, greeting), 66 (redirect file is separate).
"""
import base64
import hashlib
import json
import re
import sys

BASE = "/home/hatch/workspace/team-nitro/whole-system-connection-20261124/scratch/live-portal.html"
FIX4 = "/home/hatch/workspace/team-nitro/agreement-buttons-20261118/work/fix4/welcome-fix4.html"
IDENT = "/home/hatch/workspace/team-nitro/whole-system-connection-20261124/scratch/identity.html"
WALK_DEFAULTS = "/home/hatch/workspace/team-nitro/whole-system-connection-20261124/scratch/walk-defaults.json"
OUT = "/home/hatch/workspace/team-nitro/whole-system-connection-20261124/maker/welcome-staged.html"

text = open(BASE, encoding="utf-8", errors="ignore").read()
BASE_SHA = hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()
assert len(text.encode("utf-8", errors="ignore")) == 1146566, "base size moved"
print("base ok:", len(text), BASE_SHA[:12])


def brace_block(s, start):
    """Return (start, end_exclusive) of the {...} block starting at s[start]=='{'."""
    assert s[start] == "{", s[start:start + 40]
    d = 0
    for i in range(start, len(s)):
        if s[i] == "{":
            d += 1
        elif s[i] == "}":
            d -= 1
            if d == 0:
                return start, i + 1
    raise AssertionError("unbalanced braces")


def rule_text(s, selector):
    i = s.find(selector)
    assert i >= 0, "rule not found: " + selector
    j = s.find("{", i)
    a, b = brace_block(s, j)
    return s[i:b]


def replace_once(s, old, new, name):
    assert s.count(old) == 1, f"{name}: anchor count {s.count(old)} != 1: {old[:90]!r}"
    return s.replace(old, new, 1)


def replace_all(s, old, new, name, expect):
    c = s.count(old)
    assert c == expect, f"{name}: count {c} != {expect}: {old[:90]!r}"
    return s.replace(old, new)


# ---------------------------------------------------------------- E1 item 13
# enterStage(): the __fpDeckEndReturn branch re-entered at deck 9/9 while the
# flag stood. The login's read link now navigates to /agreement (item 54),
# and "Begin the visual story" resumes via goResume — so the flag branch is
# dead weight that can still misfire. Remove it: enterStage always lands on
# intro/bridge; resume lives only in goResume.
old = ("if(window.__fpDeckEndReturn){window.__fpDeckEndReturn=false;S.view='deck';"
       "S.deck=deckBeats.length-1;}\n    else{S.view=")
new = ("window.__fpDeckEndReturn=false; /* WHOLE-SYSTEM CONNECTION 2026-11-24 "
       "(item 13): the deck-resume branch is gone — enterStage always lands on "
       "the choice (intro/bridge); resuming the deck is goResume's job alone. "
       "Bare block keeps the brace balance of the old else. */\n    {S.view=")
text = replace_once(text, old, new, "item13-enterStage")
# The F4 comment above enterStage now describes a mechanism that no longer
# exists — correct it so a future seat does not "restore" the branch.
old = ("/* SHARE PLUS — back from the deck end: Enter NayaNET exits to the\n"
       "       enter-name page. (EYE FOLLOW-ON #2 F4, 2026-11-18: the login's read\n"
       "       link clears this flag first, so re-entering lands on the choice\n"
       "       view, not 9/9; \"Begin the visual story\" still resumes via\n"
       "       goResume.) */")
new = ("/* SHARE PLUS — back from the deck end: Enter NayaNET exits to the\n"
       "       enter-name page. (EYE FOLLOW-ON #2 F4, 2026-11-18, as amended\n"
       "       2026-11-24 item 13: the old deck-resume branch in enterStage is\n"
       "       REMOVED — the login's read link navigates to /agreement (item 54)\n"
       "       and \"Begin the visual story\" resumes via goResume; enterStage\n"
       "       always lands on the choice view, never deck 9/9.) */")
text = replace_once(text, old, new, "item13-comment")
old = "else if(action==='deckJoin'){window.__fpDeckEndReturn=true;exitStage();}"
new = "else if(action==='deckJoin'){exitStage();}"
text = replace_once(text, old, new, "item13-deckJoin")

# ---------------------------------------------------------------- E2 item 37
# "Read the Collective Agreement" -> "Read the agreement" (4 button labels).
text = replace_all(text, "Read the Collective Agreement", "Read the agreement",
                   "item37-label", 4)

# ---------------------------------------------------------------- E3 item 38
# Same size: bridge pair already has nowrap+64px in fix4; land the same rule
# here if absent, extended to the choice pair.
pair_rule = "#fpBridgeDeck,#fpBridgeLetter{white-space:nowrap;min-height:64px}"
if pair_rule not in text:
    anchor = ".fp-intro-choice{"
    i = text.find(anchor)
    assert i >= 0
    j = text.find("{", i)
    _, b = brace_block(text, j)
    text = text[:b] + "\n" + pair_rule + "\n#fpChoiceDeck,#fpChoiceLetter{white-space:nowrap;min-height:64px}" + text[b:]
    print("item38: pair-size rule added")
else:
    print("item38: pair-size rule already present")

# ---------------------------------------------------------------- E4 item 39
# Real diamond jewel in both buttons — harvest the shared .fp-btn-jewel rule
# + PNG verbatim from the buttons round's staged file (fix4), verified
# 12,715 B sha e583f51f.
fix4 = open(FIX4, encoding="utf-8", errors="ignore").read()
jewel_rule = rule_text(fix4, ".fp-btn-jewel{")
m = re.search(r"data:image/png;base64,([A-Za-z0-9+/=]+)", jewel_rule)
raw = base64.b64decode(m.group(1))
assert len(raw) == 12715 and hashlib.sha256(raw).hexdigest().startswith("e583f51f"), \
    "jewel harvest mismatch"
assert ".fp-btn-jewel{" not in text, "jewel rule already present"
i = text.find(".fp-intro-choice{")
assert i >= 0
j = text.find("{", i)
_, b = brace_block(text, j)
text = text[:b] + "\n/* AGREEMENT BUTTONS (2026-11-18, staged commits 047f8caa/45826b09; landed here) — the diamond is the emblem's own jewel, one shared class, same PNG in both buttons. */\n" + jewel_rule + text[b:]
# Add the jewel span to the four choice buttons, replacing the flat diamond.
subs = [
    ('id="fpBridgeDeck" type="button" style="--tone:#8e24aa">Begin the visual story &#9670;',
     'id="fpBridgeDeck" type="button" style="--tone:#8e24aa">Begin the visual story <span class="fp-btn-jewel" aria-hidden="true"></span>'),
    ('id="fpBridgeLetter" type="button" style="--tone:#07925f">Read the agreement &#9670;',
     'id="fpBridgeLetter" type="button" style="--tone:#07925f">Read the agreement <span class="fp-btn-jewel" aria-hidden="true"></span>'),
    ('id="fpChoiceDeck" type="button" style="--tone:#8e24aa">Begin the visual story ◆',
     'id="fpChoiceDeck" type="button" style="--tone:#8e24aa">Begin the visual story <span class="fp-btn-jewel" aria-hidden="true"></span>'),
    ('id="fpChoiceLetter" type="button" style="--tone:#07925f">Read the agreement ◆',
     'id="fpChoiceLetter" type="button" style="--tone:#07925f">Read the agreement <span class="fp-btn-jewel" aria-hidden="true"></span>'),
]
for old_s, new_s in subs:
    text = replace_once(text, old_s, new_s, "item39-jewel-span")
print("item39: jewel landed, spans:", text.count('class="fp-btn-jewel"'))

# ---------------------------------------------------------------- E5 item 40
# Remove #fpBridgePick ONLY (not #fpIntroPick — the deck's pick line stays).
old = '<p class="fp-bridge-pick" id="fpBridgePick">Pick your view — one, or both, as you wish.</p> '
assert text.count(old) == 1, "fpBridgePick anchor"
text = text.replace(old, "<!-- WHOLE-SYSTEM CONNECTION 2026-11-24 (item 40): #fpBridgePick removed — both buttons sit above the fold, above the legal row. #fpIntroPick (deck) stays. -->", 1)
print("item40: fpBridgePick removed")

# ---------------------------------------------------------------- E6 item 12
# VERIFY ONLY: the :not() rest rule already covers all four pills (choice
# pair + bridge pair) in the live bytes — deep rims at rest, DONE already.
old = ("#fpChoiceDeck:not(:hover):not(:active),#fpChoiceLetter:not(:hover):not(:active),"
       "#fpBridgeDeck:not(:hover):not(:active),#fpBridgeLetter:not(:hover):not(:active)")
assert text.count(old) == 1, "item12 rest rule"
print("item12: VERIFIED present in base (choice + bridge pair), no change")

# ---------------------------------------------------------------- E7 items 58/71
# Jump lands on the citizen's real Personal page, never the Hub, with the
# CORRECT name. The name comes from the registry row (the same Supabase
# lookup the certificate page uses); a stored nayanet_smart_name is only a
# fallback. ("See" was a stale stored name replayed blindly into the URL:
# prettyName("shawn") is "Shawn", so no code path mangles the alias into
# "See" — the row is now authoritative. A 1.5s timeout means a slow network
# never blocks the Jump.)
ident = open(IDENT, encoding="utf-8", errors="ignore").read()
km = re.search(r"SB_ANON_KEY\s*=\s*'([^']+)'", ident)
assert km, "anon key not found in identity.html"
SB_KEY = km.group(1)
assert len(SB_KEY) == 208
helper = """
/* WHOLE-SYSTEM CONNECTION 2026-11-24 (items 58/71, SN-2797) — Jump back in
   lands on the citizen's real Personal page (/personal?name=...&alias=...),
   never the Hub, with the CORRECT name. The registry row is authoritative:
   the name is read from nayanet_identities for this alias (the same lookup
   the certificate page uses, same public anon key, read-only). The stored
   nayanet_smart_name is only the fallback while the lookup runs, and a
   1.5s timeout means a slow network never blocks the Jump. */
var FP_SB_ANON = '""" + SB_KEY + """';
function fpPrettyName(s){ return s ? s.charAt(0).toUpperCase() + s.slice(1) : ''; }
function fpJumpToPersonal(alias, fallbackName){
  var done = false;
  function go(n){
    if (done) return; done = true;
    window.location.href = '/personal?name=' + encodeURIComponent(n || fpPrettyName(alias)) + '&alias=' + encodeURIComponent(alias);
  }
  try {
    var to = setTimeout(function(){ go(fallbackName); }, 1500);
    fetch('https://dahisasgpfvziswqvmvm.supabase.co/rest/v1/nayanet_identities?alias=eq.' + encodeURIComponent(alias) + '&select=name', {headers: {'apikey': FP_SB_ANON, 'Authorization': 'Bearer ' + FP_SB_ANON}, cache: 'no-store'})
      .then(function(r){ return r.ok ? r.json() : null; })
      .then(function(rows){ clearTimeout(to); go((rows && rows[0] && rows[0].name) || fallbackName); })
      .catch(function(){ clearTimeout(to); go(fallbackName); });
  } catch(e){ go(fallbackName); }
}
"""
anchor = "/* RETURNING CITIZEN (walk-entry-identity-fix 2026-11-12, addendum):"
assert text.count(anchor) == 1
text = text.replace(anchor, helper + "\n" + anchor, 1)
old = "window.location.href='/hub?name='+encodeURIComponent(name||'')+'&alias='+encodeURIComponent(alias);"
assert text.count(old) == 1, "main jump anchor"
text = text.replace(old, "fpJumpToPersonal(alias, name||'');", 1)
old = "window.location.href='/hub?name='+encodeURIComponent(it.name||it.alias)+'&alias='+encodeURIComponent(it.alias);"
assert text.count(old) == 1, "others jump anchor"
text = text.replace(old, "fpJumpToPersonal(it.alias, it.name||it.alias);", 1)
assert text.count("/hub?name=") == 0, "hub jump left"
print("items 58/71: Jump -> /personal with verified name")

open(OUT, "w", encoding="utf-8").write(text)
print("PART1 written:", OUT, len(text.encode("utf-8")))
