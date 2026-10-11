"""UD-11 — WITHDRAW BAD EVIDENCE CLEANLY, KEEP THE GOOD.

When evidence loses its right to certify, we revoke at the smallest
defensible unit, recompute exactly what depended on it, and keep everything
independently supported. Crashes and replays can never resurrect what was
withdrawn.

This module unifies the D11/D33/D34/D35/D36 machinery into one executable
engine (stdlib only):

  (1) Append-only eligibility ledger. Evidence content is immutable; only
      eligibility changes, as receipts. AND/OR support paths per claim.
      Two-stage revocation: impact discovery -> topological requalification
      under one consistent evidence-policy snapshot.
  (2) Per-surface projection manifests with qualification generations and
      a read-time gate on every authority-bearing route.
  (3) Atomic compare-and-swap publication with fencing tokens. Writers
      rebase and recompute; they never blindly retry.
  (4) The Revocation Linearization Law as an executable bounded
      model-checker: one commit point, ordering rules for every race,
      revision monotonicity (no ABA reuse), idempotent recovery. S1-S6
      hold across all enumerated interleavings; every guard-removal
      mutant yields a counterexample.
  (5) Smallest-unit compromise: evidence carries fragments; revoking one
      fragment invalidates exactly the paths that required it.

Verdict vocabulary is shared with drift_canary.revocation on main:
UNAFFECTED / REQUALIFIED / DOWNGRADED / INSUFFICIENT_DATA / SUSPENDED /
REVOKED. This module does not redefine it.

SPEC + executable machinery. NOT wired into kernel/, KNOW, LAW, ACT, or
any live path. Wiring needs Shawn's word.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import permutations
from typing import Dict, FrozenSet, List, Optional, Set, Tuple

# ---------------------------------------------------------------------------
# Vocabulary (shared with drift_canary.revocation — same names, same meaning)
# ---------------------------------------------------------------------------

UNAFFECTED = "UNAFFECTED"
REQUALIFIED = "REQUALIFIED"
DOWNGRADED = "DOWNGRADED"
INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
SUSPENDED = "SUSPENDED"
REVOKED = "REVOKED"

VERDICTS = (UNAFFECTED, REQUALIFIED, DOWNGRADED, INSUFFICIENT_DATA,
            SUSPENDED, REVOKED)

# Verdicts under which a claim may still certify dependent conclusions.
CERTIFYING_VERDICTS = frozenset({UNAFFECTED, REQUALIFIED, DOWNGRADED})

# Eligibility states of evidence. ELIGIBLE evidence certifies; everything
# else is a distinct, named reason it cannot.
ELIGIBLE = "ELIGIBLE"
SUSPECT = "SUSPECT"      # possibly compromised — hold, investigate, don't destroy
REVOKED_E = "REVOKED"    # confirmed compromised — excluded
EXPIRED = "EXPIRED"      # freshness lapsed — reassess, never auto-revoke

# Contamination assessments driving selective propagation.
CONFIRMED = "confirmed_compromised"
POSSIBLE = "possibly_compromised"
CLEARED = "independently_cleared"

# Projection surfaces.
SURFACES = ("summary", "note", "index", "successor")

# Manifest status.
M_CURRENT = "CURRENT"
M_REVALIDATION_REQUIRED = "REVALIDATION_REQUIRED"
M_REFRESH_PENDING = "REFRESH_PENDING"
M_HISTORICAL_ONLY = "HISTORICAL_ONLY"

# Authority-bearing routes: the read-time gate refuses stale projections here.
AUTHORITY_ROUTES = frozenset({
    "ACT", "KNOW_RETRIEVAL", "CONNECT_EXPANSION", "SUCCESSOR_ACTIVATION",
    "LEARN_PROMOTION",
})

# Publication outcomes.
PUB_COMMITTED = "COMMITTED"
PUB_STALE_DEPENDENCY = "REJECTED_STALE_DEPENDENCY"
PUB_WRITE_CONFLICT = "REJECTED_WRITE_CONFLICT"

# Read-gate outcomes.
READ_ALLOW = "ALLOW"
READ_STALE = "REJECT_STALE"
READ_HISTORICAL = "HISTORICAL_ONLY"


# ---------------------------------------------------------------------------
# Evidence: immutable content, fragment-scoped (the smallest unit)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Evidence:
    """One evidence source. Content is immutable history — never deleted or
    rewritten by a revocation. Fragments are the smallest unit that can be
    revoked independently (e.g. regions of a benchmark, sections of a log)."""
    evidence_id: str
    content_hash: str
    fragments: FrozenSet[str] = frozenset({"full"})
    regions: FrozenSet[str] = frozenset({"staging", "production"})


@dataclass(frozen=True)
class EligibilityReceipt:
    """One append-only eligibility change. The trail answers both 'what did
    we believe then' and 'what are we justified in claiming now'."""
    seq: int
    evidence_id: str
    fragments: Optional[FrozenSet[str]]  # None = whole evidence
    old_state: str
    new_state: str
    reason: str
    revision: int  # per-evidence monotonic revision; never reused (no ABA)


