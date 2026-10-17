"""Smart App freeze lock for kernel/value_calculus.py v1.0.0.

This is the MECHANICAL form of the freeze: the Smart App contract is locked
at v1.0.0. Additive changes are allowed (new optional parameters, new
functions, new optional constants). Breaking changes are NOT allowed:

- removing or renaming a frozen public function or class,
- changing the required parameters of a frozen public function,
- removing a frozen optional parameter name,
- changing SMART_APP_ID, ENGINE_VERSION, or the frozen constant set,
- non-deterministic behavior.

Any breaking change ships as a NEW major Smart App version, never a silent
edit. Red: keep the freeze honest. Green: the contract holds.
"""

import inspect
import json

import kernel.value_calculus as vc

FROZEN = {
    "functions": {
        "build_contribution_receipt": {
            "required": [
                "contribution_id",
                "action_class",
                "provenance",
                "privacy",
                "raw_activity",
                "quality",
                "relevance",
                "verification_strength",
                "impact",
                "novelty",
                "verified_delta",
                "scoring_profile_id",
                "scoring_profile_version",
                "points_per_unit",
                "repeat_decay",
                "evidence_refs",
                "explanation"
            ],
            "optional": [
                "verification"
            ]
        },
        "build_decision_receipt": {
            "required": [
                "decision_id",
                "objective",
                "baseline_id",
                "stakeholders",
                "horizon",
                "evaluation",
                "authority_basis",
                "evidence_refs",
                "observation_window",
                "verification"
            ],
            "optional": [
                "delta_v_actual"
            ]
        },
        "build_recalibration_receipt": {
            "required": [
                "current_profile",
                "proposed_version",
                "records"
            ],
            "optional": [
                "proposed_priorities",
                "proposed_thresholds",
                "evidence_refs"
            ]
        },
        "calibration_summary": {
            "required": [
                "records"
            ],
            "optional": []
        },
        "combine_next_best_action_score": {
            "required": [
                "candidate",
                "profile"
            ],
            "optional": []
        },
        "consequential_use_eligible": {
            "required": [
                "request",
                "profile"
            ],
            "optional": []
        },
        "conservative_value": {
            "required": [
                "candidate",
                "baseline",
                "profile"
            ],
            "optional": []
        },
        "contribution_points": {
            "required": [
                "cvs",
                "points_per_unit"
            ],
            "optional": [
                "repeat_decay"
            ]
        },
        "contribution_value_score": {
            "required": [
                "quality",
                "relevance",
                "verification",
                "impact",
                "novelty",
                "verified_delta"
            ],
            "optional": []
        },
        "delta_value": {
            "required": [
                "candidate",
                "baseline",
                "profile"
            ],
            "optional": []
        },
        "evaluate_candidates": {
            "required": [
                "candidates",
                "baseline_id",
                "profile"
            ],
            "optional": [
                "risk_policy"
            ]
        },
        "gate_candidate": {
            "required": [
                "candidate",
                "profile",
                "risk_policy"
            ],
            "optional": []
        },
        "independent_recompute": {
            "required": [
                "receipt",
                "candidates",
                "profile"
            ],
            "optional": [
                "risk_policy"
            ]
        },
        "interval_gap": {
            "required": [
                "first",
                "second"
            ],
            "optional": []
        },
        "pareto_frontier": {
            "required": [
                "rows"
            ],
            "optional": []
        },
        "promote_recalibration": {
            "required": [
                "receipt",
                "current_profile",
                "verified",
                "authorized"
            ],
            "optional": []
        },
        "rank_next_best_actions": {
            "required": [
                "candidates"
            ],
            "optional": [
                "profile"
            ]
        },
        "relative_margin": {
            "required": [
                "first",
                "second"
            ],
            "optional": [
                "epsilon"
            ]
        },
        "retrieval_eligible": {
            "required": [
                "request"
            ],
            "optional": []
        },
        "score_quality": {
            "required": [
                "candidate",
                "profile"
            ],
            "optional": []
        },
        "value_interval": {
            "required": [
                "candidate",
                "baseline",
                "profile"
            ],
            "optional": []
        },
        "verification_state": {
            "required": [
                "outcome_passed",
                "observation_window_closed",
                "delayed_harm_material"
            ],
            "optional": []
        }
    },
    "classes": [
        "Candidate",
        "NextBestActionCandidate",
        "NextBestActionProfile",
        "NextBestActionResult",
        "OperationRequest",
        "PVEstimate",
        "QualityProfile",
        "RiskPolicy",
        "TailRisk"
    ],
    "engine_version": "DECISION-VALUE-CALCULUS-V2.1",
    "smart_app_version": "1.0.0",
    "smart_app_id": "nayapower.decision-value-calculus"
}


