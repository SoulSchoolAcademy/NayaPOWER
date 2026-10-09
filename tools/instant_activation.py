#!/usr/bin/env python3
"""Instant activation for Shawn-verified captures.

Shawn's Verification Law (2026-10-09, ratified standing law):
    When Shawn says "smart note this," THAT IS THE VERIFICATION.
    He verified it when he said it. It activates INSTANTLY --
    no queue, no second verification, no waiting.
    Same for any user's direct capture request: the ask is the verification.

This module is the governed repo-side writer for that transition. A
Shawn-verified capture flows:

    capture -> persist -> receipt -> smart link -> ACTIVATED

in ONE motion, with zero queue and zero second-guessing.

What this module is NOT:
- It does NOT duplicate the canonical Receiver
  (supabase/functions/v7-smart-note-canonical). IB identity allocation
  stays with the Receiver; this module governs the repo-side truth-state
  transition for captures carrying the shawn_direct marker.
- It does NOT weaken the CANDIDATE path. Captures WITHOUT a valid
  shawn_direct marker are refused here (fail-closed) and belong to the
  admission-contract lane (Learning Builder B). The promotion thresholds
  in smart_note_v2.promote_note are untouched.
- It does NOT mint IB identity. The repo-side IB slug follows the existing
  repo convention (IB-SMART-NOTE-<date>-<slug>); the canonical UUID event
  identity remains the Receiver's to allocate.

Marker contract (on the capture JSON):
    "verification": {
        "source": "shawn_direct",        # exact string, nothing else qualifies
        "verifier": "Shawn",             # the Human Director, exact string
        "verifier_role": "human_director",
        "directive_quote": "smart note this: ...",  # his actual words, non-empty
        "directed_at": "2026-10-09T17:30:00Z",       # ISO-8601, not in the future
        "directive_ref": "..."           # optional: chat/message reference
    }

Trust boundary (documented, not hidden): the marker is asserted by the
capturing agent at capture time. Forgery is a provenance lie, which is
itself a standing law violation -- and the receipt records the full
marker (quote + timestamp + reference) so any forgery is auditable from
the receipt alone. The module's job is to make the honest path instant
and the dishonest path loudly refused, not to solve agent identity.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import smart_note_v2 as sn2
from smart_link import smart_link_for

SHAWN_DIRECT = "shawn_direct"
SHAWN_VERIFIER = "Shawn"
SHAWN_VERIFIER_ROLE = "human_director"

RECEIPT_SCHEMA = "naya.instant-activation-receipt.v1"
RECEIPT_DIR = Path(".naya") / "memory" / "smart-notes" / "instant-activations"

# Small clock-skew allowance for directed_at timestamps, in seconds.
_FUTURE_SKEW_S = 600
_MIN_QUOTE_LEN = 8


class InstantActivationRefused(Exception):
    """Raised when a capture may not take the instant path. Fail-closed."""

    def __init__(self, code: str, detail: str):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def _parse_ts(ts):
    try:
        dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (ValueError, TypeError):
        return None


def validate_shawn_direct(capture) -> dict:
    """Strictly validate the shawn_direct verification marker.

    Returns the normalized verification record. Raises
    InstantActivationRefused(NOT_SHAWN_VERIFIED) on ANY defect --
    missing marker, wrong source, wrong verifier, empty quote,
    unparseable or future timestamp. There is no partial credit.
    """
    v = (capture or {}).get("verification")
    if not isinstance(v, dict):
        raise InstantActivationRefused(
            "NOT_SHAWN_VERIFIED",
            "capture has no verification marker; the instant path requires "
            "verification.source='shawn_direct'. Route through the admission "
            "contract instead.",
        )
    if v.get("source") != SHAWN_DIRECT:
        raise InstantActivationRefused(
            "NOT_SHAWN_VERIFIED",
            f"verification.source is {v.get('source')!r}, not 'shawn_direct'. "
            "Only Shawn's direct verification takes the instant path.",
        )
    if v.get("verifier") != SHAWN_VERIFIER:
        raise InstantActivationRefused(
            "NOT_SHAWN_VERIFIED",
            f"verification.verifier is {v.get('verifier')!r}, not 'Shawn'. "
            "The instant path is for the Human Director's verification only.",
        )
    quote = v.get("directive_quote")
    if not isinstance(quote, str) or len(quote.strip()) < _MIN_QUOTE_LEN:
        raise InstantActivationRefused(
            "NOT_SHAWN_VERIFIED",
            "verification.directive_quote is missing or empty. The marker must "
            "carry Shawn's actual words so the receipt is auditable.",
        )
    directed_at = _parse_ts(v.get("directed_at"))
    if directed_at is None:
        raise InstantActivationRefused(
            "NOT_SHAWN_VERIFIED",
            f"verification.directed_at is unparseable: {v.get('directed_at')!r}.",
        )
    now = datetime.now(timezone.utc)
    if (directed_at - now).total_seconds() > _FUTURE_SKEW_S:
        raise InstantActivationRefused(
            "NOT_SHAWN_VERIFIED",
            "verification.directed_at is in the future. A future-dated "
            "verification cannot authorize the instant path.",
        )
    return {
        "source": SHAWN_DIRECT,
        "verifier": SHAWN_VERIFIER,
        "verifier_role": v.get("verifier_role") or SHAWN_VERIFIER_ROLE,
        "directive_quote": quote.strip(),
        "directed_at": directed_at.isoformat(),
        "directive_ref": v.get("directive_ref"),
    }


def _ib_slug(title: str, captured_at: str) -> str:
    date = (captured_at or "")[:10].replace("-", "")
    return f"IB-SMART-NOTE-{date}-{sn2.slug(title or 'untitled')}"


def _hash_receipt(receipt: dict) -> str:
    clean = {k: v for k, v in receipt.items() if k != "receipt_hash"}
    canonical = json.dumps(clean, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _build_block(capture: dict, ib: str) -> dict:
    """Build the persisted-block representation for the repo-side flow.

    understanding_state is VERIFIED because the Human Director's direct
    verification -- the highest authority in the system -- is the evidence.
    This is the repo-side truth; the canonical Receiver remains the sole
    minter of UUID event identity for the database side.
    """
    intel = capture.get("intelligence") or {}
    if isinstance(intel, dict):
        lesson_obj = {
            "essence": str(intel.get("essence") or capture.get("lesson") or ""),
            "human_view": intel.get("human_view") or {},
            "simple_view": intel.get("simple_view") or {},
            "naya_view": intel.get("naya_view") or {},
            "machine_view": intel.get("machine_view") or {},
            "learning_lesson": str(intel.get("learning_lesson") or capture.get("lesson") or ""),
            "priority": str(intel.get("priority") or ""),
            "applicability": str(intel.get("applicability") or ""),
            "connections": intel.get("connections") or [],
            "decisions": intel.get("decisions") or [],
            "uncertainty": str(intel.get("uncertainty") or ""),
        }
    else:
        lesson_obj = {
            "essence": str(capture.get("lesson") or ""),
            "human_view": {}, "simple_view": {}, "naya_view": {},
            "machine_view": {}, "learning_lesson": str(capture.get("lesson") or ""),
            "priority": "", "applicability": "", "connections": [],
            "decisions": [], "uncertainty": "",
        }
    return {
        "intelligent_block_id": ib,
        "block_id": ib,
        "content": {"lesson": json.dumps(lesson_obj, ensure_ascii=False)},
        "understanding_state": "VERIFIED",
        "owner_scope": str(capture.get("scope") or capture.get("owner_scope") or "PRIVATE").upper(),
    }


def _build_verify_equiv(block: dict, receipt_id: str) -> dict:
    """Build the verify-equivalent structure render() and the registry need.

    Lineage ids are deterministic derivations of the activation receipt id,
    namespaced so they can never collide with Receiver-minted UUIDs.
    """
    def _lid(kind: str) -> str:
        return f"instant-{kind}:" + hashlib.sha256(
            f"{receipt_id}:{kind}".encode()).hexdigest()[:32]

    return {
        "persisted": {
            "block": block,
            "event": {"id": _lid("event")},
            "lineage": {"id": _lid("lineage")},
            "relationship": {"relationship_id": _lid("relationship")},
            "index": {"id": _lid("index")},
            "checkpoint": {"id": _lid("checkpoint")},
            "receipt": {"id": receipt_id},
        }
    }


def activate(capture: dict, *, registry_path=None, receipt_dir=None,
             private_root=None, brain_root=None) -> dict:
    """Activate a Shawn-verified capture in one motion.

    Steps (all inside this call, no queue, no second verification):
      1. validate the shawn_direct marker (fail-closed),
      2. reserve the SN id,
      3. render the projection,
      4. write the registry entry with truth_state=VERIFIED,
      5. mint the activation receipt,
      6. produce the smart link.

    brain_root overrides the projection root (tests). The smart link is
    always derived from the canonical BRAIN/05-MEMORY/SMART-NOTES/ suffix,
    so it names the location the file WILL have on main.

    Returns a dict with sn_id, intelligent_block_id, projection_path,
    smart_link, truth_state, receipt, and receipt_path.

    Raises InstantActivationRefused for anything without a valid marker.
    """
    verification = validate_shawn_direct(capture)

    title = str(capture.get("title") or "").strip()
    if not title:
        raise InstantActivationRefused("NOT_SHAWN_VERIFIED",
                                       "capture has no title; cannot activate.")
    source = capture.get("source") or {}
    captured_at = str(source.get("captured_at") or capture.get("captured_at_utc") or "")
    if not captured_at:
        captured_at = _utcnow()
        source = {**source, "captured_at": captured_at}
    capture = {**capture, "source": source}

    ib = _ib_slug(title, captured_at)

    # Reserve the SN id authoritatively (same seam the project flow uses).
    sn_id = sn2.reserve_smart_note_id(capture, ib, registry_path)

    # Activation receipt id first: lineage ids derive from it.
    receipt_id = "instant-activation:" + hashlib.sha256(
        f"{ib}:{sn_id}:{captured_at}".encode()).hexdigest()[:32]

    block = _build_block(capture, ib)
    verify = _build_verify_equiv(block, receipt_id)

    # Render the projection (reuses the canonical renderer).
    render_capture = {
        "title": title,
        "source": {"captured_at": captured_at},
        "canonical_intent": capture.get("canonical_intent", "CAPTURE_DURABLE_INTELLIGENCE"),
        "category": capture.get("category", "smart-note"),
        "topic": capture.get("topic", "general"),
        "subtopic": capture.get("subtopic", "general"),
        "projection": capture.get("projection", {}),
        "lifecycle_state": capture.get("lifecycle_state", "ACTIVE"),
    }
    _old_brain_root = sn2.BRAIN_SMART_NOTE_ROOT
    if brain_root is not None:
        sn2.BRAIN_SMART_NOTE_ROOT = Path(brain_root)
    try:
        projection = sn2.render(render_capture, verify, private_root, sn_id=sn_id)
    finally:
        sn2.BRAIN_SMART_NOTE_ROOT = _old_brain_root
    effective_brain_root = Path(brain_root) if brain_root is not None else _old_brain_root

    # Registry write: reuse the canonical locked writer, then stamp the
    # Shawn-verification provenance onto the entry inside the same
    # transaction (atomic with the entry itself).
    reg_path = Path(registry_path) if registry_path else sn2.REGISTRY
    with sn2.registry_transaction(str(reg_path)) as registry:
        entry = sn2._update_registry_locked(render_capture, verify, projection,
                                            registry, sn_id=sn_id)
        entry["truth_state"] = "VERIFIED"
        entry["verification_method"] = "shawn_direct_verification"
        entry["verified_by"] = "Shawn (Human Director)"
        entry["verification"] = verification
        entry["activation_receipt_id"] = receipt_id

    # Canonical smart link from the BRAIN/05-MEMORY/SMART-NOTES/ suffix.
    # PRIVATE-scope captures project to the private surface instead: the
    # activation still succeeds, but no canonical link is produced (a
    # 404-for-strangers link must never be presented as resolvable --
    # smart_link.py D2). The receipt records the honest link status.
    try:
        rel_brain = projection.relative_to(effective_brain_root)
        link_path = "BRAIN/05-MEMORY/SMART-NOTES/" + str(rel_brain).replace("\\", "/")
        smart_link = smart_link_for(link_path)
        smart_link_status = entry.get("smart_link_status") or "ACTIVE"
    except Exception:
        smart_link = None
        smart_link_status = "PENDING_PRIVATE_PROJECTION"

    receipt = {
        "schema": RECEIPT_SCHEMA,
        "receipt_id": receipt_id,
        "activated_at": _utcnow(),
        "smart_note_id": sn_id,
        "intelligent_block_id": ib,
        "title": title,
        "truth_state": "VERIFIED",
        "verification": verification,
        "content_hash": entry.get("content_hash"),
        "projection_path": entry.get("projection_path"),
        "smart_link": smart_link,
        "smart_link_status": smart_link_status,
        "law": "Shawn's Verification Law (2026-10-09): his word IS the verification.",
    }
    receipt["receipt_hash"] = _hash_receipt(receipt)

    rdir = Path(receipt_dir) if receipt_dir else sn2.ROOT / RECEIPT_DIR
    rdir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_sn = re.sub(r"[^A-Za-z0-9-]", "_", sn_id)
    receipt_path = rdir / f"{ts}-{safe_sn}-instant-activation.json"
    receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n",
                            encoding="utf-8")

    return {
        "activated": True,
        "sn_id": sn_id,
        "intelligent_block_id": ib,
        "projection_path": str(projection),
        "smart_link": smart_link,
        "truth_state": "VERIFIED",
        "verification_method": "shawn_direct_verification",
        "receipt": receipt,
        "receipt_path": str(receipt_path),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Instant activation for Shawn-verified captures.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("activate", help="Activate a Shawn-verified capture JSON in one motion.")
    a.add_argument("--capture", required=True, help="Path to the capture JSON.")
    a.add_argument("--registry", default=None, help="Registry path (default: canonical).")
    a.add_argument("--receipt-dir", default=None)
    a.add_argument("--private-root", default=None)
    a.add_argument("--brain-root", default=None, help="Projection root override (tests).")
    a.add_argument("--out", default=None, help="Write the activation result JSON here.")
    args = ap.parse_args(argv)

    capture = json.loads(Path(args.capture).read_text(encoding="utf-8"))
    try:
        result = activate(capture, registry_path=args.registry,
                          receipt_dir=args.receipt_dir,
                          private_root=args.private_root,
                          brain_root=args.brain_root)
    except InstantActivationRefused as e:
        print(json.dumps({"activated": False, "code": e.code, "detail": e.detail},
                         ensure_ascii=False))
        return 3
    if args.out:
        Path(args.out).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                                  encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "receipt"},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