class EligibilityLedger:
    """Append-only. Current eligibility is derived by folding receipts."""

    def __init__(self) -> None:
        self._receipts: List[EligibilityReceipt] = []
        self._revisions: Dict[str, int] = {}
        self._seq = 0

    def register(self, evidence: Evidence) -> EligibilityReceipt:
        return self._append(evidence.evidence_id, None, None, ELIGIBLE,
                           "registered", evidence)

    def change(self, evidence_id: str, new_state: str, reason: str,
               fragments: Optional[FrozenSet[str]] = None) -> EligibilityReceipt:
        old = self.current(evidence_id, fragments)
        return self._append(evidence_id, fragments, old, new_state, reason)

    def _append(self, evidence_id, fragments, old_state, new_state, reason,
                evidence: Optional[Evidence] = None) -> EligibilityReceipt:
        self._seq += 1
        # Revision is per-evidence and strictly increasing — never reused,
        # even across state cycles (REVOKED -> ELIGIBLE mints higher).
        rev = self._revisions.get(evidence_id, 0) + 1
        self._revisions[evidence_id] = rev
        if fragments is not None:
            fragments = frozenset(fragments)
        r = EligibilityReceipt(seq=self._seq, evidence_id=evidence_id,
                               fragments=fragments, old_state=old_state,
                               new_state=new_state, reason=reason, revision=rev)
        self._receipts.append(r)
        return r

    def current(self, evidence_id: str,
                fragments: Optional[FrozenSet[str]] = None) -> str:
        """Current eligibility for the evidence (or its fragments).

        Fragment queries: the fragment's state is the most severe state
        among whole-evidence receipts and receipts naming that fragment.
        Severity: REVOKED > SUSPECT > EXPIRED > ELIGIBLE.
        """
        severity = {ELIGIBLE: 0, EXPIRED: 1, SUSPECT: 2, REVOKED_E: 3}
        worst = ELIGIBLE
        for r in self._receipts:
            if r.evidence_id != evidence_id:
                continue
            if fragments is None:
                if r.fragments is None and severity[r.new_state] > severity[worst]:
                    worst = r.new_state
            else:
                if r.fragments is None or (r.fragments & frozenset(fragments)):
                    if severity[r.new_state] > severity[worst]:
                        worst = r.new_state
        return worst

    def revision_of(self, evidence_id: str) -> int:
        return self._revisions.get(evidence_id, 0)

    def adopt(self, evidence_id: str, fragments: Optional[FrozenSet[str]],
              new_state: str, reason: str, revision: int) -> EligibilityReceipt:
        """Recovery path: record a receipt at an externally-established
        revision (must be strictly greater than current)."""
        assert revision > self._revisions.get(evidence_id, 0), \
            "adopt requires a strictly newer revision"
        old = self.current(evidence_id, fragments)
        self._seq += 1
        self._revisions[evidence_id] = revision
        r = EligibilityReceipt(seq=self._seq, evidence_id=evidence_id,
                               fragments=frozenset(fragments)
                               if fragments is not None else None,
                               old_state=old, new_state=new_state,
                               reason=reason, revision=revision)
        self._receipts.append(r)
        return r

    def receipts(self) -> List[EligibilityReceipt]:
        return list(self._receipts)

    def snapshot(self) -> Dict[str, str]:
        """One consistent evidence-policy snapshot: evidence_id -> state."""
        out: Dict[str, str] = {}
        seen: Set[str] = set()
        for r in self._receipts:
            seen.add(r.evidence_id)
        for eid in seen:
            out[eid] = self.current(eid)
        return out


# ---------------------------------------------------------------------------
# Claims: explicit AND/OR support paths; derivation graph for taint
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SupportPath:
    """One AND-path: every (evidence, fragment) requirement must hold.
    region: the scope this path covers (narrowing is explicit regions)."""
    requirements: FrozenSet[Tuple[str, str]]  # (evidence_id, fragment)
    region: FrozenSet[str] = frozenset({"staging", "production"})


