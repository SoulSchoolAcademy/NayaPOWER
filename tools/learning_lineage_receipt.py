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
COMPLETE only when all 11 stages are PRESENT. On current main the five
post-promotion stages are UNINSTRUMENTED, so COMPLETE is unreachable --
that is the honest instrumentation gap, now visible in one place.

Pure functions only: no DB, no network. A reader assembles the bundle;
this module reconstructs and judges. Machine-falsifiable via
tests/test_learning_lineage_receipt.py.
"""

from __future__ import annotations

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
UNINSTRUMENTED_OWNERS: dict[str, str] = {
    "retrieval": "learn-builder (convergence item D: durable retrieval/application receipts)",
    "applicability": "learn-builder (convergence item D; #1733 decision-context boundary)",
    "application": "learn-builder (convergence item D)",
    "outcome": "learn-builder (convergence item D)",
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


def _stage(status: str, refs: dict[str, Any] | None = None, note: str = "") -> dict[str, Any]:
    return {"status": status, "refs": refs or {}, "note": note}


def _link_mismatch(label: str, expected: Any, actual: Any) -> str:
    return f"{label}: expected={expected!r} actual={actual!r}"


def reconstruct(bundle: dict[str, Any]) -> dict[str, Any]:
    """Reconstruct the universal lineage receipt for one learning.

    bundle keys (all optional except 'learning'):
      cognition_event, commit_receipt, intelligent_block, learning,
      relationship, checkpoint, verification, authority_ref_links
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

    # ---- post-promotion stages: uninstrumented on current main ----
    for stage in ("retrieval", "applicability", "application", "outcome",
                  "reuse", "generalization", "successor"):
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
