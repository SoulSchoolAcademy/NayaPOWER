#!/usr/bin/env python3
"""
Learning Loop — Layer 6 of the Ultimate Decision Machine.

The machine improves itself from experience. Every decision writes a receipt;
later, the actual outcome is recorded. Over time the loop measures:

  - calibration: was predicted confidence honest?
    (90% confident but right only 60% of the time = miscalibrated)
  - overweighting: which dimensions score too high on decisions that failed?
  - blind spots: which kinds of decisions does it consistently get wrong?

The loop LEARNS; it never self-modifies. Weight adjustments are PROPOSALS —
candidate records requiring explicit independent acceptance. Nothing here
changes scoring silently. A proposal is a suggestion with evidence, not an edit.

Fail-closed throughout:
  - unknown outcomes never count as successes (or failures) — excluded
  - insufficient history says "not enough data", never an invented trend
  - corrupted ledger lines are quarantined, never parsed optimistically
  - append-only: receipts are never mutated; corrections are new receipts
    referencing the old via "supersedes"
  - an outcome for an unknown receipt_id is rejected, not dangled
  - zero network calls. Local reasoning only.

Ledger: one JSONL file, three record types: "decision", "outcome",
"weight_proposal". Every line is one JSON object.

Usage:
  python3 tools/learning_loop.py write-receipt --scored '<json>' --intent '<json>' [--ledger PATH] [--supersedes ID]
  python3 tools/learning_loop.py record-outcome --receipt ID --actual SUCCESS|PARTIAL|FAILURE|UNKNOWN --observed-by SELF_REPORTED|OBSERVED|VERIFIED [--note TEXT] [--ledger PATH]
  python3 tools/learning_loop.py calibrate [--ledger PATH]
  python3 tools/learning_loop.py propose-weights [--ledger PATH]
  python3 tools/learning_loop.py accept-proposal --proposal ID --by NAME [--ledger PATH]
  python3 tools/learning_loop.py reject-proposal --proposal ID --by NAME [--ledger PATH]
  python3 tools/learning_loop.py show-ledger [--ledger PATH]

Exit codes:
  0 — ok
  1 — error (bad input, unknown id, unreadable ledger)
  2 — honest "not enough data" (calibrate / propose-weights with insufficient history)
"""

import argparse
import hashlib
import json
import os
import secrets
import sys
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCHEMA_VERSION = "1"
DEFAULT_LEDGER = "learning_ledger.jsonl"

# Outcome labels — canonical uppercase, exactly as the Compass product spec
# requires: SELF_REPORTED / OBSERVED / VERIFIED. Input is accepted
# case-insensitively and normalized to canonical.
ACTUAL_LABELS = ("SUCCESS", "PARTIAL", "FAILURE", "UNKNOWN")
OBSERVED_BY_LABELS = ("SELF_REPORTED", "OBSERVED", "VERIFIED")

# Numeric value of a known outcome for calibration math. UNKNOWN is never
# mapped — it is excluded from every rate, never counted as success.
OUTCOME_SCORE = {"SUCCESS": 1.0, "PARTIAL": 0.5, "FAILURE": 0.0}

# Calibration bins over predicted confidence (whole-percent display elsewhere;
# bins here are honest ranges, low edge inclusive).
CALIBRATION_BINS = [(0.50, 0.60), (0.60, 0.70), (0.70, 0.80),
                    (0.80, 0.90), (0.90, 1.01)]

MIN_DECISIONS_FOR_CALIBRATION = 10   # fewer → "not enough data"
MIN_DECISIONS_FOR_PROPOSAL = 20      # weight proposals need more evidence
MIN_SUCCESS_N = 5                    # per-group minimums for overweighting signals
MIN_FAILURE_N = 3
OVERWEIGHT_GAP = 0.15                # mean_failed - mean_success above this → signal

# Conservative tuning bounds. A proposal may only shrink an overweighted
# dimension by PROPOSAL_SHRINK, never below WEIGHT_FLOOR, never above
# WEIGHT_CAP. Renormalized to sum 1.0 afterwards.
PROPOSAL_SHRINK = 0.90
WEIGHT_FLOOR = 0.05
WEIGHT_CAP = 0.60

DIMENSIONS = ["mission_value", "evidence", "risk", "cost", "urgency"]


# ---------------------------------------------------------------------------
# Small utilities
# ---------------------------------------------------------------------------

def now_utc():
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix):
    return f"{prefix}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}-{secrets.token_hex(3)}"