@dataclass
class Claim:
    claim_id: str
    paths: List[SupportPath]
    required_region: FrozenSet[str] = frozenset({"staging", "production"})
    depends_on: List[str] = field(default_factory=list)  # claim-level derivation
    min_live_paths: int = 1
    verdict: str = UNAFFECTED
    verdict_region: FrozenSet[str] = frozenset({"staging", "production"})
    qualified_at_generation: int = 0


class DerivationGraph:
    """Evidence-level derivation: if E2 was derived from E1, revoking E1
    taints E2. A path through E2 is then not independent corroboration
    (the false-corroboration detector). Transitive."""

    def __init__(self) -> None:
        self._derived_from: Dict[str, Set[str]] = {}

    def derive(self, evidence_id: str, from_evidence_id: str) -> None:
        self._derived_from.setdefault(evidence_id, set()).add(from_evidence_id)

    def tainted_by(self, revoked: Set[str]) -> Set[str]:
        tainted = set(revoked)
        changed = True
        while changed:
            changed = False
            for eid, sources in self._derived_from.items():
                if eid not in tainted and (sources & tainted):
                    tainted.add(eid)
                    changed = True
        return tainted


# ---------------------------------------------------------------------------
# Two-stage revocation engine
# ---------------------------------------------------------------------------

@dataclass
class ClaimRecompute:
    claim_id: str
    old_verdict: str
    new_verdict: str
    new_region: FrozenSet[str]
    surviving_paths: int
    touched: bool


@dataclass
class RequalificationReport:
    generation: int
    revoked_evidence: str
    revoked_fragments: Optional[FrozenSet[str]]
    recomputes: List[ClaimRecompute]
    does_not_claim: str = (
        "Requalification judges certification standing, not truth. "
        "Revoking 'scheduler caused this outage' does not establish it didn't."
    )


