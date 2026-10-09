"""Receipt-driven evidence assembler for the E0-E7 ladder (convergence item C).

The E0-E7 evaluator (tools/learning_evidence_ladder.py, #1826) computes the
EARNED level from an evidence bundle -- but nothing in the tree assembles
that bundle from real instrument output. Every ladder test feeds hand-built
fixtures. This module is the missing READER that the D instrument's
docstring names ("readers assemble evidence bundles and the ladder
evaluates them"): it consumes real receipts and emits evaluator-ready
evidence, so E0-E7 advancement becomes behaviorally testable.

Consumes (pure: no DB, no network):
  - B lineage bundle via tools/learning_lineage_receipt.reconstruct() -- REAL
  - D-shaped receipts (retrieval / application / outcome) attached under the
    attach_to_lineage_bundle keys -- digest- and link-verified HERE
  - runtime evidence records: comprehension, transfer, successor_use,
    retention, mastery (shape-checked pass-through; the runtime reader
    supplies them from the rows it already persists)

Produces: the exact evidence dict the ladder's evaluate() consumes, plus
advance(), which computes the earned-level TRAJECTORY across ordered
evidence snapshots -- advancement as a function of evidence history, not
a claimed field.

Fail-closed rules (never repaired, never rounded up):
  - a receipt whose digest does not recompute, whose schema mismatches, or
    whose links break is EXCLUDED from the bundle; the ladder then
    naturally caps the earned level at the last proven transition.
  - a receipt carrying any forbidden authority field is excluded (a receipt
    is evidence, never authority -- the #1712 lesson).
  - malformed input is unproven, never an exception (matches the
    evaluator's contract).

CONTRACT MIRROR (drift guard): D's emitter
(Learning-team PR #1882, tools/learning_application_receipt.py) is not on
main yet, so the digest contract -- sha256 of canonical JSON of the
apply-time core, RET-/APP-/OUT- prefix, first 32 hex chars -- is mirrored
here in _mirror_*. tests/test_learning_evidence_assembler.py pins the
mirror against fixed vectors. When #1882 merges, replace the mirrors with
imports and delete this paragraph.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

from learning_evidence_ladder import LEVEL_ORDER, evaluate
from learning_lineage_receipt import reconstruct

SCHEMA = "NAYANET_LEARNING_EVIDENCE_ASSEMBLY_V1"

# --- D-contract mirror (see module docstring) -------------------------------
_MIRROR_RETRIEVAL_SCHEMA = "NAYANET_LEARNING_RETRIEVAL_RECEIPT_V1"
_MIRROR_APPLICATION_SCHEMA = "NAYANET_LEARNING_APPLICATION_RECEIPT_V1"
_MIRROR_OUTCOME_SCHEMA = "NAYANET_LEARNING_OUTCOME_RECORD_V1"

_MIRROR_PREFIX = {"retrieval": "RET", "application": "APP", "outcome": "OUT"}

_MIRROR_CORES = {
    "retrieval": (
        ["schema", "lesson_id", "retriever", "retrieved_at",
         "query_context", "lesson_content_sha"],
        "receipt_id",
        _MIRROR_RETRIEVAL_SCHEMA,
        ("lesson_id", "retriever", "retrieved_at"),
    ),
    "application": (
        ["schema", "lesson_id", "retrieval_ref", "task_ref",
         "applier", "applied_at"],
        "receipt_id",
        _MIRROR_APPLICATION_SCHEMA,
        ("lesson_id", "retrieval_ref", "task_ref", "applier", "applied_at"),
    ),
    "outcome": (
        ["schema", "application_receipt_id", "lesson_id", "task_ref",
         "measured_effect", "observed_at"],
        "record_id",
        _MIRROR_OUTCOME_SCHEMA,
        ("application_receipt_id", "lesson_id", "task_ref",
         "measured_effect", "observed_at"),
    ),
}

# A receipt must never pose as its own authority (the #1712 defect).
_FORBIDDEN_AUTHORITY_FIELDS = frozenset(
    {"authorized", "is_authorized", "authority_granted",
     "grant", "grant_id", "self_authorized"}
)

_CAPTURE_TS_KEYS = ("captured_at", "created_at", "observed_at",
                    "committed_at", "timestamp")


def _is_nonempty_str(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _mirror_canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True)


def _mirror_digest_id(kind: str, core: dict[str, Any]) -> str:
    digest = hashlib.sha256(
        _mirror_canonical(core).encode("utf-8")).hexdigest()[:32]
    return "%s-%s" % (_MIRROR_PREFIX[kind], digest)


def _mirror_verify(receipt: Any, kind: str) -> tuple[bool, list[str]]:
    """Fail-closed mirror of D's validate_* for one receipt. Never raises."""
    codes: list[str] = []
    core_fields, id_field, schema, required = _MIRROR_CORES[kind]
    if not isinstance(receipt, dict):
        return False, ["RECEIPT_NOT_AN_OBJECT: %s" % kind]
    if receipt.get("schema") != schema:
        codes.append("SCHEMA_MISMATCH: expected %s" % schema)
    for field in required:
        if not _is_nonempty_str(receipt.get(field)):
            codes.append("MISSING_REQUIRED_FIELD: %s" % field)
    bad = sorted(_FORBIDDEN_AUTHORITY_FIELDS & set(receipt.keys()))
    for field in bad:
        codes.append("FORBIDDEN_AUTHORITY_FIELD: %s carries %s" % (kind, field))
    try:
        core = {f: receipt.get(f) for f in core_fields}
        expected = _mirror_digest_id(kind, core)
    except Exception:
        expected = None
    if expected is not None and receipt.get(id_field) != expected:
        codes.append("IDEMPOTENCY_MISMATCH: %s does not recompute from core"
                     % id_field)
    return not codes, codes


