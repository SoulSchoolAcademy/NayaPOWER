#!/usr/bin/env python3
"""Validate BRAIN/08-SUCCESSION/0002-SUCCESSOR-HANDOFF-VERIFICATION-V1.json.

Fail-closed rules (UNKNOWN != PASS):
  - stage claims are only honored when the evidence the stage's gate requires
    is present; missing evidence -> the stage claim is rejected.
  - stage_history must equal stages[0..index(stage)] exactly: forward-only,
    one stage at a time, no skips, no backward moves.
  - completeness: every package section with empty/missing content must be
    named in gaps with a non-empty reason; a section that is neither present
    nor gapped is a fabrication risk -> rejected. A gapped section with
    content is contradictory -> rejected.
  - intelligence items must each carry a proof_state; VERIFIED requires a
    verification_ref; proof-less intelligence is UNVERIFIED, never VERIFIED.
  - authority: manufactures_authority must be false; missing authority
    context requires a READ_ONLY fallback; READ_ONLY requires empty authority
    context, FULL requires non-empty authority context.
  - continuity: the verification receipt must verify against the package's
    own declared basis SHA; a mismatched basis is STALE, never transferred.
    A FAIL receipt is recorded honestly but can never yield TRANSFERRED.
  - transfer: the decision outcome must equal the record outcome; terminal
    outcomes require their own evidence (PASS receipt; stale note; reason).
  - status must remain PROPOSED_CANONICAL until human-director ratification;
    CANONICAL is rejected here.
Usage: python3 tools/validate_successor_handoff.py
Exit 0 when the handoff file is internally consistent and evidence-bound.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "BRAIN/08-SUCCESSION/0002-SUCCESSOR-HANDOFF-VERIFICATION-V1.json"

SCHEMA = "naya.successor-handoff-verification.v1"
ALLOWED_STATUSES = {"PROPOSED_CANONICAL"}
STAGES = [
    "ASSEMBLE",
    "COMPLETENESS_CHECK",
    "AUTHORITY_BOUND",
    "CONTINUITY_VERIFY",
    "TRANSFER",
]
SECTIONS = [
    "identity",
    "current_reality",
    "applicable_intelligence",
    "authority_context",
    "unresolved_uncertainty",
    "recent_outcomes",
    "verified_learning",
    "active_work",
    "constraints",
    "proof",
    "next_actions",
]
OUTCOMES_ACTIVE = {"ACTIVE"}
TERMINAL_OUTCOMES = {"TRANSFERRED", "TRANSFERRED_READ_ONLY", "REJECTED", "STALE"}
OUTCOMES = OUTCOMES_ACTIVE | TERMINAL_OUTCOMES
FALLBACK_MODES = {"FULL", "READ_ONLY"}
PROOF_STATES = {"VERIFIED", "UNVERIFIED"}
RECEIPT_RESULTS = {"PASS", "FAIL"}
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def _nonempty_str(value):
    return isinstance(value, str) and bool(value.strip())


def _nonempty_str_list(value):
    return (
        isinstance(value, list)
        and bool(value)
        and all(_nonempty_str(v) for v in value)
    )


def _assemble_failures(rid, record):
    out = []
    manifest = record.get("source_manifest")
    if not isinstance(manifest, dict):
        out.append(f"{rid}: SOURCE_MANIFEST_NOT_AN_OBJECT")
    else:
        for section in SECTIONS:
            if not _nonempty_str(manifest.get(section)):
                out.append(
                    f"{rid}: SOURCE_MANIFEST_INCOMPLETE: section {section!r} "
                    "must name a non-empty canonical source"
                )
    if record.get("self_describing") is not True:
        out.append(
            f"{rid}: SELF_DESCRIBING_REQUIRED: self_describing must be true "
            "(schema id, section map, discovery pointer)"
        )
    if not SHA_RE.match(str(record.get("package_basis_sha") or "")):
        out.append(
            f"{rid}: BASIS_SHA_INVALID: package_basis_sha must be a 40-hex SHA"
        )
    return out


def _completeness_failures(rid, record):
    out = []
    sections = record.get("sections")
    if not isinstance(sections, dict):
        out.append(f"{rid}: SECTIONS_NOT_AN_OBJECT")
        return out
    gaps = record.get("gaps")
    if not isinstance(gaps, list):
        out.append(f"{rid}: GAPS_NOT_A_LIST")
        return out
    gap_sections = set()
    for g in gaps:
        if not isinstance(g, dict):
            out.append(f"{rid}: GAP_NOT_AN_OBJECT")
            continue
        sec = g.get("section")
        if sec not in SECTIONS:
            out.append(f"{rid}: GAP_SECTION_UNKNOWN: {sec!r}")
            continue
        if sec in gap_sections:
            out.append(f"{rid}: GAP_SECTION_DUPLICATE: {sec!r}")
        gap_sections.add(sec)
        if not _nonempty_str(g.get("reason")):
            out.append(f"{rid}: GAP_REASON_MISSING: {sec!r} needs a non-empty reason")
    for section in SECTIONS:
        content = sections.get(section)
        has_content = _nonempty_str(content)
        is_gapped = section in gap_sections
        if not has_content and not is_gapped:
            out.append(
                f"{rid}: SECTION_UNGAPPED_MISSING: {section!r} is empty and "
                "not named as an explicit gap (fabrication risk)"
            )
        if has_content and is_gapped:
            out.append(
                f"{rid}: GAP_CONTENT_CONFLICT: {section!r} has content but is "
                "also listed as a gap"
            )
    items = record.get("intelligence_items")
    if not isinstance(items, list) or not items:
        out.append(f"{rid}: INTELLIGENCE_ITEMS_MISSING: non-empty list required")
    else:
        for i, item in enumerate(items):
            if not isinstance(item, dict) or not _nonempty_str(item.get("key")):
                out.append(f"{rid}: INTELLIGENCE_ITEM_INVALID: item {i}")
                continue
            state = item.get("proof_state")
            if state not in PROOF_STATES:
                out.append(
                    f"{rid}: INTELLIGENCE_PROOF_STATE_INVALID: {state!r} "
                    "must be VERIFIED or UNVERIFIED"
                )
            elif state == "VERIFIED" and not _nonempty_str(item.get("verification_ref")):
                out.append(
                    f"{rid}: VERIFIED_WITHOUT_REF: {item.get('key')!r} claims "
                    "VERIFIED with no verification_ref"
                )
    return out


def _authority_failures(rid, record):
    out = []
    check = record.get("authority_check")
    if not isinstance(check, dict):
        out.append(f"{rid}: AUTHORITY_CHECK_NOT_AN_OBJECT")
    else:
        if check.get("manufactures_authority") is not False:
            out.append(
                f"{rid}: AUTHORITY_CLAIM_REJECTED: manufactures_authority "
                "must be false — a successor package never manufactures authority"
            )
        if not _nonempty_str(check.get("note")):
            out.append(f"{rid}: AUTHORITY_NOTE_MISSING")
    mode = record.get("fallback_mode")
    if mode not in FALLBACK_MODES:
        out.append(f"{rid}: FALLBACK_MODE_INVALID: {mode!r}")
        return out
    sections = record.get("sections") or {}
    auth_present = _nonempty_str(sections.get("authority_context"))
    if mode == "FULL" and not auth_present:
        out.append(
            f"{rid}: AUTHORITY_CONTEXT_MISSING_NO_FALLBACK: FULL mode requires "
            "a non-empty authority_context section; declare READ_ONLY instead"
        )
    if mode == "READ_ONLY" and auth_present:
        out.append(
            f"{rid}: FALLBACK_CONTRADICTS_CONTEXT: READ_ONLY mode requires an "
            "empty authority_context section"
        )
    return out


def _continuity_failures(rid, record):
    out = []
    receipt = record.get("verification_receipt")
    if not isinstance(receipt, dict):
        out.append(f"{rid}: RECEIPT_NOT_AN_OBJECT")
        return out
    sha = receipt.get("verified_against_sha")
    if not SHA_RE.match(str(sha or "")):
        out.append(
            f"{rid}: RECEIPT_SHA_INVALID: verified_against_sha must be 40-hex"
        )
    elif sha != record.get("package_basis_sha"):
        out.append(
            f"{rid}: STALE_BASIS_MISMATCH: receipt verifies {sha!r} but the "
            "package basis is {!r} — stale package, never transferred".format(
                record.get("package_basis_sha")
            )
        )
    if not _nonempty_str_list(receipt.get("checks")):
        out.append(
            f"{rid}: RECEIPT_CHECKS_MISSING: checks must be a non-empty list "
            "of non-empty strings"
        )
    if receipt.get("result") not in RECEIPT_RESULTS:
        out.append(
            f"{rid}: RECEIPT_RESULT_INVALID: {receipt.get('result')!r} "
            "must be PASS or FAIL"
        )
    if not _nonempty_str(receipt.get("verifier")):
        out.append(f"{rid}: RECEIPT_VERIFIER_MISSING")
    return out


def _transfer_failures(rid, record):
    out = []
    decision = record.get("transfer_decision")
    if not isinstance(decision, dict):
        out.append(f"{rid}: DECISION_NOT_AN_OBJECT")
        return out
    outcome = record.get("outcome")
    if decision.get("outcome") != outcome:
        out.append(
            f"{rid}: DECISION_OUTCOME_MISMATCH: decision says "
            f"{decision.get('outcome')!r} but record outcome is {outcome!r}"
        )
    if not _nonempty_str(decision.get("declared_at")):
        out.append(f"{rid}: DECISION_DECLARED_AT_MISSING")
    if not _nonempty_str(decision.get("note")):
        out.append(f"{rid}: DECISION_NOTE_MISSING")
    receipt = record.get("verification_receipt") or {}
    receipt_ok = receipt.get("result") == "PASS"
    if outcome in {"TRANSFERRED", "TRANSFERRED_READ_ONLY"} and not receipt_ok:
        out.append(
            f"{rid}: TRANSFER_WITHOUT_PASS: {outcome} requires a PASS "
            "continuity receipt (a FAIL receipt halts the handoff)"
        )
    mode = record.get("fallback_mode")
    if outcome == "TRANSFERRED" and mode != "FULL":
        out.append(
            f"{rid}: FULL_TRANSFER_READ_ONLY_FALLBACK: TRANSFERRED requires "
            "fallback_mode FULL"
        )
    if outcome == "TRANSFERRED_READ_ONLY" and mode != "READ_ONLY":
        out.append(
            f"{rid}: READ_ONLY_TRANSFER_FULL_FALLBACK: TRANSFERRED_READ_ONLY "
            "requires fallback_mode READ_ONLY"
        )
    if outcome == "STALE" and not _nonempty_str(record.get("staleness_note")):
        out.append(
            f"{rid}: STALE_NOTE_MISSING: STALE requires a note naming the "
            "newer canonical head"
        )
    if outcome == "REJECTED" and not _nonempty_str(record.get("rejection_reason")):
        out.append(
            f"{rid}: REJECTION_REASON_MISSING: REJECTED requires a "
            "rejection_reason (halt; alert the human director)"
        )
    return out


def _record_failures(rid, record):
    out = []
    stage = record.get("stage")
    if stage not in STAGES:
        out.append(f"{rid}: STAGE_INVALID: {stage!r} not in handoff stages")
        return out
    outcome = record.get("outcome", "ACTIVE")
    if outcome not in OUTCOMES:
        out.append(f"{rid}: OUTCOME_INVALID: {outcome!r}")
    idx = STAGES.index(stage)
    expected_history = STAGES[: idx + 1]
    if record.get("stage_history") != expected_history:
        out.append(
            f"{rid}: STAGE_HISTORY_INVALID: {record.get('stage_history')!r} "
            f"!= {expected_history!r} (forward-only, no skips, no backward)"
        )
    if stage != "TRANSFER" and outcome != "ACTIVE":
        out.append(
            f"{rid}: OUTCOME_PREMATURE: terminal outcome {outcome!r} at stage "
            f"{stage} — terminal outcomes belong at TRANSFER"
        )
    if stage == "TRANSFER" and outcome == "ACTIVE":
        out.append(f"{rid}: OUTCOME_MISSING: TRANSFER stage needs a terminal outcome")
    gate_stages = STAGES[: idx + 1]
    if "ASSEMBLE" in gate_stages:
        out.extend(_assemble_failures(rid, record))
    if "COMPLETENESS_CHECK" in gate_stages:
        out.extend(_completeness_failures(rid, record))
    if "AUTHORITY_BOUND" in gate_stages:
        out.extend(_authority_failures(rid, record))
    if "CONTINUITY_VERIFY" in gate_stages:
        out.extend(_continuity_failures(rid, record))
    if "TRANSFER" in gate_stages:
        out.extend(_transfer_failures(rid, record))
    return out


def failures(data):
    out = []
    if data.get("schema") != SCHEMA:
        out.append(f"SCHEMA_MISMATCH: {data.get('schema')!r} != {SCHEMA!r}")
    if data.get("status") not in ALLOWED_STATUSES:
        out.append(
            f"STATUS_NOT_PROPOSED_CANONICAL: {data.get('status')!r} "
            "(CANONICAL requires human-director ratification)"
        )
    if data.get("stages") != STAGES:
        out.append(
            f"STAGE_ORDER_MISMATCH: {data.get('stages')!r} != {STAGES!r} "
            "(pipeline is fixed by the contract V1)"
        )
    if not SHA_RE.match(str(data.get("as_of") or "")):
        out.append(f"AS_OF_NOT_PINNED_SHA: {data.get('as_of')!r}")
    records = data.get("records")
    if not isinstance(records, list):
        out.append("RECORDS_NOT_A_LIST")
        return out
    seen = set()
    for i, record in enumerate(records):
        if not isinstance(record, dict):
            out.append(f"RECORD_{i}_NOT_AN_OBJECT")
            continue
        rid = record.get("record_id")
        if not _nonempty_str(rid):
            out.append(f"RECORD_{i}: RECORD_ID_MISSING")
            rid = f"RECORD_{i}"
        if rid in seen:
            out.append(f"{rid}: RECORD_ID_DUPLICATE")
        seen.add(rid)
        out.extend(_record_failures(rid, record))
    return out


def main() -> int:
    try:
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    except Exception as exc:  # fail closed on unreadable fixture
        print(json.dumps({"schema": "naya.successor-handoff-verification.validation-report",
                          "failures": [f"FIXTURE_UNREADABLE: {exc}"],
                          "passed": False}, indent=2))
        return 1
    fails = failures(data)
    print(json.dumps({"schema": "naya.successor-handoff-verification.validation-report",
                      "as_of": data.get("as_of"), "failures": fails,
                      "passed": not fails}, indent=2))
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
