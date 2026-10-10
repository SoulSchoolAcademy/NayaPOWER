"""D33 — Selective Evidence Revocation and Claim Requalification.

Implements the decisive D33 experiment: revoke an ineligible evidence
source's right to support a claim, then independently recompute every
materially dependent conclusion — without deleting the source, assuming
its observations false, or revoking unrelated conclusions.

Core law (D33): revoke the evidence contribution first. Revoke or
downgrade a qualification only if the remaining admissible evidence no
longer establishes the required claim. Preserve every independently
sufficient conclusion. Evidence stays historically preserved; its
eligibility can change; qualifications are recomputed; only genuinely
unsupported conclusions lose standing.

Four distinctions, never collapsed:
  historical existence / observed content / current eligibility /
  factual correctness.

Composes (extends, never duplicates):
  drift_canary.revocation  — the six qualification verdicts
                             (UNAFFECTED / REQUALIFIED / DOWNGRADED /
                             INSUFFICIENT_DATA / SUSPENDED / REVOKED),
                             contribution-vs-qualification revocation,
                             append-only compromise records. The verdict
                             vocabulary is IMPORTED, not redefined.
  drift_canary.propagation — independence states, support-set and
                             region-verdict vocabulary.
  drift_canary.uncertainty — confirmed / possibly / cleared / unassessed
                             assessment states and qualification policy.

The D33 layer added here: explicit AND/OR support sets per claim, the
derivation graph (false-corroboration detection), the two-stage
recomputer (impact discovery -> topological requalification under one
consistent evidence-policy snapshot), scope narrowing (not fractional
confidence), selective propagation by contamination assessment, stale
certificate rejection at consequential use (TOCTOU close), and the
immutable history that answers both "what did we believe then" and
"what are we justified in claiming now".

SPEC + deterministic fixture machinery. NOT wired into kernel/, KNOW,
LAW, ACT, or any live path. Wiring needs Shawn's word.
"""
from __future__ import annotations

from dataclasses import dataclass, field

# The six verdicts are imported from the on-main contract — D33 must not
# invent a competing vocabulary.
from drift_canary.revocation import VERDICTS as QUALIFICATION_VERDICTS

# Re-exported for convenience; the canonical definition lives in
# drift_canary.revocation.
UNAFFECTED = "UNAFFECTED"
REQUALIFIED = "REQUALIFIED"
DOWNGRADED = "DOWNGRADED"
INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
SUSPENDED = "SUSPENDED"
REVOKED = "REVOKED"

assert set(QUALIFICATION_VERDICTS) == {
    UNAFFECTED, REQUALIFIED, DOWNGRADED, INSUFFICIENT_DATA, SUSPENDED, REVOKED
}, "D33 must share revocation.py's verdict vocabulary exactly"

# Eligibility states of an evidence source. ELIGIBLE sources certify;
# everything else is a distinct, named reason a source cannot.
ELIGIBLE = "ELIGIBLE"
SUSPENDED_SRC = "SUSPENDED"          # possibly compromised — hold, don't destroy
REVOKED_SRC = "REVOKED"              # confirmed compromised — excluded
EXPIRED_SRC = "EXPIRED"              # freshness lapsed — reassess, never auto-revoke

# Contamination assessments (uncertainty.py's four states, applied).
CONFIRMED_COMPROMISED = "confirmed_compromised"
POSSIBLY_COMPROMISED = "possibly_compromised"
INDEPENDENTLY_CLEARED = "independently_cleared"
UNASSESSED = "unassessed"

# Regions. A claim's scope is a set of regions; surviving evidence may
# cover only some of them. Narrowing is explicit — never "50% confidence".
STAGING = "staging"
PRODUCTION = "production"

# Path states under a status snapshot.
PATH_LIVE = "live"
PATH_DEAD = "dead"                    # revoked source (or tainted derivation) in path
PATH_SUSPENDED = "suspended"          # possibly-compromised source in path
PATH_FRESHNESS = "freshness"          # expired source in path — reassess, not revoke

# Certificate decisions at consequential use.
CERT_ACCEPTED = "ACCEPTED"
CERT_STALE_VERSION = "REJECTED_STALE_VERSION"
CERT_VERDICT_CHANGED = "REJECTED_VERDICT_CHANGED"

