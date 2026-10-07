"""Conformance: CVO outcome axes.

Canonical spec: BRAIN/03-KERNEL/SCHEMA/CVO-OUTCOME-AXES-V1.json.

Two mechanisms, both capable of disagreeing:
  1. Producer sweep — every causal_assessment / verification_status literal the
     CVO producers emit must be inside the spec's enums. A producer that
     invents a new status value FAILS this test.
  2. Spec-derived validator + negative controls — the validator implements the
     spec's conformance predicate (including NOT_PROVEN semantics). Malformed
     CVOs must be REJECTED. A validator that accepts one FAILS this test.

Producers (CVO-constructing edge functions):
  - supabase/functions/nayanet-causal-verify/index.ts
  - supabase/functions/nayanet-causal-learning-experiment/index.ts
(nayanet-learning-verify only references causal_verification_id; it does not
construct CVO blocks.)
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "BRAIN" / "03-KERNEL" / "SCHEMA" / "CVO-OUTCOME-AXES-V1.json"
PRODUCERS = [
    ROOT / "supabase" / "functions" / "nayanet-causal-verify" / "index.ts",
    ROOT / "supabase" / "functions" / "nayanet-causal-learning-experiment" / "index.ts",
]
FIXTURE = ROOT / "causal-learning-experiment-receipt.json"
CVO_SCHEMA = "NAYANET_CAUSAL_VERIFICATION_V1"


def load_spec() -> dict:
    return json.loads(SPEC.read_text(encoding="utf-8"))


def emitted_literals(source: str, field: str) -> set[str]:
    """All UPPERCASE string literals assigned to (or compared against) a field."""
    pat = re.compile(rf"{field}\s*(?::|=|===)\s*\"([A-Z][A-Z0-9_]*)\"")
    return set(pat.findall(source))


# ---------------------------------------------------------------------------
# Spec integrity
# ---------------------------------------------------------------------------

def test_spec_loads_and_enums_are_nonempty_and_unique():
    spec = load_spec()
    assert spec["status"] == "CANDIDATE"
    for axis in ("causal_assessment", "verification_status"):
        values = spec["axes"][axis]["enum"]
        assert len(values) >= 1, f"{axis} enum must not be empty"
        assert len(values) == len(set(values)), f"{axis} enum has duplicates"
    for axis in ("observation_status", "authority_status"):
        values = spec["axes"][axis]["observed_values"]
        assert len(values) >= 1, f"{axis} observed_values must not be empty"


# ---------------------------------------------------------------------------
# 1. Producer sweep — producers must not emit values outside the spec
# ---------------------------------------------------------------------------

def test_producer_causal_assessment_literals_conform():
    spec = load_spec()
    allowed = set(spec["axes"]["causal_assessment"]["enum"])
    for producer in PRODUCERS:
        source = producer.read_text(encoding="utf-8")
        found = emitted_literals(source, "causal_assessment") | emitted_literals(
            source, "recomputed_causal_assessment"
        )
        assert found, f"{producer.name}: no causal_assessment literals found (sweep broken?)"
        rogue = found - allowed
        assert not rogue, (
            f"{producer.name} emits causal_assessment value(s) outside the spec: {rogue}. "
            "Amend CVO-OUTCOME-AXES-V1.json by PR first."
        )


def test_producer_verification_status_literals_conform():
    spec = load_spec()
    allowed = set(spec["axes"]["verification_status"]["enum"])
    for producer in PRODUCERS:
        source = producer.read_text(encoding="utf-8")
        found = emitted_literals(source, "verification_status")
        assert found, f"{producer.name}: no verification_status literals found (sweep broken?)"
        rogue = found - allowed
        assert not rogue, (
            f"{producer.name} emits verification_status value(s) outside the spec: {rogue}. "
            "Amend CVO-OUTCOME-AXES-V1.json by PR first."
        )


def test_producer_authority_status_conforms():
    spec = load_spec()
    allowed = set(spec["axes"]["authority_status"]["observed_values"])
    for producer in PRODUCERS:
        source = producer.read_text(encoding="utf-8")
        # authority block: authority:{status:"AUTHORIZED",...} (whitespace may vary)
        found = set(re.findall(r"authority:\s*\{\s*status:\s*\"([A-Z][A-Z0-9_]*)\"", source))
        assert found, f"{producer.name}: no authority.status literal found (sweep broken?)"
        rogue = found - allowed
        assert not rogue, f"{producer.name} authority.status outside spec: {rogue}"


def test_producer_success_gate_is_fail_closed():
    """observation.status axis: CAUSAL_SUPPORTED requires both receipts SUCCESS."""
    for producer in PRODUCERS:
        source = producer.read_text(encoding="utf-8")
        assert '"SUCCESS"' in source, f"{producer.name}: SUCCESS gate literal missing"
    causal_verify = PRODUCERS[0].read_text(encoding="utf-8")
    assert "PAIRED_ACTION_OUTCOME_NOT_SUCCESS" in causal_verify
    # The non-SUCCESS path must be a hard rejection (non-2xx), never a soft pass.
    m = re.search(
        r'status !== "SUCCESS"[^{]*\{\s*\{[^}]*return json\(\{ok:false[^}]*\},(\d+)\)',
        causal_verify,
    )
    assert m and int(m.group(1)) >= 400, "non-SUCCESS receipts must fail closed (4xx)"


# ---------------------------------------------------------------------------
# Canonical fixture conforms
# ---------------------------------------------------------------------------

def test_receipt_fixture_conforms_to_spec():
    spec = load_spec()
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    cvo = fixture["causal_verification"]
    assert cvo["schema"] == CVO_SCHEMA
    assert cvo["causal_assessment"] in spec["axes"]["causal_assessment"]["enum"]
    assert cvo["verification_status"] in spec["axes"]["verification_status"]["enum"]
    assert cvo["observation"]["status"] in spec["axes"]["observation_status"]["observed_values"]
    assert cvo["authority"]["status"] in spec["axes"]["authority_status"]["observed_values"]
    assert isinstance(cvo["limitations"], list) and cvo["limitations"]


# ---------------------------------------------------------------------------
# Verify-mode fail-closed semantics (NOT_PROVEN default)
# ---------------------------------------------------------------------------

def test_verify_mode_declares_executor_claim_untrusted():
    """The executor's word alone never suffices — both verifiers say so."""
    for producer in PRODUCERS:
        source = producer.read_text(encoding="utf-8")
        assert "executor_claim_trusted:false" in source, (
            f"{producer.name}: verify path must declare executor_claim_trusted:false"
        )


