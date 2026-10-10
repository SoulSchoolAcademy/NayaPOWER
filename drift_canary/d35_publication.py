"""D35 — Preventing Stale Qualifications From Being Republished (spec fixture).

THE JOB: Enforce monotonic qualification revision, atomic publication checks,
and mandatory read-time freshness checks across every intelligence projection.

CORE RULE: No cached artifact, background worker, concurrent writer, or
successor may publish or reuse a qualification unless its evidence
dependencies are valid at the moment of publication or consequential use.
Older evidence can remain in history, but it cannot regain current authority
through a delayed write.

  StaleWriter             -> RejectPublication
  RevokedEvidence         -> NoStaleCertification
  IndependentValidSupport -> PreserveSupportedClaim

This is a DISTRIBUTED CONSISTENCY problem, not a cache-expiration problem:
a cache accurate when generated can be dangerous by publication time.

Architecture:
  RevisionAuthority    — one shared authority allocates three MONOTONIC
                         revision streams: evidence eligibility / claim
                         qualification / projection. Statuses are NOT
                         monotonic (SUSPENDED may return to REQUALIFIED) —
                         but every transition takes a NEWER revision plus new
                         evidence. The history is monotonic; the status is not.
  FencingToken         — issued at read time; proves "I read at triple T". A
                         valid token NEVER replaces the evidence-version check.
  PublicationAuthority — the atomic publication boundary. Every publish is a
                         compare-and-swap evaluated against ONE consistent
                         snapshot:
                           PublishAllowed = ProjectionHeadMatches
                                          ∧ QualificationDependenciesCurrent
                                          ∧ EvidenceDependenciesAdmissible
                         On failure: STALE_DEPENDENCY or WRITE_CONFLICT. The
                         writer rebases and recomputes — never blindly retries.
  Revocation ordering  — revocation is effective BEFORE cache refresh
                         completes: synchronous invalidation + async repair +
                         read-time verification. Invariant:
                           PublishedCurrent(P) ⇒ ValidDependencies(P, now)

Per-surface publication rules:
  summary            — compare-and-swap against the projection head
  smart_note         — append-only with idempotent event IDs (replay = dedupe)
  index              — atomic pointer replacement (no torn reads)
  successor_package  — sealed at build; MANDATORY reconciliation at use

Crash recovery: transactional outbox (intent recorded before application;
replayed exactly once on recovery), idempotent refresh, reconciliation job.
Notification loss may DELAY refresh but must never RESTORE eligibility.

Composes with D33's concepts (eligibility revocation, support paths) and the
on-main contracts. SPEC + fixture machinery only — not wired into any live
path. No existing contracts changed.
"""
from __future__ import annotations

from dataclasses import dataclass, field

# --- Verdict vocabulary: imported from the on-main contract, asserted identical
# at import so this fixture can never drift into a competing verdict set. ---
from drift_canary import revocation as _revocation
from drift_canary import propagation as _propagation

assert _revocation.VERDICTS == (
    "UNAFFECTED",
    "REQUALIFIED",
    "DOWNGRADED",
    "INSUFFICIENT_DATA",
    "SUSPENDED",
    "REVOKED",
), "D35 requires the on-main six-verdict vocabulary"
assert set(_propagation.SURFACE_RULES) >= {
    "summary", "index", "smart_note", "successor_package",
}, "D35 requires the on-main four-surface rules"

VERDICTS = _revocation.VERDICTS

# Publication outcomes.
PUBLISHED = "PUBLISHED"
STALE_DEPENDENCY = "STALE_DEPENDENCY"   # a dependency moved under the writer
WRITE_CONFLICT = "WRITE_CONFLICT"       # the projection head moved
TOKEN_REJECTED = "TOKEN_REJECTED"       # forged / wrong-authority token
SCOPE_VIOLATION = "SCOPE_VIOLATION"     # publish claims more than evidence supports
DUPLICATE_EVENT = "DUPLICATE_EVENT"     # idempotent replay, safely deduped

# Fragment currency.
CURRENT = "CURRENT"
INVALID = "INVALID"     # synchronously invalidated by a revocation
REPAIRED = "REPAIRED"   # async repair recomputed and republished