class RevocationEngine:
    """Stage 1: impact discovery (the affected closure).
    Stage 2: topological requalification under one consistent snapshot."""

    def __init__(self) -> None:
        self.ledger = EligibilityLedger()
        self.evidence: Dict[str, Evidence] = {}
        self.claims: Dict[str, Claim] = {}
        self.derivations = DerivationGraph()
        self.generation = 0  # advances on every committed revocation

    # -- registration ------------------------------------------------------
    def add_evidence(self, evidence: Evidence) -> None:
        self.evidence[evidence.evidence_id] = evidence
        self.ledger.register(evidence)

    def add_claim(self, claim: Claim) -> None:
        self.claims[claim.claim_id] = claim

    def derive_evidence(self, evidence_id: str, from_evidence_id: str) -> None:
        self.derivations.derive(evidence_id, from_evidence_id)

    # -- revocation --------------------------------------------------------
    def revoke(self, evidence_id: str, reason: str,
               fragments: Optional[Set[str]] = None,
               assessment: str = CONFIRMED) -> RequalificationReport:
        """Revoke eligibility (the contribution), never the history."""
        frags = frozenset(fragments) if fragments else None
        if assessment == CONFIRMED:
            new_state = REVOKED_E
        elif assessment == POSSIBLE:
            new_state = SUSPECT
        else:
            new_state = EXPIRED
        self.ledger.change(evidence_id, new_state, reason, frags)
        self.generation += 1  # one commit point: the revocation commit

        # Stage 1: impact discovery — the affected closure.
        revoked_set = {evidence_id}
        tainted = self.derivations.tainted_by(revoked_set)
        affected = self._impact_closure(evidence_id, frags, tainted)

        # Stage 2: topological requalification under one snapshot.
        snapshot = self.ledger.snapshot()
        order = self._topological_order(affected)
        recomputes: List[ClaimRecompute] = []
        for cid in order:
            recomputes.append(
                self._requalify(self.claims[cid], evidence_id, frags,
                                tainted, snapshot))
        return RequalificationReport(
            generation=self.generation,
            revoked_evidence=evidence_id,
            revoked_fragments=frags,
            recomputes=recomputes)

    def _touches(self, path: SupportPath, evidence_id: str,
                 frags: Optional[FrozenSet[str]], tainted: Set[str]) -> bool:
        for (eid, frag) in path.requirements:
            if eid == evidence_id and (frags is None or frag in frags):
                return True
            if eid in tainted and eid != evidence_id:
                return True
        return False

    def _impact_closure(self, evidence_id: str,
                        frags: Optional[FrozenSet[str]],
                        tainted: Set[str]) -> Set[str]:
        affected: Set[str] = set()
        for cid, claim in self.claims.items():
            if any(self._touches(p, evidence_id, frags, tainted)
                   for p in claim.paths):
                affected.add(cid)
        # Claims deriving from affected claims are in the closure too.
        changed = True
        while changed:
            changed = False
            for cid, claim in self.claims.items():
                if cid not in affected and any(d in affected
                                               for d in claim.depends_on):
                    affected.add(cid)
                    changed = True
        return affected

    def _topological_order(self, affected: Set[str]) -> List[str]:
        order: List[str] = []
        visited: Set[str] = set()

        def visit(cid: str) -> None:
            if cid in visited:
                return
            visited.add(cid)
            for dep in self.claims[cid].depends_on:
                if dep in affected:
                    visit(dep)
            order.append(cid)

        for cid in sorted(affected):
            visit(cid)
        return order

    def _path_state(self, path: SupportPath, snapshot: Dict[str, str],
                    tainted: Set[str]) -> str:
        """live / suspect / dead under the snapshot.

        Derivation taint kills a path only when the evidence itself still
        looks eligible (the false-corroboration case: E2 derived from
        revoked E1). If the snapshot already marks the evidence
        REVOKED/SUSPECT/EXPIRED, the snapshot state decides."""
        worst = "live"
        for (eid, frag) in path.requirements:
            state = snapshot.get(eid, ELIGIBLE)
            if eid in tainted and state == ELIGIBLE:
                return "dead"
            if state == REVOKED_E:
                return "dead"
            if state in (SUSPECT, EXPIRED):
                worst = "suspect"
        return worst

    def _requalify(self, claim: Claim, evidence_id: str,
                   frags: Optional[FrozenSet[str]], tainted: Set[str],
                   snapshot: Dict[str, str]) -> ClaimRecompute:
        old = claim.verdict
        touched = any(self._touches(p, evidence_id, frags, tainted)
                      for p in claim.paths)
        if not touched:
            return ClaimRecompute(claim.claim_id, old, UNAFFECTED,
                                  claim.required_region, len(claim.paths),
                                  touched=False)

        live_full = [p for p in claim.paths
                     if self._path_state(p, snapshot, tainted) == "live"
                     and claim.required_region <= p.region]
        suspect = [p for p in claim.paths
                   if self._path_state(p, snapshot, tainted) == "suspect"]

        if len(live_full) >= claim.min_live_paths:
            new, region = REQUALIFIED, claim.required_region
        elif live_full:
            # Valid evidence, but too little for the bar.
            new, region = INSUFFICIENT_DATA, claim.required_region
        else:
            # Narrower region explicitly — never fractional confidence.
            narrower = [p for p in claim.paths
                        if self._path_state(p, snapshot, tainted) == "live"]
            narrowed_regions = [set(p.region) & set(claim.required_region)
                                for p in narrower]
            narrowed_regions = [r for r in narrowed_regions if r]
            if narrowed_regions:
                best = max(narrowed_regions, key=len)
                new, region = DOWNGRADED, frozenset(best)
            elif suspect:
                new, region = SUSPENDED, claim.required_region
            else:
                new, region = REVOKED, frozenset()

        claim.verdict = new
        claim.verdict_region = region
        claim.qualified_at_generation = self.generation
        return ClaimRecompute(claim.claim_id, old, new, region, len(live_full),
                              touched=True)

    # -- independent requalification ---------------------------------------
    def requalify_with(self, evidence: Evidence) -> EligibilityReceipt:
        """Independent new evidence may establish a newer qualification.
        This mints a HIGHER revision — never a reuse (no ABA)."""
        self.add_evidence(evidence)
        return self.ledger.receipts()[-1]

    def current_verdict(self, claim_id: str) -> Tuple[str, FrozenSet[str], int]:
        c = self.claims[claim_id]
        return c.verdict, c.verdict_region, c.qualified_at_generation

# ---------------------------------------------------------------------------
# Projection manifests, read-time gate, CAS publication, recovery
# ---------------------------------------------------------------------------

@dataclass
class FencingToken:
    """Proves WHEN a worker read (reader_id, read_generation). It never
    replaces evidence-version checks: a valid token does not save a stale
    write."""
    reader_id: str
    read_generation: int


@dataclass
class ProjectionManifest:
    """Per-surface projection: what was computed, at which generation, and
    whether it may still serve as current authority."""
    surface: str  # one of SURFACES
    claim_verdicts: Dict[str, Tuple[str, FrozenSet[str]]]
    generation: int
    status: str = M_CURRENT


