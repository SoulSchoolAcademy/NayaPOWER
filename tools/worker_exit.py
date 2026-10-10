#!/usr/bin/env python3
"""
worker_exit.py — Machine-enforced exit verifier for every worker shift.

Every worker MUST run this last. It validates the shift's claimed outcome
against evidence before the worker is allowed to report success.

Usage:
    python3 tools/worker_exit.py --claim <nothing_changed|work_done|blocked> [--evidence <text>]

Exit codes:
    0 = Report accepted. Worker may exit.
    1 = Report rejected. Claim does not match evidence. Fix and re-run.

This is THE PROTOCOL, step 5 (VERIFY), enforced in code — not prose.

Rules enforced:
- "work_done" requires evidence: named files changed, PR opened, or specific verifiable outcome.
- "nothing_changed" requires no evidence (it IS the evidence of discipline).
- "blocked" requires naming the blocker.
- Vague claims ("did stuff", "checked things", "worked on it") are REJECTED.
"""

import argparse
import re
import sys

# Patterns that indicate vague, unverifiable claims
VAGUE_PATTERNS = [
    r'\bdid stuff\b',
    r'\bworked on\b.*\bthings\b',
    r'\bchecked things\b',
    r'\bmade progress\b(?!\s+on\s+\S+)',  # "made progress" without saying on what
    r'\blooked into\b(?!\s+\S+)',
    r'\bstuff happened\b',
]

# Patterns that indicate concrete, verifiable evidence
EVIDENCE_PATTERNS = [
    r'PR\s*#\d+',                    # PR number
    r'\b[0-9a-f]{7,40}\b',           # SHA
    r'comment\s+\d{9,}',              # comment ID
    r'merged',                        # merge action
    r'verified',                      # verification claim
    r'\.md\b|\.py\b|\.json\b',       # file changed
    r'nothing changed',               # valid no-work outcome
    r'no pending',                    # valid no-work outcome
    r'blocked by',                    # valid blocked outcome
    r'tip\s+[0-9a-f]{7}',            # tip reference
]


def is_vague(text):
    """Check if the evidence text is vague hand-waving."""
    text_lower = text.lower()
    for pattern in VAGUE_PATTERNS:
        if re.search(pattern, text_lower):
            return True
    return False


def has_evidence(text):
    """Check if the evidence text contains verifiable specifics."""
    text_lower = text.lower()
    for pattern in EVIDENCE_PATTERNS:
        if re.search(pattern, text_lower):
            return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Worker exit verifier")
    parser.add_argument("--claim", required=True,
                        choices=["nothing_changed", "work_done", "blocked"],
                        help="What the worker claims happened")
    parser.add_argument("--evidence", default="",
                        help="Evidence supporting the claim")
    args = parser.parse_args()

    claim = args.claim
    evidence = args.evidence.strip()

    # Rule 1: nothing_changed needs no evidence — it IS the disciplined outcome
    if claim == "nothing_changed":
        print("ACCEPTED: nothing_changed. Clean exit. This is excellence.")
        sys.exit(0)

    # Rule 2: blocked requires naming the blocker
    if claim == "blocked":
        if not evidence:
            print("REJECTED: 'blocked' claim requires naming the blocker. What blocked you?")
            sys.exit(1)
        print(f"ACCEPTED: blocked. Blocker recorded: {evidence[:100]}")
        sys.exit(0)

    # Rule 3: work_done requires verifiable evidence
    if claim == "work_done":
        if not evidence:
            print("REJECTED: 'work_done' claim requires evidence. What specifically did you do?")
            sys.exit(1)
        if is_vague(evidence):
            print(f"REJECTED: evidence is vague hand-waving: '{evidence[:100]}'")
            print("Name the PR, SHA, file, comment ID, or specific verifiable outcome.")
            sys.exit(1)
        if not has_evidence(evidence):
            print(f"REJECTED: evidence lacks verifiable specifics: '{evidence[:100]}'")
            print("Include: PR number, commit SHA, file changed, comment ID, or exact verification.")
            sys.exit(1)
        print("ACCEPTED: work_done with verifiable evidence.")
        sys.exit(0)


if __name__ == "__main__":
    main()
