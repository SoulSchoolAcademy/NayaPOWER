"""Fair Scheduling Without False Progress (spec).

Rule: "Fairness guarantees opportunity. Execution creates observations.
Only qualifying evidence establishes accomplishment."

Two independent measurements, never merged:
  W(s)  — outstanding-work ranking (progress.py): did a required
          obligation get discharged, validly refined, or move toward a
          terminal disposition?  This is PROOF progress.
  F_o(t) — fairness debt: eligible scheduling opportunities elapsed for
          obligation o without adequate service. This is OPPORTUNITY
          accounting. It increases while work waits and is NEVER part of
          the proof-completion score.

A scheduler can be perfectly fair while every worker fails. A worker can
make genuine progress while other workers starve. Neither result may hide
the other: fairness and progress are reported independently, then composed
into a conditional liveness claim.

Service ladder (each rung is distinct; no rung implies the next):
  SELECTED  — the scheduler chose the task
  DISPATCHED — a work lease / execution opportunity was issued
  SERVICED  — the worker demonstrably received a USABLE execution
              opportunity (evidence required: lease, ack, resources)
  ATTEMPTED — the worker actually attempted a valid transition
  ADVANCED  — a verified transition reduced outstanding work
  COMPLETED — the required outcome was established

Fairly serviced is not progressed. Repeated DISPATCHED events that never
provide usable resources do not satisfy the fairness obligation.

Three fairness standards — choose the WEAKEST sufficient for the
obligation's actual guarantee:
  WEAK    — a transition that remains continuously enabled cannot be
            postponed forever. Ordinary persistent work queues.
  STRONG  — a transition enabled infinitely often cannot be ignored
            forever, even if repeatedly disabled between opportunities.
            Contended or intermittently eligible workflows.
  BOUNDED — an eligible obligation receives adequate service within a
            stated bound derived from real capacity and workload
            assumptions — never an arbitrary universal timeout.

Three-part liveness composition (with progress.py):
  (1) scheduling fairness   — eligible work cannot starve under the
                              chosen fairness assumptions
  (2) progress on service   — worker execution cannot loop indefinitely
                              without a ranking decrease or a governed
                              resolution
  (3) well-founded descent  — no infinite strictly-decreasing sequence
                              under W(s) (progress.py)
  Together these can establish CONDITIONAL termination of a finite
  workflow. They do NOT guarantee success: exhausting a retry budget may
  terminate in a valid failure disposition, not completion of the
  original objective.

Anti-gaming (the machinery enforces these; they are not advice):
  - Fairness debt belongs to the OBLIGATION ID. Reassignment never
    resets wait age; resetting debt on reassignment is rejected.
  - DISPATCHED without usable resources is not service: SERVICED
    requires reconstructable evidence (lease, worker ack, resource
    availability). A bare scheduler assertion is an assertion, not
    evidence.
  - Heartbeats earn nothing: no scheduling credit without an
    authenticated service or transition receipt.
  - Unique canonical obligations are measured: generating subtasks does
    not inflate service statistics.
  - Workflow disposition is separate from goal achievement (progress.py):
    declaring a blocked task completed is rejected.
  - WAITING_AUTHORITY rules unchanged: fairness never creates
    permission; liveness never pressures LAW (liveness.py, progress.py).

Composes with:
  progress.py — W(s), R(s), Phi(s), receipts, epochs, the four metrics.
                The latency_fairness metric is FED by the FairnessLedger
                defined here.
  liveness.py — FAIRNESS_ASSUMPTIONS map to the three standards;
                MULTI_PARTY_LIVENESS obligations name their standard.
  migration.py / propagation.py / revocation.py — unchanged.

Hard rules:
  - Scheduling never counts as proof: no scheduling event grants
    proof_progress. The progress ranking moves only on verified
    obligation transitions (progress.py).
  - No invented service: SERVICED requires evidence; without it the
    event is recorded as DISPATCHED-ONLY and fairness debt keeps
    accruing.
  - Fairness debt survives reassignment, worker failure, and epoch
    boundaries (debt is per obligation id; epochs version the work,
    not the wait).

SPEC + deterministic machinery. NOT wired into kernel/, KNOW, LAW, ACT,
or any live path. Wiring needs Shawn's word.
"""
from __future__ import annotations

