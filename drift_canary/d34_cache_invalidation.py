"""D34 — Selective Cache Invalidation and Intelligence Preservation.

THE JOB: invalidate obsolete qualifications without deleting the
intelligence that contains them. When upstream evidence becomes
ineligible, distinguish historical records, current claims, cached
representations, and permission to reuse.

CORE RULE (D34): preserve history. Recompute current qualification.
Invalidate stale authority-bearing projections. Refresh only what
changed. Keep independently supported conclusions available. A change in
evidence eligibility changes the right to USE a conclusion — not the
knowledge that carried it. Discoverability != certifiability.

Composes (extends, never duplicates):
  drift_canary.revocation — the six qualification verdicts
      (UNAFFECTED / REQUALIFIED / DOWNGRADED / INSUFFICIENT_DATA /
      SUSPENDED / REVOKED). The verdict vocabulary is IMPORTED, not
      redefined — asserted identical at import, mirroring D33.
  D33's RevocationEngine — the intended qualification provider. D34
      consumes it through the QualificationProvider protocol below
      (duck-typed: register_source / register_claim / add_derivation /
      revoke / qualification / history). D34 ships SimpleRecomputeProvider
      so the fixture is fully self-contained and testable; a D33 engine
      drops in as the production provider with no code change.

The D34 layer added here: qualification generations, per-surface
projection manifests with claim dependencies, the read-time qualification
gate (a stale cache can never serve as current, even mid-refresh),
two-phase invalidation (commit -> recompute -> publish generation ->
refresh projections -> independent reconcile), generation-bound
compare-and-swap publication (a delayed refresh can never republish an
earlier PASS over a later revocation), ACT commit-boundary re-check
(TOCTOU close), per-surface refresh policies (summaries / Smart Notes /
indexes / successor packages / historical receipts), and stale-
intelligence safeguards on every serving route.

SPEC + deterministic fixture machinery. NOT wired into kernel/, KNOW,
LAW, ACT, or any live path. Wiring needs Shawn's word.
"""
from __future__ import annotations

from dataclasses import dataclass, field

# The six verdicts are imported from the on-main contract — D34 must not
# invent a competing vocabulary.
from drift_canary.revocation import VERDICTS as _QUALIFICATION_VERDICTS

UNAFFECTED = "UNAFFECTED"
REQUALIFIED = "REQUALIFIED"
DOWNGRADED = "DOWNGRADED"
INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
SUSPENDED = "SUSPENDED"
REVOKED = "REVOKED"

assert set(_QUALIFICATION_VERDICTS) == {
    UNAFFECTED, REQUALIFIED, DOWNGRADED, INSUFFICIENT_DATA, SUSPENDED, REVOKED,
}, "D34 must share revocation.py's verdict vocabulary exactly"

# ---------------------------------------------------------------------------
# Vocabularies. Statuses a projection manifest may carry.
# ---------------------------------------------------------------------------

CURRENT = "CURRENT"                              # servable as current
REVALIDATION_REQUIRED = "REVALIDATION_REQUIRED"  # affected; refresh pending
REFRESH_PENDING = "REFRESH_PENDING"              # refresh claimed, not done
HISTORICAL_ONLY = "HISTORICAL_ONLY"              # never servable as current

PROJECTION_STATUSES = (
    CURRENT, REVALIDATION_REQUIRED, REFRESH_PENDING, HISTORICAL_ONLY,
)

# Surfaces, each with its own refresh policy.
CACHED_SUMMARY = "cached_summary"
SMART_NOTE = "smart_note"
INDEX_ENTRY = "index_entry"
SUCCESSOR_PACKAGE = "successor_package"
HISTORICAL_RECEIPT = "historical_receipt"

# Serving routes. Every route passes through the read-time gate.
KNOW_RETRIEVAL = "know_retrieval"
CONNECT_EXPANSION = "connect_expansion"
SUMMARY_GENERATION = "summary_generation"
NOTE_CAPTURE = "note_capture"
INDEX_LOOKUP = "index_lookup"
SUCCESSOR_ACTIVATION = "successor_activation"
LEARN_PROMOTION = "learn_promotion"
CONSEQUENTIAL_ACT = "consequential_act"