def _as_dict(v):
    return v if isinstance(v, dict) else {}


def _as_list(v):
    return v if isinstance(v, list) else []


def _as_num(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def _as_str(v, default=""):
    return v if isinstance(v, str) else default


def canon_label(value, allowed, name):
    """Normalize a label case-insensitively to canonical uppercase.

    Raises ValueError on anything not in the allowed set — never guess.
    """
    if not isinstance(value, str):
        raise ValueError(f"{name} must be a string, got {type(value).__name__}")
    up = value.strip().upper()
    if up not in allowed:
        raise ValueError(
            f"{name} must be one of {list(allowed)}, got {value!r}")
    return up


def option_fingerprint(opt):
    """Stable identity for an option across receipts.

    Built from the option's own provenance fields — the same real-world
    option described twice gets the same fingerprint.
    """
    opt = _as_dict(opt)
    raw = "|".join([
        _as_str(opt.get("id")),
        _as_str(opt.get("title")),
        _as_str(opt.get("source")),
        _as_str(opt.get("source_type")),
    ])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12]


def snapshot_id_from(intent, scored):
    """Best-effort world-model snapshot id. Honest null when absent."""
    intent = _as_dict(intent)
    scored = _as_dict(scored)
    for holder in (intent, _as_dict(intent.get("world_context")), scored):
        sid = holder.get("snapshot_id") or holder.get("snapshot_utc")
        if isinstance(sid, str) and sid.strip():
            return sid.strip()
    return None


# ---------------------------------------------------------------------------
# Decision receipts — append-only
# ---------------------------------------------------------------------------

def normalize_dimension(d):
    """One scored dimension, defensively normalized. Mirrors Layer 5's shape."""
    d = _as_dict(d)
    return {
        "value": _as_num(d.get("value")),
        "confidence": _as_num(d.get("confidence")) or 0.0,
        "evidence": [_as_str(e) for e in _as_list(d.get("evidence"))],
    }


def normalize_option(opt):
    """One scored option as the receipt stores it — with fingerprint."""
    opt = _as_dict(opt)
    dims = _as_dict(opt.get("dimensions"))
    return {
        "id": opt.get("id"),
        "title": _as_str(opt.get("title")),
        "source": _as_str(opt.get("source")),
        "source_type": _as_str(opt.get("source_type")),
        "fingerprint": option_fingerprint(opt),
        "gated": bool(opt.get("gated", False)),
        "gate_reasons": [_as_str(r) for r in _as_list(opt.get("gate_reasons"))],
        "rank": opt.get("rank"),
        "dimensions": {k: normalize_dimension(dims.get(k)) for k in DIMENSIONS},
        "total": _as_num(opt.get("total")),
        "total_confidence": _as_num(opt.get("total_confidence")),
        "unknown_dimensions": [_as_str(u) for u in _as_list(opt.get("unknown_dimensions"))],
    }


def build_receipt(scored, intent, supersedes=None):
    """Build a decision receipt from Layer 4's scored output + Layer 2 intent.

    Never throws on ragged input — missing pieces become honest nulls, and
    a decision with no recommendation predicts nothing (excluded from
    calibration, not scored as a guess).
    """
    scored = _as_dict(scored)
    intent = _as_dict(intent)
    if supersedes is not None and not isinstance(supersedes, str):
        raise ValueError("supersedes must be a receipt_id string or null")

    options = [normalize_option(o) for o in _as_list(scored.get("options"))]
    rec = _as_dict(scored.get("recommendation"))
    recommendation = None
    predicted_confidence = None
    range_warning = None
    weights_warning = None
    weights = _as_dict(scored.get("weights"))
    if weights:
        wsum = sum(v for v in weights.values()
                   if isinstance(v, (int, float)) and not isinstance(v, bool))
        if abs(wsum - 1.0) > 0.01:
            weights_warning = (
                f"recorded weights sum to {round(wsum, 4)}, not 1.0 — "
                f"upstream scoring bug suspected; kept as recorded")
    if rec.get("option_id") is not None:
        recommendation = {
            "option_id": rec.get("option_id"),
            "title": _as_str(rec.get("title")),
            "total": _as_num(rec.get("total")),
            "total_confidence": _as_num(rec.get("total_confidence")),
        }
        predicted_confidence = _as_num(rec.get("total_confidence"))
        if predicted_confidence is not None and not (0.0 <= predicted_confidence <= 1.0):
            # The receipt records what the machine SAID — even an absurd
            # confidence is data (it signals an upstream bug). Flag it,
            # don't silently drop or clamp it.
            range_warning = (
                f"predicted_confidence {predicted_confidence} outside [0,1] — "
                f"upstream scoring bug suspected; kept as recorded")

    return {
        "record_type": "decision",
        "schema_version": SCHEMA_VERSION,
        "receipt_id": new_id("rcpt"),
        "written_utc": now_utc(),
        "supersedes": supersedes,
        "intent": {
            "intent_type": intent.get("intent_type"),
            "objective": _as_str(intent.get("objective")),
            "snapshot_id": snapshot_id_from(intent, scored),
            "decision_weight": intent.get("decision_weight"),
            "stakes": intent.get("stakes"),
        },
        "weights": _as_dict(scored.get("weights")),
        "weights_schema_version": scored.get("weights_schema_version"),
        "options": options,
        "recommendation": recommendation,
        # The machine bets its recommendation succeeds. No recommendation →
        # no prediction → excluded from calibration (never scored as a guess).
        "predicted_confidence": predicted_confidence,
        "predicted_outcome": "success" if recommendation else None,
        "notes": [_as_str(n) for n in _as_list(scored.get("notes"))],
        "warnings": ([_as_str(w) for w in _as_list(scored.get("warnings"))]
                     + ([range_warning] if range_warning else [])
                     + ([weights_warning] if weights_warning else [])),
    }