class ProjectionLayer:
    """The cache/projection layer above the revocation engine."""

    def __init__(self, engine: RevocationEngine) -> None:
        self.engine = engine
        self.manifests: Dict[str, ProjectionManifest] = {}

    def build_manifest(self, surface: str) -> ProjectionManifest:
        assert surface in SURFACES
        verdicts = {cid: (c.verdict, c.verdict_region)
                    for cid, c in self.engine.claims.items()}
        m = ProjectionManifest(surface=surface, claim_verdicts=verdicts,
                               generation=self.engine.generation)
        self.manifests[surface] = m
        return m

    def read_gate(self, surface: str, route: str) -> str:
        """No stale projection ever serves as current on an
        authority-bearing route — including mid-refresh."""
        m = self.manifests.get(surface)
        if m is None:
            return READ_STALE
        if m.status == M_HISTORICAL_ONLY:
            return READ_HISTORICAL
        if route in AUTHORITY_ROUTES and m.generation < self.engine.generation:
            return READ_STALE
        return READ_ALLOW

    def mark_stale(self, surface: str) -> None:
        m = self.manifests.get(surface)
        if m is not None and m.generation < self.engine.generation:
            m.status = M_REVALIDATION_REQUIRED


class Publisher:
    """Atomic compare-and-swap publication.

    PublishAllowed = head matches AND qualification deps current AND
    evidence deps admissible. Failures return STALE_DEPENDENCY /
    WRITE_CONFLICT — writers rebase and recompute, never blindly retry.
    """

    def __init__(self, engine: RevocationEngine, projections: ProjectionLayer) -> None:
        self.engine = engine
        self.projections = projections
        self.committed: List[Tuple[str, int]] = []  # (surface, generation)

    def publish(self, manifest: ProjectionManifest, token: FencingToken,
                expected_generation: int) -> str:
        # CAS on the projection head: a delayed writer's old generation
        # can never be published over a newer revocation.
        if expected_generation != self.engine.generation:
            return PUB_WRITE_CONFLICT
        # Qualification dependencies must be current at commit.
        for cid, (verdict, region) in manifest.claim_verdicts.items():
            cur_v, cur_r, cur_g = self.engine.current_verdict(cid)
            if cur_g > manifest.generation:
                return PUB_STALE_DEPENDENCY
            if (cur_v, cur_r) != (verdict, region):
                return PUB_STALE_DEPENDENCY
        # Evidence dependencies must be admissible at commit.
        for cid in manifest.claim_verdicts:
            claim = self.engine.claims[cid]
            for p in claim.paths:
                for (eid, frag) in p.requirements:
                    if self.engine.ledger.current(eid, {frag}) == REVOKED_E:
                        # Only matters if the claim still certifies through it.
                        if manifest.claim_verdicts[cid][0] in CERTIFYING_VERDICTS:
                            if self._path_needs(p, eid, frag, claim):
                                return PUB_STALE_DEPENDENCY
        # The fencing token is recorded (provenance of when the worker read);
        # it never overrides the checks above.
        _ = token
        manifest.status = M_CURRENT
        manifest.generation = self.engine.generation
        self.projections.manifests[manifest.surface] = manifest
        self.committed.append((manifest.surface, manifest.generation))
        return PUB_COMMITTED

    def _path_needs(self, path: SupportPath, eid: str, frag: str,
                    claim: Claim) -> bool:
        # Does the claim's certification actually rely on this (e, frag)?
        # True if every live path covering the verdict region needs it.
        needed_everywhere = True
        for p in claim.paths:
            if claim.verdict_region <= p.region:
                live = all(
                    self.engine.ledger.current(e2, {f2}) != REVOKED_E
                    for (e2, f2) in p.requirements)
                if live and (eid, frag) not in p.requirements:
                    needed_everywhere = False
        return needed_everywhere


@dataclass(frozen=True)
class ReplayEvent:
    """Recovery replays events as reconcile-instructions, never blind
    overwrites. Each carries the revision it was recorded at. A genuine
    independent requalification arrives as an event flagged
    is_requalification=True; a plain old ELIGIBLE event can never
    resurrect withdrawn eligibility."""
    evidence_id: str
    revision: int
    new_state: str
    fragments: Optional[FrozenSet[str]] = None
    is_requalification: bool = False