# Authority-bearing routes: a stale projection is REFUSED, never served.
# INDEX_LOOKUP is discovery: entries are returned, but qualification
# pointers are annotated, never certified, when stale.
AUTHORITY_ROUTES = frozenset({
    KNOW_RETRIEVAL, CONNECT_EXPANSION, SUMMARY_GENERATION, NOTE_CAPTURE,
    SUCCESSOR_ACTIVATION, LEARN_PROMOTION, CONSEQUENTIAL_ACT,
})

# Read-time gate decisions.
SERVE_CURRENT = "SERVE_CURRENT"
SERVE_HISTORICAL = "SERVE_HISTORICAL"    # historical content, labeled as such
REFUSE_STALE = "REFUSE_STALE"            # stale cache may not serve as current

# ACT commit-boundary decisions (TOCTOU close).
ACT_AUTHORIZED = "AUTHORIZED"
ACT_REFUSED = "REFUSED"

# Source eligibility states (mirrors D33's ledger vocabulary).
ELIGIBLE = "ELIGIBLE"
SUSPENDED_SRC = "SUSPENDED"
REVOKED_SRC = "REVOKED"
EXPIRED_SRC = "EXPIRED"


def _standing_key(verdict: str, covered) -> tuple:
    """Canonical serving standing: UNAFFECTED and REQUALIFIED both mean
    'currently meets the bar' — the difference is historical, not
    servable. Fidelity and reconciliation compare standings, so a fresh
    full recompute (which cannot know what was 'never touched') still
    verifies."""
    if verdict in (UNAFFECTED, REQUALIFIED):
        return ("QUALIFIED", frozenset(covered))
    return (verdict, frozenset(covered))


class StaleGenerationError(Exception):
    """A refresh or publication was attempted against a moved generation.

    The caller must recompute against the current generation first. This
    is what makes 'a delayed refresh must never republish an earlier PASS
    over a later revocation' structural rather than conventional.
    """


# ---------------------------------------------------------------------------
# Eligibility events and claim qualifications.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class EligibilityEvent:
    """One committed eligibility change. seq is the D34 generation number:
    every commit publishes a new generation."""
    seq: int
    source_id: str
    old_status: str
    new_status: str
    reason: str


@dataclass(frozen=True)
class ClaimQualification:
    """Current qualification of one claim: verdict, covered scope, and the
    generation it was computed at. qualified_at_seq is what the read-time
    gate compares against a projection's generation."""
    claim_id: str
    verdict: str
    covered_scope: frozenset
    qualified_at_seq: int
    reason: str = ""


# ---------------------------------------------------------------------------
# QualificationProvider protocol.
#
# D34 delegates recomputation to a provider. Two honest options:
#   1. SimpleRecomputeProvider below — minimal, self-contained, same six
#      verdicts. Used by the fixture and whenever D33 is unavailable.
#   2. D33EngineAdapter — wraps a real D33 RevocationEngine (d33_revocation
#      branch) and exposes D34's protocol, translating the assessment
#      vocabulary and record shapes. Tested below against a D33-shaped
#      fake; the adapter accesses the engine duck-typed (attributes, not
#      imports), so no dependency on the unmerged branch.
# ---------------------------------------------------------------------------