def build_outcome_record(receipt_id, actual, observed_by, note=""):
    """An outcome is a separate record linked to a receipt — the receipt
    itself is never mutated."""
    return {
        "record_type": "outcome",
        "schema_version": SCHEMA_VERSION,
        "outcome_id": new_id("outc"),
        "receipt_id": receipt_id,
        "recorded_utc": now_utc(),
        "actual": canon_label(actual, ACTUAL_LABELS, "actual"),
        "observed_by": canon_label(observed_by, OBSERVED_BY_LABELS, "observed_by"),
        "note": _as_str(note),
    }


# ---------------------------------------------------------------------------
# Ledger I/O — append-only file, corrupted lines quarantined
# ---------------------------------------------------------------------------

def load_ledger(path):
    """Load every record from the JSONL ledger.

    Returns (records, quarantined). A quarantined entry is a dict with
    line_no, raw snippet, and reason — corrupted lines are reported, never
    parsed optimistically, and never silently dropped.
    """
    records = []
    quarantined = []
    if not os.path.exists(path):
        return records, quarantined
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            s = line.strip()
            if not s:
                continue
            try:
                obj = json.loads(s)
            except json.JSONDecodeError as e:
                quarantined.append({
                    "line_no": i, "reason": f"invalid JSON: {e}",
                    "raw": s[:200],
                })
                continue
            if not isinstance(obj, dict) or obj.get("record_type") not in (
                    "decision", "outcome", "weight_proposal",
                    "proposal_decision"):
                quarantined.append({
                    "line_no": i,
                    "reason": "missing or unknown record_type",
                    "raw": s[:200],
                })
                continue
            if obj.get("schema_version") != SCHEMA_VERSION:
                quarantined.append({
                    "line_no": i,
                    "reason": f"unsupported schema_version {obj.get('schema_version')!r}",
                    "raw": s[:200],
                })
                continue
            records.append(obj)
    return records, quarantined


def append_record(path, record):
    """Append one record. The file is never rewritten — append-only.

    An exclusive advisory lock guards the append so concurrent workers
    cannot interleave lines. Locking is best-effort on platforms without
    fcntl (the write itself is still a single append).
    """
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)
    line = json.dumps(record, sort_keys=True) + "\n"
    with open(path, "a", encoding="utf-8") as f:
        try:
            import fcntl
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                f.write(line)
                f.flush()
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        except ImportError:
            f.write(line)
    return record


def index_receipts(records):
    """Map receipt_id → decision record. On duplicate ids (should not happen)
    the FIRST written wins — append-only means the original stands."""
    idx = {}
    for r in records:
        if r.get("record_type") == "decision":
            idx.setdefault(r.get("receipt_id"), r)
    return idx


def index_outcomes(records):
    """Map receipt_id → list of outcome records (a receipt may be observed
    more than once; e.g. self-reported then verified)."""
    idx = {}
    for r in records:
        if r.get("record_type") == "outcome":
            idx.setdefault(r.get("receipt_id"), []).append(r)
    return idx


