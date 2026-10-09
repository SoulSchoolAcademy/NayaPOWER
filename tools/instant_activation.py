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
        "directive_ref": "chat:session-abc123",      # REQUIRED, see trust model
        #   - "chat:<opaque-ref>": his words arrived in direct chat.
        #   - "feed:<issue>#issuecomment-<id>": his words arrived via a
        #     GitHub comment (e.g. "feed:1354#issuecomment-6085793228").
        "content_hash": "…"              # OPTIONAL: binds the marker to the
                                         # exact lesson bytes; mismatch refuses.
    }

Trust model -- EXACT claims, read before relying on this module:
- REFUSED (mechanistic): malformed markers -- missing/wrong source,
  wrong verifier, empty quote, unparseable or future timestamp,
  missing or malformed directive_ref. Malformed forgery never activates.
- CHECKABLE (mechanistic when a verifier runs): a feed-type
  directive_ref names a GitHub comment. With a verifier configured
  (activate(..., ref_verifier=...) or the CLI --verify-ref flag), the
  comment's author must be the repo owner account or the activation is
  refused (DIRECTIVE_REF_UNVERIFIED). Without a verifier the check is
  recorded in the receipt as deferred -- never as passed.
- HONESTY-PLUS-AUDIT (explicit, not mechanistic): a chat-type
  directive_ref cannot be independently verified from this seat -- no
  chat-truth source exists here. A well-formed chat-ref marker minted
  by a non-Shawn agent WILL activate. The forgery is fully auditable
  from the receipt (quote + timestamp + ref + content hash), and
  minting one is a standing law violation -- but this module does not
  refuse it. Closing that gap needs a chat-truth source (named below
  under "What remains").
- REPLAY-RESISTANT (mechanistic): a marker is single-use per content.
  directive_digest binds the marker instance (quote + timestamp + ref);
  reusing the same marker for DIFFERENT content is refused
  (MARKER_REPLAYED). Re-activating identical content is idempotent.

What remains (named, not hidden):
- A chat-truth source: something this module can call to confirm
  "Shawn said these words in this chat." Until that exists, chat-ref
  identity rests on honesty-plus-audit.
- The deployed Receiver (supabase/functions/v7-smart-note-canonical)
  hardcodes learning_evidence rows to CANDIDATE; the shawn_direct
  branch on that insert needs Shawn's per-change authorization
  (protected gate) before the instant path is live in production.
- Operating contract section 3's blanket CANDIDATE ceiling needs the
  ratified Shawn-exception written in (flag for Naya 1, citing the
  Verification Law).

How it is invoked (A6 wiring): the canonical entry point is
    python3 tools/smart_note_v2.py capture --capture <capture.json>
which routes shawn_direct-marked captures here and everything else to
the standard project path or a fail-closed refusal. This module's own
CLI (python3 tools/instant_activation.py activate --capture ...) is the
direct tool for the instant path.
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


# directive_ref contract: "chat:<opaque-ref>" or "feed:<issue>#issuecomment-<id>".
_REF_RE = re.compile(r"^(chat|feed):(.+)$")
_FEED_REF_RE = re.compile(r"^(\d+)#issuecomment-(\d+)$")

# GitHub account expected to author Shawn-relayed directives on the feed.
# Parameterizable (expected_author) -- the default is the repo owner account.
_DEFAULT_EXPECTED_AUTHOR = "SoulSchoolAcademy"
_DEFAULT_REPO = "SoulSchoolAcademy/NayaPOWER"


def parse_directive_ref(ref):
    """Parse and validate a directive_ref. Returns (ref_type, detail).

    ref_type is "chat" or "feed". Raises InstantActivationRefused
    (NOT_SHAWN_VERIFIED) when the ref is missing or malformed -- a
    marker without a checkable reference never takes the instant path.
    """
    m = _REF_RE.match(str(ref or "").strip())
    if not m:
        raise InstantActivationRefused(
            "NOT_SHAWN_VERIFIED",
            f"verification.directive_ref is missing or malformed: {ref!r}. "
            "It must be 'chat:<ref>' or 'feed:<issue>#issuecomment-<id>' so "
            "the directive is attributable.",
        )
    ref_type, rest = m.group(1), m.group(2).strip()
    if not rest:
        raise InstantActivationRefused(
            "NOT_SHAWN_VERIFIED",
            f"verification.directive_ref has an empty {ref_type} reference.",
        )
    if ref_type == "feed":
        fm = _FEED_REF_RE.match(rest)
        if not fm:
            raise InstantActivationRefused(
                "NOT_SHAWN_VERIFIED",
                f"feed directive_ref malformed: {ref!r}. Expected "
                "'feed:<issue>#issuecomment-<comment-id>'.",
            )
        return "feed", {"issue": fm.group(1), "comment_id": fm.group(2)}
    return "chat", {"opaque_ref": rest}


