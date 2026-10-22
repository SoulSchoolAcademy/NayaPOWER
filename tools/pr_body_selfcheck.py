#!/usr/bin/env python3
"""Pre-post PR body self-check.

Runs the RECEIPT gate's OWN checks (tools/check_pr_receipt) against a PR
body BEFORE it is posted, so a format miss the gate would fail in CI is
caught at the desk. Recurring class closed: the bold-vs-H2 miss —
`**Evidence**` instead of `## Evidence` — that burned PR #2612's first
gate run (#2597 lineage: a human caught what the machine should have).

Nothing here reimplements the gate: the tool imports the gate module and
runs its main(); the verdict is the gate's verdict, observed locally.
Compare the body against the gate's own regex before CI does — by running
the gate itself.

Usage:
    python3 tools/pr_body_selfcheck.py <body-file>
    cat body.md | python3 tools/pr_body_selfcheck.py
Run from the repo root (or the PR head checkout): handle-liveness checks
(git cat-file) resolve against the current checkout.

Exit 0: the receipt gate would be GREEN locally.
Exit 1: the receipt gate would be RED — fix before posting (the gate's own
         reason is printed verbatim).
Exit 2: no body given.
Warnings (never fail the check):
    no 'Seat: ...' tag — the evidence gate treats a missing author seat as
    vacuous independence; declare it so reviews bind to the author seat.
Stdlib only.
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def read_body(argv):
    if len(argv) > 1:
        with open(argv[1], "r", encoding="utf-8") as f:
            return f.read()
    data = sys.stdin.read()
    if not data.strip():
        print("SELFCHECK: no body given (file arg or stdin).", file=sys.stderr)
        return None
    return data


def main():
    body = read_body(sys.argv)
    if body is None:
        return 2
    os.environ["PR_BODY"] = body

    import check_pr_receipt  # the gate itself — never reimplemented

    buf = io.StringIO()
    old = sys.stdout
    sys.stdout = buf
    try:
        check_pr_receipt.main()
        code = 0
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else 1
    finally:
        sys.stdout = old
    gate_out = buf.getvalue().rstrip()

    if code != 0:
        print("SELFCHECK FAIL: the receipt gate would be RED on this body.")
        print("--- the gate's own reason ---")
        print(gate_out)
        print("-----------------------------")
        print("Fix the body and re-run before posting.")
        return 1

    # Gate GREEN locally. Soft check: seat tag (evidence gate, note 6).
    warn = ""
    try:
        import ci_claim_evidence_gate
        if not ci_claim_evidence_gate.parse_seat_tag(body):
            warn = ("warning: no 'Seat: ...' tag in the body. The evidence gate "
                    "treats a missing author seat as vacuous independence — "
                    "declare your seat so reviews bind to it.")
    except Exception as e:  # the soft check never fails the hard one
        warn = "warning: seat-tag check skipped (%s)." % e

    print("SELFCHECK PASS: the receipt gate would be GREEN locally.")
    print("--- the gate's own verdict ---")
    print(gate_out)
    if warn:
        print(warn)
    return 0


if __name__ == "__main__":
    sys.exit(main())
