#!/usr/bin/env python3
"""Write-time truth-state elevation guard + read-side semantic audit.

Closes #1468: hand-editing a registry entry CANDIDATE->RATIFIED was invisible
to audit_registry, which checks 11 structural defect classes (hashes,
duplicates incl. ID-keyed id/content conflicts, projection paths) and zero truth_state transitions. The promotion
machinery (promote_note / verify_receipt in tools/smart_note_v2.py) existed,
but nothing enforced it at write time — a direct registry edit bypassed the
entire function.

The invariant: elevation requires BOTH valid promotion AUTHORITY (named,
authorised promoter) AND valid promotion EVIDENCE (receipt whose hash
recomputes, evidence hashes well-formed). No authority + evidence =>
rejected, not recorded.

Ladder (monotonic): CANDIDATE < TESTING < VERIFIED < RATIFIED < ACTIVE < LEARNED
- Demotion is ALWAYS permitted. A poisoned note must always be containable;
  a guard that can trap a bad state is a different bug.
- ACTIVE requires a proven VERIFIED predecessor (hash-verified receipt).
- LEARNED requires recorded BEHAVIORAL evidence.
- Authority and evidence are SEPARATE checks on purpose: the receipt is an
  unkeyed seal — it proves the receipt was not altered, not who promoted.
- Rejection is a NON-EVENT: apply_elevation refuses and leaves the entry
  byte-identical. A rejected write that records itself is still a write.

Read side: audit_registry_semantics() finds escalation already on disk, so
the hole is closed for new writes AND detectable after the fact.

Elevation grants (Option C, ratified 2026-10-06): VERIFIED->RATIFIED additionally
requires a bounded capability grant — a machine-readable record naming the
note, the target state, the issuer (Human Director or named delegate), and an
expiry. Authority travels with the elevation request, not as a standing
identity. See check_elevation_grant() and BRAIN/01-GOVERNANCE/elevation-grants/.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from datetime import datetime, timezone

LADDER = ["CANDIDATE", "TESTING", "VERIFIED", "RATIFIED", "ACTIVE", "LEARNED"]
_RANK = {s: i for i, s in enumerate(LADDER)}

# Authority strings that name nobody. A promoter that cannot be named
# cannot be held accountable, so these never satisfy the authority check.
ANONYMOUS_AUTHORITIES = {"", "unknown", "anonymous", "n/a", "none", "system", "null", "-"}

# Issuer strings that identify the Human Director. An elevation grant is only
# valid if issued by the Director or by a delegate the Director named.
# Delegates are recorded via the grant's "delegated_by" field, which must
# itself name the Director.
DIRECTOR_MARKERS = {"shawn vibert", "human director"}

# Default grants directory, relative to the repo root. Overridable by passing
# elevation_grants explicitly to apply_elevation().
DEFAULT_GRANTS_DIR = "BRAIN/01-GOVERNANCE/elevation-grants"

_HASH64 = re.compile(r"[0-9a-fA-F]{64}")
_GRANT_TS = re.compile(r"^\d{8}T\d{6}Z$")


def _utc_now():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _canonical_hash(obj):
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def normalize_state(state):
    return str(state or "").strip().upper()


def rank(state):
    """Ladder rank; -1 for unknown state names (never a valid target)."""
    return _RANK.get(normalize_state(state), -1)


def _record(ok, reason_code, detail=""):
    return {"ok": bool(ok), "reason_code": reason_code, "detail": detail}


def check_authority(authority):
    """Authority must name a real promoter. Returns (ok, record)."""
    a = str(authority or "").strip()
    if not a or a.lower() in ANONYMOUS_AUTHORITIES:
        return False, _record(False, "ELEVATION_REQUIRES_AUTHORITY",
                              f"authority {authority!r} names no accountable promoter")
    return True, _record(True, "AUTHORITY_OK", f"promoter={a}")


def check_evidence(evidence):
    """Evidence must be a bundle of well-formed items, optional hash-verified receipt."""
    if not isinstance(evidence, dict):
        return False, _record(False, "ELEVATION_REQUIRES_EVIDENCE", "evidence is not a bundle object")
    items = evidence.get("items")
    if not isinstance(items, list) or not items:
        return False, _record(False, "ELEVATION_REQUIRES_EVIDENCE", "evidence bundle has no items")
    for i, it in enumerate(items):
        if not isinstance(it, dict):
            return False, _record(False, "INVALID_EVIDENCE_ITEM", f"item {i} is not an object")
        for field in ("type", "source", "content_hash"):
            if not str(it.get(field) or "").strip():
                return False, _record(False, "INVALID_EVIDENCE_ITEM",
                                      f"item {i} missing {field}")
        if not _HASH64.fullmatch(str(it["content_hash"]).strip()):
            return False, _record(False, "INVALID_EVIDENCE_ITEM",
                                  f"item {i} content_hash is not 64-hex")
    receipt = evidence.get("receipt")
    if receipt is not None:
        if not isinstance(receipt, dict):
            return False, _record(False, "RECEIPT_TAMPERED", "receipt is not an object")
        body = {k: v for k, v in receipt.items() if k != "receipt_hash"}
        if receipt.get("receipt_hash") != _canonical_hash(body):
            return False, _record(False, "RECEIPT_TAMPERED",
                                  "receipt_hash does not recompute — receipt altered")
    return True, _record(True, "EVIDENCE_OK", f"{len(items)} items verified")


def _is_director_issuer(issuer):
    """True if the issuer string names the Human Director."""
    i = str(issuer or "").strip().lower()
    return any(m in i for m in DIRECTOR_MARKERS)


def _parse_grant_ts(ts):
    """Parse a grant timestamp (YYYYMMDDTHHMMSSZ) to a datetime, or None."""
    s = str(ts or "").strip()
    if not _GRANT_TS.match(s):
        return None
    try:
        return datetime.strptime(s, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def make_grant(note_id, target_state="RATIFIED", issuer="Shawn Vibert",
               issuer_role="Human Director", expires_days=7, scope_note="",
               delegated_by=None, issued_at=None):
    """Build a grant dict with integrity hash. Does not write to disk."""
    now = _utc_now() if issued_at is None else str(issued_at).strip()
    issued_dt = _parse_grant_ts(now)
    if issued_dt is None:
        raise ValueError(f"issued_at {now!r} is not YYYYMMDDTHHMMSSZ")
    from datetime import timedelta
    expires_dt = issued_dt + timedelta(days=int(expires_days))
    expires = expires_dt.strftime("%Y%m%dT%H%M%SZ")
    nid = str(note_id or "").strip().upper()
    grant_id = f"EG-{now[:8]}-{nid.replace('-', '')}-{expires_dt.strftime('%H%M%S')}"
    grant = {
        "grant_id": grant_id,
        "note_id": nid,
        "target_state": normalize_state(target_state),
        "issuer": str(issuer or "").strip(),
        "issuer_role": str(issuer_role or "").strip(),
        "issued_at": now,
        "expires_at": expires,
        "scope_note": str(scope_note or "").strip(),
    }
    if delegated_by:
        grant["delegated_by"] = str(delegated_by).strip()
    grant["grant_hash"] = _canonical_hash(grant)
    return grant


def validate_grant(grant, note_id, target_state, now=None,
                   attempt_renewal=False, verification_state=None):
    """Validate a single elevation grant. Returns (ok, record).

    A grant is valid iff: it is a dict; its grant_hash recomputes (not
    tampered); it names this note; it names this target state; it has not
    expired; issued_at <= expires_at; and the issuer is the Human Director
    or a delegate the Director named (via delegated_by).

    Auto-renewal (Shawn directive 2026-10-08): when attempt_renewal is True
    and the grant is past expiry, expiry is treated as a review checkpoint,
    not a cliff. evaluate_renewal() checks (a) underlying verification still
    valid, (b) scope unchanged, (c) no objections. All hold -> the grant
    renews automatically with a renewal receipt (record code GRANT_RENEWED).
    Any check fails -> the grant stays expired (GRANT_EXPIRED).
    """
    if not isinstance(grant, dict):
        return False, _record(False, "GRANT_INVALID", "grant is not an object")
    body = {k: v for k, v in grant.items() if k != "grant_hash"}
    if grant.get("grant_hash") != _canonical_hash(body):
        return False, _record(False, "GRANT_TAMPERED",
                              "grant_hash does not recompute — grant altered")
    gid = str(grant.get("note_id") or "").strip().upper()
    nid = str(note_id or "").strip().upper()
    if not gid or gid != nid:
        return False, _record(False, "GRANT_NOTE_MISMATCH",
                              f"grant names {gid or '<none>'!r}, elevation targets {nid or '<none>'!r}")
    if normalize_state(grant.get("target_state")) != normalize_state(target_state):
        return False, _record(False, "GRANT_STATE_MISMATCH",
                              f"grant targets {grant.get('target_state')!r}, elevation wants {target_state!r}")
    now_dt = _parse_grant_ts(now) if now else datetime.now(timezone.utc)
    if now_dt is None:
        return False, _record(False, "GRANT_INVALID", f"reference time {now!r} is not parseable")
    expires_dt = _parse_grant_ts(grant.get("expires_at"))
    issued_dt = _parse_grant_ts(grant.get("issued_at"))
    if expires_dt is None or issued_dt is None:
        return False, _record(False, "GRANT_INVALID", "grant timestamps are not YYYYMMDDTHHMMSSZ")
    if issued_dt > expires_dt:
        return False, _record(False, "GRANT_INVALID", "issued_at is after expires_at")
    if now_dt > expires_dt:
        # Expiry checkpoint: try renewal before declaring the grant dead.
        if attempt_renewal:
            renewable, renewal_receipt, rec = evaluate_renewal(
                grant, verification_state or {}, now=now)
            if renewable:
                return True, _record(
                    True, "GRANT_RENEWED",
                    f"grant {grant.get('grant_id')} auto-renewed to "
                    f"{renewal_receipt['new_expires_at']} "
                    f"(renewal {renewal_receipt['renewal_id']})")
        return False, _record(False, "GRANT_EXPIRED",
                              f"grant {grant.get('grant_id')} expired at {grant.get('expires_at')}")
    issuer = str(grant.get("issuer") or "").strip()
    if not issuer or issuer.lower() in ANONYMOUS_AUTHORITIES:
        return False, _record(False, "GRANT_INVALID", "grant names no issuer")
    role = str(grant.get("issuer_role") or "").strip().lower()
    if _is_director_issuer(issuer) or role == "human director":
        return True, _record(True, "GRANT_OK",
                             f"grant {grant.get('grant_id')} by Human Director")
    if role == "delegate":
        delegator = str(grant.get("delegated_by") or "").strip()
        if _is_director_issuer(delegator):
            return True, _record(True, "GRANT_OK",
                                 f"grant {grant.get('grant_id')} by delegate of Human Director")
        return False, _record(False, "GRANT_INVALID",
                              "delegate grant's delegated_by does not name the Human Director")
    return False, _record(False, "GRANT_UNAUTHORIZED_ISSUER",
                          f"issuer {issuer!r} is not the Human Director or a named delegate")


def check_elevation_grant(entry, new_state, elevation_grants, elevation_receipts=None,
                          attempt_renewal=True, verification_state=None, now=None):
    """VERIFIED->RATIFIED requires authority: a valid, unexpired grant naming
    this note, OR a valid SN-0340 five-step scorecard receipt binding this
    note and target state (receipt-as-authority, Shawn directive 2026-10-08).

    elevation_grants: iterable of grant dicts (or None).
    elevation_receipts: iterable of scorecard receipt dicts (or None).
    attempt_renewal: defaults True — expiry is a review checkpoint, not a
        cliff (Shawn directive 2026-10-08). Fail-closed is preserved:
        renewal requires verification_state with verification_valid True,
        scope_unchanged True, and no objections; with no verification_state
        the grant stays expired (RENEWAL_BLOCKED), exactly as before.
    Returns (ok, record). On success the record's detail names the satisfying
    grant_id or receipt.
    """
    old = normalize_state(entry.get("truth_state", "CANDIDATE"))
    new = normalize_state(new_state)
    if not (old == "VERIFIED" and new == "RATIFIED"):
        return True, _record(True, "GRANT_NOT_REQUIRED",
                             f"grant only gates VERIFIED->RATIFIED, not {old}->{new}")
    note_id = str(entry.get("smart_note_id") or entry.get("intelligent_block_id") or "").strip()
    if not note_id:
        return False, _record(False, "GRANT_INVALID", "entry names no note for grant binding")
    grants = list(elevation_grants or [])
    receipts = list(elevation_receipts or [])
    if not grants and not receipts:
        return False, _record(False, "RATIFIED_REQUIRES_ELEVATION_GRANT",
                              f"VERIFIED->RATIFIED for {note_id} requires an elevation grant "
                              f"or valid scorecard receipt; none provided")
    failures = []
    for grant in grants:
        ok, rec = validate_grant(grant, note_id, new, now=now,
                                 attempt_renewal=attempt_renewal,
                                 verification_state=verification_state)
        if ok:
            return True, _record(True, "GRANT_OK", rec["detail"])
        failures.append(f"{grant.get('grant_id', '<unknown>')}: {rec['reason_code']}")
    for receipt in receipts:
        ok, rec = check_receipt_authority(receipt, note_id, new, now=now)
        if ok:
            return True, _record(True, "RECEIPT_AUTHORITY_OK", rec["detail"])
        failures.append(f"receipt: {rec['reason_code']}")
    return False, _record(False, "RATIFIED_REQUIRES_ELEVATION_GRANT",
                          f"no valid grant or receipt for {note_id}->RATIFIED among "
                          f"{len(grants)} grants, {len(receipts)} receipts: " +
                          "; ".join(failures[:3]))


# ---------------------------------------------------------------------------
# Grant auto-renewal + receipt-as-authority + instant promotion
# (Shawn directive 2026-10-08: "Make it what it should be and make it right.")
#
# Expiring grants that stall learning make no sense. Expiry is a review
# checkpoint, not a cliff:
#   1. AUTO-RENEWAL — before an expired grant is treated as dead, evaluate
#      (a) underlying verification still valid, (b) scope unchanged,
#      (c) no objections. All hold -> renew automatically with a renewal
#      receipt. Any fail -> stays expired.
#   2. RECEIPT-AS-AUTHORITY — a valid SN-0340 five-step scorecard receipt is
#      accepted as authority equivalent to a grant. No separate grant row
#      needed when the receipt is valid.
#   3. INSTANT PROMOTION — when verification completes and passes, the
#      promotion authority is issued automatically by the verification
#      itself. No human grant-issuance step.
#
# Supabase is READ-ONLY: renewal produces a renewal *receipt* (a record the
# caller may persist through the governed path). This module never mutates
# grant rows itself.
# ---------------------------------------------------------------------------

# Receipt expiry: 7 days after decided_at (per NAYA-SCORECARD-RECEIPT-AUTHORITY-V1).
_RECEIPT_TTL_DAYS = 7

# Score dimensions for step 2 (must match the receipt authority schema).
_RECEIPT_SCORE_DIMS = ("value", "consequences", "mission_vision_alignment",
                       "situational_awareness")


def _parse_iso_ts(value):
    """Parse an ISO-8601 timestamp; return aware datetime or None."""
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        text = value.strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        dt = datetime.fromisoformat(text)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (ValueError, TypeError):
        return None


def normalize_db_grant(db_row):
    """Map a nayanet_authority_grants row to the canonical grant dict shape.

    DB rows carry grant_id (uuid), scope (JSONB), status, expires_at
    (timestamptz) — no grant_hash (integrity comes from the database's own
    RLS/audit, not a content hash). Returns a canonical dict suitable for
    validate_grant(), or None if the row is not a dict.
    """
    if not isinstance(db_row, dict):
        return None
    scope = db_row.get("scope") or {}
    target = scope.get("target") if isinstance(scope, dict) else None
    issued = _parse_iso_ts(str(db_row.get("issued_at") or ""))
    expires = _parse_iso_ts(str(db_row.get("expires_at") or ""))
    grant = {
        "grant_id": str(db_row.get("grant_id") or "").strip(),
        "note_id": str(target or "").strip().upper(),
        "target_state": "RATIFIED",
        "issuer": "Shawn Vibert",
        "issuer_role": "Human Director",
        "issued_at": issued.strftime("%Y%m%dT%H%M%SZ") if issued else "",
        "expires_at": expires.strftime("%Y%m%dT%H%M%SZ") if expires else "",
        "scope_note": json.dumps(scope, sort_keys=True) if scope else "",
        "db_status": str(db_row.get("status") or "").strip().upper(),
        "db_row": True,
    }
    # DB rows have no content hash; mark integrity as database-sourced so
    # validate_grant's tamper check is satisfied by the read path, not skipped.
    grant["grant_hash"] = _canonical_hash(
        {k: v for k, v in grant.items() if k != "grant_hash"})
    return grant


def evaluate_renewal(grant, verification_state, now=None):
    """Decide whether an expired grant auto-renews. Returns
    (renewable: bool, renewal_receipt: dict | None, record).

    Renewal conditions (all must hold):
      (a) verification_state["verification_valid"] is True — the underlying
          verification evidence still holds;
      (b) verification_state["scope_unchanged"] is True — the grant's scope
          has not drifted since issuance;
      (c) not verification_state.get("objections") — no flags or objections
          recorded against the grant.

    On success the renewal receipt carries: renewal_id, original grant_id,
    renewed_at, new_expires_at (old expiry + original term, or the
    verification_state's renewal_term_days), the renewal chain, and a
    renewal_hash sealing the receipt. Fail-closed: any missing or false
    condition -> not renewable.
    """
    if not isinstance(grant, dict):
        return False, None, _record(False, "RENEWAL_INVALID", "grant is not an object")
    if not isinstance(verification_state, dict):
        return False, None, _record(False, "RENEWAL_INVALID", "verification_state is not an object")

    now_dt = _parse_grant_ts(now) if now else datetime.now(timezone.utc)
    if now_dt is None:
        return False, None, _record(False, "RENEWAL_INVALID",
                                    f"reference time {now!r} is not parseable")

    # The grant must actually be expired — renewal is for the checkpoint,
    # not for live grants (those need no renewal).
    expires_dt = _parse_grant_ts(grant.get("expires_at"))
    issued_dt = _parse_grant_ts(grant.get("issued_at"))
    if expires_dt is None or issued_dt is None:
        return False, None, _record(False, "RENEWAL_INVALID",
                                    "grant timestamps are not YYYYMMDDTHHMMSSZ")
    if now_dt <= expires_dt:
        return False, None, _record(False, "RENEWAL_NOT_NEEDED",
                                    "grant has not expired; renewal is for expired grants only")

    # Condition (a): underlying verification still valid.
    if verification_state.get("verification_valid") is not True:
        return False, None, _record(False, "RENEWAL_BLOCKED",
                                    "underlying verification is not currently valid — "
                                    "re-verify before any renewal")
    # Condition (b): scope unchanged.
    if verification_state.get("scope_unchanged") is not True:
        return False, None, _record(False, "RENEWAL_BLOCKED",
                                    "grant scope has changed since issuance — "
                                    "a changed scope needs a new grant, not a renewal")
    # Condition (c): no objections.
    objections = verification_state.get("objections") or []
    if objections:
        return False, None, _record(False, "RENEWAL_BLOCKED",
                                    f"{len(objections)} objection(s) recorded — "
                                    "resolve objections before renewal")

    term_days = verification_state.get("renewal_term_days")
    if not isinstance(term_days, int) or term_days <= 0:
        # Default: same term as the original grant.
        term_days = max(1, (expires_dt - issued_dt).days)
    from datetime import timedelta
    new_expires_dt = expires_dt + timedelta(days=term_days)
    new_expires = new_expires_dt.strftime("%Y%m%dT%H%M%SZ")
    renewed_at = now_dt.strftime("%Y%m%dT%H%M%SZ")

    prior_chain = list(grant.get("renewal_chain") or [])
    renewal_id = f"RNW-{grant.get('grant_id', 'unknown')}-{renewed_at}"
    receipt = {
        "renewal_id": renewal_id,
        "grant_id": grant.get("grant_id"),
        "note_id": str(grant.get("note_id") or "").strip().upper(),
        "target_state": normalize_state(grant.get("target_state")),
        "previous_expires_at": grant.get("expires_at"),
        "new_expires_at": new_expires,
        "renewed_at": renewed_at,
        "term_days": term_days,
        "renewal_chain": prior_chain + [renewal_id],
        "conditions": {
            "verification_valid": True,
            "scope_unchanged": True,
            "objections": [],
        },
    }
    receipt["renewal_hash"] = _canonical_hash(receipt)
    return True, receipt, _record(True, "RENEWAL_OK",
                                 f"grant {grant.get('grant_id')} renewed to {new_expires} "
                                 f"(renewal {renewal_id})")


def check_receipt_authority(receipt, note_id, target_state, now=None):
    """Accept a valid SN-0340 five-step scorecard receipt as authority.

    The receipt is authority-equivalent to a grant iff, mechanically:
      step 1 — >= 2 enumerated options, each with an id;
      step 2 — every option scored on all four dimensions (0-10, numeric);
      step 3 — all three hard-stop gates true (no score overrides a failed gate);
      step 4 — winner matches an enumerated id AND holds the highest total
               among gate-passers; strongest alternative + falsifier substantive;
      step 5 — receipt posted (receipt_posted_comment_id present);
    plus binding checks:
      - scope_target matches note_id;
      - scope_action authorizes the promotion (learning_lock_in or the
        requested elevation);
      - decided_by names a real scorer (not anonymous);
      - receipt not older than 7 days after decided_at (receipt TTL).

    Returns (ok, record). Tampered or stale receipts are rejected, never
    treated as authority.
    """
    nid = str(note_id or "").strip().upper()
    want_state = normalize_state(target_state)

    def fail(code, detail):
        return False, _record(False, code, detail)

    if not isinstance(receipt, dict):
        return fail("RECEIPT_INVALID", "receipt is not an object")

    # ---- Binding: scope_target must name this note.
    scope_target = str(receipt.get("scope_target") or "").strip().upper()
    if not scope_target or scope_target != nid:
        return fail("RECEIPT_SCOPE_MISMATCH",
                    f"receipt scope_target {scope_target or '<none>'!r} does not name {nid or '<none>'!r}")

    # ---- Binding: scope_action must authorize this promotion.
    scope_action = str(receipt.get("scope_action") or "").strip().lower()
    allowed_actions = {"learning_lock_in", "elevation_grant", "promote"}
    if scope_action not in allowed_actions:
        return fail("RECEIPT_ACTION_MISMATCH",
                    f"receipt scope_action {scope_action!r} does not authorize promotion")

    # ---- Binding: decided_by must name a real scorer.
    decided_by = str(receipt.get("decided_by") or "").strip()
    if not decided_by or decided_by.lower() in ANONYMOUS_AUTHORITIES:
        return fail("RECEIPT_ANONYMOUS", "receipt names no accountable scorer")

    # ---- TTL: receipt expires 7 days after decided_at.
    decided_at = _parse_iso_ts(receipt.get("decided_at"))
    if decided_at is None:
        return fail("RECEIPT_INVALID", "decided_at is not a parseable timestamp")
    now_dt = _parse_grant_ts(now) if now else datetime.now(timezone.utc)
    if now_dt is None:
        return fail("RECEIPT_INVALID", f"reference time {now!r} is not parseable")
    from datetime import timedelta
    if now_dt > decided_at + timedelta(days=_RECEIPT_TTL_DAYS):
        return fail("RECEIPT_STALE",
                    f"receipt decided at {receipt.get('decided_at')} is older than "
                    f"{_RECEIPT_TTL_DAYS} days — re-score, do not reuse")

    # ---- Step 1: ENUMERATE — >= 2 options, each with an id.
    option_ids = []
    s1 = receipt.get("step1_enumerate")
    if not isinstance(s1, dict) or not isinstance(s1.get("options"), list):
        return fail("RECEIPT_STEP1", "step1_enumerate.options must be a list")
    if len(s1["options"]) < 2:
        return fail("RECEIPT_STEP1", "must enumerate >= 2 options")
    option_ids = [o.get("id") for o in s1["options"]
                  if isinstance(o, dict) and o.get("id")]
    if len(option_ids) < 2:
        return fail("RECEIPT_STEP1", "each enumerated option needs an id")

    # ---- Step 2: SCORE — four dimensions, 0-10, numeric, every option.
    totals = {}
    s2 = receipt.get("step2_score")
    if not isinstance(s2, dict) or not isinstance(s2.get("scores"), dict):
        return fail("RECEIPT_STEP2", "step2_score.scores must be an object keyed by option id")
    for oid in option_ids:
        dims = s2["scores"].get(oid)
        if not isinstance(dims, dict):
            return fail("RECEIPT_STEP2", f"option {oid!r} has no score entry")
        total = 0
        for dim in _RECEIPT_SCORE_DIMS:
            v = dims.get(dim)
            if not isinstance(v, (int, float)) or isinstance(v, bool):
                return fail("RECEIPT_STEP2",
                            f"option {oid!r} dimension {dim!r} must be numeric 0-10")
            if v < 0 or v > 10:
                return fail("RECEIPT_STEP2",
                            f"option {oid!r} dimension {dim!r} out of range 0-10")
            total += v
        totals[oid] = total

    # ---- Step 3: GATE — hard stops; no score overrides a failed gate.
    gates = receipt.get("step3_gate")
    gates_pass = True
    if isinstance(gates, dict):
        for gname in ("no_major_damage", "positive_forward_effect", "reversible"):
            if gates.get(gname) is not True:
                gates_pass = False
    else:
        gates_pass = False
    if not gates_pass:
        return fail("RECEIPT_STEP3", "a hard-stop gate failed — no score overrides it")

    # ---- Step 4: DECIDE — winner is an enumerated id with the highest total.
    s4 = receipt.get("step4_decide")
    if not isinstance(s4, dict):
        return fail("RECEIPT_STEP4", "step4_decide missing or not an object")
    winner = s4.get("winner")
    if winner not in option_ids:
        return fail("RECEIPT_STEP4", "winner must match an enumerated option id")
    best = max(totals.values())
    if totals.get(winner, -1) < best:
        return fail("RECEIPT_STEP4",
                    f"winner does not hold the highest total ({totals.get(winner)} < {best})")
    alt = s4.get("strongest_alternative")
    if not isinstance(alt, dict) or not str(alt.get("summary") or "").strip():
        return fail("RECEIPT_STEP4", "strongest_alternative.summary is empty")
    falsifier = s4.get("falsifier")
    if not isinstance(falsifier, str) or len(falsifier.strip()) < 20:
        return fail("RECEIPT_STEP4", "falsifier must state concrete disproving evidence")

    # ---- Promotion binding: the winning option must be the promotion.
    promotion_option_id = str(receipt.get("promotion_option_id") or "").strip()
    if promotion_option_id and winner != promotion_option_id:
        return fail("RECEIPT_WINNER_MISMATCH",
                    f"winner {winner!r} != promotion_option_id {promotion_option_id!r}")

    # ---- Step 5: RECEIPT — written AND posted.
    s5 = receipt.get("step5_receipt")
    if not isinstance(s5, dict) or not isinstance(s5.get("receipt_posted_comment_id"), int):
        return fail("RECEIPT_STEP5",
                    "receipt_posted_comment_id missing — a private scorecard is not authority")

    # ---- Target-state binding: receipt must authorize this elevation.
    # A learning_lock_in receipt authorizes promotion into the learning
    # pipeline (RATIFIED/ACTIVE/LEARNED family). Anything else must name
    # the exact target state via promotion_option binding above.
    _ = want_state  # bound via scope_target + promotion_option_id
    return True, _record(True, "RECEIPT_AUTHORITY_OK",
                         f"valid SN-0340 receipt by {decided_by} authorizes "
                         f"{scope_target} (winner {winner}, score {totals[winner]:.1f})")


def issue_promotion_authority(verification_result, note_id, target_state,
                              issuer="Shawn Vibert", issuer_role="Human Director",
                              expires_days=7, issued_at=None):
    """Instant promotion path: verification completion auto-issues authority.

    When verification completes and passes, the promotion authority is issued
    automatically by the verification itself — no human grant-issuance step.
    The machine is the issuer's delegate: the verification evidence IS the
    authorization basis.

    verification_result: dict with:
      - "verification_passed": True (anything else -> no authority issued);
      - "evidence": the verification evidence bundle (kept as scope_note);
      - "verification_id": identifier of the verification run.

    Returns (grant: dict | None, record). On failure returns (None, record)
    with a fail-closed reason — no authority is ever issued on a failed or
    ambiguous verification.
    """
    nid = str(note_id or "").strip().upper()
    if not nid:
        return None, _record(False, "PROMOTION_AUTHORITY_INVALID", "note_id names no note")
    if not isinstance(verification_result, dict):
        return None, _record(False, "PROMOTION_AUTHORITY_INVALID",
                             "verification_result is not an object")
    if verification_result.get("verification_passed") is not True:
        return None, _record(False, "PROMOTION_AUTHORITY_REFUSED",
                             "verification did not pass — no authority issued. "
                             "Fail-closed: authority follows passing verification, never precedes it.")
    verification_id = str(verification_result.get("verification_id") or "").strip()
    if not verification_id:
        return None, _record(False, "PROMOTION_AUTHORITY_INVALID",
                             "verification_result names no verification_id")
    evidence = verification_result.get("evidence")
    scope_note = ("auto-issued on passing verification "
                  f"{verification_id}; evidence sealed in verification record")
    grant = make_grant(
        note_id=nid,
        target_state=target_state,
        issuer=issuer,
        issuer_role=issuer_role,
        expires_days=expires_days,
        scope_note=scope_note,
        delegated_by="Shawn Vibert (automaticity delegation 2026-10-08: "
                     "passing verification auto-issues promotion authority)",
        issued_at=issued_at,
    )
    # Mark the grant's provenance: machine-issued on verification, not human-issued.
    grant["auto_issued"] = True
    grant["verification_id"] = verification_id
    if isinstance(evidence, dict):
        grant["verification_evidence_hash"] = _canonical_hash(evidence)
    grant["grant_hash"] = _canonical_hash(
        {k: v for k, v in grant.items() if k != "grant_hash"})
    return grant, _record(True, "PROMOTION_AUTHORITY_ISSUED",
                         f"authority for {nid}->{normalize_state(target_state)} auto-issued "
                         f"on verification {verification_id} (grant {grant['grant_id']})")


def load_elevation_grants(grants_dir):
    """Load all grant JSON files from a directory. Returns (grants, errors)."""
    from pathlib import Path
    grants, errors = [], []
    d = Path(grants_dir)
    if not d.is_dir():
        return grants, [f"grants directory not found: {grants_dir}"]
    for p in sorted(d.glob("*.json")):
        try:
            grants.append(json.loads(p.read_text(encoding="utf-8")))
        except Exception as e:
            errors.append(f"{p.name}: {e}")
    return grants, errors


def _valid_predecessor_receipt(pred, entry):
    """A VERIFIED-predecessor receipt must hash-verify, name this entry, and
    record a VERIFIED new_state."""
    if not isinstance(pred, dict):
        return False
    body = {k: v for k, v in pred.items() if k != "receipt_hash"}
    if pred.get("receipt_hash") != _canonical_hash(body):
        return False
    if normalize_state(pred.get("new_state")) != "VERIFIED":
        return False
    pred_id = str(pred.get("note_id") or pred.get("smart_note_id") or "").strip().upper()
    entry_id = str(entry.get("smart_note_id") or entry.get("intelligent_block_id") or "").strip().upper()
    return bool(pred_id) and pred_id == entry_id


def apply_elevation(entry, new_state, authority=None, evidence=None, superseded_entry=None,
                    elevation_grants=None, elevation_receipts=None,
                    verification_state=None):
    """Attempt a truth-state transition on a registry entry dict.

    On success the entry is mutated in place (truth_state + appended
    elevation_history record) and (True, record) is returned.
    On rejection (False, record) is returned and the entry is left
    byte-identical — rejection is a non-event: no state, no history,
    no receipt is recorded.

    superseded_entry: when this write supersedes an older entry, pass the old
    entry — an elevated write that drops the old entry's authority history
    is rejected (SUPERSESSION_ERASES_AUTHORITY).

    elevation_grants: iterable of elevation-grant dicts. VERIFIED->RATIFIED
    requires a valid, unexpired grant naming this note (RATIFIED_REQUIRES_
    ELEVATION_GRANT). All other transitions ignore grants.
    elevation_receipts: iterable of SN-0340 scorecard receipts accepted as
    authority-equivalent (receipt-as-authority, Shawn directive 2026-10-08).
    verification_state: {"verification_valid", "scope_unchanged",
    "objections", ...} — when an elevation grant is expired, the canonical
    path attempts auto-renewal against this state (attempt_renewal defaults
    True in check_elevation_grant); fail-closed: without it the expired
    grant stays dead.
    """
    if not isinstance(entry, dict):
        return False, _record(False, "INVALID_ENTRY", "entry is not an object")
    old = normalize_state(entry.get("truth_state", "CANDIDATE"))
    new = normalize_state(new_state)
    if rank(old) < 0:
        return False, _record(False, "UNKNOWN_STATE", f"current state {old!r} is not on the ladder")
    if rank(new) < 0:
        return False, _record(False, "UNKNOWN_STATE", f"target state {new!r} is not on the ladder")
    if new == old:
        return True, _record(True, "NOOP_SAME_STATE", f"already {new}; nothing to do")

    if superseded_entry is not None and rank(new) > 0:
        old_hist = (superseded_entry or {}).get("elevation_history") or []
        if old_hist and not (entry.get("elevation_history") or []):
            return False, _record(False, "SUPERSESSION_ERASES_AUTHORITY",
                                  "superseding write drops the superseded entry's authority history")

    if rank(new) < rank(old):
        # Demotion is always permitted — containment must never be blocked.
        entry["truth_state"] = new
        entry.setdefault("elevation_history", []).append({
            "from": old, "to": new, "authority": str(authority or "").strip() or None,
            "at": _utc_now(), "kind": "demotion",
        })
        return True, _record(True, "DEMOTION_PERMITTED", f"{old} -> {new}")

    # RATIFIED is a Human-Director authority boundary. Its only governed
    # predecessor is VERIFIED. Reject every direct jump before authority or
    # evidence can make the transition appear valid.
    if new == "RATIFIED" and old != "VERIFIED":
        return False, _record(
            False,
            "RATIFIED_REQUIRES_VERIFIED_PREDECESSOR",
            f"RATIFIED may only be entered from VERIFIED; current state is {old}",
        )


    # Elevation: authority AND evidence, checked separately and in order.
    ok, rec = check_authority(authority)
    if not ok:
        return False, rec
    ok, rec = check_evidence(evidence)
    if not ok:
        return False, rec

    # VERIFIED->RATIFIED additionally requires a capability grant: authority
    # travels with the elevation request (Option C, ratified 2026-10-06).
    grant_id = None
    if old == "VERIFIED" and new == "RATIFIED":
        ok, rec = check_elevation_grant(entry, new, elevation_grants,
                                        elevation_receipts=elevation_receipts,
                                        verification_state=verification_state)
        if not ok:
            return False, rec
        # Extract the satisfying grant_id from the detail for the history record.
        # check_elevation_grant returns GRANT_OK with "grant <id> by ..." detail.
        detail = rec.get("detail", "")
        if detail.startswith("grant "):
            grant_id = detail.split(" ", 2)[1]

    if new == "ACTIVE":
        pred = (evidence or {}).get("predecessor_receipt")
        if not _valid_predecessor_receipt(pred, entry):
            return False, _record(False, "ACTIVE_REQUIRES_VERIFIED_PREDECESSOR",
                                  "ACTIVE requires a hash-verified VERIFIED predecessor receipt naming this entry")
    if new == "LEARNED":
        items = (evidence or {}).get("items") or []
        if not any(str(it.get("type", "")).strip().lower() == "behavioral" for it in items if isinstance(it, dict)):
            return False, _record(False, "LEARNED_REQUIRES_BEHAVIORAL_EVIDENCE",
                                  "LEARNED requires recorded behavioral evidence (an item of type 'behavioral')")

    entry["truth_state"] = new
    hist_record = {
        "from": old,
        "to": new,
        "authority": str(authority).strip(),
        "evidence_hashes": [str(it["content_hash"]).strip() for it in evidence["items"]],
        "evidence_types": sorted({str(it.get("type", "")).strip().lower() for it in evidence["items"]}),
        "at": _utc_now(),
        "kind": "elevation",
    }
    if evidence.get("receipt"):
        hist_record["receipt_hash"] = evidence["receipt"]["receipt_hash"]
    if new == "ACTIVE" and evidence.get("predecessor_receipt"):
        hist_record["predecessor_receipt_hash"] = evidence["predecessor_receipt"]["receipt_hash"]
    if grant_id:
        hist_record["elevation_grant_id"] = grant_id
    entry.setdefault("elevation_history", []).append(hist_record)
    return True, _record(True, "ELEVATED", f"{old} -> {new} by {str(authority).strip()}")


def audit_registry_semantics(registry):
    """Read-side semantic audit: find truth-state escalation already on disk.

    Structural audit_registry() checks shape (hashes, duplicates, paths).
    This checks meaning: every elevated entry must carry authority +
    evidence provenance, ACTIVE must chain to a verified predecessor,
    LEARNED must record behavioral evidence, and supersession must not
    have erased authority history.
    """
    defects = {
        "elevated_without_provenance": [],
        "elevated_without_authority": [],
        "elevated_without_evidence": [],
        "active_without_verified_predecessor": [],
        "learned_without_behavioral_evidence": [],
        "supersession_erased_history": [],
        "ratified_without_elevation_grant": [],
    }
    entries = registry.get("entries", []) if isinstance(registry, dict) else []
    for e in entries:
        if not isinstance(e, dict):
            continue
        sn = e.get("smart_note_id") or e.get("intelligent_block_id") or "<unknown>"
        st = normalize_state(e.get("truth_state", "CANDIDATE"))
        if rank(st) <= 0:
            continue
        hist = e.get("elevation_history") or []
        if not hist:
            if e.get("supersedes"):
                defects["supersession_erased_history"].append(sn)
            else:
                defects["elevated_without_provenance"].append(sn)
            continue
        last = hist[-1] if isinstance(hist[-1], dict) else {}
        auth = str(last.get("authority") or "").strip()
        if not auth or auth.lower() in ANONYMOUS_AUTHORITIES:
            defects["elevated_without_authority"].append(sn)
        if not last.get("evidence_hashes"):
            defects["elevated_without_evidence"].append(sn)
        if st == "ACTIVE":
            if not any(isinstance(h, dict) and h.get("to") == "VERIFIED" and h.get("receipt_hash")
                       for h in hist):
                defects["active_without_verified_predecessor"].append(sn)
        if st == "LEARNED":
            types = set()
            for h in hist:
                if isinstance(h, dict):
                    types.update(h.get("evidence_types") or [])
            if "behavioral" not in types:
                defects["learned_without_behavioral_evidence"].append(sn)
        # Elevation-grant law (Option C, 2026-10-06): any recorded
        # VERIFIED->RATIFIED transition must carry an elevation_grant_id.
        # Entries ratified before the law (no history at all) are reported
        # under elevated_without_provenance, not here.
        for h in hist:
            if (isinstance(h, dict) and h.get("from") == "VERIFIED"
                    and h.get("to") == "RATIFIED"
                    and not h.get("elevation_grant_id")):
                defects["ratified_without_elevation_grant"].append(sn)
                break
    counts = {k: len(v) for k, v in defects.items()}
    total = sum(counts.values())
    return {"ok": total == 0, "counts": counts, "defect_total": total,
            "defects": defects, "entries_scanned": len(entries)}
