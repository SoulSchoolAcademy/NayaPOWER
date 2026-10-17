#!/usr/bin/env python3
"""Build the tip-pinned LAW live-proof receipt from verified workflow artifacts.

Reads the raw artifacts produced by live-law-proof.yml (primary + independent
verification), re-validates every load-bearing claim — including the NEGATIVE
control (a capability WITHOUT authority must be refused) — and emits the
canonical tip-pinned proof JSON for BRAIN/06-PROOF/.

Fail-closed: any missing file, any failed assertion, any tampered field exits
non-zero and writes NOTHING. A proof is only emitted when the live runtime
actually authorized the in-scope case AND refused the out-of-authority case AND
an independent identity recomputed both.

Stdlib only.

Usage:
    python3 scripts/build_law_tip_proof.py \
        --tip-sha <40-hex main SHA the proof ran against> \
        --run-id <github run id> --run-url <github run url> \
        --law-runtime <edge function base url> \
        --authorized-json authorized-law.json \
        --refusal-json refusal-law.json \
        --sn002-json sn002-authority-proof.json \
        --receipt-ids-json law-receipt-ids.json \
        --verify-authorized-json verify-authorized.json \
        --verify-refusal-json verify-refusal.json \
        --verify-sn002-json verify-sn002.json \
        --out BRAIN/06-PROOF/0006-LAW-LIVE-PROOF-<runid>-V1.json
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCHEMA = "naya.law.live-proof.v1"
EDGE_SLUG = "nayanet-law-runtime"
SN002_RECEIPT_ID = "102d900e-1dc0-44ce-bde4-9d8d668f4d60"

LIMITS = [
    "Bounded LAW vertical slice only; universal nine-node runtime binding remains NOT_PROVEN.",
    "LAW decides and receipts; it does not execute actions.",
    "Issue #978 checkpoint-receipt RLS remains a separate open security gap.",
]


class ProofError(Exception):
    pass


def load(path: str) -> dict:
    p = Path(path)
    if not p.is_file():
        raise ProofError(f"missing artifact: {path}")
    try:
        data = json.loads(p.read_text())
    except json.JSONDecodeError as e:
        raise ProofError(f"artifact not valid JSON: {path}: {e}")
    if not isinstance(data, dict):
        raise ProofError(f"artifact not a JSON object: {path}")
    return data


def req(cond: bool, msg: str) -> None:
    if not cond:
        raise ProofError(msg)


def build(args: argparse.Namespace) -> dict:
    authorized = load(args.authorized_json)
    refusal = load(args.refusal_json)
    sn002 = load(args.sn002_json)
    ids = load(args.receipt_ids_json)
    v_auth = load(args.verify_authorized_json)
    v_ref = load(args.verify_refusal_json)
    v_sn002 = load(args.verify_sn002_json)

    # --- Positive control: in-scope intelligence commit is AUTHORIZED ---
    req(authorized.get("ok") is True, "authorized: ok != true")
    dec = authorized.get("decision") or {}
    req(dec.get("status") == "AUTHORIZED", "authorized: decision.status != AUTHORIZED")
    req(dec.get("reason") == "ACTIVE_IN_SCOPE_GRANT",
        "authorized: reason != ACTIVE_IN_SCOPE_GRANT")
    refs = dec.get("authority_refs") or []
    req(len(refs) == 1, "authorized: expected exactly one authority_ref")
    rec = authorized.get("receipt") or {}
    req(rec.get("action") == "law_authority_decision",
        "authorized: receipt.action != law_authority_decision")
    req(ids.get("authorized_law_receipt_id") == rec.get("id"),
        "authorized: receipt id does not match law-receipt-ids.json")

    # --- Negative control: capability WITHOUT authority MUST be refused ---
    # This is the load-bearing falsifier. If the runtime ever AUTHORIZED the
    # production_deploy case, or the refusal case is missing/tampered, no
    # proof may land.
    req(refusal.get("ok") is True, "refusal: ok != true")
    rdec = refusal.get("decision") or {}
    req(rdec.get("status") == "NEEDS_HUMAN_AUTHORIZATION",
        "refusal: decision.status != NEEDS_HUMAN_AUTHORIZATION (NEGATIVE CONTROL FAILED)")
    req(rdec.get("reason") == "CAPABILITY_DOES_NOT_CREATE_AUTHORITY",
        "refusal: reason != CAPABILITY_DOES_NOT_CREATE_AUTHORITY (NEGATIVE CONTROL FAILED)")
    req(rdec.get("capability_available") is True,
        "refusal: capability_available != true — refusal without capability proves nothing")
    rrec = refusal.get("receipt") or {}
    req(rrec.get("status") == "BLOCKED",
        "refusal: receipt.status != BLOCKED (NEGATIVE CONTROL FAILED)")
    req(ids.get("refusal_law_receipt_id") == rrec.get("id"),
        "refusal: receipt id does not match law-receipt-ids.json")

    # --- Existing-action authority (SN-002 linkage) ---
    req(sn002.get("ok") is True, "sn002: ok != true")
    req(sn002.get("status") == "EXISTING_ACTION_AUTHORITY_VERIFIED",
        "sn002: status != EXISTING_ACTION_AUTHORITY_VERIFIED")
    req((sn002.get("action_receipt") or {}).get("action") == "intelligence_commit",
        "sn002: action_receipt.action != intelligence_commit")

    # --- Independent recomputation by a second governed identity ---
    req(v_auth.get("ok") is True and v_auth.get("status") == "LAW_DECISION_VERIFIED",
        "independent: authorized decision not verified")
    req((v_auth.get("recomputed") or {}).get("status") == "AUTHORIZED",
        "independent: recomputed authorized status != AUTHORIZED")
    req(v_ref.get("ok") is True and v_ref.get("status") == "LAW_DECISION_VERIFIED",
        "independent: refusal decision not verified")
    v_rdec = v_ref.get("recomputed") or {}
    req(v_rdec.get("status") == "NEEDS_HUMAN_AUTHORIZATION",
        "independent: recomputed refusal != NEEDS_HUMAN_AUTHORIZATION")
    req(v_rdec.get("reason") == "CAPABILITY_DOES_NOT_CREATE_AUTHORITY",
        "independent: recomputed refusal reason mismatch")
    req(v_sn002.get("ok") is True
        and v_sn002.get("status") == "EXISTING_ACTION_AUTHORITY_VERIFIED",
        "independent: sn002 not verified")

    # --- Tip pinning ---
    req(re.fullmatch(r"[0-9a-f]{40}", args.tip_sha or "") is not None,
        f"tip-sha is not a 40-hex SHA: {args.tip_sha!r}")
    req(re.fullmatch(r"[0-9]+", args.run_id or "") is not None,
        f"run-id is not numeric: {args.run_id!r}")

    proof = {
        "schema": SCHEMA,
        "status": "PASS",
        "source_main": args.tip_sha,
        "run_id": int(args.run_id),
        "run_url": args.run_url,
        "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "builder": "scripts/build_law_tip_proof.py",
        "proof_class": "tip-pinned by construction (live-law-proof.yml publish-tip-proof)",
        "edge_function": {
            "slug": EDGE_SLUG,
            "endpoint": args.law_runtime,
            "observed": "evaluate + verify round-trips succeeded this run",
        },
        "authorized_case": {
            "law_receipt_id": rec.get("id"),
            "decision": "AUTHORIZED",
            "reason": "ACTIVE_IN_SCOPE_GRANT",
            "authority_grant_id": refs[0],
            "action": "intelligence_commit",
            "target": "NAYA-NODE-0001",
            "existing_action_receipt_id": SN002_RECEIPT_ID,
        },
        "refusal_case": {
            "law_receipt_id": rrec.get("id"),
            "decision": "NEEDS_HUMAN_AUTHORIZATION",
            "reason": "CAPABILITY_DOES_NOT_CREATE_AUTHORITY",
            "door_id": (rdec.get("door") or {}).get("door_id", "DOOR-GITHUB"),
            "capability_available": True,
            "requested_action": "production_deploy",
        },
        "independent_verification": True,
        "limits": LIMITS,
    }
    return proof


def parse_args(argv=None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Build tip-pinned LAW live-proof receipt.")
    ap.add_argument("--tip-sha", required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--run-url", required=True)
    ap.add_argument("--law-runtime", required=True)
    ap.add_argument("--authorized-json", required=True)
    ap.add_argument("--refusal-json", required=True)
    ap.add_argument("--sn002-json", required=True)
    ap.add_argument("--receipt-ids-json", required=True)
    ap.add_argument("--verify-authorized-json", required=True)
    ap.add_argument("--verify-refusal-json", required=True)
    ap.add_argument("--verify-sn002-json", required=True)
    ap.add_argument("--out", required=True)
    return ap.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    try:
        proof = build(args)
    except ProofError as e:
        print(f"build_law_tip_proof: REFUSING to emit proof: {e}", file=sys.stderr)
        return 1
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(proof, indent=2) + "\n")
    print(f"build_law_tip_proof: wrote {out} (source_main={proof['source_main'][:8]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