def latest_outcome(outcomes):
    """The most recently recorded outcome wins. Ties → last in file order."""
    if not outcomes:
        return None
    return max(outcomes, key=lambda o: o.get("recorded_utc", ""))


def resolve_corrections(receipts):
    """Follow supersedes chains to the latest correction of each decision.

    Returns (live_ids, id_to_live, anomalies):
      - live_ids: receipt_ids that count for calibration (superseded
        originals are retired, not double-counted).
      - id_to_live: maps EVERY receipt_id (including retired ones) to its
        live head — so outcomes recorded against an original transfer to
        the live correction instead of being dropped.
    A cycle or a dangling supersedes reference is fail-closed: the chain is
    left at the original and the anomaly is reported, never looped.
    """
    by_id = {r.get("receipt_id"): r for r in receipts}
    superseded_by = {}
    anomalies = []
    for r in receipts:
        sup = r.get("supersedes")
        if sup:
            if sup == r.get("receipt_id"):
                anomalies.append(f"receipt {r.get('receipt_id')} supersedes itself")
                continue
            if sup not in by_id:
                anomalies.append(
                    f"receipt {r.get('receipt_id')} supersedes unknown {sup}")
                continue
            superseded_by[sup] = r.get("receipt_id")

    def live_head(rid):
        seen = {rid}
        cur = rid
        while cur in superseded_by:
            cur = superseded_by[cur]
            if cur in seen:
                anomalies.append(f"supersedes cycle at {cur}")
                break
            seen.add(cur)
        return cur

    id_to_live = {r.get("receipt_id"): live_head(r.get("receipt_id"))
                  for r in receipts}
    live_ids = sorted(set(id_to_live.values()))
    return live_ids, id_to_live, anomalies


# ---------------------------------------------------------------------------
# Calibration — was predicted confidence honest?
# ---------------------------------------------------------------------------

def _known_outcome_value(outcome):
    """Numeric value of an outcome, or None for UNKNOWN/missing.

    UNKNOWN is excluded from every rate — it never counts as success
    and never counts as failure. That is the fail-closed rule.
    """
    if not outcome:
        return None
    actual = outcome.get("actual")
    if actual == "UNKNOWN":
        return None
    return OUTCOME_SCORE.get(actual)


def calibration_data(records):
    """Join live decision receipts with their latest known outcomes.

    Returns (samples, meta) where each sample is
    (predicted_confidence, outcome_value, receipt_id, intent_type).
    Only decisions that made a recommendation with a predicted confidence
    AND have a known (non-UNKNOWN) outcome are included.
    """
    decisions = [r for r in records if r.get("record_type") == "decision"]
    outcomes = index_outcomes(records)
    live_ids, id_to_live, anomalies = resolve_corrections(decisions)
    live = {r.get("receipt_id"): r for r in decisions
            if r.get("receipt_id") in live_ids}
    # Outcomes transfer to the live head of their correction chain, so an
    # outcome observed against an original is not dropped when the receipt
    # is corrected. Latest recorded outcome wins per live decision.
    outcomes_by_live = {}
    for rid, olist in outcomes.items():
        head = id_to_live.get(rid, rid)
        outcomes_by_live.setdefault(head, []).extend(olist)
    samples = []
    for rid in live_ids:
        r = live.get(rid)
        if not r:
            continue
        pc = _as_num(r.get("predicted_confidence"))
        if pc is None:
            continue  # no recommendation → nothing was predicted
        val = _known_outcome_value(latest_outcome(outcomes_by_live.get(rid, [])))
        if val is None:
            continue  # UNKNOWN or unobserved → excluded, never assumed
        samples.append({
            "predicted": pc,
            "value": val,
            "receipt_id": rid,
            "intent_type": _as_dict(r.get("intent")).get("intent_type"),
        })
    return samples, {"anomalies": anomalies,
                     "quarantine_note": "see load_ledger"}


def bin_index(predicted):
    """Bin a predicted confidence. Always returns a bin — out-of-range
    predictions clamp to the nearest edge bin rather than vanishing
    from the math."""
    for i, (lo, hi) in enumerate(CALIBRATION_BINS):
        if lo <= predicted < hi:
            return i
    if predicted < CALIBRATION_BINS[0][0]:
        return 0
    return len(CALIBRATION_BINS) - 1


