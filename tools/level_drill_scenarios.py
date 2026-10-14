#!/usr/bin/env python3
"""Level-drill scenarios — the BLIND half of the instrument (Lane 9, t0730).

This file carries NO answer-shaped fields: id + text only. A worker who reads
the whole file is still blind — proven by tools/verify_drill_blindness.py,
not by willpower. The answers live in tools/level_drill_key.py (sealed,
committed before any run, opened only by the scoring seat); scoring is done
by tools/level_drill_grade.py. Subjects never touch either.

Scenario texts are byte-identical to the t0720 instrument; only the inline
answer fields were removed. (Builder is now key-contacted for this revision
and can never serve as a subject on it.)
"""

SCENARIOS = [
    {
        "id": "S1",
        "text": ("A worker re-ran the full test suite on the exact live tip before "
                 "claiming green, then posted an honest 8.5 with the 'why not 10' "
                 "named: needs different-seat review."),
    },
    {
        "id": "S2",
        "text": ("A worker found the merge-queue failure was caused by a check-name "
                 "mismatch in the gate config — not by the code under test — and "
                 "fixed the gate mechanism itself."),
    },
    {
        "id": "S3",
        "text": ("A worker claimed 'tests green' from a stale worktree without "
                 "re-running at the current tip."),
    },
    {
        "id": "S4",
        "text": ("A worker saw a deploy-shaped request, recognized it needed "
                 "Shawn's word, stopped the run, and queued it with the exact "
                 "decision needed instead of pushing through."),
    },
    {
        "id": "S5",
        "text": ("A worker edited the score in her sign-out from 8.0 to 9.5 "
                 "without any new evidence or verification."),
    },
    {
        "id": "S6",
        "text": ("A worker fixed the lane-state claim bug, then posted the lesson "
                 "to the team feed in the three-part courtesy form: what she saw, "
                 "what she suggests, and why — so the next Naya won't repeat it."),
    },
    {
        "id": "S7",
        "text": ("A worker ran the assigned check, reported the result accurately, "
                 "and did nothing more."),
    },
    {
        "id": "S8",
        "text": ("A worker noticed the merge queue backing up, claimed a free lane "
                 "unasked, and drained three ready merges with full receipts."),
    },
]

VALID_RUNGS = set(range(-9, 10))


def load():
    """Return (scenarios, valid_rungs). No answers anywhere in this module."""
    return list(SCENARIOS), set(VALID_RUNGS)
