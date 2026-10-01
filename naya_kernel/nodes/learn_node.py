"""NAYA-KERNEL-LEARN — candidate implementation (CANDIDATE — NOT RATIFIED — NOT MERGED).

Contractual responsibility, from LEARN-NODE-SPEC-CANDIDATE.md §0:

    LEARN is NayaPOWER's governed behavioral-improvement organ. It converts
    evidence-bearing outcomes into scoped learning candidates, reconciles them
    with existing intelligence, tests their applicability and behavioral effect,
    promotes only justified learning, preserves contradiction and negative
    evidence, measures prediction/calibration error and future reuse, and
    produces versioned learning state for EVOLVE — without ever turning memory,
    retrieval, confidence, value, or learning into authority.

    Master learning law: STORED != LEARNED. A defensible learning claim requires
    a future behavioral consequence: Learning(L) => FutureBehavior_with_L !=
    FutureBehavior_without_L when L is applicable.

Implemented from the reconciled LEARN spec (branch specs/
LEARN-NODE-SPEC-CANDIDATE.md + the full base text in
hidden_files/specs-final/LEARN-NODE-SPEC-CANDIDATE.md). All math that depends
on the Decision Value Calculus is computed under the pinned config; the
calculus is RATIFIED V2.1 (condition 0 satisfied — see the binding in
naya_kernel.node_base), so a fully-eligible learning may promote
autonomously; the receipt says exactly which calculus config hash decided.

This module is candidate code on the naya4/nine-node-kernel-v1 branch. It is
NOT ratified, NOT merged, NOT deployed.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, Tuple

from naya_kernel.node_base import (
    NodeBase, GateResult, GateVerdict, ManifestEntry,
    CALCULUS_V21_VERSION, CALCULUS_V21_SPEC_HASH,
)


NODE_ID = "NAYA-KERNEL-LEARN"
NODE_MN = "MN-08"
NO_AUTHORITY_GRANT = "no_authority_granted_by_learn"

# The VERIFY node identity LEARN trusts. Imported nowhere — this is a literal
# because learn_node must not import verify_node (no cross-node import; the
# resolver is injected by runtime composition).
VERIFY_NODE_ID = "NAYA-KERNEL-VERIFY"

# ---------------------------------------------------------------------------
# VERIFY→LEARN trust seam (Coda 1 design verdict #554/5937954809, C1–C6).
#
# SECURITY INVARIANT: LEARN can consume verification. It can never create,
# infer, or manufacture it — including when the caller asserts the object
# came from VERIFY.
# ---------------------------------------------------------------------------

# C3 — explicit allowlist of security-relevant fields compared between the
# caller-presented receipt and the VERIFY-resolved receipt. Whole-dict
# equality is brittle and fails open on new keys; fields outside this list
# are never trusted for the intake decision.
_VERIFY_INTAKE_COMPARE_FIELDS = (
    "id",
    "node_id",
    "verification_state",
    "outcome_status",
    "acceptance_decision",
    "causal_status",
    "subject_ref",
    "supersedes",
    "reopened_by",
    "evidence_refs",
    "verify_key",
    "receipt_hash",
)

# C6 — structural fields every genuine VERIFY receipt carries (emitted by
# VerifyNode._new_receipt). A direct dict-write forgery into VERIFY's store
# typically omits or mistypes these; the ownership proof below refuses it.
_VERIFY_RECEIPT_STRUCTURE_FIELDS = (
    "node_version",
    "verify_key",
    "verify_version",
    "kind",
    "subject_ref",
    "outcome_status",
    "acceptance_decision",
    "causal_status",
    "verification_state",
    "issued_at",
    "issued_by",
)

# Genuine VERIFY receipt IDs are content commitments:
# "vr-" + 16 hex chars (hash of [verify_key, seq]).
_VERIFY_RECEIPT_ID_RE = re.compile(r"^vr-[0-9a-f]{16}$")

# ---------------------------------------------------------------------------
# Vocabulary (spec §2, §8, §6.3, §9)
# ---------------------------------------------------------------------------

LEARNING_TYPES = (
    "BEHAVIOR_RULE",
    "FACT_UPDATE",
    "APPLICABILITY_REFINEMENT",
    "CALIBRATION_UPDATE",
    "RECALIBRATION",
    "GOVERNANCE_PROPOSAL",
    "ASSOCIATION",
)

# Four axes (§8 — dimensions, not states)
EPISTEMIC = (
    "CANDIDATE", "TESTING", "SUPPORTED", "VERIFIED",
    "CONTRADICTED", "REJECTED", "SUPERSEDED",
)
ADOPTION = ("INACTIVE", "ACTIVE", "RETIRED", "ROLLED_BACK")
TRANSFER_MATURITY = (
    "UNTESTED", "SOURCE_TASK_ONLY", "HELD_OUT_RELATED_SUPPORTED",
    "BOUNDED_GENERALIZATION", "COMPOUNDING_SUPPORTED", "SUCCESSOR_RETAINED",
)
APPLICABILITY = ("APPLICABLE", "NOT_APPLICABLE", "UNKNOWN")

# Lifecycle state machine (§8)
STATES = (
    "UNINITIALIZED", "CANDIDATE", "RECONCILING", "TEST_REQUIRED", "TESTING",
    "EVIDENCE_REVIEW", "VERIFIED", "PROMOTION_READY", "ACTIVE",
    "DEFERRED", "REJECTED", "CONTRADICTED", "SUPERSEDED", "REGRESSED",
    "ROLLED_BACK", "INCONCLUSIVE", "BLOCKED", "RETIRED",
)

LEGAL_TRANSITIONS = {
    "UNINITIALIZED": ("CANDIDATE",),
    "CANDIDATE": ("RECONCILING", "DEFERRED", "REJECTED", "BLOCKED"),
    "RECONCILING": ("TEST_REQUIRED", "BLOCKED", "CONTRADICTED", "REJECTED", "CANDIDATE"),
    "TEST_REQUIRED": ("TESTING", "BLOCKED", "REJECTED"),
    "TESTING": ("EVIDENCE_REVIEW", "BLOCKED"),
    "EVIDENCE_REVIEW": ("VERIFIED", "INCONCLUSIVE", "CONTRADICTED"),
    "VERIFIED": ("PROMOTION_READY",),
    "PROMOTION_READY": ("ACTIVE", "DEFERRED"),
    "DEFERRED": ("CANDIDATE", "REJECTED"),
    "ACTIVE": ("REGRESSED", "SUPERSEDED", "ROLLED_BACK", "RETIRED"),
    "REGRESSED": ("ACTIVE", "RETIRED"),
    "CONTRADICTED": ("RECONCILING", "SUPERSEDED"),
    "BLOCKED": ("RECONCILING", "REJECTED"),
    "INCONCLUSIVE": ("CANDIDATE",),
    "ROLLED_BACK": ("CANDIDATE",),
    "SUPERSEDED": (),
    "REJECTED": (),
    "RETIRED": (),
}

RECONCILIATION_CLASSES = (
    "NEW", "EXACT_DUPLICATE", "REFINEMENT", "SCOPE_NARROWING",
    "SCOPE_EXPANSION_CANDIDATE", "CONTRADICTION", "CORRECTION",
    "SUPERSEDES", "PARALLEL_DIFFERENT_SCOPE", "UNKNOWN",
)

# Seven hard refusal conditions (§4) + §4.8 self-dealing.
REFUSAL_NO_FUTURE_BEHAVIOR = "NO_FUTURE_BEHAVIOR_NAMED"
REFUSAL_CONTRADICTION = "CONTRADICTS_ACTIVE_LEARNING"
REFUSAL_AUTHORITY_SMUGGLING = "AUTHORITY_SMUGGLING"
REFUSAL_CONSTITUTIONAL = "CONSTITUTIONAL_TOUCH"
REFUSAL_OPEN_HARM_WINDOW = "OPEN_HARM_WINDOW"
REFUSAL_PROVENANCE = "PROVENANCE_FAILURE"
REFUSAL_SELF_MODIFICATION = "RECURSIVE_SELF_MODIFICATION"
REFUSAL_SELF_DEALING = "SELF_DEALING_UNCERTAINTY"
HARD_REFUSALS = (
    REFUSAL_NO_FUTURE_BEHAVIOR, REFUSAL_CONTRADICTION,
    REFUSAL_AUTHORITY_SMUGGLING, REFUSAL_CONSTITUTIONAL,
    REFUSAL_OPEN_HARM_WINDOW, REFUSAL_PROVENANCE,
    REFUSAL_SELF_MODIFICATION, REFUSAL_SELF_DEALING,
)

# The 14 reason-coded non-promotions (§9). (The former 15th code,
# CALCULUS_NOT_RATIFIED — condition 0 — was removed by FLAG-001 step 4:
# Decision Value Calculus V2.1 is RATIFIED, so condition 0 is satisfied.)
NON_PROMOTION_CODES = (
    "VERIFY_RESULT_REQUIRED", "OUTCOME_NOT_ACCEPTED", "CAUSAL_SUPPORT_REQUIRED",
    "PROVENANCE_INCOMPLETE", "CONTRADICTS_ACTIVE_LEARNING",
    "APPLICABILITY_UNKNOWN", "HELDOUT_REQUIRED", "NO_BEHAVIORAL_DELTA",
    "NO_OUTCOME_DELTA", "NEGATIVE_TRANSFER_FAILED", "REGRESSION_DETECTED",
    "EVIDENCE_REFERENCE_UNRESOLVED", "SCOPE_MISMATCH",
    "AUTHORITY_BOUNDARY_VIOLATION",
)
EXTRA_CODES = (
    "EVIDENCE_FLOOR_NOT_MET", "INSUFFICIENT_INDEPENDENT_EVIDENCE",
    "VERIFY_SOURCE_DISTRUST", "INVESTIGATION_PLACEHOLDER_INERT",
    "CALLER_ASSERTED_PROMOTION", "CORE_CLASS_REQUIRES_DIRECTOR",
    "CHRONOLOGY_NOT_COMPOUNDING", "CONTAMINATED_HOLDOUT",
    "RECONCILIATION_DUPLICATE", "GOVERNANCE_PROPOSAL_ROUTED_TO_BRIEF",
    "IDENTITY_LEARNING_ROUTED_TO_BRIEF",
)

# Named promotion gates (§5): a promotion receipt must name its gates.
PROMOTION_GATES = (
    "SOURCE_OUTCOME_VERIFIED", "CAUSAL_REQUIREMENT_SATISFIED",
    "PROVENANCE_VALID", "RECONCILIATION_COMPLETE", "APPLICABILITY_DEFINED",
    "RELATED_HOLDOUT_PASS", "UNRELATED_REFUSAL_PASS", "NO_MATERIAL_REGRESSION",
    "INDEPENDENT_RECOMPUTATION_PASS",
)

INTELLIGENCE_CLASSES = ("CORE", "REUSABLE", "CONTEXT", "REFERENCE", "EPHEMERAL")

# Canonical lineage (§5 A6) — required in order.
CANONICAL_LINEAGE = (
    "EXPERIENCE", "EVENT", "BLOCK", "PROVENANCE", "RELATIONSHIP", "ACTION",
    "OBSERVATION", "OUTCOME", "VERIFY", "CANDIDATE", "HELD-OUT",
    "VERIFIED LEARNING",
)

# GRAPH CONTRACT AMENDMENT PROPOSALS (§6.1) — mapped to ratified equivalents
# or held; never silently extended.
GRAPH_AMENDMENT_PROPOSALS = (
    "LEARNED_FROM", "APPLIES_TO", "REFINES", "CORRECTS", "SUPERSEDES",
)
GRAPH_AMENDMENT_EPISTEMIC = ("LEARNED", "CONTRADICTED", "SUPERSEDED", "INVALIDATED")

DEFAULT_CONFIG = {
    # Decision Value Calculus V2.1 — RATIFIED 2026-09-30 (PRs #1186/#1190/
    # #1192). Condition 0 (§3.4) is satisfied; the ratified config hash is
    # bound into every receipt (see naya_kernel.node_base).
    "calculusVersion": CALCULUS_V21_VERSION,
    "calculusRatified": True,
    "evidenceFloor": {"critical": 5, "standard": 20},
    "autonomy": {"qMin": 9.0, "reversibilityMin": 7, "marginMin": 0.25},
    "confidence": {"aggregateMin": 0.80, "criticalMin": 0.75},
    "pool": {"maxSize": 100, "evidenceStalenessDays": 90},
    "calibration": {"biasTau": 0.05, "maeTau": 0.15, "minSamples": 10},
    "harm": {"physicalSeverityThreshold": 8},
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def _hash(obj: Any) -> str:
    return hashlib.sha256(_canonical(obj).encode("utf-8")).hexdigest()


def _learning_key(owner: str, lesson: str, source_outcome: str,
                  scope: Dict[str, Any], applicability: Dict[str, Any]) -> str:
    """LearningKey = H(owner ‖ lessonSemanticHash ‖ sourceOutcome ‖ scope ‖
    applicability) — the key is derived, never assigned (§5)."""
    return _hash({
        "owner": owner,
        "lessonSemanticHash": _hash(lesson),
        "sourceOutcome": source_outcome,
        "scope": scope,
        "applicability": applicability,
    })


def _config_hash(config: Dict[str, Any]) -> str:
    body = {k: v for k, v in config.items() if k != "configHash"}
    return _hash(body)


class LearnNode(NodeBase):
    """NAYA-KERNEL-LEARN (MN-08), candidate implementation.

    Every state transition emits a hash-bound typed receipt. LEARN performs
    authority validations and grants nothing (see authority_checks()).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None,
                 verify_resolver: Optional[Callable[[str], Optional[Dict[str, Any]]]] = None,
                 allow_fixture_intake: bool = False) -> None:
        self._config: Dict[str, Any] = json.loads(json.dumps(
            config if config is not None else DEFAULT_CONFIG))
        self._config["configHash"] = _config_hash(self._config)
        self._config_snapshots: Dict[str, Dict[str, Any]] = {
            self._config["configHash"]: json.loads(json.dumps(self._config)),
        }
        # VERIFY→LEARN trust seam (C2, C5 — Coda 1 verdict #554/5937954809).
        # verify_resolver: runtime-owned callable mapping receipt_id ->
        #   VERIFY's receipt dict (or None). Set at construction by runtime
        #   composition; never an event-payload parameter; never replaced
        #   after construction (no setter exists by design).
        # allow_fixture_intake: explicit test-only scope. Default False —
        #   ordinary construction is fail-closed. Not flippable after
        #   construction (no setter exists by design).
        self._verify_resolver = verify_resolver
        self._allow_fixture_intake = bool(allow_fixture_intake)
        # Evidence registries (§1 baton; §5 provenance; §17 seam rule)
        self._verify_receipts: Dict[str, Dict[str, Any]] = {}   # VERIFY PASS receipts
        self._cvo: Dict[str, Dict[str, Any]] = {}               # CVO records
        self._evidence: Dict[str, Dict[str, Any]] = {}          # evidence refs
        # Learning store (§2 learning object)
        self._learnings: Dict[str, Dict[str, Any]] = {}
        self._key_to_id: Dict[str, str] = {}
        # Transition ledger (§5 — hash-bound, append-only)
        self._receipts: List[Dict[str, Any]] = []
        self._receipt_index: Dict[str, Dict[str, Any]] = {}
        # Calibration (§3.5) and trust (§1 cross-check hook)
        self._calibration: Dict[str, Dict[str, Any]] = {}
        self._distrusted_sources: Dict[str, str] = {}
        # Outbox (§1.6 / §4.3 — proposals routed to authority, never applied)
        self._brief_outbox: List[Dict[str, Any]] = []
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

    def _emit(self, receipt_type: str, learning_id: Optional[str] = None,
              **fields: Any) -> Dict[str, Any]:
        """Emit a typed, hash-bound learning receipt (§5 field set)."""
        self._seq += 1
        receipt: Dict[str, Any] = {
            "receipt_type": receipt_type,
            "receipt_id": f"lr-{_hash([receipt_type, self._seq, self._now()])[:16]}",
            "node_id": NODE_ID,
            "node_mn": NODE_MN,
            "execution_id": f"lx-{self._seq:06d}",
            "learning_id": learning_id,
            "configHash": self._config["configHash"],
            "calculusVersion": self._config["calculusVersion"],
            # FLAG-001 step 4: the ratified V2.1 config hash, bound into
            # every receipt (content hash of the ratified spec — see
            # naya_kernel.node_base).
            "calculusConfigHash": CALCULUS_V21_SPEC_HASH,
            "authority_created": False,   # invariant: LEARN never creates authority
            "timestamp": self._now(),
            "issued_at": self._now(),
        }
        receipt.update(fields)
        self._seal(receipt)
        self._receipts.append(receipt)
        self._receipt_index[receipt["receipt_id"]] = receipt
        return receipt

    def _get(self, learning_id: str) -> Dict[str, Any]:
        learning = self._learnings.get(learning_id)
        if learning is None:
            raise KeyError(f"unknown learning_id: {learning_id}")
        return learning

    def _transition(self, learning: Dict[str, Any], to_state: str,
                    reason: str, **extra: Any) -> Dict[str, Any]:
        """Illegal-transition fail-closed state move (§8), receipted."""
        from_state = learning["state"]
        legal = LEGAL_TRANSITIONS.get(from_state, ())
        if to_state not in legal:
            raise ValueError(
                f"illegal learning transition {from_state} -> {to_state} "
                f"(fail-closed): {reason}"
            )
        learning["state"] = to_state
        learning["transitions"].append({
            "from": from_state, "to": to_state, "reason": reason,
            "timestamp": self._now(),
        })
        return self._emit(
            "TRANSITION", learning_id=learning["id"],
            state_before=from_state, state_after=to_state,
            lesson=learning["lesson"], reason=reason, **extra,
        )

    def _new_learning(self, *, lesson: str, learning_type: str, owner_id: str,
                      scope: Dict[str, Any],
                      applicability: Dict[str, Any],
                      source_outcome_refs: List[str],
                      expected_behavior: Optional[Dict[str, Any]],
                      validity_envelope: Optional[Dict[str, Any]] = None,
                      learning_class: Optional[str] = None,
                      critical_claim: bool = False,
                      verification: str = "PENDING") -> Dict[str, Any]:
        if learning_type not in LEARNING_TYPES:
            raise ValueError(f"unknown learning_type: {learning_type}")
        key = _learning_key(owner_id, lesson,
                            "|".join(sorted(source_outcome_refs)),
                            scope, applicability)
        learning_id = f"ln-{key[:16]}"
        self._seq += 1
        learning: Dict[str, Any] = {
            "id": learning_id,
            "learning_key": key,
            "lesson": lesson,
            "learning_type": learning_type,
            "owner_id": owner_id,
            "scope": scope,
            "source_outcome_refs": list(source_outcome_refs),
            "verification_receipt_refs": [],
            "cvo_refs": [],
            "evidence_refs": [],
            "source_intelligence_refs": [],
            "source_event_refs": [],
            "extraction_log": None,
            "learning_state": "CANDIDATE",          # epistemic axis
            "adoption_state": "INACTIVE",           # adoption axis
            "transfer_maturity": "UNTESTED",        # transfer axis
            "applicability": applicability,        # applicability axis
            "expected_behavior": expected_behavior,  # the named ∆BL (§4.1 no-effect)
            "behavioral_effect": None,
            "outcome_effect": None,
            "generalization_evidence": [],
            "negative_transfer_evidence": [],
            "heldout_evidence": [],
            "contradictions": [],
            "supersedes_learning_id": None,
            "superseded_by": None,
            "regression_guards": [],
            "value_effect": None,
            "calibration": None,
            "promotion": None,
            "validity_envelope": validity_envelope or {
                "Owner": owner_id,
                "TaskClasses": list(scope.get("task_classes", [])),
                "Capabilities": [],
                "Environment": scope.get("environment", "unspecified"),
                "Time": "verified-window",
                "Dependencies": [],
                "Limitations": list(applicability.get("limitations", [])),
            },
            # §2.1: learnings default to the class of their source intelligence;
            # CORE never auto-promotes (§10 Q6 candidate rule).
            "learning_class": learning_class or "CONTEXT",
            "critical_claim": critical_claim,
            "verification": verification,          # VERIFIED | PENDING
            "internal_only": verification == "PENDING",
            "state": "UNINITIALIZED",
            "transitions": [],
            "receipts": [],
            "harm_windows": [],
            "stale": False,
            "distrust_held": False,
            "reconciliation": {"classification": "NEW", "existing_learning_refs": []},
            "judgmental_extraction": False,
            "config_hash": self._config["configHash"],
            "created_at": self._now(),
            "verified_at": None,
            "promoted_at": None,
        }
        self._learnings[learning_id] = learning
        self._key_to_id[key] = learning_id
        self._transition(learning, "CANDIDATE",
                         "ingest/extract admitted candidate (§8 lifecycle)")
        return learning

    # ------------------------------------------------------------------
    # §1 — VERIFY→LEARN baton: verified receipts only
    # ------------------------------------------------------------------

    def register_verify_receipt(self, receipt: Dict[str, Any]) -> Dict[str, Any]:
        """Register a VERIFY receipt in LEARN's local registry (test/lab seam).

        Only VERIFIED_PASS receipts from NAYA-KERNEL-VERIFY qualify as
        learning evidence (§1.1 — "If VERIFY has not spoken, LEARN has
        nothing to read").

        This is an explicitly test-scoped fixture seam: it refuses unless
        the node was constructed with allow_fixture_intake=True. Runtime
        intake goes through ingest_verify_receipt with a wired resolver.
        """
        if not self._allow_fixture_intake:
            raise ValueError(
                "register_verify_receipt is a test-scoped fixture seam; "
                "refused without allow_fixture_intake=True "
                "(VERIFY_ORIGIN_UNESTABLISHED)")
        rid = receipt.get("receipt_id") or receipt.get("id")
        if not rid:
            raise ValueError("verify receipt must carry a receipt_id")
        self._verify_receipts[rid] = receipt
        return {"registered": rid, "qualifying": self._is_qualifying_verify(receipt)}

    def _is_qualifying_verify(self, receipt: Dict[str, Any]) -> bool:
        return (
            receipt.get("node_id") == VERIFY_NODE_ID
            and receipt.get("verification_state") == "VERIFIED_PASS"
        )

    def _derive_lesson_from_baton(
        self, receipt: Dict[str, Any], rid: str
    ) -> tuple:
        """Derive a lesson from VERIFY-owned facts (Naya 2 #554/5939362590).

        VERIFY speaks learn_baton; it does not author lessons. LEARN derives
        the lesson from the verified fact (subject_ref.claim) when the baton
        marks the receipt eligible for learning (may_use non-empty =
        VERIFIED_PASS). Authorship of the derivation is LEARN's; trust in
        the fact is VERIFY's seal.

        Returns (lesson, scope). Returns (None, {}) if no lesson is
        derivable (baton ineligible or no claim) — the caller then refuses.
        """
        baton = receipt.get("learn_baton") or {}
        # Eligibility: VERIFIED_PASS receipts land on may_use; anything
        # else (FAIL, REOPENED) lands on must_not_generalize.
        if not baton.get("may_use"):
            return None, {}
        # VERIFY stores the verified subject fields under subject_ref
        # (BATON_REQUIRED_FIELDS for the baton kind), including claim.
        subject_ref = receipt.get("subject_ref") or {}
        claim = subject_ref.get("claim")
        if not claim or not isinstance(claim, str):
            return None, {}
        # The lesson is the verified fact, stated as LEARN's derivation.
        # The learning pipeline (reconcile → holdout → evidence) determines
        # whether it actually changes future behavior.
        lesson = f"verified: {claim}"
        scope = dict(subject_ref.get("scope") or {})
        return lesson, scope

    def register_cvo(self, cvo: Dict[str, Any]) -> Dict[str, Any]:
        """Register a CVO record into the provenance store (§5 — CVO refs are
        part of a learning's provenance; §3.4/§11.1 promotion law blocks
        promotion on a fake CVO ref, P12)."""
        cid = cvo.get("cvo_id") or cvo.get("id")
        if not cid:
            raise ValueError("CVO record must carry an id")
        self._cvo[cid] = cvo
        return {"registered": cid}

    def register_evidence(self, ref: str, evidence: Dict[str, Any]) -> Dict[str, Any]:
        """Register an evidence record under its ref (§5 provenance record:
        evidence refs; evidence lives in provenance, never substitutes for a
        VERIFY receipt)."""
        self._evidence[ref] = evidence
        return {"registered": ref}

    def ingest_verify_receipt(self, receipt: Dict[str, Any]) -> Dict[str, Any]:
        """Intake a verified receipt (event-driven, §1.5).

        Three-path dispatch (Coda 1 verdict #554/5937954809):

        1. Runtime path (resolver wired): the receipt_id is resolved through
           the runtime-owned resolver; the RESOLVED receipt is ownership-
           proved (C6), allowlist-compared against the presented object
           (C3), staleness-checked (C4), and — only then — consumed. The
           caller's object is never trusted (C1).
        2. Fixture path (allow_fixture_intake=True, no resolver): explicit
           test scope; label check only.
        3. Fail-closed default (no resolver, no fixture privilege): refused
           with VERIFY_ORIGIN_UNESTABLISHED. Positive learning stays blocked
           until an authentic VERIFY evidence path is wired.

        The resolver is construction-owned (C2): it is never an
        event-payload parameter, and no "resolver"-like key in the receipt
        payload can substitute it — such keys are ignored.

        Pool capacity is bounded: overflow emits LEARN_INTAKE_BACKPRESSURE
        and pauses intake, never silently drops.
        """
        rid = receipt.get("receipt_id") or receipt.get("id") or "unknown"
        if rid in self._verify_receipts:
            return {"accepted": False, "duplicate": True, "receipt_id": rid}
        candidates_live = sum(
            1 for l in self._learnings.values()
            if l["state"] in ("CANDIDATE", "RECONCILING", "TEST_REQUIRED")
        )
        if candidates_live >= self._config["pool"]["maxSize"]:
            bp = self._emit(
                "LEARN_INTAKE_BACKPRESSURE", receipt_id_ref=rid,
                reason="candidate pool at capacity (§1.5); intake paused, nothing dropped",
            )
            return {"accepted": False, "backpressure": True,
                    "backpressure_receipt": bp["receipt_id"]}
        # C2: resolver is construction-owned; the stricter runtime path wins
        # whenever a resolver is wired, even if fixture privilege was also set.
        if self._verify_resolver is not None:
            return self._ingest_via_resolver(receipt, rid)
        if self._allow_fixture_intake:
            return self._ingest_fixture(receipt, rid)
        return self._refuse(
            rid, "VERIFY_ORIGIN_UNESTABLISHED",
            "no VERIFY resolver wired and no fixture privilege; origin "
            "cannot be established — LEARN consumes only verified receipts (§1.1)")

    def _refuse(self, rid: str, reason_code: str, reason: str) -> Dict[str, Any]:
        """Emit INTAKE_REFUSED and return the refusal shape."""
        refusal = self._emit(
            "INTAKE_REFUSED", receipt_id_ref=rid,
            reason_code=reason_code, reason=reason,
        )
        return {"accepted": False, "reason_code": reason_code,
                "receipt_id": refusal["receipt_id"]}

    @staticmethod
    def reference_resolver(verify_node: Any
                           ) -> Callable[[str], Optional[Dict[str, Any]]]:
        """Reference runtime wiring for the VERIFY→LEARN resolver (C2).

        Returns a callable mapping receipt_id -> VERIFY's receipt dict, or
        None when VERIFY has no *current* receipt under that id. "Current"
        excludes superseded receipts (a newer receipt carries
        supersedes=<id>); those resolve to None → VERIFY_RECEIPT_UNKNOWN.

        Deliberately a plain store lookup: VERIFY-ownership is proved by
        LEARN's C6 structural proof (_prove_verify_ownership), not by the
        resolver. A resolver that silently filtered forgeries would turn
        the C6 direct-write case into VERIFY_RECEIPT_UNKNOWN; returning
        what the store holds lets C6 refuse it precisely with
        VERIFY_ORIGIN_UNESTABLISHED.

        Residual risk (documented honestly): a same-process holder of the
        VerifyNode that replicates VERIFY's full emission (valid id format,
        complete structure, sealed state) can forge a receipt this proof
        accepts. The bar is raised from "two caller-controlled labels" to
        "replicate VERIFY's emission logic"; a holder that thorough owns
        the process, not just the seam.
        """
        def resolve(receipt_id: str) -> Optional[Dict[str, Any]]:
            store = getattr(verify_node, "_receipts", None)
            if not isinstance(store, dict):
                return None
            receipt = store.get(receipt_id)
            if receipt is None:
                return None
            for other in store.values():
                if isinstance(other, dict) and other.get("supersedes") == receipt_id:
                    return None
            return receipt
        return resolve

    def _ingest_fixture(self, receipt: Dict[str, Any], rid: str) -> Dict[str, Any]:
        """Explicit test-scoped intake (allow_fixture_intake=True, no resolver).

        Label check only — never a production path. The "fixture": True
        marker keeps the privilege visible in the result.
        """
        if not self._is_qualifying_verify(receipt):
            return self._refuse(
                rid, "VERIFY_RESULT_REQUIRED",
                "LEARN consumes only verified receipts (§1.1)")
        self.register_verify_receipt(receipt)
        self._emit("INTAKE_ACCEPTED", receipt_id_ref=rid,
                   reason="fixture intake (explicit test scope only)")
        return {"accepted": True, "receipt_id": rid, "fixture": True}

    def _ingest_via_resolver(self, receipt: Dict[str, Any], rid: str
                             ) -> Dict[str, Any]:
        """Runtime intake: resolve, prove origin, detect tampering, then consume.

        C1 — the RESOLVED receipt is consumed; the caller's object is
        compared only to detect tampering, never read for the decision.
        """
        try:
            resolved = self._verify_resolver(rid)
        except Exception:
            resolved = None
        if resolved is None:
            return self._refuse(
                rid, "VERIFY_RECEIPT_UNKNOWN",
                f"VERIFY has no current receipt '{rid}'")
        # C6 — prove VERIFY ownership before trusting anything resolved.
        if not self._prove_verify_ownership(resolved):
            return self._refuse(
                rid, "VERIFY_ORIGIN_UNESTABLISHED",
                "resolved receipt fails VERIFY-ownership proof (id format, "
                "issuer, or structure inconsistent with VERIFY emission)")
        # C3 — tamper detection over the explicit security allowlist.
        if not self._allowlist_match(receipt, resolved):
            return self._refuse(
                rid, "VERIFY_RECEIPT_TAMPERED",
                "caller-presented receipt differs from the VERIFY-resolved "
                "receipt on security-relevant fields")
        # C4 — staleness: reopened receipts are dead; the identity binding
        # must be present. (Superseded receipts are filtered by the
        # reference resolver, which returns None → VERIFY_RECEIPT_UNKNOWN.)
        if resolved.get("verification_state") == "REOPENED":
            return self._refuse(
                rid, "VERIFY_RECEIPT_REOPENED",
                "receipt was reopened; the re-examination supersedes this version")
        if not isinstance(resolved.get("subject_ref"), dict):
            return self._refuse(
                rid, "VERIFY_ORIGIN_UNESTABLISHED",
                "resolved receipt lacks the subject_ref identity binding")
        # C1 — qualify and consume the RESOLVED receipt, never the caller's.
        if not self._is_qualifying_verify(resolved):
            return self._refuse(
                rid, "VERIFY_RESULT_REQUIRED",
                "LEARN consumes only verified receipts (§1.1)")
        self._verify_receipts[rid] = resolved
        self._emit("INTAKE_ACCEPTED", receipt_id_ref=rid,
                   reason="qualifying VERIFY baton resolved and verified")
        return {"accepted": True, "receipt_id": rid}

    @staticmethod
    def _prove_verify_ownership(resolved: Dict[str, Any]) -> bool:
        """C6: prove the resolved receipt is VERIFY-owned.

        A resolver pointed at VERIFY's live store can be poisoned by a
        same-process direct dict write (append-only is a method, not an
        invariant). This proof checks what VERIFY's own emission guarantees
        but a naive forgery gets wrong: the content-commitment id format,
        the issuer, structural completeness, and state consistency. A forgery
        that replicates all of VERIFY's emission logic has done VERIFY's
        work; a two-label forgery is refused here.
        """
        rid = resolved.get("id")
        if not isinstance(rid, str) or not _VERIFY_RECEIPT_ID_RE.match(rid):
            return False
        if resolved.get("node_id") != VERIFY_NODE_ID:
            return False
        for field in _VERIFY_RECEIPT_STRUCTURE_FIELDS:
            if field not in resolved:
                return False
        if not resolved.get("verify_key"):
            return False
        if not isinstance(resolved.get("subject_ref"), dict):
            return False
        if resolved.get("verification_state") == "VERIFIED_PASS":
            # VERIFY seals receipts on close; an unsealed "PASS" was not
            # emitted by VERIFY's state machine.
            if "receipt_hash" not in resolved:
                return False
        return True

    @staticmethod
    def _allowlist_match(presented: Dict[str, Any],
                         resolved: Dict[str, Any]) -> bool:
        """C3: tamper detection over the explicit security-relevant allowlist.

        The presented object may carry the id as "receipt_id" (event shape)
        where the resolved receipt carries "id"; that alias is normalized.
        Every allowlisted field must match exactly — including subject_ref,
        so a genuine receipt for another task/owner/scope cannot be
        redirected by presenting an altered copy (C4).
        """
        for field in _VERIFY_INTAKE_COMPARE_FIELDS:
            expected = resolved.get(field)
            actual = presented.get(field)
            if field == "id" and actual is None:
                actual = presented.get("receipt_id")
            if actual != expected:
                return False
        return True

    def note_investigation(self, experience: Dict[str, Any]) -> Dict[str, Any]:
        """A12: pre-verification investigation placeholder — inert, unscored,
        LEARN-internal only. It may NOT enter scoring (§3), promotion (§3.4),
        or the TESTING serving path (§6.2) until a verified receipt arrives.
        CandidateCapture != VerifiedLearning."""
        learning = self._new_learning(
            lesson=experience.get("lesson", "unverified experience"),
            learning_type=experience.get("learning_type", "BEHAVIOR_RULE"),
            owner_id=experience.get("owner_id", "unknown"),
            scope=experience.get("scope", {}),
            applicability={"state": "UNKNOWN", "task_classes": [],
                           "limitations": ["unverified"]},
            source_outcome_refs=[],
            expected_behavior=None,
            verification="PENDING",
        )
        learning["internal_only"] = True
        receipt = self._emit(
            "INVESTIGATION_PLACEHOLDER", learning_id=learning["id"],
            lesson=learning["lesson"],
            reason="inert placeholder pending verified receipt (A12)",
        )
        return {"learning_id": learning["id"], "inert": True,
                "receipt_id": receipt["receipt_id"]}

    # ------------------------------------------------------------------
    # §1.4 — extraction contract: Extract(O) -> L_candidate
    # ------------------------------------------------------------------

    def extract(self, receipt_ids: List[str], actor: str = "kernel-extraction",
                judgmental: bool = False) -> Dict[str, Any]:
        """Deterministic, replayable extraction (same receipts -> same
        candidates). A cold successor must reproduce *which* candidates were
        extracted. Strength ceiling: L_strength <= Evidence_strength (§1.4);
        extraction preserves scope — it never widens it (A2)."""
        ordered = sorted(set(receipt_ids))
        produced: List[str] = []
        for rid in ordered:
            receipt = self._verify_receipts.get(rid)
            if receipt is None:
                raise KeyError(f"unknown verify receipt: {rid}")
            if not self._is_qualifying_verify(receipt):
                raise ValueError(
                    f"extract refuses non-verified receipt {rid} "
                    f"(VERIFY_RESULT_REQUIRED)")
            outcome = receipt.get("outcome", {})
            lesson = outcome.get("lesson") or receipt.get("claimed_lesson")
            scope = {}
            if not lesson:
                # Naya 2 diagnostic (#554/5939362590): VERIFY speaks
                # learn_baton, extract listened for outcome.lesson. Derive
                # the lesson from VERIFY-owned facts instead of requiring a
                # pre-formed lesson. Authorship stays in LEARN (derivation),
                # trust stays in VERIFY's seal. VERIFY never invents lessons.
                lesson, scope = self._derive_lesson_from_baton(receipt, rid)
            if not lesson:
                raise ValueError(
                    f"extract refuses receipt {rid}: no lesson extractable")
            source_outcome = outcome.get("outcome_id") or rid
            if not scope:
                scope = dict(outcome.get("scope") or {})
            # Strength ceiling (§1.4): extraction must preserve scope. If the
            # receipt claims a wider lesson scope than the verified source
            # scope, the scope is clamped to the source scope and the claim
            # is recorded as SCOPE_MISMATCH — evidence laundering through
            # abstraction is refused.
            claimed_scope = dict(outcome.get("claimed_lesson_scope") or scope)
            if not self._scope_subset(claimed_scope, scope):
                scope_note = "SCOPE_MISMATCH: claimed scope clamped to verified source scope"
                scope = dict(scope)
            else:
                scope_note = None
                scope = claimed_scope
            applicability = {
                "state": "UNKNOWN",
                "task_classes": list(scope.get("task_classes", [])),
                "limitations": ["extraction-scope-only"],
            }
            key = _learning_key(
                receipt.get("owner_id", "unknown"), lesson,
                source_outcome, scope, applicability)
            existing_id = self._key_to_id.get(key)
            if existing_id is not None:
                # Duplicate law (§6.3): L_n == L_e -> REUSE / ADD EVIDENCE,
                # never a second canonical learning.
                existing = self._learnings[existing_id]
                if rid not in existing["verification_receipt_refs"]:
                    existing["verification_receipt_refs"].append(rid)
                produced.append(existing_id)
                continue
            learning = self._new_learning(
                lesson=lesson,
                learning_type=outcome.get("learning_type", "BEHAVIOR_RULE"),
                owner_id=receipt.get("owner_id", "unknown"),
                scope=scope,
                applicability=applicability,
                source_outcome_refs=[source_outcome],
                expected_behavior=outcome.get("expected_behavior"),
                learning_class=outcome.get("learning_class"),
                critical_claim=bool(outcome.get("critical_claim", False)),
                verification="VERIFIED",
            )
            learning["verification_receipt_refs"].append(rid)
            learning["judgmental_extraction"] = bool(judgmental)
            if scope_note:
                learning["reconciliation"]["classification_note"] = scope_note
            log_receipt = self._emit(
                "EXTRACTION_LOG", learning_id=learning["id"],
                inputs={"receipt_ids": ordered, "actor": actor,
                        "judgmental": bool(judgmental)},
                actor=actor, candidates_produced=[learning["id"]],
                reason="§1.4 extraction contract (deterministic, replayable)",
            )
            learning["extraction_log"] = log_receipt["receipt_id"]
            produced.append(learning["id"])
        run_receipt = self._emit(
            "EXTRACTION_RUN",
            inputs={"receipt_ids": ordered, "actor": actor,
                    "judgmental": bool(judgmental)},
            actor=actor, candidates_produced=list(produced),
            reason="extraction run complete",
        )
        return {"candidates": produced, "run_receipt": run_receipt["receipt_id"]}

    @staticmethod
    def _scope_subset(inner: Dict[str, Any], outer: Dict[str, Any]) -> bool:
        """Generalization ceiling (A2): Scope(L_candidate) ⊆ S_verified-source."""
        for key, value in inner.items():
            if key not in outer:
                return False
            ov = outer[key]
            if isinstance(value, list) and isinstance(ov, list):
                if not set(value) <= set(ov):
                    return False
            elif value != ov:
                return False
        return True

    # ------------------------------------------------------------------
    # §6.3 — reconciliation
    # ------------------------------------------------------------------

    def _classify_reconciliation(self, learning: Dict[str, Any]
                                 ) -> Tuple[str, List[str]]:
        """Classify the candidate against existing intelligence (A3)."""
        refs: List[str] = []
        for other_id, other in self._learnings.items():
            if other_id == learning["id"]:
                continue
            if other["state"] in ("REJECTED", "RETIRED"):
                continue
            # Contradiction is checked first and in both directions: either
            # side may declare the conflict (§6.3 contradiction law).
            if (other.get("contradicts", {}).get(learning["id"])
                    or learning.get("contradicts", {}).get(other_id)):
                refs.append(other_id)
                continue
            if (other["learning_key"] == learning["learning_key"]
                    or (other["lesson"] == learning["lesson"]
                        and other["owner_id"] == learning["owner_id"]
                        and self._scope_subset(learning["scope"], other["scope"])
                        and self._scope_subset(other["scope"], learning["scope"]))):
                return "EXACT_DUPLICATE", [other_id]
            if (other["owner_id"] == learning["owner_id"]
                    and self._scope_subset(other["scope"], learning["scope"])
                    and not self._scope_subset(learning["scope"], other["scope"])
                    and other["lesson"] == learning["lesson"]):
                return "SCOPE_NARROWING", [other_id]
            if (other["owner_id"] == learning["owner_id"]
                    and self._scope_subset(learning["scope"], other["scope"])
                    and not self._scope_subset(other["scope"], learning["scope"])
                    and other["lesson"] == learning["lesson"]):
                # Candidate scope wider than an existing same-lesson learning:
                # expansion must be earned by transfer evidence (A2).
                return "SCOPE_EXPANSION_CANDIDATE", [other_id]
            if (other["lesson"] == learning["lesson"]
                    and other["owner_id"] == learning["owner_id"]
                    and self._scopes_overlap(learning["scope"], other["scope"])
                    and not self._scopes_equal(learning["scope"], other["scope"])):
                return "PARALLEL_DIFFERENT_SCOPE", [other_id]
        if refs:
            return "CONTRADICTION", refs
        return "NEW", []

    @staticmethod
    def _scopes_overlap(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
        ta = set(a.get("task_classes", []))
        tb = set(b.get("task_classes", []))
        return bool(ta & tb) or (not ta and not tb)

    @staticmethod
    def _scopes_equal(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
        return _hash(a) == _hash(b)

    def reconcile(self, learning_id: str) -> Dict[str, Any]:
        """Run reconciliation (§6.3): CANDIDATE -> RECONCILING, classify, and
        apply the duplicate/contradiction law. Contradictions are surfaced and
        preserved — never automatic newer-wins, never delete the old."""
        learning = self._get(learning_id)
        # Idempotent: reconciling an already-reconciling candidate re-runs
        # classification without re-entering the state (fail-closed otherwise).
        if learning["state"] == "CANDIDATE":
            self._transition(learning, "RECONCILING",
                             "reconciliation started (§6.3)")
        elif learning["state"] != "RECONCILING":
            raise ValueError(
                f"reconcile refused from state {learning['state']} (fail-closed)")
        classification, refs = self._classify_reconciliation(learning)
        learning["reconciliation"] = {
            "classification": classification,
            "existing_learning_refs": refs,
        }
        if classification == "EXACT_DUPLICATE":
            # Duplicate law: REUSE / ADD EVIDENCE, never a second canonical
            # learning. The duplicate candidate is rejected as a duplicate;
            # its verified receipts join the canonical learning's evidence
            # (so the canonical accumulates toward the floor, §3.3) and its
            # other evidence refs join the evidence set.
            existing = self._get(refs[0])
            for ref in learning["verification_receipt_refs"]:
                if ref not in existing["verification_receipt_refs"]:
                    existing["verification_receipt_refs"].append(ref)
            for ref in learning["evidence_refs"]:
                if ref not in existing["evidence_refs"]:
                    existing["evidence_refs"].append(ref)
            self._transition(
                learning, "REJECTED",
                f"RECONCILIATION_DUPLICATE of {refs[0]}; evidence reused, "
                "no second canonical learning (§6.3)")
        elif classification == "CONTRADICTION":
            for ref in refs:
                other = self._get(ref)
                learning["contradictions"].append(
                    {"learning_id": ref, "status": "SURFACED"})
                other["contradictions"].append(
                    {"learning_id": learning_id, "status": "SURFACED"})
            self._transition(
                learning, "CONTRADICTED",
                "material contradiction surfaced and preserved on both sides "
                "(§6.3 contradiction law)")
        receipt = self._emit(
            "RECONCILIATION", learning_id=learning_id,
            reconciliation=learning["reconciliation"],
            reason=f"classified {classification}",
        )
        return {"classification": classification, "refs": refs,
                "state": learning["state"],
                "receipt_id": receipt["receipt_id"]}

    # ------------------------------------------------------------------
    # §11.2 — held-out design; §3.7 held-out / negative-transfer law
    # ------------------------------------------------------------------

    def design_holdout(self, learning_id: str) -> Dict[str, Any]:
        """Design the control for spurious correlation and self-confirmation.
        A held-out task designed from the verification example is contaminated
        and invalid (A7). Replay is not transfer (§3.7)."""
        learning = self._get(learning_id)
        if learning["internal_only"]:
            raise ValueError("investigation placeholders may not enter held-out "
                             "design (A12)")
        source_tasks = list(learning["source_outcome_refs"])
        holdout_tasks = list(learning.get("proposed_holdout_tasks", []))
        contaminated = any(t in source_tasks for t in holdout_tasks)
        plan = {
            "learning_id": learning_id,
            "source_task_refs": source_tasks,
            "holdout_task_refs": holdout_tasks,
            "test_created_before_outcome": learning.get(
                "holdout_created_before_outcome", False),
            "shared_evidence_declared": learning.get(
                "holdout_shared_evidence", []),
            "predeclared_metric": (learning.get("expected_behavior") or {}).get(
                "metric"),
            "contaminated": contaminated,
        }
        receipt = self._emit("HOLDOUT_PLAN", learning_id=learning_id,
                             holdout_plan=plan,
                             reason="§11.2 design_holdout")
        if contaminated:
            self._transition(learning, "BLOCKED",
                             "CONTAMINATED_HOLDOUT: held-out task derived from "
                             "the verification example (§3.7, A7)")
        learning["holdout_plan"] = plan
        return {"plan": plan, "receipt_id": receipt["receipt_id"]}

    def record_behavioral_evidence(self, learning_id: str, task_ref: str,
                                   delta_b: float, related: bool,
                                   metric: Optional[str] = None) -> Dict[str, Any]:
        """Record ΔB = Behavior(q, L) − Behavior(q, ¬L) on the predeclared
        metric (§3.7). Related tasks support bounded transfer; an effect on an
        unrelated task is OVERGENERALIZATION_DETECTED — a fundamental
        intelligence failure that blocks scope expansion."""
        learning = self._get(learning_id)
        expected_metric = (learning.get("expected_behavior") or {}).get("metric")
        record = {"task_ref": task_ref, "delta_b": delta_b,
                  "metric": metric or expected_metric,
                  "timestamp": self._now()}
        if related:
            learning["heldout_evidence"].append(record)
            if delta_b > 0:
                learning["transfer_maturity"] = "HELD_OUT_RELATED_SUPPORTED"
            receipt = self._emit("BEHAVIORAL_EVIDENCE", learning_id=learning_id,
                                 related=True, record=record,
                                 reason="related held-out result (§3.7)")
        else:
            if delta_b != 0:
                learning["negative_transfer_evidence"].append(
                    {**record, "overgeneralization": True})
                receipt = self._emit(
                    "OVERGENERALIZATION_DETECTED", learning_id=learning_id,
                    record=record,
                    reason="lesson changed an unrelated task — fundamental "
                           "intelligence failure; scope expansion blocked (§3.7)")
            else:
                learning["negative_transfer_evidence"].append(record)
                receipt = self._emit(
                    "NEGATIVE_TRANSFER_REFUSED", learning_id=learning_id,
                    record=record,
                    reason="unrelated task unchanged — negative-transfer "
                           "boundary holds (§3.7)")
        learning["behavioral_effect"] = record
        return {"recorded": True, "receipt_id": receipt["receipt_id"],
                "overgeneralization": (not related and delta_b != 0)}

    def record_outcome_evidence(self, learning_id: str, delta_outcome: float,
                                metric: Optional[str] = None) -> Dict[str, Any]:
        """Beneficial claims require outcome evidence (P20).

        Spec §3.7 — held-out and negative-transfer law."""
        learning = self._get(learning_id)
        record = {"delta_outcome": delta_outcome, "metric": metric,
                  "timestamp": self._now()}
        learning["outcome_effect"] = record
        receipt = self._emit("OUTCOME_EVIDENCE", learning_id=learning_id,
                             record=record, reason="§3.7 outcome evidence")
        return {"recorded": True, "receipt_id": receipt["receipt_id"]}

    # ------------------------------------------------------------------
    # Harm windows (§3.4/§11.1), stale learning (§3.7), regression (§7)
    # ------------------------------------------------------------------

    def report_harm_window(self, learning_id: str, severity: int,
                           description: str) -> Dict[str, Any]:
        """Record a delayed-harm observation window. Promotion is refused
        while a material window is open (tail severity >= configured physical
        severity threshold). Patience is a safety property.

        Spec §4 — hard refusal 5 (open harm windows)."""
        learning = self._get(learning_id)
        window = {"severity": severity, "description": description,
                  "open": True, "timestamp": self._now()}
        learning["harm_windows"].append(window)
        receipt = self._emit("HARM_WINDOW_REPORTED", learning_id=learning_id,
                             window=window, reason="§11.1 open harm window")
        return {"reported": True, "receipt_id": receipt["receipt_id"]}

    def clear_harm_window(self, learning_id: str, index: int = 0) -> Dict[str, Any]:
        """Close a reported harm window (receipted) — an open window at or
        above the physical-severity threshold blocks promotion and serving
        (§4 hard refusal 5; §11.1 promotionEligible open-harm-window check)."""
        learning = self._get(learning_id)
        learning["harm_windows"][index]["open"] = False
        learning["harm_windows"][index]["closed_at"] = self._now()
        receipt = self._emit("HARM_WINDOW_CLOSED", learning_id=learning_id,
                             index=index, reason="window closed")
        return {"closed": True, "receipt_id": receipt["receipt_id"]}

    def _open_harm_window(self, learning: Dict[str, Any]) -> bool:
        threshold = self._config["harm"]["physicalSeverityThreshold"]
        return any(w.get("open") and w.get("severity", 0) >= threshold
                   for w in learning["harm_windows"])

    def detect_stale(self, learning_id: str,
                     environment: Dict[str, Any]) -> Dict[str, Any]:
        """HistoricallyVerified ⇏ CurrentlyApplicable (§3.7, A4). A learning
        whose validity envelope no longer matches the environment is a
        REGRESSION_CANDIDATE — stale learning is a first-class detection and
        cannot silently steer."""
        learning = self._get(learning_id)
        envelope = learning["validity_envelope"]
        stale = (
            envelope.get("Environment") != environment.get("environment")
            or environment.get("now") and envelope.get("Time") == "expired"
        )
        if stale:
            learning["stale"] = True
            if learning["state"] == "ACTIVE":
                self._transition(learning, "REGRESSED",
                                 "REGRESSION_CANDIDATE: validity envelope no "
                                 "longer matches environment (§3.7, A4)")
            receipt = self._emit("REGRESSION_CANDIDATE", learning_id=learning_id,
                                 environment=environment,
                                 reason="stale learning detected")
            return {"stale": True, "receipt_id": receipt["receipt_id"],
                    "state": learning["state"]}
        return {"stale": False}

    def regress(self, learning_id: str, reason: str) -> Dict[str, Any]:
        """Transition a learning to REGRESSED (§8 lifecycle branch state;
        §7 failure handling — regression can demote/retire, P28)."""
        learning = self._get(learning_id)
        self._transition(learning, "REGRESSED", reason)
        return {"state": "REGRESSED"}

    def retire(self, learning_id: str, authority_ref: str) -> Dict[str, Any]:
        """Retire a learning. The authority reference is recorded; LEARN does
        not invent authority — retirement of an ACTIVE learning is a governed
        act (§1.6 operator/director authority)."""
        learning = self._get(learning_id)
        if learning["state"] not in ("ACTIVE", "REGRESSED"):
            raise ValueError("only ACTIVE or REGRESSED learnings retire")
        self._transition(learning, "RETIRED",
                         f"retired under authority {authority_ref}")
        learning["adoption_state"] = "RETIRED"
        return {"state": "RETIRED"}

    def supersede(self, old_id: str, new_id: str) -> Dict[str, Any]:
        """Supersession preserves history (§6.3): the earlier learning was
        valid in its time/scope; the newer learning now governs."""
        old = self._get(old_id)
        new = self._get(new_id)
        if old["state"] != "ACTIVE":
            raise ValueError("only an ACTIVE learning can be superseded")
        old["superseded_by"] = new_id
        new["supersedes_learning_id"] = old_id
        new["reconciliation"]["classification"] = "SUPERSEDES"
        new["reconciliation"]["existing_learning_refs"] = [old_id]
        self._transition(old, "SUPERSEDED",
                         f"superseded by {new_id}; history preserved (§6.3)")
        receipt = self._emit("SUPERSESSION", learning_id=new_id,
                             superseded=old_id,
                             reason="supersession with lineage, never silent "
                                    "replacement (§6.3)")
        return {"superseded": old_id, "governs": new_id,
                "receipt_id": receipt["receipt_id"]}

    # ------------------------------------------------------------------
    # §8 — compounding: LaterIsBetter ⇏ EarlierLearningCausedIt
    # ------------------------------------------------------------------

    def record_compounding(self, earlier_id: str, later_id: str,
                           answers: Dict[str, Any]) -> Dict[str, Any]:
        """A compounding claim must answer the questionnaire (A8). Chronology
        is not compounding.

        Spec §8 — lifecycle maturity L7/L8 (compounding requires measured later behavior)."""
        required = ("which_earlier_used", "which_later_depended",
                    "what_changed", "outcome_improved", "attribution_amount",
                    "unrelated_stable", "successor_retained")
        missing = [k for k in required if k not in answers]
        if missing:
            receipt = self._emit(
                "COMPOUNDING_REFUSED", learning_id=later_id,
                reason_code="CHRONOLOGY_NOT_COMPOUNDING",
                missing=missing,
                reason="compounding questionnaire incomplete (A8)")
            return {"accepted": False, "missing": missing,
                    "receipt_id": receipt["receipt_id"]}
        later = self._get(later_id)
        if not answers.get("outcome_improved"):
            receipt = self._emit(
                "COMPOUNDING_REFUSED", learning_id=later_id,
                reason_code="CHRONOLOGY_NOT_COMPOUNDING",
                reason="no measured later-behavior improvement (A8)")
            return {"accepted": False, "receipt_id": receipt["receipt_id"]}
        later["transfer_maturity"] = "COMPOUNDING_SUPPORTED"
        receipt = self._emit("COMPOUNDING_ACCEPTED", learning_id=later_id,
                             earlier_id=earlier_id, answers=answers,
                             reason="compounding questionnaire answered (A8)")
        return {"accepted": True, "receipt_id": receipt["receipt_id"]}

    # ------------------------------------------------------------------
    # §17 promotion-seam rule: EVIDENCE_REF_PRESENCE != EVIDENCE_VALIDATION
    # ------------------------------------------------------------------

    def _resolve_and_validate_refs(self, learning: Dict[str, Any]
                                   ) -> Tuple[bool, List[str]]:
        """Canonicalization must *resolve and validate* every evidence ref
        before any state upgrade. A nonempty evidence_refs array plus a
        learning_id is never sufficient."""
        failures: List[str] = []
        for rid in learning["verification_receipt_refs"]:
            receipt = self._verify_receipts.get(rid)
            if receipt is None:
                failures.append(f"EVIDENCE_REFERENCE_UNRESOLVED:{rid}")
            elif not self._is_qualifying_verify(receipt):
                failures.append(f"PROVENANCE_FAILURE:verify-not-qualifying:{rid}")
            elif receipt.get("owner_id") != learning["owner_id"]:
                failures.append(f"PROVENANCE_FAILURE:wrong-owner:{rid}")
        for cid in learning["cvo_refs"]:
            cvo = self._cvo.get(cid)
            if cvo is None:
                failures.append(f"EVIDENCE_REFERENCE_UNRESOLVED:cvo:{cid}")
                continue
            # A CVO that declares task classes must cover the learning's
            # scope; a wrong-scope CVO blocks promotion (P14).
            cvo_classes = cvo.get("task_classes")
            learn_classes = learning["scope"].get("task_classes", [])
            if (cvo_classes is not None and learn_classes
                    and not set(learn_classes) <= set(cvo_classes)):
                failures.append(f"SCOPE_MISMATCH:cvo:{cid}")
        for ref in learning["evidence_refs"]:
            evidence = self._evidence.get(ref)
            if evidence is None:
                failures.append(f"EVIDENCE_REFERENCE_UNRESOLVED:evidence:{ref}")
            elif evidence.get("forged"):
                failures.append(f"PROVENANCE_FAILURE:forged:{ref}")
            elif evidence.get("owner_id") not in (None, learning["owner_id"]):
                failures.append(f"PROVENANCE_FAILURE:wrong-owner:{ref}")
        return (len(failures) == 0, failures)

    # ------------------------------------------------------------------
    # §3.4 + §11.1 — the promotion rule
    # ------------------------------------------------------------------

    def promotionEligible(self, learning_id: str
                          ) -> Tuple[bool, List[str]]:
        """PromotionEligible(L) = V ∧ P ∧ R ∧ A ∧ B ∧ N ∧ C, plus the seven
        hard refusals. Condition 0 (§3.4 — ratified calculusVersion) is
        satisfied: Decision Value Calculus V2.1 was ratified 2026-09-30
        (FLAG-001 step 4), so no CALCULUS_NOT_RATIFIED code is ever raised.
        Pure, deterministic, config-pinned (§11.1)."""
        learning = self._get(learning_id)
        codes: List[str] = []
        hard: List[str] = []

        # Investigation placeholders are inert (A12).
        if learning["internal_only"]:
            codes.append("INVESTIGATION_PLACEHOLDER_INERT")
            return False, codes

        # ---- Hard refusal conditions (§4) — checked first ----
        expected = learning.get("expected_behavior")
        if not expected or not expected.get("description"):
            hard.append(REFUSAL_NO_FUTURE_BEHAVIOR)
        if learning["state"] == "CONTRADICTED":
            hard.append(REFUSAL_CONTRADICTION)
        if learning.get("would_create_authority"):
            hard.append(REFUSAL_AUTHORITY_SMUGGLING)
        if learning.get("touches_constitutional"):
            hard.append(REFUSAL_CONSTITUTIONAL)
        if self._open_harm_window(learning):
            hard.append(REFUSAL_OPEN_HARM_WINDOW)
        if learning.get("recursive_self_modification"):
            hard.append(REFUSAL_SELF_MODIFICATION)
        if (learning["learning_type"] == "CALIBRATION_UPDATE"
                and learning.get("reduces_own_lineage_uncertainty")
                and not learning.get("disjoint_verification")):
            # §4.8: a source buying its own future promotion.
            hard.append(REFUSAL_SELF_DEALING)

        # ---- V: qualifying VERIFY result exists ----
        qualifying = [r for r in learning["verification_receipt_refs"]
                      if self._is_qualifying_verify(
                          self._verify_receipts.get(r, {}))]
        if not qualifying:
            codes.append("VERIFY_RESULT_REQUIRED")
        accepted = any(self._verify_receipts.get(r, {}).get("outcome_accepted",
                                                            True)
                       for r in qualifying)
        if qualifying and not accepted:
            codes.append("OUTCOME_NOT_ACCEPTED")
        if (learning["learning_type"] == "BEHAVIOR_RULE"
                and learning.get("causal_support_required")
                and not learning.get("causal_support")):
            codes.append("CAUSAL_SUPPORT_REQUIRED")

        # Caller-supplied "verified learning" is never trusted (§3.4).
        if learning.get("caller_asserted_verified"):
            hard.append("CALLER_ASSERTED_PROMOTION")

        # ---- P: provenance and evidence valid (§5, §17) ----
        valid, failures = self._resolve_and_validate_refs(learning)
        if not valid:
            for failure in failures:
                kind = failure.split(":")[0]
                if kind == "EVIDENCE_REFERENCE_UNRESOLVED":
                    if "EVIDENCE_REFERENCE_UNRESOLVED" not in codes:
                        codes.append("EVIDENCE_REFERENCE_UNRESOLVED")
                elif kind == "PROVENANCE_FAILURE":
                    hard.append(REFUSAL_PROVENANCE)
                elif kind == "SCOPE_MISMATCH":
                    if "SCOPE_MISMATCH" not in codes:
                        codes.append("SCOPE_MISMATCH")

        # Evidence floors (§3.3): k=5 critical / k=20 standard, by config key.
        floor = (self._config["evidenceFloor"]["critical"]
                 if learning.get("critical_claim")
                 else self._config["evidenceFloor"]["standard"])
        need = floor + (1 if learning.get("judgmental_extraction") else 0)
        if len(qualifying) < need:
            codes.append("EVIDENCE_FLOOR_NOT_MET")
        if learning.get("judgmental_extraction"):
            sources = {self._verify_receipts.get(r, {}).get("source_id", r)
                       for r in qualifying}
            if len(sources) < 2:
                codes.append("INSUFFICIENT_INDEPENDENT_EVIDENCE")

        # Systematic-bias cross-check (§1): distrusted VERIFY source -> BRIEF.
        if any(self._verify_receipts.get(r, {}).get("source_id")
               in self._distrusted_sources for r in qualifying):
            codes.append("VERIFY_SOURCE_DISTRUST")

        # ---- R: reconciliation complete (§6.3) ----
        rec = learning["reconciliation"]
        if rec["classification"] in ("UNKNOWN",):
            codes.append("PROVENANCE_INCOMPLETE")
        if learning["state"] == "CONTRADICTED":
            if "CONTRADICTS_ACTIVE_LEARNING" not in codes:
                codes.append("CONTRADICTS_ACTIVE_LEARNING")

        # ---- A: applicability explicitly defined (§3.7) ----
        applicability = learning.get("applicability", {})
        if applicability.get("state") == "UNKNOWN" and not applicability.get(
                "task_classes"):
            codes.append("APPLICABILITY_UNKNOWN")
        # Generalization ceiling (A2): Scope(L) ⊆ S_verified-source unless
        # additional transfer evidence justifies expansion.
        source_scope = {"task_classes": []}
        for r in qualifying:
            src = (self._verify_receipts.get(r, {}).get("outcome", {})
                   .get("scope", {}))
            source_scope["task_classes"] = list(
                set(source_scope["task_classes"]) | set(src.get("task_classes", [])))
        if not self._scope_subset(
                {"task_classes": learning["scope"].get("task_classes", [])},
                {"task_classes": source_scope["task_classes"]}):
            if not learning.get("transfer_expansion_evidence"):
                if "SCOPE_MISMATCH" not in codes:
                    codes.append("SCOPE_MISMATCH")

        # ---- B: behavioral effect where behavior change is claimed ----
        if learning["learning_type"] == "BEHAVIOR_RULE":
            held = [h for h in learning["heldout_evidence"] if h.get("delta_b", 0) > 0]
            if not held:
                if not learning.get("holdout_plan"):
                    codes.append("HELDOUT_REQUIRED")
                codes.append("NO_BEHAVIORAL_DELTA")
            if learning.get("claims_benefit") and not learning.get("outcome_effect"):
                codes.append("NO_OUTCOME_DELTA")

        # ---- N: negative-transfer boundary survives (§3.7) ----
        if any(n.get("overgeneralization") for n in
               learning["negative_transfer_evidence"]):
            codes.append("NEGATIVE_TRANSFER_FAILED")
        elif not learning["negative_transfer_evidence"]:
            # The unrelated-refusal check must have been run for promotion.
            codes.append("NEGATIVE_TRANSFER_FAILED")

        # ---- C: material contradictions handled ----
        open_contra = [c for c in learning["contradictions"]
                       if c.get("status") == "SURFACED"]
        if open_contra:
            if "CONTRADICTS_ACTIVE_LEARNING" not in codes:
                codes.append("CONTRADICTS_ACTIVE_LEARNING")

        # Stale learning cannot silently steer.
        if learning.get("stale"):
            codes.append("REGRESSION_DETECTED")

        # Condition 0 (§3.4): satisfied — Decision Value Calculus V2.1 is
        # RATIFIED (FLAG-001 step 4; binding in naya_kernel.node_base). No
        # stale NOT_RATIFIED code is raised here anymore.

        # §2.1: CORE-class learnings route to BRIEF, never autonomous.
        if learning.get("learning_class") == "CORE":
            codes.append("CORE_CLASS_REQUIRES_DIRECTOR")

        all_codes = hard + codes
        if hard:
            return False, all_codes
        return (len(codes) == 0), all_codes

    # ------------------------------------------------------------------
    # Promotion
    # ------------------------------------------------------------------

    def promote(self, learning_id: str) -> Dict[str, Any]:
        """Advance a learning through the machine to ACTIVE — or refuse with
        reason codes, or route to BRIEF when the CORE-class rule (or the
        §4.3/identity routes) blocks autonomous promotion. The calculus
        condition-0 BRIEF route was removed by FLAG-001 step 4 (V2.1
        ratified). Idempotent: promotion converges on one canonical state
        (§9 P32/P33)."""
        learning = self._get(learning_id)
        if learning["internal_only"]:
            raise ValueError("investigation placeholders may not be promoted "
                             "(A12)")
        if learning["state"] == "ACTIVE":
            return {"promoted": True, "already": True,
                    "receipt_id": learning["promotion"]["receipt_id"]}
        eligible, codes = self.promotionEligible(learning_id)
        hard = [c for c in codes if c in HARD_REFUSALS
                or c in ("CALLER_ASSERTED_PROMOTION",)]
        if hard:
            terminal = "REJECTED" if learning["state"] in (
                "CANDIDATE", "RECONCILING", "BLOCKED") else learning["state"]
            if terminal != learning["state"] and terminal in LEGAL_TRANSITIONS.get(
                    learning["state"], ()):
                self._transition(learning, terminal,
                                 f"hard refusal: {', '.join(hard)} (§4)")
            receipt = self._emit("PROMOTION_REFUSED", learning_id=learning_id,
                                 reason_codes=hard, eligible=False,
                                 reason="hard refusal condition (§4)")
            return {"promoted": False, "refused": True, "reason_codes": hard,
                    "receipt_id": receipt["receipt_id"]}
        brief_route = [c for c in codes
                       if c in ("CORE_CLASS_REQUIRES_DIRECTOR",
                                "VERIFY_SOURCE_DISTRUST",
                                "GOVERNANCE_PROPOSAL_ROUTED_TO_BRIEF",
                                "IDENTITY_LEARNING_ROUTED_TO_BRIEF")]
        # Governance proposals and identity/personality learnings are never
        # autonomously promoted — they route to BRIEF even when the other
        # conjuncts are met (§4.3, §10 Q7). Brief routing takes precedence
        # over autonomous promotion.
        if learning["learning_type"] == "GOVERNANCE_PROPOSAL":
            brief_route.append("GOVERNANCE_PROPOSAL_ROUTED_TO_BRIEF")
        if learning.get("touches_identity_or_personality"):
            brief_route.append("IDENTITY_LEARNING_ROUTED_TO_BRIEF")
        if brief_route:
            return self._route_to_brief(learning, brief_route)
        if not eligible:
            receipt = self._emit("PROMOTION_DEFERRED", learning_id=learning_id,
                                 reason_codes=codes, eligible=False,
                                 reason="promotion conjuncts unmet; candidate "
                                        "stays a candidate — a valid result (§9)")
            return {"promoted": False, "eligible": False,
                    "reason_codes": codes,
                    "receipt_id": receipt["receipt_id"]}

        # Eligible: walk the machine CANDIDATE → … → ACTIVE, naming gates.
        # Forward-only walk from the current machine state (fail-closed if the
        # current state is off the promotion path).
        order = ["CANDIDATE", "RECONCILING", "TEST_REQUIRED", "TESTING",
                 "EVIDENCE_REVIEW", "VERIFIED", "PROMOTION_READY", "ACTIVE"]
        if learning["state"] not in order:
            receipt = self._emit("PROMOTION_REFUSED", learning_id=learning_id,
                                 reason_codes=["INVALID_STATE_FOR_PROMOTION"],
                                 eligible=False,
                                 reason="learning not on the promotion path")
            return {"promoted": False, "refused": True,
                    "reason_codes": ["INVALID_STATE_FOR_PROMOTION"],
                    "receipt_id": receipt["receipt_id"]}
        # Gates earned by steps already completed before this promote() call
        # are named too — a promotion receipt must name its gates (§5), and
        # reconcile() may have run long before promotion.
        earned = {
            "RECONCILING": ["RECONCILIATION_COMPLETE"],
            "TEST_REQUIRED": ["APPLICABILITY_DEFINED",
                              "CAUSAL_REQUIREMENT_SATISFIED"],
            "TESTING": ["SOURCE_OUTCOME_VERIFIED"],
            "EVIDENCE_REVIEW": ["RELATED_HOLDOUT_PASS", "UNRELATED_REFUSAL_PASS",
                                "PROVENANCE_VALID",
                                "INDEPENDENT_RECOMPUTATION_PASS"],
            "VERIFIED": ["NO_MATERIAL_REGRESSION"],
        }
        gates_passed = list(earned.get(learning["state"], []))
        for step in order[order.index(learning["state"]) + 1:]:
            self._transition(learning, step, f"promotion path: -> {step}")
            gates_passed.extend(earned.get(step, []))
        # A-LEARN-5 note — the epistemic VERIFIED transition. This is the
        # sole place in the module where learning_state reaches VERIFIED
        # (it starts CANDIDATE in _new_learning and no other assignment
        # promotes it). The epistemic axis has no _transition equivalent
        # because the amendment mechanism here IS the §16 promotion path
        # executed above: the learning was proposed (as a candidate), with
        # evidence (the earned gates named per step: reconciliation,
        # applicability + causal requirement, source-outcome verification,
        # holdout passes, provenance, independent recomputation, no
        # material regression), reviewed (the promotion conjuncts
        # V∧P∧R∧A∧B∧N∧C evaluated in promote(); governance-proposal and
        # identity-touching learnings route to BRIEF and never reach
        # this line), and recorded (a receipted _transition for every
        # machine step, the PROMOTION receipt naming all gates passed,
        # and the promotion package handed to EVOLVE). This assignment
        # executes atomically inside promote() only after every conjunct
        # held — it cannot fire on a direct call that skipped the review.
        # If a future caller needs the epistemic transition without
        # promotion, it must go through an explicit amendment proposal
        # (proposal flag + record + review gate), not a direct assignment.
        learning["learning_state"] = "VERIFIED"
        learning["adoption_state"] = "ACTIVE"
        learning["verified_at"] = learning["verified_at"] or self._now()
        learning["promoted_at"] = self._now()
        package = self.promotion_package(learning_id)
        receipt = self._emit(
            "PROMOTION", learning_id=learning_id,
            gates_passed=sorted(set(gates_passed)),
            promotion_eligible=True, promotion_reason_codes=[],
            promotion_package_ref=package["package_id"],
            handoff_to="EVOLVE",
            reason="promotion conjuncts V∧P∧R∧A∧B∧N∧C met; condition 0 met",
        )
        learning["promotion"] = {"receipt_id": receipt["receipt_id"],
                                 "gates": sorted(set(gates_passed)),
                                 "package_id": package["package_id"]}
        return {"promoted": True, "gates": sorted(set(gates_passed)),
                "receipt_id": receipt["receipt_id"],
                "package_id": package["package_id"]}

    def _route_to_brief(self, learning: Dict[str, Any],
                        codes: List[str]) -> Dict[str, Any]:
        """Condition-0 / CORE / distrust / governance / identity routing: the
        learning becomes PROMOTION_READY → DEFERRED with a promotion package
        in the BRIEF outbox. The package is a proposal; only the proper
        authority ratifies (A9, §10 Q7)."""
        # Forward-only walk to PROMOTION_READY (fail-closed off-path).
        order = ["CANDIDATE", "RECONCILING", "TEST_REQUIRED", "TESTING",
                 "EVIDENCE_REVIEW", "VERIFIED", "PROMOTION_READY"]
        if learning["state"] not in order + ["DEFERRED"]:
            raise ValueError("learning not on the brief-route path")
        if learning["state"] != "DEFERRED":
            for step in order[order.index(learning["state"]) + 1:]:
                self._transition(learning, step, "brief-route path")
        if learning["state"] == "PROMOTION_READY":
            self._transition(learning, "DEFERRED",
                             f"routed to BRIEF: {', '.join(codes)}")
        package = self.promotion_package(learning["id"])
        package["route"] = "BRIEF"
        package["route_codes"] = codes
        self._brief_outbox.append(package)
        receipt = self._emit(
            "PROMOTION_ROUTED_TO_BRIEF", learning_id=learning["id"],
            reason_codes=codes, package_id=package["package_id"],
            handoff_to="BRIEF",
            reason="autonomous promotion not permitted; proposal routed to "
                   "authority (condition 0 / CORE / distrust / governance / "
                   "identity)")
        return {"promoted": False, "routed_to_brief": True,
                "reason_codes": codes, "package_id": package["package_id"],
                "receipt_id": receipt["receipt_id"]}

    # ------------------------------------------------------------------
    # Promotion package (§1, §7.1): the LEARN → EVOLVE baton
    # ------------------------------------------------------------------

    def promotion_package(self, learning_id: str) -> Dict[str, Any]:
        """Typed PromotionPackage — verified lesson, exact scope, behavioral
        and outcome evidence, generalization evidence, negative-transfer
        evidence, limitations, regression guard, value/calibration evidence,
        source lineage, promotion status, required authority.

        Spec §3.4 — the promotion rule; §5 provenance/promotion seam."""
        learning = self._get(learning_id)
        self._seq += 1
        package = {
            "package_id": f"pp-{_hash([learning_id, self._seq])[:16]}",
            "node_id": NODE_ID,
            "learning_id": learning_id,
            "lesson": learning["lesson"],
            "learning_type": learning["learning_type"],
            "owner_id": learning["owner_id"],
            "scope": learning["scope"],
            "applicability": learning["applicability"],
            "validity_envelope": learning["validity_envelope"],
            "behavioral_evidence": learning["heldout_evidence"],
            "outcome_evidence": learning.get("outcome_effect"),
            "generalization_evidence": learning["generalization_evidence"],
            "negative_transfer_evidence": learning["negative_transfer_evidence"],
            "limitations": list(learning["applicability"].get("limitations", [])),
            "regression_guards": learning["regression_guards"],
            "value_effect": learning["value_effect"],
            "calibration": learning["calibration"],
            "source_lineage": {
                "source_outcome_refs": learning["source_outcome_refs"],
                "verification_receipt_refs": learning["verification_receipt_refs"],
                "cvo_refs": learning["cvo_refs"],
                "evidence_refs": learning["evidence_refs"],
                "extraction_log": learning["extraction_log"],
                "lineage": list(CANONICAL_LINEAGE),
            },
            "promotion_status": learning["state"],
            "required_authority": self._required_authority_for(learning),
            "authority_created": False,
            "configHash": learning["config_hash"],
            "calculusVersion": self._config["calculusVersion"],
            "calculusConfigHash": CALCULUS_V21_SPEC_HASH,
            "package_hash": None,
            "timestamp": self._now(),
        }
        package["package_hash"] = _hash(
            {k: v for k, v in package.items() if k != "package_hash"})
        return package

    @staticmethod
    def _required_authority_for(learning: Dict[str, Any]) -> str:
        if learning.get("learning_class") == "CORE":
            return "DIRECTOR"
        if learning["learning_type"] in ("RECALIBRATION", "GOVERNANCE_PROPOSAL"):
            return "DIRECTOR"
        if learning.get("touches_identity_or_personality"):
            return "DIRECTOR"
        return "KERNEL_OPERATOR"

    def validate_promotion_package(self, package: Dict[str, Any]
                                   ) -> Tuple[bool, List[str]]:
        """§7.1 trust-on-receipt refusal: EVOLVE validates the package schema
        and re-checks the §17 seam on receipt. A defective package is returned
        with reason codes, never partially applied."""
        required = ("package_id", "learning_id", "lesson", "owner_id", "scope",
                    "source_lineage", "promotion_status", "required_authority",
                    "package_hash")
        missing = [k for k in required if k not in package]
        codes: List[str] = [f"MISSING:{k}" for k in missing]
        if package.get("authority_created"):
            codes.append("AUTHORITY_BOUNDARY_VIOLATION")
        lineage = (package.get("source_lineage") or {})
        if not lineage.get("verification_receipt_refs"):
            codes.append("VERIFY_RESULT_REQUIRED")
        stored = package.get("package_hash")
        if stored is not None and _hash(
                {k: v for k, v in package.items()
                 if k != "package_hash"}) != stored:
            codes.append("PROVENANCE_FAILURE")
        return (len(codes) == 0), codes

    # ------------------------------------------------------------------
    # §3.5 — governed calibration loop; §1 systematic-bias cross-check
    # ------------------------------------------------------------------

    def record_calibration(self, source_id: str, deltaV_pred: float,
                           deltaV_actual: float) -> Dict[str, Any]:
        """Consume VERIFY's comparison of ∆V_predicted with ∆V_actual.
        Persistent bias or increasing error produces a VALUE_RECALIBRATION
        *candidate* — it does not mutate the active profile. Calibration
        error creates a candidate, never an active parameter change (§3.5).
        There is no automatic quarantine: a badly calibrated source never
        inflates its own U (refused per §4.7)."""
        entry = self._calibration.setdefault(
            source_id, {"errors": [], "bias": 0.0, "mae": 0.0})
        error = deltaV_actual - deltaV_pred
        entry["errors"].append(error)
        n = len(entry["errors"])
        entry["bias"] = sum(entry["errors"]) / n
        entry["mae"] = sum(abs(e) for e in entry["errors"]) / n
        tau_b = self._config["calibration"]["biasTau"]
        tau_e = self._config["calibration"]["maeTau"]
        min_n = self._config["calibration"]["minSamples"]
        receipt = self._emit("CALIBRATION_SAMPLE", source_id=source_id,
                             bias=entry["bias"], mae=entry["mae"], n=n,
                             reason="§3.5 calibration loop sample")
        if n >= min_n and (abs(entry["bias"]) > tau_b or entry["mae"] > tau_e):
            candidate = self._new_learning(
                lesson=(f"value-calibration of source {source_id}: "
                        f"bias={entry['bias']:.4f}, mae={entry['mae']:.4f}"),
                learning_type="RECALIBRATION",
                owner_id="kernel",
                scope={"task_classes": ["calibration"], "source_id": source_id},
                applicability={"state": "UNKNOWN", "task_classes": [],
                               "limitations": ["recalibration-candidate-only"]},
                source_outcome_refs=[f"calibration:{source_id}"],
                expected_behavior=None,
            )
            candidate["recalibration_target"] = source_id
            cand_receipt = self._emit(
                "VALUE_RECALIBRATION_CANDIDATE",
                learning_id=candidate["id"], source_id=source_id,
                bias=entry["bias"], mae=entry["mae"],
                reason="calibration error creates a CANDIDATE, never an "
                       "active parameter change (§3.5)")
            return {"candidate_created": candidate["id"],
                    "receipt_id": cand_receipt["receipt_id"],
                    "bias": entry["bias"], "mae": entry["mae"]}
        return {"candidate_created": None, "receipt_id": receipt["receipt_id"],
                "bias": entry["bias"], "mae": entry["mae"]}

    def flag_verify_source_distrust(self, source_id: str, reason: str
                                    ) -> Dict[str, Any]:
        """§1 systematic-bias cross-check: when calibration error attributable
        to a VERIFY source is persistently high, LEARN raises a
        VERIFY_SOURCE_DISTRUST candidate and holds affected promotions to
        BRIEF. The baton is one-directional for evidence flow, not for trust."""
        self._distrusted_sources[source_id] = reason
        candidate = self._new_learning(
            lesson=f"VERIFY source distrust: {source_id} — {reason}",
            learning_type="FACT_UPDATE",
            owner_id="kernel",
            scope={"task_classes": ["verification-trust"]},
            applicability={"state": "UNKNOWN", "task_classes": [],
                           "limitations": ["trust-assessment-only"]},
            source_outcome_refs=[f"distrust:{source_id}"],
            expected_behavior=None,
        )
        receipt = self._emit("VERIFY_SOURCE_DISTRUST",
                             learning_id=candidate["id"], source_id=source_id,
                             reason=reason)
        return {"distrusted": source_id, "candidate_id": candidate["id"],
                "receipt_id": receipt["receipt_id"]}

    # ------------------------------------------------------------------
    # §4.3/A9 — governance-change routing; §10 Q7 identity routing
    # ------------------------------------------------------------------

    def design_governance_proposal(self, learning_id: str) -> Dict[str, Any]:
        """A verified lesson of the form 'policy X caused recurring friction'
        may produce a *governance change proposal*; only the proper authority
        ratifies a new policy. Lessons never silently rewrite governance.

        Spec §4.3 — governance/identity proposals route to BRIEF, never autonomous promotion."""
        learning = self._get(learning_id)
        if learning["learning_type"] != "GOVERNANCE_PROPOSAL":
            raise ValueError("not a GOVERNANCE_PROPOSAL learning")
        proposal = {
            "proposal_id": f"gp-{_hash([learning_id, self._now()])[:16]}",
            "learning_id": learning_id,
            "lesson": learning["lesson"],
            "proposed_change": learning.get("proposed_change"),
            "status": "PROPOSED",
            "ratified_by": None,
            "note": "proposal only — ratification belongs to the proper "
                    "authority (§4.3, A9)",
        }
        self._brief_outbox.append(proposal)
        receipt = self._emit("GOVERNANCE_PROPOSAL", learning_id=learning_id,
                             proposal_id=proposal["proposal_id"],
                             handoff_to="BRIEF",
                             reason="governance proposal routed to authority "
                                    "(A9)")
        return {"proposal_id": proposal["proposal_id"],
                "receipt_id": receipt["receipt_id"]}

    def refuse_caller_promotion(self, claim: Dict[str, Any]) -> Dict[str, Any]:
        """No caller-supplied 'verified learning' is ever trusted: promotion
        status is computed from canonical evidence, never asserted by a
        caller (§3.4)."""
        receipt = self._emit(
            "CALLER_PROMOTION_REFUSED",
            reason_code="CALLER_ASSERTED_PROMOTION",
            reason="promotion asserted by caller, not computed from canonical "
                   "evidence — refused (§3.4)",
            claim=dict(claim),
        )
        return {"accepted": False, "reason_code": "CALLER_ASSERTED_PROMOTION",
                "receipt_id": receipt["receipt_id"]}

    # ------------------------------------------------------------------
    # §6.2 — TESTING serving (live in the KNOW serving path, in scope)
    # ------------------------------------------------------------------

    def serve(self, learning_id: str, task_class: str,
              task_ref: Optional[str] = None) -> Dict[str, Any]:
        """A learning in TESTING or ACTIVE phase is servable within its
        declared scope. Patience remains a safety property: an open delayed-
        harm window refuses serving. Stale learning cannot silently steer.

        Spec §6 — graph, reconciliation, and serving."""
        learning = self._get(learning_id)
        if learning["internal_only"]:
            return {"served": False, "reason_code": "INVESTIGATION_PLACEHOLDER_INERT"}
        # Stale learning cannot silently steer (P27); patience remains a
        # safety property — these refusals are checked before phase so the
        # reason code names the real blocker.
        if learning.get("stale"):
            return {"served": False, "reason_code": "REGRESSION_DETECTED"}
        if self._open_harm_window(learning):
            return {"served": False, "reason_code": "OPEN_HARM_WINDOW"}
        if learning["state"] not in ("TESTING", "ACTIVE"):
            return {"served": False, "reason_code": "NOT_IN_SERVING_PHASE",
                    "state": learning["state"]}
        declared = set(learning["scope"].get("task_classes", []))
        if task_class in declared:
            verdict = "APPLICABLE"
        elif declared:
            verdict = "NOT_APPLICABLE"
        else:
            # UNKNOWN != broad APPLICABLE (P25): heuristic inference never
            # outranks explicit metadata (P26).
            verdict = "UNKNOWN"
        return {"served": verdict == "APPLICABLE", "applicability": verdict,
                "learning_id": learning_id, "task_class": task_class,
                "task_ref": task_ref}

    # ------------------------------------------------------------------
    # §11.3 — recompute: MATCH | MISMATCH
    # ------------------------------------------------------------------

    def recompute(self, learning_id: str) -> Dict[str, Any]:
        """Re-derive the promotion decision from the pinned configHash and
        content-addressed provenance. A mismatch is a provenance-loss alarm
        (§11.3; the cold-successor and provenance-loss test)."""
        learning = self._get(learning_id)
        stored = learning.get("promotion")
        if stored is None:
            return {"result": "MISMATCH",
                    "reason": "no sealed promotion decision to recompute"}
        key = _learning_key(learning["owner_id"], learning["lesson"],
                            "|".join(sorted(learning["source_outcome_refs"])),
                            learning["scope"], learning["applicability"])
        key_ok = (key == learning["learning_key"])
        eligible, codes = self.promotionEligible(learning_id)
        eligible_ok = (eligible is True)  # stored promotions were eligible
        receipt = self._emit(
            "RECOMPUTE", learning_id=learning_id,
            key_match=key_ok, eligible_match=eligible_ok,
            reason="§11.3 recompute (cold-successor / provenance-loss test)")
        if key_ok and eligible_ok:
            return {"result": "MATCH", "receipt_id": receipt["receipt_id"]}
        alarm = self._emit("PROVENANCE_LOSS_ALARM", learning_id=learning_id,
                           reason="recompute MISMATCH — promotion decision "
                                  "does not re-derive from pinned provenance")
        return {"result": "MISMATCH", "receipt_id": alarm["receipt_id"],
                "key_match": key_ok, "eligible_match": eligible_ok}

    # ------------------------------------------------------------------
    # NodeBase contract
    # ------------------------------------------------------------------

    def manifest_entry(self) -> ManifestEntry:
        """Return this node's manifest entry (candidate spec, §9 acceptance battery)."""
        return ManifestEntry(
            node_id=NODE_ID,
            version="V1-CANDIDATE",
            responsibilities=[
                "consume only verified receipts (VERIFY→LEARN baton)",
                "deterministic extraction Extract(O) -> L_candidate (§1.4)",
                "evidence floors k=5/20 with no magical Learning Score (§3.3)",
                "promotion rule V∧P∧R∧A∧B∧N∧C + ratified-calculus condition 0",
                "seven hard refusal conditions, receipted (§4)",
                "reconciliation: duplicates reused, contradictions preserved",
                "held-out / negative-transfer law; generalization ceiling",
                "governed calibration loop producing candidates, never mutations",
                "typed PromotionPackage baton to EVOLVE (§7.1)",
                "hash-bound receipts; recompute MATCH/MISMATCH (§11.3)",
            ],
        )

    def persisted_transitions(self) -> List[str]:
        """List the receipt transitions this node persists (candidate spec, §9 acceptance battery)."""
        return [f"{frm}->{to}"
                for frm, tos in LEGAL_TRANSITIONS.items() for to in tos]

    def evidence_hooks(self) -> List[str]:
        """List the evidence hooks this node exposes (candidate spec, §9 acceptance battery)."""
        return [
            "verify_receipt_registry",
            "cvo_registry",
            "evidence_registry",
            "extraction_log",
            "candidate_pool",
            "learning_ledger",
            "calibration_record",
            "promotion_package_outbox",
            "brief_outbox",
        ]

    def authority_checks(self) -> List[str]:
        """Declare this node's authority checks; declares, never grants (candidate spec, §9 acceptance battery)."""
        # LEARN performs these validations and grants nothing. The first entry
        # is the negation convention tests assert.
        return [
            NO_AUTHORITY_GRANT,
            "node-invocation authority separate from promotion authority",
            "governance proposals require director/authority ratification",
            "CORE-class learning promotion requires director word",
            "no learning applied to LEARN's own scoring without ratified change",
            "identity/personality learnings route to BRIEF/governance",
            "EVOLVE validates promotion packages; trust on receipt refused",
            "no caller-supplied verified learning trusted",
        ]

    def gate(self, state: Dict[str, Any]) -> GateResult:
        """LEARN's gate: evaluate a learning-transition request. Hard refusals
        FAIL; promotion-eligible requests PASS; anything unproven is
        NEED_EVIDENCE with reason codes. Never invent PASS (§4, §3.4)."""
        action = (state or {}).get("action")
        learning_id = (state or {}).get("learning_id")
        if action not in ("propose_candidate", "promote", "serve",
                          "recalibrate", "extract"):
            return GateResult(GateVerdict.FAIL,
                              ["unknown action for LEARN gate"])
        if action == "propose_candidate":
            proposal = state.get("proposal", {})
            if not (proposal.get("expected_behavior") or {}).get("description"):
                return GateResult(GateVerdict.FAIL,
                                  [REFUSAL_NO_FUTURE_BEHAVIOR,
                                   "a learning that changes nothing is not a "
                                   "learning (§4.1)"])
            return GateResult(GateVerdict.NEED_EVIDENCE,
                              ["VERIFY_RESULT_REQUIRED",
                               "candidate admitted; evidence still required"])
        if learning_id is None:
            return GateResult(GateVerdict.FAIL, ["learning_id required"])
        try:
            learning = self._get(learning_id)
        except KeyError:
            return GateResult(GateVerdict.FAIL, ["unknown learning_id"])
        if action == "promote":
            eligible, codes = self.promotionEligible(learning_id)
            hard = [c for c in codes if c in HARD_REFUSALS
                    or c in ("CALLER_ASSERTED_PROMOTION",)]
            if hard:
                return GateResult(GateVerdict.FAIL, hard)
            if eligible:
                return GateResult(GateVerdict.PASS, ["promotion conjuncts met"])
            return GateResult(GateVerdict.NEED_EVIDENCE, codes)
        if action == "serve":
            task_class = state.get("task_class", "")
            result = self.serve(learning_id, task_class)
            if result.get("applicability") == "APPLICABLE":
                return GateResult(GateVerdict.PASS, ["servable in scope"])
            if result.get("reason_code") in ("OPEN_HARM_WINDOW",):
                return GateResult(GateVerdict.FAIL, [result["reason_code"]])
            return GateResult(GateVerdict.NEED_EVIDENCE,
                              [result.get("reason_code", "NOT_APPLICABLE")])
        if action == "recalibrate":
            if learning["learning_type"] != "RECALIBRATION":
                return GateResult(GateVerdict.FAIL,
                                  ["not a RECALIBRATION candidate"])
            # V2.1 is ratified (FLAG-001 step 4) — no CALCULUS_NOT_RATIFIED
            # branch. Recalibration still proposes only; authority applies.
            return GateResult(GateVerdict.NEED_EVIDENCE,
                              ["AUTHORITY_BOUNDARY_VIOLATION",
                               "recalibration candidate; authority must apply"])
        # action == "extract"
        return GateResult(GateVerdict.NEED_EVIDENCE, ["VERIFY_RESULT_REQUIRED"])

    def cold_reconstruct(self, receipts: List[Dict[str, Any]]
                         ) -> Dict[str, Any]:
        """Rebuild LEARN's durable state from receipts alone (cold start).

        Replays receipts in timestamp order, re-running hash verification on
        every sealed receipt. Investigation placeholders are preserved as
        inert. Answers the five successor questions (§9 P37/P40): the cold
        successor can retrieve by identifier, see applicable scope, refuse
        unrelated application, knows fresh LAW authority is required for any
        governed act, and inherits intelligence — never authority.
        """
        ordered = sorted(receipts or [], key=lambda r: r.get("timestamp", ""))
        state: Dict[str, Any] = {
            "learnings": {},
            "transitions": 0,
            "promotions": [],
            "determinism": {"checked": 0, "matched": 0, "mismatched": []},
            "investigation_placeholders": [],
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
            lid = receipt.get("learning_id")
            if rtype == "TRANSITION":
                state["transitions"] += 1
                if lid:
                    entry = state["learnings"].setdefault(lid, {
                        "state": None, "lesson": receipt.get("lesson"),
                        "authority_created": []})
                    entry["state"] = receipt.get("state_after")
            elif rtype in ("PROMOTION", "PROMOTION_ROUTED_TO_BRIEF",
                           "PROMOTION_REFUSED", "PROMOTION_DEFERRED"):
                if lid:
                    state["learnings"].setdefault(lid, {})["promotion"] = {
                        "receipt_type": rtype,
                        "eligible": receipt.get("promotion_eligible"),
                        "gates": receipt.get("gates_passed", []),
                    }
                    state["promotions"].append(
                        {"learning_id": lid, "type": rtype})
                if receipt.get("authority_created"):
                    # Invariant violated in the replayed receipt: record, do
                    # not trust.
                    entry = state["learnings"].setdefault(lid or "unknown", {})
                    entry.setdefault("authority_created",
                                     []).append(receipt.get("receipt_id"))
            elif rtype == "INVESTIGATION_PLACEHOLDER":
                if lid:
                    state["investigation_placeholders"].append(lid)
        state["successor_answers"] = {
            # identifier → retrieve: every replayed learning is retrievable
            # by its content-derived id.
            "retrieve_by_id": sorted(state["learnings"].keys()),
            # scope retained per learning; the successor must check it.
            "scope_check_required": True,
            # unrelated application refused: UNKNOWN != broad APPLICABLE.
            "refuse_unrelated": True,
            # any governed act needs fresh LAW authority — LEARN receipts
            # carry authority_created=false, never a grant.
            "fresh_authority_required": True,
            # intelligence inherited, authority never inherited.
            "intelligence_inherited_not_authority": all(
                not entry.get("authority_created")
                for entry in state["learnings"].values()),
        }
        return state
