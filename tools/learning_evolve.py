"""EVOLVE node — the compounding measurement instrument.

Naya 1's definition: EVOLVE measures whether future decisions improve,
preserves successful learning, corrects wrong lessons, and makes the next
learning cycle more effective.

This module is pure: no DB, no network. It consumes a lesson plus the
lesson\'s recorded application history (application receipts + outcome
records, the instrument from tools/learning_application_receipt.py) and
produces:

  (a) an improvement measurement — did decisions that applied this lesson
      outperform the no-lesson baseline? (delta_vs_baseline, with an honest
      UNKNOWN when no baseline was supplied)
  (b) a preservation verdict — KEEP | FLAG_FOR_REVIEW | CORRECT
  (c) correction records — when a lesson proves wrong in a verified
      application, one correction record per falsifying observation.

THE CORRECTION LIFECYCLE (the mechanism, not a suggestion):

  Wrong lessons are never silently overwritten and never deleted. A
  correction record is emitted as a NEW record with lifecycle_state
  PENDING_ADMISSION carrying the SUPERSEDES edge back to the original.
  Only apply_supersession() performs the atomic transition, and only when
  the correction has been admitted: the original goes ACTIVE -> SUPERSEDED
  (with superseded_by_lesson_id + supersession_reason), the correction goes
  PENDING_ADMISSION -> ACTIVE. Every step is fail-closed and validated;
  the original record is never mutated in place — supersession returns new
  dicts, the input records are untouched.

THE COMPOUNDING LOOP:

  Each cycle\'s per-lesson measurements feed emit_cycle_summary(), which
  aggregates by task class: which kinds of lessons actually improve
  decisions. The summary is the artifact the NEXT cycle\'s admission reads
  — admission gets sharper because EVOLVE measured what worked, not because
  anyone asserted it.

HONEST BOUNDS (stated, not hidden):

  * Only independently verified outcomes count: an outcome is verified iff
    independent_verification names a verifier distinct from the applier
    (the E3 law — executor-owned observation is not verification). A lesson
    with zero verified outcomes is FLAG_FOR_REVIEW, never KEEP.
  * delta_vs_baseline requires a baseline success rate for the same task
    class WITHOUT the lesson (the admission gate\'s control arm is the
    natural source). No baseline -> delta is UNKNOWN with the reason named.
  * n < 3 verified applications -> the measurement carries low_sample: True.
  * The corrected_claim is DERIVED (original claim narrowed by the observed
    falsifying condition), marked as a correction CANDIDATE, never asserted
    as verified truth. It must pass VERIFY before it becomes ACTIVE.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

EVOLVE_MEASUREMENT_SCHEMA = "NAYANET_LEARNING_EVOLVE_MEASUREMENT_V1"
CORRECTION_SCHEMA = "NAYANET_LEARNING_CORRECTION_RECORD_V1"
CYCLE_SUMMARY_SCHEMA = "NAYANET_LEARNING_CYCLE_SUMMARY_V1"

# Preservation verdicts
KEEP = "KEEP"
FLAG_FOR_REVIEW = "FLAG_FOR_REVIEW"
CORRECT = "CORRECT"

# Lifecycle states used by this module (aligned with the capture lifecycle:
# ACTIVE | SUPERSEDED, plus the correction's pre-admission state).
LIFECYCLE_ACTIVE = "ACTIVE"
LIFECYCLE_SUPERSEDED = "SUPERSEDED"
LIFECYCLE_PENDING_ADMISSION = "PENDING_ADMISSION"

# Named failure / verdict reasons
LESSON_NOT_ACTIVE = "LESSON_NOT_ACTIVE"
NO_VERIFIED_OUTCOMES = "NO_VERIFIED_OUTCOMES"
NO_BASELINE = "NO_BASELINE"
FALSIFIED_IN_APPLICATION = "FALSIFIED_IN_APPLICATION"
LOW_SAMPLE = "LOW_SAMPLE"

MIN_SAMPLE_FOR_STABLE_MEASUREMENT = 3


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _digest_id(prefix: str, core: dict[str, Any]) -> str:
    digest = hashlib.sha256(_canonical(core).encode("utf-8")).hexdigest()[:32]
    return "%s-%s" % (prefix, digest)


def _require_str(mapping: dict[str, Any], name: str, where: str) -> str:
    value = mapping.get(name)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(
            "REQUIRED_FIELD_MISSING: %s.%s must be a non-empty string" % (where, name)
        )
    return value.strip()


def _require_dict(mapping: dict[str, Any], name: str, where: str) -> dict[str, Any]:
    value = mapping.get(name)
    if not isinstance(value, dict):
        raise ValueError(
            "REQUIRED_FIELD_MISSING: %s.%s must be an object" % (where, name)
        )
    return value


def _require_bool(mapping: dict[str, Any], name: str, where: str) -> bool:
    value = mapping.get(name)
    if not isinstance(value, bool):
        raise ValueError(
            "REQUIRED_FIELD_MISSING: %s.%s must be a boolean true/false" % (where, name)
        )
    return value


def _optional_rate(value: Any, where: str) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("INVALID_BASELINE: %s must be a number in [0, 1]" % where)
    rate = float(value)
    if not 0.0 <= rate <= 1.0:
        raise ValueError("INVALID_BASELINE: %s must be a number in [0, 1]" % where)
    return rate


def _is_verified(application: dict[str, Any]) -> tuple[bool, str]:
    """An outcome is verified iff a distinct verifier attests it.

    Returns (verified, verifier_or_reason). Verifier == applier is recorded
    honestly and does NOT count — self-attestation is not verification.
    """
    iv = application.get("independent_verification")
    if iv is None:
        return False, "no independent_verification supplied"
    if not isinstance(iv, dict):
        raise ValueError(
            "INVALID_VERIFICATION: independent_verification must be an object when supplied"
        )
    verifier = iv.get("verifier")
    verified_at = iv.get("verified_at")
    if not (isinstance(verifier, str) and verifier.strip()):
        return False, "independent_verification.verifier missing"
    if not (isinstance(verified_at, str) and verified_at.strip()):
        return False, "independent_verification.verified_at missing"
    applier = application.get("applier")
    if isinstance(applier, str) and applier.strip() and verifier.strip() == applier.strip():
        return False, "verifier == applier: self-attestation is not verification"
    return True, verifier.strip()


def _validate_application(app: dict[str, Any], index: int) -> dict[str, Any]:
    where = "applications[%d]" % index
    if not isinstance(app, dict):
        raise ValueError("INVALID_APPLICATION: %s must be an object" % where)
    _require_str(app, "application_receipt_id", where)
    _require_str(app, "task_ref", where)
    _require_str(app, "applier", where)
    outcome = _require_dict(app, "outcome", where)
    _require_bool(outcome, "success", where + ".outcome")
    _require_str(outcome, "effect_text", where + ".outcome")
    _require_str(outcome, "observed_at", where + ".outcome")
    return app


@dataclass(frozen=True)
class EvolveResult:
    """The EVOLVE verdict for one lesson."""

    lesson_id: str
    measurement: dict[str, Any]
    verdict: str
    verdict_reason: str
    correction_records: tuple[dict[str, Any], ...] = field(default_factory=tuple)


def evolve_lesson(
    lesson: dict[str, Any],
    applications: list[dict[str, Any]],
    baseline_success_rate: float | None = None,
) -> EvolveResult:
    """Measure one lesson against its recorded application history.

    lesson: {lesson_id, claim, lifecycle_state, lesson_kind?, content_sha?}
    applications: list of application records, each
        {application_receipt_id, task_ref, task_class?, applier, applied_at,
         decision_summary?,
         outcome: {success: bool, effect_text, observed_at},
         independent_verification: {verifier, verified_at} | None,
         baseline_success_rate?: float}
    baseline_success_rate: lesson-level default no-lesson baseline for the
        task class (the admission control arm is the natural source).

    Raises ValueError (fail-closed, named) on a non-ACTIVE lesson or
    malformed input. Never returns a manufactured verdict.
    """
    if not isinstance(lesson, dict):
        raise ValueError("INVALID_LESSON: lesson must be an object")
    lesson_id = _require_str(lesson, "lesson_id", "lesson")
    claim = _require_str(lesson, "claim", "lesson")
    lifecycle = str(lesson.get("lifecycle_state", "")).upper()
    if lifecycle != LIFECYCLE_ACTIVE:
        raise ValueError(
            "%s: evolve operates on ACTIVE lessons only; lesson %r is %r. "
            "SUPERSEDED lessons are immutable history." % (LESSON_NOT_ACTIVE, lesson_id, lifecycle)
        )
    if not isinstance(applications, list):
        raise ValueError("INVALID_APPLICATIONS: applications must be a list")
    validated = [_validate_application(app, i) for i, app in enumerate(applications)]
    lesson_baseline = _optional_rate(baseline_success_rate, "baseline_success_rate")

    verified_apps: list[dict[str, Any]] = []
    unverified_reasons: list[str] = []
    for app in validated:
        ok, detail = _is_verified(app)
        if ok:
            verified_apps.append(app)
        else:
            unverified_reasons.append(
                "%s: %s" % (app["application_receipt_id"], detail)
            )

    n = len(verified_apps)
    successes = sum(1 for app in validated if _is_verified(app)[0] and app["outcome"]["success"])
    failures = [app for app in verified_apps if not app["outcome"]["success"]]
    observed_rate: float | None = (successes / n) if n else None

    # Baseline: per-application rate wins over the lesson-level default;
    # absent everywhere, the delta is honestly UNKNOWN.
    baseline: float | None = lesson_baseline
    per_app_baselines = [
        _optional_rate(app.get("baseline_success_rate"), "applications[].baseline_success_rate")
        for app in verified_apps
    ]
    known = [b for b in per_app_baselines if b is not None]
    if known:
        baseline = sum(known) / len(known)

    delta: float | None = None
    delta_reason = NO_BASELINE + ": no no-lesson baseline supplied for this task class"
    if observed_rate is not None and baseline is not None:
        delta = observed_rate - baseline
        delta_reason = "observed %.3f vs baseline %.3f over %d verified applications" % (
            observed_rate, baseline, n,
        )

    measurement = {
        "schema": EVOLVE_MEASUREMENT_SCHEMA,
        "lesson_id": lesson_id,
        "measured_at": _utcnow(),
        "verified_applications": n,
        "verified_successes": successes,
        "verified_failures": len(failures),
        "observed_success_rate": observed_rate,
        "baseline_success_rate": baseline,
        "delta_vs_baseline": delta,
        "delta_basis": delta_reason,
        "low_sample": n < MIN_SAMPLE_FOR_STABLE_MEASUREMENT,
        "unverified_application_reasons": unverified_reasons,
        "task_classes": sorted({str(app.get("task_class") or app["task_ref"]) for app in verified_apps}),
    }

    if n == 0:
        return EvolveResult(
            lesson_id=lesson_id,
            measurement=measurement,
            verdict=FLAG_FOR_REVIEW,
            verdict_reason=(
                "%s: %d application(s) recorded but none independently verified "
                "(verifier must differ from applier). Measurement requires "
                "verification; self-attestation never counts." % (NO_VERIFIED_OUTCOMES, len(validated))
            ),
        )

    if failures:
        corrections = tuple(
            emit_correction_record(lesson, app, [a["application_receipt_id"] for a in verified_apps if a["outcome"]["success"]])
            for app in failures
        )
        return EvolveResult(
            lesson_id=lesson_id,
            measurement=measurement,
            verdict=CORRECT,
            verdict_reason=(
                "%s: %d of %d verified applications falsified the lesson "
                "(%s). Correction record(s) emitted; original lesson untouched "
                "until a correction is admitted." % (
                    FALSIFIED_IN_APPLICATION, len(failures), n,
                    ", ".join(a["application_receipt_id"] for a in failures),
                )
            ),
            correction_records=corrections,
        )

    reason = "all %d verified applications succeeded" % n
    if delta is not None:
        reason += "; delta_vs_baseline=%+.3f" % delta
    else:
        reason += "; baseline unknown (%s)" % NO_BASELINE
    return EvolveResult(
        lesson_id=lesson_id,
        measurement=measurement,
        verdict=KEEP,
        verdict_reason=reason,
    )


def emit_correction_record(
    lesson: dict[str, Any],
    failed_application: dict[str, Any],
    preserved_application_ids: list[str],
) -> dict[str, Any]:
    """Emit a correction record for one falsifying application.

    The record is NEW (deterministic id COR-<sha>), carries the SUPERSEDES
    edge back to the original lesson, and starts at PENDING_ADMISSION — it
    must pass VERIFY before it can become ACTIVE. The original lesson is
    never modified here; apply_supersession() performs the transition.
    """
    lesson_id = _require_str(lesson, "lesson_id", "lesson")
    claim = _require_str(lesson, "claim", "lesson")
    receipt_id = _require_str(failed_application, "application_receipt_id", "failed_application")
    task_ref = _require_str(failed_application, "task_ref", "failed_application")
    outcome = _require_dict(failed_application, "outcome", "failed_application")
    effect_text = _require_str(outcome, "effect_text", "failed_application.outcome")
    iv = failed_application.get("independent_verification") or {}
    verifier = iv.get("verifier", "unknown-verifier")
    verified_at = iv.get("verified_at", "")

    task_class = str(failed_application.get("task_class") or task_ref)
    # The corrected claim is DERIVED, not invented: the original claim
    # narrowed by the observed falsifying condition. It is a candidate that
    # must be independently verified and admitted — never asserted as truth.
    corrected_claim = (
        "%s [EVOLVE correction: falsified for %s by %s (verified by %s); "
        "scope narrowed to exclude the observed failure condition. "
        "Correction candidate — requires independent verification and admission.]"
        % (claim, task_class, receipt_id, verifier)
    )
    supersession_reason = (
        "falsifying observation in %s (%s): %s — verified by %s%s. "
        "Original claim preserved verbatim below; nothing was overwritten." % (
            task_ref, receipt_id, effect_text, verifier,
            (" at %s" % verified_at) if verified_at else "",
        )
    )
    core = {
        "schema": CORRECTION_SCHEMA,
        "lesson_id": lesson_id,
        "supersedes_lesson_id": lesson_id,
        "application_receipt_id": receipt_id,
    }
    record = dict(core)
    record["correction_id"] = _digest_id("COR", core)
    record["supersession_reason"] = supersession_reason
    record["original_claim"] = claim
    record["corrected_claim"] = corrected_claim
    record["falsifying_evidence"] = {
        "application_receipt_id": receipt_id,
        "task_ref": task_ref,
        "task_class": task_class,
        "effect_text": effect_text,
        "verifier": verifier,
        "verified_at": verified_at,
    }
    # The wins are preserved, not rewritten: their receipt ids ride along so
    # a reader can see exactly what evidence the correction inherits.
    record["preserved_evidence"] = {
        "successful_application_receipt_ids": list(preserved_application_ids),
        "note": "successful applications are preserved as evidence; only the falsified scope is narrowed",
    }
    record["lifecycle_state"] = LIFECYCLE_PENDING_ADMISSION
    record["emitted_at"] = _utcnow()
    return record


def apply_supersession(
    original: dict[str, Any], correction: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Atomically supersede a wrong lesson with its admitted correction.

    Fail-closed validation (any violation raises ValueError, nothing is
    written):
      - original must be ACTIVE; correction must be PENDING_ADMISSION
      - correction.supersedes_lesson_id must equal original.lesson_id
      - correction.supersession_reason must be non-empty
      - correction.corrected_claim must differ from original.claim (it must
        actually correct something)
      - correction must have been admitted (admitted_by + admitted_at present)

    Returns (original_superseded, correction_active) as NEW dicts. The input
    records are never mutated — history is preserved, never overwritten.
    """
    if not isinstance(original, dict) or not isinstance(correction, dict):
        raise ValueError("INVALID_SUPERSESSION: original and correction must be objects")
    lesson_id = _require_str(original, "lesson_id", "original")
    if str(original.get("lifecycle_state", "")).upper() != LIFECYCLE_ACTIVE:
        raise ValueError(
            "INVALID_SUPERSESSION: original lesson %r is not ACTIVE (got %r)" % (
                lesson_id, original.get("lifecycle_state"))
        )
    if str(correction.get("lifecycle_state", "")).upper() != LIFECYCLE_PENDING_ADMISSION:
        raise ValueError(
            "INVALID_SUPERSESSION: correction %r is not PENDING_ADMISSION (got %r)" % (
                correction.get("correction_id"), correction.get("lifecycle_state"))
        )
    if str(correction.get("supersedes_lesson_id", "")) != lesson_id:
        raise ValueError(
            "INVALID_SUPERSESSION: correction.supersedes_lesson_id=%r does not point at original %r" % (
                correction.get("supersedes_lesson_id"), lesson_id)
        )
    reason = correction.get("supersession_reason")
    if not (isinstance(reason, str) and reason.strip()):
        raise ValueError("INVALID_SUPERSESSION: correction.supersession_reason must be non-empty")
    corrected_claim = correction.get("corrected_claim")
    if not (isinstance(corrected_claim, str) and corrected_claim.strip()):
        raise ValueError("INVALID_SUPERSESSION: correction.corrected_claim must be non-empty")
    if corrected_claim.strip() == str(original.get("claim", "")).strip():
        raise ValueError(
            "INVALID_SUPERSESSION: correction.corrected_claim is identical to the original claim — "
            "a correction must correct something"
        )
    if not correction.get("admitted_at"):
        raise ValueError(
            "INVALID_SUPERSESSION: correction %r has not been admitted (admitted_at missing). "
            "A correction becomes ACTIVE only through VERIFY admission — never by EVOLVE fiat." % (
                correction.get("correction_id"))
        )

    superseded = dict(original)
    superseded["lifecycle_state"] = LIFECYCLE_SUPERSEDED
    superseded["superseded_by_lesson_id"] = correction.get("correction_id")
    superseded["supersession_reason"] = reason.strip()
    superseded["superseded_at"] = _utcnow()

    active = dict(correction)
    active["lifecycle_state"] = LIFECYCLE_ACTIVE
    active["activated_at"] = _utcnow()
    return superseded, active


