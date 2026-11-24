#!/usr/bin/env python3
"""v2b: pause the idle enterPulse animation while the choice play disc is
pressed, so the :active scale(.94) is deterministic (the running animation
animates transform and composites with the press transform, making the held
value non-deterministic: 0.94 one run, 0.993 mid-pulse the next)."""
import hashlib

p = 'agreement.html'
t = open(p, encoding='utf-8', errors='ignore').read()
old = ("#screen-choice .choice-play:active .pm-play-disc{transform:scale(.94);"
       "filter:brightness(.72);box-shadow:0 0 2px 0 rgba(255,255,255,.08)}")
new = ("#screen-choice .choice-play:active .pm-play-disc{animation:none;"
       "transform:scale(.94);filter:brightness(.72);"
       "box-shadow:0 0 2px 0 rgba(255,255,255,.08)}")
assert t.count(old) == 1, f"disc :active rule count {t.count(old)}"
t = t.replace(old, new)
open(p, 'w', encoding='utf-8').write(t)
print("agreement:", len(t.encode()), "B  sha256", hashlib.sha256(t.encode()).hexdigest())
print("disc :active rule now pauses animation:", t.count(new) == 1)