def calibration_report(records):
    """Calibration report over the ledger.

    Honest about sample size: fewer than MIN_DECISIONS_FOR_CALIBRATION
    decisions with known outcomes → status "insufficient_data", no verdict.
    """
    samples, meta = calibration_data(records)
    n = len(samples)
    report = {
        "status": "ok" if n >= MIN_DECISIONS_FOR_CALIBRATION else "insufficient_data",
        "n_decisions": n,
        "min_required": MIN_DECISIONS_FOR_CALIBRATION,
        "bins": [],
        "expected_calibration_error": None,
        "verdict": None,
        "anomalies": meta["anomalies"],
    }
    if report["status"] != "ok":
        report["verdict"] = (
            f"not enough data — {n} decided outcomes, "
            f"need {MIN_DECISIONS_FOR_CALIBRATION}")
        return report

    bins = []
    for i, (lo, hi) in enumerate(CALIBRATION_BINS):
        in_bin = [s for s in samples if bin_index(s["predicted"]) == i]
        if not in_bin:
            bins.append({"range": [lo, round(hi, 2)], "n": 0,
                         "mean_predicted": None, "observed_rate": None,
                         "gap": None})
            continue
        mean_p = sum(s["predicted"] for s in in_bin) / len(in_bin)
        obs = sum(s["value"] for s in in_bin) / len(in_bin)
        bins.append({"range": [lo, round(hi, 2)], "n": len(in_bin),
                     "mean_predicted": round(mean_p, 3),
                     "observed_rate": round(obs, 3),
                     "gap": round(abs(obs - mean_p), 3)})
    report["bins"] = bins
    ece = sum((b["n"] / n) * b["gap"] for b in bins if b["n"])
    report["expected_calibration_error"] = round(ece, 3)
    if ece < 0.10:
        report["verdict"] = "calibrated — predicted confidence matches outcomes"
    elif ece < 0.20:
        report["verdict"] = "watch — confidence drifts from outcomes, investigate"
    else:
        report["verdict"] = "miscalibrated — confidence does not match outcomes"
    return report


def overweighting_signals(records):
    """Per-dimension signals: does a dimension score high on failures?

    For each dimension, compare its mean value on SUCCESS decisions vs
    FAILURE decisions (PARTIAL counts in neither group — it is neither).
    A dimension averaging clearly higher on failures than on successes is
    either overweighted or mis-scored. Minimum group sizes apply; anything
    smaller reports "insufficient data for this dimension", not a signal.
    """
    samples, _ = calibration_data(records)
    decisions = {r.get("receipt_id"): r for r in records
                 if r.get("record_type") == "decision"}
    # Transfer outcomes to live correction heads (same rule as calibration).
    raw_outcomes = index_outcomes(records)
    _, id_to_live, _ = resolve_corrections(
        [r for r in records if r.get("record_type") == "decision"])
    outcomes_by_live = {}
    for rid, olist in raw_outcomes.items():
        outcomes_by_live.setdefault(id_to_live.get(rid, rid), []).extend(olist)
    signals = []
    for dim in DIMENSIONS:
        succ_vals, fail_vals = [], []
        for s in samples:
            r = decisions.get(s["receipt_id"])
            if not r:
                continue
            # find the recommended option's dimension value
            rec_id = _as_dict(r.get("recommendation")).get("option_id")
            opt = next((o for o in _as_list(r.get("options"))
                        if o.get("id") == rec_id), None)
            if not opt:
                continue
            val = _as_num(_as_dict(_as_dict(opt.get("dimensions")).get(dim)).get("value"))
            if val is None:
                continue
            actual = (latest_outcome(outcomes_by_live.get(s["receipt_id"], []))
                      or {}).get("actual")
            if actual == "SUCCESS":
                succ_vals.append(val)
            elif actual == "FAILURE":
                fail_vals.append(val)
        entry = {"dimension": dim, "n_success": len(succ_vals),
                 "n_failure": len(fail_vals)}
        if len(succ_vals) < MIN_SUCCESS_N or len(fail_vals) < MIN_FAILURE_N:
            entry["status"] = "insufficient_data"
            signals.append(entry)
            continue
        mean_s = sum(succ_vals) / len(succ_vals)
        mean_f = sum(fail_vals) / len(fail_vals)
        entry["mean_on_success"] = round(mean_s, 3)
        entry["mean_on_failure"] = round(mean_f, 3)
        entry["gap"] = round(mean_f - mean_s, 3)
        if entry["gap"] >= OVERWEIGHT_GAP:
            entry["status"] = "overweighted_signal"
            entry["message"] = (
                f"{dim} averages {entry['mean_on_failure']} on failed decisions "
                f"vs {entry['mean_on_success']} on successful ones "
                f"(gap {entry['gap']} ≥ {OVERWEIGHT_GAP}) — scores high where "
                f"it should discriminate; candidate for a weight reduction")
        else:
            entry["status"] = "ok"
        signals.append(entry)
    return signals


