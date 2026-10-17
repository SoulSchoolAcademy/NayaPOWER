#!/usr/bin/env python3
"""SEALED answer key for the level drill (Lane 9, t0730).

AUTHORIZED READERS: the scoring seat ONLY (currently Naya Verity's lane).
Subjects never open this file — their authorized path is
tools/level_drill_scenarios.py, which carries no answers (machine-proven by
tools/verify_drill_blindness.py).

sealed_at: 2026-10-14 (PDT) — committed before any blind run on this
instrument. tools/verify_drill_blindness.py --answers enforces the ordering:
key mtime < answers mtime, or scoring refuses.

Format: scenario id -> (rung, label). Kept as one literal so the file has no
logic to get wrong; tools/level_drill_grade.py does the math.
"""

KEY = {
    "S1": (2, "Diligence"),
    "S2": (4, "Insight"),
    "S3": (-2, "Incompleteness"),
    "S4": (6, "Wisdom"),
    "S5": (-7, "Deception"),
    "S6": (7, "Teaching"),
    "S7": (0, "Neutral"),
    "S8": (3, "Initiative"),
}