def verify_d_receipts(bundle: Any) -> dict[str, Any]:
    """Verify every D-shaped receipt attached to a lineage bundle.

    Checks digest integrity per receipt and the two links the ladder's E2/E3
    transitions depend on: application.retrieval_ref -> retrieval receipt id,
    outcome.application_receipt_id -> application receipt id, with lesson
    agreement on both. Returns the verified sets plus audit codes. Never
    raises.
    """
    bundle = bundle if isinstance(bundle, dict) else {}
    learning = bundle.get("learning")
    learning = learning if isinstance(learning, dict) else {}
    lesson_id = str(learning.get("id") or "")

    def _of_kind(key: str) -> list[dict[str, Any]]:
        items = bundle.get(key)
        return [i for i in items] if isinstance(items, list) else []

    retrievals = _of_kind("retrieval_receipts")
    applications = _of_kind("application_receipts")
    outcomes = _of_kind("outcome_records")

    codes: list[str] = []
    valid_retrieval: dict[str, dict[str, Any]] = {}
    for r in retrievals:
        ok, rc = _mirror_verify(r, "retrieval")
        codes.extend(rc)
        if ok and str(r.get("lesson_id") or "") == lesson_id:
            valid_retrieval[str(r.get("receipt_id"))] = r
        elif ok:
            codes.append("RECEIPT_LESSON_MISMATCH: retrieval for another lesson")

    valid_application: dict[str, dict[str, Any]] = {}
    for a in applications:
        ok, ac = _mirror_verify(a, "application")
        codes.extend(ac)
        if not ok:
            continue
        if str(a.get("lesson_id") or "") != lesson_id:
            codes.append("RECEIPT_LESSON_MISMATCH: application for another lesson")
            continue
        ref = str(a.get("retrieval_ref") or "")
        if ref not in valid_retrieval:
            codes.append("RETRIEVAL_BINDING_BROKEN: application %s names "
                         "unknown/unverified retrieval %s"
                         % (a.get("receipt_id"), ref))
            continue
        valid_application[str(a.get("receipt_id"))] = a

    valid_outcome: dict[str, dict[str, Any]] = {}
    for o in outcomes:
        ok, oc = _mirror_verify(o, "outcome")
        codes.extend(oc)
        if not ok:
            continue
        if str(o.get("lesson_id") or "") != lesson_id:
            codes.append("RECEIPT_LESSON_MISMATCH: outcome for another lesson")
            continue
        app_id = str(o.get("application_receipt_id") or "")
        if app_id not in valid_application:
            codes.append("OUTCOME_APPLICATION_LINK_BROKEN: outcome %s names "
                         "unknown/unverified application %s"
                         % (o.get("record_id"), app_id))
            continue
        valid_outcome[str(o.get("record_id"))] = o

    return {
        "schema": SCHEMA,
        "lesson_id": lesson_id,
        "valid_retrievals": valid_retrieval,
        "valid_applications": valid_application,
        "valid_outcomes": valid_outcome,
        "codes": codes,
    }


