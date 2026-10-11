#!/usr/bin/env python3
"""D60 fairness-debt bounds gate — wire the bound engine onto the fairness path.

The D60 engine (drift_canary/fairness_debt_bounds.py, PR #2315) computes
exact lower/upper fairness-debt bounds across every independently
defensible scheduling history — in O(N), no enumeration. It closes the
gap D59 leaves open: D59's governor enumerates 2^k compatible histories
(fail-closed cap 2^12) and cannot assess a window with many unresolved
rounds, even when the unresolved rounds sit in short, independent
missing intervals where the bounds are exactly computable. This gate
puts that mechanism on a live operating path: every debt-bound claim
registered in tools/d60_fairness_debt_bounds_manifest.json is judged by
the REAL engine, rebuilt from the claim's declared evidence. A claim
that launders the bounds — asserting a settled conclusion where the
engine finds the debt interval straddling the bound, or asserting clear
where the engine proves breach — is BLOCKED.

Exit contract (the whole point of the gate):
  0  PASS     — every registered claim certified by the engine.
  0  DORMANT  — manifest absent or registers zero claims. Explicit, never a
                false green: the gate says "nothing to judge".
  1  VIOLATION— a proven BREACH (every defensible history over the bound),
                or a conclusion mismatch (bound-laundering: settling an
                undecided obligation as clear, clearing a proven breach,
                or manufacturing doubt where the evidence settles it).
  2  BROKEN   — fail-closed: manifest corrupt, claim fields unparseable,
                the engine refuses (e.g. a missing interval past the
                finite cap — D61 territory, unjudgeable here), or claims
                exist but the mechanism is absent (the gate refuses to
                certify on defaults — it never invents the engine).

The gate never invents fields: unknown verdicts, defect kinds,
components, or conclusion values are BROKEN, not defaulted.

Directive: D60 (Fairness-Debt Bounds Under Missing Evidence, AER-LIVE-5),
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
DEFAULT_MANIFEST = TOOLS_DIR / "d60_fairness_debt_bounds_manifest.json"

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


class GateBroken(Exception):
    """Fail-closed: the gate cannot trust its inputs. Exit 2."""


class MechanismMissing(Exception):
    """The D60 engine is absent. Exit 2 when claims exist, else DORMANT."""


def _load_mechanism():
    """Import the REAL D60 engine plus its D58/D59 dependencies.

    Never synthesized, never defaulted. Verifies the required API surface
    so a neutered module cannot silently pass as the mechanism.
    """
    try:
        import drift_canary.fairness_debt_bounds as d60
        import drift_canary.unresolved_evidence as ue
        import drift_canary.eligibility_proof as eproof
        from drift_canary import fairness as fairness_mod
    except ImportError as exc:
        raise MechanismMissing(
            f"D60 mechanism not importable: {exc}")
    for attr in ("DebtBoundEngine", "DebtBoundError",
                 "MissingIntervalTooLongError", "MAX_MISSING_INTERVAL_ROUNDS"):
        if not hasattr(d60, attr):
            raise MechanismMissing(
                f"mechanism missing required API: {attr}")
    for attr in ("RoundRecord", "ComponentDefect", "DEFECT_KINDS",
                 "BREACH_VERDICTS", "VERDICTS"):
        if not hasattr(ue, attr):
            raise MechanismMissing(
                f"unresolved_evidence missing required API: {attr}")
    if not hasattr(eproof, "COMPONENTS"):
        raise MechanismMissing("eligibility_proof missing COMPONENTS")
    if not hasattr(fairness_mod, "FairnessContract"):
        raise MechanismMissing("fairness missing FairnessContract")
    return d60, ue, eproof, fairness_mod


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


def _parse_defects(raw, ue, eproof, claim_id, seq):
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
        if kind not in ue.DEFECT_KINDS:
            raise GateBroken(
                f"claim {claim_id} round {seq} defect {i}: unknown defect "
                f"kind {kind!r} (never defaulted)")
        detail = _as_nonempty_str(
            d.get("detail"),
            f"claim {claim_id} round {seq} defect {i} detail")
        defects.append(ue.ComponentDefect(
            component=component, kind=kind, detail=detail))
    return tuple(defects)


def _parse_rounds(raw, ue, eproof, claim_id, obligation_id):
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
        if verdict not in ue.VERDICTS:
            raise GateBroken(
                f"claim {claim_id} round {seq}: unknown verdict "
                f"{verdict_raw!r} (never defaulted)")
        adequate = _as_bool(r.get("adequate_service"),
                            f"claim {claim_id} round {seq} adequate_service")
        defects = _parse_defects(r.get("defects", []), ue, eproof,
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
            records.append(ue.RoundRecord(
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


def _fraud_pattern(asserted, actual):
    """Name the defect class when the mismatch matches a known shape.

    Note: actual == "BREACH" never reaches here — a proven breach is
    blocked by the BREACH check first, with its own reason.
    """
    if asserted == "NO_BREACH" and actual == "UNRESOLVED":
        return ("unknown-laundering: the claim settles an undecided "
                "obligation as clear — collapsing the debt interval to a "
                "single conclusion is the exact defect D60 exists to "
                "prevent")
    if asserted == "BREACH" and actual == "NO_BREACH":
        return ("false breach: the claim asserts a fairness breach the "
                "defensible histories clear on every completion")
    if asserted == "UNRESOLVED" and actual == "NO_BREACH":
        return ("manufactured doubt: the engine proves NO_BREACH on every "
                "defensible history — the claim manufactures uncertainty "
                "where the evidence settles it")
    return ""


def judge_claim(claim, d60, ue, eproof, fairness_mod):
    """Judge one claim against the real bound engine. Returns a result dict."""
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
    if asserted not in ue.BREACH_VERDICTS:
        raise GateBroken(
            f"claim {claim_id}: unknown asserted_conclusion {asserted!r} "
            "(never defaulted)")

    records = _parse_rounds(claim["rounds"], ue, eproof, claim_id,
                            obligation_id)

    try:
        contract = fairness_mod.FairnessContract(
            obligation_id=obligation_id,
            revision="d60-wire/1",
            standard="BOUNDED",
            eligibility_predicate="d60-wire: the fairness duty applies",
            service_predicate="d60-wire: adequate service",
            service_bound_rounds=bound,
            capacity_basis=capacity_basis,
        )
    except (AssertionError, TypeError, ValueError) as exc:
        raise GateBroken(
            f"claim {claim_id}: contract rejected by the mechanism: {exc}")

    try:
        receipt = d60.DebtBoundEngine.compute(records, contract)
    except d60.DebtBoundError as exc:
        # The engine refuses rather than manufacturing bounds (e.g. a
        # missing interval past the finite cap — D61 territory). The gate
        # fails closed: an unjudgeable claim is BROKEN, never passed.
        raise GateBroken(
            f"claim {claim_id}: engine refused to bound: {exc}")

    result = {
        "id": claim_id,
        "obligation_id": obligation_id,
        "asserted": asserted,
        "actual": receipt.verdict,
        "debt_min": receipt.debt_min,
        "debt_max": receipt.debt_max,
        "bound": receipt.bound,
        "histories_admitted": receipt.histories_admitted,
        "unresolved_rounds": list(receipt.unresolved_rounds),
        "missing_intervals": len(receipt.missing_intervals),
    }

    if receipt.verdict == "BREACH":
        result["verdict"] = "violation"
        result["reason"] = (
            f"proven BREACH: every one of "
            f"{receipt.histories_admitted} defensible histories ends "
            f"over the bound (debt {receipt.debt_min}.."
            f"{receipt.debt_max} > {receipt.bound}) — blocked until "
            "the breach is repaired")
        return result
    if asserted != receipt.verdict:
        result["verdict"] = "violation"
        result["reason"] = (
            _fraud_pattern(asserted, receipt.verdict)
            or f"conclusion mismatch: asserted {asserted}, engine finds "
               f"{receipt.verdict} over {receipt.histories_admitted} "
               f"histories (debt {receipt.debt_min}.."
               f"{receipt.debt_max}, bound {receipt.bound})")
        return result
    result["verdict"] = "certified"
    return result


def _finish(exit_code, verdict, reason, results, as_json):
    payload = {"verdict": verdict, "reason": reason, "claims": results}
    if as_json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"D60 fairness-debt bounds gate: {verdict} — {reason}")
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
        description="Judge debt-bound claims against the D60 engine.")
    parser.add_argument("--manifest",
                        default=str(DEFAULT_MANIFEST),
                        help="path to d60_fairness_debt_bounds_manifest.json")
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
        d60, ue, eproof, fairness_mod = _load_mechanism()
    except MechanismMissing as exc:
        return _finish(EXIT_BROKEN, "BROKEN",
                       f"{exc}: {len(claims)} claim(s) registered but cannot "
                       "be certified — refusing to pass on defaults",
                       [], args.as_json)
    results = []
    try:
        for entry in claims:
            results.append(judge_claim(entry, d60, ue, eproof, fairness_mod))
    except GateBroken as exc:
        return _finish(EXIT_BROKEN, "BROKEN", str(exc), results, args.as_json)
    violations = [r for r in results if r["verdict"] == "violation"]
    if violations:
        return _finish(EXIT_VIOLATION, "VIOLATION",
                       f"{len(violations)}/{len(results)} claim(s) blocked",
                       results, args.as_json)
    return _finish(EXIT_PASS, "PASS",
                   f"{len(results)} claim(s) certified by the D60 engine",
                   results, args.as_json)


if __name__ == "__main__":
    sys.exit(main())