def test_verify_mode_gates_validity_on_reread_evidence():
    """Both verifiers re-read persisted receipts and compute a `valid` boolean
    over evidence-derived checks; the HTTP status is gated on it (200 vs 409).
    nayanet-causal-verify re-validates the declared CVO against re-read
    receipts; nayanet-causal-learning-experiment fully recomputes the
    assessment. In both, the executor's declared value is never sufficient."""
    for producer in PRODUCERS:
        source = producer.read_text(encoding="utf-8")
        assert '.from("nayanet_execution_receipts")' in source, (
            f"{producer.name}: verify path must re-read persisted receipts"
        )
        assert re.search(r"valid\s*\?\s*200\s*:\s*409", source), (
            f"{producer.name}: verify-mode failure must return 409, not 2xx"
        )


def test_learning_experiment_publishes_recomputed_assessment():
    """The stronger property, where implemented: the verifier publishes its own
    recomputed assessment and requires declared == recomputed."""
    source = PRODUCERS[1].read_text(encoding="utf-8")
    assert "recomputed_causal_assessment" in source
    assert "declared_matches_recomputation" in source


def test_absent_cvo_is_not_proven_not_an_error_silenced():
    """No persisted causal_verification -> explicit 409, never a silent pass."""
    learning_experiment = PRODUCERS[1].read_text(encoding="utf-8")
    assert "CVO_NOT_PERSISTED" in learning_experiment


# ---------------------------------------------------------------------------
# 2. Spec-derived validator + negative controls (the check can disagree)
# ---------------------------------------------------------------------------

