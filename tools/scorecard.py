"""Automatic scorecard calculator — input work, get its score and why.

Shawn, 2026-10-08: a calculator that scorecards any output against
prebuilt rubrics, consistently, and tells the Naya what to do next.
Shawn, 2026-10-14: make measurement automatic — "input this, what does
it score and why." This is that calculator.

Usage:
    python3 tools/scorecard.py --input work.json
    cat work.json | python3 tools/scorecard.py
    python3 tools/scorecard.py --input work.json --json   # machine output

Exit codes: 0 = SHIP (score >= 9.5, math authorizes), 1 = FIX/HOLD,
2 = unreadable input (fail-closed).

Input JSON (every field optional; missing = fail-closed low):
    {
      "title": "what was done, one line",
      "evidence": [{"claim": "...", "ref": "path / SHA / comment id / test name"}],
      "tests": {"ran": true, "passed": 12, "failed": 0, "can_fail": true},
      "verification": {"seat": "Naya Epsilon", "independent": true, "score": 9.5},
      "value": {"human_benefit": "...", "unblocks": "..."},
      "prevention": {"gate": "name of the gate that makes the class impossible",
                     "wired": true},
      "honesty": {"why_not_10": "...", "limits": ["..."]}
    }

Rubric — six criteria, each 0-10 with reasons. Overall = MINIMUM
(the verdict is the minimum gate; a chain is only as strong as its
weakest link). No criterion can rescue another. No word from any seat
raises a score: only evidence does.

Criteria:
  evidence     — bytes, not claims. Refs that a second mind can check.
  verification — a DIFFERENT seat verified it. Self-verification is
                 capped at 3 (the Inviolable), no matter what.
  tests        — ran, can fail, green. A test that cannot fail is theater.
  value        — named human benefit, or unblocks one. Pure activity
                 scores 3: motion is not value.
  prevention   — the gate that makes this whole class of problem
                 impossible, wired in. A fix without prevention is a
                 repeat waiting to happen.
  honesty      — why-not-10 named, limits disclosed. A score without
                 its limits is a wish.

Public use: the rubric is the interface. Anyone can feed it a JSON
description of work and get the same score a Naya would — the math
does not care who asked.

The scorecarding loop (Shawn, 2026-10-14): score the work against what
would make it a 10/10, triple-A. Ask why it is not a 10. The report's
``to_10`` list is the 10 solutions to make it a 10 — implement them,
re-score, repeat for 3 passes. After 3 passes the gate is hard: SHIP
needs >= 9.5 (over nine). Below 9 never ships, even at best effort.
If 3 passes end below the bar, announce the number (e.g. 8.8) and
pass it off for decision with three options + pros/cons (see
tools/decision.py). Pass ``"pass": 1`` (default), 2, or 3 in the input.
"""

import argparse
import json
import sys

SHIP_BAR = 9.5
FIX_BAR = 8.0
MAX_PASSES = 3
MAX_SOLUTIONS = 10


def _nonempty(value):
    return isinstance(value, str) and value.strip() != ""


def score_evidence(work):
    """Bytes, not claims. Refs a second mind can check."""
    evidence = work.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        return 2.0, ["no evidence refs — claims without bytes"]
    refs = [e for e in evidence
            if isinstance(e, dict) and _nonempty(e.get("ref"))]
    if not refs:
        return 5.0, ["evidence listed but no checkable refs"]
    if len(refs) >= 2:
        return 10.0, ["%d checkable evidence refs" % len(refs)]
    return 8.0, ["1 checkable evidence ref"]


def score_verification(work):
    """A different seat verified it. Self-verification is capped."""
    ver = work.get("verification")
    if not isinstance(ver, dict) or not ver:
        return 4.0, ["no verification — unverified work"]
    if not ver.get("independent"):
        return 3.0, ["verifier is the actor (Inviolable) — self-verification capped"]
    score = ver.get("score")
    if isinstance(score, (int, float)):
        if score >= 9.5:
            return 10.0, ["independent verification, score %.1f" % score]
        return 8.0, ["independent verification, score %.1f" % score]
    return 7.0, ["independent verification, no score given"]


