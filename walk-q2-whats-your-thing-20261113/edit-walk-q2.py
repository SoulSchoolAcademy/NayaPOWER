#!/usr/bin/env python3
"""Walk Q2 reword — edit the staged v22 served bytes in place, Q2 only.

Base: /tmp/walk-v22.html — harvested fresh from the staging host
(3,363,931 B, sha256 227a667e4eb8e7f38fc8859495fa934b1a3b865323767816f94009b1d0df88c3).
NEVER the local walk-beginning-fixed.html (names-page round's working copy).

Every replacement is an exact-string replace with a count assertion.
The key data-key="into", KEYS, and the S2 Box mapping are never touched.
The eye entries live in CHOICE_EYES["into"] — the brief mislabels the
variable as BOARD_INFO (BOARD_INFO only holds personal/business/space);
the strings the brief quotes match CHOICE_EYES verbatim, and that is
what this script edits. The Full Custom eye (data-eye="2-custom") shows
CUSTOM_WAYS, shared across all ten questions; its third way points at
"the examples above" — the new examples — so it needs no text change.
"""
import hashlib
import sys

SRC = "/tmp/walk-v22.html"
OUT = "/home/hatch/workspace/team-nitro/walk-q2-whats-your-thing-20261113/walk-beginning-fixed.html"

s = open(SRC, encoding="utf-8").read()
assert hashlib.sha256(s.encode()).hexdigest() == \
    "227a667e4eb8e7f38fc8859495fa934b1a3b865323767816f94009b1d0df88c3", "base sha moved — STOP"
assert len(s.encode()) == 3363931, "base size moved — STOP"

# --- the new words (harvest traced in the record) ---
NEW_HEADING = '"What\'s your thing? What do you love? What do you love to do?"'
NEW_A = ("My thing is music \u2014 the songs I love and the artists I play "
         "over and over. Because nobody should feel alone in the thing they "
         "love, and my music is how my people find me.")
NEW_B = ("My thing is making money \u2014 I make a page about Naya and send "
         "people to it, and I get 50% of the revenue, paid when we're paid. "
         "Anybody can.")
NEW_C = ("My thing is the connection itself \u2014 the moment two like minds "
         "find each other across the world and realize they were never "
         "alone. Sometimes your thing is what you love, sometimes it's your "
         "job \u2014 either way, that moment becomes our place: a smart hub, "
         "a digital world where everybody meets on the one thing we love.")

# CHOICE_EYES uses plain " quotes and a literal single-backslash \u2014
# escape in the file bytes (verified by codepoint: 0x5c + u2014).
NEW_EYES = (
    '"into":[["Naya\'s warm & plain voice \\u2014 my thing is music.",'
    '"Music is the thing \\u2014 the songs and the artists I love.",'
    '"It fills your Personal page and your Space \\u2014 the people you want around you.",'
    '"The right people recognize themselves in it."],'
    '["Naya\'s bold & short voice \\u2014 making money, with a page about Naya.",'
    '"One line that says the whole thing: the thing is making money, the page is about Naya.",'
    '"It fills your Personal page and your Space \\u2014 the people you want around you.",'
    '"People feel the promise at once."],'
    '["Naya\'s full & visionary voice \\u2014 the moment becomes a place.",'
    '"It paints the moment everything is for \\u2014 and the place it becomes: a smart hub, a digital world.",'
    '"It fills your Personal page and your Space \\u2014 the people you want around you.",'
    '"People can feel themselves in that moment."]]'
)

OLD_EYES = (
    '"into":[["Naya\'s warm & plain voice \\u2014 finding each other, and why.",'
    '"Nobody should feel alone in the thing they love.",'
    '"It fills your Personal page and your Space \\u2014 the people you want around you.",'
    '"The right people recognize themselves in it."],'
    '["Naya\'s bold & short voice \\u2014 connecting like minds.",'
    '"One line that says the whole thing.",'
    '"It fills your Personal page and your Space \\u2014 the people you want around you.",'
    '"People feel the promise at once."],'
    '["Naya\'s full & visionary voice \\u2014 the moment two like minds meet.",'
    '"It paints the moment everything is for.",'
    '"It fills your Personal page and your Space \\u2014 the people you want around you.",'
    '"People can feel themselves in that moment."]]'
)


