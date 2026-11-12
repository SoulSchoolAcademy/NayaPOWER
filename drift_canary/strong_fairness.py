"""Strong fairness: when weak fairness is not enough (spec).

Rule: "Require strong fairness when an outstanding, legitimately
executable obligation can become enabled infinitely often without ever
remaining continuously enabled, and when indefinite starvation would
violate the intended liveness guarantee."

Key distinction:
  Weak fairness protects CONTINUOUSLY enabled work:
      FG E_o  =>  GF S_o
  Strong fairness protects REPEATEDLY enabled work that could otherwise
  be starved indefinitely:
      GF E_o  =>  GF S_o

Critical: strong fairness must NEVER become an excuse to execute during
an unauthorized or unsafe window. It governs scheduling OPPORTUNITIES,
not permission. Fairness never creates permission (fairness.py,
liveness.py, progress.py).

And: S_o =/=> dW < 0. Service is not proof progress. A task may be
served but fail, legitimately retry, or produce insufficient evidence.
The well-founded outstanding-work measure W decreases only when the
governing progress rules justify a reduction.

This module extends drift_canary/fairness.py with:
  1. the standard-selection decision rule (when WEAK / STRONG /
     BOUNDED / NEITHER is required),
  2. the eight-assumption checklist (each with required evidence),
  3. the three-proof composition for conditional termination,
  4. flicker-aware fairness-debt accounting (debt survives temporary
     ineligibility; eligibility epochs are counted, not reset),
  5. a finite-abstraction model checker for the weak-vs-strong
     distinction, and the decisive two-scheduler experiment.

Composes with:
  fairness.py  — service ladder, FAIRNESS_STANDARDS, FairnessLedger,
                 FairnessContract, three truths, receipts.
  progress.py  — W(s), R(s), Phi(s); service never grants proof progress.
  liveness.py  — MULTI_PARTY_LIVENESS obligations name their standard;
                 WAITING_AUTHORITY rules unchanged.

SPEC + deterministic machinery. NOT wired into kernel/, KNOW, LAW, ACT,
or any live path. Wiring needs Shawn's word.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from drift_canary.fairness import (
    ADEQUATE_SERVICE_RUNG,
    DeterministicScheduler,
    FairnessContract,
    FairnessLedger,
    SchedulingEvent,
    event_adequate_service,
    ladder_rank,
)

# ---------------------------------------------------------------------------
# 1. Standard-selection decision rule.
#
# Do NOT make STRONG the universal default: it imposes unnecessary
# scheduler obligations, complicates verification, and can hide defects
# in how eligibility is defined. Choose the WEAKEST sufficient standard.
# ---------------------------------------------------------------------------
# Situation codes for the decision rule.
SITUATIONS = (
    "CONTINUOUSLY_RUNNABLE",      # stays runnable until serviced
    "FLICKERING_SHARED_RESOURCE", # eligible windows flicker; resource taken
    "COMPETING_HIGH_PRIORITY",    # recurring high-priority work preempts
    "HARD_DEADLINE",              # must be served within a stated bound
    "HUMAN_AUTH_MISSING",         # required human authorization absent
    "FINITE_BRIEF_WINDOWS",       # only finitely many brief windows ever
    "WORKER_NOT_EXECUTABLE",      # cannot execute during observed windows
    "OR_BRANCH_SATISFIED",        # an OR alternative already discharged it
)

# situation -> (required_standard, reason). "NEITHER" means no fairness
# rule alone establishes the needed guarantee — fix the underlying
# problem first (readiness, authority, or retire the obligation).
STANDARD_DECISION_RULE = {
    "CONTINUOUSLY_RUNNABLE":
        ("WEAK",
         "continuous eligibility is sufficient; weak fairness guarantees "
         "eventual service"),
    "FLICKERING_SHARED_RESOURCE":
        ("STRONG",
         "eligibility may flicker forever; weak fairness permits "
         "indefinite postponement of intermittently enabled work"),
    "COMPETING_HIGH_PRIORITY":
        ("STRONG",
         "recurring preemption can starve the obligation under weak "
         "fairness; strong fairness is required where starvation must "
         "be prevented"),
    "HARD_DEADLINE":
        ("BOUNDED",
         "strong fairness alone provides no deadline; a bounded service "
         "guarantee with a capacity-derived bound is required"),
    "HUMAN_AUTH_MISSING":
        ("NEITHER",
         "neither fairness rule authorizes execution; LAW remains a hard "
         "gate — fairness governs opportunities, not permission"),
    "FINITE_BRIEF_WINDOWS":
        ("NEITHER",
         "strong fairness requires infinitely recurring eligibility; "
         "with only finitely many windows, no fairness rule alone "
         "guarantees service"),
    "WORKER_NOT_EXECUTABLE":
        ("NEITHER",
         "apparent eligibility is not a usable scheduling opportunity; "
         "repair the readiness/resource contract first"),
    "OR_BRANCH_SATISFIED":
        ("NEITHER",
         "no remaining need for that branch to execute; retire the "
         "unnecessary branch's service obligation"),
}


def recommend_standard(situation: str) -> tuple:
    """Return (standard, reason) for the given scheduling situation.

    'NEITHER' means: do not reach for a stronger fairness rule — fix
    the underlying authority, readiness, or obligation-lifecycle problem.
    """
    assert situation in STANDARD_DECISION_RULE, f"unknown situation {situation}"
    return STANDARD_DECISION_RULE[situation]


# ---------------------------------------------------------------------------
# 2. Eight assumptions. Each must be established with evidence before a
# strong-fairness qualification can be claimed. A missing assumption is
# a missing proof obligation, not a minor deduction.
# ---------------------------------------------------------------------------
# (assumption_id, required_evidence_description)
EIGHT_ASSUMPTIONS = (
    ("PERSISTENT_IDENTITY",
     "the same outstanding obligation (id + revision) survives retry, "
     "requeue, and reassignment"),
    ("GENUINE_ENABLING",
     "the transition is actually permitted and executable whenever it "
     "is recorded as enabled — nominal eligibility is not enough"),
    ("RECURRING_OPPORTUNITY",
     "the environment or upstream system provides infinitely recurring "
     "eligibility under the stated model assumptions"),
    ("SCHEDULER_OBSERVABILITY",
     "each relevant enabling opportunity is visible to the scheduling "
     "mechanism"),
    ("IMPLEMENTABILITY",
     "resource capacity, atomicity, and contention rules permit the "
     "promised service — the model's enabled transition must be a real "
     "possible step"),
    ("STRONGLY_FAIR_SELECTION",
     "an infinitely-often-enabled, outstanding transition cannot be "
     "perpetually ignored by the scheduling policy"),
    ("PROGRESS_AFTER_SERVICE",
     "real execution eventually discharges work, consumes bounded "
     "recovery capacity, or reaches a governed disposition"),
    ("SAFETY_PRESERVATION",
     "fair service cannot bypass LAW, privacy, resource ownership, "
     "current qualification, or idempotency"),
)


def check_assumptions(evidence: dict) -> list:
    """Check the eight assumptions against supplied evidence.

    evidence: {assumption_id: evidence_description_or_None}.
    Returns a list of (assumption_id, satisfied, detail). An unsatisfied
    assumption blocks a strong-fairness qualification claim.
    """
    results = []
    for assumption_id, required in EIGHT_ASSUMPTIONS:
        ev = evidence.get(assumption_id)
        if ev:
            results.append((assumption_id, True,
                            f"established: {ev}"))
        else:
            results.append((assumption_id, False,
                            f"MISSING — required evidence: {required}"))
    return results


def assumptions_satisfied(check_results: list) -> tuple:
    """Do all eight assumptions hold? Returns (ok, missing_ids)."""
    missing = [a for a, ok, _ in check_results if not ok]
    if missing:
        return False, missing
    return True, []


# ---------------------------------------------------------------------------
# 3. Three-proof composition for conditional termination.
#
# The three sub-proofs must be kept distinct:
#   (A) opportunity liveness  — will the transition become enabled again?
#   (B) scheduler fairness    — will an enabled transition get service?
#   (C) execution progress    — will service advance or honestly resolve?
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class ThreeSubProofs:
    """The three independently established sub-proofs for a strong-fairness
    conditional-termination claim."""
    opportunity_recurs: bool      # (A) eligibility recurs infinitely often
                                  #     while the obligation is outstanding
    strong_fairness_applies: bool # (B) the scheduler will eventually give
                                  #     genuine service to the recurring
                                  #     obligation
    service_drives_resolution: bool  # (C) repeated service cannot loop
                                  #     forever: each service either
                                  #     discharges work, consumes bounded
                                  #     recovery, or reaches a governed
                                  #     disposition
    detail: str = ""


def compose_strong_termination(proofs: ThreeSubProofs) -> tuple:
    """Compose the three sub-proofs into a conditional-termination claim.

    Returns (established, verdict, reason). The verdict is CONDITIONAL —
    it is NOT a success guarantee: retry exhaustion may terminate in
    INSUFFICIENT_EVIDENCE or FAILED_RECOVERABLY_EXHAUSTED, and success
    additionally requires VERIFY to confirm the outcome.
    """
    if not proofs.opportunity_recurs:
        return False, "TERMINATION_UNPROVEN", (
            "opportunity liveness not established: if eligibility stops "
            "recurring, strong fairness provides no useful guarantee; "
            "the scheduler is not responsible for manufacturing the "
            "opportunity")
    if not proofs.strong_fairness_applies:
        return False, "TERMINATION_UNPROVEN", (
            "scheduler fairness not established: a repeatedly enabled "
            "obligation may be starved forever without a strongly fair "
            "selection policy")
    if not proofs.service_drives_resolution:
        return False, "TERMINATION_UNPROVEN", (
            "execution progress not established: infinitely serviced "
            "work that only ever retries still fails liveness; service "
            "must drive a ranking decrease or a governed disposition")
    return True, "CONDITIONAL_TERMINATION", (
        "opportunity recurs + strong fairness applies + service drives "
        "finite resolution: the workflow eventually reaches a legitimate "
        "terminal disposition under the stated assumptions. This is NOT "
        "a promise of successful completion.")


# ---------------------------------------------------------------------------
# 4. Flicker-aware fairness-debt accounting.
#
# For intermittently eligible work the ledger must:
#   - count eligible epochs (recurrence evidence),
#   - NEVER reset debt on temporary ineligibility,
#   - NEVER reset debt on reassignment,
#   - NEVER fabricate service,
#   - NEVER execute while actually ineligible.
#
# A finite debt counter is an OPERATIONAL signal, not a formal proof of
# strong fairness (which concerns infinite behavior). The scheduling
# policy must demonstrably prioritize persistent, repeatedly enabled
# obligations for the duty to be real.
# ---------------------------------------------------------------------------
@dataclass
class FlickerLedger:
    """Per-obligation record for intermittently eligible work.

    Extends the fairness ledger with recurrence tracking: eligible
    epochs, usable service opportunities, and service events — the
    operational evidence for the GF E_o premise.
    """
    obligation_id: str
    fairness_policy: str = "STRONG"     # WEAK | STRONG | BOUNDED
    obligation_status: str = "OUTSTANDING"
    eligible_epochs: int = 0           # rounds where eligible=True
    usable_service_opportunities: int = 0  # epochs with genuine, schedulable
                                          # opportunity (see schedulability)
    service_events: int = 0            # rounds with adequate service
    fairness_debt: int = 0             # eligible epochs without service
    worker_reassignments: int = 0
    verified_proof_progress: int = 0
    remaining_recovery_budget: int = 0
    last_service_receipt: str = ""

    def record_round(self, eligible: bool, adequate_service: bool,
                     service_receipt: str = "",
                     usable_opportunity: bool = True) -> tuple:
        """Record one scheduler round for a flickering obligation.

        - Ineligible round: eligible_epochs unchanged, debt UNCHANGED
          (no reset, no accrual — no fairness duty while ineligible).
        - Eligible + adequate service: debt -> 0, service event recorded.
        - Eligible + inadequate service: eligible_epochs += 1, debt += 1.
        usable_opportunity=False marks a nominal-but-not-executable
        window: it counts NEITHER as recurrence evidence NOR as a
        missed opportunity (apparent eligibility is not a usable
        scheduling opportunity — fix readiness first).
        """
        if not eligible:
            return True, self.fairness_debt, (
                f"{self.obligation_id}: ineligible round — debt unchanged "
                f"at {self.fairness_debt} (no reset through temporary "
                f"ineligibility)")
        if not usable_opportunity:
            return True, self.fairness_debt, (
                f"{self.obligation_id}: nominal eligibility only, not a "
                f"usable opportunity — excluded from recurrence and debt "
                f"accounting")
        self.eligible_epochs += 1
        self.usable_service_opportunities += 1
        if adequate_service:
            self.service_events += 1
            self.fairness_debt = 0
            if service_receipt:
                self.last_service_receipt = service_receipt
            return True, 0, (
                f"{self.obligation_id}: adequate service in eligible "
                f"epoch {self.eligible_epochs}; debt reset to 0")
        self.fairness_debt += 1
        return True, self.fairness_debt, (
            f"{self.obligation_id}: eligible epoch {self.eligible_epochs} "
            f"without adequate service; debt now {self.fairness_debt}")

    def reassign(self, from_worker: str, to_worker: str) -> tuple:
        """Reassignment preserves EVERYTHING: debt, epochs, budget.
        Resetting any of them is rejected."""
        self.worker_reassignments += 1
        return True, self.fairness_debt, (
            f"{self.obligation_id}: reassigned {from_worker}->{to_worker} "
            f"(#{self.worker_reassignments}); debt={self.fairness_debt}, "
            f"eligible_epochs={self.eligible_epochs}, "
            f"budget={self.remaining_recovery_budget} — all preserved")


def strong_fairness_duty_owed(ledger: FlickerLedger,
                              starvation_threshold: int) -> tuple:
    """Does the scheduler owe this obligation service now?

    A strong-fairness duty is owed when the obligation is OUTSTANDING,
    its fairness policy is STRONG, and its debt has reached the
    operational starvation threshold. The duty is to provide a genuine
    service opportunity — never to execute without permission.
    Returns (owed, reason).
    """
    if ledger.obligation_status != "OUTSTANDING":
        return False, (
            f"{ledger.obligation_id}: no duty — obligation is "
            f"{ledger.obligation_status}, fairness obligation terminates "
            f"appropriately")
    if ledger.fairness_policy != "STRONG":
        return False, (
            f"{ledger.obligation_id}: policy is {ledger.fairness_policy}, "
            f"not STRONG — no strong-fairness duty")
    if ledger.fairness_debt >= starvation_threshold:
        return True, (
            f"{ledger.obligation_id}: STRONG-fairness duty owed — debt "
            f"{ledger.fairness_debt} >= threshold {starvation_threshold} "
            f"across {ledger.eligible_epochs} eligible epochs; scheduler "
            f"must provide a genuine service opportunity (permission "
            f"gates unchanged)")
    return False, (
        f"{ledger.obligation_id}: debt {ledger.fairness_debt} below "
        f"threshold {starvation_threshold}; no duty yet")


# ---------------------------------------------------------------------------
# 5. Finite-abstraction model checker for the weak-vs-strong distinction.
#
# A schedule is a finite sequence of rounds. Each round: (eligible, served)
# where served implies a genuine service opportunity was provided.
# Two scheduler policies:
#   WEAK_ONLY  — serves an obligation only when it has been continuously
#                eligible for `patience` consecutive rounds.
#   STRONG     — serves any outstanding obligation whose fairness debt
#                reaches `threshold`, regardless of eligibility gaps.
# The checker asks: does the policy admit a starvation trace — an
# obligation eligible infinitely often (in the finite sense: eligible in
# unboundedly many rounds of a repeating pattern) that is never served?
# ---------------------------------------------------------------------------
def simulate_policy(schedule_pattern: list, policy: str,
                    patience: int = 3, threshold: int = 4,
                    repeats: int = 30) -> dict:
    """Simulate a scheduler policy over a repeating eligibility pattern.

    schedule_pattern: list of bool — eligible per round in one period.
    policy: "WEAK_ONLY" or "STRONG".
    Returns {served_rounds, missed_eligible_epochs, max_debt,
             starved: bool}.
    starved=True means the pattern admits a starvation trace under the
    policy: eligible epochs recur without bound while service never
    arrives — exactly what strong fairness must exclude.
    """
    assert policy in ("WEAK_ONLY", "STRONG")
    consecutive = 0
    debt = 0
    served_rounds = []
    missed = 0
    max_debt = 0
    n = 0
    for _ in range(repeats):
        for eligible in schedule_pattern:
            n += 1
            if not eligible:
                consecutive = 0
                # WEAK_ONLY: ineligibility breaks continuity; debt is
                # tracked but the weak policy never acts on flicker.
                continue
            consecutive += 1
            debt += 1
            max_debt = max(max_debt, debt)
            serve = False
            if policy == "WEAK_ONLY":
                serve = consecutive >= patience
            else:  # STRONG
                serve = debt >= threshold
            if serve:
                served_rounds.append(n)
                debt = 0
                consecutive = 0
            else:
                missed += 1
    starved = (missed > 0 and not served_rounds
               and any(schedule_pattern))
    return {
        "policy": policy,
        "rounds": n,
        "served_rounds": served_rounds,
        "missed_eligible_epochs": missed,
        "max_debt": max_debt,
        "starved": starved,
    }


def check_weak_starvation_counterexample(schedule_pattern: list,
                                         patience: int = 3,
                                         repeats: int = 30) -> tuple:
    """Is this flicker pattern a valid weak-fairness starvation
    counterexample? Returns (is_counterexample, evidence).

    A valid counterexample: the obligation is eligible infinitely often
    (recurs in every period) yet a WEAK_ONLY scheduler never serves it —
    proving weak fairness does not exclude the starvation trace.
    """
    weak = simulate_policy(schedule_pattern, "WEAK_ONLY",
                           patience=patience, repeats=repeats)
    if not any(schedule_pattern):
        return False, "pattern never eligible: no fairness duty at all"
    if weak["starved"]:
        return True, (
            f"valid weak-fairness starvation counterexample: pattern "
            f"{schedule_pattern} eligible every period, WEAK_ONLY "
            f"served {len(weak['served_rounds'])} times over "
            f"{weak['rounds']} rounds, missed "
            f"{weak['missed_eligible_epochs']} eligible epochs")
    return False, (
        f"WEAK_ONLY served the obligation "
        f"{len(weak['served_rounds'])} times — no starvation trace")


def check_strong_excludes_starvation(schedule_pattern: list,
                                     threshold: int = 4,
                                     repeats: int = 30) -> tuple:
    """Does the STRONG policy exclude the starvation trace for this
    pattern? Returns (excluded, evidence)."""
    strong = simulate_policy(schedule_pattern, "STRONG",
                             threshold=threshold, repeats=repeats)
    if not any(schedule_pattern):
        return True, "pattern never eligible: nothing to exclude"
    if strong["starved"]:
        return False, (
            f"STRONG policy FAILED to exclude starvation: missed "
            f"{strong['missed_eligible_epochs']} eligible epochs with "
            f"zero service")
    return True, (
        f"STRONG policy excludes the starvation trace: served "
        f"{len(strong['served_rounds'])} times, max debt "
        f"{strong['max_debt']}")


# ---------------------------------------------------------------------------
# Schedulability: a nominal eligibility window is not automatically a
# usable opportunity. A 1us resource release with a 10ms dispatch cost
# is not actionable. The protocol may need reservation, durable queue
# entries, atomic claims, or ownership transfer to turn intermittent
# availability into an executable opportunity.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class SchedulabilityAssessment:
    """Is an observed eligibility window actually usable?"""
    window_description: str
    window_us: float               # observed availability window, microseconds
    dispatch_cost_us: float        # cost to assign a worker, microseconds
    mechanism: str = ""            # reservation / queue / atomic-claim /
                                   # ownership-transfer / none

    def usable(self) -> tuple:
        if self.dispatch_cost_us <= 0:
            return False, "dispatch cost unknown: cannot assess usability"
        if self.window_us < self.dispatch_cost_us:
            return False, (
                f"window {self.window_us}us < dispatch cost "
                f"{self.dispatch_cost_us}us: NOT a usable opportunity — "
                f"strong fairness is not a substitute for fixing this "
                f"mismatch (need: {self.mechanism or 'a reservation/claim '
                'mechanism'})")
        return True, (
            f"window {self.window_us}us >= dispatch cost "
            f"{self.dispatch_cost_us}us: usable opportunity")


# ---------------------------------------------------------------------------
# Strong-fairness contract: extends FairnessContract with the recurrence
# and schedulability evidence the GF E_o premise requires.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class StrongFairnessContract:
    """Machine-readable strong-fairness contract for one obligation."""
    obligation_id: str
    revision: str
    eligibility_predicate: str
    service_predicate: str
    # The GF E_o premise, operationalized:
    recurrence_basis: str = ""        # why eligibility recurs infinitely
                                      # often under the model assumptions
    schedulability_mechanism: str = ""  # reservation / queue /
                                      # atomic-claim / ownership-transfer
    starvation_threshold_epochs: int = 0  # operational debt threshold
    wait_accounting: str = "ELIGIBLE_EPOCHS_NO_RESET_ON_FLICKER"
    preserve_across_reassignment: bool = True

    def __post_init__(self):
        assert self.obligation_id, "contract needs an obligation id"
        assert self.eligibility_predicate, "eligibility predicate required"
        assert self.service_predicate, "service predicate required"
        assert self.recurrence_basis, (
            "STRONG fairness needs a stated recurrence basis — the "
            "GF E_o premise must be evidenced, not assumed")
        assert self.starvation_threshold_epochs > 0, (
            "STRONG fairness needs an operational starvation threshold")

    def to_fairness_contract(self) -> FairnessContract:
        return FairnessContract(
            obligation_id=self.obligation_id,
            revision=self.revision,
            standard="STRONG",
            eligibility_predicate=self.eligibility_predicate,
            service_predicate=self.service_predicate,
            wait_accounting=self.wait_accounting,
            preserve_across_reassignment=self.preserve_across_reassignment,
        )
