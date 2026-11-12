"""Canonical durable retrieval/application receipt instrument (convergence item D).

Convergence audit item D: "durable retrieval/application receipts linked to
outcome + independent verification." The merged E0-E7 ladder (convergence
item C, tools/learning_evidence_ladder.py) names THIS instrument as the
witness owner for two transitions:

  E2_CAN_DO      requires application_receipt {retrieval_ref, task_ref,
                 applied_at, applier} -- the retrieval -> application binding
                 is E2's witness.
  E3_INDEPENDENT requires outcome {measured_effect, independent_verification
                 .{verifier, verified_at}} with verifier != applier -- executor
                 -owned observation is not verification.

This module is that instrument, pure: no DB, no network. The runtime (or a
test harness) persists the emitted dicts; readers assemble evidence bundles
and the ladder evaluates them. Three records, append-only, linked by
deterministic IDs:

  retrieval_receipt   NAYANET_LEARNING_RETRIEVAL_RECEIPT_V1
                      who retrieved what, when, from where (durable refs to
                      the persisted rows the runtime already keeps)
  application_receipt NAYANET_LEARNING_APPLICATION_RECEIPT_V1
                      which retrieval bound to which task, by which applier
                      (E2 evidence). Outcome and independent verification are
                      appended later -- the receipt_id is computed from the
                      apply-time core ONLY, so it is stable across phases
                      (idempotency / replay safety, matching the P0
                      idempotency gate).
  outcome_record      NAYANET_LEARNING_OUTCOME_RECORD_V1
                      the measured effect of the application, with the
                      independent verification that turns an executor-owned
                      observation into E3 evidence. Verifier == applier fails
                      closed (self-attestation is not verification).

LAW BAKED IN (the #1712 lesson): a receipt is evidence, never authority.
This module carries no grant, accepts no grant, and exposes no function any
authority gate may accept. authority_refs are LINKS ONLY; the forbidden
fields below are refused at emit time (ValueError) and flagged at validate
time. There is no satisfies_authority here on purpose: receipts never
satisfy authority.

The lineage-bundle contract for convergence item B (learn-builder's lane):
readers should append this module's outputs to the B receipt bundle under
the keys "retrieval_receipts" and "application_receipts"
(see attach_to_lineage_bundle). B's reconstruction loop can then resolve
its retrieval / applicability / application / outcome stages instead of
leaving them UNINSTRUMENTED. This module does NOT modify B's module -- the
wiring belongs to the B lane.

Machine-falsifiable via tests/test_learning_application_receipt.py,
including seam tests that run this module's outputs through the ladder's
real _transition_e2 / _transition_e3 predicates.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

RETRIEVAL_SCHEMA = "NAYANET_LEARNING_RETRIEVAL_RECEIPT_V1"
SCHEMA = "NAYANET_LEARNING_APPLICATION_RECEIPT_V1"
OUTCOME_SCHEMA = "NAYANET_LEARNING_OUTCOME_RECORD_V1"

# Fields a receipt must NEVER carry: any one of these would let a receipt
# pose as its own authority (the exact #1712 defect, same guard as the
# lineage receipt).
FORBIDDEN_AUTHORITY_FIELDS = frozenset(
    {"authorized", "is_authorized", "authority_granted", "grant", "grant_id", "self_authorized"}
)

_ID_PREFIX = {"retrieval": "RET", "application": "APP", "outcome": "OUT"}


def _canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _digest_id(kind: str, core: dict[str, Any]) -> str:
    digest = hashlib.sha256(_canonical(core).encode("utf-8")).hexdigest()[:32]
    return "%s-%s" % (_ID_PREFIX[kind], digest)


def _is_nonempty_str(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _require_str(name: str, value: Any) -> str:
    if not _is_nonempty_str(value):
        raise ValueError("REQUIRED_FIELD_MISSING: %s must be a non-empty string" % name)
    return str(value).strip()


def _check_forbidden(mapping: dict[str, Any], where: str) -> list[str]:
    found = sorted(FORBIDDEN_AUTHORITY_FIELDS & set(mapping.keys()))
    return ["FORBIDDEN_AUTHORITY_FIELD: %s carries %s" % (where, f) for f in found]


# ---------------------------------------------------------------------------
# Emitters
# ---------------------------------------------------------------------------

def emit_retrieval_receipt(
    lesson_id: str,
    retriever: str,
    retrieved_at: str,
    query_context: str | None = None,
    lesson_content_sha: str | None = None,
    source_refs: list[str] | None = None,
    authority_ref_links: list[str] | None = None,
) -> dict[str, Any]:
    """Emit a durable retrieval receipt: who retrieved what, when, from where.

    source_refs: durable refs (row ids, event ids) the runtime already
    persists for the retrieval -- this receipt binds them to the lesson.
    lesson_content_sha: hash of the retrieved lesson content, so a later
    reader can prove WHAT was retrieved, not just that something was.
    """
    lesson_id = _require_str("lesson_id", lesson_id)
    retriever = _require_str("retriever", retriever)
    retrieved_at = _require_str("retrieved_at", retrieved_at)
    core = {
        "schema": RETRIEVAL_SCHEMA,
        "lesson_id": lesson_id,
        "retriever": retriever,
        "retrieved_at": retrieved_at,
        "query_context": query_context or "",
        "lesson_content_sha": lesson_content_sha or "",
    }
    receipt = dict(core)
    receipt["receipt_id"] = _digest_id("retrieval", core)
    receipt["kind"] = "retrieval"
    receipt["source_refs"] = [str(r) for r in (source_refs or [])]
    receipt["authority_refs"] = [str(r) for r in (authority_ref_links or [])]
    bad = _check_forbidden(receipt, "retrieval_receipt")
    if bad:
        raise ValueError(bad[0])
    return receipt


def emit_application_receipt(
    lesson_id: str,
    retrieval_ref: str,
    task_ref: str,
    applier: str,
    applied_at: str,
    applicability: dict[str, Any] | None = None,
    authority_ref_links: list[str] | None = None,
) -> dict[str, Any]:
    """Emit the E2 evidence: retrieval -> application binding.

    applicability (optional): {relevance_rationale, task_match} -- why this
    lesson applied to this task. Covers the lineage receipt's applicability
    stage; recorded at apply time, immutable afterwards.

    Outcome and independent verification are appended later via
    link_outcome / emit_outcome_record. receipt_id covers the apply-time
    core only and never changes across phases.
    """
    lesson_id = _require_str("lesson_id", lesson_id)
    retrieval_ref = _require_str("retrieval_ref", retrieval_ref)
    task_ref = _require_str("task_ref", task_ref)
    applier = _require_str("applier", applier)
    applied_at = _require_str("applied_at", applied_at)
    if applicability is not None and not isinstance(applicability, dict):
        raise ValueError("REQUIRED_FIELD_MISSING: applicability must be an object when supplied")
    core = {
        "schema": SCHEMA,
        "lesson_id": lesson_id,
        "retrieval_ref": retrieval_ref,
        "task_ref": task_ref,
        "applier": applier,
        "applied_at": applied_at,
    }
    receipt = dict(core)
    receipt["receipt_id"] = _digest_id("application", core)
    receipt["kind"] = "application"
    receipt["applicability"] = dict(applicability or {})
    receipt["outcome_ref"] = None  # linked later; receipt_id stays stable
    receipt["authority_refs"] = [str(r) for r in (authority_ref_links or [])]
    bad = _check_forbidden(receipt, "application_receipt")
    if bad:
        raise ValueError(bad[0])
    return receipt


def emit_outcome_record(
    application_receipt_id: str,
    lesson_id: str,
    task_ref: str,
    measured_effect: str,
    observed_at: str,
    outcome_ref: str | None = None,
    independent_verification: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Emit the measured effect of an application, with independent verification.

    measured_effect: the observed change, in the applier's own words
    (executor-owned observation). It becomes E3 evidence ONLY when
    independent_verification names a verifier distinct from the applier
    (verified_at required). Verifier == applier is recorded honestly and
    fails the E3 seam -- self-attestation is not verification.

    outcome_ref: durable ref to the persisted outcome row (execution receipt,
    cognition event, etc.) the runtime keeps.
    """
    application_receipt_id = _require_str("application_receipt_id", application_receipt_id)
    lesson_id = _require_str("lesson_id", lesson_id)
    task_ref = _require_str("task_ref", task_ref)
    measured_effect = _require_str("measured_effect", measured_effect)
    observed_at = _require_str("observed_at", observed_at)
    iv = dict(independent_verification or {})
    if independent_verification is not None and not isinstance(independent_verification, dict):
        raise ValueError("REQUIRED_FIELD_MISSING: independent_verification must be an object when supplied")
    core = {
        "schema": OUTCOME_SCHEMA,
        "application_receipt_id": application_receipt_id,
        "lesson_id": lesson_id,
        "task_ref": task_ref,
        "measured_effect": measured_effect,
        "observed_at": observed_at,
    }
    record = dict(core)
    record["record_id"] = _digest_id("outcome", core)
    record["kind"] = "outcome"
    record["outcome_ref"] = outcome_ref or ""
    record["independent_verification"] = iv
    return record