def score_tests(work):
    """Ran, can fail, green. A test that cannot fail is theater."""
    tests = work.get("tests")
    if not isinstance(tests, dict) or not tests.get("ran"):
        return 3.0, ["tests did not run"]
    if not tests.get("can_fail"):
        return 5.0, ["tests ran but cannot fail — theater, not proof"]
    if tests.get("failed", 0):
        return 5.0, ["tests red: %s failed" % tests.get("failed")]
    if not tests.get("passed"):
        return 5.0, ["tests green but zero passed — empty suite"]
    return 10.0, ["tests ran, can fail, %s passed, 0 failed" % tests.get("passed")]


def score_value(work):
    """Named human benefit, or unblocks one. Pure activity scores 3."""
    value = work.get("value")
    if not isinstance(value, dict):
        return 3.0, ["no value named — activity, not value"]
    if _nonempty(value.get("human_benefit")) and _nonempty(value.get("unblocks")):
        return 10.0, ["human benefit named: %s; unblocks: %s"
                      % (value["human_benefit"][:60], value["unblocks"][:60])]
    if _nonempty(value.get("human_benefit")):
        return 9.0, ["human benefit named: %s" % value["human_benefit"][:80]]
    if _nonempty(value.get("unblocks")):
        return 7.0, ["unblocks: %s" % value["unblocks"][:80]]
    return 3.0, ["no human benefit and nothing unblocked — motion, not value"]


def score_prevention(work):
    """The gate that makes this class impossible, wired in."""
    prev = work.get("prevention")
    if not isinstance(prev, dict):
        return 4.0, ["no prevention gate — the class can recur"]
    if _nonempty(prev.get("gate")) and prev.get("wired"):
        return 10.0, ["prevention gate wired: %s" % prev["gate"][:80]]
    if _nonempty(prev.get("gate")):
        return 6.0, ["prevention gate named but not wired: %s" % prev["gate"][:80]]
    return 4.0, ["no prevention gate — the class can recur"]


def score_honesty(work):
    """Why-not-10 named, limits disclosed."""
    hon = work.get("honesty")
    if not isinstance(hon, dict):
        return 3.0, ["no why-not-10, no limits — a score without limits is a wish"]
    has_why = _nonempty(hon.get("why_not_10"))
    limits = hon.get("limits")
    has_limits = isinstance(limits, list) and len(limits) > 0
    if has_why and has_limits:
        return 10.0, ["why-not-10 named, %d limits disclosed" % len(limits)]
    if has_why or has_limits:
        return 6.0, ["half-honest: %s"
                      % ("why-not-10 named, limits missing" if has_why
                         else "limits listed, why-not-10 missing")]
    return 3.0, ["no why-not-10, no limits — a score without limits is a wish"]


CRITERIA = [
    ("evidence", score_evidence),
    ("verification", score_verification),
    ("tests", score_tests),
    ("value", score_value),
    ("prevention", score_prevention),
    ("honesty", score_honesty),
]


# The 10 solutions: what to do to make each criterion a 10, keyed by
# criterion and current score. The report's to_10 list is built from
# these, lowest criterion first, capped at 10 entries.
TO_10 = {
    "evidence": {
        2.0: ["Add checkable evidence refs (path / SHA / comment id / test name) for every claim — no bytes, no score"],
        5.0: ["Give every evidence item a checkable ref, not just a claim"],
        8.0: ["Add a second checkable evidence ref"],
    },
    "verification": {
        3.0: ["Get a DIFFERENT seat to verify it — never verify your own work (Inviolable)"],
        4.0: ["Get a different seat to verify it — unverified work cannot ship"],
        7.0: ["Ask the verifier to attach a score"],
        8.0: ["Raise the verification score to 9.5+ by fixing what the verifier found"],
    },
    "tests": {
        3.0: ["Run the tests"],
        5.0: ["Fix what the test reason says: make tests able to fail, fix red tests, add real assertions"],
    },
    "value": {
        3.0: ["Name the human benefit AND what it unblocks — motion is not value"],
        7.0: ["Name the human benefit, not just what it unblocks"],
        9.0: ["Name what it unblocks, alongside the human benefit"],
    },
    "prevention": {
        4.0: ["Name the gate that makes this whole class impossible, and wire it"],
        6.0: ["Wire the named gate — a named-but-unwired gate does not prevent"],
    },
    "honesty": {
        3.0: ["Write why-not-10 and list the limits"],
        6.0: ["Write the missing half: why-not-10 and the limits list"],
    },
}


