"""Responsibility-boundary contract: assign every condition, decision and
progress guarantee to the component that actually controls it (spec).

Principle: "Control determines responsibility. Contracts define
guarantees. Independent evidence establishes what occurred. No component
may move its own obligations into another component's assumptions merely
by changing a status, label, interface description or model-checking
configuration."

This prevents three common failures:
  1. A scheduler calls its own resource-allocation failure an
     environment outage.
  2. A worker calls repeated unsuccessful execution a scheduler problem,
     despite receiving usable service.
  3. An environment assumption guarantees eventual service, hiding the
     very scheduler fairness defect the model checker should find.

Ownership table:
  ENVIRONMENT  owns external resource conditions, availability, and
               independently controlled prerequisites. Must establish:
               conditions necessary for a transition to become possible.
               Cannot claim: scheduler selection or service.
  SCHEDULER    owns queue policy, allocation, dispatch, worker selection,
               scheduler-controlled resources. Must establish: eligible
               work receives the promised usable service. Cannot claim:
               service completed the task.
  WORKER       owns execution attempts, task logic, bounded recovery,
               outcome production. Must establish: adequate service
               produces the specified progress or a valid disposition.
               Cannot claim: a dispatch alone proves its work succeeded.
  VERIFY       owns independent assessment of all three. Must establish:
               source-bound evidence, valid assumptions, correct
               verdicts. Cannot claim: authority to execute or weaken
               the requirements.
  LAW          is the authority boundary governing what operations are
               permitted. It is NEVER an environmental convenience that
               may be assumed away.

Proof composition (no circularity):
  A_E /\\ S   |= G_S        scheduler fair-service guarantee, PROVED
  A_E /\\ G_S /\\ W |= G_W  worker conditional progress guarantee, PROVED
G_S must be proved; it cannot appear among the scheduler's environmental
assumptions. A worker may assume genuine usable service, never its own
successful output. Five distinct stages are tracked: environmental
possibility, scheduler opportunity, actual service, verified
advancement, terminal disposition.

Composes with:
  fairness_verify.py — AssumptionContract, vacuity detection, the
                       independence review (this module references the
                       sibling FAAP registry's `control_boundary`
                       field; it does not duplicate the registry).
  fairness.py        — service ladder (dispatch != service).
  progress.py        — proof vs termination progress (service != proof).
  liveness.py        — WAITING_AUTHORITY; liveness never creates
                       permission; LAW stays the authority boundary.

SPEC + deterministic machinery. NOT wired into kernel/, KNOW, LAW, ACT,
or any live path. Wiring needs Shawn's word.
"""
from __future__ import annotations

from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# 1. Component ownership table.
# ---------------------------------------------------------------------------
COMPONENTS = ("ENVIRONMENT", "SCHEDULER", "WORKER", "VERIFY", "LAW")

OWNERSHIP = {
    "ENVIRONMENT": {
        "owns": (
            "external resource conditions",
            "service availability",
            "independently controlled prerequisites",
        ),
        "must_establish": (
            "conditions necessary for a transition to become possible",
        ),
        "cannot_claim": (
            "that the scheduler selected or serviced the transition",
        ),
    },
    "SCHEDULER": {
        "owns": (
            "queue policy",
            "resource allocation",
            "dispatch",
            "worker selection",
            "scheduler-controlled resources",
        ),
        "must_establish": (
            "eligible work receives the promised usable service",
        ),
        "cannot_claim": (
            "that service completed the task",
        ),
    },
    "WORKER": {
        "owns": (
            "execution attempts",
            "task logic",
            "bounded recovery",
            "outcome production",
        ),
        "must_establish": (
            "adequate service produces the specified progress "
            "or a valid disposition",
        ),
        "cannot_claim": (
            "that a dispatch alone proves its work succeeded",
        ),
    },
    "VERIFY": {
        "owns": (
            "independent assessment of environment, scheduler, worker",
        ),
        "must_establish": (
            "source-bound evidence",
            "valid assumptions",
            "correct verdicts",
        ),
        "cannot_claim": (
            "authority to execute or weaken the requirements",
        ),
    },
    "LAW": {
        "owns": (
            "the authority boundary governing permitted operations",
        ),
        "must_establish": (
            "which operations are permitted, by whom, under what "
            "authorization",
        ),
        "cannot_claim": (),
        "never_assumable_away": True,
    },
}