# ACT commit-boundary decisions (TOCTOU close).
ACT_AUTHORIZED = "AUTHORIZED"
ACT_REFUSED = "REFUSED"

# Verdicts under which a claim may still certify dependent conclusions.
CERTIFYING_VERDICTS = {UNAFFECTED, REQUALIFIED, DOWNGRADED}


# ---------------------------------------------------------------------------
# Evidence sources: history is preserved; eligibility is versioned.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class EvidenceSource:
    """One evidence source. observed_content is immutable history — it is
    NEVER deleted or rewritten by a revocation. Only eligibility changes."""
    source_id: str
    observed_content: str
    scope: frozenset = frozenset({STAGING, PRODUCTION})
    coverage: str = "complete"        # "complete" | "gap" (missing interval)


@dataclass(frozen=True)
class EligibilityReceipt:
    """Append-only record of one eligibility change. The trail answers both
    'what did we believe then' and 'what are we justified in claiming now'."""
    receipt_id: str
    source_id: str
    previous_status: str
    new_status: str
    reason: str
    assessment: str
    policy_version: int


@dataclass(frozen=True)
class FreshnessReassessment:
    """An expired source demands human/operator reassessment of freshness —
    it is never auto-revoked and never auto-cleared."""
    source_id: str
    policy_version: int
    action: str = "REASSESS_FRESHNESS"


class EligibilityLedger:
    """Append-only ledger. status() reflects the latest receipt; history is
    never rewritten."""

    def __init__(self) -> None:
        self._sources: dict[str, EvidenceSource] = {}
        self._receipts: list[EligibilityReceipt] = []
        self._counter = 0

    def register(self, source: EvidenceSource) -> None:
        if source.source_id in self._sources:
            raise ValueError(f"duplicate source {source.source_id}")
        self._sources[source.source_id] = source

    def source(self, source_id: str) -> EvidenceSource:
        return self._sources[source_id]

    def status(self, source_id: str) -> str:
        for r in reversed(self._receipts):
            if r.source_id == source_id:
                return r.new_status
        return ELIGIBLE

    def change(self, source_id: str, new_status: str, reason: str,
               assessment: str, policy_version: int) -> EligibilityReceipt:
        if source_id not in self._sources:
            raise KeyError(f"unknown source {source_id}")
        self._counter += 1
        receipt = EligibilityReceipt(
            receipt_id=f"ELR-{self._counter:04d}",
            source_id=source_id,
            previous_status=self.status(source_id),
            new_status=new_status,
            reason=reason,
            assessment=assessment,
            policy_version=policy_version,
        )
        self._receipts.append(receipt)
        return receipt

    def receipts(self) -> tuple[EligibilityReceipt, ...]:
        return tuple(self._receipts)


# ---------------------------------------------------------------------------
# Derivation graph: catches sources masquerading as independent.
# ---------------------------------------------------------------------------

class DerivationGraph:
    """derived_id -> origin_id. A path that avoids a revoked source but
    runs through material secretly derived from it was never independent."""

    def __init__(self) -> None:
        self._origin: dict[str, str] = {}

    def add(self, derived_id: str, origin_id: str) -> None:
        if derived_id == origin_id:
            raise ValueError("a source cannot derive from itself")
        self._origin[derived_id] = origin_id

    def ancestors(self, source_id: str) -> frozenset:
        seen: set[str] = set()
        cur = self._origin.get(source_id)
        while cur is not None and cur not in seen:
            seen.add(cur)
            cur = self._origin.get(cur)
        return frozenset(seen)

    def tainted_by(self, source_id: str, tainted: frozenset) -> bool:
        """True if the source itself or any derivation ancestor is tainted."""
        return bool(({source_id} | self.ancestors(source_id)) & tainted)


# ---------------------------------------------------------------------------
# Claims with explicit AND/OR support sets.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SupportPath:
    """One AND-conjunction of sources (one OR-branch of the claim) and the
    region scope that branch actually covers."""
    sources: frozenset
    scope: frozenset = frozenset({STAGING, PRODUCTION})


