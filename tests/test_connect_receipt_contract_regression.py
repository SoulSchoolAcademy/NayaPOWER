"""Regression guard for the CONNECT runtime receipt contract.

Coder 2, 2026-09-28.

FINDING THIS GUARDS
-------------------
`supabase/functions/nayanet-cold-runtime-proof/index.ts` in `mode === "connect"`
emitted no `behavior` object and no `authority_boundary` object at all. Three
independent signals showed that single root cause:

  1. `tests/test_connect_runtime_identity_contract.py` failed, because the
     source contained no `blocked_by: "LAW"`.
  2. Live run 36445685851 job `live-connect` died with `KeyError: 'behavior'`.
  3. `independent-connect-verification` was therefore SKIPPED.

So CONNECT -- the kernel function that decides what intelligence is connected
to the body -- produced ZERO evidence that it refuses to authorize consequential
actions. The contract was coherent and consistent between the test and the
verifier. The implementation was the broken layer.

The contract is NOT to be weakened. Knowledge may influence reasoning; knowledge
does not create authority. CONNECT may connect and recognize applicability, but
it must never grant authority for a consequential action.

These tests are source-and-fixture level. They do NOT claim runtime evidence.
Live CONNECT proof remains BLOCKED until the corrected function is redeployed,
because the deployed artifact still predates this fix (source/runtime parity).
"""

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
VERIFIER = REPO / "tests" / "verify_connect_runtime_receipt.py"
FUNCTION = REPO / "supabase" / "functions" / "nayanet-cold-runtime-proof" / "index.ts"


def _binding():
    return {"status": "ACTIVE", "scope": {"target": "NAYA-NODE-0001"}, "actions": ["naya_node_apply"]}


def _good_receipt():
    return {
        # Document-level parity marker. The deployed bundle cannot be inspected from
        # outside, so the contract now requires the runtime to declare which
        # canonical commit it was built from. Without this, a source change that
        # was never deployed is undetectable.
        "deployed_source_revision": "76f0360cd3dc5e1f0b1a1b1e6f5d3b8a4c2e9f710",
        "receipt": {
            "receipt_type": "NAYA-LIVE-CONNECT-RUNTIME-RECEIPT-V1",
            "naya_id": "NAYA-NODE-0001",
            "block_id": "IB-NAYA-NODE-0001-0001",
            "block_owner_match": True,
            "authorization_binding": _binding(),
            "connect": {"connected": True, "relationship_count": 2, "verified_support_count": 1},
            "authority_boundary": {
                "connect_grants_authority": False,
                "consequential_actions_authorized": False,
            },
            "behavior": {"consequential": True, "allowed": False, "executed": False, "blocked_by": "LAW"},
            "production_mutation_performed": False,
            "rls_changed": False,
            "credentials_committed": False,
        }
    }


def _run(receipt, tmp_path):
    path = tmp_path / "receipt.json"
    path.write_text(json.dumps(receipt), encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(VERIFIER), str(path)],
        capture_output=True, text=True, cwd=str(REPO),
    )


def test_connect_source_emits_behavior_and_authority_boundary():
    source = FUNCTION.read_text(encoding="utf-8")
    for literal in ('consequential: true', 'allowed: false', 'executed: false', 'blocked_by: "LAW"',
                    'connect_grants_authority: false'):
        assert literal in source, f"connect mode does not emit {literal}"


def test_verifier_accepts_a_conformant_receipt(tmp_path):
    result = _run(_good_receipt(), tmp_path)
    assert result.returncode == 0, result.stdout + result.stderr


def test_verifier_rejects_missing_behavior_legibly_not_keyerror(tmp_path):
    receipt = _good_receipt()
    del receipt["receipt"]["behavior"]
    result = _run(receipt, tmp_path)
    assert result.returncode != 0
    combined = result.stdout + result.stderr
    assert "CONTRACT_DRIFT" in combined, combined
    assert "KeyError" not in combined, "verifier must diagnose, not crash"


def test_verifier_rejects_missing_authority_boundary_legibly(tmp_path):
    receipt = _good_receipt()
    del receipt["receipt"]["authority_boundary"]
    result = _run(receipt, tmp_path)
    assert result.returncode != 0
    assert "CONTRACT_DRIFT" in (result.stdout + result.stderr)


def test_verifier_rejects_a_receipt_where_connect_claims_authority(tmp_path):
    """Negative path: a receipt asserting CONNECT granted authority must FAIL."""
    receipt = _good_receipt()
    receipt["receipt"]["authority_boundary"]["connect_grants_authority"] = True
    result = _run(receipt, tmp_path)
    assert result.returncode != 0, "verifier accepted a receipt claiming CONNECT grants authority"


def test_verifier_rejects_a_receipt_where_consequential_action_executed(tmp_path):
    """Negative path: CONNECT executing a consequential action must FAIL."""
    receipt = _good_receipt()
    receipt["receipt"]["behavior"]["executed"] = True
    result = _run(receipt, tmp_path)
    assert result.returncode != 0, "verifier accepted a receipt where CONNECT executed the action"


def test_verifier_rejects_a_receipt_blocked_by_something_other_than_law(tmp_path):
    receipt = _good_receipt()
    receipt["receipt"]["behavior"]["blocked_by"] = "NONE"
    result = _run(receipt, tmp_path)
    assert result.returncode != 0


def test_verifier_rejects_credential_commit_claim(tmp_path):
    receipt = _good_receipt()
    receipt["receipt"]["credentials_committed"] = True
    result = _run(receipt, tmp_path)
    assert result.returncode != 0