@dataclass(frozen=True)
class RevisionTriple:
    """One consistent snapshot of the three authority-allocated streams."""
    evidence_rev: int
    qualification_rev: int
    projection_rev: int

    def __le__(self, other: "RevisionTriple") -> bool:
        return (self.evidence_rev <= other.evidence_rev
                and self.qualification_rev <= other.qualification_rev
                and self.projection_rev <= other.projection_rev)


class RevisionAuthority:
    """The single shared authority that allocates monotonic revisions.

    Three INDEPENDENT streams: an evidence revocation must not consume
    qualification revisions, and a publication must not consume evidence
    revisions. Each stream starts at 1 and only moves forward.
    """

    def __init__(self) -> None:
        self._evidence_rev = 0
        self._qualification_rev = 0
        self._projection_rev = 0
        self._token_seq = 0

    def bump_evidence(self) -> int:
        self._evidence_rev += 1
        return self._evidence_rev

    def bump_qualification(self) -> int:
        self._qualification_rev += 1
        return self._qualification_rev

    def bump_projection(self) -> int:
        self._projection_rev += 1
        return self._projection_rev

    def current(self) -> RevisionTriple:
        return RevisionTriple(self._evidence_rev, self._qualification_rev,
                              self._projection_rev)

    def issue_fencing_token(self, worker_id: str) -> "FencingToken":
        """A token proves WHEN a worker read. It grants no publication right
        beyond what the version checks allow — tokens don't replace
        evidence-version checks."""
        self._token_seq += 1
        return FencingToken(token_id=f"tok-{self._token_seq}",
                            worker_id=worker_id,
                            issued_at=self.current(),
                            authority_id=id(self))


@dataclass(frozen=True)
class FencingToken:
    token_id: str
    worker_id: str
    issued_at: RevisionTriple
    authority_id: int


@dataclass
class EvidenceRecord:
    ev_id: str
    eligible: bool = True
    evidence_rev: int = 0   # rev at which eligibility was last set


@dataclass
class QualificationRecord:
    claim_id: str
    verdict: str
    qualification_rev: int
    # evidence dependencies pinned at qualification time: ev_id -> ev_rev
    evidence_deps: dict = field(default_factory=dict)
    scope: frozenset = frozenset()


@dataclass
class FragmentManifest:
    """Per-fragment dependency manifest. Fragments are the unit of
    selectivity: an unaffected fragment survives without a global rebuild."""
    fragment_id: str
    claim_id: str
    qualification_rev_at_read: int
    evidence_deps_at_read: dict      # ev_id -> ev_rev pinned at read
    projection_head_at_read: int
    scope_at_read: frozenset = frozenset()   # qualified scope the writer saw
    token: FencingToken = None


@dataclass
class ProjectionFragment:
    fragment_id: str
    surface: str            # summary | smart_note | index | successor_package
    content: str
    manifest: FragmentManifest
    status: str = CURRENT   # CURRENT | INVALID | REPAIRED


@dataclass
class PublicationOutcome:
    ok: bool
    reason: str             # PUBLISHED | STALE_DEPENDENCY | WRITE_CONFLICT | ...
    fragment_id: str = ""
    projection_rev: int = 0
    detail: str = ""


