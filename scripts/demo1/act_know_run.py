#!/usr/bin/env python3
"""Demo-1 ACT→KNOW run: hand a real staging execution receipt to KNOW.

Chain (all local, no production write):
  1. Load the ACT execution receipt (default: the P1 live run's receipt).
  2. Verify it end-to-end (seal recompute + artifact re-hash) — BEFORE
     KNOW is touched; any failure refuses here.
  3. Build the KNOW ingestion candidate FROM the verified facts only.
  4. kernel.decide() with the KNOW sub-state carrying the candidate —
     the kernel's KNOW gate runs the §3.1 ingestion gate end-to-end.
  5. Retrieve the observation back through KNOW's own retrieval gates.
  6. (--seam-adapter PATH) Project the kernel decision receipt through
     Naya 2's project_kernel_receipt READ-ONLY (pure function — no I/O,
     no database call) and print the projected ledger parameters.

Stated boundaries:
- KNOW's store is in-memory (runtime-local), not the production ledger.
- The --seam-adapter owner_id is a format-valid TEST uuid, not a real
  auth.users identity; the real demo identity is Shawn's call.
- The ACT-verb receipt authorizing the staging execution carries the
  suite's director_order test attestation (P1 boundary); LAW-side
  minting inside the Python kernel remains a named gap.

Usage:
    python3 scripts/demo1/act_know_run.py [--root DIR] [--receipt PATH]
                                         [--seam-adapter PATH]

Default root: ~/workspace/demo-staging
Default receipt: <root>/receipts/exec-b97b2def9160ba53.json (P1 live run)
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
# Demo gate states are the shared fixtures from the kernel test suite —
# the canonical demo sub-states, not production data.
sys.path.insert(0, str(REPO_ROOT / "tests"))

from naya_kernel import act_know_handoff as handoff
from naya_kernel.kernel import Kernel, verify_decision_receipt

import test_nodes.test_kernel_nine_node as T

PRINCIPAL = {"identity": "naya-demo", "entitled_scopes": ["public", "team"]}
DEFAULT_EXECUTION_ID = "exec-b97b2def9160ba53"
# Format-valid TEST uuid for the read-only projection check only.
TEST_OWNER_ID = "123e4567-e89b-12d3-a456-426614174000"


def _gate_states(kernel):
    return {
        "SELF": T.self_state(), "LAW": T.law_state(), "ACT": T.act_state(),
        "PROVE": T.prove_state(kernel), "CONNECT": T.connect_state(),
        "VERIFY": T.verify_state(kernel), "LEARN": T.learn_state(kernel),
        "EVOLVE": {"action": "metrics"},
    }


def _load_adapter(path):
    spec = importlib.util.spec_from_file_location(
        "persistence_seam_adapter", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path.home() / "workspace"
                                          / "demo-staging"),
                    help="staging root; receipt binds <root>/demo-staging/<file>")
    ap.add_argument("--receipt", default=None,
                    help="ACT execution receipt JSON (default: the P1 live run)")
    ap.add_argument("--seam-adapter", default=None,
                    help="path to Naya 2's persistence_seam.py for a "
                         "READ-ONLY projection (no database call)")
    args = ap.parse_args()

    root = Path(args.root)
    staging_root = str(root.parent) if root.name == "demo-staging" else str(root)
    receipt_path = Path(args.receipt) if args.receipt else \
        root / "receipts" / (DEFAULT_EXECUTION_ID + ".json")
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    print("receipt:", receipt_path)

    kernel = Kernel()
    try:
        result = handoff.handoff_act_to_know(
            kernel, receipt, staging_root=staging_root,
            principal=PRINCIPAL, gate_states=_gate_states(kernel),
            decision_id="demo1-act-know-live-001")
    except handoff.HandoffRefused as exc:
        print("HANDOFF REFUSED:", exc)
        return 1

    obs = result["observation"]
    print("verified: seal MATCH, artifact re-hash MATCH")
    print("execution_id:", obs["execution_id"])
    print("artifact:", obs["artifact_relpath"],
          "(%d bytes, sha256:%s…)" % (obs["artifact_bytes"],
                                      obs["artifact_sha256"][:16]))
    print("KNOW gate:", result["know_verdict"])
    print("KNOW block:", result["block_id"])

    know = kernel.nodes["KNOW"]
    served = know.retrieve(
        {"text": "staging.write_file executed",
         "requested_scopes": ["public"],
         "identity_binding": {"verified": True}},
        PRINCIPAL)
    print("KNOW retrieve: admitted=%s served=%d"
          % (served["admitted"], len(served["blocks"])))
    if not any(b["id"] == result["block_id"] for b in served["blocks"]):
        print("RETRIEVAL FAILED — block not served")
        return 1

    decision_receipt = result["decision_receipt"]
    print("decision:", decision_receipt["receipt_id"],
          "| verdict:", decision_receipt["verdict"])
    print("inputs_hash:", decision_receipt["inputs_hash"])
    check = verify_decision_receipt(decision_receipt)
    print("decision seal recompute:", check["result"])

    # Persist the decision receipt + the decided input state beside the ACT
    # execution receipt: the durable pair the seam's inputs_hash recompute
    # needs (local stand-in — the production ledger write is not performed).
    receipts_dir = receipt_path.parent
    decision_path = receipts_dir / (decision_receipt["receipt_id"] + ".json")
    decision_path.write_text(
        json.dumps({"decision_receipt": decision_receipt,
                    "input_state": result["input_state"]},
                   indent=2, sort_keys=True),
        encoding="utf-8")
    print("decision receipt:", decision_path)

    if args.seam_adapter:
        seam = _load_adapter(args.seam_adapter)
        params = seam.project_kernel_receipt(
            decision_receipt,
            owner_id=TEST_OWNER_ID,
            kernel_sha="123fc98ed86daccf8364a419bece89566b6d6ecc",
            inputs_state=result["input_state"],
        )
        print()
        print("seam projection (READ-ONLY — no database call):")
        print("  p_owner_id:", params["p_owner_id"])
        print("  p_event_type:", params["p_event_type"],
              "| p_source_table:", params["p_source_table"])
        print("  p_source_id:", params["p_source_id"])
        print("  p_event_at == receipt issued_at:",
              params["p_event_at"] == decision_receipt["issued_at"])
        print("  p_verification:", params["p_verification"])
        print("  p_value is the full native receipt:",
              params["p_value"] == decision_receipt)
        print("  p_outcome (must stay empty at insert):", params["p_outcome"])
        # The adapter's own recompute, independently:
        canon = json.dumps(result["input_state"], sort_keys=True,
                           separators=(",", ":"), ensure_ascii=True)
        ih = hashlib.sha256(canon.encode("utf-8")).hexdigest()
        print("  inputs_hash recompute MATCH:",
              ih == decision_receipt["inputs_hash"])
    else:
        print()
        print("Tip: pass --seam-adapter <persistence_seam.py> for the "
              "read-only ledger projection.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