# The five stages of a liveness claim; each belongs to a component.
STAGES = (
    "ENVIRONMENTAL_POSSIBILITY",   # ENVIRONMENT
    "SCHEDULER_OPPORTUNITY",       # SCHEDULER
    "ACTUAL_SERVICE",              # SCHEDULER -> WORKER handoff
    "VERIFIED_ADVANCEMENT",        # VERIFY (worker progress, checked)
    "TERMINAL_DISPOSITION",        # VERIFY (governed resolution)
)

STAGE_OWNER = {
    "ENVIRONMENTAL_POSSIBILITY": "ENVIRONMENT",
    "SCHEDULER_OPPORTUNITY": "SCHEDULER",
    "ACTUAL_SERVICE": "SCHEDULER",
    "VERIFIED_ADVANCEMENT": "VERIFY",
    "TERMINAL_DISPOSITION": "VERIFY",
}

# Canonical demo: the label alone tells nothing about responsibility.
# DATABASE_UNAVAILABLE has three different owners depending on control.
DATABASE_UNAVAILABLE_CASES = (
    {
        "case": "external database down despite valid scheduler request",
        "controller": "ENVIRONMENT",
        "classification": "ENVIRONMENT",
    },
    {
        "case": "database available but scheduler never assigns a connection",
        "controller": "SCHEDULER",
        "classification": "SCHEDULER",
    },
    {
        "case": "worker receives the connection but uses it incorrectly",
        "controller": "WORKER",
        "classification": "WORKER",
    },
)

FAILURE_CLASSIFICATIONS = (
    "ENVIRONMENT",
    "SCHEDULER",
    "WORKER",
    "SHARED",        # must be decomposed before it can govern anything
    "UNDETERMINED",  # evidence insufficient; investigate, never auto-blame
)


# ---------------------------------------------------------------------------
# 2. Proof composition: A_E /\ S |= G_S ; A_E /\ G_S /\ W |= G_W.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class ProofContract:
    """Machine-checkable proof composition for one liveness claim.

    environmental_assumptions: A_E — independently justified, never
        scheduler-controlled conditions disguised as environment.
    scheduler_model: S — the scheduler behavior under test.
    worker_model: W — the worker behavior under test.
    scheduler_guarantee: G_S — the fair-service guarantee to PROVE.
    worker_guarantee: G_W — the conditional progress guarantee to PROVE.
    """
    contract_id: str
    environmental_assumptions: tuple
    scheduler_model: str
    worker_model: str
    scheduler_guarantee: str
    worker_guarantee: str

    def __post_init__(self):
        assert self.contract_id
        lowered = " ".join(self.environmental_assumptions).lower()
        # G_S cannot appear among the scheduler's environmental
        # assumptions — that is assuming the result.
        if "fair" in lowered and "fair" in self.scheduler_guarantee.lower():
            raise AssertionError(
                "circular proof contract: the scheduler's fair-service "
                "guarantee appears among its environmental assumptions"
            )


def check_worker_assumption(assumed: str) -> tuple:
    """A worker may assume genuine usable service, never its own output.

    Returns (ok, finding). Assuming successful output is assuming the
    conclusion of the worker's own proof obligation.
    """
    text = assumed.lower()
    if any(k in text for k in ("output succeeded", "task completed",
                               "work succeeded", "outcome achieved")):
        return (False, "CIRCULAR: worker assumes its own successful "
                       "output — G_W must be proved from service, not "
                       "assumed")
    if "usable service" in text or "genuine service" in text:
        return (True, "worker may assume genuine usable service")
    return (True, "assumption is not a worker-output claim")


def check_law_not_assumed(assumptions: tuple) -> tuple:
    """LAW is the authority boundary; it may never be assumed away.

    Returns (ok, finding).
    """
    for a in assumptions:
        text = a.lower()
        if ("law" in text and ("assume" in text or "waive" in text
                               or "bypass" in text)):
            return (False, "LAW cannot be assumed away: authority is a "
                           "boundary, not an environmental convenience")
    return (True, "LAW intact as authority boundary")