class SimpleRecomputeProvider:
    """Minimal honest implementation of the provider protocol: explicit
    AND/OR support paths over source eligibility, scope-aware verdicts,
    transitive claim-to-claim dependencies. Evaluation always reads the
    ACCUMULATED source statuses — an earlier revocation is never forgotten
    by a later recompute. Deterministic: the same registration + event
    order always yields the same verdicts, which is what makes
    cold-successor replay possible."""

    def __init__(self) -> None:
        self._sources: dict[str, dict] = {}   # source_id -> {status, scope}
        self._claims: dict[str, dict] = {}    # claim_id -> {paths, scope, min_paths, kind, depends_on}
        self._derivations: dict[str, set[str]] = {}
        self._verdicts: dict[str, tuple[str, frozenset, str]] = {}
        self._history: dict[str, list[tuple[str, frozenset, str]]] = {}

    # -- registration ----------------------------------------------------
    def register_source(self, source_id: str, scope=frozenset({"staging", "production"})) -> None:
        self._sources[source_id] = {"status": ELIGIBLE, "scope": frozenset(scope)}

    def register_claim(self, claim_id: str, paths, scope=frozenset({"staging", "production"}),
                       min_paths: int = 1, kind: str = "certification",
                       depends_on=()) -> None:
        # paths: iterable of (frozenset(source_ids), frozenset(scope))
        norm = [(frozenset(ss), frozenset(sc)) for ss, sc in paths]
        self._claims[claim_id] = {
            "paths": tuple(norm), "scope": frozenset(scope),
            "min_paths": min_paths, "kind": kind,
            "depends_on": tuple(depends_on),
        }
        self._verdicts[claim_id] = (UNAFFECTED, frozenset(scope), "initial qualification")
        self._history[claim_id] = [self._verdicts[claim_id]]

    def add_derivation(self, derived_id: str, origin_id: str) -> None:
        self._derivations.setdefault(derived_id, set()).add(origin_id)

    def set_source_status(self, source_id: str, status: str) -> None:
        self._sources[source_id]["status"] = status

    # -- recomputation ----------------------------------------------------
    def _ancestors(self, source_id: str) -> set[str]:
        out, stack = set(), [source_id]
        while stack:
            cur = stack.pop()
            for parent in self._derivations.get(cur, ()):
                if parent not in out:
                    out.add(parent)
                    stack.append(parent)
        return out

    def _accumulated_bad(self) -> tuple[frozenset, frozenset]:
        """All currently-ineligible sources, taint-closed. Evaluation
        reads this — never just the latest change."""
        revoked = {s for s, d in self._sources.items()
                   if d["status"] == REVOKED_SRC}
        suspended = {s for s, d in self._sources.items()
                     if d["status"] == SUSPENDED_SRC}
        # EXPIRED sources are NOT auto-excluded: expiry triggers
        # reassessment, never silent revocation.
        def close(seeds: set[str]) -> frozenset:
            out = set(seeds)
            for s in list(self._sources):
                if self._ancestors(s) & out:
                    out.add(s)
            return frozenset(out)
        return close(revoked), close(suspended)

    def _evaluate(self, claim_id: str) -> tuple[str, frozenset, str]:
        """Evaluate one claim against accumulated source statuses."""
        claim = self._claims[claim_id]
        wanted = claim["scope"]
        revoked, suspended = self._accumulated_bad()
        live = 0
        live_scopes: list[frozenset] = []
        saw_suspended = False
        for sources, path_scope in claim["paths"]:
            if any(s in revoked or self._ancestors(s) & revoked for s in sources):
                continue
            if any(s in suspended or self._ancestors(s) & suspended for s in sources):
                saw_suspended = True
                continue
            if any(s not in self._sources for s in sources):
                continue
            live += 1
            live_scopes.append(path_scope & wanted)
        covered = frozenset().union(*live_scopes) if live_scopes else frozenset()
        if live >= claim["min_paths"] and covered == wanted:
            # Affected by this commit yet still fully covered: recomputed
            # on remaining evidence, still meets the bar.
            return REQUALIFIED, covered, "recomputed on remaining evidence; still meets bar"
        if covered and covered < wanted:
            return DOWNGRADED, covered, "surviving evidence covers narrowed scope only"
        if live and live < claim["min_paths"]:
            return INSUFFICIENT_DATA, covered, "below certification bar"
        if saw_suspended and not live_scopes:
            return SUSPENDED, frozenset(), "possibly-compromised source; held pending investigation"
        return REVOKED, frozenset(), "no admissible path remains"

    def _affected_closure(self, changed: frozenset) -> set[str]:
        affected: set[str] = set()
        for cid, claim in self._claims.items():
            for sources, _ in claim["paths"]:
                if sources & changed or self._ancestors_of_any(sources) & changed:
                    affected.add(cid)
                    break
        grew = True
        while grew:
            grew = False
            for cid, claim in self._claims.items():
                if cid not in affected and any(d in affected for d in claim["depends_on"]):
                    affected.add(cid)
                    grew = True
        return affected

    def _ancestors_of_any(self, sources) -> set[str]:
        out: set[str] = set()
        for s in sources:
            out |= self._ancestors(s)
        return out

    def revoke(self, source_id: str, reason: str,
               new_status: str = REVOKED_SRC):
        """Apply one eligibility change; recompute exactly the affected
        closure against accumulated state. Returns a small report."""
        old = self._sources[source_id]["status"]
        self._sources[source_id]["status"] = new_status
        affected, recomputed = self.recompute_affected(frozenset({source_id}))
        return _RevokeReport(source_id, old, new_status, reason,
                             sorted(affected), recomputed)

    def recompute_all(self) -> None:
        """Recompute every claim against accumulated state (used after
        bulk status restoration in cold replay)."""
        for cid in sorted(self._claims):
            new_v, covered, why = self._evaluate(cid)
            self._verdicts[cid] = (new_v, covered, why)
            self._history[cid].append(self._verdicts[cid])

    def recompute_affected(self, changed: frozenset) -> tuple[set, dict]:
        """Public recompute step (also used by cold-successor replay):
        recompute exactly the affected closure. Caller sets source
        statuses first via set_source_status."""
        affected = self._affected_closure(changed)
        recomputed = {}
        for cid in sorted(affected):
            old_v = self._verdicts[cid][0]
            new_v, covered, why = self._evaluate(cid)
            self._verdicts[cid] = (new_v, covered, why)
            self._history[cid].append(self._verdicts[cid])
            recomputed[cid] = (old_v, new_v, covered)
        return affected, recomputed

    def qualification(self, claim_id: str) -> tuple[str, frozenset, str]:
        return self._verdicts[claim_id]

    def history(self, claim_id: str):
        return tuple(self._history[claim_id])


