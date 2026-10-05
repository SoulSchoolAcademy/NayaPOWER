#!/usr/bin/env python3
"""Deployed edge-function SOURCE/RUNTIME PARITY detector.

WHY THIS EXISTS
---------------
This repository now has a governed production-promotion pipeline. Runtime parity
still must never be inferred from repository source alone: every deployed
component must be bound to the authorized source/artifact and independently
observed at runtime. Historical deployments may predate the governed path.

Consequence: a merged source fix can be cited as fixed and never reach runtime,
and nothing in the repo would detect it. The CONNECT authority-boundary evidence
was missing from the deployed artifact for exactly this reason until it was
refreshed by hand.

THE QUESTION THIS ACTUALLY ANSWERS
----------------------------------
The deployed artifact does not change when main moves. So "was the observation
taken at HEAD" is the WRONG question - it would report UNKNOWN forever, which is
how the first version of this detector was wrong. The right question has two
independent parts:

  1. CONFORMANCE - does the observed runtime response satisfy the canonical
     receipt contract? The contract is IMPORTED from
     tests/verify_connect_runtime_receipt.py, so this detector cannot drift away
     from the contract it is supposed to enforce.

  2. CURRENCY   - has contract-bearing canonical source changed since the
     observation was taken? If it has, the deployed artifact may no longer match
     canonical source and the answer is no longer knowable without a redeploy and
     a fresh observation. Computed from real git objects, not assumed.

VERDICTS
  MATCH   conformant AND canonical unchanged since the observation. Exit 0.
  DRIFT   the observed runtime response violates the canonical contract. Exit 1.
  STALE   conformant, but canonical moved since. The deploy may be behind. Exit 1.
  UNKNOWN no usable observation. Exit 1.

THE ONE RULE
  UNKNOWN is never reported as MATCH, and never exits 0. An unverified system is
  not a verified system. DRIFT and STALE also exit 1 deliberately: a stale deploy
  is not a pass, and neither is an unverifiable one.

CONFORMANCE IS A MINIMUM, NOT AN EXACT SHAPE
A receipt legitimately carries additional provenance - owner_id, token_jti,
relationships, verified_at, authority_boundary.authority_source. An earlier
version of this detector treated those as divergence and produced a FALSE
POSITIVE against a genuine, conformant runtime receipt. A governance detector
that cries drift on a good artifact trains the team to ignore it, which is worse
than having no detector at all.

SCOPE - READ BEFORE TRUSTING A GREEN
This proves contract conformance for ONE function's ONE mode. It does NOT police
field VALUES, does NOT cover any other function, and says nothing about the
health of the rest of the runtime. MATCH means "this receipt contract is
satisfied by the last observed runtime response, and canonical source has not
moved since" - nothing more. Value-level enforcement belongs to
tests/verify_connect_runtime_receipt.py.

Usage:
  python BRAIN/12-ENGINEERING/verify-deployed-runtime-parity.py
Exit codes: 0 MATCH | 1 DRIFT / STALE / UNKNOWN | 2 harness error
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
VERIFIER = REPO / "tests" / "verify_connect_runtime_receipt.py"
OBSERVATION = REPO / ".naya" / "evidence" / "deployed-runtime-observation.json"
CANONICAL_SOURCE = REPO / "supabase" / "functions" / "nayanet-cold-runtime-proof" / "index.ts"

# The DEPLOYED artifact is the function source. If it changed after the
# observation, the artifact serving traffic may no longer be current canonical.
DEPLOYED_SOURCE_PATHS = ("supabase/functions/nayanet-cold-runtime-proof/index.ts",)

# The CONTRACT is the verifier. A change here does not mean the deploy is stale -
# it is always evaluated against the CURRENT contract during conformance. A
# refactor of the verifier that preserves the requirement set must not be
# reported as drift, which is a false positive this detector once produced.
CONTRACT_PATHS = ("tests/verify_connect_runtime_receipt.py",)

sys.path.insert(0, str(REPO / "tests"))
import verify_connect_runtime_receipt as contract  # noqa: E402


def canonical_requirements() -> set:
    """Fully-qualified required field names derived from the canonical verifier.

    The verifier's tuples are BARE subfield names ('blocked_by') while observed
    keys are QUALIFIED ('behavior.blocked_by'). Qualify them here so both sides
    of the comparison share a namespace. Getting this wrong makes every
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


def _git(*args) -> str:
    return subprocess.run(["git", *args], cwd=str(REPO), capture_output=True, text=True).stdout


def _flatten(receipt: dict) -> set:
    keys = set(receipt.keys())
    for group in ("behavior", "authority_boundary", "connect"):
        sub = receipt.get(group)
        if isinstance(sub, dict):
            keys |= {f"{group}.{k}" for k in sub}
    return keys


def _paths_changed_since(observed_commit: str, paths: tuple) -> bool | None:
    """True if any of `paths` differs between the observation commit and HEAD.

    Returns None when undeterminable, which callers must treat as unknown rather
    than as 'unchanged'.
    """
    if not observed_commit or _git("cat-file", "-t", observed_commit).strip() != "commit":
        return None
    for path in paths:
        before = _git("show", f"{observed_commit}:{path}")
        after = _git("show", f"HEAD:{path}")
        if not before or not after:
            return None
        if before != after:
            return True
    return False


def deployed_source_changed_since(observed_commit: str) -> bool | None:
    """Has the code that actually gets deployed changed since the observation?"""
    return _paths_changed_since(observed_commit, DEPLOYED_SOURCE_PATHS)


def contract_changed_since(observed_commit: str) -> bool | None:
    """Informational only: has the receipt contract been edited since?"""
    return _paths_changed_since(observed_commit, CONTRACT_PATHS)