def rep(old, new, expect=1):
    global s
    n = s.count(old)
    assert n == expect, "expected %d of %r, found %d" % (expect, old[:70], n)
    s = s.replace(old, new)


# 1. Heading, line 346
rep('<h1 class="p3-question">"What are you into, and why?"</h1>',
    '<h1 class="p3-question">%s</h1>' % NEW_HEADING)

# 2. The three example textareas (lines 349-351) — replace by textarea id anchor
rep("id=\"choice-2-A\" rows=\"2\" readonly>I'm into people finding each other \u2014 the person who loves what you love, doing what you do, anywhere in the world. Because nobody should feel alone in the thing they love.</textarea>",
    "id=\"choice-2-A\" rows=\"2\" readonly>" + NEW_A + "</textarea>")
rep("id=\"choice-2-B\" rows=\"2\" readonly>Connecting like minds. Because the right person changes everything.</textarea>",
    "id=\"choice-2-B\" rows=\"2\" readonly>" + NEW_B + "</textarea>")
rep("id=\"choice-2-C\" rows=\"2\" readonly>I'm into the connection itself \u2014 the moment two like minds find each other across the world and realize they were never alone. That's what I'm into, and why: everything else is just the road to that moment.</textarea>",
    "id=\"choice-2-C\" rows=\"2\" readonly>" + NEW_C + "</textarea>")

# 3. Hints, lines 365-366 — tip text AND aria-label (each appears twice: label + tip).
# File bytes carry a plain apostrophe (0x27, no backslash — verified by codepoint).
rep("Click the button and tell us what you're into", "Click the button and tell us what your thing is", expect=2)
rep("Type in what you're into, and why", "Type in what your thing is, and what you love to do", expect=2)

# 4. Eye entries (CHOICE_EYES "into")
rep(OLD_EYES, NEW_EYES)

# --- verification: what must be true of the result ---
assert s.count("What are you into") == 0, "old question still present"
assert s.count("what you're into") == 0, "old hint phrasing still present"
assert 'data-key="into"' in s, "key lost!"
assert "KEYS = ['about', 'into', 'vision', 'mission', 'motto', 'goal', 'biz_do', 'biz_offer', 'biz_building', 'space']" in s, "KEYS changed!"
assert s.count("answers.into") == 2, "S2 mapping changed!"
assert s.count(NEW_HEADING) == 1
assert s.count(NEW_A) == 1 and s.count(NEW_B) == 1 and s.count(NEW_C) == 1
assert s.count("Click the button and tell us what your thing is") == 2
assert s.count("Type in what your thing is, and what you love to do") == 2
# out-of-scope strings that must stay exactly as they were
assert s.count("what you are into") == 1, "BOARD_INFO personal line touched!"
assert s.count("Copy-paste from your AI into the box") == 20, "paste hint touched!"  # 10 steps x label + tip
assert s.count("2 of 10") == 1
# the other nine question headings, word for word
for h in ['"Tell me who you are, in your own words"',
          '"What is your vision?"', '"What is your mission?"',
          '"What is your motto?"', '"Your goal — for your life"',
          '"What do you do?"', '"What do you offer?"',
          '"What are you building, and what\'s the goal?"',
          '"What kind of space do you want around it, and who do you want to meet there?"']:
    assert s.count(h) == 1, "other question changed or missing: %s" % h

# diff scope: only Q2 lines may differ (346 heading, 349-351 examples,
# 365-366 hints, 1280 CHOICE_EYES "into")
old_lines = open(SRC, encoding="utf-8").read().split("\n")
new_lines = s.split("\n")
assert len(old_lines) == len(new_lines), "line count changed!"
changed = [i + 1 for i, (a, b) in enumerate(zip(old_lines, new_lines)) if a != b]
print("changed lines:", changed)
assert changed == [346, 349, 350, 351, 365, 366, 1280], "change outside Q2 + eyes: %s" % changed

open(OUT, "w", encoding="utf-8").write(s)
raw = s.encode()
print("wrote %s bytes=%d sha256=%s" % (OUT, len(raw), hashlib.sha256(raw).hexdigest()))
print("grep 'What are you into':", s.count("What are you into"))
print("grep \"what you're into\":", s.count("what you're into"))
print("OK — Q2 reword applied, Q2 only")