# ---------------------------------------------------------------------------
# 3. Versioned responsibility records. `controller` is the PRIMARY field.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class ResponsibilityRecord:
    """One condition's responsibility, pinned to its controller.

    An agent's narrative about who caused a failure cannot override the
    independently established control boundary. `controller` is primary;
    everything else is interpreted through it.
    """
    condition: str
    controller: str                    # PRIMARY: who controls the condition
    producer_guarantee: str
    consumer_assumption: str
    observation_boundary: str          # where the handoff is observable
    evidence: tuple                    # independent receipts
    failure_classification: str        # one of FAILURE_CLASSIFICATIONS
    applicable_version: str            # exact runtime/interface revisions

    def __post_init__(self):
        assert self.condition and self.controller
        assert self.controller in COMPONENTS, (
            f"unknown controller {self.controller}")
        assert self.failure_classification in FAILURE_CLASSIFICATIONS, (
            f"unknown classification {self.failure_classification}")
        if self.failure_classification == "SHARED":
            raise AssertionError(
                "SHARED ownership must be decomposed into per-component "
                "guarantees before it can govern anything — use "
                "decompose_shared()")


def classify_with_narrative(record: ResponsibilityRecord,
                            narrative_blame: str) -> tuple:
    """Classify a failure by control, never by narrative.

    Returns (classification, reason). A component's story about who
    caused the failure cannot override the record's controller.
    """
    if narrative_blame != record.controller:
        return (record.failure_classification,
                f"narrative blames {narrative_blame} but the independently "
                f"established controller is {record.controller}: control "
                f"determines responsibility, not the story")
    return (record.failure_classification,
            f"narrative agrees with controller {record.controller}")


def decompose_shared(condition: str, parts: tuple,
                     applicable_version: str) -> tuple:
    """Decompose genuinely shared ownership into per-component records.

    Each part: (controller, producer_guarantee, consumer_assumption,
    observation_boundary, evidence). Each resulting record carries its
    own proof; the SHARED label never governs.
    """
    records = []
    for (controller, producer_guarantee, consumer_assumption,
            observation_boundary, evidence) in parts:
        records.append(ResponsibilityRecord(
            condition=f"{condition} [{controller}]",
            controller=controller,
            producer_guarantee=producer_guarantee,
            consumer_assumption=consumer_assumption,
            observation_boundary=observation_boundary,
            evidence=tuple(evidence),
            failure_classification=controller,
            applicable_version=applicable_version,
        ))
    return tuple(records)


# Join point with the sibling FAAP registry: FAAP owns assumption
# records with a `control_boundary` field. This module references them
# by duck-typing (the sibling builds concurrently); no hard import, no
# duplicated registry.
def link_assumption(assumption) -> tuple:
    """Check a FAAP assumption record's control boundary against ownership.

    Expects an object with `assumption_id` and `control_boundary`
    attributes. Returns (ok, finding).
    """
    boundary = getattr(assumption, "control_boundary", None)
    aid = getattr(assumption, "assumption_id", "?")
    if boundary is None:
        return (False, f"assumption {aid} has no control_boundary: "
                       "unlinked assumptions cannot restrict the model")
    if boundary not in COMPONENTS:
        return (False, f"assumption {aid} control_boundary {boundary} "
                       "is not a recognized component")
    return (True, f"assumption {aid} linked to controller {boundary}")


# ---------------------------------------------------------------------------
# 4. Interface compatibility: G_producer => A_consumer, in matching scope.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class InterfaceEdge:
    """One producer -> consumer handoff in the liveness claim."""
    edge_id: str
    producer: str            # component
    consumer: str            # component
    producer_guarantee: str
    consumer_assumption: str
    scope: str               # matching scope/time/versions/environment


# Strength ordering for the canonical guarantee vocabulary. A producer
# guarantee weaker than the consumer assumption is an interface
# mismatch — never silently strengthened.
GUARANTEE_STRENGTH = {
    "never": 0,
    "occasionally": 1,
    "repeatedly": 2,
    "always": 3,
}


