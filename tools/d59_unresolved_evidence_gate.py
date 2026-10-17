#!/usr/bin/env python3
"""D59 unresolved-evidence claims gate — wire the governor onto the fairness path.

The D59 governor (drift_canary/unresolved_evidence.py, PR #2313) governs
unresolved eligibility evidence: every UNDETERMINED round carries its defect
reason (MISSING / CONTRADICTORY / STALE / UNVERIFIABLE), breach is assessed
three-valued over every compatible history (a single debt number cannot hold
uncertainty), and each unresolved round spawns a reconstruction obligation
with its own attempt budget and fairness contract. This gate puts that
mechanism on a live operating path: every unresolved-evidence claim
registered in tools/d59_unresolved_evidence_manifest.json is judged by the
REAL governor, rebuilt from the claim's declared evidence. A claim that
launders uncertainty — asserting a settled conclusion where the governor
finds the histories straddling the bound, or leaving unresolved rounds with
no reconstruction coverage (the ungoverned hole D59 exists to close) — is
BLOCKED.

Exit contract (the whole point of the gate):
  0  PASS     — every registered claim certified by the governor.
  0  DORMANT  — manifest absent or registers zero claims. Explicit, never a
                false green: the gate says "nothing to judge".
  1  VIOLATION— a proven BREACH (every compatible history over the bound), a
                conclusion mismatch (unknown-laundering: settling an
                undecided obligation as clear, or the reverse), or unresolved
                rounds with no reconstruction coverage.
  2  BROKEN   — fail-closed: manifest corrupt, claim fields unparseable, or
                claims exist but the mechanism is absent (the gate refuses to
                certify on defaults — it never invents the governor).

The gate never invents fields: unknown verdicts, defect kinds, components,
conclusion values, or reconstruction states are BROKEN, not defaulted.

Directive: D59 (Governing Unresolved Eligibility Evidence, AER-LIVE-4),
wave 4, owner naya2. Wired by the night-shift WIRE lane. No merge — Shawn
pulls triggers.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent
DEFAULT_MANIFEST = TOOLS_DIR / "d59_unresolved_evidence_manifest.json"

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
    {"id", "obligation_id", "bound", "capacity_basis",
     "asserted_conclusion", "rounds"})
RECONSTRUCTION_STATES = ("open", "settled", "escalated")


class GateBroken(Exception):
    """Fail-closed: the gate cannot trust its inputs. Exit 2."""


class MechanismMissing(Exception):
    """The D59 governor is absent. Exit 2 when claims exist, else DORMANT."""


def _load_mechanism():
    """Import the REAL D59 governor plus its D58/fairness dependencies.

    Never synthesized, never defaulted. Verifies the required API surface
    so a neutered module cannot silently pass as the mechanism.
    """
    try:
        import drift_canary.unresolved_evidence as mech
        import drift_canary.eligibility_proof as eproof
        from drift_canary import fairness as fairness_mod
    except ImportError as exc:
        raise MechanismMissing(
            f"D59 mechanism not importable: {exc}")
    for attr in ("UnresolvedEvidenceGovernor", "RoundRecord",
                 "ComponentDefect", "DEFECT_KINDS", "BREACH_VERDICTS",
                 "VERDICTS", "UnresolvedEvidenceError"):
        if not hasattr(mech, attr):
            raise MechanismMissing(
                f"mechanism missing required API: {attr}")
    if not hasattr(eproof, "COMPONENTS"):
        raise MechanismMissing("eligibility_proof missing COMPONENTS")
    if not hasattr(fairness_mod, "FairnessContract"):
        raise MechanismMissing("fairness missing FairnessContract")
    return mech, eproof, fairness_mod


def _load_manifest(path):
    """Load the claims manifest. Returns None when the file is absent.

    Raises GateBroken on anything untrustworthy: bad JSON, wrong shape,
    duplicate ids, claims missing required keys.
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
        if cid in seen:
            raise GateBroken(f"duplicate claim id: {cid!r}")
        seen.add(cid)
    return data


def _as_int(value, what):
    if isinstance(value, bool) or not isinstance(value, int):
        raise GateBroken(f"{what} must be an integer, got {value!r} "
                         "(never defaulted)")
    return value


def _as_bool(value, what):
    if not isinstance(value, bool):
        raise GateBroken(f"{what} must be true/false, got {value!r} "
                         "(never defaulted)")
    return value


def _as_nonempty_str(value, what):
    if not isinstance(value, str) or not value.strip():
        raise GateBroken(f"{what} must be a non-empty string, "
                         f"got {value!r} (never defaulted)")
    return value


