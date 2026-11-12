#!/usr/bin/env python3
"""Trusted issuance: mint a run-attested activation receipt.

Runs ONLY in .github/workflows/activation-mint.yml (base code, trusted
runner, workflow_dispatch). It resolves truth ITSELF (runner-written event
payload + live GitHub API — the same protected source as the gate), binds
the caller-supplied deliverables, and attests the minting run
(run_id + run_attempt). The delivery gate verifies the attestation via the
live API: the run must exist in the gated repository, have run the base
mint workflow to success, and its artifact's receipt.json must be
byte-identical to the presented receipt.

The deliverables input is UNTRUSTED (the dispatcher supplies paths+hashes)
but SAFE: the mint only binds what it is told, and the delivery gate
recomputes every hash from the PR's actual bytes. Lying at dispatch time
produces a receipt that cannot verify at delivery.

Usage:
    python3 tools/activation_mint.py --deliverables '<json>' --job '...'
        --proof-plan '...' --gates 'Usefulness Gate,...' --out receipt.json
"""

import argparse
import json
import os
import re
import sys
from datetime import timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from activation_gate import (  # noqa: E402 — same protected source
    resolve_truth, SCHEMA, SHA40_RE, SHA64_RE, CANONICAL_SOURCES,
    _safe_repo_path, _is_deliverable, MINT_WORKFLOW_PATH)

SESSION_TTL_HINT = "4h"


def parse_args(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--deliverables", required=True,
                    help='JSON list of {"path", "sha256"[, "action":"delete"]}')
    ap.add_argument("--job", required=True, help="one sentence: the real outcome")
    ap.add_argument("--proof-plan", default="", help="how the work is verified")
    ap.add_argument("--gates", default="Usefulness Gate",
                    help="comma-separated governing gates")
    ap.add_argument("--session-id", default="",
                    help="activating session id (default: mint run id)")
    ap.add_argument("--naya-identity", default="activation-mint",
                    help="activating seat identity")
    ap.add_argument("--out", required=True, help="receipt output path")
    return ap.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        deliverables = json.loads(args.deliverables)
    except ValueError as e:
        print("mint: deliverables JSON unparseable: %s" % e, file=sys.stderr)
        return 2
    if not isinstance(deliverables, list) or not deliverables:
        print("mint: deliverables must be a non-empty list", file=sys.stderr)
        return 2
    for i, entry in enumerate(deliverables):
        if not isinstance(entry, dict):
            print("mint: deliverables[%d] not an object" % i, file=sys.stderr)
            return 2
        path = entry.get("path", "")
        if not _safe_repo_path(path) or not _is_deliverable(path):
            print("mint: deliverables[%d] path %r unsafe or not a deliverable"
                  % (i, path), file=sys.stderr)
            return 2
        if not isinstance(entry.get("sha256"), str) or not SHA64_RE.match(
                entry.get("sha256", "")):
            print("mint: deliverables[%d] sha256 malformed" % i, file=sys.stderr)
            return 2
        action = entry.get("action", "ship")
        if action not in ("ship", "delete"):
            print("mint: deliverables[%d] action %r unknown" % (i, action),
                  file=sys.stderr)
            return 2

    try:
        truth = resolve_truth()
    except RuntimeError as e:
        print("mint: cannot establish trusted truth: %s" % e, file=sys.stderr)
        return 2

    run_id = os.environ.get("GITHUB_RUN_ID", "").strip()
    run_attempt = os.environ.get("GITHUB_RUN_ATTEMPT", "1").strip()
    if not run_id:
        print("mint: no GITHUB_RUN_ID — refusing (mint only in the trusted "
              "runner)", file=sys.stderr)
        return 2

    receipt = {
        "schema": SCHEMA,
        "status": "ACTIVATED",
        "session_id": args.session_id or ("mint-run-%s" % run_id),
        "naya_identity": args.naya_identity,
        "human_authority": "Shawn",
        "repository": truth["repository"],
        "job": args.job,
        "gates": [g.strip() for g in args.gates.split(",") if g.strip()],
        "proof_plan": args.proof_plan,
        "main_sha": truth["main_sha"],
        "activated_at": truth["now"].isoformat(),
        "loaded": dict(truth["source_blobs"]),
        "deliverables": [
            {"path": e["path"], "sha256": e["sha256"].lower(),
             **({"action": "delete"} if e.get("action") == "delete" else {})}
            for e in deliverables
        ],
        "attestation": {
            "workflow": MINT_WORKFLOW_PATH,
            "run_id": int(run_id),
            "run_attempt": int(run_attempt) if run_attempt.isdigit() else 1,
            "_note": ("minted by the trusted runner; the delivery gate "
                      "verifies this run via the live API"),
        },
    }
    # sanity: the receipt we just minted must pass the predicate's
    # receipt-side checks against the same truth (fail fast, not at delivery)
    from activation_gate import check_receipt  # noqa: E402
    raw = json.dumps(receipt, sort_keys=True).encode()
    _r, verdict, violations = check_receipt(raw, truth)
    if verdict != "PASS":
        print("mint: self-check failed: %s" % violations, file=sys.stderr)
        return 2
    with open(args.out, "wb") as f:
        f.write(raw)
    print("mint: attested receipt for %d deliverable(s), run %s (tip %s)"
          % (len(deliverables), run_id, truth["main_sha"][:12]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
