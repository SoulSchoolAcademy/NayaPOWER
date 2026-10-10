"""Canonical universal learning-lineage receipt (convergence item B).

One receipt reconstructs the full learning journey end-to-end:

    capture -> retention -> retrieval -> applicability -> application ->
    outcome -> verification -> promotion -> reuse -> generalization -> successor

The audit (2026-10-07) found lineage fragmented across JSONB links
(learning_evidence -> intelligent block -> relationship -> checkpoint ->
execution receipt -> causal verification -> successor) with no single
universal receipt making the chain trivially reconstructable. This module
is that receipt: given a bundle of the rows the runtime already persists,
it emits one schema'd object with every stage resolved, or fails closed
naming the exact broken hop.

LAW BAKED IN (the #1712 lesson): a receipt is evidence, never authority.
The receipt carries authority_refs as LINKS ONLY. It exposes no field any
authority gate may accept as a grant, and satisfies_authority() denies a
receipt presented alone -- always. Scorecard/receipt = qualification
evidence inside a Human-rooted authority envelope, never the envelope.

Stage states:
  PRESENT        emitter exists on current main and the link resolves
  PENDING        learning has not reached this stage yet (legitimate)
  GAP            emitter exists but the expected link is missing/broken
                 -> verdict BROKEN, gap names the exact hop
  UNINSTRUMENTED no emitter exists on current main -> explicit
                 known-unknown with the owning lane (never hidden)

Verdict: BROKEN if any GAP; PARTIAL if any PENDING/UNINSTRUMENTED;
COMPLETE only when all 11 stages are PRESENT. The retrieval /
applicability / application / outcome stages are UNINSTRUMENTED until a
reader attaches convergence-item-D receipts (retrieval_receipts,
application_receipts, outcome_records, attached via
attach_to_lineage_bundle()) -- the consumer wiring for that contract
lives in this module, so those four stages become machine-resolvable the
moment receipts exist. reuse / generalization / successor remain
uninstrumented (successor-builder's lane); COMPLETE stays unreachable
until those lanes emit -- the honest gap, visible in one place.

Pure functions only: no DB, no network. A reader assembles the bundle;
this module reconstructs and judges. Machine-falsifiable via
tests/test_learning_lineage_receipt.py and
tests/test_lineage_receipt_evidence_consumption.py.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any

SCHEMA = "NAYANET_LEARNING_LINEAGE_RECEIPT_V1"

STAGES: tuple[str, ...] = (
    "capture",
    "retention",
    "retrieval",
    "applicability",
    "application",
    "outcome",
    "verification",
    "promotion",
    "reuse",
    "generalization",
    "successor",
)

# Stages with no emitter on current main: explicit known-unknowns.
# retrieval / applicability / application / outcome stay UNINSTRUMENTED
# only until D-shaped receipts are attached to the bundle; the consumer
# wiring below resolves them then. The emitters live with the runtime and
# the Learning-team D instrument (PR #1882).
UNINSTRUMENTED_OWNERS: dict[str, str] = {
    "retrieval": "runtime + Learning-team D instrument (PR #1882); consumer wired -- attach via attach_to_lineage_bundle()",
    "applicability": "runtime + Learning-team D instrument (PR #1882); consumer wired",
    "application": "runtime + Learning-team D instrument (PR #1882); consumer wired",
    "outcome": "runtime + Learning-team D instrument (PR #1882); consumer wired",
    "reuse": "successor-builder",
    "generalization": "successor-builder",
    "successor": "successor-builder",
}

# Fields a receipt must NEVER carry: any one of these would let a receipt
# pose as its own authority (the exact #1712 defect).
FORBIDDEN_AUTHORITY_FIELDS = frozenset(
    {"authorized", "is_authorized", "authority_granted", "grant", "grant_id", "self_authorized"}
)

_PROMOTED_STATUSES = {"ACTIVE", "LEARNED"}


# ---------------------------------------------------------------------------
# Convergence consumer: D-shaped receipt attachment (items B + D)
#
# Convergence item D's emitter (tools/learning_application_receipt.py,
# Learning-team PR #1882) produces three append-only records:
#   retrieval_receipt   NAYANET_LEARNING_RETRIEVAL_RECEIPT_V1
#   application_receipt NAYANET_LEARNING_APPLICATION_RECEIPT_V1
#   outcome_record      NAYANET_LEARNING_OUTCOME_RECORD_V1
# A reader attaches them to a lineage bundle via attach_to_lineage_bundle()
# under the keys "retrieval_receipts", "application_receipts" and
# "outcome_records" (lists). This module CONSUMES those keys and resolves
# its retrieval / applicability / application / outcome stages from them --
# that is the convergence of B (lineage reconstructability) with D
# (durable receipts linked to outcome). D is not on main yet, so this
# consumer keys to the published schema contract, not to D's module.
#
# Fail-closed contract (never rounded up, never assumed):
#  - schema marker must match exactly the published schema string;
#  - the id must recompute from the apply-time core fields (sha256 of
#    canonical JSON, first 32 hex, RET-/APP-/OUT- prefix) -- a tampered
#    receipt fails integrity and the stage goes GAP, never PRESENT;
#  - lesson_id must equal the reconstructed learning's id;
#  - application receipts must resolve retrieval_ref to an attached
#    retrieval receipt; outcome records must resolve
#    application_receipt_id to an attached application receipt.
# A stage with attached-but-invalid evidence -> GAP naming the failure.
# A stage with no attached evidence -> UNINSTRUMENTED (honest), exactly
# as before this wiring. Attached evidence never becomes authority.
# ---------------------------------------------------------------------------

RETRIEVAL_SCHEMA = "NAYANET_LEARNING_RETRIEVAL_RECEIPT_V1"
APPLICATION_SCHEMA = "NAYANET_LEARNING_APPLICATION_RECEIPT_V1"
OUTCOME_SCHEMA = "NAYANET_LEARNING_OUTCOME_RECORD_V1"

_EVIDENCE_SCHEMA = {
    "retrieval": RETRIEVAL_SCHEMA,
    "application": APPLICATION_SCHEMA,
    "outcome": OUTCOME_SCHEMA,
}
_EVIDENCE_DIGEST_PREFIX = {"retrieval": "RET", "application": "APP", "outcome": "OUT"}
_EVIDENCE_ID_FIELD = {"retrieval": "receipt_id", "application": "receipt_id", "outcome": "record_id"}
_EVIDENCE_CORE_FIELDS = {
    # Must mirror the emitter's apply-time core exactly (see D module).
    "retrieval": ("schema", "lesson_id", "retriever", "retrieved_at",
                  "query_context", "lesson_content_sha"),
    "application": ("schema", "lesson_id", "retrieval_ref", "task_ref",
                    "applier", "applied_at"),
    "outcome": ("schema", "application_receipt_id", "lesson_id", "task_ref",
                "measured_effect", "observed_at"),
}
_EVIDENCE_BUNDLE_KEYS = {
    "retrieval": "retrieval_receipts",
    "application": "application_receipts",
    "outcome": "outcome_records",
}


def _canonical_core(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _recompute_evidence_id(kind: str, record: dict[str, Any]) -> str:
    core = {f: record.get(f) for f in _EVIDENCE_CORE_FIELDS[kind]}
    digest = hashlib.sha256(_canonical_core(core).encode("utf-8")).hexdigest()[:32]
    return "%s-%s" % (_EVIDENCE_DIGEST_PREFIX[kind], digest)


def _check_evidence(kind: str, record: Any, learning_id: Any) -> tuple[bool, str, str]:
    """Classify one attached evidence record.

    Returns (ok, evidence_id, failure). failure names the exact defect;
    ok=True means schema, integrity and lesson linkage all hold.
    """
    label = kind.upper()
    if not isinstance(record, dict):
        return False, "", "%s_ENTRY_NOT_OBJECT: attached evidence must be an object" % label
    expected_schema = _EVIDENCE_SCHEMA[kind]
    if record.get("schema") != expected_schema:
        return False, "", "%s_SCHEMA_MISMATCH: expected=%r actual=%r" % (
            label, expected_schema, record.get("schema"))
    rid = str(record.get(_EVIDENCE_ID_FIELD[kind]) or "")
    if rid != _recompute_evidence_id(kind, record):
        return False, "", "%s_INTEGRITY_FAILED: id=%r does not recompute from core fields" % (label, rid)
    if str(record.get("lesson_id") or "") != str(learning_id or ""):
        return False, "", "%s_LESSON_MISMATCH: record lesson=%r learning=%r" % (
            label, record.get("lesson_id"), learning_id)
    return True, rid, ""


def _resolve_evidence_stages(
    bundle: dict[str, Any],
    learning_id: Any,
    stages: dict[str, dict[str, Any]],
    gaps: list[str],
    links_verified: list[str],
    uninstrumented: list[str],
) -> None:
    """Resolve retrieval / applicability / application / outcome from
    attached D-shaped receipts. Mutates the shared stage lists."""

    def _mark_uninstrumented(stage: str) -> None:
        owner = UNINSTRUMENTED_OWNERS[stage]
        uninstrumented.append("%s: %s" % (stage, owner))
        stages[stage] = _stage("UNINSTRUMENTED", note="no receipts attached; owner: %s" % owner)

    attached_kinds = [k for k, key in _EVIDENCE_BUNDLE_KEYS.items() if bundle.get(key)]
    if not attached_kinds:
        for stage in ("retrieval", "applicability", "application", "outcome"):
            _mark_uninstrumented(stage)
        return

    # Classify every attached record: valid (id -> record) vs failures.
    valid: dict[str, dict[str, dict[str, Any]]] = {"retrieval": {}, "application": {}, "outcome": {}}
    broken_key = False
    for kind, key in _EVIDENCE_BUNDLE_KEYS.items():
        records = bundle.get(key)
        if records is None:
            continue
        if not isinstance(records, list):
            gaps.append("EVIDENCE_KEY_NOT_LIST: %s must be a list" % key)
            broken_key = True
            continue
        for record in records:
            ok, rid, failure = _check_evidence(kind, record, learning_id)
            if ok:
                valid[kind][rid] = record
            else:
                gaps.append(failure)

    # ---- retrieval: at least one integrity-verified receipt for the learning ----
    if bundle.get(_EVIDENCE_BUNDLE_KEYS["retrieval"]):
        rids = sorted(valid["retrieval"])
        if rids:
            stages["retrieval"] = _stage("PRESENT", {"receipt_ids": rids, "count": len(rids)})
            for rid in rids:
                links_verified.append("retrieval_receipt.%s -> learning.%s" % (rid, learning_id))
        else:
            stages["retrieval"] = _stage("GAP", note="retrieval receipts attached but none valid; see gaps")
    else:
        _mark_uninstrumented("retrieval")

    # ---- application: valid receipt whose retrieval_ref resolves ----
    if bundle.get(_EVIDENCE_BUNDLE_KEYS["application"]):
        bound, dangling = [], []
        for rid, rec in valid["application"].items():
            ref = str(rec.get("retrieval_ref") or "")
            (bound if ref in valid["retrieval"] else dangling).append((rid, ref))
        if dangling:
            for rid, ref in dangling:
                gaps.append("APPLICATION_RETRIEVAL_LINK_BROKEN: receipt=%s retrieval_ref=%r not attached"
                            % (rid, ref))
        if bound:
            stages["application"] = _stage("PRESENT", {
                "receipt_ids": sorted(r for r, _ in bound),
                "retrieval_refs": sorted({ref for _, ref in bound}),
            })
            for rid, ref in bound:
                links_verified.append("application_receipt.%s -> retrieval_receipt.%s" % (rid, ref))
        else:
            stages["application"] = _stage("GAP", note="application receipts attached but none resolve; see gaps")
    else:
        _mark_uninstrumented("application")

    # ---- applicability: rationale recorded at apply time on a valid receipt ----
    if bundle.get(_EVIDENCE_BUNDLE_KEYS["application"]):
        with_rationale = [rid for rid, rec in valid["application"].items()
                          if isinstance(rec.get("applicability"), dict)
                          and (str(rec["applicability"].get("relevance_rationale") or "").strip()
                               or str(rec["applicability"].get("task_match") or "").strip())]
        if with_rationale:
            stages["applicability"] = _stage("PRESENT", {
                "receipt_ids": sorted(with_rationale),
                "rationale": {rid: valid["application"][rid]["applicability"] for rid in sorted(with_rationale)},
            })
            links_verified.append("applicability.rationale recorded at apply time on %d receipt(s)"
                                  % len(with_rationale))
        elif valid["application"]:
            stages["applicability"] = _stage("PENDING",
                                            note="application evidence present; no applicability rationale recorded")
        else:
            stages["applicability"] = _stage("GAP", note="no valid application receipt carries an applicability rationale")
    else:
        _mark_uninstrumented("applicability")

    # ---- outcome: valid record resolving to an attached application receipt ----
    if bundle.get(_EVIDENCE_BUNDLE_KEYS["outcome"]):
        linked, unlinked = [], []
        for rid, rec in valid["outcome"].items():
            app_ref = str(rec.get("application_receipt_id") or "")
            (linked if app_ref in valid["application"] else unlinked).append((rid, app_ref))
        if unlinked:
            for rid, app_ref in unlinked:
                gaps.append("OUTCOME_APPLICATION_LINK_BROKEN: record=%s application_receipt_id=%r not attached"
                            % (rid, app_ref))
        if linked:
            verifiers = sorted({
                str((valid["outcome"][rid].get("independent_verification") or {}).get("verifier") or "")
                for rid, _ in linked
            } - {""})
            refs: dict[str, Any] = {"record_ids": sorted(r for r, _ in linked)}
            if verifiers:
                refs["independent_verifiers"] = verifiers
            stages["outcome"] = _stage("PRESENT", refs)
            for rid, app_ref in linked:
                links_verified.append("outcome_record.%s -> application_receipt.%s" % (rid, app_ref))
        else:
            stages["outcome"] = _stage("GAP", note="outcome records attached but none resolve; see gaps")
    else:
        _mark_uninstrumented("outcome")

    if broken_key:
        # A malformed evidence key poisons the evidence stages that depend on it.
        for stage in ("retrieval", "application", "applicability", "outcome"):
            if stages.get(stage, {}).get("status") == "UNINSTRUMENTED":
                stages[stage] = _stage("GAP", note="evidence key malformed; see gaps")


def _stage(status: str, refs: dict[str, Any] | None = None, note: str = "") -> dict[str, Any]:
    return {"status": status, "refs": refs or {}, "note": note}


def _link_mismatch(label: str, expected: Any, actual: Any) -> str:
    return f"{label}: expected={expected!r} actual={actual!r}"


def reconstruct(bundle: dict[str, Any]) -> dict[str, Any]:
    """Reconstruct the universal lineage receipt for one learning.

    bundle keys (all optional except 'learning'):
      cognition_event, commit_receipt, intelligent_block, learning,
      relationship, checkpoint, verification, authority_ref_links,
      retrieval_receipts, application_receipts, outcome_records
      (the last three are convergence-item-D receipts, attached via
      attach_to_lineage_bundle(); the resolver verifies their integrity
      and linkages before marking stages PRESENT)
    """
    gaps: list[str] = []
    links_verified: list[str] = []
    uninstrumented: list[str] = []
    stages: dict[str, dict[str, Any]] = {}

    if not isinstance(bundle, dict) or not isinstance(bundle.get("learning"), dict):
        receipt = _empty_receipt(None, "BUNDLE_MISSING_LEARNING")
        receipt["gaps"] = ["BUNDLE_MISSING_LEARNING"]
        receipt["verdict"] = "BROKEN"
        return receipt

    learning: dict[str, Any] = bundle["learning"]
    learning_id = learning.get("id")
    observed: dict[str, Any] = learning.get("observed_value") or {}
    status = str(learning.get("status") or "CANDIDATE")
    promoted = status in _PROMOTED_STATUSES

    # ---- capture: cognition event + intelligence_commit receipt ----
    event = bundle.get("cognition_event")
    commit = bundle.get("commit_receipt")
    if isinstance(event, dict) and isinstance(commit, dict):
        if str(observed.get("source_event_id") or "") == str(event.get("id") or ""):
            links_verified.append("learning.observed_value.source_event_id -> cognition_event.id")
        else:
            gaps.append(_link_mismatch("CAPTURE_EVENT_LINK_BROKEN",
                                       observed.get("source_event_id"), event.get("id")))
        if str(observed.get("commit_receipt_id") or "") == str(commit.get("id") or ""):
            links_verified.append("learning.observed_value.commit_receipt_id -> commit_receipt.id")
        else:
            gaps.append(_link_mismatch("CAPTURE_RECEIPT_LINK_BROKEN",
                                       observed.get("commit_receipt_id"), commit.get("id")))
        stages["capture"] = _stage(
            "PRESENT" if not any(g.startswith("CAPTURE_") for g in gaps) else "GAP",
            {"event_id": event.get("id"), "event_key": event.get("event_id"),
             "commit_receipt_id": commit.get("id"), "commit_action": commit.get("action")},
        )
    else:
        gaps.append("CAPTURE_ROWS_MISSING")
        stages["capture"] = _stage("GAP", note="cognition_event and/or commit_receipt absent from bundle")

    # ---- retention: intelligent block carries the learning ----
    block = bundle.get("intelligent_block")
    if isinstance(block, dict):
        if str(observed.get("intelligent_block_id") or "") == str(block.get("intelligent_block_id") or ""):
            links_verified.append("learning.observed_value.intelligent_block_id -> block.intelligent_block_id")
        else:
            gaps.append(_link_mismatch("RETENTION_BLOCK_LINK_BROKEN",
                                       observed.get("intelligent_block_id"), block.get("intelligent_block_id")))
        stages["retention"] = _stage(
            "PRESENT" if not any(g.startswith("RETENTION_") for g in gaps) else "GAP",
            {"intelligent_block_id": block.get("intelligent_block_id"),
             "understanding_state": block.get("understanding_state")},
        )
    else:
        gaps.append("RETENTION_BLOCK_MISSING")
        stages["retention"] = _stage("GAP", note="intelligent_block absent from bundle")

    # ---- assembled lineage links: lineage -> relationship -> index -> checkpoint ----
    for key, table_key, label in (
        ("lineage_id", None, "LINEAGE_ID"),
        ("relationship_id", "relationship", "RELATIONSHIP"),
        ("index_id", None, "INDEX_ID"),
        ("checkpoint_id", "checkpoint", "CHECKPOINT"),
    ):
        observed_val = observed.get(key)
        if not observed_val:
            gaps.append(f"{label}_MISSING_FROM_OBSERVED_VALUE")
            continue
        row = bundle.get(table_key) if table_key else {"id": observed_val}
        row_id = (row or {}).get("relationship_id" if table_key == "relationship" else "id")
        if table_key and (not isinstance(row, dict) or str(row_id or "") != str(observed_val or "")):
            gaps.append(_link_mismatch(f"{label}_LINK_BROKEN", observed_val, row_id))
        else:
            links_verified.append(f"learning.observed_value.{key} -> {label.lower()}")

    # ---- evidence stages: retrieval / applicability / application / outcome ----
    # Resolved from attached D-shaped receipts when present (consumer wiring
    # for the attach_to_lineage_bundle() contract); UNINSTRUMENTED otherwise.
    _resolve_evidence_stages(bundle, learning_id, stages, gaps, links_verified, uninstrumented)

    # ---- post-promotion stages: still uninstrumented on current main ----
    for stage in ("reuse", "generalization", "successor"):
        owner = UNINSTRUMENTED_OWNERS[stage]
        uninstrumented.append(f"{stage}: {owner}")
        stages[stage] = _stage("UNINSTRUMENTED", note=f"no emitter on current main; owner: {owner}")

    # ---- verification: independent causal verification evidence ----
    verification = bundle.get("verification")
    cvo_ref = None
    if isinstance(block, dict):
        for ref in (block.get("evidence_refs") or []):
            if isinstance(ref, dict) and ref.get("learning_verification_ref"):
                cvo_ref = ref["learning_verification_ref"]
                break
            if isinstance(ref, dict) and ref.get("causal_verification_id"):
                cvo_ref = ref["causal_verification_id"]
                break
    if promoted:
        if isinstance(verification, dict) and verification.get("cvo_id"):
            links_verified.append("verification.cvo_id -> independent causal verification")
            stages["verification"] = _stage("PRESENT",
                                            {"cvo_id": verification.get("cvo_id"),
                                             "method": verification.get("method")})
        elif cvo_ref:
            links_verified.append("block.evidence_refs -> causal verification ref")
            stages["verification"] = _stage("PRESENT", {"ref": cvo_ref})
        else:
            gaps.append("PROMOTION_WITHOUT_VERIFICATION: status=%s but no CVO ref or verification evidence" % status)
            stages["verification"] = _stage("GAP",
                                            note="promoted without independent verification evidence; SN-0340 UNKNOWN != PASS")
    else:
        if isinstance(verification, dict) and verification.get("cvo_id"):
            stages["verification"] = _stage("PRESENT", {"cvo_id": verification.get("cvo_id")})
        else:
            stages["verification"] = _stage("PENDING", note="candidate not yet verified; verification_method=%s"
                                            % str(learning.get("verification_method") or "")[:120])

    # ---- promotion: learning row + receipt learning[] entries ----
    if promoted:
        stages["promotion"] = _stage("PRESENT", {"learning_id": learning_id, "status": status,
                                                "provenance": learning.get("provenance")})
        links_verified.append("learning.status -> %s (promoted)" % status)
    else:
        stages["promotion"] = _stage("PENDING", note="status=%s; promotion requires independent verification" % status)

    # ---- authority_refs: LINKS ONLY. Never authority. ----
    authority_refs: list[str] = []
    for src in (bundle.get("authority_ref_links") or [],
                ((block.get("provenance") or {}) if isinstance(block, dict) else {}).get("law_authority_refs") or []):
        for ref in src if isinstance(src, list) else []:
            if isinstance(ref, str) and ref not in authority_refs:
                authority_refs.append(ref)

    verdict = "COMPLETE"
    if gaps:
        verdict = "BROKEN"
    elif uninstrumented or any(s["status"] == "PENDING" for s in stages.values()):
        verdict = "PARTIAL"

    receipt: dict[str, Any] = {
        "schema": SCHEMA,
        "learning_id": learning_id,
        "target_id": learning.get("target_id"),
        "level": learning.get("level"),
        "stages": stages,
        "links_verified": links_verified,
        "gaps": gaps,
        "uninstrumented": uninstrumented,
        "authority_refs": authority_refs,
        "verdict": verdict,
    }
    # Machine-enforced invariant: the receipt can never pose as authority.
    assert not (FORBIDDEN_AUTHORITY_FIELDS & set(receipt.keys())), "receipt carries forbidden authority field"
    return receipt


def _empty_receipt(learning_id: Any, note: str) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "learning_id": learning_id,
        "target_id": None,
        "level": None,
        "stages": {s: _stage("GAP", note=note) for s in STAGES},
        "links_verified": [],
        "gaps": [],
        "uninstrumented": [],
        "authority_refs": [],
        "verdict": "BROKEN",
    }


def satisfies_authority(receipt: dict[str, Any], grant: dict[str, Any] | None = None) -> bool:
    """Authority boundary, machine-enforced.

    A receipt alone NEVER satisfies an authority check -- that was the #1712
    defect (a fabricated scorecard receipt resolved authorized:true with no
    grant). Authority is decided by a Human-rooted grant object; the receipt
    only supplies qualification evidence inside that envelope.
    """
    if not isinstance(receipt, dict) or receipt.get("schema") != SCHEMA:
        return False
    if not isinstance(grant, dict):
        return False
    return grant.get("human_rooted") is True and bool(grant.get("grant_id"))


def summarize(receipt: dict[str, Any]) -> str:
    """One-line human summary of a lineage receipt."""
    stages = receipt.get("stages") or {}
    present = sum(1 for s in stages.values() if s.get("status") == "PRESENT")
    return ("lineage %s | %s | %d/%d stages present | %d gaps | %d uninstrumented | authority_refs=%d (links only)"
            % (receipt.get("learning_id"), receipt.get("verdict"), present, len(STAGES),
               len(receipt.get("gaps") or []), len(receipt.get("uninstrumented") or []),
               len(receipt.get("authority_refs") or [])))
