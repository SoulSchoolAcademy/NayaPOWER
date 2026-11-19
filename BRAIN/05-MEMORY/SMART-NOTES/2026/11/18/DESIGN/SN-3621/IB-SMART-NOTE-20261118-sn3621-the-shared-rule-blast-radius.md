# SN-3621 — The Shared-Rule Blast Radius

**Filed:** Intelligence Loop run 342, 2026-11-18 — numbering confirmed by `next-sn-number.py` (exit 0) immediately before filing: next free SN-3621; filed as SN-3621 under its draft number.

**Filed by:** Intelligence Loop run 342, 2026-11-18 — Hub follow-on checker GOES BACK, coordinator report 03:12Z.

**Paired Naya Note:** NN-20261118-the-shared-rule-blast-radius

## The teaching, in his words (verbatim)

The checker's finding, in the captain's record: the kept filing edited the shared rule itself — line 2016, `.intel-type` — to remove a halo from one panel, and every non-panel label in the system gained box-shadows. The fix: restore line 2016 verbatim, halo removal via a panel-scoped override only.

## The understanding

One line, edited for one panel, changed labels everywhere — the blast radius of a shared rule is the whole system. The discipline is the lesson: never fix a local problem by editing the shared rule. Restore it verbatim first, then scope the fix to the panel that owns the problem, and prove the other labels are untouched. The checker earned the catch by diffing the shared rule, not by looking at the one panel.

## The law

Before editing any shared rule, name every place it reaches. If the fix belongs to one panel, the override lives in that panel's scope and the shared rule stays byte-identical.

## Owed from this dictation

Hub follow-on fix round 2 (coordinator 0929b5c4): line 2016 restored verbatim, halo removal panel-scoped only, proven by diff.

**A shared rule is shared — an edit to it is an edit to every page that uses it.**
