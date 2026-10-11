#!/usr/bin/env python3
"""D61 unbounded-debt bounds gate — wire the engine onto the fairness path.

The D61 mechanism (drift_canary/unbounded_debt_bounds.py, PR #2316) is the
unbounded missing-interval debt law (AER-LIVE-6): an unbounded scheduling
gap is a constrained set of possible event sequences — never an asserted
fact — and the verdict answers off the PEAK, never the final. The flagship
fraud is the AER-LIVE-006 mutation: the terminal service S clears the
counter (final debt 0), so a compliance claim that examines only the final
debt declares NO_BREACH over an interval whose attainable peak is
one-to-infinity. The independent verifier refuses it — final-debt-only
evidence cannot establish compliance, because the peak is the controlling
quantity and a later service reset never erases a possible earlier breach.

This gate puts that mechanism on a live operating path: every compliance
claim registered in tools/d61_unbounded_debt_manifest.json is cold-judged by
the REAL D61 engine, reconstructed from the claim's own interval + contract
+ finite-limit bytes. A claim the law refuses — final-debt-only NO_BREACH,
NO_BREACH against an unbounded peak, a circular finite limit (the SLA under
test as its own evidence), an inadmissible limit source, a claim
inconsistent with its receipt, an unjudgeable contract — is BLOCKED. The
gate also dogfoods the mechanism's own integrity: every judged receipt is
re-checked against the verdict-off-peak coherence rules, and the mechanism's
own receipt invariants failing means the mechanism is broken — the gate
fails closed, never certifies on a broken engine.

OPERATING PATH (what this protects and how to verify it stays connected):
  Path: the fairness CI path — any PR touching
  drift_canary/unbounded_debt_bounds.py, drift_canary/fairness.py, this
  gate, its manifest, or its tests.
  Trigger: the unbounded-debt-gate check on pull_request / push-to-main.
  Block: check red (exit 1 VIOLATION or exit 2 BROKEN) blocks the merge path.
  Defect class: compliance claims over unbounded missing intervals that the
  D61 law refuses — final-debt-only NO_BREACH (AER-LIVE-006), NO_BREACH
  against an unbounded peak, circular finite limits, inadmissible limit
  sources, receipt-inconsistent claims.
  Verify-still-connected: `python tools/d61_unbounded_debt_gate.py --json`
  must exit 0 DORMANT on a claim-free tree; registering the manifest's
  worked DB-EXAMPLE claim must exit 1 naming FinalDebtOnlyClaimError;
  claims present with the mechanism deleted must exit 2. If the workflow
  file disappears from .github/workflows/, the path is unwired — re-add it.

Exit contract (the whole point of the gate):
  0  PASS     — every registered claim certified by the cold engine.
  0  DORMANT  — manifest absent or registers zero claims. Explicit, never a
                false green: the gate says "nothing to judge".
  1  VIOLATION— a claim BLOCKED: the law refuses it (the mechanism raises
                one of its fail-closed UnboundedDebtError refusals —
                FinalDebtOnlyClaimError, PeakUnboundedClaimError,
                ClaimMismatchError, CircularEvidenceError,
                UnknownLimitSourceError, UnboundedContractError,
                ContractObligationMismatchError — or the claim's own
                parameters are unjudgeable). The mechanism's own words name
                the refusal.
  2  BROKEN   — fail-closed: manifest corrupt, claim fields untrustworthy,
                an unknown assertion value, claims exist but the mechanism
                is absent, or the mechanism's own verdict-off-peak
                invariants broke (receipt coherence dogfood failed). The
                gate never invents the engine and never defaults an unknown.

The gate never invents fields: unknown assertions, malformed shapes, or
missing keys are BROKEN, not defaulted. Claim CONTENT refused by the law is
VIOLATION, not BROKEN — the distinction is whose trust broke: the
manifest's (BROKEN) or the claim's (VIOLATION).

Structural note: the gate binds contract.obligation_id = claim
obligation_id, so cross-obligation judgment (ContractObligationMismatch)
is structurally impossible through the gate — the protection holds by
construction, not by test.

Directive: D61 (Fairness-Debt Bounds for Unbounded Missing Intervals,
AER-LIVE-6, Naya 3's intel #2175/6102429215), owner naya2. Wired by the
night-shift WIRE lane. No merge — the merge lane owns it.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent
DEFAULT_MANIFEST = TOOLS_DIR / "d61_unbounded_debt_manifest.json"

# The mechanism lives in the drift_canary package at the repo root. The
# workflow runs this script as `python tools/...` (script dir on sys.path,
# not the repo root), so the root is appended explicitly. Appended — not
# prepended — so a test/battery overlay earlier on sys.path (or PYTHONPATH)
# keeps winning; the repo root is the fallback, never an override.
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

EXIT_PASS = 0
EXIT_VIOLATION = 1
EXIT_BROKEN = 2

REQUIRED_CLAIM_KEYS = frozenset(
    {"id", "obligation_id", "claimant", "evidence_ref",
     "asserts", "interval", "contract", "evidence"})
ASSERTIONS = ("NO_BREACH", "BREACH", "UNRESOLVED")

REQUIRED_INTERVAL_KEYS = frozenset(
    {"entry_debt_lo", "entry_debt_hi", "must_end_with_service"})
REQUIRED_CONTRACT_KEYS = frozenset(
    {"revision", "standard", "eligibility_predicate", "service_predicate",
     "service_bound_rounds", "capacity_basis"})
REQUIRED_LIMIT_KEYS = frozenset(
    {"source", "max_unserved_rounds", "evidence_ref"})

# API surface the gate depends on. A neutered module that lacks any of
# these cannot silently pass as the mechanism.
MECH_ATTRS = (
    "UnboundedDebtEngine", "verify_compliance_claim",
    "UnboundedInterval", "FiniteLimit",
    "UnboundedDebtError", "UnboundedContractError",
    "ContractObligationMismatchError", "UnknownLimitSourceError",
    "CircularEvidenceError", "FinalDebtOnlyClaimError",
    "PeakUnboundedClaimError", "ClaimMismatchError",
    "BREACH", "NO_BREACH", "UNRESOLVED",
    "PROVEN_UNBOUNDED", "NO_FINITE_BOUND_ESTABLISHED",
    "FINITE_LIMIT_ESTABLISHED", "FINITE_LIMIT_SOURCES", "VERDICTS",
)


class GateBroken(Exception):
    """Fail-closed: the gate cannot trust its inputs. Exit 2."""


class MechanismMissing(Exception):
    """The D61 engine is absent. Exit 2 when claims exist, else DORMANT."""


def _load_mechanism():
    """Import the REAL D61 engine. Never synthesized, never defaulted.

    Verifies the required API surface so a neutered module cannot silently
    pass as the mechanism. FairnessContract comes from the real
    drift_canary.fairness seam the mechanism itself composes with.
    """
    try:
        import drift_canary.unbounded_debt_bounds as mech
    except ImportError as exc:
        raise MechanismMissing(f"D61 mechanism not importable: {exc}")
    for attr in MECH_ATTRS:
        if not hasattr(mech, attr):
            raise MechanismMissing(
                f"mechanism missing required API: {attr}")
    try:
        from drift_canary.fairness import FairnessContract
    except ImportError as exc:
        raise MechanismMissing(
            f"D61 mechanism's fairness seam not importable: {exc}")
    return mech, FairnessContract


def _load_manifest(path):
    """Load the claims manifest. Returns None when the file is absent.

    Raises GateBroken on anything untrustworthy: bad JSON, wrong shape,
    duplicate ids, claims missing required keys, non-string identity
    fields, unknown assertions, non-dict interval/contract/evidence.
    Value semantics (debt ranges, bound coherence, limit admissibility)
    belong to the mechanism at judge time — the manifest loader checks
    structure, never law.
    """
    p = Path(path)
    if not p.is_file():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        raise GateBroken(f"manifest is not valid JSON: {exc}")
    if not isinstance(data, dict) or not isinstance(data.get("claims"), list):
        raise GateBroken("manifest must be an object with a 'claims' list")
    seen = set()
    for entry in data["claims"]:
        if not isinstance(entry, dict):
            raise GateBroken("every claim must be an object")
        missing = REQUIRED_CLAIM_KEYS - set(entry.keys())
        if missing:
            raise GateBroken(
                f"claim missing required keys: {sorted(missing)}")
        cid = entry["id"]
        _as_nonempty_str(cid, "claim id")
        if cid in seen:
            raise GateBroken(f"duplicate claim id: {cid!r}")
        seen.add(cid)
        for key in ("obligation_id", "claimant", "evidence_ref"):
            _as_nonempty_str(entry[key], f"claim {cid} {key}")
        asserts = entry["asserts"]
        if asserts not in ASSERTIONS:
            raise GateBroken(
                f"claim {cid}: unknown asserts {asserts!r} (never defaulted)")
        for key in ("interval", "contract", "evidence"):
            if not isinstance(entry[key], dict):
                raise GateBroken(
                    f"claim {cid}: {key} must be an object")
        _check_shape(cid, "interval", entry["interval"],
                     REQUIRED_INTERVAL_KEYS)
        _check_shape(cid, "contract", entry["contract"],
                     REQUIRED_CONTRACT_KEYS)
        limit = entry.get("finite_limit")
        if limit is not None:
            if not isinstance(limit, dict):
                raise GateBroken(f"claim {cid}: finite_limit must be an "
                                 "object")
            _check_shape(cid, "finite_limit", limit, REQUIRED_LIMIT_KEYS)
    return data


def _check_shape(cid, what, obj, required):
    missing = required - set(obj.keys())
    if missing:
        raise GateBroken(
            f"claim {cid}: {what} missing required keys: "
            f"{sorted(missing)}")


def _as_nonempty_str(value, what):
    if not isinstance(value, str) or not value.strip():
        raise GateBroken(f"{what} must be a non-empty string, "
                         f"got {value!r} (never defaulted)")
    return value


def _build_objects(claim, mech, FairnessContract):
    """Rebuild the law's inputs from the claim's own bytes.

    Raises the mechanism's own fail-closed refusals (UnboundedDebtError
    subclasses) when the claim's parameters are unjudgeable — those become
    VIOLATION at judge time. Raises AssertionError only when the claim's
    contract params break the fairness seam's own asserts — also the
    claim's fault, also VIOLATION.
    """
    cid = claim["id"]
    obligation_id = claim["obligation_id"]
    iv = claim["interval"]
    interval = mech.UnboundedInterval(
        obligation_id=obligation_id,
        entry_debt_lo=iv["entry_debt_lo"],
        entry_debt_hi=iv["entry_debt_hi"],
        must_end_with_service=bool(iv["must_end_with_service"]),
    )
    co = claim["contract"]
    # contract.obligation_id is bound to the claim's obligation_id by
    # construction — cross-obligation judgment is structurally impossible
    # through this gate.
    try:
        contract = FairnessContract(
            obligation_id=obligation_id,
            revision=co["revision"],
            standard=co["standard"],
            eligibility_predicate=co["eligibility_predicate"],
            service_predicate=co["service_predicate"],
            service_bound_rounds=co["service_bound_rounds"],
            capacity_basis=co["capacity_basis"],
        )
    except AssertionError as exc:
        raise mech.UnboundedDebtError(
            f"claim {cid}: contract parameters break the fairness seam: "
            f"{exc}")
    finite_limit = None
    tested_sla_ref = claim.get("tested_sla_ref", "")
    if not isinstance(tested_sla_ref, str):
        raise mech.UnboundedDebtError(
            f"claim {cid}: tested_sla_ref must be a string")
    raw_limit = claim.get("finite_limit")
    if raw_limit is not None:
        finite_limit = mech.FiniteLimit(
            source=raw_limit["source"],
            max_unserved_rounds=raw_limit["max_unserved_rounds"],
            evidence_ref=raw_limit["evidence_ref"],
        )
    return interval, contract, finite_limit, tested_sla_ref


def _dogfood_receipt_coherence(receipt, mech, claim_id):
    """Re-check the verdict-off-peak coherence on every judged receipt.

    The mechanism's own __post_init__ asserts these; this is the gate's
    explicit statement of what it depends on. A receipt that violates them
    means the ENGINE is broken — fail closed (GateBroken), never certify.
    """
    ok = True
    detail = ""
    if receipt.verdict == mech.BREACH:
        ok = receipt.peak_lower_bound > receipt.bound
        detail = (f"BREACH needs peak_lower_bound > bound, got "
                  f"{receipt.peak_lower_bound} vs {receipt.bound}")
    elif receipt.verdict == mech.NO_BREACH:
        ok = (receipt.finite_limit is not None
              and receipt.peak_upper_bound is not None
              and receipt.peak_upper_bound <= receipt.bound)
        detail = ("NO_BREACH needs a finite limit and peak_upper_bound <= "
                  f"bound, got limit={receipt.finite_limit is not None}, "
                  f"upper={receipt.peak_upper_bound}, bound={receipt.bound}")
    elif receipt.verdict == mech.UNRESOLVED:
        ok = not (receipt.peak_lower_bound > receipt.bound)
        detail = (f"UNRESOLVED contradicts a proven peak breach: "
                  f"peak_lower_bound {receipt.peak_lower_bound} > bound "
                  f"{receipt.bound}")
    else:
        ok = False
        detail = f"unknown verdict {receipt.verdict!r}"
    if receipt.peak_status not in (
            mech.PROVEN_UNBOUNDED, mech.NO_FINITE_BOUND_ESTABLISHED,
            mech.FINITE_LIMIT_ESTABLISHED):
        ok = False
        detail = f"interchanged peak status {receipt.peak_status!r}"
    if not ok:
        raise GateBroken(
            f"claim {claim_id}: mechanism integrity broken — receipt "
            f"violates verdict-off-peak coherence ({detail})")


def judge_claim(claim, mech, FairnessContract):
    """Judge one claim against the real cold engine. Returns a result dict.

    VIOLATION (exit 1) when the law refuses the claim — the mechanism's
    own UnboundedDebtError words name the refusal. BROKEN (exit 2) when
    the engine's own invariants break.
    """
    claim_id = claim["id"]
    obligation_id = claim["obligation_id"]
    asserts = claim["asserts"]
    evidence = claim["evidence"]

    # Rebuild the law's inputs from the claim's own bytes. The law's
    # fail-closed refusals (bad debt range, non-BOUNDED contract,
    # inadmissible limit source) mean the claim is unjudgeable — BLOCKED.
    try:
        interval, contract, finite_limit, tested_sla_ref = _build_objects(
            claim, mech, FairnessContract)
    except mech.UnboundedDebtError as exc:
        return {
            "id": claim_id, "obligation_id": obligation_id,
            "asserted": asserts, "actual": "UNJUDGEABLE",
            "verdict": "violation",
            "reason": (f"the law refuses the claim's own parameters: "
                       f"{type(exc).__name__}: {exc}"),
        }

    # Cold assessment by the REAL engine. Its own invariant asserts
    # firing means the engine is broken — fail closed, never certify.
    try:
        receipt = mech.UnboundedDebtEngine.assess(
            interval, contract, finite_limit, tested_sla_ref)
    except AssertionError as exc:
        raise GateBroken(
            f"claim {claim_id}: mechanism integrity broken — the engine's "
            f"own invariants fired: {exc}")
    except mech.UnboundedDebtError as exc:
        return {
            "id": claim_id, "obligation_id": obligation_id,
            "asserted": asserts, "actual": "UNJUDGEABLE",
            "verdict": "violation",
            "reason": (f"the law refuses to assess this claim: "
                       f"{type(exc).__name__}: {exc}"),
        }

    # Dogfood the mechanism's integrity: verdict-off-peak coherence must
    # hold on every judged receipt, or the engine is broken.
    _dogfood_receipt_coherence(receipt, mech, claim_id)

    # The independent verifier: accepts or refuses the compliance claim.
    try:
        outcome = mech.verify_compliance_claim(receipt, asserts, evidence)
    except mech.UnboundedDebtError as exc:
        return {
            "id": claim_id, "obligation_id": obligation_id,
            "asserted": asserts, "actual": receipt.verdict,
            "verdict": "violation",
            "reason": (f"independent verifier REFUSED the claim: "
                       f"{type(exc).__name__}: {exc}"),
        }
    assert outcome == "ACCEPTED", outcome  # the verifier's only pass word

    return {
        "id": claim_id, "obligation_id": obligation_id,
        "claimant": claim["claimant"], "evidence_ref": claim["evidence_ref"],
        "asserted": asserts, "actual": receipt.verdict,
        "peak_status": receipt.peak_status,
        "peak_lower_bound": receipt.peak_lower_bound,
        "peak_upper_bound": receipt.peak_upper_bound,
        "verdict": "certified",
        "reason": (f"cold engine ACCEPTED: receipt verdict {receipt.verdict}, "
                   f"peak {receipt.peak_status} "
                   f"[{receipt.peak_lower_bound}, "
                   f"{receipt.peak_upper_bound}], bound {receipt.bound}"),
    }


def _finish(exit_code, verdict, reason, results, as_json):
    payload = {"verdict": verdict, "reason": reason, "claims": results}
    if as_json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"D61 unbounded-debt gate: {verdict} — {reason}")
        for r in results:
            line = (f"  [{r['verdict']}] {r['id']}: asserted={r['asserted']} "
                    f"actual={r['actual']}")
            if r.get("reason"):
                line += f" — {r['reason']}"
            print(line)
    return exit_code


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Judge unbounded-interval compliance claims against "
                    "the D61 engine.")
    parser.add_argument("--manifest",
                        default=str(DEFAULT_MANIFEST),
                        help="path to d61_unbounded_debt_manifest.json")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="machine-readable output")
    args = parser.parse_args(argv)

    try:
        data = _load_manifest(args.manifest)
    except GateBroken as exc:
        return _finish(EXIT_BROKEN, "BROKEN", str(exc), [], args.as_json)
    if data is None:
        return _finish(EXIT_PASS, "DORMANT",
                       "manifest absent: nothing to judge (explicit)",
                       [], args.as_json)
    claims = data["claims"]
    if not claims:
        return _finish(EXIT_PASS, "DORMANT",
                       "manifest registers zero claims: nothing to judge "
                       "(explicit, not a false green)",
                       [], args.as_json)
    try:
        mech, FairnessContract = _load_mechanism()
    except MechanismMissing as exc:
        return _finish(EXIT_BROKEN, "BROKEN",
                       f"{exc}: {len(claims)} claim(s) registered but cannot "
                       "be certified — refusing to pass on defaults",
                       [], args.as_json)
    results = []
    try:
        for entry in claims:
            results.append(judge_claim(entry, mech, FairnessContract))
    except GateBroken as exc:
        return _finish(EXIT_BROKEN, "BROKEN", str(exc), results, args.as_json)
    violations = [r for r in results if r["verdict"] == "violation"]
    if violations:
        return _finish(EXIT_VIOLATION, "VIOLATION",
                       f"{len(violations)}/{len(results)} claim(s) blocked",
                       results, args.as_json)
    return _finish(EXIT_PASS, "PASS",
                   f"{len(results)} claim(s) certified by the D61 engine",
                   results, args.as_json)


if __name__ == "__main__":
    sys.exit(main())
