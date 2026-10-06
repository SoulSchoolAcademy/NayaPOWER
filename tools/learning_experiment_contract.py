"""Machine-checkable pre-registration gate for NayaPOWER causal-learning experiments.

This validates experiment DESIGN only. It never claims that learning occurred.
A passing manifest means the experiment is hard enough and pre-registered
enough to run without quietly changing the answer key after seeing outcomes.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose, isfinite
import re
from typing import Any

REQUIRED_ARMS = {"CONTROL", "TREATMENT", "WRONG_LESSON"}
REQUIRED_WEIGHTS = {"accuracy", "diagnostic_order", "cost", "consistency", "negative_transfer_guard"}


@dataclass(frozen=True)
class ContractResult:
    ok: bool
    errors: tuple[str, ...]


def validate_round2_manifest(manifest: dict[str, Any]) -> ContractResult:
    if not isinstance(manifest, dict):
        return ContractResult(ok=False, errors=("MANIFEST_MUST_BE_OBJECT",))
    errors: list[str] = []

    if manifest.get("schema") != "NAYAPOWER_LEARNING_COMPOUNDING_EXPERIMENT_V2":
        errors.append("SCHEMA_MISMATCH")

    status = str(manifest.get("status", ""))
    if status != "PREREGISTERED":
        errors.append("STATUS_MUST_BE_PREREGISTERED")

    arms = manifest.get("arms")
    if not isinstance(arms, list):
        errors.append("ARMS_REQUIRED")
        arms = []
    arm_names = [a.get("name") if isinstance(a, dict) else None for a in arms]
    if (len(arm_names) != len(REQUIRED_ARMS)
            or any(not isinstance(name, str) for name in arm_names)
            or set(arm_names) != REQUIRED_ARMS):
        errors.append("EXACT_ABC_ARMS_REQUIRED")

    min_trials = manifest.get("minimum_trials_per_arm")
    if type(min_trials) is not int or min_trials < 5:
        errors.append("MINIMUM_FIVE_TRIALS_PER_ARM")

    negative_transfer = manifest.get("negative_transfer")
    if not isinstance(negative_transfer, dict):
        errors.append("NEGATIVE_TRANSFER_PLAN_REQUIRED")
    else:
        if negative_transfer.get("required") is not True:
            errors.append("NEGATIVE_TRANSFER_MUST_BE_REQUIRED")
        nt_trials = negative_transfer.get("minimum_trials")
        if type(nt_trials) is not int or nt_trials < 5:
            errors.append("MINIMUM_FIVE_NEGATIVE_TRANSFER_TRIALS")

    scoring = manifest.get("scoring")
    if not isinstance(scoring, dict):
        errors.append("SCORING_REQUIRED")
    else:
        weights = scoring.get("weights")
        if not isinstance(weights, dict) or set(weights) != REQUIRED_WEIGHTS:
            errors.append("SCORING_WEIGHTS_INCOMPLETE")
        else:
            values = [weights[k] for k in REQUIRED_WEIGHTS]
            if any(type(v) not in (int, float) for v in values):
                errors.append("SCORING_WEIGHTS_NON_NUMERIC")
            else:
                # Range checks also reject NaN/Infinity and avoid converting
                # unbounded integers to floats before they can be rejected.
                if any(not 0 <= v <= 1 or not isfinite(v) for v in values):
                    errors.append("SCORING_WEIGHTS_MUST_BE_FINITE_NONNEGATIVE")
                elif not isclose(sum(values), 1.0, rel_tol=0.0, abs_tol=1e-9):
                    errors.append("SCORING_WEIGHTS_MUST_SUM_TO_ONE")
        if scoring.get("negative_transfer_is_hard_gate") is not True:
            errors.append("NEGATIVE_TRANSFER_HARD_GATE_REQUIRED")

    answer_key = manifest.get("answer_key")
    if not isinstance(answer_key, dict):
        errors.append("ANSWER_KEY_PLAN_REQUIRED")
    else:
        if answer_key.get("prevalidated_before_trials") is not True:
            errors.append("ANSWER_KEY_PREVALIDATION_REQUIRED")
        builder_value = answer_key.get("builder")
        verifier_value = answer_key.get("independent_verifier")
        builder = builder_value.strip() if isinstance(builder_value, str) else ""
        verifier = verifier_value.strip() if isinstance(verifier_value, str) else ""
        if not builder or not verifier:
            errors.append("BUILDER_AND_VERIFIER_REQUIRED")
        elif builder == verifier:
            errors.append("ANSWER_KEY_VERIFIER_MUST_BE_INDEPENDENT")
        fixture_shas = answer_key.get("fixture_shas")
        if not isinstance(fixture_shas, list) or not fixture_shas:
            errors.append("FIXTURE_SHAS_REQUIRED")
        elif any(not isinstance(x, str) or re.fullmatch(r"[0-9a-fA-F]{40}", x) is None
                 for x in fixture_shas):
            errors.append("FIXTURE_SHA_MUST_BE_40_HEX")

    evidence = manifest.get("evidence_capture")
    if not isinstance(evidence, dict):
        errors.append("EVIDENCE_CAPTURE_REQUIRED")
    else:
        if evidence.get("raw_transcripts_required") is not True:
            errors.append("RAW_TRANSCRIPTS_REQUIRED")
        if evidence.get("exact_tool_call_counts_required") is not True:
            errors.append("EXACT_TOOL_CALL_COUNTS_REQUIRED")
        if evidence.get("immutable_fixture_binding_required") is not True:
            errors.append("IMMUTABLE_FIXTURE_BINDING_REQUIRED")

    hypotheses = manifest.get("hypotheses")
    if (not isinstance(hypotheses, list) or len(hypotheses) < 4
            or any(not isinstance(h, str) or not h.strip() for h in hypotheses)
            or len({h.strip() for h in hypotheses}) < 4):
        errors.append("FOUR_HYPOTHESES_REQUIRED")

    # Pre-registration is invalid if it already contains observed outcomes.
    forbidden = {"results", "observed_scores", "winner", "causal_verdict"}
    leaked = sorted(k for k in forbidden if k in manifest)
    if leaked:
        errors.append("OUTCOME_LEAKAGE_BEFORE_TRIALS:" + ",".join(leaked))

    return ContractResult(ok=not errors, errors=tuple(errors))