@dataclass(frozen=True)
class Claim:
    """A qualification claim. paths are OR-branches; scope is the claimed
    region set; min_paths is the certification bar (how many independent
    admissible paths the claim requires — mirroring the two-independent
    rule: certification claims need 2, observational claims need 1)."""
    claim_id: str
    paths: tuple[SupportPath, ...]
    scope: frozenset = frozenset({STAGING, PRODUCTION})
    min_paths: int = 1
    kind: str = "certification"       # "certification" | "observational"
    requires_completeness: bool = False
    depends_on: tuple[str, ...] = ()  # claims whose standing this one needs


@dataclass(frozen=True)
class QualificationRecord:
    claim_id: str
    verdict: str
    covered_scope: frozenset
    reason: str
    policy_version: int


@dataclass(frozen=True)
class Certificate:
    """A pinned qualification, presented at consequential use. Pinning the
    policy version is what makes stale-certificate rejection possible."""
    claim_id: str
    verdict: str
    covered_scope: frozenset
    policy_version: int


@dataclass(frozen=True)
class ClaimRecomputation:
    claim_id: str
    old_verdict: str
    new_verdict: str
    covered_scope: frozenset
    reason: str


@dataclass
class RecomputationReport:
    policy_version: int
    revoked_source: str
    receipts: list[EligibilityReceipt] = field(default_factory=list)
    affected_claims: list[str] = field(default_factory=list)
    recomputations: list[ClaimRecomputation] = field(default_factory=list)
    reassessments: list[FreshnessReassessment] = field(default_factory=list)
    recompute_order: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# The engine: two-stage recomputation under one consistent snapshot.
# ---------------------------------------------------------------------------

