#!/usr/bin/env python3
"""Agreement MERGE EYE FOLLOW-ON edits, part 2 (2026-11-17).
Operates on the part-1 outputs (root sha bced9fca8, agreement sha 1764dbda).
Three small completions found by verification:
 (a) the legal pages' Keep reading buttons (class p3-enter letter-next
     deck-next, text 'Keep reading') take their rim from the legal PAGE's
     inline --tone - the purple/green pages (terms, cookies, accessibility,
     disclaimer) still showed bright rims. Button-scoped deep overrides,
     same treatment as the letter/deck Keep reading buttons in part 1.
 (b) the deck-end 'Enter NayaNET' literal '#40d3bb' - deepTone() already
     maps it at runtime, but the literal in the bytes should read deep too.
 (c) /agreement .play-btn has no base transition, so its press/release
     would snap instantly; give it an .18s spring so the release reads.
"""
import hashlib

WORK = "/home/hatch/workspace/team-nitro/agreement-merge-eye-followon-20261117/work/"
ROOT = WORK + "welcome-followon.html"
AGMT = WORK + "agreement-followon.html"

def rep(h, old, new, expect=1, label=""):
    n = h.count(old)
    assert n == expect, "%s: anchor count %d != %d :: %r" % (label, n, expect, old[:100])
    return h.replace(old, new)

def write_resilient(path, data, chunk=8192):
    import os, time
    if os.path.exists(path):
        os.remove(path)
    with open(path, "wb") as g:
        off = 0
        while off < len(data):
            piece = data[off:off + chunk]
            done = False
            for attempt in range(40):
                try:
                    g.write(piece); g.flush(); done = True; break
                except PermissionError:
                    time.sleep(5)
            if not done:
                raise IOError("could not write chunk at offset %d after retries" % off)
            off += len(piece)
    print("wrote %s %d B" % (path, len(data)))

h = open(ROOT, encoding="utf-8").read()
assert hashlib.sha256(h.encode()).hexdigest().startswith("bced9fca8"), "root part-1 output moved"

# (a) legal Keep reading rims go deep on the button only (pages keep tones).
h = rep(h, '#deckBody article[data-beat="3"] .deck-next{--tone:#07925f}',
        '#deckBody article[data-beat="3"] .deck-next{--tone:#07925f}\n'
        '#fpLegal #legal-terms .deck-next{--tone:#8e24aa}\n'
        '#fpLegal #legal-cookies .deck-next{--tone:#07925f}\n'
        '#fpLegal #legal-accessibility .deck-next{--tone:#8e24aa}\n'
        '#fpLegal #legal-disclaimer .deck-next{--tone:#07925f}',
        1, "legal keep-reading deep")

# (b) deck-end 'Enter NayaNET' literal goes deep in the bytes as well.
h = rep(h, "','#40d3bb','deckJoin')", "','#0e7490','deckJoin')", 1, "deckJoin literal")

write_resilient(ROOT, h.encode())
print("root written: %d B sha %s" % (len(h.encode()), hashlib.sha256(h.encode()).hexdigest()[:12]))

a = open(AGMT, encoding="utf-8").read()
assert hashlib.sha256(a.encode()).hexdigest().startswith("1764dbda"), "agreement part-1 output moved"

# (c) play-btn spring: an .18s ease-out return so the release reads.
a = rep(a, ".play-btn:active{transform:scale(.94);",
        ".play-btn{transition:transform .18s ease-out,filter .18s ease-out,box-shadow .18s ease-out}\n.play-btn:active{transform:scale(.94);",
        1, "play-btn transition")

write_resilient(AGMT, a.encode())
print("agreement written: %d B sha %s" % (len(a.encode()), hashlib.sha256(a.encode()).hexdigest()[:12]))
print("ALL PART-2 EDITS APPLIED")
