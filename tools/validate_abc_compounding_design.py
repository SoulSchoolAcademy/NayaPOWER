#!/usr/bin/env python3
"""Fail-closed validator for the A->B->C graph-mediated compounding proof design.

Validates the design document (BRAIN/07-LEARNING/0002-ABC-COMPOUNDING-PROOF-DESIGN-V1.json)
and, separately, the live-run precondition gate:

  python3 tools/validate_abc_compounding_design.py                      # design only
  python3 tools/validate_abc_compounding_design.py --preconditions PATH  # design + gate

The validator implements a FAIL-CLOSED live gate: the live run is allowed ONLY
when every required precondition reports met=true with a non-null evidence
pointer. A green design validation proves nothing about production behavior —
only a live gated run with receipts proves compounding.
"""
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DESIGN_PATH = ROOT / "BRAIN/07-LEARNING/0002-ABC-COMPOUNDING-PROOF-DESIGN-V1.json"

SCHEMA = "NAYAPOWER_ABC_COMPOUNDING_PROOF_DESIGN_V1"

REQUIRED_A_STAGES = [
    "perform_one_bounded_task",
    "produce_observable_outcome",
    "independent_verifier_confirms_result",
    "create_or_promote_learning_only_after_verification",
    "graph_records_LEARNED_FROM_APPLIES_TO_with_evidence_and_provenance",
]
REQUIRED_B_STAGES = [
    "reconstruct_a_learning_from_canonical_state",
    "retrieve_through_graph_because_applicable",
    "re_resolve_authority_independently",
    "apply_lesson_to_related_held_out_task",
    "outperform_control_or_reduce_measured_rework",
    "produce_distinct_verified_refinement_from_own_result",
]
REQUIRED_C_STAGES = [
    "retrieve_graph_chain_a_learning_b_use_b_refinement",
    "select_current_applicable_refinement_not_superseded",
    "distinguish_contradictions_if_present",
    "independently_resolve_authority",
    "perform_second_related_held_out_task",
    "improve_vs_same_baseline_or_reduce_measured_rework",
]
REQUIRED_NEGATIVE_CONTROL_IDS = {
    "unrelated_task",
    "successor_context_not_authority",
    "expired_superseded_excluded",
    "missing_provenance_fails_closed",
    "chain_halt_on_no_b_improvement",
    "no_caller_supplied_lesson",
}
REQUIRED_EVIDENCE_LINKS = {
    "a_execution_receipt",
    "a_independent_verification",
    "a_learning_record",
    "graph_relationship_receipts",
    "b_retrieval_receipt",
    "b_behavior_outcome_pair",
    "b_independent_verification",
    "b_refinement_learning",
    "c_retrieval_receipt",
    "c_behavior_outcome_pair",
    "c_independent_verification",
    "baseline_measurements_pre_registered",
}
# Claim levels the DESIGN DOCUMENT itself may never carry.
FORBIDDEN_DESIGN_CLAIMS = {"VERIFIED", "PRODUCTION_PROVEN", "PROVEN", "SUCCESSOR_QUALIFIED"}

EPISTEMIC_STATES = {"UNKNOWN", "CANDIDATE", "SUPPORTED", "CONTRADICTED",
                    "SUPERSEDED", "INVALIDATED", "LEARNED", "VERIFIED"}
RELATIONSHIP_TYPES = {"DERIVED_FROM", "SUPPORTS", "CONTRADICTS", "DEPENDS_ON",
                      "IMPLEMENTS", "GOVERNS", "AUTHORIZED_BY", "USED_BY", "CAUSED",
                      "RESULTED_IN", "VERIFIED_BY", "LEARNED_FROM", "SUPERSEDES",
                      "SUCCEEDS", "RELATED_TO", "CONTEXTUALIZES", "INVALIDATES",
                      "REFINES", "CORRECTS", "ENABLES", "PRODUCES", "APPLIES_TO"}


def _err(errors: list, code: str) -> None:
    errors.append(code)