class RevocationEngine:
    def __init__(self) -> None:
        self.ledger = EligibilityLedger()
        self.derivations = DerivationGraph()
        self._claims: dict[str, Claim] = {}
        self._records: dict[str, QualificationRecord] = {}
        self._history: dict[str, list[QualificationRecord]] = {}
        self.policy_version = 1

    # -- registration ----------------------------------------------------

    def register_source(self, source: EvidenceSource) -> None:
        self.ledger.register(source)

    def register_claim(self, claim: Claim) -> None:
        if claim.claim_id in self._claims:
            raise ValueError(f"duplicate claim {claim.claim_id}")
        for p in claim.paths:
            for s in p.sources:
                if s not in self.ledger._sources:
                    raise KeyError(f"claim {claim.claim_id} references "
                                   f"unknown source {s}")
        self._claims[claim.claim_id] = claim
        rec = QualificationRecord(
            claim_id=claim.claim_id,
            verdict=UNAFFECTED,
            covered_scope=claim.scope,
            reason="no revocation event on record",
            policy_version=self.policy_version,
        )
        self._records[claim.claim_id] = rec
        self._history.setdefault(claim.claim_id, []).append(rec)

    def add_derivation(self, derived_id: str, origin_id: str) -> None:
        self.derivations.add(derived_id, origin_id)

    # -- the revocation event --------------------------------------------

    def revoke(self, source_id: str, reason: str,
               assessment: str = CONFIRMED_COMPROMISED) -> RecomputationReport:
        """Two-stage recomputation. Stage 1 (CONNECT): discover the affected
        closure. Stage 2 (PROVE/VERIFY): recompute each affected claim in
        topological order under ONE consistent evidence-policy snapshot."""
        if assessment == CONFIRMED_COMPROMISED:
            new_status = REVOKED_SRC
        elif assessment == POSSIBLY_COMPROMISED:
            new_status = SUSPENDED_SRC
        elif assessment == UNASSESSED:
            raise ValueError("UNASSESSED sources are never revoked — "
                             "review first (uncertainty.py: REVIEW_REQUIRED)")
        else:  # "expired"
            new_status = EXPIRED_SRC

        self.policy_version += 1
        version = self.policy_version
        report = RecomputationReport(
            policy_version=version, revoked_source=source_id)

        receipt = self.ledger.change(source_id, new_status, reason,
                                     assessment, version)
        report.receipts.append(receipt)

        if new_status == EXPIRED_SRC:
            # Expired is reassessed, never auto-revoked.
            report.reassessments.append(
                FreshnessReassessment(source_id, version))

        # Consistent snapshot: every verdict below is computed against the
        # statuses as of this policy version — never interleaved updates.
        snapshot = {s: self.ledger.status(s) for s in self.ledger._sources}
        revoked = frozenset(s for s, st in snapshot.items()
                            if st == REVOKED_SRC)
        suspended = frozenset(s for s, st in snapshot.items()
                              if st in (SUSPENDED_SRC, EXPIRED_SRC))

        # Stage 1 — impact discovery: claims whose support closure mentions
        # the source (directly or through a tainted derivation), plus every
        # claim that transitively depends on an affected claim. This is the
        # smallest defensible affected closure: independent claims are not
        # recomputed and keep their standing.
        directly = {
            cid for cid, c in self._claims.items()
            if any(source_id in p.sources or
                   any(self.derivations.tainted_by(s, {source_id})
                       for s in p.sources)
                   for p in c.paths)
        }
        affected = set(directly)
        changed = True
        while changed:
            changed = False
            for cid, c in self._claims.items():
                if cid not in affected and any(d in affected
                                               for d in c.depends_on):
                    affected.add(cid)
                    changed = True
        report.affected_claims = sorted(affected)

        # Stage 2 — topological recomputation: dependencies first.
        order = self._topological_order(affected)
        report.recompute_order = order
        for cid in order:
            claim = self._claims[cid]
            old = self._records[cid]
            verdict, covered, reason = self._compute(
                claim, snapshot, revoked, suspended)
            rec = QualificationRecord(cid, verdict, covered, reason, version)
            self._records[cid] = rec
            self._history[cid].append(rec)
            report.recomputations.append(ClaimRecomputation(
                cid, old.verdict, verdict, covered, reason))
        return report

    def note_coverage_gap(self, source_id: str) -> RecomputationReport:
        """A missing observation interval reopens completeness-dependent
        claims — it does not revoke anything."""
        self.policy_version += 1
        version = self.policy_version
        report = RecomputationReport(
            policy_version=version, revoked_source=source_id)
        affected = {
            cid for cid, c in self._claims.items()
            if c.requires_completeness and any(
                source_id in p.sources for p in c.paths)
        }
        report.affected_claims = sorted(affected)
        snapshot = {s: self.ledger.status(s) for s in self.ledger._sources}
        revoked = frozenset(s for s, st in snapshot.items()
                            if st == REVOKED_SRC)
        suspended = frozenset(s for s, st in snapshot.items()
                              if st in (SUSPENDED_SRC, EXPIRED_SRC))
        order = self._topological_order(affected)
        report.recompute_order = order
        for cid in order:
            claim = self._claims[cid]
            old = self._records[cid]
            verdict, covered, reason = self._compute(
                claim, snapshot, revoked, suspended, gap_source=source_id)
            rec = QualificationRecord(cid, verdict, covered, reason, version)
            self._records[cid] = rec
            self._history[cid].append(rec)
            report.recomputations.append(ClaimRecomputation(
                cid, old.verdict, verdict, covered, reason))
        return report

    # -- verdict computation ----------------------------------------------

    def _path_state(self, path: SupportPath, snapshot: dict,
                    revoked: frozenset, suspended: frozenset) -> str:
        for s in path.sources:
            st = snapshot[s]
            if st == REVOKED_SRC or self.derivations.tainted_by(s, revoked):
                return PATH_DEAD
            if st in (SUSPENDED_SRC, EXPIRED_SRC) or \
                    self.derivations.tainted_by(s, suspended):
                return PATH_SUSPENDED if st == SUSPENDED_SRC else PATH_FRESHNESS
        # An expired source never auto-revokes — but a path through one
        # cannot certify until freshness is reassessed.
        for s in path.sources:
            if snapshot[s] == EXPIRED_SRC:
                return PATH_FRESHNESS
        return PATH_LIVE

    def _compute(self, claim: Claim, snapshot: dict, revoked: frozenset,
                 suspended: frozenset, gap_source: str | None = None
                 ) -> tuple[str, frozenset, str]:
        # Dependencies gate: a claim cannot out-qualify what it stands on.
        for dep in claim.depends_on:
            dep_rec = self._records.get(dep)
            if dep_rec is None or dep_rec.verdict not in CERTIFYING_VERDICTS:
                return (SUSPENDED, frozenset(),
                        f"dependency {dep} not certifying "
                        f"({dep_rec.verdict if dep_rec else 'unknown'})")

        states = [self._path_state(p, snapshot, revoked, suspended)
                  for p in claim.paths]
        live = [p for p, st in zip(claim.paths, states) if st == PATH_LIVE]
        suspended_paths = [p for p, st in zip(claim.paths, states)
                           if st in (PATH_SUSPENDED, PATH_FRESHNESS)]

        # Completeness-dependent claims reopen when a live path's source has
        # a coverage gap over the required interval.
        if gap_source is not None and claim.requires_completeness:
            gapped = [p for p in live if gap_source in p.sources]
            if gapped and all(
                    self.ledger.source(s).coverage == "gap"
                    for p in gapped for s in p.sources
                    if s == gap_source):
                return (INSUFFICIENT_DATA, frozenset(),
                        f"coverage gap on {gap_source}: completeness-"
                        f"dependent claim reopened, not revoked")

        covered: frozenset = frozenset()
        for p in live:
            covered = covered | p.scope

        if len(live) >= claim.min_paths and claim.scope <= covered:
            return (REQUALIFIED, claim.scope,
                    f"{len(live)} independent admissible path(s) cover "
                    f"the full claimed scope")
        if live and claim.scope <= covered:
            # Full scope covered but fewer independent paths than the bar.
            return (INSUFFICIENT_DATA, covered,
                    f"only {len(live)}/{claim.min_paths} independent "
                    f"path(s): evidence valid but too little for the bar")
        if covered:
            # Surviving evidence covers only part of the claimed scope:
            # narrow the claim explicitly — never a fractional confidence.
            return (DOWNGRADED, covered,
                    f"scope narrowed to {sorted(covered)}: surviving "
                    f"evidence does not cover {sorted(claim.scope - covered)}")
        if suspended_paths:
            freshness = any(st == PATH_FRESHNESS
                            for st in states)
            if freshness:
                return (SUSPENDED, frozenset(),
                        "freshness reassessment required — expired evidence "
                        "is never auto-revoked")
            return (SUSPENDED, frozenset(),
                    "possible contamination: held pending investigation — "
                    "suspended, not destroyed")
        return (REVOKED, frozenset(),
                "no admissible support path remains")

    def _topological_order(self, affected: set[str]) -> list[str]:
        order: list[str] = []
        visited: set[str] = set()

        def visit(cid: str) -> None:
            if cid in visited:
                return
            visited.add(cid)
            for dep in self._claims[cid].depends_on:
                if dep in affected:
                    visit(dep)
            order.append(cid)

        for cid in sorted(affected):
            visit(cid)
        return order

    # -- reads --------------------------------------------------------------

    def qualification(self, claim_id: str) -> QualificationRecord:
        return self._records[claim_id]

    def history(self, claim_id: str) -> tuple[QualificationRecord, ...]:
        """Both 'what did we believe then' and 'what now' — immutable."""
        return tuple(self._history[claim_id])

    def issue_certificate(self, claim_id: str) -> Certificate:
        rec = self._records[claim_id]
        return Certificate(claim_id, rec.verdict, rec.covered_scope,
                           rec.policy_version)

    def check_at_use(self, cert: Certificate) -> str:
        """Eligibility re-enforced at consequential use. A certificate pinned
        to an older policy version is stale the moment the world changed."""
        current = self._records[cert.claim_id]
        if cert.policy_version != self.policy_version:
            return CERT_STALE_VERSION
        if cert.verdict != current.verdict or \
                cert.covered_scope != current.covered_scope:
            return CERT_VERDICT_CHANGED
        return CERT_ACCEPTED

    def authorize_act(self, claim_id: str, cert: Certificate) -> str:
        """The ACT commit-boundary check: re-verify qualification at the
        instant of use, closing the TOCTOU race between check and act."""
        if self.check_at_use(cert) != CERT_ACCEPTED:
            return ACT_REFUSED
        if cert.verdict not in CERTIFYING_VERDICTS:
            return ACT_REFUSED
        return ACT_AUTHORIZED