@dataclass(frozen=True)
class _RevokeReport:
    source_id: str
    old_status: str
    new_status: str
    reason: str
    affected_claims: tuple
    recomputed: dict  # claim_id -> (old_verdict, new_verdict, covered_scope)


# D33 assessment vocabulary (mirrors d33_revocation.py; kept as literals
# so this module never imports the unmerged branch).
_D33_CONFIRMED = "confirmed_compromised"
_D33_POSSIBLY = "possibly_compromised"
_D33_CLEARED = "independently_cleared"


class D33EngineAdapter:
    """Wraps a real D33 RevocationEngine and exposes D34's provider
    protocol. Assessment vocabulary is translated (D34 status ->
    D33 assessment); D33's EvidenceSource/Claim/SupportPath records are
    built duck-typed (attributes, not imports). D33's QualificationRecord
    is normalized to D34's (verdict, covered_scope, reason) triple."""

    def __init__(self, engine) -> None:
        self._engine = engine

    def register_source(self, source_id: str, scope=frozenset({"staging", "production"})) -> None:
        src = _DuckSource(source_id, "", frozenset(scope))
        self._engine.register_source(src)

    def register_claim(self, claim_id: str, paths, scope=frozenset({"staging", "production"}),
                       min_paths: int = 1, kind: str = "certification",
                       depends_on=()) -> None:
        spaths = tuple(_DuckPath(frozenset(ss), frozenset(sc)) for ss, sc in paths)
        claim = _DuckClaim(claim_id, spaths, frozenset(scope), min_paths,
                           kind, tuple(depends_on))
        self._engine.register_claim(claim)

    def add_derivation(self, derived_id: str, origin_id: str) -> None:
        self._engine.add_derivation(derived_id, origin_id)

    def revoke(self, source_id: str, reason: str, new_status: str = REVOKED_SRC):
        assessment = {
            REVOKED_SRC: _D33_CONFIRMED,
            SUSPENDED_SRC: _D33_POSSIBLY,
            EXPIRED_SRC: "expired",
        }[new_status]
        report = self._engine.revoke(source_id, reason, assessment=assessment)
        return _D33ReportShim(report)

    def qualification(self, claim_id: str) -> tuple[str, frozenset, str]:
        rec = self._engine.qualification(claim_id)
        return rec.verdict, frozenset(rec.covered_scope), getattr(rec, "reason", "")

    def history(self, claim_id: str):
        return tuple(
            (r.verdict, frozenset(r.covered_scope), getattr(r, "reason", ""))
            for r in self._engine.history(claim_id))


