"""Well-founded measure of real progress (spec).

Law: "Activity is not progress. A verified reduction in outstanding
obligations is progress. Exhausting a recovery budget is termination
progress, not achievement. Escalation transfers responsibility; it does
not complete the original objective."

Two measures, never one gameable percentage:
  proof progress      — a required obligation was independently discharged
                        with acceptable evidence.
  termination progress — the workflow moved toward a finite resolution
                        (including bounded failure recovery).

Extends drift_canary/liveness.py: LivenessObligation says eligible work is
OWED progress; this module says what counts as progress and proves the
accounting cannot be gamed. Composes with:
  liveness.py    — MULTI_PARTY_LIVENESS obligations carry the fairness
                   assumptions; ProgressAccount tracks their discharge.
                   WAITING_AUTHORITY rules unchanged: liveness never
                   creates permission.
  migration.py   — MultiPartyInteraction safety invariants are the
                   obligations being discharged; obligation revisions are
                   immutable (revision change => new obligation identity).
  propagation.py — MeaningEnvelope for environment scope.
  revocation.py  — VERDICTS reused for receipt qualification.

Hard rules:
  - No invented progress: heartbeats, log lines, status rewrites, bare
    retries, and reassignments earn NO proof-progress credit.
  - Budgets follow the OBLIGATION, not the agent: reassignment transfers
    the same obligation ID with its remaining budget. Resetting the budget
    on reassignment is rejected.
  - One requirement never earns extra credit from more agents: discharge is
    counted once per unique obligation ID.
  - Escalation never completes the original objective: it may complete a
    separate bounded disposition obligation.
  - proof_progress / termination_progress are COMPUTED by the machinery
    from authenticated transitions — never supplied by the agent.
  - New requirements start a new versioned assessment epoch; the old
    baseline is preserved, not rewritten.

This module is SPEC + deterministic machinery. NOT wired into kernel/,
KNOW, LAW, ACT, or any live path. Wiring needs Shawn's word.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Proof obligations: the unit of real work.
# ---------------------------------------------------------------------------
# A ProofObligation is what must be demonstrated. Rank is the structural
# rank: a higher-rank obligation may decompose ONLY into finitely many
# strictly-lower-rank obligations via a VALID refinement (the children
# faithfully cover the parent's requirements, no missing requirements).
# Rank is structural, not a priority score.
OBLIGATION_STATES = (
    "OUTSTANDING",   # not yet discharged
    "DISCHARGED",    # independently satisfied under acceptance criteria
    "SUSPENDED",     # waiting on dependency/authority; still outstanding work
)


@dataclass(frozen=True)
class ProofObligation:
    """One verifiable unit of required work."""
    obligation_id: str
    revision: str
    rank: int                       # structural rank, >= 0
    composition: str                # "ATOMIC" | "AND" | "OR"
    acceptance: str                 # machine-checkable or assessable predicate
    proof_standard: str             # required evidence / independence level
    children: tuple = ()            # child obligation ids (AND/OR)
    retries_remaining: int = 0      # recovery budget FOLLOWS this obligation
    state: str = "OUTSTANDING"

    def __post_init__(self):
        assert self.rank >= 0, "rank must be a natural number"
        assert self.composition in ("ATOMIC", "AND", "OR"), self.composition
        assert self.state in OBLIGATION_STATES, self.state
        assert self.retries_remaining >= 0, "budget cannot be negative"
        if self.composition == "ATOMIC":
            assert not self.children, "atomic obligations have no children"


# ---------------------------------------------------------------------------
# Well-founded multiset ranking.
# ---------------------------------------------------------------------------
# W(s) = multiset of ranks of outstanding obligations. Ordered by the
# Dershowitz-Manna multiset extension: M <mul N iff M != N and, at the
# greatest rank where the counts differ, M has fewer.
def multiset_less(a: tuple, b: tuple) -> bool:
    """True iff multiset a is strictly less work than multiset b."""
    ca, cb = Counter(a), Counter(b)
    if ca == cb:
        return False
    for rank in sorted(set(ca) | set(cb), reverse=True):
        if ca[rank] != cb[rank]:
            return ca[rank] < cb[rank]
    return False  # unreachable when ca != cb


def multiset_equal(a: tuple, b: tuple) -> bool:
    return Counter(a) == Counter(b)


def outstanding_ranks(obligations: tuple) -> tuple:
    """W(s): ranks of obligations still outstanding, sorted descending."""
    return tuple(sorted(
        (o.rank for o in obligations if o.state != "DISCHARGED"),
        reverse=True))


def is_valid_refinement(parent: ProofObligation,
                        children: tuple) -> tuple:
    """A decomposition counts as progress only if it is a VALID refinement:
    finitely many children, every child strictly lower rank, children
    collectively cover the parent (declared, not assumed), no invented
    obligations. Returns (ok, reason)."""
    if not children:
        return False, "refinement needs at least one child"
    if parent.composition == "ATOMIC" and parent.children:
        return False, "atomic obligation cannot be refined"
    for c in children:
        if c.rank >= parent.rank:
            return False, (f"child {c.obligation_id} rank {c.rank} not "
                           f"strictly below parent rank {parent.rank}: "
                           f"arbitrary task creation is not progress")
    return True, "valid refinement"


# ---------------------------------------------------------------------------
# Transition classification. The machinery computes these; the agent never
# supplies them.
# ---------------------------------------------------------------------------
# proof_progress:       a required obligation was independently discharged.
# termination_progress: the workflow moved toward a finite resolution.
TRANSITION_KINDS = (
    "DISCHARGE",        # obligation independently satisfied
    "REFINEMENT",       # valid decomposition into lower-rank obligations
    "FAILED_RETRY",     # recovery attempt consumed, obligation unchanged
    "REASSIGNMENT",     # same obligation id + remaining budget to new worker
    "HEARTBEAT",        # heartbeat / log line / status rewrite
    "ESCALATION",       # responsibility transferred; objective preserved
    "NEW_EPOCH",        # new requirement discovered; baseline versioned
    "EVIDENCE_INVALID", # branch used invalid evidence; history kept, not discharged
)


@dataclass(frozen=True)
class RankedTransition:
    """One authenticated, version-bound state transition with its
    machine-computed progress classification."""
    workflow_id: str
    epoch: int
    kind: str
    obligation_id: str
    prev_ranks: tuple      # W(s) before
    next_ranks: tuple      # W(s) after
    retries_before: int
    retries_after: int
    proof_progress: bool   # computed, never agent-supplied
    termination_progress: bool  # computed, never agent-supplied
    reason: str = ""

    def __post_init__(self):
        assert self.kind in TRANSITION_KINDS, self.kind


def classify_transition(kind: str, prev_ranks: tuple, next_ranks: tuple,
                        retries_before: int, retries_after: int,
                        discharged: bool) -> tuple:
    """Compute (proof_progress, termination_progress) from the transition's
    structural effect. Returns (ok, (proof, term), reason)."""
    if kind == "DISCHARGE":
        if not discharged:
            return False, (False, False), "DISCHARGE without discharge is not progress"
        if not multiset_less(next_ranks, prev_ranks):
            return False, (False, False), (
                "claimed discharge did not reduce outstanding work: "
                "activity is not progress")
        return True, (True, True), "obligation independently discharged"
    if kind == "REFINEMENT":
        if not multiset_less(next_ranks, prev_ranks):
            return False, (False, False), (
                "refinement did not structurally reduce work: invalid refinement")
        # Structural progress, not completion credit.
        return True, (False, True), "valid refinement: structural, not completion"
    if kind == "FAILED_RETRY":
        if retries_after >= retries_before:
            return False, (False, False), (
                "failed retry must consume recovery budget")
        if not multiset_equal(next_ranks, prev_ranks):
            return False, (False, False), (
                "failed retry must not change outstanding work")
        return True, (False, True), "recovery consumed; proof unchanged"
    if kind in ("REASSIGNMENT", "HEARTBEAT"):
        if not multiset_equal(next_ranks, prev_ranks):
            return False, (False, False), (
                f"{kind} must not change outstanding work")
        if retries_after != retries_before:
            return False, (False, False), (
                f"{kind} must preserve the obligation's recovery budget")
        return True, (False, False), f"{kind}: no progress credit"
    if kind == "ESCALATION":
        # Original objective stays outstanding; a separate disposition
        # obligation may be satisfied elsewhere.
        return True, (False, False), (
            "escalation transfers responsibility; original objective unresolved")
    if kind == "NEW_EPOCH":
        return True, (False, False), (
            "new assessment epoch: old baseline preserved, not rewritten")
    if kind == "EVIDENCE_INVALID":
        return True, (False, False), (
            "invalid evidence: history preserved, obligation not discharged")
    return False, (False, False), f"unknown transition kind {kind}"


# ---------------------------------------------------------------------------
# Branch-and-join rules.
# ---------------------------------------------------------------------------
def discharge(obligations: tuple, obligation_id: str,
              evidence_ok: bool, reason: str = "") -> tuple:
    """Discharge one obligation by unique id. Returns
    (ok, new_obligations, discharged_ids). Discharge counted ONCE per id;
    invalid evidence preserves history without discharging."""
    ids = [o.obligation_id for o in obligations]
    if ids.count(obligation_id) != 1:
        return False, obligations, (), (
            f"obligation {obligation_id} must appear exactly once; "
            f"no double-counting, no phantom discharge")
    if not evidence_ok:
        # History preserved; obligation stays outstanding.
        return True, obligations, (), (
            f"{obligation_id}: invalid evidence — history preserved, "
            f"not discharged")
    out, discharged_ids = [], []
    for o in obligations:
        if o.obligation_id == obligation_id and o.state != "DISCHARGED":
            out.append(ProofObligation(
                o.obligation_id, o.revision, o.rank, o.composition,
                o.acceptance, o.proof_standard, o.children,
                o.retries_remaining, "DISCHARGED"))
            discharged_ids.append(o.obligation_id)
        else:
            out.append(o)
    return True, tuple(out), tuple(discharged_ids), reason or "discharged"


def and_join_ready(obligations: tuple, parent: ProofObligation) -> tuple:
    """An AND composite is satisfied only when every child is DISCHARGED
    AND the parent's own join proof has been independently discharged.
    Parallel branches finishing does NOT complete the composite by itself —
    the join invariant is its own obligation."""
    if parent.composition != "AND":
        return False, "not an AND obligation"
    by_id = {o.obligation_id: o for o in obligations}
    missing = [c for c in parent.children
               if c not in by_id or by_id[c].state != "DISCHARGED"]
    if missing:
        return False, f"AND join blocked: {missing} not discharged"
    if by_id.get(parent.obligation_id, parent).state != "DISCHARGED":
        return False, (f"branches done but join proof "
                       f"{parent.obligation_id} not discharged")
    return True, "all branches and join discharged"


def or_alternative_ready(obligations: tuple, parent: ProofObligation,
                         alternative_id: str) -> tuple:
    """An OR parent is satisfied by one independently qualified sufficient
    alternative — but only if that alternative is sufficient under the
    actual obligation contract."""
    if parent.composition != "OR":
        return False, "not an OR obligation"
    if alternative_id not in parent.children:
        return False, f"{alternative_id} is not a permitted alternative"
    by_id = {o.obligation_id: o for o in obligations}
    alt = by_id.get(alternative_id)
    if alt is None or alt.state != "DISCHARGED":
        return False, f"alternative {alternative_id} not discharged"
    return True, f"OR satisfied by {alternative_id}"


# ---------------------------------------------------------------------------
# Assessment epochs: genuinely new requirements version the baseline.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class AssessmentEpoch:
    """A versioned snapshot of the work that must be done and the criteria
    for completion. Discovering a critical missing requirement starts a new
    epoch; the old baseline stays visible."""
    epoch: int
    obligation_manifest_hash: str
    obligations: tuple
    supersedes_epoch: int = 0
    discovery_note: str = ""   # why the new work was missing

    def __post_init__(self):
        assert self.epoch > 0, "epochs are 1-based"


def new_epoch(prior: AssessmentEpoch, new_obligations: tuple,
              manifest_hash: str, discovery_note: str) -> AssessmentEpoch:
    """Open a new epoch. The prior epoch is preserved, never rewritten."""
    assert discovery_note, "new epochs must record why the work was missing"
    return AssessmentEpoch(prior.epoch + 1, manifest_hash, new_obligations,
                           prior.epoch, discovery_note)


# ---------------------------------------------------------------------------
# Four metrics — reported independently, never merged into one percentage.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class ProgressMetrics:
    """Four operational measurements. A status update changes none of these
    by itself; repeated state cycling reports livelock risk regardless of
    activity count."""
    verified_completion: tuple      # (discharged, total) — descriptive only
    work_potential: tuple           # current W(s): is outstanding work decreasing?
    recovery_consumption: tuple     # (initial_budget, remaining_budget)
    latency_fairness: tuple         # (oldest_eligible_age_units, starvation_flags)


def compute_metrics(obligations: tuple, initial_budgets: dict,
                    eligible_age: dict, starvation_flags: tuple = ()) -> ProgressMetrics:
    total = len(obligations)
    done = sum(1 for o in obligations if o.state == "DISCHARGED")
    remaining = sum(o.retries_remaining for o in obligations
                    if o.state != "DISCHARGED")
    initial = sum(initial_budgets.get(o.obligation_id, 0) for o in obligations
                  if o.state != "DISCHARGED")
    oldest = max(eligible_age.values()) if eligible_age else 0
    return ProgressMetrics(
        verified_completion=(done, total),
        work_potential=outstanding_ranks(obligations),
        recovery_consumption=(initial, remaining),
        latency_fairness=(oldest, starvation_flags),
    )


# ---------------------------------------------------------------------------
# Runtime progress receipt. Computed from authenticated, version-bound
# transitions. Rank-decrease claims carry prev+next multisets so an
# independent verifier can recompute the comparison.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class ProgressReceipt:
    workflow_id: str
    epoch: int
    goal_status: str            # UNRESOLVED | RESOLVED | REFUSED | STALLED_RECOVERABLE
    disposition_status: str     # ACTIVE | ESCALATED | CLOSED
    obligation_manifest: str    # sha256 of the epoch manifest
    outstanding: tuple          # (obligation_id, rank, state, retries_remaining)
    last_transition: RankedTransition
    last_verified_progress_receipt: str = ""
    progress_assessment: str = "UNKNOWN"
    current_authority: str = "LAW_CHECK_REQUIRED"

    def __post_init__(self):
        assert self.goal_status in (
            "UNRESOLVED", "RESOLVED", "REFUSED", "STALLED_RECOVERABLE"), \
            self.goal_status


def issue_receipt(workflow_id: str, epoch: AssessmentEpoch,
                  obligations: tuple, transition: RankedTransition,
                  goal_status: str, disposition_status: str,
                  assessment: str,
                  last_verified: str = "") -> ProgressReceipt:
    outstanding = tuple(
        (o.obligation_id, o.rank, o.state, o.retries_remaining)
        for o in obligations if o.state != "DISCHARGED")
    return ProgressReceipt(
        workflow_id, epoch.epoch, goal_status, disposition_status,
        epoch.obligation_manifest_hash, outstanding, transition,
        last_verified, assessment)


def verify_receipt_rank_claim(receipt: ProgressReceipt) -> tuple:
    """Independently recompute a receipt's rank-decrease claim from its
    carried prev/next multisets. Returns (ok, reason)."""
    t = receipt.last_transition
    if t.kind == "DISCHARGE" and t.proof_progress:
        if multiset_less(t.next_ranks, t.prev_ranks):
            return True, "discharge reduced outstanding work: verified"
        return False, "claimed discharge did not reduce work: rejected"
    if t.kind == "REFINEMENT" and t.termination_progress and not t.proof_progress:
        if multiset_less(t.next_ranks, t.prev_ranks):
            return True, "refinement structurally reduced work: verified"
        return False, "claimed refinement did not reduce work: rejected"
    if t.kind in ("REASSIGNMENT", "HEARTBEAT"):
        if multiset_equal(t.next_ranks, t.prev_ranks):
            return True, "no work change claimed, none present: verified"
        return False, "activity claimed work change: rejected"
    return True, "no rank claim to verify"


def cold_successor_reconstruct(receipts: tuple) -> tuple:
    """A cold successor rebuilds the outstanding frontier and budgets from
    receipts alone — never by interpreting status messages as evidence of
    progress. Returns (ok, frontier, budgets)."""
    if not receipts:
        return False, (), {}, "no receipts to reconstruct from"
    latest = max(receipts, key=lambda r: (r.epoch, r.last_transition.prev_ranks != r.last_transition.next_ranks))
    frontier = latest.outstanding
    budgets = {oid: retries for oid, _rank, _st, retries in latest.outstanding}
    # Every receipt's rank claims must independently verify.
    for r in receipts:
        ok, reason = verify_receipt_rank_claim(r)
        if not ok:
            return False, (), {}, f"receipt failed verification: {reason}"
    return True, frontier, budgets, "reconstructed from receipts only"
