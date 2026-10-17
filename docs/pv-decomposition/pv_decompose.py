"""Reference implementation for PV-DECOMPOSITION-SPEC-0.1 (CANDIDATE, unwired).

Takes a term-list JSON (see worked-example-2576-repair.json) and emits the
decomposition receipt. Deterministic: no randomness, no hidden defaults,
round-half-even to 6dp applied once at component level.

Usage: python3 pv_decompose.py <terms.json>
"""

from __future__ import annotations

import json
import sys
from decimal import Decimal, ROUND_HALF_EVEN

SPEC_VERSION = "PV-DECOMP-0.1"
BUCKETS = ("B", "H", "C", "R")
UNITS = ("value_points", "hours", "usd", "count", "probability")
FIXED_RATES = {"value_points": 1.0}  # DEFAULT_RATE_TABLE v0.1: only fixed rate
Q6 = Decimal("0.000001")


def _r6(x: float) -> float:
    return float(Decimal(str(x)).quantize(Q6, rounding=ROUND_HALF_EVEN))


def _clamp(x: float, lo: float = 0.0, hi: float = 10.0) -> float:
    return max(lo, min(hi, x))


def normalize_term(t: dict) -> float:
    """Normalize() per spec section 4. Raises ValueError on any spec violation."""
    tid = t.get("id", "?")
    bucket = t.get("bucket")
    if bucket not in BUCKETS:
        raise ValueError(f"term {tid}: bad bucket {bucket!r}")
    unit = t.get("unit")
    if unit not in UNITS:
        raise ValueError(f"term {tid}: unknown unit {unit!r} (fail-closed)")
    conf = t.get("confidence")
    if not isinstance(conf, (int, float)) or not 0.0 <= conf <= 1.0:
        raise ValueError(f"term {tid}: confidence must be in [0,1]")

    if unit == "probability":
        if bucket != "R":
            raise ValueError(f"term {tid}: probability unit only valid in R bucket")
        sev = t.get("severity_0_10")
        prob = t.get("probability")
        if sev is None or prob is None:
            raise ValueError(f"term {tid}: R/probability term needs severity_0_10 + probability")
        if not 0.0 <= float(sev) <= 10.0 or not 0.0 <= float(prob) <= 1.0:
            raise ValueError(f"term {tid}: severity in [0,10], probability in [0,1]")
        return _clamp(float(sev) * float(prob))

    rate = t.get("unit_rate", FIXED_RATES.get(unit))
    if rate is None:
        raise ValueError(f"term {tid}: unit {unit!r} needs a stated unit_rate (no silent default)")
    rate = float(rate)
    if rate <= 0:
        raise ValueError(f"term {tid}: unit_rate must be > 0")
    raw = float(t["raw_magnitude"])
    if raw < 0:
        raise ValueError(f"term {tid}: raw_magnitude must be >= 0 (deltas are unsigned; sign lives in the bucket)")
    return _clamp(raw * rate)


def decompose(doc: dict) -> dict:
    if doc.get("spec_version") != SPEC_VERSION:
        raise ValueError(f"spec_version must be {SPEC_VERSION}")
    terms = doc["terms"]
    if not terms:
        raise ValueError("term list must be non-empty")

    # Distinct-evidence rule (anti-gaming): one fact, one term.
    seen_refs = set()
    for t in terms:
        ref = t.get("evidence_ref") or t.get("quote_span")
        if not ref:
            raise ValueError(f"term {t.get('id', '?')}: needs evidence_ref or quote_span")
        if ref in seen_refs:
            raise ValueError(f"duplicate evidence ref (term-splitting): {ref[:60]!r}")
        seen_refs.add(ref)

    comp = {b: 0.0 for b in BUCKETS}
    comp_conf = {b: 1.0 for b in BUCKETS}
    term_out = []
    buckets_seen = set()
    for t in terms:
        n = normalize_term(t)
        b = t["bucket"]
        buckets_seen.add(b)
        comp[b] += n
        comp_conf[b] = min(comp_conf[b], float(t["confidence"]))
        entry = {"id": t["id"], "bucket": b, "normalized": _r6(n)}
        if b == "R" and t["unit"] == "probability":
            sev, prob = float(t["severity_0_10"]), float(t["probability"])
            entry["risk_policy_trip"] = sev >= 9.0 and prob >= 0.01
        term_out.append(entry)

    # Zero Value Law: empty bucket is UNMEASURED (confidence 0.0) unless the
    # receipt carries an explicit zero_attestation {scope, confidence}.
    attest = doc.get("zero_attestations", {}) or {}
    for b in BUCKETS:
        if b not in buckets_seen:
            a = attest.get(b)
            if a is None:
                comp_conf[b] = 0.0
            else:
                c = a.get("confidence")
                if not isinstance(c, (int, float)) or not 0.0 <= c <= 1.0:
                    raise ValueError(f"zero_attestation[{b}]: confidence must be in [0,1]")
                if not a.get("scope"):
                    raise ValueError(f"zero_attestation[{b}]: scope required")
                comp_conf[b] = float(c)

    result = {b: _r6(comp[b]) for b in BUCKETS}
    # pv mirrors kernel/value_calculus.py PVEstimate.pv with uncertainty_scale=1.0
    # (min over ALL four components, matching min_component_confidence's .get(k, 0.0))
    min_conf = min(comp_conf[b] for b in BUCKETS)
    residual = max(result["R"], 1.0 * (1.0 - min_conf))
    pv = _r6(result["B"] - result["H"] - result["C"] - residual)
    return {
        "spec_version": SPEC_VERSION,
        "decision_id": doc.get("decision_id"),
        "baseline_id": doc.get("baseline_id"),
        "terms": term_out,
        "B": result["B"], "H": result["H"], "C": result["C"], "R": result["R"],
        "component_confidence": {b: _r6(comp_conf[b]) for b in BUCKETS},
        "evidence_count": len(terms),
        "pv": pv,
    }


def main() -> None:
    doc = json.load(open(sys.argv[1]))
    print(json.dumps(decompose(doc), indent=2))


if __name__ == "__main__":
    main()