def blind_spot_report(records):
    """Success rate per intent type — where does the machine get it wrong?

    Only intent types with ≥5 decided outcomes are reported; smaller groups
    say "insufficient data" rather than inventing a pattern.
    """
    samples, _ = calibration_data(records)
    by_type = {}
    for s in samples:
        t = s["intent_type"] or "unknown_intent"
        by_type.setdefault(t, []).append(s["value"])
    spots = []
    for t, vals in sorted(by_type.items()):
        entry = {"intent_type": t, "n": len(vals)}
        if len(vals) < 5:
            entry["status"] = "insufficient_data"
        else:
            rate = sum(vals) / len(vals)
            entry["success_rate"] = round(rate, 3)
            entry["status"] = "blind_spot" if rate < 0.5 else "ok"
            if entry["status"] == "blind_spot":
                entry["message"] = (
                    f"{t}: success rate {entry['success_rate']} over "
                    f"{len(vals)} decisions — the machine consistently "
                    f"gets this kind of decision wrong")
        spots.append(entry)
    return spots


# ---------------------------------------------------------------------------
# Weight proposals — conservative, never silent
# ---------------------------------------------------------------------------

def propose_weight_adjustments(records):
    """Propose weight adjustments from calibration evidence.

    Conservative by construction:
      - only dimensions with an overweighting signal AND enough history
      - shrink by PROPOSAL_SHRINK, bounded by WEIGHT_FLOOR / WEIGHT_CAP
      - renormalized to sum 1.0
      - returned as a PROPOSAL RECORD — applying it requires an explicit,
        independent accept_proposal call. This function changes nothing.
    """
    samples, _ = calibration_data(records)
    n = len(samples)
    if n < MIN_DECISIONS_FOR_PROPOSAL:
        return {"status": "insufficient_data",
                "n_decisions": n,
                "min_required": MIN_DECISIONS_FOR_PROPOSAL,
                "message": f"not enough data — {n} decided outcomes, "
                           f"need {MIN_DECISIONS_FOR_PROPOSAL}"}
    signals = overweighting_signals(records)
    flagged = [s for s in signals if s.get("status") == "overweighted_signal"]
    if not flagged:
        return {"status": "no_adjustment",
                "n_decisions": n,
                "message": "no dimension shows an overweighting signal — "
                           "weights stand"}

    # Current weights: from the most recent decision receipt that has them.
    decisions = [r for r in records if r.get("record_type") == "decision"]
    current = {}
    current_schema = None
    for r in reversed(decisions):
        w = _as_dict(r.get("weights"))
        if w:
            current = {k: _as_num(v) for k, v in w.items()
                       if k in DIMENSIONS and _as_num(v) is not None}
            current_schema = r.get("weights_schema_version")
            break
    if not current:
        return {"status": "insufficient_data",
                "message": "no receipt carries weights to adjust"}

    adjustments = {}
    proposed = dict(current)
    for s in flagged:
        dim = s["dimension"]
        old = proposed.get(dim)
        if old is None:
            continue
        new = max(WEIGHT_FLOOR, min(WEIGHT_CAP, old * PROPOSAL_SHRINK))
        new = round(new, 4)
        if new != old:
            adjustments[dim] = {
                "old": old, "new": new,
                "reason": s.get("message", "overweighting signal"),
            }
            proposed[dim] = new
    if not adjustments:
        return {"status": "no_adjustment",
                "message": "signals present but weights already at bounds"}
    total = sum(proposed.values())
    renormalized = {k: round(v / total, 4) for k, v in proposed.items()}
    for dim, adj in adjustments.items():
        adj["new_renormalized"] = renormalized[dim]

    return {
        "status": "proposed",
        "proposal": {
            "record_type": "weight_proposal",
            "schema_version": SCHEMA_VERSION,
            "proposal_id": new_id("prop"),
            "created_utc": now_utc(),
            "based_on": {
                "n_decisions": n,
                "min_required": MIN_DECISIONS_FOR_PROPOSAL,
                "weights_schema_version": current_schema,
                "calibration_ece": calibration_report(records).get(
                    "expected_calibration_error"),
            },
            "adjustments": adjustments,
            "renormalized_weights": renormalized,
            "bounds": {"shrink": PROPOSAL_SHRINK, "floor": WEIGHT_FLOOR,
                       "cap": WEIGHT_CAP},
            "status": "proposed",
            "decided_by": None,
            "decided_utc": None,
            "note": "PROPOSAL ONLY — requires explicit independent acceptance "
                    "via accept-proposal before any scoring weights change. "
                    "This record changes nothing by itself.",
        },
    }