def verify_feed_ref(ref, *, transport=None,
                    expected_author=_DEFAULT_EXPECTED_AUTHOR,
                    repo=_DEFAULT_REPO):
    """Mechanically verify a feed-type directive_ref.

    transport(issue, comment_id) -> dict (the GitHub comment payload) is
    injectable so this is testable without network. With transport=None
    the check is NOT performed -- returns {"checkable": True,
    "checked": False, "reason": "no verifier configured"} (deferred,
    never passed).

    With a transport: the comment must exist and its author login must
    equal expected_author. Raises InstantActivationRefused
    (DIRECTIVE_REF_UNVERIFIED) otherwise.
    """
    ref_type, detail = parse_directive_ref(ref)
    if ref_type != "feed":
        return {"checkable": False, "checked": False,
                "reason": "chat refs are honesty-plus-audit, not verifiable"}
    if transport is None:
        return {"checkable": True, "checked": False,
                "reason": "no verifier configured; check deferred"}
    try:
        payload = transport(detail["issue"], detail["comment_id"])
    except Exception as e:
        raise InstantActivationRefused(
            "DIRECTIVE_REF_UNVERIFIED",
            f"could not fetch referenced comment {ref}: {e}. "
            "Fail-closed: an unverifiable feed reference does not activate.")
    author = ((payload or {}).get("user") or {}).get("login")
    if author != expected_author:
        raise InstantActivationRefused(
            "DIRECTIVE_REF_UNVERIFIED",
            f"referenced comment {ref} was authored by {author!r}, not the "
            f"expected {expected_author!r}. A feed reference must name "
            "Shawn's own words.")
    return {"checkable": True, "checked": True, "author": author,
            "comment_id": detail["comment_id"], "issue": detail["issue"]}