def validate_cvo(cvo: dict, spec: dict) -> tuple[bool, list[str]]:
    """Conformance predicate straight from the spec. Returns (accepted, reasons)."""
    reasons: list[str] = []
    if not isinstance(cvo, dict):
        return False, ["not an object"]
    if cvo.get("schema") != CVO_SCHEMA:
        reasons.append(f"schema != {CVO_SCHEMA}")
    axes = spec["axes"]
    if cvo.get("causal_assessment") not in axes["causal_assessment"]["enum"]:
        reasons.append(f"causal_assessment {cvo.get('causal_assessment')!r} not in spec enum")
    if cvo.get("verification_status") not in axes["verification_status"]["enum"]:
        reasons.append(f"verification_status {cvo.get('verification_status')!r} not in spec enum")
    obs = cvo.get("observation") or {}
    if obs.get("status") not in axes["observation_status"]["observed_values"]:
        reasons.append(f"observation.status {obs.get('status')!r} not in spec values")
    auth = cvo.get("authority") or {}
    if auth.get("status") not in axes["authority_status"]["observed_values"]:
        reasons.append(f"authority.status {auth.get('status')!r} not in spec values")
    # Independence: an executor-declared-only CVO never exits NOT_PROVEN.
    method = str(cvo.get("verification_method") or "")
    recomputed = "recomputed_causal_assessment" in cvo
    if method.startswith("executor-declared") and not recomputed:
        reasons.append("executor-declared without independent recomputation -> NOT_PROVEN")
    # Contradictory verdict: verified status with an unsupported assessment.
    if (
        cvo.get("verification_status") == "OUTCOME_VERIFIED"
        and cvo.get("causal_assessment") == "CAUSAL_NOT_SUPPORTED"
    ):
        reasons.append("OUTCOME_VERIFIED contradicts CAUSAL_NOT_SUPPORTED")
    if not isinstance(cvo.get("limitations"), list) or not cvo.get("limitations"):
        reasons.append("limitations missing (bounded-claim honesty required)")
    return (not reasons), reasons


def canonical_cvo() -> dict:
    return {
        "schema": CVO_SCHEMA,
        "causal_assessment": "CAUSAL_SUPPORTED",
        "verification_status": "OUTCOME_VERIFIED",
        "observation": {"result": "x", "status": "SUCCESS"},
        "authority": {"status": "AUTHORIZED"},
        "verification_method": "independent-runtime-reverification",
        "recomputed_causal_assessment": "CAUSAL_SUPPORTED",
        "limitations": ["bounded paired experiment"],
    }


def test_validator_accepts_canonical_cvo():
    ok, reasons = validate_cvo(canonical_cvo(), load_spec())
    assert ok, f"canonical CVO rejected: {reasons}"


def test_validator_rejects_unknown_causal_assessment():
    bad = canonical_cvo()
    bad["causal_assessment"] = "CAUSAL_MAYBE"
    ok, reasons = validate_cvo(bad, load_spec())
    assert not ok, "validator accepted an unknown causal_assessment — the check cannot disagree"
    assert any("causal_assessment" in r for r in reasons)


def test_validator_rejects_missing_verification_status():
    bad = canonical_cvo()
    del bad["verification_status"]
    ok, _ = validate_cvo(bad, load_spec())
    assert not ok, "validator accepted a CVO with no verification_status"


def test_validator_rejects_executor_declared_presented_as_verified():
    """The NOT_PROVEN core: an executor-declared CAUSAL_SUPPORTED with no
    independent recomputation must stay NOT_PROVEN, even though the declared
    value itself is a legal enum member."""
    bad = canonical_cvo()
    bad["verification_method"] = "executor-declared-cvo-pending-independent-runtime-reverification"
    del bad["recomputed_causal_assessment"]
    ok, reasons = validate_cvo(bad, load_spec())
    assert not ok, "validator let an executor-declared claim exit NOT_PROVEN"
    assert any("NOT_PROVEN" in r for r in reasons)


def test_validator_rejects_contradictory_verdict():
    bad = canonical_cvo()
    bad["causal_assessment"] = "CAUSAL_NOT_SUPPORTED"
    ok, reasons = validate_cvo(bad, load_spec())
    assert not ok, "validator accepted OUTCOME_VERIFIED + CAUSAL_NOT_SUPPORTED"
    assert any("contradicts" in r for r in reasons)


def test_validator_rejects_missing_limitations():
    bad = canonical_cvo()
    bad["limitations"] = []
    ok, _ = validate_cvo(bad, load_spec())
    assert not ok, "validator accepted a CVO with no limitations"
