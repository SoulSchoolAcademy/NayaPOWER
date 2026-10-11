#!/usr/bin/env python3
"""Trusted issuance: mint a run-attested protocol read receipt.

Runs ONLY in .github/workflows/read-receipt-mint.yml (base code, trusted
runner, workflow_dispatch). It grades the caller-supplied answers against the
CANONICAL authority questions (imported from kernel/protocol/read_receipt.py —
the same source the boot gate grades against), refuses to mint on any failed
answer, and attests the minting run (run_id + run_attempt). The boot gate
verifies the attestation via the live API: the run must exist in the gated
repository, have run the base mint workflow to success, and its artifact's
receipt.json must be byte-identical to the presented receipt.

The answers input is UNTRUSTED (the dispatcher supplies them) but SAFE: the
mint grades them itself against the canonical questions. Wrong answers produce
no receipt — the mint exits non-zero. A forger who knows the right answers
still cannot self-mint: only THIS workflow's attested run passes
verify_issuance.

HONEST CAVEAT (documented, not hidden): run-attestation proves "the trusted
runner ran and graded THESE answers", not "which agent it ran for". The
agent_id in the receipt is caller-supplied. This narrows the identity gap
(the old unkeyed receipt proved nothing about issuance at all) but does not
fully close it.

Usage:
    python3 tools/read_receipt_mint.py --agent-id 'naya-5' \
        --answers '{"q1": "Shawn Vibert", ...}' --out receipt.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                os.pardir))
from kernel.protocol.read_receipt import (  # noqa: E402 — canonical source
    AUTHORITY_QUESTIONS,
    PROTOCOL_VERSION,
    ReadReceipt,
    grade_answer,
)

MINT_WORKFLOW_PATH = ".github/workflows/read-receipt-mint.yml"


def parse_args(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--agent-id", required=True,
                    help="claiming agent seat id (caller-supplied, attested not proven)")
    ap.add_argument("--answers", required=True,
                    help='JSON object mapping question id -> answer text, e.g. {"q1": "..."}')
    ap.add_argument("--out", required=True, help="receipt output path")
    return ap.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    run_id = os.environ.get("GITHUB_RUN_ID", "").strip()
    run_attempt = os.environ.get("GITHUB_RUN_ATTEMPT", "1").strip()
    if not run_id:
        print("mint: no GITHUB_RUN_ID — refusing (mint only in the trusted "
              "runner)", file=sys.stderr)
        return 2

    try:
        answers = json.loads(args.answers)
    except ValueError as e:
        print("mint: answers JSON unparseable: %s" % e, file=sys.stderr)
        return 2
    if not isinstance(answers, dict):
        print("mint: answers must be a JSON object", file=sys.stderr)
        return 2

    # Grade against the CANONICAL questions — the same source the boot gate uses.
    results = {}
    for q in AUTHORITY_QUESTIONS:
        ans = answers.get(q["id"], "")
        if not isinstance(ans, str):
            ans = str(ans)
        results[q["id"]] = grade_answer(q, ans)
    passed = all(results.values())
    if not passed:
        failed = sorted(k for k, v in results.items() if not v)
        print("mint: answers failed grading for %s — no receipt minted"
              % failed, file=sys.stderr)
        return 2

    # Build the integrity-signed receipt (same construction as issue_receipt).
    receipt = ReadReceipt(
        agent_id=args.agent_id,
        protocol_version=PROTOCOL_VERSION,
        answers=results,
        passed=True,
    ).sign()

    envelope = {
        "schema": "naya/read-receipt-attested-v1",
        "receipt": {
            "agent_id": receipt.agent_id,
            "protocol_version": receipt.protocol_version,
            "answers": receipt.answers,
            "passed": receipt.passed,
            "issued_at": receipt.issued_at,
            "receipt_hash": receipt.receipt_hash,
        },
        "attestation": {
            "workflow": MINT_WORKFLOW_PATH,
            "run_id": int(run_id),
            "run_attempt": int(run_attempt) if run_attempt.isdigit() else 1,
            "minted_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "_note": ("minted by the trusted runner; the boot gate verifies "
                      "this run via the live API. Attestation proves the "
                      "runner ran, not which agent it ran for."),
        },
    }

    # Sanity: the receipt we just minted must pass the integrity check
    # (fail fast here, not at boot).
    check = ReadReceipt(
        agent_id=receipt.agent_id,
        protocol_version=receipt.protocol_version,
        answers=receipt.answers,
        passed=receipt.passed,
        issued_at=receipt.issued_at,
        receipt_hash=receipt.receipt_hash,
    )
    if not check.verify():
        print("mint: self-check failed — minted receipt does not verify",
              file=sys.stderr)
        return 2

    raw = json.dumps(envelope, sort_keys=True).encode()
    with open(args.out, "wb") as f:
        f.write(raw)
    print("mint: attested read receipt for %s, run %s (protocol %s)"
          % (args.agent_id, run_id, PROTOCOL_VERSION))
    return 0


if __name__ == "__main__":
    sys.exit(main())