def emit_cycle_summary(measurements: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate one cycle's EVOLVE measurements into the compounding summary.

    The summary answers: which kinds of lessons actually improve decisions?
    The next cycle's admission reads this — that is the compounding loop.
    Measurements with no verified applications contribute their verdict only;
    they never inflate the rate math.
    """
    if not isinstance(measurements, list):
        raise ValueError("INVALID_MEASUREMENTS: measurements must be a list")
    by_class: dict[str, dict[str, Any]] = {}
    for m in measurements:
        if not isinstance(m, dict):
            raise ValueError("INVALID_MEASUREMENTS: each measurement must be an object")
        for task_class in m.get("task_classes", []) or ["(unclassified)"]:
            bucket = by_class.setdefault(task_class, {
                "lessons": 0,
                "verified_applications": 0,
                "verified_successes": 0,
                "deltas": [],
                "corrections": 0,
            })
            bucket["lessons"] += 1
            n = m.get("verified_applications") or 0
            bucket["verified_applications"] += n
            bucket["verified_successes"] += m.get("verified_successes") or 0
            if m.get("delta_vs_baseline") is not None:
                bucket["deltas"].append(m["delta_vs_baseline"])
            bucket["corrections"] += m.get("verified_failures") or 0

    classes: dict[str, dict[str, Any]] = {}
    for task_class, b in sorted(by_class.items()):
        n = b["verified_applications"]
        classes[task_class] = {
            "lessons": b["lessons"],
            "verified_applications": n,
            "observed_success_rate": (b["verified_successes"] / n) if n else None,
            "mean_delta_vs_baseline": (sum(b["deltas"]) / len(b["deltas"])) if b["deltas"] else None,
            "corrections_emitted": b["corrections"],
        }

    guidance = [
        "prefer lessons for task classes with positive mean delta_vs_baseline: %s" % (
            ", ".join(c for c, s in classes.items() if (s["mean_delta_vs_baseline"] or 0) > 0) or "(none measured yet)"
        ),
        "treat task classes with corrections as falsification-prone: %s" % (
            ", ".join(c for c, s in classes.items() if s["corrections_emitted"] > 0) or "(none)"
        ),
        "withhold admission weight from task classes with no verified applications: %s" % (
            ", ".join(c for c, s in classes.items() if s["verified_applications"] == 0) or "(none)"
        ),
    ]
    core_ids = sorted(str(m.get("lesson_id", "")) for m in measurements)
    summary = {
        "schema": CYCLE_SUMMARY_SCHEMA,
        "cycle_id": _digest_id("CYC", {"lessons": core_ids}),
        "measured_at": _utcnow(),
        "lesson_count": len(measurements),
        "by_task_class": classes,
        "admission_guidance": guidance,
    }
    return summary
