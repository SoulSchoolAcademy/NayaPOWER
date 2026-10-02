"""Demo-1 P3: PROVE/CONNECT handling of the handed-off KNOW observation.

Takes the P2 ACT->KNOW handoff output plus the original ACT execution
receipt, verifies the whole chain AGAIN (EXECUTED path, ACT seal recompute,
receipt-hash consistency with the handoff's observation, artifact re-hash,
handoff decision-receipt seal, KNOW block provenance + gated retrieval)
BEFORE PROVE ever sees it. The post-action PROOF_CLAIM is built FROM the
verified facts only:

  post-action proof = observation + outcome + acceptance + causal limits
                      + learning eligibility

Master-directive law enforced here:
- NEVER outcome-proof-before-ACT: without an EXECUTED ACT execution behind
  the claim, verification refuses first — there is nothing to prove.
- ACT success != outcome success: the claim bounds itself to the bound
  artifact bytes; no effect beyond them is asserted (A4), and the causal
  limit rides in the claim itself, not in a comment.
- PROVE never writes VERIFIED: L2/L4 map to SUPPORTED per the ratified V2
  enum mapping (LADDER_TO_V2_EPISTEMIC) — never VERIFIED.

The claim climbs the kernel's PROVE gate inside ``decide()``; the sealed
claim crosses the CONNECT boundary via PROVE's ``crossing_check`` —
nothing unproven crosses. VERIFY/LEARN/EVOLVE remain named next actions.

Refusal is fail-closed: any verification failure raises
``ProveObservationRefused`` before ``decide()`` is called, so PROVE holds
nothing from a broken observation.

This module is a projection over existing seams — it does not create a
second registry, a second store, or a second receipt system:
- the seal check reuses ``ActNode.recompute`` (ACT §4.1);
- the handoff receipt seal reuses ``verify_decision_receipt``;
- certification reuses ``ProveNode`` through the kernel's PROVE gate;
- the CONNECT boundary reuses PROVE's ``crossing_check``;
- durability projection reuses the same decision-receipt contract the
  persistence seam consumes (receipt_hash / inputs_hash recompute).
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from naya_kernel.kernel import verify_decision_receipt
from naya_kernel.nodes import act_node

_DEMO_PRINCIPAL_NOTE = "test principal; not a production identity"


class ProveObservationRefused(Exception):
    """The post-action proof was refused. PROVE was not touched."""


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def verify_observation_chain(kernel,
                             handoff_result: Dict[str, Any],
                             act_receipt: Dict[str, Any],
                             staging_root: str,
                             *,
                             principal: Dict[str, Any],
                             now: Optional[str] = None) -> Dict[str, Any]:
    """Re-verify the full ACT->KNOW chain BEFORE PROVE sees anything.

    Checks, in order: the handoff output and the ACT receipt are dicts; the
    ACT receipt's path was EXECUTED (never proof-before-ACT); the receipt's
    hash matches the hash the handoff bound into its observation; the ACT
    seal recomputes; the artifact resolves inside the sandbox, exists, and
    re-hashes to the bound SHA-256; the handoff decision receipt's seal
    recomputes; the KNOW block exists with the ACT provenance ref; the
    block is served back through KNOW's own gated retrieval.

    Returns the verified facts. Raises ``ProveObservationRefused`` on the
    first failure — before any PROVE state is touched.
    """
    if not isinstance(handoff_result, dict):
        raise ProveObservationRefused(
            "proof refused: handoff result is not a JSON object")
    if not isinstance(act_receipt, dict):
        raise ProveObservationRefused(
            "proof refused: act receipt is not a JSON object")
    observation = handoff_result.get("observation") or {}
    execution_id = observation.get("execution_id") or "<unknown>"

    def refuse(reason: str) -> ProveObservationRefused:
        return ProveObservationRefused(
            f"proof refused for observation {execution_id}: {reason}")

    # 1. NEVER outcome-proof-before-ACT: without an EXECUTED ACT execution
    #    there is nothing post-action to prove. This fires before the seal
    #    check on purpose — existence precedes authenticity.
    if act_receipt.get("path") != "EXECUTED":
        raise refuse(
            f"no EXECUTED ACT execution behind this claim "
            f"(path is {act_receipt.get('path')!r}) — proof-before-ACT refused")

    # 2. The receipt handed to PROVE must be the one the handoff verified.
    if act_receipt.get("receipt_hash") != observation.get("receipt_hash"):
        raise refuse(
            "act receipt does not match the observation the handoff bound "
            "(receipt_hash mismatch)")

    # 3. Seal: the receipt must recompute under ACT's canonicalization.
    try:
        seal = act_node.ActNode().recompute(act_receipt)
    except Exception as exc:
        raise refuse(f"seal check raised {type(exc).__name__}: {exc}")
    if seal != "MATCH":
        raise refuse("receipt seal MISMATCH — not ACT-canonical or tampered")

    # 4. Re-observe the artifact: resolve inside the sandbox; refuse escapes;
    #    the bytes must re-hash to the bound SHA-256.
    relpath = str(observation.get("artifact_relpath") or "")
    if not relpath.startswith("demo-staging/"):
        raise refuse(
            f"artifact relpath is not sandbox-scoped: {relpath!r}")
    root = Path(staging_root).resolve()
    sandbox = root / "demo-staging"
    target = (sandbox / relpath[len("demo-staging/"):]).resolve()
    if sandbox not in target.parents and target != sandbox:
        raise refuse(f"artifact path escapes the staging sandbox: {relpath!r}")
    if not target.is_file():
        raise refuse(f"artifact not re-observable on disk: {target}")
    actual_sha = _sha256_file(target)
    if actual_sha != observation.get("artifact_sha256"):
        raise refuse(
            f"artifact sha256 MISMATCH — observation binds "
            f"{str(observation.get('artifact_sha256'))[:16]}…, disk has "
            f"{actual_sha[:16]}…")

    # 5. The handoff's decision receipt must still seal-verify: the
    #    acceptance (KNOW gate PASS) is attested, not assumed.
    decision_receipt = handoff_result.get("decision_receipt") or {}
    check = verify_decision_receipt(decision_receipt)
    if check.get("result") != "MATCH":
        raise refuse("handoff decision receipt seal MISMATCH")

    # 6. The KNOW block must exist and carry the ACT provenance ref.
    block_id = handoff_result.get("block_id")
    know = kernel.nodes["KNOW"]
    block = (know.blocks or {}).get(block_id)
    if block is None:
        raise refuse(f"KNOW block {block_id!r} not present in the store")
    provenance_ref = "act-execution:%s" % observation.get("execution_id")
    sources = (block.get("provenance") or {}).get("sources") or []
    if not any(s.get("ref") == provenance_ref for s in sources):
        raise refuse(
            f"KNOW block {block_id!r} carries no {provenance_ref} source")

    # 7. The block must be served back through KNOW's own gated retrieval —
    #    admission, not assumption.
    served = know.retrieve(
        {"text": "%s executed" % observation.get("tool_id"),
         "requested_scopes": ["public"],
         "identity_binding": {"verified": True}},
        principal)
    if not served.get("admitted") or not any(
            b.get("id") == block_id for b in served.get("blocks") or []):
        raise refuse(
            f"KNOW gated retrieval did not serve block {block_id!r}")

    verified_at = now or _utcnow()
    return {
        "execution_id": observation.get("execution_id"),
        "issued_at": observation.get("issued_at"),
        "tool_id": observation.get("tool_id"),
        "receipt_hash": observation.get("receipt_hash"),
        "artifact_relpath": relpath,
        "artifact_sha256": actual_sha,
        "artifact_bytes": target.stat().st_size,
        "handoff_decision_id": decision_receipt.get("decision_id"),
        "handoff_receipt_id": decision_receipt.get("receipt_id"),
        "handoff_receipt_hash": decision_receipt.get("receipt_hash"),
        "block_id": block_id,
        "block_content_sha256": _sha256_text(block.get("content") or ""),
        "verified_at": verified_at,
    }


def build_post_action_claim(verified: Dict[str, Any],
                            *,
                            now: Optional[str] = None) -> Dict[str, Any]:
    """Build the post-action PROOF_CLAIM FROM the verified facts only.

    The builder reads an explicit, fixed key list from ``verified`` — any
    extra key a caller injects (e.g. an inflated outcome) never reaches the
    claim. The claim asserts: observation (A1), outcome-as-observed (A2),
    acceptance (A3), causal limits (A4), learning eligibility (A5).
    """
    as_of = now or verified.get("verified_at") or _utcnow()
    execution_id = verified["execution_id"]
    tool_id = verified["tool_id"]
    issued_at = verified["issued_at"]
    receipt_hash = verified["receipt_hash"]
    relpath = verified["artifact_relpath"]
    artifact_sha256 = verified["artifact_sha256"]
    artifact_bytes = verified["artifact_bytes"]
    handoff_receipt_hash = verified["handoff_receipt_hash"]
    block_id = verified["block_id"]
    block_content_sha256 = verified["block_content_sha256"]

    def ev(address: str, source: str, method: str,
           failure_mode: str) -> Dict[str, Any]:
        return {
            "address": address,
            "source": source,
            "acquisition_method": method,
            "acquired_at": as_of,
            "qualified_oracle": True,
            "failure_mode": failure_mode,
            "independent_of_claim": True,
            "restates_claim": False,
            "provisional_until": None,
        }

    evidence = [
        ev("act-receipt:sha256:" + receipt_hash,
           "act-execution-receipt",
           "ActNode.recompute seal verification",
           "receipt-canonicalization-drift"),
        ev("artifact:sha256:" + artifact_sha256,
           "demo-staging-disk",
           "artifact bytes sha256 read-back",
           "disk-read-tamper-window"),
        ev("decision-receipt:sha256:" + handoff_receipt_hash,
           "kernel-decision-receipt",
           "verify_decision_receipt recompute",
           "decision-canonicalization-drift"),
        ev("know-block:sha256:" + block_content_sha256,
           "know-inmemory-store",
           "block read by provenance ref",
           "store-write-path-confusion"),
        ev("know-retrieval:sha256:" + block_content_sha256,
           "know-gated-retrieval",
           "admitted retrieval serve path",
           "retrieval-admission-bypass"),
    ]

    assertions = [
        {
            # A1 — observation: the execution happened.
            "text": (
                "ACT execution %s ran tool %s (path EXECUTED) at %s; "
                "act receipt sha256:%s."
            ) % (execution_id, tool_id, issued_at, receipt_hash),
            "evidence": ["act-receipt:sha256:" + receipt_hash],
        },
        {
            # A2 — outcome, as observed: exactly the bound bytes, re-read.
            "text": (
                "The execution wrote %s (%d bytes, sha256:%s); the bytes "
                "were re-observed on disk after the handoff and match the "
                "receipt's binding exactly."
            ) % (relpath, artifact_bytes, artifact_sha256),
            "evidence": ["artifact:sha256:" + artifact_sha256],
        },
        {
            # A3 — acceptance: KNOW took the observation through its gate.
            "text": (
                "KNOW accepted the observation: block %s ingested with "
                "ACTION_OUTCOME provenance act-execution:%s, KNOW gate PASS "
                "attested by handoff decision receipt sha256:%s, and the "
                "block served back through KNOW's gated retrieval."
            ) % (block_id, execution_id, handoff_receipt_hash),
            "evidence": [
                "know-block:sha256:" + block_content_sha256,
                "decision-receipt:sha256:" + handoff_receipt_hash,
                "know-retrieval:sha256:" + block_content_sha256,
            ],
        },
        {
            # A4 — causal limits: ACT success is not outcome success. The
            # claim stops at the bound bytes; nothing beyond them is
            # asserted, predicted, or implied.
            "text": (
                "Causal limit: this proof claims nothing beyond the bound "
                "artifact bytes of %s (sha256:%s). ACT success is execution "
                "success, not outcome success — no downstream effect, "
                "notification, or deployment is asserted."
            ) % (relpath, artifact_sha256),
            "evidence": ["act-receipt:sha256:" + receipt_hash],
        },
        {
            # A5 — learning eligibility: eligible for LEARN intake as a
            # single-execution EPHEMERAL observation. Eligibility is not a
            # learning claim — no behavior change is asserted.
            "text": (
                "The observation act-execution:%s is eligible for LEARN "
                "intake as one EPHEMERAL ACTION_OUTCOME observation "
                "(block %s). Eligibility asserts no learning, no behavior "
                "change, and no generalization."
            ) % (execution_id, block_id),
            "evidence": ["know-block:sha256:" + block_content_sha256],
        },
    ]

    return {
        "id": "demo1-prove-obs-%s" % str(execution_id)[:8],
        "class": "EMPIRICAL",
        "assertion": "post-action proof of the Demo-1 ACT->KNOW observation",
        "assertions": assertions,
        "evidence": evidence,
        "stakes": "low",
        "required_level": 2,
        "overturn_conditions": [
            "the act receipt seal fails recompute",
            "the artifact bytes on disk diverge from the bound sha256",
            "the handoff decision receipt seal fails recompute",
            "the KNOW block is missing or lacks the act-execution provenance ref",
            "an effect beyond the bound artifact bytes is observed",
        ],
        "observation_recorded_with_method": True,
        "raw_data_retained": True,
        "freshness_seconds": 7 * 24 * 3600,
        "as_of": as_of,
        # G5 — fresh re-derivation path: this module re-verified the chain
        # independently of the handoff module (code_path), and the record
        # can in principle disagree (a failed re-verify refuses before any
        # claim is built).
        "recompute": {
            "independence_dimension": "code_path",
            "can_disagree": True,
            "result": "MATCH",
        },
    }


def prove_observation(kernel,
                      handoff_result: Dict[str, Any],
                      act_receipt: Dict[str, Any],
                      *,
                      staging_root: str,
                      principal: Dict[str, Any],
                      gate_states: Dict[str, Any],
                      decision_id: Optional[str] = None,
                      now: Optional[str] = None) -> Dict[str, Any]:
    """Prove the handed-off KNOW observation through the kernel.

    1. ``verify_observation_chain`` — raises ``ProveObservationRefused``
       before PROVE is touched on any failure.
    2. Build the post-action claim from the verified facts only.
    3. Submit + advance on the kernel's PROVE node until the claim seals
       at its required level (low stakes: L2). Unsealed after the ladder
       is exhausted -> refuse.
    4. ``kernel.decide()`` with the PROVE sub-state carrying
       ``{claim, principal}`` — the kernel's PROVE gate must PASS.
    5. ``crossing_check`` — the sealed claim must be admitted to cross
       the CONNECT boundary; refusal here is fail-closed.

    Returns the decision receipt, the decided input state (for the seam's
    ``inputs_hash`` recompute), the claim id, the proof level, the sealed
    receipt id, the crossing verdict, and the verified facts. The caller
    projects the decision receipt through ``project_kernel_receipt``
    read-only; this function performs no I/O beyond reading the
    already-verified artifact bytes.
    """
    verified = verify_observation_chain(
        kernel, handoff_result, act_receipt, staging_root,
        principal=principal, now=now)
    claim = build_post_action_claim(verified, now=now)

    prove = kernel.nodes["PROVE"]
    submitted = prove.submit(claim, principal)
    claim_id = submitted["claim_id"]
    sealed = False
    level = 0
    receipt_id = submitted["receipt_id"]
    for _ in range(4):
        advanced = prove.advance(claim_id, principal=principal)
        level = advanced.get("level", level)
        receipt_id = advanced.get("receipt_id", receipt_id)
        if advanced.get("sealed"):
            sealed = True
            break
    if not sealed:
        raise ProveObservationRefused(
            f"proof refused for observation {verified['execution_id']}: "
            f"claim {claim_id} did not seal at its required level "
            f"(held at L{level})")

    gates = dict(gate_states)
    gates["PROVE"] = {"claim": claim, "operation": "intake"}
    state = {"decision_id": decision_id or
             "demo1-prove-obs-%s" % str(verified["execution_id"])[:8],
             "gates": gates}

    out = kernel.decide(state)
    decision_receipt = out["decision_receipt"]
    prove_gate = next((g for g in decision_receipt["gates"]
                       if g["node"] == "PROVE"), None)
    if prove_gate is None or prove_gate["verdict"] != "PASS":
        raise ProveObservationRefused(
            "proof refused: PROVE gate did not PASS: %s"
            % ((prove_gate or {}).get("reasons") or
               ["no PROVE gate record in decision"]))

    # CONNECT boundary: nothing unproven crosses.
    crossing = prove.crossing_check(claim_id)
    if not crossing.get("cross"):
        raise ProveObservationRefused(
            "proof refused: CONNECT crossing refused: %s"
            % crossing.get("reason"))

    return {
        "decision_receipt": decision_receipt,
        "input_state": state,
        "claim_id": claim_id,
        "claim": claim,
        "proof_level": level,
        "sealed_receipt_id": receipt_id,
        "prove_verdict": prove_gate["verdict"],
        "prove_gate_reasons": list(prove_gate["reasons"]),
        "crossing": crossing,
        "verified": verified,
        "observation": handoff_result.get("observation"),
        "block_id": handoff_result.get("block_id"),
    }
