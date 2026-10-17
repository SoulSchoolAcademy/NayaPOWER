#!/usr/bin/env python3
"""Advisory check: does a Shawn-facing deliverable carry a 9+ scorecard?

SN-0526 - Quality Before Speed, The 9+ Delivery Law (Shawn Vibert, 2026-10-08 -
RATIFIED): "No agent sends Shawn anything below 9/10. Every deliverable gets
scorecarded by the sending agent BEFORE it reaches him. If it's not 9+, it
goes back - never forward."

This tool is the FIRST mechanical rung of that law's enforcement. It examines
a deliverable text (PR body, delivery note, chat message) and reports three
verdicts:
  1. SHAWN_FACING  - does the text claim to go to Shawn / be a delivery?
  2. SCORECARD     - does it carry a scorecard with a numeric x/10 score?
  3. NINE_PLUS     - is the best claimed score >= 9.0?

It does NOT validate the score's honesty - Shawn spot-checks the math
(nine-floor doctrine). Honest self-scoring is the next rung.

Usage:
    python3 tools/check_nine_plus_delivery.py --body-file <path> [--pr N] [--summary]
    python3 tools/check_nine_plus_delivery.py --body-env PR_BODY [--pr N] [--summary]
    python3 tools/check_nine_plus_delivery.py --body "<text>" [--pr N] [--summary]
    python3 tools/check_nine_plus_delivery.py --deliverable "<text>" [--summary]
        # assert the text IS Shawn-facing; a missing/unreadable score then fails.

Exit codes:
    0 = PASS           (Shawn-facing, scorecarded, best score >= 9.0)
    1 = FAIL           (Shawn-facing but unscored, or best score < 9.0 -
                        the law fires: it goes back, never forward)
    2 = NOT_SHAWN_FACING (lane traffic, not a deliverable to Shawn - neutral)
    3 = usage / input error

Fail-closed: with --deliverable asserted, an unreadable or unscored body is
FAIL, never PASS. UNKNOWN != PASS.

The CI workflow calling this tool is ADVISORY ONLY: it always succeeds the
check and reports the verdict in the step summary. Promoting this to a
required/blocking check is a merge-policy change and needs the Human
Director's explicit word.

Stdlib only.
"""

import argparse
import os
import re
import sys

# Phrases that mark a text as addressed to Shawn / a delivery to him.
SHAWN_FACING_RES = (
    re.compile(r"\bshawn\b", re.IGNORECASE),
    re.compile(r"merge link", re.IGNORECASE),
    re.compile(r"for your review", re.IGNORECASE),
    re.compile(r"for shawn", re.IGNORECASE),
    re.compile(r"\bdeliver(y|able|ed)?\b", re.IGNORECASE),
    re.compile(r"\bshipped\b", re.IGNORECASE),
    re.compile(r"ready for you", re.IGNORECASE),
    re.compile(r"please merge", re.IGNORECASE),
    re.compile(r"awaiting your", re.IGNORECASE),
)

# A claimed numeric score, e.g. "9.5/10", "9 / 10", "10/10".
SCORE_RE = re.compile(r"\b(10(?:\.0+)?|[0-9](?:\.\d+)?)\s*/\s*10\b")

# A scorecard scaffold signal.
SCORECARD_RE = re.compile(r"scorecard", re.IGNORECASE)


def detect_shawn_facing(text):
    """Return (is_facing, matched_phrase) for Shawn-facing delivery signals."""
    for rx in SHAWN_FACING_RES:
        m = rx.search(text)
        if m:
            return True, m.group(0)
    return False, ""


def extract_scores(text):
    """Return the list of claimed numeric scores (floats) in the text."""
    return [float(m.group(1)) for m in SCORE_RE.finditer(text)]