def guarantee_strength(text: str):
    """Map a guarantee/assumption text to a coarse strength level.

    Returns None when the text uses no recognized strength word.
    """
    lowered = text.lower()
    for word, level in GUARANTEE_STRENGTH.items():
        if word in lowered:
            return level
    return None


def check_interface(edge: InterfaceEdge) -> tuple:
    """Check G_producer => A_consumer within matching scope.

    Returns (ok, findings). A weaker producer guarantee than the
    consumer assumption is a mismatch; the environment is never
    silently strengthened to make the consumer's proof pass.
    """
    findings = []
    g = guarantee_strength(edge.producer_guarantee)
    a = guarantee_strength(edge.consumer_assumption)
    if g is not None and a is not None and g < a:
        findings.append(
            f"INTERFACE MISMATCH on {edge.edge_id}: producer guarantees "
            f"'{edge.producer_guarantee}' (strength {g}) but consumer "
            f"assumes '{edge.consumer_assumption}' (strength {a}) — the "
            f"environment must not be silently strengthened")
    ok = not findings
    return (ok, findings)


def detect_circular_chain(edges: tuple) -> tuple:
    """Reject circular proof-justification chains.

    A chain like SCHEDULER fairness -> ENVIRONMENT availability ->
    SCHEDULER fairness is circular unless decomposed into
    independently justified, non-circular contracts. Circular
    operational graphs are not auto-invalid; circular proof
    justification without an independent foundation is.
    Returns (ok, findings).
    """
    findings = []
    # Build a justification graph: consumer assumption depends on
    # producer guarantee. Look for cycles that pass through a
    # fairness claim about the component being verified.
    nodes = {}
    for e in edges:
        nodes.setdefault(e.consumer, set()).add(e.producer)
    # Simple cycle detection over the component graph.
    def has_cycle(start, current, seen):
        for nxt in nodes.get(current, ()):  # current depends on nxt
            if nxt == start:
                return True
            if nxt not in seen and has_cycle(start, nxt, seen | {nxt}):
                return True
        return False
    for comp in nodes:
        if has_cycle(comp, comp, {comp}):
            text = " ".join(
                (e.producer_guarantee + " " + e.consumer_assumption)
                for e in edges).lower()
            if "fair" in text:
                findings.append(
                    f"CIRCULAR JUSTIFICATION involving {comp}: an "
                    f"assumption chain cycles back through a fairness "
                    f"claim — decompose into independently justified "
                    f"non-circular contracts")
    return (not findings, findings)


# ---------------------------------------------------------------------------
# 5. Two-sided boundary evidence. Dispatch != service; service != progress.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class BoundaryWitnesses:
    """Evidence from both sides of every boundary.

    environment: resource availability/unavailability with scope+timing.
    scheduler:   obligation eligible, considered, dispatched, resourced.
    worker:      dispatch accepted, usable attempt, effect/failure recorded.
    """
    environment: dict
    scheduler: dict
    worker: dict


BOUNDARY_VERDICTS = (
    "ENVIRONMENT",
    "SCHEDULER",
    "WORKER",
    "BOUNDARY_UNDETERMINED",  # traces conflict or lack timing — investigate
)


