#!/usr/bin/env python3
"""Advisory check: does a PR body carry the Scorecard Law's five-step receipt?

Scorecard Law (Shawn Vibert, 2026-10-05 — RATIFIED): every real decision gets
a written scorecard receipt; no receipt, no merge. The receipt IS the five
steps: 1. ENUMERATE  2. SCORE  3. GATE  4. DECIDE  5. RECEIPT.

This tool is the FIRST mechanical rung of that law's enforcement: it detects
whether the PR body contains a scorecard receipt section with all five steps.
It does NOT validate the receipt's quality — structured validation against
tools/auto_merge_gate.py's pr_state schema is the next rung.

Usage:
    python3 tools/check_scorecard_receipt.py --body-file <path>
    python3 tools/check_scorecard_receipt.py --body-env PR_BODY
    python3 tools/check_scorecard_receipt.py --body "<text>"

Exit codes:
    0 = PRESENT (section found, 5/5 steps)
    1 = PARTIAL (section found, 1-4 steps) or MISSING (no section)
    2 = usage / input error

The CI workflow that calls this tool is ADVISORY ONLY: it always succeeds the
check and reports the verdict in the step summary. Promoting this to a
required/blocking check is a merge-policy change and needs the Human
Director's word.

Fail-closed: an unreadable body is MISSING, never PRESENT. UNKNOWN != PASS.

Stdlib only.
"""

import argparse
import json
import os
import re
import sys

STEP_KEYWORDS = ("enumerate", "score", "gate", "decide", "receipt")

# A scorecard receipt section header, e.g. "## Scorecard receipt".
SECTION_RE = re.compile(r"^#{1,6}\s+.*scorecard.*$", re.IGNORECASE | re.MULTILINE)

# Any markdown header, used to bound the section.
HEADER_RE = re.compile(r"^#{1,6}\s+", re.MULTILINE)


def extract_section(body):
    """Return the scorecard receipt section text (without its header line)."""
    m = SECTION_RE.search(body)
    if not m:
        return None
    rest = body[m.end():]
    nxt = HEADER_RE.search(rest)
    if nxt:
        rest = rest[:nxt.start()]
    return rest


def check_steps(section):
    """Return (found_steps, missing_steps) for the five Scorecard Law steps."""
    found = []
    missing = []
    for kw in STEP_KEYWORDS:
        # Word-boundary match so "score" does not match "scorecard" or "scores".
        if re.search(r"\b" + re.escape(kw) + r"\b", section, re.IGNORECASE):
            found.append(kw)
        else:
            missing.append(kw)
    return found, missing


def verdict_for(body):
    section = extract_section(body)
    if section is None:
        return {
            "verdict": "MISSING",
            "steps_found": [],
            "steps_missing": list(STEP_KEYWORDS),
            "detail": "No scorecard receipt section found in the PR body. "
                      "The Scorecard Law requires the five-step receipt "
                      "(enumerate / score / gate / decide / receipt) in the PR body.",
        }
    found, missing = check_steps(section)
    if not found:
        # A header mentioning "scorecard" with zero of the five steps is not
        # a receipt — it is MISSING wearing a header.
        return {
            "verdict": "MISSING",
            "steps_found": [],
            "steps_missing": list(STEP_KEYWORDS),
            "detail": "A scorecard section header was found but none of the "
                      "five steps (enumerate / score / gate / decide / receipt) "
                      "appear in it. The Scorecard Law requires the five-step "
                      "receipt in the PR body.",
        }
    if not missing:
        return {
            "verdict": "PRESENT",
            "steps_found": found,
            "steps_missing": [],
            "detail": "Scorecard receipt section present with all five steps.",
        }
    return {
        "verdict": "PARTIAL",
        "steps_found": found,
        "steps_missing": missing,
        "detail": "Scorecard receipt section found but %d/5 steps present; "
                  "missing: %s." % (len(found), ", ".join(missing)),
    }


def render_summary(result, pr_number=None):
    lines = []
    title = "Scorecard receipt: %s" % result["verdict"]
    if pr_number:
        title += " (PR #%s)" % pr_number
    lines.append("## " + title)
    lines.append("")
    lines.append(result["detail"])
    lines.append("")
    lines.append("| Step | Found |")
    lines.append("|------|-------|")
    for kw in STEP_KEYWORDS:
        mark = "yes" if kw in result["steps_found"] else "no"
        lines.append("| %s | %s |" % (kw, mark))
    lines.append("")
    if result["verdict"] != "PRESENT":
        lines.append(
            "> Advisory: this check never blocks merging. "
            "The merging seat applies the Scorecard Law protocol manually: "
            "no receipt, no merge."
        )
    else:
        lines.append(
            "> Advisory: receipt presence is verified mechanically; receipt "
            "quality is the merging seat's judgment under the Scorecard Law."
        )
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--body-file", help="Path to a file containing the PR body")
    src.add_argument("--body-env", help="Name of an env var containing the PR body")
    src.add_argument("--body", help="PR body text directly")
    ap.add_argument("--pr", default=None, help="PR number (for the summary only)")
    ap.add_argument("--json", action="store_true", help="Emit JSON verdict to stdout")
    ap.add_argument("--summary", action="store_true",
                    help="Emit markdown summary to stdout (for $GITHUB_STEP_SUMMARY)")
    args = ap.parse_args(argv)

    try:
        if args.body_file:
            with open(args.body_file, "r", encoding="utf-8") as f:
                body = f.read()
        elif args.body_env:
            body = os.environ.get(args.body_env, "")
        else:
            body = args.body
    except OSError as e:
        print("SCORECARD-RECEIPT: ERROR reading body: %s" % e, file=sys.stderr)
        return 2

    if body is None:
        body = ""
    result = verdict_for(body)
    result["pr"] = args.pr

    if args.json:
        print(json.dumps(result, indent=2))
    elif args.summary:
        print(render_summary(result, args.pr))
    else:
        print("SCORECARD-RECEIPT: %s — %s" % (result["verdict"], result["detail"]))

    return 0 if result["verdict"] == "PRESENT" else 1


if __name__ == "__main__":
    sys.exit(main())
