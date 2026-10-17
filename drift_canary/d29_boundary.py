"""D29 — Environment–Scheduler–Worker Responsibility Boundary (fixture).

Implements the decisive D29 experiment: a controlled KNOW → LAW → ACT →
VERIFY workflow with three injected failures. An independent verifier
classifies each failure from EVIDENCE ALONE — never from component
narrative labels — and the same observable symptom (an uncompleted
workflow) must classify differently depending on independently
established environmental availability, scheduler service, and worker
execution evidence.

Core rule (D29): a component cannot convert its own failure into another
component's assumption. Responsibility follows control. The controller
field of the responsibility record is decisive; no agent narrative
overrides the independently established control boundary.

Composes (extends, never duplicates):
  fairness.py — service ladder, FairnessLedger, DeterministicScheduler,
                event_adequate_service, assess_three_truths,
                compose_conditional_liveness.
  progress.py — ProofObligation, discharge, classify_transition.
  liveness.py — detect_starvation (independent cross-check).

The D29 layer added here is: the independent environment witness, the
versioned responsibility record, and the evidence-based boundary
classifier. None of those exist in the three contracts — that is the gap
this fixture fills, as specified.

SPEC + deterministic fixture machinery. NOT wired into kernel/, KNOW,
LAW, ACT, or any live path. Wiring needs Shawn's word.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from drift_canary.fairness import (
    DeterministicScheduler,
    FairnessContract,
    FairnessLedger,
    ThreeTruths,
    assess_three_truths,
    compose_conditional_liveness,
    event_adequate_service,
    ladder_rank,
)
from drift_canary.progress import (
    ProofObligation,
    classify_transition,
    discharge,
)

# ---------------------------------------------------------------------------
# Verdict vocabulary. The verifier may ONLY emit these; it may never emit
# a component's narrative label as a verdict.
# ---------------------------------------------------------------------------
VERDICTS = (
    "ENVIRONMENT_BLOCKER",       # external resource genuinely unavailable
    "SCHEDULER_STARVATION",       # eligible work never dispatched
    "SCHEDULER_SERVICE_FAILURE",  # dispatched but no usable service provided
    "WORKER_NONPROGRESS",         # adequate service, no verified advancement
    "BOUNDARY_UNDETERMINED",      # evidence insufficient — not blame-by-default
    "COMPLETED",                  # the workflow actually completed
)

CONTROLLERS = (
    "ENVIRONMENT",
    "SCHEDULER",
    "WORKER",
    "UNDETERMINED",
)

# The three canonical fault injections of the D29 decisive experiment.
CASES = ("A", "B", "C")

# Obligation under test: D29's sharpest case — ACT eligible to run but
# does not receive a database connection.
OBLIGATION_ID = "ACT-042"
WORKFLOW_ID = "WF-D29"
RESOURCE_ID = "DB-CONN"


# ---------------------------------------------------------------------------
# Evidence structures.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class EnvironmentObservation:
    """One INDEPENDENT observation of external resource conditions.

    Produced by the environment witness — never by the scheduler or the
    worker. A single worker-produced log must not certify what the
    environment did.
    """
    seq: int
    resource_id: str
    available: bool
    scope: str = ""


@dataclass(frozen=True)
class ComponentReport:
    """What a component CLAIMS happened. Narrative only.

    The verifier must NEVER consult these labels when determining
    responsibility; they exist so the fixture can prove false blame does
    not move the verdict.
    """
    component: str   # ENVIRONMENT | SCHEDULER | WORKER
    label: str       # e.g. DATABASE_UNAVAILABLE, SCHEDULER_STARVATION
    seq: int = 0


@dataclass(frozen=True)
class ResponsibilityRecord:
    """D29's versioned responsibility record for one liveness condition.

    The controller field is decisive: an agent's narrative about who
    caused a failure cannot override the independently established
    control boundary.
    """
    condition: str
    controller: str              # one of CONTROLLERS
    producer_guarantee: str
    consumer_assumption: str
    evidence_refs: tuple
    classification: str          # one of VERDICTS
    revision: str = "v1"

    def __post_init__(self):
        assert self.controller in CONTROLLERS, self.controller
        assert self.classification in VERDICTS, self.classification


@dataclass
class BoundaryCaseResult:
    """Everything the independent verifier used and produced for one
    injected failure — evidence in, verdict out, labels ignored."""
    case: str
    verdict: str
    record: ResponsibilityRecord
    truths: ThreeTruths
    liveness_verdict: str
    obligation: ProofObligation
    ledger: FairnessLedger           # the scheduler evidence, for re-derivation
    env_observations: tuple
    component_reports: tuple     # narrative labels; NOT used for the verdict
    serviced_rounds: int
    advanced_rounds: int
    detail: str = ""


# ---------------------------------------------------------------------------
# The independent boundary verifier.
# ---------------------------------------------------------------------------
def classify_boundary(env_observations: tuple,
                      ledger: FairnessLedger,
                      obligation_id: str,
                      serviced_rounds: int,
                      advanced_rounds: int,
                      debt_threshold: int = 3) -> tuple:
    """Classify responsibility from EVIDENCE ALONE.

    Precedence is the D29 rule, in order:
      1. Environment: if the resource was never available per the
         independent witness, the blocker is environmental — scheduler
         fairness debt accrued in that window is EXPLAINED, not blame.
      2. Scheduler: eligible work waited without adequate service while
         the resource was available. Dispatch-without-service and
         never-dispatched are distinguished by the ladder evidence.
      3. Worker: adequate service was delivered but produced no verified
         advancement or governed disposition.
      4. Otherwise: BOUNDARY_UNDETERMINED — never blame-by-default.

    Returns (verdict, controller, reason). Component narrative labels are
    not an input at all: there is no parameter for them to enter through.
    """
    avail = [o.available for o in env_observations]
    if avail and not any(avail):
        return ("ENVIRONMENT_BLOCKER", "ENVIRONMENT",
                "resource never available per independent environment "
                "witness; scheduler/worker inactivity in that window is "
                "explained, not blame")
    debt = ledger.debt(obligation_id)
    if debt >= debt_threshold:
        # Distinguish withholding from dispatch-without-service by the
        # highest ladder rung actually evidenced while eligible.
        max_rung = max(
            (ladder_rank(e.rung) for e in ledger.history
             if e.obligation_id == obligation_id and e.eligible),
            default=-1,
        )
        if max_rung >= ladder_rank("DISPATCHED"):
            return ("SCHEDULER_SERVICE_FAILURE", "SCHEDULER",
                    f"debt={debt} >= threshold {debt_threshold} with "
                    f"resource available: dispatched but never provided "
                    f"usable service (DISPATCHED-ONLY is not service)")
        return ("SCHEDULER_STARVATION", "SCHEDULER",
                f"debt={debt} >= threshold {debt_threshold} with resource "
                f"available: eligible work was never dispatched")
    if serviced_rounds > 0 and advanced_rounds == 0:
        return ("WORKER_NONPROGRESS", "WORKER",
                "adequate service delivered but no verified advancement "
                "or governed disposition: progress-on-service failed")
    return ("BOUNDARY_UNDETERMINED", "UNDETERMINED",
            "evidence insufficient to assign responsibility; "
            "withholding blame by default")


# ---------------------------------------------------------------------------
# The three injected failures.
# ---------------------------------------------------------------------------
def _contract() -> FairnessContract:
    return FairnessContract(
        obligation_id=OBLIGATION_ID,
        revision="v1",
        standard="WEAK",
        eligibility_predicate="ELIGIBLE_WHEN_RUNNABLE",
        service_predicate="USABLE_EXECUTION_OPPORTUNITY",
    )


def run_case(case: str, rounds: int = 6,
             false_blame: tuple = ()) -> BoundaryCaseResult:
    """Run one D29 fault injection through a scripted KNOW → LAW → ACT →
    VERIFY workflow.

    case "A": environment failure — the DB connection is genuinely
        unavailable every round. Scheduler dispatches (DISPATCHED-ONLY:
        no usable service possible); worker never receives service.
    case "B": scheduler failure — resource available, obligation eligible,
        but the scheduler withholds dispatch indefinitely.
    case "C": worker failure — adequate service every round, but the
        worker never advances the obligation.

    false_blame: tuple of ComponentReport — narrative labels the failing
    (or any) component emits. Recorded on the result; never consulted by
    the verifier.

    In ALL cases the workflow ends uncompleted (the same observable
    symptom); only the evidence — and therefore the verdict — differs.
    """
    assert case in CASES, f"unknown D29 case {case}"
    assert rounds > 0

    env_available = {"A": False, "B": True, "C": True}[case]
    env_observations = tuple(
        EnvironmentObservation(seq=i, resource_id=RESOURCE_ID,
                               available=env_available,
                               scope="fixture-window")
        for i in range(1, rounds + 1)
    )

    ledger = FairnessLedger()
    ledger.register(_contract())
    sched = DeterministicScheduler(ledger)

    obligation = ProofObligation(
        obligation_id=OBLIGATION_ID, revision="v1", rank=1,
        composition="ATOMIC",
        acceptance="ACT executes against DB-CONN and records outcome",
        proof_standard="INDEPENDENT_VERIFICATION",
        retries_remaining=3,
    )

    for i in range(1, rounds + 1):
        if case == "A":
            # Scheduler makes its valid request; the resource is down, so
            # no usable service can be evidenced. DISPATCHED-ONLY.
            sched.round(OBLIGATION_ID, WORKFLOW_ID, eligible=True,
                        rung="DISPATCHED",
                        evidence={"lease_id": f"L-A-{i}"},
                        note="dispatch attempted; resource unavailable")
            # Worker receives nothing usable: no attempts.
        elif case == "B":
            # Scheduler withholds: eligible, never dispatches.
            sched.round(OBLIGATION_ID, WORKFLOW_ID, eligible=True,
                        rung="SELECTED", evidence={},
                        note="eligible but never dispatched")
        else:  # case C
            # Adequate service every round: full evidence, debt resets.
            sched.round(
                OBLIGATION_ID, WORKFLOW_ID, eligible=True, rung="SERVICED",
                evidence={"lease_id": f"L-C-{i}",
                          "worker_ack": f"ACK-C-{i}",
                          "resources_available": True},
                note="usable execution opportunity delivered")
            # Worker attempts but never advances: FAILED_RETRY consumes
            # budget; the obligation stays OUTSTANDING.
            ok, (proof, term), _ = classify_transition(
                "FAILED_RETRY",
                prev_ranks=(1,), next_ranks=(1,),
                retries_before=3, retries_after=2, discharged=False)
            assert ok and not proof and term

    serviced_rounds = sum(
        1 for e in ledger.history
        if e.obligation_id == OBLIGATION_ID and event_adequate_service(e)[0]
    )
    advanced_rounds = 0  # nothing ever discharged in any case: same symptom
    assert obligation.state == "OUTSTANDING"

    truths = assess_three_truths(
        ledger, OBLIGATION_ID, debt_threshold=3,
        serviced_rounds=serviced_rounds,
        advanced_rounds=advanced_rounds,
        rank_decreasing=False)
    _, liveness_verdict, _ = compose_conditional_liveness(truths)

    verdict, controller, reason = classify_boundary(
        env_observations, ledger, OBLIGATION_ID,
        serviced_rounds, advanced_rounds, debt_threshold=3)

    record = ResponsibilityRecord(
        condition="usable_execution_opportunity",
        controller=controller,
        producer_guarantee={
            "ENVIRONMENT": "resource offer observable under stated conditions",
            "SCHEDULER": "eligible obligation fairly serviced",
            "WORKER": "attempt outcome recorded",
            "UNDETERMINED": "no established producer guarantee",
        }[controller],
        consumer_assumption="worker receives an assigned, usable connection",
        evidence_refs=(f"env:{RESOURCE_ID}",
                       f"ledger:{OBLIGATION_ID}",
                       f"obligation:{OBLIGATION_ID}:v1"),
        classification=verdict,
        revision="v1",
    )
    return BoundaryCaseResult(
        case=case, verdict=verdict, record=record, truths=truths,
        liveness_verdict=liveness_verdict, obligation=obligation,
        ledger=ledger,
        env_observations=env_observations,
        component_reports=tuple(false_blame),
        serviced_rounds=serviced_rounds,
        advanced_rounds=advanced_rounds,
        detail=f"case {case}: {reason}")


def verify_against_ledger(result: BoundaryCaseResult) -> tuple:
    """Independent cross-check: recompute scheduler debt from the raw
    event history and confirm the verdict's scheduler premise.

    Returns (ok, reason). This is the D28-style independent audit applied
    to the D29 fixture: the classifier's inputs are re-derived, not
    trusted.
    """
    ledger = result.ledger
    debt = 0
    for e in sorted((x for x in ledger.history
                     if x.obligation_id == OBLIGATION_ID),
                    key=lambda x: x.seq):
        if not e.eligible:
            continue
        adequate, _ = event_adequate_service(e)
        debt = 0 if adequate else debt + 1
    if result.verdict in ("SCHEDULER_STARVATION",
                          "SCHEDULER_SERVICE_FAILURE") and debt < 3:
        return False, ("verdict blames scheduler but recomputed debt "
                       f"{debt} is below threshold")
    if result.verdict == "WORKER_NONPROGRESS" and debt != 0:
        return False, ("verdict blames worker but scheduler debt "
                       f"{debt} != 0: service was not adequate")
    if result.verdict == "ENVIRONMENT_BLOCKER" and any(
            o.available for o in result.env_observations):
        return False, "verdict claims environment but resource was available"
    return True, "verdict premises independently re-derived from evidence"
