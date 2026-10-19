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
    python3 tools/pr_body_selfcheck.py [--head <pr-head-sha>] <body-file>
    cat body.md | python3 tools/pr_body_selfcheck.py [--head <pr-head-sha>]
    python3 tools/pr_body_selfcheck.py --head <sha> <body-file>
Run from the repo root (or the PR head checkout): handle-liveness checks
(git cat-file) resolve against the current checkout. --head is optional;
when given, a liveness probe (git cat-file -e <sha>^{commit}) warns if
this checkout lacks the PR head object — a stale checkout manufactures
phantom gate verdicts (row-2: full-SHA handle dead locally, PASS at the
PR head). The probe is warn-never-fail: it never changes the exit code.
Stdlib only.

Exit 0: the receipt gate would be GREEN locally.
Exit 1: the receipt gate would be RED — fix before posting (the gate's own
         reason is printed verbatim).
Exit 2: no body given.
Warnings (never fail the check):
    no 'Seat: ...' tag — the evidence gate treats a missing author seat as
    vacuous independence; declare it so reviews bind to the author seat.
    --head liveness: checkout lacks the PR head object — verdict may be a
    phantom of a stale checkout; re-run from the PR-head checkout.
"""
import argparse
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def parse_args(argv):
    p = argparse.ArgumentParser(
        description="Pre-post PR body self-check (the receipt gate, locally).")
    p.add_argument("body", nargs="?", default=None,
                   help="PR body file; reads stdin when omitted.")
    p.add_argument("--head", default=None, metavar="SHA",
                   help="optional PR head SHA: warn (never fail) when this "
                        "checkout lacks the head object.")
    return p.parse_args(argv)


def read_body(args):
    if args.body is not None:
        with open(args.body, "r", encoding="utf-8") as f:
            return f.read()
    data = sys.stdin.read()
    if not data.strip():
        print("SELFCHECK: no body given (file arg or stdin).", file=sys.stderr)
        return None
    return data


def head_liveness_warning(sha):
    """Warn-never-fail probe: None when the checkout holds <sha>^{commit}.

    Returns a warning string when the checkout LACKS the head object or
    when git is unavailable — never raises, never fails the check.
    """
    try:
        r = subprocess.run(
            ["git", "cat-file", "-e", sha + "^{commit}"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return ("warning: --head liveness probe skipped (git unavailable); "
                "run from the PR-head checkout to prove handle liveness.")
    if r.returncode != 0:
        return ("warning: this checkout lacks the PR-head object %s "
                "(git cat-file -e %s^{commit} failed). A PASS here may be a "
                "phantom of a stale checkout — re-run from the PR-head "
                "checkout before posting.") % (sha, sha)
    return None


def main():
    args = parse_args(sys.argv[1:])
    body = read_body(args)
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

    # --head liveness probe: warn-never-fail, computed once, printed on
    # both verdict paths. A stale checkout manufactures phantom verdicts
    # in EITHER direction (dead-SHA handle fails locally but passes at the
    # PR head; and a PASS on a checkout missing the head is unearned).
    head_warn = head_liveness_warning(args.head) if args.head else None

    if code != 0:
        print("SELFCHECK FAIL: the receipt gate would be RED on this body.")
        print("--- the gate's own reason ---")
        print(gate_out)
        print("-----------------------------")
        if head_warn:
            print(head_warn)
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
    if head_warn:
        print(head_warn)
    return 0


if __name__ == "__main__":
    sys.exit(main())