def link_outcome(
    application_receipt: dict[str, Any],
    outcome_record: dict[str, Any],
) -> dict[str, Any]:
    """Link an outcome record to its application receipt (append-only phase 2).

    Returns a NEW receipt dict with outcome_ref set. The receipt_id is NOT
    recomputed -- it covers the apply-time core only, so linking is
    idempotent and replay-safe. Fails closed (ValueError) if the outcome
    record names a different application receipt or a different lesson.
    """
    if not isinstance(application_receipt, dict) or not isinstance(outcome_record, dict):
        raise ValueError("LINK_TYPE_ERROR: receipt and outcome record must be objects")
    if str(outcome_record.get("application_receipt_id") or "") != str(application_receipt.get("receipt_id") or ""):
        raise ValueError(
            "OUTCOME_LINK_MISMATCH: outcome_record.application_receipt_id=%r != receipt_id=%r"
            % (outcome_record.get("application_receipt_id"), application_receipt.get("receipt_id"))
        )
    if str(outcome_record.get("lesson_id") or "") != str(application_receipt.get("lesson_id") or ""):
        raise ValueError(
            "OUTCOME_LESSON_MISMATCH: outcome lesson %r != receipt lesson %r"
            % (outcome_record.get("lesson_id"), application_receipt.get("lesson_id"))
        )
    linked = dict(application_receipt)
    linked["outcome_ref"] = outcome_record.get("record_id")
    return linked