def build_proposal_decision(proposal_id, decided_by, accept):
    """Accept or reject a weight proposal — as a NEW append-only record.

    The proposal record itself is never mutated. The effective status of a
    proposal is its latest proposal_decision record, or "proposed" when
    none exists. Explicit human (or independent seat) action is the only
    path from proposed to accepted.
    """
    if not isinstance(proposal_id, str) or not proposal_id:
        raise ValueError("proposal_id must be a non-empty string")
    if not isinstance(decided_by, str) or not decided_by.strip():
        raise ValueError("decided_by must name who decided")
    return {
        "record_type": "proposal_decision",
        "schema_version": SCHEMA_VERSION,
        "decision_id": new_id("pdec"),
        "proposal_id": proposal_id,
        "decision": "accepted" if accept else "rejected",
        "decided_by": decided_by.strip(),
        "decided_utc": now_utc(),
    }


def proposal_status(records, proposal_id):
    """Effective status of a proposal: latest decision wins, else 'proposed'."""
    proposal = next(
        (r for r in records
         if r.get("record_type") == "weight_proposal"
         and r.get("proposal_id") == proposal_id), None)
    if proposal is None:
        raise ValueError(f"unknown proposal_id {proposal_id!r}")
    decisions = [r for r in records
                 if r.get("record_type") == "proposal_decision"
                 and r.get("proposal_id") == proposal_id]
    if not decisions:
        return "proposed"
    latest = max(decisions, key=lambda d: d.get("decided_utc", ""))
    return "accepted" if latest.get("decision") == "accepted" else "rejected"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _read_json_arg(value, name):
    if value == "-":
        raw = sys.stdin.read()
    else:
        raw = value
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"{name} is not valid JSON: {e}")


def _out(obj):
    print(json.dumps(obj, indent=2, sort_keys=True))


def _err(message):
    print(json.dumps({"ok": False, "error": message}, sort_keys=True),
          file=sys.stderr)


def cmd_write_receipt(args):
    try:
        scored = _read_json_arg(args.scored, "--scored")
        intent = _read_json_arg(args.intent, "--intent") if args.intent else {}
        receipt = build_receipt(scored, intent, supersedes=args.supersedes)
    except ValueError as e:
        _err(str(e))
        return 1
    append_record(args.ledger, receipt)
    _out({"ok": True, "receipt_id": receipt["receipt_id"],
          "ledger": os.path.abspath(args.ledger),
          "predicted_confidence": receipt["predicted_confidence"]})
    return 0


def cmd_record_outcome(args):
    try:
        records, quarantined = load_ledger(args.ledger)
    except OSError as e:
        _err(f"cannot read ledger: {e}")
        return 1
    idx = index_receipts(records)
    if args.receipt not in idx:
        _err(f"unknown receipt_id {args.receipt!r} — outcome rejected, "
             f"not dangled")
        return 1
    try:
        rec = build_outcome_record(args.receipt, args.actual,
                                   args.observed_by, args.note or "")
    except ValueError as e:
        _err(str(e))
        return 1
    append_record(args.ledger, rec)
    if quarantined:
        print(json.dumps({"quarantined_lines": len(quarantined)},
                         sort_keys=True), file=sys.stderr)
    _out({"ok": True, "outcome_id": rec["outcome_id"],
          "receipt_id": args.receipt, "actual": rec["actual"],
          "observed_by": rec["observed_by"]})
    return 0


def cmd_calibrate(args):
    try:
        records, quarantined = load_ledger(args.ledger)
    except OSError as e:
        _err(f"cannot read ledger: {e}")
        return 1
    report = calibration_report(records)
    report["quarantined_lines"] = len(quarantined)
    report["overweighting"] = overweighting_signals(records)
    report["blind_spots"] = blind_spot_report(records)
    _out(report)
    return 0 if report["status"] == "ok" else 2


