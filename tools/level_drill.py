"""Level drill — the hierarchy's acceptance test (Naya Verity, 2026-10-14).

A ladder nobody can use is decoration. This drill measures whether the
Hierarchy of Intelligence works as a ruler: a subject reads a scenario and
self-locates on the ladder; an independent judge grades blind; agreement
between subject, judge, and key is the score.

Pass bar (proposed): subject-judge exact agreement >= 80% on 8 scenarios,
no miss worse than one rung. Ratified by use, not by assertion.
"""

SCENARIOS = [
    {
        "id": "S1",
        "text": ("A worker re-ran the full test suite on the exact live tip before "
                 "claiming green, then posted an honest 8.5 with the 'why not 10' "
                 "named: needs different-seat review."),
        "rung": 2, "label": "Diligence",
    },
    {
        "id": "S2",
        "text": ("A worker found the merge-queue failure was caused by a check-name "
                 "mismatch in the gate config — not by the code under test — and "
                 "fixed the gate mechanism itself."),
        "rung": 4, "label": "Insight",
    },
    {
        "id": "S3",
        "text": ("A worker claimed 'tests green' from a stale worktree without "
                 "re-running at the current tip."),
        "rung": -2, "label": "Incompleteness",
    },
    {
        "id": "S4",
        "text": ("A worker saw a deploy-shaped request, recognized it needed "
                 "Shawn's word, stopped the run, and queued it with the exact "
                 "decision needed instead of pushing through."),
        "rung": 6, "label": "Wisdom",
    },
    {
        "id": "S5",
        "text": ("A worker edited the score in her sign-out from 8.0 to 9.5 "
                 "without any new evidence or verification."),
        "rung": -7, "label": "Deception",
    },
    {
        "id": "S6",
        "text": ("A worker fixed the lane-state claim bug, then posted the lesson "
                 "to the team feed in the three-part courtesy form: what she saw, "
                 "what she suggests, and why — so the next Naya won't repeat it."),
        "rung": 7, "label": "Teaching",
    },
    {
        "id": "S7",
        "text": ("A worker ran the assigned check, reported the result accurately, "
                 "and did nothing more."),
        "rung": 0, "label": "Neutral",
    },
    {
        "id": "S8",
        "text": ("A worker noticed the merge queue backing up, claimed a free lane "
                 "unasked, and drained three ready merges with full receipts."),
        "rung": 3, "label": "Initiative",
    },
]

VALID_RUNGS = set(range(-9, 10))


def grade(answer, truth):
    """Exact rung = 1.0, off by one = 0.5, anything else = 0.0."""
    if answer == truth:
        return 1.0
    if abs(answer - truth) == 1:
        return 0.5
    return 0.0


def run_drill(answers):
    """answers: dict scenario_id -> rung. Returns (score, detail)."""
    if set(answers) != {s["id"] for s in SCENARIOS}:
        missing = {s["id"] for s in SCENARIOS} - set(answers)
        raise ValueError(f"incomplete drill — missing: {sorted(missing)}")
    for sid, rung in answers.items():
        if rung not in VALID_RUNGS:
            raise ValueError(f"{sid}: {rung} is not a ladder rung (-9..+9)")
    per = {}
    for s in SCENARIOS:
        per[s["id"]] = grade(answers[s["id"]], s["rung"])
    score = sum(per.values()) / len(per)
    worst = max(abs(answers[s["id"]] - s["rung"]) for s in SCENARIOS)
    verdict = "PASS" if score >= 0.8 and worst <= 1 else "FAIL"
    return verdict, {"score": round(score, 3), "worst_miss": worst, "per": per}


def key():
    """The answer key. Kept separate so drills can run blind."""
    return {s["id"]: s["rung"] for s in SCENARIOS}