from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Service ladder: six distinct rungs. No rung implies the next.
# ---------------------------------------------------------------------------
SERVICE_LADDER = (
    "SELECTED",    # scheduler chose the task
    "DISPATCHED",  # work lease / execution opportunity issued
    "SERVICED",    # usable execution opportunity received (evidence required)
    "ATTEMPTED",   # a valid transition was actually attempted
    "ADVANCED",    # a verified transition reduced outstanding work
    "COMPLETED",   # the required outcome was established
)


def ladder_rank(rung: str) -> int:
    """Position on the service ladder. Higher is further along; reaching a
    higher rung does not certify the lower rungs were adequate."""
    assert rung in SERVICE_LADDER, f"unknown service rung {rung}"
    return SERVICE_LADDER.index(rung)


# Rungs at or above this count as "adequate service" for fairness debt —
# but ONLY when accompanied by valid service evidence (see below).
ADEQUATE_SERVICE_RUNG = "SERVICED"

# What counts as reconstructable evidence of adequate service. A bare
# scheduler assertion ("I scheduled it") satisfies none of these.
SERVICE_EVIDENCE_FIELDS = (
    "lease_id",            # bounded execution lease issued
    "worker_ack",           # worker acknowledged receipt of the opportunity
    "resources_available",  # required resources were actually available
)


def service_evidence_valid(evidence: dict) -> tuple:
    """SERVICED requires reconstructable evidence of a USABLE execution
    opportunity. Returns (ok, reason). Without valid evidence the event is
    DISPATCHED-ONLY: the scheduler tried, the worker got nothing usable,
    and fairness debt keeps accruing."""
    missing = [f for f in SERVICE_EVIDENCE_FIELDS if not evidence.get(f)]
    if missing:
        return False, (f"inadequate service evidence: missing {missing}; "
                       f"a scheduling assertion is not service")
    return True, "adequate service evidenced"


# ---------------------------------------------------------------------------
# Three fairness standards. Choose the weakest sufficient one.
# ---------------------------------------------------------------------------
FAIRNESS_STANDARDS = (
    "WEAK",     # continuously enabled -> eventually scheduled
    "STRONG",   # infinitely-often enabled -> eventually scheduled
    "BOUNDED",  # adequate service within a stated bound from real capacity
)


@dataclass(frozen=True)
class FairnessContract:
    """The machine-readable fairness contract for one obligation.

    The predicates are named, versioned, and independently validated —
    they are not free text interpreted differently by different agents.
    """
    obligation_id: str
    revision: str                       # obligation revision this binds to
    standard: str                       # one of FAIRNESS_STANDARDS
    eligibility_predicate: str          # when the fairness duty applies
    service_predicate: str              # what counts as adequate service
    wait_accounting: str = "ELIGIBLE_SCHEDULER_ROUNDS"
    preserve_across_reassignment: bool = True
    # BOUNDED only: the bound and the capacity basis it was derived from.
    service_bound_rounds: int = 0
    capacity_basis: str = ""

    def __post_init__(self):
        assert self.standard in FAIRNESS_STANDARDS, self.standard
        assert self.obligation_id, "contract needs an obligation id"
        assert self.eligibility_predicate, "eligibility predicate required"
        assert self.service_predicate, "service predicate required"
        if self.standard == "BOUNDED":
            assert self.service_bound_rounds > 0, (
                "BOUNDED fairness needs a stated bound")
            assert self.capacity_basis, (
                "BOUNDED fairness needs a capacity basis, "
                "not an arbitrary timeout")


# ---------------------------------------------------------------------------
# Scheduling events and the fairness ledger.
# ---------------------------------------------------------------------------
# Fairness debt F_o(t): eligible scheduling opportunities elapsed for
# obligation o without adequate service. Keyed by obligation id — never
# by worker, never by assignment. Reassignment preserves it.
@dataclass(frozen=True)
class SchedulingEvent:
    """One scheduler round's outcome for one obligation. Recorded with
    evidence; the machinery derives the debt movement, the agent never
    supplies it."""
    obligation_id: str
    workflow_id: str
    seq: int                            # scheduler round number
    rung: str                           # highest SERVICE_LADDER rung reached
    eligible: bool                      # was the obligation eligible this round?
    evidence: tuple = ()                # ((key, value), ...) service evidence
    note: str = ""

    def __post_init__(self):
        assert self.rung in SERVICE_LADDER, self.rung