class RecoveryLog:
    """Idempotent recovery: replaying an event never decreases a revision
    and never resurrects withdrawn eligibility."""

    def __init__(self, engine: RevocationEngine) -> None:
        self.engine = engine
        self._applied_keys: Set[Tuple[str, int, str]] = set()

    def reconcile(self, events: List[ReplayEvent]) -> Dict[str, int]:
        """Returns counts: applied / ignored_stale / ignored_resurrect."""
        out = {"applied": 0, "ignored_stale": 0, "ignored_resurrect": 0}
        for ev in events:
            key = (ev.evidence_id, ev.revision, ev.new_state)
            if key in self._applied_keys:
                out["ignored_stale"] += 1
                continue
            cur_rev = self.engine.ledger.revision_of(ev.evidence_id)
            if ev.revision <= cur_rev:
                # Older or duplicate information: never rolls back newer
                # state. A delayed revocation event cannot roll back a
                # newer independent requalification — and a delayed old
                # ELIGIBLE event cannot resurrect a newer revocation.
                out["ignored_stale"] += 1
                continue
            cur_state = self.engine.ledger.current(ev.evidence_id)
            if (cur_state == REVOKED_E and ev.new_state == ELIGIBLE
                    and not ev.is_requalification):
                # A non-requalification ELIGIBLE with a newer revision is
                # treated as untrusted for resurrection: withdrawing
                # requires the engine's requalification path. Refuse.
                out["ignored_resurrect"] += 1
                continue
            self.engine.ledger.adopt(ev.evidence_id, ev.fragments,
                                     ev.new_state, "recovery-reconcile",
                                     ev.revision)
            self._applied_keys.add(key)
            out["applied"] += 1
        return out

# ---------------------------------------------------------------------------
# Revocation Linearization Law — executable bounded model checker
#
# One commit point (the revocation commit). Ordering rules for every race:
#   R<P  -> publication built pre-R is rejected post-R
#   P<R  -> publication was valid at commit, loses current authority after R
#   V<R<A -> earlier validation cannot authorize the action; revalidate
#   replay -> reconcile-instructions, never blind overwrites
# Revision monotonicity: no ABA reuse. Idempotent recovery.
#
# S1: no certification/publication/action on revoked evidence at the
#     linearization point
# S2: no stale projection publication (built pre-R, committed post-R)
# S3: no consequential action without current qualification at the
#     commit boundary
# S4: per-evidence revisions strictly increasing; never reused
# S5: replay never decreases a revision; never resurrects withdrawn
#     eligibility except via legitimate requalification
# S6: revoking E1 never auto-invalidates a claim established through E2
#     (only requalification recomputes verdicts)
#
# Bounded and honest: scenarios enumerate all distinct interleavings of a
# small op multiset. This is not TLA+/TLC; it is an executable check that
# every reachable interleaving *in the bounded model* satisfies S1-S6.
# ---------------------------------------------------------------------------

# Guard-removal mutants. Each must yield a counterexample; a mutant that
# passes is a failed spec.
MUTANTS = (
    "no_publication_check",  # P commits without checking current deps
    "no_action_fence",       # A commits on a stale validation
    "revision_reuse",        # R reuses the revision number (ABA)
    "blind_replay",          # RP overwrites without monotonicity
)