def correlate_witnesses(w: BoundaryWitnesses) -> tuple:
    """Correlate the three witnesses with provenance checks.

    Returns (verdict, reasons). Dispatch is not service; service is not
    progress. Conflicting or under-timed traces yield
    BOUNDARY_UNDETERMINED — never automatic blame against whichever
    component reported last.
    """
    reasons = []
    env = w.environment
    sch = w.scheduler
    wrk = w.worker

    # Provenance: every witness must say who produced it and when.
    for name, wit in (("environment", env), ("scheduler", sch),
                      ("worker", wrk)):
        if not wit.get("producer"):
            return ("BOUNDARY_UNDETERMINED",
                    [f"{name} witness has no producer: provenance missing"])
        if wit.get("timestamp") is None:
            return ("BOUNDARY_UNDETERMINED",
                    [f"{name} witness has no timestamp: timing "
                     f"indeterminate"])

    # Conflict: two witnesses disagree about the same handoff.
    if env.get("resource_available") is True and sch.get(
            "resource_requested") is True and not sch.get("resource_assigned"):
        return ("SCHEDULER",
                ["resource available and requested but never assigned: "
                 "scheduler allocation failure"])
    if env.get("resource_available") is False:
        if sch.get("resource_requested"):
            return ("ENVIRONMENT",
                    ["scheduler made a valid request; external resource "
                     "unavailable: environment failure"])
        return ("BOUNDARY_UNDETERMINED",
                ["resource unavailable but no scheduler request recorded: "
                 "cannot distinguish environment outage from scheduler "
                 "never asking"])
    if sch.get("dispatched") and not sch.get("usable_resources_provided"):
        return ("SCHEDULER",
                ["dispatch without usable resources: service guarantee "
                 "failure — dispatch is not service"])
    if sch.get("usable_service_delivered") and wrk.get("attempted"):
        if not wrk.get("ranking_reduced") and not wrk.get(
                "valid_disposition"):
            return ("WORKER",
                    ["usable service delivered and attempted, but no "
                     "ranking reduction and no valid disposition: worker "
                     "progress-on-service failure — service is not proof"])
        return ("BOUNDARY_UNDETERMINED",
                ["service delivered and progress recorded: no failure "
                 "at this boundary"])
    if wrk.get("reported_success") and not wrk.get("outcome_present"):
        return ("WORKER",
                ["worker reported success but outcome absent: outcome "
                 "verification failure"])
    return ("BOUNDARY_UNDETERMINED",
            ["traces do not establish a failure at any boundary"])


# ---------------------------------------------------------------------------
# 6. Enforcement contract (machine-readable; proposed, not deployed schema).
# ---------------------------------------------------------------------------
ENFORCEMENT_CONSTRAINTS = (
    "dispatch_is_not_service",
    "service_is_not_proof_progress",
    "scheduler_controlled_blocking_is_not_environment_failure",
    "responsibility_transfer_requires_verified_contract",
    "human_authority_cannot_be_assumed",
)


@dataclass(frozen=True)
class ResponsibilityBoundaryContract:
    """Machine-readable enforcement contract.

    Proposed representation, NOT a deployed NayaPOWER schema.
    qualification starts UNPROVEN and moves only on verified evidence.
    """
    contract_id: str
    revision: str
    condition: str
    interfaces: tuple          # tuple[InterfaceEdge]
    constraints: tuple = ENFORCEMENT_CONSTRAINTS
    qualification: str = "UNPROVEN"  # UNPROVEN | QUALIFIED | REJECTED

    def __post_init__(self):
        assert self.contract_id and self.revision and self.condition
        assert all(isinstance(e, InterfaceEdge) for e in self.interfaces)
        assert self.qualification in ("UNPROVEN", "QUALIFIED", "REJECTED")


def check_constraint(contract: ResponsibilityBoundaryContract,
                     constraint: str, evidence: dict) -> tuple:
    """Enforce one named constraint against boundary evidence.

    Returns (ok, finding).
    """
    if constraint == "dispatch_is_not_service":
        if evidence.get("dispatched") and not evidence.get(
                "usable_service_delivered"):
            return (False, "dispatch without usable service violates "
                           "dispatch_is_not_service")
    elif constraint == "service_is_not_proof_progress":
        if evidence.get("usable_service_delivered") and evidence.get(
                "claimed_progress") and not evidence.get(
                "verifier_confirmed_progress"):
            return (False, "service claimed as progress without verifier "
                           "confirmation violates service_is_not_proof_progress")
    elif constraint == "scheduler_controlled_blocking_is_not_environment_failure":
        if evidence.get("blocked_by") == "SCHEDULER" and evidence.get(
                "labeled_as") == "ENVIRONMENT":
            return (False, "scheduler-controlled blocking labeled as "
                           "environment failure: responsibility-boundary "
                           "violation")
    elif constraint == "responsibility_transfer_requires_verified_contract":
        if evidence.get("controller_changed") and not evidence.get(
                "migration_receipt"):
            return (False, "controller changed without a versioned "
                           "boundary migration receipt")
    elif constraint == "human_authority_cannot_be_assumed":
        if evidence.get("assumes_human_authority"):
            return (False, "human authority assumed without authorization")
    else:
        return (False, f"unknown constraint {constraint}")
    return (True, f"constraint {constraint} holds on this evidence")


