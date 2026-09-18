#!/usr/bin/env python3
"""Fail-closed validator for the Naya Power Progress Index.

The index is the canonical measurement layer. It records, for each checkpoint, the exact
baseline HEAD, the exact execution HEAD and their topology, the weighted subsystem scores,
the declared vs computed aggregate, the independently adjudicated verdict, and the accept/reject
status under the 9.0 floor. It authorizes nothing and executes nothing.

Commands:
  validate     structural + arithmetic + verdict validation (GREEN/RED)
  adjudicate   recompute aggregates and the verdict from the recorded evidence
  self-test    adversarial RED/GREEN proof that a broken index fails closed
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
INDEX_PATH = ROOT / ".naya" / "state" / "CHECKPOINT-001.json"
SCHEMA_PATH = ROOT / ".naya" / "state" / "NAYA-POWER-PROGRESS-INDEX-V1.schema.json"

SCHEMA_ID = "naya-power-progress-index/v1"
REPOSITORY = "SoulSchoolAcademy/NayaPOWER"
BAND_NAMES = ("Failing", "Developing", "Strong but incomplete", "Accepted", "Elite", "Objective achieved")
VERIFICATIONS = {"REMOTE_CONFIRMED_VIA_FETCH", "LOCAL_ONLY", "UNVERIFIED"}
WEIGHT_TOLERANCE = 0.05
MEAN_TOLERANCE = 0.005
DIVERGENCE_TOLERANCE = 0.0001


def load(path: Path = INDEX_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _is_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_num(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _is_hex40(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 40 and all(char in "0123456789abcdef" for char in value)


def _band_for(score: float, bands: list[dict[str, Any]]) -> str | None:
    for band in bands:
        if band["min"] - 1e-9 <= score <= band["max"] + 1e-9:
            return band["status"]
    return None


def _computed(subsystems: list[dict[str, Any]]) -> tuple[float, float, float]:
    total_weight = sum(item["weight_pct"] for item in subsystems)
    weighted = sum(item["weight_pct"] * item["score"] for item in subsystems) / total_weight if total_weight else 0.0
    mean = sum(item["score"] for item in subsystems) / len(subsystems)
    return total_weight, round(weighted, 4), round(mean, 4)


def validate(index: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(index, dict):
        return ["index must be an object"]
    if index.get("$schema") != SCHEMA_ID:
        errors.append(f"index: invalid $schema (expected {SCHEMA_ID})")
    if index.get("status") != "CANONICAL":
        errors.append("index: status must be CANONICAL")

    law = index.get("acceptance_law")
    floor = target = objective = None
    bands: list[dict[str, Any]] = []
    if not isinstance(law, dict):
        errors.append("index: acceptance_law object is required")
    else:
        floor, target, objective = law.get("floor"), law.get("target"), law.get("objective")
        if floor != 9.0:
            errors.append("acceptance_law: floor must be 9.0")
        if target != 9.5:
            errors.append("acceptance_law: target must be 9.5")
        if objective != 10.0:
            errors.append("acceptance_law: objective must be 10.0")
        if not _is_text(law.get("rule")):
            errors.append("acceptance_law: rule is required")
        raw_bands = law.get("bands")
        if not isinstance(raw_bands, list) or not raw_bands:
            errors.append("acceptance_law: bands must be a non-empty list")
        else:
            for position, band in enumerate(raw_bands):
                if not isinstance(band, dict) or not _is_num(band.get("min")) or not _is_num(band.get("max")):
                    errors.append(f"acceptance_law.bands[{position}]: min/max must be numbers")
                    continue
                if band["status"] not in BAND_NAMES:
                    errors.append(f"acceptance_law.bands[{position}]: unknown status")
                bands.append(band)
            if bands:
                ordered = sorted(bands, key=lambda b: b["min"])
                if ordered[0]["min"] != 0.0:
                    errors.append("acceptance_law.bands: must start at 0.0")
                if ordered[-1]["max"] != 10.0:
                    errors.append("acceptance_law.bands: must end at 10.0")
                for left, right in zip(ordered, ordered[1:]):
                    if abs((right["min"] - 0.1) - left["max"]) > 1e-6:
                        errors.append(f"acceptance_law.bands: gap or overlap between {left['status']} and {right['status']}")

    checkpoints = index.get("checkpoints")
    if not isinstance(checkpoints, list) or not checkpoints:
        errors.append("index: checkpoints must be a non-empty list")
        return errors

    seen_ids: set[str] = set()
    seen_seq: set[int] = set()
    for position, checkpoint in enumerate(checkpoints):
        label = f"checkpoint[{position}]"
        if not isinstance(checkpoint, dict):
            errors.append(f"{label}: must be an object")
            continue
        cid = checkpoint.get("checkpoint_id")
        if not _is_text(cid):
            errors.append(f"{label}: checkpoint_id is required")
            continue
        label = cid
        if cid in seen_ids:
            errors.append(f"{label}: duplicate checkpoint_id")
        seen_ids.add(cid)
        if checkpoint.get("sequence") in seen_seq:
            errors.append(f"{label}: duplicate sequence")
        if isinstance(checkpoint.get("sequence"), int):
            seen_seq.add(checkpoint["sequence"])
        if checkpoint.get("kind") not in {"BASELINE", "PROGRESS"}:
            errors.append(f"{label}: kind must be BASELINE or PROGRESS")
        for field in ("recorded_at", "recorded_by", "next_action"):
            if not _is_text(checkpoint.get(field)):
                errors.append(f"{label}: {field} is required")
        if checkpoint.get("repository") != REPOSITORY:
            errors.append(f"{label}: repository must be {REPOSITORY}")

        baseline = checkpoint.get("baseline_reference")
        if not isinstance(baseline, dict) or not _is_hex40(baseline.get("main_head")):
            errors.append(f"{label}: baseline_reference.main_head must be a 40-hex commit")
        elif baseline.get("observed_by") not in {"human", "machine"}:
            errors.append(f"{label}: baseline_reference.observed_by must be human or machine")
        elif baseline.get("verification") not in VERIFICATIONS:
            errors.append(f"{label}: baseline_reference.verification is invalid")

        execution = checkpoint.get("execution_head")
        relation: dict[str, Any] = {}
        if not isinstance(execution, dict) or not _is_hex40(execution.get("commit")):
            errors.append(f"{label}: execution_head.commit must be a 40-hex commit")
        elif not _is_text(execution.get("branch")):
            errors.append(f"{label}: execution_head.branch is required")
        else:
            relation = execution.get("relation_to_baseline") or {}
            if not _is_hex40(relation.get("merge_base")):
                errors.append(f"{label}: relation_to_baseline.merge_base must be a 40-hex commit")
            for field in ("ahead", "behind"):
                if not isinstance(relation.get(field), int) or isinstance(relation.get(field), bool) or relation[field] < 0:
                    errors.append(f"{label}: relation_to_baseline.{field} must be a non-negative integer")
            if not isinstance(relation.get("is_ancestor"), bool):
                errors.append(f"{label}: relation_to_baseline.is_ancestor must be a boolean")
            elif isinstance(relation.get("behind"), int):
                if relation["is_ancestor"] != (relation["behind"] == 0):
                    errors.append(f"{label}: is_ancestor must be true exactly when behind == 0")

        subsystems = checkpoint.get("subsystems")
        total_weight = None
        if not isinstance(subsystems, list) or len(subsystems) != 10:
            errors.append(f"{label}: exactly 10 subsystems are required")
        else:
            ids = [item.get("id") for item in subsystems]
            if len(set(ids)) != 10:
                errors.append(f"{label}: subsystem ids must be unique")
            for position, item in enumerate(subsystems):
                name = item.get("name", f"subsystem[{position}]")
                if not _is_text(item.get("id")) or not str(item.get("id")).startswith("S"):
                    errors.append(f"{label}.{name}: id must be S00-style")
                if not _is_text(item.get("name")):
                    errors.append(f"{label}: subsystem name is required")
                weight = item.get("weight_pct")
                score = item.get("score")
                if not _is_num(weight) or not 0 <= weight <= 100:
                    errors.append(f"{label}.{name}: weight_pct must be 0..100")
                if not _is_num(score) or not 0 <= score <= 10:
                    errors.append(f"{label}.{name}: score must be 0..10")
                elif bands:
                    expected = _band_for(float(score), bands)
                    if expected and item.get("status") != expected:
                        errors.append(f"{label}.{name}: status must be {expected} for score {score}")
            if all(_is_num(item.get("weight_pct")) and _is_num(item.get("score")) for item in subsystems) and bands:
                total_weight, weighted, mean = _computed(subsystems)
                aggregate = checkpoint.get("aggregate")
                if not isinstance(aggregate, dict):
                    errors.append(f"{label}: aggregate object is required")
                else:
                    declared_weight_sum = aggregate.get("weight_sum")
                    weight_sum_valid = aggregate.get("weight_sum_valid")
                    declared_weighted = aggregate.get("weighted_total")
                    declared_mean = aggregate.get("unweighted_mean")
                    declared_score = aggregate.get("declared_system_score")
                    divergence = aggregate.get("divergence")
                    if not _is_num(declared_weight_sum) or abs(declared_weight_sum - total_weight) > DIVERGENCE_TOLERANCE:
                        errors.append(f"{label}: weight_sum must equal the computed sum {total_weight}")
                    expected_valid = total_weight == 100
                    if weight_sum_valid is not expected_valid:
                        errors.append(f"{label}: weight_sum_valid must be {expected_valid} for a weight sum of {total_weight}")
                    if not expected_valid:
                        notes = list(checkpoint.get("known_risks") or []) + list(checkpoint.get("unknowns") or [])
                        if not any("weight" in str(note).lower() for note in notes):
                            errors.append(f"{label}: an invalid weight sum must be recorded as a known risk or unknown")
                    if not _is_num(declared_weighted) or abs(declared_weighted - weighted) > WEIGHT_TOLERANCE:
                        errors.append(f"{label}: weighted_total must equal the normalized weighted mean {weighted} (±{WEIGHT_TOLERANCE})")
                    if not _is_num(declared_mean) or abs(declared_mean - mean) > MEAN_TOLERANCE:
                        errors.append(f"{label}: unweighted_mean must equal {mean} (±{MEAN_TOLERANCE})")
                    if not _is_num(declared_score):
                        errors.append(f"{label}: declared_system_score must be a number")
                    if not _is_text(aggregate.get("declared_source")):
                        errors.append(f"{label}: aggregate.declared_source is required")
                    if not _is_num(declared_score) or not _is_num(declared_weighted):
                        pass
                    elif not _is_num(divergence) or abs(divergence - (declared_score - declared_weighted)) > DIVERGENCE_TOLERANCE:
                        errors.append(f"{label}: divergence must equal declared_system_score - weighted_total")
                    if _is_num(declared_score) and floor is not None:
                        verdict = checkpoint.get("verdict")
                        if not isinstance(verdict, dict):
                            errors.append(f"{label}: verdict object is required")
                        else:
                            adjudicated = verdict.get("adjudicated_score")
                            if verdict.get("threshold") != floor:
                                errors.append(f"{label}: verdict.threshold must equal acceptance_law.floor")
                            if not _is_num(adjudicated) or abs(adjudicated - declared_score) > DIVERGENCE_TOLERANCE:
                                errors.append(f"{label}: verdict.adjudicated_score must equal declared_system_score for a BASELINE checkpoint")
                            if not _is_text(verdict.get("reason")):
                                errors.append(f"{label}: verdict.reason is required")
                            if isinstance(adjudicated, bool) or not _is_num(adjudicated):
                                errors.append(f"{label}: verdict.adjudicated_score must be a number")
                            else:
                                expected_accepted = adjudicated >= floor
                                if verdict.get("accepted") is not expected_accepted:
                                    errors.append(f"{label}: accepted must be {expected_accepted} under the {floor} floor")
                                expected_status = _band_for(float(adjudicated), bands)
                                if expected_status and verdict.get("status") != expected_status:
                                    errors.append(f"{label}: verdict.status must be {expected_status} for score {adjudicated}")

        for field in ("evidence", "highest_value_improvements"):
            value = checkpoint.get(field)
            if not isinstance(value, list) or not value:
                errors.append(f"{label}: {field} must be a non-empty list")
        for item in checkpoint.get("highest_value_improvements") or []:
            if not isinstance(item, dict):
                errors.append(f"{label}: improvement entries must be objects")
                continue
            if not (isinstance(item.get("id"), str) and item["id"].startswith("P0-")):
                errors.append(f"{label}: improvement id must be P0-x")
            if not (isinstance(item.get("queue_task"), str) and item["queue_task"].startswith("TASK-")):
                errors.append(f"{label}: improvement queue_task must be a TASK- id")
            for field in ("title", "why"):
                if not _is_text(item.get(field)):
                    errors.append(f"{label}: improvement {field} is required")
        for field in ("known_risks", "unknowns"):
            if not isinstance(checkpoint.get(field), list):
                errors.append(f"{label}: {field} must be a list")
    return errors


def adjudicate(index: dict[str, Any]) -> dict[str, Any]:
    law = index["acceptance_law"]
    results = []
    for checkpoint in index["checkpoints"]:
        total_weight, weighted, mean = _computed(checkpoint["subsystems"])
        declaration = checkpoint["aggregate"]
        adjudicated = checkpoint["verdict"]["adjudicated_score"]
        results.append({
            "checkpoint_id": checkpoint["checkpoint_id"],
            "subsystem_count": len(checkpoint["subsystems"]),
            "weight_sum": total_weight,
            "weight_sum_valid": total_weight == 100,
            "weighted_total": weighted,
            "unweighted_mean": mean,
            "declared_system_score": declaration["declared_system_score"],
            "divergence": round(declaration["declared_system_score"] - weighted, 4),
            "adjudicated_score": adjudicated,
            "band": _band_for(float(adjudicated), law["bands"]),
            "floor": law["floor"],
            "accepted": adjudicated >= law["floor"],
        })
    return {"status": "ADJUDICATED", "checkpoints": results}


def _clone(index: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(index))


def self_test() -> int:
    base = load()
    assert not validate(base), "canonical index must validate"

    def ck0(mutator) -> dict[str, Any]:
        clone = _clone(base)
        mutator(clone["checkpoints"][0])
        return clone

    checks = [
        ("accepted below floor", ck0(lambda c: c["verdict"].update(accepted=True)), "accepted must be False"),
        ("weighted total arithmetic lie", ck0(lambda c: c["aggregate"].update(weighted_total=9.9)), "weighted_total must equal"),
        ("divergence lie", ck0(lambda c: c["aggregate"].update(divergence=0.0)), "divergence must equal"),
        ("subsystem status mismatch", ck0(lambda c: c["subsystems"][2].update(status="Developing")), "status must be Failing"),
        ("verdict status mismatch", ck0(lambda c: c["verdict"].update(status="Accepted")), "verdict.status must be Developing"),
        ("bad baseline hex", ck0(lambda c: c["baseline_reference"].update(main_head="94d2c5")), "baseline_reference.main_head must be a 40-hex commit"),
        ("ancestor/behind contradiction", ck0(lambda c: c["execution_head"]["relation_to_baseline"].update(is_ancestor=True)), "is_ancestor must be true exactly when behind == 0"),
        ("wrong subsystem count", ck0(lambda c: c["subsystems"].pop()), "exactly 10 subsystems"),
        ("weight sum mismatch", ck0(lambda c: c["subsystems"][0].update(weight_pct=14)), "weight_sum must equal"),
        ("weight sum validity lie", ck0(lambda c: c["aggregate"].update(weight_sum_valid=True)), "weight_sum_valid must be False"),
        ("invalid floor", lambda: {**_clone(base), "acceptance_law": {**base["acceptance_law"], "floor": 8.0}}, "floor must be 9.0"),
    ]
    failures = 0
    for name, mutated, expected in checks:
        errors = validate(mutated if isinstance(mutated, dict) else mutated())
        matched = any(expected in error for error in errors)
        print(f"{'PASS' if matched else 'FAIL'}: {name} -> {'RED' if errors else 'GREEN'}")
        if not matched:
            failures += 1
            print(f"  expected substring: {expected}")
            print(f"  actual errors: {errors}")

    result = adjudicate(base)
    record = result["checkpoints"][0]
    print(f"ADJUDICATED {record['checkpoint_id']}: weighted={record['weighted_total']} mean={record['unweighted_mean']} "
          f"declared={record['declared_system_score']} divergence={record['divergence']} "
          f"verdict={record['band']} accepted={record['accepted']}")
    if record["accepted"]:
        failures += 1
        print("FAIL: the 6.70 baseline must not be accepted")
    if failures:
        print(f"FAIL - {failures} self-test assertion(s) failed")
        return 1
    print("PASS - Progress Index validation, acceptance law, and independent adjudication are GREEN")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Naya Power Progress Index validator")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    sub.add_parser("adjudicate")
    sub.add_parser("self-test")
    args = parser.parse_args()
    try:
        index = load()
    except (OSError, json.JSONDecodeError) as exc:
        print(f"PROGRESS_INDEX=RED\nFIRST_DIVERGENCE={exc}")
        return 1
    if args.command == "self-test":
        return self_test()
    errors = validate(index)
    if args.command == "validate":
        if errors:
            print("PROGRESS_INDEX=RED")
            for error in errors:
                print(f"- {error}")
            return 1
        print(f"PROGRESS_INDEX=GREEN ({len(index['checkpoints'])} checkpoint(s))")
        return 0
    if errors:
        print("PROGRESS_INDEX=RED - fix validation before adjudicating")
        for error in errors:
            print(f"- {error}")
        return 1
    print(json.dumps(adjudicate(index), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
