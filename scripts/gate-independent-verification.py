#!/usr/bin/env python3
"""P0 Gate 2 — Independent Verification (machine-falsifiable).

A claim of `independent_verification: true` is OPERATIVE only if a machine
can falsify it. Self-attestation must read as NOT verified.

Operational definition of "independent" (from production receipts
cold-successor-receipt-verified.json, causal-learning-experiment-receipt.json):
  V1  DISTINCT VERIFIER — verifier identity present AND != executor identity.
      Same identity (or missing verifier) = self-attestation = FAIL.
  V2  VERIFIER MODE     — a recognized verification mode is declared.
  V3  RECOMPUTATION     — evidence the verifier recomputed from authoritative
      state rather than trusting the executor's claim.
  V4  NO TRUST          — executor_claim_trusted must not be true. A verifier
      that trusts the claim did not verify independently.
  V5  RECONSTRUCTABLE  — a third party can reconstruct the verification.

Usage:
    python3 scripts/gate-independent-verification.py <receipt.json> [...]
    python3 scripts/gate-independent-verification.py --self-test
        (runs the gate against the two production receipts = must PASS,
         and against fabricated self-attested receipts = must FAIL)

Exit 0 = all artifacts pass. Exit 1 = any artifact fails (names it).

Falsifier: craft a receipt with independent_verification:true but the
verifier_runtime_jti == executor_runtime_jti. This gate MUST fail it.
If it passes, the gate is broken.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RECOGNIZED_MODES = {
    "AUTHORITATIVE_REREAD_AND_RECOMPUTATION",
    "INDEPENDENT_REPLAY",
    "HELD_OUT_RETEST",
    "CROSS_SEAT_REVIEW",
}

# Field aliases: receipts use slightly different shapes; normalize first.
VERIFIER_ID_FIELDS = ["verifier_runtime_jti", "verifier_identity", "verifier_jti"]
EXECUTOR_ID_FIELDS = ["executor_runtime_jti", "executor_identity", "executor_jti", "actor_runtime_jti"]
RECOMPUTE_FIELDS = [
    "recomputed_from_authoritative_state",
    "recomputation",
    "independent_recomputation",
]
RECONSTRUCT_FIELDS = ["reconstructable_by", "reconstruction_path"]


def _first(d: dict, fields: list[str]):
    for f in fields:
        v = d.get(f)
        if v:
            return v
    return None


def _basis(d: dict) -> dict:
    b = d.get("independent_verification_basis")
    return b if isinstance(b, dict) else {}


# Concrete artifact nouns: a reconstruction path must name WHAT to re-read,
# not just assert that someone could check.
CONCRETE_ARTIFACT_NOUNS = {
    "learning", "block", "relationship", "grant", "receipt", "table",
    "event", "checkpoint", "index", "artifact", "run",
}


def _names_concrete_artifacts(text: str) -> bool:
    """A reconstruction path is concrete if it names specific artifacts:
    identifier-like tokens (UUID/IB-/ids) or concrete artifact nouns,
    in a non-trivial statement."""
    if len(text.strip()) < 40:
        return False
    low = text.lower()
    has_id = bool(re.search(r"\b[0-9a-f]{8}-[0-9a-f]{4}\b|\bIB-[A-Z0-9-]+\b|\bid\b", low))
    has_noun = any(n in low for n in CONCRETE_ARTIFACT_NOUNS)
    return has_id or has_noun


def verify_artifact(path: Path) -> tuple[bool, list[str]]:
    """Return (passed, failures). Any claimed independent verification that
    cannot prove independence FAILS."""
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as e:
        return False, [f"unreadable artifact: {e}"]

    failures: list[str] = []
    claimed = data.get("independent_verification") is True
    if not claimed:
        # Nothing claimed, nothing to falsify. (A separate gate may require
        # verification where the contract demands it.)
        return True, []

    basis = _basis(data)
    verifier = _first(data, VERIFIER_ID_FIELDS) or _first(basis, VERIFIER_ID_FIELDS)
    executor = _first(data, EXECUTOR_ID_FIELDS) or _first(basis, EXECUTOR_ID_FIELDS)

    # V1: distinct verifier identity.
    if not verifier:
        failures.append("V1: verifier identity missing — self-attestation reads as NOT verified")
    elif verifier == executor:
        failures.append(
            f"V1: verifier identity == executor identity ({verifier}) — "
            "a verifier cannot independently verify its own claim"
        )

    # V2: recognized verifier mode.
    mode = data.get("verifier_mode") or basis.get("verifier_mode")
    if not mode:
        failures.append("V2: verifier_mode missing — no declared verification method")
    elif mode not in RECOGNIZED_MODES:
        failures.append(f"V2: verifier_mode {mode!r} not recognized {sorted(RECOGNIZED_MODES)}")

    # V3: recomputation evidence — two tiers, both machine-checkable.
    #   STRONG: verifier embedded its recomputation from authoritative state.
    #   RECONSTRUCTABLE: verifier named the concrete artifacts a third party
    #     needs to recompute (distinct identity + recognized mode required).
    recomputed = _first(basis, RECOMPUTE_FIELDS) or _first(data, RECOMPUTE_FIELDS)
    matches = basis.get("declared_matches_recomputation") or data.get("declared_matches_recomputation")
    tier = None
    if recomputed and matches is True:
        tier = "STRONG"
    else:
        recon = _first(data, RECONSTRUCT_FIELDS) or _first(basis, RECONSTRUCT_FIELDS)
        if recon and _names_concrete_artifacts(str(recon)):
            tier = "RECONSTRUCTABLE"
    if tier is None:
        failures.append("V3: no recomputation evidence and no concrete reconstruction path — "
                        "verifier must recompute from authoritative state or name exactly "
                        "what a third party must re-read to recompute")
    elif tier == "RECONSTRUCTABLE":
        print(f"      note V3: {path.name} meets RECONSTRUCTABLE tier (not STRONG) — "
              "recomputation not embedded")

    # V4: verifier must not trust the executor's claim.
    trusted = basis.get("executor_claim_trusted")
    if trusted is True:
        failures.append("V4: executor_claim_trusted is true — trust is not verification")

    # V5: reconstructable by a third party.
    recon = _first(data, RECONSTRUCT_FIELDS) or _first(basis, RECONSTRUCT_FIELDS)
    if not recon:
        failures.append("V5: not reconstructable — no reconstructable_by path for a third party")

    return (not failures), failures


# ---------------------------------------------------------------------------
# Self-test: the gate must PASS real receipts and FAIL fabrications.
# ---------------------------------------------------------------------------

def _fabricate_self_attested(tmp: Path) -> Path:
    p = tmp / "fabricated-self-attested.json"
    p.write_text(json.dumps({
        "schema": "FABRICATED",
        "independent_verification": True,
        "verifier_mode": "AUTHORITATIVE_REREAD_AND_RECOMPUTATION",
        # Same identity on both sides: the actor verified itself.
        "executor_runtime_jti": "same-jti-both-sides",
        "verifier_runtime_jti": "same-jti-both-sides",
        "executor_claim_trusted": True,
    }))
    return p


def _fabricate_no_recomputation(tmp: Path) -> Path:
    p = tmp / "fabricated-no-recomputation.json"
    p.write_text(json.dumps({
        "schema": "FABRICATED",
        "independent_verification": True,
        "verifier_mode": "AUTHORITATIVE_REREAD_AND_RECOMPUTATION",
        "executor_runtime_jti": "executor-aaa",
        "verifier_runtime_jti": "verifier-bbb",
        "executor_claim_trusted": False,
        # No recomputed_from_authoritative_state, no reconstructable_by.
    }))
    return p


def self_test(repo_root: Path) -> bool:
    import tempfile
    ok = True
    # Real receipts must PASS.
    real = [
        repo_root / "cold-successor-receipt-verified.json",
        repo_root / "causal-learning-experiment-receipt.json",
    ]
    for r in real:
        if not r.exists():
            print(f"SELF-TEST SKIP: {r.name} not present at {repo_root}")
            continue
        passed, failures = verify_artifact(r)
        if not passed:
            print(f"SELF-TEST FAIL: real receipt {r.name} did not pass: {failures}")
            ok = False
        else:
            print(f"SELF-TEST PASS: real receipt {r.name} verified as independent")
    # Fabrications must FAIL.
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for fab in (_fabricate_self_attested(tmp), _fabricate_no_recomputation(tmp)):
            passed, failures = verify_artifact(fab)
            if passed:
                print(f"SELF-TEST FAIL: fabrication {fab.name} PASSED — gate is broken")
                ok = False
            else:
                print(f"SELF-TEST PASS: fabrication {fab.name} correctly FAILED "
                      f"({'; '.join(failures)[:100]})")
    return ok


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("artifacts", nargs="*", help="receipt JSON files to verify")
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--root", default=".", help="repo root for self-test receipts")
    args = ap.parse_args()

    if args.self_test:
        good = self_test(Path(args.root))
        print()
        print("GATE RESULT:", "PASS — self-test green" if good else "FAIL — self-test red")
        return 0 if good else 1

    if not args.artifacts:
        ap.error("provide artifact paths or --self-test")

    all_ok = True
    for a in args.artifacts:
        passed, failures = verify_artifact(Path(a))
        if passed:
            print(f"PASS: {a} — independent verification proven")
        else:
            all_ok = False
            print(f"FAIL: {a}")
            for f in failures:
                print(f"      {f}")
    print()
    print("GATE RESULT:", "PASS" if all_ok else "FAIL — unverified claims present")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