# ---------------------------------------------------------------------------
# Validators (fail-closed audits; never raise on receipt content)
# ---------------------------------------------------------------------------

def _recompute_id(kind: str, receipt: dict[str, Any], core_fields: list[str], id_field: str) -> str | None:
    try:
        core = {f: receipt.get(f) for f in core_fields}
        return _digest_id(kind, core)
    except Exception:
        return None


def validate_retrieval_receipt(receipt: dict[str, Any]) -> dict[str, Any]:
    """Fail-closed audit of a retrieval receipt."""
    codes: list[str] = []
    receipt = receipt if isinstance(receipt, dict) else {}
    if receipt.get("schema") != RETRIEVAL_SCHEMA:
        codes.append("SCHEMA_MISMATCH: expected %s" % RETRIEVAL_SCHEMA)
    for field in ("lesson_id", "retriever", "retrieved_at"):
        if not _is_nonempty_str(receipt.get(field)):
            codes.append("MISSING_REQUIRED_FIELD: %s" % field)
    codes.extend(_check_forbidden(receipt, "retrieval_receipt"))
    expected = _recompute_id(
        "retrieval", receipt,
        ["schema", "lesson_id", "retriever", "retrieved_at", "query_context", "lesson_content_sha"],
        "receipt_id",
    )
    if expected is not None and receipt.get("receipt_id") != expected:
        codes.append("IDEMPOTENCY_MISMATCH: receipt_id does not recompute from core fields")
    return {"valid": not codes, "codes": codes, "receipt_id": receipt.get("receipt_id")}