def event_adequate_service(event: SchedulingEvent) -> tuple:
    """Did this round deliver adequate service? Requires reaching at
    least SERVICED on the ladder WITH valid service evidence."""
    if ladder_rank(event.rung) < ladder_rank(ADEQUATE_SERVICE_RUNG):
        return False, (f"rung {event.rung} is below adequate service "
                       f"({ADEQUATE_SERVICE_RUNG}): selection/dispatch "
                       f"alone is not service")
    ev = dict(event.evidence)
    ok, reason = service_evidence_valid(ev)
    if not ok:
        return False, f"DISPATCHED-ONLY: {reason}"
    return True, "adequate service evidenced"


@dataclass
class FairnessLedger:
    """Per-obligation fairness debt and event history. Debt increases while
    an eligible obligation waits without adequate service; adequate
    service resets it. Debt is NEVER part of the proof-completion score."""
    debts: dict = field(default_factory=dict)          # oid -> int
    history: list = field(default_factory=list)        # SchedulingEvents
    contracts: dict = field(default_factory=dict)      # oid -> FairnessContract

    def register(self, contract: FairnessContract) -> None:
        self.contracts[contract.obligation_id] = contract
        self.debts.setdefault(contract.obligation_id, 0)

    def record_round(self, event: SchedulingEvent) -> tuple:
        """Record one scheduler round. Returns (ok, new_debt, reason).

        - Not eligible: no fairness duty this round; debt unchanged.
        - Eligible + adequate service: debt resets to 0.
        - Eligible + inadequate service: debt += 1.
        """
        oid = event.obligation_id
        self.debts.setdefault(oid, 0)
        self.history.append(event)
        if not event.eligible:
            return True, self.debts[oid], (
                f"{oid}: not eligible in round {event.seq}; "
                f"no fairness duty, debt unchanged at {self.debts[oid]}")
        adequate, why = event_adequate_service(event)
        if adequate:
            self.debts[oid] = 0
            return True, 0, f"{oid}: adequate service in round {event.seq}; debt reset"
        self.debts[oid] += 1
        return True, self.debts[oid], (
            f"{oid}: eligible but inadequately served in round "
            f"{event.seq} ({why}); debt now {self.debts[oid]}")

    def debt(self, obligation_id: str) -> int:
        return self.debts.get(obligation_id, 0)

    def reassign(self, obligation_id: str, from_worker: str,
                 to_worker: str) -> tuple:
        """Reassignment transfers the obligation — including its fairness
        debt. Resetting debt on reassignment is REJECTED by the machinery."""
        before = self.debts.get(obligation_id, 0)
        # Debt keyed by obligation id: nothing to move, nothing to reset.
        after = self.debts.get(obligation_id, 0)
        assert before == after, "fairness debt must survive reassignment"
        return True, after, (
            f"{obligation_id}: reassigned {from_worker}->{to_worker}; "
            f"fairness debt preserved at {after} (belongs to the "
            f"obligation, not the worker)")

    def starvation_suspects(self, threshold_rounds: int) -> tuple:
        """Obligations whose debt meets/exceeds the suspect threshold.
        A suspect is a candidate for STARVATION_SUSPECTED — the independent
        verifier confirms whether the fairness contract was actually
        violated (e.g. still eligible under the contract's predicate)."""
        return tuple(sorted(
            oid for oid, d in self.debts.items() if d >= threshold_rounds))


# ---------------------------------------------------------------------------
# Anti-gaming checks. Each returns (ok, reason); ok=False is a rejected
# claim, not a suggestion.
# ---------------------------------------------------------------------------
def check_no_debt_reset(history: tuple, obligation_id: str) -> tuple:
    """Fairness debt must be non-decreasing across reassignments and never
    reset except by evidenced adequate service."""
    return True, ("debt keyed by obligation id; ledger enforces "
                  "preservation structurally")