def _parse_defects(raw, mech, eproof, claim_id, seq):
    if not isinstance(raw, list):
        raise GateBroken(
            f"claim {claim_id} round {seq}: defects must be a list")
    defects = []
    for i, d in enumerate(raw):
        if not isinstance(d, dict):
            raise GateBroken(
                f"claim {claim_id} round {seq} defect {i}: must be an object")
        component = d.get("component")
        if component not in eproof.COMPONENTS:
            raise GateBroken(
                f"claim {claim_id} round {seq} defect {i}: unknown component "
                f"{component!r} (never defaulted)")
        kind = d.get("kind")
        if kind not in mech.DEFECT_KINDS:
            raise GateBroken(
                f"claim {claim_id} round {seq} defect {i}: unknown defect "
                f"kind {kind!r} (never defaulted)")
        detail = _as_nonempty_str(
            d.get("detail"),
            f"claim {claim_id} round {seq} defect {i} detail")
        defects.append(mech.ComponentDefect(
            component=component, kind=kind, detail=detail))
    return tuple(defects)


def _parse_rounds(raw, mech, eproof, claim_id, obligation_id):
    if not isinstance(raw, list) or not raw:
        raise GateBroken(
            f"claim {claim_id}: rounds must be a non-empty list")
    records = []
    for i, r in enumerate(raw):
        if not isinstance(r, dict):
            raise GateBroken(f"claim {claim_id} round {i}: must be an object")
        seq = _as_int(r.get("round_seq"), f"claim {claim_id} round {i} seq")
        verdict_raw = r.get("verdict")
        verdict = (verdict_raw.upper()
                   if isinstance(verdict_raw, str) else verdict_raw)
        if verdict not in mech.VERDICTS:
            raise GateBroken(
                f"claim {claim_id} round {seq}: unknown verdict "
                f"{verdict_raw!r} (never defaulted)")
        adequate = _as_bool(r.get("adequate_service"),
                            f"claim {claim_id} round {seq} adequate_service")
        defects = _parse_defects(r.get("defects", []), mech, eproof,
                                 claim_id, seq)
        if verdict == "UNDETERMINED" and not defects:
            raise GateBroken(
                f"claim {claim_id} round {seq}: UNDETERMINED must carry its "
                "defect reason(s) — the verdict never travels alone")
        if verdict != "UNDETERMINED" and defects:
            raise GateBroken(
                f"claim {claim_id} round {seq}: settled verdicts carry no "
                "defects")
        try:
            records.append(mech.RoundRecord(
                round_seq=seq,
                obligation_id=obligation_id,
                verdict=verdict,
                adequate_service=adequate,
                defects=defects,
            ))
        except (AssertionError, TypeError, ValueError) as exc:
            raise GateBroken(
                f"claim {claim_id} round {seq}: rejected by the mechanism: "
                f"{exc}")
    return records


def _parse_reconstructions(raw, claim_id):
    if raw is None:
        return {}
    if not isinstance(raw, list):
        raise GateBroken(
            f"claim {claim_id}: reconstructions must be a list")
    covered = {}
    for i, r in enumerate(raw):
        if not isinstance(r, dict):
            raise GateBroken(
                f"claim {claim_id} reconstruction {i}: must be an object")
        seq = _as_int(r.get("round_seq"),
                      f"claim {claim_id} reconstruction {i} seq")
        status = r.get("status")
        if status not in RECONSTRUCTION_STATES:
            raise GateBroken(
                f"claim {claim_id} reconstruction {i}: unknown status "
                f"{status!r} (never defaulted)")
        reason = r.get("reason", "")
        if status == "escalated":
            _as_nonempty_str(
                reason,
                f"claim {claim_id} reconstruction {i} reason")
        if seq in covered:
            raise GateBroken(
                f"claim {claim_id}: duplicate reconstruction for round {seq}")
        covered[seq] = {"status": status, "reason": reason}
    return covered


def _fraud_pattern(asserted, actual):
    """Name the defect class when the mismatch matches a known shape."""
    if asserted == "NO_BREACH" and actual == "UNRESOLVED":
        return ("unknown-laundering: the claim settles an undecided "
                "obligation as clear — collapsing the debt range to a "
                "single conclusion is the exact defect D59 exists to "
                "prevent")
    if asserted == "BREACH" and actual == "NO_BREACH":
        return ("false breach: the claim asserts a fairness breach the "
                "compatible histories clear on every completion")
    if asserted == "UNRESOLVED" and actual in ("BREACH", "NO_BREACH"):
        return (f"undecided asserted as undecided-able: the governor proves "
                f"{actual} on every compatible history — the claim "
                "manufactures doubt where the evidence settles it")
    return ""


