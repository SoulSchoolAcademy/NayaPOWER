"""Learning yield / retention / mastery scorer (convergence item d).

Consumes the machines built for convergence items B and C and scores the
learning population against them:

    B  tools/learning_lineage_receipt.py   (reconstruct: one receipt per learning)
    C  tools/learning_evidence_ladder.py   (evaluate: earned E0-E7 level per learning)
    gate tools/verified_verdict_gate.py    (NAYANET_VERIFIED_VERDICT_RECEIPT_V1 --
                                           on branch naya5/verified-verdict-gate;
                                           this scorer keys to its published
                                           schema contract, not to its module)

Three scored dimensions:

  YIELD     For each of the 11 lineage stages, the share of learnings whose
            reconstructed stage is PRESENT, over the learnings where that
            stage is instrumented. Headline ratios (verification / application /
            outcome / reuse yield) with EXPLICIT denominators.
  RETENTION For learnings with a last-evidence timestamp, retained vs decayed
            against an explicit window. No timestamp -> UNKNOWN, never decayed
            by default.
  MASTERY   Ladder distribution (earned levels, never claimed) and counted
            level advancements: a transition counts only when the ladder's own
            evaluation earns the target level for that learning.

Fail-closed honesty rules (the Usefulness Gate as code):
  - No ratio is ever emitted with a zero denominator: the key is None and the
    reason is named. A 0.0 that cannot be computed is a lie with formatting.
  - An empty population scores INSUFFICIENT_DATA, not 0.0.
  - Stages with no emitter on current main (reuse / generalization / successor
    per UNINSTRUMENTED_OWNERS) yield None with reason UNINSTRUMENTED.
  - Malformed entries are skipped and NAMED in `skipped`; the scorer never
    raises on malformed input.
  - The score is evidence, never authority (the #1712 lesson): this module
    exposes no field any authority gate may accept as a grant.

BUILT_NOT_RUN: until the learning chain is live-exercised end-to-end (needs
Shawn's word: production writes + a blind scorer), there are no live
populations to score. This module is behaviorally proven on fixtures via
tests/test_learning_yield_scorer.py; live scoring is the deployment-gated
follow-up, not this commit.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

import learning_lineage_receipt as lineage
import learning_evidence_ladder as ladder

SCHEMA = "NAYANET_LEARNING_YIELD_SCORE_V1"
VERIFIED_VERDICT_SCHEMA = "NAYANET_VERIFIED_VERDICT_RECEIPT_V1"

DEFAULT_RETENTION_WINDOW_DAYS = 30


def _canonical_core(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _digest(*parts: Any) -> str:
    h = hashlib.sha256()
    for part in parts:
        h.update(_canonical_core(part).encode("utf-8"))
    return h.hexdigest()[:32]


def _parse_ts(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        ts = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    return ts


def _ratio(numerator: int, denominator: int, reason: str) -> dict[str, Any]:
    """A ratio with an explicit denominator, or an honest None."""
    if denominator <= 0:
        return {"value": None, "numerator": numerator, "denominator": denominator,
                "reason": reason}
    return {"value": numerator / denominator, "numerator": numerator,
            "denominator": denominator, "reason": "computed"}


def _check_verdict_receipt(receipt: Any, learning_id: Any) -> tuple[bool, str]:
    """Structural validation of a VERIFIED_VERDICT receipt against the
    published schema contract (the gate module lives on a branch; this
    keys to the contract, mirroring how the lineage receipt keys to D)."""
    if not isinstance(receipt, dict):
        return False, "VERDICT_ENTRY_NOT_OBJECT"
    if receipt.get("schema") != VERIFIED_VERDICT_SCHEMA:
        return False, "VERDICT_SCHEMA_MISMATCH: expected=%r actual=%r" % (
            VERIFIED_VERDICT_SCHEMA, receipt.get("schema"))
    if str(receipt.get("learning_id") or "") != str(learning_id or ""):
        return False, "VERDICT_LESSON_MISMATCH: receipt=%r learning=%r" % (
            receipt.get("learning_id"), learning_id)
    if not isinstance(receipt.get("verdict"), str):
        return False, "VERDICT_MISSING_VERDICT_FIELD"
    return True, ""


def score_population(population: dict[str, Any]) -> dict[str, Any]:
    """Score a learning population.

    population keys (all optional):
      chains               list of lineage bundles (B-receipt bundle contract)
      ladder_evaluations   list of ladder evaluation objects (C contract),
                           each with a learning_id
      verdict_receipts     list of NAYANET_VERIFIED_VERDICT_RECEIPT_V1 receipts
      level_transitions    list of {learning_id, from_level, to_level,
                           evidence_ref} advancement claims
      activity             {learning_id: {"last_evidence_at": iso-ts}}
      as_of                ISO timestamp for retention math (default: now UTC)
      retention_window_days int (default 30)
      captured_total       int | None -- population denominator from the
                           learning store; when absent, denominators fall
                           back to the supplied chains and say so

    Never raises on malformed input. Returns the score object.
    """
    pop = population if isinstance(population, dict) else {}
    skipped: list[str] = []

    chains = pop.get("chains")
    chains = chains if isinstance(chains, list) else []
    evaluations = pop.get("ladder_evaluations")
    evaluations = evaluations if isinstance(evaluations, list) else []
    verdict_receipts = pop.get("verdict_receipts")
    verdict_receipts = verdict_receipts if isinstance(verdict_receipts, list) else []
    transitions = pop.get("level_transitions")
    transitions = transitions if isinstance(transitions, list) else []
    activity = pop.get("activity")
    activity = activity if isinstance(activity, dict) else {}

    captured_total = pop.get("captured_total")
    if not isinstance(captured_total, int) or captured_total < 0:
        captured_total = None

    # ---- empty population: the honest answer is INSUFFICIENT_DATA ----
    if not chains and captured_total is None:
        return _score_object(
            verdict="INSUFFICIENT_DATA",
            note="no chains and no captured_total supplied: nothing to score",
            skipped=skipped, digest_seed={"empty": True},
        )

    # ---- reconstruct every chain through the B receipt ----
    receipts: list[dict[str, Any]] = []
    for i, bundle in enumerate(chains):
        try:
            receipt = lineage.reconstruct(bundle)
        except Exception as exc:  # fail-closed: reconstruct promises never to raise,
            skipped.append("chain[%d]: reconstruct raised (%s)" % (i, type(exc).__name__))
            continue
        if not isinstance(receipt, dict):
            skipped.append("chain[%d]: reconstruct returned non-object" % i)
            continue
        receipts.append(receipt)

    # ---- index ladder evaluations + verdict receipts by learning ----
    earned_by_learning: dict[str, dict[str, Any]] = {}
    for i, ev in enumerate(evaluations):
        if not isinstance(ev, dict) or ev.get("schema") != ladder.SCHEMA:
            skipped.append("ladder_evaluations[%d]: not a ladder evaluation object" % i)
            continue
        lid = str(ev.get("learning_id") or "")
        if not lid:
            skipped.append("ladder_evaluations[%d]: missing learning_id" % i)
            continue
        earned_by_learning[lid] = ev

    valid_verdicts: dict[str, dict[str, Any]] = {}
    for i, vr in enumerate(verdict_receipts):
        if not isinstance(vr, dict):
            skipped.append("verdict_receipts[%d]: VERDICT_ENTRY_NOT_OBJECT" % i)
            continue
        lid = str(vr.get("learning_id") or "")
        ok, reason = _check_verdict_receipt(vr, lid if lid else None)
        if not ok:
            skipped.append("verdict_receipts[%d]: %s" % (i, reason))
            continue
        valid_verdicts[lid] = vr

    # ---- YIELD: per-stage PRESENT over instrumented ----
    stage_counts: dict[str, dict[str, int]] = {
        s: {"present": 0, "instrumented": 0} for s in lineage.STAGES
    }
    verdicts_seen: list[str] = []
    for receipt in receipts:
        stages = receipt.get("stages") or {}
        if not isinstance(stages, dict):
            skipped.append("receipt %r: stages not an object" % receipt.get("learning_id"))
            continue
        verdicts_seen.append(str(receipt.get("verdict") or ""))
        for stage in lineage.STAGES:
            s = stages.get(stage)
            if not isinstance(s, dict):
                continue
            status = s.get("status")
            if status == "UNINSTRUMENTED":
                continue  # never an instrumented stage
            stage_counts[stage]["instrumented"] += 1
            if status == "PRESENT":
                stage_counts[stage]["present"] += 1

    stage_yield: dict[str, dict[str, Any]] = {}
    for stage in lineage.STAGES:
        counts = stage_counts[stage]
        if counts["instrumented"] == 0:
            stage_yield[stage] = {"value": None,
                                  "reason": "UNINSTRUMENTED: no emitter on current main "
                                            "(owner: %s)" % lineage.UNINSTRUMENTED_OWNERS.get(stage, "unknown")}
        else:
            stage_yield[stage] = _ratio(counts["present"], counts["instrumented"], "computed")

    # Headline yields: verification / application / outcome / reuse.
    # Denominator is the supplied chains unless captured_total is known.
    head_denom = captured_total if captured_total is not None else len(receipts)
    denom_reason = ("captured_total from learning store"
                    if captured_total is not None else "supplied chains (captured_total unknown)")
    headline: dict[str, dict[str, Any]] = {}
    for stage, key in (("verification", "verification_yield"),
                       ("application", "application_yield"),
                       ("outcome", "outcome_yield"),
                       ("reuse", "reuse_yield")):
        counts = stage_counts[stage]
        if counts["instrumented"] == 0:
            headline[key] = {"value": None, "numerator": 0, "denominator": head_denom,
                             "reason": "UNINSTRUMENTED stage: no emitter on current main"}
        else:
            r = _ratio(counts["present"], head_denom,
                       denom_reason if head_denom > 0 else "no chains scored")
            headline[key] = r

    # Verified-verdict yield: receipts stamped by the 5-point gate.
    verified_positives = sum(1 for vr in valid_verdicts.values()
                             if str(vr.get("verdict") or "").upper() == "VERIFIED")
    headline["verified_verdict_yield"] = _ratio(
        verified_positives, head_denom,
        denom_reason if head_denom > 0 else "no chains scored")
    headline["verified_verdict_receipts"] = {
        "valid": len(valid_verdicts), "positive": verified_positives,
        "invalid_skipped": sum(1 for s in skipped if "verdict_receipts" in s),
    }

    # ---- RETENTION ----
    window_days = pop.get("retention_window_days")
    if not isinstance(window_days, int) or window_days <= 0:
        window_days = DEFAULT_RETENTION_WINDOW_DAYS
    as_of = _parse_ts(pop.get("as_of")) or datetime.now(timezone.utc)
    retained = decayed = unknown = 0
    for receipt in receipts:
        lid = str(receipt.get("learning_id") or "")
        entry = activity.get(lid)
        ts = _parse_ts(entry.get("last_evidence_at")) if isinstance(entry, dict) else None
        if ts is None:
            unknown += 1
        elif (as_of - ts).days <= window_days:
            retained += 1
        else:
            decayed += 1
    retention_denom = retained + decayed
    retention = {
        "window_days": window_days,
        "retained": retained,
        "decayed": decayed,
        "unknown": unknown,
        "retention_share": _ratio(retained, retention_denom,
                                 "computed over timestamped learnings" if retention_denom
                                 else "no learnings carry last_evidence_at: retention unscorable"),
    }

    # ---- MASTERY: earned-level distribution + counted advancements ----
    distribution: dict[str, int] = {lvl: 0 for lvl in ladder.LEVEL_ORDER}
    distribution["UNPROVEN"] = 0
    claimed_overrides = 0
    for lid, ev in earned_by_learning.items():
        earned = str(ev.get("earned_level") or "UNPROVEN")
        distribution[earned] = distribution.get(earned, 0) + 1
        claimed = ev.get("claimed_level")
        if claimed and claimed != earned:
            claimed_overrides += 1
    eval_denom = len(earned_by_learning)
    mastered = distribution.get("E6_RETAINED", 0) + distribution.get("E7_MASTERED", 0)
    mastery = {
        "distribution": distribution,
        "evaluated": eval_denom,
        "mastered_share": _ratio(mastered, eval_denom,
                                "E6+E7 over ladder-evaluated learnings" if eval_denom
                                else "no ladder evaluations supplied: mastery unscorable"),
        "claimed_above_earned": claimed_overrides,
    }

    # Advancements count only when the ladder itself earns the target level.
    advanced = 0
    advanced_claims = 0
    for i, tr in enumerate(transitions):
        if not isinstance(tr, dict):
            skipped.append("level_transitions[%d]: not an object" % i)
            continue
        lid = str(tr.get("learning_id") or "")
        to_level = str(tr.get("to_level") or "")
        ev = earned_by_learning.get(lid)
        if ev is None:
            skipped.append("level_transitions[%d]: no ladder evaluation for %r" % (i, lid))
            continue
        advanced_claims += 1
        if str(ev.get("earned_level") or "") == to_level and to_level in ladder.LEVEL_ORDER:
            advanced += 1
    mastery["advancements"] = {
        "counted": advanced,
        "claims": advanced_claims,
        "share": _ratio(advanced, advanced_claims,
                        "counted over claimed with ladder evidence" if advanced_claims
                        else "no level transitions supplied"),
    }

    # ---- population verdict ----
    n = len(receipts)
    if any(v == "BROKEN" for v in verdicts_seen):
        pop_verdict = "BROKEN"
        note = "at least one reconstructed chain is BROKEN; see stage yields"
    elif all(v == "COMPLETE" for v in verdicts_seen) and n:
        pop_verdict = "COMPLETE"
        note = "every scored chain reconstructs COMPLETE"
    else:
        pop_verdict = "PARTIAL"
        note = ("chains scored=%d; reuse/generalization/successor are UNINSTRUMENTED "
                "on current main so COMPLETE is unreachable until successor lanes emit"
                % n)

    score = _score_object(
        verdict=pop_verdict, note=note, skipped=skipped,
        digest_seed={
            "chains": n,
            "evaluations": eval_denom,
            "verdict_receipts": len(valid_verdicts),
            "stage_present": {s: stage_counts[s]["present"] for s in lineage.STAGES},
        },
    )
    score["population"] = {
        "chains_scored": n,
        "chains_supplied": len(chains),
        "captured_total": captured_total,
        "denominator_basis": ("captured_total" if captured_total is not None
                              else "supplied chains"),
    }
    score["yield"] = {"stages": stage_yield, "headline": headline}
    score["retention"] = retention
    score["mastery"] = mastery
    return score


def _score_object(verdict: str, note: str, skipped: list[str],
                  digest_seed: dict[str, Any]) -> dict[str, Any]:
    score_id = "YLD-" + _digest(SCHEMA, verdict, digest_seed)
    return {
        "schema": SCHEMA,
        "score_id": score_id,
        "verdict": verdict,
        "note": note,
        "skipped": skipped,
    }


def summarize(score: dict[str, Any]) -> str:
    """One-line human summary of a yield score."""
    y = (score.get("yield") or {}).get("headline") or {}
    parts = []
    for key in ("verification_yield", "application_yield", "outcome_yield", "reuse_yield"):
        r = y.get(key) or {}
        v = r.get("value")
        parts.append("%s=%s" % (key, "n/a" if v is None else "%.2f" % v))
    m = (score.get("mastery") or {}).get("mastered_share") or {}
    mv = m.get("value")
    parts.append("mastered=%s" % ("n/a" if mv is None else "%.2f" % mv))
    ret = (score.get("retention") or {}).get("retention_share") or {}
    rv = ret.get("value")
    parts.append("retained=%s" % ("n/a" if rv is None else "%.2f" % rv))
    return ("yield-score %s | %s | %s | skipped=%d"
            % (score.get("score_id"), score.get("verdict"), " ".join(parts),
               len(score.get("skipped") or [])))