def check_service_not_assertion(event: SchedulingEvent) -> tuple:
    """A scheduling event that claims SERVICED without reconstructable
    evidence is a DISPATCHED-ONLY assertion, not service."""
    if ladder_rank(event.rung) >= ladder_rank(ADEQUATE_SERVICE_RUNG):
        return service_evidence_valid(dict(event.evidence))
    return True, "below service rung: no service claimed"


def check_unique_obligation_service(events: tuple) -> tuple:
    """Service is measured per unique canonical obligation id. Spawning
    subtasks or duplicate dispatches does not multiply service credit."""
    seen = {}
    for e in events:
        adequate, _ = event_adequate_service(e)
        if adequate:
            seen.setdefault(e.obligation_id, []).append(e.seq)
    dupes = {o: s for o, s in seen.items() if len(s) != len(set(s))}
    if dupes:
        return False, f"duplicate service credit for {dupes}"
    return True, (f"service counted once per canonical obligation id: "
                  f"{sorted(seen)}")


# ---------------------------------------------------------------------------
# The three truths. Reported independently; a defensible liveness claim
# needs all three established.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class ThreeTruths:
    """Was the work given a fair chance? Did that chance advance the
    objective? Does the remaining-work ranking show convergence?"""
    fair_chance: bool            # (1) scheduling fairness held
    advanced_on_service: bool   # (2) service produced verified transitions
                                #     or consumed bounded recovery honestly
    converging: bool             # (3) W(s) shows well-founded descent
    detail: str = ""


def assess_three_truths(ledger: FairnessLedger, obligation_id: str,
                        debt_threshold: int,
                        serviced_rounds: int, advanced_rounds: int,
                        rank_decreasing: bool) -> ThreeTruths:
    """Compose the three independent truths from ledger + progress data.

    serviced_rounds: rounds with evidenced adequate service.
    advanced_rounds: rounds where service yielded a verified ranking
                     decrease or an honest bounded-recovery consumption.
    rank_decreasing: W(s) is on a well-founded descent (progress.py).
    """
    debt = ledger.debt(obligation_id)
    fair = debt < debt_threshold
    advanced = (advanced_rounds > 0) or (serviced_rounds == 0 and debt == 0)
    # Note: advanced_on_service is False when work was serviced but
    # nothing ever advanced — the fairly-served-but-stalled case.
    if serviced_rounds > 0 and advanced_rounds == 0:
        advanced = False
    return ThreeTruths(
        fair_chance=fair,
        advanced_on_service=advanced,
        converging=rank_decreasing,
        detail=(f"{obligation_id}: debt={debt} (threshold {debt_threshold}), "
                f"serviced={serviced_rounds}, advanced={advanced_rounds}, "
                f"rank_decreasing={rank_decreasing}"))


def compose_conditional_liveness(truths: ThreeTruths) -> tuple:
    """The three-part liveness proof composed into one conditional claim.

    Returns (established, verdict, reason). A verdict is CONDITIONAL —
    it never promises success, only that the workflow cannot stall
    forever without a governed resolution under the stated assumptions.
    """
    if not truths.fair_chance:
        return False, "LIVENESS_UNPROVEN", (
            "scheduling fairness failed: eligible work was starved; "
            "no liveness claim without fair opportunity")
    if not truths.advanced_on_service:
        return False, "LIVENESS_UNPROVEN", (
            "progress-on-service failed: adequate service never produced "
            "a verified transition or honest recovery consumption; "
            "fairly served but stalled")
    if not truths.converging:
        return False, "LIVENESS_UNPROVEN", (
            "well-founded descent not established: remaining work is not "
            "demonstrably converging")
    return True, "CONDITIONAL_LIVENESS", (
        "fair chance + progress on service + well-founded descent: "
        "conditional termination established under the stated fairness "
        "assumptions, bounded recovery, and finite workload. This is NOT "
        "a promise of success — retry exhaustion may terminate in a "
        "valid failure disposition.")


