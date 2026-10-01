"""ACT→KNOW handoff for Demo-1 (naya4 builder lane).

Takes a staging ACT *execution* receipt, verifies it end-to-end (seal
recompute + artifact re-hash against the receipt's bound SHA-256) BEFORE
KNOW ever sees it, builds the KNOW ingestion candidate FROM the verified
facts only, and runs it through the kernel's KNOW gate inside ``decide()``.
The resulting kernel decision receipt carries every field the persistence
seam requires (Naya 2's ``project_kernel_receipt``, PR #1243):
``receipt_hash``, ``receipt_id``, ``decision_id``, ``issued_at``,
``kernel_version``, ``verdict`` — plus ``inputs_hash`` over the decided
input state for the adapter's recompute-or-reject.

Refusal is fail-closed: any verification failure raises ``HandoffRefused``
before ``decide()`` is called, so KNOW holds nothing from a broken handoff.

This module is a projection over existing seams — it does not create a
second registry, a second store, or a second receipt system:
- the capability stays declared in the canonical Smart Door registry
  (``naya_kernel.smart_door``);
- the receipt seal check reuses ``ActNode.recompute`` (ACT §4.1);
- ingestion and retrieval reuse ``KnowNode.ingest`` / ``KnowNode.retrieve``;
- durability projection reuses Naya 2's ``project_kernel_receipt``
  (read-only; this module never touches a database).
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any, Dict, Optional

from naya_kernel.nodes import act_node

# Matches the executor's own effects string (naya_kernel.smart_door):
#   "wrote demo-staging/<file> (<n> bytes, sha256:<hex>)"
#   "already_present demo-staging/<file> (<n> bytes, sha256:<hex>) — ..."
_EFFECTS_RE = re.compile(
    r"(?:wrote|already_present) demo-staging/(\S+) "
    r"\((\d+) bytes, sha256:([0-9a-f]{64})\)"
)

_DEMO_PRINCIPAL_NOTE = "test principal; not a production identity"


class HandoffRefused(Exception):
    """The ACT→KNOW handoff was refused. KNOW was not touched."""


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_act_execution_receipt(receipt: Dict[str, Any],
                                 staging_root: str) -> Dict[str, Any]:
    """Verify a staging ACT execution receipt end-to-end.

    Checks, in order: the receipt is a dict; the ACT seal recomputes
    (``ActNode.recompute`` §4.1); the execution path was EXECUTED; the
    bound artifact parses from ``effects_observed``; the artifact resolves
    inside ``<staging_root>/demo-staging/`` (no escape); the file exists;
    its SHA-256 matches the receipt's bound hash.

    Returns the verified observation facts. Raises ``HandoffRefused`` on
    the first failure — before any KNOW state is touched.
    """
    if not isinstance(receipt, dict):
        raise HandoffRefused("handoff refused: receipt is not a JSON object")
    execution_id = receipt.get("execution_id") or "<unknown>"

    def refuse(reason: str) -> HandoffRefused:
        return HandoffRefused(
            f"handoff refused for act-execution {execution_id}: {reason}")

    # 1. Seal: the receipt must recompute under ACT's canonicalization.
    try:
        seal = act_node.ActNode().recompute(receipt)
    except Exception as exc:
        raise refuse(f"seal check raised {type(exc).__name__}: {exc}")
    if seal != "MATCH":
        raise refuse("receipt seal MISMATCH — not ACT-canonical or tampered")

    # 2. Only successful executions hand off observations in Demo-1.
    if receipt.get("path") != "EXECUTED":
        raise refuse(f"execution path is {receipt.get('path')!r}, not EXECUTED")

    # 3. The artifact binding must parse from the receipt's own observation.
    effects = receipt.get("effects_observed") or ""
    match = _EFFECTS_RE.search(str(effects))
    if not match:
        raise refuse("effects_observed carries no parseable artifact binding")
    filename, size_claim, sha_claim = match.group(1), int(match.group(2)), match.group(3)

    # 4. Resolve inside the sandbox; refuse escapes.
    root = Path(staging_root).resolve()
    sandbox = root / "demo-staging"
    target = (sandbox / filename).resolve()
    if sandbox not in target.parents and target != sandbox:
        raise refuse(f"artifact path escapes the staging sandbox: {filename!r}")
    if not target.is_file():
        raise refuse(f"artifact not re-observable on disk: {target}")

    # 5. Re-hash the bytes; the binding must hold.
    actual_sha = _sha256_file(target)
    if actual_sha != sha_claim:
        raise refuse(
            f"artifact sha256 MISMATCH — receipt binds {sha_claim[:16]}…, "
            f"disk has {actual_sha[:16]}…")

    return {
        "execution_id": receipt.get("execution_id"),
        "issued_at": receipt.get("issued_at"),
        "receipt_hash": receipt.get("receipt_hash"),
        "tool_id": (receipt.get("tool") or {}).get("tool_id"),
        "artifact_relpath": f"demo-staging/{filename}",
        "artifact_sha256": actual_sha,
        "artifact_bytes": target.stat().st_size,
        "artifact_size_claim": size_claim,
    }


def build_observation_candidate(observation: Dict[str, Any]) -> Dict[str, Any]:
    """Build the KNOW ingestion candidate FROM verified observation facts.

    The candidate claims nothing the verification did not establish: the
    execution id, timestamps, hashes, and artifact bytes all come from the
    verified receipt + the re-hashed file. Provenance kind is
    ACTION_OUTCOME; class is EPHEMERAL (a single execution's observation,
    superseded by the next run) with recorded signals.
    """
    content = (
        "ACT observation: %(tool_id)s executed (execution_id=%(execution_id)s) "
        "at %(issued_at)s; wrote %(artifact_relpath)s "
        "(%(artifact_bytes)d bytes, sha256:%(artifact_sha256)s); "
        "act receipt %(receipt_hash)s."
    ) % observation
    return {
        "content": content,
        "proposed_class": "EPHEMERAL",
        "class_signals": [
            {"signal": "single-execution-observation", "value": 1.0},
            {"signal": "superseded-by-next-demo-run", "value": 0.9},
            {"signal": "artifact-rehashed-at-handoff", "value": 1.0},
        ],
        "classifier": "auto",
        "provenance": {"sources": [{
            "kind": "ACTION_OUTCOME",
            "ref": "act-execution:%s" % observation["execution_id"],
            "capturedAt": observation["issued_at"],
            "capturedBy": "naya4-act-know-handoff",
            "receipt_hash": observation["receipt_hash"],
            "artifact_sha256": observation["artifact_sha256"],
        }]},
        "identity_binding": {"verified": True,
                             "by": "demo-principal-attestation",
                             "note": _DEMO_PRINCIPAL_NOTE},
        "owner_scope": "public",
        "epistemic_state": "INGESTED",
    }


def handoff_act_to_know(kernel,
                        receipt: Dict[str, Any],
                        *,
                        staging_root: str,
                        principal: Dict[str, Any],
                        gate_states: Dict[str, Any],
                        decision_id: Optional[str] = None,
                        now: Optional[str] = None) -> Dict[str, Any]:
    """Run the ACT→KNOW handoff through the kernel.

    1. ``verify_act_execution_receipt`` — raises ``HandoffRefused`` before
       KNOW is touched on any failure.
    2. Build the candidate from the verified facts only.
    3. ``kernel.decide()`` with the KNOW sub-state carrying
       ``{candidate, principal}`` — the kernel's KNOW gate runs the §3.1
       ingestion gate end-to-end; every other gate keeps its supplied
       sub-state.
    4. The KNOW gate must PASS; the ingested block is located by its
       provenance ref (never by recomputing KNOW's internal id scheme).

    Returns the decision receipt, the decided input state (for the seam's
    ``inputs_hash`` recompute), the KNOW block id, and the verified
    observation. The caller projects the decision receipt through
    ``project_kernel_receipt`` read-only; this function performs no I/O
    beyond reading the already-verified artifact bytes.
    """
    observation = verify_act_execution_receipt(receipt, staging_root)
    candidate = build_observation_candidate(observation)

    know_state: Dict[str, Any] = {"candidate": candidate,
                                  "principal": dict(principal)}
    if now is not None:
        know_state["now"] = now
    gates = dict(gate_states)
    gates["KNOW"] = know_state
    state = {"decision_id": decision_id or
             "demo1-act-know-%s" % str(observation["execution_id"])[:8],
             "gates": gates}

    out = kernel.decide(state)
    decision_receipt = out["decision_receipt"]
    know_gate = next((g for g in decision_receipt["gates"]
                      if g["node"] == "KNOW"), None)
    if know_gate is None or know_gate["verdict"] != "PASS":
        raise HandoffRefused(
            "handoff refused: KNOW gate did not PASS: %s"
            % ((know_gate or {}).get("reasons") or
               ["no KNOW gate record in decision"]))

    provenance_ref = "act-execution:%s" % observation["execution_id"]
    know_node = kernel.nodes["KNOW"]
    block_id = next(
        (bid for bid, block in know_node.blocks.items()
         if any(s.get("ref") == provenance_ref
                for s in (block.get("provenance") or {}).get("sources", []))),
        None)
    if block_id is None:
        raise HandoffRefused(
            "handoff refused: KNOW gate passed but the observation block "
            "was not found by provenance ref")

    return {
        "decision_receipt": decision_receipt,
        "input_state": state,
        "block_id": block_id,
        "know_verdict": know_gate["verdict"],
        "know_gate_reasons": list(know_gate["reasons"]),
        "observation": observation,
        "candidate": candidate,
    }
