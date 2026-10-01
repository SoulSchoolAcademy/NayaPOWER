"""NAYA-KERNEL-SELF — CANDIDATE implementation (NOT RATIFIED — NOT MERGED).

Implements the SELF node contract from SELF-NODE-SPEC-CANDIDATE.md (draft)
against the NodeBase interface. Candidate code on a feature branch: it proves
the spec is implementable; it grants nothing, merges nothing, deploys nothing.

Contractual responsibility (spec §0): SELF answers three questions before
anything else may happen — who is acting, under what identity and mission,
and what durable state may safely continue. Every pipeline cycle begins at
SELF; nothing downstream may execute until SELF reaches READY.

Gate input contract (`state` dict keys; all reads are explicit, nothing is
inferred):
  execution_id        unique per boot; replay detection key (§4.2)
  seen_execution_ids  registry of already-used execution IDs
  identity_claim      {"type": "NAYA"|"DIRECTOR"|"TOOL"|"DELEGATE", ...}
  identity_binding    {"binding_ref": str, "verified": bool, "actor_type": str}
                      — caller-supplied identity WITHOUT a verified binding is
                      untrusted (spec §1.1, master §10) → refusal §4.1
  identity_evidence_sources  list of signals offered as identity evidence;
                      any of the spec-excluded signals (§3.2) → refusal §4.6
  mission_ref / scope_ref    content-addressed refs; must resolve in
                      ratified_sources or §4.7 fires
  ratified_sources    {ref: content} — the ratified record (content-addressed)
  mission_ambiguous   bool — binding valid but mission ambiguous → recorded
                      in `unknown`, scope narrowed (§7 failure table)
  owner_scope         whose data this instance serves (consent boundary)
  checkpoint          {"hash": str, "payload": {...}, "owner_scope": str,
                       "superseded_by": str|None}
  predecessor_receipt {"receipt_hash": str, "checkpoint_hash": str,
                       "config_hash": str, "predecessor_hash": str|None, ...}
  receipt_chain       full chain head-wards, for fork detection (§4.2)
  successor_package   from EVOLVE; {"carries_authority": bool, ...} —
                      authority intact → REFUSED, never silently stripped (§4.5)
  genesis             {"ratified": bool, "first_execution_id": str} —
                      lawful first boot path (§10.1, §4.3, §4.4)
  kernel_revision / config_hash  config this instance runs under
  known / unknown / blocked      truth-boundary seeds (§2, §7)

Gate verdicts:
  PASS          READY (or DEGRADED — proceeds only with narrowed, explicitly
                flagged scope, §6)
  FAIL          FAILED/BLOCKED — pipeline halts before LAW; the refusal
                condition and its evidence are named in `reasons`
  NEED_EVIDENCE the gate cannot reach PASS on the evidence in `state` and
                must not silently become PASS
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from naya_kernel.node_base import GateResult, GateVerdict, ManifestEntry, NodeBase
from naya_kernel.nodes.evolve_node import package_hash as _successor_seal

NODE_ID = "NAYA-KERNEL-SELF"
NODE_VERSION = "0.1.0-candidate"
PIPELINE_POSITION = 1

# Master invariant (spec §3.2): these signals are EXCLUDED as identity or
# ownership evidence. None of them appear in IdentityContext, none satisfy a
# refusal condition, none can substitute for the four continuity items (§3.1).
EXCLUDED_IDENTITY_SIGNALS = frozenset({
    "name_similarity",
    "chat_text_possession",
    "browser_state",
    "timing",
    "object_id",
    "usefulness",
})

# §10.3 draft: fail closed to the minimum named in the ratified scope.
MINIMUM_VIABLE_SCOPE = {
    "actions": [],
    "note": "minimum viable scope: identity continuity only; "
            "no consequential action permitted",
}


def _canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def _sha256(obj: Any) -> str:
    return hashlib.sha256(_canonical(obj).encode("utf-8")).hexdigest()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _deepcopy_json(obj: Any) -> Any:
    return json.loads(_canonical(obj))


def _hash_content(receipt: Dict[str, Any]) -> Dict[str, Any]:
    """Canonical content covered by a boot receipt's hash.

    Covers everything except ``receipt_hash`` itself, with
    ``identityContext.boot_receipt_id`` normalized to None (it is sealed to
    the receipt_hash after hashing; see _build_receipt).
    """
    content = {k: v for k, v in receipt.items() if k != "receipt_hash"}
    identity_context = dict(content.get("identityContext") or {})
    identity_context["boot_receipt_id"] = None
    content["identityContext"] = identity_context
    return content


class SelfNode(NodeBase):
    """NAYA-KERNEL-SELF. Boot-time identity, mission, and continuity gate."""

    def __init__(self) -> None:
        self.machine_state = "UNINITIALIZED"
        self.last_boot_receipt: Optional[Dict[str, Any]] = None

    # ------------------------------------------------------------------
    # NodeBase interface
    # ------------------------------------------------------------------
    def manifest_entry(self) -> ManifestEntry:
        """Return this node's manifest entry (candidate spec, §9 acceptance battery)."""
        return ManifestEntry(
            node_id=NODE_ID,
            version=NODE_VERSION,
            responsibilities=[
                "establish actor identity via authenticated binding "
                "(never from names, similarity, or claims)",
                "re-establish mission and scope from ratified, "
                "content-addressed sources at every boot",
                "verify checkpoint integrity (hash-bound) and the "
                "unbroken continuity receipt chain (all four §3.1 items)",
                "classify known / unknown / blocked (truth boundary) "
                "as a first-class, receipted output",
                "emit the typed boot receipt; fail closed (never proceed "
                "to LAW except from READY or explicitly flagged DEGRADED)",
                "refuse authority inheritance, ownership inference, and "
                "cross-owner leakage loudly with receipted evidence",
            ],
        )

    def gate(self, state: Dict[str, Any]) -> GateResult:
        """Run the SELF boot sequence; return PASS/FAIL/NEED_EVIDENCE.

        Implements the §2 sync boot order and the §4 refusal conditions.
        Fail-fast: the first refusal halts the boot and names its evidence.
        """
        inputs = _deepcopy_json(state)
        transitions: List[Dict[str, Any]] = []
        execution_id = inputs.get("execution_id")

        def transition(to_state: str, reason: str,
                       evidence: Optional[List[str]] = None) -> None:
            entry = {
                "before": self.machine_state,
                "after": to_state,
                "reason": reason,
                "execution_id": execution_id,
                "evidence_refs": evidence or [],
                "at": _now_iso(),
            }
            transitions.append(entry)
            self.machine_state = to_state

        transition("BOOTING", "boot begins (spec §6)")

        def refuse(condition: str, detail: str,
                  evidence: Optional[List[str]] = None) -> GateResult:
            transition("FAILED", f"{condition}: {detail}", evidence)
            receipt = self._build_receipt(
                inputs, transitions, "FAILED", None, None, None, None, None,
            )
            self.last_boot_receipt = receipt
            return GateResult(
                verdict=GateVerdict.FAIL,
                reasons=[f"SELF refuses — {condition} (§4). {detail}"],
            )

        # §4.2 (replay): without an execution_id, replay detection is
        # impossible — the boot cannot be receipted, so it cannot proceed.
        if not execution_id:
            return refuse("missing execution_id",
                          "replay detection impossible; boot unreceiptable")

        if execution_id in inputs.get("seen_execution_ids", []):
            return refuse("replayed execution_id",
                          f"execution_id {execution_id!r} already used; "
                          "the replay changes nothing (§7)")

        # §4.1: unauthenticated identity. Names are claims; bindings are proof.
        binding = inputs.get("identity_binding") or {}
        if not binding.get("verified") or not binding.get("binding_ref"):
            return refuse("unauthenticated identity (§4.1)",
                          "caller-supplied identity arrived without an "
                          "authenticated binding")

        # §4.2: identity conflict — claim inconsistent with binding.
        claim = inputs.get("identity_claim") or {}
        binding_actor = binding.get("actor_type")
        if binding_actor and claim.get("type") and binding_actor != claim["type"]:
            return refuse("identity conflict (§4.2)",
                          f"claimed type {claim['type']!r} != binding actor "
                          f"{binding_actor!r}; never 'pick the more plausible'")

        # §4.2: forked continuity chain — two successors, one predecessor.
        fork = self._detect_fork(inputs.get("receipt_chain", []))
        if fork:
            return refuse("forked continuity chain (§4.2)",
                          f"two receipts share predecessor {fork!r}; both "
                          "halt, resolution is director-owned (§10.2)")

        # §4.6: ownership/identity inference from excluded signals.
        excluded = [s for s in inputs.get("identity_evidence_sources", [])
                    if s in EXCLUDED_IDENTITY_SIGNALS]
        if excluded:
            return refuse("ownership inference (§4.6)",
                          f"excluded identity signals offered as evidence: "
                          f"{sorted(excluded)}; the attempt is receipted")

        # §4.4: broken continuity chain — all four §3.1 items or lawful genesis.
        predecessor = inputs.get("predecessor_receipt")
        genesis = inputs.get("genesis") or {}
        genesis_boot = False
        if predecessor is None:
            if (genesis.get("ratified")
                    and execution_id == genesis.get("first_execution_id")):
                genesis_boot = True
            else:
                return refuse(
                    "broken continuity chain (§4.4)",
                    "no predecessor receipt and no ratified re-genesis; "
                    "the chain is the identity")
        else:
            if not self._verify_receipt_hash(predecessor):
                return refuse("broken continuity chain (§4.4)",
                              "predecessor receipt hash does not recompute; "
                              "the receipt is unverifiable")

        # §4.5: authority inheritance attempt — refuse the package, never
        # silently strip it (silent repair is itself an authority decision,
        # and SELF makes none).
        package = inputs.get("successor_package")
        if package and package.get("carries_authority"):
            return refuse("authority inheritance attempt (§4.5)",
                          "successor package carries authority forward; "
                          "strip_inherited_authority violated — refused, "
                          "not cleaned")

        # §4.8: cross-owner leakage — critical failure: halt, name it, notify.
        owner_scope = inputs.get("owner_scope")
        for source, label in ((inputs.get("checkpoint"), "checkpoint"),
                              (package, "successor_package")):
            src_owner = (source or {}).get("owner_scope")
            if src_owner and owner_scope and src_owner != owner_scope:
                return refuse(
                    "cross-owner leakage (§4.8)",
                    f"{label} belongs to owner_scope {src_owner!r}, "
                    f"instance serves {owner_scope!r}; owner boundaries "
                    f"are identity boundaries — notify")

        # §5.2/A5: successor package seal integrity. EVOLVE seals the
        # package with package_hash = H_S over the canonical body; a
        # material mutation creates a new version, never a silent edit.
        # The seal must recompute before any package content is trusted
        # downstream: a tampered (or seal-less) package is refused as
        # predecessor intelligence, never booted on. Placed after §4.5/§4.8
        # so their existing refusal reasons are preserved; every mutation
        # breaks the seal, so the seal is the backstop either way. A
        # missing package (genesis or package-less boot) is unaffected.
        if package is not None:
            sealed = package.get("package_hash")
            if not sealed or _successor_seal(package) != sealed:
                return refuse(
                    "successor package seal failure (§5.2/A5)",
                    "package_hash does not recompute over the package body; "
                    "the package was mutated after sealing (or carries no "
                    "seal) — refused as predecessor intelligence, never "
                    "booted on")

        # §4.3: checkpoint integrity. Hash mismatch → refused, never degraded.
        checkpoint = inputs.get("checkpoint")
        checkpoint_hash: Optional[str] = None
        stale_checkpoint = False
        if checkpoint is None:
            if not genesis_boot:
                return refuse("checkpoint integrity failure (§4.3)",
                              "missing checkpoint with no lawful genesis path")
        else:
            claimed = checkpoint.get("hash")
            recomputed = _sha256(checkpoint.get("payload"))
            if not claimed or claimed != recomputed:
                return refuse("checkpoint integrity failure (§4.3)",
                              "loaded checkpoint hash does not recompute; "
                              "a corrupt checkpoint is refused, not degraded")
            expected = (predecessor or {}).get("checkpoint_hash")
            if expected and claimed != expected:
                return refuse(
                    "checkpoint integrity failure (§4.3)",
                    "checkpoint hash != predecessor's emitted checkpoint "
                    "hash; there is no 'close enough' in identity")
            checkpoint_hash = claimed
            if checkpoint.get("superseded_by"):
                # Valid hash but superseded: explicitly stale — treated as
                # unknown, never as current (§7).
                stale_checkpoint = True

        # §4.7: mission/scope must trace to ratified, content-addressed
        # sources. Mission unratified → refuse. Scope unratified → fail
        # closed to the minimum viable (§10.3), DEGRADED, never widened.
        ratified = inputs.get("ratified_sources") or {}
        mission_ref = inputs.get("mission_ref")
        scope_ref = inputs.get("scope_ref")
        if not mission_ref or mission_ref not in ratified:
            return refuse("mission from unratified source (§4.7)",
                          f"mission_ref {mission_ref!r} does not resolve to "
                          "a ratified content-addressed source")
        degraded_reasons: List[str] = []
        effective_scope: Any = ratified.get(scope_ref)
        if not scope_ref or scope_ref not in ratified:
            degraded_reasons.append(
                "scope_ref does not resolve to a ratified source — scope "
                "narrowed to the minimum viable (§4.7, §10.3); "
                "DEGRADED still halts consequential action")
            effective_scope = _deepcopy_json(MINIMUM_VIABLE_SCOPE)
        if inputs.get("mission_ambiguous"):
            # Binding valid but mission ambiguous: ambiguity is recorded in
            # `unknown` and scope is narrowed — never resolved by guessing.
            degraded_reasons.append(
                "mission ambiguous despite valid binding — ambiguity "
                "recorded in `unknown`, scope narrowed (§7)")
            effective_scope = _deepcopy_json(MINIMUM_VIABLE_SCOPE)

        # Truth boundary (§2, §7): unknown is a respectable, receipted state.
        known = list(inputs.get("known", []))
        unknown = list(inputs.get("unknown", []))
        blocked = list(inputs.get("blocked", []))
        if stale_checkpoint:
            unknown.append("checkpoint_content: superseded, treated as unknown")
        if inputs.get("mission_ambiguous"):
            unknown.append("mission: binding valid but mission ambiguous")
        truth_boundary = {"known": known, "unknown": unknown, "blocked": blocked}

        # Identity context (§2) — the handoff to LAW.
        identity_context = {
            "node_id": NODE_ID,
            "execution_id": execution_id,
            "kernel_revision": inputs.get("kernel_revision"),
            "actor": {
                "type": claim.get("type", binding_actor),
                "authenticated": True,
                "binding_ref": binding.get("binding_ref"),
            },
            "mission_ref": mission_ref,
            "scope_ref": scope_ref,
            "owner_scope": owner_scope,
            "predecessor_binding": (predecessor or {}).get("receipt_hash"),
            "checkpoint_ref": checkpoint_hash,
            "truth_boundary": truth_boundary,
            "boot_receipt_id": None,  # filled after the receipt is hashed
        }

        boot_state = "DEGRADED" if degraded_reasons else "READY"
        transition(boot_state,
                   "all §2 sync functions pass"
                   + ("; " + "; ".join(degraded_reasons) if degraded_reasons
                      else ""))

        receipt = self._build_receipt(
            inputs, transitions, boot_state, identity_context, truth_boundary,
            checkpoint_hash, effective_scope, degraded_reasons,
        )
        # boot_receipt_id is sealed inside _build_receipt (hash-bound).
        self.last_boot_receipt = receipt

        reasons = [f"SELF {boot_state}: identity authenticated, mission "
                   f"re-established from ratified source {mission_ref!r}, "
                   f"continuity verified (genesis={genesis_boot})"]
        reasons.extend(f"DEGRADED: {r}" for r in degraded_reasons)
        return GateResult(verdict=GateVerdict.PASS, reasons=reasons)

    def persisted_transitions(self) -> List[str]:
        """Every state transition this node persists (receipted).

        Spec §5 — typed boot receipt transition log."""
        return [
            "UNINITIALIZED->BOOTING",
            "BOOTING->READY",
            "BOOTING->DEGRADED",
            "BOOTING->FAILED",
            "BOOTING->BLOCKED",
            "boot_receipt_issued",
            "continuity_write",          # async preserve_continuity (§2)
            "successor_context_assembled",  # async prepare_successor_context
        ]

    def evidence_hooks(self) -> List[str]:
        """Evidence sources this node reads/writes.

        Spec §5 — boot receipt evidence bindings."""
        return [
            "identity_binding_registry",   # read: authenticate_identity
            "ratified_source_store",       # read: establish_mission/scope
            "checkpoint_store",            # read: load_checkpoint
            "continuity_receipt_chain",    # read: preserve_continuity chain
            "execution_id_registry",       # read/write: replay detection
            "boot_receipt_log",            # write: typed boot receipts (§5)
        ]

    def authority_checks(self) -> List[str]:
        """Authority validations SELF performs before acting.

        SELF never grants authority (master invariant, §1.3); it declares the
        authority boundary and LAW validates it. These are checks, not grants.
        """
        return [
            "strip_inherited_authority_verified",   # §4.5: refuse, not strip
            "authority_boundary_declared_not_granted",  # §1.2: LAW validates
            "owner_scope_isolation_checked",        # §4.8: no cross-owner state
            "no_authority_grant_performed",        # invariant: never in SELF's
                                                  # vocabulary
        ]

    def cold_reconstruct(self, receipts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Rebuild SELF's durable state from receipts alone (§8).

        Ordered procedure; every step's inputs are content-addressed and named
        in the receipt; no step draws on private or unrecorded sources. The
        determinism check (§3.3) is enforced: same inputs must reach the same
        state, or the chain is defective and reconstruction FAILS.
        """
        if not receipts:
            return {"status": "FAILED",
                    "reasons": ["§8.1: no receipts — successor package, "
                                "receipt chain, and ratified sources are all "
                                "unavailable; stop here"]}

        receipt = receipts[-1]  # latest boot receipt
        if not self._verify_receipt_hash(receipt):
            return {"status": "FAILED",
                    "reasons": ["receipt hash does not recompute — defective "
                                "provenance; the boot it describes is not "
                                "trusted (§5)"]}

        recorded_state = receipt.get("boot_state")
        if recorded_state in ("FAILED", "BLOCKED"):
            return {"status": "FAILED",
                    "reasons": [f"boot receipt records {recorded_state}; a "
                                "cold successor does not proceed from a "
                                "failed boot (§8)"]}

        inputs = receipt.get("inputs")
        if not inputs:
            return {"status": "FAILED",
                    "reasons": ["§8: receipt names no inputs — hidden "
                                "reconstruction is not permitted (§3.3)"]}

        # Determinism check (§3.3): a second cold instance given the same
        # inputs must reach the same READY/DEGRADED state.
        replay = SelfNode().gate(inputs)
        replay_state = ("READY" if replay.verdict == GateVerdict.PASS
                        and not any(r.startswith("DEGRADED")
                                    for r in replay.reasons)
                        else "DEGRADED" if replay.verdict == GateVerdict.PASS
                        else "FAILED")
        if replay.verdict != GateVerdict.PASS or replay_state != recorded_state:
            return {"status": "FAILED",
                    "reasons": [f"determinism check failed: same inputs "
                                f"reached {replay_state}, receipt records "
                                f"{recorded_state} (§3.3)"]}

        return {
            "status": recorded_state,  # READY or DEGRADED
            "identity_context": receipt.get("identityContext"),
            "truth_boundary": receipt.get("truth_boundary"),
            "continuity": {
                "predecessor_binding_hash":
                    receipt.get("predecessor_binding_hash"),
                "checkpoint_hash": receipt.get("checkpoint_hash"),
                "config_hash": receipt.get("config_hash"),
            },
            "reasons": [f"cold reconstruction from receipt "
                        f"{receipt.get('receipt_hash')} (§8); determinism "
                        f"check MATCH"],
        }

    # ------------------------------------------------------------------
    # Boot receipt (§5) and the cold-successor recompute test
    # ------------------------------------------------------------------
    def recompute(self, boot_receipt: Dict[str, Any]) -> str:
        """Recompute the boot decision from the receipt's inputs (§5).

        An independent cold instance given the receipt and its referenced
        inputs must recompute the boot decision exactly → MATCH. A receipt
        that cannot be recomputed is defective provenance.
        """
        inputs = (boot_receipt or {}).get("inputs")
        if not inputs:
            return "MISMATCH"
        if not self._verify_receipt_hash(boot_receipt):
            return "MISMATCH"
        result = SelfNode().gate(inputs)
        recorded = boot_receipt.get("boot_state")
        reached = ("READY" if result.verdict == GateVerdict.PASS
                   and not any(r.startswith("DEGRADED") for r in result.reasons)
                   else "DEGRADED" if result.verdict == GateVerdict.PASS
                   else "FAILED")
        return "MATCH" if reached == recorded else "MISMATCH"

    def _build_receipt(self, inputs: Dict[str, Any],
                       transitions: List[Dict[str, Any]],
                       boot_state: str,
                       identity_context: Optional[Dict[str, Any]],
                       truth_boundary: Optional[Dict[str, Any]],
                       checkpoint_hash: Optional[str],
                       effective_scope: Any,
                       degraded_reasons: Optional[List[str]]) -> Dict[str, Any]:
        predecessor = inputs.get("predecessor_receipt") or {}
        binding = inputs.get("identity_binding") or {}
        config_hash = inputs.get("config_hash") or _sha256(
            {"kernel_revision": inputs.get("kernel_revision")})
        receipt = {
            "node_id": NODE_ID,
            "node_version": NODE_VERSION,
            "boot_state": boot_state,
            "identityContext": identity_context or {},
            "predecessor_binding_hash": predecessor.get("receipt_hash"),
            "checkpoint_hash": checkpoint_hash,
            "config_hash": config_hash,
            "mission_ref": inputs.get("mission_ref"),
            "scope_ref": inputs.get("scope_ref"),
            "effective_scope": effective_scope,
            "degraded_reasons": degraded_reasons or [],
            "truth_boundary": truth_boundary or {"known": [], "unknown": [],
                                                 "blocked": []},
            "transition_log": transitions,
            "async_receipts": [],  # preserve_continuity / prepare_successor_
                                   # context emit their own receipts at runtime
            "issued_at": _now_iso(),
            "issued_by": binding.get("binding_ref"),
            "owner_scope": inputs.get("owner_scope"),
            "inputs": inputs,  # every input named; no hidden reconstruction
        }
        receipt["receipt_hash"] = _sha256(_hash_content(receipt))
        # Seal the cross-reference AFTER the hash is computed; verification
        # normalizes boot_receipt_id back to None before recomputing, so the
        # seal is tamper-evident, not tamper-creating.
        receipt["identityContext"]["boot_receipt_id"] = receipt["receipt_hash"]
        return receipt

    @staticmethod
    def _verify_receipt_hash(receipt: Dict[str, Any]) -> bool:
        claimed = (receipt or {}).get("receipt_hash")
        if not claimed:
            return False
        identity_context = receipt.get("identityContext")
        if isinstance(identity_context, dict):
            # A SELF boot receipt: the seal binds boot_receipt_id to the
            # receipt hash, and the hash covers the normalized content.
            if identity_context.get("boot_receipt_id") != claimed:
                return False
            content = _hash_content(receipt)
        else:
            # A continuity/predecessor receipt (different type): plain
            # hash check over everything but the hash itself.
            content = {k: v for k, v in receipt.items()
                       if k != "receipt_hash"}
        return _sha256(content) == claimed

    @staticmethod
    def _detect_fork(chain: List[Dict[str, Any]]) -> Optional[str]:
        """Two receipts sharing one predecessor = forked chain (§4.2).

        The root slot (predecessor_hash None) counts too: two distinct
        genesis receipts are two claimants for one identity — both halt,
        resolution is director-owned (§10.2).
        """
        seen: Dict[Any, str] = {}
        for r in chain or []:
            pred = r.get("predecessor_hash")  # None = the root slot
            rh = r.get("receipt_hash")
            if rh is None:
                continue
            if pred in seen and seen[pred] != rh:
                return "genesis" if pred is None else str(pred)
            seen[pred] = rh
        return None