def _capture_receipt(bundle: dict[str, Any],
                     reconstruction: dict[str, Any]) -> dict[str, Any] | None:
    """E0 evidence: capture is proven only if B's reconstruction marks the
    capture stage PRESENT and the block/event rows name a block and a time."""
    stages = reconstruction.get("stages") or {}
    capture = stages.get("capture") or {}
    if capture.get("status") != "PRESENT":
        return None
    block = bundle.get("intelligent_block")
    block = block if isinstance(block, dict) else {}
    event = bundle.get("cognition_event")
    event = event if isinstance(event, dict) else {}
    commit = bundle.get("commit_receipt")
    commit = commit if isinstance(commit, dict) else {}
    block_id = block.get("intelligent_block_id")
    captured_at = None
    for row in (event, commit):
        if isinstance(row, dict):
            for key in _CAPTURE_TS_KEYS:
                if _is_nonempty_str(row.get(key)):
                    captured_at = row.get(key)
                    break
        if captured_at:
            break
    if _is_nonempty_str(block_id) and _is_nonempty_str(captured_at):
        return {"intelligent_block_id": block_id, "captured_at": captured_at}
    return None


def _shape_ok(obj: Any, *fields: str) -> bool:
    return isinstance(obj, dict) and all(
        _is_nonempty_str(obj.get(f)) for f in fields)


def assemble_evidence(
    lesson_id: str,
    lineage_bundle: dict[str, Any] | None,
    comprehension: dict[str, Any] | None = None,
    transfer: list[dict[str, Any]] | None = None,
    successor_use: list[dict[str, Any]] | None = None,
    retention: dict[str, Any] | None = None,
    mastery: dict[str, Any] | None = None,
    conflicts: bool = False,
    stale: bool = False,
) -> dict[str, Any]:
    """Assemble the ladder's evidence bundle from real instrument output.

    Runs the REAL B reconstructor on the bundle, verifies the attached
    D receipts by contract, and maps the verified artifacts to the exact
    evidence fields the ladder's transitions read. Anything unverifiable
    is omitted -- the ladder caps the earned level on its own.
    Never raises on malformed input.
    """
    lesson_id = str(lesson_id or "")
    bundle = lineage_bundle if isinstance(lineage_bundle, dict) else {}
    try:
        reconstruction = reconstruct(bundle)
    except Exception:
        reconstruction = {"stages": {}, "gaps": ["RECONSTRUCTION_FAILED"],
                          "verdict": "BROKEN"}

    verified = verify_d_receipts(bundle)
    applications = verified["valid_applications"]
    outcomes = verified["valid_outcomes"]

    # Newest verified application for this lesson wins (apply-time evidence
    # is append-only; the latest binding is the live one).
    application = None
    if applications:
        application = max(
            applications.values(),
            key=lambda a: str(a.get("applied_at") or ""),
        )
    outcome = None
    if application is not None:
        app_id = str(application.get("receipt_id") or "")
        linked = [o for o in outcomes.values()
                  if str(o.get("application_receipt_id") or "") == app_id]
        if linked:
            outcome = max(linked,
                          key=lambda o: str(o.get("observed_at") or ""))

    evidence: dict[str, Any] = {}
    capture = _capture_receipt(bundle, reconstruction)
    if capture is not None:
        evidence["capture_receipt"] = capture
    if _shape_ok(comprehension, "control_receipt", "treatment_receipt",
                 "independent_verifier", "verified_at"):
        evidence["comprehension"] = comprehension
    if application is not None:
        evidence["application_receipt"] = {
            "retrieval_ref": application.get("retrieval_ref"),
            "task_ref": application.get("task_ref"),
            "applied_at": application.get("applied_at"),
            "applier": application.get("applier"),
        }
    if outcome is not None:
        evidence["outcome"] = {
            "measured_effect": outcome.get("measured_effect"),
            "independent_verification":
                outcome.get("independent_verification") or {},
        }
    if isinstance(transfer, list):
        evidence["transfer"] = [t for t in transfer if isinstance(t, dict)]
    if isinstance(successor_use, list):
        evidence["successor_use"] = [u for u in successor_use
                                     if isinstance(u, dict)]
    if _shape_ok(retention, "revalidated_at", "revalidation_receipt"):
        evidence["retention"] = retention
    if (isinstance(mastery, dict)
            and isinstance(mastery.get("distinct_verifiers"), int)
            and isinstance(mastery.get("distinct_transfer_domains"), int)):
        evidence["mastery"] = mastery
    if conflicts:
        evidence["conflicts"] = True
    if stale:
        evidence["stale"] = True

    return {
        "schema": SCHEMA,
        "lesson_id": lesson_id,
        "evidence": evidence,
        "receipt_audit_codes": verified["codes"],
        "reconstruction_verdict": reconstruction.get("verdict"),
        "verified_counts": {
            "retrievals": len(verified["valid_retrievals"]),
            "applications": len(verified["valid_applications"]),
            "outcomes": len(verified["valid_outcomes"]),
        },
    }


