#!/usr/bin/env python3
"""In-memory dict-key check + context dump for the repair round.
Reads staged page bytes from stdin. Prints: for each candidate key whether
it exists in MW_I18N (es/fr/de values), how the guarded slGraphHTML does
'Busiest: ', and full context around each F-site function."""
import hashlib, json, re, sys

raw = sys.stdin.buffer.read()
assert hashlib.sha256(raw).hexdigest() == "f9f58cc77807aa01a85be6c89c8b2b7078a52fd04cd74da172add029e5de0c24"
text = raw.decode("utf-8")
m = re.search(r"var MW_I18N\s*=\s*(\{.*?\});", text, re.S)
d = json.loads(m.group(1))
stripped = text[:m.start()] + "/*DICT*/" + text[m.end():]

KEYS = [
 "Plugged into this world",
 "<b>Birth score</b> — every post, note and share moves the needle.",
 "Birth score — every post, note and share moves the needle.",
 "Quiet — the first post, note or invite lights the needle.",
 "Reading your actions…",
 "No clicks yet — share a link and the first click lands here.",
 "Busiest: ",
 "Busiest:",
 "Posts, messages and invites together.",
 "Posts, notes, messages and invites together.",
 "A quiet stretch — the next post, message or invite lights the first bar.",
 "A quiet stretch — the next post, message or invite lights the first circle.",
 "A quiet stretch so far — the chart is waiting.",
 "The next post, note, message or invite lights the first bar.",
 "of recorded invites joined",
 "Make a post",
 "Send a message",
 "Add a Smart Link",
 "Add to a list",
 "Add something",
 "Add",
 "Change picture",
 "Edit photo",
 "Video note",
 "Voice note",
 "Untitled note",
 "Hide breakdown",
 "Breakdown",
 "The next post, note, message or invite lights the first circle.",
 "The circles show the story week by week; the totals cover the whole story.",
]
for k in KEYS:
    if k in d["es"]:
        print(f"IN-DICT  {k!r}  es={d['es'][k]!r} fr={d['fr'][k]!r} de={d['de'][k]!r}")
    else:
        print(f"MISSING  {k!r}")

print("\n=== Busiest guarded sites (slGraphHTML) ===")
for m2 in re.finditer(r"Busiest", stripped):
    i = m2.start()
    print("--- line", stripped.count("\n", 0, i) + 1, "---")
    print(stripped[max(0, i-200):i+260].replace("\n", "\\n"))