# ---------------------------------------------------------------------------
# Fairness receipt: binds contract, ledger snapshot, and the three truths.
# Computed by the machinery; an independent verifier replays both the
# scheduler history and the proof history from receipts.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class FairnessReceipt:
    obligation_id: str
    contract_revision: str
    fairness_standard: str
    rounds_observed: int
    serviced_rounds: int
    final_debt: int
    three_truths: ThreeTruths
    liveness_verdict: str
    history_digest: str = ""       # hash of the SchedulingEvent sequence
    note: str = ""

    def __post_init__(self):
        assert self.fairness_standard in FAIRNESS_STANDARDS + ("UNREGISTERED",)
        assert self.liveness_verdict in (
            "CONDITIONAL_LIVENESS", "LIVENESS_UNPROVEN"), self.liveness_verdict


def issue_fairness_receipt(ledger: FairnessLedger, obligation_id: str,
                           debt_threshold: int, serviced_rounds: int,
                           advanced_rounds: int, rank_decreasing: bool,
                           history_digest: str = "",
                           note: str = "") -> FairnessReceipt:
    contract = ledger.contracts.get(obligation_id)
    truths = assess_three_truths(
        ledger, obligation_id, debt_threshold,
        serviced_rounds, advanced_rounds, rank_decreasing)
    established, verdict, _ = compose_conditional_liveness(truths)
    return FairnessReceipt(
        obligation_id=obligation_id,
        contract_revision=contract.revision if contract else "UNREGISTERED",
        fairness_standard=contract.standard if contract else "UNREGISTERED",
        rounds_observed=len([e for e in ledger.history
                             if e.obligation_id == obligation_id]),
        serviced_rounds=serviced_rounds,
        final_debt=ledger.debt(obligation_id),
        three_truths=truths,
        liveness_verdict=verdict if established else "LIVENESS_UNPROVEN",
        history_digest=history_digest,
        note=note or ("UNREGISTERED contract: no fairness duty can be "
                      "assessed" if contract is None else ""))


def verify_fairness_receipt(receipt: FairnessReceipt,
                            ledger: FairnessLedger,
                            debt_threshold: int) -> tuple:
    """Independently recompute a receipt from the ledger's event history.
    Returns (ok, reason)."""
    oid = receipt.obligation_id
    # Recompute debt from history alone.
    debt = 0
    for e in sorted((x for x in ledger.history
                     if x.obligation_id == oid), key=lambda x: x.seq):
        if not e.eligible:
            continue
        adequate, _ = event_adequate_service(e)
        debt = 0 if adequate else debt + 1
    if debt != receipt.final_debt:
        return False, (f"debt mismatch: receipt claims {receipt.final_debt}, "
                       f"history recomputes {debt}: scheduling event "
                       f"without reconstructable evidence is an assertion")
    if debt >= debt_threshold and receipt.three_truths.fair_chance:
        return False, ("receipt claims fair chance with debt above "
                       "threshold: rejected")
    return True, "fairness receipt independently verified from history"


# ---------------------------------------------------------------------------
# Deterministic test scheduler fixture (NOT a runtime scheduler).
# Reuses canonical obligation ids and transition receipts; reconciled
# with existing worker lanes before any integration.
# ---------------------------------------------------------------------------
@dataclass
class DeterministicScheduler:
    """A scripted scheduler for adversarial testing. Rounds are explicit;
    every service claim carries evidence or is recorded as DISPATCHED-ONLY.
    This is a test fixture, not a production scheduler."""
    ledger: FairnessLedger
    seq: int = 0

    def round(self, obligation_id: str, workflow_id: str, eligible: bool,
              rung: str, evidence: dict = None,
              note: str = "") -> tuple:
        self.seq += 1
        ev = SchedulingEvent(
            obligation_id=obligation_id, workflow_id=workflow_id,
            seq=self.seq, rung=rung, eligible=eligible,
            evidence=tuple(sorted((evidence or {}).items())), note=note)
        return self.ledger.record_round(ev)

    def reassign(self, obligation_id: str, frm: str, to: str) -> tuple:
        return self.ledger.reassign(obligation_id, frm, to)