def _rank(level: str) -> int:
    return LEVEL_ORDER.index(level) if level in LEVEL_ORDER else -1


def advance(
    lesson_id: str,
    claimed_level: str,
    snapshots: list[dict[str, Any]],
    producer_id: str | None = None,
) -> dict[str, Any]:
    """Compute the earned-level trajectory across ordered evidence snapshots.

    Each snapshot carries the assemble_evidence() inputs for one point in
    time. Returns the per-snapshot evaluation plus the transitions between
    them: ADVANCED (evidence earned a higher level), HELD (no movement),
    REGRESSED (earned level dropped -- flagged, never silent).
    Advancement is a function of evidence history, not a claimed field.
    Never raises on malformed input.
    """
    lesson_id = str(lesson_id or "")
    snapshots = snapshots if isinstance(snapshots, list) else []
    trajectory: list[dict[str, Any]] = []
    transitions: list[dict[str, Any]] = []
    regressions: list[dict[str, Any]] = []
    prev_earned: str | None = None

    for index, snap in enumerate(snapshots):
        snap = snap if isinstance(snap, dict) else {}
        assembled = assemble_evidence(
            lesson_id,
            snap.get("lineage_bundle"),
            comprehension=snap.get("comprehension"),
            transfer=snap.get("transfer"),
            successor_use=snap.get("successor_use"),
            retention=snap.get("retention"),
            mastery=snap.get("mastery"),
            conflicts=bool(snap.get("conflicts")),
            stale=bool(snap.get("stale")),
        )
        evaluation = evaluate({
            "id": lesson_id,
            "producer_id": producer_id,
            "claimed_level": claimed_level,
            "evidence": assembled["evidence"],
        })
        earned = str(evaluation.get("earned_level") or "UNPROVEN")
        trajectory.append({
            "index": index,
            "earned_level": earned,
            "verdict": evaluation.get("verdict"),
            "verdict_code": evaluation.get("verdict_code"),
            "proven_count": len(evaluation.get("proven_chain") or []),
            "cap_note": evaluation.get("cap_note") or "",
        })
        if prev_earned is not None and earned != prev_earned:
            if _rank(earned) > _rank(prev_earned):
                transitions.append({
                    "at_index": index,
                    "kind": "ADVANCED",
                    "from": prev_earned,
                    "to": earned,
                })
            else:
                entry = {
                    "at_index": index,
                    "kind": "REGRESSED",
                    "from": prev_earned,
                    "to": earned,
                    "reason": (evaluation.get("cap_note") or ""
                               or "; ".join(
                                   (evaluation.get("unproven") or [])[:2])),
                }
                transitions.append(entry)
                regressions.append(entry)
        elif prev_earned is not None:
            transitions.append({
                "at_index": index,
                "kind": "HELD",
                "from": prev_earned,
                "to": earned,
            })
        prev_earned = earned

    final = trajectory[-1] if trajectory else {
        "index": -1, "earned_level": "UNPROVEN", "verdict": "UNPROVEN",
        "verdict_code": "NO_SNAPSHOTS", "proven_count": 0, "cap_note": "",
    }
    return {
        "schema": SCHEMA,
        "lesson_id": lesson_id,
        "claimed_level": claimed_level,
        "trajectory": trajectory,
        "transitions": transitions,
        "regressions": regressions,
        "final_earned_level": final["earned_level"],
        "final_verdict": final["verdict"],
    }
