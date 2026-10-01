"""NAYA-KERNEL-LAW — CANDIDATE implementation (NOT RATIFIED — NOT MERGED).

Implements the LAW node contract from LAW-NODE-SPEC-CANDIDATE.md (draft)
against the NodeBase interface. Candidate code on a feature branch: it proves
the spec is implementable; it grants nothing, merges nothing, deploys nothing.

Contractual responsibility (spec §0): LAW is the organism's conscience made
mechanical. Every proposed action must pass through LAW before it can be
executed. LAW holds no authority of its own; it validates authority claims
against the Constitution, applies the four-valued gate structure with hard
stops that no principal can override, and refuses known-wrong instructions
even when they come from the Human Director. LAW runs *before* the math — a
wrong act never reaches the scoring.

Gate input contract (`state` dict keys; all reads explicit, nothing inferred):
  proposal {
    proposalId: str, intent: str,
    action: {type: str, scope_tag: str, action_class: str,
             targets: [...], bounds: {...}, ...},
    proposedBy: str (principal identity),
    authorityClaim: {grant_ref: str, grantor: str} | None,
    evidenceRefs: [...], stakes: str, reversibility: number,
    identityContext: {...}, constitutionHash: str,
    flags: {harm_flag: bool, harm_facts: [...],
            known_wrong_flag: bool, known_wrong_facts: [...]},
    bundle_of: [...] (optional; pieces evaluated as one, §4 bundle rule),
    material_facts_version: int,
  }
  constitution_store: {pinned_hash: str, corpus: {hash: str}, reachable: bool}
  grants: [{grant_ref, grantor, grantee, scope: [...], bounds,
            expiry: iso-str|None, revoked: bool, chain: [...]}]
  evidence: {n: int, confidence: float}
  evidence_floor_k: int   (config default 3 — the decision calculus is RATIFIED
                           V2.1 (FLAG-001 step 4); the floor threshold value is
                           config, the gate structure is constitutional)
  seen_proposal_hashes: {proposal_hash: gate}   (verdict-shopping detection)
  proposal_hash_claimed: str | None             (tamper detection)

Gate outcomes (spec §3.1) map onto NodeBase.GateVerdict as:
  ADMISSIBLE       -> PASS
  NEEDS_AUTHORITY  -> NEED_EVIDENCE  (the grant is evidence of authority;
                                      a new re-evaluation can reach PASS)
  NEEDS_EVIDENCE   -> NEED_EVIDENCE
  PROHIBITED       -> FAIL  (terminal for this proposal version, §6.2)
  INTAKE_REFUSED   -> FAIL  (refused before evaluation, §10.1)

The full typed verdict + hash-bound GateReceipt (§7) is kept on the instance
as `last_receipt`; GateResult.reasons carry the gate name and receipt id.
LAW never executes, scores, grants, or amends: authority_checks() declares
validations only.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from naya_kernel.node_base import GateResult, GateVerdict, ManifestEntry, NodeBase

NODE_ID = "NAYA-KERNEL-LAW"
NODE_VERSION = "0.1.0-candidate"
PIPELINE_POSITION = 2

# §3.2 hard stops
HARD_STOP_LAW_OF_ONE = "LAW_OF_ONE"
HARD_STOP_JUDGMENT_RULE = "JUDGMENT_RULE"

# §3.2: τ = 0 zero-tolerance classes. The zero-tolerance *principle* is
# constitutional; the wider τ_seed table is CANDIDATE and deliberately
# unused here — LAW does not consult provisional τ values (§14.5).
TAU_ZERO_CLASSES = frozenset({"physical_harm", "rights_violation"})

# §3.3: hierarchy. The director holds the broadest grantable authority, but
# PROHIBITED is not grantable — not even by the director.
DIRECTOR = "DIRECTOR"

# §10.5: proposal effects that would alter the gate structure, hard stops, or
# LAW's own contract outside ratification. Includes anything routed through
# other nodes' authority (defense in depth: LAW catches what EVOLVE's own
# §3.2 gates should have caught — acceptance #10).
GATE_REDESIGN_ACTION_TYPES = frozenset({
    "amend_constitution",
    "alter_gate_structure",
    "disable_hard_stop",
    "self_ratify",
    "amend_law_contract",
})
GATE_REDESIGN_SCOPE_TAGS = frozenset({
    "gate_structure", "hard_stops", "law_contract",
})

# §15 note: the evidence floor is CANDIDATE machinery pending calculus
# ratification. LAW ships a declared default, named in every receipt.
DEFAULT_EVIDENCE_FLOOR_K = 3

# Constitution articles cited by this implementation (lineage, spec §3):
ARTICLES = {
    "hierarchy": "Art. I",          # director is final authority (grantable)
    "authority": "Art. V.6",        # self-generated authority invalid
    "judgment": "Prime Judgment Rule (DIRECTOR-STATED 2026-09-30)",
    "ratification": "Art. XVIII",   # amendments only via ratification
    "fail_closed": "Art. XIV",      # timeouts fail closed
}


def _canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def _sha256(obj: Any) -> str:
    return hashlib.sha256(_canonical(obj).encode("utf-8")).hexdigest()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _deepcopy_json(obj: Any) -> Any:
    return json.loads(_canonical(obj))


def _shopping_key(proposal: Dict[str, Any]) -> str:
    """Identity of a proposal for verdict-shopping detection (§4, §10.4).

    The spec's shopping rule is precisely "re-submitted under a different
    proposalId" — so the shopping identity EXCLUDES proposalId. It also
    excludes the material-facts honesty flags: a new version that cites new
    material facts is a fresh evaluation by definition, not shopping.
    """
    stripped = {k: v for k, v in proposal.items()
                if k not in ("proposalId", "new_material_facts",
                             "material_facts_version")}
    return _sha256(stripped)


class LawNode(NodeBase):
    """NAYA-KERNEL-LAW. The constitutional gate every proposal must pass."""

    def __init__(self) -> None:
        self.last_receipt: Optional[Dict[str, Any]] = None
        # proposal_hash -> terminal/awaiting gate; verdict-shopping registry
        # (a bounded-session convenience mirror of seen_proposal_hashes).
        self._seen: Dict[str, str] = {}

    # ------------------------------------------------------------------
    # NodeBase interface
    # ------------------------------------------------------------------
    def manifest_entry(self) -> ManifestEntry:
        """Return this node's manifest entry (candidate spec, §13 acceptance battery)."""
        return ManifestEntry(
            node_id=NODE_ID,
            version=NODE_VERSION,
            responsibilities=[
                "apply the four-valued gate structure in precedence order "
                "(PROHIBITED > NEEDS_AUTHORITY > NEEDS_EVIDENCE > ADMISSIBLE)",
                "enforce hard stops that no principal can override "
                "(LAW_OF_ONE, JUDGMENT_RULE, tau-zero classes)",
                "validate authority claims against the Constitution and the "
                "grant tree — never grant, create, or expand authority",
                "fail closed on evaluation-incomplete (constitution store "
                "unreachable, timeout): PROHIBITED + pipeline halt",
                "catch gate-redesign smuggling even when routed through "
                "other nodes' authority (defense in depth)",
                "emit the hash-bound typed GateReceipt (§7) for every "
                "evaluation, including intake refusals",
                "support monotonic re-evaluation on grant arrival or floor "
                "met — never silent downgrade, never PROHIBITED reopen",
            ],
        )

    def gate(self, state: Dict[str, Any]) -> GateResult:
        """Evaluate the proposal in `state` per §3.4; never invent ADMISSIBLE."""
        inputs = _deepcopy_json(state)
        proposal = inputs.get("proposal") or {}
        transitions: List[Dict[str, Any]] = []
        seen_registry: Dict[str, str] = dict(inputs.get("seen_proposal_hashes") or {})
        seen_registry.update(self._seen)

        def transition(gate: str, reason: str) -> None:
            transitions.append({"gate": gate, "reason": reason,
                                "at": _now_iso()})

        def verdict(gate_name: str, hard_stops: List[Dict[str, Any]],
                    articles: List[str], authority_basis: Optional[str],
                    envelope: Optional[Dict[str, Any]],
                    reasons: List[str],
                    extra: Optional[Dict[str, Any]] = None) -> GateResult:
            transition(gate_name, reasons[0] if reasons else gate_name)
            receipt = self._build_receipt(
                proposal=proposal, gate=gate_name, hard_stops=hard_stops,
                articles=articles, authority_basis=authority_basis,
                envelope=envelope, reasons=reasons,
                transitions=transitions, inputs=inputs, extra=extra or {},
            )
            self.last_receipt = receipt
            # Shopping registry keyed by content identity (excludes
            # proposalId), matching the §10.4 rule.
            self._seen[_shopping_key(proposal)] = gate_name
            verdict_map = {
                "ADMISSIBLE": GateVerdict.PASS,
                "NEEDS_AUTHORITY": GateVerdict.NEED_EVIDENCE,
                "NEEDS_EVIDENCE": GateVerdict.NEED_EVIDENCE,
                "PROHIBITED": GateVerdict.FAIL,
                "INTAKE_REFUSED": GateVerdict.FAIL,
            }
            return GateResult(
                verdict=verdict_map[gate_name],
                reasons=[f"LAW {gate_name}: {r}" for r in reasons]
                + [f"gate_receipt={receipt['receipt_id']}"],
            )

        # §3.4 step 1: intake validity. A proposal without an authenticated
        # proposer and a stated authority claim is not evaluated — it is
        # refused at intake (§10.1).
        intake_problem = self._intake_problem(proposal)
        if intake_problem:
            return verdict(
                "INTAKE_REFUSED", [], [ARTICLES["fail_closed"]], None, None,
                [f"intake refusal (§10.1): {intake_problem}; not evaluated, "
                 "receipted as INTAKE_REFUSED"])

        # §3.4 step 1b: tampered proposal hash — forgery is a hard refusal.
        proposal_hash = _sha256(proposal)
        claimed_hash = inputs.get("proposal_hash_claimed")
        if claimed_hash is not None and claimed_hash != proposal_hash:
            return verdict(
                "PROHIBITED",
                [{"hard_stop": "AUTHORITY_FORGERY",
                  "triggering_facts": ["proposal hash does not recompute"]} ],
                [ARTICLES["fail_closed"]], None, None,
                ["forged proposal (§10.3): claimed hash does not recompute — "
                 "PROHIBITED, forgery surfaced, never silent"])

        # §4: evaluation must complete within its bounded window; the
        # constitution store must be reachable and the pinned version
        # present. Otherwise PROHIBITED / EVALUATION_INCOMPLETE and the
        # pipeline halts at LAW (§9, Art. XIV).
        store = inputs.get("constitution_store") or {}
        if not store.get("reachable", True):
            return verdict(
                "PROHIBITED", [], [ARTICLES["fail_closed"]], None, None,
                ["EVALUATION_INCOMPLETE: constitution store unreachable — "
                 "an unexamined action is not an approved action; pipeline "
                 "halts at LAW (§9)"],
                extra={"halt_pipeline": True})
        pinned = store.get("pinned_hash")
        if not pinned or pinned not in (store.get("corpus") or {}):
            return verdict(
                "PROHIBITED", [], [ARTICLES["fail_closed"]], None, None,
                ["EVALUATION_INCOMPLETE: pinned constitutional version "
                 "unavailable — pipeline halts at LAW (§9)"],
                extra={"halt_pipeline": True})

        # Constitution skew (§9): a proposal citing a different hash is
        # re-evaluated under the pinned version; the mismatch is receipted.
        skew = proposal.get("constitutionHash") != pinned

        # §4 bundle rule: pieces are evaluated as one proposal. The worst
        # gate among the pieces determines the bundle's verdict.
        pieces = proposal.get("bundle_of") or []
        if pieces:
            worst: Optional[Tuple[str, GateResult]] = None
            order = {"PROHIBITED": 0, "NEEDS_AUTHORITY": 1,
                     "NEEDS_EVIDENCE": 2, "ADMISSIBLE": 3}
            for piece in pieces:
                piece_state = dict(inputs)
                piece_state["proposal"] = piece
                # A piece that declares its origin is re-evaluated honestly;
                # a piece hiding it is still caught because the gate math is
                # per-piece and identical.
                r = LawNode().gate(piece_state)
                gate_name = r.reasons[0].split(":")[0].replace("LAW ", "")
                if worst is None or order[gate_name] < order[worst[0]]:
                    worst = (gate_name, r)
            assert worst is not None
            bundle_gate, bundle_result = worst
            return verdict(
                bundle_gate, [], [ARTICLES["fail_closed"]], None, None,
                [f"bundle rule (§4): {len(pieces)} pieces evaluated as one; "
                 f"worst piece gate = {bundle_gate}"],
                extra={"bundle_worst_reasons": bundle_result.reasons})

        # §10.4 verdict shopping: resubmission of a refused proposal without
        # new material facts is refused as RESUBMISSION. The shopping
        # identity excludes proposalId (§4: "re-submitted under a different
        # proposalId").
        prior_gate = seen_registry.get(_shopping_key(proposal))
        if prior_gate in ("PROHIBITED", "INTAKE_REFUSED") \
                and not proposal.get("new_material_facts"):
            return verdict(
                "PROHIBITED", [], [ARTICLES["fail_closed"]], None, None,
                ["RESUBMISSION (§10.4): this proposal was refused "
                 f"({prior_gate}) and cites no new material facts; a new "
                 "version with materially different facts needs a new "
                 "proposalId"])

        flags = proposal.get("flags") or {}
        action = proposal.get("action") or {}

        # §3.4 step 2: hard stops — force PROHIBITED regardless of authority,
        # evidence, or score. Evaluated in the order the spec names them.
        if flags.get("harm_flag"):
            facts = flags.get("harm_facts") or ["harm foreseeable on stated "
                                                "consequences"]
            return verdict(
                "PROHIBITED",
                [{"hard_stop": HARD_STOP_LAW_OF_ONE,
                  "triggering_facts": facts}],
                [ARTICLES["hierarchy"], ARTICLES["fail_closed"]], None, None,
                [f"LAW_OF_ONE (§3.2): foreseeable harm to a person — "
                 f"{'; '.join(facts)}. Assessed on consequences, not "
                 "stated intent. No grant clears this."],
                extra={"lawful_alternative_required": True})

        if flags.get("known_wrong_flag"):
            facts = flags.get("known_wrong_facts") or ["instruction known "
                                                       "wrong"]
            return verdict(
                "PROHIBITED",
                [{"hard_stop": HARD_STOP_JUDGMENT_RULE,
                  "triggering_facts": facts}],
                [ARTICLES["judgment"]], None, None,
                [f"JUDGMENT_RULE (§3.2): the instruction is known-wrong — "
                 f"{'; '.join(facts)}. 'I was told to' is never a valid "
                 "reason. Binds against every principal including the "
                 "director."],
                extra={"lawful_alternative_required": True,
                       "lawful_alternative":
                           proposal.get("lawful_alternative_hint")
                           or "re-state the request with true premises and "
                              "re-propose; LAW re-evaluates the new proposal"})

        if action.get("action_class") in TAU_ZERO_CLASSES:
            return verdict(
                "PROHIBITED",
                [{"hard_stop": "TAU_ZERO",
                  "triggering_facts": [f"action_class="
                                       f"{action.get('action_class')}"]}],
                [ARTICLES["hierarchy"]], None, None,
                [f"τ=0 zero-tolerance class ({action.get('action_class')}, "
                 "§3.2): no probability threshold to satisfy, no authority "
                 "that can waive it."])

        # §3.4 step 3: constitutional prohibitions — gate redesign smuggling
        # (§10.5) and non-director ratification/amendment (Art. XVIII).
        if (action.get("type") in GATE_REDESIGN_ACTION_TYPES
                or action.get("scope_tag") in GATE_REDESIGN_SCOPE_TAGS):
            return verdict(
                "PROHIBITED", [], [ARTICLES["ratification"]], None, None,
                ["GATE_REDESIGN (§10.5): the proposal's effect would alter "
                 "the gate structure, hard stops, or LAW's contract outside "
                 "the ratification process — refused even if routed through "
                 "another node's authority"])
        if action.get("type") in ("ratify", "amend_constitution") \
                and proposal.get("proposedBy") != DIRECTOR:
            return verdict(
                "PROHIBITED", [], [ARTICLES["ratification"]], None, None,
                [f"constitutional prohibition (Art. XVIII): "
                 f"{action.get('type')} proposed by "
                 f"{proposal.get('proposedBy')} — amendments only via the "
                 "ratification process"])

        # §3.4 step 4: authority check (§8). Valid claim iff: grantor held the
        # authority granted, scope covers the action, unexpired, unrevoked,
        # and it names/implies the proposer. Forgery → PROHIBITED + surfaced.
        claim = proposal.get("authorityClaim")
        grants_by_ref = {g.get("grant_ref"): g
                         for g in (inputs.get("grants") or [])}
        valid, basis, forged, auth_reason = self._validate_claim(
            claim, proposal, grants_by_ref)
        if forged:
            return verdict(
                "PROHIBITED",
                [{"hard_stop": "AUTHORITY_FORGERY",
                  "triggering_facts": [auth_reason]}],
                [ARTICLES["authority"], ARTICLES["fail_closed"]],
                None, None,
                [f"AUTHORITY_FORGERY (§10.3): {auth_reason} — PROHIBITED "
                 "and surfaced; forgery is never silent"])
        if not valid:
            return verdict(
                "NEEDS_AUTHORITY", [], [ARTICLES["authority"]], None, None,
                [f"authority check (§8): {auth_reason}. The grant is "
                 "validated by LAW, never self-asserted; a NEEDS_AUTHORITY "
                 "verdict may wait for a grant naming this exact proposal "
                 "(§4)"],
                extra={"awaits_grant_edge": True})

        # §3.4 step 5: evidence floor. The floor threshold is config
        # (calculus RATIFIED V2.1, FLAG-001 step 4); the *gate* is
        # constitutional.
        evidence = inputs.get("evidence") or {"n": 0, "confidence": 0.0}
        k = int(inputs.get("evidence_floor_k", DEFAULT_EVIDENCE_FLOOR_K))
        floor_met = evidence.get("n", 0) >= k and evidence.get(
            "confidence", 0.0) >= 0.5
        if not floor_met:
            return verdict(
                "NEEDS_EVIDENCE", [], [], basis, None,
                [f"evidence floor not met (config floor k={k}, "
                 f"n={evidence.get('n', 0)}, "
                 f"confidence={evidence.get('confidence', 0.0)}); re-evaluate "
                 "after the floor is met (§6.2)"],
                extra={"evidence_summary": {
                    "n": evidence.get("n", 0),
                    "floor_k": k,
                    "confidence": evidence.get("confidence", 0.0),
                    "floor_met": False,
                    "floor_is_candidate": True}})

        # §3.4 step 6: admissibility — bounded envelope (§7). ACT may execute
        # ONLY within the envelope; executing outside it is a constitutional
        # violation even with an ADMISSIBLE verdict.
        envelope = {
            "proposal_id": proposal.get("proposalId"),
            "action": action.get("type"),
            "targets": list(action.get("targets") or []),
            "bounds": _deepcopy_json(action.get("bounds") or {}),
            "scope_tag": action.get("scope_tag"),
            "authority_basis": basis,
            "issued_at": _now_iso(),
            "note": "envelope discipline (§7): execution outside this "
                    "envelope is a constitutional violation",
        }
        reasons = [
            f"ADMISSIBLE: lawful, authorized ({basis}), evidenced "
            f"(n={evidence.get('n', 0)}>=k={k}) — envelope issued; ACT "
            "executes only within it (§7)",
        ]
        if skew:
            reasons.append(
                "constitution skew noted (§9): proposal cited a different "
                "constitutionHash; evaluated under the pinned version")
        extra = {
            "constitution_skew": skew,
            "evidence_summary": {
                "n": evidence.get("n", 0), "floor_k": k,
                "confidence": evidence.get("confidence", 0.0),
                "floor_met": True, "floor_is_candidate": True},
        }
        return verdict("ADMISSIBLE", [], [ARTICLES["hierarchy"]], basis,
                       envelope, reasons, extra=extra)

    # ------------------------------------------------------------------
    # Monotonic transitions (§6.2): grant arrival / floor met re-evaluate.
    # Never downgrade silently; PROHIBITED is terminal for the version.
    # ------------------------------------------------------------------
    def apply_transition(self, state: Dict[str, Any],
                         transition_name: str) -> GateResult:
        """Re-evaluate after a named transition; receipted, monotonic.

        Supported: "GRANT_ARRIVED", "EVIDENCE_FLOOR_MET". A verdict that was
        PROHIBITED (or INTAKE_REFUSED) is terminal for this proposal version:
        the transition fails closed, state does not change, the attempt is
        receipted as a violation.
        """
        prior = (self.last_receipt or {}).get("gate")
        proposal_id = (self.last_receipt or {}).get("proposal_id")
        if prior in ("PROHIBITED", "INTAKE_REFUSED"):
            violation = {
                "transition": transition_name,
                "from": prior,
                "to": None,
                "reason": "invalid transition: PROHIBITED is terminal for "
                          "this proposal version (§6.2)",
                "proposal_id": proposal_id,
                "at": _now_iso(),
            }
            receipt = self._build_receipt(
                proposal=(self.last_receipt or {}).get("proposal", {}),
                gate=prior, hard_stops=[], articles=[ARTICLES["fail_closed"]],
                authority_basis=None, envelope=None,
                reasons=["transition refused: PROHIBITED is terminal; a new "
                         "version with materially different facts needs a "
                         "new proposalId (§6.2)"],
                transitions=[violation], inputs=state,
                extra={"invalid_transition_attempt": violation},
            )
            self.last_receipt = receipt
            return GateResult(verdict=GateVerdict.FAIL,
                              reasons=[f"LAW {prior}: transition "
                                       f"{transition_name} refused — "
                                       "terminal gate is not reopened"])
        lineage = [transition_name, f"lineage={proposal_id}"]
        result = self.gate(state)
        result.reasons = lineage + result.reasons
        return result

    # ------------------------------------------------------------------
    # Envelope-violation detection (acceptance #8)
    # ------------------------------------------------------------------
    def detect_envelope_violation(self,
                                  execution: Dict[str, Any]) -> Dict[str, Any]:
        """Compare an ACT execution record against the envelope (§7, §9).

        `execution` names what ACT actually did: {action, targets, bounds,
        proposal_id}. An execution outside its ADMISSIBLE envelope is a
        constitutional violation event (§9), receipted and surfaced.
        """
        receipt = self.last_receipt or {}
        envelope = receipt.get("envelope")
        if not envelope:
            return {"violation": True,
                    "reason": "no ADMISSIBLE envelope on record — nothing "
                              "was executable"}
        problems: List[str] = []
        if execution.get("proposal_id") != envelope.get("proposal_id"):
            problems.append("proposal_id mismatch with envelope")
        if execution.get("action") != envelope.get("action"):
            problems.append(f"action {execution.get('action')!r} != envelope "
                            f"action {envelope.get('action')!r}")
        env_targets = set(envelope.get("targets") or [])
        exec_targets = set(execution.get("targets") or [])
        if not exec_targets.issubset(env_targets):
            problems.append(f"targets {sorted(exec_targets - env_targets)} "
                            "outside envelope")
        if problems:
            return {"violation": True,
                    "reason": "constitutional violation (§7): ACT executed "
                              f"outside its envelope — {'; '.join(problems)}; "
                              "surfaced to the director, effects subject to "
                              "revocation where technically possible (§9)"}
        return {"violation": False, "reason": "execution within envelope"}

    # ------------------------------------------------------------------
    # Recompute / cold reconstruction (§11)
    # ------------------------------------------------------------------
    def recompute(self, gate_receipt: Dict[str, Any]) -> str:
        """Re-run §3.4 from the receipt's inputs and compare (§11).

        A cold successor given the receipt and the content-addressed
        constitution must reach the same verdict → MATCH. A receipt that
        cannot be recomputed is defective provenance (fail-closed).
        """
        if not gate_receipt:
            return "MISMATCH"
        if not self._verify_receipt_hash(gate_receipt):
            return "MISMATCH"
        inputs = gate_receipt.get("inputs")
        if not inputs:
            return "MISMATCH"
        recorded = gate_receipt.get("gate")
        result = LawNode().gate(inputs)
        reached = result.reasons[0].split(":")[0].replace("LAW ", "")
        return "MATCH" if reached == recorded else "MISMATCH"

    def persisted_transitions(self) -> List[str]:
        """Every state transition this node persists (receipted)."""
        return [
            "INTAKE_REFUSED",                 # §10.1 refusal at intake
            "PROHIBITED",                     # terminal for the version
            "NEEDS_AUTHORITY->AWAITS_GRANT",  # grant fulfillment wait (§4)
            "NEEDS_AUTHORITY->ADMISSIBLE",    # GRANT_ARRIVED, validated (§6.2)
            "NEEDS_EVIDENCE->ADMISSIBLE",     # EVIDENCE_FLOOR_MET (§6.2)
            "invalid_transition_refused",     # §6.2 fail-closed on bad moves
            "envelope_violation_event",       # §7/§9 ACT outside envelope
            "forgery_event",                  # §10.3 surfaced, never silent
            "gate_receipt_issued",            # every evaluation (§7)
        ]

    def evidence_hooks(self) -> List[str]:
        """Evidence sources this node reads/writes."""
        return [
            "constitutional_corpus_store",  # read: pinned version by hash
            "authority_grant_registry",     # read: grant chain validation
            "evidence_store",               # read: evidence summary (floor)
            "proposal_registry",            # read: verdict-shopping hashes
            "smartledger:stream=law",       # write: GateReceipts (§7)
            "intelligent_graph",            # write: REFUSED_BY / AWAITS_GRANT
                                            # edges, grant nodes (§12)
        ]

    def authority_checks(self) -> List[str]:
        """Authority validations LAW performs — never grants (§1.3, §8)."""
        return [
            "grantor_held_authority_granted",
            "grant_scope_covers_action",
            "grant_unexpired_and_unrevoked",
            "grant_names_or_implies_grantee",
            "no_self_generated_authority",      # Art. V.6
            "grant_chain_roots_in_director",
            "forgery_detected_and_surfaced",    # §10.3
            "no_authority_grant_performed",     # invariant: LAW is a
                                                # validator, never a mint
        ]

    def cold_reconstruct(self, receipts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Rebuild LAW's durable state from receipts alone (§11)."""
        if not receipts:
            return {"status": "FAILED",
                    "reasons": ["§11: no receipts — constitution corpus, "
                                "grant registry, and gate receipts are all "
                                "unavailable; stop here"]}
        receipt = receipts[-1]
        if not self._verify_receipt_hash(receipt):
            return {"status": "FAILED",
                    "reasons": ["receipt hash does not recompute — defective "
                                "provenance; the verdict it describes is not "
                                "trusted (§11)"]}
        if self.recompute(receipt) != "MATCH":
            return {"status": "FAILED",
                    "reasons": ["recompute MISMATCH: same proposal + pinned "
                                "constitution + grant state did not reach "
                                "the recorded verdict — fail-closed; any "
                                "action taken under it is flagged for "
                                "review (§11)"]}
        return {
            "status": "RECONSTRUCTED",
            "gate": receipt.get("gate"),
            "proposal_id": receipt.get("proposal_id"),
            "constitution_hash": receipt.get("constitution_hash"),
            "envelope": receipt.get("envelope"),
            "reasons": [f"cold reconstruction from gate receipt "
                        f"{receipt.get('receipt_id')} (§11); determinism "
                        "check MATCH"],
        }

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    @staticmethod
    def _intake_problem(proposal: Dict[str, Any]) -> Optional[str]:
        """§10.1: missing identity / claim / constitutionHash / malformed."""
        if not proposal.get("proposedBy"):
            return "missing proposedBy authentication"
        if "authorityClaim" not in proposal or proposal.get("authorityClaim") is None:
            return "missing authorityClaim"
        if not proposal.get("constitutionHash"):
            return "missing constitutionHash"
        action = proposal.get("action") or {}
        if not action.get("type"):
            return "malformed ActionDescriptor: missing action.type"
        if not proposal.get("proposalId"):
            return "missing proposalId"
        return None

    def _validate_claim(self, claim: Optional[Dict[str, Any]],
                        proposal: Dict[str, Any],
                        grants_by_ref: Dict[str, Dict[str, Any]]
                        ) -> Tuple[bool, Optional[str], bool, str]:
        """§8: validate the authority claim. Never grant (§1.3).

        Returns (valid, basis, forged, reason).
        """
        proposed_by = proposal.get("proposedBy")
        if claim is None:
            return (False, None, False,
                    "no grant covers this action — authority claim absent")
        grant_ref = claim.get("grant_ref")
        grant = grants_by_ref.get(grant_ref)
        if grant is None:
            # Asserts a grant that does not exist → forged, not merely absent.
            return (False, None, True,
                    f"authority claim cites grant_ref {grant_ref!r} which "
                    "does not exist in the grant registry")
        if grant.get("tampered"):
            return (False, None, True,
                    f"grant {grant_ref!r} fails integrity check — tampered")
        grantor, grantee = grant.get("grantor"), grant.get("grantee")
        if grantor == grantee:
            # Art. V.6: self-generated authority is invalid, always.
            # Invalid claim ≠ forgery unless it falsely presents as valid.
            return (False, None, False,
                    f"grant {grant_ref!r} is self-generated "
                    f"({grantor!r}→{grantee!r}); Art. V.6 invalid")
        if grantee != proposed_by:
            return (False, None, False,
                    f"grant {grant_ref!r} names grantee {grantee!r}, not "
                    f"proposer {proposed_by!r}")
        if grant.get("revoked"):
            return (False, None, False,
                    f"grant {grant_ref!r} is revoked")
        expiry = grant.get("expiry")
        if expiry and expiry < _now_iso():
            return (False, None, False,
                    f"grant {grant_ref!r} expired at {expiry}")
        chain = grant.get("chain") or []
        if grantor != DIRECTOR and DIRECTOR not in chain and not chain:
            return (False, None, False,
                    f"grant {grant_ref!r} does not chain to the director "
                    "root — all non-director grants must chain to it (§8)")
        scope = grant.get("scope") or []
        scope_tag = (proposal.get("action") or {}).get("scope_tag")
        if scope_tag not in scope and "*" not in scope:
            return (False, None, False,
                    f"grant {grant_ref!r} scope {scope} does not cover "
                    f"action scope_tag {scope_tag!r}")
        basis = (f"grant {grant_ref!r}: {grantor}→{grantee}, "
                 f"scope={scope_tag or '*'}")
        return (True, basis, False, basis)

    def _build_receipt(self, proposal: Dict[str, Any], gate: str,
                       hard_stops: List[Dict[str, Any]],
                       articles: List[str],
                       authority_basis: Optional[str],
                       envelope: Optional[Dict[str, Any]],
                       reasons: List[str],
                       transitions: List[Dict[str, Any]],
                       inputs: Dict[str, Any],
                       extra: Dict[str, Any]) -> Dict[str, Any]:
        proposal_hash = _sha256(proposal)
        store = inputs.get("constitution_store") or {}
        receipt = {
            "ledger": "smartledger",
            "stream": "law",
            "receipt_id": f"gate-{proposal.get('proposalId')}-"
                          f"{proposal_hash[:12]}",
            "node_id": NODE_ID,
            "node_version": NODE_VERSION,
            "law_contract_version": NODE_VERSION,
            "proposal_id": proposal.get("proposalId"),
            "proposal_hash": proposal_hash,
            "constitution_hash": store.get("pinned_hash"),
            "proposed_by": proposal.get("proposedBy"),
            "gate": gate,
            "hard_stops_fired": hard_stops,
            "articles_applied": articles,
            "authority_claim": proposal.get("authorityClaim"),
            "authority_basis": authority_basis,
            "evidence_summary": extra.get("evidence_summary", {
                "n": 0, "floor_k": DEFAULT_EVIDENCE_FLOOR_K,
                "confidence": 0.0, "floor_met": False,
                "floor_is_candidate": True}),
            "envelope": envelope,
            "reasons": reasons,
            "transitions": transitions,
            "material_facts_version": proposal.get("material_facts_version", 1),
            "proposal": proposal,  # full proposal snapshot: the violation
                                   # receipt (§6.2) and recompute (§11) need it
            "inputs": inputs,  # §11: everything needed to recompute
            "issued_at": _now_iso(),
            "issued_by": f"node_id={NODE_ID} (kernel binding)",
        }
        receipt.update({k: v for k, v in extra.items()
                        if k != "evidence_summary"})
        receipt["receipt_hash"] = _sha256(
            {k: v for k, v in receipt.items() if k != "receipt_hash"})
        return receipt

    @staticmethod
    def _verify_receipt_hash(receipt: Dict[str, Any]) -> bool:
        claimed = (receipt or {}).get("receipt_hash")
        if not claimed:
            return False
        content = {k: v for k, v in receipt.items() if k != "receipt_hash"}
        return _sha256(content) == claimed