class PublicationAuthority:
    """The atomic publication boundary.

    All state transitions that matter happen here, against one consistent
    snapshot per operation. In this fixture "atomic" is modeled by evaluating
    the full CAS predicate against a single snapshot taken at operation start
    — no interleaving is possible inside one publish() call, which is exactly
    the guarantee a real atomic boundary must provide.
    """

    def __init__(self) -> None:
        self.revisions = RevisionAuthority()
        self.evidence: dict[str, EvidenceRecord] = {}
        self.qualifications: dict[str, QualificationRecord] = {}
        self.fragments: dict[str, ProjectionFragment] = {}
        self.projection_head: int = 0
        self.seen_event_ids: set[str] = set()   # smart-note idempotency
        self.index_pointer: str | None = None   # atomic pointer replacement
        self.outbox: list[dict] = []            # transactional outbox
        self.applied_intents: set[str] = set()  # exactly-once tracking

    # ------------------------------------------------------------------
    # Setup / qualification lifecycle
    # ------------------------------------------------------------------
    def register_evidence(self, ev_id: str) -> EvidenceRecord:
        rev = self.revisions.bump_evidence()
        rec = EvidenceRecord(ev_id=ev_id, eligible=True, evidence_rev=rev)
        self.evidence[ev_id] = rec
        return rec

    def qualify(self, claim_id: str, verdict: str,
                evidence_ids: tuple[str, ...], scope: frozenset = frozenset()
                ) -> QualificationRecord:
        """(Re)qualify a claim. Every transition — including SUSPENDED back to
        REQUALIFIED — takes a NEWER revision plus the then-current evidence
        pins. Statuses aren't monotonic; the history is."""
        assert verdict in VERDICTS, f"unknown verdict {verdict}"
        deps = {}
        for eid in evidence_ids:
            rec = self.evidence.get(eid)
            assert rec is not None, f"unknown evidence {eid}"
            assert rec.eligible, f"cannot qualify on ineligible evidence {eid}"
            deps[eid] = rec.evidence_rev
        rev = self.revisions.bump_qualification()
        q = QualificationRecord(claim_id=claim_id, verdict=verdict,
                                qualification_rev=rev,
                                evidence_deps=deps, scope=scope)
        self.qualifications[claim_id] = q
        return q

    def revoke_evidence(self, ev_id: str) -> int:
        """Revocation is effective BEFORE cache refresh completes.

        Synchronous part (this call): bump the evidence stream and mark every
        fragment whose manifest pinned the old eligibility INVALID. Async
        repair (recompute + republish) happens separately via
        repair_fragment(). Notification loss may delay repair — it can never
        restore eligibility.
        """
        rec = self.evidence.get(ev_id)
        assert rec is not None, f"unknown evidence {ev_id}"
        rec.eligible = False
        new_rev = self.revisions.bump_evidence()
        rec.evidence_rev = new_rev
        # Synchronous invalidation: any fragment depending on this evidence
        # is INVALID as of NOW, before any refresh runs.
        for frag in self.fragments.values():
            if frag.status == CURRENT and ev_id in frag.manifest.evidence_deps_at_read:
                frag.status = INVALID
        return new_rev

    # ------------------------------------------------------------------
    # Read path: read-time freshness verification
    # ------------------------------------------------------------------
    def read_for_write(self, claim_id: str, worker_id: str
                       ) -> tuple[FragmentManifest, FencingToken]:
        """A worker reads the claim's current qualification and receives a
        fencing token. The manifest pins exactly what the writer saw."""
        q = self.qualifications.get(claim_id)
        assert q is not None, f"unknown claim {claim_id}"
        token = self.revisions.issue_fencing_token(worker_id)
        manifest = FragmentManifest(
            fragment_id=f"frag-{claim_id}-{token.token_id}",
            claim_id=claim_id,
            qualification_rev_at_read=q.qualification_rev,
            evidence_deps_at_read=dict(q.evidence_deps),
            projection_head_at_read=self.projection_head,
            scope_at_read=q.scope,
            token=token,
        )
        return manifest, token

    def read_current(self, fragment_id: str) -> str:
        """Read-time verification: a CURRENT fragment is re-checked against
        live state on every read. Returns CURRENT or INVALID."""
        frag = self.fragments.get(fragment_id)
        if frag is None or frag.status != CURRENT:
            return INVALID
        if not self._dependencies_valid(frag.manifest):
            frag.status = INVALID
            return INVALID
        return CURRENT

    # ------------------------------------------------------------------
    # The atomic publication boundary
    # ------------------------------------------------------------------
    def _token_valid(self, token: FencingToken) -> bool:
        return token.authority_id == id(self.revisions)

    def _dependencies_valid(self, manifest: FragmentManifest) -> bool:
        """QualificationDependenciesCurrent ∧ EvidenceDependenciesAdmissible."""
        q = self.qualifications.get(manifest.claim_id)
        if q is None:
            return False
        if q.qualification_rev != manifest.qualification_rev_at_read:
            return False
        for eid, pinned_rev in manifest.evidence_deps_at_read.items():
            rec = self.evidence.get(eid)
            if rec is None or not rec.eligible:
                return False
            if rec.evidence_rev != pinned_rev:
                return False
        return True

    def publish_summary(self, manifest: FragmentManifest, content: str,
                        scope: frozenset) -> PublicationOutcome:
        """Summaries publish by compare-and-swap against the projection head.

        PublishAllowed = ProjectionHeadMatches
                       ∧ QualificationDependenciesCurrent
                       ∧ EvidenceDependenciesAdmissible, evaluated atomically.
        """
        if not self._token_valid(manifest.token):
            return PublicationOutcome(False, TOKEN_REJECTED,
                                      manifest.fragment_id,
                                      detail="token not issued by this authority")
        # Scope check against what the writer actually saw: a publication
        # may never claim more than its pinned evidence supports. Currency is
        # judged by the CAS predicate below, not by re-scoping against a
        # qualification the writer never read.
        if not scope <= manifest.scope_at_read:
            return PublicationOutcome(False, SCOPE_VIOLATION,
                                      manifest.fragment_id,
                                      detail="scope exceeds the qualified scope "
                                             "pinned at read time")
        # Atomic CAS predicate against one consistent snapshot.
        if manifest.projection_head_at_read != self.projection_head:
            return PublicationOutcome(False, WRITE_CONFLICT,
                                      manifest.fragment_id,
                                      detail="projection head moved; rebase required")
        if not self._dependencies_valid(manifest):
            return PublicationOutcome(False, STALE_DEPENDENCY,
                                      manifest.fragment_id,
                                      detail="qualification or evidence revision "
                                             "moved under the writer")
        # All three hold: commit.
        new_head = self.revisions.bump_projection()
        self.projection_head = new_head
        frag = ProjectionFragment(fragment_id=manifest.fragment_id,
                                  surface="summary", content=content,
                                  manifest=manifest, status=CURRENT)
        self.fragments[frag.fragment_id] = frag
        return PublicationOutcome(True, PUBLISHED, frag.fragment_id,
                                  projection_rev=new_head)

    def append_smart_note(self, event_id: str, claim_id: str, content: str
                          ) -> PublicationOutcome:
        """Smart notes are append-only with idempotent event IDs: replaying
        the same event is a safe no-op, never a double application."""
        if event_id in self.seen_event_ids:
            return PublicationOutcome(False, DUPLICATE_EVENT, "",
                                      detail=f"event {event_id} already applied")
        self.seen_event_ids.add(event_id)
        new_head = self.revisions.bump_projection()
        self.projection_head = new_head
        return PublicationOutcome(True, PUBLISHED, f"note-{event_id}",
                                  projection_rev=new_head)

    def replace_index_pointer(self, new_pointer: str,
                              expected_old: str | None) -> PublicationOutcome:
        """Indexes publish by atomic pointer replacement: readers see the old
        pointer or the new pointer, never a torn index."""
        if self.index_pointer != expected_old:
            return PublicationOutcome(False, WRITE_CONFLICT, "",
                                      detail="index pointer moved; rebase required")
        self.index_pointer = new_pointer
        new_head = self.revisions.bump_projection()
        self.projection_head = new_head
        return PublicationOutcome(True, PUBLISHED, f"index->{new_pointer}",
                                  projection_rev=new_head)

    # ------------------------------------------------------------------
    # Successor packages: sealed at build, reconciled at use
    # ------------------------------------------------------------------
    def seal_successor_package(self, claim_id: str) -> dict:
        """Seal the package with the full revision triple and dependency pins.
        Sealing confers NO current authority — only history."""
        q = self.qualifications.get(claim_id)
        assert q is not None, f"unknown claim {claim_id}"
        return {
            "claim_id": claim_id,
            "verdict_at_seal": q.verdict,
            "sealed_triple": self.revisions.current(),
            "qualification_rev_at_seal": q.qualification_rev,
            "evidence_pins": dict(q.evidence_deps),
            "scope": q.scope,
        }

    def reconcile_package(self, package: dict) -> PublicationOutcome:
        """MANDATORY reconciliation before a successor treats a sealed package
        as current certification. A package sealed at R5 MUST fail against R8
        state. History remains readable; current certification is withheld."""
        claim_id = package["claim_id"]
        q = self.qualifications.get(claim_id)
        if q is None:
            return PublicationOutcome(False, STALE_DEPENDENCY, "",
                                      detail="claim unknown at reconcile time")
        if q.qualification_rev != package["qualification_rev_at_seal"]:
            return PublicationOutcome(False, STALE_DEPENDENCY, "",
                                      detail="qualification revision moved "
                                             "since seal")
        for eid, pinned_rev in package["evidence_pins"].items():
            rec = self.evidence.get(eid)
            if rec is None or not rec.eligible or rec.evidence_rev != pinned_rev:
                return PublicationOutcome(False, STALE_DEPENDENCY, "",
                                          detail=f"evidence {eid} no longer "
                                                 "admissible")
        return PublicationOutcome(True, PUBLISHED, "",
                                  detail="package reconciles with current state")

    # ------------------------------------------------------------------
    # Async repair + crash recovery
    # ------------------------------------------------------------------
    def repair_fragment(self, fragment_id: str, worker_id: str
                        ) -> PublicationOutcome:
        """Async repair path: re-read current state, recompute, and republish
        through the same atomic boundary. A repaired fragment gets a fresh
        manifest — repair never resurrects a stale one."""
        frag = self.fragments.get(fragment_id)
        if frag is None:
            return PublicationOutcome(False, STALE_DEPENDENCY, fragment_id,
                                      detail="unknown fragment")
        manifest, _ = self.read_for_write(frag.manifest.claim_id, worker_id)
        new_manifest = FragmentManifest(
            fragment_id=fragment_id,
            claim_id=manifest.claim_id,
            qualification_rev_at_read=manifest.qualification_rev_at_read,
            evidence_deps_at_read=manifest.evidence_deps_at_read,
            projection_head_at_read=manifest.projection_head_at_read,
            scope_at_read=manifest.scope_at_read,
            token=manifest.token,
        )
        frag.manifest = new_manifest
        frag.status = REPAIRED
        # Repair republishes through the CAS boundary like any other write.
        out = self.publish_summary(
            new_manifest, frag.content + " [repaired]",
            self.qualifications[frag.manifest.claim_id].scope)
        if out.ok:
            frag.status = CURRENT
        return out

    def record_intent(self, intent_id: str, op: str, payload: dict) -> None:
        """Transactional outbox: the intent is recorded BEFORE application."""
        self.outbox.append({"intent_id": intent_id, "op": op,
                            "payload": payload})

    def recover(self) -> list[str]:
        """Crash recovery: replay outbox intents exactly once. Intents whose
        preconditions no longer hold are skipped, never force-applied."""
        replayed = []
        for intent in self.outbox:
            iid = intent["intent_id"]
            if iid in self.applied_intents:
                continue  # already applied before the crash
            if intent["op"] == "append_smart_note":
                out = self.append_smart_note(iid, intent["payload"]["claim_id"],
                                             intent["payload"]["content"])
                if out.ok or out.reason == DUPLICATE_EVENT:
                    self.applied_intents.add(iid)
                    replayed.append(iid)
            # Unknown or precondition-failed intents are left for the
            # reconciliation job; never force-applied.
        return replayed

    # ------------------------------------------------------------------
    # The invariant, checkable after every operation
    # ------------------------------------------------------------------
    def assert_invariant(self) -> None:
        """PublishedCurrent(P) ⇒ ValidDependencies(P, current state).

        Every fragment marked CURRENT must have live-valid dependencies.
        Raises AssertionError naming the violator — a stale write that became
        current authority is a system failure, not a test failure.
        """
        for fid, frag in self.fragments.items():
            if frag.status == CURRENT and not self._dependencies_valid(frag.manifest):
                raise AssertionError(
                    f"INVARIANT VIOLATED: fragment {fid} is CURRENT with "
                    f"invalid dependencies — a stale write became authority")