def evaluate(body, asserted_deliverable=False):
    """Evaluate one deliverable text.

    Returns (exit_code, verdict_dict). Verdict dict carries the three
    mechanical facts: shawn_facing, scorecard_present, nine_plus, plus the
    best claimed score and the facing signal matched.
    """
    if body is None:
        return 3, {"error": "no body supplied"}

    shawn_facing, signal = detect_shawn_facing(body)
    if asserted_deliverable:
        shawn_facing, signal = True, "--deliverable asserted"

    scores = extract_scores(body)
    scorecard = SCORECARD_RE.search(body) is not None or bool(scores)
    best = max(scores) if scores else None
    nine_plus = best is not None and best >= 9.0

    verdict = {
        "shawn_facing": shawn_facing,
        "facing_signal": signal,
        "scorecard_present": scorecard,
        "claimed_scores": scores,
        "best_score": best,
        "nine_plus": nine_plus,
    }

    if not shawn_facing:
        return 2, verdict
    if best is None:
        # Shawn-facing but unscored: violates "scorecarded BEFORE it reaches him".
        return 1, verdict
    return (0 if nine_plus else 1), verdict


def render_summary(pr, exit_code, verdict):
    code_word = {0: "PASS", 1: "FAIL", 2: "NOT_SHAWN_FACING", 3: "ERROR"}[exit_code]
    lines = [
        "## 9+ Delivery Gate (advisory)",
        "",
        "SN-0526 - no agent sends Shawn anything below 9/10; every deliverable",
        "is scorecarded BEFORE it reaches him. First mechanical rung only:",
        "presence and threshold, not honesty.",
        "",
        f"**Verdict: `{code_word}`**" + (f" (PR #{pr})" if pr else ""),
        "",
        f"- Shawn-facing: `{verdict.get('shawn_facing')}`"
        + (f" (signal: _{verdict.get('facing_signal')}_)" if verdict.get("shawn_facing") else ""),
        f"- Scorecard present: `{verdict.get('scorecard_present')}`",
        f"- Claimed scores: `{verdict.get('claimed_scores')}`",
        f"- Best score: `{verdict.get('best_score')}`",
        f"- Nine-plus: `{verdict.get('nine_plus')}`",
        "",
    ]
    if exit_code == 1:
        lines.append(
            "> The 9+ Delivery Law fires: this text reaches for Shawn but is "
            "unscored or below 9.0 - it goes back, never forward."
        )
    elif exit_code == 0:
        lines.append(
            "> Carries a 9+ scorecard. Honesty of the score is Shawn's spot-check "
            "(nine-floor doctrine) - this rung checks presence and threshold only."
        )
    elif exit_code == 2:
        lines.append("> Lane traffic, not a deliverable to Shawn - neutral.")
    lines.append("")
    lines.append(
        "_Advisory only: this check never blocks. Promoting it to a required "
        "check needs the Human Director's explicit word._"
    )
    return "\n".join(lines)


def read_body(args):
    if args.body is not None:
        return args.body
    if args.body_file is not None:
        try:
            with open(args.body_file, "r", encoding="utf-8") as f:
                return f.read()
        except OSError:
            return None
    if args.body_env is not None:
        return os.environ.get(args.body_env)
    if args.deliverable is not None:
        return args.deliverable
    return None


def main(argv=None):
    parser = argparse.ArgumentParser(description="SN-0526 9+ delivery gate (advisory).")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--body", help="deliverable text inline")
    group.add_argument("--body-file", help="path to file holding the deliverable text")
    group.add_argument("--body-env", help="env var holding the deliverable text")
    group.add_argument("--deliverable", help="assert the text IS Shawn-facing")
    parser.add_argument("--pr", help="PR number, for the summary only")
    parser.add_argument("--summary", action="store_true", help="print a markdown summary")
    args = parser.parse_args(argv)

    body = read_body(args)
    if body is None:
        print("check_nine_plus_delivery: unreadable or missing body", file=sys.stderr)
        return 3

    exit_code, verdict = evaluate(body, asserted_deliverable=args.deliverable is not None)
    if args.summary:
        print(render_summary(args.pr, exit_code, verdict))
    else:
        code_word = {0: "PASS", 1: "FAIL", 2: "NOT_SHAWN_FACING", 3: "ERROR"}[exit_code]
        print(f"9+ delivery gate verdict: {code_word} (best={verdict.get('best_score')})")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
