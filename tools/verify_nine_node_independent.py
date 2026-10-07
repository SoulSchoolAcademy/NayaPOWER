#!/usr/bin/env python3
"""Independent recomputation for the final nine-node behavioral acceptance claim.

This verifier deliberately does not accept the executor's independent_verification
field as evidence. It reconstructs the graph proof from the raw persisted control/treatment
receipts and relationship rows, validates the remaining component artifacts and lineage,
requires a fresh verifier identity, and fails closed when required evidence is missing,
mutated, or out of lineage.
"""

from __future__ import annotations

from typing import Any


ORDER = ["SELF", "LAW", "ACT", "KNOW", "PROVE", "CONNECT", "VERIFY", "LEARN", "EVOLVE"]
REQUIRED = ("executor", "cold", "graph", "graph_verify", "promotion", "reread", "evolve")


def _nonempty(value: Any) -> bool:
    return value is not None and value != ""


def _same(a: Any, b: Any) -> bool:
    return a == b


def verify_bundle(
    bundle: dict[str, Any],
    *,
    verifier_jti: str,
    expected_source_revision: str | None = None,
) -> dict[str, Any]:
    errors: list[str] = []

    missing = [name for name in REQUIRED if not isinstance(bundle.get(name), dict)]
    if missing:
        errors.extend(missing)

    executor = bundle.get("executor") or {}
    cold = bundle.get("cold") or {}
    graph = bundle.get("graph") or {}
    graph_verify = bundle.get("graph_verify") or {}
    promotion = bundle.get("promotion") or {}
    reread = bundle.get("reread") or {}
    evolve = bundle.get("evolve") or {}

    executor_jti = str(executor.get("token_jti") or "")
    verifier_jti = str(verifier_jti or "")

    if not executor_jti or not verifier_jti or executor_jti == verifier_jti:
        errors.append("verifier_identity")

    source_revision = str(expected_source_revision or executor.get("source_revision") or "")
    source_bindings = {
        "executor": executor.get("source_revision"),
        "cold": cold.get("deployed_source_revision"),
        "graph": graph.get("source_revision"),
        "graph_verify": graph_verify.get("source_revision"),
        "promotion": promotion.get("source_revision"),
        "reread": reread.get("source_revision"),
        "evolve": evolve.get("source_revision"),
    }
    source_bindings_complete = bool(source_revision) and all(_nonempty(v) for v in source_bindings.values())
    source_revision_consistent = source_bindings_complete and all(
        str(v) == source_revision for v in source_bindings.values()
    )
    if expected_source_revision and source_revision != str(expected_source_revision):
        source_revision_consistent = False
    if not source_bindings_complete:
        errors.append("source_revision_missing")
    if not source_revision_consistent:
        errors.append("source_revision_consistency")

    cold_receipt = cold.get("receipt") or {}
    cold_executor_jti = str(cold_receipt.get("token_jti") or "")
    executor_identity_bound = bool(executor_jti) and cold_executor_jti == executor_jti
    if not executor_identity_bound:
        errors.append("executor_identity_binding")
    self_ok = (
        cold.get("deployed_source_revision") == executor.get("source_revision")
        and cold_receipt.get("naya_id") == "NAYA-NODE-0001"
        and _nonempty(cold_receipt.get("owner_id"))
        and cold_receipt.get("runtime_identity") == "github-actions-oidc"
        and _nonempty(cold_receipt.get("workflow_ref"))
        and executor_identity_bound
    )
    if not self_ok:
        errors.append("self_evidence")

    graph_control = graph.get("control") or {}
    graph_treatment = graph.get("treatment") or {}
    delta = graph.get("behavioral_delta") or {}
    act_ok = (
        _nonempty(graph_control.get("receipt_id"))
        and _nonempty(graph_treatment.get("receipt_id"))
        and graph_control.get("receipt_id") != graph_treatment.get("receipt_id")
        and _nonempty(graph_control.get("behavior"))
        and _nonempty(graph_treatment.get("behavior"))
        and graph_control.get("behavior") != graph_treatment.get("behavior")
        and delta.get("changed") is True
    )
    if not act_ok:
        errors.append("behavioral_delta")

    graph_verification = graph_verify.get("verification") or {}
    raw_receipts = graph_verify.get("receipts") or {}
    raw_control = raw_receipts.get("control") or {}
    raw_treatment = raw_receipts.get("treatment") or {}
    raw_relationships = graph_verify.get("relationships") or []
    raw_control_evidence = raw_control.get("evidence") or {}
    raw_treatment_evidence = raw_treatment.get("evidence") or {}
    selected_relationship_ids = {
        str(item.get("relationship_id") or "")
        for item in raw_treatment_evidence.get("selected_relationships") or []
        if isinstance(item, dict) and _nonempty(item.get("relationship_id"))
    }
    paired_ids_match = (
        raw_control.get("id") == graph_control.get("receipt_id")
        and raw_treatment.get("id") == graph_treatment.get("receipt_id")
        and raw_control.get("id") != raw_treatment.get("id")
    )
    raw_graph_conditions_ok = (
        raw_control_evidence.get("condition") == "OFF"
        and raw_control_evidence.get("relationship_context_enabled") is False
        and raw_treatment_evidence.get("condition") == "ON"
        and raw_treatment_evidence.get("relationship_context_enabled") is True
        and raw_control_evidence.get("task_id") == raw_treatment_evidence.get("task_id")
        and _nonempty(raw_control_evidence.get("task_id"))
        and raw_control_evidence.get("task_class") == raw_treatment_evidence.get("task_class")
        and _nonempty(raw_control_evidence.get("task_class"))
        and raw_control_evidence.get("intelligent_block_id") == raw_treatment_evidence.get("intelligent_block_id")
        and _nonempty(raw_control_evidence.get("intelligent_block_id"))
    )
    raw_behavioral_delta = (
        _nonempty(raw_control.get("observed_result"))
        and _nonempty(raw_treatment.get("observed_result"))
        and raw_control.get("observed_result") != raw_treatment.get("observed_result")
    )
    eligible_relationships = [
        row for row in raw_relationships
        if isinstance(row, dict)
        and row.get("relationship_id") in selected_relationship_ids
        and row.get("target_id") == raw_treatment_evidence.get("intelligent_block_id")
        and row.get("relationship_type") == "VERIFIED_BY"
        and row.get("epistemic_state") == "VERIFIED"
        and row.get("status") == "ACTIVE"
        and _nonempty(row.get("provenance"))
        and _nonempty(row.get("evidence_refs"))
        and isinstance(row.get("applicability"), dict)
        and row["applicability"].get("state") == "APPLICABLE"
        and raw_treatment_evidence.get("task_class") in (row["applicability"].get("task_classes") or [])
    ]
    raw_graph_evidence_ok = (
        paired_ids_match
        and raw_graph_conditions_ok
        and raw_behavioral_delta
        and bool(selected_relationship_ids)
        and len(eligible_relationships) == len(selected_relationship_ids)
    )
    if not raw_graph_evidence_ok:
        errors.append("graph_raw_evidence")

    prove_ok = (
        raw_graph_evidence_ok
        and graph_verification.get("persisted_pair_re_read") is True
    )
    if not prove_ok:
        errors.append("graph_reconstruction")

    promotion_result = promotion.get("result") or {}
    promotion_learning = promotion_result.get("learning") or {}
    promotion_verification = promotion.get("verification_record") or {}
    promotion_integration = promotion.get("integration") or {}
    reread_learning = reread.get("learning") or {}
    reread_integration = reread.get("integration") or {}

    learning_ok = (
        _nonempty(promotion_learning.get("id"))
        and promotion_learning.get("status") == "ACTIVE"
        and promotion_verification.get("verified") is True
        and promotion_integration.get("progressive_intelligence_lock_in") is True
    )
    if not learning_ok:
        errors.append("learning_verification")

    learning_lineage_ok = (
        promotion_learning.get("id") == reread_learning.get("id")
        and reread_learning.get("status") == "ACTIVE"
        and reread.get("independent_reread") is True
        and reread_integration.get("intelligent_block_state") == "LEARNED"
    )
    if not learning_lineage_ok:
        errors.append("learning_lineage")

    evolve_related = evolve.get("related_task") or {}
    evolve_unrelated = evolve.get("unrelated_task") or {}
    unrelated_refusal_ok = evolve_unrelated.get("correct_refusal") is True
    if not unrelated_refusal_ok:
        errors.append("unrelated_refusal")

    evolve_ok = (
        evolve.get("independent_verification") is True
        and evolve.get("authority_inherited") is False
        and _nonempty(evolve_related.get("task_id"))
        and _nonempty(evolve_related.get("behavior"))
        and _nonempty(evolve_unrelated.get("task_id"))
    )
    if not evolve_ok:
        errors.append("evolve_evidence")

    authority_noninheritance_ok = evolve.get("authority_inherited") is False
    if not authority_noninheritance_ok:
        errors.append("authority_noninheritance")

    evidence_refs = {
        "SELF": [
            "cold-runtime-1.json#receipt.naya_id",
            "cold-runtime-1.json#receipt.owner_id",
            "cold-runtime-1.json#receipt.runtime_identity",
            "cold-runtime-1.json#receipt.workflow_ref",
        ],
        "LAW": [
            "active-learning-generalization-successor-proof.json#authority_inherited",
            "active-learning-generalization-successor-proof.json#unrelated_task.correct_refusal",
        ],
        "ACT": [
            str(graph_control.get("receipt_id") or ""),
            str(graph_treatment.get("receipt_id") or ""),
        ],
        "KNOW": [
            str(reread_learning.get("id") or ""),
            "retained-learning-reread.json#integration.intelligent_block_state",
        ],
        "PROVE": [
            "cold-graph-independent-verification.json#verification.persisted_pair_re_read",
            "cold-graph-independent-verification.json#verification.treatment_relationships_verified",
        ],
        "CONNECT": [
            "cold-graph-behavior-pair.json#control.receipt_id",
            "cold-graph-behavior-pair.json#treatment.receipt_id",
        ],
        "VERIFY": [
            "cold-graph-independent-verification.json#verification.independently_reconstructed",
            "active-learning-generalization-successor-proof.json#independent_verification",
        ],
        "LEARN": [
            str(promotion_learning.get("id") or ""),
            "learning-promotion.json#verification_record.verified",
        ],
        "EVOLVE": [
            str(evolve_related.get("task_id") or ""),
            str(evolve_unrelated.get("task_id") or ""),
        ],
    }

    for node in ORDER:
        if any(not _nonempty(ref) for ref in evidence_refs[node]):
            errors.append(f"{node.lower()}_evidence_refs")

    recomputed = {
        "verification_basis": "INDEPENDENT_COMPONENT_RECOMPUTATION",
        "source_revision_consistent": source_revision_consistent,
        "self_evidence": self_ok,
        "behavioral_delta_present": act_ok,
        "graph_reconstruction": prove_ok,
        "learning_verified": learning_ok,
        "learning_lineage": learning_lineage_ok,
        "evolve_evidence": evolve_ok,
        "authority_noninheritance": authority_noninheritance_ok,
        "node_order": ORDER,
    }

    # Never read executor["independent_verification"] as an input to the verdict.
    passed = not errors and verifier_jti != executor_jti and bool(verifier_jti)

    return {
        "ok": passed,
        "independent_verification": passed,
        "executor_claim_trusted": False,
        "executor_runtime_jti": executor_jti,
        "verifier_runtime_jti": verifier_jti,
        "evidence_refs": evidence_refs,
        "recomputed": recomputed,
        "errors": errors,
    }


def main() -> int:
    import argparse
    import json
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", required=True)
    parser.add_argument("--verifier-jti", required=True)
    parser.add_argument("--expected-source-revision", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    bundle = json.loads(Path(args.bundle).read_text(encoding="utf-8"))
    result = verify_bundle(
        bundle,
        verifier_jti=args.verifier_jti,
        expected_source_revision=args.expected_source_revision,
    )
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
