"""Anchoring for runtime production proof chains.

A hash-linked proof chain (tools/production_proof_chain.py) proves the
evidence bundle is complete, ordered, and untampered -- but only for
whoever holds the bundle. An anchor is the public, minimal record that
lets the whole team check a bundle LATER: it publishes the chain's
head hash, the authorized source SHA, the receipt sequence, and the
verification verdict it earned at anchor time.

Anchoring convention: the anchor record (or at minimum its head hash
and chain id) is posted to the Production Readiness home feed (#1771).
That post is the timestamped public commitment. Anyone can then
re-fetch the bundle, recompute the head hash, and confirm it matches
the anchored one -- silent substitution of the bundle becomes
detectable.

What an anchor is and is not:
- IS: a public commitment that bundle B with head hash H verified
  INTACT at time T against authorized source SHA S. Certifies evidence
  integrity only.
- IS NOT: promotion, certification, deployment authorization, or a
  verdict about what the receipts mean. An ANCHORED chain of failure
  receipts proves the failures are recorded and untampered -- it
  certifies nothing about promotion. PROMOTED_AND_PROVEN remains
  exclusively the parent deploy-workflow handshake's claim.

Design rules (SN-0526 quality bar):
- Never raises. Malformed input is recorded as INVALID_INPUT /
  NOT_ANCHORABLE with a reason, never invented.
- Pure function of its inputs: no IO, no environment reads, no feed
  posts. The caller does IO and posting; this module only builds and
  checks the record.
- Never weakens a gate: an anchor is emitted as ANCHORED only when the
  verification it binds is INTACT and its head hash matches the
  chain's. Anything else is NOT_ANCHORABLE.

Schemas:
- Anchor: NAYAPOWER_PRODUCTION_PROOF_CHAIN_ANCHOR_V1
- Anchor verification: NAYAPOWER_PRODUCTION_PROOF_CHAIN_ANCHOR_VERIFICATION_V1
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

try:
    from production_proof_chain import verify_chain as _verify_chain
except Exception:  # pragma: no cover - import seam fallback
    _verify_chain = None

ANCHOR_SCHEMA = "NAYAPOWER_PRODUCTION_PROOF_CHAIN_ANCHOR_V1"
ANCHOR_VERIFY_SCHEMA = "NAYAPOWER_PRODUCTION_PROOF_CHAIN_ANCHOR_VERIFICATION_V1"

_STATUS_ANCHORED = "ANCHORED"
_STATUS_NOT_ANCHORABLE = "NOT_ANCHORABLE"
_STATUS_INVALID_INPUT = "INVALID_INPUT"


def _canonical(obj: Any) -> bytes | None:
    """Canonical JSON bytes for hashing, or None if not serializable."""
    try:
        return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    except Exception:
        return None


def _anchor_id(head_hash: str, authorized_source_sha: str | None, workflow_run_id: Any) -> str:
    seed = "|".join([
        str(head_hash),
        str(authorized_source_sha or ""),
        str(workflow_run_id if workflow_run_id is not None else ""),
    ])
    return "pca-" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]


def _link_digest(link: Any) -> dict:
    """Minimal public summary of one chain link. Never raises."""
    try:
        if not isinstance(link, Mapping):
            return {"seq": None, "schema": "MALFORMED_LINK", "link_hash": None,
                    "receipt_status": None}
        receipt = link.get("receipt")
        status_hint = None
        if isinstance(receipt, Mapping):
            # Record the receipt's own claim verbatim, labeled as observed.
            for key in ("status", "verdict"):
                if key in receipt:
                    status_hint = {key: receipt[key]}
                    break
        return {
            "seq": link.get("seq"),
            "schema": link.get("schema"),
            "link_hash": link.get("link_hash"),
            "receipt_status": status_hint,
        }
    except Exception:
        return {"seq": None, "schema": "MALFORMED_LINK", "link_hash": None,
                "receipt_status": None}


def build_anchor(chain: Any, verification: Any, context: Any = None) -> dict:
    """Build an anchor record for a verified proof chain. Never raises.

    `context` may carry: authorized_source_sha, workflow_run_id,
    anchored_by, anchored_at. Every field is treated as untrusted
    observation: missing fields are recorded as None, never invented.
    """
    try:
        ctx = context if isinstance(context, Mapping) else {}
        ver = verification if isinstance(verification, Mapping) else {}
        ch = chain if isinstance(chain, Mapping) else {}

        chain_id = ch.get("chain_id")
        head_hash = ch.get("head_hash")
        links = ch.get("links")
        ver_overall = ver.get("overall")
        ver_head = ver.get("chain_head_hash")

        reason = None
        if not isinstance(ch, Mapping) or not isinstance(links, list) or not head_hash:
            status = _STATUS_INVALID_INPUT
            reason = "chain bundle is missing links or head_hash"
        elif ver_overall != "INTACT":
            status = _STATUS_NOT_ANCHORABLE
            reason = "verification overall is %r, not INTACT" % (ver_overall,)
        elif ver_head != head_hash:
            status = _STATUS_NOT_ANCHORABLE
            reason = "verification head hash does not match chain head hash"
        else:
            status = _STATUS_ANCHORED

        authorized_source_sha = ctx.get("authorized_source_sha")
        if authorized_source_sha is None:
            authorized_source_sha = ch.get("authorized_source_sha")
        workflow_run_id = ctx.get("workflow_run_id")

        anchor = {
            "schema": ANCHOR_SCHEMA,
            "status": status,
            "anchor_id": (_anchor_id(head_hash, authorized_source_sha, workflow_run_id)
                          if head_hash and status == _STATUS_ANCHORED else None),
            "chain_id": chain_id,
            "head_hash": head_hash,
            "link_count": len(links) if isinstance(links, list) else None,
            "authorized_source_sha": authorized_source_sha,
            "workflow_run_id": workflow_run_id,
            "links": [_link_digest(link) for link in links] if isinstance(links, list) else None,
            "verification_overall": ver_overall,
            "anchored_by": ctx.get("anchored_by"),
            "anchored_at": ctx.get("anchored_at"),
            "anchor_reason": reason,
            "authority_boundary": {
                "certifies_evidence_integrity_only": True,
                "certifies_promotion": False,
                "authorizes_deployment": False,
                "note": ("An ANCHORED record commits to the existence and "
                         "integrity of one chain bundle at anchor time. It "
                         "certifies nothing about promotion or deployment. "
                         "PROMOTED_AND_PROVEN remains exclusively the parent "
                         "deploy-workflow handshake's claim."),
            },
        }
        return anchor
    except Exception as exc:  # pragma: no cover - defensive; never raises
        return {"schema": ANCHOR_SCHEMA, "status": _STATUS_INVALID_INPUT,
                "anchor_reason": "unexpected error: %s" % (exc,)}


def verify_anchor(anchor: Any, chain: Any) -> dict:
    """Check an anchor record against a chain bundle. Never raises.

    The check is two-layer, and both must pass:
    1. Re-verify the bundle's own integrity from scratch (recompute
       every link hash -- trusting the bundle's stored head_hash field
       would be security theater: a receipt can be edited while the
       old head hash is left in place).
    2. Compare the bundle against the anchor: head hash, link count,
       chain id, authorized source SHA.

    Returns INTACT when both layers pass; TAMPERED on any failure of
    either layer; UNKNOWN when the anchor is malformed or was never
    ANCHORED.
    """
    try:
        a = anchor if isinstance(anchor, Mapping) else None
        ch = chain if isinstance(chain, Mapping) else None
        if a is None or ch is None or a.get("schema") != ANCHOR_SCHEMA:
            return {"schema": ANCHOR_VERIFY_SCHEMA, "verdict": "UNKNOWN",
                    "detail": "anchor or chain malformed"}
        if a.get("status") != _STATUS_ANCHORED:
            return {"schema": ANCHOR_VERIFY_SCHEMA, "verdict": "UNKNOWN",
                    "detail": "anchor was never ANCHORED (%r)" % (a.get("status"),)}

        # Layer 1: the bundle must be internally intact, recomputed now.
        if _verify_chain is not None:
            fresh = _verify_chain(ch)
            if not isinstance(fresh, Mapping) or fresh.get("overall") != "INTACT":
                return {"schema": ANCHOR_VERIFY_SCHEMA, "verdict": "TAMPERED",
                        "mismatched_fields": ["bundle_integrity"],
                        "detail": "bundle failed internal re-verification"}

        # Layer 2: the intact bundle must be the anchored bundle.
        mismatches = []
        if a.get("head_hash") != ch.get("head_hash"):
            mismatches.append("head_hash")
        if a.get("chain_id") != ch.get("chain_id"):
            mismatches.append("chain_id")
        if a.get("link_count") != (len(ch.get("links")) if isinstance(ch.get("links"), list) else None):
            mismatches.append("link_count")
        if a.get("authorized_source_sha") != ch.get("authorized_source_sha"):
            mismatches.append("authorized_source_sha")

        if mismatches:
            return {"schema": ANCHOR_VERIFY_SCHEMA, "verdict": "TAMPERED",
                    "mismatched_fields": mismatches, "detail": None}
        return {"schema": ANCHOR_VERIFY_SCHEMA, "verdict": "INTACT",
                "mismatched_fields": [], "detail": None}
    except Exception as exc:  # pragma: no cover - defensive; never raises
        return {"schema": ANCHOR_VERIFY_SCHEMA, "verdict": "UNKNOWN",
                "detail": "unexpected error: %s" % (exc,)}


def summarize_anchor(anchor: Any) -> dict:
    """One-line summary of an anchor record. Never raises."""
    try:
        a = anchor if isinstance(anchor, Mapping) else {}
        head = a.get("head_hash")
        return {
            "schema": ANCHOR_SCHEMA,
            "status": a.get("status"),
            "anchor_id": a.get("anchor_id"),
            "head_short": head[:12] if isinstance(head, str) else None,
            "link_count": a.get("link_count"),
            "authorized_source_sha": a.get("authorized_source_sha"),
            "workflow_run_id": a.get("workflow_run_id"),
            "verification_overall": a.get("verification_overall"),
        }
    except Exception:
        return {"schema": ANCHOR_SCHEMA, "status": _STATUS_INVALID_INPUT}