def validate_application_receipt(
    receipt: dict[str, Any],
    retrieval_receipt: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Fail-closed audit of an application receipt.

    When the retrieval receipt is supplied, the retrieval_ref binding is
    checked end to end: ref == retrieval receipt id AND lesson ids agree.
    That binding is the E2 witness the ladder names.
    """
    codes: list[str] = []
    receipt = receipt if isinstance(receipt, dict) else {}
    if receipt.get("schema") != SCHEMA:
        codes.append("SCHEMA_MISMATCH: expected %s" % SCHEMA)
    for field in ("lesson_id", "retrieval_ref", "task_ref", "applier", "applied_at"):
        if not _is_nonempty_str(receipt.get(field)):
            codes.append("MISSING_REQUIRED_FIELD: %s" % field)
    codes.extend(_check_forbidden(receipt, "application_receipt"))
    expected = _recompute_id(
        "application", receipt,
        ["schema", "lesson_id", "retrieval_ref", "task_ref", "applier", "applied_at"],
        "receipt_id",
    )
    if expected is not None and receipt.get("receipt_id") != expected:
        codes.append("IDEMPOTENCY_MISMATCH: receipt_id does not recompute from apply-time core")
    if retrieval_receipt is not None:
        if not isinstance(retrieval_receipt, dict):
            codes.append("RETRIEVAL_BINDING_BROKEN: retrieval receipt is not an object")
        else:
            if str(receipt.get("retrieval_ref") or "") != str(retrieval_receipt.get("receipt_id") or ""):
                codes.append(
                    "RETRIEVAL_BINDING_BROKEN: retrieval_ref=%r != retrieval receipt_id=%r"
                    % (receipt.get("retrieval_ref"), retrieval_receipt.get("receipt_id"))
                )
            if str(receipt.get("lesson_id") or "") != str(retrieval_receipt.get("lesson_id") or ""):
                codes.append(
                    "RETRIEVAL_BINDING_BROKEN: receipt lesson %r != retrieval lesson %r"
                    % (receipt.get("lesson_id"), retrieval_receipt.get("lesson_id"))
                )
    e2 = qualifies_for_e2(receipt) and not any(
        c.startswith(("SCHEMA_MISMATCH", "IDEMPOTENCY_MISMATCH", "FORBIDDEN_AUTHORITY_FIELD",
                      "MISSING_REQUIRED_FIELD", "RETRIEVAL_BINDING_BROKEN")) for c in codes
    )
    return {
        "valid": not codes,
        "codes": codes,
        "e2_eligible": e2,
        "receipt_id": receipt.get("receipt_id"),
    }


def validate_outcome_record(
    record: dict[str, Any],
    applier: str | None = None,
) -> dict[str, Any]:
    """Fail-closed audit of an outcome record.

    applier: when supplied, verifier == applier fails closed as
    SELF_ATTESTED_VERIFICATION (the E3 falsifier).
    """
    codes: list[str] = []
    record = record if isinstance(record, dict) else {}
    if record.get("schema") != OUTCOME_SCHEMA:
        codes.append("SCHEMA_MISMATCH: expected %s" % OUTCOME_SCHEMA)
    for field in ("application_receipt_id", "lesson_id", "task_ref", "observed_at"):
        if not _is_nonempty_str(record.get(field)):
            codes.append("MISSING_REQUIRED_FIELD: %s" % field)
    if not _is_nonempty_str(record.get("measured_effect")):
        codes.append("OUTCOME_UNMEASURED: no measured_effect; executor observation without a measurement is not evidence")
    iv = record.get("independent_verification")
    if isinstance(iv, dict) and iv:
        if not _is_nonempty_str(iv.get("verifier")) or not _is_nonempty_str(iv.get("verified_at")):
            codes.append("INDEPENDENT_VERIFICATION_INCOMPLETE: verifier and verified_at both required")
        elif applier and str(iv.get("verifier")) == str(applier):
            codes.append("SELF_ATTESTED_VERIFICATION: verifier is the applier (executor-owned observation)")
    elif iv is not None and not isinstance(iv, dict):
        codes.append("INDEPENDENT_VERIFICATION_INCOMPLETE: must be an object when supplied")
    expected = _recompute_id(
        "outcome", record,
        ["schema", "application_receipt_id", "lesson_id", "task_ref", "measured_effect", "observed_at"],
        "record_id",
    )
    if expected is not None and record.get("record_id") != expected:
        codes.append("IDEMPOTENCY_MISMATCH: record_id does not recompute from core fields")
    return {
        "valid": not codes,
        "codes": codes,
        "has_independent_verification": isinstance(iv, dict) and bool(iv)
        and _is_nonempty_str(iv.get("verifier")) and _is_nonempty_str(iv.get("verified_at"))
        and not (applier and str(iv.get("verifier")) == str(applier)),
        "record_id": record.get("record_id"),
    }


# ---------------------------------------------------------------------------
# Ladder eligibility mirrors (same field semantics as _transition_e2/_transition_e3)
# ---------------------------------------------------------------------------

def qualifies_for_e2(application_receipt: dict[str, Any]) -> bool:
    """The exact E2 witness: retrieval_ref/task_ref/applied_at/applier present."""
    if not isinstance(application_receipt, dict):
        return False
    return all(
        _is_nonempty_str(application_receipt.get(f))
        for f in ("retrieval_ref", "task_ref", "applied_at", "applier")
    )


def qualifies_for_e3(application_receipt: dict[str, Any], outcome_record: dict[str, Any]) -> bool:
    """E3 needs a measured outcome AND an independent verifier distinct from the applier."""
    if not isinstance(application_receipt, dict) or not isinstance(outcome_record, dict):
        return False
    if str(outcome_record.get("application_receipt_id") or "") != str(application_receipt.get("receipt_id") or ""):
        return False
    if not _is_nonempty_str(outcome_record.get("measured_effect")):
        return False
    iv = outcome_record.get("independent_verification")
    if not isinstance(iv, dict):
        return False
    if not _is_nonempty_str(iv.get("verifier")) or not _is_nonempty_str(iv.get("verified_at")):
        return False
    applier = str(application_receipt.get("applier") or "")
    return not (applier and str(iv.get("verifier")) == applier)


# ---------------------------------------------------------------------------
# Lineage-bundle adapter (convergence item B contract)
# ---------------------------------------------------------------------------

def attach_to_lineage_bundle(
    bundle: dict[str, Any],
    retrieval_receipt: dict[str, Any] | None = None,
    application_receipt: dict[str, Any] | None = None,
    outcome_record: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Append D's receipts to a lineage bundle for the B reconstruction loop.

    Adds the keys "retrieval_receipts", "application_receipts" and
    "outcome_records" (lists). Returns a NEW bundle; the input is not
    mutated. B's receipt module (learn-builder's lane) consumes these keys
    to resolve its retrieval / applicability / application / outcome stages.
    """
    if not isinstance(bundle, dict):
        raise ValueError("BUNDLE_MUST_BE_OBJECT")
    out = dict(bundle)
    for key, value in (
        ("retrieval_receipts", retrieval_receipt),
        ("application_receipts", application_receipt),
        ("outcome_records", outcome_record),
    ):
        if value is None:
            continue
        existing = out.get(key)
        out[key] = ([dict(r) for r in existing] if isinstance(existing, list) else []) + [dict(value)]
    return out


def summarize_application_receipt(receipt: dict[str, Any]) -> str:
    """One-line human summary."""
    receipt = receipt if isinstance(receipt, dict) else {}
    return (
        "application %s | lesson=%s | retrieval_ref=%s | task=%s | applier=%s | "
        "e2_eligible=%s | outcome_ref=%s"
        % (
            receipt.get("receipt_id"), receipt.get("lesson_id"), receipt.get("retrieval_ref"),
            receipt.get("task_ref"), receipt.get("applier"),
            qualifies_for_e2(receipt), receipt.get("outcome_ref") or "none",
        )
    )
