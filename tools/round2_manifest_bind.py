"""Bind real Round-2 fixtures to the machine-checked preregistration contract.

This is the executable form of "Naya 4/Coda 2 bind real Round-2 fixtures
to this contract, prevalidate keys, then execute trials" (PR #1612 body).

It builds a NAYAPOWER_LEARNING_COMPOUNDING_EXPERIMENT_V2 manifest from
explicit inputs and validates it with tools.learning_experiment_contract.
It never claims learning occurred. Design-only gate.

Fixture identity is the git blob SHA-1 of file bytes (40 hex) — the same
identifier the team cites as `blob <sha>` in evidence. Raw sha1 of file
bytes is a different number and MUST NOT be substituted: publisher-posted
blob SHAs and trial-time re-hashes must use one function. Re-hash at trial
time with verify_fixture_binding; any drift fails the binding.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Sequence

from tools.learning_experiment_contract import (
    ContractResult,
    validate_round2_manifest,
)

SCHEMA = "NAYAPOWER_LEARNING_COMPOUNDING_EXPERIMENT_V2"

FROZEN_WEIGHTS: dict[str, float] = {
    "accuracy": 0.4,
    "diagnostic_order": 0.2,
    "cost": 0.2,
    "consistency": 0.1,
    "negative_transfer_guard": 0.1,
}

FORBIDDEN_EXTRAS = {"results", "observed_scores", "winner", "causal_verdict"}


def blob_sha_file(path: str | Path) -> str:
    """Return the git blob SHA-1 (40 hex) of file bytes. Raises FileNotFoundError."""
    data = Path(path).read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def build_manifest(
    builder: str,
    independent_verifier: str,
    fixture_paths: Sequence[str | Path],
    hypotheses: Sequence[str],
    minimum_trials_per_arm: int = 5,
    negative_transfer_trials: int = 5,
    extras: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a V2 preregistration manifest with frozen weights.

    Fail-fast: blank builder/verifier, empty fixture list, fewer than four
    distinct nonempty hypotheses, non-integer or underpowered trial counts,
    and pre-trial outcome extras are refused here with the contract's error
    codes instead of producing a manifest the gate must reject.
    Raises FileNotFoundError for missing fixtures, ValueError otherwise.
    """
    if not str(builder).strip() or not str(independent_verifier).strip():
        raise ValueError("BUILDER_AND_VERIFIER_REQUIRED")
    if str(builder).strip() == str(independent_verifier).strip():
        raise ValueError("ANSWER_KEY_VERIFIER_MUST_BE_INDEPENDENT")
    if not fixture_paths:
        raise ValueError("FIXTURE_SHAS_REQUIRED")
    distinct = {str(h).strip() for h in hypotheses if str(h).strip()}
    if len(distinct) < 4:
        raise ValueError("FOUR_HYPOTHESES_REQUIRED")
    if (
        not isinstance(minimum_trials_per_arm, int)
        or minimum_trials_per_arm < 5
        or not isinstance(negative_transfer_trials, int)
        or negative_transfer_trials < 5
    ):
        raise ValueError("MINIMUM_FIVE_TRIALS_PER_ARM")
    if extras:
        leaked = sorted(k for k in FORBIDDEN_EXTRAS if k in extras)
        if leaked:
            raise ValueError("OUTCOME_LEAKAGE_BEFORE_TRIALS:" + ",".join(leaked))
    fixture_shas = [blob_sha_file(p) for p in fixture_paths]
    manifest: dict[str, Any] = {
        "schema": SCHEMA,
        "status": "PREREGISTERED",
        "arms": [
            {"name": "CONTROL"},
            {"name": "TREATMENT"},
            {"name": "WRONG_LESSON"},
        ],
        "minimum_trials_per_arm": minimum_trials_per_arm,
        "negative_transfer": {
            "required": True,
            "minimum_trials": negative_transfer_trials,
        },
        "scoring": {
            "weights": dict(FROZEN_WEIGHTS),
            "negative_transfer_is_hard_gate": True,
        },
        "answer_key": {
            "prevalidated_before_trials": True,
            "builder": builder,
            "independent_verifier": independent_verifier,
            "fixture_shas": fixture_shas,
        },
        "evidence_capture": {
            "raw_transcripts_required": True,
            "exact_tool_call_counts_required": True,
            "immutable_fixture_binding_required": True,
        },
        "hypotheses": list(hypotheses),
    }
    if extras:
        manifest.update(extras)
    return manifest


def bind_and_validate(
    builder: str,
    independent_verifier: str,
    fixture_paths: Sequence[str | Path],
    hypotheses: Sequence[str],
    minimum_trials_per_arm: int = 5,
    negative_transfer_trials: int = 5,
    extras: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], ContractResult]:
    """Build the manifest and run the machine-check. Returns both."""
    manifest = build_manifest(
        builder,
        independent_verifier,
        fixture_paths,
        hypotheses,
        minimum_trials_per_arm,
        negative_transfer_trials,
        extras,
    )
    return manifest, validate_round2_manifest(manifest)


def verify_fixture_binding(
    manifest: dict[str, Any], fixture_paths: Sequence[str | Path]
) -> tuple[bool, list[str]]:
    """Re-hash fixtures and compare against the manifest binding.

    Returns (ok, drifted_paths). Order-insensitive; compares sha sets.
    """
    try:
        bound = set(manifest["answer_key"]["fixture_shas"])
    except (KeyError, TypeError):
        return False, [str(p) for p in fixture_paths]
    current = {}
    drifted = []
    for p in fixture_paths:
        try:
            current[str(p)] = blob_sha_file(p)
        except FileNotFoundError:
            drifted.append(f"{p}:MISSING")
    current_shas = set(current.values())
    if current_shas != bound:
        for p, sha in current.items():
            if sha not in bound:
                drifted.append(p)
        return False, drifted
    return True, []


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Bind Round-2 fixtures to the V2 preregistration contract."
    )
    parser.add_argument("--builder", required=True)
    parser.add_argument("--independent-verifier", required=True)
    parser.add_argument("--fixture", action="append", default=[], dest="fixtures")
    parser.add_argument("--hypothesis", action="append", default=[])
    parser.add_argument("--trials-per-arm", type=int, default=5)
    parser.add_argument("--nt-trials", type=int, default=5)
    args = parser.parse_args(argv)
    try:
        manifest, result = bind_and_validate(
            args.builder,
            args.independent_verifier,
            args.fixtures,
            args.hypothesis,
            args.trials_per_arm,
            args.nt_trials,
        )
    except (FileNotFoundError, ValueError) as exc:
        print(f"BIND_REFUSED: {exc}")
        return 2
    if not result.ok:
        print("CONTRACT_REJECTED: " + ",".join(result.errors))
        return 1
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
