"""Guard the canonical live-proof index.

Coder 2, 2026-09-28.

WHY
---
`evidence/live-proof-index.json` exists so a cold Naya can reconstruct "what was
actually proved" from the repository, without being told and without spelunking
through Actions run ids. That value depends entirely on the index being TRUE.

A stale or overclaiming proof index is worse than none. It would let a successor
reconstruct a confident, tidy, wrong picture of the system - which is precisely
the failure the North Star exists to prevent. So the index is guarded on four
axes:

  1. It must record real digests (64 hex chars) for real artifact names.
  2. It must not overclaim: every establishment MUST carry a
     `does_not_establish` boundary. A proof that hides its limits is marketing.
  3. The claims it makes must be internally consistent with each other - e.g. a
     cold-successor entry that claims continuity while recording a non-zero
     successor grant count is self-contradictory and must fail.
  4. It must not reference forbidden credentials.
"""

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
INDEX = REPO / "evidence" / "live-proof-index.json"
GENERATOR = REPO / "BRAIN" / "12-ENGINEERING" / "record-live-proof-index.py"

REQUIRED_CLAIMS = (
    "connect_authority_boundary",
    "cold_successor_continuity",
    "causal_learning_influence",
    "graph_context_behavioural_influence",
)


def _index() -> dict:
    return json.loads(INDEX.read_text(encoding="utf-8"))


def test_index_is_wellformed_and_traced_to_a_real_run():
    d = _index()
    assert d["schema"] == "NAYAPOWER_LIVE_PROOF_INDEX_V1"
    assert re.fullmatch(r"\d{6,}", d["run_id"]), d["run_id"]
    assert re.fullmatch(r"[0-9a-f]{40}", d["head_sha"]), d["head_sha"]
    assert d["artifacts"], "index must record the artifacts it points at"
    for name, meta in d["artifacts"].items():
        assert re.fullmatch(r"[0-9a-f]{64}", meta["digest_sha256"]), f"{name} has no real sha256"
        assert meta["bytes"] > 0


def test_every_claim_states_what_it_does_not_establish():
    """No claim without a boundary. This is the anti-marketing guard."""
    d = _index()
    for name in REQUIRED_CLAIMS:
        claim = d["establishes"][name]
        assert "establishes" in claim and claim["establishes"]
        assert "does_not_establish" in claim, f"{name} must state its limits"
        assert claim["does_not_establish"], f"{name} has an EMPTY limit - that is overclaiming"


def test_cold_successor_claim_is_internally_consistent():
    """
    If the index claims successor continuity, the recorded evidence must show
    zero inherited authority. A contradiction must fail here, not in production.
    """
    c = _index()["establishes"]["cold_successor_continuity"]
    ab = c["authority_boundary"]
    assert ab["successor_grant_count"] == 0, "continuity claimed with a non-zero successor grant count"
    assert ab["authority_inherited"] is False
    assert ab["knowledge_creates_authority"] is False
    assert ab["retrieval_creates_authority"] is False
    assert c["cold_start"]["local_state_used"] is False
    assert c["cold_start"]["intelligence_content_accepted_as_input"] is False
    assert c["independent_recheck"]["successor_grant_count"] == 0
    assert c["reconstructed_lesson"], "continuity claimed with no reconstructed lesson"


def test_causal_claim_records_that_the_executor_was_not_trusted():
    c = _index()["establishes"]["causal_learning_influence"]
    basis = c["independent_verification_basis"]
    assert basis["executor_claim_trusted"] is False, (
        "index claims causal verification while recording that the executor's claim WAS trusted"
    )
    assert basis["declared_matches_recomputation"] is True
    recomp = basis["recomputed_from_authoritative_state"]
    assert recomp["recomputed_causal_assessment"] == "CAUSAL_SUPPORTED"
    assert recomp["behavioral_delta_present"] is True
    assert recomp["task_equivalence"] is True
    assert c["executor_runtime_jti"] != c["verifier_runtime_jti"], (
        "index claims independent verification but records the same runtime as executor and verifier"
    )


def test_graph_claim_does_not_claim_generalisation():
    g = _index()["establishes"]["graph_context_behavioural_influence"]
    assert g["control_behavior"] != g["treatment_behavior"], "no behavioural delta recorded"
    assert "NOT evidence of generalized" in g["does_not_establish"]


def test_connect_claim_records_a_refusal_not_a_permission():
    c = _index()["establishes"]["connect_authority_boundary"]
    b = c["behavior"]
    assert b["consequential"] is True
    assert b["allowed"] is False
    assert b["executed"] is False
    assert b["blocked_by"] == "LAW"
    assert c["authority_boundary"]["connect_grants_authority"] is False


def test_index_never_references_forbidden_credentials():
    raw = INDEX.read_text(encoding="utf-8").lower()
    for forbidden in ("service_role", "supabase_user_access_token", "supabase_user_refresh_token",
                      "publishable_key"):
        assert forbidden not in raw, f"index must not reference {forbidden}"


def test_generator_refuses_to_index_a_partial_run():
    """Missing artifact must fail loudly rather than produce a confident partial index."""
    import subprocess
    import sys
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run(
            [sys.executable, str(GENERATOR), tmp, "--run-id", "123456", "--head-sha", "a" * 40],
            capture_output=True, text=True, cwd=str(REPO),
        )
        assert r.returncode != 0
        assert "Refusing to index a partial run" in (r.stdout + r.stderr)