def evaluate(observation: dict | None, source_changed_since_observation: bool | None) -> tuple:
    """Return (verdict, findings). Pure, so every branch is regression-testable."""
    if observation is None:
        return "UNKNOWN", ["no runtime observation recorded: the deployed artifact has never been observed"]

    if not observation.get("canonical_commit_observed"):
        return "UNKNOWN", ["observation does not record which canonical commit it was taken against"]

    document = observation.get("observed_document")
    if not isinstance(document, dict):
        return "UNKNOWN", ["observation carries no observed_document"]

    # 1. CURRENCY, decided by the runtime itself. The deployed bundle reports the
    #    commit it was built from; that is the only trustworthy drift signal,
    #    because source moves constantly while a deployed artifact does not.
    revision = document.get("deployed_source_revision")
    if revision is None:
        return "DRIFT", [
            "DEPLOYED ARTIFACT PREDATES REVISION STAMPING: the runtime does not report "
            "deployed_source_revision, so it is impossible to tell which canonical commit is serving "
            "traffic. A source change that was never deployed would be undetectable."
        ]
    if revision == contract.UNSTAMPED:
        return "UNKNOWN", [
            "the deployed artifact reports deployed_source_revision=UNSTAMPED. Deployed-vs-canonical "
            "parity is UNDECIDABLE, not verified. Whoever deploys must stamp this constant with the "
            "commit actually deployed, then redeploy."
        ]
    expected = str(observation["canonical_commit_observed"])
    same_revision = str(revision).startswith(expected[:8]) or expected.startswith(str(revision)[:8])
    if not same_revision:
        if source_changed_since_observation is None:
            return "UNKNOWN", [
                "the runtime revision differs from the observed canonical commit, but deployable source "
                "equivalence could not be established"
            ]
        if source_changed_since_observation:
            return "STALE", [
                f"the deployed artifact was built from {str(revision)[:8]} and deployable function source "
                f"differs at canonical {expected[:8]}. Redeploy."
            ]
        # Repository history moved, but the deployable function source is byte-equivalent.
        # Treat this as source-equivalent rather than forcing a no-op redeploy.

    receipt = document.get("receipt")
    if not isinstance(receipt, dict):
        return "UNKNOWN", ["observation carries no observed_receipt object"]

    seen = _flatten(receipt)
    missing = sorted(canonical_requirements() - seen)
    if missing:
        return "DRIFT", [
            f"DEPLOYED ARTIFACT VIOLATES CANONICAL CONTRACT: missing {len(missing)} required field(s): "
            f"{', '.join(missing)}",
            f"observed via {observation.get('provenance', 'unrecorded provenance')}",
        ]

    if source_changed_since_observation is None:
        return "UNKNOWN", [
            "contract-bearing canonical source could not be compared against the observation commit, "
            "so currency is unknown"
        ]
    if source_changed_since_observation:
        return "STALE", [
            f"the observed runtime response conforms, but the deployed function source changed "
            f"after commit {observation['canonical_commit_observed'][:8]}. Redeploy and re-observe."
        ]

    return "MATCH", []


def main() -> int:
    if not VERIFIER.exists() or not CANONICAL_SOURCE.exists():
        print("harness error: canonical verifier or function source is missing")
        return 2

    observation = None
    if OBSERVATION.exists():
        observation = json.loads(OBSERVATION.read_text(encoding="utf-8"))

    observation_commit = (observation or {}).get("canonical_commit_observed", "")
    runtime_revision = str(((observation or {}).get("observed_document") or {}).get("deployed_source_revision") or "")
    comparison_base = runtime_revision if runtime_revision and runtime_revision != contract.UNSTAMPED else observation_commit
    changed = deployed_source_changed_since(comparison_base)
    contract_edited = contract_changed_since((observation or {}).get("canonical_commit_observed", ""))
    verdict, findings = evaluate(observation, changed)

    print("=" * 76)
    print("DEPLOYED EDGE FUNCTION - SOURCE/RUNTIME PARITY")
    print("=" * 76)
    print("function        : nayanet-cold-runtime-proof (mode=connect)")
    print(f"contract source : {VERIFIER.relative_to(REPO).as_posix()}")
    print(f"observation     : {OBSERVATION.relative_to(REPO).as_posix() if OBSERVATION.exists() else 'ABSENT'}")
    if observation:
        print(f"observed against: {str(observation.get('canonical_commit_observed'))[:8]}")
        print(f"provenance      : {observation.get('provenance', 'unrecorded')}")
        if observation.get("artifact_digest_sha256"):
            print(f"artifact sha256 : {observation['artifact_digest_sha256'][:32]}...")
    print(f"deployed source differs from runtime revision : {changed}")
    print(f"contract edited since : {contract_edited}  (informational only)")
    print(f"VERDICT         : {verdict}")
    for f in findings:
        print(f"  - {f}")

    if verdict == "MATCH":
        print("\nMATCH: the last observed runtime response satisfies the canonical contract, and")
        print("contract-bearing canonical source has not changed since it was taken.")
        print("SCOPE: one function, one mode, contract conformance. Not whole-runtime health.")
        return 0

    if verdict == "STALE":
        print("\nSTALE IS NOT A PASS. A conformant receipt from an older canonical contract is not")
        print("evidence that the currently deployed artifact matches current canonical source.")
    elif verdict == "UNKNOWN":
        print("\nUNKNOWN IS NOT PASS. No runtime claim is reproducible until an observation of the")
        print("deployed artifact is recorded against a known canonical commit.")
    else:
        print("\nDRIFT IS A FAILURE. The deployed artifact does not satisfy the canonical contract.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
