#!/usr/bin/env python3
"""Agreement MERGE EYE FOLLOW-ON — FIX PASS (2026-11-18).
Checker NOT PASS on exactly one failure (F3) + one noted deviation (F2).

F3 — the two named "I agree" end buttons (#letterPageAgree, #dealAgreeBtn,
class "p3-enter deal-agree-btn") still carry the BRIGHT emerald rim/glow
from the rule `#fpAgreement .deal-agree-btn, #fpLegal .deal-agree-btn` at
welcome offset 568141 (border #2fe89e, glow rgba(47,232,158,...)). Neither
button has any --tone set and the EYEFOLLOW block mentions deal-agree-btn
0 times; the prior claim "'I agree' x3 -> #07925f" is FALSE in bytes.
Fix: ONE button-scoped rule, same selector, later in the cascade (inside
the EYEFOLLOW block at the end of the last <style>), so it wins at equal
specificity (1,1,0): border 1.5px solid #07925f, glow rgba(7,146,95,...),
mirroring the bright rule's box-shadow structure exactly. Rest state only:
while held, the higher-specificity :active rule
(#fpAgreement .p3-enter:active, (1,2,0)) still collapses the glow.

F2 deviation — `.new-account` depresses (scale .97, pre-existing rule) +
dims (brightness .75, EYEFOLLOW) but its hover glow
(0 0 28px rgba(255,255,255,.45)) is NOT collapsed while held — the glow
grows on press, contrary to the brief's "shadow collapse" letter. Fix:
add the shadow/glow collapse to the EYEFOLLOW `.new-account:active` rule
(small contact shadow, same pattern as the sibling :active rules).

Nothing else is touched. Base: welcome-staged.html sha c8f0df54 (filed
commit f5c94741, PR #3453). Writes the fixed bytes back to
welcome-staged.html and a copy to work/welcome-fixpass.html.
Usage: python3 edit-fixpass.py (prints new size + sha256).
"""
import hashlib
import os

WELCOME = "/home/hatch/workspace/team-nitro/walk-v23-assembly-20261114/welcome-staged.html"
OUT_COPY = "/home/hatch/workspace/team-nitro/agreement-merge-eye-followon-20261117/work/welcome-fixpass.html"
BASE_SHA = "c8f0df54dabda441418304962f4c1cd9a01f07efe80a8fd94dee8e8245e3af1d"

# --- F3 anchor: the last --tone override line in the EYEFOLLOW block ---
F3_ANCHOR = '#fpLegal #legal-disclaimer .deck-next{--tone:#07925f}'
F3_INSERT = (
    '\n/* FIX-PASS (2026-11-18, checker F3 NOT PASS): the two "I agree" end\n'
    '   buttons (#letterPageAgree, #dealAgreeBtn, class p3-enter\n'
    '   deal-agree-btn) still carried the BRIGHT emerald rim/glow from the\n'
    '   rule at offset 568141 (border #2fe89e, glow rgba(47,232,158,...));\n'
    '   no --tone ever touched them and the EYEFOLLOW block mentioned\n'
    '   deal-agree-btn 0 times. This rule is the SAME selector, later in\n'
    '   the cascade, so it wins at equal specificity: border and glow go\n'
    '   DEEP emerald #07925f (Laws SS3.1, one deep hex per hue). Rest state\n'
    '   only - while held, the higher-specificity :active rule\n'
    '   (#fpAgreement .p3-enter:active) still collapses the glow. */\n'
    '#fpAgreement .deal-agree-btn, #fpLegal .deal-agree-btn{border:1.5px solid #07925f;box-shadow:0 0 34px rgba(7,146,95,.55),0 0 60px rgba(7,146,95,.25),inset 0 1.5px 0 rgba(255,255,255,.35),inset 0 -4px 10px rgba(0,0,0,.85)}'
)

# --- F2 anchor: the EYEFOLLOW .new-account press rule (NOT the earlier
# pre-existing `.new-account:active{transform:scale(.97)}` rule) ---
F2_OLD = '.new-account:active{filter:brightness(.75)}'
F2_NEW = (
    '/* FIX-PASS (2026-11-18, checker F2 deviation): .new-account\'s hover\n'
    '   glow (0 0 28px rgba(255,255,255,.45)) was NOT collapsed while held.\n'
    '   It now collapses to the small contact shadow like every other\n'
    '   button; the earlier scale(.97) rule still depresses it. */\n'
    '.new-account:active{filter:brightness(.75);box-shadow:0 2px 6px rgba(0,0,0,.6),0 0 6px rgba(255,255,255,.12);transition:transform .07s ease,filter .07s ease,box-shadow .07s ease}'
)


def write_resilient(path, data):
    """8KB-chunk writer with per-chunk retry (EPERM-flake workaround,
    per the maker report)."""
    import time
    for attempt in range(5):
        try:
            with open(path, "wb") as f:
                for i in range(0, len(data), 8192):
                    f.write(data[i:i + 8192])
            return
        except OSError as e:
            print("write attempt %d failed (%s), retrying" % (attempt + 1, e))
            time.sleep(2)
    raise OSError("write failed after retries: %s" % path)


def main():
    raw = open(WELCOME, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    print("base welcome %d B sha %s" % (len(raw), sha))
    assert sha == BASE_SHA, "base moved: %s" % sha
    s = raw.decode("utf-8")

    # F3: exactly one anchor, inside the EYEFOLLOW block (after offset 676114)
    assert s.count(F3_ANCHOR) == 1, "F3 anchor count %d" % s.count(F3_ANCHOR)
    assert s.find(F3_ANCHOR) > 676114, "F3 anchor not in EYEFOLLOW block"
    s = s.replace(F3_ANCHOR, F3_ANCHOR + F3_INSERT, 1)

    # F2: exactly one EYEFOLLOW .new-account:active rule
    assert s.count(F2_OLD) == 1, "F2 old-rule count %d" % s.count(F2_OLD)
    assert s.find(F2_OLD) > 676114, "F2 rule not in EYEFOLLOW block"
    s = s.replace(F2_OLD, F2_NEW, 1)

    # Sanity: the bright deal-agree rule is untouched (only overridden later)
    assert s.count('border:1.5px solid #2fe89e') == 1, "bright rule moved"
    assert s.count('#fpAgreement .deal-agree-btn, #fpLegal .deal-agree-btn{border:1.5px solid #07925f') == 1
    assert s.count('deal-agree-btn') == 12, "deal-agree-btn count moved: %d" % s.count('deal-agree-btn')  # base 8 + 2 (new rule selector) + 2 (fix comment)
    # F2: the earlier scale(.97) rule still exists; hover glow rule untouched
    assert s.count('.new-account:active{transform:scale(.97);}') == 1
    assert s.count('box-shadow:0 0 28px rgba(255,255,255,.45)') == 1

    out = s.encode("utf-8")
    print("new welcome %d B sha %s" % (len(out), hashlib.sha256(out).hexdigest()))
    write_resilient(WELCOME, out)
    write_resilient(OUT_COPY, out)
    print("wrote %s and %s" % (WELCOME, OUT_COPY))


if __name__ == "__main__":
    main()