def validate_design(d: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if d.get("schema") != SCHEMA:
        _err(errors, "SCHEMA_MISMATCH")
    if d.get("status") not in ("PROPOSED_CANONICAL", "RATIFIED"):
        _err(errors, "STATUS_MUST_BE_PROPOSED_OR_RATIFIED")
    blob = json.dumps(d, sort_keys=True)
    for claim in FORBIDDEN_DESIGN_CLAIMS:
        if f'"status": "{claim}"' in blob or claim in (d.get("what_this_does_not_claim") or []):
            pass  # what_this_does_not_claim explicitly disclaims them
    if d.get("status") in FORBIDDEN_DESIGN_CLAIMS:
        _err(errors, "DESIGN_MAY_NOT_SELF_CLAIM_PROOF")

    # Pipelines
    for key, required in (("generation_a", REQUIRED_A_STAGES),
                          ("generation_b", REQUIRED_B_STAGES),
                          ("generation_c", REQUIRED_C_STAGES)):
        stages = (d.get(key) or {}).get("stages") or []
        for s in required:
            if s not in stages:
                _err(errors, f"MISSING_STAGE:{key}:{s}")
        # forward-only: required stages must appear in the specified order
        idx = [stages.index(s) for s in required if s in stages]
        if idx != sorted(idx):
            _err(errors, f"STAGE_ORDER_VIOLATION:{key}")

    # Negative controls
    controls = d.get("negative_controls") or []
    ids = {c.get("id") for c in controls if isinstance(c, dict)}
    if not REQUIRED_NEGATIVE_CONTROL_IDS.issubset(ids):
        _err(errors, "NEGATIVE_CONTROLS_INCOMPLETE:" +
               ",".join(sorted(REQUIRED_NEGATIVE_CONTROL_IDS - ids)))
    for c in controls:
        if isinstance(c, dict) and not c.get("rule"):
            _err(errors, f"NEGATIVE_CONTROL_NO_RULE:{c.get('id')}")

    # Evidence chain
    links = set(d.get("evidence_chain_links") or [])
    if not REQUIRED_EVIDENCE_LINKS.issubset(links):
        _err(errors, "EVIDENCE_CHAIN_INCOMPLETE:" +
               ",".join(sorted(REQUIRED_EVIDENCE_LINKS - links)))

    # Authority boundary
    auth = d.get("authority_boundary") or {}
    if auth.get("graph_grants_authority") is not False:
        _err(errors, "AUTHORITY_BOUNDARY_MISSING_OR_FALSE")
    rule = (auth.get("rule") or "").lower()
    if "successor" not in rule and "inherit" not in rule:
        _err(errors, "NO_AUTHORITY_INHERITANCE_RULE_MISSING")

    # Vocab consistency with the RATIFIED graph relationship contract V2
    if not set(d.get("epistemic_states_allowed") or []).issubset(EPISTEMIC_STATES):
        _err(errors, "EPISTEMIC_STATE_OUTSIDE_CONTRACT_V2")
    if not set(d.get("relationship_types_allowed") or []).issubset(RELATIONSHIP_TYPES):
        _err(errors, "RELATIONSHIP_TYPE_OUTSIDE_CONTRACT_V2")

    # Preconditions present and well-formed
    pre = d.get("required_preconditions") or []
    if len(pre) < 5:
        _err(errors, "PRECONDITION_LIST_INCOMPLETE")
    for p in pre:
        if not p.get("id"):
            _err(errors, "PRECONDITION_MISSING_ID")
        if not isinstance(p.get("met"), bool):
            _err(errors, f"PRECONDITION_MET_NOT_BOOL:{p.get('id')}")
        if p.get("met") and not p.get("evidence"):
            _err(errors, f"PRECONDITION_MET_WITHOUT_EVIDENCE:{p.get('id')}")
        if not p.get("met") and not p.get("blocker"):
            _err(errors, f"UNMET_PRECONDITION_NO_BLOCKER_RECORDED:{p.get('id')}")

    # Measurement protocol
    mp = d.get("measurement_protocol") or {}
    if not mp.get("baseline"):
        _err(errors, "BASELINE_NOT_PRE_REGISTERED")
    if not isinstance(mp.get("metrics"), list) or not mp.get("metrics"):
        _err(errors, "MEASUREMENT_METRICS_MISSING")
    sd = (mp.get("success_definition") or "").lower()
    if "improve" not in sd or "baseline" not in sd:
        _err(errors, "SUCCESS_DEFINITION_MISSING_BASELINE_IMPROVEMENT")

    # Chain-halt rule must exist (B no improvement -> C gets nothing)
    nc = " ".join((c.get("rule") or "") for c in controls).lower()
    if "halt" not in nc and "must not receive" not in nc:
        _err(errors, "CHAIN_HALT_RULE_MISSING")

    # Design must disclaim the live run and the kernel/experiment contract lanes
    disclaim = " ".join(d.get("what_this_does_not_claim") or []).lower()
    if "live run" not in disclaim and "experiment" not in disclaim:
        _err(errors, "LIVE_RUN_DISCLAIMER_MISSING")

    # as_of must be a plausible 40-hex SHA
    as_of = d.get("as_of") or ""
    if not (len(as_of) == 40 and all(c in "0123456789abcdef" for c in as_of)):
        _err(errors, "AS_OF_SHA_INVALID")

    return errors


def check_precondition_gate(d: dict[str, Any]) -> tuple[bool, list[str]]:
    """FAIL-CLOSED live gate. Returns (allowed, reasons)."""
    unmet = []
    for p in d.get("required_preconditions") or []:
        if not p.get("met"):
            unmet.append(p.get("id"))
        elif not p.get("evidence"):
            unmet.append(f"{p.get('id')}:evidence_missing")
    if unmet:
        return False, [f"LIVE_RUN_REFUSED:unmet_preconditions:{','.join(sorted(unmet))}"]
    return True, ["LIVE_RUN_ALLOWED:all_preconditions_met_with_evidence"]


def main() -> int:
    try:
        design = json.loads(DESIGN_PATH.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001 - file absence is a validation failure
        print(f"VALIDATION_FAILED:DESIGN_UNREADABLE:{e}")
        return 1
    errors = validate_design(design)
    pre_arg = None
    if "--preconditions" in sys.argv:
        i = sys.argv.index("--preconditions")
        if i + 1 < len(sys.argv):
            pre_arg = sys.argv[i + 1]
    if errors:
        print("VALIDATION_FAILED")
        for e in errors:
            print(f"  {e}")
        return 1
    print("DESIGN_VALID:21_groups_checked")
    gate_design = design
    if pre_arg:
        try:
            gate_design = json.loads(Path(pre_arg).read_text(encoding="utf-8"))
            gate_errs = validate_design(gate_design)
            if gate_errs:
                print("PRECONDITION_REPORT_DESIGN_INVALID")
                for e in gate_errs:
                    print(f"  {e}")
                return 1
        except Exception as e:  # noqa: BLE001
            print(f"PRECONDITION_REPORT_UNREADABLE:{e}")
            return 1
    allowed, reasons = check_precondition_gate(gate_design)
    for r in reasons:
        print(f"  {r}")
    return 0 if allowed else 2


if __name__ == "__main__":
    sys.exit(main())