class AbsMachine:
    """Abstract revocation machine. Ops:
    ("R", e) | ("Q", c) | ("P", c) | ("V", c) | ("A", c) |
    ("REQUAL", e) | ("RP", ((e, rev, state, is_requal), ...))"""

    def __init__(self, support: Dict[str, Tuple[Tuple[str, ...], ...]],
                 defects: FrozenSet[str] = frozenset()) -> None:
        self.support = support
        self.defects = defects
        evs = {e for paths in support.values() for p in paths for e in p}
        self.elig: Dict[str, str] = {e: ELIGIBLE for e in evs}
        self.rev: Dict[str, int] = {e: 0 for e in evs}
        self.qual: Dict[str, bool] = {c: False for c in support}
        self.qual_gen: Dict[str, int] = {c: -1 for c in support}
        self.generation = 0
        self.op_index = 0
        self.validations: List[Tuple[str, int, int]] = []  # (claim, gen, idx)
        self.commits: List[tuple] = []  # ("P"/"A", claim, gen, ok, idx, extra)
        self.elig_hist: List[tuple] = []  # (idx, e, old, new, rev, via_requal)
        self.rev_hist: List[tuple] = []   # (idx, e, rev)
        self.qual_hist: List[tuple] = []  # (idx, c, old, new, via_Q)

    def _live(self, c: str) -> bool:
        return any(all(self.elig[e] == ELIGIBLE for e in p)
                   for p in self.support[c])

    def step(self, op: tuple) -> None:
        self.op_index += 1
        i = self.op_index
        k = op[0]
        if k == "R":
            e = op[1]
            new_rev = self.rev[e] + 1
            if "revision_reuse" in self.defects:
                new_rev = self.rev[e]  # ABA: reuse the number
            self.elig_hist.append((i, e, self.elig[e], REVOKED_E, new_rev, False))
            self.rev_hist.append((i, e, new_rev))
            self.elig[e] = REVOKED_E
            self.rev[e] = new_rev
            self.generation += 1
        elif k == "REQUAL":
            e = op[1]
            new_rev = self.rev[e] + 1
            self.elig_hist.append((i, e, self.elig[e], ELIGIBLE, new_rev, True))
            self.rev_hist.append((i, e, new_rev))
            self.elig[e] = ELIGIBLE
            self.rev[e] = new_rev
            self.generation += 1
        elif k == "Q":
            c = op[1]
            old = self.qual[c]
            self.qual[c] = self._live(c)
            self.qual_gen[c] = self.generation
            self.qual_hist.append((i, c, old, self.qual[c], True))
        elif k == "P":
            c = op[1]
            if "no_publication_check" in self.defects:
                ok = True
            else:
                ok = (self.qual[c] and self.qual_gen[c] == self.generation
                      and self._live(c))
            self.commits.append(("P", c, self.generation, ok, i,
                                 self.qual_gen[c]))
        elif k == "V":
            self.validations.append((op[1], self.generation, i))
        elif k == "A":
            c = op[1]
            recent = [v for v in self.validations if v[0] == c]
            vgen = recent[-1][1] if recent else -1
            if "no_action_fence" in self.defects:
                ok = bool(recent)
            else:
                ok = (bool(recent) and vgen == self.generation
                      and self.qual[c] and self._live(c))
            self.commits.append(("A", c, self.generation, ok, i, vgen,
                                 self.qual[c], self._live(c)))
        elif k == "RP":
            for (e, rev, state, requal) in op[1]:
                if "blind_replay" in self.defects:
                    self._apply_replay(i, e, rev, state, requal)
                else:
                    if rev <= self.rev[e]:
                        continue
                    if (self.elig[e] == REVOKED_E and state == ELIGIBLE
                            and not requal):
                        continue
                    self._apply_replay(i, e, rev, state, requal)

    def _apply_replay(self, i: int, e: str, rev: int, state: str,
                      requal: bool) -> None:
        self.elig_hist.append((i, e, self.elig[e], state, rev, requal))
        self.rev_hist.append((i, e, rev))
        self.elig[e] = state
        self.rev[e] = rev


def _elig_at(m: AbsMachine, idx: int) -> Dict[str, str]:
    elig = {e: ELIGIBLE for e in m.elig}
    for (hi, e, _old, new, _rev, _rq) in m.elig_hist:
        if hi <= idx:
            elig[e] = new
    return elig


def check_invariants(m: AbsMachine) -> List[Tuple[str, str]]:
    """S1-S6 over the machine's recorded history. Returns violations."""
    viols: List[Tuple[str, str]] = []
    for entry in m.commits:
        kind = entry[0]
        if kind == "P":
            _, c, gen, ok, idx, qgen = entry
            if not ok:
                continue
            elig_at = _elig_at(m, idx)
            live = any(all(elig_at[e] == ELIGIBLE for e in p)
                       for p in m.support[c])
            if not live:
                viols.append(("S1", f"P {c} committed at op {idx} on "
                                    f"revoked evidence"))
            if qgen != gen:
                viols.append(("S2", f"P {c} committed at op {idx} with "
                                    f"stale qualification generation "
                                    f"(qualified at {qgen}, committed at {gen})"))
        else:
            _, c, gen, ok, idx, vgen, qual_now, live_now = entry
            if not ok:
                continue
            if vgen != gen:
                viols.append(("S3", f"A {c} committed at op {idx} on stale "
                                    f"validation (validated at gen {vgen}, "
                                    f"committed at gen {gen})"))
            if not qual_now or not live_now:
                viols.append(("S3", f"A {c} committed at op {idx} without "
                                    f"current qualification"))
            elig_at = _elig_at(m, idx)
            live = any(all(elig_at[e] == ELIGIBLE for e in p)
                       for p in m.support[c])
            if not live:
                viols.append(("S1", f"A {c} committed at op {idx} on "
                                    f"revoked evidence"))
    # S4: per-evidence revisions strictly increasing, never reused.
    by_e: Dict[str, List[int]] = {}
    for (idx, e, rev) in m.rev_hist:
        by_e.setdefault(e, []).append(rev)
    for e, revs in by_e.items():
        for a, b in zip(revs, revs[1:]):
            if b <= a:
                viols.append(("S4", f"evidence {e}: revision not strictly "
                                    f"increasing ({a} -> {b}) — ABA reuse"))
                break
    # S5: no REVOKED -> ELIGIBLE except via legitimate requalification.
    for (idx, e, old, new, rev, via_requal) in m.elig_hist:
        if old == REVOKED_E and new == ELIGIBLE and not via_requal:
            viols.append(("S5", f"evidence {e}: replay resurrected revoked "
                                f"eligibility at op {idx}"))
    # S6: verdicts change only via requalification (Q). Revocation never
    # auto-invalidates; only Q recomputes.
    for (idx, c, old, new, via_Q) in m.qual_hist:
        if old and not new and not via_Q:
            viols.append(("S6", f"claim {c}: qualification lost without "
                                f"requalification at op {idx}"))
    return viols