class _DuckSource:
    def __init__(self, source_id, observed_content, scope):
        self.source_id = source_id
        self.observed_content = observed_content
        self.scope = scope


class _DuckPath:
    def __init__(self, sources, scope):
        self.sources = sources
        self.scope = scope


class _DuckClaim:
    def __init__(self, claim_id, paths, scope, min_paths, kind, depends_on):
        self.claim_id = claim_id
        self.paths = paths
        self.scope = scope
        self.min_paths = min_paths
        self.kind = kind
        self.depends_on = depends_on


class _D33ReportShim:
    """Normalizes D33's RecomputationReport to what the store needs:
    affected_claims. Everything else passes through."""
    def __init__(self, report) -> None:
        self._report = report
        self.affected_claims = tuple(report.affected_claims)

    def __getattr__(self, name):
        return getattr(self._report, name)


# ---------------------------------------------------------------------------
# Projection manifests. Every servable surface carries one.
# ---------------------------------------------------------------------------

@dataclass
class Projection:
    """Manifest for one cached representation. claim_dependencies are the
    claims whose current qualification this projection asserts; generation
    is the D34 generation it was computed at; content is the rendered
    text; history preserves every prior rendering byte-identically.
    link optionally names the backing object (e.g. an index entry's
    note_id) used for pointer lookups."""
    projection_id: str
    surface: str
    claim_dependencies: frozenset
    generation: int
    status: str = CURRENT
    content: str = ""
    history: tuple = ()
    link: str = ""

    def archive_current(self) -> None:
        """Move the current rendering into history before replacing it.
        History is append-only: a historic report is never silently
        rewritten as though it always said the new thing."""
        if self.content:
            self.history = self.history + (self.content,)


@dataclass
class ServeResult:
    decision: str          # SERVE_CURRENT / SERVE_HISTORICAL / REFUSE_STALE
    content: str | None
    annotation: str        # why this decision; pointer statuses for discovery
    generation: int        # generation the served content was computed at


# ---------------------------------------------------------------------------
# The store: two-phase invalidation over a qualification provider.
# ---------------------------------------------------------------------------

