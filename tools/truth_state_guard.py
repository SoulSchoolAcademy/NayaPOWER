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

_HASH64 = re.compile(r"[0-9a-fA-F]{64}")


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


def apply_elevation(entry, new_state, authority=None, evidence=None, superseded_entry=None):
    """Attempt a truth-state transition on a registry entry dict.

    On success the entry is mutated in place (truth_state + appended
    elevation_history record) and (True, record) is returned.
    On rejection (False, record) is returned and the entry is left
    byte-identical — rejection is a non-event: no state, no history,
    no receipt is recorded.

    superseded_entry: when this write supersedes an older entry, pass the old
    entry — an elevated write that drops the old entry's authority history
    is rejected (SUPERSESSION_ERASES_AUTHORITY).
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

    # Elevation: authority AND evidence, checked separately and in order.
    ok, rec = check_authority(authority)
    if not ok:
        return False, rec
    ok, rec = check_evidence(evidence)
    if not ok:
        return False, rec

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
    counts = {k: len(v) for k, v in defects.items()}
    total = sum(counts.values())
    return {"ok": total == 0, "counts": counts, "defect_total": total,
            "defects": defects, "entries_scanned": len(entries)}