# ---------------------------------------------------------------------------
# 7. Adversarial fault injection: hold two components correct, break one.
# ---------------------------------------------------------------------------
# Each scenario: (injected_defect, correct_diagnostic).
FAULT_INJECTION_TABLE = (
    ("external resource never becomes available",
     "ENVIRONMENT"),
    ("resource available, scheduler never allocates it",
     "SCHEDULER"),
    ("scheduler marks its own blocked queue as externally ineligible",
     "SCHEDULER"),   # responsibility-boundary violation
    ("scheduler dispatches but provides no usable resources",
     "SCHEDULER"),   # service guarantee failure
    ("worker receives usable service but loops without progress",
     "WORKER"),      # progress-on-service failure
    ("worker reports success but outcome is absent",
     "WORKER"),      # outcome verification failure
    ("worker changes and fairness counters reset",
     "SCHEDULER"),   # scheduler bookkeeping defect
    ("scheduler works, but LAW authorization is absent",
     "LAW"),         # legitimate authority block, not starvation
    ("producer guarantee does not meet consumer assumption",
     "INTERFACE"),   # interface contract mismatch
    ("logs conflict and no independent evidence resolves them",
     "BOUNDARY_UNDETERMINED"),
)

FAULT_MODELS = ("ENVIRONMENT_BROKEN", "SCHEDULER_BROKEN", "WORKER_BROKEN")


def run_fault_scenario(defect: str, witnesses: BoundaryWitnesses,
                       claimed_owner: str | None = None) -> tuple:
    """Run one fault-injection scenario through the verifier.

    The verifier must identify the actual control relationship, not
    accept a substituted label. Returns (verdict, reasons, label_ok)
    where label_ok is False when the claimed owner was wrong.
    """
    verdict, reasons = correlate_witnesses(witnesses)
    label_ok = (claimed_owner is None) or (claimed_owner == verdict)
    return (verdict, reasons, label_ok)


def check_component_supplied_assumption(assumption_owner: str,
                                        verified_component: str,
                                        independently_justified: bool,
                                        conditional: bool) -> tuple:
    """A PASS under an assumption supplied by the verified component is
    insufficient without independent justification or explicit
    conditional classification. Returns (ok, finding).
    """
    if assumption_owner == verified_component and not independently_justified:
        if conditional:
            return (True, "assumption explicitly classified as conditional "
                          "proof premise")
        return (False, "assumption supplied by the component under "
                       "verification without independent justification: "
                       "insufficient for qualification")
    return (True, "assumption sourcing acceptable")


# ---------------------------------------------------------------------------
# 8. Boundary migration receipts: ownership changes only at a revision.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class BoundaryMigrationReceipt:
    """Versioned record of a responsibility transfer.

    Ownership changes only at the effective boundary revision.
    Old traces remain interpretable under their contemporary contracts;
    a modified label never retroactively absolves historical behavior.
    """
    receipt_id: str
    previous_controller: str
    new_controller: str
    guarantee_transferred: str
    new_producer_assumption: str
    new_consumer_assumption: str
    interface_evidence: tuple
    old_receipts_applicable: tuple   # which old receipts still apply
    new_tests_required: tuple        # fairness/progress tests now needed
    effective_revision: str

    def __post_init__(self):
        assert self.receipt_id and self.effective_revision
        assert self.previous_controller in COMPONENTS
        assert self.new_controller in COMPONENTS
        assert self.previous_controller != self.new_controller


def check_no_retroactive_absolution(receipt: BoundaryMigrationReceipt,
                                    historical_verdict: str,
                                    historical_controller: str) -> tuple:
    """A migration cannot absolve the historical controller's behavior.

    Returns (ok, finding).
    """
    if historical_controller == receipt.previous_controller:
        return (True, f"historical verdict '{historical_verdict}' stands "
                      f"under {historical_controller}: migration at "
                      f"{receipt.effective_revision} is not retroactive")
    return (True, "no historical behavior of the previous controller at "
                  "issue")


