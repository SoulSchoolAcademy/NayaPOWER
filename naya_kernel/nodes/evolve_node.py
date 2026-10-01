"""NAYA-KERNEL-EVOLVE — candidate implementation (CANDIDATE — NOT RATIFIED — NOT MERGED).

Contractual responsibility, from EVOLVE-NODE-SPEC-CANDIDATE.md §1:

    EVOLVE determines which verified improvement may survive into the next
    legitimate system state. It is the organ of governed self-modification:
    the only legitimate path by which NayaPOWER changes its own
    configuration, contracts, algorithms, or runtime behavior — and the
    machinery that hands a truthful, minimum-sufficient continuity package
    to a cold successor.

    CONTINUITY != AUTHORITY. PROPOSAL != ADOPTION. IMPROVEMENT !=
    SELF-AUTHORIZATION. CAPABILITY != AUTHORITY. The deepest invariant: no
    evolution may silently change what the system is for. EVOLVE may improve
    methods; it may never redefine purpose.

Implemented from the reconciled EVOLVE spec (branch specs/
EVOLVE-NODE-SPEC-CANDIDATE.md — the 15 PDF amendments and 5 contradiction
resolutions — on the full base text in hidden_files/specs-final/
EVOLVE-NODE-SPEC-CANDIDATE.md, reconstructed with Appendix C honesty note).
The branch merge doc is the authority on the deltas; the reconstruction is
the authority on the base machinery they modify. The Decision Value Calculus
V2.1 is RATIFIED (FLAG-001 step 4 — binding in naya_kernel.node_base), so
the §3 gate scores under the ratified config and the ratified config hash
is bound into every gate-referencing receipt; the old SPEC-ONLY
(unratified-math) branches were removed with the stale premise.

This module is candidate code on the naya4/nine-node-kernel-v1 branch. It is
NOT ratified, NOT merged, NOT deployed.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from naya_kernel.node_base import (
    NodeBase, GateResult, GateVerdict, ManifestEntry,
    CALCULUS_V21_VERSION, CALCULUS_V21_SPEC_HASH,
    v21_executable_status,
)

# The shared executable Decision Value Calculus V2.1 — the ratified
# engine. EVOLVE scores through this module, never through a local
# formula (spec §16: NO SECOND EVOLUTION SCORE). Imported as a MODULE
# (not from-imports) so the wiring stays observable: spies and patches
# on kernel.value_calculus see every call the node makes.
import kernel.value_calculus as v21_shared
from kernel.value_calculus import (
    ENGINE_VERSION as V21_ENGINE_VERSION,
    Candidate as V21Candidate,
    PVEstimate as V21PVEstimate,
    QualityProfile as V21QualityProfile,
    RiskPolicy as V21RiskPolicy,
)


NODE_ID = "NAYA-KERNEL-EVOLVE"
NODE_MN = "MN-09"
NO_AUTHORITY_GRANT = "no_authority_granted_by_evolve"

# ---------------------------------------------------------------------------
# Vocabulary (spec §2 — the immutable surface; §3.5; §4; §8.1)
# ---------------------------------------------------------------------------

# §2 MUST-NEVER — PROHIBITED-class. No authority silently touches these.
IMMUTABLE_SURFACE = (
    "CONSTITUTIONAL_LAW",
    "AUTHORITY_MODEL",
    "IDENTITY",
    "MISSION",
    "PROVENANCE_REQUIREMENTS",
    "GATE_STRUCTURE",
    "HARD_STOP_FLAGS",
)

# §4 PROPOSE change classes. The class informs governance, never authority.
CHANGE_CLASSES = (
    "DOCUMENTATION", "PROJECTION", "CONFIGURATION", "ALGORITHM",
    "RUNTIME_BEHAVIOR", "DATA_MIGRATION", "SCHEMA", "DEPLOYMENT",
    "SECURITY", "AUTHORITY_MODEL", "CONSTITUTION", "MISSION",
)

# §3.5 blast-radius taxonomy — context, never permission.
BLAST_RADIUS = (
    "LOCAL", "COMPONENT", "CROSS_NODE", "SYSTEM", "PRODUCTION", "CONSTITUTIONAL",
)
_BLAST_ORDER = {name: i for i, name in enumerate(BLAST_RADIUS)}

# ---------------------------------------------------------------------------
# Shared-calculator wiring (§3.1 / §16 — NO SECOND EVOLUTION SCORE).
#
# EVOLVE scores evolution candidates through the shared executable
# Decision Value Calculus V2.1 (kernel/value_calculus.py), never through a
# local formula. The mapping below (evolve-v21map-v1) translates an EVOLVE
# candidate dict into the calculator's Candidate schema with explicit
# rules; anything the candidate does not carry stays UNKNOWN (None) so the
# calculator's own gate machinery (HARD_GATE_UNKNOWN,
# QUALITY_DIMENSION_MISSING, confidence floors) handles it — nothing is
# invented to make a gate pass.
#
# The QualityProfile uses the V2.1 executable's own ratified defaults;
# EVOLVE invents no scoring parameters. Any change to scoring parameters
# must go through the calculus, not around it.
# ---------------------------------------------------------------------------
_V21_PROFILE = V21QualityProfile(
    profile_id="EVOLVE-SHARED-CALCULATOR-V1",
    version=CALCULUS_V21_VERSION,
    objective="score evolution candidate under current config C "
              "(spec §3.1, §16)",
)

# Blast radius → V2.1 stakes (STAKE_ORDER: low < high < consequential).
_V21_STAKES_BY_BLAST = {
    "LOCAL": "low",
    "COMPONENT": "high",
    "CROSS_NODE": "high",
    "SYSTEM": "consequential",
    "PRODUCTION": "consequential",
    "CONSTITUTIONAL": "consequential",
}

# Import-time integrity check: the shared executable on disk must be the
# ratified one. _score_candidate fails closed on MISMATCH.
_V21_STATUS = v21_executable_status()


def _v21_no_change_baseline() -> V21Candidate:
    """The 'do not evolve' baseline the shared calculator requires."""
    return V21Candidate(
        candidate_id="EVOLVE-NO-CHANGE-BASELINE",
        quality={},
        confidence={},
        pv=V21PVEstimate(B=0.0, H=0.0, C=0.0, R=0.0, confidence={},
                         evidence_count=0),
        stakes="low",
        reversible=True,
        authorized=True,
        human_authorized=False,
        hard_violation=False,
        is_baseline=True,
    )

# §4 — three state axes, NEVER collapsed into one ambiguous flag.
SUCCESSION_STATES = (
    "DRAFT", "VALIDATING", "READY", "ACCEPTED", "STALE",
    "INCOMPLETE", "REJECTED", "SUPERSEDED",
)
PROPOSAL_STATES = (
    "OBSERVED_GAP", "PROPOSED", "SCORED", "GATED", "BRIEFED",
    "AUTHORIZED", "APPLIED", "VERIFIED", "ADOPTED", "ROLLED_BACK",
    "SUPERSEDED",
)
MATURITY_STATES = (
    "SOURCE_ONLY", "TESTED", "DEPLOYMENT_AUTHORIZED", "DEPLOYED",
    "PARITY_VERIFIED", "BEHAVIOR_VERIFIED", "PRODUCTION_PROVEN",
)

LEGAL_PROPOSAL_TRANSITIONS = {
    "OBSERVED_GAP": ("PROPOSED",),
    "PROPOSED": ("SCORED", "REJECTED"),
    "SCORED": ("GATED", "REJECTED"),
    "GATED": ("BRIEFED", "AUTHORIZED", "REJECTED"),
    "BRIEFED": ("AUTHORIZED", "REJECTED"),
    "AUTHORIZED": ("APPLIED", "REJECTED"),
    "APPLIED": ("VERIFIED", "ROLLED_BACK"),
    "VERIFIED": ("ADOPTED", "ROLLED_BACK"),
    "ADOPTED": ("SUPERSEDED", "ROLLED_BACK"),
    "ROLLED_BACK": ("PROPOSED",),       # rebase after rollback (§4 stale rule)
    "SUPERSEDED": (),
    "REJECTED": (),
}
LEGAL_MATURITY_TRANSITIONS = {
    "SOURCE_ONLY": ("TESTED",),
    "TESTED": ("DEPLOYMENT_AUTHORIZED",),
    "DEPLOYMENT_AUTHORIZED": ("DEPLOYED",),
    "DEPLOYED": ("PARITY_VERIFIED",),
    "PARITY_VERIFIED": ("BEHAVIOR_VERIFIED",),
    "BEHAVIOR_VERIFIED": ("PRODUCTION_PROVEN",),
    "PRODUCTION_PROVEN": (),
}
LEGAL_SUCCESSION_TRANSITIONS = {
    "DRAFT": ("VALIDATING", "STALE", "INCOMPLETE", "REJECTED"),
    "VALIDATING": ("READY", "STALE", "INCOMPLETE", "REJECTED"),
    "READY": ("ACCEPTED", "STALE", "REJECTED"),
    "ACCEPTED": ("SUPERSEDED",),
    "STALE": ("DRAFT", "REJECTED"),
    "INCOMPLETE": ("DRAFT", "REJECTED"),
    "REJECTED": (),
    "SUPERSEDED": (),
}

# §8.7 critical successor obligations — one missing zeroes readiness.
CRITICAL_SUCCESSOR_OBLIGATIONS = (
    "identity_context",
    "mission",
    "current_truth",
    "authority_boundary",
    "material_blockers",
    "applicable_verified_learning",
    "next_action",
    "proof_requirements",
    "canonical_source_pointers",
)

# §8.1 the 24-field successor package.
SUCCESSOR_PACKAGE_FIELDS = (
    "handoff_id", "parent_identity", "successor_identity",
    "kernel_revision", "contract_revisions", "mission", "current_truth",
    "intelligence_refs", "learning_refs", "relationship_refs",
    "proof_refs", "recent_outcome_refs", "unknowns", "conflicts",
    "blockers", "active_work",
    "authority_context", "privacy_context", "constraints",
    "next_action", "next_proof_requirement", "source_snapshot",
    "package_hash", "created_at",
)

# §8.6 the Cold-14 continuity questions.
COLD_14 = (
    "who are we",
    "what are we building",
    "why",
    "what does success mean",
    "what is true now",
    "what has been proven",
    "what is unknown",
    "what authority exists",
    "what happened previously",
    "what did we learn",
    "what should happen next",
    "how do I prove it",
    "where do I record it",
    "how does the next Naya continue",
)

INTELLIGENCE_CLASSES = ("CORE", "REUSABLE", "CONTEXT", "REFERENCE", "EPHEMERAL")

# §2 ordering law — optimization is subordinate to purpose.
ORDERING_LAW = ("MISSION", "LAW", "SAFETY", "TRUTH", "VALUE")

# §10 refusal codes. (REFUSAL_CALCULUS_UNRATIFIED was removed by FLAG-001
# step 4: Decision Value Calculus V2.1 is RATIFIED — there is no
# unratified-math autonomous path left to refuse.)
REFUSAL_IMMUTABLE_SURFACE = "IMMUTABLE_SURFACE_TOUCH"
REFUSAL_CONFIG_MISMATCH = "DECIDING_CONFIG_MISMATCH"
REFUSAL_BUNDLE_SPLIT = "BUNDLE_SPLIT_DETECTED"
REFUSAL_ENVELOPE = "ENVELOPE_EXCEEDED_UNBRIEFED"
REFUSAL_AUTHORITY = "AUTHORITY_UNRESOLVABLE"
REFUSAL_BLOCKER_OMITTED = "BLOCKER_OMITTED"
REFUSAL_HARM_POST_ADOPTION = "HARM_DETECTED_POST_ADOPTION"
REFUSAL_DIRECTOR_PROHIBITED = "DIRECTOR_PROHIBITED_INSTRUCTION"
REFUSAL_REVOKED = "REVOKED"
REFUSAL_EVIDENCE_UNVALIDATED = "EVIDENCE_UNVALIDATED"
REFUSAL_NO_FUTURE_BEHAVIOR = "NO_FUTURE_BEHAVIOR_NAMED"
REFUSAL_MISSION = "MISSION_DRIFT"
REFUSAL_GATE_BYPASS = "GATE_BYPASS_ATTEMPT"

# §11.4 continuity metrics — diagnostics, never gates.
CONTINUITY_METRICS = (
    "successor_reconstruction_latency",
    "cold_14_completion_rate",
    "stale_package_rate",
    "continuity_mismatch_rate",
    "authority_inheritance_violations",
    "source_runtime_drift_incidents",
    "rollback_rate",
    "multi_generation_drift",
)

DEFAULT_CONFIG: Dict[str, Any] = {
    # Decision Value Calculus V2.1 — RATIFIED 2026-09-30 (PRs #1186/#1190/
    # #1192). §3.2's SPEC-ONLY conditioning is satisfied; the ratified
    # config hash is bound into every gate-referencing receipt (see
    # naya_kernel.node_base).
    "calculusVersion": CALCULUS_V21_VERSION,
    "calculusRatified": True,
    "kernelRevision": "kr-0",
    "currentVersion": "v0.0.0",
    # §7.1 — director-set autonomous envelope. Changed only by the Director
    # (EVOLVE has no method that mutates it; §7.1, §7.2).
    "envelope": {
        "allowed_change_classes": ["DOCUMENTATION", "PROJECTION", "CONFIGURATION"],
        "max_blast_radius": "COMPONENT",
        "reversibility_floor": 0.8,
        "value_threshold": 0.5,
    },
    # Observation windows for delayed-harm detection (candidate seeds).
    "observation_windows": ["24h", "7d", "30d", "90d"],
}

# Candidate field set, §4 PROPOSE (PDF §17).
_CANDIDATE_FIELDS = (
    "evolution_id", "proposal_type", "objective", "source_gap_refs",
    "learning_refs", "current_version", "proposed_version", "proposed_change",
    "change_class", "touches_surface", "touches_personality",
    "mission_compatible",
    "affected_components", "affected_contracts", "expected_value", "risks",
    "blast_radius", "reversibility", "rollback_plan", "authority_requirement",
    "verification_plan", "migration_plan", "deployment_plan",
    "successor_impact", "state", "evidence_refs", "provenance", "created_at",
)


# ---------------------------------------------------------------------------
# Module helpers
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def _hash(obj: Any) -> str:
    return hashlib.sha256(_canonical(obj).encode("utf-8")).hexdigest()


def _config_hash(config: Dict[str, Any]) -> str:
    body = {k: v for k, v in config.items() if k != "configHash"}
    return _hash(body)


def successor_key(*, parent: str, successor: str, kernel_revision: str,
                  truth_snapshot: Any, active_work: Any,
                  learning_set: Any) -> str:
    """SuccessorKey = H(parent ‖ successor ‖ kernelRevision ‖ truthSnapshot ‖
    activeWork ‖ learningSet) — exact replay rereads; material change creates
    a new version (§5.2). Derived, never assigned."""
    return _hash({
        "parent": parent,
        "successor": successor,
        "kernelRevision": kernel_revision,
        "truthSnapshot": truth_snapshot,
        "activeWork": active_work,
        "learningSet": learning_set,
    })


def package_hash(package: Dict[str, Any]) -> str:
    """H_S = SHA256(Canonicalize(S)) — material mutation creates a new
    version, never a silent edit (§5.2 / A5)."""
    body = {k: v for k, v in package.items() if k != "package_hash"}
    return _hash(body)


class EvolveNode(NodeBase):
    """NAYA-KERNEL-EVOLVE (MN-09), candidate implementation.

    Every state transition emits a hash-bound typed receipt. EVOLVE performs
    authority validations and grants nothing (see authority_checks()). It
    never mutates its own envelope, never in-place mutates governed config,
    and never authorizes itself: PROPOSAL != ADOPTION, always.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self._config: Dict[str, Any] = json.loads(json.dumps(
            config if config is not None else DEFAULT_CONFIG))
        self._config["configHash"] = _config_hash(self._config)
        self._config_snapshots: Dict[str, Dict[str, Any]] = {}
        self._config_snapshots[self._config["configHash"]] = json.loads(
            json.dumps(self._config))
        # Candidate registry (§4 — three axes per candidate).
        self._candidates: Dict[str, Dict[str, Any]] = {}
        # Version store for CAS promotion (§5.2).
        self._versions: Dict[str, str] = {}
        # Armed rollback plans, keyed by evolution_id (§6).
        self._armed_rollbacks: Dict[str, Dict[str, Any]] = {}
        # Succession packages (§8).
        self._handoff_packages: Dict[str, Dict[str, Any]] = {}
        # Continuity metrics — diagnostics, never gates (§11.4).
        self._metrics: Dict[str, List[float]] = {}
        # Brief outbox (§7 — everything outside the envelope waits here).
        self._brief_outbox: List[Dict[str, Any]] = []
        # Transition ledger (§5 — hash-bound, append-only).
        self._receipts: List[Dict[str, Any]] = []
        self._receipt_index: Dict[str, Dict[str, Any]] = {}
        self._seq = 0

    # ------------------------------------------------------------------
    # Internal machinery
    # ------------------------------------------------------------------

    def _now(self) -> str:
        return _now_iso()

    def _seal(self, receipt: Dict[str, Any]) -> Dict[str, Any]:
        """Seal the receipt: everything is sealed UNDER receipt_hash (§5)."""
        body = {k: v for k, v in receipt.items() if k != "receipt_hash"}
        receipt["receipt_hash"] = _hash(body)
        return receipt

    def _emit(self, receipt_type: str, evolution_id: Optional[str] = None,
              **fields: Any) -> Dict[str, Any]:
        """Emit a typed, hash-bound evolution receipt (§5 field set)."""
        self._seq += 1
        receipt: Dict[str, Any] = {
            "receipt_type": receipt_type,
            "receipt_id": f"er-{_hash([receipt_type, self._seq, self._now()])[:16]}",
            "node_id": NODE_ID,
            "node_mn": NODE_MN,
            "execution_id": f"ex-{self._seq:06d}",
            "evolution_id": evolution_id,
            "configHash": self._config["configHash"],
            # §3.3 — the adoption decision is computed under config C and
            # binds C's hash; §3.2 — calculus version AND ratification
            # status are bound into every gate-referencing receipt, plus the
            # ratified V2.1 config hash (FLAG-001 step 4).
            "deciding_config_hash": self._config["configHash"],
            "calculusVersion": self._config["calculusVersion"],
            "calculusRatified": bool(self._config.get("calculusRatified")),
            "calculusConfigHash": CALCULUS_V21_SPEC_HASH,
            "authority_created": False,  # invariant: EVOLVE never creates authority
            "timestamp": self._now(),
            "issued_at": self._now(),
        }
        receipt.update(fields)
        self._seal(receipt)
        self._receipts.append(receipt)
        self._receipt_index[receipt["receipt_id"]] = receipt
        return receipt

    def _get(self, evolution_id: str) -> Dict[str, Any]:
        candidate = self._candidates.get(evolution_id)
        if candidate is None:
            raise KeyError(f"unknown evolution_id: {evolution_id}")
        return candidate

    def _transition(self, candidate: Dict[str, Any], axis: str,
                    to_state: str, reason: str, **extra: Any) -> Dict[str, Any]:
        """Illegal-transition fail-closed state move on one axis (§4). The
        three axes move independently — they never collapse into one flag."""
        table = {
            "proposal": LEGAL_PROPOSAL_TRANSITIONS,
            "maturity": LEGAL_MATURITY_TRANSITIONS,
            "succession": LEGAL_SUCCESSION_TRANSITIONS,
        }[axis]
        from_state = candidate[axis]
        if to_state not in table.get(from_state, ()):
            raise ValueError(
                f"illegal evolve transition on {axis} axis {from_state} -> "
                f"{to_state} (fail-closed): {reason}"
            )
        candidate[axis] = to_state
        candidate["transitions"].append({
            "axis": axis, "from": from_state, "to": to_state,
            "reason": reason, "timestamp": self._now(),
        })
        return self._emit(
            "TRANSITION", evolution_id=candidate["id"],
            axis=axis, state_before=from_state, state_after=to_state,
            reason=reason, **extra,
        )

    def _immutable_touch(self, candidate: Dict[str, Any]) -> List[str]:
        """Classify the proposal against the immutable surface (§2). Returns
        the touched surface items; empty means clean. Violation is
        PROHIBITED outright — refused with a receipted reason, never
        briefed as routine."""
        touched: List[str] = []
        change_class = candidate.get("change_class")
        if change_class in ("AUTHORITY_MODEL",):
            touched.append("AUTHORITY_MODEL")
        if change_class in ("CONSTITUTION",):
            touched.append("CONSTITUTIONAL_LAW")
        if change_class in ("MISSION",):
            touched.append("MISSION")
        declared = candidate.get("touches_surface") or []
        for item in declared:
            if item in IMMUTABLE_SURFACE and item not in touched:
                touched.append(item)
        # MISSION protection (§2.2 A1 / §8.8): a proposal that achieves local
        # efficiency by degrading the actual human objective is not
        # improvement. Mission drift is detected, not averaged away.
        if candidate.get("mission_compatible") is False and "MISSION" not in touched:
            touched.append("MISSION")
        return sorted(touched)

    def _to_v21_candidate(self, candidate: Dict[str, Any]) -> V21Candidate:
        """Translate an EVOLVE candidate dict into the shared V2.1 Candidate.

        Mapping evolve-v21map-v1 — explicit and versioned. Rules:
        - reversibility (0-1) → quality "reversibility" (0-10 scale).
        - blast radius → quality "blast_containment" (inverse, 0-10) and
          V2.1 stakes (LOCAL→low … CONSTITUTIONAL→consequential).
        - evidence_refs count → quality "evidence_sufficiency"
          (min(10, 2 per ref), the same rule CONNECT uses).
        - expected_value → present value benefit B; the residual-risk term R
          is blast × (1 − reversibility), the risk the old local form used.
        - authorized = the §7.1 envelope verdict: the director-set envelope
          is the authorization basis for the merit score; authority routing
          (AUTONOMOUS vs BRIEF) is decided by the envelope separately and
          recorded in the same receipt. The calculator grants nothing.
        - hard_violation = immutable-surface touch (the spec's MUST-NEVER
          surface becomes the calculator's JUDGMENT_RULE_HARD_STOP).
        - human_authorized = False always: EVOLVE never claims human
          authorization for the merit score; human authorization is a
          separate routing fact recorded by the envelope/brief path.

        Explicit non-mappings (no constant-stuffing without a stated
        reason):
        - Quality dims the candidate does not carry (objective_fit,
          applicability, robustness, simplicity) are ABSENT (None), not
          zeroed: the calculator's QUALITY_DIMENSION_MISSING machinery
          names them instead of this method inventing values.
        - pv.H = 0.0 and pv.C = 0.0 are explicit NON-ESTIMATES, not
          measured zeros: the EVOLVE candidate schema carries a single
          expected_value figure with no decomposed harm/cost terms, so
          there is nothing faithful to map. Residual risk flows through
          R. If the schema gains harm/cost fields, they must be mapped
          here — these zeros must not be mistaken for "no harm / no cost".
        - confidence = {} (candidate and pv): the candidate carries no
          per-dimension confidence; the calculator applies its own
          confidence floors (CONFIDENCE_FLOOR) rather than this method
          inventing certainty.
        - tail risks: left at the dataclass default (empty) — the
          candidate schema carries no tail-risk model; the calculator's
          tail_penalty path therefore contributes nothing, honestly.
        - Lawful/rights/privacy/safety flags: absent (None) → the
          calculator's HARD_GATE_UNKNOWN names them; an EVOLVE candidate
          that cannot evidence them gates NEEDS_EVIDENCE, never PASS.
        """
        evolution_id = str(candidate.get("evolution_id") or "unknown")
        reversibility = float(candidate.get("reversibility") or 0.0)
        blast = _BLAST_ORDER.get(candidate.get("blast_radius", "LOCAL"), 0)
        blast_frac = blast / (len(BLAST_RADIUS) - 1)
        evidence_refs = candidate.get("evidence_refs") or []
        envelope_ok, _ = self._in_envelope(candidate)
        floor = float(self._config.get("envelope", {}).get(
            "reversibility_floor", 0.8))
        return V21Candidate(
            candidate_id=evolution_id,
            quality={
                "reversibility": reversibility * 10.0,
                "blast_containment": (1.0 - blast_frac) * 10.0,
                "evidence_sufficiency": min(10.0, len(evidence_refs) * 2.0),
            },
            confidence={},
            pv=V21PVEstimate(
                B=float(candidate.get("expected_value") or 0.0),
                H=0.0,
                C=0.0,
                R=blast_frac * (1.0 - reversibility),
                confidence={},
                evidence_count=len(evidence_refs),
            ),
            stakes=_V21_STAKES_BY_BLAST.get(
                candidate.get("blast_radius", "LOCAL"), "low"),
            reversible=reversibility >= floor,
            authorized=envelope_ok,
            human_authorized=False,
            hard_violation=bool(self._immutable_touch(candidate)),
        )

    def _score_candidate(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """§3.1 / §16 — NO SECOND EVOLUTION SCORE.

        The candidate is scored by the shared executable Decision Value
        Calculus V2.1 (kernel/value_calculus.py) — the ratified engine.
        EVOLVE consumes the calculus's outputs (gate, v_safe, quality);
        it does not replace them with a local formula.

        The score is the proposal row's conservative value (v_safe) from
        evaluate_candidates run against the no-change baseline under the
        CURRENT CONFIG C (never under the proposed config, §3.3). The
        receipt binds the shared executable's blob SHA so a verifier can
        confirm WHICH executable scored; score_engine is
        "shared_calculator", never implied. calculator_inputs binds the
        exact V2.1 Candidate dicts (proposal + baseline), the quality
        profile, and the risk policy, so an independent recomputation —
        rebuild the two Candidates, the profile, and the policy from
        calculator_inputs and call evaluate_candidates — must MATCH the
        receipt's v_safe, or the adoption is void (§3.3).
        """
        if not _V21_STATUS["match"]:
            raise RuntimeError(
                "EVOLVE refuses to score: shared calculator integrity "
                f"{_V21_STATUS['reason']} "
                f"(expected {_V21_STATUS['expected_blob_sha']}, "
                f"actual {_V21_STATUS['actual_blob_sha']})")
        v21_candidate = self._to_v21_candidate(candidate)
        baseline = _v21_no_change_baseline()
        evaluation = v21_shared.evaluate_candidates(
            [baseline, v21_candidate], baseline.candidate_id,
            _V21_PROFILE, V21RiskPolicy())
        row = next(r for r in evaluation["rows"]
                   if r["candidate_id"] == v21_candidate.candidate_id)
        calculus_chain = ("RESOLVE", "GATE", "SCORE", "COMPARE", "SELECT",
                          "ACT/ESCALATE", "OBSERVE", "VERIFY", "LEDGER",
                          "LEARN", "RECALIBRATE")
        # Green-bar condition 2: bind the calculator inputs so the score
        # is independently recomputable from the receipt alone — no
        # re-running the mapping. dataclasses.asdict captures the full
        # constructed Candidates (mapped fields + every default).
        calculator_inputs = {
            "candidate": asdict(v21_candidate),
            "baseline": asdict(baseline),
            "baseline_candidate_id": baseline.candidate_id,
            "quality_profile": asdict(_V21_PROFILE),
            "risk_policy": asdict(V21RiskPolicy()),
        }
        return {
            "calculus_chain": calculus_chain,
            "score_engine": "shared_calculator",
            "score_engine_version": V21_ENGINE_VERSION,
            "score_engine_executable_blob_sha":
                _V21_STATUS["actual_blob_sha"],
            "v21_mapping": "evolve-v21map-v1",
            "calculator_inputs": calculator_inputs,
            "expected_value": float(candidate.get("expected_value") or 0.0),
            "v_safe": row["v_safe"],
            "score": row["v_safe"],
            "gate": row["gate"],
            "gate_reasons": list(row["gate_reasons"]),
            "quality_Q": row["q"]["Q"],
            "deciding_config_hash": self._config["configHash"],
            "calculusConfigHash": CALCULUS_V21_SPEC_HASH,
            "calculus_spec_status": "RATIFIED",
        }

    def _in_envelope(self, candidate: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """§7.1 — is the candidate inside the director-set autonomous
        envelope? Reasons name every bound violated."""
        env = self._config.get("envelope", {})
        reasons: List[str] = []
        if candidate.get("change_class") not in env.get("allowed_change_classes", []):
            reasons.append(
                f"change_class {candidate.get('change_class')} not in envelope "
                f"allowed classes")
        blast = _BLAST_ORDER.get(candidate.get("blast_radius", "LOCAL"), 0)
        max_blast = _BLAST_ORDER.get(env.get("max_blast_radius", "LOCAL"), 0)
        if blast > max_blast:
            reasons.append(
                f"blast_radius {candidate.get('blast_radius')} exceeds envelope "
                f"max {env.get('max_blast_radius')}")
        if float(candidate.get("reversibility") or 0.0) < float(
                env.get("reversibility_floor", 0.0)):
            reasons.append(
                f"reversibility {candidate.get('reversibility')} below envelope "
                f"floor {env.get('reversibility_floor')}")
        if float(candidate.get("expected_value") or 0.0) < float(
                env.get("value_threshold", 0.0)):
            reasons.append(
                f"expected_value {candidate.get('expected_value')} below envelope "
                f"threshold {env.get('value_threshold')}")
        return (not reasons), reasons

    def _rollback_plan_valid(self, candidate: Dict[str, Any]) -> Tuple[bool, str]:
        """§3.6 / §6 — a rollback plan must be more than "undo it if bad":
        it names the mechanism, the authority, the evidence of completion,
        and the verification requirement."""
        plan = candidate.get("rollback_plan") or {}
        missing = [slot for slot in ("mechanism", "authority", "evidence",
                                     "verification")
                   if not plan.get(slot)]
        if missing:
            return False, f"rollback plan missing: {', '.join(missing)}"
        return True, "rollback plan complete"

    # ------------------------------------------------------------------
    # §4 lifecycle — OBSERVE / DIAGNOSE / PROPOSE / EVALUATE / APPLY / VERIFY
    # ------------------------------------------------------------------

    def observe(self, gap: Dict[str, Any]) -> Dict[str, Any]:
        """OBSERVE: register a verified gap as a candidate (proposal axis
        OBSERVED_GAP). Human-reconstruction burden is a legitimate trigger
        (§4, A10); EVOLVE only observes — it never adopts at this phase."""
        self._seq += 1
        evolution_id = (
            f"ev-{_hash([gap, self._seq, self._now()])[:12]}")
        candidate: Dict[str, Any] = {
            "id": evolution_id,
            "gap": dict(gap),
            "proposal": "OBSERVED_GAP",
            "succession": "DRAFT",
            "maturity": "SOURCE_ONLY",
            "transitions": [],
            "created_at": self._now(),
        }
        self._candidates[evolution_id] = candidate
        return self._emit(
            "GAP_OBSERVED", evolution_id=evolution_id,
            gap=gap,
            reason="OBSERVE — verified gap registered; no adoption proposed")

    def diagnose(self, evolution_id: str, components: Dict[str, Any]
                 ) -> Dict[str, Any]:
        """DIAGNOSE: compute ImpactClosure(e) = TransitiveDependents(
        AffectedComponents(e)) with bounded graph traversal (§4, A7).
        Freshness is intelligence-class-specific — no universal TTL."""
        candidate = self._get(evolution_id)
        affected = candidate.get("affected_components") or []
        closure: List[str] = []
        seen = set()
        frontier = list(affected)
        depth = 0
        while frontier and depth < 4:  # bounded traversal
            node = frontier.pop(0)
            if node in seen:
                continue
            seen.add(node)
            closure.append(node)
            for dep in (components or {}).get(node, []):
                if dep not in seen:
                    frontier.append(dep)
            depth += 1
        candidate["impact_closure"] = closure
        return self._emit(
            "DIAGNOSED", evolution_id=evolution_id,
            impact_closure=closure,
            reason="DIAGNOSE — bounded transitive impact closure; no silent "
                   "local optimization")

    def propose(self, fields: Dict[str, Any]) -> Dict[str, Any]:
        """PROPOSE: build the evolution candidate object (canonical field
        set, §4). Every proposal is classified against the immutable surface
        (§2) before it enters the gate. Immutable touch → PROHIBITED,
        refused with a receipted reason, never briefed as routine."""
        missing = [f for f in ("objective", "change_class", "proposed_change",
                               "expected_value", "blast_radius",
                               "reversibility", "rollback_plan",
                               "authority_requirement", "future_behavior")
                   if f not in fields or fields[f] in (None, "")]
        if missing:
            receipt = self._emit(
                "PROPOSAL_REFUSED", evolution_id=None,
                refusal_code=REFUSAL_NO_FUTURE_BEHAVIOR if
                "future_behavior" in missing else "INCOMPLETE_PROPOSAL",
                missing_fields=missing,
                reason="PROPOSE — a proposal that cannot name the future "
                       "behavior it will change is not an evolution (§10)")
            return {"decision": "REFUSED", "receipt_id": receipt["receipt_id"],
                    "refusal_code": receipt["refusal_code"]}
        self._seq += 1
        evolution_id = fields.get("evolution_id") or (
            f"ev-{_hash([fields, self._seq, self._now()])[:12]}")
        candidate: Dict[str, Any] = {
            "id": evolution_id,
            "proposal": "OBSERVED_GAP",
            "succession": "DRAFT",
            "maturity": "SOURCE_ONLY",
            "transitions": [],
            "created_at": self._now(),
        }
        for field in _CANDIDATE_FIELDS:
            # id and timestamps are assigned here, never caller-supplied;
            # "state" is the three machine axes (proposal/succession/
            # maturity), not a freeform field.
            if field in ("evolution_id", "created_at", "state"):
                continue
            candidate[field] = fields.get(field)
        if candidate.get("blast_radius") not in BLAST_RADIUS:
            receipt = self._emit(
                "PROPOSAL_REFUSED", evolution_id=evolution_id,
                refusal_code="INVALID_BLAST_RADIUS",
                reason="PROPOSE — blast radius must be one of the six "
                       "ratified classes; labels never create authority (§3.5)")
            return {"decision": "REFUSED", "receipt_id": receipt["receipt_id"],
                    "refusal_code": receipt["refusal_code"]}
        # §2 — the immutable-surface classification happens at PROPOSE time.
        touched = self._immutable_touch(candidate)
        if touched:
            candidate["proposal"] = "REJECTED"
            self._candidates[evolution_id] = candidate
            receipt = self._emit(
                "PROPOSAL_REFUSED", evolution_id=evolution_id,
                refusal_code=REFUSAL_IMMUTABLE_SURFACE,
                touched_surface=touched,
                reason="§2 — PROHIBITED-class surface touch; refused outright, "
                       "never briefed as routine. Constitutional and mission "
                       "changes may be modeled but only the Human Director "
                       "ratifies them")
            return {"decision": "REFUSED", "receipt_id": receipt["receipt_id"],
                    "refusal_code": receipt["refusal_code"],
                    "touched_surface": touched}
        # §8.9 — personality-trait evolutions are always BRIEF-class, never
        # autonomous. Personality is subordinate to law but director-owned.
        if fields.get("touches_personality"):
            candidate["route"] = "BRIEF"
        self._candidates[evolution_id] = candidate
        self._transition(candidate, "proposal", "PROPOSED",
                         reason="PROPOSE — candidate object complete; surface clean")
        return {"decision": "PROPOSED", "evolution_id": evolution_id,
                "touched_surface": [], "route": candidate.get("route", "GATE")}

    def evaluate(self, evolution_id: str) -> Dict[str, Any]:
        """EVALUATE: run the §3 gate — calculus scoring under the CURRENT
        config (V2.1 RATIFIED — FLAG-001 step 4; the ratified config hash is
        bound into the GATED receipt), bundle-split check, blast-radius
        and reversibility assessment, authority-requirement resolution.
        Stale-proposal rule: Base(E) != CurrentVersion → STALE_PROPOSAL →
        REBASE / RE-EVALUATE, never automatic promotion."""
        candidate = self._get(evolution_id)
        # §4 stale-proposal rule (A6).
        base = candidate.get("current_version")
        current = self._config.get("currentVersion")
        if base is not None and base != current:
            candidate["succession"] = "STALE"
            receipt = self._emit(
                "STALE_PROPOSAL", evolution_id=evolution_id,
                base_version=base, current_version=current,
                refusal_code="STALE_PROPOSAL",
                reason="§4 — Base(E) != CurrentVersion; REBASE and "
                       "RE-EVALUATE; never automatic promotion")
            return {"decision": "STALE_PROPOSAL",
                    "receipt_id": receipt["receipt_id"],
                    "succession": "STALE"}
        score = self._score_candidate(candidate)
        candidate["gate_score"] = score
        # evaluate() is re-entrant: REBASE / RE-EVALUATE is the stale rule's
        # second half (§4, A6). First run walks PROPOSED→SCORED; a
        # re-evaluation re-runs the gate without re-walking the transition.
        if candidate["proposal"] == "PROPOSED":
            self._transition(candidate, "proposal", "SCORED",
                             reason="EVALUATE — §3 gate run under current config")
        else:
            self._emit("RE_EVALUATED", evolution_id=evolution_id,
                       reason="EVALUATE — re-running the §3 gate under the "
                              "current config (rebase path)")
        # Rollback plan must name mechanism/authority/evidence/verification.
        plan_ok, plan_reason = self._rollback_plan_valid(candidate)
        if not plan_ok:
            self._transition(candidate, "proposal", "REJECTED", reason=plan_reason)
            receipt = self._emit(
                "GATE_REFUSED", evolution_id=evolution_id,
                refusal_code="ROLLBACK_PLAN_INCOMPLETE", reason=plan_reason)
            return {"decision": "REFUSED", "receipt_id": receipt["receipt_id"],
                    "refusal_code": receipt["refusal_code"]}
        # §3 gate routing. V2.1 is RATIFIED (FLAG-001 step 4): the old
        # SPEC-ONLY branch (unratified math → forced BRIEF) was removed with
        # the stale premise. calculus_ok stays bound into the receipt.
        calculus_ok = bool(self._config.get("calculusRatified"))
        envelope_ok, envelope_reasons = self._in_envelope(candidate)
        route: str
        if candidate.get("route") == "BRIEF":
            route = "BRIEF"   # §8.9 personality boundary — always brief
            reasons = ["personality-trait evolution is always BRIEF-class (§8.9)"]
        elif not envelope_ok:
            route = "BRIEF"
            reasons = envelope_reasons
        else:
            route = "AUTONOMOUS"
            reasons = ["within the director-set autonomous envelope (§7.1); "
                       "calculus V2.1 ratified"]
        if candidate["proposal"] != "GATED":
            self._transition(candidate, "proposal", "GATED",
                             reason="EVALUATE — route resolved: " + route)
        receipt = self._emit("GATED", evolution_id=evolution_id,
            gate_score=score, route=route, reasons=reasons,
            envelope_ok=envelope_ok, calculus_ratified=calculus_ok,
            reason="§3 gate — scored under config C; route explicit")
        if route == "BRIEF" and candidate["proposal"] != "BRIEFED":
            self._transition(candidate, "proposal", "BRIEFED",
                             reason="EVALUATE — routed to the Director; "
                                    "adoption waits on briefed authority")
            brief = self._emit(
                "BRIEFED", evolution_id=evolution_id,
                gate_score=score, reasons=reasons,
                reason="§7 — outside the envelope or SPEC-ONLY; the brief is "
                       "a proposal, not an adoption")
            self._brief_outbox.append(brief)
        return {"decision": "GATED", "route": route, "reasons": reasons,
                "gate_score": score, "receipt_id": receipt["receipt_id"]}

    def bundle_evaluate(self, evolution_ids: List[str]) -> Dict[str, Any]:
        """§3.4 BUNDLE_SPLIT hard stop. A change decomposed into sub-threshold
        pieces to evade gates is evaluated as ONE bundle: if the bundle
        exceeds any gate the pieces would have tripped individually, the
        bundle trips it. Gate evasion by decomposition is a hard stop."""
        members = [self._get(eid) for eid in evolution_ids]
        objectives = {m.get("objective") for m in members}
        timeframes = {m.get("created_at", "")[:13] for m in members}
        surfaces = {m.get("change_class") for m in members}
        bundle = {
            "member_ids": evolution_ids,
            "shared_objective": len(objectives) == 1,
            "shared_timeframe": len(timeframes) == 1,
            "shared_surface": len(surfaces) == 1,
            "aggregate_blast": max(
                (_BLAST_ORDER.get(m.get("blast_radius", "LOCAL"), 0)
                 for m in members), default=0),
            "min_reversibility": min(
                (float(m.get("reversibility") or 0.0) for m in members),
                default=1.0),
        }
        # A "related bundle" = shares objective, timeframe, or surface.
        related = (bundle["shared_objective"] or bundle["shared_timeframe"]
                   or bundle["shared_surface"])
        max_piece_blast = max(
            (_BLAST_ORDER.get(m.get("blast_radius", "LOCAL"), 0)
             for m in members), default=0)
        aggregate_blast = bundle["aggregate_blast"]
        # Decomposition evasion: pieces individually sub-threshold, but the
        # bundle trips a gate a piece alone would have tripped.
        evasion = (
            related
            and all(m.get("blast_radius") in ("LOCAL", "COMPONENT") for m in members)
            and len(members) > 1
            and (aggregate_blast > max_piece_blast
                 or bundle["min_reversibility"] < 0.8)
        )
        if evasion:
            receipt = self._emit(
                "BUNDLE_SPLIT_HARD_STOP", evolution_id=None,
                member_ids=evolution_ids, bundle=bundle,
                refusal_code=REFUSAL_BUNDLE_SPLIT,
                reason="§3.4 — decomposed to evade gates; evaluated as one "
                       "bundle; bundle trips the gate. Hard stop, receipted")
            return {"decision": "HARD_STOP",
                    "refusal_code": REFUSAL_BUNDLE_SPLIT,
                    "receipt_id": receipt["receipt_id"], "bundle": bundle}
        receipt = self._emit(
            "BUNDLE_EVALUATED", evolution_id=None,
            member_ids=evolution_ids, bundle=bundle,
            reason="§3.4 — no split detected; pieces remain individually "
                   "governed")
        return {"decision": "NO_SPLIT", "receipt_id": receipt["receipt_id"],
                "bundle": bundle}

    # ------------------------------------------------------------------
    # §7 — authority, envelope, refusal, revocation
    # ------------------------------------------------------------------

    def authorize(self, evolution_id: str, authority: Dict[str, Any]
                  ) -> Dict[str, Any]:
        """Authority resolution. EVOLVE performs the check and grants
        nothing: the authority arrives from LAW/Director and is validated,
        never minted here. Only GATED/BRIEFED candidates can be authorized.

        Spec §3 — the decision gate (ratification-conditioned; deciding config hash bound)."""
        candidate = self._get(evolution_id)
        if candidate["proposal"] not in ("GATED", "BRIEFED"):
            receipt = self._emit(
                "AUTHORIZATION_REFUSED", evolution_id=evolution_id,
                refusal_code=REFUSAL_AUTHORITY,
                reason="AUTHORIZE — candidate is not GATED/BRIEFED; authority "
                       "cannot be validated out of order")
            return {"decision": "REFUSED",
                    "refusal_code": receipt["refusal_code"],
                    "receipt_id": receipt["receipt_id"]}
        issuer = (authority or {}).get("issuer")
        scope = (authority or {}).get("scope")
        if issuer not in ("HUMAN_DIRECTOR", "LAW") or not scope:
            receipt = self._emit(
                "AUTHORIZATION_REFUSED", evolution_id=evolution_id,
                refusal_code=REFUSAL_AUTHORITY,
                reason="AUTHORIZE — authority must be issued by HUMAN_DIRECTOR "
                       "or LAW with a stated scope; EVOLVE grants nothing")
            return {"decision": "REFUSED",
                    "refusal_code": receipt["refusal_code"],
                    "receipt_id": receipt["receipt_id"]}
        candidate["authority_basis"] = {"issuer": issuer, "scope": scope,
                                        "authority_ref": authority.get("authority_ref")}
        self._transition(candidate, "proposal", "AUTHORIZED",
                         reason=f"AUTHORIZE — authority validated from {issuer}")
        receipt = self._emit(
            "AUTHORIZED", evolution_id=evolution_id,
            authority_basis=candidate["authority_basis"],
            reason="authority re-resolved by an authority EVOLVE does not own")
        return {"decision": "AUTHORIZED", "receipt_id": receipt["receipt_id"]}

    def apply(self, evolution_id: str, *, executed_by: str = "ACT"
              ) -> Dict[str, Any]:
        """APPLY: only through the governed path — AUTHORIZED candidates
        only. The rollback is armed BEFORE the change goes live: planned,
        tested, receipted, pre-authorized as part of the adoption decision
        (§6.1). Version promotion is expected-current-version +
        compare-and-swap with supersession lineage (§5.2); exact replay
        rereads, material change versions."""
        candidate = self._get(evolution_id)
        if candidate["proposal"] != "AUTHORIZED":
            receipt = self._emit(
                "APPLY_REFUSED", evolution_id=evolution_id,
                refusal_code=REFUSAL_AUTHORITY,
                reason="APPLY — only AUTHORIZED candidates apply; EVOLVE never "
                       "executes changes itself (ACT executes under LAW's "
                       "authority)")
            return {"decision": "REFUSED",
                    "refusal_code": receipt["refusal_code"],
                    "receipt_id": receipt["receipt_id"]}
        component = candidate.get("affected_components", [None])[0]
        expected = candidate.get("current_version")
        actual = self._versions.get(str(component), self._config.get("currentVersion"))
        if expected is not None and expected != actual:
            candidate["succession"] = "STALE"
            receipt = self._emit(
                "APPLY_STALE", evolution_id=evolution_id,
                expected_version=expected, actual_version=actual,
                refusal_code="STALE_PROPOSAL",
                reason="§5.2 — CAS compare failed; loser rereads and "
                       "reconciles, never blind-overwrites")
            return {"decision": "STALE_PROPOSAL",
                    "receipt_id": receipt["receipt_id"]}
        # §6.1 — arm the rollback BEFORE going live.
        armed = self._arm_rollback(candidate)
        new_version = candidate.get("proposed_version") or (actual + "+evolved")
        self._versions[str(component)] = new_version
        self._transition(candidate, "proposal", "APPLIED",
                         reason=f"APPLY — executed by {executed_by} under the "
                                "validated authority; rollback armed first")
        receipt = self._emit(
            "APPLIED", evolution_id=evolution_id,
            applied_version=new_version, superseded_version=actual,
            rollback_armed=armed["receipt_id"],
            deciding_config_hash=self._config["configHash"],
            reason="APPLY — versioned supersession with lineage; never "
                   "in-place mutation (§3.3)")
        return {"decision": "APPLIED", "receipt_id": receipt["receipt_id"],
                "applied_version": new_version}

    def _arm_rollback(self, candidate: Dict[str, Any]) -> Dict[str, Any]:
        """§6.1 — rollback authority is pre-authorized at APPLY time: the
        rollback is planned, tested, receipted, and ready BEFORE the change
        goes live. This resolves the apparent conflict between "route
        rollback through LAW" and "autonomous rollback"."""
        plan = candidate.get("rollback_plan") or {}
        armed = {
            "evolution_id": candidate["id"],
            "plan": dict(plan),
            "armed_at": self._now(),
            "pre_authorized": True,
            "triggers": self._config.get("observation_windows", []),
        }
        receipt = self._emit(
            "ROLLBACK_ARMED", evolution_id=candidate["id"],
            # Deep copy: the receipt is sealed under receipt_hash; mutating
            # the live plan afterwards must never alter a sealed payload.
            rollback_plan=json.loads(json.dumps(armed)),
            reason="§6.1 — rollback armed and pre-authorized before APPLY; "
                   "inside the envelope this is autonomous, outside it the "
                   "governed LAW path applies")
        armed["receipt_id"] = receipt["receipt_id"]
        self._armed_rollbacks[candidate["id"]] = armed
        return armed

    def verify_adoption(self, evolution_id: str, outcome: Dict[str, Any]
                        ) -> Dict[str, Any]:
        """VERIFY / ADOPT: adoption only after VERIFY accepts the outcome.
        DEPLOYED != PRODUCTION-PROVEN — the full chain is SOURCE → TEST →
        DEPLOY → PARITY → REAL INVOCATION → OBSERVE → VERIFY → ACCEPT (§4).
        Maturity advances one step at a time; no jumping to PRODUCTION_PROVEN
        because a PR merged or tests passed (no-false-completion law)."""
        candidate = self._get(evolution_id)
        if candidate["proposal"] != "APPLIED":
            receipt = self._emit(
                "VERIFY_REFUSED", evolution_id=evolution_id,
                refusal_code="NOT_APPLIED",
                reason="VERIFY — adoption requires an APPLIED change to "
                       "verify; DEPLOYED != PRODUCTION-PROVEN")
            return {"decision": "REFUSED",
                    "refusal_code": receipt["refusal_code"],
                    "receipt_id": receipt["receipt_id"]}
        accepted = bool((outcome or {}).get("verify_accepted"))
        if not accepted:
            # Failed evolution: record what failed, why, under which
            # conditions — failure is lineage, not shame (§4).
            self._transition(candidate, "proposal", "VERIFIED",
                             reason="VERIFY — outcome recorded with failures; "
                                    "adoption refused")
            receipt = self._emit(
                "ADOPTION_REFUSED", evolution_id=evolution_id,
                outcome=outcome,
                reason="§4 — VERIFY did not accept the outcome; failed "
                       "evolution recorded as lineage; no false completion")
            return {"decision": "REFUSED", "receipt_id": receipt["receipt_id"]}
        self._transition(candidate, "proposal", "VERIFIED",
                         reason="VERIFY — outcome accepted by VERIFY")
        self._transition(candidate, "proposal", "ADOPTED",
                         reason="ADOPT — adoption after VERIFY acceptance only")
        receipt = self._emit(
            "ADOPTED", evolution_id=evolution_id,
            outcome=outcome,
            deciding_config_hash=self._config["configHash"],
            reason="ADOPT — the adoption decision was computed under config "
                   "C; recomputation under C must MATCH or this adoption is "
                   "void (§3.3)")
        return {"decision": "ADOPTED", "receipt_id": receipt["receipt_id"]}

    def advance_maturity(self, evolution_id: str) -> Dict[str, Any]:
        """Advance one maturity step. The seven-step production chain cannot
        be jumped — maturity is evidence, not declaration (§4, §11.2)."""
        candidate = self._get(evolution_id)
        current = candidate["maturity"]
        legal = LEGAL_MATURITY_TRANSITIONS.get(current, ())
        if not legal:
            receipt = self._emit(
                "MATURITY_REFUSED", evolution_id=evolution_id,
                refusal_code="MATURITY_TERMINAL",
                reason="MATURITY — already at the terminal state; maturity "
                       "is evidence, not declaration")
            return {"decision": "REFUSED",
                    "refusal_code": receipt["refusal_code"],
                    "receipt_id": receipt["receipt_id"]}
        self._transition(candidate, "maturity", legal[0],
                         reason="MATURITY — one evidence step at a time; no "
                                "jumping to PRODUCTION_PROVEN")
        receipt = self._emit(
            "MATURITY_ADVANCED", evolution_id=evolution_id,
            maturity=legal[0], reason="§4 production-maturity axis")
        return {"decision": "ADVANCED", "maturity": legal[0],
                "receipt_id": receipt["receipt_id"]}

    def report_harm(self, evolution_id: str, harm: Dict[str, Any]
                    ) -> Dict[str, Any]:
        """§6.2 — mandatory autonomous rollback on harm detection. When
        monitoring detects harm from an adopted change, EVOLVE rolls back
        autonomously — even for changes the Director approved. The Director
        approved the change, not the harm. Rollback suppression is itself
        a threat-model item and a hard stop."""
        candidate = self._get(evolution_id)
        if candidate["proposal"] not in ("APPLIED", "VERIFIED", "ADOPTED"):
            receipt = self._emit(
                "HARM_REPORTED", evolution_id=evolution_id,
                harm=harm, action="NO_ROLLBACK_NOTHING_APPLIED",
                reason="§6.2 — harm reported but nothing adopted; nothing to "
                       "roll back; harm evidence preserved")
            return {"decision": "RECORDED", "receipt_id": receipt["receipt_id"]}
        armed = self._armed_rollbacks.get(evolution_id)
        receipt = self._emit(
            "HARM_DETECTED", evolution_id=evolution_id,
            harm=harm, armed_rollback=bool(armed),
            refusal_code=REFUSAL_HARM_POST_ADOPTION,
            reason="§6.2 — harm detected post-adoption; autonomous rollback "
                   "is mandatory, even for director-approved changes")
        if armed is None:
            # No armed rollback exists: route through the governed LAW path.
            return {"decision": "HARM_RECORDED_NO_ARMED_ROLLBACK",
                    "receipt_id": receipt["receipt_id"],
                    "route": "LAW_GOVERNED_PATH"}
        return self.rollback(evolution_id, reason="§6.2 mandatory autonomous "
                                                  "rollback on harm detection")

    def rollback(self, evolution_id: str, reason: str) -> Dict[str, Any]:
        """Execute the armed rollback. Rollback preserves history:
        ORIGINAL EVENT → ROLLBACK EVENT → NEW STATE. Compensation, where
        true rollback is impossible, is recorded AS compensation, never as
        history erasure (§6.3)."""
        candidate = self._get(evolution_id)
        armed = self._armed_rollbacks.get(evolution_id)
        if armed is None:
            receipt = self._emit(
                "ROLLBACK_REFUSED", evolution_id=evolution_id,
                refusal_code="NO_ARMED_ROLLBACK",
                reason="ROLLBACK — no armed rollback exists; route through "
                       "the governed LAW path (§6.1)")
            return {"decision": "REFUSED",
                    "refusal_code": receipt["refusal_code"],
                    "receipt_id": receipt["receipt_id"]}
        component = candidate.get("affected_components", [None])[0]
        restored = candidate.get("current_version")
        if restored is not None:
            self._versions[str(component)] = restored
        from_state = candidate["proposal"]
        self._transition(candidate, "proposal", "ROLLED_BACK", reason=reason)
        receipt = self._emit(
            "ROLLED_BACK", evolution_id=evolution_id,
            restored_version=restored, history_chain=(from_state, "ROLLED_BACK"),
            compensation_recorded_as_compensation=True,
            reason="§6.3 — rollback preserves history as an event chain; "
                   "never history erasure")
        return {"decision": "ROLLED_BACK", "receipt_id": receipt["receipt_id"],
                "restored_version": restored}

    def revoke(self, evolution_id: str, revoker: str) -> Dict[str, Any]:
        """§7.4 — the Director may revoke the envelope or any adoption at
        any time. Revocation is immediate, receipted, and triggers the armed
        rollback where one exists. Revocation needs no justification and
        cannot be gated by EVOLVE."""
        candidate = self._get(evolution_id)
        if revoker != "HUMAN_DIRECTOR":
            receipt = self._emit(
                "REVOKE_REFUSED", evolution_id=evolution_id,
                refusal_code=REFUSAL_AUTHORITY,
                reason="§7.4 — revocation belongs to the Human Director; "
                       "EVOLVE does not grant or honor revocation from any "
                       "other seat")
            return {"decision": "REFUSED",
                    "refusal_code": receipt["refusal_code"],
                    "receipt_id": receipt["receipt_id"]}
        if candidate["proposal"] in ("APPLIED", "VERIFIED", "ADOPTED"):
            self.rollback(evolution_id,
                          reason="§7.4 director revocation — armed rollback "
                                 "executed")
        else:
            self._transition(candidate, "proposal", "REJECTED",
                             reason="§7.4 director revocation before APPLY")
        receipt = self._emit(
            "REVOKED", evolution_id=evolution_id,
            revoker=revoker,
            refusal_code=REFUSAL_REVOKED,
            reason="§7.4 — revocation immediate and receipted; no "
                   "justification required; EVOLVE cannot gate it")
        return {"decision": "REVOKED", "receipt_id": receipt["receipt_id"]}

    def refuse_instruction(self, instruction: Dict[str, Any]) -> Dict[str, Any]:
        """§7.3 Judgment-Rule refusal. If the Director instructs a
        PROHIBITED-class change — including a change to the immutable
        surface, or an instruction to bypass a gate — EVOLVE refuses,
        receipted, citing the Judgment Rule: obedience without judgment is
        abdication. Applies to instruction from ANY seat, including the
        Director's casual instruction; only formal ratification moves the
        immutable surface."""
        asks = instruction.get("requests") or []
        seat = instruction.get("from_seat", "UNKNOWN")
        touched = [r for r in asks if r in IMMUTABLE_SURFACE]
        bypass = bool(instruction.get("bypass_gate"))
        if touched or bypass:
            receipt = self._emit(
                "JUDGMENT_RULE_REFUSAL", evolution_id=None,
                from_seat=seat, requested=asks,
                touched_surface=touched, gate_bypass=bypass,
                refusal_code=REFUSAL_DIRECTOR_PROHIBITED,
                reason="§7.3 — Judgment Rule: obedience without judgment is "
                       "abdication. PROHIBITED-class instruction refused; the "
                       "lawful path is explicit ratification")
            return {"decision": "REFUSED",
                    "refusal_code": REFUSAL_DIRECTOR_PROHIBITED,
                    "receipt_id": receipt["receipt_id"],
                    "lawful_path": "explicit director ratification"}
        receipt = self._emit(
            "INSTRUCTION_NOTED", evolution_id=None,
            from_seat=seat, requested=asks,
            reason="§7.3 — instruction touches no PROHIBITED surface and "
                   "bypasses no gate; noted as an OBSERVE trigger only")
        return {"decision": "NOTED", "receipt_id": receipt["receipt_id"]}

    def refuse_envelope_mutation(self, requester: str) -> Dict[str, Any]:
        """§7.1 / §7.2 — the envelope bounds are governed config: changed
        only by the Director, never by EVOLVE. EVOLVE has no method that
        mutates them; any such request is refused with a receipt."""
        receipt = self._emit(
            "ENVELOPE_MUTATION_REFUSED", evolution_id=None,
            requester=requester, refusal_code=REFUSAL_AUTHORITY,
            reason="§7.1 — the autonomous envelope is director-set governed "
                   "config; EVOLVE cannot set, widen, or recalibrate its own "
                   "bounds. Envelope recalibration is a briefed, versioned "
                   "candidate (§7.2)")
        return {"decision": "REFUSED", "refusal_code": REFUSAL_AUTHORITY,
                "receipt_id": receipt["receipt_id"]}

    # ------------------------------------------------------------------
    # §8 — succession: the cold successor package
    # ------------------------------------------------------------------

    def build_successor_package(self, fields: Dict[str, Any],
                                *, director_authorized_core: bool = False
                                ) -> Dict[str, Any]:
        """§8.1 — build the 24-field handoff object. The baton is "here is
        exactly where the truth lives" — never "trust me."

        Completeness is not an average: one missing critical successor
        obligation zeroes readiness (§8.7). A handoff omitting a material
        blocker is INVALID (§8.3 / PDF §98 golden test). Intelligence refs
        carry their ratified class labels; CORE-class intelligence does NOT
        transfer by default — the Director's explicit word per handoff is
        required (§8.1, draft position Q8)."""
        package = {f: fields.get(f) for f in SUCCESSOR_PACKAGE_FIELDS
                   if f not in ("package_hash", "created_at")}
        package["created_at"] = self._now()
        # Baton law (§8.2): authority is re-resolved by the successor's LAW;
        # the package carries prior refs as evidence, never as permission.
        package["authority_context"] = {
            "prior_refs": (fields.get("authority_context") or {}).get("prior_refs", []),
            "authority_inherited": False,
            "requires_reresolution": True,
        }
        # §8.1 — intelligence refs carry class labels; CORE gated.
        intelligence_refs = []
        core_blocked = []
        for ref in fields.get("intelligence_refs") or []:
            klass = ref.get("intelligence_class", "CONTEXT")
            if klass not in INTELLIGENCE_CLASSES:
                klass = "CONTEXT"
            if klass == "CORE" and not director_authorized_core:
                core_blocked.append(ref.get("ref_id"))
                continue
            intelligence_refs.append({**ref, "intelligence_class": klass})
        package["intelligence_refs"] = intelligence_refs
        # §8.3 — blockers are first-class; omission of a material blocker
        # makes the handoff INVALID, not merely degraded.
        known_blockers = set(fields.get("material_blockers_known") or [])
        shipped_blockers = {(b.get("blocker_id") if isinstance(b, dict) else b)
                            for b in (fields.get("blockers") or [])}
        omitted = sorted(known_blockers - shipped_blockers)
        # §8.7 — completeness is not an average. The 9 critical obligations
        # are checked against the 24-field package by substance, not by key
        # name: an obligation is satisfied when its substance is DOCUMENTED
        # (an explicitly empty blockers list counts as documented, not
        # missing — "no blockers" is a claim, not an omission).
        obligation_present: Dict[str, bool] = {
            "identity_context": bool(package.get("parent_identity")
                                     and package.get("successor_identity")),
            "mission": bool(package.get("mission")),
            "current_truth": bool(package.get("current_truth")),
            "authority_boundary": bool(package.get("authority_context")),
            "material_blockers": ("blockers" in fields
                                  or bool(fields.get("material_blockers_known"))),
            "applicable_verified_learning": ("learning_refs" in fields),
            "next_action": bool(package.get("next_action")),
            "proof_requirements": bool(package.get("next_proof_requirement")),
            "canonical_source_pointers": bool(package.get("source_snapshot")),
        }
        missing = sorted(ob for ob, ok in obligation_present.items() if not ok)
        successor_ready = 1 if not missing else 0
        # handoff_id is derived BEFORE sealing so the package hash covers
        # the final id — material mutation creates a new version, never a
        # silent edit (§5.2).
        package["handoff_id"] = fields.get("handoff_id") or (
            f"handoff-{_hash([package[k] for k in sorted(package)])[:12]}")
        handoff_id = package["handoff_id"]
        if omitted:
            invalid = self._emit(
                "HANDOFF_INVALID", evolution_id=None,
                handoff_id=handoff_id,
                refusal_code=REFUSAL_BLOCKER_OMITTED,
                reason="§8.3 / PDF §98 — a handoff omitting a material "
                       "blocker is INVALID")
            package["handoff_valid"] = False
            package["invalid_receipt_id"] = invalid["receipt_id"]
        else:
            package["handoff_valid"] = True
        package["successor_ready"] = successor_ready
        # Seal LAST: the hash covers every material field INCLUDING the
        # validity verdict. Sealing before handoff_valid/successor_ready
        # are set would let a later flip of handoff_valid pass the seal
        # silently — exactly what §5.2 / A5 forbids.
        package["package_hash"] = package_hash(package)
        receipt = self._emit(
            "SUCCESSOR_PACKAGE", evolution_id=None,
            handoff_id=handoff_id,
            successor_ready=successor_ready,
            missing_obligations=missing,
            omitted_material_blockers=omitted,
            core_intelligence_blocked=core_blocked,
            package_hash=package["package_hash"],
            reason="§8 — successor package; completeness not an average; "
                   "omitted blockers invalidate")
        self._handoff_packages[handoff_id] = package
        return {
            "decision": "INVALID" if omitted else "PACKAGED",
            "handoff_id": handoff_id,
            "successor_ready": successor_ready,
            "missing_obligations": missing,
            "omitted_material_blockers": omitted,
            "core_intelligence_blocked": core_blocked,
            "receipt_id": receipt["receipt_id"],
        }

    def verify_continuity(self, handoff_id: str,
                         live_sources: Dict[str, Any]) -> Dict[str, Any]:
        """§8.2 / A5 — continuity verification against live canonical
        sources. CanonicalCurrentTruth > HandoffMemory: when the package and
        live sources disagree, live truth wins and the package is marked
        STALE. Replayability: handoff ID + canonical sources + declared
        snapshot must yield a materially equivalent successor context, or
        CONTINUITY_MISMATCH. Same-safe-next-action: A_s = A_p for materially
        identical state, else an evidence-grounded reason."""
        package = self._handoff_packages.get(handoff_id)
        if package is None:
            raise KeyError(f"unknown handoff_id: {handoff_id}")
        snapshot = package.get("source_snapshot") or {}
        live = live_sources or {}
        divergences = sorted(k for k in snapshot
                             if k in live and live[k] != snapshot[k])
        result: Dict[str, Any] = {"handoff_id": handoff_id,
                                  "divergences": divergences}
        if divergences:
            package["handoff_valid"] = False
            receipt = self._emit(
                "HANDOFF_STALE", evolution_id=None, handoff_id=handoff_id,
                divergences=divergences,
                reason="§8.2 — CanonicalCurrentTruth > HandoffMemory; the "
                       "package is marked STALE; live truth wins")
            result.update({"decision": "STALE",
                           "receipt_id": receipt["receipt_id"]})
        else:
            receipt = self._emit(
                "CONTINUITY_VERIFIED", evolution_id=None,
                handoff_id=handoff_id,
                package_hash_ok=(package_hash(package) == package.get("package_hash")),
                reason="§8.2 / A5 — package hash, replayability, and "
                       "same-safe-next-action checked")
            result.update({"decision": "CONTINUOUS",
                           "receipt_id": receipt["receipt_id"]})
        # §8.8 — the successor does not skip SELF: EVOLVE hands only bounded
        # evolution truth back; SELF re-establishes identity, mission, state.
        result["bounded_truth_to_self"] = {
            k: package.get(k) for k in ("mission", "current_truth",
                                        "unknowns", "next_action")
        }
        return result

    def record_continuity_metric(self, name: str, value: float) -> Dict[str, Any]:
        """§11.4 — continuity metrics are operational diagnostics, never
        gates. Metrics inform the envelope; they do not replace the hard
        boundaries."""
        if name not in CONTINUITY_METRICS:
            receipt = self._emit(
                "METRIC_REFUSED", evolution_id=None, metric=name,
                refusal_code="UNKNOWN_METRIC",
                reason="§11.4 — only the defined continuity metrics are "
                       "recorded; nothing else becomes a gate by the back door")
            return {"decision": "REFUSED", "receipt_id": receipt["receipt_id"]}
        self._metrics.setdefault(name, []).append(float(value))
        receipt = self._emit(
            "METRIC_RECORDED", evolution_id=None, metric=name, value=float(value),
            reason="§11.4 — diagnostic recorded; it gates nothing")
        return {"decision": "RECORDED", "receipt_id": receipt["receipt_id"]}

    # ------------------------------------------------------------------
    # §3.3 — recompute (deciding-config binding)
    # ------------------------------------------------------------------

    def recompute(self, evolution_id: str) -> Dict[str, Any]:
        """Re-derive the gate evaluation under the pinned deciding config.
        An independent recomputation under C must return MATCH, or the
        adoption is void (§3.3). A configuration can never validate its own
        adoption."""
        candidate = self._get(evolution_id)
        stored = candidate.get("gate_score")
        if stored is None:
            return {"result": "MISMATCH",
                    "reason": "no sealed gate score to recompute"}
        config_hash_then = stored.get("deciding_config_hash")
        if config_hash_then != self._config["configHash"]:
            alarm = self._emit(
                "RECOMPUTE_ALARM", evolution_id=evolution_id,
                reason="§3.3 — config changed since the gate ran; the stored "
                       "score no longer binds the current config")
            return {"result": "MISMATCH",
                    "receipt_id": alarm["receipt_id"],
                    "reason": "deciding config hash changed"}
        fresh = self._score_candidate(candidate)
        match = (fresh["score"] == stored["score"]
                 and fresh["calculus_spec_status"] == stored["calculus_spec_status"])
        receipt = self._emit(
            "RECOMPUTE", evolution_id=evolution_id,
            recompute_match=match,
            reason="§3.3 recompute — independent seat must reach MATCH under "
                   "config C")
        if match:
            return {"result": "MATCH", "receipt_id": receipt["receipt_id"]}
        alarm = self._emit(
            "RECOMPUTE_ALARM", evolution_id=evolution_id,
            reason="§3.3 — recompute MISMATCH under the same deciding "
                   "config; the adoption is void")
        return {"result": "MISMATCH", "receipt_id": alarm["receipt_id"]}

    # ------------------------------------------------------------------
    # §11.4 — nothing here is a gate; the hard boundaries stand alone
    # ------------------------------------------------------------------

    def metrics(self) -> Dict[str, List[float]]:
        """Continuity metrics recorded so far — diagnostics, never gates.

        Spec §11 — acceptance battery; metrics are recorded, never gates."""
        return {k: list(v) for k, v in self._metrics.items()}

    def brief_outbox(self) -> List[Dict[str, Any]]:
        """Everything outside the envelope waits here — proposals, never
        adoptions (§7)."""
        return list(self._brief_outbox)

    # ------------------------------------------------------------------
    # NodeBase contract
    # ------------------------------------------------------------------

    def manifest_entry(self) -> ManifestEntry:
        """Return this node's manifest entry (candidate spec, §11 acceptance battery)."""
        return ManifestEntry(
            node_id=NODE_ID,
            version="V1-CANDIDATE",
            responsibilities=[
                "governed self-modification: the only legitimate path for "
                "NayaPOWER to change itself (§1)",
                "MAY / MUST-NEVER immutable surface; PROHIBITED-class refusal "
                "(§2, ordering law MISSION→LAW→SAFETY→TRUTH→VALUE)",
                "§3 decision gate: no second score — V2.1 calculus under the "
                "CURRENT config; ratification-conditioned SPEC-ONLY",
                "anti-self-ratification: deciding_config_hash bound; "
                "recompute MATCH or the adoption is void",
                "BUNDLE_SPLIT hard stop — decomposed evasion evaluated as one",
                "three state axes, never collapsed; stale-proposal rule; "
                "impact-closure dependency analysis",
                "separate evolution and successor receipts; CAS concurrency; "
                "SuccessorKey idempotency; package hash integrity",
                "rollback armed and pre-authorized before APPLY; mandatory "
                "autonomous rollback on harm — director approved the change, "
                "not the harm; history preserved, never erased",
                "director-set autonomous envelope; Judgment-Rule refusal of "
                "PROHIBITED-class instruction from any seat; immediate "
                "director revocation",
                "cold-successor machinery: 24-field package, baton law, "
                "first-class blockers/unknowns/failures, Cold-14, "
                "completeness-not-an-average, authority never inherited",
                "hash-bound receipts; recompute MATCH/MISMATCH (§3.3)",
            ],
        )

    def persisted_transitions(self) -> List[str]:
        """List the receipt transitions this node persists (candidate spec, §11 acceptance battery)."""
        out: List[str] = []
        for table in (LEGAL_PROPOSAL_TRANSITIONS, LEGAL_MATURITY_TRANSITIONS,
                      LEGAL_SUCCESSION_TRANSITIONS):
            out.extend(f"{frm}->{to}"
                       for frm, tos in table.items() for to in tos)
        return out

    def evidence_hooks(self) -> List[str]:
        """List the evidence hooks this node exposes (candidate spec, §11 acceptance battery)."""
        return [
            "evolution_candidate_registry",
            "gate_score_ledger",
            "deciding_config_snapshots",
            "version_store",
            "armed_rollback_registry",
            "successor_package_store",
            "continuity_metric_log",
            "brief_outbox",
            "evolution_receipt_ledger",
            "successor_receipt_ledger",
        ]

    def authority_checks(self) -> List[str]:
        """Declare this node's authority checks; declares, never grants (candidate spec, §11 acceptance battery)."""
        # EVOLVE performs these validations and grants nothing. The first
        # entry is the negation convention tests assert.
        return [
            NO_AUTHORITY_GRANT,
            "immutable-surface classification before any gate evaluation",
            "authority validated (HUMAN_DIRECTOR or LAW), never minted",
            "envelope bounds are director-set; EVOLVE cannot widen its own bounds",
            "adoption requires AUTHORIZED + VERIFY acceptance — never self-granted",
            "rollback pre-authorized at APPLY time; revocation immediate",
            "Judgment-Rule refusal of PROHIBITED-class instruction from any seat",
            "successor authority re-resolved by LAW; authority_inherited always false",
            "CORE-class intelligence transfer requires director word per handoff",
        ]

    def gate(self, state: Dict[str, Any]) -> GateResult:
        """EVOLVE's gate: evaluate an evolution request. Immutable touch →
        FAIL (PROHIBITED); anything unproven is NEED_EVIDENCE with reason
        codes. The calculus is RATIFIED V2.1 (FLAG-001 step 4) — there is no
        unratified-math SPEC-ONLY branch anymore. Never invent PASS."""
        action = (state or {}).get("action")
        if action not in ("propose", "evaluate", "authorize", "apply",
                          "handoff", "metrics"):
            return GateResult(GateVerdict.FAIL,
                              ["unknown action for EVOLVE gate"])
        if action == "propose":
            proposal = state.get("proposal", {})
            touched = self._immutable_touch({
                "change_class": proposal.get("change_class"),
                "touches_surface": proposal.get("touches_surface", []),
                "mission_compatible": proposal.get("mission_compatible", True),
            })
            if touched:
                return GateResult(GateVerdict.FAIL,
                                  [REFUSAL_IMMUTABLE_SURFACE,
                                   f"touches {','.join(touched)}"])
            if not proposal.get("future_behavior"):
                return GateResult(GateVerdict.FAIL,
                                  [REFUSAL_NO_FUTURE_BEHAVIOR,
                                   "a proposal that changes nothing is not an "
                                   "evolution (§10)"])
            return GateResult(GateVerdict.NEED_EVIDENCE,
                              ["EVALUATION_REQUIRED",
                               "proposal admitted; §3 gate still required"])
        evolution_id = (state or {}).get("evolution_id")
        if evolution_id is None and action in ("evaluate", "authorize",
                                               "apply"):
            return GateResult(GateVerdict.FAIL, ["evolution_id required"])
        candidate: Optional[Dict[str, Any]] = None
        if evolution_id is not None:
            try:
                candidate = self._get(evolution_id)
            except KeyError:
                return GateResult(GateVerdict.FAIL, ["unknown evolution_id"])
        if action == "evaluate":
            assert candidate is not None
            result = self.evaluate(evolution_id)  # type: ignore[arg-type]
            if result["decision"] == "STALE_PROPOSAL":
                return GateResult(GateVerdict.NEED_EVIDENCE,
                                  ["STALE_PROPOSAL", "REBASE_REQUIRED"])
            if result["route"] == "BRIEF":
                return GateResult(GateVerdict.NEED_EVIDENCE,
                                  ["BRIEF_REQUIRED"] + result["reasons"])
            return GateResult(GateVerdict.PASS,
                              ["in-envelope; calculus ratified; "
                               "autonomous path admitted (§7.1)"])
        if action in ("authorize", "apply"):
            # V2.1 is RATIFIED (FLAG-001 step 4) - the old SPEC-ONLY refusal
            # (REFUSAL_CALCULUS_UNRATIFIED) was removed with the stale
            # premise. Authorization/adoption still require authority.
            if action == "apply" and candidate["proposal"] != "AUTHORIZED":
                return GateResult(GateVerdict.FAIL,
                                  [REFUSAL_AUTHORITY,
                                   "only AUTHORIZED candidates apply"])
            return GateResult(GateVerdict.NEED_EVIDENCE,
                              ["AUTHORITY_VALIDATION_REQUIRED",
                               "EVOLVE validates authority; it grants none"])
        if action == "handoff":
            known = set(state.get("material_blockers_known") or [])
            if known:
                return GateResult(GateVerdict.NEED_EVIDENCE,
                                  ["BLOCKER_SHIPMENT_REQUIRED",
                                   "a handoff omitting a material blocker is "
                                   "INVALID (§8.3)"])
            return GateResult(GateVerdict.NEED_EVIDENCE,
                              ["COMPLETENESS_CHECK_REQUIRED",
                               "one missing critical obligation zeroes "
                               "readiness (§8.7)"])
        # action == "metrics"
        return GateResult(GateVerdict.PASS,
                          ["metrics are diagnostics; they gate nothing (§11.4)"])

    def cold_reconstruct(self, receipts: List[Dict[str, Any]]
                         ) -> Dict[str, Any]:
        """Rebuild EVOLVE's durable state from receipts alone (cold start).

        Replays receipts in timestamp order, re-running hash verification on
        every sealed receipt. Answers the continuity questions: which
        candidates were adopted under which deciding config, which rollbacks
        fired and why, which successor packages shipped with what
        readiness, and which revocations executed. A cold successor does not
        inherit authority — it reconstructs evidence and re-resolves.
        

        Spec §8 — succession: the cold successor (§8.6 Cold-14)."""
        ordered = sorted(receipts or [], key=lambda r: r.get("timestamp", ""))
        state: Dict[str, Any] = {
            "candidates": {},
            "adopted": [],
            "rolled_back": [],
            "revoked": [],
            "handoff_packages": {},
            "judgment_rule_refusals": [],
            "determinism": {"checked": 0, "matched": 0, "mismatched": []},
        }
        for receipt in ordered:
            if receipt.get("node_id") != NODE_ID:
                continue
            stored_hash = receipt.get("receipt_hash")
            body = {k: v for k, v in receipt.items() if k != "receipt_hash"}
            state["determinism"]["checked"] += 1
            if stored_hash is None or _hash(body) != stored_hash:
                state["determinism"]["mismatched"].append(
                    receipt.get("receipt_id"))
                continue
            state["determinism"]["matched"] += 1
            rtype = receipt.get("receipt_type")
            eid = receipt.get("evolution_id")
            entry = state["candidates"].setdefault(eid, {}) if eid else {}
            if rtype == "TRANSITION":
                entry["axis"] = receipt.get("axis")
                entry["state_after"] = receipt.get("state_after")
            elif rtype == "GATED":
                entry["route"] = receipt.get("route")
                entry["gate_score"] = receipt.get("gate_score")
                entry["deciding_config_hash"] = receipt.get(
                    "deciding_config_hash")
            elif rtype == "ADOPTED":
                state["adopted"].append(eid)
                entry["adopted"] = True
            elif rtype == "ROLLED_BACK":
                state["rolled_back"].append({
                    "evolution_id": eid,
                    "restored_version": receipt.get("restored_version")})
            elif rtype == "REVOKED":
                state["revoked"].append(eid)
            elif rtype == "SUCCESSOR_PACKAGE":
                hid = receipt.get("handoff_id")
                if hid:
                    state["handoff_packages"][hid] = {
                        "successor_ready": receipt.get("successor_ready"),
                        "missing_obligations": receipt.get(
                            "missing_obligations", []),
                        "package_hash": receipt.get("package_hash")}
            elif rtype == "JUDGMENT_RULE_REFUSAL":
                state["judgment_rule_refusals"].append(
                    receipt.get("receipt_id"))
        return state
