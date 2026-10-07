#!/usr/bin/env python3
"""Write-time truth-state elevation guard + read-side semantic audit.

Closes #1468: hand-editing a registry entry CANDIDATE->RATIFIED was invisible
to audit_registry, which checks 10 structural defect classes (hashes,
duplicates, projection paths) and zero truth_state transitions. The promotion
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

# Legacy elevations ratified by the Human Director's explicit word BEFORE the
# elevation machinery existed (2026-10-06 and earlier). Named, dated,
# attributed, reported-not-blocking per the Ratchet pattern (SN-0285):
# block NEW drift without reddening main on legacy truth. These eight notes
# carry RATIFIED without machine-readable elevation_history because the
# authority+evidence recording did not exist when Shawn ratified them —
# backfilling history now would itself be fabrication. This list is CLOSED:
# no entry may ever be added; every post-machinery elevation must carry its
# authority + evidence provenance or the semantic audit flags it.
LEGACY_GRANDFATHERED_ELEVATIONS = frozenset({
    "SN-016",               # Prime Judgment Rule (ratified 2026-09-30)
    "SN-0340",              # Scorecard Law (ratified 2026-10-05)
    "SN-0399",              # Self-directed intelligence under governance (ratified 2026-10-05)
    "SN-0400",              # Captain directive (ratified 2026-10-05)
    "SN-0408",              # Deletion discipline (ratified 2026-10-05)
    "SN-0459",              # (ratified pre-machinery)
    "SN-0522",              # Prime 3 — the math decides (ratified 2026-10-07)
    "SN-NET-POWER-MAGIC-001",
})


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


def validate_grant(grant, note_id, target_state, now=None):
    """Validate a single elevation grant. Returns (ok, record).

    A grant is valid iff: it is a dict; its grant_hash recomputes (not
    tampered); it names this note; it names this target state; it has not
    expired; issued_at <= expires_at; and the issuer is the Human Director
    or a delegate the Director named (via delegated_by).
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


def check_elevation_grant(entry, new_state, elevation_grants):
    """VERIFIED->RATIFIED requires a valid, unexpired grant naming this note.

    elevation_grants: iterable of grant dicts (or None). Returns (ok, record).
    On success the record's detail names the satisfying grant_id.
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
    if not grants:
        return False, _record(False, "RATIFIED_REQUIRES_ELEVATION_GRANT",
                              f"VERIFIED->RATIFIED for {note_id} requires an elevation grant; none provided")
    failures = []
    for grant in grants:
        ok, rec = validate_grant(grant, note_id, new)
        if ok:
            return True, _record(True, "GRANT_OK", rec["detail"])
        failures.append(f"{grant.get('grant_id', '<unknown>')}: {rec['reason_code']}")
    return False, _record(False, "RATIFIED_REQUIRES_ELEVATION_GRANT",
                          f"no valid grant for {note_id}->RATIFIED among {len(grants)}: " +
                          "; ".join(failures[:3]))


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
                    elevation_grants=None):
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
        ok, rec = check_elevation_grant(entry, new, elevation_grants)
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


def audit_registry_semantics(registry, grandfathered=LEGACY_GRANDFATHERED_ELEVATIONS):
    """Read-side semantic audit: find truth-state escalation already on disk.

    Structural audit_registry() checks shape (hashes, duplicates, paths).
    This checks meaning: every elevated entry must carry authority +
    evidence provenance, ACTIVE must chain to a verified predecessor,
    LEARNED must record behavioral evidence, and supersession must not
    have erased authority history.

    grandfathered: smart_note_ids ratified before the elevation machinery
    existed (LEGACY_GRANDFATHERED_ELEVATIONS). They are reported-not-blocking:
    named, dated, attributed, never extended.
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
            elif str(e.get("smart_note_id") or "").strip().upper() not in (grandfathered or ()):
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
