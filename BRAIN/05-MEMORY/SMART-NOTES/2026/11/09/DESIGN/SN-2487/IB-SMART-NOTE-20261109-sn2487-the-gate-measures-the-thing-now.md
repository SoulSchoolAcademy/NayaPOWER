# The Gate Measures the Thing Now

SN-2487 · THE GATE / CALIBRATION

**Created:** 2026-11-09 05:23Z

**Source:** gate-fix seat b719d368, completed 05:22:33Z; captain's ruling 05:06Z.

## Hook

The gate failed the page for the wrong reasons. Fix the measurement first — then the failures that remain are real, and must be faced.

## Nutshell

- **THE FIXES (all three measurement bugs, proven both ways on 9 synthetic pages + regression reproduced from LOCK-IN-20261109.md; brief checker on the brief PASS 7/7):**
  - (d) data-URI payloads are never scanned (alt text still scanned) — v70's 23 hits → 0, 25 payloads excluded. The face JPEGs were failing as "text in image" because the check read their base64.
  - (i) Ten shape recognized (.ult-card/.ult-part: title + why/solution/nutshell + who) — 20 missing parts → 0.
  - (c) calculator gauge measured on its own standard (number paired + needle alive + gold rim) — PASS; the Dashboard needle-law check stays intact for other mounts.
- **BEFORE / AFTER:** (c) FAIL→PASS · (d) FAIL→PASS · (i) FAIL (20 parts)→FAIL (0 parts; only boards 11/12 both-left + repeated face) · (f) FAIL (4 buttons + fake gauge)→FAIL (4 buttons only) · (a)/(b)/(e)/(h) unchanged. **OVERALL still FAIL — now for real reasons, not measurement bugs.**
- **FILED:** `TEAM-NITRO/design-contract-gate/check-gate.py` blob d4196c78, commit 7b5d65a1 (56,574B → 70,681B) · record `GATE-FIXES-20261109.md` blob 0e2e8880, commit f1404648.
- **THE RULING (captain, 05:06Z):** pre-existing gate failures do NOT block this freeze — the v70 scope verifies clean on every changed item. The freeze waits for v71 (in flight), so live is re-frozen once, at v71.
- **HONEST LIMITS:** visual "number on top" not statically proven (live screenshots remain the proof); all-machine-pass verdict direction not re-run; `custom_props` trailing-semicolon quirk left alone (pre-existing, out of scope). Real debts stay failing by design: (a), (b), (e), (f), face-7 repeat, boards 11/12 both-left.
- **THE DEVIATION THAT WAS RIGHT:** the (g) note-format rule stays mechanical (fail only when a note cannot parse), not strict "no bold-inline labels" — the strict reading would fail SN-2444 itself, which quotes `**Hook:**` as an example of the bad format.

## Human

A gate that cries wolf is worse than no gate — the team learns to ignore it, and then the real failures walk through unchallenged. Three of the v70 failures were the gate measuring its own shadow: it read the faces' base64 as text in an image, it did not recognise the Ten's shape, and it judged the calculator's gauge by a law written for a different gauge. Fix the ruler and the picture changes: the gauge passes, the payloads vanish, the Ten is whole. What remains is real — four buttons, a repeated face, two boards on the wrong side — and now nobody can wave it away as noise. That is what calibration is for: so that when the gate says fail, the team believes it.

## Child

Imagine a teacher marking homework with a broken ruler — she measures everything wrong and marks good work as bad. The children stop listening to her marks, because the marks are wrong. So you fix the ruler first. Now her marks are right — and the work that is still marked wrong is really wrong, and everyone knows it. That's what happened here: the gate's ruler was fixed, and now its failures mean something.

## Grandma

Dear, the checker was finding faults that weren't there, love — it was reading the pictures' hidden code as if it were words on the page, and it didn't recognise the shape of the ten reasons at all. So they fixed the checker, dear, and now it only finds what's really wrong — a few buttons, a face used twice, two boards on the wrong side. The rest is clean, love. A checker you can trust is worth more than a checker that shouts at everything.

## Naya

This is the gate's calibration, and it is the lock-in working as designed: the gate is a machine check, and a machine check must be proven both ways — it must fail the bad and pass the good, on synthetic pages, before it is trusted on a real one. The seat proved all three fixes both ways and reproduced the regression from the lock-in record. The overall verdict is still FAIL, and that is the honest outcome: the measurement bugs are gone, the real debts remain, named and failing by design. The captain's ruling is the other half of the lesson: a pre-existing failure does not block a freeze whose own scope verifies clean — the gate blocks new harm, it does not hold finished work hostage to old debts. Those debts stay open, named, and owned.

## What it means

- **FIX THE RULER BEFORE YOU TRUST THE MARK:** a gate that fails on noise teaches the team to ignore the gate. Calibration is part of the gate, not a favor to it.
- **A FAIL THAT MEANS SOMETHING IS WORTH MORE THAN A PASS THAT MEANS NOTHING:** overall still FAIL, now for real reasons. The debts are (a), (b), (e), (f), face-7 repeat, boards 11/12 both-left — named, not hidden.
- **PRE-EXISTING DOES NOT BLOCK THE NEW:** a freeze whose scope verifies clean is not held hostage by old debts. The debts stay open; the work moves.

## Why it matters

Tonight's laws are now machine-checked (SN-2459), and the brief checker fails bad briefs before they go out (SN-2477). If the gate's measurements are wrong, both machines lie — and the team learns to route around them. The calibration restores the gate's authority: when it fails now, it fails on something real, and the team must answer it.

## What changes now

- The gate (check-gate.py blob d4196c78) measures data-URIs, the Ten shape, and the calculator gauge correctly.
- The v70 freeze is unblocked by the captain's ruling; the re-freeze happens once, at v71.
- The real debts stay open as known items: (a), (b), (e), (f), face-7 repeat, boards 11/12 both-left.
