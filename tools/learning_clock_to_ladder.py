"""Clock-to-ladder bridge: T6 VERIFIED meta row -> ladder evidence record.

Convergence items B/C (learn lane). The ladder
(tools/learning_evidence_ladder.py) computes the EARNED E0-E7 level from an
evidence bundle, but NOTHING in the tree produced that bundle from a
learn-clock T6 VERIFIED row: the assembler's runtime-record pass-through
(comprehension / transfer / successor_use / retention / mastery) has no
clock producer, so a T6 lesson earned E0 by construction -- the convergence
audit's D verdict was ABSENT for every lesson, and its E cross-check found
"NO producer" for E1. This module is that producer.

This module is the PRODUCER, not a second evaluator: it validates the T6
meta row against the EXTENDED T6 contract and builds the ladder-ready
record. The ladder's evaluate() remains the sole judge of the earned level.

Feed path (read this before wiring a caller): the record goes DIRECTLY to
learning_evidence_ladder.evaluate() with a caller-set claimed_level. It
does NOT go through assemble_evidence(): the assembler takes
application/outcome evidence as D-receipts attached to a lineage bundle,
and packaging clock fields as D-receipts would duplicate D's emitter
(PR #1882, not on main yet -- the assembler mirrors that contract for the
same reason). When D's emitter lands, a D-packaging step can sit beside
this bridge; until then the direct-to-evaluate path is the honest one.

EXTENDED T6 CONTRACT -- what a T6 meta row MUST carry to earn E1-E3:
  stage == 6, stage_name == "T6_VERIFIED" (T6_PROBE rows never qualify:
  FAIL / NO-TRANSFER-MEASURED emit no T6, by the tail wire's law)
  lesson_id matching LC-YYYYMMDD-NNN
  verdict == "PASS"
  judge_seat, author_seat -- nonempty; normalized judge != normalized author
    (the Inviolable, mechanical)
  verified_at -- nonempty, parseable ISO-8601 (naive assumed UTC)
  control_receipt, treatment_receipt -- nonempty strings (E1)
  retrieval_ref, task_ref, applier, applied_at -- nonempty; applied_at
    parseable ISO-8601 (E2). The T6 row carries the T5 application facts
    forward so one row is self-contained evidence.
  measured_effect -- nonempty STRING (E3). The ladder's _has() and D's
    outcome contract both require a string ("control 12/20 -> treatment
    19/20"), so a bare number is rejected, not coerced.
  independent_verification is CONSTRUCTED from judge_seat + verified_at:
  the judge's T6 verdict IS the independent verification -- no separate
  IV input. The judge must also differ (normalized) from the applier
  (the ladder's E3 executor-owned-observation rule).

Fail-closed rules (never repaired, never rounded up):
  - validate_t6_meta() returns audit codes; ANY code -> record None.
  - never raises on malformed input: malformed is unproven, not an exception.
  - never fabricates capture_receipt: E0 needs a caller-supplied
    capture_receipt (from the T1 row / lineage) with
    intelligent_block_id + captured_at. Without it the evidence omits the
    capture key and the ladder reports UNPROVEN -- which is the true state.
  - a row carrying any forbidden authority field is rejected (a receipt is
    evidence, never authority -- the #1712 lesson).
  - the bridge sets NO transfer / successor_use / retention / mastery /
    conflicts / stale keys: T6 proves E1-E3 only. E4-E7 need their own
    evidence, so a full T6 record earns exactly E3_INDEPENDENT.

Identity: separation checks use learning_admission_gate.normalize_identity
(strip + casefold) -- the ladder itself compares exact strings, so the
bridge normalizes BEFORE the ladder sees the seats; the ladder's
exact-match checks are a second layer, not the first.
KNOWN BOUNDARY (not fixed here): the canonical normalizer does NOT equate
hyphen with space, so "naya-verity" passes as a different seat from
"Naya Verity". The bridge faithfully applies the canonical rule; if the
admission-gate owner strengthens the normalizer (different-seat decision),
the bridge strengthens with it because it imports normalize_identity
instead of copying it. A test pins this behavior so the change is visible.

Named-next (NOT done here): extend the tail wire's `verify` command to
accept the extended fields (control/treatment receipts, retrieval/task/
applier/applied_at, measured_effect, verified_at) so a T6 emit writes a
bridge-ready row in one pass; upgrade the convergence audit's (C) T6 check
to call validate_t6_meta() instead of its inline thresholds.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

from learning_admission_gate import normalize_identity

SCHEMA = "NAYANET_LEARNING_CLOCK_TO_LADDER_V1"

_LESSON_RE = re.compile(r"^LC-\d{8}-\d{3}$")

# A receipt must never pose as its own authority (the #1712 defect).
# Same set as the assembler's -- duplicated as a literal, not imported,
# because the assembler's is private; the two must stay in sync.
_FORBIDDEN_AUTHORITY_FIELDS = frozenset(
    {"authorized", "is_authorized", "authority_granted",
     "grant", "grant_id", "self_authorized"}
)

_REQUIRED_STR_FIELDS = (
    "control_receipt",
    "treatment_receipt",
    "judge_seat",
    "author_seat",
    "retrieval_ref",
    "task_ref",
    "applier",
    "verified_at",
    "applied_at",
    "measured_effect",
    "verdict",
    "lesson_id",
)


def _nonempty_str(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _parse_ts(value: Any) -> datetime | None:
    """Parse an ISO-8601 timestamp. Naive values are assumed UTC.

    None if unparseable. Mirrors the admission gate's rule; kept local
    because the gate's parser is private.
    """
    if not _nonempty_str(value):
        return None
    text = str(value).strip()
    if text.endswith(("Z", "z")):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def validate_t6_meta(meta: Any) -> list[str]:
    """Audit a T6 clock meta row against the extended T6 contract.

    Returns audit codes; empty means the row is bridge-ready. Never raises.
    """
    codes: list[str] = []
    if not isinstance(meta, dict):
        return ["META_NOT_AN_OBJECT"]
    for field in sorted(_FORBIDDEN_AUTHORITY_FIELDS & set(meta.keys())):
        codes.append("FORBIDDEN_AUTHORITY_FIELD: meta carries %s" % field)
    if meta.get("stage") != 6:
        codes.append(
            "INVALID_STAGE: expected stage 6 (T6_VERIFIED), got %r"
            % (meta.get("stage"),))
    if "stage_name" in meta and meta.get("stage_name") != "T6_VERIFIED":
        codes.append(
            "INVALID_STAGE_NAME: expected T6_VERIFIED, got %r"
            % (meta.get("stage_name"),))
    lesson_id = meta.get("lesson_id")
    if not _nonempty_str(lesson_id) or not _LESSON_RE.match(str(lesson_id).strip()):
        codes.append("INVALID_LESSON_ID: %r" % (lesson_id,))
    if meta.get("verdict") != "PASS":
        codes.append("VERDICT_NOT_PASS: %r" % (meta.get("verdict"),))
    for field in _REQUIRED_STR_FIELDS:
        if field == "measured_effect":
            continue  # type-checked separately below
        if not _nonempty_str(meta.get(field)):
            codes.append("MISSING_REQUIRED_FIELD: %s" % field)
    measured = meta.get("measured_effect")
    if measured is None or (isinstance(measured, str) and not measured.strip()):
        codes.append("MISSING_REQUIRED_FIELD: measured_effect")
    elif not isinstance(measured, str):
        codes.append(
            "MEASURED_EFFECT_MUST_BE_STRING: ladder _has() and D's outcome "
            "contract require a string, got %s" % type(measured).__name__)
    for field in ("verified_at", "applied_at"):
        if _nonempty_str(meta.get(field)) and _parse_ts(meta.get(field)) is None:
            codes.append("INVALID_TIMESTAMP: %s=%r" % (field, meta.get(field)))
    judge = meta.get("judge_seat")
    author = meta.get("author_seat")
    applier = meta.get("applier")
    if _nonempty_str(judge) and _nonempty_str(author):
        if normalize_identity(judge) == normalize_identity(author):
            codes.append(
                "JUDGE_IS_AUTHOR: judge %r normalizes to author %r "
                "(Inviolable)" % (judge, author))
    if _nonempty_str(judge) and _nonempty_str(applier):
        if normalize_identity(judge) == normalize_identity(applier):
            codes.append(
                "JUDGE_IS_APPLIER: judge %r normalizes to applier %r "
                "(executor-owned observation)" % (judge, applier))
    return codes


def _validate_capture_receipt(capture: Any) -> list[str]:
    codes: list[str] = []
    if not isinstance(capture, dict):
        return ["INVALID_CAPTURE_RECEIPT: not an object"]
    for field in sorted(_FORBIDDEN_AUTHORITY_FIELDS & set(capture.keys())):
        codes.append(
            "FORBIDDEN_AUTHORITY_FIELD: capture_receipt carries %s" % field)
    if not _nonempty_str(capture.get("intelligent_block_id")):
        codes.append(
            "INVALID_CAPTURE_RECEIPT: missing intelligent_block_id")
    if not _nonempty_str(capture.get("captured_at")):
        codes.append("INVALID_CAPTURE_RECEIPT: missing captured_at")
    return codes


def t6_meta_to_record(
    meta: Any,
    capture_receipt: Any = None,
) -> tuple[dict[str, Any] | None, list[str]]:
    """Build the ladder-ready record for a T6 VERIFIED meta row.

    Returns (record, codes). ANY code -> record None (atomic, fail-closed).
    The record carries no claimed_level: the caller sets it for
    evaluate(). Never raises on malformed input.
    """
    try:
        codes = validate_t6_meta(meta)
        capture_codes: list[str] = []
        if capture_receipt is not None:
            capture_codes = _validate_capture_receipt(capture_receipt)
        codes.extend(capture_codes)
        if codes:
            return None, codes
        assert isinstance(meta, dict)  # validated above; keeps typing honest
        judge = str(meta["judge_seat"]).strip()
        author = str(meta["author_seat"]).strip()
        verified_at = str(meta["verified_at"]).strip()
        evidence: dict[str, Any] = {
            "comprehension": {
                "control_receipt": str(meta["control_receipt"]).strip(),
                "treatment_receipt": str(meta["treatment_receipt"]).strip(),
                "independent_verifier": judge,
                "verified_at": verified_at,
            },
            "application_receipt": {
                "retrieval_ref": str(meta["retrieval_ref"]).strip(),
                "task_ref": str(meta["task_ref"]).strip(),
                "applied_at": str(meta["applied_at"]).strip(),
                "applier": str(meta["applier"]).strip(),
            },
            "outcome": {
                "measured_effect": str(meta["measured_effect"]).strip(),
                "independent_verification": {
                    "verifier": judge,
                    "verified_at": verified_at,
                },
            },
        }
        if capture_receipt is not None:
            assert isinstance(capture_receipt, dict)  # validated above
            evidence["capture_receipt"] = {
                "intelligent_block_id": str(
                    capture_receipt["intelligent_block_id"]).strip(),
                "captured_at": str(capture_receipt["captured_at"]).strip(),
            }
        record = {
            "schema": SCHEMA,
            "id": str(meta["lesson_id"]).strip(),
            "producer_id": author,
            "evidence": evidence,
        }
        return record, []
    except Exception as exc:  # malformed input is unproven, never an exception
        return None, ["BRIDGE_ERROR: %s: %s" % (type(exc).__name__, exc)]