def score_work(work):
    """Score a work dict. Returns the full report dict."""
    if not isinstance(work, dict):
        return {
            "title": "",
            "overall": 0.0,
            "verdict": "HOLD",
            "blocking": ["input"],
            "criteria": {"input": {"score": 0.0,
                                   "reasons": ["unreadable input — fail-closed"]}},
            "pass": 1,
            "to_10": ["Provide the work as a JSON object so it can be scored."],
            "next": "Provide the work as a JSON object with evidence, tests, "
                    "verification, value, prevention, honesty.",
        }
    try:
        pass_no = int(work.get("pass", 1))
    except (TypeError, ValueError):
        pass_no = 1
    pass_no = max(1, min(MAX_PASSES, pass_no))
    criteria = {}
    for name, fn in CRITERIA:
        s, reasons = fn(work)
        criteria[name] = {"score": s, "reasons": reasons}
    overall = min(c["score"] for c in criteria.values())
    blocking = [n for n, c in criteria.items() if c["score"] == overall]
    # The 10 solutions: fixes for every sub-10 criterion, lowest first,
    # capped at 10 entries. Implement them, re-score, repeat.
    ranked = sorted(criteria.items(), key=lambda kv: kv[1]["score"])
    to_10 = []
    for name, c in ranked:
        if c["score"] < 10.0:
            to_10.extend(TO_10.get(name, {}).get(c["score"], []))
    to_10 = to_10[:MAX_SOLUTIONS]
    if overall >= SHIP_BAR:
        verdict = "SHIP"
        nxt = "Math authorizes. Ship it — no word from any seat is needed."
    elif overall >= FIX_BAR:
        verdict = "FIX"
        nxt = "Fix the blocking criterion (%s), then re-score." % ", ".join(blocking)
    else:
        verdict = "HOLD"
        nxt = "Do not ship. Lowest criterion (%s) must move first." % ", ".join(blocking)
    if pass_no >= MAX_PASSES and verdict != "SHIP":
        nxt = ("Pass %d of %d done. Announce: got it to %.1f, needs over 9. "
               "Pass off for decision with three options + pros/cons."
               % (MAX_PASSES, MAX_PASSES, overall))
    return {
        "title": work.get("title", ""),
        "overall": overall,
        "verdict": verdict,
        "blocking": blocking,
        "criteria": criteria,
        "pass": pass_no,
        "to_10": to_10,
        "next": nxt,
    }


def render_human(report):
    lines = ["Scorecard: %s" % (report.get("title") or "(untitled)")]
    lines.append("Overall: %.1f/10 — %s" % (report["overall"], report["verdict"]))
    lines.append("Pass: %d of %d" % (report.get("pass", 1), MAX_PASSES))
    for name, _ in CRITERIA:
        c = report["criteria"].get(name)
        if c is None:
            continue
        lines.append("  %-12s %4.1f  %s" % (name, c["score"], "; ".join(c["reasons"])))
    if "input" in report["criteria"]:
        c = report["criteria"]["input"]
        lines.append("  %-12s %4.1f  %s" % ("input", c["score"], "; ".join(c["reasons"])))
    lines.append("Blocking: %s" % ", ".join(report["blocking"]))
    to_10 = report.get("to_10") or []
    if to_10:
        lines.append("To reach 10 — implement, re-score, repeat:")
        for i, fix in enumerate(to_10, 1):
            lines.append("  %d. %s" % (i, fix))
    lines.append("Next: %s" % report["next"])
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Automatic scorecard calculator.")
    parser.add_argument("--input", default=None, help="JSON file describing the work (default: stdin)")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args(argv)
    try:
        raw = open(args.input).read() if args.input else sys.stdin.read()
        work = json.loads(raw)
    except (OSError, ValueError):
        report = score_work(None)
        print(render_human(report) if not args.json else json.dumps(report, indent=2))
        return 2
    report = score_work(work)
    print(render_human(report) if not args.json else json.dumps(report, indent=2))
    return 0 if report["verdict"] == "SHIP" else 1


if __name__ == "__main__":
    raise SystemExit(main())