def cmd_propose_weights(args):
    try:
        records, quarantined = load_ledger(args.ledger)
    except OSError as e:
        _err(f"cannot read ledger: {e}")
        return 1
    result = propose_weight_adjustments(records)
    if result["status"] == "proposed":
        append_record(args.ledger, result["proposal"])
        _out({"ok": True,
              "proposal_id": result["proposal"]["proposal_id"],
              "adjustments": result["proposal"]["adjustments"],
              "renormalized_weights":
                  result["proposal"]["renormalized_weights"],
              "note": result["proposal"]["note"]})
        return 0
    _out({"ok": False, **result})
    return 2


def cmd_decide_proposal(args, accept):
    try:
        records, quarantined = load_ledger(args.ledger)
    except OSError as e:
        _err(f"cannot read ledger: {e}")
        return 1
    try:
        current = proposal_status(records, args.proposal)
    except ValueError as e:
        _err(str(e))
        return 1
    if current != "proposed":
        _err(f"proposal {args.proposal} is already {current} — "
             f"decisions are append-only, not re-decided")
        return 1
    try:
        rec = build_proposal_decision(args.proposal, args.by, accept)
    except ValueError as e:
        _err(str(e))
        return 1
    append_record(args.ledger, rec)
    _out({"ok": True, "proposal_id": args.proposal,
          "decision": rec["decision"], "decided_by": rec["decided_by"]})
    return 0


def cmd_show_ledger(args):
    try:
        records, quarantined = load_ledger(args.ledger)
    except OSError as e:
        _err(f"cannot read ledger: {e}")
        return 1
    counts = {}
    for r in records:
        counts[r["record_type"]] = counts.get(r["record_type"], 0) + 1
    samples, meta = calibration_data(records)
    # effective proposal statuses (latest decision wins, else "proposed")
    proposals = {}
    for r in records:
        if r.get("record_type") == "weight_proposal":
            pid = r.get("proposal_id")
            try:
                proposals[pid] = proposal_status(records, pid)
            except ValueError:
                proposals[pid] = "unknown"
    _out({
        "ok": True,
        "ledger": os.path.abspath(args.ledger),
        "records": len(records),
        "by_type": counts,
        "quarantined_lines": len(quarantined),
        "decisions_with_known_outcomes": len(samples),
        "proposal_statuses": proposals,
        "correction_anomalies": meta["anomalies"],
    })
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Learning loop — Layer 6 of the Ultimate Decision Machine")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def _add_ledger(p):
        p.add_argument("--ledger", default=DEFAULT_LEDGER,
                       help="JSONL ledger path")

    p = sub.add_parser("write-receipt")
    _add_ledger(p)
    p.add_argument("--scored", required=True,
                   help="Layer 4 score_options() JSON (or - for stdin)")
    p.add_argument("--intent", default="",
                   help="Layer 2 intent JSON (or - for stdin)")
    p.add_argument("--supersedes", default=None,
                   help="receipt_id this receipt corrects")

    p = sub.add_parser("record-outcome")
    _add_ledger(p)
    p.add_argument("--receipt", required=True)
    p.add_argument("--actual", required=True,
                   help="SUCCESS|PARTIAL|FAILURE|UNKNOWN")
    p.add_argument("--observed-by", required=True,
                   help="SELF_REPORTED|OBSERVED|VERIFIED")
    p.add_argument("--note", default="")

    p = sub.add_parser("calibrate")
    _add_ledger(p)
    p = sub.add_parser("propose-weights")
    _add_ledger(p)

    p = sub.add_parser("accept-proposal")
    _add_ledger(p)
    p.add_argument("--proposal", required=True)
    p.add_argument("--by", required=True)

    p = sub.add_parser("reject-proposal")
    _add_ledger(p)
    p.add_argument("--proposal", required=True)
    p.add_argument("--by", required=True)

    p = sub.add_parser("show-ledger")
    _add_ledger(p)

    args = ap.parse_args(argv)
    handlers = {
        "write-receipt": cmd_write_receipt,
        "record-outcome": cmd_record_outcome,
        "calibrate": cmd_calibrate,
        "propose-weights": cmd_propose_weights,
        "accept-proposal": lambda a: cmd_decide_proposal(a, True),
        "reject-proposal": lambda a: cmd_decide_proposal(a, False),
        "show-ledger": cmd_show_ledger,
    }
    return handlers[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