def _gh_api_transport(issue, comment_id, *, repo=_DEFAULT_REPO, gh_api=None,
                      timeout=30):
    """Feed-ref transport over the repo's quiet gh-api path (subprocess)."""
    import subprocess
    gh = gh_api or str(Path.home() / "workspace" / "naya" / "bin" / "gh-api")
    r = subprocess.run(
        [gh, "GET", f"/repos/{repo}/issues/comments/{comment_id}"],
        capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(f"gh-api GET comment {comment_id} failed: "
                           f"{r.stderr[:200]}")
    try:
        payload = json.loads(r.stdout)
    except Exception as e:
        raise RuntimeError(f"gh-api returned non-JSON for comment "
                           f"{comment_id}: {e}")
    if isinstance(payload, dict) and payload.get("message"):
        raise RuntimeError(f"gh-api error for comment {comment_id}: "
                           f"{str(payload.get('message'))[:200]}")
    return payload


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
    # directive_ref is REQUIRED and format-validated: the marker must name
    # an attributable directive (chat ref or feed comment ref). A marker
    # without a checkable reference never takes the instant path.
    ref_type, _ref_detail = parse_directive_ref(v.get("directive_ref"))
    quote_clean = quote.strip()
    directed_iso = directed_at.isoformat()
    ref_clean = str(v.get("directive_ref")).strip()
    directive_digest = hashlib.sha256(
        "|".join([quote_clean, directed_iso, ref_clean]).encode("utf-8")
    ).hexdigest()
    trust_basis = ("mechanistic-checkable" if ref_type == "feed"
                   else "honesty-plus-audit")
    return {
        "source": SHAWN_DIRECT,
        "verifier": SHAWN_VERIFIER,
        "verifier_role": v.get("verifier_role") or SHAWN_VERIFIER_ROLE,
        "directive_quote": quote_clean,
        "directed_at": directed_iso,
        "directive_ref": ref_clean,
        "ref_type": ref_type,
        "trust_basis": trust_basis,
        "directive_digest": directive_digest,
        # Optional marker-declared content binding (A3): when present it
        # must equal the recomputed lesson hash or the input is tampered.
        "declared_content_hash": v.get("content_hash"),
    }


def _canonical_lesson_bytes(capture) -> bytes:
    """Canonical bytes of the capture's lesson content (integrity binding)."""
    intel = capture.get("intelligence")
    lesson = intel if isinstance(intel, dict) else {"lesson": capture.get("lesson")}
    canonical = json.dumps(lesson, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=False)
    return canonical.encode("utf-8")


def check_capture_integrity(capture) -> dict:
    """Run the automatic machine integrity guards on the instant path.

    Naya 1's acceptance (2026-10-09): instant authorization skips the
    human value-review queue, NOT machine integrity checks. These run on
    every instant activation, authorized or not:
      - schema: required fields present and well-formed
      - provenance: captured_at parseable
      - privacy: scope, when declared, is a known value
      - integrity: a declared content_hash must match recomputed bytes

    Returns the list of passed checks. Raises InstantActivationRefused
    with MALFORMED_INPUT or TAMPERED_INPUT on any failure.
    """
    checks = []
    title = (capture or {}).get("title")
    if not isinstance(title, str) or not title.strip():
        raise InstantActivationRefused("MALFORMED_INPUT",
                                       "capture.title is missing or empty.")
    checks.append("schema:title_present")

    intel = (capture or {}).get("intelligence")
    lesson = capture.get("lesson")
    if not isinstance(intel, dict) and not (isinstance(lesson, str) and lesson.strip()):
        raise InstantActivationRefused("MALFORMED_INPUT",
                                       "capture has no lesson content "
                                       "(intelligence dict or lesson string).")
    checks.append("schema:lesson_present")

    captured_at = str(((capture or {}).get("source") or {}).get("captured_at") or "")
    if _parse_ts(captured_at) is None:
        raise InstantActivationRefused("MALFORMED_INPUT",
                                       f"source.captured_at unparseable: {captured_at!r}.")
    checks.append("provenance:captured_at_parseable")

    scope = str(capture.get("scope") or capture.get("owner_scope") or "PRIVATE").upper()
    if scope not in {"PRIVATE", "PUBLIC", "COLLECTIVE"}:
        raise InstantActivationRefused("MALFORMED_INPUT",
                                       f"unknown scope {scope!r}; expected "
                                       "PRIVATE, PUBLIC, or COLLECTIVE.")
    checks.append("privacy:scope_known")

    declared = (capture or {}).get("content_hash")
    if declared:
        recomputed = hashlib.sha256(_canonical_lesson_bytes(capture)).hexdigest()
        if str(declared).lower() != recomputed:
            raise InstantActivationRefused(
                "TAMPERED_INPUT",
                "capture.content_hash does not match the recomputed lesson "
                "bytes; the input was tampered with after hashing.")
        checks.append("integrity:content_hash_bound")
    else:
        checks.append("integrity:content_hash_computed")
    return {"checks": checks,
            "content_hash": hashlib.sha256(_canonical_lesson_bytes(capture)).hexdigest()}


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


def _check_no_marker_replay(receipt_dir, directive_digest, content_hash,
                           directive_ref):
    """Refuse a marker reused for different content (A3).

    A marker is single-use per content: directive_digest binds the marker
    instance (quote + timestamp + ref). If the receipt dir already holds a
    receipt with the same directive_digest but a DIFFERENT content_hash,
    the marker is being replayed onto new content -> MARKER_REPLAYED.
    Same digest + same hash is idempotent re-activation (allowed).
    Receipts predating directive_digest (v1) are skipped.
    """
    rdir = Path(receipt_dir)
    if not rdir.is_dir():
        return
    for p in sorted(rdir.glob("*.json")):
        try:
            r = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue  # not ours / corrupt: never blocks activation
        v = (r or {}).get("verification") or {}
        if v.get("directive_digest") != directive_digest:
            continue
        if v.get("content_hash") != content_hash:
            raise InstantActivationRefused(
                "MARKER_REPLAYED",
                f"directive {directive_ref!r} already activated different "
                f"content (receipt {p.name}). A marker is single-use per "
                "content; mint a new directive for new content.")


def activate(capture: dict, *, registry_path=None, receipt_dir=None,
             private_root=None, brain_root=None, ref_verifier=None) -> dict:
    """Activate a Shawn-verified capture in one motion.

    Steps (all inside this call, no queue, no second human value-review):
      1. validate the shawn_direct marker, incl. required directive_ref
         (fail-closed),
      2. run the automatic machine integrity guards (fail-closed),
      3. bind the marker to the content: a declared content_hash must
         match; a marker already used for different content is refused
         (MARKER_REPLAYED),
      4. verify a feed-type directive_ref when a verifier is configured
         (fail-closed on failure; deferred and recorded otherwise),
      5. reserve the SN id,
      6. render the projection,
      7. write the registry entry with truth_state=VERIFIED,
      8. mint the activation receipt (with the full trust record),
      9. verify the persisted bytes by read-back (fail-closed),
      10. produce the smart link.

    Naya 1's acceptance (2026-10-09): instant authorization skips the
    value-review queue, NOT machine integrity checks. This function is
    capture activation, not learning proof -- it must never be reported
    as causal behavioral learning or successor reuse.
    """
    verification = validate_shawn_direct(capture)
    integrity = check_capture_integrity(capture)
    content_hash = integrity["content_hash"]

    # A3: marker-declared content binding. When the marker names the exact
    # lesson bytes, they must match what is being activated.
    declared = verification.get("declared_content_hash")
    if declared is not None and str(declared).lower() != content_hash:
        raise InstantActivationRefused(
            "TAMPERED_INPUT",
            "verification.content_hash does not match the recomputed lesson "
            "bytes; the marker was bound to different content.")

    rdir = Path(receipt_dir) if receipt_dir else sn2.ROOT / RECEIPT_DIR

    # A3: replay guard -- before anything is written.
    _check_no_marker_replay(rdir, verification["directive_digest"],
                            content_hash, verification["directive_ref"])

    # A1: feed-type refs are mechanically checkable. With a verifier,
    # a wrong-author reference refuses; without one the check is
    # recorded as deferred (never as passed).
    ref_check = {"checkable": verification["ref_type"] == "feed",
                 "checked": False}
    if verification["ref_type"] == "feed" and ref_verifier is not None:
        ref_check = verify_feed_ref(verification["directive_ref"],
                                    transport=ref_verifier)
    elif verification["ref_type"] == "feed":
        ref_check = {"checkable": True, "checked": False,
                     "reason": "no verifier configured; check deferred"}
    verification["ref_check"] = ref_check
    verification["content_hash"] = content_hash

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
        "integrity_checks": integrity["checks"],
        "law": "Shawn's Verification Law (2026-10-09): his word IS the verification.",
    }
    receipt["receipt_hash"] = _hash_receipt(receipt)

    rdir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_sn = re.sub(r"[^A-Za-z0-9-]", "_", sn_id)
    receipt_path = rdir / f"{ts}-{safe_sn}-instant-activation.json"
    receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n",
                            encoding="utf-8")

    # Genuine persistence receipt: read the stored bytes back and verify.
    # A receipt for bytes that were never durably written is a lie with
    # formatting (Usefulness Gate). Any mismatch fails closed.
    stored = json.loads(receipt_path.read_text(encoding="utf-8"))
    if stored.get("receipt_hash") != receipt["receipt_hash"]:
        raise InstantActivationRefused(
            "PERSISTENCE_NOT_VERIFIED",
            "receipt bytes read back do not match the minted receipt.")
    stored_reg = json.loads(reg_path.read_text(encoding="utf-8"))
    stored_entry = next(
        (e for e in stored_reg.get("entries", [])
         if e.get("intelligent_block_id") == ib), None)
    if stored_entry is None or stored_entry.get("truth_state") != "VERIFIED":
        raise InstantActivationRefused(
            "PERSISTENCE_NOT_VERIFIED",
            "registry entry read back is missing or not VERIFIED.")
    if not projection.exists():
        raise InstantActivationRefused(
            "PERSISTENCE_NOT_VERIFIED",
            f"projection file missing at {projection}.")

    return {
        "activated": True,
        "sn_id": sn_id,
        "intelligent_block_id": ib,
        "projection_path": str(projection),
        "smart_link": smart_link,
        "truth_state": "VERIFIED",
        "verification_method": "shawn_direct_verification",
        "integrity_checks": integrity["checks"],
        "persistence_verified": True,
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
    a.add_argument("--verify-ref", action="store_true",
                   help="Mechanically verify a feed-type directive_ref via the "
                        "repo's gh-api path (fail-closed on mismatch). Without "
                        "this flag the feed check is recorded as deferred.")
    v = sub.add_parser("verify-ref",
                       help="Audit a directive_ref after the fact: parse it and, "
                            "for feed refs, verify the comment author via gh-api.")
    v.add_argument("--ref", required=True, help="The directive_ref to check.")
    v.add_argument("--expected-author", default=_DEFAULT_EXPECTED_AUTHOR)
    args = ap.parse_args(argv)

    if args.cmd == "verify-ref":
        try:
            rec = verify_feed_ref(args.ref, transport=_gh_api_transport,
                                  expected_author=args.expected_author)
        except InstantActivationRefused as e:
            print(json.dumps({"verified": False, "code": e.code,
                              "detail": e.detail}, ensure_ascii=False))
            return 3
        print(json.dumps({"verified": True, **rec}, ensure_ascii=False))
        return 0

    capture = json.loads(Path(args.capture).read_text(encoding="utf-8"))
    verifier = _gh_api_transport if args.verify_ref else None
    try:
        result = activate(capture, registry_path=args.registry,
                          receipt_dir=args.receipt_dir,
                          private_root=args.private_root,
                          brain_root=args.brain_root,
                          ref_verifier=verifier)
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
