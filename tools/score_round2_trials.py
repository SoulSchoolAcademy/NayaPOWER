"""Score executed Round-2 trials against the frozen V2 rubric.

Design-only contract lives in tools.learning_experiment_contract;
fixture binding lives in tools.round2_manifest_bind. This module scores
EXECUTED trials. It never manufactures transcripts: every trial must carry
its raw transcript path and exact tool-call count, or the trial is VOID
(round-1 receipt gap: summaries without transcripts do not count).

Trial schema (dict):
  trial_id: str, arm: CONTROL|TREATMENT|WRONG_LESSON,
  negative_transfer: bool, verdict_correct: bool,
  cited_lesson: bool (retrieved AND cited the lesson),
  diagnostic_order: float 0..1, tool_call_count: int (>=0, exact),
  consistent: bool, transcript_path: str (non-empty)

Verdict:
  FAIL when any negative-transfer trial is wrong (hard gate), evidence is
  void/duplicated, any arm has fewer than five trials, or fewer than five
  negative-transfer trials exist. Transcript paths must resolve to readable,
  nonempty files relative to the current working directory.
  INCONCLUSIVE when control >= treatment accuracy (ceiling/adjacent
  knowledge, F3 class) or treatment wins without citation majority and
  without beating WRONG_LESSON (attribution failure, F2 class).
  PASS otherwise, with arm scores reported. PASS means the scored evidence
  meets the bar; it is not a learning claim by itself.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from tools.round2_manifest_bind import FROZEN_WEIGHTS

ARMS = ("CONTROL", "TREATMENT", "WRONG_LESSON")


@dataclass(frozen=True)
class TrialVerdict:
    verdict: str
    reasons: tuple[str, ...]
    arm_scores: dict[str, float]
    arm_accuracy: dict[str, float]
    cost_ratio_treatment_vs_control: float | None


def _validate_trial(trial: dict[str, Any]) -> str | None:
    """Return an error string when the trial is VOID, else None."""
    if not isinstance(trial, dict):
        return "VOID:trial must be an object"
    if trial.get("arm") not in ARMS:
        return "VOID:unknown arm"
    for key in (
        "trial_id",
        "negative_transfer",
        "verdict_correct",
        "cited_lesson",
        "diagnostic_order",
        "tool_call_count",
        "consistent",
        "transcript_path",
    ):
        if key not in trial:
            return f"VOID:missing {key}"
    if not isinstance(trial["trial_id"], str) or not trial["trial_id"].strip():
        return "VOID:trial_id must be a nonempty string"
    for key in ("verdict_correct", "cited_lesson", "consistent", "negative_transfer"):
        if type(trial[key]) is not bool:
            return f"VOID:{key} must be a boolean"
    order = trial["diagnostic_order"]
    if type(order) not in (int, float) or not 0.0 <= order <= 1.0:
        return "VOID:diagnostic_order outside 0..1"
    count = trial["tool_call_count"]
    if type(count) is not int or count < 0:
        return "VOID:tool_call_count must be an exact non-negative int"
    transcript = trial["transcript_path"]
    if not isinstance(transcript, str) or not transcript.strip():
        return "VOID:transcript_path empty (summaries do not count)"
    try:
        path = Path(transcript)
        if not path.is_file() or not path.read_bytes().strip():
            return "VOID:transcript must be a readable nonempty file"
    except (OSError, ValueError):
        return "VOID:transcript must be a readable nonempty file"
    return None


def score_trials(trials: Sequence[dict[str, Any]]) -> TrialVerdict:
    """Score trials with local transcript checks; raises ValueError on no valid trials.

    File presence is necessary, not proof of transcript authenticity, answer-key
    correctness, fixture binding or accurate reported tool counts. Independent
    recomputation remains required before making a learning claim.
    """
    valid: list[dict[str, Any]] = []
    voided: list[str] = []
    seen_ids: set[str] = set()
    for trial in trials:
        error = _validate_trial(trial)
        if not error:
            trial_id = trial["trial_id"].strip()
            if trial_id in seen_ids:
                error = "VOID:duplicate trial_id"
            else:
                seen_ids.add(trial_id)
        if error:
            trial_id = trial.get("trial_id", "?") if isinstance(trial, dict) else "?"
            voided.append(f"{trial_id}:{error}")
        else:
            valid.append(trial)
    if not valid:
        raise ValueError("NO_VALID_TRIALS:" + ";".join(voided))

    by_arm: dict[str, list[dict[str, Any]]] = {arm: [] for arm in ARMS}
    for trial in valid:
        by_arm[str(trial["arm"])].append(trial)

    reasons: list[str] = []
    if voided:
        reasons.append(f"{len(voided)} void trial(s): " + ";".join(voided[:5]))

    nt_failed = [
        t["trial_id"]
        for t in valid
        if t.get("negative_transfer") is True and t["verdict_correct"] is not True
    ]
    if nt_failed:
        return TrialVerdict(
            verdict="FAIL",
            reasons=tuple(
                reasons + [f"NT_HARD_GATE: {len(nt_failed)} flipped: {nt_failed[:5]}"]
            ),
            arm_scores={},
            arm_accuracy={},
            cost_ratio_treatment_vs_control=None,
        )

    missing = [arm for arm in ARMS if not by_arm[arm]]
    if missing:
        return TrialVerdict(
            verdict="FAIL",
            reasons=tuple(reasons + [f"MISSING_ARM:{','.join(missing)}"]),
            arm_scores={},
            arm_accuracy={},
            cost_ratio_treatment_vs_control=None,
        )

    # The executed battery must satisfy the same minimums as preregistration.
    # Invalid evidence is a failed gate, never a silently excluded observation.
    underpowered = [arm for arm in ARMS if len(by_arm[arm]) < 5]
    if underpowered:
        reasons.append("MINIMUM_FIVE_TRIALS_PER_ARM:" + ",".join(underpowered))
    nt_count = sum(t["negative_transfer"] for t in valid)
    if nt_count < 5:
        reasons.append("MINIMUM_FIVE_NEGATIVE_TRANSFER_TRIALS")
    if voided or underpowered or nt_count < 5:
        return TrialVerdict(
            verdict="FAIL",
            reasons=tuple(reasons),
            arm_scores={},
            arm_accuracy={},
            cost_ratio_treatment_vs_control=None,
        )

    def mean(items: list[dict[str, Any]], key: str) -> float:
        if key == "accuracy":
            return sum(1.0 if t["verdict_correct"] else 0.0 for t in items) / len(items)
        if key == "citation":
            return sum(1.0 if t["cited_lesson"] else 0.0 for t in items) / len(items)
        if key == "cost":
            return sum(float(t["tool_call_count"]) for t in items) / len(items)
        if key == "consistency":
            return sum(1.0 if t["consistent"] else 0.0 for t in items) / len(items)
        return sum(float(t[key]) for t in items) / len(items)

    arm_accuracy = {arm: mean(by_arm[arm], "accuracy") for arm in ARMS}
    control_mean_cost = mean(by_arm["CONTROL"], "cost")
    treatment_mean_cost = mean(by_arm["TREATMENT"], "cost")
    cost_ratio = (
        treatment_mean_cost / control_mean_cost if control_mean_cost > 0 else None
    )

    arm_scores = {}
    for arm in ARMS:
        items = by_arm[arm]
        cost_component = 1.0
        if arm == "TREATMENT" and cost_ratio is not None and cost_ratio > 1.3:
            cost_component = max(0.0, 1.0 - (cost_ratio - 1.3))
        arm_scores[arm] = (
            FROZEN_WEIGHTS["accuracy"] * mean(items, "accuracy")
            + FROZEN_WEIGHTS["diagnostic_order"] * mean(items, "diagnostic_order")
            + FROZEN_WEIGHTS["cost"] * cost_component
            + FROZEN_WEIGHTS["consistency"] * mean(items, "consistency")
            + FROZEN_WEIGHTS["negative_transfer_guard"] * 1.0
        )

    if arm_accuracy["CONTROL"] >= arm_accuracy["TREATMENT"]:
        return TrialVerdict(
            verdict="INCONCLUSIVE",
            reasons=tuple(
                reasons
                + [
                    f"CEILING: control {arm_accuracy['CONTROL']:.2f} >= "
                    f"treatment {arm_accuracy['TREATMENT']:.2f}"
                ]
            ),
            arm_scores=arm_scores,
            arm_accuracy=arm_accuracy,
            cost_ratio_treatment_vs_control=cost_ratio,
        )

    treatment_cited = mean(by_arm["TREATMENT"], "citation")
    if treatment_cited < 0.5 and arm_accuracy["TREATMENT"] <= arm_accuracy["WRONG_LESSON"]:
        return TrialVerdict(
            verdict="INCONCLUSIVE",
            reasons=tuple(
                reasons
                + [
                    f"ATTRIBUTION: cited {treatment_cited:.2f} and treatment "
                    f"{arm_accuracy['TREATMENT']:.2f} <= wrong-lesson "
                    f"{arm_accuracy['WRONG_LESSON']:.2f}"
                ]
            ),
            arm_scores=arm_scores,
            arm_accuracy=arm_accuracy,
            cost_ratio_treatment_vs_control=cost_ratio,
        )

    return TrialVerdict(
        verdict="PASS",
        reasons=tuple(reasons or ["bar met; NT gate held; attribution holds"]),
        arm_scores=arm_scores,
        arm_accuracy=arm_accuracy,
        cost_ratio_treatment_vs_control=cost_ratio,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Score executed Round-2 trials.")
    parser.add_argument("--trials", required=True, help="JSON file: list of trials")
    args = parser.parse_args(argv)
    with open(args.trials, encoding="utf-8") as handle:
        trials = json.load(handle)
    try:
        result = score_trials(trials)
    except ValueError as exc:
        print(f"SCORE_REFUSED: {exc}")
        return 2
    print(
        json.dumps(
            {
                "verdict": result.verdict,
                "reasons": list(result.reasons),
                "arm_scores": result.arm_scores,
                "arm_accuracy": result.arm_accuracy,
                "cost_ratio_treatment_vs_control": result.cost_ratio_treatment_vs_control,
            },
            indent=2,
        )
    )
    return 0 if result.verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
