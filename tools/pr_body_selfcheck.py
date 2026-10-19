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
    python3 tools/pr_body_selfcheck.py [--head <rev>] <body-file>
    cat body.md | python3 tools/pr_body_selfcheck.py [--head <rev>]
--head <rev> (optional): warn when the current checkout lacks the named PR
head object (rev expression or full SHA). A stale checkout manufactures
phantom receipt-gate failures (Gamma w493: full-SHA handle dead locally,
PASS at the PR head). Warn-only: never changes the exit code.
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
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def parse_args(argv):
    """Split the optional --head <rev> flag from the body source.

    Returns (head_rev or None, body_argv) where body_argv keeps the
    program-name slot read_body expects ([0]) followed by the remaining
    positional args (a body file path, or empty for stdin).
    """
    head_rev = None
    rest = []
    i = 1
    while i < len(argv):
        if argv[i] == "--head":
            if i + 1 >= len(argv):
                print("SELFCHECK: --head needs a value (rev or SHA).", file=sys.stderr)
                return None, None  # caller fails closed with exit 2
            head_rev = argv[i + 1]
            i += 2
        else:
            rest.append(argv[i])
            i += 1
    return head_rev, ["prog"] + rest


def warn_head_liveness(head_rev):
    """Warn (never fail) when the checkout lacks the named PR head object.

    The receipt gate's handle-liveness checks (git cat-file) resolve against
    the current checkout — a checkout that predates the PR head manufactures
    phantom failures. Advisory only: the gate's own exit code is untouched.
    """
    try:
        r = subprocess.run(
            ["git", "cat-file", "-e", head_rev + "^{commit}"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30,
        )
        present = r.returncode == 0
    except Exception:
        present = False  # git missing, not a repo, timeout — warn, never fail
    if not present:
        print(
            "warning: --head %s is not present in this checkout "
            "(git cat-file -e failed). Run from the PR-head checkout, or "
            "expect phantom receipt-gate failures. This warning never fails "
            "the check." % head_rev
        )


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
    head_rev, body_argv = parse_args(sys.argv)
    if body_argv is None:
        return 2  # valueless --head: fail closed, message already printed
    if head_rev:
        warn_head_liveness(head_rev)
    body = read_body(body_argv)
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