def _params(fn):
    sig = inspect.signature(fn)
    req, opt = [], []
    for p, pr in sig.parameters.items():
        if pr.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue
        (req if pr.default is inspect.Parameter.empty else opt).append(p)
    return req, opt


def test_smart_app_version_stamps():
    assert vc.SMART_APP_ID == FROZEN["smart_app_id"] == "nayapower.decision-value-calculus"
    assert vc.SMART_APP_VERSION == FROZEN["smart_app_version"] == "1.0.0"
    assert vc.ENGINE_VERSION == FROZEN["engine_version"] == "DECISION-VALUE-CALCULUS-V2.1"


def test_frozen_classes_present():
    for name in FROZEN["classes"]:
        assert inspect.isclass(getattr(vc, name, None)), f"frozen class missing: {name}"


def test_frozen_functions_additive_only():
    for name, spec in FROZEN["functions"].items():
        fn = getattr(vc, name, None)
        assert inspect.isfunction(fn), f"frozen function missing: {name}"
        req, opt = _params(fn)
        # Required params: identical, in order. Rename/remove breaks the freeze.
        assert req == spec["required"], f"required params changed: {name}"
        # Optional params: may only GROW (superset). Remove/rename breaks the freeze.
        assert set(spec["optional"]) <= set(opt), f"optional params shrank: {name}"


def test_frozen_constant_set_intact():
    assert vc.QUALITY_DIMENSIONS == (
        "objective_fit", "evidence_sufficiency", "applicability",
        "robustness", "reversibility", "blast_containment", "simplicity",
    )
    assert set(vc.DEFAULT_QUALITY_PRIORITIES) == set(vc.QUALITY_DIMENSIONS)
    for name in ("PROHIBITED", "NEEDS_AUTHORITY", "NEEDS_EVIDENCE", "ADMISSIBLE",
                 "ACT", "READ_MORE", "ASK", "REFUSE"):
        assert isinstance(getattr(vc, name), str) and getattr(vc, name)


def _pv(B=8, H=0, C=1, R=0.2, conf=0.95, evidence_count=3):
    return vc.PVEstimate(B, H, C, R, {k: conf for k in ("B", "H", "C", "R")}, evidence_count)


def _quality(score=9.5, conf=0.95):
    dims = {d: score for d in vc.QUALITY_DIMENSIONS}
    return dims, {k: conf for k in dims}


def _cand(cid, *, baseline=False, B=8, score=9.5, conf=0.95):
    q, c = _quality(score, conf)
    return vc.Candidate(
        cid, q, c, _pv(B=B, conf=conf), authorized=True, reversible=True,
        human_authorized=False, is_baseline=baseline,
        lawful=True, rights_safe=True, privacy_safe=True, safety_safe=True,
    )


def _sample_decision():
    profile = vc.QualityProfile(
        profile_id="SMART-APP-FREEZE-SAMPLE",
        version="1.0.0",
        objective="prove the frozen contract is deterministic",
        min_evidence_count=2,
        relative_margin=0.10,
    )
    return profile, _cand("a", B=9, score=9.5), _cand("b", B=7, score=4.0)


def test_deterministic_evaluate_candidates():
    profile, a, b = _sample_decision()
    base = _cand("base", baseline=True, B=5, score=9.5)
    first = vc.evaluate_candidates([base, a, b], "base", profile)
    second = vc.evaluate_candidates([base, a, b], "base", profile)
    assert json.dumps(first, sort_keys=True, default=str) == \
        json.dumps(second, sort_keys=True, default=str)
    # the winner is genuinely the higher-quality candidate
    assert first["decision"] == vc.ACT
    assert first["selected"] == "a"


def test_score_and_gate_contract():
    profile, a, b = _sample_decision()
    scores = vc.score_quality(a, profile)
    assert "Q" in scores
    assert vc.score_quality(a, profile)["Q"] > vc.score_quality(b, profile)["Q"]
    verdict, reasons, detail = vc.gate_candidate(a, profile, vc.RiskPolicy())
    assert verdict in (vc.PROHIBITED, vc.NEEDS_AUTHORITY, vc.NEEDS_EVIDENCE, vc.ADMISSIBLE)
    assert isinstance(reasons, list) and isinstance(detail, dict)
