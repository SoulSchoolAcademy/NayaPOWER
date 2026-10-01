"""Regression guard for the CONNECT canonical bounded graph seam (issue #1021).

CONNECT has exactly one canonical executable runtime seam — the bounded
graph-behavior/graph-verify pair in `nayanet-cold-runtime-proof` — and this
test guards two invariants:

1. The seam remains present on the tree under test:
   - `supabase/functions/nayanet-cold-runtime-proof/index.ts` still implements
     `mode === "graph-behavior"` and `mode === "graph-verify"`;
   - the OFF/ON control/treatment pair semantics are intact
     (REQUIRE_DIRECT_CANONICAL_INTELLIGENCE vs
     APPLY_CONTEXTUALIZED_VERIFIED_INTELLIGENCE, re-read + eligibility gate);
   - `.github/workflows/live-supabase-runtime-proof.yml` still invokes
     `?mode=graph-behavior`;
   - `tests/verify_cold_graph_behavior.py` still exists.

2. Canonical CONNECT metadata does not overclaim full CONNECT:
   - `BRAIN/03-KERNEL/NODES/CONNECT/0001-CONTRACT.md` records the bounded seam,
     the exact-revision proof marker, and the explicit NOT-PROVEN limits;
   - the runtime registry CONNECT binding keeps a fail-closed proof_boundary:
     binding existence is not proof, and current influence is not
     production-proven.

No new graph, no new persistence, no new authority, no runtime behavior change.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FUNCTION = ROOT / "supabase" / "functions" / "nayanet-cold-runtime-proof" / "index.ts"
WORKFLOW = ROOT / ".github" / "workflows" / "live-supabase-runtime-proof.yml"
VERIFY_SCRIPT = ROOT / "tests" / "verify_cold_graph_behavior.py"
CONTRACT = ROOT / "BRAIN" / "03-KERNEL" / "NODES" / "CONNECT" / "0001-CONTRACT.md"
REGISTRY = ROOT / "BRAIN" / "03-KERNEL" / "0003-RUNTIME-REGISTRY-V1.json"

# Exact-revision proof marker recorded in issue #1021.
PROOF_COMMIT = "c9b31890c93f4f5f7d60bb8cd346093c11ab427f"
PROOF_RUN = "36516790588"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_graph_behavior_mode_present_in_cold_runtime_seam():
    source = _text(FUNCTION)
    assert 'mode === "graph-behavior"' in source
    assert "APPLY_CONTEXTUALIZED_VERIFIED_INTELLIGENCE" in source


def test_graph_verify_mode_present_with_off_on_pair_semantics():
    source = _text(FUNCTION)
    assert 'mode === "graph-verify"' in source
    # Control/treatment pair: graph OFF vs graph ON observed-behavior delta.
    assert "REQUIRE_DIRECT_CANONICAL_INTELLIGENCE" in source
    assert "APPLY_CONTEXTUALIZED_VERIFIED_INTELLIGENCE" in source
    # Pair receipt verification is intact: required receipt ids, pair mismatch
    # rejection, persisted-receipt re-read, eligibility gate on re-read rows.
    assert "RECEIPT_IDS_REQUIRED" in source
    assert "GRAPH_CONTROL_TREATMENT_INPUT_MISMATCH" in source
    assert "graphRelationshipEligible" in source


def test_live_workflow_still_invokes_graph_behavior_seam():
    workflow = _text(WORKFLOW)
    assert "?mode=graph-behavior" in workflow


def test_graph_behavior_verify_script_still_present():
    assert VERIFY_SCRIPT.is_file(), (
        "tests/verify_cold_graph_behavior.py must remain present "
        "(it is part of the bounded seam)"
    )


def test_contract_records_bounded_seam_exact_revision_and_limits():
    contract = _text(CONTRACT)
    # Bounded seam reference.
    assert "graph-behavior" in contract
    assert "graph-verify" in contract
    assert "nayanet-cold-runtime-proof" in contract
    # Exact-revision proof marker (proof does not transfer to other commits).
    assert PROOF_COMMIT in contract
    assert PROOF_RUN in contract
    assert "exact-revision" in contract
    # Explicit NOT-PROVEN limits — the anti-overclaim anchor.
    for limit in (
        "production parity",
        "multi-hop",
        "cycle handling",
        "freshness semantics",
        "supersession",
        "universal CONNECT",
    ):
        assert limit in contract, f"contract must carry NOT-PROVEN limit: {limit}"
    # One canonical seam rule: no parallel graph path.
    assert "no second graph path" in contract or "No new graph" in contract


def test_registry_connect_binding_stays_fail_closed():
    registry = json.loads(_text(REGISTRY))
    binding = registry["node_runtime_bindings"]["CONNECT"]
    # The binding must not claim full CONNECT: status must carry the
    # parity-pending qualification, never a bare ACTIVE/PROVEN/LIVE claim.
    status = binding["status"].upper()
    assert "PENDING" in status, f"CONNECT binding status must stay pending-qualified: {binding['status']}"
    assert status not in {"ACTIVE", "PROVEN", "LIVE", "PRODUCTION"}, (
        f"CONNECT binding overclaims full CONNECT: {binding['status']}"
    )
    # The proof boundary must stay fail-closed: binding existence is not proof,
    # current influence is not production-proven.
    boundary = binding["proof_boundary"].lower()
    assert "not production-proven" in boundary, (
        "CONNECT proof_boundary must keep the fail-closed 'not production-proven' marker"
    )
