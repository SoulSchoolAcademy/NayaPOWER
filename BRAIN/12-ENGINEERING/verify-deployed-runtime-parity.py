#!/usr/bin/env python3
"""Deployed edge-function SOURCE/RUNTIME PARITY detector.

WHY THIS EXISTS
---------------
This repository has NO deployment pipeline. There is no `supabase functions deploy`
in any workflow, no `SUPABASE_ACCESS_TOKEN` (the management token deploy requires),
and no `supabase/config.toml`. Every edge function reaches runtime through an
untracked human action.

Consequence: a merged source fix can be cited as fixed and never reach runtime,
and NOTHING in the repo would detect it. That is not hypothetical - it is how
`nayanet-cold-runtime-proof` ended up deployed without the `behavior` /
`authority_boundary` evidence that the canonical verifier requires, and how its
`independent-connect-verification` job sat SKIPPED while every other job looked
fine.

So the most dangerous object in this project is a green run resting on a
hand-deployed artifact nobody can verify. This detector makes that state VISIBLE
instead of silent.

HOW IT WORKS WITHOUT A MANAGEMENT TOKEN
---------------------------------------
It does not query Supabase (no credential, and service-role access is forbidden
for proof). Instead it compares two things:

  CANONICAL = the receipt contract, imported from the canonical verifier
              tests/verify_connect_runtime_receipt.py. Single source of truth, so
              this detector cannot drift away from the contract it enforces.
  OBSERVED  = a recorded runtime response plus its provenance, from
              evidence/deployed-runtime-observation.json.

The observed receipt is produced by the real runtime, so this is evidence of what
is actually deployed, not a claim about it.

VERDICTS
--------
  MATCH    canonical source and the last observed runtime agree.
  DRIFT    they disagree. The named fields are printed. This is a FAILURE.
  UNKNOWN  no observation has been recorded, or the observation predates the
           source it is being compared against.

THE ONE RULE THIS SCRIPT ENFORCES:
  UNKNOWN is never reported as MATCH, and never exits 0.
An unverified system is not a verified system. Absence of evidence is not
evidence of absence of drift.

Usage:
  python BRAIN/12-ENGINEERING/verify-deployed-runtime-parity.py
Exit codes: 0 MATCH | 1 DRIFT or UNKNOWN (both are non-pass) | 2 harness error
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
VERIFIER = REPO / "tests" / "verify_connect_runtime_receipt.py"
OBSERVATION = REPO / "evidence" / "deployed-runtime-observation.json"
CANONICAL_SOURCE = REPO / "supabase" / "functions" / "nayanet-cold-runtime-proof" / "index.ts"

sys.path.insert(0, str(REPO / "tests"))
import verify_connect_runtime_receipt as contract  # noqa: E402


def _canonical_requirements() -> set:
    """Fully-qualified required field names, derived from the canonical verifier.

    The verifier's tuples are BARE subfield names ('blocked_by'), while observed
    keys are QUALIFIED ('behavior.blocked_by'). Qualify them here so the two sides
    of the comparison are in the same namespace. Getting this wrong makes every
    conforming receipt look like drift.
    """
    required = set(contract.REQUIRED_RECEIPT_FIELDS)
    for group, fields in (
        ("connect", contract.REQUIRED_CONNECT_FIELDS),
        ("behavior", contract.REQUIRED_BEHAVIOR_FIELDS),
        ("authority_boundary", contract.REQUIRED_AUTHORITY_BOUNDARY_FIELDS),
    ):
        required |= {f"{group}.{f}" for f in fields}
    return required


def _source_commit() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=str(REPO), capture_output=True, text=True
    ).stdout.strip()


def _flatten(receipt: dict) -> set:
    keys = set(receipt.keys())
    for group in ("behavior", "authority_boundary", "connect"):
        sub = receipt.get(group)
        if isinstance(sub, dict):
            keys |= {f"{group}.{k}" for k in sub}
    return keys


def evaluate(observation: dict | None, source_commit: str) -> tuple:
    """Return (verdict, findings). Pure, so it can be regression-tested."""
    required_keys = _canonical_requirements()

    if observation is None:
        return "UNKNOWN", ["no runtime observation recorded: a deployed artifact has never been observed"]

    observed_commit = observation.get("canonical_commit_observed")
    if not observed_commit:
        return "UNKNOWN", ["observation does not record which canonical commit it was taken against"]
    if observed_commit != source_commit:
        return "UNKNOWN", [
            f"observation was taken against canonical {observed_commit[:8]} but HEAD is {source_commit[:8]}; "
            "the comparison would be invalid"
        ]

    receipt = observation.get("observed_receipt")
    if not isinstance(receipt, dict):
        return "UNKNOWN", ["observation carries no observed_receipt object"]

    seen = _flatten(receipt)
    missing = sorted(required_keys - seen)
    if missing:
        return "DRIFT", [
            f"DEPLOYED ARTIFACT IS STALE: runtime is missing {len(missing)} field(s) the canonical "
            f"verifier requires: {', '.join(missing)}",
            f"observed via {observation.get('provenance', 'unknown provenance')}",
        ]

    unknown = sorted(seen - required_keys)
    if unknown:
        return "DRIFT", [
            f"runtime emits field(s) absent from the canonical contract: {', '.join(unknown)}",
            "an undeployed or divergent artifact is serving traffic",
        ]
    return "MATCH", []


def main() -> int:
    if not VERIFIER.exists():
        print(f"harness error: canonical verifier missing at {VERIFIER}")
        return 2
    if not CANONICAL_SOURCE.exists():
        print(f"harness error: canonical function source missing at {CANONICAL_SOURCE}")
        return 2

    observation = None
    if OBSERVATION.exists():
        observation = json.loads(OBSERVATION.read_text(encoding="utf-8"))

    verdict, findings = evaluate(observation, _source_commit())

    print("=" * 74)
    print("DEPLOYED EDGE FUNCTION - SOURCE/RUNTIME PARITY")
    print("=" * 74)
    print(f"canonical source : {CANONICAL_SOURCE.relative_to(REPO).as_posix()}")
    print(f"contract source  : {VERIFIER.relative_to(REPO).as_posix()}")
    print(f"observation      : {OBSERVATION.relative_to(REPO).as_posix() if OBSERVATION.exists() else 'ABSENT'}")
    if observation:
        print(f"observed against : {str(observation.get('canonical_commit_observed'))[:8]}")
        print(f"provenance       : {observation.get('provenance', 'unrecorded')}")
    print(f"verdict          : {verdict}")
    for f in findings:
        print(f"  - {f}")

    if verdict == "MATCH":
        print("\nMATCH: the last observed runtime response satisfies the canonical contract.")
        return 0

    if verdict == "UNKNOWN":
        print("\nUNKNOWN IS NOT PASS. No runtime claim in this project is reproducible until an")
        print("observation of the deployed artifact is recorded against the current canonical commit.")
    else:
        print("\nDRIFT IS A FAILURE. Canonical source has advanced past the deployed artifact, and the")
        print("deployed artifact is the one serving traffic and producing every live receipt.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