# ---------------------------------------------------------------------------
# 9. Three indicators + interface consistency verdict. Never averaged.
# ---------------------------------------------------------------------------
INDICATORS = (
    "ENVIRONMENTAL_ASSUMPTION_COVERAGE",
    "SCHEDULER_FAIRNESS_COMPLIANCE",
    "WORKER_PROGRESS_COMPLIANCE",
)


@dataclass(frozen=True)
class AccountabilityScorecard:
    """Three separate indicators plus an interface consistency verdict.

    A failure in one dimension is never averaged away by strong
    performance in another: 10/10 progress cannot compensate for a
    violated LAW boundary or an unjustified fairness assumption.
    """
    environmental_coverage: str    # JUSTIFIED | CONDITIONAL | UNJUSTIFIED
    scheduler_compliance: str       # COMPLIANT | VIOLATED | UNDETERMINED
    worker_compliance: str          # COMPLIANT | VIOLATED | UNDETERMINED
    interface_consistent: bool
    law_boundary_intact: bool

    def overall(self) -> tuple:
        """The composed verdict. Never an average."""
        if not self.law_boundary_intact:
            return ("REJECTED",
                    "LAW boundary violated: no other score compensates")
        if self.environmental_coverage == "UNJUSTIFIED":
            return ("REJECTED",
                    "environmental assumptions unjustified: qualification "
                    "unproven regardless of other scores")
        if not self.interface_consistent:
            return ("REJECTED",
                    "interface mismatch: producer guarantees do not meet "
                    "consumer assumptions")
        parts = [self.scheduler_compliance, self.worker_compliance]
        if "VIOLATED" in parts:
            return ("REJECTED",
                    "a component guarantee is violated: strong performance "
                    "elsewhere does not compensate")
        if "UNDETERMINED" in parts:
            return ("UNDETERMINED", "a component verdict is undetermined")
        return ("QUALIFIED_IN_SCOPE",
                "all three indicators hold and interfaces compose")


# ---------------------------------------------------------------------------
# 10. Decisive experiment: KNOW -> LAW -> ACT -> VERIFY, three failures.
# ---------------------------------------------------------------------------
def decisive_experiment_case(case: str, false_blame: str | None = None
                             ) -> tuple:
    """Run one case of the decisive experiment.

    case: "A" (environment failure), "B" (scheduler failure),
          "C" (worker failure).
    false_blame: component the failing part falsely accuses (the
          verifier must see through it).
    Returns (verdict, reasons) — the verifier's classification.
    """
    base = {"producer": "sim", "timestamp": 1}
    if case == "A":
        w = BoundaryWitnesses(
            environment={**base, "resource_available": False},
            scheduler={**base, "resource_requested": True,
                       "resource_assigned": False},
            worker={**base, "attempted": False},
        )
        expected = "ENVIRONMENT"
    elif case == "B":
        w = BoundaryWitnesses(
            environment={**base, "resource_available": True},
            scheduler={**base, "resource_requested": True,
                       "resource_assigned": False},
            worker={**base, "attempted": False},
        )
        expected = "SCHEDULER"
    elif case == "C":
        w = BoundaryWitnesses(
            environment={**base, "resource_available": True},
            scheduler={**base, "resource_requested": True,
                       "resource_assigned": True,
                       "dispatched": True,
                       "usable_resources_provided": True,
                       "usable_service_delivered": True},
            worker={**base, "attempted": True,
                    "ranking_reduced": False,
                    "valid_disposition": False},
        )
        expected = "WORKER"
    else:
        raise AssertionError(f"unknown case {case}")
    verdict, reasons = correlate_witnesses(w)
    note = (f" — false blame of {false_blame} rejected: control, not "
            f"narrative" if false_blame else "")
    ok = (verdict == expected)
    return (verdict,
            [f"expected {expected}, got {verdict}"] + reasons +
            ([f"false blame '{false_blame}' did not move the verdict{note}"]
             if false_blame else []),
            ok)