def judge_claim(claim, mech, eproof, fairness_mod):
    """Judge one claim against the real governor. Returns a result dict."""
    claim_id = claim["id"]
    obligation_id = _as_nonempty_str(claim["obligation_id"],
                                     f"claim {claim_id} obligation_id")
    bound = _as_int(claim["bound"], f"claim {claim_id} bound")
    if bound <= 0:
        raise GateBroken(f"claim {claim_id}: bound must be positive, "
                         f"got {bound}")
    capacity_basis = _as_nonempty_str(claim["capacity_basis"],
                                      f"claim {claim_id} capacity_basis")
    asserted = claim["asserted_conclusion"]
    if asserted not in mech.BREACH_VERDICTS:
        raise GateBroken(
            f"claim {claim_id}: unknown asserted_conclusion {asserted!r} "
            "(never defaulted)")

    records = _parse_rounds(claim["rounds"], mech, eproof, claim_id,
                            obligation_id)
    reconstructions = _parse_reconstructions(claim.get("reconstructions"),
                                            claim_id)

    governor = mech.UnresolvedEvidenceGovernor()
    try:
        for record in records:
            governor.register_round(record)
    except mech.UnresolvedEvidenceError as exc:
        raise GateBroken(f"claim {claim_id}: governor refused a round: {exc}")

    try:
        contract = fairness_mod.FairnessContract(
            obligation_id=obligation_id,
            revision="d59-wire/1",
            standard="BOUNDED",
            eligibility_predicate="d59-wire: the fairness duty applies",
            service_predicate="d59-wire: adequate service",
            service_bound_rounds=bound,
            capacity_basis=capacity_basis,
        )
    except (AssertionError, TypeError, ValueError) as exc:
        raise GateBroken(
            f"claim {claim_id}: contract rejected by the mechanism: {exc}")

    try:
        assessment = governor.assess(obligation_id, contract)
    except mech.UnresolvedEvidenceError as exc:
        # The governor refuses rather than manufacturing a verdict (e.g.
        # the history space exceeds the honest-enumeration cap). The gate
        # fails closed: an unjudgeable claim is BROKEN, never passed.
        raise GateBroken(
            f"claim {claim_id}: governor refused to assess: {exc}")

    result = {
        "id": claim_id,
        "obligation_id": obligation_id,
        "asserted": asserted,
        "actual": assessment.verdict,
        "debt_min": assessment.debt_min,
        "debt_max": assessment.debt_max,
        "bound": assessment.bound,
        "histories_examined": assessment.histories_examined,
        "unresolved_rounds": list(assessment.unresolved_rounds),
        "reconstructions": reconstructions,
    }

    if assessment.verdict == "BREACH":
        result["verdict"] = "violation"
        result["reason"] = (
            f"proven BREACH: every one of "
            f"{assessment.histories_examined} compatible histories ends "
            f"over the bound (debt {assessment.debt_min}.."
            f"{assessment.debt_max} > {assessment.bound}) — blocked until "
            "the breach is repaired")
        return result
    if asserted != assessment.verdict:
        result["verdict"] = "violation"
        result["reason"] = (
            _fraud_pattern(asserted, assessment.verdict)
            or f"conclusion mismatch: asserted {asserted}, governor finds "
               f"{assessment.verdict} over {assessment.histories_examined} "
               f"histories (debt {assessment.debt_min}.."
               f"{assessment.debt_max}, bound {assessment.bound})")
        return result
    if assessment.verdict == "UNRESOLVED":
        uncovered = [s for s in assessment.unresolved_rounds
                     if s not in reconstructions]
        if uncovered:
            result["verdict"] = "violation"
            result["reason"] = (
                f"ungoverned hole: round(s) {uncovered} unresolved with no "
                "reconstruction obligation — D59 requires every UNDETERMINED "
                "round to spawn its own repair obligation; an unclaimed "
                "round is the defect this gate exists to close")
            return result
    result["verdict"] = "certified"
    return result


def _finish(exit_code, verdict, reason, results, as_json):
    payload = {"verdict": verdict, "reason": reason, "claims": results}
    if as_json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"D59 unresolved-evidence gate: {verdict} — {reason}")
        for r in results:
            line = (f"  [{r['verdict']}] {r['id']}: asserted={r['asserted']} "
                    f"actual={r['actual']} debt={r['debt_min']}.."
                    f"{r['debt_max']} bound={r['bound']}")
            if r.get("reason"):
                line += f" — {r['reason']}"
            print(line)
    return exit_code


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Judge unresolved-evidence claims against the D59 "
                    "governor.")
    parser.add_argument("--manifest",
                        default=str(DEFAULT_MANIFEST),
                        help="path to d59_unresolved_evidence_manifest.json")
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
        mech, eproof, fairness_mod = _load_mechanism()
    except MechanismMissing as exc:
        return _finish(EXIT_BROKEN, "BROKEN",
                       f"{exc}: {len(claims)} claim(s) registered but cannot "
                       "be certified — refusing to pass on defaults",
                       [], args.as_json)
    results = []
    try:
        for entry in claims:
            results.append(judge_claim(entry, mech, eproof, fairness_mod))
    except GateBroken as exc:
        return _finish(EXIT_BROKEN, "BROKEN", str(exc), results, args.as_json)
    violations = [r for r in results if r["verdict"] == "violation"]
    if violations:
        return _finish(EXIT_VIOLATION, "VIOLATION",
                       f"{len(violations)}/{len(results)} claim(s) blocked",
                       results, args.as_json)
    return _finish(EXIT_PASS, "PASS",
                   f"{len(results)} claim(s) certified by the D59 governor",
                   results, args.as_json)


if __name__ == "__main__":
    sys.exit(main())
