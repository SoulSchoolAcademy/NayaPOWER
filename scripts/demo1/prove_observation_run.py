#!/usr/bin/env python3
"""Demo-1 P3 live run: PROVE/CONNECT handling of a real handed-off observation.

Chain (all local, no production write):
  1. Load a persisted ACT execution receipt (default: the P1 live run's
     receipt) + the artifact bytes on disk.
  2. Cold-replay the P2 ACT->KNOW handoff deterministically from those
     persisted inputs (the KNOW store is in-memory; nothing is carried
     over from any prior process).
  3. Re-verify the whole chain (EXECUTED path, ACT seal, receipt-hash
     consistency, artifact re-hash, handoff decision seal, KNOW block
     provenance + gated retrieval) — BEFORE PROVE sees anything.
  4. Build the post-action PROOF_CLAIM from the verified facts only and
     certify it through the kernel's PROVE gate inside decide().
  5. crossing_check admits the sealed claim across the CONNECT boundary.
  6. Persist the decision receipt + decided input state beside the ACT
     execution receipt (local stand-in — the production ledger write is
     not performed).

Stated boundaries:
- KNOW's store is in-memory (runtime-local), not the production ledger.
- The demo principal is a test identity; the real demo identity binding
  remains a named open question for Shawn.
- The ACT-verb receipt authorizing the staging execution carries the
  suite's director_order test attestation (P1 boundary); full LAW-side
  minting inside the Python kernel remains a named gap.

Usage:
    python3 scripts/demo1/prove_observation_run.py [--root DIR] [--receipt PATH]

Default root: ~/workspace/demo-staging
Default receipt: <root>/receipts/exec-b97b2def9160ba53.json (P1 live run)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
# Demo gate states are the shared fixtures from the kernel test suite —
# the canonical demo sub-states, not production data.
sys.path.insert(0, str(REPO_ROOT / "tests"))

from naya_kernel import act_know_handoff as handoff
from naya_kernel import prove_observation as prove_obs
from naya_kernel.kernel import Kernel, verify_decision_receipt

import test_nodes.test_kernel_nine_node as T

PRINCIPAL = {"identity": "naya-demo", "entitled_scopes": ["public", "team"]}
DEFAULT_EXECUTION_ID = "exec-b97b2def9160ba53"


def _gate_states(kernel):
    from naya_kernel.nodes import learn_node as _learn_node
    kernel.nodes["LEARN"] = _learn_node.LearnNode(allow_fixture_intake=True)
    return {
        "SELF": T.self_state(), "LAW": T.law_state(), "ACT": T.act_state(),
        "KNOW": T.know_state(),
        "PROVE": T.prove_state(kernel), "CONNECT": T.connect_state(),
        "VERIFY": T.verify_state(kernel), "LEARN": T.learn_state(kernel),
        "EVOLVE": {"action": "metrics"},
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path.home() / "workspace"
                                          / "demo-staging"),
                    help="staging root; receipt binds <root>/demo-staging/<file>")
    ap.add_argument("--receipt", default=None,
                    help="ACT execution receipt JSON (default: the P1 live run)")
    args = ap.parse_args()

    root = Path(args.root)
    staging_root = str(root.parent) if root.name == "demo-staging" else str(root)
    receipt_path = Path(args.receipt) if args.receipt else \
        root / "receipts" / (DEFAULT_EXECUTION_ID + ".json")
    act_receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    print("receipt:", receipt_path)

    kernel = Kernel()
    now = datetime.now(timezone.utc).isoformat()
    # One gate-state context for the whole cold replay: the handoff and
    # the proof share the kernel, exactly as the test chain does.
    gates = _gate_states(kernel)

    # Cold replay: the P2 handoff re-derived from persisted inputs only.
    try:
        handoff_result = handoff.handoff_act_to_know(
            kernel, act_receipt, staging_root=staging_root,
            principal=PRINCIPAL, gate_states=gates,
            decision_id="demo1-prove-live-handoff")
    except handoff.HandoffRefused as exc:
        print("HANDOFF REFUSED:", exc)
        return 1
    print("handoff replayed: KNOW gate", handoff_result["know_verdict"],
          "| block", handoff_result["block_id"])

    try:
        result = prove_obs.prove_observation(
            kernel, handoff_result, act_receipt,
            staging_root=staging_root, principal=PRINCIPAL,
            gate_states=gates,
            decision_id="demo1-prove-live-001", now=now)
    except prove_obs.ProveObservationRefused as exc:
        print("PROOF REFUSED:", exc)
        return 1

    obs = result["verified"]
    print("re-verified: EXECUTED path, ACT seal MATCH, artifact re-hash MATCH,")
    print("             handoff decision seal MATCH, KNOW block + retrieval MATCH")
    print("execution_id:", obs["execution_id"])
    print("artifact:", obs["artifact_relpath"],
          "(%d bytes, sha256:%s…)" % (obs["artifact_bytes"],
                                      obs["artifact_sha256"][:16]))
    print("PROVE gate:", result["prove_verdict"],
          "| level: L%d" % result["proof_level"],
          "| sealed receipt:", result["sealed_receipt_id"])
    print("CONNECT crossing:", result["crossing"]["cross"])

    decision_receipt = result["decision_receipt"]
    print("decision:", decision_receipt["receipt_id"],
          "| verdict:", decision_receipt["verdict"])
    print("inputs_hash:", decision_receipt["inputs_hash"])
    check = verify_decision_receipt(decision_receipt)
    print("decision seal recompute:", check["result"])
    canon = json.dumps(result["input_state"], sort_keys=True,
                       separators=(",", ":"), ensure_ascii=True)
    ih = hashlib.sha256(canon.encode("utf-8")).hexdigest()
    print("inputs_hash recompute MATCH:", ih == decision_receipt["inputs_hash"])

    # Persist the decision receipt + the decided input state beside the ACT
    # execution receipt: the durable pair the seam's inputs_hash recompute
    # needs (local stand-in — the production ledger write is not performed).
    receipts_dir = receipt_path.parent
    decision_path = receipts_dir / (decision_receipt["receipt_id"] + ".json")
    decision_path.write_text(
        json.dumps({"decision_receipt": decision_receipt,
                    "input_state": result["input_state"],
                    "proof_claim_id": result["claim_id"],
                    "proof_level": result["proof_level"],
                    "sealed_receipt_id": result["sealed_receipt_id"],
                    "crossing": result["crossing"]},
                   indent=2, sort_keys=True),
        encoding="utf-8")
    print("decision receipt:", decision_path)
    sha = hashlib.sha256(decision_path.read_bytes()).hexdigest()
    print("decision receipt sha256:", sha)
    return 0


if __name__ == "__main__":
    sys.exit(main())