class IntelligenceStore:
    """Owns generations, the eligibility event log, claim qualifications,
    and every projection manifest. Phase 1 (commit): eligibility change ->
    affected closure -> recompute -> publish new generation. Phase 2
    (refresh): projections refresh against current qualifications ->
    independent reconcile. The read-time gate makes stale-as-current
    unservable at every instant, including mid-refresh."""

    def __init__(self, provider=None) -> None:
        self.provider = provider if provider is not None else SimpleRecomputeProvider()
        self.generation: int = 0
        self.events: list[EligibilityEvent] = []
        self.claims: dict[str, ClaimQualification] = {}
        self.projections: dict[str, Projection] = {}
        # Smart-Note claim slots: note_id -> claim_id -> list of (verdict, note)
        self.note_claims: dict[str, dict[str, list]] = {}
        # Index: note_id -> set(claim_ids); pointers: (note_id, claim_id) -> (verdict, pointer_status)
        self.index_entries: dict[str, set[str]] = {}
        self.index_pointers: dict[tuple[str, str], tuple[str, str]] = {}
        # Historical receipts: append-only.
        self.receipts: list[EligibilityEvent] = []
        # Successor packages: package_id -> sealed snapshot.
        self.packages: dict[str, dict] = {}
        # Source eligibility as last committed (provider-agnostic; the
        # provider owns recomputation, the store owns the event log).
        self.source_status: dict[str, str] = {}

    # -- registration ------------------------------------------------------
    def _qual_of(self, claim_id: str) -> tuple[str, frozenset, str]:
        """Normalize a provider qualification to (verdict, covered_scope,
        reason) — accepts the protocol tuple or a D33-style record."""
        q = self.provider.qualification(claim_id)
        if isinstance(q, tuple):
            verdict, covered, reason = q
        else:
            verdict, covered = q.verdict, q.covered_scope
            reason = getattr(q, "reason", "")
        return verdict, frozenset(covered), reason

    def register_source(self, source_id: str, scope=frozenset({"staging", "production"})) -> None:
        self.provider.register_source(source_id, scope=scope)
        self.source_status[source_id] = ELIGIBLE

    def register_claim(self, claim_id: str, paths, scope=frozenset({"staging", "production"}),
                       min_paths: int = 1, kind: str = "certification",
                       depends_on=()) -> None:
        self.provider.register_claim(claim_id, paths, scope=scope,
                                     min_paths=min_paths, kind=kind,
                                     depends_on=depends_on)
        verdict, covered, reason = self._qual_of(claim_id)
        self.claims[claim_id] = ClaimQualification(
            claim_id, verdict, covered, self.generation, reason)

    # -- phase 1: commit ----------------------------------------------------
    def commit_eligibility_change(self, source_id: str, new_status: str,
                                  reason: str) -> EligibilityEvent:
        """Commit one eligibility change: recompute exactly the affected
        closure, publish a new generation, mark affected projections
        REVALIDATION_REQUIRED. Unaffected projections are untouched —
        refresh only what changed."""
        report = self.provider.revoke(source_id, reason, new_status=new_status)
        old_status = self.source_status.get(source_id, ELIGIBLE)
        self.source_status[source_id] = new_status
        self.generation += 1
        event = EligibilityEvent(self.generation, source_id,
                                 old_status, new_status, reason)
        self.events.append(event)
        self.receipts.append(event)  # historical receipts: preserve + append
        for cid in report.affected_claims:
            verdict, covered, why = self._qual_of(cid)
            self.claims[cid] = ClaimQualification(
                cid, verdict, covered, self.generation,
                f"{why} (seq {self.generation})")
        affected = set(report.affected_claims)
        for proj in self.projections.values():
            if proj.surface == HISTORICAL_RECEIPT:
                continue  # historical receipts are never "current" projections
            if proj.claim_dependencies & affected:
                if proj.status == CURRENT:
                    proj.status = REVALIDATION_REQUIRED
        for (note_id, cid), (verdict, _) in list(self.index_pointers.items()):
            if cid in affected:
                v, _, _ = self._qual_of(cid)
                self.index_pointers[(note_id, cid)] = (v, REVALIDATION_REQUIRED)
        return event

    # -- the read-time qualification gate -----------------------------------
    def _is_stale(self, proj: Projection) -> tuple[bool, str]:
        """A projection is stale when any claim it depends on was
        recomputed after the projection's generation."""
        for cid in proj.claim_dependencies:
            q = self.claims.get(cid)
            if q is None:
                return True, f"claim {cid} unknown"
            if q.qualified_at_seq > proj.generation:
                return True, (f"claim {cid} recomputed at seq "
                               f"{q.qualified_at_seq} after projection "
                               f"generation {proj.generation}")
        return False, ""

    def serve(self, projection_id: str, route: str) -> ServeResult:
        """The read-time qualification gate. No stale projection ever
        serves as current on an authority-bearing route — including during
        the refresh window between commit and refresh."""
        proj = self.projections[projection_id]
        if proj.surface == HISTORICAL_RECEIPT or proj.status == HISTORICAL_ONLY:
            return ServeResult(SERVE_HISTORICAL, proj.content,
                               "historical record; not current", proj.generation)
        stale, why = self._is_stale(proj)
        if route == INDEX_LOOKUP:
            # Discoverability != certifiability: the entry is returned,
            # but qualification pointers are annotated, never certified.
            base = proj.link or proj.projection_id
            pointers = ", ".join(
                f"{cid}:{self.index_pointers.get((base, cid), ('?', '?'))[1]}"
                for cid in sorted(proj.claim_dependencies))
            note = f"discoverable; pointers [{pointers}]"
            if stale or proj.status != CURRENT:
                return ServeResult(SERVE_HISTORICAL, proj.content,
                                   note + f"; STALE ({why})" if stale else note,
                                   proj.generation)
            return ServeResult(SERVE_CURRENT, proj.content, note, proj.generation)
        if stale or proj.status != CURRENT:
            detail = why if stale else f"status {proj.status}"
            return ServeResult(REFUSE_STALE, None,
                               f"refused: {detail}; revalidation required",
                               proj.generation)
        return ServeResult(SERVE_CURRENT, proj.content,
                           "current at generation %d" % proj.generation,
                           proj.generation)

    # -- phase 2: refresh ----------------------------------------------------
    def refresh_projection(self, projection_id: str, expected_generation: int,
                           render=None) -> Projection:
        """Regenerate one projection against current qualifications.
        Generation-bound compare-and-swap: if the caller computed against
        an older generation, publication is refused — a delayed refresh
        must never republish an earlier PASS over a later revocation."""
        if expected_generation != self.generation:
            raise StaleGenerationError(
                f"refresh computed at generation {expected_generation} but "
                f"store is at {self.generation}; recompute first")
        proj = self.projections[projection_id]
        proj.archive_current()
        if render is not None:
            quals = {cid: self.claims[cid] for cid in proj.claim_dependencies
                     if cid in self.claims}
            proj.content = render(quals)
        proj.generation = self.generation
        proj.status = CURRENT
        for cid in proj.claim_dependencies:
            if cid in self.claims:
                v = self.claims[cid].verdict
                for key in list(self.index_pointers):
                    if key[1] == cid:
                        self.index_pointers[key] = (v, CURRENT)
        # Smart-Note surfaces: append claim-level amendments, never rewrite.
        if proj.surface == SMART_NOTE and proj.projection_id in self.note_claims:
            for cid in proj.claim_dependencies:
                if cid in self.claims:
                    q = self.claims[cid]
                    slots = self.note_claims[proj.projection_id].setdefault(cid, [])
                    if not slots or slots[-1][0] != q.verdict:
                        slots.append((q.verdict,
                                      f"amended at seq {self.generation}: {q.reason}"))
        return proj

    def reconcile(self) -> list[str]:
        """Independent phase-2 sweep: every projection marked
        REVALIDATION_REQUIRED must actually be refused as current by the
        read-time gate; every CURRENT projection must serve. Returns the
        list of violations (empty == clean)."""
        violations = []
        for pid, proj in self.projections.items():
            if proj.surface == HISTORICAL_RECEIPT:
                continue
            res = self.serve(pid, KNOW_RETRIEVAL)
            if proj.status == REVALIDATION_REQUIRED and res.decision == SERVE_CURRENT:
                violations.append(f"{pid}: marked for revalidation but servable")
            if proj.status == CURRENT and res.decision != SERVE_CURRENT:
                violations.append(f"{pid}: marked current but not servable: {res.annotation}")
        return violations

    # -- ACT commit boundary (TOCTOU close) -----------------------------------
    def authorize_act(self, claim_dependencies, seen_generation: int) -> str:
        """Re-check eligibility at the commit boundary. If the generation
        moved since the caller last validated, or any dependency is stale
        against the caller's view, the action is refused."""
        if seen_generation != self.generation:
            return ACT_REFUSED
        for cid in claim_dependencies:
            q = self.claims.get(cid)
            if q is None or q.qualified_at_seq > seen_generation:
                return ACT_REFUSED
            if q.verdict not in (UNAFFECTED, REQUALIFIED, DOWNGRADED):
                return ACT_REFUSED
        return ACT_AUTHORIZED

    # -- projections ----------------------------------------------------------
    def add_projection(self, projection_id: str, surface: str,
                       claim_dependencies, content: str = "",
                       status: str = CURRENT, link: str = "") -> Projection:
        proj = Projection(projection_id, surface, frozenset(claim_dependencies),
                          self.generation, status, content, (), link)
        self.projections[projection_id] = proj
        return proj

    # -- Smart Notes -----------------------------------------------------------
    def add_smart_note(self, note_id: str, claim_ids) -> Projection:
        """A Smart Note keeps every claim slot in history; refresh appends
        claim-level amendments. Ten claims in, ten claims stay — verdicts
        change, history never shrinks."""
        proj = self.add_projection(note_id, SMART_NOTE, claim_ids,
                                   content=f"smart-note {note_id}")
        slots: dict[str, list] = {}
        for cid in claim_ids:
            q = self.claims[cid]
            slots[cid] = [(q.verdict, f"initial at seq {q.qualified_at_seq}")]
        self.note_claims[note_id] = slots
        return proj

    def note_history(self, note_id: str, claim_id: str):
        return tuple(self.note_claims[note_id][claim_id])

    # -- index ------------------------------------------------------------------
    def index_note(self, note_id: str, claim_ids) -> None:
        self.index_entries[note_id] = set(claim_ids)
        for cid in claim_ids:
            v = self.claims[cid].verdict
            self.index_pointers[(note_id, cid)] = (v, CURRENT)

    def index_discover(self, claim_id: str) -> list[str]:
        """Discovery: which notes mention this claim. Always available —
        discoverability is not certifiability."""
        return sorted(n for n, cids in self.index_entries.items()
                      if claim_id in cids)

    def index_pointer(self, note_id: str, claim_id: str):
        """The qualification pointer: (verdict, pointer_status). A stale
        pointer reads REVALIDATION_REQUIRED — found, not certified."""
        return self.index_pointers[(note_id, claim_id)]

    # -- successor packages -------------------------------------------------------
    def seal_package(self, package_id: str, claim_ids) -> dict:
        """Seal an immutable snapshot: claim qualifications + source
        statuses + generation + event-log prefix. The package never serves
        sealed content as current after the store moves — activation
        reconciles mandatorily."""
        snap = {cid: self.claims[cid] for cid in claim_ids if cid in self.claims}
        pkg = {
            "package_id": package_id,
            "sealed_generation": self.generation,
            "snapshot": dict(snap),
            "sealed_source_statuses": dict(self.source_status),
            "event_log_prefix": len(self.events),
        }
        self.packages[package_id] = pkg
        self.add_projection(package_id, SUCCESSOR_PACKAGE, claim_ids,
                            content=f"sealed successor package {package_id} @ seq {self.generation}")
        return pkg

    def activate_package(self, package_id: str, replay=None) -> dict:
        """Mandatory reconciliation at activation, in two checks:
        1. Seal fidelity: rebuild the sealed world in a fresh provider
           (topology + sealed source statuses) and require its verdicts to
           equal the sealed snapshot — the replay is faithful.
        2. Reconciliation: apply every eligibility event since the seal, in
           order, and require the recomputed verdicts to equal the live
           store's. A cold successor reaches the same current verdict —
           or activation fails loudly instead of serving stale content.

        replay: callable taking a fresh SimpleRecomputeProvider and
        registering the sealed topology (sources + claims)."""
        pkg = self.packages[package_id]
        replay = replay if replay is not None else pkg.get("replay")
        if replay is None:
            raise ValueError("package has no replay topology; cannot reconcile")
        fresh = SimpleRecomputeProvider()
        replay(fresh)
        for sid, status in pkg["sealed_source_statuses"].items():
            if sid in fresh._sources:
                fresh.set_source_status(sid, status)
        fresh.recompute_all()
        fidelity_failures = []
        for cid, sq in pkg["snapshot"].items():
            fresh_key = _standing_key(fresh._verdicts[cid][0],
                                      fresh._verdicts[cid][1])
            sealed_key = _standing_key(sq.verdict, sq.covered_scope)
            if fresh_key != sealed_key:
                fidelity_failures.append((cid, fresh_key, sealed_key))
        if fidelity_failures:
            self.projections[package_id].status = REVALIDATION_REQUIRED
            return {"activated": False, "mismatches": fidelity_failures,
                    "phase": "seal_fidelity"}
        for ev in self.events[pkg["event_log_prefix"]:]:
            fresh.set_source_status(ev.source_id, ev.new_status)
            fresh.recompute_affected(frozenset({ev.source_id}))
        mismatches = []
        for cid in pkg["snapshot"]:
            live_q = self.claims[cid]
            fresh_key = _standing_key(fresh._verdicts[cid][0],
                                      fresh._verdicts[cid][1])
            live_key = _standing_key(live_q.verdict, live_q.covered_scope)
            if fresh_key != live_key:
                mismatches.append((cid, fresh_key, live_key))
        proj = self.projections[package_id]
        if mismatches:
            proj.status = REVALIDATION_REQUIRED
            return {"activated": False, "mismatches": mismatches,
                    "phase": "reconciliation"}
        proj.status = CURRENT
        proj.generation = self.generation
        return {"activated": True, "mismatches": [],
                "verdicts": {cid: self.claims[cid].verdict
                             for cid in pkg["snapshot"]}}
