#!/usr/bin/env python3
"""Instant activation path for human-director-verified Smart Notes.

Shawn's Verification Law (standing law, 2026-10-09): when Shawn says
"smart note this," THAT IS THE VERIFICATION. He verified it when he said
it. It activates INSTANTLY -- no queue, no second verification, no waiting.
Same for any authorized human's direct capture request: the ask is the
verification. Treating his verified word as unverified input is a law
violation.

This module is an EXTENSION of the existing capture seam -- not a parallel
capture system. It reuses, in order:
  tools/smart_note_v2.py : reserve_smart_note_id, render, _update_registry_locked,
                           registry_transaction, retrieve, slug, _atomic_write_json
  tools/smart_link.py    : smart_link_for (shape validation; never fabricated)
  tools/sn002_conformance.py : check_capture (the capture must pass the gate)
  BRAIN/00-SPEC/NIA-LANGUAGE-INTENT-V1.json : the canonical capture vocabulary

Pipeline (mirrors the `project` CLI order in smart_note_v2):
  INTENT -> GUARDS -> DISTILL -> BUILD v2 CAPTURE -> WRITE -> RECEIPT
    -> RESERVE SN -> RENDER PROJECTION -> REGISTER INDEX -> SMART LINK PAYLOAD

The automatic truth ceiling (CANDIDATE) is NOT weakened: it stays recorded
in machine_view.automatic_truth_ceiling for the automatic path. The
human-director override is explicit, separate, and auditable:
  authority = "human-director-verified"
  machine_view.human_director_override = {verified, by, at_utc, basis, law}

FAIL-CLOSED: anything not human-verified must NOT take this path. A
system-captured item (source_kind != "human_direct") or an unknown human
raises SystemExit with a machine-readable INSTANT_ACTIVATION_REFUSED code.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

# Both import forms must work (same pattern as tools/smart_note_v2.py):
#   python -m tools.instant_activation   (repo root on sys.path)
#   python tools/instant_activation.py   (tools/ on sys.path)
try:
    from tools import smart_note_v2 as sn2
    from tools import smart_link as sl
    from tools import sn002_conformance as conf
except ImportError:  # running by path: sys.path[0] is tools/
    import smart_note_v2 as sn2
    import smart_link as sl
    import sn002_conformance as conf

ROOT = Path(__file__).resolve().parents[1]

CAPTURE_SCHEMA = "naya.smart-note-capture.v2"
RECEIPT_SCHEMA = "naya.instant-activation-receipt.v1"
PAYLOAD_SCHEMA = "naya.smart-link-payload.v1"
AUTHORITY = "human-director-verified"
TRUTH_STATE = "VERIFIED"
LIFECYCLE_STATE = "ACTIVE"

# The Human Director. Other authorized humans may be passed explicitly via
# authorized_humans; agent seats (naya-1..5, coda-*, codex) and "system" are
# NEVER authorized for this path.
DEFAULT_AUTHORIZED_HUMANS = frozenset({
    "shawn", "shawn vibert", "human-director", "human director",
})

NIA_SPEC_REL = Path("BRAIN") / "00-SPEC" / "NIA-LANGUAGE-INTENT-V1.json"
RECEIPT_DIR_REL = Path(".naya") / "memory" / "smart-notes" / "instant-activations"

# Task-mandated equivalents (Shawn's Verification Law brief): intent is
# semantic, not phrase-bound -- "smart note this", "lock this in", "bank
# this", "note this", "capture this" and equivalents all count. "bank this"
# is not in the NIA spec's strong list, so it is supplemented explicitly
# here (auditable, layered on top of the spec -- never a silent replacement).
TASK_EQUIVALENT_STRONG_ALIASES = ("bank this", "capture this")


# ============================================================================
# INTENT RECOGNITION
# ============================================================================
# Vocabulary is READ from the canonical NIA spec at call time (never a
# hardcoded copy) so the spec stays the single source of truth. Intent is
# semantic, not phrase-bound (contract section 6): the strong aliases below
# come from the spec; contextual aliases need substantive content.
#
# The recognizer is deliberately CONSERVATIVE: this path stamps
# human-director-verified, so a false positive is worse than a false
# negative. Interrogatives, retractions, and quoted third-party speech
# always fail closed to NO capture ("silence beats garbage").

_RETRACTION_RES = [
    r"\bnever mind\b",
    r"\bforget (it|that|this)\b",
    r"\bignore (this|that|it)\b",
    r"\bretract\b",
    r"\bcancel (that|this)\b",
    r"\bno need to (note|capture|save|store|bank)\b",
    r"\bdo not (note|capture|save|store|bank) (this|that|it)\b",
    r"\bdon'?t (note|capture|save|store|bank) (this|that|it)\b",
    r"\bactually,? no\b",
    r"\bon second thought\b",
    r"\bnot worth (noting|capturing|saving)\b",
]
_ATTRIBUTION_RES = [
    r"\b(he|she|they) (said|says|told me)\b",
    r"\btold me to\b",
]
_QUESTION_LEADS = (
    "should i", "can you", "could you", "would you", "do you",
    "what does", "what is", "what's", "how do", "how does",
    "is this worth", "do i need", "shall i",
)


def _normalize(text: str) -> str:
    t = str(text or "")
    t = t.replace("\u201c", '"').replace("\u201d", '"')
    t = t.replace("\u2018", "'").replace("\u2019", "'")
    t = t.replace("\u2014", "-").replace("\u2013", "-")
    return " ".join(t.lower().split())


def _load_nia_vocabulary(root=None):
    root = Path(root) if root else ROOT
    p = root / NIA_SPEC_REL
    if not p.is_file():
        raise SystemExit(
            "INSTANT_ACTIVATION_REFUSED:NIA_SPEC_MISSING:" + str(p)
        )
    spec = json.loads(p.read_text(encoding="utf-8"))
    strong = [str(a).lower() for a in spec.get("strong_capture_aliases", [])]
    contextual = [str(a).lower() for a in spec.get("contextual_capture_aliases", [])]
    if not strong:
        raise SystemExit("INSTANT_ACTIVATION_REFUSED:NIA_VOCABULARY_EMPTY")
    return strong, contextual


def _strip_alias(norm: str, alias: str) -> str:
    i = norm.find(alias)
    rest = norm[i + len(alias):] if i >= 0 else norm
    rest = re.sub(r"^[\s:;,\-\u2014\u2013\"'()\[\]]+", "", rest)
    rest = re.sub(r"[\s\"'()\[\]]+$", "", rest)
    return rest


def _substantive(text: str) -> bool:
    words = text.split()
    return len(words) >= 3 and len(text) >= 12


def detect_capture_intent(utterance: str, distilled: str | None = None,
                          root=None) -> dict:
    """Decide capture-intent yes/no for a human utterance.

    Returns {intent, alias, kind, refusal, distilled}. `distilled` may be
    supplied by the caller (the task's (human_id, utterance, distilled
    intelligence) triple); otherwise the recognizer attempts to distill
    the lesson from the utterance itself.
    """
    norm = _normalize(utterance)
    if not norm:
        return {"intent": False, "alias": None, "kind": None,
                "refusal": "EMPTY_UTTERANCE", "distilled": None}

    # 1. Retractions / explicit do-not-capture always win (fail closed).
    for rx in _RETRACTION_RES:
        if re.search(rx, norm):
            return {"intent": False, "alias": None, "kind": None,
                    "refusal": "RETRACTED:" + rx, "distilled": None}

    # 2. Interrogatives are not directives. A question never captures --
    #    ambiguity on a VERIFIED-stamping path fails closed to silence.
    if norm.rstrip().endswith("?"):
        return {"intent": False, "alias": None, "kind": None,
                "refusal": "INTERROGATIVE", "distilled": None}
    if norm.startswith(_QUESTION_LEADS):
        return {"intent": False, "alias": None, "kind": None,
                "refusal": "INTERROGATIVE_LEAD", "distilled": None}

    # 3. Quoted / attributed third-party speech is not the human's own ask.
    for rx in _ATTRIBUTION_RES:
        if re.search(rx, norm):
            return {"intent": False, "alias": None, "kind": None,
                    "refusal": "QUOTED_THIRD_PARTY", "distilled": None}

    # 4. Positive: strong aliases from the canonical NIA spec, plus the
    # task-mandated equivalents (auditable supplement, never a replacement).
    strong, contextual = _load_nia_vocabulary(root)
    strong = list(strong) + [a for a in TASK_EQUIVALENT_STRONG_ALIASES
                             if a not in strong]
    for alias in sorted(strong, key=len, reverse=True):
        if alias and alias in norm:
            lesson = (distilled or "").strip() or _strip_alias(norm, alias)
            if not _substantive(lesson):
                return {"intent": False, "alias": alias, "kind": "strong",
                        "refusal": "NO_DISTILLABLE_CONTENT", "distilled": None}
            return {"intent": True, "alias": alias, "kind": "strong",
                    "refusal": None, "distilled": lesson}

    # 5. Contextual aliases need the referent to be clear: substantive
    #    content must be present, otherwise the intent is ambiguous.
    for alias in sorted(contextual, key=len, reverse=True):
        if alias and alias in norm:
            lesson = (distilled or "").strip() or _strip_alias(norm, alias)
            if not _substantive(lesson):
                return {"intent": False, "alias": alias, "kind": "contextual",
                        "refusal": "AMBIGUOUS_REFERENT", "distilled": None}
            return {"intent": True, "alias": alias, "kind": "contextual",
                    "refusal": None, "distilled": lesson}

    return {"intent": False, "alias": None, "kind": None,
            "refusal": "NO_CAPTURE_INTENT", "distilled": None}


# ============================================================================
# INSTANT CAPTURE
# ============================================================================

@dataclass
class InstantActivationResult:
    intent: dict
    receipt: dict
    smart_link_payload: dict
    capture_path: str
    projection_path: str
    receipt_path: str
    smart_note_id: str
    intelligent_block_id: str
    conformant: bool = field(default=False)


def _utc_now():
    return datetime.now(timezone.utc)


def _build_intelligence(intel: dict, source_utterance: str) -> dict:
    """Build the full v2 intelligence structure from caller-supplied distillation.

    Required input: intel["lesson"] (the durable lesson). Views default to the
    lesson text itself -- never fabricated specifics.
    """
    lesson = str(intel.get("lesson") or intel.get("essence") or "").strip()
    if not lesson:
        raise SystemExit("INSTANT_ACTIVATION_REFUSED:EMPTY_DISTILLED_INTELLIGENCE")
    hv = intel.get("human_view") or {}
    sv = intel.get("simple_view") or {}
    nv = intel.get("naya_view") or {}
    av = intel.get("ai_view") or {}
    mv = intel.get("machine_view") or {}
    machine_view = dict(mv)
    # The automatic truth ceiling is NOT weakened: it governs the automatic
    # path. The human-director override is explicit and separate.
    machine_view["automatic_truth_ceiling"] = "CANDIDATE"
    machine_view["raw_source_separate_from_distillation"] = True
    return {
        "essence": str(intel.get("essence") or lesson),
        "human_view": {
            "meaning": str(hv.get("meaning") or lesson),
            "simple_rule": str(hv.get("simple_rule") or lesson),
            "why_it_matters": str(hv.get("why_it_matters") or lesson),
        },
        "simple_view": {
            "child": str(sv.get("child") or lesson),
            "grandma": str(sv.get("grandma") or lesson),
        },
        "naya_view": {
            "purpose": str(nv.get("purpose") or lesson),
            "architectural_rule": str(nv.get("architectural_rule") or lesson),
        },
        "ai_view": dict(av) or {"operator_guidance": lesson},
        "machine_view": machine_view,
        "decisions": list(intel.get("decisions") or []),
        "connections": list(intel.get("connections") or []),
        "uncertainty": str(intel.get("uncertainty") or
                           "Human-director-verified capture: the lesson is verified by the "
                           "director's explicit ask, not by independent evidence. "
                           "Applicability beyond the stated context is unproven."),
        "applicability": str(intel.get("applicability") or
                              "Applies whenever the stated situation recurs."),
        "learning_lesson": lesson,
        "successor_effect": str(intel.get("successor_effect") or
                                "A cold successor retrieving this note can apply the lesson "
                                "without re-deriving it."),
        "priority": str(intel.get("priority") or ""),
        "truth_state": TRUTH_STATE,
    }


def _human_director_override(now_iso: str) -> dict:
    return {
        "verified": True,
        "authority": AUTHORITY,
        "by": "Shawn Vibert, human director",
        "at_utc": now_iso,
        "basis": "human_director_capture_request",
        "law": ("Shawn's Verification Law: the ask is the verification -- "
                "activates instantly, no queue, no second verification."),
    }


def capture_instant(*, human_id: str, utterance: str, intelligence: dict,
                    source_kind: str = "human_direct",
                    authorized_humans=None,
                    category: str = "SYSTEM_INTELLIGENCE",
                    topic: str = "SMART_NOTE_SYSTEM",
                    subtopic: str = "INSTANT_ACTIVATION",
                    owner_scope: str = "PRIVATE",
                    root=None) -> InstantActivationResult:
    """Instant-activate a human-director-verified Smart Note.

    FAIL-CLOSED guards (each raises SystemExit with a machine-readable code):
      - source_kind != "human_direct"  -> NOT_HUMAN_DIRECT
      - human_id not in authorized set  -> UNAUTHORIZED_HUMAN
      - no capture intent in utterance  -> NO_CAPTURE_INTENT / reason
      - no distillable intelligence     -> EMPTY_DISTILLED_INTELLIGENCE
    """
    # ---- Guard 1: only human-direct sources take this path ----
    if source_kind != "human_direct":
        raise SystemExit(
            "INSTANT_ACTIVATION_REFUSED:NOT_HUMAN_DIRECT:"
            f"source_kind={source_kind}:route_to=admission_contract_path"
        )
    # ---- Guard 2: only authorized humans (default: the Human Director) ----
    auth = {h.lower() for h in (authorized_humans or DEFAULT_AUTHORIZED_HUMANS)}
    hid = str(human_id or "").strip().lower()
    if not hid or hid not in auth:
        raise SystemExit(
            "INSTANT_ACTIVATION_REFUSED:UNAUTHORIZED_HUMAN:"
            f"human_id={human_id!r}:agent_and_system_sources_never_authorized"
        )
    # ---- Guard 3: the utterance must carry capture intent ----
    intel_in = dict(intelligence or {})
    intent = detect_capture_intent(
        utterance,
        distilled=str(intel_in.get("lesson") or intel_in.get("essence") or ""),
        root=root,
    )
    if not intent["intent"]:
        raise SystemExit(
            "INSTANT_ACTIVATION_REFUSED:NO_CAPTURE_INTENT:"
            f"{intent['refusal']}"
        )

    root = Path(root) if root else ROOT
    now = _utc_now()
    now_iso = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    date = now.strftime("%Y-%m-%d")
    yyyymmdd = now.strftime("%Y%m%d")

    title = str(intel_in.get("title") or intent["distilled"] or "Smart Note")[:140]
    slug = (sn2.slug(title)[:48] or "smart-note")
    ib = (f"IB-SMART-NOTE-{yyyymmdd}-"
          f"{hashlib.sha256((utterance + now_iso).encode()).hexdigest()[:8]}-"
          f"{slug}")

    registry_path = root / ".naya" / "memory" / "smart-notes" / "index.json"
    capture_dir = root / ".naya" / "capture"
    brain_root = root / "BRAIN" / "05-MEMORY" / "SMART-NOTES"

    # Reserve the SN authoritatively BEFORE writing anything (same order as
    # the `project` CLI: reserve -> render -> register).
    sn_id = sn2.reserve_smart_note_id({"smart_note_id": ""}, ib,
                                      registry_path=str(registry_path))
    capture_id = f"{yyyymmdd}-{sn_id.lower()}-{slug}"
    filename = f"SMART-NOTE-{yyyymmdd}-{sn_id.lower()}-{slug}.json"

    intelligence = _build_intelligence(intel_in, utterance)
    intelligence["machine_view"]["human_director_override"] = \
        _human_director_override(now_iso)
    intelligence["machine_view"]["source_utterance"] = utterance

    capture = {
        "schema": CAPTURE_SCHEMA,
        "smart_note_id": sn_id,
        "capture_id": capture_id,
        "title": title,
        "category": category,
        "topic": topic,
        "subtopic": subtopic,
        "canonical_intent": "CAPTURE_DURABLE_INTELLIGENCE",
        "lifecycle_state": LIFECYCLE_STATE,
        # --- human-director verification (Shawn's Verification Law) ---
        "authority": AUTHORITY,
        "verified_by": "Shawn Vibert, human director",
        "verified_at_utc": now_iso,
        "verification_basis": "human_director_capture_request",
        "verification_law": ("Shawn's Verification Law: when the human director "
                             "says 'smart note this,' THAT IS THE VERIFICATION. "
                             "The ask is the verification; activates instantly."),
        "source_utterance": utterance,
        "source": {
            "captured_at": date,
            "captured_at_utc": now_iso,
            "source_type": "human_director_direct_capture",
            "source_reference": (
                f"Direct capture request from the human director "
                f"({human_id}), {now_iso}: {utterance[:280]}"
            ),
        },
        "projection": {
            "category_slug": sn2.slug(category).upper().replace("-", "_"),
            "topic_slug": sn2.slug(topic).upper().replace("-", "_"),
            "subtopic_slug": sn2.slug(subtopic).upper().replace("-", "_"),
            "publication_scope": "PRIVATE",
            "human_director_authorized_publication": False,
        },
        "intelligence": intelligence,
    }

    # Write the canonical capture (atomic: temp + os.replace).
    capture_path = capture_dir / filename
    sn2._atomic_write_json(str(capture_path), capture)
    capture_sha256 = hashlib.sha256(
        capture_path.read_bytes()).hexdigest()

    # Machine receipt.
    receipt_id = str(uuid.uuid4())
    receipt = {
        "schema": RECEIPT_SCHEMA,
        "receipt_id": receipt_id,
        "capture_id": capture_id,
        "smart_note_id": sn_id,
        "intelligent_block_id": ib,
        "capture_path": str(capture_path.relative_to(root)).replace("\\", "/"),
        "capture_sha256": capture_sha256,
        "captured_at_utc": now_iso,
        "authority": AUTHORITY,
        "verified_by": "Shawn Vibert, human director",
        "verified_at_utc": now_iso,
        "verification_basis": "human_director_capture_request",
        "source_utterance": utterance,
        "truth_state": TRUTH_STATE,
        "lifecycle_state": LIFECYCLE_STATE,
    }
    receipt["receipt_hash"] = sn2._hash_receipt(receipt)

    # The verify payload: for a human-verified capture, the verification
    # event IS the receipt. Same shape the pipeline's render()/registry
    # writers expect (lesson serializes the exact intelligence dict so the
    # audit's content-hash reconciliation matches).
    lesson_json = json.dumps(intelligence, ensure_ascii=False)
    verify = {
        "persisted": {
            "block": {
                "intelligent_block_id": ib,
                "content": {"lesson": lesson_json},
                "owner_scope": owner_scope,
                "understanding_state": TRUTH_STATE,
            },
            "event": {"id": receipt_id},
            "lineage": {"id": receipt_id},
            "relationship": {"relationship_id": receipt_id},
            "index": {"id": receipt_id},
            "checkpoint": {"id": receipt_id},
            "receipt": {"id": receipt_id},
        },
        "supersession_proof": None,
    }

    # Render the human-readable projection (PRIVATE scope needs an explicit
    # private surface; the repo's BRAIN hierarchy is the authenticated
    # private surface, matching the SN-001 precedent: PRIVATE scope,
    # GITHUB_BRAIN_PUBLISHED, ACTIVE_AUTH_GATED).
    projection = sn2.render(capture, verify, private_root=str(brain_root),
                            sn_id=sn_id)

    # Register in the projection index (the surface retrieve() actually
    # reads -- a capture file alone is invisible to it).
    with sn2.registry_transaction(str(registry_path)) as registry:
        entry = sn2._update_registry_locked(capture, verify, projection,
                                           registry, sn_id=sn_id)
        # _update_registry_locked resolves projection paths against
        # smart_note_v2.ROOT. When this module operates on a different root
        # (test harness), those fields come back None; recompute them
        # against OUR root with the same semantics. No-op in production
        # where the roots are identical.
        if not entry.get("projection_path") and \
                str(projection).startswith(str(root)):
            rel = str(projection.relative_to(root)).replace("\\", "/")
            entry["projection_path"] = rel
            entry["projection_status"] = "GITHUB_BRAIN_PUBLISHED"
            entry["smart_link"] = \
                "https://github.com/SoulSchoolAcademy/NayaPOWER/blob/main/" + rel
            entry["smart_link_status"] = (
                "ACTIVE_AUTH_GATED"
                if str(owner_scope).upper() == "PRIVATE" else "ACTIVE")

    # Persist the receipt + smart-link payload as durable evidence.
    rel_projection = str(projection.relative_to(root)).replace("\\", "/")
    smart_link_url = sl.smart_link_for(rel_projection)  # shape-validated
    payload = {
        "schema": PAYLOAD_SCHEMA,
        "smart_note_id": sn_id,
        "intelligent_block_id": ib,
        "title": title,
        "captured": {
            "capture_path": str(capture_path.relative_to(root)).replace("\\", "/"),
            "registry": str(registry_path.relative_to(root)).replace("\\", "/"),
            "registry_entry": entry.get("intelligent_block_id"),
        },
        "projection": {
            "projection_path": rel_projection,
            "smart_link": smart_link_url,
            "smart_link_status": entry.get("smart_link_status"),
            "resolves": ("on main after the branch merges; branch build only "
                         "-- never presented as universally resolvable before that"),
        },
        "receipt": receipt,
        "learning_state": {
            "truth_state": TRUTH_STATE,
            "lifecycle_state": LIFECYCLE_STATE,
            "authority": AUTHORITY,
            "automatic_path_ceiling": ("CANDIDATE (unchanged -- governs the "
                                       "automatic path only; the human-director "
                                       "override is recorded in authority)"),
        },
        "verification_law": ("Shawn's Verification Law: the ask is the "
                             "verification."),
    }
    receipt_doc = {"receipt": receipt, "smart_link_payload": payload,
                   "intent": intent}
    receipt_path = (root / RECEIPT_DIR_REL) / f"{capture_id}.json"
    sn2._atomic_write_json(str(receipt_path), receipt_doc)

    # Conformance: the new capture must pass the SN-002 gate (never weaken it).
    conformance = conf.check_capture(str(capture_path))

    return InstantActivationResult(
        intent=intent, receipt=receipt, smart_link_payload=payload,
        capture_path=str(capture_path),
        projection_path=str(projection),
        receipt_path=str(receipt_path),
        smart_note_id=sn_id, intelligent_block_id=ib,
        conformant=conformance.conformant,
    )


# ============================================================================
# RECEIPT VERIFICATION
# ============================================================================

def verify_instant_receipt(receipt: dict | str | Path, root=None) -> tuple[bool, str]:
    """Independently re-verify an instant-activation receipt.

    Recomputes the decision from the receipt's recorded inputs without
    trusting the capturer: hash integrity, schema, authority, capture file
    bytes, registry entry, and projection file.
    """
    root = Path(root) if root else ROOT
    if isinstance(receipt, (str, Path)):
        receipt = json.loads(Path(receipt).read_text(encoding="utf-8"))
        if "receipt" in receipt and "smart_link_payload" in receipt:
            receipt = receipt["receipt"]
    if not isinstance(receipt, dict):
        return False, "receipt is not a JSON object"
    if receipt.get("schema") != RECEIPT_SCHEMA:
        return False, f"unknown receipt schema: {receipt.get('schema')!r}"
    if receipt.get("receipt_hash") != sn2._hash_receipt(receipt):
        return False, "receipt hash mismatch -- receipt has been tampered with"
    if receipt.get("authority") != AUTHORITY:
        return False, f"authority is not {AUTHORITY!r}: {receipt.get('authority')!r}"
    if receipt.get("truth_state") != TRUTH_STATE:
        return False, f"truth_state is not {TRUTH_STATE!r}"

    cap_path = root / str(receipt.get("capture_path") or "")
    if not cap_path.is_file():
        return False, f"capture file missing: {receipt.get('capture_path')}"
    actual_sha = hashlib.sha256(cap_path.read_bytes()).hexdigest()
    if actual_sha != receipt.get("capture_sha256"):
        return False, "capture bytes do not match receipt capture_sha256"

    capture = json.loads(cap_path.read_text(encoding="utf-8"))
    if capture.get("authority") != AUTHORITY:
        return False, "capture file lacks the human-director-verified authority stamp"
    if not capture.get("source_utterance"):
        return False, "capture file lacks the source utterance"

    reg_path = root / ".naya" / "memory" / "smart-notes" / "index.json"
    registry = json.loads(reg_path.read_text(encoding="utf-8"))
    entry = next(
        (e for e in registry.get("entries", [])
         if e.get("smart_note_id") == receipt.get("smart_note_id")
         and e.get("intelligent_block_id") == receipt.get("intelligent_block_id")),
        None,
    )
    if entry is None:
        return False, "no registry entry matches receipt SN + IB"
    if str(entry.get("truth_state", "")).upper() != TRUTH_STATE:
        return False, f"registry truth_state is {entry.get('truth_state')!r}, not VERIFIED"

    proj = entry.get("projection_path")
    if not proj or not (root / proj).is_file():
        return False, f"projection file missing: {proj}"

    return True, (
        f"receipt verified: {receipt['smart_note_id']} / "
        f"{receipt['intelligent_block_id']} is VERIFIED/ACTIVE under "
        f"{AUTHORITY}; capture, registry, and projection all reconcile"
    )


# ============================================================================
# CLI
# ============================================================================

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="instant_activation",
                                 description="Instant activation path for "
                                             "human-director-verified Smart Notes.")
    ap.add_argument("--root", default="",
                    help="repo root override (tests); default: live repo")
    sub = ap.add_subparsers(dest="cmd", required=True)

    it = sub.add_parser("intent", help="classify capture intent of an utterance")
    it.add_argument("--utterance", required=True)
    it.add_argument("--distilled", default="")

    cp = sub.add_parser("capture", help="instant-activate one human-verified note")
    cp.add_argument("--human-id", required=True)
    cp.add_argument("--utterance", required=True)
    cp.add_argument("--intelligence-json", default="")
    cp.add_argument("--intelligence-file", default="")
    cp.add_argument("--source-kind", default="human_direct")
    cp.add_argument("--category", default="SYSTEM_INTELLIGENCE")
    cp.add_argument("--topic", default="SMART_NOTE_SYSTEM")
    cp.add_argument("--subtopic", default="INSTANT_ACTIVATION")

    vf = sub.add_parser("verify", help="independently verify an instant receipt")
    vf.add_argument("--receipt", required=True,
                    help="path to the receipt JSON (or the instant-activations doc)")

    args = ap.parse_args(argv)
    root = Path(args.root) if args.root else None

    if args.cmd == "intent":
        try:
            res = detect_capture_intent(args.utterance,
                                        distilled=args.distilled or None,
                                        root=root)
        except SystemExit as ex:
            print(json.dumps({"intent": False, "refusal": str(ex),
                              "error": True}, ensure_ascii=False))
            return 2
        print(json.dumps(res, ensure_ascii=False))
        return 0

    if args.cmd == "capture":
        intel = {}
        if args.intelligence_file:
            intel = json.loads(Path(args.intelligence_file).read_text(encoding="utf-8"))
        elif args.intelligence_json:
            intel = json.loads(args.intelligence_json)
        try:
            res = capture_instant(
                human_id=args.human_id, utterance=args.utterance,
                intelligence=intel, source_kind=args.source_kind,
                category=args.category, topic=args.topic,
                subtopic=args.subtopic, root=root)
        except SystemExit as ex:
            print(f"REFUSED {ex}", file=sys.stderr)
            return 2
        print(json.dumps({
            "smart_note_id": res.smart_note_id,
            "intelligent_block_id": res.intelligent_block_id,
            "capture_path": res.capture_path,
            "projection_path": res.projection_path,
            "receipt_path": res.receipt_path,
            "conformant": res.conformant,
            "receipt": res.receipt,
            "smart_link_payload": res.smart_link_payload,
        }, indent=2, ensure_ascii=False))
        return 0

    if args.cmd == "verify":
        ok, detail = verify_instant_receipt(args.receipt, root=root)
        print(json.dumps({"verified": ok, "detail": detail}, ensure_ascii=False))
        return 0 if ok else 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
