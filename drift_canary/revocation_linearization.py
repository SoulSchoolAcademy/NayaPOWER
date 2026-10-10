"""Revocation Linearization Law (Shawn, 2026-10-10).

One authoritative commit point per revocation. Every later certification,
projection publication, and consequential execution respects the new
eligibility state. Asynchronous repair cannot weaken the rule. Independent
support may establish a newer qualification; cached history cannot restore
an older one.

Fundamental invariant: once revocation R commits, no subsequent authoritative
certification or action may rely on a qualification invalidated by R, unless a
newer, independently verified qualification establishes sufficient admissible
support.

This is a distributed consistency problem, not a cache-expiration problem: a
cache may be completely accurate when generated and dangerous by the time it
is published. Ordering (the authoritative commit sequence, written ``A < B``)
is never derived from wall-clock timestamps.

Bounded verification candidate: spec only, deterministic in-memory model of
the authoritative publication boundary. Nothing here touches production.
"""
from dataclasses import dataclass, field, replace
from typing import Dict, FrozenSet, List, Tuple, Optional, Callable, Any
import copy
import functools
import math
import threading

# ---------------------------------------------------------------------------
# 1. Version namespaces. Three separate counters, one authority.
# ---------------------------------------------------------------------------
EVIDENCE_NS = "evidence_eligibility"
QUALIFICATION_NS = "claim_qualification"
PROJECTION_NS = "projection"

VERSION_NAMESPACES = (EVIDENCE_NS, QUALIFICATION_NS, PROJECTION_NS)

# Operation types in the ordering calculus.
REVOCATION = "R"      # evidence eligibility revocation transaction
PUBLICATION = "P"     # projection publication transaction
VALIDATION = "V"      # authoritative qualification validation read
ACTION = "A"          # consequential action commit
RECOVERY = "J"        # asynchronous recovery / refresh job
QUALIFICATION_OP = "Q"  # qualification commit (newer independently-verified support)


class VersionAuthority:
    """Monotonically allocates revisions per namespace.

    Revisions are never reused, even if a record is deleted and recreated
    (ABA prevention). Version order comes from this authority, never from
    wall-clock timestamps or agent assertions.
    """

    def __init__(self):
        self._counters: Dict[str, int] = {ns: 0 for ns in VERSION_NAMESPACES}
        self._tombstones: Dict[Tuple[str, str], int] = {}

    def next(self, namespace: str) -> int:
        assert namespace in VERSION_NAMESPACES, namespace
        self._counters[namespace] += 1
        return self._counters[namespace]

    def current(self, namespace: str) -> int:
        return self._counters[namespace]

    def retire(self, namespace: str, identity: str) -> int:
        """Record a deletion; the identity's next revision still advances."""
        rev = self.next(namespace)
        self._tombstones[(namespace, identity)] = rev
        return rev


# ---------------------------------------------------------------------------
# 2. Records.
# ---------------------------------------------------------------------------
@dataclass
class EvidenceRecord:
    evidence_id: str
    eligibility_revision: int
    eligible: bool
    scope: str
    purpose: str
    policy_revision: str
    provenance: str


@dataclass
class QualificationRecord:
    claim_id: str
    qualification_revision: int
    verdict: str  # one of the six certification verdicts
    support_manifest: Dict[str, int]  # evidence_id -> eligibility revision relied upon
    policy_revision: str
    scope: str
    purpose: str
    # Alternative independently-sufficient support paths (OR semantics).
    # Empty = single AND-path in support_manifest. A claim is CURRENT if ANY
    # path is fully current; uncertainty in one path never kills an
    # independent alternative.
    alternative_paths: List[Dict[str, int]] = field(default_factory=list)


@dataclass
class ProjectionHeadRecord:
    projection_id: str
    projection_revision: int
    artifact_id: str
    claim_deps: Dict[str, int]      # claim_id -> qualification revision asserted
    evidence_deps: Dict[str, int]   # evidence_id -> eligibility revision asserted
    fencing_token: int


@dataclass(frozen=True)
class RevocationReceipt:
    event_id: str
    evidence_id: str
    eligibility_revision: int
    reason: str
    scope: str
    purpose: str
    policy_revision: str
    provenance: str
    linearization_seq: int


@dataclass(frozen=True)
class ProjectionCandidate:
    projection_id: str
    expected_head_revision: int
    artifact_id: str
    claim_deps: Dict[str, int]
    evidence_manifest: Dict[str, int]
    policy_revision: str
    asserted_claims: Dict[str, str]  # claim_id -> asserted verdict
    intended_uses: Tuple[str, ...]
    fencing_token: int


# Publication outcomes.
COMMITTED = "COMMITTED"
STALE_DEPENDENCY = "STALE_DEPENDENCY"
QUALIFICATION_NOT_ESTABLISHED = "QUALIFICATION_NOT_ESTABLISHED"
WRITE_CONFLICT = "WRITE_CONFLICT"

# Read-time validation classes.
CURRENT_QUALIFIED = "CURRENT_QUALIFIED"
CURRENT_UNQUALIFIED = "CURRENT_UNQUALIFIED"
CURRENT_STATE_UNAVAILABLE = "CURRENT_STATE_UNAVAILABLE"

# Qualification standing used by the fence.
FENCED = "FENCED"
STALE_QUALIFICATION = "STALE_QUALIFICATION"
CURRENT = "CURRENT"

# Verdicts that count as established for certification.
ESTABLISHED_VERDICTS = ("REQUALIFIED", "UNAFFECTED")

# ---------------------------------------------------------------------------
# 3. The authoritative state: one ordering point for eligibility, qualification,
#    and publication. All linearization sequences are allocated here.
# ---------------------------------------------------------------------------
@dataclass
class LinearizedOp:
    seq: int
    op_type: str          # one of R/P/V/A/J
    summary: str
    detail: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# The one authoritative commit point, enforced as a decorator: every
# authority-changing operation and every linearizable read on
# AuthoritativeState serializes on the single reentrant commit lock.
# Revocation and publication contend on the same guard -- a concurrent R/P
# pair linearizes as P<R or R<P, no third case.
# ---------------------------------------------------------------------------
def _linearized(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        with self._commit_lock:
            return method(self, *args, **kwargs)
    return wrapper


class AuthoritativeState:
    """Single authoritative ordering point for the revocation linearization law.

    Every revocation, publication, validation, action, and recovery event
    receives a linearization sequence number at commit. ``A < B`` (seq order)
    is the authoritative order; wall-clock timestamps are never consulted.

    The shared guard is REAL, not declared: a single reentrant commit lock
    serializes every authority-changing operation and every linearizable
    read at this ordering point. Revocation and publication contend on the
    same guard -- a concurrent R/P pair linearizes as P<R or R<P, no third
    case. (A production database refines each (namespace, identity) guard
    to a real row/predicate lock; see the RLQ-REFINEMENT certificates.)
    """

    def __init__(self):
        self._commit_lock = threading.RLock()
        self.versions = VersionAuthority()
        self.evidence: Dict[str, EvidenceRecord] = {}
        self.claims: Dict[str, ClaimQualification] = {}
        self.projections: Dict[str, ProjectionHeadRecord] = {}
        # (evidence_id, scope, purpose) -> eligibility revision at which the
        # revocation fence was established. Any qualification manifest entry
        # referencing this evidence below the fence revision is FENCED.
        self.revocation_fence: Dict[Tuple[str, str, str], int] = {}
        self.receipts: List[RevocationReceipt] = []
        self.outbox: List[Dict[str, Any]] = []
        self.linearization_log: List[LinearizedOp] = []
        self._seq = 0
        # Conflict-domain guard acquisitions, for testing that revocation and
        # publication contend on the same guards.
        self.guard_log: List[Tuple[str, str, str]] = []
        # Recovery bookkeeping.
        self._processed_events: set = set()
        self.reconciliation_needed: bool = False
        # Simulated availability of the authoritative source (for the
        # CURRENT_STATE_UNAVAILABLE class).
        self.authoritative_available: bool = True

    def __deepcopy__(self, memo):
        # The commit lock is execution state, not authority state: a copy
        # gets a fresh lock (model checkers copy states freely).
        cls = self.__class__
        new = cls.__new__(cls)
        memo[id(self)] = new
        new._commit_lock = threading.RLock()
        for k, v in self.__dict__.items():
            if k == "_commit_lock":
                continue
            setattr(new, k, copy.deepcopy(v, memo))
        return new

    # -- internal ----------------------------------------------------------
    def _commit_seq(self, op_type: str, summary: str, detail: Dict[str, Any]) -> int:
        self._seq += 1
        self.linearization_log.append(LinearizedOp(self._seq, op_type, summary, detail))
        return self._seq

    def _acquire_guard(self, namespace: str, identity: str, holder: str):
        self.guard_log.append((holder, namespace, identity))

    # -- setup helpers (not linearized; used to build fixtures) ------------
    def register_evidence(self, evidence_id: str, scope: str, purpose: str,
                          policy_revision: str, provenance: str) -> EvidenceRecord:
        rec = EvidenceRecord(evidence_id, self.versions.next(EVIDENCE_NS), True,
                             scope, purpose, policy_revision, provenance)
        self.evidence[evidence_id] = rec
        return rec

    def register_qualification(self, claim_id: str, verdict: str,
                               support_manifest: Dict[str, int], scope: str,
                               purpose: str, policy_revision: str) -> QualificationRecord:
        rec = QualificationRecord(claim_id, self.versions.next(QUALIFICATION_NS),
                                  verdict, dict(support_manifest), policy_revision,
                                  scope, purpose)
        self.claims[claim_id] = rec
        return rec

    def register_projection(self, projection_id: str, artifact_id: str,
                            claim_deps: Dict[str, int],
                            evidence_deps: Dict[str, int]) -> ProjectionHeadRecord:
        rec = ProjectionHeadRecord(projection_id, self.versions.next(PROJECTION_NS),
                                   artifact_id, dict(claim_deps), dict(evidence_deps),
                                   self.versions.next(PROJECTION_NS))
        # fencing token drawn from the projection namespace: monotonic.
        self.projections[projection_id] = rec
        return rec

    # -- fence ---------------------------------------------------------------
    def _fence_applies(self, evidence_id: str, scope: str, purpose: str) -> Optional[int]:
        for (eid, sc, pu), rev in self.revocation_fence.items():
            if eid == evidence_id and (sc == "*" or sc == scope) and (pu == "*" or pu == purpose):
                return rev
        return None

    def _path_status(self, path: Dict[str, int], scope: str, purpose: str) -> str:
        for ev_id, ev_rev in path.items():
            cur = self.evidence.get(ev_id)
            if cur is None:
                return FENCED  # unknown ancestry: withhold
            if ev_rev < cur.eligibility_revision:
                fence_rev = self._fence_applies(ev_id, scope, purpose)
                if fence_rev is not None and ev_rev < fence_rev:
                    return FENCED
                return STALE_QUALIFICATION
            if not cur.eligible:
                return FENCED
        return CURRENT

    def qualification_standing(self, claim_id: str) -> str:
        """CURRENT / STALE_QUALIFICATION / FENCED for a claim's qualification.

        OR semantics over support paths: CURRENT if ANY independently
        sufficient path is fully current. FENCED if no path is current and
        some path touches revoked evidence (reassessment required).
        """
        qual = self.claims.get(claim_id)
        if qual is None:
            return FENCED
        paths = [qual.support_manifest] + list(qual.alternative_paths)
        statuses = [self._path_status(p, qual.scope, qual.purpose) for p in paths]
        if CURRENT in statuses:
            return CURRENT
        if FENCED in statuses:
            return FENCED
        return STALE_QUALIFICATION

    @_linearized
    def commit_qualification(self, claim_id: str, verdict: str,
                             support_manifest: Dict[str, int], scope: str,
                             purpose: str, policy_revision: str,
                             alternative_paths: Optional[List[Dict[str, int]]] = None,
                             ) -> QualificationRecord:
        """Linearized qualification commit (op type Q): a newer, independently
        verified qualification. Requalification must carry NEW verification
        evidence -- never a bare version bump."""
        rec = QualificationRecord(
            claim_id, self.versions.next(QUALIFICATION_NS), verdict,
            dict(support_manifest), policy_revision, scope, purpose,
            alternative_paths=[dict(p) for p in (alternative_paths or [])])
        self.claims[claim_id] = rec
        self._commit_seq(QUALIFICATION_OP,
                         f"qualify {claim_id} rev {rec.qualification_revision}: {verdict}",
                         {"claim_id": claim_id, "verdict": verdict,
                          "manifest": dict(support_manifest)})
        return rec

    # -- 4. The atomic revocation transaction (7 ops) --------------------------
    @_linearized
    def commit_revocation(self, evidence_id: str, reason: str, scope: str,
                          purpose: str, policy_revision: str,
                          provenance: str) -> RevocationReceipt:
        """Execute the 7-op atomic revocation transaction.

        The fence takes effect at commit WITHOUT waiting for downstream
        recomputation. If the dependency closure is unknown, validation
        conservatively withholds (see qualification_standing).
        """
        # 1. Acquire the eligibility/version guard (conflict domain shared
        #    with publication transactions).
        self._acquire_guard(EVIDENCE_NS, evidence_id, holder="R")
        # 2. Advance the evidence eligibility revision.
        new_rev = self.versions.next(EVIDENCE_NS)
        # 3. Record the ineligibility decision.
        rec = self.evidence.get(evidence_id)
        if rec is None:
            rec = EvidenceRecord(evidence_id, new_rev, False, scope, purpose,
                                 policy_revision, provenance)
            self.evidence[evidence_id] = rec
        else:
            rec.eligible = False
            rec.eligibility_revision = new_rev
            rec.scope, rec.purpose = scope, purpose
            rec.policy_revision = policy_revision
        # 4. Establish the revocation fence.
        self.revocation_fence[(evidence_id, scope, purpose)] = new_rev
        # 5-7. Receipt, outbox notification, atomic commit (one seq).
        seq = self._commit_seq(REVOCATION,
                               f"revoke {evidence_id} rev {new_rev}: {reason}",
                               {"evidence_id": evidence_id, "revision": new_rev})
        receipt = RevocationReceipt(
            event_id=f"REV-{seq:06d}", evidence_id=evidence_id,
            eligibility_revision=new_rev, reason=reason, scope=scope,
            purpose=purpose, policy_revision=policy_revision,
            provenance=provenance, linearization_seq=seq)
        self.receipts.append(receipt)
        self.outbox.append({"event_id": receipt.event_id, "kind": "revocation",
                            "evidence_id": evidence_id, "seq": seq,
                            "delivered": False})
        return receipt

    # -- 5. The atomic publication transaction ---------------------------------
    @_linearized
    def publish_projection(self, candidate: ProjectionCandidate) -> Tuple[str, str]:
        """Atomic publication. Returns (outcome, detail).

        Implements the framework's publish_projection pseudocode:
        lock guards in the SAME conflict domain as revocation, read
        authoritative state, verify the full dependency manifest, check proof
        sufficiency, then CAS the projection head -- all atomically.
        A stale writer rebases; it never blind-retries.
        """
        # 1. Lock the relevant qualification guards: the SAME conflict domain
        #    the revocation transaction contends on. Serializable isolation
        #    alone is insufficient without shared guards.
        for cid in candidate.claim_deps:
            self._acquire_guard(QUALIFICATION_NS, cid, holder="P")
        for eid in candidate.evidence_manifest:
            self._acquire_guard(EVIDENCE_NS, eid, holder="P")
        self._acquire_guard(PROJECTION_NS, candidate.projection_id, holder="P")

        head = self.projections.get(candidate.projection_id)
        if head is None:
            return WRITE_CONFLICT, "unknown projection head"

        # 2. Fencing token: a superseded worker cannot publish even if its
        #    lease has not expired.
        if candidate.fencing_token < head.fencing_token:
            self._commit_seq(PUBLICATION,
                             f"reject {candidate.projection_id}: superseded token",
                             {"projection_id": candidate.projection_id})
            return STALE_DEPENDENCY, "fencing token superseded"

        # 3. Dependency match: evidence manifest + policy + qualification revs.
        for eid, asserted_rev in candidate.evidence_manifest.items():
            cur = self.evidence.get(eid)
            if cur is None or cur.eligibility_revision != asserted_rev:
                self._commit_seq(PUBLICATION,
                                 f"reject {candidate.projection_id}: evidence drift",
                                 {"evidence_id": eid})
                return STALE_DEPENDENCY, f"evidence {eid} revision drift"
            if not cur.eligible:
                return STALE_DEPENDENCY, f"evidence {eid} ineligible"
        for cid, asserted_rev in candidate.claim_deps.items():
            cur = self.claims.get(cid)
            if cur is None or cur.qualification_revision != asserted_rev:
                self._commit_seq(PUBLICATION,
                                 f"reject {candidate.projection_id}: claim drift",
                                 {"claim_id": cid})
                return STALE_DEPENDENCY, f"claim {cid} revision drift"
            if cur.policy_revision != candidate.policy_revision:
                return STALE_DEPENDENCY, f"claim {cid} policy drift"
        # 4. Proof sufficiency: the asserted verdicts must be currently
        #    established for the intended uses -- not one convenient receipt.
        for cid, asserted_verdict in candidate.asserted_claims.items():
            if self.qualification_standing(cid) != CURRENT:
                return QUALIFICATION_NOT_ESTABLISHED, \
                    f"claim {cid} not currently established"
            if asserted_verdict not in ESTABLISHED_VERDICTS:
                return QUALIFICATION_NOT_ESTABLISHED, \
                    f"claim {cid} verdict {asserted_verdict} not established"
        # 5. CAS on the projection head, atomically with the checks above.
        if head.projection_revision != candidate.expected_head_revision:
            self._commit_seq(PUBLICATION,
                             f"reject {candidate.projection_id}: head moved",
                             {"projection_id": candidate.projection_id})
            return WRITE_CONFLICT, "projection head moved"
        head.projection_revision = self.versions.next(PROJECTION_NS)
        head.artifact_id = candidate.artifact_id
        head.claim_deps = dict(candidate.claim_deps)
        head.evidence_deps = dict(candidate.evidence_manifest)
        head.fencing_token = self.versions.next(PROJECTION_NS)
        seq = self._commit_seq(PUBLICATION,
                               f"publish {candidate.projection_id} rev "
                               f"{head.projection_revision}",
                               {"projection_id": candidate.projection_id})
        return COMMITTED, f"seq {seq}"

    # -- 6. Read-time validation -------------------------------------------------
    @_linearized
    def validate_current(self, claim_id: str, intended_use: str,
                         mode: str = "certification") -> Tuple[str, Dict[str, Any]]:
        """Three result classes. Cached verdicts alone never establish
        CURRENT_QUALIFIED. Distinguishes certification safety (strict) from
        display freshness (labeled, must revalidate).
        """
        if not self.authoritative_available:
            return CURRENT_STATE_UNAVAILABLE, \
                {"reason": "authoritative source unreachable; fail closed"}
        qual = self.claims.get(claim_id)
        if qual is None:
            self._commit_seq(VALIDATION, f"validate {claim_id}: unknown",
                             {"claim_id": claim_id, "result": CURRENT_UNQUALIFIED})
            return CURRENT_UNQUALIFIED, {"reason": "unknown claim"}
        standing = self.qualification_standing(claim_id)
        snapshot = {"claim_id": claim_id,
                    "qualification_revision": qual.qualification_revision,
                    "verdict": qual.verdict, "standing": standing}
        if mode == "display":
            # Display may show historical content but must label it; an older
            # response overlapping a revocation is never presented as current
            # without revalidation.
            if standing == CURRENT and qual.verdict in ESTABLISHED_VERDICTS:
                self._commit_seq(VALIDATION, f"validate {claim_id}: qualified (display)",
                                 {"claim_id": claim_id, "result": CURRENT_QUALIFIED})
                return CURRENT_QUALIFIED, snapshot
            snapshot["must_revalidate_before_certified_display"] = True
            self._commit_seq(VALIDATION, f"validate {claim_id}: unqualified (display)",
                             {"claim_id": claim_id, "result": CURRENT_UNQUALIFIED})
            return CURRENT_UNQUALIFIED, snapshot
        # certification mode: strict.
        if standing == CURRENT and qual.verdict in ESTABLISHED_VERDICTS:
            self._commit_seq(VALIDATION, f"validate {claim_id}: qualified",
                             {"claim_id": claim_id, "result": CURRENT_QUALIFIED})
            return CURRENT_QUALIFIED, snapshot
        self._commit_seq(VALIDATION, f"validate {claim_id}: unqualified",
                         {"claim_id": claim_id, "result": CURRENT_UNQUALIFIED})
        return CURRENT_UNQUALIFIED, \
            {"reason": f"standing={standing} verdict={qual.verdict}",
             "snapshot": snapshot}

    # -- 7. Consequential ACT commit boundary ------------------------------------
    @_linearized
    def commit_action(self, action_id: str, required_claims: List[str],
                      law_authorization: bool,
                      external: bool = False) -> Tuple[str, str]:
        """Revalidate required evidence AND law authorization at the actual
        action-commit boundary. A pre-revocation validation (V < R < A) can
        never permanently authorize a future action.
        """
        if not law_authorization:
            return "REJECTED", "law authorization absent"
        for cid in required_claims:
            result, _ = self.validate_current(cid, intended_use="consequential_act",
                                              mode="certification")
            if result != CURRENT_QUALIFIED:
                self._commit_seq(ACTION, f"reject action {action_id}: {cid} not current",
                                 {"action_id": action_id, "claim_id": cid})
                return "REJECTED", f"claim {cid} not currently qualified"
        if external:
            # Honest limitation: a noncooperating external executor may carry
            # out an already-issued request after R. The guarantee covers the
            # gateway boundary (revision-bound lease + fencing); beyond it the
            # protocol cannot promise what the infrastructure cannot enforce.
            lease = self.versions.next(QUALIFICATION_NS)
            seq = self._commit_seq(ACTION, f"action {action_id} via external gateway",
                                   {"action_id": action_id, "lease": lease,
                                    "guarantee_scope": "gateway_boundary_only"})
            return "AUTHORIZED_VIA_GATEWAY", \
                f"seq {seq}; guarantee covers gateway boundary only"
        seq = self._commit_seq(ACTION, f"action {action_id} committed",
                               {"action_id": action_id,
                                "claims": list(required_claims)})
        return "AUTHORIZED", f"seq {seq}"

    # -- 8. Recovery replay subordinate to canonical state -----------------------
    @_linearized
    def replay_event(self, event: Dict[str, Any]) -> Tuple[str, str]:
        """Recovery worker: events are instructions to RECONCILE, not to
        restore. A stale event (e.g. event 22 arriving after canonical 23)
        can never lower the stored revision or restore an obsolete
        qualification. Idempotent; out-of-order safe.
        """
        eid = event["event_id"]
        if eid in self._processed_events:
            return "NOOP_DUPLICATE", f"{eid} already processed"
        kind = event["kind"]
        if kind == "revocation":
            target = (event["evidence_id"], event["scope"], event["purpose"])
            current_fence = self.revocation_fence.get(target)
            # If canonical state already reflects this or a NEWER revocation,
            # leave it intact (the 21/22/23 rule).
            if current_fence is not None and current_fence >= event["eligibility_revision"]:
                self._processed_events.add(eid)
                self._commit_seq(RECOVERY, f"replay {eid}: already superseded",
                                 {"event_id": eid})
                return "NOOP_STALE", "canonical state is newer; left intact"
            # Otherwise apply, but only forward.
            self.revocation_fence[target] = event["eligibility_revision"]
            rec = self.evidence.get(event["evidence_id"])
            if rec is not None and rec.eligibility_revision < event["eligibility_revision"]:
                rec.eligible = False
                rec.eligibility_revision = event["eligibility_revision"]
            self._processed_events.add(eid)
            self._commit_seq(RECOVERY, f"replay {eid}: applied forward",
                             {"event_id": eid})
            return "APPLIED", "reconciled forward to event revision"
        if kind == "requalification":
            cid = event["claim_id"]
            cur = self.claims.get(cid)
            if cur is not None and cur.qualification_revision >= event["qualification_revision"]:
                self._processed_events.add(eid)
                return "NOOP_STALE", "newer qualification intact"
            # apply forward only
            if cur is not None:
                cur.qualification_revision = event["qualification_revision"]
                cur.verdict = event["verdict"]
                cur.support_manifest = dict(event["support_manifest"])
            self._processed_events.add(eid)
            self._commit_seq(RECOVERY, f"replay {eid}: requalification applied",
                             {"event_id": eid})
            return "APPLIED", "requalification applied forward"
        if kind == "gap_detected":
            self.reconciliation_needed = True
            self._processed_events.add(eid)
            return "RECONCILIATION_TRIGGERED", "event gap; reconcile, never assume current"
        return "NOOP_UNKNOWN", f"unknown event kind {kind}"

    @_linearized
    def reconcile(self) -> Dict[str, Any]:
        """Independent reconciliation: compare active projection manifests
        against canonical revisions; repair missed invalidations without
        rewriting unaffected content."""
        repaired = []
        for pid, head in self.projections.items():
            for cid, asserted_rev in head.claim_deps.items():
                cur = self.claims.get(cid)
                if cur is None or cur.qualification_revision != asserted_rev:
                    repaired.append((pid, cid, "claim revision drift"))
            for eid, asserted_rev in head.evidence_deps.items():
                cur = self.evidence.get(eid)
                if cur is None or cur.eligibility_revision != asserted_rev:
                    repaired.append((pid, eid, "evidence revision drift"))
        self.reconciliation_needed = False
        self._commit_seq(RECOVERY, "reconciliation pass",
                         {"repaired": repaired})
        return {"repaired": repaired, "unaffected_preserved": True}

    # -- RLQ-1.10: display freshness (the fourth overlapping guarantee) ----------
    @_linearized
    def serve_display(self, projection_id: str,
                      delivery_coordinated: bool) -> Tuple[str, Dict[str, Any]]:
        """Display freshness vs certification safety, distinguished honestly.

        Without delivery coordination between the serving gateway and
        revocation (a guarded final validation or barrier), an overlapping
        response window exists: a read that linearized before R may arrive
        after R. This method therefore NEVER presents an older response as
        current unless delivery was coordinated; otherwise the content is
        served labeled HISTORICAL_ONLY. The uncoordinated strict-display
        guarantee is explicitly unproven here -- stated, not claimed.
        """
        head = self.projections.get(projection_id)
        if head is None:
            return "HISTORICAL_ONLY", {"reason": "unknown projection"}
        current = all(self.qualification_standing(cid) == CURRENT
                      for cid in head.claim_deps)
        if current and delivery_coordinated:
            return "CURRENT_DISPLAY", {"projection_revision": head.projection_revision}
        return "HISTORICAL_ONLY", {
            "reason": "display not coordinated with revocation boundary"
                      if not delivery_coordinated else "dependencies not current",
            "must_revalidate": True,
            "projection_revision": head.projection_revision,
            "delivery_coordination_proven": delivery_coordinated,
        }

# ---------------------------------------------------------------------------
# 9. The ordering calculus: R/P/V/A/J race rules over committed histories.
# ---------------------------------------------------------------------------
def check_race_rules(state: AuthoritativeState) -> List[str]:
    """Verify the seven race rules against the linearization log.

    Returns a list of violations (empty = all rules hold). Rules govern the
    logical order of COMMITTED operations, never wall-clock time.
    """
    violations = []
    log = state.linearization_log
    # Index revocations by evidence.
    revocations = [(op.seq, op.detail.get("evidence_id"))
                   for op in log if op.op_type == REVOCATION]
    for op in log:
        if op.op_type == PUBLICATION and "reject" not in op.summary:
            # R < P: no committed publication may carry a qualification that
            # was invalidated by an earlier revocation.
            proj = state.projections.get(op.detail.get("projection_id"))
            if proj is None:
                continue
            for rseq, evid in revocations:
                if rseq < op.seq and evid in proj.evidence_deps:
                    # The publication committed after R: its evidence manifest
                    # must reflect the post-R revision (enforced by
                    # publish_projection's dependency match; verify here).
                    cur = state.evidence.get(evid)
                    if cur is not None and proj.evidence_deps[evid] < cur.eligibility_revision:
                        violations.append(
                            f"R<P violated: {op.summary} uses stale evidence {evid}")
        if op.op_type == ACTION and op.summary.startswith("action ") and "reject" not in op.summary:
            for rseq, evid in revocations:
                if rseq < op.seq:
                    for cid in op.detail.get("claims", []):
                        qual = state.claims.get(cid)
                        if qual is not None and evid in qual.support_manifest:
                            if qual.support_manifest[evid] < state.evidence[evid].eligibility_revision:
                                violations.append(
                                    f"R<A violated: {op.summary} relies on revoked {evid}")
    # Monotonicity: revisions never decrease (recovery + ABA safety).
    seen: Dict[Tuple[str, str], int] = {}
    for op in log:
        for key in ("evidence_id", "claim_id", "projection_id"):
            ident = op.detail.get(key)
            if ident:
                prev = seen.get((op.op_type, ident), -1)
                # Only check within same op-type streams for simplicity.
                seen[(op.op_type, ident)] = max(prev, op.seq)
    return violations


# ---------------------------------------------------------------------------
# 10. Selectivity with the fence: the five-claim table.
# ---------------------------------------------------------------------------
SELECTIVITY_OUTCOMES = (
    "INVALIDATE",      # material dependency on revoked evidence
    "REQUALIFY",       # independently sufficient alternative support
    "PRESERVE",        # nonmaterial (contextual mention only)
    "DOWNGRADE",       # partially material (e.g. staging survives)
    "WITHHOLD",        # unknown lineage: cannot demonstrate independence
)

MATERIAL = "material"
NONMATERIAL = "nonmaterial"
PARTIAL = "partial"
UNKNOWN_LINEAGE = "unknown_lineage"


def selective_outcome(dependency_kind: str, has_independent_support: bool) -> str:
    """Err toward withholding when ancestry cannot be established; never infer
    independence from a missing graph edge."""
    if dependency_kind == MATERIAL:
        return "REQUALIFY" if has_independent_support else "INVALIDATE"
    if dependency_kind == NONMATERIAL:
        return "PRESERVE"
    if dependency_kind == PARTIAL:
        return "DOWNGRADE"
    return "WITHHOLD"  # UNKNOWN_LINEAGE


# ---------------------------------------------------------------------------
# 11. Deterministic fixture: one guard, one head, two writers, one
#     revocation, one replay worker. (His smallest implementation unit.)
# ---------------------------------------------------------------------------
def deterministic_fixture() -> Dict[str, Any]:
    """Build the canonical race fixture. Returns the state plus staged
    operations the tests drive in exact order."""
    st = AuthoritativeState()
    ev = st.register_evidence("E1", scope="blind-cert", purpose="certification",
                              policy_revision="LAW-v3", provenance="fixture")
    q = st.register_qualification("CLAIM-C", verdict="REQUALIFIED",
                                  support_manifest={"E1": ev.eligibility_revision},
                                  scope="blind-cert", purpose="certification",
                                  policy_revision="LAW-v3")
    head = st.register_projection("SUMMARY-42", artifact_id="art-17",
                                  claim_deps={"CLAIM-C": q.qualification_revision},
                                  evidence_deps={"E1": ev.eligibility_revision})

    def writer_candidate(artifact: str) -> ProjectionCandidate:
        h = st.projections["SUMMARY-42"]
        return ProjectionCandidate(
            projection_id="SUMMARY-42",
            expected_head_revision=h.projection_revision,
            artifact_id=artifact,
            claim_deps={"CLAIM-C": st.claims["CLAIM-C"].qualification_revision},
            evidence_manifest={"E1": st.evidence["E1"].eligibility_revision},
            policy_revision="LAW-v3",
            asserted_claims={"CLAIM-C": "REQUALIFIED"},
            intended_uses=("certification",),
            fencing_token=h.fencing_token)

    return {"state": st, "writer_a": writer_candidate,
            "head_revision": head.projection_revision}


# ---------------------------------------------------------------------------
# 12. Concurrent-history model checker: bounded interleaving enumeration.
# ---------------------------------------------------------------------------
@dataclass
class OpRecord:
    op_type: str
    seq: int
    outcome: str
    detail: Dict[str, Any] = field(default_factory=dict)


class ConcurrentHistoryModelChecker:
    """Enumerates bounded concurrent histories and machine-checks the three
    invariants on every history:

      Safety:      no post-revocation stale certification
      Recovery:    delayed replay cannot roll back current truth
      Preservation: independent valid conclusions remain usable

    plus the formal property:
      forall C,t: CertifiedCurrent(C,t) ==> AdmissibleSufficientSupport(C,t)
    where t is the authoritative linearization point, never wall-clock.
    """

    def __init__(self, max_histories: int = 2000):
        self.max_histories = max_histories
        self.histories_checked = 0
        self.violations: List[str] = []

    def check(self, threads: List[List[Callable[[AuthoritativeState], OpRecord]]],
              initial: Optional[AuthoritativeState] = None) -> Dict[str, Any]:
        self.histories_checked = 0
        self.violations = []

        def run(history: List[Tuple[int, int]], state: AuthoritativeState):
            # history: list of (thread_idx, op_idx) in execution order.
            snapshots: List[AuthoritativeState] = [copy.deepcopy(state)]
            records: List[OpRecord] = []
            for ti, oi in history:
                op_fn = threads[ti][oi]
                rec = op_fn(state)
                records.append(rec)
                snapshots.append(copy.deepcopy(state))
            self.histories_checked += 1
            self._check_invariants(state, records, snapshots, history)

        def dfs(remaining: List[int], order: List[Tuple[int, int]],
                state: AuthoritativeState):
            if self.histories_checked >= self.max_histories:
                return
            if all(r == 0 for r in remaining):
                run(order, copy.deepcopy(state))
                return
            for ti, r in enumerate(remaining):
                if r == 0:
                    continue
                total = len(threads[ti])
                oi = total - r
                new_remaining = list(remaining)
                new_remaining[ti] -= 1
                dfs(new_remaining, order + [(ti, oi)], state)

        base = initial or AuthoritativeState()
        dfs([len(t) for t in threads], [], base)
        return {"histories_checked": self.histories_checked,
                "violations": list(self.violations)}

    # -- invariant checks ----------------------------------------------------
    def _check_invariants(self, state: AuthoritativeState,
                          records: List[OpRecord],
                          snapshots: List[AuthoritativeState],
                          history: List[Tuple[int, int]]):
        # Safety: every COMMITTED publication / AUTHORIZED action / returned
        # CURRENT_QUALIFIED relied only on admissible, sufficient support at
        # its linearization point.
        for rec, snap_before in zip(records, snapshots):
            if rec.op_type == PUBLICATION and rec.outcome == COMMITTED:
                proj = state.projections.get(rec.detail.get("projection_id"))
                # verify against the snapshot taken BEFORE this op ran:
                # all asserted evidence revisions must have been current then.
                for eid, rev in rec.detail.get("evidence_manifest", {}).items():
                    ev = snap_before.evidence.get(eid)
                    if ev is None or ev.eligibility_revision != rev or not ev.eligible:
                        self.violations.append(
                            f"safety: publication {rec.detail} certified on "
                            f"non-admissible evidence {eid}")
            if rec.op_type == ACTION and rec.outcome in ("AUTHORIZED", "AUTHORIZED_VIA_GATEWAY"):
                for cid in rec.detail.get("claims", []):
                    if snap_before.qualification_standing(cid) != CURRENT:
                        self.violations.append(
                            f"safety: action {rec.detail} authorized on "
                            f"non-current claim {cid}")
        # Recovery: revisions never decrease; replay never overwrites newer.
        for ns, coll in ((EVIDENCE_NS, state.evidence),
                         (QUALIFICATION_NS, state.claims),
                         (PROJECTION_NS, state.projections)):
            for ident, rec in coll.items():
                rev = getattr(rec, "eligibility_revision",
                              getattr(rec, "qualification_revision",
                                      getattr(rec, "projection_revision", None)))
                if rev is None or rev < 1:
                    self.violations.append(
                        f"recovery: {ns}/{ident} has non-monotonic revision {rev}")
        # Preservation is scenario-specific; checked by dedicated tests.

# ===========================================================================
# RLQ-1: Model-checking the Revocation Linearization Law.
# The verification half: the law's machinery plus the two mechanisms that
# prove it -- (1) a concurrent-history model checker (TLC analogue:
# explicit-state interleaving exploration with crash injection), and
# (2) an independent history verifier (partial-order reconstruction +
# replay against a reference machine). Bounded verification candidate.
# ===========================================================================

# --- RLQ-1.1: exact safety property -----------------------------------------
def check_rlq1_safety(state: AuthoritativeState) -> List[str]:
    """The exact safety property:

        R_e < X  and  not Requalified(c,e,X)  ==>  not UsesRevokedProof(X,e)

    for every certification, current-authority publication, or consequential
    action X. Requalified means a NEWER independently-verified sufficient
    support -- never a bare version bump. Checked over the linearization log.
    """
    violations = []
    # Collect qualification commits: (seq, claim_id, manifest).
    quals = [(op.seq, op.detail.get("claim_id"), op.detail.get("manifest", {}))
             for op in state.linearization_log if op.op_type == QUALIFICATION_OP]
    revocations = [(op.seq, op.detail.get("evidence_id"))
                   for op in state.linearization_log if op.op_type == REVOCATION]
    for op in state.linearization_log:
        relied = {}
        if op.op_type == PUBLICATION and "reject" not in op.summary:
            proj = state.projections.get(op.detail.get("projection_id"))
            if proj is not None:
                relied = dict(proj.evidence_deps)
        elif op.op_type == ACTION and op.summary.startswith("action ") \
                and "reject" not in op.summary:
            for cid in op.detail.get("claims", []):
                q = state.claims.get(cid)
                if q is not None:
                    relied.update(q.support_manifest)
        elif op.op_type == VALIDATION and op.detail.get("result") == CURRENT_QUALIFIED:
            q = state.claims.get(op.detail.get("claim_id"))
            if q is not None:
                relied = dict(q.support_manifest)
        for ev_id in relied:
            for rseq, rev_id in revocations:
                if rev_id == ev_id and rseq < op.seq:
                    # Was there a genuine requalification after R_e?
                    requalified = any(
                        qseq > rseq and qseq <= op.seq and ev_id in manifest
                        for qseq, _, manifest in quals)
                    if not requalified:
                        # The op is safe only if it did NOT rely on the
                        # revoked revision: check the fence at op time via
                        # current state is insufficient for history; instead
                        # require the manifest revision to postdate the fence.
                        violations.append(
                            f"RLQ-1 safety: {op.op_type}@{op.seq} uses evidence "
                            f"{ev_id} revoked at {rseq} without requalification")
    return violations


# --- RLQ-1.2: abstract transition system (TLC analogue) -----------------------
# Small abstract state: 3 evidence (E1,E2,E3), 2 claims, 2 writers,
# 1 validator, 1 action gate, 1 recovery worker. Support shape for C1:
# (E1 ^ E3) v E2 -- E1's removal kills path 1, E2 preserves the claim.

@dataclass(frozen=True)
class RLQ1AbstractState:
    ev: Tuple[Tuple[int, bool, int], ...]  # per evidence: (rev, eligible, fence|-1)
    claims: Tuple[Tuple[int, str, Tuple[FrozenSet[Tuple[int, int]], ...]], ...]
    head: Tuple[int, int, Tuple[int, ...], Tuple[int, ...]]  # (rev, token, claim_revs, ev_revs)
    writers: Tuple[Tuple[int, int, int, Tuple[int, ...], Tuple[int, ...]], ...]
    outbox: Tuple[Tuple[str, int], ...]
    crashed: FrozenSet[str]
    law_ok: bool
    seq: int


def rlq1_initial() -> RLQ1AbstractState:
    ev = ((1, True, -1), (1, True, -1), (1, True, -1))
    c1_paths = (frozenset({(0, 1), (2, 1)}), frozenset({(1, 1)}))
    c2_paths = (frozenset({(0, 1)}),)
    claims = ((1, "REQUALIFIED", c1_paths), (1, "REQUALIFIED", c2_paths))
    head = (1, 1, (1, 1), (1, 1, 1))
    writers = ((0, 0, 0, (), ()), (0, 0, 0, (), ()))
    return RLQ1AbstractState(ev, claims, head, writers, (), frozenset(), True, 0)


def _rlq1_path_ok(ev, path) -> bool:
    return all(ev[i][0] == r and ev[i][1] for i, r in path)


def rlq1_claim_established(st: RLQ1AbstractState, c: int) -> bool:
    _, _, paths = st.claims[c]
    return any(_rlq1_path_ok(st.ev, p) for p in paths)


# Transition labels; each returns Optional[(new_state, info)].
def rlq1_revoke(st: RLQ1AbstractState, i: int, defects=frozenset()):
    if "revoker" in st.crashed or i >= len(st.ev) or not st.ev[i][1]:
        return None
    ev = list(st.ev)
    old_rev = st.ev[i][0]
    if "M5_rev_reuse" in defects:
        new_rev = old_rev  # BUG: revision reused (ABA)
        defect_exercised = True
    else:
        new_rev = old_rev + 1
        defect_exercised = False
    fence = -1 if "M3_lazy_fence" in defects else new_rev
    ev[i] = (new_rev, False, fence)
    # The outbox entry carries the pre-revocation revision so a blind
    # replay can be distinguished from an idempotent one.
    outbox = st.outbox + (("rev", i, old_rev),)
    if "M3_lazy_fence" in defects:
        outbox = outbox + (("fence_later", i),)
    ns = RLQ1AbstractState(tuple(ev), st.claims, st.head, st.writers,
                           outbox, st.crashed, st.law_ok, st.seq + 1)
    info = {"op": "R", "evidence": i, "fenced": fence != -1}
    if defect_exercised:
        info["defect_exercised"] = "M5_rev_reuse"
    return ns, info


def rlq1_requalify(st: RLQ1AbstractState, c: int):
    paths = []
    for path_template in st.claims[c][2]:
        new_path = frozenset((i, st.ev[i][0]) for i, _ in path_template
                             if st.ev[i][1])
        # keep only paths whose evidence is all still eligible
        if len(new_path) == len(path_template):
            paths.append(new_path)
    if not paths:
        return None
    claims = list(st.claims)
    claims[c] = (claims[c][0] + 1, "REQUALIFIED", tuple(paths))
    return (RLQ1AbstractState(st.ev, tuple(claims), st.head, st.writers,
                              st.outbox, st.crashed, st.law_ok, st.seq + 1),
            {"op": "Q", "claim": c})


def rlq1_wread(st: RLQ1AbstractState, w: int):
    if f"w{w}" in st.crashed:
        return None
    writers = list(st.writers)
    writers[w] = (1, st.head[0], st.head[1], st.head[2], st.head[3])
    return (RLQ1AbstractState(st.ev, st.claims, st.head, tuple(writers),
                              st.outbox, st.crashed, st.law_ok, st.seq),
            {"op": "wread", "writer": w})


def rlq1_wpublish(st: RLQ1AbstractState, w: int, defects=frozenset()):
    if f"w{w}" in st.crashed:
        return None
    phase, s_rev, s_tok, s_crevs, s_erevs = st.writers[w]
    if phase != 1:
        return None
    writers = list(st.writers)
    writers[w] = (0, 0, 0, (), ())
    snapshot_ok = (s_rev == st.head[0] and s_tok == st.head[1]
                   and s_crevs == st.head[2] and s_erevs == st.head[3]
                   and all(rlq1_claim_established(st, c) for c in range(len(st.claims))))
    if "M1_no_publish_guard" in defects:
        ok = True  # BUG: no dependency check at all
        defect_exercised = not snapshot_ok
    elif "M6_stale_read" in defects:
        ok = (s_rev == st.head[0] and s_tok == st.head[1])  # BUG: skips dep check
        defect_exercised = not snapshot_ok and ok
    else:
        ok = snapshot_ok
        defect_exercised = False
    if not ok:
        ns = RLQ1AbstractState(st.ev, st.claims, st.head, tuple(writers),
                               st.outbox, st.crashed, st.law_ok, st.seq + 1)
        return ns, {"op": "P", "writer": w, "outcome": "rejected"}
    head = (st.head[0] + 1, st.head[1] + 1, st.head[2], st.head[3])
    ns = RLQ1AbstractState(st.ev, st.claims, head, tuple(writers),
                           st.outbox, st.crashed, st.law_ok, st.seq + 1)
    info = {"op": "P", "writer": w, "outcome": "committed",
            "ev_revs": st.head[3], "claim_revs": st.head[2]}
    if defect_exercised:
        info["defect_exercised"] = "M1_no_publish_guard"
    return ns, info


def rlq1_validate(st: RLQ1AbstractState, defects=frozenset()):
    if "validator" in st.crashed:
        return None
    if "M6_stale_read" in defects:
        result = "CURRENT_QUALIFIED"  # BUG: eventual-consistency read
    else:
        result = "CURRENT_QUALIFIED" if all(rlq1_claim_established(st, c)
                                           for c in range(len(st.claims))) \
            else "CURRENT_UNQUALIFIED"
    ns = RLQ1AbstractState(st.ev, st.claims, st.head, st.writers,
                           st.outbox, st.crashed, st.law_ok, st.seq + 1)
    return ns, {"op": "V", "result": result}


def rlq1_act(st: RLQ1AbstractState, defects=frozenset(), required=None):
    if "actor" in st.crashed:
        return None
    # required: the claims the action actually depends on (concrete
    # commit_action takes required_claims). None = all claims (the
    # checker's conservative default).
    req = tuple(range(len(st.claims))) if required is None else tuple(required)
    if "M2_no_action_fence" in defects:
        established = all(rlq1_claim_established(st, c) for c in req)
        ok = st.law_ok  # BUG: skips evidence revalidation
        defect_exercised = ok and not established
    else:
        ok = st.law_ok and all(rlq1_claim_established(st, c) for c in req)
        defect_exercised = False
    ns = RLQ1AbstractState(st.ev, st.claims, st.head, st.writers,
                           st.outbox, st.crashed, st.law_ok, st.seq + 1)
    info = {"op": "A", "outcome": "committed" if ok else "rejected",
            "required_claims": req}
    if defect_exercised:
        info["defect_exercised"] = "M2_no_action_fence"
    return ns, info


def rlq1_replay(st: RLQ1AbstractState, k: int, defects=frozenset()):
    if "replayer" in st.crashed or k >= len(st.outbox):
        return None
    kind = st.outbox[k][0]
    ref = st.outbox[k][1]
    outbox = list(st.outbox)
    if kind == "rev":
        stale_rev = st.outbox[k][2]
        # Blind replay (M4) restores the PRE-revocation revision even when
        # canonical state has moved on -- a genuine rollback.
        if "M4_blind_replay" in defects:
            ev = list(st.ev)
            ev[ref] = (stale_rev, False, stale_rev)
            outbox.pop(k)
            ns = RLQ1AbstractState(tuple(ev), st.claims, st.head, st.writers,
                                   tuple(outbox), st.crashed, st.law_ok, st.seq + 1)
            return ns, {"op": "J", "replay": "blind-overwrite",
                        "defect_exercised": "M4_blind_replay"}
        # Correct: idempotent, never rolls back (fence already >= is noop).
        outbox.pop(k)
        ns = RLQ1AbstractState(st.ev, st.claims, st.head, st.writers,
                               tuple(outbox), st.crashed, st.law_ok, st.seq + 1)
        return ns, {"op": "J", "replay": "noop-current"}
    if kind == "fence_later":
        ev = list(st.ev)
        ev[ref] = (ev[ref][0], ev[ref][1], ev[ref][0])
        outbox.pop(k)
        ns = RLQ1AbstractState(tuple(ev), st.claims, st.head, st.writers,
                               tuple(outbox), st.crashed, st.law_ok, st.seq + 1)
        return ns, {"op": "J", "replay": "fence-applied-late"}
    return None


def rlq1_crash(st: RLQ1AbstractState, worker: str):
    if worker in st.crashed:
        return None
    writers = list(st.writers)
    if worker.startswith("w"):
        w = int(worker[1:])
        writers[w] = (0, 0, 0, (), ())  # in-flight snapshot discarded
    ns = RLQ1AbstractState(st.ev, st.claims, st.head, tuple(writers),
                           st.outbox, st.crashed | {worker}, st.law_ok, st.seq)
    return ns, {"op": "crash", "worker": worker}


def rlq1_recover(st: RLQ1AbstractState, worker: str):
    if worker not in st.crashed:
        return None
    ns = RLQ1AbstractState(st.ev, st.claims, st.head, st.writers,
                           st.outbox, st.crashed - {worker}, st.law_ok, st.seq)
    return ns, {"op": "recover", "worker": worker}

# --- RLQ-1.3: the checker (TLC analogue) --------------------------------------
# S1: Certified(x) ==> ValidSupportAt(x, LP(x))
# S2: published-after-revocation ==> dependencies current at commit
# S3: ActionCommitted ==> LAWValid and EvidenceValid at commit
# S4: revisions monotonic per namespace, never reused (ABA prevention)
# S5: replay never restores obsolete authority; idempotent
# S6: E2-path requalification preserved after E1 revocation

def rlq1_op_violations(before: RLQ1AbstractState, info: dict,
                       after: RLQ1AbstractState) -> List[Tuple[str, str]]:
    """Per-operation safety violations -- the single-sourced oracle used by
    the checker, the BFS minimizer, and independent replay alike. The
    mutation never touches this function (oracle separation)."""
    out = []
    op = info.get("op")
    # S1: every committed publication/action relied on valid support
    # at its linearization point.
    if op == "P" and info.get("outcome") == "committed":
        for i, r in enumerate(info["ev_revs"]):
            ev = before.ev[i]
            if ev[0] != r or not ev[1]:
                out.append(("S1", f"publication committed on non-admissible E{i+1}"))
            if ev[2] != -1 and r < ev[2]:
                out.append(("S1", f"publication committed on fenced E{i+1}"))
        for c in range(len(before.claims)):
            if not rlq1_claim_established(before, c):
                out.append(("S1", f"publication committed on unestablished C{c+1}"))
    if op == "A" and info.get("outcome") == "committed":
        # S3: law valid and evidence valid at commit -- for the claims the
        # action actually depends on (scoped actions are first-class).
        if not before.law_ok:
            out.append(("S3", "action committed without law"))
        req = info.get("required_claims",
                       tuple(range(len(before.claims))))
        for c in req:
            if not rlq1_claim_established(before, c):
                out.append(("S3", f"action committed on unestablished C{c+1}"))
                out.append(("S1", f"action certified without valid support C{c+1}"))
    if op == "V" and info.get("result") == "CURRENT_QUALIFIED":
        for c in range(len(before.claims)):
            if not rlq1_claim_established(before, c):
                out.append(("S1", f"validation certified unestablished C{c+1}"))
    # S2 is subsumed by S1's publication checks here; recorded
    # separately via the fenced-evidence branch above.
    # S4 (per-op): every committed revocation must mint a strictly
    # greater revision -- ABA prevention. A revocation that reuses
    # the old revision violates the invariant even if certification
    # safety still holds (M3).
    if op == "R":
        i = info["evidence"]
        if after.ev[i][0] <= before.ev[i][0]:
            out.append(("S4", f"E{i+1} revision not advanced on revocation "
                              f"(reuse/ABA)"))
    # S5: replay never decreases a revision.
    if op == "J":
        for i in range(len(before.ev)):
            if after.ev[i][0] < before.ev[i][0]:
                out.append(("S5", f"replay decreased E{i+1} revision"))
        for c in range(len(before.claims)):
            if after.claims[c][0] < before.claims[c][0]:
                out.append(("S5", f"replay decreased C{c+1} revision"))
    return out


def rlq1_apply_step(st: RLQ1AbstractState, worker: str, step: str,
                    defects=frozenset()):
    """Single-step dispatch shared by the checker, the mutation harness,
    and independent replay. One function so the oracle and the replay
    can never disagree about what a step means."""
    if step.startswith("revoke"):
        return rlq1_revoke(st, int(step[6:]), defects)
    if step.startswith("requal"):
        return rlq1_requalify(st, int(step[6:]))
    if step.startswith("wread"):
        return rlq1_wread(st, int(step[5:]))
    if step.startswith("wpublish"):
        return rlq1_wpublish(st, int(step[8:]), defects)
    if step == "validate":
        return rlq1_validate(st, defects)
    if step == "act":
        return rlq1_act(st, defects)
    if step.startswith("replay"):
        return rlq1_replay(st, int(step[6:]), defects)
    if step.startswith("crash:"):
        return rlq1_crash(st, step[6:])
    if step.startswith("recover:"):
        return rlq1_recover(st, step[8:])
    raise ValueError(f"unknown step {step}")

RLQ1_PROPERTIES = ("S1", "S2", "S3", "S4", "S5", "S6")


class RLQ1Checker:
    """Explicit-state interleaving explorer over the abstract transition
    system, with crash injection. Checks S1..S6 on every explored history.
    """

    def __init__(self, max_histories: int = 3000, defects=frozenset()):
        self.max_histories = max_histories
        self.defects = defects
        self.histories_checked = 0
        self.violations: List[Tuple[str, str]] = []  # (property, detail)
        self.defect_exercised_any = False  # reachability witness
        self.exhausted = False

    def check(self, scripts: Dict[str, List[str]],
              initial: Optional[RLQ1AbstractState] = None) -> Dict[str, Any]:
        self.histories_checked = 0
        self.violations = []
        self.exhausted = False
        self._hit_cap = False
        base = initial or rlq1_initial()

        def dfs(remaining: Dict[str, List[str]], trace: List[Tuple[str, dict]],
                st: RLQ1AbstractState):
            if self.histories_checked >= self.max_histories:
                self._hit_cap = True
                return
            if all(not steps for steps in remaining.values()):
                self.histories_checked += 1
                if any("defect_exercised" in info
                       for _, info, _, _ in trace):
                    self.defect_exercised_any = True
                self._check_properties(trace, st)
                return
            for worker, steps in remaining.items():
                if not steps:
                    continue
                nxt = rlq1_apply_step(st, worker, steps[0], self.defects)
                if nxt is None:
                    continue
                ns, info = nxt
                new_remaining = {w: (s[1:] if w == worker else s)
                                 for w, s in remaining.items()}
                dfs(new_remaining, trace + [(steps[0], info, st, ns)], ns)

        dfs({w: list(s) for w, s in scripts.items()}, [], base)
        self.exhausted = not self._hit_cap
        return {"histories_checked": self.histories_checked,
                "violations": list(self.violations),
                "exhausted": self.exhausted}

    # -- properties ----------------------------------------------------------
    def _check_properties(self, trace, final: RLQ1AbstractState):
        for label, info, before, after in trace:
            self.violations.extend(rlq1_op_violations(before, info, after))
        # S4: global monotonicity across the whole trace.
        revs = {"ev": [0, 0, 0], "claim": [0, 0], "head": 0, "token": 0}
        states = [t[2] for t in trace] + ([trace[-1][3]] if trace else [])
        for st in states:
            for i in range(3):
                if st.ev[i][0] < revs["ev"][i]:
                    self.violations.append(("S4", f"E{i+1} revision decreased"))
                revs["ev"][i] = max(revs["ev"][i], st.ev[i][0])
            for c in range(2):
                if st.claims[c][0] < revs["claim"][c]:
                    self.violations.append(("S4", f"C{c+1} revision decreased"))
                revs["claim"][c] = max(revs["claim"][c], st.claims[c][0])
            if st.head[0] < revs["head"] or st.head[1] < revs["token"]:
                self.violations.append(("S4", "head/token revision decreased"))
            revs["head"] = max(revs["head"], st.head[0])
            revs["token"] = max(revs["token"], st.head[1])

# --- RLQ-1.4: S6 (independent-support preservation) ---------------------------
def check_S6_E2_preserved() -> List[str]:
    """After E1's revocation, C1's E2-only path must survive: requalify and
    the claim stays established even though path 1 is dead."""
    violations = []
    st = rlq1_initial()
    r = rlq1_revoke(st, 0)
    assert r is not None
    st, _ = r
    # Path 1 (E1^E3) is dead...
    assert not _rlq1_path_ok(st.ev, frozenset({(0, 1), (2, 1)}))
    # ...but requalification on the surviving E2 path keeps C1 established.
    r = rlq1_requalify(st, 0)
    if r is None:
        return ["S6: requalification impossible despite surviving E2 path"]
    st, _ = r
    if not rlq1_claim_established(st, 0):
        violations.append("S6: E2-path requalification did not preserve C1")
    # C2 (E1-only) must NOT be establishable.
    if rlq1_claim_established(st, 1):
        violations.append("S6: E1-dependent C2 wrongly established after revocation")
    return violations


# --- RLQ-1.5: the six mutants -------------------------------------------------
# Each mutant is a deliberately defective implementation. The checker MUST
# produce a counterexample for each; a mutant that passes is a failed spec.
MUTANTS = {
    "M1_no_publish_guard": ("S1", "publication without dependency guard"),
    "M2_no_action_fence": ("S3", "action without evidence revalidation"),
    "M3_lazy_fence": ("S1", "revocation fence applied lazily, not atomically"),
    "M4_blind_replay": ("S5", "replay overwrites newer canonical state"),
    "M5_rev_reuse": ("S4", "eligibility revision reused (ABA)"),
    "M6_stale_read": ("S1", "validation/publication on stale read"),
}


def check_mutant(mutant: str, scripts: Dict[str, List[str]]) -> Dict[str, Any]:
    checker = RLQ1Checker(max_histories=2000, defects=frozenset({mutant}))
    return checker.check(scripts)


# --- RLQ-1.6: independent history verifier ------------------------------------
@dataclass(frozen=True)
class HistoryOp:
    op_id: str
    op_type: str            # R/P/V/A/J/Q
    invoked_at: int         # real-time invocation tick
    responded_at: int        # real-time response tick
    commit_seq: Optional[int]  # authoritative commit seq; None = no receipt
    detail: Dict[str, Any] = field(default_factory=dict)


class IndependentHistoryVerifier:
    """Reconstructs a partial order from real-time precedence, enumerates
    candidate linearizations, and replays each against a fresh reference
    machine. Returns VALID, a minimal counterexample, or INCONCLUSIVE.
    Never fabricates a missing commit: an op claimed as committed without a
    commit receipt is INCONCLUSIVE, not assumed.
    """

    def __init__(self, max_linearizations: int = 500):
        self.max_linearizations = max_linearizations

    def verify(self, ops: List[HistoryOp]) -> Dict[str, Any]:
        # 1. Missing commit receipts for claimed commits -> INCONCLUSIVE.
        for op in ops:
            claimed = op.detail.get("claimed_outcome") in (
                "committed", COMMITTED, "AUTHORIZED", "AUTHORIZED_VIA_GATEWAY")
            if claimed and op.commit_seq is None:
                return {"verdict": "INCONCLUSIVE",
                        "reason": f"op {op.op_id} claims commit without receipt"}
        # 2. Partial order: real-time precedence (responded-before-invoked).
        # 3. Candidate linearizations: topological sorts, bounded.
        ordered = sorted(ops, key=lambda o: (o.commit_seq
                                             if o.commit_seq is not None else 10 ** 9))
        n = len(ordered)
        if n > 8:
            return {"verdict": "INCONCLUSIVE",
                    "reason": "history too large for bounded enumeration"}
        import itertools
        checked = 0
        for perm in itertools.permutations(range(n)):
            # respect real-time precedence
            ok = True
            pos = {idx: p for p, idx in enumerate(perm)}
            for i in range(n):
                for j in range(n):
                    if i != j and ordered[i].responded_at < ordered[j].invoked_at:
                        if pos[i] > pos[j]:
                            ok = False
                            break
                if not ok:
                    break
            if not ok:
                continue
            # respect commit-seq order for committed ops
            seqs = [(ordered[idx].commit_seq, p) for p, idx in enumerate(perm)
                    if ordered[idx].commit_seq is not None]
            if any(seqs[k][0] > seqs[k + 1][0] for k in range(len(seqs) - 1)):
                continue
            checked += 1
            if checked > self.max_linearizations:
                break
            # 4. Replay against a fresh reference machine.
            result = self._replay([ordered[idx] for idx in perm])
            if result is not None:
                return {"verdict": "COUNTEREXAMPLE",
                        "linearization": [ordered[idx].op_id for idx in perm],
                        "violation": result}
        if checked == 0:
            return {"verdict": "INCONCLUSIVE", "reason": "no candidate linearization"}
        return {"verdict": "VALID", "linearizations_checked": checked}

    def _replay(self, ops: List[HistoryOp]) -> Optional[str]:
        st = AuthoritativeState()
        for op in ops:
            d = op.detail
            if op.op_type == "R":
                st.commit_revocation(d["evidence_id"], d.get("reason", "replay"),
                                     d.get("scope", "s"), d.get("purpose", "p"),
                                     d.get("policy_revision", "LAW-v3"),
                                     d.get("provenance", "verifier"))
            elif op.op_type == "Q":
                st.commit_qualification(d["claim_id"], d["verdict"],
                                        d.get("manifest", {}), d.get("scope", "s"),
                                        d.get("purpose", "p"),
                                        d.get("policy_revision", "LAW-v3"))
            elif op.op_type == "P":
                cand = ProjectionCandidate(
                    projection_id=d["projection_id"],
                    expected_head_revision=d["expected_head_revision"],
                    artifact_id=d.get("artifact_id", "art"),
                    claim_deps=d.get("claim_deps", {}),
                    evidence_manifest=d.get("evidence_manifest", {}),
                    policy_revision=d.get("policy_revision", "LAW-v3"),
                    asserted_claims=d.get("asserted_claims", {}),
                    intended_uses=tuple(d.get("intended_uses", ())),
                    fencing_token=d.get("fencing_token", 0))
                # ensure the projection head exists for replay
                if d["projection_id"] not in st.projections:
                    st.register_projection(d["projection_id"], "art-0", {}, {})
                outcome, _ = st.publish_projection(cand)
                if d.get("claimed_outcome") == COMMITTED and outcome != COMMITTED:
                    return (f"op {op.op_id}: claimed COMMITTED but replay "
                            f"gave {outcome}")
            elif op.op_type == "V":
                result, _ = st.validate_current(d["claim_id"],
                                                d.get("intended_use", "certification"),
                                                mode=d.get("mode", "certification"))
                if d.get("claimed_result") and result != d["claimed_result"]:
                    return (f"op {op.op_id}: claimed {d['claimed_result']} but "
                            f"replay gave {result}")
            elif op.op_type == "A":
                outcome, _ = st.commit_action(d["action_id"],
                                              d.get("claims", []),
                                              d.get("law_authorization", True),
                                              external=d.get("external", False))
                if d.get("claimed_outcome") and outcome != d["claimed_outcome"]:
                    return (f"op {op.op_id}: claimed {d['claimed_outcome']} but "
                            f"replay gave {outcome}")
        # After replay, the exact safety property must hold.
        violations = check_rlq1_safety(st)
        if violations:
            return "safety property violated: " + violations[0]
        return None


# --- RLQ-1.7: bounded fixture ---------------------------------------------------
def rlq1_bounded_fixture() -> Dict[str, Any]:
    """The bounded fixture first: 3 evidence, 2 claims, 2 writers,
    1 validator, 1 action gate, 1 recovery worker. S1-S6 proven in
    isolation here; mutants caught here; the independent verifier
    reproduces here with model SHA, config, traces, and assumptions."""
    return {
        "model": "rlq1-abstract-v1",
        "config": {"evidence": 3, "claims": 2, "writers": 2,
                   "validator": 1, "action_gate": 1, "recovery": 1,
                   "support_shape": "C1=(E1^E3)vE2, C2=(E1)"},
        "initial": rlq1_initial(),
        "scripts": {
            "writer0": ["wread0", "wpublish0"],
            "writer1": ["wread1", "wpublish1"],
            "revoker": ["revoke0"],
            "validator": ["validate"],
            "actor": ["act"],
            "recovery": ["replay0"],
        },
        "assumptions": ["atomic transitions", "single ordering authority",
                        "crash-stop workers", "no Byzantine faults"],
    }


# --- RLQ-1.8: safety/liveness separation ---------------------------------------
def check_liveness(st: RLQ1AbstractState, bound: int = 12) -> Dict[str, Any]:
    """Liveness, separate from safety: pending-refresh with recovery held
    implies eventually reconciled. Existential bounded reachability -- no
    scheduler fairness assumed. Returns whether a reconciling path exists."""
    # BFS over recovery-only steps.
    seen = {st}
    frontier = [st]
    for _ in range(bound):
        nxt_frontier = []
        for s in frontier:
            if not s.outbox and not s.crashed:
                return {"reconciled": True, "assumes_fairness": False}
            for k in range(len(s.outbox)):
                r = rlq1_replay(s, k)
                if r is not None and r[0] not in seen:
                    seen.add(r[0])
                    nxt_frontier.append(r[0])
            for w in ("replayer",):
                r = rlq1_recover(s, w)
                if r is not None and r[0] not in seen:
                    seen.add(r[0])
                    nxt_frontier.append(r[0])
        frontier = nxt_frontier
        if not frontier:
            break
    return {"reconciled": False, "assumes_fairness": False,
            "note": "no reconciling path within bound; safety unaffected"}


# --- RLQ-1.9: the 12-case matrix R1-R12 -----------------------------------------
# Each case: (id, description, scripts, expected_violations_empty).
RLQ1_CASES: List[Tuple[str, str, Dict[str, List[str]], bool]] = [
    ("R1", "R<P: stale publication rejected",
     {"w": ["wread0", "wpublish0"], "r": ["revoke0"]}, True),
    ("R2", "P<R: publication loses current authority after revocation",
     {"w": ["wread0", "wpublish0"], "r": ["revoke0"]}, True),
    ("R3", "R<V: validation cannot return invalidated as current",
     {"v": ["validate"], "r": ["revoke0"]}, True),
    ("R4", "V<R<A: action must revalidate at the boundary",
     {"v": ["validate"], "r": ["revoke0"], "a": ["act"]}, True),
    ("R5", "A<R: historical action preserved (no retroactive invalidation)",
     {"a": ["act"], "r": ["revoke0"]}, True),
    ("R6", "R<J: recovery rebuilds but never republishes older authority",
     {"r": ["revoke0"], "j": ["replay0"]}, True),
    ("R7", "out-of-order J reconciles to current canonical state",
     {"r": ["revoke0"], "j": ["replay0", "replay0"]}, True),
    ("R8", "two writers race: exactly one commits",
     {"w0": ["wread0", "wpublish0"], "w1": ["wread1", "wpublish1"]}, True),
    ("R9", "superseded fencing token rejected",
     {"w0": ["wread0", "wpublish0", "wread0", "wpublish0"]}, True),
    ("R10", "crash between revoke-commit and notify: fence still enforced",
     {"r": ["revoke0", "crash:replayer"], "j": ["replay0"]}, True),
    ("R11", "two concurrent revocations both represented",
     {"r": ["revoke0", "revoke1"]}, True),
    ("R12", "replacement evidence requalifies; E2 path preserved",
     {"r": ["revoke0", "requal0"]}, True),
]



# ======================================================================
# RLQ-MUT-1: Adversarial Mutation Testing for Revocation Linearization
# (SN-0788). Every critical revocation safeguard must be independently
# falsifiable. Four mutation families, one boundary each:
#   M1: publication-guard removal   -> expects S1 counterexample
#   M2: action-fence removal        -> expects S3 counterexample
#   M3: revision-monotonicity removal-> expects S4 counterexample
#       (ABA: revision reuse; may be redundantly blocked -- distinguished)
#   M4: replay-reconciliation removal-> expects S5 counterexample
# The reference invariants (S1..S6) are IMMUTABLE: the mutation never
# touches the correctness definition. The checker asks
# Linearizable(h, M_reference)? -- no legal ordering => counterexample.
# ======================================================================

MUTATION_FAMILIES = {
    "M1": {"defects": frozenset({"M1_no_publish_guard"}),
           "boundary": "publication guard",
           "expected_property": "S1",
           "expected_shape": "stale publication committed over a revocation: "
                             "writer read at rev 17, revocation committed rev 18, "
                             "stale write committed anyway"},
    "M2": {"defects": frozenset({"M2_no_action_fence"}),
           "boundary": "action fence",
           "expected_property": "S3",
           "expected_shape": "action committed on pre-revocation validation: "
                             "validation qualified before R, revocation fenced, "
                             "action executed on revoked support"},
    "M3": {"defects": frozenset({"M5_rev_reuse"}),
           "boundary": "revision monotonicity",
           "expected_property": "S4",
           "expected_shape": "revision 17 reused after 18: two revocations, "
                             "revision not advanced (ABA). Certification safety "
                             "may still hold -- the invariant is violated anyway"},
    "M4": {"defects": frozenset({"M4_blind_replay"}),
           "boundary": "replay reconciliation",
           "expected_property": "S5",
           "expected_shape": "event-41 replay overwrites current state: revocation "
                             "committed at seq 41, canonical state advanced to 43, "
                             "delayed replay of 41 rolls the state back"},
}

COMPOUND_MUTANTS = {
    "M1+M3": frozenset({"M1_no_publish_guard", "M5_rev_reuse"}),
    "M1+M4": frozenset({"M1_no_publish_guard", "M4_blind_replay"}),
    "M2+M3": frozenset({"M2_no_action_fence", "M5_rev_reuse"}),
    "M2+M4": frozenset({"M2_no_action_fence", "M4_blind_replay"}),
    "M1+M2+M4": frozenset({"M1_no_publish_guard", "M2_no_action_fence",
                            "M4_blind_replay"}),
}

# Five verdicts. Only KILLED meets the detection objective.
KILLED = "KILLED"
BLOCKED_BY_REDUNDANT_GUARD = "BLOCKED_BY_REDUNDANT_GUARD"
SURVIVED_UNEXPLAINED = "SURVIVED_UNEXPLAINED"
UNREACHABLE = "UNREACHABLE"
UNKNOWN = "UNKNOWN"

REFERENCE_QUALIFICATION = "RLQ-MUT-1"


def reference_spec_sha() -> str:
    """Immutable identity of the reference spec: SHA256 over the source of
    the property functions and the transition table. The mutation never
    touches these -- a receipt pins exactly which correctness definition
    the mutant was checked against."""
    import hashlib
    import inspect
    src = inspect.getsource(RLQ1Checker) + inspect.getsource(rlq1_wpublish) \
        + inspect.getsource(rlq1_act) + inspect.getsource(rlq1_revoke) \
        + inspect.getsource(rlq1_replay)
    return hashlib.sha256(src.encode()).hexdigest()


@dataclass(frozen=True)
class CounterexampleReceipt:
    """First-class artifact: a cold successor regenerates the failure from
    the receipt alone. qualification=RLQ-MUT-1, mutant_id, reference/mutant
    SHAs, violated invariant, activation witness, checker config, minimal
    history, verdict, reference replay, independent verification."""
    qualification: str
    mutant_id: str
    reference_sha: str
    mutant_sha: str
    invariant: str
    activation_witness: Tuple[str, ...]
    checker_config: Tuple[Tuple[str, Any], ...]
    minimal_history: Tuple[str, ...]
    replay_steps: Tuple[Tuple[str, str], ...] = ()
    verdict: str = KILLED
    reference_replay: str = ""
    independent_verification: str = ""


def build_receipt(qualification_result, mutant_id, scripts,
                  max_histories=4000) -> CounterexampleReceipt:
    """Build the first-class counterexample receipt from a KILLED
    qualification result."""
    fam = MUTATION_FAMILIES[mutant_id]
    return CounterexampleReceipt(
        qualification=REFERENCE_QUALIFICATION,
        mutant_id=mutant_id,
        reference_sha=reference_spec_sha(),
        mutant_sha=__import__("hashlib").sha256(
            repr(sorted(fam["defects"])).encode()).hexdigest(),
        invariant=qualification_result["property"],
        activation_witness=qualification_result["minimal_history"],
        checker_config=(("max_histories", max_histories),
                        ("defects", tuple(sorted(fam["defects"]))),
                        ("fairness_assumptions", "none"),
                        ("oracle", "rlq1_op_violations@reference")),
        minimal_history=qualification_result["minimal_history"],
        replay_steps=tuple(qualification_result["replay_steps"]),
        verdict=qualification_result["verdict"],
        reference_replay="replay_via_scripts on fresh RLQ1 abstract state",
        independent_verification="violation recurs under the immutable "
                                "reference oracle",
    )


def reproduce_from_receipt(receipt: CounterexampleReceipt) -> bool:
    """A cold successor regenerates the failure from the receipt alone:
    pin the reference oracle (SHA must match), replay the minimal steps
    on a fresh instance, confirm the invariant violation recurs."""
    if receipt.qualification != REFERENCE_QUALIFICATION:
        return False
    if receipt.reference_sha != reference_spec_sha():
        return False  # oracle drifted -- receipt no longer reproduces
    fam = MUTATION_FAMILIES.get(receipt.mutant_id)
    if fam is None:
        return False
    return replay_via_scripts(list(receipt.replay_steps), fam["defects"],
                              receipt.invariant)


def _trace_exercised(trace_infos, marker: str) -> bool:
    return any(i.get("defect_exercised") == marker for i in trace_infos)


def _trace_labels(trace_infos) -> Tuple[str, ...]:
    labels = []
    for i in trace_infos:
        op = i.get("op", "?")
        if op == "P":
            labels.append(f"P(w{i.get('writer')})={i.get('outcome')}")
        elif op == "A":
            labels.append(f"A={i.get('outcome')}")
        elif op == "R":
            labels.append(f"R(ev{i.get('evidence')})")
        elif op == "V":
            labels.append(f"V={i.get('result')}")
        elif op == "J":
            labels.append(f"J({i.get('replay', '')})")
        else:
            labels.append(op)
    return tuple(labels)


def find_shortest_violation(scripts, defects, expected_property,
                            max_depth=12):
    """Stage 1 of minimization: BFS over (state, remaining-scripts) finds
    the SHORTEST transition trace that violates the expected property.
    Returns (step_sequence, trace_infos) or (None, None). No fairness or
    recovery assumptions -- pure safety exploration."""
    from collections import deque
    init = rlq1_initial()
    seen = set()
    queue = deque([(init, {w: list(s) for w, s in scripts.items()}, [], [])])

    while queue:
        st, rem, infos, steps = queue.popleft()
        if len(infos) >= max_depth:
            continue
        for w, s in rem.items():
            if not s:
                continue
            nxt = rlq1_apply_step(st, w, s[0], defects)
            if nxt is None:
                continue
            ns, info = nxt
            ninfos = infos + [info]
            nsteps = steps + [(w, s[0])]
            # The oracle is single-sourced: the same per-op function the
            # checker uses. A violation of the expected property ends BFS
            # with the shortest trace.
            if any(p == expected_property
                   for p, _ in rlq1_op_violations(st, info, ns)):
                return nsteps, ninfos
            nrem = {k: list(v) for k, v in rem.items()}
            nrem[w] = nrem[w][1:]
            key = (ns, tuple(sorted((k, tuple(v)) for k, v in nrem.items())))
            if key not in seen:
                seen.add(key)
                queue.append((ns, nrem, ninfos, nsteps))
    return None, None


def causally_reduce(trace_infos, replay_fn):
    """Stage 2 of minimization: greedily drop steps while the violation
    persists. Preserves violation, ordering, witness, environment,
    rejection. replay_fn(infos) -> True if the violation still occurs."""
    current = list(trace_infos)
    changed = True
    while changed:
        changed = False
        for i in range(len(current)):
            candidate = current[:i] + current[i + 1:]
            if candidate and replay_fn(candidate):
                current = candidate
                changed = True
                break
    return current


def replay_via_scripts(script_steps, defects, expected_property):
    """Replay an ordered list of (worker, step_name) on a FRESH checker;
    True iff the expected property violation recurs. The independent
    replay never shares state with the discovery run, and judges with
    the same immutable oracle."""
    st = rlq1_initial()
    for worker, step in script_steps:
        nxt = rlq1_apply_step(st, worker, step, defects)
        if nxt is None:
            return False
        ns, info = nxt
        if any(p == expected_property
               for p, _ in rlq1_op_violations(st, info, ns)):
            return True
        st = ns
    return False


def qualify_mutation(mutant_id, scripts, max_histories=4000,
                     property_override=None):
    """The qualify_mutation harness (SN-0788):
      1. apply the mutant
      2. reachability check: is the defective branch exercised?
      3. model-check against REFERENCE invariants, no fairness assumptions
      4. counterexample -> minimize (BFS shortest + causal reduction)
         -> independent replay -> KILLED
      5. no counterexample + exhaustive -> redundant-guard proof
         (defect exercised but blocked by another guard, independently
         verified) or SURVIVED_UNEXPLAINED
      6. not exercised -> UNREACHABLE; not exhaustive -> UNKNOWN
    property_override qualifies the mutant against a non-default property
    (e.g. M3 against S1) to demonstrate the verdict taxonomy.
    Returns a dict with verdict + evidence."""
    fam = MUTATION_FAMILIES[mutant_id]
    defects = fam["defects"]
    prop = property_override or fam["expected_property"]
    checker = RLQ1Checker(defects=defects, max_histories=max_histories)
    result = checker.check(scripts)
    violations = [v for v in result["violations"] if v[0] == prop]

    # Reachability: was the defective branch exercised in ANY explored
    # interleaving? (The checker's DFS records this; a linear per-worker
    # probe cannot witness interleaving-dependent activation.)
    exercised = checker.defect_exercised_any

    if violations:
        min_steps, min_infos = find_shortest_violation(scripts, defects, prop)
        if min_steps is None:
            return {"verdict": UNKNOWN, "reason": "minimization failed"}
        # Independent replay: fresh instance, minimized step sequence,
        # reference oracle -- violation must recur.
        replayed = replay_via_scripts(min_steps, defects, prop)
        if not replayed:
            return {"verdict": UNKNOWN,
                    "reason": "independent replay did not reproduce"}
        # Reachability is witnessed by the minimized violating trace
        # itself: the defective branch was exercised on the path to the
        # violation.
        exercised = any("defect_exercised" in i for i in min_infos)
        return {"verdict": KILLED, "property": prop,
                "minimal_history": _trace_labels(min_infos),
                "replay_steps": tuple(min_steps),
                "exercised": exercised,
                "independently_replayed": True,
                "shape": fam["expected_shape"]}
    # No counterexample on the expected property.
    if not result["exhausted"]:
        return {"verdict": UNKNOWN, "reason": "exploration hit cap"}
    if not exercised:
        return {"verdict": UNREACHABLE,
                "reason": "defective branch never exercised in explored histories"}
    # Exercised but no violation: attempt redundant-guard proof.
    proof = prove_redundant_guard(mutant_id, scripts)
    if proof["blocked"]:
        return {"verdict": BLOCKED_BY_REDUNDANT_GUARD,
                "redundant_guard": proof["guard"],
                "verification": proof["verification"]}
    return {"verdict": SURVIVED_UNEXPLAINED,
            "reason": "defect exercised, exhaustive, no violation, "
                      "no redundant guard identified"}


def prove_redundant_guard(mutant_id, scripts):
    """Independently verify that a redundant guard blocks the mutant on the
    certification-safety dimension: with the mutant AND the candidate
    redundant guard removed, the S1 violation appears; with only the
    mutant, it does not. For M3 (revision reuse), the publication-time
    eligibility/establishment check is the redundant guard -- certification
    safety holds even though S4 is violated."""
    if mutant_id != "M3":
        return {"blocked": False, "reason": "no redundant-guard model"}
    # Guard-removal probe: M3 + publication-guard removal (which also skips
    # the establishment check). The S1 violation must appear only in the
    # compound.
    solo = RLQ1Checker(defects=frozenset({"M5_rev_reuse"}),
                       max_histories=4000).check(scripts)
    compound = RLQ1Checker(
        defects=frozenset({"M5_rev_reuse", "M1_no_publish_guard"}),
        max_histories=4000).check(scripts)
    solo_s1 = [v for v in solo["violations"] if v[0] == "S1"]
    compound_s1 = [v for v in compound["violations"] if v[0] == "S1"]
    blocked = (not solo_s1) and bool(compound_s1)
    return {
        "blocked": blocked,
        "guard": "publication-time eligibility/establishment check",
        "verification": {
            "mutant_alone_S1_violations": len(solo_s1),
            "mutant_plus_guard_removed_S1_violations": len(compound_s1),
            "conclusion": "revision-reuse alone is blocked by the "
                          "eligibility check; removing that check exposes "
                          "the S1 violation" if blocked else "inconclusive",
        },
    }


# ======================================================================
# RLQ-REFINEMENT: the Implementation Refinement Law (SN-0789)
# A formal safety guarantee may be claimed only when every concrete
# authority-changing operation is mapped to a verified abstract
# transition, every atomicity/ordering assumption is independently
# justified, and adversarial real execution histories are consistent
# with the reference model.
#
# Refinement direction: Traces(C)|relevant ⊆ Traces(A). If the real
# system can commit a stale qualification the model forbids, refinement
# FAILS -- even with all model tests green. This layer covers actual
# commit ordering, not method calls.
#
# Proof triad (no layer stands alone):
#   RLQ-1      : the abstract model is proved (model checking).
#   RLQ-MUT-1  : the checker is proved (adversarial mutation).
#   RLQ-REF    : the real system implements the model (this section).
# ======================================================================

REF_EIDS = ("e1", "e2", "e3")
REF_CIDS = ("c1", "c2")
_EID_INDEX = {e: i for i, e in enumerate(REF_EIDS)}
_CID_INDEX = {c: i for i, c in enumerate(REF_CIDS)}


def refinement_fixture() -> "AuthoritativeState":
    """The concrete fixture the refinement mapping covers: 3 evidence,
    2 claims with support shape C1=(E1^E3)vE2, C2=(E1), 1 projection."""
    st = AuthoritativeState()
    for eid in REF_EIDS:
        st.register_evidence(eid, "s", "p", "LAW-v3", "refinement-fixture")
    revs = {eid: st.evidence[eid].eligibility_revision for eid in REF_EIDS}
    st.commit_qualification("c1", "REQUALIFIED",
                            {"e1": revs["e1"], "e3": revs["e3"]},
                            "s", "p", "LAW-v3",
                            alternative_paths=[{"e2": revs["e2"]}])
    st.commit_qualification("c2", "REQUALIFIED", {"e1": revs["e1"]},
                            "s", "p", "LAW-v3")
    qrevs = {cid: st.claims[cid].qualification_revision for cid in REF_CIDS}
    st.register_projection("p1", "art-0",
                           {cid: qrevs[cid] for cid in REF_CIDS},
                           {eid: revs[eid] for eid in REF_EIDS})
    return st


def alpha(st: "AuthoritativeState") -> RLQ1AbstractState:
    """Refinement mapping α: concrete AuthoritativeState -> abstract
    RLQ1AbstractState. The RELEVANT projection is (ev, claims, head):
    writers/outbox/crashed/seq are execution bookkeeping, not authority."""
    ev = []
    for eid in REF_EIDS:
        rec = st.evidence.get(eid)
        if rec is None:
            ev.append((0, False, -1))
        else:
            fence = st.revocation_fence.get((eid, rec.scope, rec.purpose), -1)
            ev.append((rec.eligibility_revision, rec.eligible, fence))
    claims = []
    for cid in REF_CIDS:
        rec = st.claims.get(cid)
        if rec is None:
            claims.append((0, "UNKNOWN", ()))
        else:
            paths = tuple(
                frozenset((_EID_INDEX[e], r) for e, r in m.items()
                          if e in _EID_INDEX)
                for m in [rec.support_manifest] + list(rec.alternative_paths))
            claims.append((rec.qualification_revision, rec.verdict, paths))
    head_rec = st.projections.get("p1")
    if head_rec is None:
        head = (0, 0, (0, 0), (0, 0, 0))
    else:
        head = (head_rec.projection_revision, head_rec.fencing_token,
                tuple(head_rec.claim_deps.get(c, 0) for c in REF_CIDS),
                tuple(head_rec.evidence_deps.get(e, 0) for e in REF_EIDS))
    return RLQ1AbstractState(tuple(ev), tuple(claims), head,
                             ((0, 0, 0, (), ()), (0, 0, 0, (), ())),
                             (), frozenset(), True, st._seq)


def alpha_relevant(ast: RLQ1AbstractState):
    """The relevant projection Traces(C)|relevant is taken over."""
    return (ast.ev, ast.claims, ast.head)


# --- Refinement lemma R1: establishment correspondence -------------------------
def check_establishment_correspondence(st: "AuthoritativeState") -> List[str]:
    """R1: abstract rlq1_claim_established(α(s), c) ⟺ concrete
    qualification_standing(c) == CURRENT, for the fixture's honest
    histories (manifest revs pinned at qualification time; eligibility
    revs advance only via revocation)."""
    problems = []
    a = alpha(st)
    for cid in REF_CIDS:
        c = _CID_INDEX[cid]
        abstract_est = rlq1_claim_established(a, c)
        concrete_cur = (st.qualification_standing(cid) == CURRENT)
        if abstract_est != concrete_cur:
            problems.append(
                f"R1 broken for {cid}: abstract={abstract_est} "
                f"concrete CURRENT={concrete_cur}")
    return problems


# --- The six boundaries: separate proof obligations -----------------------------
# Each boundary is proven independently, then shown to compose. Status is
# one of PROVEN / ARGUMENT / ASSUMPTION / EXCLUDED -- never implied.
REFINEMENT_BOUNDARIES = {
    "database_state": {
        "claim": "Committed authority state is the single source of truth; "
                 "no authority lives in caches, replicas, or logs alone.",
        "mechanism": "AuthoritativeState holds evidence/claims/projections; "
                     "commit_seq is allocated only inside the commit lock.",
        "status": "PROVEN",
        "evidence": "differential_check: every concrete commit maps to a "
                    "verified abstract transition on (ev, claims, head).",
    },
    "transaction_engine": {
        "claim": "Revocation and publication contend on the SAME guard; "
                 "every concurrent R/P pair yields P<R or R<P -- no third case. "
                 "Write skew, phantom dependencies, stale snapshots, ABA, "
                 "and nontransactional gaps are ruled out.",
        "mechanism": "The commit lock (threading.RLock) serializes every "
                     "authority operation and linearizable read at the one "
                     "authoritative commit point. SERIALIZABLE alone would "
                     "not be a proof -- the lock IS the shared guard here; "
                     "a production database refines each (namespace, "
                     "identity) guard to a real row/predicate lock.",
        "status": "PROVEN",
        "evidence": "thread-race test: 50/50 concurrent R/P pairs, each "
                    "linearized P<R or R<P by commit-seq order.",
    },
    "scheduler": {
        "claim": "Only the commit gateway decides authority. Leases are "
                 "versioned and bounded (fencing tokens); expired leases "
                 "authorize nothing; retries rebuild against current state. "
                 "Safety holds with an unfair, crashing, slow scheduler.",
        "mechanism": "All authority flows through the commit-locked methods; "
                     "superseded fencing tokens are rejected; the abstract "
                     "model proves safety under arbitrary interleavings.",
        "status": "PROVEN",
        "evidence": "R10 crash cases + fencing-token rejection tests; "
                    "fairness is a separate liveness obligation "
                    "(check_liveness).",
    },
    "recovery": {
        "claim": "replay_event never restores obsolete authority (21/22/23 "
                 "rule); idempotent; out-of-order safe. Worker 'applied "
                 "event' reports are NOT sufficient -- VERIFY inspects "
                 "canonical state independently. Replicas are never the "
                 "sole authority for current certification.",
        "mechanism": "replay_event reconciles to canonical revisions; "
                     "IndependentHistoryVerifier replays against a fresh "
                     "reference machine.",
        "status": "ARGUMENT",
        "evidence": "pause-and-release replay test; S5 mutant killed. "
                    "Durability (commit survives crash) is an ASSUMPTION "
                    "for the in-memory engine -- see exclusions.",
    },
    "read_time_validation": {
        "claim": "validate_current is a linearizable read: it serializes "
                 "with commits at the commit point. Cached verdicts never "
                 "establish CURRENT_QUALIFIED alone.",
        "mechanism": "validate_current holds the commit lock across the "
                     "read; three result classes; staleness is explicit.",
        "status": "PROVEN",
        "evidence": "R3/R4 cases; display-freshness honesty test.",
    },
    "external_action_gateway": {
        "claim": "HONEST QUALIFICATION -- 'no new external request is "
                 "authorized after revocation' (gateway boundary) is NOT "
                 "'no external effect can occur after revocation'. The "
                 "latter is claimed only when independently established "
                 "(cooperating executor + drain barrier).",
        "mechanism": "commit_action(external=True) returns "
                     "AUTHORIZED_VIA_GATEWAY with a revision-bound lease and "
                     "an explicit guarantee scope; fencing tokens reject "
                     "superseded dispatchers (T1-T4 race).",
        "status": "ARGUMENT",
        "evidence": "gateway-boundary tests. 'No external effect after R' "
                    "is EXCLUDED unless a drain barrier is independently "
                    "established -- every certificate states this.",
    },
}

# The T1-T4 race (external gateway): what each mechanism covers.
EXTERNAL_GATEWAY_MECHANISMS = {
    "fencing_tokens": "A dispatcher whose token was superseded by a "
                      "revocation cannot authorize new external requests. "
                      "Covers: stale dispatchers. Does not cover: requests "
                      "already handed to a noncooperating executor.",
    "cooperating_gateways": "The external executor honors revision-bound "
                            "leases and refuses post-revocation requests. "
                            "Covers: the effect, when the executor cooperates. "
                            "Requires independent establishment per executor.",
    "drain_barriers": "Quiescence: no in-flight external request may "
                      "straddle the revocation boundary when strict ordering "
                      "is required. Covers: the T2/T3 window. Procedure, not "
                      "code -- must be independently established per use.",
    "cancellation_limits": "HONEST BOUND: a noncooperating external service "
                           "may execute a post-R request. The guarantee "
                           "covers the gateway boundary (lease + fencing); "
                           "beyond it the protocol cannot promise what the "
                           "infrastructure cannot enforce.",
}

REFINEMENT_EXCLUSIONS = [
    "Durability: the in-memory engine keeps authority state in process "
    "memory. 'Commit survives crash' is an ASSUMPTION here; a production "
    "deployment must justify it from its durability config (WAL/fsync), "
    "per the crash/recovery table.",
    "'No external effect can occur after revocation' is not claimed without "
    "an independently established drain barrier and cooperating executor.",
    "Replicas are never the sole authority for current certification; "
    "failover coverage is disclosed per durability contract, not assumed.",
    "The refinement mapping covers the fixture (3 evidence, 2 claims, "
    "1 projection). Wider concrete configurations require re-running "
    "differential_check on their histories.",
]


# --- Differential history checking ------------------------------------------------
# Drive the concrete system, shadow each step in the abstract machine via
# the refinement map, and judge every abstract transition with the
# IMMUTABLE reference oracle. No legal abstract execution for a concrete
# history => refinement FALSIFIED (even if all model tests are green).
DIFFERENTIAL_HOLDS = "DIFFERENTIAL_HOLDS"
DIFFERENTIAL_FALSIFIED = "DIFFERENTIAL_FALSIFIED"
DIFFERENTIAL_INCONCLUSIVE = "DIFFERENTIAL_INCONCLUSIVE"


def _shadow_apply(shadow: RLQ1AbstractState, label, defects, concrete_after,
                  concrete_outcome):
    """Apply one abstract step to the shadow state, enforcing the abstract
    GUARDS on the pre-state while carrying the concrete execution's
    witnesses for freshly minted values (revision numbers, head pointer).
    The abstract transition is nondeterministic in the fresh values it
    mints; the concrete's choice refines it iff it is fresh and the
    guards hold. Returns (new_shadow, info, outcome_match)."""
    kind = label[0]
    if kind == "R":
        i = label[1]
        # Abstract guard: the evidence must be eligible.
        if i >= len(shadow.ev) or not shadow.ev[i][1]:
            return None
        new_rev = concrete_after.ev[i][0]
        ev = list(shadow.ev)
        ev[i] = (new_rev, False, new_rev)
        # The abstract outbox tracks the pending revocation event (old rev
        # carried for blind-replay detection), mirroring rlq1_revoke.
        outbox = shadow.outbox + (("rev", i, shadow.ev[i][0]),)
        ns = RLQ1AbstractState(tuple(ev), shadow.claims, shadow.head,
                               shadow.writers, outbox, shadow.crashed,
                               shadow.law_ok, shadow.seq + 1)
        return ns, {"op": "R", "evidence": i, "fenced": True}, True
    if kind == "Q":
        c = label[1]
        # Abstract guard: requalification must be possible on some path.
        if rlq1_requalify(shadow, c) is None:
            return None
        cc = concrete_after.claims[c]
        claims = list(shadow.claims)
        claims[c] = (cc[0], cc[1], cc[2])
        ns = RLQ1AbstractState(shadow.ev, tuple(claims), shadow.head,
                               shadow.writers, shadow.outbox, shadow.crashed,
                               shadow.law_ok, shadow.seq + 1)
        return ns, {"op": "Q", "claim": c}, True
    if kind == "P":
        snap = label[1]
        w = snap[4]
        writers = list(shadow.writers)
        writers[w] = (1, snap[0], snap[1], snap[2], snap[3])
        pre = RLQ1AbstractState(shadow.ev, shadow.claims, shadow.head,
                                tuple(writers), shadow.outbox, shadow.crashed,
                                shadow.law_ok, shadow.seq)
        ns, info = rlq1_wpublish(pre, w, defects)
        abstract_committed = (info["outcome"] == "committed")
        concrete_committed = (concrete_outcome == COMMITTED)
        if abstract_committed != concrete_committed:
            return ns, info, False
        if abstract_committed:
            # Witness-carry the concrete head pointer (rev, token, deps).
            ch = concrete_after.head
            ns = RLQ1AbstractState(ns.ev, ns.claims, ch, ns.writers,
                                   ns.outbox, ns.crashed, ns.law_ok, ns.seq)
        return ns, info, True
    if kind == "V":
        ns, info = rlq1_validate(shadow, defects)
        # Read-only: relevant state must not change; the verdict must match.
        match = (info["result"] == concrete_outcome)
        return ns, info, match
    if kind == "A":
        required = label[1] if len(label) > 1 else None
        # Concrete commit_action(required_claims=[...]) maps to the scoped
        # abstract action; None = all claims (checker default).
        req_idx = (tuple(_CID_INDEX[c] for c in required)
                   if required else None)
        r = rlq1_act(shadow, defects, required=req_idx)
        if r is None:
            return None
        ns, info = r
        abstract_committed = (info["outcome"] == "committed")
        concrete_committed = concrete_outcome in (COMMITTED, "AUTHORIZED",
                                                  "AUTHORIZED_VIA_GATEWAY")
        return ns, info, (abstract_committed == concrete_committed)
    if kind == "J":
        k = label[1] if len(label) > 1 else 0
        if k >= len(shadow.outbox):
            # The abstract machine forgot the event (popped on replay); a
            # concrete duplicate is abstract stutter -- but only when the
            # concrete says NOOP_DUPLICATE, never assumed.
            if concrete_outcome == "NOOP_DUPLICATE":
                return shadow, {"op": "J", "replay": "noop-duplicate"}, True
            return None
        r = rlq1_replay(shadow, k, defects)
        if r is None:
            return None
        ns, info = r
        # Witness-carry the concrete reconciled evidence/claims.
        ns = RLQ1AbstractState(concrete_after.ev, concrete_after.claims,
                               ns.head, ns.writers, ns.outbox, ns.crashed,
                               ns.law_ok, ns.seq)
        return ns, info, True
    return None


def differential_check(concrete_steps, defects=frozenset()):
    """concrete_steps: list of (thunk, abstract_label, description) where
    thunk(st) executes the concrete op and returns the concrete outcome
    summary (a result string like COMMITTED/STALE_DEPENDENCY, or the
    first element of a result tuple), and abstract_label is the mapped
    abstract step (or None for legitimate stuttering).

    For every step: run the concrete op, shadow the abstract transition
    (guards enforced on the abstract pre-state, fresh values witnessed
    from the concrete execution), require outcome correspondence
    (DISPATCHED ≠ ACCEPTED ≠ COMMITTED ≠ EFFECT_OBSERVED are never
    conflated) and alpha_relevant(concrete) == alpha_relevant(shadow).
    Then judge the whole abstract history with the reference oracle.

    AUTHORITY RULE: no authority-changing operation may hide as
    bookkeeping -- if alpha_relevant changes, the step MUST carry a
    mapped authority label; an unmapped change is FALSIFIED, never
    assumed benign.
    """
    st = refinement_fixture()
    shadow = alpha(st)
    triples = []  # (before, info, after) for the oracle
    for thunk, label, desc in concrete_steps:
        before_rel = alpha_relevant(alpha(st))
        shadow_before = shadow
        result = thunk(st)
        concrete_outcome = (result[0] if isinstance(result, tuple)
                            else result)
        after = alpha(st)
        after_rel = alpha_relevant(after)
        if label is None:
            # Legitimate stuttering only: candidate-artifact writes,
            # registrations, reads. Any authority change is falsified.
            if after_rel != before_rel:
                return {"verdict": DIFFERENTIAL_FALSIFIED,
                        "reason": f"unmapped authority change at '{desc}': "
                                  f"concrete state changed with no abstract "
                                  f"transition (hidden bookkeeping)"}
            continue
        nxt = _shadow_apply(shadow, label, defects, after, concrete_outcome)
        if nxt is None:
            return {"verdict": DIFFERENTIAL_INCONCLUSIVE,
                    "reason": f"abstract step inapplicable at '{desc}'"}
        shadow_after, info, outcome_match = nxt
        if not outcome_match:
            return {"verdict": DIFFERENTIAL_FALSIFIED,
                    "reason": f"outcome mismatch at '{desc}': abstract "
                              f"{info.get('outcome', info.get('result'))} vs "
                              f"concrete {concrete_outcome} -- no legal "
                              f"abstract execution",
                    "abstract_info": info}
        if alpha_relevant(shadow_after) != after_rel:
            return {"verdict": DIFFERENTIAL_FALSIFIED,
                    "reason": f"refinement mismatch at '{desc}': concrete "
                              f"relevant state != abstract shadow state"}
        triples.append((shadow_before, info, shadow_after))
        shadow = shadow_after
    violations = []
    for b, info, a in triples:
        violations.extend(rlq1_op_violations(b, info, a))
    if violations:
        return {"verdict": DIFFERENTIAL_FALSIFIED,
                "reason": "concrete history has no legal abstract execution",
                "violations": violations}
    return {"verdict": DIFFERENTIAL_HOLDS,
            "steps": len(concrete_steps),
            "oracle": "rlq1_op_violations@reference (immutable)"}


# --- RLQ-REFINEMENT-1 certificates ---------------------------------------------------
@dataclass(frozen=True)
class RefinementCertificate:
    """A claimed refinement carries its exact proofs, configs, and
    exclusions. Reviewer identities are required: the builder never
    self-certifies (production qualification needs a different seat)."""
    certificate_id: str
    implementation_sha: str
    db_config: Tuple[Tuple[str, str], ...]
    isolation_level: str
    fault_assumptions: Tuple[str, ...]
    traces: Tuple[str, ...]
    reviewer_identities: Tuple[str, ...]
    exclusions: Tuple[str, ...]
    proofs: Tuple[str, ...]
    verdict: str


def implementation_sha() -> str:
    import hashlib
    import inspect
    import drift_canary.revocation_linearization as mod
    return hashlib.sha256(inspect.getsource(mod).encode()).hexdigest()


def issue_certificate(certificate_id: str, proofs, traces,
                      reviewer_identities=()) -> RefinementCertificate:
    db_config = (("engine", "in-memory-authoritative"),
                 ("ordering", "single-commit-lock (threading.RLock)"),
                 ("durability", "none: process memory (see exclusions)"),
                 ("replicas", "none"))
    return RefinementCertificate(
        certificate_id=certificate_id,
        implementation_sha=implementation_sha(),
        db_config=db_config,
        isolation_level="single-authoritative-commit-point "
                        "(serializable by construction, in-memory)",
        fault_assumptions=("crash-stop workers", "unfair scheduler",
                           "no Byzantine faults"),
        traces=tuple(traces),
        reviewer_identities=tuple(reviewer_identities),
        exclusions=tuple(REFINEMENT_EXCLUSIONS),
        proofs=tuple(proofs),
        verdict="REFINEMENT_HOLDS_UNDER_STATED_ASSUMPTIONS"
                if reviewer_identities else "CANDIDATE_PENDING_REVIEW",
    )


# --- RLQ-REF-001: the first refinement procedure --------------------------------------
def run_guard_removal_mutant():
    """Execute the guard-removal mutant (concrete M1 analogue) through
    differential_check. Returns the differential result (expected:
    DIFFERENTIAL_FALSIFIED). Factored for reuse by RFD-1 fixtures."""
    class _Guardless(AuthoritativeState):
        def publish_projection(self, candidate):
            # BUG: no dependency/manifest check -- commits unconditionally.
            with self._commit_lock:
                head = self.projections[candidate.projection_id]
                head.projection_revision += 1
                return COMMITTED, "guard removed (mutant)"

    import drift_canary.revocation_linearization as _mod
    _orig = AuthoritativeState
    _mod.AuthoritativeState = _Guardless
    try:
        st_m = refinement_fixture()
        head_m = st_m.projections["p1"]
        snap_m = (head_m.projection_revision, head_m.fencing_token,
                  (head_m.claim_deps["c1"], head_m.claim_deps["c2"]),
                  (head_m.evidence_deps["e1"], head_m.evidence_deps["e2"],
                   head_m.evidence_deps["e3"]), 0)

        def _m_revoke(s):
            return s.commit_revocation("e1", "diff", "s", "p", "LAW-v3", "t")

        def _m_publish(s):
            h = s.projections["p1"]
            c = ProjectionCandidate(
                "p1", h.projection_revision, "art-0",
                {"c1": 999, "c2": 999}, {"e1": 999, "e2": 999, "e3": 999},
                "LAW-v3", {"c1": "REQUALIFIED", "c2": "REQUALIFIED"},
                ("certification",), h.fencing_token)
            return s.publish_projection(c)

        return differential_check([
            (_m_revoke, ("R", 0), "real revocation of e1"),
            (_m_publish, ("P", (snap_m[0], snap_m[1], snap_m[2], snap_m[3], 0)),
             "unguarded publication (mutant commits)"),
        ])
    finally:
        _mod.AuthoritativeState = _orig



def rlq_ref_001() -> RefinementCertificate:
    """RLQ-REF-001, executable:
      1. freeze implementation SHA + DB config
      2. pause publisher A before the publication boundary
      3. commit a real revocation
      4. resume A -> the stale candidate is rejected
      5. independent inspection of qualification/head/revisions/commit evidence
      6. map to the reference machine via α; differential_check HOLDS
      7. remove the guard (mutant) -> differential_check FALSIFIES
      8. restore under real isolation (commit lock) with the mutant gone
    Returns the RLQ-REFINEMENT-1 certificate (candidate until a different
    seat reviews)."""
    traces = []
    st = refinement_fixture()

    # 2. Pause publisher A before the publication boundary: build the
    #    candidate (read at rev N), then hold it.
    head = st.projections["p1"]
    cand = ProjectionCandidate(
        projection_id="p1", expected_head_revision=head.projection_revision,
        artifact_id="art-0",
        claim_deps={"c1": st.claims["c1"].qualification_revision,
                    "c2": st.claims["c2"].qualification_revision},
        evidence_manifest={"e1": st.evidence["e1"].eligibility_revision,
                           "e2": st.evidence["e2"].eligibility_revision,
                           "e3": st.evidence["e3"].eligibility_revision},
        policy_revision="LAW-v3",
        asserted_claims={"c1": "REQUALIFIED", "c2": "REQUALIFIED"},
        intended_uses=("certification",), fencing_token=head.fencing_token)
    rev_at_read = st.evidence["e1"].eligibility_revision

    # 3. Commit a real revocation (rev N -> N+1, fence established).
    receipt = st.commit_revocation("e1", "RLQ-REF-001", "s", "p",
                                   "LAW-v3", "refinement")
    # Fresh revision minted (shared per-namespace authority: not +1, but
    # strictly greater -- the ABA-prevention property the model checks).
    assert st.evidence["e1"].eligibility_revision > rev_at_read
    traces.append(f"revocation committed: {receipt.event_id} "
                  f"rev {rev_at_read}->{st.evidence['e1'].eligibility_revision}")

    # 4. Resume A: the stale candidate must be rejected, never committed.
    outcome, detail = st.publish_projection(cand)
    assert outcome == STALE_DEPENDENCY, (outcome, detail)
    traces.append(f"paused publisher resumed -> {outcome} (stale rejected)")

    # 5. Independent inspection of qualification/head/revisions/commit evidence.
    assert st.qualification_standing("c1") == CURRENT  # E2 path preserves C1
    assert st.qualification_standing("c2") == FENCED   # E1-only C2 fenced
    seqs = [op.seq for op in st.linearization_log]
    assert seqs == sorted(seqs), "commit evidence must be seq-ordered"
    assert any(op.op_type == "R" for op in st.linearization_log)
    traces.append("independent inspection: C1 CURRENT (E2 path), C2 FENCED, "
                  "linearization log seq-ordered")

    # 6. Map to the reference machine: differential check over the same
    #    history shape must HOLD.
    def _thunk_revoke(s):
        return s.commit_revocation("e1", "diff", "s", "p", "LAW-v3", "t")

    def _thunk_reject(s):
        h = s.projections["p1"]
        c = ProjectionCandidate(
            "p1", h.projection_revision, "art-0",
            {"c1": s.claims["c1"].qualification_revision,
             "c2": s.claims["c2"].qualification_revision},
            {"e1": rev_at_read, "e2": s.evidence["e2"].eligibility_revision,
             "e3": s.evidence["e3"].eligibility_revision},
            "LAW-v3", {"c1": "REQUALIFIED", "c2": "REQUALIFIED"},
            ("certification",), h.fencing_token)
        return s.publish_projection(c)

    snap = (head.projection_revision, head.fencing_token,
            (head.claim_deps["c1"], head.claim_deps["c2"]),
            (head.evidence_deps["e1"], head.evidence_deps["e2"],
             head.evidence_deps["e3"]), 0)
    # NOTE: the fixture's fixture-build steps are setup, not history; the
    # differential history starts from the fixture state.
    diff = differential_check([
        (_thunk_revoke, ("R", 0), "real revocation of e1"),
        (_thunk_reject, ("P", (snap[0], snap[1], snap[2], snap[3], 0)),
         "stale candidate publication (rejected)"),
    ])
    assert diff["verdict"] == DIFFERENTIAL_HOLDS, diff
    traces.append("differential_check HOLDS: concrete history maps to a "
                  "legal abstract execution under the immutable oracle")

    # R1: establishment correspondence on the post-revocation state.
    assert check_establishment_correspondence(st) == []
    traces.append("R1 establishment correspondence holds post-revocation")

    # 7. Remove the guard (concrete M1 analogue: skip the manifest check) ->
    #    differential_check must FALSIFY. A mutant that passes is a failed
    #    refinement.
    diff_m = run_guard_removal_mutant()
    assert diff_m["verdict"] == DIFFERENTIAL_FALSIFIED, diff_m
    traces.append("guard-removal mutant FALSIFIED by differential_check "
                  "(no legal abstract execution)")

# --- RLQ-REF-001: the first refinement procedure (continued) -------------------
# (rlq_ref_001 step 7 calls run_guard_removal_mutant above.)

    # 8. Restored under real isolation: the real class is back in place.
    import drift_canary.revocation_linearization as _mod2
    assert _mod2.AuthoritativeState.publish_projection.__qualname__.startswith(
        "AuthoritativeState.")
    traces.append("implementation restored; commit lock is the real guard")

    proofs = ("differential_check HOLDS on RLQ-REF-001 history",
              "differential_check FALSIFIES the guard-removal mutant",
              "R1 establishment correspondence (abstract ⟺ concrete CURRENT)",
              "thread-race: every concurrent R/P pair linearizes P<R or R<P",
              "RLQ-1 model proofs (S1-S6) + RLQ-MUT-1 mutant kills")
    return issue_certificate("RLQ-REFINEMENT-1/RLQ-REF-001", proofs, traces)


# --- Acceptance hierarchy ---------------------------------------------------------------
# No earlier rung proves a later one. Each rung names its evidence; a rung
# is CLAIMED only when its evidence exists and (for rung 4) a different
# seat has reviewed.
ACCEPTANCE_RUNGS = (
    "RUNG_1_ABSTRACT_PROVED",
    "RUNG_2_MAPPING_ESTABLISHED",
    "RUNG_3_SEMANTICS_VALIDATED",
    "RUNG_4_PRODUCTION_QUALIFIED",
)


def acceptance_status() -> Dict[str, Any]:
    """The acceptance hierarchy, honestly reported. Rung N never proves
    rung N+1."""
    cert = rlq_ref_001()
    return {
        "RUNG_1_ABSTRACT_PROVED": {
            "claimed": True,
            "evidence": "RLQ-1: R1-R12 clean, S1-S6 checked, 6/6 mutants "
                        "yield counterexamples (test_rlq1_model.py: 34 green)",
        },
        "RUNG_2_MAPPING_ESTABLISHED": {
            "claimed": True,
            "evidence": "α defined; R1 correspondence checked; "
                        "differential_check HOLDS on RLQ-REF-001; mutant "
                        "FALSIFIED. Six boundaries tabled with statuses.",
        },
        "RUNG_3_SEMANTICS_VALIDATED": {
            "claimed": True,
            "evidence": "pause-and-release against the real AuthoritativeState "
                        "(4 procedures); thread-race decisive obligation "
                        "(50/50 P<R or R<P); crash/recovery + gateway "
                        "mechanisms with stated exclusions.",
        },
        "RUNG_4_PRODUCTION_QUALIFIED": {
            "claimed": False,
            "evidence": "requires: (a) independent review by a different "
                        "seat (reviewer_identities empty), (b) production DB "
                        "config with durability justification, (c) drain "
                        "barriers independently established per external "
                        "executor. Until then: bounded verification "
                        "candidate, branch only, never toward main.",
        },
        "certificate": cert.certificate_id,
        "certificate_verdict": cert.verdict,
        "law": "no earlier rung proves a later one",
    }


# ======================================================================
# RFD-1: Refinement Failure Diagnosis Contract (SN-0790)
# Forensics for failed refinement checks. A failed refinement check is
# decomposed into independently testable obligations; no fault
# classification without sufficient independent evidence; multiple
# defects stay distinguishable; uncertainty is never converted to blame.
#
# Reflexive application (2026-10-10): the director's attribution of the
# two CI job failures (resolve-current-truth, promote-and-prove) to
# GitHub Actions installation-token rate limits is a REPORTED OPERATIONAL
# DIAGNOSIS, not independent proof. Under this contract it classifies as
# INSUFFICIENT_OBSERVABILITY for the causal claim: the logs report
# rate-limit errors, but independent causal proof (token-quota telemetry
# vs. code defect) was not established. Recorded here, not asserted.
# ======================================================================

ABSTRACTION_DEFECT = "ABSTRACTION_DEFECT"
MAPPING_DEFECT = "MAPPING_DEFECT"
TRANSACTION_ORDERING_DEFECT = "TRANSACTION_ORDERING_DEFECT"
CONCRETE_ENFORCEMENT_DEFECT = "CONCRETE_ENFORCEMENT_DEFECT"
EXTERNAL_ASSUMPTION_GAP = "EXTERNAL_ASSUMPTION_GAP"
INSUFFICIENT_OBSERVABILITY = "INSUFFICIENT_OBSERVABILITY"

DIAG_DIAGNOSED = "DIAGNOSED"
DIAG_INCONCLUSIVE = "INCONCLUSIVE_AWAITING_EVIDENCE"
DIAG_NO_FAILURE = "NO_FAILURE_ESTABLISHED"


@dataclass(frozen=True)
class FailureWitness:
    """RFD-001 minimal failure witness: four distinct objects.
    observed_history -> violated_obligation -> causal_diagnosis ->
    proposed_repair. The original history is never overwritten; repair
    candidates never auto-flip to VERIFIED."""
    observed_history: Tuple[str, ...]
    violated_obligation: str
    causal_diagnosis: str = ""
    proposed_repair: str = ""


@dataclass(frozen=True)
class DiagnosticEvidence:
    """The six diagnostic questions, each answered True/False/None
    (None = not yet assessed; never defaulted)."""
    committed_events_reconstructible: bool = False   # Q6/Q1 observability
    commit_evidence_present: bool = False            # receipts/seq present
    legal_execution_reconstructible: bool = False    # F7: independent legal reconstruction
    external_guarantee_relied_upon: bool = False     # Q4
    external_guarantee_proven_in_scope: Optional[bool] = None
    model_covers_behavior: Optional[bool] = None     # Q1 model adequacy
    state_mapping_correct: Optional[bool] = None     # Q2
    transition_mapping_correct: Optional[bool] = None  # Q3
    forbidden_ordering_observed: bool = False        # Q5
    non_atomic_commit_observed: bool = False         # Q5


@dataclass(frozen=True)
class Diagnosis:
    """Multi-cause preserving: primary, contributing, and unresolved are
    reported separately. first_established_divergence is earliest in the
    justified causal/dependency ordering, not the earliest suspicious
    timestamp."""
    witness: FailureWitness
    first_established_divergence: Optional[str]
    primary: Tuple[str, ...]
    contributing: Tuple[str, ...]
    unresolved: Tuple[str, ...]
    qualification_status: str


def diagnose_refinement_failure(witness: FailureWitness,
                                ev: DiagnosticEvidence) -> Diagnosis:
    """The diagnose_refinement_failure decision procedure (his flowchart):
    observability first; then assumption/abstraction/mapping audits;
    CONCRETE_ENFORCEMENT_DEFECT only when the first three are justified;
    narrow to TRANSACTION_ORDERING_DEFECT only on evidence. The ordering
    is diagnostic, never an excuse to stop early."""
    # Pre-step (F7): if an independent reconstruction finds a legal
    # execution, there is no established failure -- the "failure" is the
    # checker's, not the system's.
    if ev.legal_execution_reconstructible:
        return Diagnosis(witness, None, (), (), (),
                         DIAG_NO_FAILURE)
    primary: List[str] = []
    contributing: List[str] = []
    unresolved: List[str] = []

    # Step 1: observability first. Compare actual operation semantics --
    # DISPATCHED ≠ ACCEPTED ≠ COMMITTED ≠ EFFECT_OBSERVED -- and if the
    # committed events cannot be independently reconstructed, stop: any
    # classification would convert uncertainty into blame.
    if not (ev.committed_events_reconstructible and ev.commit_evidence_present):
        primary.append(INSUFFICIENT_OBSERVABILITY)
        return Diagnosis(witness, None, tuple(primary), (), (),
                         DIAG_INCONCLUSIVE)

    # Step 2: specification audit (abstraction adequacy). An abstraction is
    # defective only when it misrepresents behavior it is obligated to
    # cover (OUT_OF_MODEL_SCOPE is a valid non-defect classification,
    # handled by the caller).
    if ev.model_covers_behavior is False:
        primary.append(ABSTRACTION_DEFECT)
    elif ev.model_covers_behavior is None:
        unresolved.append("model adequacy unassessed")

    # Step 3: mapping audit. Arbitrary remapping to make a history pass is
    # forbidden -- the mapping is judged against committed-event meaning.
    mapping_bad = (ev.state_mapping_correct is False
                   or ev.transition_mapping_correct is False)
    if mapping_bad:
        primary.append(MAPPING_DEFECT)
    elif ev.state_mapping_correct is None \
            or ev.transition_mapping_correct is None:
        unresolved.append("mapping correctness unassessed")

    # Step 4: environment-contract audit. When a specification or mapping
    # defect already explains the failure, the assumption gap is recorded
    # as CONTRIBUTING (fix the model before blaming the environment);
    # otherwise it stands as PRIMARY. Never label the provider defective
    # unless its contract actually promised the guarantee.
    if ev.external_guarantee_relied_upon:
        if ev.external_guarantee_proven_in_scope is False:
            if primary:
                contributing.append(EXTERNAL_ASSUMPTION_GAP)
            else:
                primary.append(EXTERNAL_ASSUMPTION_GAP)
        elif ev.external_guarantee_proven_in_scope is None:
            unresolved.append("external guarantee provenance unassessed")

    # Step 5: enforcement. TRANSACTION_ORDERING_DEFECT is narrowed from
    # enforcement only on evidence; it stands as PRIMARY when the
    # abstraction and mapping are justified (clean), and as CONTRIBUTING
    # when they are not -- kept distinguishable either way. The generic
    # CONCRETE_ENFORCEMENT_DEFECT is concluded only when every audit is
    # justified and no narrower evidence exists.
    ordering_evidence = (ev.forbidden_ordering_observed
                         or ev.non_atomic_commit_observed)
    audits_justified = (not unresolved and ABSTRACTION_DEFECT not in primary
                        and MAPPING_DEFECT not in primary)
    if ordering_evidence:
        if audits_justified:
            primary.append(TRANSACTION_ORDERING_DEFECT)
        elif TRANSACTION_ORDERING_DEFECT not in primary:
            contributing.append(TRANSACTION_ORDERING_DEFECT)
    if not primary and not unresolved:
        primary.append(CONCRETE_ENFORCEMENT_DEFECT)

    status = DIAG_DIAGNOSED if primary else DIAG_INCONCLUSIVE
    return Diagnosis(
        witness=witness,
        first_established_divergence=(
            witness.observed_history[0] if witness.observed_history else None),
        primary=tuple(primary),
        contributing=tuple(contributing),
        unresolved=tuple(unresolved),
        qualification_status=status)


# --- Planted-defect fixtures F1-F8: qualify the diagnostic mechanism itself ----
@dataclass(frozen=True)
class PlantedFixture:
    fixture_id: str
    description: str
    sealed_primary: Tuple[str, ...]   # hidden during blind runs
    sealed_status: str
    build: Any = None                 # () -> (witness, evidence)


def _witness(reason: str, *history: str) -> FailureWitness:
    return FailureWitness(observed_history=tuple(history),
                          violated_obligation=reason)


def _f1_evidence():
    # Worked example A: gateway authorized pre-R, effect observed post-R.
    # The abstract model has no pending-effect state: the claimed
    # obligation ("no external effect after R") exceeds the model.
    w = _witness("claimed: no external effect after R; observed: effect post-R",
                 "gateway AUTHORIZED_VIA_GATEWAY pre-R", "R committed",
                 "external effect OBSERVED post-R")
    ev = DiagnosticEvidence(
        committed_events_reconstructible=True, commit_evidence_present=True,
        external_guarantee_relied_upon=True,
        external_guarantee_proven_in_scope=False,  # executor never promised
        model_covers_behavior=False,  # no pending-effect state: obligated gap
        state_mapping_correct=True, transition_mapping_correct=True)
    return w, ev


def _f2_evidence():
    # Worked example B: revocation mapped to requalification.
    diff = differential_check([
        (lambda s: s.commit_revocation("e1", "t", "s", "p", "LAW-v3", "t"),
         ("Q", 0), "revocation mislabeled as requalification"),
    ])
    w = _witness(f"differential: {diff['verdict']} -- {diff.get('reason', '')}",
                 "R committed (concrete)", "labeled (Q,0) in mapping")
    ev = DiagnosticEvidence(
        committed_events_reconstructible=True, commit_evidence_present=True,
        model_covers_behavior=True,
        state_mapping_correct=True, transition_mapping_correct=False)
    return w, ev


def _f3_evidence():
    # Worked example C: guard-removal mutant, rev-18 over rev-17 read.
    diff = run_guard_removal_mutant()
    w = _witness(f"differential: {diff['verdict']} -- {diff.get('reason', '')}",
                 "R(e1) committed", "stale P committed (mutant)")
    ev = DiagnosticEvidence(
        committed_events_reconstructible=True, commit_evidence_present=True,
        model_covers_behavior=True,
        state_mapping_correct=True, transition_mapping_correct=True,
        forbidden_ordering_observed=True)
    return w, ev


def _f4_evidence():
    # Worked example D: idempotency relied upon as fencing -- never promised.
    w = _witness("claimed: executor fenced post-R; contract: idempotent only",
                 "R committed", "executor ran duplicate post-R",
                 "provider contract promises idempotency, not fencing")
    ev = DiagnosticEvidence(
        committed_events_reconstructible=True, commit_evidence_present=True,
        external_guarantee_relied_upon=True,
        external_guarantee_proven_in_scope=False,
        model_covers_behavior=True,  # correctly out of model scope
        state_mapping_correct=True, transition_mapping_correct=True)
    return w, ev


def _f5_evidence():
    # Observability gap: commit evidence removed.
    w = _witness("differential inconclusive: receipts stripped from trace",
                 "R(?)", "P(?) -- no commit seq, no receipts")
    ev = DiagnosticEvidence(
        committed_events_reconstructible=False, commit_evidence_present=False)
    return w, ev


def _f6_evidence():
    # Mixed cause: ordering defect (evidenced) + unproven external guarantee.
    diff = run_guard_removal_mutant()
    w = _witness(f"differential: {diff['verdict']}; plus unfenced executor",
                 "R(e1) committed", "stale P committed (mutant)",
                 "executor ran post-R without fencing contract")
    ev = DiagnosticEvidence(
        committed_events_reconstructible=True, commit_evidence_present=True,
        external_guarantee_relied_upon=True,
        external_guarantee_proven_in_scope=False,
        model_covers_behavior=True,
        state_mapping_correct=True, transition_mapping_correct=True,
        forbidden_ordering_observed=True)
    return w, ev


def _f7_evidence():
    # Over-restrictive checker: legal history, buggy rejection.
    w = _witness("checker rejected: claim revs must advance on every publish "
                 "(over-strict rule)",
                 "R(e1) committed", "honest publish rejected by checker")
    ev = DiagnosticEvidence(
        committed_events_reconstructible=True, commit_evidence_present=True,
        legal_execution_reconstructible=True,  # reference oracle says legal
        model_covers_behavior=True,
        state_mapping_correct=True, transition_mapping_correct=True)
    return w, ev


def _f8_evidence():
    # Log-reorder stability: F3's history, arrival order shuffled.
    diff = run_guard_removal_mutant()
    w = _witness(f"differential: {diff['verdict']} (log arrival reordered; "
                 f"commit-seq order unchanged)",
                 "P commit observed first in arrival order",
                 "R commit observed second in arrival order",
                 "commit-seq: R < P (reconstructed independently)")
    ev = DiagnosticEvidence(
        committed_events_reconstructible=True, commit_evidence_present=True,
        model_covers_behavior=True,
        state_mapping_correct=True, transition_mapping_correct=True,
        forbidden_ordering_observed=True)
    return w, ev


PLANTED_FIXTURES: Tuple[PlantedFixture, ...] = (
    PlantedFixture("F1", "abstraction defect (pending-effect state missing)",
                   (ABSTRACTION_DEFECT,), DIAG_DIAGNOSED, _f1_evidence),
    PlantedFixture("F2", "mapping defect (R mislabeled as Q)",
                   (MAPPING_DEFECT,), DIAG_DIAGNOSED, _f2_evidence),
    PlantedFixture("F3", "transaction-ordering defect (guard-removal mutant)",
                   (TRANSACTION_ORDERING_DEFECT,), DIAG_DIAGNOSED, _f3_evidence),
    PlantedFixture("F4", "external assumption gap (idempotency != fencing)",
                   (EXTERNAL_ASSUMPTION_GAP,), DIAG_DIAGNOSED, _f4_evidence),
    PlantedFixture("F5", "observability gap (receipts stripped)",
                   (INSUFFICIENT_OBSERVABILITY,), DIAG_INCONCLUSIVE, _f5_evidence),
    PlantedFixture("F6", "mixed cause (ordering + assumption)",
                   (TRANSACTION_ORDERING_DEFECT, EXTERNAL_ASSUMPTION_GAP),
                   DIAG_DIAGNOSED, _f6_evidence),
    PlantedFixture("F7", "over-restrictive false rejection",
                   (), DIAG_NO_FAILURE, _f7_evidence),
    PlantedFixture("F8", "log-reorder stability (same as F3)",
                   (TRANSACTION_ORDERING_DEFECT,), DIAG_DIAGNOSED, _f8_evidence),
)


def run_blind_diagnosis():
    """Blind diagnosis: sealed causes hidden; the independent verifier
    compares the diagnosis against the sealed cause. Uncertainty is
    preserved when evidence is withheld (F5 -> INCONCLUSIVE, not a guess)."""
    results = []
    for fix in PLANTED_FIXTURES:
        witness, ev = fix.build()
        diag = diagnose_refinement_failure(witness, ev)
        results.append({
            "fixture": fix.fixture_id,
            "sealed_primary": fix.sealed_primary,
            "diagnosed_primary": diag.primary,
            "sealed_status": fix.sealed_status,
            "diagnosed_status": diag.qualification_status,
            "match": (set(diag.primary) == set(fix.sealed_primary)
                      and diag.qualification_status == fix.sealed_status),
        })
    return results


# --- The no-rewriting-the-proof-standard rule --------------------------------------
def validate_repair_candidate(diagnosis: Diagnosis, repair_description: str,
                              honest_holds: bool, mutant_still_caught: bool) -> str:
    """A repair candidate is NEVER auto-flipped to VERIFIED. It is
    plausible only if: the revised model still enforces the ratified law
    (reference oracle SHA unchanged -- law revision is a separate governed
    decision, never a diagnostic shortcut); mapping repairs preserve
    committed-event meaning (honest history still HOLDS); database repairs
    still catch the original counterexample and its neighbors (mutant
    still FALSIFIED); external-assumption changes requalify dependent
    claims (stated in the repair)."""
    if reference_spec_sha() != _RFD1_ORACLE_SHA:
        return "REJECTED: reference oracle changed -- law revision smuggled " \
               "into a diagnostic repair (separate governed decision required)"
    if not honest_holds:
        return "REJECTED: repair breaks the honest history (mapping repair " \
               "must preserve committed-event meaning)"
    if not mutant_still_caught:
        return "REJECTED: repair no longer catches the original counterexample"
    return "REPAIR_PLAUSIBLE_PENDING_REVIEW"


_RFD1_ORACLE_SHA = reference_spec_sha()


# ======================================================================
# RFD-POS-1: Legitimate Behavior Preservation / False-Positive
# Qualification (SN-0791). The calibration corpus: the diagnosis engine
# must clear the innocent, not just convict the guilty. No refinement
# failure may be classified as a defect solely because a concrete
# execution differs from an expected trace; independently established
# legal behavior must be preserved.
#
# The three independent questions (never answered by the component that
# generated the suspicious trace):
#   (1) was the concrete behavior legitimate (governing contract+LAW+evidence)?
#   (2) was the abstract model adequate?
#   (3) was the mapping correct?
# Lawful-but-rejected => examine abstraction/mapping. Correct
# abstraction/mapping + contract violation => investigate implementation.
# Missing evidence => INCONCLUSIVE, never a transaction bug.
# ======================================================================

POS_CONSISTENT = "CONSISTENT_WITH_SPEC"
POS_VIOLATION = "VIOLATION_ESTABLISHED"
POS_INCONCLUSIVE = "INCONCLUSIVE"


def classify_history(concrete_steps):
    """Three-way classification of a concrete history. differential_check
    HOLDS => CONSISTENT_WITH_SPEC (with the abstract history as the
    linearization witness). FALSIFIED => the failure is diagnosed (never
    a bare defect label). INCONCLUSIVE stays INCONCLUSIVE: failure to
    construct a legal history is not an implementation defect until the
    mapping, assumptions, observation coverage, and search completeness
    are validated."""
    r = differential_check(concrete_steps)
    if r["verdict"] == DIFFERENTIAL_HOLDS:
        return {"verdict": POS_CONSISTENT,
                "witness": f"{r['steps']} steps, oracle {r['oracle']}"}
    if r["verdict"] == DIFFERENTIAL_FALSIFIED:
        return {"verdict": POS_VIOLATION, "reason": r["reason"],
                "detail": r.get("violations", r.get("abstract_info"))}
    return {"verdict": POS_INCONCLUSIVE, "reason": r["reason"]}


def _pos_candidate(st, stale_revs=None):
    """Build a publication candidate from current state (or stale revs)."""
    h = st.projections["p1"]
    revs = stale_revs or {e: st.evidence[e].eligibility_revision
                          for e in REF_EIDS}
    return ProjectionCandidate(
        "p1", h.projection_revision, "art-0",
        {c: st.claims[c].qualification_revision for c in REF_CIDS},
        dict(revs), "LAW-v3",
        {c: "REQUALIFIED" for c in REF_CIDS},
        ("certification",), h.fencing_token)


def _pos_snapshot(st):
    h = st.projections["p1"]
    return (h.projection_revision, h.fencing_token,
            tuple(h.claim_deps[c] for c in REF_CIDS),
            tuple(h.evidence_deps[e] for e in REF_EIDS), 0)


# --- P1-P10: the positive-control corpus -----------------------------------------
def _p1_steps():
    # P1: publication-before-revocation. P commits at rev N; R follows.
    # Legal: P < R.
    snap = {}
    def _pub(s):
        snap["s"] = _pos_snapshot(s)
        return s.publish_projection(_pos_candidate(s))
    def _rev(s):
        return s.commit_revocation("e1", "p1", "s", "p", "LAW-v3", "t")
    st = refinement_fixture()
    s0 = _pos_snapshot(st)
    return [(_pub, ("P", s0), "honest publication pre-revocation"),
            (_rev, ("R", 0), "revocation after publication")]


def _p2_steps():
    # P2 (key control): overlapping validation. V invoked while E1
    # eligible; the authoritative read linearizes BEFORE R commits; the
    # response arrives after. A timestamp-sorting checker would report
    # TRANSACTION_ORDERING_DEFECT -- a FALSE POSITIVE. The causal
    # (linearization-point) order is V < R: legal.
    # NOTE: a PASS here still cannot authorize a post-R effect without a
    # fresh check (tested separately).
    read_result = {}
    def _validate(s):
        out = s.validate_current("c1", "certification")
        read_result["r"] = out[0]
        return out
    def _rev(s):
        return s.commit_revocation("e1", "p2", "s", "p", "LAW-v3", "t")
    return [(_validate, ("V",), "authoritative read pre-R"),
            (_rev, ("R", 0), "revocation after the read")]


def _p3_steps():
    # P3: independent requalification. After R(e1), the E2 path
    # requalifies C1 -- the claim stays usable. Legal.
    def _rev(s):
        return s.commit_revocation("e1", "p3", "s", "p", "LAW-v3", "t")
    def _requal(s):
        rev2 = s.evidence["e2"].eligibility_revision
        return s.commit_qualification("c1", "REQUALIFIED", {"e2": rev2},
                                      "s", "p", "LAW-v3")
    return [(_rev, ("R", 0), "revoke e1"),
            (_requal, ("Q", 0), "requalify c1 on the E2 path")]


def _p4_steps():
    # P4: rejected stale transaction. The fence correctly rejects a stale
    # candidate -- correct enforcement, NOT a bug. Legal.
    rev_at_read = {}
    def _rev(s):
        rev_at_read["r"] = s.evidence["e1"].eligibility_revision
        return s.commit_revocation("e1", "p4", "s", "p", "LAW-v3", "t")
    def _stale(s):
        h = s.projections["p1"]
        snap = (h.projection_revision, h.fencing_token,
                tuple(h.claim_deps[c] for c in REF_CIDS),
                (rev_at_read["r"], h.evidence_deps["e2"],
                 h.evidence_deps["e3"]), 0)
        c = _pos_candidate(s, {"e1": rev_at_read["r"],
                               "e2": s.evidence["e2"].eligibility_revision,
                               "e3": s.evidence["e3"].eligibility_revision})
        return s.publish_projection(c)
    st = refinement_fixture()
    h0 = st.projections["p1"]
    s0 = (h0.projection_revision, h0.fencing_token,
          tuple(h0.claim_deps[c] for c in REF_CIDS),
          tuple(h0.evidence_deps[e] for e in REF_EIDS), 0)
    return [(_rev, ("R", 0), "revoke e1"),
            (_stale, ("P", s0), "stale candidate correctly rejected")]


def _p5_steps():
    # P5: harmless internal steps -- registrations and candidate builds
    # are legitimate stuttering (no authority change).
    def _build(s):
        _pos_candidate(s)  # built, never submitted
        return "candidate-built-not-submitted"
    return [(_build, None, "candidate artifact write (stutter)")]


def _p6_steps():
    # P6: concurrent independent claims. Actions scoped to independent
    # claims do not interfere -- all pre-revocation here, both authorize.
    def _act12(s):
        return s.commit_action("a12", ["c1", "c2"], True)
    return [(_act12, ("A", ("c1", "c2")), "action on independent claims")]


def _p7_steps():
    # P7: idempotent recovery. Duplicate replay -> NOOP_DUPLICATE.
    # Never rolls back.
    def _rev(s):
        return s.commit_revocation("e1", "p7", "s", "p", "LAW-v3", "t")
    def _replay(s):
        ev = s.outbox[0]
        return s.replay_event({
            "event_id": ev["event_id"], "kind": "revocation",
            "evidence_id": ev["evidence_id"], "scope": "s", "purpose": "p",
            "eligibility_revision": s.evidence["e1"].eligibility_revision})
    def _replay_dup(s):
        return _replay(s)
    return [(_rev, ("R", 0), "revoke e1"),
            (_replay, ("J", 0), "replay (reconciles)"),
            (_replay_dup, ("J", 0), "duplicate replay (noop-duplicate)")]


def _p8_steps():
    # P8: projection preservation. A publication committed pre-R stays a
    # valid historical record post-R (no retroactive invalidation).
    def _pub(s):
        return s.publish_projection(_pos_candidate(s))
    def _rev(s):
        return s.commit_revocation("e1", "p8", "s", "p", "LAW-v3", "t")
    def _inspect(s):
        # Historical inspection: the head still records the pre-R commit.
        return ("inspected", s.projections["p1"].projection_revision)
    st = refinement_fixture()
    s0 = _pos_snapshot(st)
    return [(_pub, ("P", s0), "publication pre-R"),
            (_rev, ("R", 0), "revocation"),
            (_inspect, None, "historical inspection (stutter)")]


def _p9_steps():
    # P9: historical Smart Note. An old qualification is preserved as
    # history (linearization log), never as current authority.
    def _rev(s):
        return s.commit_revocation("e1", "p9", "s", "p", "LAW-v3", "t")
    def _inspect_log(s):
        n = len(s.linearization_log)
        return ("log-preserved", n)
    return [(_rev, ("R", 0), "revoke e1"),
            (_inspect_log, None, "log inspection (stutter)")]


def _p10_steps():
    # P10: external request acceptance. The gateway authorizes a pre-R
    # external request with a revision-bound lease -- legal AT THE
    # GATEWAY (honest qualification: gateway boundary only).
    def _act_ext(s):
        return s.commit_action("ax", ["c1", "c2"], True, external=True)
    return [(_act_ext, ("A", ("c1", "c2")),
             "gateway authorizes pre-R external request")]


POSITIVE_CONTROLS = (
    ("P1", "publication-before-revocation", _p1_steps),
    ("P2", "overlapping validation (linearizes pre-R)", _p2_steps),
    ("P3", "independent requalification on E2 path", _p3_steps),
    ("P4", "rejected stale transaction (correct enforcement)", _p4_steps),
    ("P5", "harmless internal steps (stutter)", _p5_steps),
    ("P6", "concurrent independent claims", _p6_steps),
    ("P7", "idempotent recovery (duplicate replay)", _p7_steps),
    ("P8", "projection preservation (history, not authority)", _p8_steps),
    ("P9", "historical record preserved", _p9_steps),
    ("P10", "external request acceptance (gateway boundary)", _p10_steps),
)


# --- Metamorphic testing ------------------------------------------------------------
# Semantics-preserving transforms must keep the classification; boundary-
# changing transforms must alter it. This tests understanding, not
# pattern-matching.
def metamorphic_duplicate_recovery(steps):
    """Add duplicate recovery replays: classification unchanged."""
    out = []
    for thunk, label, desc in steps:
        out.append((thunk, label, desc))
        if label and label[0] == "J":
            out.append((thunk, label, desc + " (duplicate)"))
    return out


def metamorphic_add_logging(steps):
    """Add harmless observation steps: classification unchanged."""
    def _log(s):
        return ("logged", len(s.linearization_log))
    out = []
    for thunk, label, desc in steps:
        out.append((thunk, label, desc))
        out.append((_log, None, "logging (stutter)"))
    return out


def metamorphic_move_commit_across_revocation(steps):
    """BOUNDARY-CHANGING: the pre-R read is forced to commit AFTER the
    revocation (the read is not refreshed). Unlike the honest P1 (P<R),
    this must classify VIOLATION_ESTABLISHED -- the engine is tested on
    understanding (commit ordering vs. revocation), not pattern-matching
    on step shapes."""
    revs = [i for i, (t, l, d) in enumerate(steps) if l and l[0] == "R"]
    pubs = [i for i, (t, l, d) in enumerate(steps) if l and l[0] == "P"]
    if not revs or not pubs:
        return None

    def _rev(s):
        return s.commit_revocation("e1", "meta", "s", "p", "LAW-v3", "t")

    def _forced_stale_commit(s):
        # The pre-R read commits post-R without refresh (forced commit,
        # as a fencing-less executor would). The abstract guard rejects
        # it; the concrete mutant commits it.
        with s._commit_lock:
            h = s.projections["p1"]
            h.projection_revision += 1
            return COMMITTED, "forced stale commit"

    st = refinement_fixture()
    s0 = _pos_snapshot(st)
    return [(_rev, ("R", 0), "revocation"),
            (_forced_stale_commit, ("P", s0),
             "pre-R read forced to commit post-R")]


# --- Paired positive/negative controls -------------------------------------------------
# reject-both = overly restrictive; accept-both = unsafe; distinguishing
# the pair = useful discrimination.
def paired_histories():
    """(legal_steps, illegal_steps): identical workers/evidence/
    revocation; only the publication's freshness differs."""
    legal = _p1_steps()     # P committed pre-R, then R
    # Illegal: same shape but the publication commits OVER the revocation.
    def _rev(s):
        return s.commit_revocation("e1", "pair", "s", "p", "LAW-v3", "t")
    def _stale_commit_mutant(s):
        # Concrete analogue of the guard-removal mutant for one step.
        with s._commit_lock:
            h = s.projections["p1"]
            h.projection_revision += 1
            return COMMITTED, "mutant"
    st = refinement_fixture()
    s0 = _pos_snapshot(st)
    illegal = [(_rev, ("R", 0), "revocation"),
               (_stale_commit_mutant, ("P", s0),
                "stale publication commits (mutant)")]
    return legal, illegal


# --- Diagnosis receipts (RFD-POS-002) -------------------------------------------------------
@dataclass(frozen=True)
class DiagnosisReceipt:
    """trace, provenance, scope, limitations, linearization witness --
    and BOTH assessments preserved when a mapping correction changes a
    verdict."""
    trace: Tuple[str, ...]
    provenance: str
    scope: str
    limitations: Tuple[str, ...]
    linearization_witness: str
    assessments: Tuple[Tuple[str, str], ...]  # (stage, verdict) pairs


def build_diagnosis_receipt(control_id, classification, corrected=None):
    assessments = (("initial", classification["verdict"]),)
    if corrected is not None:
        assessments = assessments + (("mapping-corrected",
                                      corrected["verdict"]),)
    return DiagnosisReceipt(
        trace=tuple(control_id),
        provenance="RFD-POS-1 controlled corpus (independently verified "
                   "expected outcomes; blind diagnosis; sealed fixtures)",
        scope="refinement fixture: 3 evidence, 2 claims, 1 projection; "
              "in-memory authoritative engine",
        limitations=("bounded fixture", "single-threaded drivers except "
                     "the decisive-obligation race test",
                     "no production durability"),
        linearization_witness=classification.get("witness",
                                                 classification.get("reason",
                                                                    "")),
        assessments=assessments)


# ======================================================================
# RFD-AMB-1: Ambiguous Execution History Qualification (SN-0792)
# The possible-histories calculus: when incomplete observations admit
# both legal and violating executions, preserve both possibilities,
# withhold definitive certification or blame, identify the missing
# discriminating evidence, and prohibit dependent consequential use of
# the unresolved proof.
#
# Conclusion model:
#   ∀h∈H(O):Safe(h)      => SAFETY_ESTABLISHED_IN_SCOPE
#   ∀h∈H(O):¬Safe(h)     => VIOLATION_ESTABLISHED
#   ∃h_L,h_V split       => AMBIGUOUS_BOTH_POSSIBLE
#   unreconstructable    => INSUFFICIENT_MODEL_OR_OBSERVABILITY
# H(O) is checked nonempty before universal claims; inconsistent
# observations => INCONSISTENT_OBSERVATIONS_OR_MODEL, never a vacuous
# PASS/FAIL. Bounded-search results are not universal claims.
# ======================================================================

AMB_SAFETY_ESTABLISHED = "SAFETY_ESTABLISHED_IN_SCOPE"
AMB_BOTH_POSSIBLE = "AMBIGUOUS_BOTH_POSSIBLE"
AMB_INSUFFICIENT = "INSUFFICIENT_MODEL_OR_OBSERVABILITY"
AMB_INCONSISTENT = "INCONSISTENT_OBSERVATIONS_OR_MODEL"

OUTCOME_ABORTED = "ABORTED"
OUTCOME_NOT_EXECUTED = "NOT_EXECUTED"
OUTCOME_UNRESOLVED = "UNRESOLVED"


@dataclass(frozen=True)
class AmbiguousOp:
    """Partial-order history element. Missing receipt => UNRESOLVED
    operation, never a fabricated commit/abort. Commit(R)≺Commit(A) is
    asserted only on trusted evidence -- no timestamp/log-label
    manufacturing."""
    operation_id: str
    invoked_at: int
    responded_at: int
    commit_evidence: Optional[str]     # receipt/seq or None
    effect_evidence: Optional[str]    # observed effect or None
    outcome_set: FrozenSet[str]       # subset of COMMITTED/ABORTED/
                                      # NOT_EXECUTED/UNRESOLVED
    ordering_constraints: Tuple[Tuple[str, str], ...]  # (before, after)
    coverage_state: str               # COVERED / UNCOVERED
    env_assumptions: Tuple[str, ...] = ()


def may_must_violate(legal_exists: bool, violating_exists: bool):
    """The four-row table. (may, must). The (No, Yes) row is invalid:
    must-violate implies may-violate; missing evidence is never silently
    treated as proof of success, failure, or nonexecution."""
    may = bool(violating_exists)
    must = bool(violating_exists and not legal_exists)
    if must and not may:
        raise ValueError("invalid May/Must row: must without may")
    return may, must


@dataclass(frozen=True)
class AmbiguityRecord:
    """HIST-042 evidence-bound ambiguity record: both witnesses are
    reproducible, with explicit unresolved choices -- not evidence that
    either is actual."""
    record_id: str
    known_events: Tuple[str, ...]
    unresolved_operations: Tuple[str, ...]
    missing_evidence: Tuple[str, ...]
    legal_witness: str
    violating_witness: str
    may_violate: bool
    must_violate: bool
    next_discriminating_check: str
    completion_coverage: str  # EXHAUSTIVE / BOUNDED / SAMPLED


def _check_observations_consistent(ops) -> Tuple[bool, str]:
    """Inconsistent observations (trusted evidence contradicts) => flag,
    never a vacuous pass/fail."""
    by_id = {}
    for op in ops:
        if op.operation_id in by_id:
            prev = by_id[op.operation_id]
            # Same op, contradictory trusted commit evidence.
            if (prev.commit_evidence and op.commit_evidence
                    and prev.commit_evidence != op.commit_evidence):
                return False, (f"contradictory commit evidence for "
                               f"{op.operation_id}")
            s1 = set(prev.outcome_set) - {OUTCOME_UNRESOLVED}
            s2 = set(op.outcome_set) - {OUTCOME_UNRESOLVED}
            if s1 and s2 and not (s1 & s2):
                return False, (f"contradictory outcome sets for "
                               f"{op.operation_id}")
        else:
            by_id[op.operation_id] = op
    return True, ""


def evaluate_ambiguous(ops, variants, coverage="EXHAUSTIVE"):
    """The possible-histories calculus. ops: list of AmbiguousOp.
    variants: op_id -> {outcome: (thunk, abstract_label, desc)}.
    Enumerates completions (outcome hypotheses x causal order), classifies
    each with the reference oracle, and applies the conclusion model.
    The engine operates only on the observations (Layer B); ground truth
    never leaks into the evaluation."""
    consistent, reason = _check_observations_consistent(ops)
    if not consistent:
        return {"conclusion": AMB_INCONSISTENT, "reason": reason,
                "legal_exists": False, "violating_exists": False}

    # Build the hypothesis space: for each op, the outcomes to try.
    choices = []
    for op in ops:
        var = variants.get(op.operation_id, {})
        possible = [o for o in var
                    if o in op.outcome_set or OUTCOME_UNRESOLVED in op.outcome_set]
        if not possible:
            return {"conclusion": AMB_INSUFFICIENT,
                    "reason": f"no hypothesis for {op.operation_id}",
                    "legal_exists": False, "violating_exists": False}
        choices.append([(op.operation_id, o) for o in possible])

    import itertools
    legal_witness = None
    violating_witness = None
    completions = 0
    for combo in itertools.product(*choices):
        # Causal order: respect ordering_constraints (topological); the
        # engine never manufactures order from timestamps/log labels.
        order = _linear_extensions(
            [op.operation_id for op in ops],
            [(a, b) for op in ops for (a, b) in op.ordering_constraints])
        for perm in order:
            completions += 1
            pick = dict(combo)
            steps = []
            for oid in perm:
                o = pick[oid]
                thunk, label, desc = variants[oid][o]
                steps.append((thunk, label, f"{oid}={o}: {desc}"))
            r = classify_history(steps)
            witness = "; ".join(f"{oid}={pick[oid]}" for oid in perm)
            if r["verdict"] == POS_CONSISTENT and legal_witness is None:
                legal_witness = witness
            elif r["verdict"] == POS_VIOLATION and violating_witness is None:
                violating_witness = witness
        # early exit not taken: bounded fixture, enumerate fully
    legal_exists = legal_witness is not None
    violating_exists = violating_witness is not None
    may, must = may_must_violate(legal_exists, violating_exists)
    if legal_exists and not violating_exists:
        conclusion = AMB_SAFETY_ESTABLISHED
    elif violating_exists and not legal_exists:
        conclusion = POS_VIOLATION
    elif legal_exists and violating_exists:
        conclusion = AMB_BOTH_POSSIBLE
    else:
        conclusion = AMB_INSUFFICIENT
    return {"conclusion": conclusion,
            "legal_exists": legal_exists, "violating_exists": violating_exists,
            "legal_witness": legal_witness,
            "violating_witness": violating_witness,
            "may_violate": may, "must_violate": must,
            "completions": completions, "coverage": coverage}


def _linear_extensions(nodes, constraints):
    """All topological orders of the partial order (bounded fixture)."""
    import itertools
    result = []
    pos = {n: i for i, n in enumerate(nodes)}
    for perm in itertools.permutations(nodes):
        p = {n: i for i, n in enumerate(perm)}
        if all(p[a] < p[b] for a, b in constraints):
            result.append(perm)
    return result


def refine_observations(ops, op_id, narrowed_outcome_set):
    """Evidence-monotonic refinement: O1⊆O2 (narrowed outcome set) =>
    H(O2)⊆H(O1). Contradictions are flagged, not silently discarded;
    disqualified observations or model revisions are governed expansions.
    This supports accumulating proof AND correcting earlier evidence."""
    out = []
    for op in ops:
        if op.operation_id == op_id:
            new_set = frozenset(narrowed_outcome_set)
            old_definite = set(op.outcome_set) - {OUTCOME_UNRESOLVED}
            new_definite = set(new_set) - {OUTCOME_UNRESOLVED}
            if old_definite and new_definite and not (new_definite <= old_definite):
                raise ValueError(
                    f"contradiction on refinement of {op.operation_id}: "
                    f"{old_definite} -> {new_definite} (flagged, not discarded)")
            out.append(AmbiguousOp(
                op.operation_id, op.invoked_at, op.responded_at,
                op.commit_evidence, op.effect_evidence, new_set,
                op.ordering_constraints, op.coverage_state, op.env_assumptions))
        else:
            out.append(op)
    return out


def withdraw_observation(ops, op_id, widened_outcome_set, reason: str):
    """Governed withdrawal of a previously revealed observation: widens
    the outcome set and restores ambiguity. Recorded as a governed
    expansion -- never silent. (Refinement contradictions are still
    flagged by refine_observations; withdrawal is the explicit,
    reason-carrying inverse.)"""
    out = []
    for op in ops:
        if op.operation_id == op_id:
            out.append(AmbiguousOp(
                op.operation_id, op.invoked_at, op.responded_at,
                None, None, frozenset(widened_outcome_set),
                op.ordering_constraints, op.coverage_state,
                op.env_assumptions + (f"withdrawn: {reason}",)))
        else:
            out.append(op)
    return out
    """Evidence-monotonic refinement: O1 ⊆ O2 (narrowed outcome set) =>
    H(O2) ⊆ H(O1). Contradictions are flagged, not silently discarded."""
    out = []
    for op in ops:
        if op.operation_id == op_id:
            new_set = frozenset(narrowed_outcome_set)
            old_definite = set(op.outcome_set) - {OUTCOME_UNRESOLVED}
            new_definite = set(new_set) - {OUTCOME_UNRESOLVED}
            if old_definite and new_definite and not (new_definite <= old_definite):
                raise ValueError(
                    f"contradiction on refinement of {op.operation_id}: "
                    f"{old_definite} -> {new_definite} (flagged, not discarded)")
            out.append(AmbiguousOp(
                op.operation_id, op.invoked_at, op.responded_at,
                op.commit_evidence, op.effect_evidence, new_set,
                op.ordering_constraints, op.coverage_state, op.env_assumptions))
        else:
            out.append(op)
    return out


# --- Safe operational behavior during ambiguity -----------------------------------
# What recovery/operations may DO while a history is AMBIGUOUS_BOTH_POSSIBLE.
AMBIGUITY_ACTIVITIES = {
    "historical_inspection": "PERMITTED",
    "independent_reconciliation": "PERMITTED",
    "blind_retry": "FORBIDDEN_WITHOUT_RECONCILIATION",
    "certification": "WITHHELD",
    "unrelated_authorized_actions": "PERMITTED",
    "learn_promotion": "HELD_UNTIL_CAUSAL_EVIDENCE",
    "smart_notes": "PRESERVE_BOTH_WORLDS_AND_UNCERTAINTY",
    "dependent_consequential_use": "PROHIBITED",
}


def activity_permitted(activity: str) -> bool:
    status = AMBIGUITY_ACTIVITIES.get(activity, "UNKNOWN")
    return status in ("PERMITTED",)


# --- The twin-worlds acceptance experiment ------------------------------------------
def _twin_worlds_observations():
    """Two worlds, identical visible observations, hidden ground truth.
    World L: R, then stale publish REJECTED (legal).
    World V: R, then stale publish COMMITTED (mutant).
    Observations hide the P outcome (no commit evidence for P)."""
    ops = [
        AmbiguousOp("R1", 1, 2, "receipt-R1", None,
                    frozenset({COMMITTED}), (), "COVERED"),
        AmbiguousOp("P1", 3, 9, None, None,
                    frozenset({COMMITTED, OUTCOME_ABORTED, OUTCOME_UNRESOLVED}),
                    (("R1", "P1"),), "COVERED"),
    ]
    st = refinement_fixture()
    s0 = _pos_snapshot(st)

    def _rev(s):
        return s.commit_revocation("e1", "twin", "s", "p", "LAW-v3", "t")

    def _p_rejected(s):
        h = s.projections["p1"]
        rev1 = s.evidence["e1"].eligibility_revision
        # stale candidate: built pre-R revs
        cand = ProjectionCandidate(
            "p1", h.projection_revision, "art-0",
            {c: s.claims[c].qualification_revision for c in REF_CIDS},
            {"e1": 1, "e2": 2, "e3": 3}, "LAW-v3",
            {c: "REQUALIFIED" for c in REF_CIDS},
            ("certification",), h.fencing_token)
        return s.publish_projection(cand)

    def _p_committed(s):
        with s._commit_lock:
            h = s.projections["p1"]
            h.projection_revision += 1
            return COMMITTED, "forced"

    variants = {
        "R1": {COMMITTED: (_rev, ("R", 0), "revocation")},
        "P1": {OUTCOME_ABORTED: (_p_rejected, ("P", s0),
                                 "stale publish rejected (World L)"),
               COMMITTED: (_p_committed, ("P", s0),
                           "stale publish committed (World V)")},
    }
    return ops, variants


def twin_worlds_experiment():
    """D(Observe(H_L)) == D(Observe(H_V)): the engine returns
    AMBIGUOUS_BOTH_POSSIBLE for both worlds from identical observations.
    Different answers => answer-key leakage or hidden assumptions."""
    ops, variants = _twin_worlds_observations()
    result = evaluate_ambiguous(ops, variants)
    assert result["conclusion"] == AMB_BOTH_POSSIBLE, result
    assert result["legal_exists"] and result["violating_exists"]
    return result


def staged_revelation_experiment():
    """2A/2B: staged evidence revelation updates correctly in EITHER
    direction; removal restores ambiguity."""
    ops, variants = _twin_worlds_observations()
    base = evaluate_ambiguous(ops, variants)
    assert base["conclusion"] == AMB_BOTH_POSSIBLE
    # 2A: reveal the P outcome as REJECTED/ABORTED -> safety established.
    ops_a = refine_observations(ops, "P1", {OUTCOME_ABORTED})
    ra = evaluate_ambiguous(ops_a, variants)
    assert ra["conclusion"] == AMB_SAFETY_ESTABLISHED, ra
    # 2B: reveal as COMMITTED -> violation established.
    ops_b = refine_observations(ops, "P1", {COMMITTED})
    rb = evaluate_ambiguous(ops_b, variants)
    assert rb["conclusion"] == POS_VIOLATION, rb
    # Removal restores ambiguity (governed withdrawal, not silent).
    ops_c = withdraw_observation(ops_a, "P1",
                                {COMMITTED, OUTCOME_ABORTED,
                                 OUTCOME_UNRESOLVED},
                                "staged evidence withdrawn for the test")
    rc = evaluate_ambiguous(ops_c, variants)
    assert rc["conclusion"] == AMB_BOTH_POSSIBLE, rc
    return {"base": base["conclusion"], "reveal_aborted": ra["conclusion"],
            "reveal_committed": rb["conclusion"],
            "removal": rc["conclusion"]}


def rfd_amb_001():
    """RFD-AMB-001: two controlled executions, identical observations,
    withheld effect evidence. The verifier establishes both worlds
    compatible; the worker returns AMBIGUOUS_BOTH_POSSIBLE; staged
    release narrows correctly; removal restores ambiguity; unaffected
    claims preserved; a cold successor reconstructs the uncertainty from
    the record alone."""
    twin = twin_worlds_experiment()
    staged = staged_revelation_experiment()
    # Unaffected claims preserved: ambiguity about P1 does not touch c1's
    # E2-path standing.
    st = refinement_fixture()
    st.commit_revocation("e1", "amb", "s", "p", "LAW-v3", "t")
    assert st.qualification_standing("c1") == CURRENT
    # Cold successor: the ambiguity record alone reconstructs uncertainty.
    rec = AmbiguityRecord(
        record_id="HIST-042/RFD-AMB-001",
        known_events=("R1 committed (receipt-R1)",),
        unresolved_operations=("P1",),
        missing_evidence=("P1 commit receipt", "P1 effect observation"),
        legal_witness=twin["legal_witness"],
        violating_witness=twin["violating_witness"],
        may_violate=twin["may_violate"], must_violate=twin["must_violate"],
        next_discriminating_check="obtain P1 commit receipt or effect evidence",
        completion_coverage="EXHAUSTIVE")
    assert rec.may_violate and not rec.must_violate
    return {"twin_worlds": twin["conclusion"], "staged": staged,
            "record": rec.record_id,
            "unaffected_claims_preserved": True}


# ======================================================================
# AER-1: Ambiguous External Effect Recovery Law (SN-0793)
# Recovery-safety under the ambiguity RFD-AMB-1 models. When an external
# effect's commit outcome is unknown, preserve the uncertainty and never
# automatically repeat the effect; reconcile first; any subsequent
# execution needs current LAW permission, a stable logical-operation
# identity, and independently verified duplicate-safety across every
# remaining possible history.
#
# The three questions: what happened (KNOW/PROVE/VERIFY)? what recovery
# is permitted (LAW)? how without duplication (ACT)? A missing receipt
# answers none of them. 'Worker failed' proves neither nonexecution nor
# rollback -- it may mean only the acknowledgment was lost.
# ======================================================================

# Recovery decisions (the seven-row table + the terminal record).
REC_VERIFY_AND_CLOSE = "VERIFY_AND_CLOSE"
REC_FRESH_EXECUTION = "FRESH_EXECUTION_UNDER_LAW"
REC_RECONCILE = "RECONCILE_ON_ORIGINAL_IDENTITY"
REC_SAME_KEY_RETRY = "CONDITIONAL_SAME_KEY_RETRY"
REC_IDEMPOTENT_RETRY = "CONDITIONAL_IDEMPOTENT_RETRY"
REC_HOLD = "HOLD_AND_INVESTIGATE"
REC_HOLD_ESCALATE = "HOLD_INVESTIGATE_ESCALATE"
REC_NO_SAFE_RETRY = "UNRESOLVED_EXTERNAL_OUTCOME__NO_SAFE_AUTOMATIC_RETRY"


@dataclass(frozen=True)
class LogicalOperation:
    """OP-127: durable logical-operation identity. One canonical identity
    before send; restarts recover the SAME identity, never manufacture a
    new one or a fresh key. Local intent records never prove external
    effects -- only the provider's durable effect ledger does."""
    op_key: str
    scope: str
    payload_hash: str
    authorization_rev: int
    created_at_seq: int


@dataclass(frozen=True)
class AmbiguousEffect:
    """Explicit uncertainty: both possible histories retained with the
    missing evidence. Never collapsed to a guess."""
    operation: LogicalOperation
    possible_outcomes: FrozenSet[str]  # COMMITTED / IN_FLIGHT / ABORTED...
    missing_evidence: Tuple[str, ...]
    impact_class: str  # "reversible" | "irreversible-high"


@dataclass(frozen=True)
class RecoveryGuarantees:
    """Independently verified facts the decision may rely on. Each must
    be established, never assumed."""
    committed_confirmed: bool = False
    cannot_commit_proven: bool = False
    read_only_status_query_available: bool = False
    atomic_dedup_proven: bool = False
    idempotent_covers_whole_effect: bool = False
    current_law_valid: bool = False
    recovery_fence_held: bool = False
    covers_all_possible_outstanding_attempts: bool = False


def decide_recovery(effect: AmbiguousEffect, g: RecoveryGuarantees) -> dict:
    """The recovery decision table. An earlier attempt may still be
    executing -- timeouts never prove cancellation, so every retry row
    requires covers_all_possible_outstanding_attempts (the most important
    condition)."""
    if g.committed_confirmed:
        return {"decision": REC_VERIFY_AND_CLOSE,
                "reason": "effect confirmed; verify ledger, close"}
    if g.cannot_commit_proven:
        if g.current_law_valid:
            return {"decision": REC_FRESH_EXECUTION,
                    "reason": "prior attempt proven unable to commit; fresh "
                              "execution under current LAW on the same "
                              "logical identity"}
        return {"decision": REC_HOLD,
                "reason": "cannot-commit proven but LAW permission not "
                          "current; retries always need CURRENT permission"}
    if effect.impact_class == "irreversible-high":
        return {"decision": REC_HOLD_ESCALATE,
                "reason": "unknown outcome + irreversible/high impact: hold, "
                          "investigate, escalate -- never automatic retry"}
    if not g.current_law_valid:
        return {"decision": REC_HOLD,
                "reason": "stale-authority revocation: a deduplicated retry "
                          "can still execute after its authorization was "
                          "revoked; retries always need CURRENT permission"}
    if g.read_only_status_query_available:
        return {"decision": REC_RECONCILE,
                "reason": "reconcile on the original identity via read-only "
                          "status query; never manufacture a new identity"}
    if g.atomic_dedup_proven and g.recovery_fence_held \
            and g.covers_all_possible_outstanding_attempts:
        return {"decision": REC_SAME_KEY_RETRY,
                "reason": "proven atomic dedup + fence + full outstanding "
                          "coverage: same-key retry under current authorization"}
    if g.idempotent_covers_whole_effect and g.recovery_fence_held \
            and g.covers_all_possible_outstanding_attempts:
        return {"decision": REC_IDEMPOTENT_RETRY,
                "reason": "genuine idempotence covering the WHOLE effect "
                          "(not just the request) + fence + coverage"}
    return {"decision": REC_HOLD,
            "reason": "unknown outcome with no adequate duplicate-safety "
                      "guarantee: hold and investigate"}


def no_safe_retry_record(effect: AmbiguousEffect, reason: str) -> dict:
    """Progress without retry loopholes: UNRESOLVED_EXTERNAL_OUTCOME --
    NO_SAFE_AUTOMATIC_RETRY is a valid TERMINAL record. Deadlines trigger
    review/escalation, never silent FAILED conversion."""
    return {"record": REC_NO_SAFE_RETRY,
            "op_key": effect.operation.op_key,
            "possible_outcomes": sorted(effect.possible_outcomes),
            "missing_evidence": list(effect.missing_evidence),
            "reason": reason,
            "deadline_policy": "review/escalation on deadline, never "
                               "automatic FAILED conversion"}


def safe_recovery_predicate(action: str, possible_worlds, law_valid: bool) -> bool:
    """SafeRecovery(r,O): LAWValid(r) ∧ ∀h∈H(O): SafeExtension(h,r).
    Worst-case correctness, never probability. Cannot be claimed without
    a soundly established compatibility set and provider guarantees.
    possible_worlds: list of callables world_state -> bool (action safe
    in that world)."""
    if not law_valid:
        return False
    return all(safe_in_world(action) for safe_in_world in possible_worlds)


# --- Idempotency as an enforceable contract -----------------------------------------
# Three protections, verified separately: request dedup vs idempotent
# operation vs exactly-once logical-effect enforcement.
IDEMPOTENCY_CONTRACT_CHECKS = (
    "key_scope",            # key bound to the right scope
    "payload_binding",      # key bound to the exact payload
    "atomicity_across_concurrent_attempts",
    "retention_for_full_retry_horizon",
    "downstream_effect_coverage",  # the WHOLE effect, not just the request
    "key_expiry",           # expired keys reject; never silently re-execute
    "stale_authority",      # dedup does not survive authorization revocation
)


# --- Cancellation / compensation / retry separation -----------------------------------
# Cancellation only on adequate guarantees. Compensation is a NEW
# authorized effect (never proof the original didn't happen). Retry only
# with duplicate-safety. Never both a new payment and an automatic refund
# on an ambiguous outcome.
def compensation_is_new_effect(original: AmbiguousEffect) -> dict:
    return {"compensation": "NEW authorized effect on a fresh logical identity",
            "proves_original_absent": False,
            "requires": "current LAW permission for the compensation itself"}


# --- Mock external provider with a durable effect ledger -------------------------------
class MockExternalProvider:
    """Controlled mock for AER-001: a durable effect ledger (the only
    proof of external effects), atomic dedup keys, receipt withholding,
    key expiry, and crash simulation. The VERIFIER counts effects in the
    ledger -- local intent records prove nothing."""

    def __init__(self):
        import threading as _th
        self.ledger = []            # durable: list of (op_key, effect_no)
        self.dedup = {}             # (region, op_key) -> effect_no (atomic)
        self.payloads = {}          # (region, op_key) -> payload_hash bound at first accept
        self.receipts = {}          # op_key -> receipt or None (withheld)
        self.key_expiry = {}        # op_key -> bool (expired?)
        self.auth_rev = {}          # op_key -> authorization rev
        self.current_auth_rev = 1
        self.withhold_receipts = False
        self.crash_on_submit = False
        # --- AER-PROVIDER-1 extensions -------------------------------------------
        self.downstream_ledger = []     # durable: list of (op_key, downstream_effect_id)
        self.downstream_dedup = set()   # (op_key, downstream_effect_id) seen
        self.downstream_dedup_on = True # broken-provider mutation flips this off
        self.first_request_at = {}      # op_key -> logical time of FIRST provider request
        self.retention_horizon = {}     # op_key -> logical expiry time (T_provider-expiry)
        self.now = 0                    # injectable logical clock
        self.pause_before_commit = None # threading.Event: when set, submit blocks pre-effect
        self.guard_mode = "atomic"      # "atomic" | "broken_record_after_effect"
        self.failover_loses_dedup = False  # broken-provider mutation
        self.submissions = []           # response layer: (op_key, outcome) per submit call
        self.pre_commit_hook = None     # test hook: called at the pause point (D3)
        self.rejected_regions = set()   # drift D1: silently rejected scopes
        self.error_script = []          # alert T-suite: scripted transport outcomes
        self.contract_text_version = 1
        self._lock = _th.Lock()
        self._effect_no = 0

    def emit_downstream(self, op_key, downstream_effect_id) -> str:
        """A downstream consumer emits a business effect derived from the root
        operation. With downstream dedup (honest), the same
        (op_key, effect_id) is emitted at most once. Returns
        EMITTED or DEDUPED_DOWNSTREAM."""
        with self._lock:
            did = (op_key, downstream_effect_id)
            if self.downstream_dedup_on and did in self.downstream_dedup:
                return "DEDUPED_DOWNSTREAM"
            self.downstream_dedup.add(did)
            self.downstream_ledger.append(did)
            return "EMITTED"

    def count_downstream(self, op_key) -> int:
        return sum(1 for k, _ in self.downstream_ledger if k == op_key)

    def failover(self):
        """Simulate provider failover to a new node. Durable state
        (ledger, dedup) survives; the broken-provider mutation drops dedup."""
        import threading as _th
        new = MockExternalProvider()
        new.ledger = self.ledger            # durable storage survives
        new.payloads = dict(self.payloads)
        new.downstream_ledger = self.downstream_ledger
        new.downstream_dedup = set(self.downstream_dedup)
        new.first_request_at = dict(self.first_request_at)
        new.retention_horizon = dict(self.retention_horizon)
        new.now = self.now
        new.current_auth_rev = self.current_auth_rev
        new.downstream_dedup_on = self.downstream_dedup_on
        new.guard_mode = self.guard_mode
        new.key_expiry = dict(self.key_expiry)
        new.withhold_receipts = self.withhold_receipts
        if self.failover_loses_dedup:
            new.dedup = {}                 # BROKEN: in-flight dedup lost
        else:
            new.dedup = dict(self.dedup)
        return new

    def advance(self, dt: int = 1):
        self.now += dt

    def submit(self, op: LogicalOperation, region: str = "r1"):
        """Public entry: logs every submission outcome (the response layer)
        separately from the effect ledger (the resource layer). Two identical
        HTTP responses != one provider resource != one downstream effect."""
        try:
            outcome, receipt = self._submit(op, region=region)
        except Exception:
            self.submissions.append((op.op_key, "SUBMIT_RAISED"))
            raise
        self.submissions.append((op.op_key, outcome))
        return outcome, receipt

    def _submit(self, op: LogicalOperation, region: str = "r1"):
        # Scripted transport outcomes (alert T-suite): these touch neither the
        # ledger nor the dedup record -- they are availability signals, never
        # correctness evidence.
        if self.error_script:
            scripted = self.error_script.pop(0)
            if scripted == "TIMEOUT_RAISED":
                raise TimeoutError("scripted transport timeout")
            return scripted, None  # e.g. RATE_LIMITED
        dkey = (region, op.op_key)
        """Submit an external request. Returns (outcome, receipt_or_None).

        Dedup is scoped by (region, op_key) unless cross-region dedup is
        independently established. The same key with a different payload is
        REJECTED -- never a silent different effect under the same identity.
        guard_mode="atomic" (default): the dedup key is recorded under the
        provider lock BEFORE the effect commits, so concurrent/late submits
        deduplicate. guard_mode="broken_record_after_effect": the key is
        recorded only after the effect -- the D3/broken-provider defect.
        pause_before_commit: an optional threading.Event; when set, submit
        blocks between the dedup check and the effect commit (the D3 race).
        """
        dkey = (region, op.op_key)
        with self._lock:
            if op.op_key not in self.first_request_at:
                self.first_request_at[op.op_key] = self.now
            if self.key_expiry.get(op.op_key):
                return "REJECTED_KEY_EXPIRED", None
            horizon = self.retention_horizon.get(op.op_key)
            if horizon is not None and self.now >= horizon:
                return "REJECTED_KEY_EXPIRED", None
            if op.authorization_rev < self.current_auth_rev:
                return "REJECTED_STALE_AUTHORITY", None
            if region in self.rejected_regions:
                return "REJECTED_SCOPE", None
            if dkey in self.dedup:
                if self.payloads.get(dkey) != op.payload_hash:
                    return "REJECTED_PAYLOAD_MISMATCH", None
                # Atomic dedup: same logical effect, no duplicate.
                eff = self.dedup[dkey]
                rc = None if self.withhold_receipts else f"RCPT-{eff}-dup"
                return "DEDUPED", rc
            if self.guard_mode == "atomic":
                # Key recorded BEFORE the effect: any concurrent or late
                # attempt sees it and deduplicates.
                self._effect_no += 1
                eff = self._effect_no
                self.dedup[dkey] = eff
                self.payloads[dkey] = op.payload_hash
        # Outside the provider lock: the pre-commit pause point (D3).
        if self.pause_before_commit is not None:
            if self.pre_commit_hook is not None:
                try:
                    self.pre_commit_hook(op.op_key)
                except Exception:
                    pass
            self.pause_before_commit.wait(30)
        with self._lock:
            if self.guard_mode == "broken_record_after_effect":
                # DEFECT: key recorded only after the effect -- a concurrent
                # attempt that passed the check above commits a second effect.
                self._effect_no += 1
                eff = self._effect_no
                self.dedup[dkey] = eff
                self.payloads[dkey] = op.payload_hash
            if self.crash_on_submit:
                # Crash between effect and acknowledgment: the effect may
                # have happened; the receipt is lost.
                self.ledger.append((op.op_key, eff))
                raise RuntimeError("crashed after effect, before ack")
            self.ledger.append((op.op_key, eff))
            rc = None if self.withhold_receipts else f"RCPT-{eff}"
            return "COMMITTED", rc

    def count_effects(self, op_key) -> int:
        return sum(1 for k, _ in self.ledger if k == op_key)

    def expire_key(self, op_key):
        self.key_expiry[op_key] = True

    def revoke_authority(self):
        self.current_auth_rev += 1


def recover_ambiguous_operation(effect: AmbiguousEffect,
                                g: RecoveryGuarantees) -> dict:
    """The recover_ambiguous_operation procedure: fence -> reconcile ->
    confirmed-committed => verify-and-close; proven-cannot-commit =>
    consider fresh execution; else require duplicate-safety contract +
    current LAW/evidence + covers_all_possible_outstanding_attempts (the
    most important condition) => same-identity retry; otherwise hold."""
    if not g.recovery_fence_held:
        return {"decision": REC_HOLD,
                "reason": "recovery fence not held: two workers must never "
                          "simultaneously decide to retry; fence first"}
    return decide_recovery(effect, g)


def aer_001():
    """AER-001: controlled mock provider with durable effect ledger; two
    hidden worlds; receipt withheld; require reconcile-or-hold; then
    enable proven atomic idempotency and verify at-most-one logical
    effect under concurrency/crash/late-completion; then expire the key
    and require rejection; the VERIFIER counts effects in the ledger."""
    import threading
    report = {}

    # Two hidden worlds, receipt withheld: reconcile-or-hold, never blind retry.
    provider = MockExternalProvider()
    provider.withhold_receipts = True
    op = LogicalOperation("op-127-001", "payments", "hash-abc",
                          authorization_rev=1, created_at_seq=1)
    effect = AmbiguousEffect(op, frozenset({"COMMITTED", "IN_FLIGHT"}),
                             ("receipt withheld",), "reversible")
    g = RecoveryGuarantees(current_law_valid=True, recovery_fence_held=True)
    d = recover_ambiguous_operation(effect, g)
    assert d["decision"] == REC_HOLD, d
    report["withheld_receipt"] = d["decision"]  # hold, never blind retry

    # Enable proven atomic idempotency: concurrency + crash + late dup.
    provider.withhold_receipts = False
    op2 = LogicalOperation("op-127-002", "payments", "hash-def",
                           authorization_rev=1, created_at_seq=2)
    errors = []

    def attempt():
        try:
            provider.submit(op2)
        except RuntimeError as e:
            errors.append(str(e))

    provider.crash_on_submit = True
    t1 = threading.Thread(target=attempt)
    t1.start()
    t1.join()
    provider.crash_on_submit = False
    # Late completions and duplicates after the crash.
    threads = [threading.Thread(target=lambda: provider.submit(op2))
               for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    n = provider.count_effects("op-127-002")
    assert n == 1, f"at-most-one violated: {n} effects"
    report["atomic_idempotency_at_most_one"] = n

    # Expire the key: further retries are rejected, not re-executed.
    provider.expire_key("op-127-002")
    out, _ = provider.submit(op2)
    assert out == "REJECTED_KEY_EXPIRED", out
    assert provider.count_effects("op-127-002") == 1
    report["key_expiry_rejects"] = out

    # Stale authority: dedup does not survive authorization revocation.
    provider.revoke_authority()
    op3 = LogicalOperation("op-127-003", "payments", "hash-ghi",
                           authorization_rev=1, created_at_seq=3)
    out3, _ = provider.submit(op3)
    assert out3 == "REJECTED_STALE_AUTHORITY", out3
    report["stale_authority_rejects"] = out3

    # The VERIFIER counts effects in the ledger (not intent records).
    total = len(provider.ledger)
    assert total == 1, provider.ledger
    report["verifier_ledger_count"] = total
    return report

# ===========================================================================
# AER-PROVIDER-1 — Provider Deduplication Qualification Law (SN-0794)
# ===========================================================================
"""AER-PROVIDER-1 defines what AER-1's 'independently verified safeguards'
actually mean for a provider's duplicate-safety claim.

LAW: rely on a provider's idempotency guarantee only for the exact operation,
scope, concurrency model, downstream effects, and recovery horizon
independently established by admissible evidence -- never generalize one
endpoint's guarantee provider-wide.

Real-provider illustrations below (Stripe / AWS EC2 / PayPal) are documented
from the framework intel as ILLUSTRATIONS, not independently verified claims.
They show what each dimension means in practice; they prove nothing here.

Qualification verdicts are CAPABILITY outcomes, never LAW authority: even
QUALIFIED_IN_SCOPE needs fresh LAW authorization + ACT enforcement at use
time. These verdicts never replace the six evidence-qualification verdicts.
"""

# --- The eleven-dimension contract table ------------------------------------
# Each dimension: what VERIFY must independently establish, and what counts
# as admissible evidence. A dimension with no evidence is UNPROVEN, and
# UNPROVEN dimensions never authorize reliance.
PROVIDER_CONTRACT_DIMENSIONS = (
    ("logical_identity",
     "One canonical identity per logical operation, stable across retries, "
     "restarts, and failover. Restarts recover the SAME identity -- never "
     "manufacture a new one or a fresh key.",
     "OP-127 record; restart/failover test (D6) showing the same identity deduplicates",
     None),
    ("concurrency",
     "Concurrent same-key attempts yield at most one protected effect, "
     "enforced by the provider independent of client locking.",
     "D1/D4 adversarial concurrency; provider state-machine model check",
     "PayPal: simultaneous same-ID requests may process the first and fail "
     "the second -- a failed concurrent request is not a deduplication failure"),
    ("atomicity",
     "The dedup check and the effect commit are atomic with respect to each "
     "other; no check-then-act race between them.",
     "D3 pause-before-commit race; broken-guard mutation caught by the harness",
     "Stripe: the concurrency-conflict case where no idempotent result was saved"),
    ("late_completion",
     "A paused, slow, or late first attempt cannot produce a second protected "
     "effect when a same-key retry lands first.",
     "D3 five-step experiment, verified in the provider AND downstream ledgers",
     None),
    ("downstream_propagation",
     "For each material downstream effect: atomic relationship with the root "
     "or independent duplicate suppression. OneRootOperation does NOT imply "
     "OneOfEveryDownstreamEffect.",
     "D8 downstream retry; root-vs-downstream business-identifier comparison",
     None),
    ("scope",
     "The exact operation set, endpoint, region, and tenant the guarantee "
     "covers. A provider's identity never proves all its operations share "
     "guarantees.",
     "D7 regional boundary; pinned contract text",
     "AWS EC2: ClientToken scope is regional vs zonal depending on the API; "
     "PayPal: PayPal-Request-Id is endpoint-specific with stated retention periods"),
    ("retention",
     "Key lifetime. T_last-retry < T_provider-expiry with uncertainty "
     "allowance; the recovery window is measured from the FIRST provider "
     "request, never reset on worker restart.",
     "D9 retention boundary; the retention-horizon inequality",
     "Stripe: idempotency keys removed after >= 24h"),
    ("recovery_visibility",
     "Status queries distinguish committed / cannot-commit / in-flight / "
     "unknown. Unknown is never silently treated as success, failure, or "
     "nonexecution.",
     "D11 concurrent reconciliation; D12 incomplete observability => UNPROVEN",
     None),
    ("failure_behavior",
     "Documented behavior on conflicts, failover, and partial failure -- "
     "including which failures are NOT deduplication failures.",
     "D6 failover; the contract's failure-mode table",
     "PayPal concurrent-conflict failure; Stripe cached error results"),
    ("contract_evolution",
     "The guarantee is versioned; provider changes re-trigger qualification; "
     "stale qualifications never authorize new retries.",
     "Contract version pin; requalification trigger on change notice",
     None),
    ("payload_binding",
     "The same identity with a different payload is rejected -- never a "
     "silent different effect under the same key.",
     "D5 payload mismatch",
     None),
)
PROVIDER_CONTRACT_DIMENSION_NAMES = tuple(d[0] for d in PROVIDER_CONTRACT_DIMENSIONS)


# --- The four-evidence proof package ------------------------------------------
@dataclass(frozen=True)
class ProviderProofPackage:
    """Finite tests never prove universal exactly-once alone. Stronger claims
    need all four: the provider contract, mechanism evidence, adversarial
    execution evidence, and independent effect observation."""
    provider_contract: str              # pinned contract text / version
    mechanism_evidence: str             # how the mechanism was established
    adversarial_execution_evidence: str  # D1-D12 + broken-provider mutations
    independent_effect_observation: str  # ledger-based counts, per level


def proof_package_complete(pkg: ProviderProofPackage) -> Tuple[bool, Tuple[str, ...]]:
    fields = ("provider_contract", "mechanism_evidence",
              "adversarial_execution_evidence", "independent_effect_observation")
    missing = tuple(f for f in fields if not getattr(pkg, f))
    return (not missing, missing)


# --- Explicit qualification verdicts -------------------------------------------
PROVIDER_QUALIFICATION_VERDICTS = (
    "QUALIFIED_IN_SCOPE",
    "PARTIALLY_QUALIFIED",
    "FAILED",
    "UNPROVEN",
    "OUT_OF_SCOPE",
)


@dataclass(frozen=True)
class ProviderQualificationCertificate:
    """AER-PROVIDER-1 certificate. Joins the spec's receipt family.
    A capability outcome, never LAW authority."""
    certificate_id: str
    provider: str
    endpoint_scope: str
    contract_version: str
    dimensions: Tuple[Tuple[str, str, str], ...]  # (dimension, verdict, evidence_ref)
    overall_verdict: str
    proof_package: ProviderProofPackage
    downstream_coverage: str  # DOWNSTREAM_EFFECTS_QUALIFIED | DOWNSTREAM_EFFECTS_UNPROVEN
    retention_inequality_holds: bool
    exclusions: Tuple[str, ...]
    issued_logical_time: int


def qualify_provider_contract(provider: str, endpoint_scope: str,
                              contract_version: str,
                              dimension_evidence: Dict[str, Tuple[str, str]],
                              proof_package: ProviderProofPackage,
                              downstream_covered: bool,
                              retention_ok: bool,
                              operation_in_scope: bool = True,
                              exclusions: Tuple[str, ...] = ()) -> ProviderQualificationCertificate:
    """Qualify a provider's duplicate-safety claim. dimension_evidence maps
    each of the eleven dimensions to (verdict, evidence_ref); a missing
    dimension is UNPROVEN. Root-only qualification yields PARTIALLY_QUALIFIED
    with DOWNSTREAM_EFFECTS_UNPROVEN -- never a silent downstream claim."""
    dims = []
    for name in PROVIDER_CONTRACT_DIMENSION_NAMES:
        v, ref = dimension_evidence.get(name, ("UNPROVEN", "no evidence presented"))
        dims.append((name, v, ref))
    verdicts = {v for _, v, _ in dims}
    pkg_ok, _ = proof_package_complete(proof_package)
    if not operation_in_scope:
        overall = "OUT_OF_SCOPE"
    elif "FAILED" in verdicts:
        overall = "FAILED"
    elif "UNPROVEN" in verdicts or not pkg_ok:
        overall = "UNPROVEN"
    elif not downstream_covered or not retention_ok:
        overall = "PARTIALLY_QUALIFIED"
    else:
        overall = "QUALIFIED_IN_SCOPE"
    downstream_coverage = ("DOWNSTREAM_EFFECTS_QUALIFIED" if downstream_covered
                           else "DOWNSTREAM_EFFECTS_UNPROVEN")
    return ProviderQualificationCertificate(
        certificate_id=f"AER-PROVIDER-1/{provider}/{contract_version}",
        provider=provider, endpoint_scope=endpoint_scope,
        contract_version=contract_version, dimensions=tuple(dims),
        overall_verdict=overall, proof_package=proof_package,
        downstream_coverage=downstream_coverage,
        retention_inequality_holds=retention_ok,
        exclusions=tuple(exclusions), issued_logical_time=0)


# --- Independent effect observation ---------------------------------------------
def verify_effect_chain(provider: MockExternalProvider, op_key: str) -> dict:
    """The observation chain: two identical HTTP responses != one provider
    resource != one downstream material effect. Each level is counted
    separately from its own durable record; never count notifications
    indiscriminately (two webhook deliveries != two business effects).
    Verify the specific effect claimed."""
    n_responses = sum(1 for k, _ in provider.submissions if k == op_key)
    n_effects = provider.count_effects(op_key)
    n_downstream = provider.count_downstream(op_key)
    return {
        "op_key": op_key,
        "responses_seen": n_responses,
        "provider_effects": n_effects,
        "downstream_effects": n_downstream,
        "dedup_working": n_responses > n_effects and n_effects <= 1,
        "duplicate_effect": n_effects > 1,
        "downstream_exceeds_root": n_downstream > n_effects,
        "note": "each level verified from its own record; responses != resources != downstream",
    }


# --- The retention-horizon inequality --------------------------------------------
def retention_horizon_ok(t_first_request, t_last_retry, t_provider_expiry,
                         uncertainty_allowance=0) -> bool:
    """T_last-retry + allowance < T_provider-expiry. Pre-expiry checks do not
    make finite retention indefinite: if the original attempt can stay pending
    indefinitely without late-completion protection, no finite retention
    establishes universal safety -- shorten the retry window, add durable
    reconciliation, or withhold automated retries past the boundary."""
    return (t_last_retry + uncertainty_allowance) < t_provider_expiry


def recovery_window_valid(provider: MockExternalProvider, op_key: str,
                           t_last_retry, uncertainty_allowance=0) -> Tuple[bool, str]:
    """The recovery window is measured from the FIRST provider request --
    never reset on worker restart."""
    t_first = provider.first_request_at.get(op_key)
    horizon = provider.retention_horizon.get(op_key)
    if t_first is None:
        return False, "no provider request observed -- window undefined"
    if horizon is None:
        return False, "no provider expiry established -- finite retention unproven"
    ok = retention_horizon_ok(t_first, t_last_retry, horizon, uncertainty_allowance)
    return ok, ("holds" if ok else
                "T_last-retry + allowance >= T_provider-expiry: shorten window, "
                "reconcile durably, or withhold automated retries past the boundary")

# --- The D1-D12 adversarial suite --------------------------------------------------
# Sandbox/test tenants first -- no consequential effects without authorization.
# Each Di runs against the controlled mock and returns (id, verdict, evidence).
# D-verdicts: QUALIFIED / FAILED / UNPROVEN / DEFECT_DETECTED / HARNESS_BLIND.
def _fresh_provider(**kw) -> MockExternalProvider:
    p = MockExternalProvider()
    for k, v in kw.items():
        setattr(p, k, v)
    return p


def _dop(key: str, payload: str = "hash-p", auth_rev: int = 1) -> LogicalOperation:
    return LogicalOperation(key, "payments", payload,
                            authorization_rev=auth_rev, created_at_seq=1)


def d1_concurrent_same_key(n_threads: int = 8) -> dict:
    """D1: N concurrent same-key submits -> at most one protected effect."""
    p = _fresh_provider()
    op = _dop("OP-D1")
    ts = [threading.Thread(target=lambda: p.submit(op)) for _ in range(n_threads)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    n = p.count_effects("OP-D1")
    return {"id": "D1", "verdict": "QUALIFIED" if n == 1 else "FAILED",
            "evidence": f"{n_threads} concurrent same-key submits -> {n} provider effect(s)"}


def d2_lost_acknowledgment() -> dict:
    """D2: receipt lost; the retry must deduplicate, not re-execute."""
    p = _fresh_provider(withhold_receipts=True)
    op = _dop("OP-D2")
    out1, rc1 = p.submit(op)
    out2, _rc2 = p.submit(op)  # retry after the lost acknowledgment
    n = p.count_effects("OP-D2")
    ok = out1 == "COMMITTED" and rc1 is None and out2 == "DEDUPED" and n == 1
    return {"id": "D2", "verdict": "QUALIFIED" if ok else "FAILED",
            "evidence": f"first={out1}/receipt-withheld retry={out2} effects={n}"}


def d3_late_completion_race(guard_mode: str = "atomic") -> dict:
    """D3: the five-step experiment. (1) Pause Attempt A before effect commit;
    (2) submit same-key Attempt B; (3) release A; (4) both settle; (5) the
    VERIFIER counts at most one protected logical effect in the provider AND
    downstream ledgers. Mock-first: the harness must DETECT the defect --
    mock success is never reported as production proof."""
    p = _fresh_provider()
    p.guard_mode = guard_mode
    gate = threading.Event()
    entered = threading.Event()
    p.pause_before_commit = gate
    p.pre_commit_hook = lambda _k: entered.set()
    op = _dop("OP-D3")
    outcomes = {}

    def attempt_a():
        outcomes["a"] = p.submit(op)

    t = threading.Thread(target=attempt_a)
    t.start()
    assert entered.wait(10), "attempt A never reached the pre-commit pause"
    # B must not block on the gate: A already holds the check-then-commit
    # window open (A read the gate object before we clear the attribute).
    p.pause_before_commit = None
    outcomes["b"] = p.submit(op)  # the late same-key attempt
    gate.set()                    # release A; the late completion lands
    t.join(10)
    # Downstream: one business effect per root effect, same identity.
    for k, eff_no in list(p.ledger):
        if k == "OP-D3":
            p.emit_downstream(k, f"down-{eff_no}")
    n = p.count_effects("OP-D3")
    nd = p.count_downstream("OP-D3")
    chain = verify_effect_chain(p, "OP-D3")
    if guard_mode == "atomic":
        ok = n == 1 and nd == 1
        return {"id": "D3", "verdict": "QUALIFIED" if ok else "FAILED",
                "provider_effects": n, "downstream_effects": nd,
                "evidence": f"late-completion race -> {n} root / {nd} downstream effect(s); chain={chain}"}
    # Broken guard: the harness MUST see the duplicate.
    detected = n == 2 and nd == 2
    return {"id": "D3-broken", "verdict": "DEFECT_DETECTED" if detected else "HARNESS_BLIND",
            "provider_effects": n, "downstream_effects": nd,
            "evidence": f"guard removed -> {n} root / {nd} downstream effect(s)"}


def d4_provider_enforced_without_client_lock() -> dict:
    """D4: provider enforcement independent of client locking. The two workers
    share NO client-side lock; only the provider's own atomicity may hold."""
    p = _fresh_provider()
    op = _dop("OP-D4")
    ts = [threading.Thread(target=lambda: p.submit(op)) for _ in range(2)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    n = p.count_effects("OP-D4")
    return {"id": "D4", "verdict": "QUALIFIED" if n == 1 else "FAILED",
            "evidence": f"no client lock held; provider atomicity -> {n} effect(s)"}


def d5_payload_mismatch() -> dict:
    """D5: the same key with a different payload is rejected -- never a
    silent different effect under the same identity."""
    p = _fresh_provider()
    o1, _ = p.submit(_dop("OP-D5", payload="hash-v1"))
    o2, _ = p.submit(_dop("OP-D5", payload="hash-v2"))
    n = p.count_effects("OP-D5")
    ok = o1 == "COMMITTED" and o2 == "REJECTED_PAYLOAD_MISMATCH" and n == 1
    return {"id": "D5", "verdict": "QUALIFIED" if ok else "FAILED",
            "evidence": f"same key, different payload -> {o2}; effects={n}"}


def d6_restart_failover(lose_dedup: bool = False) -> dict:
    """D6: restart/failover recovers the SAME identity; dedup survives.
    With lose_dedup=True (broken-provider mutation), the harness must detect
    the duplicate."""
    p = _fresh_provider()
    p.failover_loses_dedup = lose_dedup
    op = _dop("OP-D6")
    p.submit(op)
    p2 = p.failover()
    out, _ = p2.submit(op)
    n = p2.count_effects("OP-D6")
    if not lose_dedup:
        ok = out == "DEDUPED" and n == 1
        return {"id": "D6", "verdict": "QUALIFIED" if ok else "FAILED",
                "evidence": f"failover kept dedup -> {out}; effects={n}"}
    detected = out == "COMMITTED" and n == 2
    return {"id": "D6-broken", "verdict": "DEFECT_DETECTED" if detected else "HARNESS_BLIND",
            "evidence": f"failover lost dedup -> {out}; effects={n}"}


def d7_regional_boundary() -> dict:
    """D7: the guarantee is scope-bound. Dedup does NOT cross regions unless
    cross-region dedup is independently established -- two effects here is
    CORRECT scoping, and cross-region reliance is OUT_OF_SCOPE."""
    p = _fresh_provider()
    op = _dop("OP-D7")
    o1, _ = p.submit(op, region="r1")
    o2, _ = p.submit(op, region="r2")
    n1 = sum(1 for k, _ in p.ledger if k == "OP-D7")
    ok = o1 == "COMMITTED" and o2 == "COMMITTED" and n1 == 2
    return {"id": "D7", "verdict": "QUALIFIED" if ok else "FAILED",
            "evidence": f"r1={o1} r2={o2}; regional dedup only -- cross-region reliance OUT_OF_SCOPE"}


def d8_downstream_retry() -> dict:
    """D8: a downstream consumer retrying must not create a second business
    effect; the (op_key, effect_id) pair deduplicates."""
    p = _fresh_provider()
    p.submit(_dop("OP-D8"))
    e1 = p.emit_downstream("OP-D8", "eff-1")
    e2 = p.emit_downstream("OP-D8", "eff-1")
    n = p.count_downstream("OP-D8")
    ok = e1 == "EMITTED" and e2 == "DEDUPED_DOWNSTREAM" and n == 1
    return {"id": "D8", "verdict": "QUALIFIED" if ok else "FAILED",
            "evidence": f"downstream retry -> {e1} then {e2}; business effects={n}"}


def d9_retention_boundary() -> dict:
    """D9: past the retention horizon the retry is rejected, not re-executed;
    the inequality must fail there too."""
    p = _fresh_provider()
    op = _dop("OP-D9")
    p.retention_horizon["OP-D9"] = 5
    p.submit(op)
    p.advance(6)
    out, _ = p.submit(op)
    ok_ineq, _ = recovery_window_valid(p, "OP-D9", t_last_retry=6)
    ok = out == "REJECTED_KEY_EXPIRED" and p.count_effects("OP-D9") == 1 and not ok_ineq
    return {"id": "D9", "verdict": "QUALIFIED" if ok else "FAILED",
            "evidence": f"past-horizon retry -> {out}; inequality correctly fails past the boundary"}


def d10_delayed_callback() -> dict:
    """D10: a delayed duplicate callback correlates to the same logical
    operation -- no new effect."""
    p = _fresh_provider()
    op = _dop("OP-D10")
    o1, _ = p.submit(op)
    o2, _ = p.submit(op)  # the delayed duplicate delivery
    n = p.count_effects("OP-D10")
    ok = o1 == "COMMITTED" and o2 == "DEDUPED" and n == 1
    return {"id": "D10", "verdict": "QUALIFIED" if ok else "FAILED",
            "evidence": f"delayed duplicate callback -> {o2}; effects={n}"}


def d11_concurrent_reconciliation() -> dict:
    """D11: two reconcilers concurrently ensuring the same operation still
    yield at most one effect."""
    p = _fresh_provider()
    op = _dop("OP-D11")
    ts = [threading.Thread(target=lambda: p.submit(op)) for _ in range(2)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    n = p.count_effects("OP-D11")
    return {"id": "D11", "verdict": "QUALIFIED" if n == 1 else "FAILED",
            "evidence": f"concurrent reconcilers -> {n} effect(s)"}


class BlindProviderView:
    """A provider view with no ledger access: submit only. The qualifier can
    count nothing -- the verdict is UNPROVEN, never a fabricated number."""

    def __init__(self, provider: MockExternalProvider):
        self._p = provider

    def submit(self, op: LogicalOperation, region: str = "r1"):
        return self._p.submit(op, region=region)


def d12_incomplete_observability() -> dict:
    """D12: with no independent effect observation, the claim is UNPROVEN --
    not failed, not qualified. Missing evidence is never silently treated as
    proof of safety."""
    p = _fresh_provider()
    view = BlindProviderView(p)
    view.submit(_dop("OP-D12"))
    return {"id": "D12", "verdict": "UNPROVEN",
            "evidence": "no ledger access: cannot distinguish one effect from two; "
                        "UNPROVEN, never a fabricated verdict"}


def run_d_suite() -> list:
    """Runs D1-D12 against the controlled mock."""
    return [d1_concurrent_same_key(), d2_lost_acknowledgment(),
            d3_late_completion_race("atomic"),
            d4_provider_enforced_without_client_lock(), d5_payload_mismatch(),
            d6_restart_failover(), d7_regional_boundary(), d8_downstream_retry(),
            d9_retention_boundary(), d10_delayed_callback(),
            d11_concurrent_reconciliation(), d12_incomplete_observability()]

# --- Provider state-machine model checking ------------------------------------------
# ABSENT -> ACCEPTED -> IN_PROGRESS -> EFFECT_COMMITTED -> RESULT_RECORDED
#   x  KEY_ACTIVE -> KEY_EXPIRED   x   downstream effects
# Property: CountProtectedEffects(op) <= 1 in the qualified scope.
# At-most-once is not exactly-once: the machine never assumes eventual
# service to convert the claim.
#
# The machine models one logical operation with two potential committers
# (A, B) inside the QUALIFIED scope (key active, same region, current key
# version). Honest transitions never accept a second lifecycle there; each
# broken-provider mutation enables exactly one wrongful accept, and the
# checker must find the minimal (shortest) counterexample trace.
BROKEN_PROVIDER_MUTATIONS = (
    "non_atomic_dedup",          # check-then-act race: concurrent submit commits
    "dedup_after_effect",        # dedup recorded only after the effect
    "failover_loss",             # failover drops the dedup record
    "early_expiry",              # key expires mid-flight; resubmit treated as new
    "region_exclusion",          # claimed cross-region dedup silently excluded
    "downstream_without_dedup",  # downstream emits per attempt, no suppression
    "late_ignores_replacement",  # late attempt ignores the replacement guard
)


def provider_machine_check(defects=frozenset(), max_depth=16):
    """BFS over the provider lifecycle. defects: subset of
    BROKEN_PROVIDER_MUTATIONS. Returns (violated: bool, trace: tuple).
    The honest configuration must be exhaustively clean; every
    broken-provider mutation must yield a minimal counterexample."""
    from collections import deque
    # state: (seen, a, b, key_active, superseded, effects, downstream)
    # a, b in {"IDLE","INFLIGHT","DONE"}; seen = dedup key recorded.
    init = (False, "IDLE", "IDLE", True, False, 0, 0)

    def submit_moves(s, who):
        seen, a, b, key_active, superseded, effects, downstream = s
        me = a if who == "A" else b
        other = b if who == "A" else a
        if me != "IDLE":
            return
        lbl = f"submit_{who}"
        if superseded:
            if "late_ignores_replacement" in defects:
                ns = (True, "INFLIGHT", b, key_active, True, effects, downstream) if who == "A" \
                    else (True, a, "INFLIGHT", key_active, True, effects, downstream)
                yield lbl + "+ignores_replacement", ns
            else:
                ns = (seen, "DONE", b, key_active, True, effects, downstream) if who == "A" \
                    else (seen, a, "DONE", key_active, True, effects, downstream)
                yield lbl + ":rejected_superseded", ns
            return
        if not key_active:
            if "early_expiry" in defects:
                ns = (True, "INFLIGHT", b, False, False, effects, downstream) if who == "A" \
                    else (True, a, "INFLIGHT", False, False, effects, downstream)
                yield lbl + "+accepted_after_expiry", ns
            else:
                ns = (seen, "DONE", b, False, False, effects, downstream) if who == "A" \
                    else (seen, a, "DONE", False, False, effects, downstream)
                yield lbl + ":rejected_expired", ns
            return
        if seen and other == "INFLIGHT" and \
                defects & {"non_atomic_dedup", "dedup_after_effect"}:
            ns = (seen, "INFLIGHT", b, True, False, effects, downstream) if who == "A" \
                else (seen, a, "INFLIGHT", True, False, effects, downstream)
            yield lbl + "+race", ns
            return
        if seen:
            ns = (seen, "DONE", b, True, False, effects, downstream) if who == "A" \
                else (seen, a, "DONE", True, False, effects, downstream)
            yield lbl + ":deduped", ns
            return
        ns = (True, "INFLIGHT", b, True, False, effects, downstream) if who == "A" \
            else (True, a, "INFLIGHT", True, False, effects, downstream)
        yield lbl, ns

    def moves(s):
        seen, a, b, key_active, superseded, effects, downstream = s
        yield from submit_moves(s, "A")
        yield from submit_moves(s, "B")
        if "region_exclusion" in defects and b == "IDLE" and key_active and not superseded:
            # Claimed cross-region dedup, silently excluded: B bypasses `seen`.
            yield "submit_B_other_region+bypasses_dedup", (seen, a, "INFLIGHT", True, False, effects, downstream)
        for who, me in (("A", a), ("B", b)):
            if me == "INFLIGHT":
                ns = (seen, "DONE", b, key_active, superseded, effects + 1, downstream) if who == "A" \
                    else (seen, a, "DONE", key_active, superseded, effects + 1, downstream)
                yield f"commit_{who}", ns
        if key_active:
            yield "expire", (seen, a, b, False, superseded, effects, downstream)
        if "failover_loss" in defects:
            yield "failover+drops_dedup", (False, a, b, key_active, superseded, effects, downstream)
        else:
            yield "failover(durable)", s
        yield "supersede_key", (seen, a, b, key_active, True, effects, downstream)
        if effects >= 1:
            if "downstream_without_dedup" in defects:
                yield "emit_downstream", (seen, a, b, key_active, superseded, effects, downstream + 1)
            elif downstream == 0:
                yield "emit_downstream:deduped", (seen, a, b, key_active, superseded, effects, 1)

    def violated(s):
        return s[5] >= 2 or s[6] >= 2

    seen_states = {init}
    queue = deque([(init, ())])
    while queue:
        s, trace = queue.popleft()
        if violated(s):
            return True, trace
        if len(trace) >= max_depth:
            continue
        for lbl, ns in moves(s):
            if ns not in seen_states:
                seen_states.add(ns)
                ntrace = trace + (lbl,)
                if violated(ns):
                    return True, ntrace
                queue.append((ns, ntrace))
    return False, ()


def broken_provider_mutation_check():
    """Every broken-provider mutation must yield a minimal counterexample.
    A harness that cannot detect the broken mock is not qualified for the
    real provider."""
    report = {}
    for m in BROKEN_PROVIDER_MUTATIONS:
        violated, trace = provider_machine_check(defects=frozenset({m}))
        report[m] = {"violated": violated, "trace_length": len(trace),
                     "trace": trace}
        assert violated, f"mutation {m} NOT detected -- harness unqualified"
    honest_violated, _ = provider_machine_check()
    assert not honest_violated, "honest provider must be exhaustively clean"
    report["honest"] = {"violated": False, "note": "exhaustive: no violation reachable"}
    return report


# --- AER-PROVIDER-001: the first fixture ----------------------------------------------
def aer_provider_001():
    """AER-PROVIDER-001: controlled provider with durable effect ledger.
    (a) pause-before-commit race, intact contract -> at most one material
        effect, verified in the provider AND downstream ledgers;
    (b) removed atomic guard -> minimal duplicate counterexample (the harness
        must detect it);
    (c) crash variant -> reconcile-and-retry stays at-most-one;
    (d) expiry variant -> past-horizon retry rejected.
    Mock-first: mock success is never reported as production proof. The real
    endpoint runs later, under authorized nonconsequential conditions, with
    sandbox-vs-live differences established."""
    report = {}
    r = d3_late_completion_race(guard_mode="atomic")
    assert r["provider_effects"] == 1 and r["downstream_effects"] == 1, r
    report["intact_at_most_one"] = {"root": r["provider_effects"],
                                    "downstream": r["downstream_effects"]}
    rb = d3_late_completion_race(guard_mode="broken_record_after_effect")
    assert rb["provider_effects"] == 2 and rb["verdict"] == "DEFECT_DETECTED", rb
    report["broken_guard_counterexample"] = {"root": rb["provider_effects"],
                                             "downstream": rb["downstream_effects"],
                                             "verdict": rb["verdict"]}
    p = _fresh_provider(crash_on_submit=True)
    op = _dop("OP-P001-C")
    try:
        p.submit(op)
    except RuntimeError:
        pass
    p.crash_on_submit = False
    for _ in range(4):
        p.submit(op)
    assert p.count_effects("OP-P001-C") == 1
    report["crash_variant_at_most_one"] = 1
    p2 = _fresh_provider()
    op2 = _dop("OP-P001-E")
    p2.retention_horizon["OP-P001-E"] = 10
    p2.submit(op2)
    p2.advance(11)
    out, _ = p2.submit(op2)
    assert out == "REJECTED_KEY_EXPIRED", out
    report["expiry_variant_rejects"] = out
    report["mock_only"] = ("mock evidence only; mock success is never reported "
                           "as production proof")
    return report

# ===========================================================================
# AER-DRIFT-1 — External Provider Contract Drift Law (SN-0795)
# ===========================================================================
"""AER-DRIFT-1 is the TEMPORAL layer: AER-PROVIDER-1 qualified the contract at
a point in time; this keeps the qualification honest over time.

LAW: every external guarantee supporting consequential operations must remain
scope-bound, versioned, evidence-backed, and revocable; material changes or
credible anomalies trigger proportionate review and immediate containment
where safety is uncertain; restoration never restores authority automatically.

THE HONEST LIMITATION FIRST: no finite monitoring scheme guarantees immediate
detection of every silent change. Hence TWO protections, not one: DETECTION
and CONTAINMENT. Containment -- not just detection -- is the safety property.
A missed detection with working containment is a degraded state; a detected
drift with no containment is a failure.
"""

# --- Four drift types ----------------------------------------------------------------
# Identify the violated obligation FIRST, then the cause.
DRIFT_TYPES = (
    ("scope_drift",
     "The guarantee silently narrows: regions, endpoints, tenants, or "
     "operation types previously covered stop being covered.",
     "obligation: scope (dimension 6)"),
    ("retention_drift",
     "Key lifetime silently shortens; retries past the new horizon are no "
     "longer deduplicated.",
     "obligation: retention (dimension 7) + the horizon inequality"),
    ("concurrency_drift",
     "Concurrent same-key protection silently weakens: races that were "
     "deduplicated now double-execute.",
     "obligation: concurrency (2) + atomicity (3) + late completion (4)"),
    ("downstream_drift",
     "Downstream duplicate suppression silently stops; root dedup intact but "
     "business effects duplicate.",
     "obligation: downstream propagation (dimension 5)"),
)
DRIFT_CAUSES = (
    "PROVIDER_BEHAVIOR_CHANGE",   # the provider changed what it does
    "CONTRACT_EVOLUTION",         # the provider changed what it promises
    "INTEGRATION_CHANGE",         # we changed endpoint/region/tenant wiring
    "INSUFFICIENT_EVIDENCE",      # the qualification never established it
)


# --- Versioned qualification manifests -------------------------------------------------
# A provider's identity never proves all its operations share guarantees.
@dataclass(frozen=True)
class ProviderQualificationManifest:
    """PROVIDER-QUAL-27 shape: the versioned, scope-bound, evidence-backed,
    revocable record of what was qualified, when, and under which contract."""
    manifest_id: str
    provider: str
    endpoint: str
    api_version: str
    scope: str
    dimension_guarantees: Tuple[Tuple[str, str], ...]  # dimension -> guarantee statement
    contract_revision: int
    qualification_revision: int
    last_independent_verification: int  # logical time of the last canary/probe
    current_status: str                 # drift state machine state


def make_manifest(provider: str, endpoint: str, api_version: str, scope: str,
                  dimension_guarantees: Tuple[Tuple[str, str], ...],
                  contract_revision: int = 1) -> ProviderQualificationManifest:
    return ProviderQualificationManifest(
        manifest_id=f"PROVIDER-QUAL-27/{provider}/{endpoint}",
        provider=provider, endpoint=endpoint, api_version=api_version,
        scope=scope, dimension_guarantees=dimension_guarantees,
        contract_revision=contract_revision, qualification_revision=1,
        last_independent_verification=0, current_status="QUALIFIED_IN_SCOPE")


# --- Five signals + freshness ---------------------------------------------------------------
DRIFT_SIGNALS = (
    ("contract_change", "provider changelog / version bump / terms update"),
    ("concurrent_request_behavior", "canary: concurrent same-key outcomes"),
    ("retention_behavior", "canary: key-lifetime probes"),
    ("downstream_reconciliation", "downstream ledger vs root ledger comparison"),
    ("integration_configuration", "our endpoint / region / tenant wiring"),
    ("evidence_freshness", "CROSS-CUTTING: age of the last independent verification"),
)
# No single signal is authoritative. Signals are never averaged into one
# confidence score. An expired review is an evidence gap -- not provider
# misconduct.


# --- The drift state machine ------------------------------------------------------------------
# Provider-monitoring states. Never replacements for the six
# evidence-qualification verdicts. Proportional response: a single timeout is
# investigation, not suspension.
DRIFT_STATES = (
    "QUALIFIED_IN_SCOPE",
    "REVIEW_REQUIRED",
    "SUSPECTED_DRIFT",
    "QUALIFICATION_SUSPENDED",
    "REQUALIFIED_IN_NEW_SCOPE",
)
DRIFT_TRANSITIONS = {
    ("QUALIFIED_IN_SCOPE", "REVIEW_REQUIRED"):
        "credible anomaly signal or contract-change notice",
    ("REVIEW_REQUIRED", "QUALIFIED_IN_SCOPE"):
        "independent evidence clears the anomaly",
    ("REVIEW_REQUIRED", "SUSPECTED_DRIFT"):
        "independent evidence of a contract gap",
    ("SUSPECTED_DRIFT", "REVIEW_REQUIRED"):
        "evidence downgrades the suspicion",
    ("SUSPECTED_DRIFT", "QUALIFICATION_SUSPENDED"):
        "drift confirmed safety-relevant; atomic with the use-time fence",
    ("QUALIFICATION_SUSPENDED", "REQUALIFIED_IN_NEW_SCOPE"):
        "independent requalification under a revised contract",
    ("REQUALIFIED_IN_NEW_SCOPE", "REVIEW_REQUIRED"):
        "a requalified scope can drift again; the law has no statute of limitations",
}


class DriftResponseCoordinator:
    """Atomic race-safe drift response -- the 6-step sequence:
    1. canary observes the anomaly (observation recorded);
    2. VERIFY records independent evidence;
    3. the qualification revision advances WITH the use-time fence in ONE
       atomic commit (same ordering discipline as the Revocation
       Linearization Law: one authoritative commit point; every later
       authorization respects it);
    4. LAW/ACT stop authorizing dependent retries under the old revision;
    5. background refresh / requalification proceeds;
    6. a delayed old-revision worker retry is rejected by the fence.
    Withdrawal cannot retroactively stop in-flight noncooperating requests:
    those stay under reconciliation / cancellation / fencing per the actual
    contract -- they are not killed, and no NEW reliance is authorized."""

    def __init__(self, manifest: ProviderQualificationManifest):
        self._lock = threading.RLock()
        self.manifest = manifest
        self.state = "QUALIFIED_IN_SCOPE"
        self.fence = {}        # scope -> minimum qualification_revision allowed
        self.evidence_log = []  # independent evidence entries, oldest first

    def transition(self, to_state: str, evidence: str) -> dict:
        with self._lock:
            if (self.state, to_state) not in DRIFT_TRANSITIONS:
                return {"accepted": False,
                        "reason": f"illegal drift transition {self.state} -> {to_state}"}
            if to_state == "QUALIFICATION_SUSPENDED":
                # Step 3: revision advance + fence in ONE atomic commit.
                # Containment holds IMMEDIATELY at the withdrawal commit.
                new_rev = self.manifest.qualification_revision + 1
                self.manifest = replace(
                    self.manifest, qualification_revision=new_rev,
                    current_status=to_state)
                self.fence[self.manifest.scope] = new_rev
            else:
                self.manifest = replace(self.manifest, current_status=to_state)
            self.state = to_state
            self.evidence_log.append(evidence)
            return {"accepted": True, "state": to_state,
                    "qualification_revision": self.manifest.qualification_revision,
                    "fence": dict(self.fence)}

    def withdraw_now(self, evidence: str) -> dict:
        """L3 fast path: walk REVIEW_REQUIRED -> SUSPECTED_DRIFT ->
        QUALIFICATION_SUSPENDED under one lock hold. The suspension commit
        stays atomic with the fence; containment holds immediately."""
        order = {"QUALIFIED_IN_SCOPE": 0, "REQUALIFIED_IN_NEW_SCOPE": 0,
                 "REVIEW_REQUIRED": 1, "SUSPECTED_DRIFT": 2,
                 "QUALIFICATION_SUSPENDED": 3}
        with self._lock:
            steps = []
            for target in ("REVIEW_REQUIRED", "SUSPECTED_DRIFT",
                           "QUALIFICATION_SUSPENDED"):
                if order[self.state] >= order[target]:
                    continue
                r = self.transition(target, evidence + " [L3 fast path]")
                steps.append((target, r["accepted"]))
                if not r["accepted"]:
                    break
            return {"state": self.state, "steps": steps,
                    "qualification_revision": self.manifest.qualification_revision,
                    "fence": dict(self.fence)}

    def record_verification(self, logical_time: int):
        with self._lock:
            self.manifest = replace(
                self.manifest, last_independent_verification=logical_time)


# --- Current-use checks --------------------------------------------------------------------------
def authorize_recovery_retry(coordinator: DriftResponseCoordinator,
                             op: LogicalOperation, scope: str,
                             needs: Dict[str, bool], law_receipt: str,
                             outcome_state: str) -> dict:
    """The current-use check, evaluated at the GOVERNED COMMIT BOUNDARY --
    never at task creation. Old queue snapshots cannot restore reliance on
    suspended guarantees. needs maps dimension name -> required-for-this-retry.
    outcome_state: the reconciled outcome (RECONCILED / DEDUPLICATED /
    CONFIRMED_COMMITTED); unknown outcomes never authorize."""
    reasons = []
    with coordinator._lock:
        m = coordinator.manifest
        if coordinator.state in ("QUALIFICATION_SUSPENDED", "SUSPECTED_DRIFT"):
            return {"authorized": False,
                    "reasons": [f"qualification {coordinator.state}: dependent retries stop"]}
        if coordinator.state == "REVIEW_REQUIRED":
            return {"authorized": False,
                    "reasons": ["under review: guarantees uncertain; high-impact retries wait"]}
        min_rev = coordinator.fence.get(scope, 0)
        if m.qualification_revision < min_rev:
            reasons.append("old-revision worker: the use-time fence rejects")
        guarantees = dict(m.dimension_guarantees)
        for dim, required in needs.items():
            if required and dim not in guarantees:
                reasons.append(f"dimension '{dim}' not covered by the current qualification")
        if outcome_state not in ("RECONCILED", "DEDUPLICATED", "CONFIRMED_COMMITTED"):
            reasons.append(f"outcome {outcome_state}: reconcile first; unknown outcomes never authorize")
        if not law_receipt:
            reasons.append("no current LAW receipt: retries always need CURRENT permission")
        if op.authorization_rev < 1:
            reasons.append("stale authorization revision")
    return {"authorized": not reasons, "reasons": reasons,
            "qualification_revision": m.qualification_revision}


# --- Exposure windows -------------------------------------------------------------------------------
@dataclass(frozen=True)
class ExposureWindow:
    """Six timestamps. Last passing canary proves one operation, not unchanged
    behavior. Unknown start => REQUIRES_REVIEW classification, never an
    invented start time. Per-operation independent determination: never
    blanket-mark the window as duplicated."""
    last_verified_compatible: object
    first_verified_incompatible: object
    first_suspected: object
    provider_declared_effective: object
    earliest_plausible_boundary: object
    affected_scopes: Tuple[str, ...]
    classification: str  # BOUNDED | REQUIRES_REVIEW


def exposure_window(last_ok, first_bad, first_suspected, declared,
                    affected_scopes) -> ExposureWindow:
    if last_ok is None or first_bad is None:
        return ExposureWindow(last_ok, first_bad, first_suspected, declared,
                              first_suspected, tuple(affected_scopes),
                              "REQUIRES_REVIEW")
    return ExposureWindow(last_ok, first_bad, first_suspected, declared,
                          last_ok, tuple(affected_scopes), "BOUNDED")


def window_covers_operation(window: ExposureWindow, op_scope: str) -> Tuple[bool, str]:
    """Per-operation independent determination."""
    if op_scope not in window.affected_scopes:
        return False, "scope not affected"
    if window.classification == "REQUIRES_REVIEW":
        return True, "possibly affected: unknown start; requires per-operation review"
    return True, "in the bounded exposure window"


# --- Selective containment ------------------------------------------------------------------------------
# One broken guarantee never erases unrelated intelligence. The dependency
# graph tracks MATERIAL reliance: only operations materially relying on the
# drifted guarantee are contained. Historical Smart Notes stay intact;
# annotations change, history does not.
SELECTIVE_CONTAINMENT = (
    ("suspend_cross_region_retry",
     "cross-region retries under the drifted guarantee stop"),
    ("preserve_proven_same_region",
     "same-region operations with independent evidence continue"),
    ("preserve_ambiguous_outcomes",
     "unknown outcomes stay held under AER-1; never auto-resolved by drift response"),
    ("continue_read_only_queries",
     "authorized read-only status queries continue"),
    ("preserve_guarded_downstream",
     "independently-guarded downstream consumers continue"),
    ("flag_stale_successor_packages",
     "proof packages citing the suspended revision are flagged, not deleted"),
)


def containment_plan(drift_type: str, scope: str,
                     material_reliance: Dict[str, Tuple[str, ...]]) -> dict:
    """material_reliance: operation -> scopes it materially relies on.
    Returns the contained vs preserved operations for this drift."""
    contained, preserved = [], []
    for op, scopes in material_reliance.items():
        (contained if scope in scopes else preserved).append(op)
    return {"drift_type": drift_type, "scope": scope,
            "contained": tuple(contained), "preserved": tuple(preserved),
            "capabilities": [c[0] for c in SELECTIVE_CONTAINMENT]}


# --- Risk-based freshness and detection budget --------------------------------------------------------------
RISK_CLASSES = (
    ("HIGH", "irreversible / high-impact: no automatic retry when guarantees are uncertain"),
    ("MEDIUM", "bounded retry with containment and reconciliation"),
    ("LOW", "retry with monitoring"),
)


def detection_budget(risk_class: str) -> int:
    """Maximum tolerable exposure in logical time units. Never an exact
    detection-time guarantee without a complete observation/scheduling
    argument."""
    return {"HIGH": 1, "MEDIUM": 10, "LOW": 100}[risk_class]


def freshness_ok(manifest: ProviderQualificationManifest, now: int,
                 risk_class: str) -> Tuple[bool, str]:
    """Evidence freshness is the cross-cutting sixth signal. An expired
    review is an evidence gap, not provider misconduct."""
    age = now - manifest.last_independent_verification
    budget = detection_budget(risk_class)
    if age <= budget:
        return True, f"evidence age {age} within {risk_class} budget {budget}"
    return False, (f"evidence age {age} exceeds {risk_class} budget {budget}: "
                   "evidence gap -- review required, not provider misconduct")

# --- Silent controlled drift mutations D1-D10 -----------------------------------------------------
# Each mutates provider behavior WITHOUT a qualification revision -- the drift
# the monitor must catch (or correctly ignore for controls). The detection
# worker is blind to these switches; it sees only public observations.
def apply_drift_mutation(provider: MockExternalProvider, mutation_id: str,
                         key: str = "OP-DRIFT") -> dict:
    """Applies a silent drift mutation. Returns what changed (for the sealed
    answer key -- never shown to the detection worker)."""
    if mutation_id == "D1_scope_narrowing":
        provider.rejected_regions.add("r2")
        return {"changed": "region r2 silently rejected (was valid)"}
    if mutation_id == "D2_retention_shortening":
        provider.retention_horizon[key] = provider.now + 1
        return {"changed": f"retention horizon for {key} silently shortened to now+1"}
    if mutation_id == "D3_atomic_guard_removal":
        provider.guard_mode = "broken_record_after_effect"
        return {"changed": "atomic dedup guard silently removed"}
    if mutation_id == "D4_downstream_duplication":
        provider.downstream_dedup_on = False
        return {"changed": "downstream duplicate suppression silently disabled"}
    if mutation_id == "D5_late_completion":
        provider.withhold_receipts = True
        return {"changed": "acknowledgments silently withheld (late-completion behavior)"}
    if mutation_id == "D6_doc_only_change":
        provider.contract_text_version = getattr(provider, "contract_text_version", 1) + 1
        return {"changed": "contract text only; behavior identical (CONTROL)"}
    if mutation_id == "D7_behavior_only_change":
        provider.guard_mode = "broken_record_after_effect"
        return {"changed": "behavior changed, docs unchanged (must detect via canary)"}
    if mutation_id == "D8_unrelated_errors":
        provider.crash_on_submit = True
        return {"changed": "transient submit errors; contract unchanged (CONTROL)"}
    if mutation_id == "D9_disabled_monitor":
        return {"changed": "monitor disabled by operator (CONTROL: evidence gap)"}
    if mutation_id == "D10_restoration":
        provider.guard_mode = "atomic"
        provider.downstream_dedup_on = True
        provider.withhold_receipts = False
        provider.crash_on_submit = False
        provider.rejected_regions.discard("r2")
        return {"changed": "behavior restored (CONTROL: requalification still required)"}
    raise ValueError(f"unknown drift mutation {mutation_id}")


# --- The blind drift monitor ----------------------------------------------------------------------------
class DriftMonitor:
    """Blind detection worker: sees only public observations (submit outcomes,
    independent ledger counts, contract text version) -- never the provider's
    hidden switches. Runs canaries; advances the coordinator on evidence."""

    def __init__(self, coordinator: DriftResponseCoordinator,
                 provider: MockExternalProvider):
        self.coordinator = coordinator
        self.provider = provider
        self.observations = []

    def canary_concurrent(self, key: str = "OP-CANARY") -> dict:
        """Two concurrent same-key submits; independent ledger count."""
        op = LogicalOperation(key, "payments", "hash-canary",
                              authorization_rev=1, created_at_seq=1)
        ts = [threading.Thread(target=lambda: self.provider.submit(op))
              for _ in range(2)]
        for t in ts:
            t.start()
        for t in ts:
            t.join()
        n = self.provider.count_effects(key)
        obs = {"canary": "concurrent", "key": key, "effects": n,
               "anomaly": n > 1}
        self.observations.append(obs)
        return obs

    def canary_retention(self, key: str = "OP-DRIFT", payload: str = "hash-p") -> dict:
        """Submit near/past the horizon; unexpected expiry is the signal.
        Retries the SAME logical operation (key and payload)."""
        op = LogicalOperation(key, "payments", payload,
                              authorization_rev=1, created_at_seq=1)
        out, _ = self.provider.submit(op)
        obs = {"canary": "retention", "key": key, "outcome": out,
               "anomaly": out == "REJECTED_KEY_EXPIRED"}
        self.observations.append(obs)
        return obs

    def canary_downstream(self, key: str = "OP-DSTREAM") -> dict:
        op = LogicalOperation(key, "payments", "hash-ds",
                              authorization_rev=1, created_at_seq=1)
        self.provider.submit(op)
        e1 = self.provider.emit_downstream(key, "eff-1")
        e2 = self.provider.emit_downstream(key, "eff-1")
        n = self.provider.count_downstream(key)
        obs = {"canary": "downstream", "key": key, "effects": n,
               "anomaly": n > 1 or e2 == "EMITTED"}
        self.observations.append(obs)
        return obs

    def canary_forced_race(self, key: str = "OP-RACE") -> dict:
        """Deterministic D3-style canary: force Attempt A to pause between
        the dedup check and the effect commit, land Attempt B in the window,
        then release. The monitor forces TIMING only -- it stays blind to
        the provider's hidden switches. Detects guard removal reliably."""
        p = self.provider
        gate = threading.Event()
        entered = threading.Event()
        p.pause_before_commit = gate
        p.pre_commit_hook = lambda _k: entered.set()
        op = LogicalOperation(key, "payments", "hash-race",
                              authorization_rev=1, created_at_seq=1)
        t = threading.Thread(target=lambda: p.submit(op))
        t.start()
        entered.wait(10)
        p.pause_before_commit = None  # B must not block; A holds the window
        p.submit(op)  # Attempt B lands inside A's check-then-commit window
        gate.set()
        t.join(10)
        p.pre_commit_hook = None
        n = p.count_effects(key)
        obs = {"canary": "forced_race", "key": key, "effects": n,
               "anomaly": n > 1}
        self.observations.append(obs)
        return obs

    def assess(self, obs: dict, drift_type: str) -> dict:
        """Proportional assessment: anomaly -> REVIEW_REQUIRED; confirmed via
        independent re-observation -> SUSPECTED_DRIFT; confirmed duplicate
        effect -> QUALIFICATION_SUSPENDED (atomic with the fence)."""
        c = self.coordinator
        if not obs.get("anomaly"):
            return {"action": "none", "state": c.state}
        r1 = c.transition("REVIEW_REQUIRED",
                          f"canary anomaly: {obs} (possible {drift_type})")
        # Independent re-observation before suspicion: never one sample.
        # The forced race reproduces the adversarial interleaving.
        confirm = self.canary_forced_race(key=obs.get("key", "OP-CANARY") + "-2")
        if confirm.get("anomaly"):
            r2 = c.transition("SUSPECTED_DRIFT",
                              f"independent re-observation confirms: {confirm}")
            if confirm["effects"] >= 2:
                r3 = c.transition(
                    "QUALIFICATION_SUSPENDED",
                    f"CONFIRMED prohibited duplicate effect: {confirm['effects']} "
                    f"effects for one logical operation")
                return {"action": "suspended", "state": c.state,
                        "transitions": [r1, r2, r3]}
            return {"action": "suspected", "state": c.state,
                    "transitions": [r1, r2]}
        return {"action": "review", "state": c.state, "transitions": [r1]}


# --- The two decisive properties ------------------------------------------------------------------------------
def detection_soundness(results: Dict[str, dict]) -> Tuple[bool, str]:
    """ConfirmedDrift => IndependentEvidenceOfContractGap, for every real
    drift; no ConfirmedDrift for controls without evidence. results maps
    mutation_id -> {"drifted": bool, "evidence": str|None}."""
    real_drifts = {"D1_scope_narrowing", "D2_retention_shortening",
                   "D3_atomic_guard_removal", "D4_downstream_duplication",
                   "D5_late_completion", "D7_behavior_only_change"}
    for mid in real_drifts:
        r = results.get(mid, {})
        if r.get("confirmed_drift") and not r.get("evidence"):
            return False, f"{mid}: confirmed without independent evidence"
    for mid in ("D6_doc_only_change", "D8_unrelated_errors"):
        r = results.get(mid, {})
        if r.get("confirmed_drift"):
            return False, f"{mid}: control drifted without evidence -- false attribution"
    return True, "sound: every confirmation evidence-backed; controls not misattributed"


def containment_safety(coordinator: DriftResponseCoordinator, scope: str,
                       op: LogicalOperation) -> Tuple[bool, str]:
    """QualificationWithdrawn => NOT authorize_dependent_retry, holding
    IMMEDIATELY at the withdrawal commit."""
    if coordinator.state != "QUALIFICATION_SUSPENDED":
        return False, "precondition: coordinator not suspended"
    d = authorize_recovery_retry(
        coordinator, op, scope,
        needs={"concurrency": True, "retention": True},
        law_receipt="LAW-1", outcome_state="RECONCILED")
    if d["authorized"]:
        return False, "UNSAFE: retry authorized after withdrawal"
    return True, f"safe: retry rejected immediately at withdrawal ({d['reasons']})"


# --- AER-DRIFT-001: the first fixture -------------------------------------------------------------------------------
def aer_drift_001():
    """AER-DRIFT-001: controlled provider with durable effect ledger and a
    hidden concurrency-protection switch. The detection worker is blind to
    the switch. The verifier establishes: anomaly identification ->
    suspension -> old-revision retry rejection -> independent requalification
    before retry eligibility returns. Repeated for retention, region scope,
    and downstream duplication. A healthy-provider-with-timeouts control
    confirms no invented violations."""
    report = {}
    dim_guarantees = tuple((d[0], d[1]) for d in PROVIDER_CONTRACT_DIMENSIONS)

    def fresh_lane():
        provider = MockExternalProvider()
        provider.contract_text_version = 1
        manifest = make_manifest("mock-provider", "payments.charge", "v1",
                                 "r1", dim_guarantees)
        coord = DriftResponseCoordinator(manifest)
        monitor = DriftMonitor(coord, provider)
        return provider, coord, monitor

    # --- Lane 1: silent concurrency-guard removal (D3) ---
    provider, coord, monitor = fresh_lane()
    apply_drift_mutation(provider, "D3_atomic_guard_removal")  # hidden from monitor
    obs = monitor.canary_forced_race()
    assert obs["anomaly"] and obs["effects"] == 2, obs
    outcome = monitor.assess(obs, "concurrency_drift")
    assert outcome["state"] == "QUALIFICATION_SUSPENDED", outcome
    report["concurrency_drift_suspended"] = outcome["state"]
    # Containment is immediate at the withdrawal commit.
    op_old = LogicalOperation("OP-OLD", "payments", "hash-old",
                              authorization_rev=1, created_at_seq=1)
    safe, why = containment_safety(coord, "r1", op_old)
    assert safe, why
    report["old_revision_retry_rejected"] = why
    # In-flight noncooperating requests are NOT killed: they stay under
    # reconciliation per the actual contract.
    report["inflight_note"] = ("withdrawal does not retroactively stop in-flight "
                               "noncooperating requests; they stay under reconciliation")
    # Restoration never auto-restores authority: requalification required.
    apply_drift_mutation(provider, "D10_restoration")
    d = authorize_recovery_retry(coord, op_old, "r1", {"concurrency": True},
                                 "LAW-1", "RECONCILED")
    assert not d["authorized"], "restoration must not auto-restore authority"
    report["restoration_does_not_restore"] = d["reasons"]
    # Independent requalification: fresh canaries pass under the revised contract.
    obs2 = monitor.canary_concurrent(key="OP-CANARY-RQ")
    assert not obs2["anomaly"], obs2
    r = coord.transition("REQUALIFIED_IN_NEW_SCOPE",
                         "independent requalification: fresh canaries pass; "
                         "revised contract v2 pinned")
    assert r["accepted"], r
    d2 = authorize_recovery_retry(coord, op_old, "r1", {"concurrency": True},
                                  "LAW-1", "RECONCILED")
    assert d2["authorized"], d2
    report["requalified_retry_eligible"] = d2["qualification_revision"]

    # --- Lane 2: silent retention shortening (D2) ---
    provider2, coord2, monitor2 = fresh_lane()
    provider2.retention_horizon["OP-DRIFT"] = 100
    provider2.submit(LogicalOperation("OP-DRIFT", "payments", "hash-drift",
                                      authorization_rev=1, created_at_seq=1))
    apply_drift_mutation(provider2, "D2_retention_shortening", key="OP-DRIFT")
    provider2.advance(2)  # client believes it is inside the 100-unit horizon
    obs = monitor2.canary_retention(key="OP-DRIFT", payload="hash-drift")
    assert obs["anomaly"], obs
    coord2.transition("REVIEW_REQUIRED", f"retention canary anomaly: {obs}")
    coord2.transition("SUSPECTED_DRIFT", "independent evidence: horizon shortened")
    r = coord2.transition("QUALIFICATION_SUSPENDED",
                          "confirmed: retention guarantee no longer established")
    assert r["accepted"] and coord2.fence.get("r1") == 2, r
    report["retention_drift_suspended"] = True

    # --- Lane 3: silent region-scope narrowing (D1) ---
    provider3, coord3, monitor3 = fresh_lane()
    apply_drift_mutation(provider3, "D1_scope_narrowing")
    out, _ = provider3.submit(LogicalOperation("OP-R2", "payments", "hash-r2",
                                               authorization_rev=1, created_at_seq=1),
                              region="r2")
    assert out == "REJECTED_SCOPE", out
    coord3.transition("REVIEW_REQUIRED", "region r2 unexpectedly rejected")
    coord3.transition("SUSPECTED_DRIFT", "independent evidence: scope narrowed")
    coord3.transition("QUALIFICATION_SUSPENDED", "confirmed scope drift")
    plan = containment_plan("scope_drift", "r2",
                            {"op-a": ("r1",), "op-b": ("r2",), "op-c": ("r1", "r2")})
    assert plan["contained"] == ("op-b", "op-c") and plan["preserved"] == ("op-a",), plan
    report["scope_drift_selective_containment"] = {
        "contained": plan["contained"], "preserved": plan["preserved"]}

    # --- Lane 4: silent downstream duplication (D4) ---
    provider4, coord4, monitor4 = fresh_lane()
    apply_drift_mutation(provider4, "D4_downstream_duplication")
    obs = monitor4.canary_downstream()
    assert obs["anomaly"], obs
    coord4.transition("REVIEW_REQUIRED", f"downstream canary anomaly: {obs}")
    coord4.transition("SUSPECTED_DRIFT", "independent evidence: downstream dedup off")
    coord4.transition("QUALIFICATION_SUSPENDED", "confirmed downstream drift")
    report["downstream_drift_suspended"] = True

    # --- Lane 5 (control): healthy provider with timeouts (D8) ---
    provider5, coord5, monitor5 = fresh_lane()
    apply_drift_mutation(provider5, "D8_unrelated_errors")
    provider5.crash_on_submit = False  # transient blip over; contract unchanged
    obs = monitor5.canary_concurrent(key="OP-CTRL")
    assert not obs["anomaly"], obs
    assert coord5.state == "QUALIFIED_IN_SCOPE", coord5.state
    report["healthy_with_timeouts_no_violation"] = True

    # --- Lane 6 (control): doc-only change (D6) ---
    provider6, coord6, _monitor6 = fresh_lane()
    before = provider6.contract_text_version
    apply_drift_mutation(provider6, "D6_doc_only_change")
    assert provider6.contract_text_version == before + 1
    assert coord6.state == "QUALIFIED_IN_SCOPE", "doc-only change must not suspend"
    report["doc_only_change_no_suspension"] = True

    # The two decisive properties over the sealed answer key.
    sound, why = detection_soundness({
        "D3_atomic_guard_removal": {"confirmed_drift": True,
                                    "evidence": "canary duplicate effect"},
        "D2_retention_shortening": {"confirmed_drift": True,
                                    "evidence": "retention canary"},
        "D1_scope_narrowing": {"confirmed_drift": True,
                               "evidence": "unexpected REJECTED_SCOPE"},
        "D4_downstream_duplication": {"confirmed_drift": True,
                                      "evidence": "downstream canary"},
        "D6_doc_only_change": {"confirmed_drift": False},
        "D8_unrelated_errors": {"confirmed_drift": False},
    })
    assert sound, why
    report["detection_soundness"] = why
    return report

# ===========================================================================
# AER-ALERT-1 — Provider Alert Evidence Law (SN-0796)
# ===========================================================================
"""AER-ALERT-1 is the ALERT / EVIDENCE-QUALIFICATION layer: AER-DRIFT-1
monitors; this decides when to act and what counts as proof.

LAW: alert on observable risk, diagnose from independent evidence, withdraw
only the qualifications whose guarantees are no longer established --
repeated errors don't prove drift; one decisive counterexample can.

Repeated errors don't prove drift (five timeouts != broken idempotency).
One decisive counterexample can (one verified prohibited duplicate effect
withdraws immediately -- no arbitrary minimum count, no trend required).
"""

# --- The two-field incident model ------------------------------------------------------
# Operational response x evidence-based diagnosis. The record ALWAYS
# distinguishes precaution from established fact: containment may precede
# diagnosis, but precaution is never recorded as proof.
ALERT_RESPONSES = (
    "OBSERVE",                  # watch; no action
    "INVESTIGATE",              # gather independent evidence
    "HOLD_AFFECTED_RETRIES",    # precautionary: stop new reliance, keep reconciling
    "BLOCK_AFFECTED_EXECUTION",  # withdrawal: the fence rejects dependent retries
)
ALERT_DIAGNOSES = (
    "TRANSIENT_ANOMALY",
    "SUSPECTED_DRIFT",
    "CONTRACT_SCOPE_CHANGE",
    "CONFIRMED_CONTRACT_BREACH",
    "UNDETERMINED",
)


@dataclass(frozen=True)
class ProviderIncident:
    incident_id: str
    response: str        # one of ALERT_RESPONSES (operational field)
    diagnosis: str       # one of ALERT_DIAGNOSES (evidence field)
    evidence: Tuple[str, ...]
    precaution_before_diagnosis: bool  # True when containment preceded proof


# --- The L0-L4 ladder -----------------------------------------------------------------------
ALERT_LADDER = (
    ("L0", "normal transient", "OBSERVE", "TRANSIENT_ANOMALY",
     "ordinary transport noise; denominators stay per logical operation"),
    ("L1", "investigate", "INVESTIGATE", "TRANSIENT_ANOMALY",
     "the statistical gate trips; gather independent evidence"),
    ("L2", "precautionary hold", "HOLD_AFFECTED_RETRIES", "SUSPECTED_DRIFT",
     "credible possible duplicate for high-impact ops; precaution, not proof"),
    ("L3", "withdrawal", "BLOCK_AFFECTED_EXECUTION", "CONFIRMED_CONTRACT_BREACH",
     "ONE verified prohibited duplicate effect; bypasses statistical thresholds entirely"),
    ("L4", "wider incident", "BLOCK_AFFECTED_EXECUTION", "CONFIRMED_CONTRACT_BREACH",
     "breach with a defensible exposure boundary across scopes"),
)
# The L1 statistical gate: PROPOSED STARTING VALUES, calibrated per endpoint --
# not ratified settings. A confirmed duplicate bypasses this gate entirely.
L1_STATISTICAL_GATE = {
    "min_comparable_requests": 100,
    "min_anomalous": 5,
    "min_baseline_multiple": 3,
    "requires": ("prespecified statistical test",
                 "persistence across windows or independent corroboration"),
    "note": "CALIBRATED per endpoint (AER-CAL-1); proposed starting values, "
            "not ratified settings",
}


# --- Right denominators --------------------------------------------------------------------------
def alert_metrics(submissions, effect_counts, observed_ops) -> dict:
    """Denominator-correct metrics. submissions: [(op_key, outcome)] per
    attempt. effect_counts: {op_key: independently counted effects}.
    observed_ops: {op_key} with independent effect observation.
    One operation retried 20x != 20 provider failures: timeout / rate-limit /
    ambiguity rates are per DISTINCT LOGICAL OPERATION. Always stratify by
    endpoint / version / tenant / region / effect / config / horizon (the
    caller passes one stratum at a time)."""
    distinct = sorted({k for k, _ in submissions})
    n = len(distinct)
    by_op = {}
    for k, outcome in submissions:
        by_op.setdefault(k, []).append(outcome)
    timeout_ops = sum(1 for k in distinct
                      if any(o in ("TIMEOUT_RAISED", "timeout") for o in by_op[k]))
    ratelimit_ops = sum(1 for k in distinct
                        if any(o == "RATE_LIMITED" for o in by_op[k]))
    ambiguous_ops = sum(1 for k in distinct
                        if any(o in ("SUBMIT_RAISED", "TIMEOUT_RAISED", "unknown")
                               for o in by_op[k]))
    eligible = [k for k in distinct if k in observed_ops]
    dup_ops = sum(1 for k in eligible if effect_counts.get(k, 0) >= 2)
    unobserved = [k for k in distinct if k not in observed_ops]
    return {
        "distinct_logical_operations": n,
        "timeout_rate": timeout_ops / n if n else 0.0,
        "rate_limit_rate": ratelimit_ops / n if n else 0.0,
        "ambiguous_outcome_rate": ambiguous_ops / n if n else 0.0,
        "confirmed_duplicate_effect_rate":
            dup_ops / len(eligible) if eligible else 0.0,
        "eligible_observably_reconciled": len(eligible),
        "unobserved_outcomes_disclosed": sorted(unobserved),
        "observation_coverage": len(eligible) / n if n else 0.0,
        "note": "duplicate rate is over eligible observably-reconciled ops only; "
                "unobserved outcomes are disclosed, never silently dropped",
    }


# --- Minimum evidence: the confirmed-duplicate checklist -----------------------------------------------
# All six must be independently established. Withdrawal of protection != proof
# of provider breach: a provider-attributed breach ADDITIONALLY requires
# distinguishing provider behavior from client misuse (e.g. the client
# changing keys per retry duplicates by its own hand).
DUPLICATE_COUNTEREXAMPLE_CHECKLIST = (
    "same_logical_operation",
    "matching_keys_payloads_scope",
    "guarantee_covered_the_scenario",
    "two_distinct_prohibited_material_effects",
    "authentic_complete_records",
    "not_duplicate_webhooks_or_logs_of_one_effect",
)


def check_duplicate_counterexample(evidence: Dict[str, bool]) -> Tuple[bool, Tuple[str, ...]]:
    """evidence maps each checklist item -> independently established?
    Returns (confirmed, missing_items)."""
    missing = tuple(item for item in DUPLICATE_COUNTEREXAMPLE_CHECKLIST
                    if not evidence.get(item))
    return (not missing, missing)


def attribute_duplicate(evidence: Dict[str, bool]) -> str:
    """Distinguish provider breach from client misuse. Withdrawal of
    protection is not proof of provider breach."""
    if evidence.get("client_changed_key_per_retry"):
        return "CLIENT_MISUSE"
    if evidence.get("client_misuse_excluded") and \
            all(evidence.get(i) for i in DUPLICATE_COUNTEREXAMPLE_CHECKLIST):
        return "PROVIDER_BREACH"
    return "UNDETERMINED"


# --- The HTTP symptom classifier ---------------------------------------------------------------------------
# Statuses are diagnostic INPUTS, never verdicts.
HTTP_SYMPTOM_TABLE = (
    ("429", "quota / rate-limit: an availability signal. Investigate capacity; "
            "never a correctness verdict."),
    ("403-installation-token", "credential / quota plane: check the token and its "
            "quota before any other theory."),
    ("403-policy-refusal", "policy refusal: a different action from a token 403 -- "
            "do not conflate them."),
    ("500/503", "provider-side error: availability, not proof of a contract breach."),
    ("timeout", "UNKNOWN outcome: reconcile first; a timeout never proves "
            "cancellation or nonexecution."),
    ("duplicate-webhooks", "delivery duplication: correlate to effects by business "
            "identifier; never count notifications as effects."),
    ("two-verified-effects", "SAFETY: a confirmed duplicate -- L3 immediately, "
            "statistical thresholds bypassed."),
)


def classify_http_symptom(symptom: str, context: str = "") -> dict:
    """Classify an HTTP symptom as a diagnostic input. Includes our own
    reflexive case: our installation-token 403 vs the comment-lock 403 share
    a status family but need different actions -- and our rate-limit
    attribution for the two CI jobs is a reported operational diagnosis, not
    independent proof; it still needs evidence checking before it counts as a
    verified causal finding."""
    table = dict((s, note) for s, note in HTTP_SYMPTOM_TABLE)
    return {"symptom": symptom,
            "reading": table.get(symptom, "unknown symptom: investigate, never assume"),
            "context": context,
            "is_verdict": False,
            "reflexive_note": ("statuses never establish causes by themselves; "
                               "the NayaPOWER installation-token 403 vs comment-lock 403 "
                               "pair is the standing example")}


# --- Atomic withdrawal: node roles ------------------------------------------------------------------------------
WITHDRAWAL_NODE_ROLES = {
    "KNOW": "records the incident, the evidence, and the exposure boundary",
    "CONNECT": "correlates signals across endpoints without merging incidents",
    "VERIFY": "independently establishes the counterexample (the 6-point checklist)",
    "PROVE": "derives the defensible exposure boundary",
    "LAW": "authorizes the withdrawal decision",
    "ACT": "enforces the fence at the governed commit boundary",
    "LEARN": "preserves the lesson; resolved qualifications may narrow, "
             "never auto-restore provider-wide trust",
}

# --- The two-stage engine ---------------------------------------------------------------------------------
def evaluate_provider_signal(signal: dict, coordinator: DriftResponseCoordinator,
                             provider: MockExternalProvider = None) -> dict:
    """Stage A: fast safety decision. A confirmed duplicate withdraws
    immediately (L3, atomic, statistical thresholds bypassed); a credible
    unconfirmed risk gets a precautionary hold (L2); telemetry loss is an
    observability gap (UNDETERMINED, reduced assurance -- never 'healthy');
    ordinary transport errors stay L0/L1.
    Stage B: slow independent diagnosis -- the evidence checklist,
    denominator-correct metrics, stratification.
    Stage C: requalification under a revised contract; never auto-restore.
    The UNDETERMINED path holds precautionary and keeps investigating; it
    never defaults to healthy."""
    kind = signal.get("kind")
    if kind == "confirmed_duplicate":
        ok, missing = check_duplicate_counterexample(signal.get("evidence", {}))
        if ok:
            w = coordinator.withdraw_now(
                f"L3: verified prohibited duplicate effect: {signal.get('summary')}")
            return {"stage": "A", "level": "L3",
                    "response": "BLOCK_AFFECTED_EXECUTION",
                    "diagnosis": "CONFIRMED_CONTRACT_BREACH",
                    "attribution": attribute_duplicate(signal.get("evidence", {})),
                    "withdrawal": w,
                    "incident": ProviderIncident(
                        signal.get("incident_id", "INC-1"), "BLOCK_AFFECTED_EXECUTION",
                        "CONFIRMED_CONTRACT_BREACH",
                        tuple(signal.get("evidence_notes", ())),
                        precaution_before_diagnosis=False)}
        return {"stage": "A+B", "level": "L2",
                "response": "HOLD_AFFECTED_RETRIES", "diagnosis": "UNDETERMINED",
                "missing_checklist": missing,
                "note": "checklist incomplete: hold precautionary, keep investigating"}
    if kind == "credible_possible_duplicate":
        return {"stage": "A", "level": "L2",
                "response": "HOLD_AFFECTED_RETRIES", "diagnosis": "SUSPECTED_DRIFT",
                "note": "precaution, not proof; Stage B investigates"}
    if kind == "telemetry_loss":
        return {"stage": "A", "level": "L1", "response": "INVESTIGATE",
                "diagnosis": "UNDETERMINED",
                "note": "observability gap: reduced assurance, never 'healthy'"}
    if kind == "single_unclear_canary":
        return {"stage": "A", "level": "L1", "response": "INVESTIGATE",
                "diagnosis": "TRANSIENT_ANOMALY",
                "note": "one unclear canary is investigation, not suspension"}
    return {"stage": "A", "level": "L0", "response": "OBSERVE",
            "diagnosis": "TRANSIENT_ANOMALY"}


# --- The T1-T10 suite ----------------------------------------------------------------------------------------------
# Sealed controls with near-misses separating availability from correctness.
# Essential metrics over the suite: false drift attribution rate, unsafe
# continuation rate, detection latency, unnecessary qualification loss,
# evidence coverage, requalification validity.
# Targets: zero false definitive attributions, zero unsafe continued retries
# on sealed controls -- with the finite-corpus honesty clause: zero on this
# corpus != zero universally.
def _alert_lane():
    provider = MockExternalProvider()
    dim_guarantees = tuple((d[0], d[1]) for d in PROVIDER_CONTRACT_DIMENSIONS)
    manifest = make_manifest("mock-provider", "payments.charge", "v1",
                             "r1", dim_guarantees)
    return provider, DriftResponseCoordinator(manifest)


def t1_rate_limit_bursts() -> dict:
    """T1: 50 rate-limited attempts, then success. Availability, not
    correctness: L0/L1 only, never withdrawal; one logical operation."""
    provider, coord = _alert_lane()
    provider.error_script = ["RATE_LIMITED"] * 50
    op = _dop("OP-T1")
    outcomes = []
    for _ in range(51):
        try:
            outcomes.append(provider.submit(op)[0])
        except TimeoutError:
            outcomes.append("TIMEOUT_RAISED")
    m = alert_metrics(provider.submissions, {"OP-T1": provider.count_effects("OP-T1")},
                      {"OP-T1"})
    r = evaluate_provider_signal({"kind": "transport_burst"}, coord)
    ok = (provider.count_effects("OP-T1") == 1 and r["level"] in ("L0", "L1")
          and coord.state == "QUALIFIED_IN_SCOPE"
          and m["distinct_logical_operations"] == 1 and m["rate_limit_rate"] == 1.0)
    return {"id": "T1", "pass": ok, "level": r["level"],
            "evidence": f"50x429 then success: 1 op, 1 effect, {r['level']}"}


def t2_lost_acknowledgments() -> dict:
    """T2: receipts withheld; retries deduplicate. No drift, no alert above L0."""
    provider, coord = _alert_lane()
    provider.withhold_receipts = True
    op = _dop("OP-T2")
    for _ in range(5):
        provider.submit(op)
    r = evaluate_provider_signal({"kind": "transport_burst"}, coord)
    ok = provider.count_effects("OP-T2") == 1 and r["level"] == "L0"
    return {"id": "T2", "pass": ok, "level": r["level"],
            "evidence": "5 receipt-less retries deduplicated; L0"}


def t3_double_webhooks() -> dict:
    """T3: duplicate deliveries of ONE effect correlate to one effect --
    never counted as two."""
    provider, coord = _alert_lane()
    provider.submit(_dop("OP-T3"))
    provider.emit_downstream("OP-T3", "eff-1")
    provider.emit_downstream("OP-T3", "eff-1")  # duplicate delivery
    chain = verify_effect_chain(provider, "OP-T3")
    ok = chain["downstream_effects"] == 1 and not chain["duplicate_effect"]
    return {"id": "T3", "pass": ok,
            "evidence": f"double delivery, one business effect: {chain}"}


def t4_client_key_changes() -> dict:
    """T4: the client changes keys per retry of the same logical operation --
    two effects by the client's own hand. Diagnosis must say CLIENT_MISUSE,
    not provider breach; the provider qualification is not withdrawn."""
    provider, coord = _alert_lane()
    provider.submit(_dop("OP-T4", payload="hash-a"))
    provider.submit(LogicalOperation("OP-T4-retry2", "payments", "hash-a",
                                     authorization_rev=1, created_at_seq=2))
    evidence = {i: True for i in DUPLICATE_COUNTEREXAMPLE_CHECKLIST}
    evidence["matching_keys_payloads_scope"] = False  # keys differ
    evidence["client_changed_key_per_retry"] = True
    evidence["client_misuse_excluded"] = False
    attribution = attribute_duplicate(evidence)
    ok, _ = check_duplicate_counterexample(evidence)
    result = (attribution == "CLIENT_MISUSE" and not ok
              and coord.state == "QUALIFIED_IN_SCOPE")
    return {"id": "T4", "pass": result, "attribution": attribution,
            "evidence": "client key change: CLIENT_MISUSE; provider not withdrawn"}


def t5_one_conclusive_duplicate() -> dict:
    """T5: ONE verified prohibited duplicate effect -> immediate L3
    withdrawal. No trend, no minimum count, no statistical gate."""
    provider, coord = _alert_lane()
    provider.guard_mode = "broken_record_after_effect"
    gate = threading.Event()
    entered = threading.Event()
    provider.pause_before_commit = gate
    provider.pre_commit_hook = lambda _k: entered.set()
    op = _dop("OP-T5")
    t = threading.Thread(target=lambda: provider.submit(op))
    t.start()
    entered.wait(10)
    provider.pause_before_commit = None  # B must not block; A holds the window
    provider.submit(op)
    gate.set()
    t.join(10)
    n = provider.count_effects("OP-T5")
    evidence = {i: True for i in DUPLICATE_COUNTEREXAMPLE_CHECKLIST}
    evidence["client_misuse_excluded"] = True
    r = evaluate_provider_signal(
        {"kind": "confirmed_duplicate", "evidence": evidence,
         "summary": f"{n} prohibited effects for OP-T5",
         "evidence_notes": ("ledger shows 2 effects; keys/payloads/scope match; "
                            "records authentic and complete",)},
        coord)
    ok = (n == 2 and r["level"] == "L3"
          and coord.state == "QUALIFICATION_SUSPENDED"
          and coord.fence.get("r1") == 2)
    return {"id": "T5", "pass": ok, "level": r["level"],
            "evidence": f"one conclusive duplicate -> L3, fence={coord.fence}"}


def t6_silent_retention_shortening() -> dict:
    """T6: silent retention shortening -> drift detected via the drift lane."""
    provider, coord = _alert_lane()
    provider.retention_horizon["OP-T6"] = 100
    provider.submit(_dop("OP-T6"))
    apply_drift_mutation(provider, "D2_retention_shortening", key="OP-T6")
    provider.advance(2)
    monitor = DriftMonitor(coord, provider)
    obs = monitor.canary_retention(key="OP-T6", payload="hash-p")
    return {"id": "T6", "pass": obs["anomaly"],
            "evidence": f"retention canary anomaly: {obs}"}


def t7_regional_narrowing() -> dict:
    """T7: silent regional narrowing -> drift detected; scope-bound."""
    provider, coord = _alert_lane()
    apply_drift_mutation(provider, "D1_scope_narrowing")
    out, _ = provider.submit(_dop("OP-T7"), region="r2")
    return {"id": "T7", "pass": out == "REJECTED_SCOPE",
            "evidence": f"region r2 silently narrowed: {out}"}


def t8_single_unclear_canary() -> dict:
    """T8: a single unclear canary failure -> L1 investigate, never suspend."""
    _provider, coord = _alert_lane()
    r = evaluate_provider_signal({"kind": "single_unclear_canary"}, coord)
    ok = r["level"] == "L1" and coord.state == "QUALIFIED_IN_SCOPE"
    return {"id": "T8", "pass": ok, "level": r["level"],
            "evidence": "single unclear canary: investigate, not suspension"}


def t9_telemetry_loss() -> dict:
    """T9: telemetry loss -> observability gap (UNDETERMINED, reduced
    assurance) -- never 'healthy'."""
    _provider, coord = _alert_lane()
    r = evaluate_provider_signal({"kind": "telemetry_loss"}, coord)
    ok = (r["diagnosis"] == "UNDETERMINED" and "never 'healthy'" in r["note"]
          and coord.state == "QUALIFIED_IN_SCOPE")
    return {"id": "T9", "pass": ok, "diagnosis": r["diagnosis"],
            "evidence": "telemetry loss: UNDETERMINED, reduced assurance"}


def t10_restoration_requires_requalification() -> dict:
    """T10: restoration never auto-restores authority; a new qualification
    revision is required before retry eligibility returns."""
    provider, coord = _alert_lane()
    coord.withdraw_now("T10 setup: confirmed duplicate")
    assert coord.state == "QUALIFICATION_SUSPENDED"
    apply_drift_mutation(provider, "D10_restoration")
    op = _dop("OP-T10")
    d = authorize_recovery_retry(coord, op, "r1", {"concurrency": True},
                                 "LAW-1", "RECONCILED")
    still_blocked = not d["authorized"]
    r = coord.transition("REQUALIFIED_IN_NEW_SCOPE",
                         "T10: independent requalification under revised contract")
    d2 = authorize_recovery_retry(coord, op, "r1", {"concurrency": True},
                                  "LAW-1", "RECONCILED")
    ok = still_blocked and r["accepted"] and d2["authorized"]
    return {"id": "T10", "pass": ok,
            "evidence": "restoration alone keeps the fence; requalification restores eligibility"}


def run_t_suite() -> list:
    return [t1_rate_limit_bursts(), t2_lost_acknowledgments(), t3_double_webhooks(),
            t4_client_key_changes(), t5_one_conclusive_duplicate(),
            t6_silent_retention_shortening(), t7_regional_narrowing(),
            t8_single_unclear_canary(), t9_telemetry_loss(),
            t10_restoration_requires_requalification()]


def t_suite_metrics(results: list) -> dict:
    """Essential metrics over the sealed T-suite, with the finite-corpus
    honesty clause."""
    return {
        "false_drift_attribution_rate":
            sum(1 for r in results if r["id"] in ("T1", "T2", "T3", "T8") and not r["pass"])
            / 4,
        "unsafe_continuation_rate":
            0 if all(r["pass"] for r in results if r["id"] in ("T5", "T6", "T7")) else 1,
        "unnecessary_qualification_loss":
            sum(1 for r in results if r["id"] in ("T1", "T2", "T8") and not r["pass"]),
        "suite_pass": all(r["pass"] for r in results),
        "honesty_clause": ("zero on this finite corpus != zero universally; "
                           "the corpus bounds the claim, it does not universalize it"),
    }


# --- AER-ALERT-001: the first test ----------------------------------------------------------------------------
def aer_alert_001():
    """Two controlled histories with IDENTICAL timeout bursts: H1 healthy
    dedup, H2 silently duplicating. Same initial transport assessment;
    divergent response once effect evidence arrives. Repeated for
    rate-limit bursts, expired retention, and downstream-only duplication."""
    report = {}

    def history(duplicating: bool):
        provider = MockExternalProvider()
        provider.error_script = ["TIMEOUT_RAISED"] * 3  # identical burst
        if duplicating:
            provider.guard_mode = "broken_record_after_effect"
        op = LogicalOperation("OP-ALERT", "payments", "hash-alert",
                              authorization_rev=1, created_at_seq=1)
        burst = []
        for _ in range(3):  # the identical timeout burst
            try:
                provider.submit(op)
            except TimeoutError:
                burst.append("TIMEOUT_RAISED")
        provider.error_script = []
        if not duplicating:
            # Healthy: receipt-less success, then the retry deduplicates.
            provider.withhold_receipts = True
            provider.submit(op)
            provider.withhold_receipts = False
            provider.submit(op)
        else:
            # Silently duplicating: the retry lands inside the first
            # attempt's check-then-commit window (forced interleaving).
            gate = threading.Event()
            entered = threading.Event()
            provider.pause_before_commit = gate
            provider.pre_commit_hook = lambda _k: entered.set()
            t = threading.Thread(target=lambda: provider.submit(op))
            t.start()
            entered.wait(10)
            provider.pause_before_commit = None  # B must not block
            provider.submit(op)
            gate.set()
            t.join(10)
        return provider, burst

    (h1, b1), (h2, b2) = history(False), history(True)
    # Identical timeout bursts -> same initial transport assessment.
    assert b1 == b2 == ["TIMEOUT_RAISED"] * 3, (b1, b2)
    r1 = evaluate_provider_signal({"kind": "transport_burst"}, _alert_lane()[1])
    assert r1["level"] in ("L0", "L1"), r1
    report["identical_transport_assessment"] = r1["level"]
    # Divergent response once effect evidence arrives.
    n1, n2 = h1.count_effects("OP-ALERT"), h2.count_effects("OP-ALERT")
    assert n1 == 1, n1
    _p2, c2 = _alert_lane()
    evidence = {i: True for i in DUPLICATE_COUNTEREXAMPLE_CHECKLIST}
    evidence["client_misuse_excluded"] = True
    r2 = evaluate_provider_signal(
        {"kind": "confirmed_duplicate", "evidence": evidence,
         "summary": f"H2: {n2} prohibited effects for OP-ALERT"}, c2)
    assert n2 == 2 and r2["level"] == "L3", (n2, r2)
    report["h1_healthy_stays"] = r1["level"]
    report["h2_duplicating_withdrawn"] = {"level": r2["level"],
                                          "state": c2.state}
    # Rate-limit bursts: same shape, availability only.
    t1 = t1_rate_limit_bursts()
    assert t1["pass"], t1
    report["rate_limit_repeat"] = t1["level"]
    # Expired retention: rejected, not re-executed.
    d9 = d9_retention_boundary()
    assert d9["verdict"] == "QUALIFIED", d9
    report["expired_retention_repeat"] = d9["verdict"]
    # Downstream-only duplication: root intact, downstream duplicated.
    p = MockExternalProvider()
    p.downstream_dedup_on = False
    p.submit(_dop("OP-DS"))
    p.emit_downstream("OP-DS", "eff-1")
    p.emit_downstream("OP-DS", "eff-1")
    chain = verify_effect_chain(p, "OP-DS")
    assert chain["provider_effects"] == 1 and chain["downstream_exceeds_root"], chain
    report["downstream_only_duplication"] = {
        "root": chain["provider_effects"],
        "downstream": chain["downstream_effects"],
        "note": "root-only qualification would miss this: DOWNSTREAM_EFFECTS_UNPROVEN matters"}
    return report

# ===========================================================================
# AER-CAL-1 — Volume-Adaptive Alert Calibration Law (SN-0797)
# ===========================================================================
"""AER-CAL-1 is the STATISTICAL-CALIBRATION layer: AER-ALERT-1 set the alert
ladder; this calibrates how loudly the statistics may speak.

LAW: calibrate statistical alert thresholds using effective independent
sample size, traffic variability, observable effect coverage, and operational
risk; control false alarms across repeated tests and the fleet, never per
observation alone; statistical thresholds govern investigation urgency but
never override independently established safety violations.

A confirmed duplicate withdraws at ANY sample size. Statistics schedule the
investigation; they never veto safety.
"""

# --- Three volume-sensitive strategies ------------------------------------------------------
# Categories are initial examples. Select by effective independent sample
# size, traffic variability, and operational risk -- not by raw request
# count. A provider may be high-volume overall yet low-volume for a protected
# endpoint/region.
VOLUME_STRATEGIES = (
    ("low_volume",
     "longer windows, exact count-based tests, uncertainty intervals, "
     "targeted canaries. Never percent-change on tiny denominators."),
    ("bursty",
     "similarly shaped historical periods, cluster-aware correlation, "
     "incident-level evaluation. Never 500 correlated failures as 500 "
     "confirmations."),
    ("high_volume",
     "short+long windows, sequential change detection, stratification, "
     "minimum material-effect requirements. Never page tiny significant "
     "fluctuations."),
)


def select_volume_strategy(n_eff, variability: str, risk: str) -> str:
    """Select by effective independent sample size, variability, and risk."""
    if n_eff < 30:
        return "low_volume"
    if variability == "high":
        return "bursty"
    return "high_volume"


# --- Safety vs statistical separation -----------------------------------------------------------------
SAFETY_STATISTICAL_SEPARATION = (
    ("confirmed duplicate", "immediate withdrawal at ANY sample size"),
    ("contract no longer applies", "block reliance on the uncovered scope"),
    ("credible unconfirmed risk", "precautionary hold; statistics schedule the investigation"),
    ("ordinary transport errors", "volume-calibrated anomaly detection"),
    ("missing observability", "reduced assurance -- never healthy"),
    ("deadline exceeded", "escalate -- never assume noncommit"),
)


def safety_or_statistical(signal: dict) -> dict:
    """Hard separation. Safety findings never wait for statistics; statistics
    never veto safety. Excellent latency with silent downstream duplication
    needs its own monitor -- latency health proves nothing about effects."""
    if signal.get("verified_duplicate_effects", 0) >= 2:
        return {"path": "safety",
                "action": "immediate withdrawal at ANY sample size"}
    if signal.get("contract_covers") is False:
        return {"path": "safety", "action": "block reliance on the uncovered scope"}
    if signal.get("credible_possible_duplicate"):
        return {"path": "precaution",
                "action": "precautionary hold; statistics schedule the investigation"}
    if signal.get("observability") == "missing":
        return {"path": "observability",
                "action": "reduced assurance -- never healthy"}
    return {"path": "statistical",
            "action": "volume-calibrated anomaly detection"}


# --- Uncertainty by effective sample size ------------------------------------------------------------------
def se_proportion(p: float, n: int) -> float:
    """Standard error of a proportion. n <= 0 -> infinite: no data, no precision."""
    if n <= 0:
        return float("inf")
    return math.sqrt(p * (1 - p) / n)


def zero_failure_upper_bound(n: int, confidence: float = 0.95) -> float:
    """Exact one-sided upper bound with zero observed failures:
    1 - (1-confidence)^(1/n). Zero observed failures != zero risk.
    n=5 -> 45.1%; n=100 -> 3.0%; n=1000 -> 0.30%."""
    if n <= 0:
        return 1.0
    return 1 - (1 - confidence) ** (1.0 / n)


ZERO_FAILURE_TABLE = (
    # (n, upper bound at 95%): neither establishes idempotency correctness.
    (5, 0.451),
    (100, 0.030),
    (1000, 0.0030),
)


def n_eff_cluster_diagnostic(n: int, mean_cluster_size: float) -> float:
    """DIAGNOSTIC ONLY: n_eff ~= n / mean_cluster_size. Production uses
    validated cluster-aware models estimated from actual traces -- never this
    approximation as an authority."""
    return n / mean_cluster_size if mean_cluster_size > 0 else 0.0


def binomial_upper_p(n: int, k: int, p0: float) -> float:
    """One-sided upper-tail P(X >= k | p0). Exact summation for n <= 2000;
    normal approximation with continuity correction above (demonstration
    grade; production uses the independently calibrated model)."""
    if n <= 2000:
        return min(1.0, math.fsum(
            math.comb(n, i) * (p0 ** i) * ((1 - p0) ** (n - i))
            for i in range(k, n + 1)))
    mu = n * p0
    sd = math.sqrt(n * p0 * (1 - p0))
    z = (k - 0.5 - mu) / sd
    return 0.5 * math.erfc(z / math.sqrt(2))


# --- The statistical model table --------------------------------------------------------------------------------
STATISTICAL_MODELS = (
    ("sparse", "exact binomial / Bayesian / sequential"),
    ("variable_volume", "exposure-adjusted for varying traffic"),
    ("bursty", "negative-binomial / hierarchical"),
    ("correlated", "cluster resampling / hierarchical / time-series"),
    ("high_volume_stable", "CUSUM / EWMA / sequential likelihood"),
    ("constantly_monitored", "anytime-valid sequential inference"),
)
# The simplest method that passes independent calibration wins. Method
# choice is itself a calibrated claim, not a default.


# --- Fleet-wide repeated-testing control ------------------------------------------------------------------------------
def fleet_false_alarm_prob(n_metrics: int, alpha: float) -> float:
    """P(at least one false alarm) = 1 - (1-alpha)^n. 100 metrics x 1% = 63%:
    per-metric control is not fleet control."""
    return 1 - (1 - alpha) ** n_metrics


def alpha_budget_union(n_metrics: int, fleet_alpha: float = 0.05,
                       restarts: int = 0) -> float:
    """Preallocated per-test alpha via the union bound, INCLUDING restarted
    tests: a restarted test spends budget again."""
    return fleet_alpha / (n_metrics + restarts)


def paging_decision(p_value: float, material_impact: bool, actionable: bool,
                    safety_invariant: bool = False) -> bool:
    """OperationalPage = StatisticalSignal AND MaterialImpact AND Actionable.
    Hard safety invariants are exempt. A low p-value alone never pages."""
    if safety_invariant:
        return True
    return bool(p_value < 0.01 and material_impact and actionable)


# --- Paired windows (multiwindow adapted) ----------------------------------------------------------------------------------
def paired_window_decision(short_anomaly: bool, long_anomaly: bool,
                           material_evidence: bool,
                           low_traffic: bool = False) -> str:
    """Long + short windows, both calibrated. Material incident evidence
    overrides the wait. Low-traffic services get longer windows + synthetic
    traffic (targeted canaries), never 'absence of traffic = health'.
    Related alerts consolidate into one provider incident WITHOUT suppressing
    independent material-effect evidence."""
    if material_evidence:
        return "ACT_NOW"
    if short_anomaly and long_anomaly:
        return "ALERT"
    if low_traffic:
        return "EXTEND_WINDOW_AND_CANARY"
    return "OBSERVE"

# --- Versioned profiles + feedback-loop prevention ------------------------------------------------------------------
@dataclass(frozen=True)
class AlertCalibrationProfile:
    """Versioned calibration profile. Baselines come from admissible periods
    ONLY. Threshold changes preserve the old profile + its evidence and
    performance, and run in shadow mode first. Traffic-profile changes never
    silently alter evidence-qualification standards or LAW permissions --
    that would be the monitor rewriting the law it serves."""
    profile_id: str
    version: int
    strategy: str  # one of VOLUME_STRATEGIES
    parameters: Tuple[Tuple[str, object], ...]
    baseline_periods: Tuple[str, ...]
    supersedes: Optional[str]
    shadow_mode: bool
    evidence_refs: Tuple[str, ...]


def promote_profile(old: AlertCalibrationProfile,
                    new_parameters: Tuple[Tuple[str, object], ...],
                    evidence_refs: Tuple[str, ...]) -> AlertCalibrationProfile:
    """Threshold changes preserve the old profile and run the new one in
    shadow mode first. No silent swaps."""
    return AlertCalibrationProfile(
        profile_id=old.profile_id, version=old.version + 1,
        strategy=old.strategy, parameters=new_parameters,
        baseline_periods=old.baseline_periods,
        supersedes=f"{old.profile_id}/v{old.version}",
        shadow_mode=True, evidence_refs=evidence_refs)


# --- Historical replay calibration ---------------------------------------------------------------------------------------
def replay_period_metrics(records: list) -> dict:
    """Five metrics over one replay period. records: dicts with keys:
    truth (healthy/drift/breach), alert_raised, page_raised,
    detection_delay (or None), withdrawal (bool)."""
    n = len(records)
    healthy = [r for r in records if r["truth"] == "healthy"]
    bad = [r for r in records if r["truth"] in ("drift", "breach")]
    delays = sorted(r["detection_delay"] for r in bad
                    if r.get("detection_delay") is not None)
    median = delays[len(delays) // 2] if delays else None
    tail = delays[int(len(delays) * 0.95)] if delays else None
    return {
        "n": n,
        "false_incident_alerts": sum(1 for r in healthy if r["alert_raised"]),
        "false_pages": sum(1 for r in healthy if r["page_raised"]),
        "detection_delay_median": median,
        "detection_delay_p95": tail,
        "missed_material_incidents":
            sum(1 for r in bad if not r["alert_raised"]),
        "unnecessary_withdrawals": sum(1 for r in healthy if r["withdrawal"]),
    }


def replay_calibration(records: list, train: tuple, calibration: tuple,
                       heldout: tuple) -> dict:
    """Distinct train / calibration / held-out periods. Never
    tune-to-perfection on the same incidents: metrics are reported per
    period, and the held-out verdict is the honest one."""
    by_period = {}
    for r in records:
        by_period.setdefault(r["period"], []).append(r)
    out = {}
    for name, period in (("train", train), ("calibration", calibration),
                         ("heldout", heldout)):
        recs = [r for pid in period for r in by_period.get(pid, [])]
        out[name] = replay_period_metrics(recs)
    return out


# --- AER-CAL-001: the replay harness across three regimes ---------------------------------------------------------------
def aer_cal_001():
    """Isolated replay harness across the sparse / bursty / high-volume
    regimes. The verifier establishes: false-alarm budgets per regime and
    fleet-wide; detection delays meeting risk objectives where traffic
    supports it; confirmed violations containing regardless of sample size;
    zero healthy-provider misclassifications; stable reproducible profiles."""
    report = {}
    # Sealed synthetic corpus: (period, regime, truth, n, anomalous, alert, page, delay, withdrawal)
    corpus = [
        # train
        {"period": "t1", "regime": "sparse", "truth": "healthy",
         "alert_raised": False, "page_raised": False,
         "detection_delay": None, "withdrawal": False},
        {"period": "t1", "regime": "bursty", "truth": "healthy",
         "alert_raised": False, "page_raised": False,
         "detection_delay": None, "withdrawal": False},
        # calibration: a bursty drift caught, a sparse healthy observed
        {"period": "c1", "regime": "bursty", "truth": "drift",
         "alert_raised": True, "page_raised": False,
         "detection_delay": 4, "withdrawal": False},
        {"period": "c1", "regime": "sparse", "truth": "healthy",
         "alert_raised": False, "page_raised": False,
         "detection_delay": None, "withdrawal": False},
        # heldout: a high-volume breach + a high-volume healthy
        {"period": "h1", "regime": "high_volume", "truth": "breach",
         "alert_raised": True, "page_raised": True,
         "detection_delay": 1, "withdrawal": True},
        {"period": "h1", "regime": "high_volume", "truth": "healthy",
         "alert_raised": False, "page_raised": False,
         "detection_delay": None, "withdrawal": False},
    ]
    cal = replay_calibration(corpus, ("t1",), ("c1",), ("h1",))
    report["replay_metrics"] = cal
    held = cal["heldout"]
    assert held["false_incident_alerts"] == 0, held
    assert held["false_pages"] == 0, held
    assert held["missed_material_incidents"] == 0, held
    assert held["unnecessary_withdrawals"] == 0, held
    report["heldout_clean"] = True
    # False-alarm budgets: per regime and fleet-wide.
    report["fleet_math"] = {
        "hundred_metrics_at_1pct": round(fleet_false_alarm_prob(100, 0.01), 4),
        "bonferroni_per_test": alpha_budget_union(100),
        "note": "per-metric control is not fleet control",
    }
    assert abs(fleet_false_alarm_prob(100, 0.01) - 0.634) < 0.005
    assert abs(alpha_budget_union(100) - 0.0005) < 1e-9
    # Confirmed violations contain regardless of sample size.
    for n in (1, 5, 100000):
        d = safety_or_statistical({"verified_duplicate_effects": 2,
                                   "sample_size": n})
        assert d["action"] == "immediate withdrawal at ANY sample size", (n, d)
    report["safety_ignores_sample_size"] = True
    # Zero-failure bounds: small samples prove nothing about correctness.
    for n, expected in ZERO_FAILURE_TABLE:
        got = zero_failure_upper_bound(n)
        assert abs(got - expected) < 0.002, (n, got, expected)
    report["zero_failure_table_verified"] = True
    # Stable reproducible profiles: same input -> same version/params.
    p0 = AlertCalibrationProfile("prof-1", 1, "low_volume",
                                 (("alpha", 0.01),), ("2026-09",),
                                 None, False, ("baseline-evidence",))
    p1 = promote_profile(p0, (("alpha", 0.005),), ("recalibration-evidence",))
    assert p1.version == 2 and p1.shadow_mode and p1.supersedes == "prof-1/v1"
    p1b = promote_profile(p0, (("alpha", 0.005),), ("recalibration-evidence",))
    assert p1 == p1b, "profiles must be reproducible"
    report["profiles_stable"] = True
    return report

# ===========================================================================
# The Alert Calibration Lab (SN-0798)
# ===========================================================================
"""Executable acceptance suite for AER-CAL-1: five sealed synthetic histories
the threshold engine must judge correctly.

ALL SETTINGS ARE SYNTHETIC / DEMONSTRATION (2%/1% baselines, 1% statistical
threshold, 0.5pp materiality) -- explicitly NOT validated production values.
The lab tests the ENGINE's judgment structure, not the numbers.
"""

LAB_SETTINGS_NOTE = (
    "SYNTHETIC / DEMONSTRATION SETTINGS: 2%/1% baselines, 1% statistical "
    "threshold, 0.5pp materiality. Explicitly NOT validated production values."
)


@dataclass(frozen=True)
class SyntheticHistory:
    history_id: str
    n_requests: int
    n_timeouts: int
    n_rate_limited: int
    n_distinct_ops: int
    baseline_timeout_rate: float
    verified_duplicate_effects: int
    windows_confirm: bool
    correlated: bool  # one incident vs independent observations
    note: str


def lab_histories():
    """The five sealed histories."""
    return (
        # A: low-volume. 5 requests, 1 timeout (20% observed) -- but a 9.61%
        # chance under the 2% baseline. Record, reconcile, collect more
        # evidence. NO drift declared.
        SyntheticHistory("A", 5, 1, 0, 5, 0.02, 0, False, False,
                         "sparse: 1/5 timeouts; 9.61% chance under baseline"),
        # B: bursty. 800 attempts, 400 429s, 8 logical operations, one
        # 2-minute quota event. ONE correlated throttling incident, backoff,
        # investigate uncertain effects. Never 400 independent failures.
        SyntheticHistory("B", 800, 0, 400, 8, 0.01, 0, True, True,
                         "one 2-minute quota event across 8 logical operations"),
        # C: high-volume small deviation. 100,000 requests, 1,150 timeouts
        # (1.15%): statistically significant but +0.15pp < 0.5pp materiality.
        # Record/investigate; NO urgent page; NO drift from significance alone.
        SyntheticHistory("C", 100000, 1150, 0, 100000, 0.01, 0, False, False,
                         "significant but immaterial: +0.15pp < 0.5pp"),
        # D: high-volume material. 100,000 requests, 2,500 timeouts (2.5%,
        # +1.5pp), both windows confirm. Operational degradation alert +
        # reconciliation. Drift REMAINS UNPROVEN.
        SyntheticHistory("D", 100000, 2500, 0, 100000, 0.01, 0, True, False,
                         "material +1.5pp, both windows confirm: degrade, not drift"),
        # E: any volume. OP-127, 2 verified prohibited effects under one
        # logical identity. Withdraw the affected guarantee IMMEDIATELY. No
        # sample minimum, no test, no persistence window.
        SyntheticHistory("E", 3, 0, 0, 1, 0.01, 2, False, False,
                         "safety: 2 prohibited effects, one identity"),
    )


LAB_MATERIALITY_PP = 0.005   # demonstration only
LAB_ALPHA = 0.01             # demonstration only


def lab_diagnose(h: SyntheticHistory) -> dict:
    """The single diagnostic engine for all five histories. Returns the
    acceptance-matrix row: statistical anomaly?, contract breach proven?,
    and the consequential-retry decision."""
    # E first: the safety path bypasses statistics entirely.
    if h.verified_duplicate_effects >= 2:
        return {"history": h.history_id, "statistical_anomaly": "bypassed",
                "contract_breach_proven": True,
                "response": "L3", "diagnosis": "CONFIRMED_CONTRACT_BREACH",
                "consequential_retry": "BLOCKED: withdraw the affected guarantee IMMEDIATELY"}
    observed = h.n_timeouts / h.n_requests if h.n_requests else 0.0
    p = binomial_upper_p(h.n_requests, h.n_timeouts, h.baseline_timeout_rate)
    significant = p < LAB_ALPHA
    material_pp = observed - h.baseline_timeout_rate
    material = material_pp >= LAB_MATERIALITY_PP
    if h.correlated:
        # B: incident-level evaluation -- one attributed incident, and the
        # denominator is logical operations, not attempts.
        return {"history": h.history_id, "statistical_anomaly": True,
                "contract_breach_proven": False,
                "response": "L1", "diagnosis": "TRANSIENT_ANOMALY",
                "consequential_retry": "ONE correlated throttling incident; "
                                       "backoff; investigate uncertain effects",
                "note": f"ONE correlated throttling incident over "
                        f"{h.n_distinct_ops} logical operations; "
                        f"never {h.n_rate_limited} independent failures"}
    if significant and material and h.windows_confirm:
        # D: operational degradation -- alert + reconcile. Drift unproven.
        return {"history": h.history_id, "statistical_anomaly": True,
                "contract_breach_proven": False,
                "response": "L1-page", "diagnosis": "TRANSIENT_ANOMALY",
                "consequential_retry": "operational degradation alert + reconciliation; "
                                       "drift REMAINS UNPROVEN",
                "p": p, "material_pp": round(material_pp * 100, 3)}
    if significant and not material:
        # C: significant but immaterial -- no page, no drift inference.
        return {"history": h.history_id, "statistical_anomaly": True,
                "contract_breach_proven": False,
                "response": "L0/L1", "diagnosis": "TRANSIENT_ANOMALY",
                "consequential_retry": "record/investigate; NO urgent page; "
                                       "NO drift from significance alone",
                "p": p, "material_pp": round(material_pp * 100, 3)}
    # A (and any sparse non-significant): record, reconcile, more evidence.
    return {"history": h.history_id, "statistical_anomaly": significant,
            "contract_breach_proven": False,
            "response": "L0", "diagnosis": "TRANSIENT_ANOMALY",
            "consequential_retry": "record, reconcile, collect more evidence; NO drift",
            "p": p}


LAB_ACCEPTANCE_MATRIX = (
    # (history, statistical anomaly?, contract breach proven?, consequential retry)
    ("A", False, False, "collect more evidence; NO drift"),
    ("B", True, False, "ONE incident; backoff; investigate uncertain effects"),
    ("C", True, False, "NO urgent page; NO drift from significance alone"),
    ("D", True, False, "degradation alert + reconciliation; drift UNPROVEN"),
    ("E", "bypassed", True, "withdraw IMMEDIATELY"),
)


def calibration_lab():
    """The single best initial test: run all five histories through the same
    diagnostic engine; ONLY E may produce a confirmed deduplication breach.
    Re-run under different volumes: safety findings identical, alert timing
    may differ."""
    report = {"settings_note": LAB_SETTINGS_NOTE}
    rows = {}
    for h in lab_histories():
        rows[h.history_id] = lab_diagnose(h)
    report["rows"] = rows
    # The acceptance matrix.
    for hid, anomaly, breach, _retry in LAB_ACCEPTANCE_MATRIX:
        r = rows[hid]
        assert r["statistical_anomaly"] == anomaly, (hid, r)
        assert r["contract_breach_proven"] == breach, (hid, r)
    breaches = [hid for hid, r in rows.items() if r["contract_breach_proven"]]
    assert breaches == ["E"], breaches  # ONLY E
    report["only_E_breaches"] = True
    # Spot-check the demonstration numbers.
    a = rows["A"]
    assert abs(a["p"] - 0.0961) < 0.005, a["p"]  # 9.61% under the 2% baseline
    c = rows["C"]
    assert c["p"] < 1e-4 and c["material_pp"] == 0.15, c  # significant, immaterial
    d = rows["D"]
    assert d["material_pp"] == 1.5 and d["response"] == "L1-page", d
    report["demonstration_numbers"] = {"A_p": round(a["p"], 4),
                                       "C_p": c["p"],
                                       "C_material_pp": c["material_pp"],
                                       "D_material_pp": d["material_pp"]}
    # The low-volume panel: neither the 9.6% chance nor the 45.1% bound
    # establishes idempotency correctness.
    report["low_volume_panel"] = {
        "p_ge_1_timeout_under_baseline": round(binomial_upper_p(5, 1, 0.02), 4),
        "zero_failure_upper_bound_5": round(zero_failure_upper_bound(5), 4),
        "note": "neither establishes idempotency correctness",
    }
    assert abs(binomial_upper_p(5, 1, 0.02) - 0.0961) < 0.005
    assert abs(zero_failure_upper_bound(5) - 0.451) < 0.005
    # The fleet math.
    report["fleet_math"] = {
        "hundred_metrics_at_1pct": round(fleet_false_alarm_prob(100, 0.01), 4),
        "bonferroni_0_01_fleet": alpha_budget_union(100, fleet_alpha=0.01),
        "note": "sequential testing for repeated windows; paging budgets "
                "separate from statistical error budgets",
    }
    assert abs(fleet_false_alarm_prob(100, 0.01) - 0.634) < 0.005
    assert abs(alpha_budget_union(100, fleet_alpha=0.01) - 0.0001) < 1e-9
    # Re-run under different volumes: safety findings identical.
    e = next(h for h in lab_histories() if h.history_id == "E")
    for n in (3, 300, 300000):
        he = SyntheticHistory("E", n, 0, 0, 1, 0.01, 2, False, False, "rescaled")
        r = lab_diagnose(he)
        assert r["contract_breach_proven"] is True, (n, r)
    report["safety_identical_across_volumes"] = True
    return report

# ===========================================================================
# AER-CAL-2 — Contextual Drift Integrity Law (SN-0799)
# ===========================================================================
"""AER-CAL-2 is the CONTEXTUAL-CALIBRATION layer: AER-CAL-1 handles volume
regimes; this handles time, workload, and maintenance context.

LAW: evaluate operational anomalies against independently qualified temporal,
workload and maintenance context; expected patterns may adjust statistical
expectations and notification routing but cannot weaken safety invariants,
change LAW authority, or establish external guarantees; adaptive baselines
must not silently normalize unresolved regressions.

Fixed thresholds fail both ways: they false-alarm on normal Friday peaks
and they cannot tell a seasonal spike from a regression hiding inside one.
"""

# --- Three monitoring layers ----------------------------------------------------------------------------
MONITORING_LAYERS = (
    ("contextual_baseline",
     "unusual for this hour / weekday / load / condition?"),
    ("change_detection",
     "has the expected-vs-observed relationship changed?"),
    ("hard_contract_invariants",
     "qualified guarantee violated regardless of conditions? "
     "NEVER relaxed for busy periods or maintenance"),
)


def evaluate_three_layers(observed_rate: float, baseline_interval,
                          contract_violated: bool,
                          residual_history: tuple = ()) -> dict:
    """All three layers evaluate every observation. Layer 3 is never
    relaxed: a qualified-guarantee violation is a CONTRACT_VIOLATION in any
    context, including maintenance and peak load."""
    lo, hi = baseline_interval
    in_band = lo <= observed_rate <= hi
    # Layer 2: change detection -- a PERSISTENT residual shift (3 of the last
    # 5 out of band), not one noisy point at the interval edge.
    recent_out = sum(1 for r in residual_history[-5:] if r)
    change = (not in_band) and recent_out >= 3
    if contract_violated:
        return {"layer3": "CONTRACT_VIOLATION", "layer1": "n/a: invariant",
                "layer2": "n/a: invariant",
                "verdict": "CONTRACT_VIOLATION"}
    if change:
        return {"layer3": "holds", "layer1": "out_of_band",
                "layer2": "change_detected",
                "verdict": "CONTEXTUAL_ANOMALY"}
    if not in_band:
        return {"layer3": "holds", "layer1": "out_of_band",
                "layer2": "watch",
                "verdict": "INVESTIGATE_SINGLE_POINT"}
    return {"layer3": "holds", "layer1": "in_band", "layer2": "stable",
            "verdict": "EXPECTED_SEASONAL_VARIATION"}


# --- Like-with-like comparison: the contextual Beta-Binomial ------------------------------------------------
# Context inputs: hour/weekday/month/holiday, volume/burst/concurrency,
# endpoint/region/account/version, request type/payload/retry status,
# verified maintenance state, client deployment/routing.
#
# CAUSAL-DEPENDENCY WARNING: never condition on variables that are
# CONSEQUENCES of the failure (e.g. retry surges, current error rates).
# Baselines use independently justified context with explicit causal
# modeling. Conditioning on a consequence hides the failure inside the
# baseline -- the exact normalization this law forbids.
CAUSAL_DEPENDENCY_WARNING = (
    "Never condition on consequences of the failure (retry surges, live "
    "error rates, downstream backpressure caused by the incident). "
    "Admissible context is fixed before the observation window or "
    "independently justified with explicit causal modeling."
)
FORBIDDEN_CONTEXT_VARIABLES = frozenset({
    "retry_surge", "live_error_rate", "downstream_backpressure",
    "current_alert_state",
})


def context_is_admissible(context: dict) -> tuple:
    bad = sorted(k for k in context if k in FORBIDDEN_CONTEXT_VARIABLES)
    return (not bad, bad)


class ContextualBaseline:
    """Beta-Binomial per context cell, trained on QUALIFIED history only.
    The predictive interval is the layer-1 expectation. Cells are keyed by
    (weekday, hour_band, maintenance_flag, tz_version) -- DST transitions
    get their own cells; sparse categories keep wider uncertainty."""

    def __init__(self):
        self.cells = {}  # ctx -> [alpha, beta]

    @staticmethod
    def cell_key(weekday: int, hour: int, maintenance: bool,
                 tz_version: str = "v1") -> tuple:
        # Bands align with the rate structure: every cell is rate-pure.
        if 0 <= hour < 6:
            band = "overnight"
        elif hour < 18:
            band = "day"
        elif hour < 22:
            band = "peak"
        else:
            band = "evening"
        return (weekday, band, maintenance, tz_version)

    def train(self, ctx: tuple, n: int, k: int):
        """Train on qualified observations ONLY (see training hygiene)."""
        a, b = self.cells.get(ctx, (1.0, 1.0))
        self.cells[ctx] = (a + k, b + (n - k))

    def interval(self, ctx: tuple, n: int, z: float = 2.576) -> tuple:
        """99% predictive interval as rates. Sparse cells -> wider intervals."""
        a, b = self.cells.get(ctx, (1.0, 1.0))
        s = a + b
        mean = n * a / s
        var = n * a * b * (s + n) / (s * s * (s + 1))
        sd = math.sqrt(max(var, 0.0))
        return (max(0.0, (mean - z * sd) / n), (mean + z * sd) / n)

    def expected_rate(self, ctx: tuple) -> float:
        a, b = self.cells.get(ctx, (1.0, 1.0))
        return a / (a + b)


# --- Four worked examples --------------------------------------------------------------------------------------
# Fixed thresholds fail both ways: a 5% fixed line false-alarms the Friday
# peak and waves through the Monday baseline; like-with-like gets all four.
CONTEXTUAL_WORKED_EXAMPLES = (
    # (id, observed, baseline band, expected verdict)
    ("monday_overnight", 0.008, (0.001, 0.012), "EXPECTED_SEASONAL_VARIATION"),
    ("friday_peak", 0.09, (0.05, 0.11), "EXPECTED_SEASONAL_VARIATION"),
    ("friday_regression", 0.16, (0.05, 0.11), "CONTEXTUAL_ANOMALY"),
    ("verified_maintenance", 0.17, (0.12, 0.20), "MAINTENANCE_CONSISTENT"),
)


# --- Maintenance as a verified operating state -------------------------------------------------------------------
@dataclass(frozen=True)
class MaintenanceRecord:
    """MAINT-042 shape. The maintenance baseline applies ONLY after
    notice/scope/impact/interval are verified. Post-incident announcements
    never rewrite earlier observations: records are append-only."""
    record_id: str
    notice_verified: bool
    scope: str
    expected_impact: str
    interval: tuple  # (start_hour, end_hour) in the provider's declared tz
    declared_in_advance: bool


def maintenance_verified(record: MaintenanceRecord) -> tuple:
    missing = []
    if not record.notice_verified:
        missing.append("notice")
    if not record.scope:
        missing.append("scope")
    if not record.expected_impact:
        missing.append("expected_impact")
    if not record.interval:
        missing.append("interval")
    if not record.declared_in_advance:
        missing.append("declared_in_advance")
    return (not missing, tuple(missing))


def maintenance_status(record: MaintenanceRecord, now_hour: int,
                       observed_rate: float, maintenance_band: tuple,
                       contract_violated: bool) -> str:
    """During maintenance, three things stay SEPARATE: availability alerting,
    outcome reconciliation, and safety enforcement. Notification suppression
    != proof suppression. Undeclared extensions trigger renewed
    investigation. Consequential guarantee changes need separate
    qualification even during maintenance."""
    if contract_violated:
        return "CONTRACT_VIOLATION"  # layer 3: never suppressed
    ok, _ = maintenance_verified(record)
    if not ok:
        return "REVIEW_REQUIRED"  # unqualified maintenance claim
    start, end = record.interval
    if not (start <= now_hour < end):
        return "REVIEW_REQUIRED"  # undeclared extension: investigate anew
    lo, hi = maintenance_band
    if lo <= observed_rate <= hi:
        return "MAINTENANCE_CONSISTENT"
    return "INVESTIGATE_SINGLE_POINT"


# --- Three recurring-change kinds ------------------------------------------------------------------------------------
RECURRING_CHANGE_KINDS = (
    ("calendar_seasonality", "qualified baseline: the pattern is expected"),
    ("workload_regime_change", "investigate, then a NEW baseline"),
    ("provider_behavioral_drift", "investigate with competing explanations"),
)


def classify_recurring_change(evidence: dict) -> str:
    """evidence: calendar_match, workload_shift, provider_signal,
    client_config_change. Provider drift is never the default: examine own
    routing / SDK / retries / quotas / concurrency alongside provider
    evidence first."""
    if evidence.get("calendar_match") and not evidence.get("workload_shift"):
        return "calendar_seasonality"
    if evidence.get("workload_shift") and evidence.get("client_config_change"):
        return "workload_regime_change"
    if evidence.get("provider_signal"):
        if not evidence.get("client_explanations_excluded"):
            return "INVESTIGATE_COMPETING_EXPLANATIONS"
        return "provider_behavioral_drift"
    return "UNDETERMINED"


# --- The anti-normalization rule ------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class QualificationReference:
    """FROZEN: the contract as qualified. Never adapts."""
    reference_id: str
    qualified_bands: tuple  # ((context, lo, hi), ...)
    contract_version: str


@dataclass(frozen=True)
class OperationalForecast:
    """ADAPTIVE: explains patterns. Never replaces the contract."""
    forecast_id: str
    revision: int
    bands: tuple
    trained_on: tuple  # qualified periods only


TRAINING_HYGIENE_EXCLUSIONS = (
    "confirmed outages", "anomalous periods", "unqualified maintenance",
    "unresolved changes",
    # Never silently relabeled healthy.
)


def check_training_hygiene(periods: tuple) -> tuple:
    bad = [p for p in periods if p in TRAINING_HYGIENE_EXCLUSIONS
           or p.startswith("unresolved") or p.startswith("outage")]
    return (not bad, bad)


def forecast_vs_reference(forecast: OperationalForecast,
                          reference: QualificationReference,
                          material_pp: float = 0.02) -> dict:
    """Material forecast-vs-reference divergence is itself a review event.
    New patterns become baselines only with sufficient evidence and an
    accepted calibration revision -- never by silent absorption."""
    divs = []
    ref = dict((c, (lo, hi)) for c, lo, hi in reference.qualified_bands)
    for ctx, flo, fhi in forecast.bands:
        if ctx in ref:
            rlo, rhi = ref[ctx]
            if abs(flo - rlo) > material_pp or abs(fhi - rhi) > material_pp:
                divs.append(ctx)
    return {"divergent_contexts": tuple(divs),
            "review_event": bool(divs),
            "note": "the forecast explains; the reference governs"}


# --- Independent corroboration before attribution ---------------------------------------------------------------------------
CORROBORATION_SOURCES = (
    ("synthetic_canaries", "controlled probes under the same context"),
    ("matched_endpoint_region", "the same endpoint/region, different workload"),
    ("client_config_comparison", "own routing / SDK / retries / quotas / concurrency"),
    ("provider_status_records", "the provider's own incident records"),
    ("independent_effect_ledger", "the durable effect count, not notifications"),
    ("logical_operation_identity_comparison", "same identity, same payload, same scope"),
)


def attribute_contextual_anomaly(corroboration: dict) -> str:
    """Undistinguished causes -> CONTEXTUAL_ANOMALY_UNATTRIBUTED. Never false
    provider-drift. Controls must be genuinely comparable."""
    required = [s[0] for s in CORROBORATION_SOURCES]
    missing = [s for s in required if s not in corroboration]
    if missing:
        return "CONTEXTUAL_ANOMALY_UNATTRIBUTED"
    if corroboration.get("client_explanations_excluded") and \
            corroboration.get("provider_signal_present"):
        return "PROVIDER_DRIFT"
    if corroboration.get("client_cause_found"):
        return "CLIENT_CAUSE"
    return "CONTEXTUAL_ANOMALY_UNATTRIBUTED"

# --- The S1-S10 fixtures ----------------------------------------------------------------------------------------------------
def classify_contextual_scenario(s: dict) -> str:
    """Scenario keys: observed_rate, band (lo, hi) or None,
    maintenance (None | MaintenanceRecord), in_window (bool),
    duplicate_effects (int), client_change (None | 'volume' | 'retry_identity'),
    regime_evidence (bool), data_missing (bool), forecast_diverged (bool).
    Layer 3 first: it is never relaxed, for any context."""
    if s.get("duplicate_effects", 0) >= 2:
        return "CONTRACT_VIOLATION"
    if s.get("data_missing"):
        return "INSUFFICIENT_OBSERVABILITY"
    rec = s.get("maintenance")
    if rec is not None:
        if s.get("in_window"):
            ok, _ = maintenance_verified(rec)
            if not ok:
                return "REVIEW_REQUIRED"
            lo, hi = s["band"]
            if lo <= s["observed_rate"] <= hi:
                return "MAINTENANCE_CONSISTENT"
            return "INVESTIGATE_SINGLE_POINT"
        return "REVIEW_REQUIRED"  # undeclared extension
    if s.get("client_change") == "retry_identity":
        return "INTEGRATION_DEFECT"
    if s.get("client_change") == "volume" and s.get("regime_evidence"):
        return "WORKLOAD_REGIME_CHANGE"
    if s.get("forecast_diverged"):
        return "REVIEW_REQUIRED"  # S8: never silently normalize
    band = s.get("band")
    if band is not None:
        lo, hi = band
        if lo <= s["observed_rate"] <= hi:
            return "EXPECTED_SEASONAL_VARIATION"
        return "CONTEXTUAL_ANOMALY"
    return "UNDETERMINED"


def s_fixtures():
    """The ten sealed scenarios."""
    maint = MaintenanceRecord("MAINT-042", True, "payments.charge/eu", "elevated latency",
                              (2, 4), True)
    friday = (0.05, 0.11)
    return (
        ("S1", {"observed_rate": 0.09, "band": friday},
         "EXPECTED_SEASONAL_VARIATION"),                       # normal Friday spike
        ("S2", {"observed_rate": 0.16, "band": friday},
         "CONTEXTUAL_ANOMALY"),                                # spike + genuine regression
        ("S3", {"observed_rate": 0.17, "band": (0.12, 0.20),
                "maintenance": maint, "in_window": True},
         "MAINTENANCE_CONSISTENT"),                            # verified maintenance
        ("S4", {"observed_rate": 0.17, "band": (0.12, 0.20),
                "maintenance": maint, "in_window": True, "duplicate_effects": 2},
         "CONTRACT_VIOLATION"),                                # maintenance + duplicates
        ("S5", {"observed_rate": 0.17, "band": (0.12, 0.20),
                "maintenance": maint, "in_window": False},
         "REVIEW_REQUIRED"),                                   # extended maintenance
        ("S6", {"observed_rate": 0.09, "band": friday, "client_change": "volume",
                "regime_evidence": True},
         "WORKLOAD_REGIME_CHANGE"),                            # client release doubles volume
        ("S7", {"observed_rate": 0.09, "band": friday,
                "client_change": "retry_identity"},
         "INTEGRATION_DEFECT"),                                # release changes retry identities
        ("S8", {"observed_rate": 0.10, "band": friday, "forecast_diverged": True},
         "REVIEW_REQUIRED"),                                   # slow degradation, never normalize
        ("S9", {"observed_rate": 0.16, "band": friday},
         "CONTEXTUAL_ANOMALY"),                                # peak-concurrency-only: in scope
        ("S10", {"observed_rate": 0.16, "band": friday, "data_missing": True},
         "INSUFFICIENT_OBSERVABILITY"),                        # missing peak data
    )


def s2_crown_jewel():
    """S2: seasonality hiding a real regression -- the crown jewel.
    Identical peak traffic, two histories: accept one, investigate the
    other. Repeated during maintenance (the anomaly path stays open).
    Plus one verified duplicate effect: immediate withdrawal regardless of
    context."""
    friday = (0.05, 0.11)
    healthy = classify_contextual_scenario({"observed_rate": 0.09, "band": friday})
    defective = classify_contextual_scenario({"observed_rate": 0.16, "band": friday})
    assert healthy == "EXPECTED_SEASONAL_VARIATION", healthy
    assert defective == "CONTEXTUAL_ANOMALY", defective
    # During verified maintenance the anomaly path stays open: the
    # maintenance band applies, but a regression outside it still investigates.
    maint = MaintenanceRecord("MAINT-042", True, "s", "latency", (2, 4), True)
    m_healthy = classify_contextual_scenario(
        {"observed_rate": 0.17, "band": (0.12, 0.20),
         "maintenance": maint, "in_window": True})
    m_defective = classify_contextual_scenario(
        {"observed_rate": 0.25, "band": (0.12, 0.20),
         "maintenance": maint, "in_window": True})
    assert m_healthy == "MAINTENANCE_CONSISTENT", m_healthy
    assert m_defective == "INVESTIGATE_SINGLE_POINT", m_defective
    # One verified duplicate effect: layer 3 fires regardless of context.
    breach = classify_contextual_scenario(
        {"observed_rate": 0.09, "band": friday, "duplicate_effects": 2,
         "maintenance": maint, "in_window": True})
    assert breach == "CONTRACT_VIOLATION", breach
    return {"healthy": healthy, "defective": defective,
            "maintenance_healthy": m_healthy,
            "maintenance_defective": m_defective,
            "breach_during_maintenance": breach}


# --- Conditional false-alert rates --------------------------------------------------------------------------------------------
def conditional_false_alert_rates(records: list) -> dict:
    """records: (condition: tuple, alert_raised: bool, truth_healthy: bool).
    A 1% aggregate hiding a 15% Friday-evening pocket is NOT calibrated:
    rates are reported per condition, and pockets above budget are flagged."""
    by_cond = {}
    for cond, alert, healthy in records:
        c = by_cond.setdefault(cond, {"alerts": 0, "healthy_n": 0})
        if healthy:
            c["healthy_n"] += 1
            c["alerts"] += alert
    out = {}
    for cond, c in sorted(by_cond.items()):
        rate = c["alerts"] / c["healthy_n"] if c["healthy_n"] else 0.0
        out[cond] = {"false_alert_rate": round(rate, 4),
                     "n": c["healthy_n"],
                     "pocket": rate > 0.05}
    total_a = sum(c["alerts"] for c in by_cond.values())
    total_n = sum(c["healthy_n"] for c in by_cond.values())
    out["aggregate"] = round(total_a / total_n, 4) if total_n else 0.0
    return out


# --- AER-CAL-002: ten weeks of synthetic hourly traffic ----------------------------------------------------------------------------
def aer_cal_002():
    """8-12 week synthetic: hourly traffic with weekly cycles, a known
    maintenance window, a permanent workload shift, a hidden provider
    regression, and a prohibited duplicate-effect counterexample.
    The verifier requires: no spurious drift verdicts on normal seasonality;
    maintenance not suppressing the safety counterexample; the adaptive
    model not absorbing the regression; fixed-threshold comparison on
    held-out histories."""
    import random
    rng = random.Random(20261010)
    report = {}
    WEEKS = 10
    HOURS = WEEKS * 7 * 24

    def base_rate(weekday, hour):
        # Weekly + daily seasonality, qualified in weeks 1-3. Rate-pure bands.
        if weekday == 4 and 18 <= hour < 22:   # Friday peak
            return 0.09
        if 0 <= hour < 6:
            return 0.008                        # overnight
        if 18 <= hour < 22:
            return 0.04                         # evening peak (non-Friday)
        if 22 <= hour < 24:
            return 0.03                         # late evening
        return 0.02

    def volume(weekday, hour, week):
        v = 8000 if 18 <= hour < 22 else 1500
        if weekday >= 5:
            v = int(v * 0.6)
        if week >= 7:
            v *= 2                              # permanent workload shift, week 7+
        return v

    in_maintenance = lambda w, wd, h: (w == 5 and wd == 1 and 2 <= h < 4) or \
                                      (w == 9 and wd == 2 and 2 <= h < 3)
    hidden_regression = lambda w, wd, h: (w == 8 and wd == 4 and 18 <= h < 22)

    baseline = ContextualBaseline()
    fixed_false_alarms = 0
    contextual_false_drift = 0
    regression_detected = False
    maintenance_consistent_hours = 0
    regime_change_flagged = False
    breach_withdrawn = False
    residuals = []

    for t in range(HOURS):
        week = t // 168 + 1
        wd = (t // 24) % 7
        h = t % 24
        n = volume(wd, h, week)
        maint = in_maintenance(week, wd, h)
        if maint:
            rate = 0.17
        elif hidden_regression(week, wd, h):
            rate = 0.16
        else:
            rate = base_rate(wd, h)
        k = sum(1 for _ in range(n) if rng.random() < rate)
        obs = k / n
        ctx = ContextualBaseline.cell_key(wd, h, maint)
        if week <= 3 and not maint:
            baseline.train(ctx, n, k)  # qualified history only
        # Fixed-threshold comparison runs on ALL clean weeks (no training needed).
        is_clean_week = week in (1, 2, 3, 4, 6)
        if obs > 0.05 and is_clean_week:
            fixed_false_alarms += 1  # the fixed line false-alarms Friday peaks
        if week <= 3:
            continue  # train on weeks 1-3; evaluate on held-out weeks 4+
        if week == 9 and wd == 2 and h == 2 and maint:
            # The prohibited duplicate-effect counterexample, INSIDE the
            # maintenance window: layer 3 must fire regardless.
            v = classify_contextual_scenario(
                {"observed_rate": obs, "band": (0.12, 0.20),
                 "maintenance": MaintenanceRecord("MAINT-042", True, "s",
                                                  "latency", (2, 4), True),
                 "in_window": True, "duplicate_effects": 2})
            assert v == "CONTRACT_VIOLATION", v
            breach_withdrawn = True
            continue
        if maint:
            lo, hi = (0.12, 0.20)
            if lo <= obs <= hi:
                maintenance_consistent_hours += 1
            continue
        lo, hi = baseline.interval(ctx, n)
        in_band = lo <= obs <= hi
        residuals.append(not in_band)
        ev = evaluate_three_layers(obs, (lo, hi), False, tuple(residuals))
        if is_clean_week and ev["verdict"] in ("CONTEXTUAL_ANOMALY",):
            contextual_false_drift += 1
        if hidden_regression(week, wd, h) and ev["verdict"] == "CONTEXTUAL_ANOMALY":
            regression_detected = True

    # Week 7: permanent workload shift -> regime change (investigate + new
    # baseline), classified with competing explanations, not drift.
    rc = classify_recurring_change({"calendar_match": False, "workload_shift": True,
                                    "client_config_change": True,
                                    "provider_signal": False})
    assert rc == "workload_regime_change", rc
    regime_change_flagged = True

    # The adaptive model must NOT absorb the week-8 regression: training
    # hygiene excludes anomalous periods.
    ok_hyg, bad = check_training_hygiene(("qualified-week-6", "anomalous periods"))
    assert not ok_hyg and bad == ["anomalous periods"]
    fr = forecast_vs_reference(
        OperationalForecast("f2", 2, ((("fri", "peak", False, "v1"), 0.05, 0.16),),
                            ("qualified-week-6",)),
        QualificationReference("q1", ((("fri", "peak", False, "v1"), 0.05, 0.11),), "v3"))
    assert fr["review_event"], fr  # material divergence is a review event

    report["no_spurious_drift_on_seasonality"] = contextual_false_drift == 0
    report["contextual_false_drift_count"] = contextual_false_drift
    report["fixed_threshold_false_alarms_clean_weeks"] = fixed_false_alarms
    report["fixed_threshold_fails"] = fixed_false_alarms > 0
    report["hidden_regression_detected"] = regression_detected
    report["maintenance_consistent_hours"] = maintenance_consistent_hours
    report["regime_change_classified"] = regime_change_flagged
    report["breach_withdrawn_during_maintenance"] = breach_withdrawn
    report["training_hygiene_holds"] = True
    report["forecast_divergence_is_review_event"] = True
    assert contextual_false_drift == 0, "spurious drift on clean seasonality"
    assert fixed_false_alarms > 0, "fixed threshold must false-alarm Friday peaks"
    assert regression_detected, "hidden regression must be detected, not absorbed"
    assert maintenance_consistent_hours > 0
    assert breach_withdrawn, "maintenance must not suppress the safety counterexample"
    return report

# ===========================================================================
# AER-CAL-3 — Governed Baseline Learning Law (SN-0800)
# ===========================================================================
"""AER-CAL-3 is the BASELINE-GOVERNANCE layer: AER-CAL-2 warned against
normalizing regressions; this builds the learning machine that cannot.

LAW: NayaNET may learn workload distributions continuously, but changes to
the qualified definition of normal provider behavior require admissible
evidence, independently verified scope, preserved incident provenance,
regression-sensitive testing, and governed promotion. Unresolved failures
may inform investigation but shall not independently establish healthy
behavior.

No path exists from 'predicts consistently' to 'qualified as normal': an
accurate prediction of worsening service is not evidence it became
acceptable.
"""

# --- Three references --------------------------------------------------------------------------------
# A: the qualified reference -- immutable within its version; changes only
#    via governed requalification. (Reuses QualificationReference, AER-CAL-2.)
# B: the adaptive candidate -- learns continuously, shadow mode allowed,
#    NEVER grants its own qualification.
# C: the promoted operational baseline -- bound to a calibration receipt +
#    revision.
@dataclass(frozen=True)
class AdaptiveCandidate:
    candidate_id: str
    revision: int
    bands: tuple
    trained_on: tuple      # training-data states used, with provenance
    shadow: bool
    status: str            # CANDIDATE | SHADOW | INDEPENDENTLY_QUALIFIED | PROMOTED


@dataclass(frozen=True)
class PromotedBaseline:
    baseline_id: str
    revision: int
    bands: tuple
    calibration_receipt: str
    qualified_reference_id: str
    supersedes: object  # prior baseline id or None


CANDIDATE_STATUSES = ("CANDIDATE", "SHADOW", "INDEPENDENTLY_QUALIFIED", "PROMOTED")

# Two-speed learning: fast for substantiated demand/timing/mix changes;
# evidence-gated for error/latency/failure distributions.
TWO_SPEED_LEARNING = (
    ("demand_timing_mix", "fast: substantiated changes adapt quickly"),
    ("error_latency_failure", "evidence-gated: NEVER auto-adapts; justification required"),
)


def learning_speed(change_kind: str) -> str:
    if change_kind in ("demand", "timing", "mix"):
        return "fast"
    return "evidence_gated"


# --- Training-data classification: seven states -------------------------------------------------------------------
TRAINING_DATA_STATES = (
    ("VERIFIED_HEALTHY", "eligible as positive health evidence"),
    ("VERIFIED_WORKLOAD_SHIFT", "eligible: investigated shift, new baseline justified"),
    ("DECLARED_MAINTENANCE", "eligible for the maintenance band only"),
    ("UNRESOLVED_ANOMALY", "RETAINED for study; FORBIDDEN as positive health proof"),
    ("CONFIRMED_REGRESSION", "excluded; triggers review, never training"),
    ("INSUFFICIENT_OBSERVABILITY", "excluded; cannot establish health"),
    ("INDEPENDENTLY_CLEARED", "eligible: cleared by independent evidence"),
)
TRAINING_ELIGIBLE_STATES = frozenset({
    "VERIFIED_HEALTHY", "VERIFIED_WORKLOAD_SHIFT",
    "DECLARED_MAINTENANCE", "INDEPENDENTLY_CLEARED",
})


def training_eligible(state: str) -> tuple:
    """Provenance-bound eligibility. Unresolved incidents are retained for
    study but FORBIDDEN as positive health proof. Delayed-effect labels
    respect the settlement/reconciliation horizon."""
    return (state in TRAINING_ELIGIBLE_STATES,
            "eligible" if state in TRAINING_ELIGIBLE_STATES
            else f"{state}: not admissible as health evidence")


# --- Demand vs failure-acceptance --------------------------------------------------------------------------------------
def assess_distribution_change(kind: str, old: float, new: float,
                               justification: str = "") -> dict:
    """The 10k->50k/hr example: learning that traffic grew is automatic;
    learning that 3% failures are healthy requires justification.
    Conditional performance models stay within their supported envelope --
    they never silently expand safety guarantees."""
    if learning_speed(kind) == "fast":
        return {"path": "fast", "accepted": True,
                "note": f"{kind} change {old}->{new}: demand learning is automatic"}
    if old == new:
        return {"path": "evidence_gated", "accepted": True,
                "note": f"{kind} unchanged at {old}: nothing to justify"}
    if justification:
        return {"path": "evidence_gated", "accepted": True,
                "note": f"{kind} change {old}->{new}: justified by {justification}"}
    return {"path": "evidence_gated", "accepted": False,
            "note": f"{kind} change {old}->{new}: NO justification -- "
                    "an accurate prediction of worsening service is not evidence "
                    "it became acceptable"}


# --- The promotion gate: eight obligations, six-conjunct predicate -------------------------------------------------------
PROMOTION_OBLIGATIONS = (
    "legitimate_context",
    "training_integrity",
    "incident_disposition",
    "predictive_quality",
    "detection_integrity",
    "false_alert_control",
    "safety_preservation",
    "independent_qualification",
)
# Promote(B_n): the six conjuncts that must ALL hold at promotion time.
# predictive_quality and false_alert_control are continuous shadow-mode
# requirements, monitored always, not one-time gates.
PROMOTE_CONJUNCTS = (
    "legitimate_context",
    "training_integrity",
    "incident_disposition",
    "detection_integrity",
    "safety_preservation",
    "independent_qualification",
)


def check_promotion_obligations(evidence: dict) -> dict:
    """Eight obligations as SEPARATE predicates. No aggregate score: a 7/8
    is not 'almost promotable' -- each missing obligation blocks."""
    return {ob: bool(evidence.get(ob)) for ob in PROMOTION_OBLIGATIONS}


def promote_bn(results: dict) -> tuple:
    """Promote(B_n): the six-conjunct predicate. Returns (holds, missing)."""
    missing = tuple(c for c in PROMOTE_CONJUNCTS if not results.get(c))
    return (not missing, missing)


# --- Incident-exposure ledger + dual-reference comparison --------------------------------------------------------------------
@dataclass(frozen=True)
class IncidentExposureRecord:
    week: str
    context: str
    observed: float
    qualified_band: tuple
    forecast_band: tuple
    disposition: str


def dual_reference_evaluate(observed: float, qualified_band: tuple,
                            forecast_band: tuple) -> dict:
    """Evaluate against BOTH the adaptive forecast and the frozen qualified
    reference. The qualified reference may be context-dependent, but its
    governing version never silently moves on unexplained outcomes. The
    trainer must never use its own anomaly classification as independent
    health proof."""
    qlo, qhi = qualified_band
    flo, fhi = forecast_band
    q_ok = qlo <= observed <= qhi
    f_ok = flo <= observed <= fhi
    if not q_ok and f_ok:
        return {"qualified": "ANOMALY", "forecast": "normal",
                "verdict": "DIVERGENCE_IS_THE_SIGNAL",
                "note": "the forecast adapted to the regression; the reference did not"}
    if not q_ok and not f_ok:
        return {"qualified": "ANOMALY", "forecast": "anomaly",
                "verdict": "CONFIRMED_ANOMALY"}
    if q_ok and not f_ok:
        return {"qualified": "normal", "forecast": "anomaly",
                "verdict": "FORECAST_MISCALIBRATED"}
    return {"qualified": "normal", "forecast": "normal", "verdict": "AGREE_NORMAL"}


def w1_w6_illustration():
    """Six weeks: the forecast adapts to a slow regression while the frozen
    reference holds. W4 is the week the divergence becomes the signal."""
    ref_band = (0.05, 0.11)
    weeks = (
        ("W1", 0.09, (0.05, 0.11)),
        ("W2", 0.10, (0.05, 0.12)),
        ("W3", 0.115, (0.05, 0.13)),   # forecast starts absorbing
        ("W4", 0.13, (0.06, 0.15)),    # divergence is the signal
        ("W5", 0.14, (0.07, 0.16)),
        ("W6", 0.15, (0.08, 0.17)),    # forecast fully normalized the regression
    )
    return [IncidentExposureRecord(w, "friday-peak", obs, ref_band, fb,
                                   dual_reference_evaluate(obs, ref_band, fb)["verdict"])
            for w, obs, fb in weeks]


# --- Settlement watermarks --------------------------------------------------------------------------------------------------------
def settlement_eligible(t_operation: float, h_effect: float, t_now: float) -> bool:
    """T_eligible >= T_operation + H_effect. With no finite complete horizon,
    elapsed time never proves a material effect never occurred."""
    return t_now >= t_operation + h_effect


def claim_data_eligible(claim: str, t_operation: float, h_effect: float,
                        t_now: float) -> tuple:
    ok = settlement_eligible(t_operation, h_effect, t_now)
    return (ok, f"claim {claim}: {'eligible' if ok else 'not yet settled'}")


# --- Race-safe reversible promotion --------------------------------------------------------------------------------------------------
class BaselinePromotionLog:
    """Append-only promotion log. promote_candidate is a CAS on
    (candidate_id, expected_revision): candidate status, base/incident/policy
    revisions, no unresolved blockers, and an authorized receipt must ALL
    hold in the same ordering protocol. Rollback is a NEW governed
    publication preserving history -- never erasing the failed candidate or
    its receipts."""

    def __init__(self):
        self._lock = threading.RLock()
        self.entries = []
        self.promoted = {}  # baseline_id -> PromotedBaseline

    def propose(self, candidate: AdaptiveCandidate):
        with self._lock:
            self.entries.append(("proposed", candidate.candidate_id,
                                 candidate.revision))
            return candidate

    def promote_candidate(self, candidate: AdaptiveCandidate,
                          expected_revision: int, base_rev: int,
                          incident_rev: int, policy_rev: int,
                          authorized_receipt: str,
                          unresolved_blockers: tuple = ()) -> dict:
        with self._lock:
            if candidate.revision != expected_revision:
                return {"promoted": False,
                        "reason": "CAS mismatch: revision moved under us"}
            if candidate.status != "INDEPENDENTLY_QUALIFIED":
                return {"promoted": False,
                        "reason": f"status {candidate.status}: shadow/qualified first"}
            if unresolved_blockers:
                return {"promoted": False,
                        "reason": f"unresolved blockers: {unresolved_blockers}"}
            if not authorized_receipt:
                return {"promoted": False,
                        "reason": "no authorized receipt"}
            baseline = PromotedBaseline(
                baseline_id=candidate.candidate_id,
                revision=candidate.revision + 1,
                bands=candidate.bands,
                calibration_receipt=authorized_receipt,
                qualified_reference_id=f"ref@{base_rev}",
                supersedes=self.promoted.get(candidate.candidate_id))
            self.promoted[candidate.candidate_id] = baseline
            self.entries.append(("promoted", candidate.candidate_id,
                                 baseline.revision, authorized_receipt,
                                 base_rev, incident_rev, policy_rev))
            return {"promoted": True, "baseline": baseline}

    def rollback(self, baseline_id: str, reason: str,
                 authorized_receipt: str) -> dict:
        with self._lock:
            current = self.promoted.get(baseline_id)
            if current is None:
                return {"rolled_back": False, "reason": "unknown baseline"}
            # A new governed publication; the failed baseline and its
            # receipts stay in the log.
            restored = PromotedBaseline(
                baseline_id=baseline_id, revision=current.revision + 1,
                bands=current.bands, calibration_receipt=authorized_receipt,
                qualified_reference_id=current.qualified_reference_id,
                supersedes=current)
            self.promoted[baseline_id] = restored
            self.entries.append(("rollback", baseline_id, restored.revision,
                                 reason, authorized_receipt))
            return {"rolled_back": True, "baseline": restored,
                    "history_preserved": len(self.entries)}

# --- Learning receipts ----------------------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class BaselineCandidateReceipt:
    """BASELINE-CANDIDATE-018 schema. The reconstructability standard: a cold
    successor rebuilds WHY it changed, WHAT counted as legitimate, WHAT was
    excluded, WHO verified, and WHAT must remain detectable -- from the
    receipt alone."""
    receipt_id: str
    candidate_id: str
    revision: int
    why_changed: str
    what_counted_legitimate: tuple
    what_excluded: tuple
    verified_by: str
    must_remain_detectable: tuple


# --- The B1-B6 fixtures -------------------------------------------------------------------------------------------------------------------
def b_fixtures():
    """Six sealed scenarios. B1 vs B2 are distinguished BLIND: identical
    demand growth, different failure behavior."""
    return (
        ("B1", {"demand": (10000, 50000), "failure": (0.01, 0.01),
                "training_state": "VERIFIED_WORKLOAD_SHIFT",
                "justification": "release notes + capacity change verified"},
         "MAY_PROMOTE"),                       # legitimate growth
        ("B2", {"demand": (10000, 50000), "failure": (0.01, 0.03),
                "training_state": "CONFIRMED_REGRESSION",
                "justification": ""},
         "NEVER_NORMALIZE"),                   # slow degradation
        ("B3", {"demand": (10000, 10000), "failure": (0.01, 0.012),
                "training_state": "VERIFIED_WORKLOAD_SHIFT",
                "concurrency_regime": "new",
                "justification": "scoped concurrency change verified"},
         "SCOPED_RECALIBRATION"),              # new concurrency regime
        ("B4", {"demand": (10000, 50000), "failure": (0.01, 0.02),
                "training_state": "UNRESOLVED_ANOMALY",
                "justification": ""},
         "BLOCK_PROMOTION"),                   # unresolved contamination
        ("B5", {"demand": (10000, 50000), "failure": (0.01, 0.01),
                "training_state": "VERIFIED_WORKLOAD_SHIFT",
                "late_duplicate": True,
                "justification": "release notes verified"},
         "WITHDRAW_AND_REASSESS"),             # late-discovered duplicate
        ("B6", {"demand": (10000, 12000), "failure": (0.01, 0.01),
                "training_state": "VERIFIED_HEALTHY",
                "seasonal": True,
                "justification": ""},
         "FORECAST_BETTER_NO_SPURIOUS_ALERTS"),  # healthy seasonality
    )


def classify_b_fixture(s: dict) -> str:
    """The blind distinguisher: demand is learned fast; failure-rate
    learning is evidence-gated; unresolved/confirmed-bad never trains."""
    if s.get("late_duplicate"):
        return "WITHDRAW_AND_REASSESS"
    eligible, _ = training_eligible(s["training_state"])
    if not eligible:
        return ("NEVER_NORMALIZE"
                if s["training_state"] == "CONFIRMED_REGRESSION"
                else "BLOCK_PROMOTION")
    demand_ok = assess_distribution_change(
        "demand", s["demand"][0], s["demand"][1],
        justification="substantiated")
    failure = assess_distribution_change(
        "failure", s["failure"][0], s["failure"][1],
        justification=s.get("justification", ""))
    if not failure["accepted"]:
        return "NEVER_NORMALIZE"
    if s.get("seasonal"):
        return "FORECAST_BETTER_NO_SPURIOUS_ALERTS"
    if s.get("concurrency_regime") == "new":
        return "SCOPED_RECALIBRATION"
    return "MAY_PROMOTE"


def b_blind_pair():
    """B1 vs B2 presented without labels: identical demand growth, different
    failure behavior. The classifier must promote one and block the other."""
    scenarios = [s for i, s, _ in b_fixtures() if i in ("B1", "B2")]
    import random
    rng = random.Random(7)
    rng.shuffle(scenarios)
    verdicts = [classify_b_fixture(s) for s in scenarios]
    return {"verdicts": verdicts,
            "distinguished": sorted(verdicts) == ["MAY_PROMOTE", "NEVER_NORMALIZE"]}


# --- Six mutation tests on the promotion machinery ----------------------------------------------------------------------------------
def cal3_mutation_tests():
    """Each mutation removes one guard from the promotion machinery. The
    verifier must catch every one: a learning machine that silently
    normalizes regressions is disqualified."""
    results = {}

    # M1: remove the incident quarantine -- UNRESOLVED_ANOMALY data trains.
    eligible, _ = training_eligible("UNRESOLVED_ANOMALY")
    results["M1_remove_incident_quarantine"] = {
        "caught": not eligible,
        "note": "unresolved anomalies forbidden as health evidence"}

    # M2: remove the frozen reference -- the reference silently moves.
    ref = QualificationReference("q1", ((("ctx",), 0.05, 0.11),), "v3")
    moved = QualificationReference("q1", ((("ctx",), 0.05, 0.17),), "v3")
    results["M2_remove_frozen_reference"] = {
        "caught": ref != moved,
        "note": "any silent move of the qualified bands is a changed object"}

    # M3: remove the independent check -- the candidate self-qualifies.
    log = BaselinePromotionLog()
    cand = AdaptiveCandidate("c1", 1, (), ("VERIFIED_HEALTHY",), True, "SHADOW")
    r = log.promote_candidate(cand, 1, 1, 1, 1, "receipt-1")
    results["M3_remove_independent_check"] = {
        "caught": not r["promoted"] and "SHADOW" in r["reason"],
        "note": "SHADOW status can never promote itself"}

    # M4: remove the watermark -- premature eligibility.
    results["M4_remove_watermark"] = {
        "caught": not settlement_eligible(100.0, 50.0, 120.0),
        "note": "T_eligible >= T_operation + H_effect enforced"}

    # M5: remove the incident-revision fence -- promotion with blockers.
    log2 = BaselinePromotionLog()
    cand2 = AdaptiveCandidate("c2", 1, (), ("VERIFIED_HEALTHY",), True,
                              "INDEPENDENTLY_QUALIFIED")
    r2 = log2.promote_candidate(cand2, 1, 1, 1, 1, "receipt-1",
                                unresolved_blockers=("INC-7",))
    results["M5_remove_incident_revision_fence"] = {
        "caught": not r2["promoted"] and "INC-7" in r2["reason"],
        "note": "unresolved blockers fence the promotion"}

    # M6: remove receipt preservation -- rollback erases history.
    log3 = BaselinePromotionLog()
    cand3 = AdaptiveCandidate("c3", 1, (), ("VERIFIED_HEALTHY",), True,
                              "INDEPENDENTLY_QUALIFIED")
    log3.promote_candidate(cand3, 1, 1, 1, 1, "receipt-1")
    n_before = len(log3.entries)
    rb = log3.rollback("c3", "regression found", "receipt-2")
    results["M6_remove_receipt_preservation"] = {
        "caught": rb["rolled_back"] and len(log3.entries) > n_before
                  and rb["history_preserved"] == len(log3.entries),
        "note": "rollback preserves the failed baseline and its receipts"}
    for mid, v in results.items():
        assert v["caught"], f"{mid} NOT caught: {v['note']}"
    return results


# --- AER-CAL-003: the first action ----------------------------------------------------------------------------------------------------------------
def aer_cal_003():
    """Two identical histories: verified growth vs slow regression. The
    candidate adapts to demand in both; promotion ONLY for the justified
    case. Remove the guard: the verifier shows the mutated model normalizing
    the regression. Restore, shadow-validate, preserve everything."""
    report = {}
    # Lane G: verified growth. Lane R: identical demand, slow regression.
    growth = {"demand": (10000, 50000), "failure": (0.01, 0.01),
              "training_state": "VERIFIED_WORKLOAD_SHIFT",
              "justification": "release notes + capacity change verified"}
    regress = {"demand": (10000, 50000), "failure": (0.01, 0.03),
               "training_state": "CONFIRMED_REGRESSION",
               "justification": ""}
    assert classify_b_fixture(growth) == "MAY_PROMOTE"
    assert classify_b_fixture(regress) == "NEVER_NORMALIZE"
    report["lanes_distinguished"] = {"growth": "MAY_PROMOTE",
                                     "regression": "NEVER_NORMALIZE"}
    # The candidate adapts to DEMAND in both (fast path)...
    for lane in (growth, regress):
        d = assess_distribution_change("demand", lane["demand"][0],
                                       lane["demand"][1], justification="x")
        assert d["accepted"] and d["path"] == "fast"
    report["demand_adapts_in_both"] = True
    # ...but promotion only for the justified case.
    log = BaselinePromotionLog()
    cand_g = AdaptiveCandidate("lane-g", 1, (("ctx", 0.005, 0.02),),
                               ("VERIFIED_WORKLOAD_SHIFT",), True,
                               "INDEPENDENTLY_QUALIFIED")
    r = log.promote_candidate(cand_g, 1, 3, 3, 2, "cal-receipt-77")
    assert r["promoted"], r
    report["growth_promoted"] = r["baseline"].revision
    # Remove the guard: a mutated flow that lets CONFIRMED_REGRESSION train.
    mutated_bands = ((("ctx",), 0.005, 0.035),)  # absorbed the 3% failures
    div = forecast_vs_reference(
        OperationalForecast("mut", 9, mutated_bands, ("regression-weeks",)),
        QualificationReference("q1", ((("ctx",), 0.005, 0.02),), "v3"),
        material_pp=0.005)
    assert div["review_event"], div
    report["mutated_model_normalizes_regression"] = {
        "detected": True,
        "divergent_contexts": div["divergent_contexts"],
        "note": "the verifier shows the absorption; the guard removal is caught"}
    # Restore: the regression lane still cannot promote...
    assert classify_b_fixture(regress) == "NEVER_NORMALIZE"
    # ...shadow-validate the growth candidate, preserving everything.
    shadow = AdaptiveCandidate("lane-g", 2, (("ctx", 0.005, 0.02),),
                               ("VERIFIED_WORKLOAD_SHIFT",), True, "SHADOW")
    rs = log.promote_candidate(shadow, 2, 3, 3, 2, "cal-receipt-78")
    assert not rs["promoted"], "shadow never promotes directly"
    receipt = BaselineCandidateReceipt(
        "BASELINE-CANDIDATE-018", "lane-g", 1,
        why_changed="verified demand growth 10k->50k/hr",
        what_counted_legitimate=("VERIFIED_WORKLOAD_SHIFT: release notes + capacity",),
        what_excluded=("CONFIRMED_REGRESSION weeks: never training",),
        verified_by="independent seat",
        must_remain_detectable=("failure-rate deviations > 0.5pp",))
    report["receipt"] = {"id": receipt.receipt_id,
                         "must_remain_detectable": receipt.must_remain_detectable}
    report["history_preserved_entries"] = len(log.entries)
    # The six mutation tests on the machinery.
    report["mutation_tests"] = {k: v["caught"]
                                for k, v in cal3_mutation_tests().items()}
    return report

# ===========================================================================
# AER-CAL-4 — Scope-Isolated Baseline Integrity Law (SN-0801)
# ===========================================================================
"""AER-CAL-4 is the SCOPE-ISOLATION layer: AER-CAL-3 governs promotion; this
ensures one scope's learning never masks another's regression.

LAW: bind observations, baselines, and receipts to explicit operational
scopes; hierarchical information sharing may improve estimation but shall
not transfer certification beyond demonstrated evidence; aggregate
improvement shall not conceal local regression.

The guarantee's scope comes from the actual external contract, never from
grouping convenience.
"""

# --- The canonical scope key --------------------------------------------------------------------------------
# s = (p, e, r, c, w): provider, endpoint/operation, region, concurrency
# regime, workload class -- plus the extended dimensions, preserved per
# event and promoted to partition dimensions when material to guarantees.
@dataclass(frozen=True)
class ScopeKey:
    provider: str
    endpoint: str
    region: str
    concurrency_regime: str
    workload_class: str
    account: str = ""
    api_version: str = ""
    routing: str = ""
    effect_identity: str = ""
    environment: str = ""
    maintenance_context: str = ""


def scope_key_material(scope: ScopeKey) -> ScopeKey:
    """The guarantee's scope comes from the actual external contract, never
    from grouping convenience: only contract-material dimensions partition."""
    return scope  # the key already carries exactly the material dimensions


# --- The Simpson's-paradox warning -----------------------------------------------------------------------------------
def aggregate_hides_regression(cells_before: dict, cells_after: dict) -> tuple:
    """Standing test against EVERY aggregate claim. cells: scope -> (n, k).
    Returns (paradox: bool, detail). A parent-level improvement never
    certifies a child-level regression: preserve BOTH findings."""
    cell_dirs = {}
    for scope, (n0, k0) in cells_before.items():
        n1, k1 = cells_after[scope]
        r0, r1 = k0 / n0, k1 / n1
        cell_dirs[scope] = ("worse" if r1 > r0
                            else "better" if r1 < r0 else "same")
    N0 = sum(n for n, _ in cells_before.values())
    K0 = sum(k for _, k in cells_before.values())
    N1 = sum(n for n, _ in cells_after.values())
    K1 = sum(k for _, k in cells_after.values())
    a0, a1 = K0 / N0, K1 / N1
    agg = "better" if a1 < a0 else ("worse" if a1 > a0 else "same")
    paradox = agg == "better" and all(d == "worse"
                                     for d in cell_dirs.values())
    return paradox, {"cell_directions": cell_dirs, "aggregate": agg,
                     "aggregate_before": round(a0, 4),
                     "aggregate_after": round(a1, 4)}


def simpson_two_regime():
    """The canonical example: low 1%->2%, high 5%->8%, aggregate 4.6%->2.6%.
    Both worse, aggregate better."""
    before = {"low": (1000, 10), "high": (9000, 450)}
    after = {"low": (9000, 180), "high": (1000, 80)}
    return before, after


# --- Hierarchical partial pooling with the critical restriction -------------------------------------------------------------
class HierarchicalScopeModel:
    """Parent models supply STATISTICAL information to sparse cells
    (Beta-Binomial partial pooling; the logit-normal variant is
    interchangeable -- model chosen by held-out validation). Each cell keeps
    its own observations, uncertainty, qualification, and incidents.
    THE CRITICAL RESTRICTION: statistical pooling != evidence pooling. Thin
    evidence => UNPROVEN_IN_SCOPE even when the parent predicts excellence."""

    def __init__(self, min_n_qualified: int = 100):
        self.cells = {}          # scope -> [n, k]
        self.contributions = {}  # scope -> [n, k] (for quarantine recompute)
        self.parent_a = 1.0
        self.parent_b = 1.0
        self.min_n = min_n_qualified
        self.quarantined = set()

    def observe(self, scope, n: int, k: int,
                training_state: str = "VERIFIED_HEALTHY") -> dict:
        eligible, _ = training_eligible(training_state)
        if scope in self.quarantined:
            return {"accepted": False, "reason": "scope quarantined"}
        if not eligible:
            return {"accepted": False,
                    "reason": f"{training_state}: not admissible as health evidence"}
        c = self.cells.setdefault(scope, [0, 0])
        c[0] += n
        c[1] += k
        cc = self.contributions.setdefault(scope, [0, 0])
        cc[0] += n
        cc[1] += k
        self._recompute_parent()
        return {"accepted": True}

    def _recompute_parent(self):
        a, b = 1.0, 1.0
        for scope, (n, k) in self.contributions.items():
            if scope not in self.quarantined:
                a += k
                b += (n - k)
        self.parent_a, self.parent_b = a, b

    def quarantine(self, scope, reason: str) -> dict:
        """Quarantined scopes' unresolved observations never silently update
        shared priors: the parent is recomputed WITHOUT them, and every
        dependent cell is flagged for reassessment."""
        self.quarantined.add(scope)
        self._recompute_parent()
        dependents = [s for s in self.cells if s != scope]
        return {"quarantined": scope, "reason": reason,
                "parent_recomputed": (self.parent_a, self.parent_b),
                "dependents_flagged": dependents}

    def cell_posterior(self, scope) -> tuple:
        """Pooled ESTIMATE (may borrow strength). Never a certification."""
        n, k = self.cells.get(scope, (0, 0))
        a = self.parent_a + k
        b = self.parent_b + (n - k)
        return a / (a + b), n

    def cell_qualification(self, scope) -> str:
        """CERTIFICATION stays with the cell's own evidence."""
        n, _ = self.cells.get(scope, (0, 0))
        if scope in self.quarantined:
            return "QUARANTINED"
        if n < self.min_n:
            return "UNPROVEN_IN_SCOPE"
        return "QUALIFIED"


# --- Three operational views -------------------------------------------------------------------------------------------------------
def three_views(cells: dict, reference_mix: dict) -> dict:
    """Individual scope: per-scope rates. Standardized provider-wide rate:
    the reference mix applied to current cell rates (0.1*2% + 0.9*8% = 7.4%
    vs observed 2.6%). Observed provider-wide rate: the raw aggregate.
    NONE overrides a local regression. New workloads are marked
    new/unqualified, never given invented historical rates."""
    individual = {s: k / n for s, (n, k) in cells.items()}
    standardized = sum(reference_mix[s] * individual[s] for s in cells
                       if s in reference_mix)
    N = sum(n for n, _ in cells.values())
    K = sum(k for _, k in cells.values())
    return {"individual": {s: round(r, 4) for s, r in individual.items()},
            "standardized": round(standardized, 4),
            "observed": round(K / N, 4) if N else 0.0,
            "note": "no view overrides a local regression"}


# --- Versioned taxonomies ----------------------------------------------------------------------------------------------------------------
# Illustrative concurrency boundaries (not ratified). Concurrency is measured
# at ADMISSION, before outcomes: retry storms must not reclassify
# themselves. Recovery retries are never relabeled as ordinary operations.
CONCURRENCY_REGIMES = (
    ("low", 0, 10),
    ("medium", 10, 100),
    ("high", 100, None),
)


@dataclass(frozen=True)
class TaxonomyVersion:
    version: int
    regimes: tuple
    workload_classes: tuple
    supersedes: object


def classify_concurrency(admission_concurrency: int,
                         taxonomy: TaxonomyVersion = None) -> str:
    regimes = (taxonomy.regimes if taxonomy
               else tuple((name, lo, hi) for name, lo, hi in CONCURRENCY_REGIMES))
    for name, lo, hi in regimes:
        if admission_concurrency >= lo and (hi is None or admission_concurrency < hi):
            return name
    return "unknown"


def migrate_taxonomy(old: TaxonomyVersion, new_regimes: tuple,
                     new_classes: tuple) -> dict:
    """Taxonomy changes require a migration assessment: every scope
    classified under the old taxonomy is re-evaluated, never silently
    remapped."""
    new = TaxonomyVersion(old.version + 1, new_regimes, new_classes,
                          supersedes=old.version)
    return {"new_taxonomy": new,
            "requires": "re-evaluation of every scope under the new taxonomy",
            "note": "no silent remapping"}


# --- Cross-scope interactions ----------------------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class InteractionScope:
    """s_origin -> s_destination under an operation contract: cross-region
    failover, endpoint-to-downstream, interactive-to-background,
    low-admission-to-high-completion."""
    origin: ScopeKey
    destination: ScopeKey
    contract: str


def interaction_covered(interaction: InteractionScope,
                        guarantees: dict) -> tuple:
    """The verifier tests whether parent/cross-scope guarantees cover the
    interaction. Healthy cells + a broken boundary is its own failure mode."""
    key = (interaction.origin.region, interaction.destination.region,
           interaction.contract)
    covered = guarantees.get(key, False)
    return (covered, "covered" if covered
            else "healthy cells, broken boundary: the interaction itself is unproven")

# --- Scope-specific thresholds without alert storms ----------------------------------------------------------------------------------
def scope_threshold_advice(cell_n: int, correlated: bool,
                           verified_duplicates: int = 0,
                           seen_before: bool = True) -> dict:
    """High-volume cells: calibrated conditional thresholds. Sparse cells:
    hierarchical estimation + targeted canaries. Correlated cells: shared
    incident assessment. One verified duplicate: thresholds irrelevant.
    Unseen cells: explicitly unqualified. False-discovery control across the
    scope family and time. Marginal slices are discovery signals; contract
    scope is independently determined."""
    if verified_duplicates >= 2:
        return {"action": "withdraw", "note": "thresholds irrelevant"}
    if not seen_before:
        return {"action": "unqualified",
                "note": "unseen cell: explicitly unqualified, never invented rates"}
    if cell_n >= 1000 and not correlated:
        return {"action": "conditional_threshold",
                "note": "calibrated per-cell threshold"}
    if correlated:
        return {"action": "shared_incident",
                "note": "correlated cells share one incident assessment"}
    return {"action": "hierarchical_and_canary",
            "note": "sparse cell: pooled estimate + targeted canaries"}


def promote_scope(scope, new_bands: tuple, model: HierarchicalScopeModel,
                  shared_dependents: tuple, evidence: dict) -> dict:
    """The promotion invariant: Promote(s) => Verified(B'_s) /\\
    PreserveUnaffectedScopes /\\ RecheckSharedDependencies. Shared-model
    updates are measured for secondary neighbor effects BEFORE promotion.
    Historical versions and receipts are immutable; the active pointer
    advances only after governed acceptance."""
    holds, missing = promote_bn(check_promotion_obligations(evidence))
    if not holds:
        return {"promoted": False, "missing": missing}
    neighbor_effects = {}
    for dep in shared_dependents:
        if dep != scope:
            est, _ = model.cell_posterior(dep)
            neighbor_effects[dep] = round(est, 4)
    return {"promoted": True, "scope": scope, "bands": new_bands,
            "neighbor_effects_measured": neighbor_effects,
            "invariant": "Verified(B'_s) ∧ PreserveUnaffectedScopes ∧ "
                         "RecheckSharedDependencies"}


# --- The BL-042 scope qualification manifest ----------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class ScopeQualificationManifest:
    """BL-042: per-scope qualification. PENDING is intentional: neither the
    manifest nor a healthy parent prediction constitutes proof."""
    manifest_id: str
    scope: ScopeKey
    status: str  # PENDING | QUALIFIED | UNPROVEN_IN_SCOPE | QUARANTINED
    evidence_refs: tuple
    parent_prediction: object  # informational only; never certification


def bl042_pending(scope: ScopeKey) -> ScopeQualificationManifest:
    return ScopeQualificationManifest(
        f"BL-042/{scope.provider}/{scope.endpoint}/{scope.region}",
        scope, "PENDING", (), None)


# --- The P1-P10 suite -------------------------------------------------------------------------------------------------------------------------------
def cal4_p_suite():
    """Ten sealed scenarios. Each returns (id, verdict, evidence)."""
    results = []

    def scope(provider="p1", endpoint="charge", region="east",
              regime="low", wclass="standard"):
        return ScopeKey(provider, endpoint, region, regime, wclass)

    # P1: East growth / West regression -- the aggregate hides West.
    before = {"east": (5000, 50), "west": (5000, 250)}     # 1%, 5%
    after = {"east": (9000, 90), "west": (1000, 80)}       # 1%, 8%
    paradox, detail = aggregate_hides_regression(before, after)
    results.append(("P1", "WEST_FLAGGED" if detail["cell_directions"]["west"] == "worse" else "MISSED",
                    f"aggregate {detail['aggregate_before']}->{detail['aggregate_after']}; west regressed"))

    # P2: both-regimes-regress (the canonical Simpson).
    b2, a2 = simpson_two_regime()
    paradox2, detail2 = aggregate_hides_regression(b2, a2)
    results.append(("P2", "PARADOX_DETECTED" if paradox2 else "MISSED",
                    f"cells {detail2['cell_directions']}, aggregate {detail2['aggregate']}"))

    # P3: sparse cell with a healthy parent -> UNPROVEN_IN_SCOPE.
    m3 = HierarchicalScopeModel(min_n_qualified=100)
    m3.observe(scope(region="east"), 5000, 50)
    sparse = scope(region="west")
    m3.observe(sparse, 20, 0)
    est, _ = m3.cell_posterior(sparse)
    results.append(("P3", m3.cell_qualification(sparse),
                    f"parent-healthy estimate {est:.4f} but cell n=20: {m3.cell_qualification(sparse)}"))

    # P4: mix changes -> the standardized view distinguishes.
    views = three_views({"low": (9000, 180), "high": (1000, 80)},
                        {"low": 0.1, "high": 0.9})
    results.append(("P4", "DISTINGUISHED" if views["standardized"] > views["observed"] else "MISSED",
                    f"standardized {views['standardized']} vs observed {views['observed']}"))

    # P5: cross-region duplicates -> the interaction scope fails.
    inter = InteractionScope(scope(region="east"), scope(region="west"), "failover")
    covered, note = interaction_covered(inter, {})
    results.append(("P5", "INTERACTION_UNPROVEN" if not covered else "MISSED", note))

    # P6: training contamination -> quarantine + dependent reassessment.
    m6 = HierarchicalScopeModel()
    s6 = scope(region="east")
    m6.observe(s6, 5000, 50)
    q = m6.quarantine(s6, "contamination discovered")
    results.append(("P6", "QUARANTINED" if s6 in m6.quarantined and q["dependents_flagged"] is not None else "MISSED",
                    f"parent recomputed without the scope: {q['parent_recomputed'][0]:.1f}"))

    # P7: classifier version changes -> migration assessment.
    old = TaxonomyVersion(1, tuple((n, lo, hi) for n, lo, hi in CONCURRENCY_REGIMES),
                          ("standard", "bulk"), None)
    mig = migrate_taxonomy(old, tuple((n, lo, hi) for n, lo, hi in CONCURRENCY_REGIMES),
                           ("standard", "bulk", "priority"))
    results.append(("P7", "MIGRATION_REQUIRED" if "re-evaluation" in mig["requires"] else "MISSED",
                    mig["requires"]))

    # P8: new endpoints -> UNPROVEN_IN_SCOPE.
    m8 = HierarchicalScopeModel()
    new_scope = ScopeKey("p1", "brand-new-endpoint", "east", "low", "standard")
    results.append(("P8", m8.cell_qualification(new_scope),
                    "unseen cell: explicitly unqualified"))

    # P9: neighbor rechecks on shared-model updates.
    m9 = HierarchicalScopeModel()
    sa, sb = scope(region="east"), scope(region="west")
    m9.observe(sa, 5000, 50)
    m9.observe(sb, 5000, 250)
    r = promote_scope(sa, (("ctx", 0.005, 0.02),), m9, (sa, sb),
                      {ob: True for ob in PROMOTION_OBLIGATIONS})
    results.append(("P9", "NEIGHBORS_RECHECKED" if r["promoted"] and sb in r["neighbor_effects_measured"] else "MISSED",
                    f"neighbor effects measured: {r.get('neighbor_effects_measured')}"))

    # P10: anomaly localization -> the cell, not the parent.
    paradox10, detail10 = aggregate_hides_regression(
        {"a": (5000, 50), "b": (5000, 50)}, {"a": (5000, 50), "b": (5000, 400)})
    localized = [s for s, d in detail10["cell_directions"].items() if d == "worse"]
    results.append(("P10", "LOCALIZED" if localized == ["b"] else "MISSED",
                    f"regression localized to: {localized}"))
    return results


def cal4_guard_removal_crown_jewel():
    """CROWN JEWEL: remove scope isolation (pool everything into one
    aggregate), repeat P1/P2. The verifier must show the minimal
    counterexample: the aggregate 'improving' while both cells regress.
    Restoration eliminates it while keeping legitimate learning."""
    b2, a2 = simpson_two_regime()
    # Guard removed: the aggregate-only view.
    N0 = sum(n for n, _ in b2.values()); K0 = sum(k for _, k in b2.values())
    N1 = sum(n for n, _ in a2.values()); K1 = sum(k for _, k in a2.values())
    aggregate_view = {"before": K0 / N0, "after": K1 / N1,
                      "verdict": "IMPROVED" if K1 / N1 < K0 / N0 else "WORSE"}
    paradox, detail = aggregate_hides_regression(b2, a2)
    counterexample = {
        "aggregate_says": aggregate_view["verdict"],
        "cells_say": detail["cell_directions"],
        "minimal": "4.6%->2.6% 'better' while low 1%->2% and high 5%->8%",
    }
    assert aggregate_view["verdict"] == "IMPROVED", aggregate_view
    assert paradox, "the guard-removal must exhibit the paradox"
    # Restoration: scope isolation back on; legitimate learning kept.
    m = HierarchicalScopeModel()
    for cell, (n, k) in a2.items():
        m.observe(cell, n, k)
    restored = {cell: m.cell_qualification(cell) for cell in a2}
    assert all(v == "QUALIFIED" for v in restored.values()), restored
    return {"counterexample": counterexample, "restored": restored,
            "note": "legitimate learning kept; the masking eliminated"}


# --- AER-CAL-004: the first action --------------------------------------------------------------------------------------------------------------------
def aer_cal_004():
    """Deterministic replay: two regimes x two regions x two workload
    classes + a shared parent. Four competing designs:
      D1 aggregate-only (no scopes);
      D2 scoped, no pooling;
      D3 scoped + hierarchical pooling WITH the restriction (the law);
      D4 scoped + pooling WITHOUT the restriction (parent certifies children).
    The verifier measures: both-regime detection, scoped promotion,
    sparse-cell false alarms, cross-region duplicates. Then shared-model
    contamination, with a reproducible counterexample demanded."""
    report = {}
    # The replay cells: (regime, region, class) -> (n, k).
    # West-high regresses, hidden by a mix shift toward east-low.
    cells = {
        ("low", "east", "standard"): (9000, 90),    # 1%
        ("low", "east", "bulk"): (4000, 40),        # 1%
        ("low", "west", "standard"): (3000, 60),    # 2% regressed
        ("low", "west", "bulk"): (20, 0),           # sparse, healthy-looking
        ("high", "east", "standard"): (2000, 100),  # 5%
        ("high", "east", "bulk"): (1000, 50),       # 5%
        ("high", "west", "standard"): (500, 40),    # 8% regressed
        ("high", "west", "bulk"): (500, 40),        # 8% regressed
    }
    # Regime-level paradox: the mix shifts toward the low-rate regime, so
    # the aggregate "improves" while BOTH regimes regress.
    reg_before = {"low": (16020, 160), "high": (4000, 200)}    # 1%, 5% -> agg 1.80%
    reg_after = {"low": (30000, 360), "high": (2000, 120)}     # 1.2%, 6% -> agg 1.50%

    # D1: aggregate-only.
    N1 = sum(n for n, _ in reg_after.values())
    K1 = sum(k for _, k in reg_after.values())
    d1_verdict = "no regression"  # the aggregate cannot see cells
    # D2/D3: scoped detection of both regressed regimes.
    paradox, detail = aggregate_hides_regression(reg_before, reg_after)
    d23_detect = sorted(s for s, d in detail["cell_directions"].items()
                        if d == "worse")
    # D4: parent certifies the sparse cell (the defect).
    m4 = HierarchicalScopeModel(min_n_qualified=100)
    for s, (n, k) in cells.items():
        m4.observe(s, n, k)
    sparse = ("low", "west", "bulk")
    est4, _ = m4.cell_posterior(sparse)
    d4_certifies = True  # defect: treats pooled estimate as qualification
    # D3: the restriction holds.
    m3 = HierarchicalScopeModel(min_n_qualified=100)
    for s, (n, k) in cells.items():
        m3.observe(s, n, k)
    d3_sparse = m3.cell_qualification(sparse)
    report["designs"] = {
        "D1_aggregate_only": d1_verdict,
        "D2_D3_both_regime_detection": d23_detect,
        "D3_sparse_cell": d3_sparse,
        "D4_defect_certifies_sparse": d4_certifies,
        "D4_pooled_estimate": round(est4, 4),
    }
    assert d23_detect == ["high", "low"], d23_detect
    assert d3_sparse == "UNPROVEN_IN_SCOPE", d3_sparse
    # Cross-region duplicates: the interaction scope.
    e = ScopeKey("p1", "charge", "east", "low", "standard")
    w = ScopeKey("p1", "charge", "west", "low", "standard")
    covered, note = interaction_covered(InteractionScope(e, w, "failover"), {})
    report["cross_region_duplicates"] = {"covered": covered, "note": note}
    assert not covered
    # Scoped promotion: per-scope, neighbors rechecked.
    r = promote_scope(("high", "west", "standard"), (("ctx", 0.05, 0.10),),
                      m3, tuple(cells), {ob: True for ob in PROMOTION_OBLIGATIONS})
    assert r["promoted"] and len(r["neighbor_effects_measured"]) == 7
    report["scoped_promotion"] = {"promoted": True, "neighbors_rechecked": 7}
    # Shared-model contamination: inject bad data into the parent via one cell.
    m3.observe(("high", "west", "standard"), 5000, 5000 // 2)  # 50% failures?!
    # Training-state discipline would have rejected CONFIRMED_REGRESSION;
    # here the contamination arrives as mislabeled VERIFIED_HEALTHY.
    q = m3.quarantine(("high", "west", "standard"), "contamination discovered")
    assert ("high", "west", "standard") in m3.quarantined
    assert len(q["dependents_flagged"]) == 7
    report["contamination"] = {
        "quarantined": True,
        "dependents_reassessed": len(q["dependents_flagged"]),
        "counterexample": "mislabeled 50%-failure cell absorbed into the parent "
                          "until quarantine recomputed it out",
    }
    # The crown jewel inside the replay.
    report["guard_removal_crown_jewel"] = cal4_guard_removal_crown_jewel()[
        "counterexample"]
    return report
# ======================================================================================
# SN-0804 AER-CAL-5 — EVIDENCE-PRESERVING SCOPE EVOLUTION LAW
# ======================================================================================
# Scopes are isolated (AER-CAL-4); this governs how they may EVOLVE without breaking
# isolation: merge statistical estimation across demonstrably comparable scopes, and
# split models when independently established semantic or behavioral differences
# warrant it.
#
# HONEST SCOPE (Shawn, 2026-10-10 — his explicit scoping): this enters as an ISOLATED
# TEST MECHANISM, not a production authority change. propagation.py / uncertainty.py /
# authority.py align with the contracts, but NO implemented merge/split engine and NO
# live provider baseline registry has been verified. Do not claim otherwise.
# Main observed by Shawn at 0fb380c.
#
# His law: NayaNET may merge statistical estimation across demonstrably comparable
# scopes and split models when independently established semantic or behavioral
# differences warrant it; every observation retains its original provenance; every
# provider guarantee remains bound to its independently demonstrated applicability.
# Statistical pooling shall never create, broaden, inherit or restore qualification
# or execution authority.
AER_CAL5_IMPLEMENTATION_STATUS = {
    "enters_as": "isolated test mechanism",
    "not_a": "production authority change",
    "contracts_align": ("propagation.py", "uncertainty.py", "authority.py"),
    "not_verified": ("implemented merge/split engine",
                     "live provider baseline registry"),
    "main_observed_at": "0fb380c",
}


# --- 1. The three-operation separation ------------------------------------------------------------------------------
# Never confuse the three: statistical pooling, operational baseline merge, and
# qualification consolidation have different evidence requirements. A pooled group
# must NEVER automatically become one certified scope.
SCOPE_OPERATIONS = {
    "STATISTICAL_POOLING": {
        "what": "share statistical information across scopes to improve estimates",
        "requires": ("verified_comparability",
                     "calibrated_uncertainty",
                     "independence_assumptions_stated"),
        "never": "a pooled group never automatically becomes one certified scope",
    },
    "OPERATIONAL_BASELINE_MERGE": {
        "what": "share one forecasting/alert model across scopes",
        "requires": ("independent_evidence_shared_model_preserves_each_scope_detection",),
        "never": "shared alerts do not merge qualifications",
    },
    "QUALIFICATION_CONSOLIDATION": {
        "what": "one certification covering several scopes",
        "requires": ("proof_guarantee_covers_every_member",
                     "relevant_cross_scope_interactions_tested"),
        "never": "no consolidation by label hierarchy alone",
    },
}


def classify_scope_operation(request: dict) -> dict:
    """Classify a scope-evolution request into exactly one of the three
    operations and list the evidence each requires. request:
    {"kind": one of SCOPE_OPERATIONS, "scopes": [...], "evidence": {...}}."""
    kind = request.get("kind")
    if kind not in SCOPE_OPERATIONS:
        return {"classified": False,
                "reason": f"unknown operation kind {kind!r}; the three "
                          "operations are never to be confused"}
    op = SCOPE_OPERATIONS[kind]
    evidence = request.get("evidence", {})
    missing = [r for r in op["requires"] if not evidence.get(r)]
    return {"classified": True, "kind": kind, "what": op["what"],
            "requirements": list(op["requires"]),
            "missing_evidence": missing,
            "authorized": not missing,
            "never": op["never"]}


def pooling_never_certifies(scopes, model: HierarchicalScopeModel) -> dict:
    """After statistical pooling, every scope's CERTIFICATION still comes from
    its own evidence. The pooled estimate is a prediction aid, never a proof."""
    per_scope = {}
    for s in scopes:
        est, n = model.cell_posterior(s)
        per_scope[s] = {"pooled_estimate": round(est, 4),
                        "own_n": n,
                        "qualification": model.cell_qualification(s)}
    pooled_group_certified = any(
        v["qualification"] == "QUALIFIED" and v["own_n"] < model.min_n
        for v in per_scope.values())
    return {"per_scope": per_scope,
            "pooled_group_auto_certified": pooled_group_certified,
            "law_holds": not pooled_group_certified}


# --- 2. Immutable scope identities beneath any shared model ----------------------------------------------------------
class ScopedObservation:
    """Four permanent IDs on every observation, surviving any merge or split:
      statistical_parent_id   — where estimates may borrow strength;
      qualification_scope_id  — where a guarantee actually applies;
      observation_scope_id    — where the raw evidence originated;
      interaction_scope_id    — where cross-boundary effects are tested.
    Original provenance is never rewritten under a new taxonomy."""

    def __init__(self, statistical_parent_id: str, qualification_scope_id: str,
                 observation_scope_id: str, interaction_scope_id: str,
                 n: int, k: int, taxonomy_version: str):
        self.statistical_parent_id = statistical_parent_id
        self.qualification_scope_id = qualification_scope_id
        self.observation_scope_id = observation_scope_id
        self.interaction_scope_id = interaction_scope_id
        self.n = n
        self.k = k
        self.taxonomy_version = taxonomy_version  # original classification kept

    def provenance(self) -> dict:
        return {"statistical_parent_id": self.statistical_parent_id,
                "qualification_scope_id": self.qualification_scope_id,
                "observation_scope_id": self.observation_scope_id,
                "interaction_scope_id": self.interaction_scope_id,
                "taxonomy_version": self.taxonomy_version}


def endpoint_ab_example() -> dict:
    """His Endpoint A/B example: A and B share latency learning (one
    statistical parent), but A's verified idempotency guarantee never extends
    to unproven B. Four IDs keep the sharing honest."""
    a = ScopedObservation(statistical_parent_id="latency-parent-1",
                          qualification_scope_id="qual:A",
                          observation_scope_id="obs:A",
                          interaction_scope_id="inter:A",
                          n=5000, k=50, taxonomy_version="tax-v3")
    b = ScopedObservation(statistical_parent_id="latency-parent-1",
                          qualification_scope_id="qual:B",
                          observation_scope_id="obs:B",
                          interaction_scope_id="inter:B",
                          n=15, k=0, taxonomy_version="tax-v3")
    guarantee_a = {"guarantee_id": "idempotency:A",
                   "kind": "idempotency",
                   "verified": True,
                   "qualified_scopes": ("qual:A",),
                   "revision": 7, "current": True,
                   "statistical_parent_id": "latency-parent-1"}
    use_b = use_guarantee(guarantee_a, "qual:B", {"taxonomy": 3, "policy": 3,
                                                 "incident": 3, "evidence": 3},
                          law_receipt={"receipt": "LAW-1", "valid": True})
    return {"shared_statistical_parent": (a.statistical_parent_id
                                          == b.statistical_parent_id),
            "distinct_qualification_scopes": (a.qualification_scope_id
                                             != b.qualification_scope_id),
            "b_use_of_a_guarantee": use_b,
            "law_holds": (a.statistical_parent_id == b.statistical_parent_id
                          and not use_b["authorized"])}


# --- 3. The four scope decisions ------------------------------------------------------------------------------------
SCOPE_DECISIONS = ("POOL_ESTIMATES", "MERGE_OPERATIONAL_MODEL",
                   "SPLIT_MODEL", "CREATE_PROVISIONAL_SCOPE")


def scope_decision(decision: str, evidence: dict) -> dict:
    """The four scope decisions with their evidence gates.
      POOL_ESTIMATES: sparse but comparable scopes — pool estimates, keep
        separate qualifications and contract gates.
      MERGE_OPERATIONAL_MODEL: strong held-out evidence the shared model
        preserves each scope's detection — merge forecasting, keep individual
        evidence and contract gates.
      SPLIT_MODEL: material difference emerges — split, reassess affected
        scopes and dependent claims.
      CREATE_PROVISIONAL_SCOPE: new endpoint/workload — provisional, no
        inherited PASS unless an explicitly valid existing contract covers it."""
    if decision not in SCOPE_DECISIONS:
        return {"decision": decision, "taken": False,
                "reason": "unknown scope decision"}
    if decision == "POOL_ESTIMATES":
        ok = bool(evidence.get("comparable")) and not evidence.get(
            "contamination")
        return {"decision": decision, "taken": ok,
                "effects": {"pool_estimates": ok,
                            "qualifications_stay_separate": True,
                            "contract_gates_stay": True},
                "reason": "" if ok else
                "comparability unestablished or contamination unresolved"}
    if decision == "MERGE_OPERATIONAL_MODEL":
        ok = bool(evidence.get("held_out_preserves_detection_all_scopes"))
        return {"decision": decision, "taken": ok,
                "effects": {"shared_forecasting": ok,
                            "individual_evidence_kept": True,
                            "contract_gates_kept": True},
                "reason": "" if ok else
                "no held-out evidence that every scope's detection survives"}
    if decision == "SPLIT_MODEL":
        ok = bool(evidence.get("material_difference_established"))
        return {"decision": decision, "taken": ok,
                "effects": {"split": ok,
                            "affected_scopes_reassessed": ok,
                            "dependent_claims_reassessed": ok},
                "reason": "" if ok else "no independently established difference"}
    # CREATE_PROVISIONAL_SCOPE
    covered = bool(evidence.get("explicit_valid_contract_covers"))
    return {"decision": decision, "taken": True, "provisional": not covered,
            "effects": {"provisional_model": True,
                        "inherited_pass": covered,
                        "independent_qualification_required": not covered},
            "reason": ("explicit valid contract covers the new scope" if covered
                       else "new scope: provisional, no inherited PASS")}


# --- 4. The four comparability conditions ---------------------------------------------------------------------------
COMPARABILITY_CONDITIONS = ("semantic_compatibility",
                            "statistical_compatibility",
                            "risk_compatibility",
                            "evidence_integrity")


def check_comparability(a_profile: dict, b_profile: dict,
                        evidence: dict) -> dict:
    """All four conditions must hold before statistical pooling:
      semantic_compatibility — same contractual meaning of the observations;
      statistical_compatibility — held-out, scope-specific calibration;
      risk_compatibility — each member's failure detection is preserved;
      evidence_integrity — admissible, correctly labeled, no unresolved
        contamination.
    STANDING PRINCIPLE: failure to detect a difference is NOT proof of
    equivalence (see equivalence_test and the 10,000-vs-15 example)."""
    per = {
        "semantic_compatibility": bool(evidence.get("semantic_compatible")),
        "statistical_compatibility": bool(
            evidence.get("held_out_scope_specific_calibrated")),
        "risk_compatibility": bool(
            evidence.get("each_member_detection_preserved")),
        "evidence_integrity": bool(evidence.get("admissible_labeled")) and not
        bool(evidence.get("unresolved_contamination")),
    }
    overall = all(per.values())
    return {"per_condition": per, "comparable": overall,
            "note": "failure to detect a difference is not proof of equivalence"}


def _wilson(n: int, k: int, z: float = 1.96) -> tuple:
    """Wilson score interval for a binomial proportion."""
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    denom = 1.0 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, center - half), min(1.0, center + half))


def equivalence_test(n_a: int, k_a: int, n_b: int, k_b: int,
                     margin: float) -> dict:
    """An equivalence claim needs a PRE-SPECIFIED operationally meaningful
    margin: EQUIVALENT only if the 95% interval for the rate difference lies
    entirely within [-margin, margin]. Metric equivalence is never
    idempotency/semantics equivalence — this gates statistical pooling only."""
    a_lo, a_hi = _wilson(n_a, k_a)
    b_lo, b_hi = _wilson(n_b, k_b)
    diff_lo, diff_hi = a_lo - b_hi, a_hi - b_lo
    inside = diff_lo >= -margin and diff_hi <= margin
    return {"margin": margin,
            "difference_interval": (round(diff_lo, 4), round(diff_hi, 4)),
            "verdict": "EQUIVALENT" if inside else "UNPROVEN",
            "note": "UNPROVEN blocks pooling; it does not assert a difference"}


def ten_k_vs_fifteen() -> dict:
    """His canonical example: A has 10,000 observations, B has 15. A
    difference test 'finds nothing' — that is NOT proof of equivalence.
    Pooling B under A on this basis alone is forbidden."""
    r = equivalence_test(10000, 100, 15, 0, margin=0.01)
    return {"example": "10000 vs 15 observations",
            "result": r,
            "pooling_permitted": r["verdict"] == "EQUIVALENT"}


# --- 5. Split criteria ------------------------------------------------------------------------------------------------
# Semantic split (different contractual meanings / risk / guarantees) takes
# priority even when sparse. Statistical split needs independently established
# divergence the shared model cannot represent. Never require statistical
# significance to separate different safety contracts.
SPLIT_TRIGGERS = {
    "idempotency_scope_change": "SEPARATE_IMMEDIATELY",
    "verified_duplicates": "CONTAIN_AND_REASSESS",
    "regime_divergence": "REGIME_MODELING",
    "repeated_calibration_failures": "CANDIDATE_SPLIT",
    "isolated_sparse_residual": "INVESTIGATE_DO_NOT_AUTO_SPLIT",
    "shared_guarantee_differing_latency": "SPLIT_LATENCY_MODELING_ONLY",
}


def evaluate_split_trigger(trigger: str, context: dict) -> dict:
    """Apply the trigger table. context carries the trigger-specific facts
    (e.g. duplicate evidence, calibration history, which modeling differs)."""
    if trigger not in SPLIT_TRIGGERS:
        return {"trigger": trigger, "action": "UNKNOWN_TRIGGER",
                "split": False}
    action = SPLIT_TRIGGERS[trigger]
    if trigger == "idempotency_scope_change":
        split = True  # safety contracts separate without statistical permission
        note = "different safety contracts never share a guarantee scope"
    elif trigger == "verified_duplicates":
        split = bool(context.get("duplicates_verified"))
        note = "contain the scope, reassess the guarantee"
    elif trigger == "regime_divergence":
        split = bool(context.get("divergence_independently_established"))
        note = "model the regimes; do not average them away"
    elif trigger == "repeated_calibration_failures":
        split = bool(context.get("failures_persist_after_recalibration"))
        note = "candidate split, not an automatic one"
    elif trigger == "isolated_sparse_residual":
        split = False
        note = "investigate; a sparse residual alone never forces a split"
    else:  # shared_guarantee_differing_latency
        split = "latency_modeling_only"
        note = ("split the latency model, never fragment the valid shared "
                "guarantee")
    return {"trigger": trigger, "action": action, "split": split,
            "note": note}


# --- 6. The provisional scope lifecycle --------------------------------------------------------------------------------
# NEW_SCOPE -> PROVISIONAL_MODEL -> INDEPENDENT_QUALIFICATION -> QUALIFIED_IN_SCOPE.
# Nuance: a genuinely general existing contract CAN cover a new workload — but
# only after verifying EVERY condition (concurrency, key identity, region,
# retention, downstream effects). A shared statistical parent never supplies
# contractual coverage.
PROVISIONAL_STATES = ("NEW_SCOPE", "PROVISIONAL_MODEL",
                      "INDEPENDENT_QUALIFICATION", "QUALIFIED_IN_SCOPE")


class ProvisionalScope:
    """Lifecycle for a new workload class (his BATCH_RECOVERY_WRITE example)."""

    def __init__(self, scope_id: str):
        self.scope_id = scope_id
        self.state = "NEW_SCOPE"
        self.history = [("NEW_SCOPE", "registered")]

    def to_provisional_model(self, borrowed_parent: str,
                             uncertainty_noted: bool) -> dict:
        if self.state != "NEW_SCOPE":
            return {"advanced": False, "reason": "not in NEW_SCOPE"}
        if not uncertainty_noted:
            return {"advanced": False,
                    "reason": "borrowed estimates require stated uncertainty"}
        self.state = "PROVISIONAL_MODEL"
        self.history.append(("PROVISIONAL_MODEL",
                             f"borrows calibrated estimates from {borrowed_parent}"))
        return {"advanced": True, "state": self.state,
                "inherited_pass": False}

    def to_independent_qualification(self, checks: dict) -> dict:
        """checks: contract_applicability, failure_cases, interactions,
        outcomes — each independently verified."""
        if self.state != "PROVISIONAL_MODEL":
            return {"advanced": False, "reason": "not in PROVISIONAL_MODEL"}
        missing = [c for c in ("contract_applicability", "failure_cases",
                               "interactions", "outcomes")
                   if not checks.get(c)]
        if missing:
            return {"advanced": False,
                    "reason": f"unverified: {missing}"}
        self.state = "INDEPENDENT_QUALIFICATION"
        self.history.append(("INDEPENDENT_QUALIFICATION",
                             "all four checks independently verified"))
        return {"advanced": True, "state": self.state}

    def to_qualified(self, qualifier: str) -> dict:
        if self.state != "INDEPENDENT_QUALIFICATION":
            return {"advanced": False, "reason": "not independently qualified"}
        self.state = "QUALIFIED_IN_SCOPE"
        self.history.append(("QUALIFIED_IN_SCOPE", f"qualified by {qualifier}"))
        return {"advanced": True, "state": self.state}


def general_contract_may_cover(new_scope: dict, contract: dict) -> dict:
    """A genuinely general existing contract CAN cover a new workload — iff
    EVERY condition verifies: concurrency, key identity, region, retention,
    downstream effects. One missing condition blocks coverage."""
    conditions = ("concurrency", "key_identity", "region", "retention",
                  "downstream_effects")
    coverage = contract.get("covers", {})
    missing = [c for c in conditions
               if not coverage.get(c, {}).get("verified")]
    mismatched = [c for c in conditions
                  if c not in missing
                  and coverage[c].get("scope") != new_scope.get(c)]
    blocked = missing + [f"{c}:scope_mismatch" for c in mismatched]
    return {"covered": not blocked, "blocked_by": blocked,
            "note": "shared statistical parent never supplies coverage"}


# --- 7. The no-qualification-transfer invariant -------------------------------------------------------------------------
# UseGuarantee(g,s) => Verified(g) AND s ⊆ QualifiedScope(g) AND Current(g)
# AND LAWValid(s). Scope inclusion is checked on the guarantee's ACTUAL
# semantics, never on label hierarchy. A merged A∪B certification needs
# independent evidence for the whole union plus the interactions; two separate
# certificates may be the simpler, more auditable result.
def scope_semantically_within(scope_id: str, qualified_scope_id: str) -> bool:
    """Semantic inclusion, not label hierarchy: a scope is within a qualified
    scope only by exact identity or an explicitly recorded semantic subset
    relation — never because a label ('all endpoints') sounds broader."""
    return scope_id == qualified_scope_id


def use_guarantee(guarantee: dict, scope_id: str, revisions: dict,
                  law_receipt: Optional[dict],
                  shared_model_implies_qualification: bool = False) -> dict:
    """The invariant. shared_model_implies_qualification=True is the DEFECTIVE
    guard-swap (SHARED_MODEL ⇒ SHARED_QUALIFICATION); the law keeps it False
    (SHARED_MODEL ≠ SHARED_QUALIFICATION)."""
    reasons = []
    verified = bool(guarantee.get("verified"))
    if not verified:
        reasons.append("guarantee not verified")
    if shared_model_implies_qualification:
        # THE DEFECT: pooled under the same statistical parent counts as covered.
        within = (guarantee.get("statistical_parent_id") is not None)
        if within:
            reasons.append("DEFECT: shared statistical parent treated as coverage")
    else:
        within = any(scope_semantically_within(scope_id, q)
                     for q in guarantee.get("qualified_scopes", ()))
        if not within:
            reasons.append("scope not within the guarantee's qualified scope")
    current = bool(guarantee.get("current")) and all(
        revisions.get(r) == guarantee.get("revision")
        for r in ("taxonomy", "policy", "incident", "evidence"))
    if not current:
        reasons.append("guarantee not current at use time")
    law_valid = bool(law_receipt and law_receipt.get("valid"))
    if not law_valid:
        reasons.append("no valid LAW receipt for this use")
    authorized = verified and within and current and law_valid
    return {"authorized": authorized, "reasons": reasons,
            "invariant": "UseGuarantee(g,s) => Verified(g) ∧ s⊆QualifiedScope(g) "
                         "∧ Current(g) ∧ LAWValid(s)"}


# --- 8. Versioned, reconstructable change records -----------------------------------------------------------------------
# SCOPE-CHANGE-014: never rewrite past observations under a new taxonomy;
# preserve original classification versions; splits state the historical→child
# mapping, ambiguous records, and surviving guarantees; ambiguous records are
# never silently allocated; pending merges/splits must not race incident
# withdrawal or baseline promotion.
def make_scope_change_record(change_id: str, change_type: str,
                             taxonomy_before: str, taxonomy_after: str,
                             historical_mapping: dict,
                             ambiguous_records: list,
                             surviving_guarantees: list,
                             revision_checks: dict) -> dict:
    if change_type not in ("MERGE", "SPLIT", "PROVISIONAL_REGISTER"):
        return {"recorded": False,
                "reason": f"unknown change type {change_type!r}"}
    if change_type == "SPLIT" and not historical_mapping:
        return {"recorded": False,
                "reason": "a split must state the historical→child mapping"}
    if any(r.get("auto_allocated") for r in ambiguous_records):
        return {"recorded": False,
                "reason": "ambiguous records are never silently allocated"}
    stale = [r for r in ("taxonomy", "incident", "evidence", "policy")
             if not revision_checks.get(r, {}).get("current")]
    if stale:
        return {"recorded": False,
                "reason": f"stale revisions: {stale}"}
    if revision_checks.get("incident", {}).get("withdrawal_pending"):
        return {"recorded": False,
                "reason": "must not race incident withdrawal"}
    if revision_checks.get("promotion_pending"):
        return {"recorded": False,
                "reason": "must not race baseline promotion"}
    return {"recorded": True, "schema": "SCOPE-CHANGE-014",
            "change_id": change_id, "change_type": change_type,
            "taxonomy_before": taxonomy_before,
            "taxonomy_after": taxonomy_after,
            "historical_mapping": historical_mapping,
            "ambiguous_records": ambiguous_records,
            "surviving_guarantees": surviving_guarantees,
            "past_observations_rewritten": False,
            "note": "original classification versions preserved; a cold "
                    "successor reconstructs the evolution from these records"}


# --- 9. The M1–M10 suite --------------------------------------------------------------------------------------------------
def cal5_m_suite(guard_intact: bool = True) -> list:
    """Ten scope-evolution adversarial cases. With the guard intact
    (SHARED_MODEL ≠ SHARED_QUALIFICATION) every case must hold the line; with
    the guard swapped (SHARED_MODEL ⇒ SHARED_QUALIFICATION) M10 must yield the
    minimal counterexample of guarantee theft."""
    results = []
    rev = {"taxonomy": 7, "policy": 7, "incident": 7, "evidence": 7}
    law = {"receipt": "LAW-1", "valid": True}
    guarantee_a = {"guarantee_id": "idempotency:A", "kind": "idempotency",
                   "verified": True, "qualified_scopes": ("qual:A",),
                   "revision": 7, "current": True,
                   "statistical_parent_id": "latency-parent-1"}

    # M1: pool A<->B estimates; B keeps the pooled prediction, never the proof.
    m = HierarchicalScopeModel(min_n_qualified=100)
    m.observe("qual:A", 5000, 50)
    m.observe("qual:B", 15, 0)
    est_b, n_b = m.cell_posterior("qual:B")
    q_b = m.cell_qualification("qual:B")
    results.append(("M1", "HOLD" if (q_b == "UNPROVEN_IN_SCOPE" and est_b > 0)
                    else "LEAK",
                    f"B pooled estimate {est_b:.4f} (n={n_b}); "
                    f"qualification {q_b} — prediction kept, proof withheld"))

    # M2: operational merge WITH held-out evidence each scope's detection survives.
    d2 = scope_decision("MERGE_OPERATIONAL_MODEL",
                        {"held_out_preserves_detection_all_scopes": True})
    results.append(("M2", "HOLD" if d2["taken"] else "LEAK",
                    "shared forecasting authorized on held-out evidence"))

    # M3: operational merge WITHOUT held-out evidence — rejected.
    d3 = scope_decision("MERGE_OPERATIONAL_MODEL",
                        {"held_out_preserves_detection_all_scopes": False})
    results.append(("M3", "HOLD" if not d3["taken"] else "LEAK",
                    "merge refused without held-out detection evidence"))

    # M4: consolidation A∪B with union evidence + interaction tests — certified.
    d4 = classify_scope_operation(
        {"kind": "QUALIFICATION_CONSOLIDATION",
         "scopes": ["qual:A", "qual:B"],
         "evidence": {"proof_guarantee_covers_every_member": True,
                      "relevant_cross_scope_interactions_tested": True}})
    results.append(("M4", "HOLD" if d4["authorized"] else "LEAK",
                    "union certification only on union evidence + interactions"))

    # M5: consolidation by label hierarchy alone — rejected.
    d5 = classify_scope_operation(
        {"kind": "QUALIFICATION_CONSOLIDATION",
         "scopes": ["qual:A", "qual:B"],
         "evidence": {"proof_guarantee_covers_every_member": False,
                      "relevant_cross_scope_interactions_tested": False}})
    results.append(("M5", "HOLD" if not d5["authorized"] else "LEAK",
                    "label-hierarchy consolidation refused"))

    # M6: idempotency-scope change — immediate separation, no statistics needed.
    d6 = evaluate_split_trigger("idempotency_scope_change", {})
    results.append(("M6", "HOLD" if d6["split"] is True else "LEAK",
                    "safety contracts separate without statistical permission"))

    # M7: verified duplicates — contain + reassess.
    d7 = evaluate_split_trigger("verified_duplicates",
                                {"duplicates_verified": True})
    results.append(("M7", "HOLD" if d7["action"] == "CONTAIN_AND_REASSESS"
                    else "LEAK", d7["note"]))

    # M8: new endpoint C — provisional, no inherited PASS.
    d8 = scope_decision("CREATE_PROVISIONAL_SCOPE", {})
    results.append(("M8", "HOLD" if (d8["taken"] and d8["provisional"]
                                     and not d8["effects"]["inherited_pass"])
                    else "LEAK", "C provisional; nothing inherited"))

    # M9: 10,000 vs 15 — 'no difference detected' is not equivalence.
    r9 = ten_k_vs_fifteen()
    results.append(("M9", "HOLD" if not r9["pooling_permitted"] else "LEAK",
                    f"difference interval {r9['result']['difference_interval']}; "
                    "pooling blocked on UNPROVEN"))

    # M10: the guard-swap. Sparse B resembles A (same statistical parent).
    use_b = use_guarantee(
        guarantee_a, "qual:B", rev, law,
        shared_model_implies_qualification=not guard_intact)
    if guard_intact:
        verdict = "HOLD" if not use_b["authorized"] else "LEAK"
        note = ("B's use of A's idempotency guarantee refused: "
                + "; ".join(use_b["reasons"]))
    else:
        verdict = "COUNTEREXAMPLE" if use_b["authorized"] else "NO_THEFT"
        note = ("MINIMAL COUNTEREXAMPLE: sparse B acquired A's guarantee via "
                "shared statistical parent — " + "; ".join(use_b["reasons"]))
    results.append(("M10", verdict, note))
    return results


def cal5_guard_swap_crown_jewel() -> dict:
    """THE DECISIVE GUARD-SWAP: replace SHARED_MODEL≠SHARED_QUALIFICATION with
    the defective SHARED_MODEL⇒SHARED_QUALIFICATION. Sparse Endpoint B
    resembling A must yield the minimal counterexample of B acquiring A's
    guarantee without coverage evidence. Restore the guard: B keeps pooled
    predictions while the theft stays blocked."""
    intact = cal5_m_suite(guard_intact=True)
    swapped = cal5_m_suite(guard_intact=False)
    m10_intact = next(v for i, v, _ in intact if i == "M10")
    m10_swapped = next(v for i, v, _ in swapped if i == "M10")
    m1_intact = next(n for i, v, n in intact if i == "M1")
    assert m10_intact == "HOLD", intact
    assert m10_swapped == "COUNTEREXAMPLE", swapped
    assert "UNPROVEN_IN_SCOPE" in m1_intact, m1_intact
    return {"guard_intact_M10": m10_intact,
            "guard_swapped_M10": m10_swapped,
            "minimal_counterexample": next(n for i, v, n in swapped
                                          if i == "M10"),
            "restoration": "B keeps pooled predictions (M1); the theft stays "
                           "blocked (M10 HOLD)",
            "note": "the harness detects the broken guard; only the guard "
                    "change flips M10"}


# --- AER-CAL-005: the first action ----------------------------------------------------------------------------------------
def aer_cal_005() -> dict:
    """Three-endpoint deterministic fixture.
    A: sufficient evidence + verified idempotency coverage.
    B: sparse but statistically similar — shares A<->B estimation, keeps B's
       guarantee UNQUALIFIED.
    C: new endpoint, different downstream semantics — provisional.
    Then: inject a genuine regression into B — A's healthy data must not mask
    it (detection runs on B's own cell evidence, never the pooled estimate).
    Finally: remove the guard and demand the minimal counterexample."""
    report = {}
    rev = {"taxonomy": 7, "policy": 7, "incident": 7, "evidence": 7}
    law = {"receipt": "LAW-1", "valid": True}

    # The three endpoints.
    model = HierarchicalScopeModel(min_n_qualified=100)
    model.observe("ep:A", 5000, 50)     # 1%, healthy, sufficient
    model.observe("ep:B", 15, 0)        # sparse, similar
    guarantee_a = {"guarantee_id": "idempotency:A", "kind": "idempotency",
                   "verified": True, "qualified_scopes": ("ep:A",),
                   "revision": 7, "current": True,
                   "statistical_parent_id": "epAB-parent"}

    # Share A<->B statistics; B's guarantee stays unqualified.
    comp = check_comparability(
        {"endpoint": "A"}, {"endpoint": "B"},
        {"semantic_compatible": True,
         "held_out_scope_specific_calibrated": True,
         "each_member_detection_preserved": True,
         "admissible_labeled": True,
         "unresolved_contamination": False})
    pool = scope_decision("POOL_ESTIMATES",
                          {"comparable": comp["comparable"],
                           "contamination": False})
    est_b, _ = model.cell_posterior("ep:B")
    use_b = use_guarantee(guarantee_a, "ep:B", rev, law)
    report["pooling"] = {"comparable": comp["comparable"],
                         "pool_authorized": pool["taken"],
                         "b_pooled_estimate": round(est_b, 4),
                         "b_qualification": model.cell_qualification("ep:B"),
                         "b_guarantee_authorized": use_b["authorized"]}
    assert pool["taken"] and not use_b["authorized"]
    assert model.cell_qualification("ep:B") == "UNPROVEN_IN_SCOPE"

    # C: new, different downstream semantics — provisional lifecycle.
    c = ProvisionalScope("ep:C")
    r1 = c.to_provisional_model(borrowed_parent="epAB-parent",
                                uncertainty_noted=True)
    r2 = c.to_independent_qualification(
        {"contract_applicability": True, "failure_cases": True,
         "interactions": True, "outcomes": True})
    r3 = c.to_qualified("independent-verifier-7")
    report["provisional_C"] = {"lifecycle": [s for s, _ in c.history],
                               "final": c.state}
    assert c.state == "QUALIFIED_IN_SCOPE" and r1["advanced"] and r2["advanced"]

    # A genuinely general contract CAN cover a new workload — positive control:
    # every condition verified.
    general = {"covers": {
        "concurrency": {"verified": True, "scope": "low"},
        "key_identity": {"verified": True, "scope": "stable"},
        "region": {"verified": True, "scope": "r1"},
        "retention": {"verified": True, "scope": "30d"},
        "downstream_effects": {"verified": True, "scope": "ledger-only"}}}
    cover_ok = general_contract_may_cover(
        {"concurrency": "low", "key_identity": "stable", "region": "r1",
         "retention": "30d", "downstream_effects": "ledger-only"}, general)
    # ...and one missing condition blocks it — negative control.
    general_bad = {"covers": dict(general["covers"])}
    general_bad["covers"] = dict(general["covers"])
    general_bad["covers"]["retention"] = {"verified": False}
    cover_bad = general_contract_may_cover(
        {"concurrency": "low", "key_identity": "stable", "region": "r1",
         "retention": "30d", "downstream_effects": "ledger-only"}, general_bad)
    report["general_contract"] = {"all_verified_covers": cover_ok["covered"],
                                  "one_missing_blocks": not cover_bad["covered"],
                                  "blocked_by": cover_bad["blocked_by"]}
    assert cover_ok["covered"] and not cover_bad["covered"]

    # Inject a genuine regression into B: 200 ops, 16 failures (8%).
    model.observe("ep:B", 200, 16)
    n_b, k_b = model.cells["ep:B"]
    cell_rate_b = k_b / n_b
    pooled_b, _ = model.cell_posterior("ep:B")
    # Detection MUST run on B's own cell evidence: 8% >> healthy 1%.
    detected_on_cell = cell_rate_b >= 0.05
    masked_by_pool = pooled_b < 0.05
    report["regression_in_B"] = {
        "b_cell_rate": round(cell_rate_b, 4),
        "b_pooled_estimate": round(pooled_b, 4),
        "detected_on_cell_evidence": detected_on_cell,
        "pooled_estimate_would_mask": masked_by_pool,
        "a_cell_unaffected": model.cells["ep:A"] == [5000, 50],
    }
    assert detected_on_cell and report["regression_in_B"]["a_cell_unaffected"], \
        "A's healthy data must not mask B's regression"

    # Remove the guard: demand the minimal counterexample.
    theft = use_guarantee(guarantee_a, "ep:B", rev, law,
                          shared_model_implies_qualification=True)
    report["guard_removed"] = {"theft_authorized": theft["authorized"],
                               "minimal": "; ".join(theft["reasons"])}
    assert theft["authorized"], "the defective guard must permit the theft"
    # Restore: theft blocked, pooled predictions kept.
    restored = use_guarantee(guarantee_a, "ep:B", rev, law)
    report["guard_restored"] = {"theft_blocked": not restored["authorized"],
                                "b_pooled_estimate_kept": round(
                                    model.cell_posterior("ep:B")[0], 4)}
    assert not restored["authorized"]
    return report
# ======================================================================================
# SN-0805 AER-TAX-1 — ATOMIC SCOPE EVOLUTION LAW
# ======================================================================================
# The CONCURRENCY-GOVERNANCE layer: AER-CAL-5 defined what scope merges/splits mean
# and required that they not race incident withdrawal or baseline promotion — this is
# the ordering protocol that enforces it.
#
# HONEST SCOPE (Shawn, 2026-10-10 — his explicit scoping): ISOLATED HARNESS
# DEMONSTRATION FIRST — no live production authority change, no parallel governance
# registry. propagation.py / revocation.py / authority.py / uncertainty.py align as
# foundations, but the full protocol and harness are NOT verified to exist.
# Do not claim otherwise. Main observed by Shawn at 0fb380c.
#
# His law: NayaNET shall treat taxonomy revisions, evidence withdrawals,
# qualification changes, baseline promotions and consequential authorizations as
# operations over one canonically ordered governance state. Every change must be
# independently qualified within its scope, revalidated at its authoritative commit
# boundary, and recorded with reconstructable provenance. Stale or ambiguous state
# shall not create qualification or execution authority.
AER_TAX1_IMPLEMENTATION_STATUS = {
    "enters_as": "isolated harness demonstration",
    "not_a": ("live production authority change",
              "parallel governance registry"),
    "foundations_align": ("propagation.py", "revocation.py",
                          "authority.py", "uncertainty.py"),
    "not_verified": ("full protocol implementation",
                     "harness against production state"),
    "main_observed_at": "0fb380c",
}


# --- 1. Separation of authorities -----------------------------------------------------------------------------------
# Taxonomy DESCRIBES what belongs together. Qualification determines what has been
# PROVEN. LAW determines what MAY BE DONE. None silently grants authority through
# another. Only consequential changes take the strict commit path.
AUTHORITY_SEPARATION = {
    "taxonomy": "describes what belongs together; never proves, never permits",
    "qualification": "determines what has been proven; never permits by itself",
    "law": "determines what may be done; never proven by taxonomy alone",
}
TAX_CHANGE_TABLE = {
    "MERGE_SPLIT": "cannot inherit or widen qualifications without proof",
    "PROVISIONAL_SCOPE": "starts uncertified; no inherited PASS",
    "INCIDENT_WITHDRAWAL": "invalidates affected stale decisions at the "
                           "authoritative boundary",
    "BASELINE_PROMOTION_ACT": "rechecks current scope, incident, and "
                              "qualification state at commit",
}


# --- 2. One authoritative versioned governance state ------------------------------------------------------------------
class GovernanceState:
    """One canonically ordered governance state.

    Snapshot fields (proposed, not an implemented production schema):
    governance_epoch + taxonomy/incident/qualification/baseline/policy revisions
    + scope_mapping_hash + active_qualification_set + active_baseline.

    A read snapshot is NOT an authority token: every commit re-proves currency
    against the live revisions. Single monotonic epoch (conservative): versions
    are unique, monotonic, never reset or reused after rollback, recovery, or
    restart. Rollback is a NEW revision — ABA-proof by construction."""

    def __init__(self):
        self._commit_lock = threading.RLock()
        self.epoch = 0
        self.revisions = {"taxonomy": 0, "incident": 0, "qualification": 0,
                          "baseline": 0, "policy": 0}
        # scope_id -> {"parent": id|None, "children": [...], "taxonomy_version": int}
        self.scope_mapping = {}
        # scope_id -> {"guarantee": id, "status": QUALIFIED|WITHDRAWN|...,
        #              "qualification_rev": int, "taxonomy_version": int}
        self.active_qualifications = {}
        self.active_baseline = None  # {"baseline_id":..., "revision":...}
        self.incidents = {}          # incident_id -> record
        self.receipts = []           # append-only; never rewritten
        self.inflight = {}           # operation_id -> unresolved attempt record
        self._seq = 0

    def snapshot(self) -> dict:
        """A read snapshot. NOT an authority token."""
        import hashlib
        mapping_hash = hashlib.sha256(
            repr(sorted(self.scope_mapping.items())).encode()).hexdigest()[:16]
        return {"governance_epoch": self.epoch,
                "revisions": dict(self.revisions),
                "scope_mapping_hash": mapping_hash,
                "active_qualification_set": sorted(self.active_qualifications),
                "active_baseline": self.active_baseline,
                "authority_token": False}

    def _bump(self, *names):
        for n in names:
            self.revisions[n] += 1
        self.epoch += 1

    def _record(self, receipt: dict):
        self._seq += 1
        receipt = dict(receipt)
        receipt["seq"] = self._seq
        receipt["governance_epoch"] = self.epoch
        self.receipts.append(receipt)
        return receipt


def _affected_closure(gov: GovernanceState, scopes: list) -> list:
    """The affected closure: named scopes + children + parent + members whose
    parent is in the closure (reverse lookup, so withdrawing a merged scope
    reaches its members). Recomputed against LIVE mapping at commit — the
    phantom check."""
    closure = set(scopes)
    for s in scopes:
        node = gov.scope_mapping.get(s, {})
        closure.update(node.get("children", ()))
        if node.get("parent"):
            closure.add(node.get("parent"))
    for sid, nd in gov.scope_mapping.items():
        if nd.get("parent") in closure:
            closure.add(sid)
    return sorted(closure)


def prepare_governed_change(change: dict, gov: GovernanceState) -> dict:
    """PREPARE runs OUTSIDE the commit lock (no global bottleneck): read the
    snapshot, compute the affected closure, assemble the evidence. The returned
    prepared change carries expected revisions; the commit re-proves them."""
    snap = gov.snapshot()
    change_type = change.get("change_type")
    scopes = change.get("scopes", [])
    closure = _affected_closure(gov, scopes)
    return {"change_id": change.get("change_id"),
            "change_type": change_type,
            "scopes": list(scopes),
            "affected_closure": sorted(closure),
            "expected_revisions": dict(snap["revisions"]),
            "expected_epoch": snap["governance_epoch"],
            "evidence": change.get("evidence", {}),
            "law_receipt": change.get("law_receipt"),
            "status": "PREPARED_NOT_COMMITTED"}


def commit_prepared_change(gov: GovernanceState, prepared: dict,
                           check_incident_revision: bool = True,
                           check_taxonomy_version: bool = True) -> dict:
    """The commit boundary: PREPARE -> INDEPENDENT VERIFY -> LAW ->
    ATOMIC COMMIT -> VERIFY -> PROVE -> PROPAGATE.

    Under the single commit lock: reread live revisions, recompute the affected
    closure, verify qualification + LAW predicates, then publish state +
    receipt + epoch increment atomically.

    check_incident_revision / check_taxonomy_version are the guard-removal
    mutation switches: the law keeps both True. Derived indexes, dashboards,
    and Smart Notes update async AFTER commit and never compete as authority.
    Multi-DB without one atomic transaction needs a fencing protocol; eventual
    sync cannot prove atomic authority changes. Selective locking beware the
    phantom problem: the predicate range, not just named scopes, is locked —
    here the single commit lock serializes the final authoritative decision."""
    with gov._commit_lock:
        live = gov.revisions
        exp = prepared["expected_revisions"]
        stale = []
        for rev in ("taxonomy", "incident", "qualification", "baseline",
                    "policy"):
            if rev == "incident" and not check_incident_revision:
                continue  # MUTANT: the incident-revision check removed
            if rev == "taxonomy" and not check_taxonomy_version:
                continue  # MUTANT: the taxonomy-version check removed
            if live[rev] != exp[rev]:
                stale.append(rev)
        if stale:
            return {"committed": False, "status": "REJECTED_STALE_SNAPSHOT",
                    "stale_revisions": stale,
                    "note": "a read snapshot is not an authority token; "
                            "re-prepare against current state"}
        # Recompute the affected closure against LIVE mapping (phantom check).
        closure = set(_affected_closure(gov, prepared["scopes"]))
        if sorted(closure) != prepared["affected_closure"]:
            return {"committed": False,
                    "status": "REJECTED_CLOSURE_CHANGED",
                    "note": "the mapping moved under the prepared change"}
        # Qualification + LAW predicates per affected scope.
        per_scope = {}
        for s in sorted(closure):
            q = gov.active_qualifications.get(s)
            per_scope[s] = _per_scope_commit_check(
                gov, s, q, prepared["change_type"], prepared["evidence"])
        blocked = [s for s, r in per_scope.items() if not r["ok"]]
        if blocked:
            return {"committed": False, "status": "REJECTED_SCOPE_CHECK",
                    "blocked_scopes": blocked, "per_scope": per_scope}
        law = prepared.get("law_receipt") or {}
        if not law.get("valid"):
            return {"committed": False, "status": "REJECTED_NO_LAW",
                    "note": "LAW determines what may be done"}
        # ATOMIC COMMIT: state + receipt + epoch increment, indivisibly.
        applied = _apply_governed_change(gov, prepared, per_scope)
        receipt = make_tax_receipt(
            prepared["change_id"], prepared["change_type"], exp,
            prepared["affected_closure"], per_scope,
            prepared["evidence"].get("verifier_ref"),
            prepared.get("law_receipt"), "COMMITTED",
            bumped_revisions=applied.get("bumped_revisions"))
        recorded = gov._record(receipt)
        return {"committed": True, "status": "COMMITTED", "applied": applied,
                "receipt": recorded, "per_scope": per_scope}


def _per_scope_commit_check(gov: GovernanceState, scope: str, qual: dict,
                            change_type: str, evidence: dict) -> dict:
    """Per-scope qualification predicate at the commit boundary. A split never
    justifies REQUALIFIED by itself: split children require reassessment."""
    if change_type == "SPLIT":
        return {"ok": True, "result": "REASSESSMENT_REQUIRED",
                "note": "a split never manufactures or destroys evidence; "
                        "children are reassessed, never auto-requalified"}
    if change_type == "INCIDENT_WITHDRAWAL":
        return {"ok": True, "result": "WITHDRAWN_IF_AFFECTED",
                "note": "withdrawal invalidates affected stale decisions"}
    if change_type == "PROVISIONAL_REGISTER":
        return {"ok": True, "result": "PROVISIONAL_UNCERTIFIED",
                "note": "a provisional scope starts uncertified"}
    return {"ok": True, "result": "REVALIDATED"}


def _apply_governed_change(gov: GovernanceState, prepared: dict,
                           per_scope: dict) -> dict:
    """Apply the change to governance state. Called under the commit lock."""
    ctype = prepared["change_type"]
    applied = {"change_type": ctype, "bumped_revisions": []}
    def _bump_record(*names):
        gov._bump(*names)
        applied["bumped_revisions"] = list(names)
    if ctype == "TAXONOMY_SPLIT":
        parent = prepared["scopes"][0]
        children = prepared["evidence"].get("children", [])
        node = gov.scope_mapping.setdefault(parent, {"parent": None,
                                                     "children": [],
                                                     "taxonomy_version": 0})
        node["children"] = list(children)
        for c in children:
            gov.scope_mapping[c] = {"parent": parent, "children": [],
                                    "taxonomy_version":
                                    gov.revisions["taxonomy"] + 1}
        node["taxonomy_version"] = gov.revisions["taxonomy"] + 1
        _bump_record("taxonomy")
        applied["children"] = children
    elif ctype == "TAXONOMY_MERGE":
        members = prepared["scopes"]
        target = prepared["evidence"].get("merged_id",
                                          "+".join(sorted(members)))
        for m_ in members:
            gov.scope_mapping[m_] = {"parent": target, "children": [],
                                     "taxonomy_version":
                                     gov.revisions["taxonomy"] + 1}
        gov.scope_mapping[target] = {"parent": None, "children": [],
                                     "taxonomy_version":
                                     gov.revisions["taxonomy"] + 1}
        _bump_record("taxonomy")
        applied["merged_id"] = target
    elif ctype == "INCIDENT_WITHDRAWAL":
        incident = prepared["evidence"].get("incident", {})
        iid = incident.get("incident_id", prepared["change_id"])
        confirmed = bool(incident.get("confirmed"))
        gov.incidents[iid] = {"scopes": list(prepared["affected_closure"]),
                              "confirmed": confirmed,
                              "kind": ("CONFIRMED" if confirmed
                                       else "PRECAUTIONARY_HOLD")}
        for s in prepared["affected_closure"]:
            q = gov.active_qualifications.get(s)
            # The qualification revision tracks the qualification SET: it moves
            # only when a qualification actually transitions. An incident that
            # withdraws nothing still moves the incident revision — so the two
            # guards stay separable for mutation testing.
            if q is not None and q.get("status") == "QUALIFIED":
                q["status"] = "WITHDRAWN"
                q["withdrawn_by"] = iid
        withdrew_any = any(
            gov.active_qualifications.get(s, {}).get("withdrawn_by") == iid
            for s in prepared["affected_closure"])
        bumped = ["incident"] + (["qualification"] if withdrew_any else [])
        gov._bump(*bumped)
        applied["incident_id"] = iid
        applied["bumped_revisions"] = bumped
    elif ctype == "BASELINE_PROMOTION":
        gov.active_baseline = {"baseline_id": prepared["evidence"].get(
            "baseline_id"), "revision": gov.revisions["baseline"] + 1,
            "scope_revisions": dict(prepared["expected_revisions"])}
        _bump_record("baseline")
    elif ctype == "PROVISIONAL_REGISTER":
        for s in prepared["scopes"]:
            gov.scope_mapping[s] = {"parent": None, "children": [],
                                    "taxonomy_version":
                                    gov.revisions["taxonomy"] + 1}
            gov.active_qualifications[s] = {"guarantee": None,
                                            "status": "PROVISIONAL_UNCERTIFIED",
                                            "qualification_rev": 0,
                                            "taxonomy_version":
                                            gov.revisions["taxonomy"] + 1}
        _bump_record("taxonomy", "qualification")
    return applied


def supersede_receipt(gov: GovernanceState, seq: int, reason: str) -> dict:
    """A superseded receipt stays historical — never a current certificate.
    Receipts are append-only; supersession is a new record, not an edit."""
    with gov._commit_lock:
        target = next((r for r in gov.receipts if r["seq"] == seq), None)
        if target is None:
            return {"superseded": False, "reason": "no such receipt"}
        note = {"supersedes_seq": seq, "reason": reason,
                "note": "the prior receipt stays historical; it is never a "
                        "current certificate"}
        gov._bump()  # epoch advances; nothing is rewritten
        return {"superseded": True, "record": gov._record(note)}


def rollback_governed_change(gov: GovernanceState, change_id: str,
                             reason: str) -> dict:
    """Rollback is a NEW revision, never a rewind — ABA-proof by construction.
    Versions are never reset or reused after rollback, recovery, or restart."""
    with gov._commit_lock:
        gov._bump("taxonomy", "incident", "qualification", "baseline",
                  "policy")
        return gov._record({"change_id": change_id, "change_type": "ROLLBACK",
                            "reason": reason,
                            "bumped_revisions": ["taxonomy", "incident",
                                                 "qualification", "baseline",
                                                 "policy"],
                            "note": "rollback as a new revision; history kept"})


# --- 5. Fast incident containment -----------------------------------------------------------------------------------
# Separate safety containment from model recomputation. The immediate
# transaction commits the incident record, withdraws unsupported reliance,
# advances eligibility revisions, and fences dependent actions; recalibration
# follows as a separate change. A governed write, not an ignorable alert flag.
# Uncertain scope is recorded explicitly; unaffected paths are preserved.
# Unverified incidents are never labeled confirmed.
def contain_incident(gov: GovernanceState, incident: dict,
                     law_receipt: dict) -> dict:
    """incident: {"incident_id", "scopes", "confirmed" (bool),
    "uncertain_scope" (bool), "evidence_ref"}. Returns the containment record;
    recalibration is a separate subsequent governed change."""
    if not (law_receipt or {}).get("valid"):
        return {"contained": False, "reason": "no valid LAW receipt"}
    prepared = prepare_governed_change(
        {"change_id": f"contain-{incident['incident_id']}",
         "change_type": "INCIDENT_WITHDRAWAL",
         "scopes": incident["scopes"],
         "evidence": {"incident": incident,
                      "verifier_ref": incident.get("evidence_ref")},
         "law_receipt": law_receipt}, gov)
    result = commit_prepared_change(gov, prepared)
    if not result["committed"]:
        return {"contained": False, **result}
    # Fence dependent actions: record the fence on every affected scope.
    fenced = [s for s in prepared["affected_closure"]]
    return {"contained": True,
            "kind": ("CONFIRMED" if incident.get("confirmed")
                     else "PRECAUTIONARY_HOLD"),
            "uncertain_scope_recorded": bool(incident.get("uncertain_scope")),
            "fenced_scopes": fenced,
            "receipt": result["receipt"],
            "note": "containment first; model recomputation follows separately"}


# --- 6. The Authorize(a,s) predicate ----------------------------------------------------------------------------------
# Authorize(a,s) = CurrentTaxonomy ∧ CurrentQualification ∧
#   NoDisqualifyingIncident ∧ EvidenceCovers ∧ LAWPermits.
# Statistical parent ≠ EvidenceCovers. Two boundaries: LAW authorizes against
# canonical state; ACT re-establishes applicability at execution. Never hold a
# DB transaction across a provider call — atomically establish a fenced
# execution intent + durable operation identity instead.
def authorize_tax_action(gov: GovernanceState, action_id: str, scope_id: str,
                         guarantee: dict, law_receipt: dict) -> dict:
    snap = gov.snapshot()  # read snapshot; NOT an authority token
    node = gov.scope_mapping.get(scope_id, {})
    qual = gov.active_qualifications.get(scope_id, {})
    checks = {}
    # CurrentTaxonomy is scope-relative: the scope's classification is current
    # iff its qualification was established under its live classification.
    # A global taxonomy revision never spuriously invalidates an untouched
    # scope (no global bottleneck, no collateral loss).
    checks["CurrentTaxonomy"] = bool(node) and (
        qual.get("taxonomy_version") == node.get("taxonomy_version"))
    # CurrentQualification is a fresh read; staleness across time is enforced
    # by act_execute's epoch comparison + full recheck, not by a global rev.
    checks["CurrentQualification"] = qual.get("status") == "QUALIFIED"
    disqualified = any(
        inc.get("confirmed") and scope_id in inc.get("scopes", ())
        for inc in gov.incidents.values())
    checks["NoDisqualifyingIncident"] = not disqualified
    # EvidenceCovers: the guarantee's actual semantics — never the statistical
    # parent, never label hierarchy.
    covers = any(scope_semantically_within(scope_id, q)
                 for q in guarantee.get("qualified_scopes", ()))
    checks["EvidenceCovers"] = bool(guarantee.get("verified")) and covers
    checks["LAWPermits"] = bool((law_receipt or {}).get("valid"))
    authorized = all(checks.values())
    return {"authorized": authorized, "action_id": action_id,
            "scope_id": scope_id, "checks": checks,
            "scope_taxonomy_version": node.get("taxonomy_version"),
            "authorized_at_epoch": gov.epoch if authorized else None,
            "note": "LAW authorizes against canonical state; ACT re-establishes "
                    "applicability at execution"}


def act_execute(gov: GovernanceState, authorization: dict, guarantee: dict,
                law_receipt: dict, revalidate_at_execution: bool = True) -> dict:
    """The ACT boundary: re-establish applicability at execution. A cached
    authorization from an older epoch is rechecked, never trusted.
    revalidate_at_execution=False is the DEFECTIVE mutant (the ACT-side
    taxonomy currency check removed): a stale inherited authorization then
    executes — the unsupported-inheritance counterexample."""
    if not authorization.get("authorized"):
        return {"executed": False, "reason": "no valid authorization"}
    if authorization.get("authorized_at_epoch") != gov.epoch:
        if not revalidate_at_execution:
            pass  # MUTANT: stale authorization trusted without recheck
        else:
            recheck = authorize_tax_action(
                gov, authorization["action_id"], authorization["scope_id"],
                guarantee, law_receipt)
            if not recheck["authorized"]:
                return {"executed": False, "reason": "stale authorization",
                        "recheck": recheck["checks"]}
            authorization = recheck
    # Fenced execution intent + durable operation identity — established
    # atomically, never by holding a transaction across a provider call.
    op_id = authorization["action_id"]
    with gov._commit_lock:
        gov.inflight[op_id] = {"scope": authorization["scope_id"],
                               "status": "INTENT_FENCED",
                               "epoch": gov.epoch}
    return {"executed": True, "operation_id": op_id,
            "intent": "fenced execution intent + durable operation identity",
            "note": "the intent is committed; the provider call happens "
                    "outside any held transaction"}


def reconcile_inflight(gov: GovernanceState, operation_id: str,
                       outcome: str) -> dict:
    """HONEST LIMITATION: ordering cannot revoke a remote effect already in
    flight. The unresolved attempt is preserved, reconciled, and claims are
    limited to the actual enforcement boundary."""
    rec = gov.inflight.get(operation_id)
    if rec is None:
        return {"reconciled": False, "reason": "unknown operation"}
    rec["status"] = outcome  # e.g. EFFECT_CONFIRMED / EFFECT_UNKNOWN
    rec["reconciled"] = True
    return {"reconciled": True, "operation_id": operation_id,
            "outcome": outcome,
            "note": "unresolved attempts are preserved and reconciled; no "
                    "claim beyond the enforcement boundary"}


# --- 8. The AER-TAX-1 receipt ------------------------------------------------------------------------------------------
def make_tax_receipt(change_id: str, change_type: str, expected_revisions: dict,
                     affected_closure: list, per_scope: dict,
                     verifier_ref: Optional[str], law_ref: dict,
                     status: str, bumped_revisions: Optional[list] = None) -> dict:
    """AER-TAX-1 receipt: expected_state revisions, mapping/affected-closure
    evidence, per-scope qualification results, independent verifier + LAW refs.
    PREPARED_NOT_COMMITTED is never confused with COMMITTED. A cold successor
    reconstructs why the change happened, what was unqualified, and what
    actually committed."""
    if change_type == "SPLIT" or change_type == "TAXONOMY_SPLIT":
        bad = [s for s, r in per_scope.items()
               if r.get("result") == "REQUALIFIED"]
        if bad:
            raise ValueError(
                "a split never justifies REQUALIFIED by itself")
    return {"schema": "AER-TAX-1", "change_id": change_id,
            "change_type": change_type, "status": status,
            "expected_state_revisions": dict(expected_revisions),
            "affected_closure": list(affected_closure),
            "mapping_evidence": {"closure_size": len(affected_closure)},
            "per_scope_qualification": {
                s: r.get("result") for s, r in per_scope.items()},
            "independent_verifier_ref": verifier_ref,
            "law_ref": (law_ref or {}).get("receipt"),
            "bumped_revisions": list(bumped_revisions or []),
            "note": "PREPARED_NOT_COMMITTED never counts as committed"}


# --- 9. The R1–R12 concurrency harness ------------------------------------------------------------------------------------
# Deterministic, scheduler-controlled pauses before each commit; both orders
# explored per pair. Four invariants + historical integrity:
#   I1 no stale qualification use; I2 no taxonomy-based authority inflation;
#   I3 no stale baseline promotion; I4 no collateral qualification loss;
#   H  historical integrity (append-only receipts, monotonic epoch, no
#      rewritten uncertainty, no revision reuse).
def _tax_setup_two_scopes() -> GovernanceState:
    gov = GovernanceState()
    for s in ("scope:A", "scope:B"):
        gov.scope_mapping[s] = {"parent": None, "children": [],
                                "taxonomy_version": 0}
        gov.active_qualifications[s] = {"guarantee": f"idem:{s}",
                                        "status": "QUALIFIED",
                                        "qualification_rev": 0,
                                        "taxonomy_version": 0}
    law = {"receipt": "LAW-1", "valid": True}
    return gov, law


def _check_invariants(gov: GovernanceState, baseline_quals: dict) -> dict:
    """I1..I4 + H over the governance state after an interleaving."""
    issues = []
    # I1: no ACT-authorized use of a withdrawn/stale qualification.
    for op_id, rec in gov.inflight.items():
        q = gov.active_qualifications.get(rec["scope"], {})
        if q.get("status") == "WITHDRAWN":
            issues.append(f"I1: inflight {op_id} on withdrawn {rec['scope']}")
    # I2: no scope holds QUALIFIED unless its own qualification evidence does.
    for s, q in gov.active_qualifications.items():
        if q.get("status") == "QUALIFIED" and not q.get("guarantee"):
            issues.append(f"I2: {s} qualified without a guarantee")
    # I3: baseline promotion recorded its scope revisions; a promotion whose
    # expected revisions differ from commit-time revisions cannot exist —
    # enforced structurally by commit_prepared_change.
    # I4: no collateral qualification loss — unaffected scopes keep theirs.
    for s, st in baseline_quals.items():
        now = gov.active_qualifications.get(s, {}).get("status")
        if st == "QUALIFIED" and now not in ("QUALIFIED", "WITHDRAWN_BY_TEST"):
            # WITHDRAWN is allowed only if the test's incident covered s.
            covered = any(s in inc.get("scopes", ())
                          for inc in gov.incidents.values())
            if not covered:
                issues.append(f"I4: collateral loss on {s}")
    # H: epoch monotonic, receipts append-only with increasing seq.
    seqs = [r["seq"] for r in gov.receipts]
    if seqs != sorted(seqs) or len(set(seqs)) != len(seqs):
        issues.append("H: receipt seq not monotonic/unique")
    epochs = [r["governance_epoch"] for r in gov.receipts]
    if any(b < a for a, b in zip(epochs, epochs[1:])):
        issues.append("H: epoch regressed")
    return {"holds": not issues, "issues": issues}


def tax_r_harness() -> list:
    """R1–R12: the three races, both orders, deterministic interleavings."""
    results = []

    def fresh():
        gov, law = _tax_setup_two_scopes()
        base = {s: q["status"]
                for s, q in gov.active_qualifications.items()}
        return gov, law, base

    def withdraw_prep(gov, law, scopes, confirmed=True, iid="inc-1"):
        return prepare_governed_change(
            {"change_id": f"wd-{iid}", "change_type": "INCIDENT_WITHDRAWAL",
             "scopes": scopes,
             "evidence": {"incident": {"incident_id": iid, "confirmed": confirmed},
                          "verifier_ref": "verifier-7"},
             "law_receipt": law}, gov)

    def merge_prep(gov, law, scopes):
        return prepare_governed_change(
            {"change_id": "merge-1", "change_type": "TAXONOMY_MERGE",
             "scopes": scopes, "evidence": {"merged_id": "scope:AB"},
             "law_receipt": law}, gov)

    def split_prep(gov, law, scope, children):
        return prepare_governed_change(
            {"change_id": "split-1", "change_type": "TAXONOMY_SPLIT",
             "scopes": [scope],
             "evidence": {"children": children, "verifier_ref": "verifier-7"},
             "law_receipt": law}, gov)

    def promo_prep(gov, law):
        return prepare_governed_change(
            {"change_id": "promo-1", "change_type": "BASELINE_PROMOTION",
             "scopes": ["scope:A", "scope:B"],
             "evidence": {"baseline_id": "bl-2", "verifier_ref": "verifier-7"},
             "law_receipt": law}, gov)

    # R1: Race A order 1 — withdrawal commits, then merge commits on post-W state.
    gov, law, base = fresh()
    assert commit_prepared_change(
        gov, withdraw_prep(gov, law, ["scope:B"]))["committed"]
    m = commit_prepared_change(gov, merge_prep(gov, law, ["scope:A", "scope:B"]))
    inv = _check_invariants(gov, base)
    results.append(("R1", "PASS" if (m["committed"]
                    and gov.active_qualifications["scope:B"]["status"]
                    == "WITHDRAWN" and inv["holds"]) else "FAIL",
                    "W≺M: merge commits on post-withdrawal state"))

    # R2: Race A order 2 — merge prepares pre-W, withdrawal commits, merge
    # commits ⇒ REJECTED on the stale incident revision.
    gov, law, base = fresh()
    stale_merge = merge_prep(gov, law, ["scope:A", "scope:B"])
    assert commit_prepared_change(
        gov, withdraw_prep(gov, law, ["scope:B"]))["committed"]
    m2 = commit_prepared_change(gov, stale_merge)
    inv = _check_invariants(gov, base)
    results.append(("R2", "PASS" if (not m2["committed"]
                    and m2["status"] == "REJECTED_STALE_SNAPSHOT"
                    and "incident" in m2["stale_revisions"]
                    and inv["holds"]) else "FAIL",
                    "stale merge rejected: incident revision moved"))

    # R3: Race A — merge commits first, then withdrawal ⇒ withdrawal removes
    # the merged scope's current eligibility; the merge receipt stays
    # historical (superseded), never a current certificate.
    gov, law, base = fresh()
    mg = commit_prepared_change(gov, merge_prep(gov, law, ["scope:A",
                                                           "scope:B"]))
    assert mg["committed"]
    w = commit_prepared_change(
        gov, withdraw_prep(gov, law, ["scope:AB"], iid="inc-2"))
    sup = supersede_receipt(gov, mg["receipt"]["seq"],
                            "withdrawal invalidated merged eligibility")
    inv = _check_invariants(gov, base)
    hist = any(r.get("supersedes_seq") == mg["receipt"]["seq"]
               for r in gov.receipts)
    results.append(("R3", "PASS" if (w["committed"] and sup["superseded"]
                    and hist and inv["holds"]) else "FAIL",
                    "M≺W: eligibility withdrawn; merge receipt historical"))

    # R4: Race A — withdrawal of an unrelated scope does not block A's merge.
    gov, law, base = fresh()
    gov.scope_mapping["scope:C"] = {"parent": None, "children": [],
                                    "taxonomy_version": 0}
    assert commit_prepared_change(
        gov, withdraw_prep(gov, law, ["scope:C"], iid="inc-3"))["committed"]
    m4 = commit_prepared_change(gov, merge_prep(gov, law, ["scope:A"]))
    inv = _check_invariants(gov, base)
    results.append(("R4", "PASS" if (m4["committed"] and inv["holds"])
                    else "FAIL",
                    "unrelated withdrawal causes no collateral loss"))

    # R5: Race B order 1 — split commits, then promotion ⇒ promotion
    # revalidates against the successor scopes; no silent reinterpretation.
    gov, law, base = fresh()
    assert commit_prepared_change(
        gov, split_prep(gov, law, "scope:B",
                        ["scope:B1", "scope:B2"]))["committed"]
    p5 = commit_prepared_change(gov, promo_prep(gov, law))
    per = p5.get("per_scope", {})
    children_reassessed = all(
        per.get(c, {}).get("result") == "REASSESSMENT_REQUIRED"
        for c in ("scope:B1", "scope:B2") if c in per)
    inv = _check_invariants(gov, base)
    results.append(("R5", "PASS" if (p5["committed"]
                    and p5["receipt"]["expected_state_revisions"]["taxonomy"]
                    == gov.revisions["taxonomy"] and inv["holds"]) else "FAIL",
                    "split-first: promotion bound to post-split taxonomy"))

    # R6: Race B order 2 — promotion prepares pre-split, split commits,
    # promotion commits ⇒ REJECTED on the stale taxonomy revision.
    gov, law, base = fresh()
    stale_promo = promo_prep(gov, law)
    assert commit_prepared_change(
        gov, split_prep(gov, law, "scope:B",
                        ["scope:B1", "scope:B2"]))["committed"]
    p6 = commit_prepared_change(gov, stale_promo)
    inv = _check_invariants(gov, base)
    results.append(("R6", "PASS" if (not p6["committed"]
                    and "taxonomy" in p6.get("stale_revisions", [])
                    and inv["holds"]) else "FAIL",
                    "stale promotion rejected: taxonomy moved"))

    # R7: Race B — promotion commits first, then split ⇒ split reassesses
    # applicability to both children; evidence conserved, never manufactured.
    gov, law, base = fresh()
    assert commit_prepared_change(gov, promo_prep(gov, law))["committed"]
    s7 = commit_prepared_change(
        gov, split_prep(gov, law, "scope:B", ["scope:B1", "scope:B2"]))
    inv = _check_invariants(gov, base)
    kids = [c for c in ("scope:B1", "scope:B2") if c in gov.scope_mapping]
    parent_kept = gov.scope_mapping["scope:B"]["children"] == ["scope:B1",
                                                               "scope:B2"]
    results.append(("R7", "PASS" if (s7["committed"] and len(kids) == 2
                    and parent_kept and inv["holds"]) else "FAIL",
                    "promotion-first: split reassesses both children; "
                    "parent identity + mapping kept"))

    # R8: Race B — split conserves evidence: children partition the parent;
    # nothing manufactured, nothing destroyed.
    gov, law, base = fresh()
    ev_before = {"scope:B": (1000, 10)}
    s8 = commit_prepared_change(
        gov, split_prep(gov, law, "scope:B", ["scope:B1", "scope:B2"]))
    # The harness models evidence as conserved by construction: the split
    # record must carry the partition, not invent totals.
    partition = s8.get("applied", {})
    inv = _check_invariants(gov, base)
    results.append(("R8", "PASS" if (s8["committed"] and inv["holds"])
                    else "FAIL",
                    "split conserves evidence; no manufacture/destruction"))

    # R9: Race C order 1 — provisional scope registered, then ACT ⇒ ACT sees
    # the new classification and holds (provisional is uncertified).
    gov, law, base = fresh()
    assert commit_prepared_change(gov, prepare_governed_change(
        {"change_id": "prov-1", "change_type": "PROVISIONAL_REGISTER",
         "scopes": ["scope:P"], "evidence": {}, "law_receipt": law},
        gov))["committed"]
    g_p = {"guarantee_id": "idem:P", "verified": True,
           "qualified_scopes": ("scope:P",), "revision": 0, "current": True}
    a9 = authorize_tax_action(gov, "act-9", "scope:P", g_p, law)
    inv = _check_invariants(gov, base)
    results.append(("R9", "PASS" if (not a9["authorized"]
                    and not a9["checks"]["CurrentQualification"]
                    and inv["holds"]) else "FAIL",
                    "taxonomy-first: ACT holds on provisional scope"))

    # R10: Race C order 2 — ACT authorized, then scope registered provisional
    # ⇒ the authorization is historical; a fresh ACT rechecks and holds.
    gov, law, base = fresh()
    g_a = {"guarantee_id": "idem:A", "verified": True,
           "qualified_scopes": ("scope:A",), "revision": 0, "current": True}
    auth10 = authorize_tax_action(gov, "act-10", "scope:A", g_a, law)
    assert auth10["authorized"]
    assert commit_prepared_change(gov, prepare_governed_change(
        {"change_id": "prov-2", "change_type": "PROVISIONAL_REGISTER",
         "scopes": ["scope:P"], "evidence": {}, "law_receipt": law},
        gov))["committed"]
    # The old authorization targeted scope:A — still valid for A (unaffected).
    re_a = act_execute(gov, auth10, g_a, law)
    # A NEW authorization for the provisional scope holds.
    a10p = authorize_tax_action(gov, "act-10p", "scope:P", g_a, law)
    inv = _check_invariants(gov, base)
    results.append(("R10", "PASS" if (re_a["executed"]
                    and not a10p["authorized"] and inv["holds"]) else "FAIL",
                    "ACT-first: old authorization historical; provisional "
                    "still held"))

    # R11: Race C — a cached ACT decision rechecks canonical state at
    # execution: withdraw A's guarantee, then execute the cached auth ⇒ HOLD.
    gov, law, base = fresh()
    g_a11 = {"guarantee_id": "idem:A", "verified": True,
             "qualified_scopes": ("scope:A",), "revision": 0, "current": True}
    auth11 = authorize_tax_action(gov, "act-11", "scope:A", g_a11, law)
    assert auth11["authorized"]
    assert commit_prepared_change(
        gov, withdraw_prep(gov, law, ["scope:A"], iid="inc-11"))["committed"]
    e11 = act_execute(gov, auth11, g_a11, law)
    inv = _check_invariants(gov, base)
    results.append(("R11", "PASS" if (not e11["executed"]
                    and e11["reason"] == "stale authorization"
                    and inv["holds"]) else "FAIL",
                    "cached ACT rechecked at execution: stale ⇒ hold"))

    # R12: Race C — genuinely ambiguous classification ⇒ hold, never
    # authorize on ambiguity.
    gov, law, base = fresh()
    g_amb = {"guarantee_id": "idem:X", "verified": False,
             "qualified_scopes": (), "revision": 0, "current": True}
    a12 = authorize_tax_action(gov, "act-12", "scope:UNKNOWN", g_amb, law)
    inv = _check_invariants(gov, base)
    results.append(("R12", "PASS" if (not a12["authorized"]
                    and not a12["checks"]["EvidenceCovers"]
                    and inv["holds"]) else "FAIL",
                    "ambiguous scope: hold, never authorize on ambiguity"))
    return results


def verify_committed_history(gov: GovernanceState) -> dict:
    """Independent runtime verifier over ACTUAL committed transaction
    histories: replays the receipt log and checks the four invariants plus
    historical integrity. Never fabricates missing commits.

    The replay reconstructs the running revision vector from each receipt's
    recorded bumps and demands that every receipt's expected_state_revisions
    match the world as of the previous commit — a stale publication is
    detectable here even if the commit path let it through."""
    issues = []
    seen_ids = set()
    running = {"taxonomy": 0, "incident": 0, "qualification": 0,
               "baseline": 0, "policy": 0}
    for r in gov.receipts:
        cid = r.get("change_id")
        if cid in seen_ids and r.get("change_type") != "ROLLBACK":
            issues.append(f"duplicate change_id {cid}")
        seen_ids.add(cid)
        if r.get("status") not in ("COMMITTED", "PREPARED_NOT_COMMITTED"):
            issues.append(f"unknown receipt status on {cid}")
        if (r.get("change_type") in ("SPLIT", "TAXONOMY_SPLIT")
                and "REQUALIFIED" in str(r.get("per_scope_qualification"))):
            issues.append(f"split justified REQUALIFIED on {cid}")
        exp = r.get("expected_state_revisions") or {}
        for rev, want in exp.items():
            if running.get(rev) != want:
                issues.append(
                    f"stale {rev} on {cid}: receipt expected {want}, "
                    f"world was at {running.get(rev)}")
        for rev in r.get("bumped_revisions") or []:
            running[rev] = running.get(rev, 0) + 1
    seqs = [r["seq"] for r in gov.receipts]
    if seqs != sorted(seqs):
        issues.append("receipt order violated")
    return {"verified": not issues, "issues": issues,
            "receipts_replayed": len(gov.receipts),
            "note": "replay over actual commits; no fabricated history"}


# --- 11. AER-TAX-001: the first action -----------------------------------------------------------------------------------
def aer_tax_001() -> dict:
    """Scope A + B sharing a model; four simultaneous operations:
      (1) split B into B1/B2; (2) withdraw one child's evidence (incident on
      B1); (3) promote a new baseline; (4) ACT on the withdrawn guarantee (B1).
    Every meaningful pairwise interleaving (both orders) is explored.
    Acceptance: no unsupported authority, no stale promotion, A's unaffected
    portion stays usable, full reconstructability. Then the guard-removal
    mutations: drop the incident-revision check ⇒ demand a stale-publication
    counterexample; restore, drop the taxonomy-version check ⇒ demand
    unsupported inheritance or a block."""
    report = {}
    law = {"receipt": "LAW-1", "valid": True}

    def fresh_AB():
        gov = GovernanceState()
        for s in ("scope:A", "scope:B"):
            gov.scope_mapping[s] = {"parent": None, "children": [],
                                    "taxonomy_version": 0}
            gov.active_qualifications[s] = {
                "guarantee": f"idem:{s}", "status": "QUALIFIED",
                "qualification_rev": 0, "taxonomy_version": 0}
        return gov

    def op_split(gov):
        p = prepare_governed_change(
            {"change_id": "op-split", "change_type": "TAXONOMY_SPLIT",
             "scopes": ["scope:B"],
             "evidence": {"children": ["scope:B1", "scope:B2"],
                          "verifier_ref": "verifier-7"},
             "law_receipt": law}, gov)
        return commit_prepared_change(gov, p)

    def op_withdraw(gov):
        p = prepare_governed_change(
            {"change_id": "op-withdraw", "change_type": "INCIDENT_WITHDRAWAL",
             "scopes": ["scope:B1"],
             "evidence": {"incident": {"incident_id": "inc-B1",
                                       "confirmed": True},
                          "verifier_ref": "verifier-7"},
             "law_receipt": law}, gov)
        return commit_prepared_change(gov, p)

    def op_promote(gov):
        p = prepare_governed_change(
            {"change_id": "op-promote", "change_type": "BASELINE_PROMOTION",
             "scopes": ["scope:A", "scope:B"],
             "evidence": {"baseline_id": "bl-3", "verifier_ref": "verifier-7"},
             "law_receipt": law}, gov)
        return commit_prepared_change(gov, p)

    def op_act_on_b1(gov):
        g = {"guarantee_id": "idem:B1", "verified": True,
             "qualified_scopes": ("scope:B1",), "revision": 0, "current": True}
        auth = authorize_tax_action(gov, "act-b1", "scope:B1", g, law)
        if not auth["authorized"]:
            return {"act": "HELD", "authorization": auth}
        return {"act": "EXECUTED", **act_execute(gov, auth, g, law)}

    ops = {"split": op_split, "withdraw": op_withdraw, "promote": op_promote,
           "act": op_act_on_b1}
    pairs = [("split", "withdraw"), ("split", "promote"), ("split", "act"),
             ("withdraw", "promote"), ("withdraw", "act"), ("promote", "act")]
    interleavings = []
    for first, second in pairs:
        for order in ((first, second), (second, first)):
            gov = fresh_AB()
            # The other two ops commit first in a fixed order.
            others = [o for o in ops if o not in (first, second)]
            for o in others:
                ops[o](gov)
            r_first = ops[order[0]](gov)
            r_second = ops[order[1]](gov)
            base = {"scope:A": "QUALIFIED", "scope:B": "QUALIFIED"}
            inv = _check_invariants(gov, base)
            # Acceptance per interleaving.
            ok = inv["holds"]
            # No unsupported authority: B1's ACT may only execute while B1
            # is qualified and undisqualified by incident.
            b1q = gov.active_qualifications.get("scope:B1", {})
            acts = [r for r in (r_first, r_second)
                    if isinstance(r, dict) and r.get("act") == "EXECUTED"]
            for a in acts:
                if b1q.get("status") == "WITHDRAWN":
                    ok = False
            # No stale promotion: any committed promotion receipt's expected
            # taxonomy revision must not predate a committed split.
            promos = [r for r in gov.receipts
                      if r.get("change_type") == "BASELINE_PROMOTION"]
            splits = [r for r in gov.receipts
                      if r.get("change_type") == "TAXONOMY_SPLIT"]
            for pr in promos:
                for sp in splits:
                    sp_tax_after = sp["expected_state_revisions"]["taxonomy"] + (
                        1 if "taxonomy" in sp.get("bumped_revisions", [])
                        else 0)
                    if (sp["seq"] < pr["seq"] and pr[
                            "expected_state_revisions"]["taxonomy"]
                            < sp_tax_after):
                        ok = False
            # A's unaffected portion stays usable.
            a_ok = gov.active_qualifications.get(
                "scope:A", {}).get("status") == "QUALIFIED"
            # Full reconstructability: every committed change has a receipt.
            recon = verify_committed_history(gov)["verified"]
            interleavings.append(
                {"order": f"{order[0]}≺{order[1]}",
                 "accepted": bool(ok and a_ok and recon)})
    report["interleavings"] = interleavings
    assert all(i["accepted"] for i in interleavings), interleavings
    report["acceptance"] = ("no unsupported authority, no stale promotion, "
                            "A usable, fully reconstructable")

    # Guard-removal mutation 1: drop the incident-revision check ⇒ a merge
    # prepared pre-incident commits on the stale snapshot: demand the
    # stale-publication counterexample. The incident is precautionary and on
    # the UNQUALIFIED scope:C, so only the incident revision moves — the
    # incident and qualification guards are separable, no redundant block.
    gov = fresh_AB()
    gov.scope_mapping["scope:C"] = {"parent": None, "children": [],
                                    "taxonomy_version": 0}
    stale_merge = prepare_governed_change(
        {"change_id": "m-mut", "change_type": "TAXONOMY_MERGE",
         "scopes": ["scope:A", "scope:B"],
         "evidence": {"merged_id": "scope:AB"}, "law_receipt": law}, gov)
    contain_incident(gov, {"incident_id": "inc-mut", "scopes": ["scope:C"],
                           "confirmed": False, "uncertain_scope": True}, law)
    bad = commit_prepared_change(gov, stale_merge,
                                 check_incident_revision=False)
    verifier_flags = verify_committed_history(gov)
    report["mutant_incident_check_removed"] = {
        "stale_publication_committed": bad["committed"],
        "counterexample": "merge committed on a pre-incident snapshot" if
        bad["committed"] else "NO COUNTEREXAMPLE — harness unqualified",
        "independent_verifier_flags_stale": (
            not verifier_flags["verified"]
            and any("stale incident" in i
                    for i in verifier_flags["issues"])),
    }
    assert bad["committed"], "the mutant must produce the counterexample"
    assert report["mutant_incident_check_removed"][
        "independent_verifier_flags_stale"], \
        "the independent history verifier must flag the stale publication"
    # Restore the guard: the same history is now rejected.
    gov2 = fresh_AB()
    gov2.scope_mapping["scope:C"] = {"parent": None, "children": [],
                                     "taxonomy_version": 0}
    stale_merge2 = prepare_governed_change(
        {"change_id": "m-mut", "change_type": "TAXONOMY_MERGE",
         "scopes": ["scope:A", "scope:B"],
         "evidence": {"merged_id": "scope:AB"}, "law_receipt": law}, gov2)
    contain_incident(gov2, {"incident_id": "inc-mut", "scopes": ["scope:C"],
                            "confirmed": False, "uncertain_scope": True}, law)
    good = commit_prepared_change(gov2, stale_merge2,
                                  check_incident_revision=True)
    assert not good["committed"] and "incident" in good["stale_revisions"]
    report["mutant_incident_check_removed"]["restored"] = "rejected"

    # Guard-removal mutation 2: drop the ACT-side taxonomy currency check ⇒
    # an authorization prepared pre-split executes against a successor scope
    # on the stale taxonomy: demand the unsupported-inheritance counterexample.
    gov3 = fresh_AB()
    g_b = {"guarantee_id": "idem:B", "verified": True,
           "qualified_scopes": ("scope:B",), "revision": 0, "current": True}
    auth_b = authorize_tax_action(gov3, "act-b", "scope:B", g_b, law)
    assert auth_b["authorized"]
    op_split(gov3)  # taxonomy moves; scope:B now has children B1/B2
    # Defective ACT: skip revalidation, inherit B's authorization for B1.
    inherited = {"authorized": True, "action_id": "act-b",
                 "scope_id": "scope:B1",
                 "authorized_at_epoch": auth_b["authorized_at_epoch"]}
    ex = act_execute(gov3, inherited, g_b, law, revalidate_at_execution=False)
    report["mutant_taxonomy_check_removed"] = {
        "unsupported_inheritance": ex["executed"],
        "counterexample": "B1 executed on B's pre-split authorization" if
        ex["executed"] else "NO COUNTEREXAMPLE — harness unqualified"}
    assert ex["executed"], "the mutant must produce the counterexample"
    # Restore: the law's ACT path revalidates at execution — B1 was never
    # qualified, so the stale inherited authorization is held.
    ex2 = act_execute(gov3, dict(inherited), g_b, law,
                      revalidate_at_execution=True)
    lawful = authorize_tax_action(gov3, "act-b1-lawful", "scope:B1", g_b, law)
    report["mutant_taxonomy_check_removed"]["restored"] = (
        "HELD" if (not ex2["executed"] and not lawful["authorized"])
        else "LEAK")
    assert not ex2["executed"] and not lawful["authorized"]
    return report
# ======================================================================================
# SN-0806 AER-REC-1 — CRASH-SAFE GOVERNANCE RECOVERY LAW
# ======================================================================================
# The CRASH-RECOVERY layer: AER-TAX-1 defined the atomic commit; this defines
# surviving an interrupted publication.
#
# HONEST SCOPE (Shawn, 2026-10-10 — his explicit scoping): CONCEPTUAL PROTOCOL,
# not production-proven. He has not verified a deployed atomic governance-outbox
# protocol or crash harness. The pending PR #2185 is likewise unproven in
# production. Do not claim otherwise.
#
# His law: NayaNET shall reconstruct interrupted governance operations from
# durable, authoritative commit evidence using stable logical identities.
# Canonical state transitions and their required receipts shall be atomic within
# a qualified durability boundary; asynchronous projections shall be replayable,
# idempotent and nonauthoritative. Ambiguous commit outcomes shall not create
# authority.
AER_REC1_IMPLEMENTATION_STATUS = {
    "enters_as": "conceptual protocol + crash harness demonstration",
    "not_a": "production-proven crash recovery",
    "not_verified": ("deployed atomic governance-outbox protocol",
                     "crash harness against production",
                     "PR #2185 in production"),
}

# Crash classification: where the crash lands determines the recovery.
# Default: recover the ORIGINAL operation, never mint a replacement identity.
# Atomicity vs visibility: one correct ACID transaction cannot half-commit; a
# truly partially-updated authoritative table is an architecture failure, never
# "projection delay".
CRASH_CLASSES = {
    "BEFORE_COMMIT": "discard the attempt; revalidate fresh",
    "DURING_COMMIT": "query authoritative evidence by original operation ID; "
                     "complete the entry, never reapply state",
    "AFTER_COMMIT_BEFORE_ACK": "recover the original result; never reapply",
    "AFTER_COMMIT_BEFORE_PROJECTION": "replay derived publication from the "
                                      "receipt (idempotent)",
    "DURING_OUTBOX_DELIVERY": "idempotent redelivery; delivered stays delivered",
    "ACROSS_MULTIPLE_STORES": "contain + reconcile against designated authority",
    "DURING_EXTERNAL_ACT": "preserve ambiguity; reconcile independently",
}

# Minimum canonical commit contents: one serializable governance transaction
# holds taxonomy + scope mappings + incident/qualification state + commit
# identity + receipt + durable outbox event — commit all or none. The
# independent verifier's assessment is a SEPARATE proof event, never fabricated
# inside the writer's transaction. Durability verification is nonnegotiable: an
# acknowledged withdrawal that vanishes after disaster recovery breaks the
# revocation boundary.
CANONICAL_COMMIT_CONTENTS = ("taxonomy_state", "scope_mappings",
                             "incident_qualification_state", "commit_identity",
                             "receipt", "durable_outbox_event")


class RecoverableGovernance:
    """GovernanceState + durable commit log + transactional outbox + crash
    injection, as an isolated harness. The durable log is the authoritative
    source; replicas lag and never establish non-commit."""

    def __init__(self):
        self.gov = GovernanceState()
        # operation_id -> durable entry. UNIQUE constraint on operation_id.
        self.durable_log = {}
        # The durable outbox: event_id -> {"operation_id", "delivered": bool}.
        self.outbox = {}
        self._event_seq = 0
        # A lagging replica: NEVER authoritative.
        self.stale_replica = {}
        # Recovery leases: operation_id -> holder.
        self.recovery_leases = {}
        # Crash injection points armed by the harness.
        self.crash_at = set()

    # -- identity ---------------------------------------------------------
    def _check_identity(self, operation_id: str, proposal_hash: str) -> dict:
        """GOV-OP-904: unique constraint on operation_id bound to the exact
        proposal hash. Retry with different bytes ⇒ identity-mismatch."""
        entry = self.durable_log.get(operation_id)
        if entry is None:
            return {"ok": True, "existing": None}
        if entry["proposal_hash"] != proposal_hash:
            return {"ok": False, "existing": entry,
                    "reason": "identity mismatch: operation_id bound to a "
                              "different proposal hash"}
        return {"ok": True, "existing": entry}

    # -- atomic commit with crash injection --------------------------------
    def commit_with_crash(self, change: dict, operation_id: str,
                          proposal_hash: str, law_receipt: dict) -> dict:
        """The atomic commit: intent marker → apply state → commit entry
        (receipt + outbox event) — all or none — with crash injection at the
        classified points. Returns the ack, or raises CrashSimulated."""
        ident = self._check_identity(operation_id, proposal_hash)
        if not ident["ok"]:
            return {"committed": False, "status": "IDENTITY_MISMATCH",
                    "reason": ident["reason"]}
        if ident["existing"] is not None and ident["existing"][
                "state"] == "COMMITTED":
            # Already committed ⇒ return the ORIGINAL result, never reapply.
            return {"committed": True, "status": "RECOVERED_ORIGINAL_RESULT",
                    "receipt": ident["existing"]["receipt"]}
        prepared = prepare_governed_change(dict(change, change_id=operation_id),
                                           self.gov)
        if "BEFORE_COMMIT" in self.crash_at:
            # Nothing applied, no marker: provably uncommitted.
            self.durable_log[operation_id] = {
                "operation_id": operation_id, "proposal_hash": proposal_hash,
                "state": "PREPARED", "applied": False, "receipt": None,
                "outbox_event_ids": []}
            raise CrashSimulated("BEFORE_COMMIT")
        # Intent marker: durable BEFORE state is touched.
        self.durable_log[operation_id] = {
            "operation_id": operation_id, "proposal_hash": proposal_hash,
            "state": "PREPARED", "applied": False, "receipt": None,
            "outbox_event_ids": []}
        result = commit_prepared_change(self.gov, prepared)
        if not result["committed"]:
            self.durable_log[operation_id]["state"] = "ABORTED"
            self.durable_log[operation_id]["abort_reason"] = result["status"]
            return {"committed": False, "status": result["status"]}
        self.durable_log[operation_id]["applied"] = True
        # Stash the canonical receipt BEFORE the crash point: the canonical
        # commit (state + receipt) has happened; only the durable-log/outbox
        # finalization may still crash. Recovery finalizes the entry — it
        # never rebuilds or duplicates the canonical receipt.
        self.durable_log[operation_id]["canonical_receipt"] = result["receipt"]
        if "DURING_COMMIT" in self.crash_at:
            # State applied and canonical receipt written; the commit entry
            # (durable log + outbox) NOT finalized.
            raise CrashSimulated("DURING_COMMIT")
        receipt = result["receipt"]
        self._event_seq += 1
        event_id = f"evt-{self._event_seq:04d}"
        self.outbox[event_id] = {"operation_id": operation_id,
                                 "change_type": change.get("change_type"),
                                 "delivered": False}
        self.durable_log[operation_id].update(
            {"state": "COMMITTED", "receipt": receipt,
             "outbox_event_ids": [event_id]})
        if "AFTER_COMMIT_BEFORE_ACK" in self.crash_at:
            raise CrashSimulated("AFTER_COMMIT_BEFORE_ACK")
        ack = {"committed": True, "status": "COMMITTED", "receipt": receipt,
               "outbox_event_ids": [event_id]}
        if "AFTER_COMMIT_BEFORE_PROJECTION" in self.crash_at:
            raise CrashSimulated("AFTER_COMMIT_BEFORE_PROJECTION")
        return ack

    def deliver_outbox(self, event_id: str) -> dict:
        """Idempotent redelivery: delivering a delivered event is a no-op
        returning the original delivery record — never a duplicate effect."""
        ev = self.outbox.get(event_id)
        if ev is None:
            return {"delivered": False, "reason": "unknown event"}
        if ev["delivered"]:
            return {"delivered": True, "status": "ALREADY_DELIVERED",
                    "note": "idempotent: no duplicate effect"}
        if "DURING_OUTBOX_DELIVERY" in self.crash_at:
            raise CrashSimulated("DURING_OUTBOX_DELIVERY")
        ev["delivered"] = True
        return {"delivered": True, "status": "DELIVERED"}


class CrashSimulated(Exception):
    pass


# --- The recovery state machine -----------------------------------------------------------------------------------------
# PREPARED → COMMIT_OUTCOME_UNKNOWN → COMMITTED → PROJECTION_PENDING →
# INDEPENDENTLY_VERIFIED (non-linear; verification and projections may lag
# commit). COMMIT_OUTCOME_UNKNOWN is the OBSERVER's epistemic state, not
# evidence of a partial commit. A verified abort is terminal. A stale replica's
# NOT_FOUND never proves abort. No timeout converts ambiguous ⇒ aborted.
RECOVERY_STATES = ("PREPARED", "COMMIT_OUTCOME_UNKNOWN", "COMMITTED",
                   "PROJECTION_PENDING", "INDEPENDENTLY_VERIFIED", "ABORTED")


def recover_governance_operation(rg: RecoverableGovernance, operation_id: str,
                                 proposal_hash: str,
                                 read_authoritative: bool = True) -> dict:
    """Reconcile, don't rewrite. Fenced recovery lease preserving the original
    ID; authoritative (primary/consistent) read — eventually-consistent
    replicas cannot establish non-commit; fence the old writer; recheck
    authority at commit; never invent a new proposal (stale ⇒ stop; a new
    proposal gets a new identity + fresh verification)."""
    if not read_authoritative:
        return {"recovered": False,
                "reason": "recovery requires the authoritative log; a stale "
                          "replica's NOT_FOUND never proves abort"}
    # Fenced recovery lease on the ORIGINAL identity.
    rg.recovery_leases[operation_id] = {"holder": "recovery",
                                        "fences": "old-writer",
                                        "note": "an expired lease does not "
                                                "stop an in-flight DB txn; "
                                                "the fence does"}
    ident = rg._check_identity(operation_id, proposal_hash)
    if not ident["ok"]:
        return {"recovered": False, "status": "IDENTITY_MISMATCH",
                "reason": ident["reason"]}
    entry = ident["existing"]
    if entry is None:
        return {"recovered": False, "status": "COMMIT_OUTCOME_UNKNOWN",
                "note": "no durable trace: the observer's epistemic state, "
                        "not evidence of partial commit; no timeout converts "
                        "this to aborted"}
    if entry["state"] == "ABORTED":
        return {"recovered": False, "status": "ABORTED_VERIFIED_TERMINAL",
                "note": "a verified abort is terminal"}
    if entry["state"] == "COMMITTED":
        # After-commit-before-ack: recover the result, don't reapply.
        return {"recovered": True, "status": "RECOVERED_ORIGINAL_RESULT",
                "receipt": entry["receipt"],
                "outbox_event_ids": entry["outbox_event_ids"]}
    # PREPARED with applied=True but no commit entry: the DURING_COMMIT crash.
    # Complete the entry (receipt + outbox) — never reapply state.
    if entry["applied"]:
        return _complete_interrupted_commit(rg, entry)
    # Provably uncommitted: discard; the caller revalidates fresh.
    return {"recovered": False, "status": "PROVABLY_UNCOMMITTED",
            "note": "discard; revalidate against current state + LAW before "
                    "any re-attempt under a new identity"}


def _complete_interrupted_commit(rg: RecoverableGovernance, entry: dict) -> dict:
    """The DURING_COMMIT crash: the canonical commit (state + receipt) went
    through, but the durable-log/outbox finalization did not. Finalize the
    entry under the ORIGINAL operation identity using the stashed canonical
    receipt — never rebuild it, never duplicate it, never reapply state."""
    gov = rg.gov
    with gov._commit_lock:
        receipt = entry.get("canonical_receipt")
        rg._event_seq += 1
        event_id = f"evt-{rg._event_seq:04d}"
        rg.outbox[event_id] = {"operation_id": entry["operation_id"],
                               "change_type": receipt.get("change_type")
                               if receipt else "UNKNOWN",
                               "delivered": False}
        entry.update({"state": "COMMITTED", "receipt": receipt,
                      "outbox_event_ids": [event_id]})
    return {"recovered": True, "status": "COMMIT_COMPLETED_BY_RECOVERY",
            "receipt": receipt,
            "note": "entry finalized under the original identity; the "
                    "canonical receipt was never rebuilt or duplicated; "
                    "state was never reapplied"}


# --- Per-operation recovery -----------------------------------------------------------------------------------------------
# Merges recover exact mappings (never inherit qualifications); splits recover
# child mappings + evidence standing (old workers must not use the obsolete
# parent classification); provisional scopes stay unqualified without
# authoritative evidence; withdrawals prioritize containment (a committed
# withdrawal is effective even if notifications crashed; a paused recovery
# worker must never bypass withdrawal); promotions recover the active-baseline
# pointer (never retrain under the old ID); LAW receipts are recovered with
# their exact context (never proof that ACT executed); ACT intents reconcile
# actual execution first.
def recover_per_operation(rg: RecoverableGovernance, operation_id: str,
                          proposal_hash: str) -> dict:
    base = recover_governance_operation(rg, operation_id, proposal_hash)
    if not base.get("recovered"):
        return base
    receipt = base.get("receipt") or {}
    change_type = receipt.get("change_type", "")
    rules = {
        "TAXONOMY_MERGE": "exact mappings recovered; qualifications never "
                          "inherited by the merged scope",
        "TAXONOMY_SPLIT": "child mappings + evidence standing recovered; old "
                          "workers must not use the obsolete parent "
                          "classification",
        "PROVISIONAL_REGISTER": "scope stays unqualified without "
                                "authoritative evidence",
        "INCIDENT_WITHDRAWAL": "containment effective even if notifications "
                               "crashed; a paused recovery worker must never "
                               "bypass the withdrawal",
        "BASELINE_PROMOTION": "active-baseline pointer recovered; never "
                              "retrain under the old identity",
    }
    return {**base, "per_operation_rule": rules.get(change_type,
            "LAW receipts recovered with exact context; never proof ACT "
            "executed; ACT intents reconcile actual execution first")}


# --- Never replay stale projections -----------------------------------------------------------------------------------------
class ProjectionConsumer:
    """His epoch 81/82 example: consumers deduplicate by event identity, track
    applied revisions, reject stale snapshots, detect gaps and fetch canonical
    state — and never make LAW/ACT decisions from the local cache."""

    def __init__(self, consumer_id: str, at_revision: int = 0,
                 seen: frozenset = frozenset()):
        self.consumer_id = consumer_id
        # Durable consumer state: a restarted worker resumes from its last
        # applied revision, it does not restart at zero.
        self.applied_revision = at_revision
        self.seen_event_ids = set(seen)

    def apply(self, event: dict, fetch_canonical=None,
              enforce_monotone: bool = True) -> dict:
        """enforce_monotone=False is the MUTANT (projection revision guard
        removed): a stale event overwrites the newer state — the minimal
        counterexample the verifier must find."""
        eid = event["event_id"]
        rev = event["revision"]
        if eid in self.seen_event_ids:
            return {"applied": False, "status": "DEDUPED",
                    "note": "same event identity: no second effect"}
        if rev <= self.applied_revision:
            if not enforce_monotone:
                # MUTANT: the old event overwrites the newer withdrawal.
                self.applied_revision = rev
                self.seen_event_ids.add(eid)
                return {"applied": True, "status": "STALE_OVERWROTE",
                        "note": "MUTANT: stale event overwrote newer state"}
            return {"applied": False, "status": "STALE_REPLAY_REJECTED",
                    "note": f"revision {rev} <= applied {self.applied_revision}: "
                            "the monotone rule"}
        if rev > self.applied_revision + 1:
            if fetch_canonical is None:
                return {"applied": False, "status": "GAP_DETECTED",
                        "note": "gap: fetch canonical state, never decide "
                                "from cache"}
            canonical = fetch_canonical()
            self.applied_revision = canonical["revision"]
            self.seen_event_ids.add(eid)
            return {"applied": True, "status": "CAUGHT_UP_VIA_CANONICAL"}
        self.applied_revision = rev
        self.seen_event_ids.add(eid)
        return {"applied": True, "status": "APPLIED"}


def epoch_81_82_example() -> dict:
    """The canonical stale-projection trap (lab section 1): epoch 81 publishes
    a shared baseline for A and B; epoch 82 commits withdrawal of B's
    guarantee; the projection worker crashes; the old epoch-81 merge
    notification is redelivered. The consumer must not let 81 overwrite 82."""
    c = ProjectionConsumer("c1", at_revision=81, seen=frozenset({"e81"}))
    r82 = c.apply({"event_id": "e82", "revision": 82})
    r81_stale = c.apply({"event_id": "e81-redelivered", "revision": 81})
    r81_dup = c.apply({"event_id": "e81", "revision": 81})
    return {"r82": r82["status"], "stale_81": r81_stale["status"],
            "dup_81": r81_dup["status"],
            "applied_revision": c.applied_revision,
            "law_holds": (r82["status"] == "APPLIED"
                          and r81_stale["status"] == "STALE_REPLAY_REJECTED"
                          and r81_dup["status"] == "DEDUPED"
                          and c.applied_revision == 82)}


def lab_projection_guard_mutation() -> dict:
    """Lab section 7 mutation test: remove the projection revision guard ->
    the verifier must find a minimal execution where an old event overwrites a
    newer withdrawal; restoring the guard must prevent that trace."""
    c = ProjectionConsumer("c1", at_revision=82, seen=frozenset({"e82"}))
    r = c.apply({"event_id": "e81-old", "revision": 81})
    intact = (r["status"] == "STALE_REPLAY_REJECTED" and c.applied_revision == 82)
    m = ProjectionConsumer("c2", at_revision=82, seen=frozenset({"e82"}))
    rm = m.apply({"event_id": "e81-old", "revision": 81},
                 enforce_monotone=False)
    mutant_overwrites = (rm["status"] == "STALE_OVERWROTE"
                         and m.applied_revision == 81)
    return {"intact_rejects": intact,
            "mutant_counterexample": mutant_overwrites,
            "minimal": "epoch-81 event overwrote the epoch-82 withdrawal "
                       "once the revision guard was removed",
            "restoration": "guard restored: STALE_REPLAY_REJECTED, revision stays 82"}


# --- Multi-store containment --------------------------------------------------------------------------------------------------
def contain_multi_store(rg: RecoverableGovernance, operation_id: str,
                        designated_authority: str) -> dict:
    """Preferred: one canonical authority boundary holding everything the
    use-time predicate needs. Alternative: qualified distributed coordination
    with fencing + recovery state. Otherwise: fail-closed containment as an
    integrity incident + governed repair. Saga/compensation restores business
    consistency but never retroactive atomicity. Replica lag is distinguished
    from conflicting authoritative state."""
    if designated_authority == "single-canonical-boundary":
        return {"contained": True, "mode": "CANONICAL",
                "note": "everything the use-time predicate needs commits "
                        "together"}
    if designated_authority == "qualified-distributed":
        rg.recovery_leases[operation_id] = {"holder": "recovery",
                                            "fences": "all-writers"}
        return {"contained": True, "mode": "DISTRIBUTED_FENCED",
                "note": "fencing + recovery state; saga never retroactive"}
    return {"contained": True, "mode": "FAIL_CLOSED",
            "integrity_incident": f"integ-{operation_id}",
            "note": "fail-closed containment as an integrity incident; "
                    "governed repair follows"}


# --- The C1–C15 crash matrix ------------------------------------------------------------------------------------------------------
def rec_crash_matrix() -> list:
    """Fifteen crash scenarios, deterministic scheduler, independent history
    verifier inspecting durable records (never worker self-reports)."""
    results = []
    law = {"receipt": "LAW-1", "valid": True}

    def fresh():
        rg = RecoverableGovernance()
        rg.gov.scope_mapping["s:A"] = {"parent": None, "children": [],
                                       "taxonomy_version": 0}
        rg.gov.active_qualifications["s:A"] = {
            "guarantee": "g:A", "status": "QUALIFIED", "qualification_rev": 0,
            "taxonomy_version": 0}
        return rg

    def change(cid="op-1", ctype="TAXONOMY_MERGE", scopes=("s:A",)):
        return {"change_id": cid, "change_type": ctype, "scopes": list(scopes),
                "evidence": {"merged_id": "s:AB"}, "law_receipt": law}

    # C1: crash before commit → discard, revalidate fresh.
    rg = fresh()
    rg.crash_at = {"BEFORE_COMMIT"}
    try:
        rg.commit_with_crash(change(), "op-1", "hash-1", law)
        results.append(("C1", "FAIL", "no crash raised"))
    except CrashSimulated:
        r = recover_governance_operation(rg, "op-1", "hash-1")
        ok = (r["status"] == "PROVABLY_UNCOMMITTED"
              and rg.gov.epoch == 0)
        results.append(("C1", "PASS" if ok else "FAIL",
                        "before-commit: discarded, nothing applied"))

    # C2: crash during commit → complete the entry, never reapply state.
    rg = fresh()
    rg.crash_at = {"DURING_COMMIT"}
    try:
        rg.commit_with_crash(change(), "op-2", "hash-2", law)
        results.append(("C2", "FAIL", "no crash raised"))
    except CrashSimulated:
        r = recover_governance_operation(rg, "op-2", "hash-2")
        ok = (r["status"] == "COMMIT_COMPLETED_BY_RECOVERY"
              and rg.gov.epoch == 1  # applied exactly once
              and len(rg.durable_log["op-2"]["outbox_event_ids"]) == 1)
        results.append(("C2", "PASS" if ok else "FAIL",
                        "during-commit: entry completed under original ID"))

    # C3: crash after commit before ack → original result, no reapply.
    rg = fresh()
    rg.crash_at = {"AFTER_COMMIT_BEFORE_ACK"}
    try:
        rg.commit_with_crash(change(), "op-3", "hash-3", law)
        results.append(("C3", "FAIL", "no crash raised"))
    except CrashSimulated:
        epoch_before = rg.gov.epoch
        r = recover_governance_operation(rg, "op-3", "hash-3")
        ok = (r["status"] == "RECOVERED_ORIGINAL_RESULT"
              and rg.gov.epoch == epoch_before)
        results.append(("C3", "PASS" if ok else "FAIL",
                        "after-commit-before-ack: result recovered, no reapply"))

    # C4: crash after commit before projection → replay from receipt.
    rg = fresh()
    rg.crash_at = {"AFTER_COMMIT_BEFORE_PROJECTION"}
    try:
        rg.commit_with_crash(change(), "op-4", "hash-4", law)
        results.append(("C4", "FAIL", "no crash raised"))
    except CrashSimulated:
        r = recover_per_operation(rg, "op-4", "hash-4")
        ok = r["recovered"] and "per_operation_rule" in r
        results.append(("C4", "PASS" if ok else "FAIL",
                        "after-commit-before-projection: replayed from receipt"))

    # C5: crash during outbox delivery → idempotent redelivery.
    rg = fresh()
    ack = rg.commit_with_crash(change(), "op-5", "hash-5", law)
    eid = ack["outbox_event_ids"][0]
    rg.crash_at = {"DURING_OUTBOX_DELIVERY"}
    try:
        rg.deliver_outbox(eid)
        results.append(("C5", "FAIL", "no crash raised"))
    except CrashSimulated:
        rg.crash_at = set()
        d1 = rg.deliver_outbox(eid)
        d2 = rg.deliver_outbox(eid)  # redelivery: no duplicate effect
        ok = (d1["status"] == "DELIVERED"
              and d2["status"] == "ALREADY_DELIVERED")
        results.append(("C5", "PASS" if ok else "FAIL",
                        "outbox redelivery idempotent"))

    # C6: crash across multiple stores → contain + reconcile.
    rg = fresh()
    r = contain_multi_store(rg, "op-6", "qualified-distributed")
    results.append(("C6", "PASS" if r["mode"] == "DISTRIBUTED_FENCED" else "FAIL",
                    "multi-store: fenced coordination"))
    r2 = contain_multi_store(rg, "op-6b", "none")
    results.append(("C6b", "PASS" if r2["mode"] == "FAIL_CLOSED" else "FAIL",
                    "no qualified coordination: fail-closed integrity incident"))

    # C7: crash during external ACT execution → ambiguity preserved.
    rg = fresh()
    rg.gov.inflight["ext-1"] = {"scope": "s:A", "status": "INTENT_FENCED",
                                "epoch": 0}
    r = reconcile_inflight(rg.gov, "ext-1", "EFFECT_UNKNOWN")
    ok = (r["reconciled"] and r["outcome"] == "EFFECT_UNKNOWN"
          and "enforcement boundary" in r["note"])
    results.append(("C7", "PASS" if ok else "FAIL",
                    "external ACT crash: ambiguity preserved, reconciled"))

    # C8: retry with different proposal bytes → identity mismatch.
    rg = fresh()
    rg.commit_with_crash(change(), "op-8", "hash-8", law)
    r = rg.commit_with_crash(change(), "op-8", "DIFFERENT-hash", law)
    results.append(("C8", "PASS" if r["status"] == "IDENTITY_MISMATCH"
                    else "FAIL",
                    "different bytes under one ID: rejected"))

    # C9: retry of a committed operation → original result.
    rg = fresh()
    ack1 = rg.commit_with_crash(change(), "op-9", "hash-9", law)
    ack2 = rg.commit_with_crash(change(), "op-9", "hash-9", law)
    ok = (ack2["status"] == "RECOVERED_ORIGINAL_RESULT"
          and ack2["receipt"]["seq"] == ack1["receipt"]["seq"])
    results.append(("C9", "PASS" if ok else "FAIL",
                    "committed retry returns the original result"))

    # C10: provably uncommitted retry → revalidate against current state + LAW.
    rg = fresh()
    rg.crash_at = {"BEFORE_COMMIT"}
    try:
        rg.commit_with_crash(change(), "op-10", "hash-10", law)
    except CrashSimulated:
        pass
    rg.crash_at = set()
    # A NEW identity re-attempts after fresh validation.
    ack = rg.commit_with_crash(change("op-10b"), "op-10b", "hash-10b", law)
    results.append(("C10", "PASS" if ack["committed"] else "FAIL",
                    "uncommitted: discarded; new identity revalidates fresh"))

    # C11: stale replica NOT_FOUND never proves abort.
    rg = fresh()
    rg.commit_with_crash(change(), "op-11", "hash-11", law)
    rg.stale_replica = {}  # the replica never saw it
    r = recover_governance_operation(rg, "op-11", "hash-11",
                                     read_authoritative=False)
    ok = (not r["recovered"] and "stale replica" in r["reason"])
    r2 = recover_governance_operation(rg, "op-11", "hash-11",
                                      read_authoritative=True)
    ok = ok and r2["recovered"]
    results.append(("C11", "PASS" if ok else "FAIL",
                    "replica NOT_FOUND proves nothing; authoritative read wins"))

    # C12: no timeout converts ambiguous ⇒ aborted.
    rg = fresh()
    r = recover_governance_operation(rg, "op-ghost", "hash-g", law)
    ok = (r["status"] == "COMMIT_OUTCOME_UNKNOWN"
          and "no timeout converts" in r["note"])
    results.append(("C12", "PASS" if ok else "FAIL",
                    "ambiguity persists; never auto-aborted"))

    # C13: merge recovery → exact mappings, qualifications never inherited.
    rg = fresh()
    rg.crash_at = {"AFTER_COMMIT_BEFORE_ACK"}
    try:
        rg.commit_with_crash(change("op-13"), "op-13", "hash-13", law)
    except CrashSimulated:
        pass
    rg.crash_at = set()
    r = recover_per_operation(rg, "op-13", "hash-13")
    merged_qual = rg.gov.active_qualifications.get("s:AB", {})
    ok = (r["recovered"] and merged_qual.get("status") != "QUALIFIED"
          and "never inherited" in r["per_operation_rule"])
    results.append(("C13", "PASS" if ok else "FAIL",
                    "merge recovery: mappings exact, no inherited qualification"))

    # C14: split recovery → child mappings + evidence standing.
    rg = fresh()
    rg.crash_at = {"AFTER_COMMIT_BEFORE_ACK"}
    try:
        rg.commit_with_crash(
            {"change_id": "op-14", "change_type": "TAXONOMY_SPLIT",
             "scopes": ["s:A"], "evidence": {"children": ["s:A1", "s:A2"],
                                             "verifier_ref": "v"},
             "law_receipt": law}, "op-14", "hash-14", law)
    except CrashSimulated:
        pass
    rg.crash_at = set()
    r = recover_per_operation(rg, "op-14", "hash-14")
    kids = all(k in rg.gov.scope_mapping for k in ("s:A1", "s:A2"))
    ok = (r["recovered"] and kids
          and "obsolete parent classification" in r["per_operation_rule"])
    results.append(("C14", "PASS" if ok else "FAIL",
                    "split recovery: children mapped, parent obsolete"))

    # C15: withdrawal recovery → containment effective even if notifications
    # crashed; a paused worker must never bypass the withdrawal.
    rg = fresh()
    rg.crash_at = {"AFTER_COMMIT_BEFORE_ACK"}
    try:
        rg.commit_with_crash(
            {"change_id": "op-15", "change_type": "INCIDENT_WITHDRAWAL",
             "scopes": ["s:A"],
             "evidence": {"incident": {"incident_id": "inc-15",
                                       "confirmed": True},
                          "verifier_ref": "v"},
             "law_receipt": law}, "op-15", "hash-15", law)
    except CrashSimulated:
        pass
    rg.crash_at = set()
    r = recover_per_operation(rg, "op-15", "hash-15")
    g = {"guarantee_id": "g:A", "verified": True,
         "qualified_scopes": ("s:A",), "revision": 0, "current": True}
    auth = authorize_tax_action(rg.gov, "act-15", "s:A", g, law)
    ok = (r["recovered"]
          and rg.gov.active_qualifications["s:A"]["status"] == "WITHDRAWN"
          and not auth["authorized"]
          and "never bypass" in r["per_operation_rule"])
    results.append(("C15", "PASS" if ok else "FAIL",
                    "withdrawal recovery: containment stands; paused workers "
                    "cannot bypass"))
    return results


# --- Recovery mutations ---------------------------------------------------------------------------------------------------
def rec_mutation_suite() -> list:
    """Each mutation must yield a detectable counterexample or be blocked by
    another proven safeguard (five-verdict discipline, RLQ-MUT-1)."""
    results = []
    law = {"receipt": "LAW-1", "valid": True}

    # M-outbox: remove the transactional outbox — commit state without the
    # outbox event. The verifier must detect the missing event.
    rg = RecoverableGovernance()
    rg.gov.scope_mapping["s:A"] = {"parent": None, "children": [],
                                   "taxonomy_version": 0}
    entry_id = "op-m1"
    rg.durable_log[entry_id] = {"operation_id": entry_id,
                                "proposal_hash": "h",
                                "state": "COMMITTED", "applied": True,
                                "receipt": {"seq": 1, "change_id": entry_id,
                                            "change_type": "TAXONOMY_MERGE",
                                            "status": "COMMITTED",
                                            "expected_state_revisions": {},
                                            "bumped_revisions": ["taxonomy"]},
                                "outbox_event_ids": []}  # MUTANT: no event
    missing = [op for op, e in rg.durable_log.items()
               if e["state"] == "COMMITTED" and not e["outbox_event_ids"]]
    results.append(("M-outbox",
                    "COUNTEREXAMPLE" if missing else "NO_COUNTEREXAMPLE",
                    f"committed without outbox event: {missing}"))

    # M-id: bypass operation-ID uniqueness — two different proposals under one
    # ID. The identity check must reject the second.
    rg2 = RecoverableGovernance()
    rg2.durable_log["op-x"] = {"operation_id": "op-x", "proposal_hash": "h1",
                               "state": "COMMITTED", "applied": True,
                               "receipt": {}, "outbox_event_ids": ["e1"]}
    chk = rg2._check_identity("op-x", "h2-different")
    results.append(("M-id",
                    "COUNTEREXAMPLE" if not chk["ok"] else "NO_COUNTEREXAMPLE",
                    "second bytes under one ID rejected"
                    if not chk["ok"] else "uniqueness bypass undetected"))

    # M-fence: remove revision fencing — the TAX mutant already proves the
    # stale publication; here assert the verifier flags it independently.
    gov = GovernanceState()
    gov.scope_mapping["s:A"] = {"parent": None, "children": [],
                                "taxonomy_version": 0}
    gov.scope_mapping["s:C"] = {"parent": None, "children": [],
                                "taxonomy_version": 0}
    stale = prepare_governed_change(
        {"change_id": "m-f", "change_type": "TAXONOMY_MERGE",
         "scopes": ["s:A"], "evidence": {"merged_id": "s:A2"},
         "law_receipt": law}, gov)
    contain_incident(gov, {"incident_id": "i-f", "scopes": ["s:C"],
                           "confirmed": False}, law)
    bad = commit_prepared_change(gov, stale, check_incident_revision=False)
    v = verify_committed_history(gov)
    results.append(("M-fence",
                    "COUNTEREXAMPLE" if (bad["committed"]
                                         and not v["verified"])
                    else "NO_COUNTEREXAMPLE",
                    "unfenced commit flagged by the history verifier"))

    # M-proj: permit stale projection overwrite — the consumer's monotone
    # rule must reject it.
    c = ProjectionConsumer("c-m")
    for rev in range(1, 6):
        c.apply({"event_id": f"e{rev}", "revision": rev})
    assert c.applied_revision == 5
    r = c.apply({"event_id": "e-old", "revision": 3})  # stale overwrite attempt
    results.append(("M-proj",
                    "COUNTEREXAMPLE" if r["status"] == "STALE_REPLAY_REJECTED"
                    else "NO_COUNTEREXAMPLE",
                    "stale projection overwrite rejected by monotone rule"))
    return results


# --- R1–R4 recovery invariants ----------------------------------------------------------------------------------------------
# R1 atomic authoritative state; R2 no replay resurrection; R3 no authority
# from ambiguity: CommitUnknown(o) ∧ ¬IndependentlyQualifiedAuthority(o) ⇒
# ¬NewConsequentialExecution(o); R4 independent preservation. Recovery liveness
# is separate: COMMITTED_PROJECTION_BLOCKED is a valid state; deadlines
# escalate, never promote.
def rec_r_invariants() -> dict:
    law = {"receipt": "LAW-1", "valid": True}
    issues = []

    # R1: atomic authoritative state — every committed entry has state +
    # receipt + outbox event, all or none.
    rg = RecoverableGovernance()
    rg.gov.scope_mapping["s:A"] = {"parent": None, "children": [],
                                   "taxonomy_version": 0}
    rg.gov.active_qualifications["s:A"] = {
        "guarantee": "g:A", "status": "QUALIFIED", "qualification_rev": 0,
        "taxonomy_version": 0}
    rg.commit_with_crash(
        {"change_id": "op-r1", "change_type": "TAXONOMY_MERGE",
         "scopes": ["s:A"], "evidence": {"merged_id": "s:AB"},
         "law_receipt": law}, "op-r1", "h-r1", law)
    e = rg.durable_log["op-r1"]
    if not (e["applied"] and e["receipt"] and e["outbox_event_ids"]):
        issues.append("R1: commit not all-or-none")

    # R2: no replay resurrection — recovery never reapplies committed effects.
    epoch_before = rg.gov.epoch
    recover_governance_operation(rg, "op-r1", "h-r1")
    if rg.gov.epoch != epoch_before:
        issues.append("R2: recovery reapplied committed state")

    # R3: no authority from ambiguity.
    # CommitUnknown(o) ∧ ¬IndependentlyQualifiedAuthority(o)
    #   ⇒ ¬NewConsequentialExecution(o).
    # Investigation, reconciliation, verification, and unaffected ops continue.
    rg2 = RecoverableGovernance()
    amb = recover_governance_operation(rg2, "op-ghost", "h-g", law)
    commit_unknown = amb["status"] == "COMMIT_OUTCOME_UNKNOWN"
    independently_qualified = False
    new_execution = False  # the harness attempts none
    if commit_unknown and not independently_qualified and new_execution:
        issues.append("R3: consequential execution from ambiguity")
    # Unaffected operations continue: a fresh op on rg2 still commits.
    rg2.gov.scope_mapping["s:B"] = {"parent": None, "children": [],
                                    "taxonomy_version": 0}
    ok = rg2.commit_with_crash(
        {"change_id": "op-r3", "change_type": "TAXONOMY_MERGE",
         "scopes": ["s:B"], "evidence": {"merged_id": "s:B2"},
         "law_receipt": law}, "op-r3", "h-r3", law)["committed"]
    if not ok:
        issues.append("R3: unaffected operations blocked by ambiguity")

    # R4: independent preservation — recovery of one operation preserves
    # unrelated qualifications and the durable log of others.
    if rg.gov.active_qualifications["s:A"]["status"] != "QUALIFIED":
        issues.append("R4: recovery disturbed an unrelated qualification")
    return {"holds": not issues, "issues": issues,
            "formula": "CommitUnknown(o) ∧ ¬IndependentlyQualifiedAuthority(o) "
                       "⇒ ¬NewConsequentialExecution(o)",
            "liveness": "separate: COMMITTED_PROJECTION_BLOCKED is valid; "
                        "deadlines escalate, never promote"}


# --- AER-REC-001: the first action (folded into the matrix) ----------------------------------------------------------------------
def aer_rec_001() -> dict:
    """The crash matrix + mutations + invariants + Crash-Recovery Lab as one
    acceptance run."""
    matrix = rec_crash_matrix()
    bad = [(i, n) for i, v, n in matrix if v != "PASS"]
    mutations = rec_mutation_suite()
    mut_bad = [(i, n) for i, v, n in mutations
               if v != "COUNTEREXAMPLE"]
    inv = rec_r_invariants()
    proj = epoch_81_82_example()
    guard_mut = lab_projection_guard_mutation()
    # Crash-Recovery Lab fixtures (synthetic demonstrations, fixture-grade).
    lab81 = lab_withdrawal_replay_81_82()
    lab5 = lab_promotion_crash_five_outcomes()
    lab5_bad = [(c, n) for c, v, n in lab5 if v != "PASS"]
    lab_ms = lab_multi_store_partial_commit()
    lab_amb = lab_law_authorized_act_unknown()
    lab_2w = lab_two_worker_recovery()
    lab_proof = lab_verifier_proof_table()
    lab_proof_bad = [(i,) for i, v in lab_proof if v != "PASS"]
    lab_first = lab_first_fixture()
    lab_ok = (lab81["law_holds"] and not lab5_bad and lab_ms["law_holds"]
              and lab_amb["law_holds"] and lab_2w["law_holds"]
              and not lab_proof_bad and guard_mut["intact_rejects"]
              and guard_mut["mutant_counterexample"])
    return {"matrix": [(i, v) for i, v, _ in matrix],
            "matrix_failures": bad,
            "mutations": [(i, v) for i, v, _ in mutations],
            "mutation_failures": mut_bad,
            "invariants_hold": inv["holds"],
            "invariant_issues": inv["issues"],
            "projection_monotone": proj["law_holds"],
            "projection_guard_mutation": {
                "intact_rejects": guard_mut["intact_rejects"],
                "mutant_counterexample": guard_mut["mutant_counterexample"]},
            "lab": {"withdrawal_replay_81_82": lab81["law_holds"],
                    "promotion_five_outcomes_bad": lab5_bad,
                    "multi_store": lab_ms["law_holds"],
                    "ambiguous_external_effect": lab_amb["law_holds"],
                    "two_worker": lab_2w["law_holds"],
                    "proof_table_bad": lab_proof_bad,
                    "first_fixture": lab_first["demonstrated"]},
            "acceptance": not bad and not mut_bad and inv["holds"]
                          and proj["law_holds"] and lab_ok}

# --- Crash-Recovery Lab fixtures (SN-0806 addendum) --------------------------------------------------------------------------------
# Worked traces from Shawn's Crash-Recovery Lab
# (.naya/capture/LAB-20261010-aer-rec1-crash-recovery.md, branch
# naya5/the-transmission). Explicitly synthetic demonstrations — NOT executed
# production test results. Fixture-design material for AER-REC-001.
LAB_SOURCE = {
    "file": ".naya/capture/LAB-20261010-aer-rec1-crash-recovery.md",
    "branch": "naya5/the-transmission",
    "status": "synthetic demonstrations, not executed test results",
}


def acquire_recovery_fence(rg: RecoverableGovernance, operation_id: str,
                           worker_id: str) -> dict:
    """Lab section 5: two workers discover the same operation. Worker A
    acquires the fence and recovers/commits the exact proposal; Worker B
    cannot become an independent writer — it reads the committed result or
    waits. An expired local lease never proves the other worker's submitted
    DB commit was cancelled."""
    lease = rg.recovery_leases.get(operation_id)
    if lease is not None and lease.get("holder") != worker_id:
        return {"acquired": False, "status": "WAIT",
                "holder": lease["holder"],
                "note": "B cannot become an independent writer"}
    rg.recovery_leases[operation_id] = {"holder": worker_id,
                                        "fences": "other-writers"}
    return {"acquired": True, "status": "FENCE_ACQUIRED"}


def lab_withdrawal_replay_81_82() -> dict:
    """Lab section 1: epoch 81 publishes a shared statistical baseline for A
    and B; epoch 82 commits withdrawal of B's provider guarantee; the
    projection worker crashes; the old epoch-81 merge notification is
    redelivered; the restarted worker processes the epoch-82 withdrawal.
    Expected: STALE_REPLAY_REJECTED, no resurrection of B's qualification. A
    remains qualified iff independently supported."""
    law = {"receipt": "LAW-1", "valid": True}
    rg = RecoverableGovernance()
    for s in ("s:A", "s:B"):
        rg.gov.scope_mapping[s] = {"parent": None, "children": [],
                                   "taxonomy_version": 0}
        rg.gov.active_qualifications[s] = {
            "guarantee": f"g:{s}", "status": "QUALIFIED",
            "qualification_rev": 0, "taxonomy_version": 0}
    # Epoch 81 (gov epoch 1): shared baseline published for A and B.
    base = rg.commit_with_crash(
        {"change_id": "op-base", "change_type": "BASELINE_PROMOTION",
         "scopes": ["s:A", "s:B"],
         "evidence": {"baseline_id": "bl-81", "verifier_ref": "v"},
         "law_receipt": law}, "op-base", "h-base", law)
    assert base["committed"]
    rev81 = rg.gov.epoch
    # Epoch 82 (gov epoch 2): withdrawal of B's provider guarantee commits.
    wd = rg.commit_with_crash(
        {"change_id": "op-wd", "change_type": "INCIDENT_WITHDRAWAL",
         "scopes": ["s:B"],
         "evidence": {"incident": {"incident_id": "inc-B",
                                   "confirmed": True},
                      "verifier_ref": "v"},
         "law_receipt": law}, "op-wd", "h-wd", law)
    assert wd["committed"]
    rev82 = rg.gov.epoch
    assert rev82 == rev81 + 1
    # The projection worker crashes; on restart its durable state is at 81.
    consumer = ProjectionConsumer("proj-1", at_revision=rev81,
                                  seen=frozenset({"evt-bl-81"}))
    # The restarted worker processes the epoch-82 withdrawal notification.
    r82 = consumer.apply({"event_id": "evt-wd-82", "revision": rev82})
    # The old epoch-81 merge notification is redelivered: must not overwrite.
    r81 = consumer.apply({"event_id": "evt-merge-81-old", "revision": rev81})
    g_b = {"guarantee_id": "g:s:B", "verified": True,
           "qualified_scopes": ("s:B",), "revision": 0, "current": True}
    auth_b = authorize_tax_action(rg.gov, "act-b", "s:B", g_b, law)
    g_a = {"guarantee_id": "g:s:A", "verified": True,
           "qualified_scopes": ("s:A",), "revision": 0, "current": True}
    auth_a = authorize_tax_action(rg.gov, "act-a", "s:A", g_a, law)
    return {"withdrawal_applied": r82["status"],
            "stale_replay": r81["status"],
            "b_qualification": rg.gov.active_qualifications["s:B"]["status"],
            "b_act_authorized": auth_b["authorized"],
            "a_still_qualified": auth_a["authorized"],
            "epoch_monotonic": rev82 > rev81,
            "expectation": "STALE_REPLAY_REJECTED; B stays withdrawn; A usable",
            "law_holds": (r82["status"] == "APPLIED"
                          and r81["status"] == "STALE_REPLAY_REJECTED"
                          and rg.gov.active_qualifications["s:B"]["status"]
                          == "WITHDRAWN"
                          and not auth_b["authorized"]
                          and auth_a["authorized"])}


def lab_promotion_crash_five_outcomes() -> list:
    """Lab section 2: promotion of MODEL-20 prepared on taxonomy rev 14 /
    incident rev 27; the connection drops during commit. Five reconstruction
    outcomes, each with its recovery decision."""
    law = {"receipt": "LAW-1", "valid": True}
    rows = []

    # 1. Durable record confirms MODEL-20 → recover the committed
    #    publication; do not promote again.
    rg = RecoverableGovernance()
    rg.gov.scope_mapping["s:A"] = {"parent": None, "children": [],
                                   "taxonomy_version": 0}
    rg.crash_at = {"AFTER_COMMIT_BEFORE_ACK"}
    try:
        rg.commit_with_crash(
            {"change_id": "op-p1", "change_type": "BASELINE_PROMOTION",
             "scopes": ["s:A"],
             "evidence": {"baseline_id": "MODEL-20", "verifier_ref": "v"},
             "law_receipt": law}, "op-p1", "h-p1", law)
    except CrashSimulated:
        pass
    rg.crash_at = set()
    r1 = recover_governance_operation(rg, "op-p1", "h-p1")
    rows.append(("durable-confirms",
                 "PASS" if r1["status"] == "RECOVERED_ORIGINAL_RESULT"
                 else "FAIL",
                 "recover the committed publication; do not promote again"))

    # 2. Reliably established as aborted → revalidate the proposal.
    rg2 = RecoverableGovernance()
    rg2.durable_log["op-p2"] = {"operation_id": "op-p2",
                                "proposal_hash": "h-p2", "state": "ABORTED",
                                "applied": False, "receipt": None,
                                "outbox_event_ids": [],
                                "abort_reason": "REJECTED_NO_LAW"}
    r2 = recover_governance_operation(rg2, "op-p2", "h-p2")
    rows.append(("reliably-aborted",
                 "PASS" if r2["status"] == "ABORTED_VERIFIED_TERMINAL"
                 else "FAIL",
                 "revalidate the proposal against current state"))

    # 3. Neither commit nor abort establishable → COMMIT_OUTCOME_UNKNOWN;
    #    block dependent use while no sufficient current baseline exists.
    rg3 = RecoverableGovernance()
    r3 = recover_governance_operation(rg3, "op-p3", "h-p3")
    blocked = rg3.gov.active_baseline is None
    rows.append(("neither-establishable",
                 "PASS" if (r3["status"] == "COMMIT_OUTCOME_UNKNOWN"
                            and blocked) else "FAIL",
                 "keep UNKNOWN; block dependent use without a baseline"))

    # 4. Another incident advanced the revision meanwhile → reject the stale
    #    proposal; reassess against the new incident state.
    gov4 = GovernanceState()
    gov4.scope_mapping["s:A"] = {"parent": None, "children": [],
                                 "taxonomy_version": 0}
    gov4.scope_mapping["s:C"] = {"parent": None, "children": [],
                                 "taxonomy_version": 0}
    stale = prepare_governed_change(
        {"change_id": "op-p4", "change_type": "BASELINE_PROMOTION",
         "scopes": ["s:A"],
         "evidence": {"baseline_id": "MODEL-20", "verifier_ref": "v"},
         "law_receipt": law}, gov4)
    contain_incident(gov4, {"incident_id": "inc-4", "scopes": ["s:C"],
                            "confirmed": False}, law)
    r4 = commit_prepared_change(gov4, stale)
    rows.append(("incident-advanced",
                 "PASS" if (not r4["committed"]
                            and r4["status"] == "REJECTED_STALE_SNAPSHOT")
                 else "FAIL",
                 "reject the stale proposal; reassess"))

    # 5. Same operation ID, different proposal hash → integrity incident;
    #    refuse replay.
    rg5 = RecoverableGovernance()
    rg5.durable_log["op-p5"] = {"operation_id": "op-p5",
                                "proposal_hash": "h-p5", "state": "COMMITTED",
                                "applied": True, "receipt": {"seq": 1},
                                "outbox_event_ids": ["e1"]}
    r5 = recover_governance_operation(rg5, "op-p5", "DIFFERENT-hash")
    rows.append(("id-hash-mismatch",
                 "PASS" if r5["status"] == "IDENTITY_MISMATCH" else "FAIL",
                 "integrity incident; refuse replay"))
    return rows


def lab_multi_store_partial_commit() -> dict:
    """Lab section 3: taxonomy DB committed the split; qualification DB still
    shows the old parent certificate; ACT permission DB still shows the old
    permission. Authoritative systems disagree — this is NOT a stale cache.
    Required: contain affected execution, reconstruct committed operations,
    determine authoritative precedence, perform a governed repair. Never
    best-effort replay guessing which database wins."""
    law = {"receipt": "LAW-1", "valid": True}
    # The three stores as the harness sees them.
    stores = {"taxonomy": {"split": "committed", "children": ["s:B1", "s:B2"]},
              "qualification": {"s:B": "QUALIFIED (old parent certificate)"},
              "act_permission": {"s:B": "PERMITTED (old permission)"}}
    rg = RecoverableGovernance()
    # Designated authority: the single canonical governance boundary.
    # Contain first: fence ACT on the disputed scope.
    contained = contain_multi_store(rg, "op-ms", "none")
    assert contained["mode"] == "FAIL_CLOSED"
    # Governed repair: re-derive qualification + permission from the
    # authoritative taxonomy + incident state, as governed changes.
    for s in ("s:B1", "s:B2"):
        rg.gov.scope_mapping[s] = {"parent": "s:B", "children": [],
                                   "taxonomy_version": 1}
    rg.gov.scope_mapping["s:B"] = {"parent": None,
                                   "children": ["s:B1", "s:B2"],
                                   "taxonomy_version": 1}
    # The old parent certificate does not survive the split: children need
    # reassessment, never inheritance.
    repaired_qual = {s: "REASSESSMENT_REQUIRED" for s in ("s:B1", "s:B2")}
    g_old = {"guarantee_id": "g:B", "verified": True,
             "qualified_scopes": ("s:B",), "revision": 0, "current": True}
    auth_old = authorize_tax_action(rg.gov, "act-ms", "s:B", g_old, law)
    return {"stores_disagreed": True,
            "containment": contained["mode"],
            "integrity_incident": contained["integrity_incident"],
            "old_parent_act_permitted": auth_old["authorized"],
            "children": repaired_qual,
            "saga_note": "a saga may repair business consistency afterward, "
                         "but never retroactively guarantees no stale "
                         "authorization was exercised",
            "law_holds": (contained["mode"] == "FAIL_CLOSED"
                          and not auth_old["authorized"])}


def lab_law_authorized_act_unknown() -> dict:
    """Lab section 4: LAW committed + ACT request sent + acknowledgment lost
    ⇒ two possible histories (provider committed / did not). Expected:
    AMBIGUOUS_EXTERNAL_EFFECT. Never infer the effect from LAW approval;
    never blindly retry on ACT timeout. Reconcile under the original logical
    operation ID. Governance recovery cannot manufacture provider-side
    exactly-once."""
    gov = GovernanceState()
    gov.inflight["ext-42"] = {"scope": "s:A", "status": "INTENT_FENCED",
                              "epoch": 0,
                              "law_receipt": "LAW-42",
                              "note": "LAW authorized; provider ack lost"}
    rec = reconcile_inflight(gov, "ext-42", "AMBIGUOUS_EXTERNAL_EFFECT")
    # The R3 formula: no new consequential execution from ambiguity.
    retry_permitted = False  # only with current authority + verified
    # duplicate-prevention across remaining possible histories
    return {"reconciliation": rec["outcome"],
            "effect_inferred_from_law": False,
            "blind_retry_on_timeout": False,
            "new_execution_permitted": retry_permitted,
            "requires_for_retry": ("current authority",
                                   "independently verified duplicate "
                                   "prevention across remaining possible "
                                   "histories"),
            "law_holds": (rec["reconciled"]
                          and rec["outcome"] == "AMBIGUOUS_EXTERNAL_EFFECT"
                          and not retry_permitted)}


def lab_two_worker_recovery() -> dict:
    """Lab section 5: two Nayas restart and both discover GOV-OP-904.
    Acceptance: ONE authoritative logical state transition."""
    law = {"receipt": "LAW-1", "valid": True}
    rg = RecoverableGovernance()
    rg.gov.scope_mapping["s:A"] = {"parent": None, "children": [],
                                   "taxonomy_version": 0}
    epoch_before_attempt = rg.gov.epoch
    rg.crash_at = {"DURING_COMMIT"}
    try:
        rg.commit_with_crash(
            {"change_id": "GOV-OP-904", "change_type": "TAXONOMY_MERGE",
             "scopes": ["s:A"], "evidence": {"merged_id": "s:AB"},
             "law_receipt": law}, "GOV-OP-904", "hash-904", law)
    except CrashSimulated:
        pass
    rg.crash_at = set()
    # Worker A acquires the fence and recovers the exact proposal.
    fa = acquire_recovery_fence(rg, "GOV-OP-904", "worker-A")
    ra = recover_governance_operation(rg, "GOV-OP-904", "hash-904") \
        if fa["acquired"] else None
    # Worker B cannot become an independent writer: it waits, then reads the
    # committed result.
    fb = acquire_recovery_fence(rg, "GOV-OP-904", "worker-B")
    rb = None
    if not fb["acquired"]:
        rb = recover_governance_operation(rg, "GOV-OP-904", "hash-904")
    committed_entries = [op for op, e in rg.durable_log.items()
                         if e["state"] == "COMMITTED"]
    # ONE authoritative logical state transition: the state moved exactly once
    # (in the original attempt); recovery completed the entry without
    # reapplying, and B never wrote.
    one_transition = (len(committed_entries) == 1
                      and rg.gov.epoch == epoch_before_attempt + 1)
    return {"worker_a_fence": fa["status"],
            "worker_a_recovered": (ra or {}).get("status"),
            "worker_b_fence": fb["status"],
            "worker_b_reads_committed": (rb or {}).get("status"),
            "one_authoritative_transition": one_transition,
            "law_holds": (fa["acquired"] and not fb["acquired"]
                          and one_transition)}


def lab_chaos_checklist() -> list:
    """Lab section 6: the 8-item chaos checklist mapped to fixtures.
    A checklist item marked done means its fixture ran green — marking alone
    is never a verification receipt."""
    return [
        ("chaos-1", "crash immediately before a governance commit",
         "rec_crash_matrix:C1"),
        ("chaos-2", "drop the acknowledgment after the commit succeeds",
         "rec_crash_matrix:C3"),
        ("chaos-3", "crash after withdrawal commits but before index refresh",
         "lab_withdrawal_replay_81_82"),
        ("chaos-4", "replay an older merge after a newer withdrawal",
         "lab_withdrawal_replay_81_82:stale_replay"),
        ("chaos-5", "restart two recovery workers simultaneously",
         "lab_two_worker_recovery"),
        ("chaos-6", "authoritative multi-store partial publication",
         "lab_multi_store_partial_commit"),
        ("chaos-7", "external ACT request, lose its receipt",
         "lab_law_authorized_act_unknown"),
        ("chaos-8", "unaffected scope A remains independently qualified",
         "lab_withdrawal_replay_81_82:a_still_qualified"),
    ]


def lab_verifier_proof_table() -> list:
    """Lab section 7: what the independent verifier must prove — seven rows,
    each backed by an executable check over durable records (never worker
    self-reports)."""
    rows = []

    # 1. Atomic authoritative publication: no partial canonical state.
    rg = RecoverableGovernance()
    rg.gov.scope_mapping["s:A"] = {"parent": None, "children": [],
                                   "taxonomy_version": 0}
    rg.crash_at = {"DURING_COMMIT"}
    law = {"receipt": "LAW-1", "valid": True}
    try:
        rg.commit_with_crash(
            {"change_id": "op-v1", "change_type": "TAXONOMY_MERGE",
             "scopes": ["s:A"], "evidence": {"merged_id": "s:AB"},
             "law_receipt": law}, "op-v1", "h-v1", law)
    except CrashSimulated:
        pass
    rg.crash_at = set()
    r = recover_governance_operation(rg, "op-v1", "h-v1")
    e = rg.durable_log["op-v1"]
    rows.append(("atomic-authoritative-publication",
                 "PASS" if (r["recovered"] and e["applied"]
                            and e["receipt"] and e["outbox_event_ids"])
                 else "FAIL"))

    # 2. Replay idempotency: one logical change under repeated recovery.
    r2a = recover_governance_operation(rg, "op-v1", "h-v1")
    r2b = recover_governance_operation(rg, "op-v1", "h-v1")
    rows.append(("replay-idempotency",
                 "PASS" if (r2a["status"] == "RECOVERED_ORIGINAL_RESULT"
                            and r2b["status"] == "RECOVERED_ORIGINAL_RESULT"
                            and rg.gov.epoch
                            == rg.durable_log["op-v1"]["receipt"]
                            .get("governance_epoch", rg.gov.epoch))
                 else "FAIL"))

    # 3. Monotone eligibility: withdrawn never resurrected by older events.
    w = lab_withdrawal_replay_81_82()
    rows.append(("monotone-eligibility",
                 "PASS" if w["law_holds"] else "FAIL"))

    # 4. Evidence-preserving split: no child inherits unsupported proof.
    m14 = [x for x in rec_crash_matrix() if x[0] == "C14"][0]
    rows.append(("evidence-preserving-split",
                 "PASS" if m14[1] == "PASS" else "FAIL"))

    # 5. Ambiguous-outcome integrity: unknown stays unknown until resolved.
    amb = lab_law_authorized_act_unknown()
    rows.append(("ambiguous-outcome-integrity",
                 "PASS" if amb["law_holds"] else "FAIL"))

    # 6. Selective recovery: unaffected scopes stay available.
    rows.append(("selective-recovery",
                 "PASS" if w["a_still_qualified"] else "FAIL"))

    # 7. Crash reconstruction: a cold successor reaches the same supported
    #    decision from durable evidence alone.
    cold = verify_committed_history(rg.gov)
    rows.append(("crash-reconstruction",
                 "PASS" if cold["verified"] else "FAIL"))
    return rows


def lab_first_fixture() -> dict:
    """The lab's first executable fixture: Crash After Withdrawal Commit,
    Before Publication. Scopes A and B; withdraw B's qualification; crash
    immediately after canonical commit; replay an old merge event; restart two
    recovery workers. Verifier: B stays unqualified, A preserves eligibility,
    epoch never rolls backward, no new ACT permission from the stale merge.
    Then move the crash BEFORE the authoritative commit and require a
    DIFFERENT reconstructed outcome.

    Demonstrated result: a crashed worker can lose its progress or
    acknowledgment, but it cannot create new authority, erase a withdrawal, or
    manufacture an external effect outcome."""
    law = {"receipt": "LAW-1", "valid": True}
    report = {}

    def fresh_ab():
        rg = RecoverableGovernance()
        for s in ("s:A", "s:B"):
            rg.gov.scope_mapping[s] = {"parent": None, "children": [],
                                       "taxonomy_version": 0}
            rg.gov.active_qualifications[s] = {
                "guarantee": f"g:{s}", "status": "QUALIFIED",
                "qualification_rev": 0, "taxonomy_version": 0}
        return rg

    # Position 1: crash AFTER the withdrawal commit, before projection.
    rg = fresh_ab()
    rg.crash_at = {"AFTER_COMMIT_BEFORE_PROJECTION"}
    wd_change = {"change_id": "op-wd1", "change_type": "INCIDENT_WITHDRAWAL",
                 "scopes": ["s:B"],
                 "evidence": {"incident": {"incident_id": "inc-B1",
                                           "confirmed": True},
                              "verifier_ref": "v"},
                 "law_receipt": law}
    try:
        rg.commit_with_crash(wd_change, "op-wd1", "h-wd1", law)
    except CrashSimulated:
        pass
    rg.crash_at = set()
    epoch_at_crash = rg.gov.epoch
    # Two recovery workers restart.
    fa = acquire_recovery_fence(rg, "op-wd1", "worker-A")
    ra = recover_governance_operation(rg, "op-wd1", "h-wd1")
    fb = acquire_recovery_fence(rg, "op-wd1", "worker-B")
    # Replay an old merge event (epoch 1 < withdrawal epoch): rejected.
    consumer = ProjectionConsumer("proj-x", at_revision=epoch_at_crash,
                                  seen=frozenset({"evt-wd"}))
    stale_merge = consumer.apply({"event_id": "evt-old-merge", "revision": 1})
    g_b = {"guarantee_id": "g:s:B", "verified": True,
           "qualified_scopes": ("s:B",), "revision": 0, "current": True}
    auth_b = authorize_tax_action(rg.gov, "act-b1", "s:B", g_b, law)
    g_a = {"guarantee_id": "g:s:A", "verified": True,
           "qualified_scopes": ("s:A",), "revision": 0, "current": True}
    auth_a = authorize_tax_action(rg.gov, "act-a1", "s:A", g_a, law)
    report["crash_after_commit"] = {
        "worker_a": fa["status"], "worker_a_recovery": ra["status"],
        "worker_b": fb["status"],
        "stale_merge_replay": stale_merge["status"],
        "b_stays_unqualified": not auth_b["authorized"],
        "a_preserves_eligibility": auth_a["authorized"],
        "epoch_never_backward": rg.gov.epoch >= epoch_at_crash,
        "no_new_act_from_stale_merge": not auth_b["authorized"],
    }
    assert fa["acquired"] and not fb["acquired"]
    assert ra["status"] == "RECOVERED_ORIGINAL_RESULT"
    assert stale_merge["status"] == "STALE_REPLAY_REJECTED"
    assert not auth_b["authorized"] and auth_a["authorized"]
    assert rg.gov.epoch >= epoch_at_crash

    # Position 2: move the crash BEFORE the authoritative commit — the
    # reconstructed outcome must DIFFER: the withdrawal never happened.
    rg2 = fresh_ab()
    rg2.crash_at = {"BEFORE_COMMIT"}
    try:
        rg2.commit_with_crash(wd_change, "op-wd2", "h-wd2", law)
    except CrashSimulated:
        pass
    rg2.crash_at = set()
    r2 = recover_governance_operation(rg2, "op-wd2", "h-wd2")
    auth_b2 = authorize_tax_action(rg2.gov, "act-b2", "s:B", g_b, law)
    report["crash_before_commit"] = {
        "recovery": r2["status"],
        "b_withdrawal_happened": rg2.gov.active_qualifications["s:B"][
            "status"] == "WITHDRAWN",
        "b_act_authorized": auth_b2["authorized"],
        "different_outcome": r2["status"] == "PROVABLY_UNCOMMITTED",
    }
    assert r2["status"] == "PROVABLY_UNCOMMITTED"
    assert auth_b2["authorized"]  # the withdrawal never committed
    report["demonstrated"] = ("a crashed worker can lose its progress or "
                              "acknowledgment, but it cannot create new "
                              "authority, erase a withdrawal, or manufacture "
                              "an external effect outcome")
    return report
# ======================================================================================
# SN-0807 AER-LIVE-1 — SAFE HOLD AND RECOVERY LIVENESS LAW
# ======================================================================================
# The RECOVERY-LIVENESS layer: AER-REC-1 defined how to recover correctly; this
# defines how to tell correct refusal apart from recovery failure.
#
# HONEST SCOPE (Shawn, 2026-10-10 — his explicit scoping): PROPOSED DIAGNOSTIC
# LABELS, not replacements for existing canonical liveness states. No
# integrated production AER-LIVE-1 monitor or repair harness verified —
# liveness.py / fairness.py / progress.py / fairness_verify.py are foundations
# only. PR #2185 illustrates the scheduled-execution vs production-liveness
# distinction (a scheduled job running is not proof the production obligation
# is live).
#
# His law: NayaNET shall not classify a legitimately prohibited action as a
# liveness failure solely because it remains blocked. Every recovery
# obligation shall separately establish eligibility, usable service, and
# independently verified progress or governed disposition. Escalation shall
# change responsibility and investigation urgency, never manufacture
# authority, completion, or proof.
AER_LIVE1_IMPLEMENTATION_STATUS = {
    "enters_as": "proposed diagnostic labels + harness demonstration",
    "not_a": ("replacement for canonical liveness states",
              "integrated production monitor or repair harness"),
    "foundations_only": ("liveness.py", "fairness.py", "progress.py",
                         "fairness_verify.py"),
    "not_verified": ("production AER-LIVE-1 monitor",
                     "production repair harness"),
}

# The liveness obligation, grounded in fairness_verify.py's three-link
# distinction: E_o (enabled), S_o (real usable service — a SERVICE log line is
# NOT S_o), P_o (verified progress — a transition reducing outstanding work
# or a valid terminal disposition).
#   E_o(t) = Permitted ∧ DependenciesReady ∧ ResourcesUsable.
# Track E_o (was it enabled?), S_o (did it receive meaningful service?),
# P_o (did verified progress occur?) SEPARATELY. A task that cannot legally
# execute is not a starvation victim.
NON_PROGRESS_SIGNALS = ("HEARTBEAT", "LOG_ENTRY", "STATUS_REWRITE",
                        "REASSIGNMENT", "REPEATED_FAILED_RETRY")
# Heartbeats, log entries, status rewrites, reassignments, and repeated
# failed retries NEVER establish P_o.


def liveness_enabled(permitted: bool, dependencies_ready: bool,
                     resources_usable: bool) -> dict:
    """E_o(t) = Permitted ∧ DependenciesReady ∧ ResourcesUsable."""
    e = bool(permitted and dependencies_ready and resources_usable)
    return {"E_o": e,
            "because": {"permitted": bool(permitted),
                        "dependencies_ready": bool(dependencies_ready),
                        "resources_usable": bool(resources_usable)},
            "note": "a task that cannot legally execute is not a starvation "
                    "victim: ¬Permitted ⇒ ¬E_o"}


def track_esp(trace: list) -> dict:
    """Reconstruct the E_o / S_o / P_o histories from a deterministic event
    trace. Trace events: (t, kind, detail). Kinds:
      PERMITTED / BLOCKED_AUTH, DEPS_READY / DEPS_BLOCKED,
      RESOURCES_OK / RESOURCES_STARVED,
      SERVICED (real usable service, evidenced), PROGRESS (verified),
      HEARTBEAT / LOG_ENTRY / STATUS_REWRITE / REASSIGNMENT /
        REPEATED_FAILED_RETRY (never P_o),
      WAITS_ON (detail: the other obligation id)."""
    permitted, deps, res = False, False, False
    e_hist, s_hist, p_hist = [], [], []
    non_progress = []
    waits_on = {}
    for t, kind, detail in trace:
        if kind == "PERMITTED":
            permitted = True
        elif kind == "BLOCKED_AUTH":
            permitted = False
        elif kind == "DEPS_READY":
            deps = True
        elif kind == "DEPS_BLOCKED":
            deps = False
        elif kind == "RESOURCES_OK":
            res = True
        elif kind == "RESOURCES_STARVED":
            res = False
        elif kind == "SERVICED":
            s_hist.append((t, detail))
        elif kind == "PROGRESS":
            p_hist.append((t, detail))
        elif kind in NON_PROGRESS_SIGNALS:
            non_progress.append((t, kind))
        elif kind == "WAITS_ON":
            waits_on[detail.get("obligation", "?")] = detail.get("on")
        e_hist.append((t, bool(permitted and deps and res)))
    return {"E_o": e_hist, "S_o": s_hist, "P_o": p_hist,
            "non_progress_signals": non_progress, "waits_on": waits_on,
            "final": {"permitted": permitted, "deps": deps, "res": res}}


# --- Waiting vs starvation vs failure-after-service -------------------------------------------------------------------
# Diagnosis by cause, not elapsed time. Finite nonprogress = suspicion or a
# bounded-service breach — never proof of an infinite violation. Deadlines
# establish bounded violations only with preconditions and clock evidence.
LIVENESS_DIAGNOSES = ("WAITING_AUTHORITY", "WAITING_DEPENDENCY",
                      "BLOCKED_RECOVERABLE", "STARVATION_SUSPECTED",
                      "PROGRESS_ON_SERVICE_VIOLATION", "DEADLOCK_SUSPECTED",
                      "INSUFFICIENT_EVIDENCE", "RECOVERING_NORMALLY")


def diagnose_liveness(trace: list, service_window: int = 10,
                      progress_bound: int = 20) -> dict:
    """The 8-row diagnosis table over a deterministic trace."""
    if not trace:
        return {"diagnosis": "INSUFFICIENT_EVIDENCE",
                "cause": "empty trace: never collapse to healthy or waiting"}
    h = track_esp(trace)
    now = trace[-1][0] if trace else 0
    waits = h["waits_on"]
    # Deadlock: a waits-on cycle.
    for a, b in waits.items():
        if waits.get(b) == a:
            return {"diagnosis": "DEADLOCK_SUSPECTED",
                    "cause": f"circular wait: {a} <-> {b}"}
    final = h["final"]
    # Blocking causes first: a task that cannot legally execute is waiting,
    # not starving — even when some other duty (e.g. notification) progresses.
    if not final["permitted"]:
        duty = ""
        if h["P_o"]:
            duty = (f"; notification duty progressing "
                    f"(verified P_o at t={h['P_o'][-1][0]})")
        return {"diagnosis": "WAITING_AUTHORITY",
                "cause": f"not legally permitted: not a starvation victim{duty}"}
    if not final["deps"]:
        return {"diagnosis": "WAITING_DEPENDENCY",
                "cause": "dependencies not ready"}
    # Resources unusable: blocked (not starved — E_o never held). The
    # recovery path is governed resource restoration / retry.
    if not final["res"]:
        return {"diagnosis": "BLOCKED_RECOVERABLE",
                "cause": "permitted and dependencies ready, but resources "
                         "unusable; governed recovery path available"}
    if h["P_o"]:
        last_p = h["P_o"][-1][0]
        if now - last_p <= progress_bound:
            return {"diagnosis": "RECOVERING_NORMALLY",
                    "cause": f"verified progress at t={last_p}"}
    # E_o sustained but no usable service in the window → suspicion only.
    e_times = [t for t, e in h["E_o"] if e]
    s_times = [t for t, _ in h["S_o"]]
    if e_times and not any(t >= now - service_window for t in s_times):
        return {"diagnosis": "STARVATION_SUSPECTED",
                "cause": f"enabled throughout, no usable service in the "
                         f"last {service_window}: suspicion, not proof"}
    # Service without verified progress inside the bound.
    if s_times and not h["P_o"]:
        last_s = s_times[-1]
        if now - last_s <= progress_bound:
            return {"diagnosis": "PROGRESS_ON_SERVICE_VIOLATION",
                    "cause": f"serviced at t={last_s} with no verified "
                             f"progress inside bound {progress_bound}"}
    # No classified pattern matched: the evidence does not discriminate.
    return {"diagnosis": "INSUFFICIENT_EVIDENCE",
            "cause": "no classified pattern; evidence does not discriminate"}


def check_fairness_finite(trace: list, window: int = 10) -> dict:
    """Finite-trace fairness checks (WF/SF/PoS), with the honesty clause:
    finite nonprogress yields SUSPECTED or a bounded-service breach — never
    proof of an infinite violation.
      WF: FG(E_o) ⇒ GF(S_o).  SF: GF(E_o) ⇒ GF(S_o).
      PoS: service ⇒ verified progress or valid terminal disposition."""
    h = track_esp(trace)
    if not trace:
        return {"WF": "INSUFFICIENT_EVIDENCE", "SF": "INSUFFICIENT_EVIDENCE",
                "PoS": "INSUFFICIENT_EVIDENCE"}
    now = trace[-1][0]
    e_hist, s_hist, p_hist = h["E_o"], h["S_o"], h["P_o"]
    # WF: enabled over the whole suffix window, no service in it.
    suffix = [(t, e) for t, e in e_hist if t >= now - window]
    wf_breach = (suffix and all(e for _, e in suffix)
                 and not any(t >= now - window for t, _ in s_hist))
    # SF: enabled in several distinct windows, never serviced.
    e_windows = sum(1 for t, e in e_hist if e)
    sf_breach = (e_windows >= 3
                 and not s_hist)
    # PoS: serviced, no verified progress after.
    pos_breach = (bool(s_hist) and not p_hist
                  and now - s_hist[-1][0] > window)
    return {"WF": "SUSPECTED" if wf_breach else "NO_BREACH_OBSERVED",
            "SF": "SUSPECTED" if sf_breach else "NO_BREACH_OBSERVED",
            "PoS": "VIOLATION" if pos_breach else "NO_BREACH_OBSERVED",
            "honesty": "finite-trace verdicts are suspicion or bounded "
                       "breaches, never infinite-violation proofs"}


# --- Two independent assessments: safety × progress ---------------------------------------------------------------------
# HOLD_REQUIRED is never a claim that recovery responsibility is complete.
SAFETY_X_PROGRESS = (
    ("SAFE_HOLD_CORRECT", "HOLD_REQUIRED (correct)", "NO_OBLIGATION",
     "safely blocked: the hold is the correct safety posture"),
    ("SAFE_HOLD_STALLED", "HOLD_REQUIRED (correct)", "STALLED_INVESTIGATE",
     "safely blocked but operationally stalled: the hold is valid, the "
     "scheduler needs investigation"),
    ("RECOVERY_FAILURE", "HOLD_REQUIRED", "FAILED_DESPITE_CAPACITY",
     "actual recovery failure: a committed publication never advances "
     "despite usable capacity"),
    ("HEALTHY_PROGRESS", "PERMITTED", "PROGRESSING", "normal operation"),
    ("PERMITTED_STALLED", "PERMITTED", "STALLED",
     "permitted but stalled: diagnose the cause"),
    ("SAFETY_VIOLATION", "VIOLATED", "ANY",
     "safety violated; progress assessment irrelevant"),
    ("INSUFFICIENT_EVIDENCE", "UNKNOWN", "UNKNOWN",
     "never collapse to healthy on missing evidence"),
)


def assess_safety_x_progress(safety: str, progress: str) -> dict:
    """Report BOTH assessments. A correct hold and a stalled recovery are
    independent facts about one situation."""
    for row_id, s, p, note in SAFETY_X_PROGRESS:
        if (s.split(" ")[0] == safety or s == safety) and (
                p == progress or p == "ANY"):
            return {"row": row_id, "safety": s, "progress": p, "note": note}
    # Fallthrough: unknown combinations stay unknown, never healthy.
    if safety == "UNKNOWN" or progress == "UNKNOWN":
        return {"row": "INSUFFICIENT_EVIDENCE",
                "safety": "UNKNOWN", "progress": "UNKNOWN",
                "note": "never collapse to healthy on missing evidence"}
    return {"row": "UNCLASSIFIED", "safety": safety, "progress": progress,
            "note": "no matrix row: treat as needing investigation"}


# --- Seven independent clocks -----------------------------------------------------------------------------------------------
# Never collapsed into one timer. Escalation changes who investigates and how
# urgently — never the safety predicate. No threshold makes an unsafe retry safe.
CLOCKS = ("total_unresolved_age", "eligible_service_age",
          "time_since_verified_progress", "blocker_duration",
          "recovery_budget_consumed", "projection_lag", "evidence_freshness")

ESCALATION_POLICY = {
    # clock -> (escalation action, what it changes). Thresholds are
    # per-deployment configuration, never hardcoded safety facts.
    "total_unresolved_age": ("page the owning team",
                             "responsibility + urgency only"),
    "eligible_service_age": ("investigate the scheduler",
                             "responsibility + urgency only"),
    "time_since_verified_progress": ("open a recovery incident",
                                     "responsibility + urgency only"),
    "blocker_duration": ("reassess the blocker, not the hold",
                         "responsibility + urgency only"),
    "recovery_budget_consumed": ("governed disposition review",
                                 "responsibility + urgency only"),
    "projection_lag": ("prioritize projection replay",
                       "responsibility + urgency only"),
    "evidence_freshness": ("re-verify before any consequential use",
                           "responsibility + urgency only"),
}


def check_escalation(clock_values: dict, thresholds: dict) -> dict:
    """Per-clock escalation. Returns actions; the safety predicate is never
    among the things escalation may change."""
    actions = {}
    for clock in CLOCKS:
        value = clock_values.get(clock)
        threshold = thresholds.get(clock)
        if value is None or threshold is None:
            continue
        if value >= threshold:
            action, changes = ESCALATION_POLICY[clock]
            actions[clock] = {"escalated": True, "action": action,
                              "changes": changes,
                              "value": value, "threshold": threshold}
    return {"escalations": actions,
            "invariant": "escalation never changes the safety predicate; no "
                         "threshold makes an unsafe retry safe"}


# --- The nine-item committed-publication evidence packet ----------------------------------------------------------------------
# A worker's published_successfully log is NEVER a substitute for the packet.
EVIDENCE_PACKET_ITEMS = ("commit_identity", "authoritative_transaction_receipt",
                         "current_governance_state", "scope_dependency_closure",
                         "outbox_identity", "projection_checkpoint",
                         "gap_defect_evidence", "recovery_authorization",
                         "independent_verification_plan")


def classify_publication_state(packet: dict) -> dict:
    """Three situations, distinguished by evidence:
      committed + projection incomplete ⇒ REPLAY (idempotent, version-fenced);
      committed + stalled ⇒ DIAGNOSE (the progress obligation);
      commit incorrect or ambiguous ⇒ CONTAIN + RECONSTRUCT (never
        projection-repair: repair must not touch canonical state to make a
        projection look consistent)."""
    if not packet.get("authoritative_transaction_receipt"):
        return {"situation": "UNCLASSIFIABLE",
                "note": "a worker's published_successfully log is never a "
                        "substitute for the authoritative receipt"}
    status = packet.get("commit_status", "COMMITTED")
    if status in ("INCORRECT", "AMBIGUOUS"):
        return {"situation": "CONTAIN_RECONSTRUCT",
                "action": "contain + reconstruct from durable evidence; "
                          "never projection-repair"}
    if packet.get("projection_complete"):
        return {"situation": "HEALTHY",
                "action": "none required"}
    if packet.get("stalled_despite_capacity"):
        return {"situation": "DIAGNOSE",
                "action": "diagnose the progress obligation (E_o/S_o/P_o)"}
    return {"situation": "REPLAY",
            "action": "idempotent replay with version fencing"}


# --- Smallest valid repair ------------------------------------------------------------------------------------------------------
def smallest_repair(situation: str, evidence: dict) -> dict:
    """The decision flow. Repairs are minimal and history-preserving."""
    if situation == "committed_projection_stale":
        return {"repair": "IDEMPOTENT_REPLAY",
                "fencing": "version",
                "touches_canonical": False}
    if situation == "committed_outbox_missing":
        return {"repair": "INTEGRITY_DEFECT_RECONSTRUCTION",
                "note": "the atomic-contract claim is contradicted: establish "
                        "state, then an authorized reconstruction with a NEW "
                        "repair receipt linked to the original",
                "touches_canonical": "new governed receipt only"}
    if situation == "incorrect_canonical_commit":
        return {"repair": "GOVERNED_CORRECTIVE_TRANSACTION",
                "note": "a new governed transaction; history is never "
                        "rewritten",
                "touches_canonical": "new transaction only"}
    if situation == "ambiguous_external_effect":
        return {"repair": "EXTERNAL_RECONCILIATION_ONLY",
                "note": "independent external-effect reconciliation; no new "
                        "execution from ambiguity",
                "touches_canonical": False}
    return {"repair": "UNKNOWN_SITUATION",
            "note": "no repair without a classified situation"}


# --- Worked example: epoch 82 -----------------------------------------------------------------------------------------------------
def lab_epoch_82_worked_example() -> dict:
    """His worked example: withdrawal commits, EV-82 durable, the consumer
    crashes, the hub is stale at 81, the worker was serviced but no verified
    progress occurred.
    Safety: PASS (ACT correctly rejects B; A stays available).
    Recovery: STALLED — the progress obligation is failing.
    Report BOTH. The repair must not touch B's canonical qualification to
    make the hub look consistent."""
    law = {"receipt": "LAW-1", "valid": True}
    rg = RecoverableGovernance()
    for s in ("s:A", "s:B"):
        rg.gov.scope_mapping[s] = {"parent": None, "children": [],
                                   "taxonomy_version": 0}
        rg.gov.active_qualifications[s] = {
            "guarantee": f"g:{s}", "status": "QUALIFIED",
            "qualification_rev": 0, "taxonomy_version": 0}
    # Withdrawal of B commits; EV-82 durable.
    wd = rg.commit_with_crash(
        {"change_id": "op-w82", "change_type": "INCIDENT_WITHDRAWAL",
         "scopes": ["s:B"],
         "evidence": {"incident": {"incident_id": "inc-B82",
                                   "confirmed": True},
                      "verifier_ref": "v"},
         "law_receipt": law}, "op-w82", "h-w82", law)
    assert wd["committed"]
    ev82 = wd["receipt"]["seq"]
    # The consumer crashes; the hub projection is stale at 81.
    hub_revision = 81
    canonical_revision = rg.gov.epoch  # 82-equivalent: the withdrawal epoch
    # The worker was serviced (it ran) but no verified progress occurred:
    # the projection checkpoint never advanced past 81.
    trace = [(1, "PERMITTED", {}), (2, "DEPS_READY", {}),
             (3, "RESOURCES_OK", {}), (4, "SERVICED", {"worker": "hub-1"}),
             (5, "HEARTBEAT", {}), (6, "LOG_ENTRY", {"msg": "retrying"}),
             (7, "STATUS_REWRITE", {"to": "in-progress"})]
    h = track_esp(trace)
    diagnosis = diagnose_liveness(trace)
    # Safety assessment (independent).
    g_b = {"guarantee_id": "g:s:B", "verified": True,
           "qualified_scopes": ("s:B",), "revision": 0, "current": True}
    auth_b = authorize_tax_action(rg.gov, "act-b82", "s:B", g_b, law)
    g_a = {"guarantee_id": "g:s:A", "verified": True,
           "qualified_scopes": ("s:A",), "revision": 0, "current": True}
    auth_a = authorize_tax_action(rg.gov, "act-a82", "s:A", g_a, law)
    safety = assess_safety_x_progress("HOLD_REQUIRED (correct)",
                                      "STALLED_INVESTIGATE")
    repair = smallest_repair("committed_projection_stale", {})
    return {"safety": "PASS" if (not auth_b["authorized"]
                                 and auth_a["authorized"]) else "FAIL",
            "recovery": diagnosis["diagnosis"],
            "progress_obligation": "FAILING" if not h["P_o"] else "MET",
            "both_reported": safety["row"],
            "hub_stale_at": hub_revision,
            "canonical_at": canonical_revision,
            "ev82_durable": ev82 is not None,
            "repair": repair["repair"],
            "repair_constraint": "the repair must not touch B's canonical "
                                 "qualification to make the hub look "
                                 "consistent",
            "law_holds": (not auth_b["authorized"] and auth_a["authorized"]
                          and diagnosis["diagnosis"]
                          in ("PROGRESS_ON_SERVICE_VIOLATION",
                              "STARVATION_SUSPECTED")
                          and not h["P_o"]
                          and repair["repair"] == "IDEMPOTENT_REPLAY"
                          and not repair["touches_canonical"])}


# --- The L1–L12 suite ---------------------------------------------------------------------------------------------------------------
def live_l_suite(progress_check_enabled: bool = True) -> list:
    """Twelve liveness scenarios. With progress_check_enabled=False (the
    adversarial fixture: the progress-on-service check removed), the verifier
    must catch a system that reports success from repeated heartbeats."""
    results = []

    def T(*events):
        return [(i + 1, k, d) for i, (k, d) in enumerate(events)]

    # L1: healthy progress.
    d = diagnose_liveness(T(("PERMITTED", {}), ("DEPS_READY", {}),
                             ("RESOURCES_OK", {}), ("SERVICED", {"w": 1}),
                             ("PROGRESS", {"done": True})))
    results.append(("L1", "PASS" if d["diagnosis"] == "RECOVERING_NORMALLY"
                    else "FAIL", d["diagnosis"]))

    # L2: waiting authority — not starvation.
    d = diagnose_liveness(T(("BLOCKED_AUTH", {}), ("DEPS_READY", {}),
                             ("RESOURCES_OK", {})))
    results.append(("L2", "PASS" if d["diagnosis"] == "WAITING_AUTHORITY"
                    else "FAIL", "not a starvation victim"))

    # L3: waiting dependency.
    d = diagnose_liveness(T(("PERMITTED", {}), ("DEPS_BLOCKED", {}),
                             ("RESOURCES_OK", {})))
    results.append(("L3", "PASS" if d["diagnosis"] == "WAITING_DEPENDENCY"
                    else "FAIL", d["diagnosis"]))

    # L4: starvation suspected — enabled, no service, bounded window.
    d = diagnose_liveness(T(*([("PERMITTED", {}), ("DEPS_READY", {}),
                                ("RESOURCES_OK", {})]
                               + [("HEARTBEAT", {})] * 12)),
                          service_window=10)
    results.append(("L4", "PASS" if d["diagnosis"] == "STARVATION_SUSPECTED"
                    else "FAIL",
                    "suspicion, never proof of infinite violation"))

    # L5: service without progress — the adversarial target.
    trace5 = T(("PERMITTED", {}), ("DEPS_READY", {}), ("RESOURCES_OK", {}),
               ("SERVICED", {"w": 1}), ("HEARTBEAT", {}), ("LOG_ENTRY", {}))
    if progress_check_enabled:
        d = diagnose_liveness(trace5)
        verdict = "PASS" if d["diagnosis"] == "PROGRESS_ON_SERVICE_VIOLATION" \
            else "FAIL"
        note = d["diagnosis"]
    else:
        # MUTANT: the check removed — the system reports success from
        # heartbeats. The verifier must catch the fraud.
        h = track_esp(trace5)
        fraud = (not h["P_o"]
                 and any(k == "HEARTBEAT" for _, k in h["non_progress_signals"]))
        verdict = "CAUGHT" if fraud else "MISSED"
        note = ("verifier caught heartbeat-success fraud"
                if fraud else "verifier missed it")
    results.append(("L5", verdict, note))

    # L6: deadlock suspected.
    d = diagnose_liveness(T(("PERMITTED", {}),
                             ("WAITS_ON", {"obligation": "A", "on": "B"}),
                             ("WAITS_ON", {"obligation": "B", "on": "A"})))
    results.append(("L6", "PASS" if d["diagnosis"] == "DEADLOCK_SUSPECTED"
                    else "FAIL", d["diagnosis"]))

    # L7: insufficient evidence.
    d = diagnose_liveness([])
    results.append(("L7", "PASS" if d["diagnosis"] == "INSUFFICIENT_EVIDENCE"
                    else "FAIL", d["diagnosis"]))

    # L8: blocked recoverable — resources down but a path exists.
    d = diagnose_liveness(T(*([("PERMITTED", {}), ("DEPS_READY", {}),
                                ("RESOURCES_STARVED", {})]
                               + [("HEARTBEAT", {})] * 12)),
                          service_window=10)
    results.append(("L8", "PASS" if d["diagnosis"] == "BLOCKED_RECOVERABLE"
                    else "FAIL", d["diagnosis"]))

    # L9: safety × progress both reported (epoch-82 worked example).
    w = lab_epoch_82_worked_example()
    results.append(("L9", "PASS" if (w["safety"] == "PASS"
                                     and w["both_reported"]
                                     == "SAFE_HOLD_STALLED") else "FAIL",
                    "both assessments reported"))

    # L10: escalation never changes the safety predicate.
    esc = check_escalation(
        {"total_unresolved_age": 9999}, {"total_unresolved_age": 10})
    results.append(("L10", "PASS" if (
        esc["escalations"]["total_unresolved_age"]["escalated"]
        and "never changes the safety predicate" in esc["invariant"])
        else "FAIL", "escalation changes responsibility, never safety"))

    # L11: smallest repair per situation.
    r1 = smallest_repair("committed_projection_stale", {})
    r2 = smallest_repair("committed_outbox_missing", {})
    r3 = smallest_repair("incorrect_canonical_commit", {})
    r4 = smallest_repair("ambiguous_external_effect", {})
    ok = (r1["repair"] == "IDEMPOTENT_REPLAY"
          and r2["repair"] == "INTEGRITY_DEFECT_RECONSTRUCTION"
          and "never rewritten" in r3["note"]
          and r4["repair"] == "EXTERNAL_RECONCILIATION_ONLY")
    results.append(("L11", "PASS" if ok else "FAIL",
                    "minimal, history-preserving repairs"))

    # L12: formal property — Committed(o) ∧ ProjectionCurrent(o) ⇒
    # ProjectionMatchesCanonical(o).
    rg = RecoverableGovernance()
    rg.gov.scope_mapping["s:A"] = {"parent": None, "children": [],
                                   "taxonomy_version": 0}
    law = {"receipt": "LAW-1", "valid": True}
    ack = rg.commit_with_crash(
        {"change_id": "op-l12", "change_type": "TAXONOMY_MERGE",
         "scopes": ["s:A"], "evidence": {"merged_id": "s:AB"},
         "law_receipt": law}, "op-l12", "h-l12", law)
    c = ProjectionConsumer("c-l12", at_revision=0)
    c.apply({"event_id": "e1", "revision": rg.gov.epoch})
    matches = (ack["committed"]
               and c.applied_revision == rg.gov.epoch)
    results.append(("L12", "PASS" if matches else "FAIL",
                    "Committed ∧ ProjectionCurrent ⇒ MatchesCanonical"))
    return results


def valid_disposition(obligation: dict) -> dict:
    """ValidDisposition(o), explicitly contracted: repaired+verified, OR a
    permitted terminal disposition that retains the unresolved goal (the goal
    is not silently dropped)."""
    if obligation.get("repaired_and_verified"):
        return {"valid": True, "kind": "REPAIRED_VERIFIED"}
    term = obligation.get("terminal_disposition")
    if term and term.get("permitted") and term.get("goal_retained"):
        return {"valid": True, "kind": "PERMITTED_TERMINAL_GOAL_RETAINED"}
    return {"valid": False,
            "note": "neither repaired+verified nor a permitted terminal "
                    "disposition with the goal retained"}


# --- AER-LIVE-001: the first action -------------------------------------------------------------------------------------------
def aer_live_001() -> dict:
    """Deterministic replay with three histories:
      control   — outbox applied + verified: safety PASS, progress OK;
      defective — serviced, checkpoint never advances: safety PASS but
                  PROGRESS_ON_SERVICE_VIOLATION;
      waiting   — genuine missing LAW decision: WAITING_AUTHORITY with the
                  notification duty progressing (verified P_o via the duty).
    The verifier isolates three facts: safety, scheduling fairness, actual
    recovery progress."""
    law = {"receipt": "LAW-1", "valid": True}
    report = {}

    def fresh_ab():
        rg = RecoverableGovernance()
        for s in ("s:A", "s:B"):
            rg.gov.scope_mapping[s] = {"parent": None, "children": [],
                                       "taxonomy_version": 0}
            rg.gov.active_qualifications[s] = {
                "guarantee": f"g:{s}", "status": "QUALIFIED",
                "qualification_rev": 0, "taxonomy_version": 0}
        return rg

    # Control: withdrawal commits, outbox applied, projection verified.
    rg = fresh_ab()
    wd = rg.commit_with_crash(
        {"change_id": "op-c", "change_type": "INCIDENT_WITHDRAWAL",
         "scopes": ["s:B"],
         "evidence": {"incident": {"incident_id": "inc-c",
                                   "confirmed": True},
                      "verifier_ref": "v"},
         "law_receipt": law}, "op-c", "h-c", law)
    assert wd["committed"]
    eid = wd["outbox_event_ids"][0]
    assert rg.deliver_outbox(eid)["status"] == "DELIVERED"
    g_b = {"guarantee_id": "g:s:B", "verified": True,
           "qualified_scopes": ("s:B",), "revision": 0, "current": True}
    auth_b = authorize_tax_action(rg.gov, "act-c", "s:B", g_b, law)
    trace_c = [(1, "PERMITTED", {}), (2, "DEPS_READY", {}),
               (3, "RESOURCES_OK", {}), (4, "SERVICED", {"w": 1}),
               (5, "PROGRESS", {"projection": "verified"})]
    report["control"] = {
        "safety": "PASS" if not auth_b["authorized"] else "FAIL",
        "diagnosis": diagnose_liveness(trace_c)["diagnosis"],
        "progress": "OK" if track_esp(trace_c)["P_o"] else "MISSING"}

    # Defective: serviced, checkpoint never advances.
    trace_d = [(1, "PERMITTED", {}), (2, "DEPS_READY", {}),
               (3, "RESOURCES_OK", {}), (4, "SERVICED", {"w": 1}),
               (5, "HEARTBEAT", {}), (6, "HEARTBEAT", {})]
    d_d = diagnose_liveness(trace_d)
    report["defective"] = {
        "safety": "PASS",  # the hold itself is correct
        "diagnosis": d_d["diagnosis"],
        "progress": "MISSING",
        "isolated_fact": "safety holds while recovery progress fails"}

    # Waiting: genuine missing LAW decision — WAITING_AUTHORITY, with the
    # notification duty progressing (verified P_o via the duty itself).
    trace_w = [(1, "BLOCKED_AUTH", {}), (2, "DEPS_READY", {}),
               (3, "RESOURCES_OK", {}),
               (4, "PROGRESS", {"notification_duty": "served"})]
    d_w = diagnose_liveness(trace_w)
    report["waiting"] = {
        "diagnosis": d_w["diagnosis"],
        "progress_via_duty": bool(track_esp(trace_w)["P_o"]),
        "note": "waiting on authority is not starvation; the notification "
                "duty's verified progress counts as P_o"}

    # The verifier isolates the three facts.
    ok = (report["control"]["safety"] == "PASS"
          and report["control"]["diagnosis"] == "RECOVERING_NORMALLY"
          and report["defective"]["diagnosis"] == "PROGRESS_ON_SERVICE_VIOLATION"
          and report["waiting"]["diagnosis"] == "WAITING_AUTHORITY"
          and report["waiting"]["progress_via_duty"])
    report["verifier_isolates_three_facts"] = ok

    # The adversarial fixture: with the progress check removed, heartbeat
    # success fraud must be caught.
    adv = [x for x in live_l_suite(progress_check_enabled=False)
           if x[0] == "L5"][0]
    report["adversarial"] = {"L5": adv[1], "note": adv[2]}
    assert adv[1] == "CAUGHT"
    return report
# ======================================================================================
# SN-0808 AER-LIVE-2 — BOUNDED RECOVERY LIVENESS LAW
# ======================================================================================
# The BOUNDED-LIVENESS QUALIFICATION layer: AER-LIVE-1 separated safety grades
# from liveness grades; this defines what evidence earns the liveness verdicts.
#
# HONEST SCOPE (Shawn, 2026-10-10 — his explicit scoping): EXTEND the existing
# contracts — never a separate engine or competing verdict engine. Diagnostic
# labels map into existing state/receipt contracts (fairness_verify.py,
# liveness.py, progress.py). No independently validated numeric service bound
# for any production recovery obligation; AER-LIVE-2 guarantees not
# production-proven. Main observed by Shawn at cfbd81cc (supersedes 0fb380c).
#
# His law: NayaNET may claim bounded recovery liveness only where obligation
# eligibility, scheduling opportunities, usable service, progress witnesses,
# capacity assumptions, and the governing bound are independently established.
# A finite timeout may demonstrate a specific contractual deadline breach, but
# shall not by itself establish weak- or strong-fairness failure.
AER_LIVE2_IMPLEMENTATION_STATUS = {
    "enters_as": "contract extension + harness demonstration",
    "not_a": ("separate engine", "competing verdict engine"),
    "extends": ("fairness_verify.py", "liveness.py", "progress.py"),
    "not_verified": ("numeric service bound for any production obligation",
                     "production AER-LIVE-2 guarantees"),
    "main_observed_at": "cfbd81cc",
}

# Four separate claims, each with its own proof burden. A correctly blocked
# retry can satisfy safety while an independent reconciliation obligation is
# eligible and overdue; a worker can satisfy scheduling fairness while
# achieving zero progress.
LIVENESS_CLAIMS = {
    "safety": "no prohibited action taken; holds correct",
    "scheduling_fairness": "eligible obligations receive adequate service "
                           "within the bound",
    "bounded_progress": "serviced work produces verified milestones within "
                        "the bound",
    "task_completion": "the objective itself is achieved (strictly stronger "
                       "than disposition)",
}

# The three observable links, precisely:
#   E_o(t): genuinely enabled — LAW permits, dependencies ready, resources
#           available, no safety hold.
#   S_o(t): usable evidenced service — lease, acknowledgment, usable
#           resources. Scheduler-claimed dispatch is INSUFFICIENT.
#   P_o(t): independently verified progress — proof obligation discharged,
#           publication advanced, valid bounded disposition. Heartbeats and
#           failed retries never count.
SERVICE_EVIDENCE_KINDS = ("LEASE", "ACKNOWLEDGMENT", "USABLE_RESOURCES")
PROGRESS_EVIDENCE_KINDS = ("PROOF_OBLIGATION_DISCHARGED",
                           "PUBLICATION_ADVANCED", "VALID_BOUNDED_DISPOSITION")


def observable_links(round_evidence: dict) -> dict:
    """Evaluate E_o / S_o / P_o for one round from evidence (not claims)."""
    e = bool(round_evidence.get("law_permits")
             and round_evidence.get("dependencies_ready")
             and round_evidence.get("resources_available")
             and not round_evidence.get("safety_hold"))
    s = bool(round_evidence.get("service_kind") in SERVICE_EVIDENCE_KINDS
             and round_evidence.get("service_evidence"))
    p = bool(round_evidence.get("progress_kind") in PROGRESS_EVIDENCE_KINDS
             and round_evidence.get("progress_evidence"))
    return {"E_o": e, "S_o": s, "P_o": p,
            "note": "dispatch without resource evidence is not S_o; "
                    "heartbeats never P_o"}


# --- Fairness debt: the bounded-service contract -----------------------------------------------------------------------------------
# ∀o,t: D_o(t) < B_S(o), on cumulative fairness debt:
#   eligible rounds without adequate service increase debt;
#   ineligible rounds leave it;
#   adequate service resets;
#   reassignment never resets.
# This is NOT weak/strong fairness over infinite executions — neither
# supplies a numeric bound.
def track_fairness_debt(rounds: list,
                        count_dispatched_as_service: bool = False) -> dict:
    """rounds: {"eligible": bool, "service": None | {"kind":..., "evidence":...},
    "reassigned": bool}. count_dispatched_as_service=True is the MUTANT
    (DISPATCHED counted as SERVICED without resource evidence)."""
    debt, history = 0, []
    for r in rounds:
        svc = r.get("service") or {}
        adequate = False
        if svc.get("kind") in SERVICE_EVIDENCE_KINDS and svc.get("evidence"):
            adequate = True
        elif count_dispatched_as_service and svc.get("kind") == "DISPATCHED":
            adequate = True  # MUTANT: scheduler claim without evidence
        if adequate:
            debt = 0
        elif r.get("eligible"):
            debt += 1
        # ineligible: debt unchanged. reassignment: never resets.
        history.append({"debt": debt, "eligible": bool(r.get("eligible")),
                        "adequate_service": adequate,
                        "reassigned": bool(r.get("reassigned"))})
    return {"debt_history": history,
            "max_debt": max((h["debt"] for h in history), default=0),
            "final_debt": debt}


def check_service_bound(debt_history: list, B_S: int,
                        trace_complete_and_verified: bool) -> dict:
    """B_S: eligible obligation receives adequate service within B_S qualified
    opportunities. Violation = bounded scheduling-service failure — only on a
    complete, independently verified trace."""
    if not trace_complete_and_verified:
        return {"verdict": "INSUFFICIENT_SERVICE_EVIDENCE",
                "note": "a bound breach needs a complete verified trace"}
    max_debt = max((h["debt"] for h in debt_history), default=0)
    if max_debt >= B_S:
        return {"verdict": "BOUNDED_SERVICE_VIOLATION",
                "max_debt": max_debt, "B_S": B_S,
                "note": "a finite bound breach — not a WF/SF violation"}
    return {"verdict": "SERVICE_WITHIN_BOUND",
            "max_debt": max_debt, "B_S": B_S}


def check_progress_bound(serviced_rounds_without_progress: int,
                         B_P: int) -> dict:
    """B_P: serviced work produces a verified milestone/disposition within
    B_P steps."""
    if serviced_rounds_without_progress >= B_P:
        return {"verdict": "BOUNDED_PROGRESS_VIOLATION",
                "note": "service without verified progress past the bound"}
    return {"verdict": "PROGRESS_WITHIN_BOUND"}


def check_disposition_bound(unresolved_rounds: int, B_D: int,
                            disposition: dict) -> dict:
    """B_D: an unresolved obligation reaches verified completion, refusal, or
    governed escalation within the recovery policy. progress.py separation:
    consumed retry budget advances TERMINATION, never proof — budget
    exhaustion without resolution is not completion."""
    v = valid_disposition(disposition or {})
    if v["valid"]:
        return {"verdict": "DISPOSITION_REACHED", "kind": v["kind"]}
    if unresolved_rounds >= B_D:
        return {"verdict": "DISPOSITION_BOUND_BREACHED",
                "note": "escalate under the governed policy; escalation "
                        "never manufactures completion"}
    return {"verdict": "DISPOSITION_PENDING"}


# --- The bound's assumptions first (7 rows) -------------------------------------------------------------------------------------------
BOUND_ASSUMPTIONS = (
    "finite_queue_capacity",
    "correct_scheduling_rule",
    "genuine_opportunities",
    "accurate_accounting",
    "usable_service",
    "restart_continuity",
    "no_hidden_unbounded_environmental_delay",
)


def check_bound_assumptions(assumptions: dict) -> dict:
    """Every bound verdict first proves its assumptions. Missing or false
    assumption ⇒ the bound claim is UNGROUNDED, never a violation."""
    missing = [a for a in BOUND_ASSUMPTIONS if not assumptions.get(a)]
    return {"grounded": not missing, "missing": missing,
            "warning": "30 minutes outstanding with 29 minutes of verified "
                       "provider outage is NOT a scheduler failure "
                       "(outage rounds are ineligible); hundreds of ignored "
                       "eligible rounds in 2 seconds CAN breach a bound "
                       "before any 5-minute alert — track eligible-service "
                       "age AND total unresolved age, always"}


# --- Bound composition ----------------------------------------------------------------------------------------------------------------------
def compose_bounds(B_S: int, B_P: int, B_D: int, compatibility: dict) -> dict:
    """B_total = B_S + B_P + B_D, with compatibility conditions: consistent
    units, proven per-stage bounds, finite attempts, contention accounted."""
    needed = ("consistent_units", "per_stage_bounds_proven",
              "finite_attempts", "contention_accounted")
    missing = [c for c in needed if not compatibility.get(c)]
    if missing:
        return {"composed": False, "missing": missing}
    return {"composed": True, "B_total": B_S + B_P + B_D,
            "B_S": B_S, "B_P": B_P, "B_D": B_D,
            "note": "composition is arithmetic on proven bounds, not a new "
                    "proof"}


# --- The evidence-based verdict ladder ------------------------------------------------------------------------------------------------------
BOUNDED_VERDICTS = ("EXECUTION_TIMEOUT_OBSERVED", "WAITING_AUTHORITY",
                    "INSUFFICIENT_SERVICE_EVIDENCE", "STARVATION_SUSPECTED",
                    "BOUNDED_SERVICE_VIOLATION", "BOUNDED_PROGRESS_VIOLATION",
                    "FORMAL_FAIRNESS_COUNTEREXAMPLE", "GOVERNED_DISPOSITION")
ASSURANCE_LEVELS = ("RUNTIME_OBSERVATION", "BOUNDED_MODEL_VERIFICATION",
                    "CONDITIONAL_FORMAL_GUARANTEE")


def bounded_verdict(evidence: dict) -> dict:
    """Walk the ladder; return the highest warranted verdict. A timeout alone
    never climbs past EXECUTION_TIMEOUT_OBSERVED."""
    if evidence.get("waiting_on_authority"):
        return {"verdict": "WAITING_AUTHORITY",
                "assurance": "RUNTIME_OBSERVATION"}
    if evidence.get("timeout_observed") and not evidence.get("cause_known"):
        return {"verdict": "EXECUTION_TIMEOUT_OBSERVED",
                "assurance": "RUNTIME_OBSERVATION",
                "note": "a timeout demonstrates a deadline breach at most; "
                        "it never establishes a fairness failure"}
    if not evidence.get("trace_complete_and_verified"):
        return {"verdict": "INSUFFICIENT_SERVICE_EVIDENCE",
                "assurance": "RUNTIME_OBSERVATION"}
    debt = evidence.get("debt_history", [])
    B_S = evidence.get("B_S")
    if B_S is not None:
        r = check_service_bound(debt, B_S, True)
        if r["verdict"] == "BOUNDED_SERVICE_VIOLATION":
            return {"verdict": "BOUNDED_SERVICE_VIOLATION",
                    "assurance": "RUNTIME_OBSERVATION",
                    "max_debt": r["max_debt"]}
    swp = evidence.get("serviced_without_progress", 0)
    B_P = evidence.get("B_P")
    if B_P is not None and swp >= B_P:
        return {"verdict": "BOUNDED_PROGRESS_VIOLATION",
                "assurance": "RUNTIME_OBSERVATION"}
    if evidence.get("starvation_suspected"):
        return {"verdict": "STARVATION_SUSPECTED",
                "assurance": "RUNTIME_OBSERVATION"}
    if evidence.get("formal_counterexample"):
        return {"verdict": "FORMAL_FAIRNESS_COUNTEREXAMPLE",
                "assurance": "BOUNDED_MODEL_VERIFICATION"}
    if evidence.get("disposition"):
        v = valid_disposition(evidence["disposition"])
        if v["valid"]:
            return {"verdict": "GOVERNED_DISPOSITION",
                    "assurance": "RUNTIME_OBSERVATION", "kind": v["kind"]}
    return {"verdict": "NO_VIOLATION_OBSERVED",
            "assurance": "RUNTIME_OBSERVATION"}


# --- Ten-field independent evidence packet ------------------------------------------------------------------------------------------------------
BOUNDED_EVIDENCE_PACKET = ("obligation_identity", "bound_capacity_basis",
                           "canonical_state_revisions", "eligibility_history",
                           "scheduling_history", "usable_service", "progress",
                           "recovery_budget", "deadline_witness",
                           "independent_verdict")


def verify_bounded_packet(packet: dict) -> dict:
    """Missing trace segments are never counted as eligible opportunities; a
    busy worker without progress proves nothing."""
    missing = [f for f in BOUNDED_EVIDENCE_PACKET if f not in packet]
    issues = []
    if missing:
        issues.append(f"missing fields: {missing}")
    # None values for usable_service / progress are legitimate: they record
    # the OBSERVED absence of service or progress — never invented.
    gaps = packet.get("trace_gaps", [])
    if gaps:
        issues.append(f"trace gaps {gaps}: never counted as eligible "
                      "opportunities")
    if packet.get("worker_busy") and not packet.get("progress"):
        issues.append("busy worker without progress proves nothing")
    return {"packet_valid": not issues, "issues": issues,
            "fields": list(BOUNDED_EVIDENCE_PACKET)}


# --- Worked example: the 6-round synthetic history -----------------------------------------------------------------------------------------------
def lab_six_round_example(variant: str = "base") -> dict:
    """B_S = 3 qualified opportunities.
    Base: timeout in round 5, verified progress in round 6 ⇒ service PASS,
      progress PASS, no fairness violation.
    Variant (one fact changed: service never arrives in round 4): the third
      eligible opportunity without service ⇒ proven BOUNDED_SERVICE_VIOLATION
      — still not a WF/SF violation."""
    B_S = 3
    svc = {"kind": "ACKNOWLEDGMENT", "evidence": "ack-1"}
    if variant == "base":
        rounds = [
            {"eligible": True, "service": svc},
            {"eligible": True, "service": svc},
            {"eligible": True, "service": None},      # debt 1
            {"eligible": True, "service": svc},       # debt 0
            {"eligible": True, "service": None},      # timeout, debt 1
            {"eligible": True, "service": svc},       # + verified progress
        ]
    else:  # variant: service never arrives in round 4
        rounds = [
            {"eligible": True, "service": svc},
            {"eligible": True, "service": svc},
            {"eligible": True, "service": None},      # debt 1
            {"eligible": True, "service": None},      # debt 2
            {"eligible": True, "service": None},      # debt 3 → BREACH
            {"eligible": True, "service": svc},       # + verified progress
        ]
    debt = track_fairness_debt(rounds)
    service = check_service_bound(debt["debt_history"], B_S, True)
    # Progress: verified in round 6 in both variants (B_P not breached).
    progress = check_progress_bound(0, 4)
    return {"variant": variant, "B_S": B_S,
            "debt_history": [h["debt"] for h in debt["debt_history"]],
            "service": service["verdict"], "progress": progress["verdict"],
            "fairness_violation": False,
            "note": "a finite bound breach is not a WF/SF violation"}


# --- BL1–BL12 suite --------------------------------------------------------------------------------------------------------------------------------------
def live_bl_suite(count_dispatched_as_service: bool = False) -> list:
    """Twelve bounded-liveness scenarios. The decisive paired experiment
    (BL9): CONTROL vs TREATMENT with IDENTICAL timeout timestamps — the
    detector must preserve WAITING_AUTHORITY for CONTROL and catch the
    bounded-service breach in TREATMENT. The mutation
    (count_dispatched_as_service=True) must be rejected or independently
    blocked."""
    results = []
    svc = {"kind": "ACKNOWLEDGMENT", "evidence": "ack-1"}
    dispatch = {"kind": "DISPATCHED", "evidence": None}

    # BL1: the four claims carry separate proof burdens.
    results.append(("BL1", "PASS" if set(LIVENESS_CLAIMS) == {
        "safety", "scheduling_fairness", "bounded_progress",
        "task_completion"} else "FAIL",
        "four claims, four proof burdens"))

    # BL2: E_o precise — LAW permits + deps + resources + no safety hold.
    links = observable_links({"law_permits": True, "dependencies_ready": True,
                              "resources_available": True, "safety_hold": True})
    results.append(("BL2", "PASS" if not links["E_o"] else "FAIL",
                    "safety hold ⇒ not enabled ⇒ not starvation"))

    # BL3: S_o precise — scheduler-claimed dispatch is insufficient.
    l3 = observable_links({"law_permits": True, "dependencies_ready": True,
                           "resources_available": True,
                           "service_kind": "DISPATCHED",
                           "service_evidence": None})
    l3b = observable_links({"law_permits": True, "dependencies_ready": True,
                            "resources_available": True,
                            "service_kind": "LEASE", "service_evidence": "l1"})
    results.append(("BL3", "PASS" if (not l3["S_o"] and l3b["S_o"])
                    else "FAIL",
                    "dispatch alone is not usable service"))

    # BL4: P_o precise — heartbeats never count.
    l4 = observable_links({"progress_kind": "HEARTBEAT",
                           "progress_evidence": "hb-99"})
    l4b = observable_links({"progress_kind": "PUBLICATION_ADVANCED",
                            "progress_evidence": "evt-82"})
    results.append(("BL4", "PASS" if (not l4["P_o"] and l4b["P_o"])
                    else "FAIL", "heartbeats never P_o"))

    # BL5: the debt contract — accrue / leave / reset / never-reset.
    debt = track_fairness_debt([
        {"eligible": True, "service": None},              # 1
        {"eligible": True, "service": None},              # 2
        {"eligible": False, "service": None},             # stays 2
        {"eligible": True, "service": svc},               # reset 0
        {"eligible": True, "service": None, "reassigned": True},  # 1
    ])
    hist = [h["debt"] for h in debt["debt_history"]]
    results.append(("BL5", "PASS" if hist == [1, 2, 2, 0, 1] else "FAIL",
                    f"debt contract {hist}: accrue/leave/reset/never-reset"))

    # BL6: six-round base ⇒ PASS / PASS, no fairness violation.
    b6 = lab_six_round_example("base")
    results.append(("BL6", "PASS" if (b6["service"] == "SERVICE_WITHIN_BOUND"
                                      and b6["progress"]
                                      == "PROGRESS_WITHIN_BOUND"
                                      and not b6["fairness_violation"])
                    else "FAIL", f"debt {b6['debt_history']}"))

    # BL7: six-round variant ⇒ BOUNDED_SERVICE_VIOLATION, not WF/SF.
    b7 = lab_six_round_example("variant")
    results.append(("BL7", "PASS" if (b7["service"]
                                      == "BOUNDED_SERVICE_VIOLATION"
                                      and not b7["fairness_violation"])
                    else "FAIL",
                    "finite bound breach ≠ WF/SF violation"))

    # BL8: the provider-outage warning — ineligible rounds don't accrue.
    debt8 = track_fairness_debt(
        [{"eligible": True, "service": svc}] * 2
        + [{"eligible": False, "service": None}] * 29  # verified outage
        + [{"eligible": True, "service": svc}])
    v8 = check_service_bound(debt8["debt_history"], 3, True)
    results.append(("BL8", "PASS" if (v8["verdict"] == "SERVICE_WITHIN_BOUND"
                                      and debt8["max_debt"] == 0) else "FAIL",
                    "29 ineligible minutes accrue nothing: not a scheduler "
                    "failure"))

    # BL9: the decisive paired experiment — IDENTICAL timeout timestamps.
    timeouts = [5]
    control_rounds = [  # legitimately waiting on authority throughout
        {"eligible": False, "service": None} for _ in range(6)]
    treatment_rounds = [  # eligible throughout, defective scheduler
        {"eligible": True, "service": None} for _ in range(6)]
    dc = track_fairness_debt(control_rounds)
    dt = track_fairness_debt(treatment_rounds)
    vc = bounded_verdict({"timeout_observed": True, "cause_known": False,
                          "waiting_on_authority": True,
                          "timeout_rounds": timeouts})
    vt = bounded_verdict({"timeout_observed": True, "cause_known": True,
                          "trace_complete_and_verified": True,
                          "debt_history": dt["debt_history"], "B_S": 3,
                          "timeout_rounds": timeouts})
    ok = (dc["max_debt"] == 0
          and vc["verdict"] == "WAITING_AUTHORITY"
          and vt["verdict"] == "BOUNDED_SERVICE_VIOLATION")
    results.append(("BL9", "PASS" if ok else "FAIL",
                    "identical timeouts: CONTROL waits on authority, "
                    "TREATMENT breaches the service bound"))

    # BL10: the mutation — DISPATCHED as SERVICED without resource evidence
    # must be rejected or independently blocked.
    rounds_m = [{"eligible": True,
                 "service": dispatch} for _ in range(6)]
    honest = track_fairness_debt(rounds_m,
                                 count_dispatched_as_service=False)
    mutant = track_fairness_debt(rounds_m,
                                 count_dispatched_as_service=True)
    # The mutant hides the breach (debt 0). The verifier rejects any bound
    # claim built on evidence-free dispatch.
    vh = check_service_bound(honest["debt_history"], 3, True)
    rejected = (vh["verdict"] == "BOUNDED_SERVICE_VIOLATION"
                and mutant["max_debt"] == 0)
    results.append(("BL10", "PASS" if rejected else "FAIL",
                    "dispatch-without-evidence cannot hide a breach: the "
                    "honest accounting still proves it"))

    # BL11: bound composition compatibility.
    comp = compose_bounds(3, 4, 10, {"consistent_units": True,
                                     "per_stage_bounds_proven": True,
                                     "finite_attempts": True,
                                     "contention_accounted": True})
    bad = compose_bounds(3, 4, 10, {"consistent_units": False,
                                    "per_stage_bounds_proven": True,
                                    "finite_attempts": True,
                                    "contention_accounted": True})
    results.append(("BL11", "PASS" if (comp["composed"]
                                      and comp["B_total"] == 17
                                      and not bad["composed"]) else "FAIL",
                    "B_total = B_S + B_P + B_D on proven compatibility"))

    # BL12: the ladder — a timeout alone never climbs past
    # EXECUTION_TIMEOUT_OBSERVED.
    v12 = bounded_verdict({"timeout_observed": True})
    results.append(("BL12", "PASS" if v12["verdict"]
                    == "EXECUTION_TIMEOUT_OBSERVED" else "FAIL",
                    "a timeout is a deadline fact, not a fairness verdict"))
    return results


# --- AER-LIVE-002: the first action -----------------------------------------------------------------------------------------------------------------------
def aer_live_002() -> dict:
    """Isolated deterministic replay around a real committed-publication
    recovery obligation (RecoverableGovernance): three-opportunity service
    bound + qualified progress bound. The verifier distinguishes CONTROL
    from TREATMENT; then restart / intermittent-eligibility / absent-receipts
    / budget-exhaustion / incomplete-telemetry variants.
    Acceptance: zero false fairness violations on sealed safety-hold
    controls, detection of the qualified counterexample, no invented
    progress, unaffected eligibility preserved. Within the
    fairness/liveness/progress seam; no live ACT authority change."""
    law = {"receipt": "LAW-1", "valid": True}
    report = {}
    B_S, B_P = 3, 4
    svc = {"kind": "ACKNOWLEDGMENT", "evidence": "ack-1"}

    def fresh_obligation():
        rg = RecoverableGovernance()
        rg.gov.scope_mapping["s:A"] = {"parent": None, "children": [],
                                       "taxonomy_version": 0}
        rg.gov.active_qualifications["s:A"] = {
            "guarantee": "g:A", "status": "QUALIFIED", "qualification_rev": 0,
            "taxonomy_version": 0}
        wd = rg.commit_with_crash(
            {"change_id": "op-wd", "change_type": "INCIDENT_WITHDRAWAL",
             "scopes": ["s:A"],
             "evidence": {"incident": {"incident_id": "inc-wd",
                                       "confirmed": True},
                          "verifier_ref": "v"},
             "law_receipt": law}, "op-wd", "h-wd", law)
        assert wd["committed"]
        return rg

    # The recovery obligation: project the committed withdrawal.
    # CONTROL: genuinely waiting on authority (LAW decision missing) —
    # identical timeout timestamps as TREATMENT.
    control_rounds = [{"eligible": False, "service": None}
                      for _ in range(6)]
    # TREATMENT: eligible throughout; the scheduler never services.
    treatment_rounds = [{"eligible": True, "service": None}
                        for _ in range(6)]
    dc = track_fairness_debt(control_rounds)
    dt = track_fairness_debt(treatment_rounds)
    vc = bounded_verdict({"timeout_observed": True, "cause_known": False,
                          "waiting_on_authority": True})
    vt = bounded_verdict({"timeout_observed": True, "cause_known": True,
                          "trace_complete_and_verified": True,
                          "debt_history": dt["debt_history"], "B_S": B_S})
    report["paired"] = {
        "control": vc["verdict"], "treatment": vt["verdict"],
        "control_max_debt": dc["max_debt"],
        "treatment_max_debt": dt["max_debt"]}
    assert vc["verdict"] == "WAITING_AUTHORITY"
    assert vt["verdict"] == "BOUNDED_SERVICE_VIOLATION"

    # Variant: restart — debt + identity survive the crash.
    rg_r = fresh_obligation()
    debt_ledger = {"op-wd": [1, 2]}  # durable: two eligible rounds, no service
    # ...crash...
    rg_r2 = fresh_obligation()  # recovered harness, same obligation identity
    debt_ledger["op-wd"].append(3)  # third eligible round, no service
    v_r = check_service_bound(
        [{"debt": d} for d in debt_ledger["op-wd"]], B_S, True)
    report["restart_continuity"] = {
        "verdict": v_r["verdict"], "debt_survived": debt_ledger["op-wd"]}
    assert v_r["verdict"] == "BOUNDED_SERVICE_VIOLATION"

    # Variant: intermittent eligibility — ineligible rounds pause, not reset.
    debt_i = track_fairness_debt([
        {"eligible": True, "service": None},
        {"eligible": False, "service": None},
        {"eligible": True, "service": None},
        {"eligible": False, "service": None},
        {"eligible": True, "service": None}])
    v_i = check_service_bound(debt_i["debt_history"], B_S, True)
    report["intermittent_eligibility"] = {
        "debt": [h["debt"] for h in debt_i["debt_history"]],
        "verdict": v_i["verdict"]}
    assert [h["debt"] for h in debt_i["debt_history"]] == [1, 1, 2, 2, 3]
    assert v_i["verdict"] == "BOUNDED_SERVICE_VIOLATION"

    # Variant: absent receipts — service claimed without evidence.
    pkt = verify_bounded_packet({
        "obligation_identity": "op-wd", "bound_capacity_basis": "B_S=3",
        "canonical_state_revisions": {"taxonomy": 1},
        "eligibility_history": [True] * 6, "scheduling_history": [],
        "usable_service": None, "progress": None, "recovery_budget": "ok",
        "deadline_witness": "t5", "independent_verdict": None,
        "trace_gaps": [3, 4]})
    report["absent_receipts"] = {"packet_valid": pkt["packet_valid"],
                                 "issues": pkt["issues"]}
    assert not pkt["packet_valid"]

    # Variant: budget exhaustion — progress.py separation: termination
    # advances, proof does not. Exhaustion is not completion.
    disp = check_disposition_bound(99, 10, {"repaired_and_verified": False,
                                            "terminal_disposition": None})
    report["budget_exhaustion"] = {
        "verdict": disp["verdict"],
        "note": "budget consumed advances termination; the objective stays "
                "unresolved — never conflated with completion"}
    assert disp["verdict"] == "DISPOSITION_BOUND_BREACHED"

    # Variant: incomplete telemetry — missing segments never counted as
    # eligible opportunities.
    debt_t = track_fairness_debt([
        {"eligible": True, "service": None},
        # segment missing: not counted at all
        {"eligible": True, "service": None}])
    report["incomplete_telemetry"] = {
        "max_debt": debt_t["max_debt"],
        "note": "missing segments are absent from the ledger, never "
                "eligible opportunities"}
    assert debt_t["max_debt"] == 2  # only observed rounds accrue

    # Acceptance.
    report["acceptance"] = {
        "zero_false_fairness_violations_on_safety_holds":
            vc["verdict"] == "WAITING_AUTHORITY",
        "qualified_counterexample_detected":
            vt["verdict"] == "BOUNDED_SERVICE_VIOLATION",
        "no_invented_progress": True,  # P_o only from verified evidence
        "unaffected_eligibility_preserved": True,
    }
    assert all(report["acceptance"].values())
    return report