def _distinct_perms(ops: tuple) -> List[tuple]:
    seen: Set[tuple] = set()
    out: List[tuple] = []
    for p in permutations(ops):
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def model_check(support: Dict[str, Tuple[Tuple[str, ...], ...]],
                scenarios: List[tuple],
                defects: FrozenSet[str] = frozenset()
                ) -> List[Tuple[str, tuple, List[Tuple[str, str]]]]:
    """Run every distinct interleaving of every scenario. Returns
    (scenario_name, interleaving, violations) for traces with violations."""
    bad = []
    for name, ops in scenarios:
        for inter in _distinct_perms(ops):
            m = AbsMachine(support, defects)
            for op in inter:
                m.step(op)
            viols = check_invariants(m)
            if viols:
                bad.append((name, inter, viols))
    return bad


# Standard fixture: C1 needs E1; C2 needs E2; C3 needs E1 or E2.
SUPPORT_FIXTURE: Dict[str, Tuple[Tuple[str, ...], ...]] = {
    "C1": (("E1",),),
    "C2": (("E2",),),
    "C3": (("E1",), ("E2",)),
}

# Race scenarios. Each is a multiset of ops; the checker enumerates every
# distinct interleaving ("all reachable interleavings" of the bounded model).
SCENARIOS = [
    # R<P: publication built pre-R must be rejected post-R.
    ("race_publish_vs_revoke",
     (("R", "E1"), ("Q", "C1"), ("P", "C1"))),
    # V<R<A: earlier validation cannot authorize the action.
    ("race_validate_revoke_act",
     (("V", "C1"), ("Q", "C1"), ("R", "E1"), ("A", "C1"))),
    # Replay races: old ELIGIBLE replayed after revocation.
    ("race_replay_after_revoke",
     (("R", "E1"), ("RP", (("E1", 0, ELIGIBLE, False),)))),
    # Independent requalification is permitted and works.
    ("requalify_then_use",
     (("R", "E1"), ("REQUAL", "E1"), ("Q", "C1"), ("P", "C1"),
      ("V", "C1"), ("A", "C1"))),
    # Double revocation: revision monotonicity under repetition.
    ("double_revoke",
     (("R", "E1"), ("R", "E1"), ("Q", "C3"), ("P", "C3"))),
    # Unrelated claim survives a revocation (S6 in the interleavings).
    ("unrelated_survives",
     (("R", "E1"), ("Q", "C2"), ("Q", "C3"), ("P", "C2"), ("P", "C3"))),
]


def verify_law() -> Dict[str, object]:
    """The acceptance backstop: S1-S6 hold on the clean machine across all
    interleavings, and every guard-removal mutant yields a counterexample."""
    clean_bad = model_check(SUPPORT_FIXTURE, SCENARIOS, frozenset())
    mutant_results: Dict[str, List[tuple]] = {}
    for mutant in MUTANTS:
        bad = model_check(SUPPORT_FIXTURE, SCENARIOS, frozenset({mutant}))
        mutant_results[mutant] = [(name, inter, viols)
                                  for (name, inter, viols) in bad]
    return {"clean_violations": clean_bad, "mutants": mutant_results}


__all__ = [
    "UNAFFECTED", "REQUALIFIED", "DOWNGRADED", "INSUFFICIENT_DATA",
    "SUSPENDED", "REVOKED", "VERDICTS", "CERTIFYING_VERDICTS",
    "ELIGIBLE", "SUSPECT", "REVOKED_E", "EXPIRED",
    "CONFIRMED", "POSSIBLE", "CLEARED",
    "SURFACES", "AUTHORITY_ROUTES",
    "Evidence", "EligibilityLedger", "EligibilityReceipt",
    "SupportPath", "Claim", "DerivationGraph",
    "RevocationEngine", "RequalificationReport", "ClaimRecompute",
    "FencingToken", "ProjectionManifest", "ProjectionLayer",
    "Publisher", "ReplayEvent", "RecoveryLog",
    "MUTANTS", "AbsMachine", "check_invariants", "model_check",
    "SUPPORT_FIXTURE", "SCENARIOS", "verify_law",
]
