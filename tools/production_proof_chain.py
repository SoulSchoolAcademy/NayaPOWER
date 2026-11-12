"""Runtime proof chains for the governed production promotion path.

A production-proof chain binds an ordered sequence of proof receipts into a
single hash-linked evidence bundle. Each link commits to the canonical
content hash of its receipt AND to the previous link's hash, so the chain
head hash commits to the entire evidence set: what was proven, in what
order, against which source SHA. Verification recomputes every hash and
reports per-link and overall verdicts.

Why a chain: individual receipts each prove one fact (a promotion decision,
a failure, a parity observation, a checklist verdict). A claim like
"production at SHA X is proven" is a claim about a SET of facts in a
specific ORDER (policy verdict -> gate evidence -> proof legs -> promotion
decision -> parity observation). The chain makes that set tamper-evident:
any altered, reordered, dropped, or substituted receipt breaks the chain,
and verification names the exact broken link.

Chainable receipts (recognized schemas):
- NAYAPOWER_PRODUCTION_PROMOTION_RECEIPT_V1 (success handshake; the ONLY
  issuer of PROMOTED_AND_PROVEN -- built inline by the deploy workflow)
- NAYAPOWER_PRODUCTION_PROMOTION_FAILURE_RECEIPT_V1 (always-writable
  failure receipt)
- NAYAPOWER_PRODUCTION_PROMOTION_DENIAL_V1 (promotion denial)
- NAYAPOWER_PRODUCTION_PARITY_VERDICT_V1 (production parity observation)
- NAYAPOWER_PRODUCTION_READINESS_CHECKLIST_V1 (readiness checklist verdict)
Any other mapping is chainable but its link verifies as UNKNOWN_SCHEMA:
the chain vouches for the bundle's integrity, never for the meaning of
evidence it does not recognize.

Design rules (SN-0526 quality bar):
- Never raises. Malformed input is recorded as UNKNOWN / MALFORMED, never
  invented.
- Pure function of its inputs: no IO, no environment reads. The workflow
  or caller does IO and passes parsed receipt mappings in.
- Never weakens a gate: the strongest claim this module can emit is
  chain-integrity INTACT -- the evidence bundle is complete, ordered, and
  untampered. An INTACT chain of failure receipts proves the failures
  happened and are untampered; it certifies NOTHING about promotion.
  PROMOTED_AND_PROVEN remains exclusively the parent handshake's claim.

Schemas:
- Chain: NAYAPOWER_PRODUCTION_PROOF_CHAIN_V1
- Verification: NAYAPOWER_PRODUCTION_PROOF_CHAIN_VERIFICATION_V1
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

CHAIN_SCHEMA = "NAYAPOWER_PRODUCTION_PROOF_CHAIN_V1"
VERIFY_SCHEMA = "NAYAPOWER_PRODUCTION_PROOF_CHAIN_VERIFICATION_V1"

# Anchor for the first link's prev_link_hash. A fixed public constant: the
# genesis is a domain separator, not a secret.
GENESIS = "NAYAPOWER_PRODUCTION_PROOF_CHAIN_GENESIS_V1"

SCHEMA_ABSENT = "SCHEMA_ABSENT"
MALFORMED_RECEIPT = "MALFORMED_RECEIPT"

KNOWN_RECEIPT_SCHEMAS = frozenset(
    {
        "NAYAPOWER_PRODUCTION_PROMOTION_RECEIPT_V1",
        "NAYAPOWER_PRODUCTION_PROMOTION_FAILURE_RECEIPT_V1",
        "NAYAPOWER_PRODUCTION_PROMOTION_DENIAL_V1",
        "NAYAPOWER_PRODUCTION_PARITY_VERDICT_V1",
        "NAYAPOWER_PRODUCTION_READINESS_CHECKLIST_V1",
    }
)

# Link verdicts, worst first for reporting priority.
LINK_VERDICTS = (
    "MALFORMED_LINK",
    "SEQUENCE_BREAK",
    "TAMPERED",
    "BROKEN_LINK",
    "MALFORMED_RECEIPT",
    "UNKNOWN_SCHEMA",
    "INTACT",
)

OVERALL_VERDICTS = ("INTACT", "BROKEN", "UNKNOWN")


def canonical(obj: Any) -> bytes | None:
    """Canonical JSON bytes for hashing. None when not JSON-serializable."""
    try:
        return json.dumps(
            obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True
        ).encode("utf-8")
    except (TypeError, ValueError):
        return None


def content_hash(obj: Any) -> str | None:
    """SHA-256 hex of the canonical form. None when not serializable."""
    data = canonical(obj)
    if data is None:
        return None
    return hashlib.sha256(data).hexdigest()


def _link_envelope(seq: int, schema: str, receipt_hash: str | None, prev: str) -> dict:
    return {
        "seq": seq,
        "schema": schema,
        "receipt_hash": receipt_hash,
        "prev_link_hash": prev,
    }


def _build_link(seq: int, item: Any, prev_link_hash: str) -> dict:
    """Build one chain link. Never raises; malformed items become
    MALFORMED_RECEIPT links that verification flags."""
    schema = MALFORMED_RECEIPT
    receipt: Any = None
    receipt_hash: str | None = None
    detail: str | None = None

    if isinstance(item, Mapping):
        raw_schema = item.get("schema")
        schema = raw_schema if isinstance(raw_schema, str) and raw_schema else SCHEMA_ABSENT
        receipt_hash = content_hash(item)
        if receipt_hash is None:
            # Unserializable content cannot be hashed, therefore cannot be
            # proven: record the link as malformed, embed nothing.
            detail = "UNSERIALIZABLE_CONTENT"
            schema = MALFORMED_RECEIPT
            receipt = None
        else:
            # Embed a JSON round-tripped copy: the embedded bytes are
            # exactly what was hashed, and later caller mutation of the
            # input cannot silently change the chained evidence.
            receipt = json.loads(canonical(item).decode("utf-8"))
    else:
        detail = "RECEIPT_NOT_A_MAPPING"

    envelope = _link_envelope(seq, schema, receipt_hash, prev_link_hash)
    link = {
        "seq": seq,
        "schema": schema,
        "receipt": receipt,
        "receipt_hash": receipt_hash,
        "prev_link_hash": prev_link_hash,
        "link_hash": content_hash(envelope),
    }
    if detail is not None:
        link["detail"] = detail
    return link


def chain_receipts(
    receipts: Any,
    *,
    authorized_source_sha: Any = None,
    chained_by: Any = None,
    chain_purpose: Any = None,
) -> dict:
    """Assemble an ordered proof chain from receipt mappings. Never raises.

    `receipts`: ordered list/tuple of receipt dicts, earliest evidence
    first. The order is part of the proof: verification fails on reorder.
    Non-mapping items and unserializable content become MALFORMED_RECEIPT
    links instead of raising.
    """
    input_malformed = False
    items: list[Any]
    if receipts is None:
        items = []
    elif isinstance(receipts, (list, tuple)):
        items = list(receipts)
    else:
        items = []
        input_malformed = True

    links: list[dict] = []
    prev = GENESIS
    for seq, item in enumerate(items):
        link = _build_link(seq, item, prev)
        links.append(link)
        # A malformed envelope still advances the chain: every link,
        # including malformed ones, is committed to by its successor.
        prev = link.get("link_hash") or GENESIS

    head_hash = links[-1].get("link_hash") if links else None
    chain_id = "ppc-" + head_hash[:16] if head_hash else "ppc-empty"

    return {
        "schema": CHAIN_SCHEMA,
        "chain_id": chain_id,
        "genesis": GENESIS,
        "authorized_source_sha": authorized_source_sha,
        "chain_purpose": chain_purpose,
        "chained_by": chained_by,
        "link_count": len(links),
        "links": links,
        "head_hash": head_hash,
        "input_malformed": input_malformed,
        "authority_boundary": {
            "certifies_promotion": False,
            "certifies_evidence_integrity_only": True,
            "note": (
                "An INTACT chain proves the evidence bundle is complete, "
                "ordered, and untampered. It certifies nothing about "
                "promotion. PROMOTED_AND_PROVEN is issued exclusively by "
                "NAYAPOWER_PRODUCTION_PROMOTION_RECEIPT_V1 (the parent "
                "deploy-workflow handshake)."
            ),
        },
    }


def _verify_link(link: Any, seq: int, expected_prev: str) -> dict:
    """Verify one link. Returns {seq, schema, verdict, integrity_ok, detail}."""
    if not isinstance(link, Mapping):
        return {
            "seq": seq,
            "schema": MALFORMED_RECEIPT,
            "verdict": "MALFORMED_LINK",
            "integrity_ok": False,
            "detail": "LINK_NOT_A_MAPPING",
        }

    schema = link.get("schema")
    schema = schema if isinstance(schema, str) else SCHEMA_ABSENT
    detail: str | None = None

    if link.get("seq") != seq:
        return {
            "seq": seq,
            "schema": schema,
            "verdict": "SEQUENCE_BREAK",
            "integrity_ok": False,
            "detail": f"RECORDED_SEQ_{link.get('seq')!r}_AT_POSITION_{seq}",
        }

    receipt = link.get("receipt")
    receipt_ok = isinstance(receipt, Mapping)

    # Recompute the receipt hash from the embedded receipt. A None receipt
    # (MALFORMED_RECEIPT link) recomputes to None, which matches the
    # recorded None -- the envelope is consistent; the evidence is absent.
    recomputed_receipt_hash = content_hash(receipt) if receipt_ok else None
    if recomputed_receipt_hash != link.get("receipt_hash"):
        return {
            "seq": seq,
            "schema": schema,
            "verdict": "TAMPERED",
            "integrity_ok": False,
            "detail": "RECEIPT_HASH_MISMATCH",
        }

    if link.get("prev_link_hash") != expected_prev:
        return {
            "seq": seq,
            "schema": schema,
            "verdict": "BROKEN_LINK",
            "integrity_ok": False,
            "detail": "PREV_LINK_HASH_MISMATCH",
        }

    envelope = _link_envelope(
        seq, schema, link.get("receipt_hash"), link.get("prev_link_hash")
    )
    if content_hash(envelope) != link.get("link_hash"):
        return {
            "seq": seq,
            "schema": schema,
            "verdict": "TAMPERED",
            "integrity_ok": False,
            "detail": "LINK_ENVELOPE_HASH_MISMATCH",
        }

    if not receipt_ok:
        return {
            "seq": seq,
            "schema": schema,
            "verdict": "MALFORMED_RECEIPT",
            "integrity_ok": True,
            "detail": link.get("detail") or "RECEIPT_ABSENT_OR_NOT_A_MAPPING",
        }

    if schema not in KNOWN_RECEIPT_SCHEMAS:
        return {
            "seq": seq,
            "schema": schema,
            "verdict": "UNKNOWN_SCHEMA",
            "integrity_ok": True,
            "detail": "SCHEMA_NOT_RECOGNIZED_INTEGRITY_VERIFIED",
        }

    return {
        "seq": seq,
        "schema": schema,
        "verdict": "INTACT",
        "integrity_ok": True,
        "detail": detail,
    }


def verify_chain(chain: Any) -> dict:
    """Verify a proof chain. Never raises.

    Returns a NAYAPOWER_PRODUCTION_PROOF_CHAIN_VERIFICATION_V1 verdict:
    - overall INTACT: every link intact -- the bundle is complete, ordered,
      untampered, and every receipt is a recognized schema.
    - overall BROKEN: at least one link failed; per-link verdicts name it.
    - overall UNKNOWN: the chain object itself is malformed or empty --
      an empty chain proves nothing.
    integrity_intact separates hash-mechanics soundness from
    interpretability: True means no link was tampered, reordered, or
    structurally broken, even if some receipt is uninterpretable
    (UNKNOWN_SCHEMA) or absent (MALFORMED_RECEIPT).
    """
    def unknown(reason: str) -> dict:
        return {
            "schema": VERIFY_SCHEMA,
            "chain_id": None,
            "chain_head_hash": None,
            "link_count": 0,
            "overall": "UNKNOWN",
            "integrity_intact": False,
            "reason": reason,
            "links": [],
        }

    if not isinstance(chain, Mapping):
        return unknown("CHAIN_NOT_A_MAPPING")
    if chain.get("schema") != CHAIN_SCHEMA:
        return unknown(f"UNEXPECTED_SCHEMA_{chain.get('schema')!r}")
    links = chain.get("links")
    if not isinstance(links, list):
        return unknown("LINKS_NOT_A_LIST")
    if not links:
        return unknown("EMPTY_CHAIN_PROVES_NOTHING")

    results: list[dict] = []
    expected_prev = GENESIS
    for seq, link in enumerate(links):
        result = _verify_link(link, seq, expected_prev)
        results.append(result)
        # Advance by the RECORDED link hash: a tampered link's recorded
        # hash is what its successor committed to, so the successor
        # verifies against the chain as recorded, not as recomputed.
        recorded = link.get("link_hash") if isinstance(link, Mapping) else None
        expected_prev = recorded if isinstance(recorded, str) else GENESIS

    overall = "INTACT" if all(r["verdict"] == "INTACT" for r in results) else "BROKEN"
    return {
        "schema": VERIFY_SCHEMA,
        "chain_id": chain.get("chain_id"),
        "chain_head_hash": chain.get("head_hash"),
        "link_count": len(results),
        "overall": overall,
        "integrity_intact": all(r["integrity_ok"] for r in results),
        "authorized_source_sha": chain.get("authorized_source_sha"),
        "links": results,
    }


def summarize_chain(chain: Any) -> dict:
    """One-line machine summary of a chain's CLAIMS (not a verification).

    Use verify_chain() for the verdict; this only restates what the chain
    object asserts about itself, for feed posts and logs. Never raises.
    """
    if not isinstance(chain, Mapping) or chain.get("schema") != CHAIN_SCHEMA:
        return {"chain_id": None, "error": "NOT_A_PROOF_CHAIN"}
    links = chain.get("links")
    schemas = []
    if isinstance(links, list):
        for link in links:
            if isinstance(link, Mapping):
                s = link.get("schema")
                schemas.append(s if isinstance(s, str) else SCHEMA_ABSENT)
    head = chain.get("head_hash")
    return {
        "chain_id": chain.get("chain_id"),
        "head_hash": head,
        "head_short": head[:12] if isinstance(head, str) else None,
        "link_count": chain.get("link_count"),
        "schemas": schemas,
        "authorized_source_sha": chain.get("authorized_source_sha"),
        "chain_purpose": chain.get("chain_purpose"),
    }


# Canonical order for the deploy workflow's runtime proof bundle: upstream
# gate evidence first, promotion decision (denial, success receipt, or
# failure receipt), then the parity observation last. Only receipts that
# carry a recognized schema are chained: the chain vouches for the bundle's
# integrity, never for evidence it does not recognize. The workflow still
# uploads every receipt individually; skipped roles are recorded, not
# hidden.
DEPLOY_CHAIN_ROLES = (
    "promotion_denial",
    "promotion_receipt",
    "failure_receipt",
    "parity_verdict",
)


def assemble_deploy_chain(
    receipts_by_role: Any,
    *,
    authorized_source_sha: Any = None,
    chained_by: Any = None,
    chain_purpose: Any = None,
) -> dict:
    """Assemble the deploy run's receipts into an ordered proof chain.

    `receipts_by_role` maps a DEPLOY_CHAIN_ROLES role to a receipt mapping
    (or None when that file was not produced). Pure, never raises. The
    returned chain carries `roles_chained` (role + schema per link),
    `roles_skipped` (role + reason for every role not chained), and
    `role_conflicts` (both success and failure receipts present would mean
    the run emitted two promotion decisions; chaining them is still
    integrity-honest, but the conflict is flagged loudly).
    """
    ordered: list[Any] = []
    roles_chained: list[dict] = []
    roles_skipped: list[dict] = []
    role_conflicts: list[str] = []
    items = receipts_by_role if isinstance(receipts_by_role, Mapping) else {}
    for role in DEPLOY_CHAIN_ROLES:
        receipt = items.get(role) if isinstance(items, Mapping) else None
        if receipt is None:
            roles_skipped.append({"role": role, "reason": "RECEIPT_ABSENT"})
            continue
        if not isinstance(receipt, Mapping):
            roles_skipped.append({"role": role, "reason": "RECEIPT_NOT_A_MAPPING"})
            continue
        schema = receipt.get("schema")
        if not isinstance(schema, str) or not schema:
            roles_skipped.append({"role": role, "reason": "SCHEMA_ABSENT"})
            continue
        if schema not in KNOWN_RECEIPT_SCHEMAS:
            roles_skipped.append({"role": role, "reason": f"UNKNOWN_SCHEMA_{schema}"})
            continue
        ordered.append(receipt)
        roles_chained.append({"role": role, "schema": schema})
    if (
        isinstance(items, Mapping)
        and items.get("promotion_receipt") is not None
        and items.get("failure_receipt") is not None
    ):
        role_conflicts.append("BOTH_SUCCESS_AND_FAILURE_RECEIPTS_PRESENT")

    chain = chain_receipts(
        ordered,
        authorized_source_sha=authorized_source_sha,
        chained_by=chained_by,
        chain_purpose=chain_purpose,
    )
    chain["roles_chained"] = roles_chained
    chain["roles_skipped"] = roles_skipped
    chain["role_conflicts"] = role_conflicts
    return chain


def _cli(argv: "list[str] | None" = None) -> int:
    """Independent-verification entry point for another seat or human.

    --verify FILE: verify a NAYAPOWER_PRODUCTION_PROOF_CHAIN_V1 bundle and
    print per-link verdicts. Exit 0 = INTACT, 1 = BROKEN, 2 = UNKNOWN or
    unreadable file.
    --summarize FILE: print the chain's machine summary (its claims, not a
    verification). Exit 0 on success, 2 on unreadable file.
    """
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="Verify or summarize a runtime production proof chain."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--verify", metavar="CHAIN_FILE", help="verify a proof chain file")
    group.add_argument(
        "--summarize", metavar="CHAIN_FILE", help="print a proof chain's machine summary"
    )
    args = parser.parse_args(argv)
    path = args.verify or args.summarize
    try:
        with open(path, encoding="utf-8") as f:
            chain = json.load(f)
    except (OSError, ValueError) as exc:
        print(f"cannot read chain file {path}: {exc}", file=sys.stderr)
        return 2
    if args.summarize:
        print(json.dumps(summarize_chain(chain), indent=2))
        return 0
    verdict = verify_chain(chain)
    print(f"chain_id: {verdict.get('chain_id')}")
    print(f"overall: {verdict.get('overall')}  integrity_intact: {verdict.get('integrity_intact')}")
    for link in verdict.get("links", []):
        print(f"  link {link['seq']}: {link['schema']} -> {link['verdict']} ({link['detail']})")
    overall = verdict.get("overall")
    return 0 if overall == "INTACT" else (1 if overall == "BROKEN" else 2)


if __name__ == "__main__":
    raise SystemExit(_cli())
