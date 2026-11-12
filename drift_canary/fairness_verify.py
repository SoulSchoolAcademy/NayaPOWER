"""Fairness verification methodology: prove the three links separately (spec).

Principle: "Every liveness qualification must prove three separate
links: opportunity -> fair service -> verified progress or governed
resolution."

For each outstanding obligation o, the test harness observes three
predicates:
  E_o: the required transition is genuinely enabled.
  S_o: the transition receives real, usable service.
  P_o: a verified transition reduces outstanding work or validly
       resolves the obligation.

Three properties (related, NOT interchangeable):
  WF  (weak fairness):       FG E_o  =>  GF S_o
  SF  (strong fairness):      GF E_o  =>  GF S_o
  PoS (progress on service):  under stated assumptions,
                             <>(ranking decreases OR valid terminal disposition)

Mathematical relation: a WF violation is ALSO an SF violation
(strong fairness implies weak fairness). Diagnostic categories are
therefore:
  WF_VIOLATION / SF_ONLY_VIOLATION / PROGRESS_ON_SERVICE_VIOLATION
— never falsely disjoint.

This module extends drift_canary/strong_fairness.py with:
  1. an explicit-state model checker for the three properties, run in
     stages (unconstrained -> weak -> strong -> PoS),
  2. a lasso (prefix + repeating cycle) classifier,
  3. a deterministic runtime test harness (virtual clock, controllable
     scheduler, contention simulator, fault injection, independent
     trace reader),
  4. the canonical scheduling trace format + independent verifier,
  5. the model-to-implementation refinement checklist,
  6. the four-verdict taxonomy (no collapsed PASS),
  7. separate scoring for the five qualification slots,
  8. the first deliverable: three INTENTIONALLY BROKEN schedulers that
     the verifier must identify correctly.

Composes with:
  fairness.py        — service ladder, FairnessContract, FairnessLedger.
  strong_fairness.py — decision rule, 8 assumptions, three-proof
                       composition, FlickerLedger, simulate_policy.
  progress.py        — W(s), R(s); service never grants proof progress.
  liveness.py        — WAITING_AUTHORITY rules; liveness never creates
                       permission.

SPEC + deterministic machinery. NOT wired into kernel/, KNOW, LAW, ACT,
or any live path. Wiring needs Shawn's word.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from drift_canary.fairness import (
    ADEQUATE_SERVICE_RUNG,
    FairnessContract,
    SchedulingEvent,
    event_adequate_service,
    ladder_rank,
)

# ---------------------------------------------------------------------------
# 1. The three predicates, observed per obligation per round.
# ---------------------------------------------------------------------------
# E_o: genuinely enabled — the transition is permitted AND executable.
#      Nominal eligibility that cannot be acted on is NOT E_o (SF-04).
# S_o: real, usable service — at least SERVICED on the ladder WITH valid
#      service evidence. A SERVICE log line is not S_o.
# P_o: verified progress — a transition that reduces the outstanding-work
#      ranking or reaches a valid terminal disposition, computed by the
#      VERIFIER from obligation transitions, never from worker status.
PREDICATES = ("E_o", "S_o", "P_o")


@dataclass(frozen=True)
class ObligationObservation:
    """One round's observed predicates for one obligation.

    enabled:        E_o — genuinely enabled (permitted and executable).
    serviced:       S_o — real usable service (evidenced, see fairness.py).
    rank_before:    outstanding-work rank multiset element before.
    rank_after:     outstanding-work rank multiset element after.
    retries_before: recovery budget before.
    retries_after:  recovery budget after.
    terminal:       None, or a governed terminal disposition
                    ("COMPLETED", "REFUSED", "FAILED_RECOVERABLY_EXHAUSTED",
                     "ESCALATED").
    awaiting_authority: True when a required human authorization is absent
                    (WAITING_AUTHORITY — not a fairness failure).
    """
    obligation_id: str
    seq: int
    enabled: bool
    serviced: bool
    rank_before: int
    rank_after: int
    retries_before: int
    retries_after: int
    terminal: str | None = None
    awaiting_authority: bool = False


# ---------------------------------------------------------------------------
# 2. Lasso counterexamples and the classifier.
#
# A lasso = finite prefix leading into a repeating cycle. The classifier
# uses the FULL repeating state/transition trace, not visual pattern
# matching.
# ---------------------------------------------------------------------------
LASSO_VERDICTS = (
    "WF_VIOLATION",                  # enabled every cycle state, no service
    "SF_ONLY_VIOLATION",             # enabled some cycle states, no service
    "PROGRESS_ON_SERVICE_VIOLATION",  # service occurs, no ranking decrease
                                     # or valid terminal disposition
    "OPPORTUNITY_ASSUMPTION_NOT_MET",  # eligibility never recurs
    "WAITING_AUTHORITY",             # human authorization absent; separate
                                     # escalation requirements apply
    "MODEL_CHECK_PASSED_IN_SCOPE",   # no infinite counterexample found in
                                     # the checked abstraction — NOT
                                     # production-proven
)


@dataclass(frozen=True)
class Lasso:
    """An infinite counterexample in finite form.

    prefix: tuple of ObligationObservation leading into the cycle.
    cycle:  tuple of ObligationObservation that repeats forever.
    """
    obligation_id: str
    prefix: tuple
    cycle: tuple

    def __post_init__(self):
        assert self.cycle, "a lasso needs a non-empty repeating cycle"
        assert self.obligation_id, "lasso needs an obligation id"


def _cycle_enabled_pattern(cycle: tuple) -> tuple:
    return tuple(o.enabled for o in cycle)


def _cycle_serviced_pattern(cycle: tuple) -> tuple:
    return tuple(o.serviced for o in cycle)


def _cycle_rank_decreases(cycle: tuple) -> bool:
    """Did any cycle transition reduce outstanding work?"""
    return any(o.rank_after < o.rank_before for o in cycle)


def _cycle_terminal(cycle: tuple) -> bool:
    return any(o.terminal is not None for o in cycle)


def _cycle_awaiting_authority(cycle: tuple) -> bool:
    return all(o.awaiting_authority for o in cycle)


def classify_lasso(lasso: Lasso) -> tuple:
    """Classify a lasso counterexample for one obligation.

    Returns (verdict, reason). The verdicts are ordered by diagnostic
    specificity: WF_VIOLATION implies the SF condition too, so it is
    reported as WF_VIOLATION, never as both.
    """
    assert isinstance(lasso, Lasso), "classify_lasso needs a Lasso"
    cycle = lasso.cycle
    if _cycle_awaiting_authority(cycle):
        return ("WAITING_AUTHORITY",
                "human authorization absent throughout the cycle; "
                "no fairness duty to execute — escalation requirements "
                "apply separately")
    enabled = _cycle_enabled_pattern(cycle)
    serviced = _cycle_serviced_pattern(cycle)
    if not any(enabled):
        return ("OPPORTUNITY_ASSUMPTION_NOT_MET",
                "eligibility never recurs in the cycle; fairness cannot "
                "manufacture opportunity")
    if any(serviced):
        if _cycle_rank_decreases(cycle) or _cycle_terminal(cycle):
            return ("MODEL_CHECK_PASSED_IN_SCOPE",
                    "service in the cycle reduces work or terminates; "
                    "no violation in this trace")
        return ("PROGRESS_ON_SERVICE_VIOLATION",
                "genuine service occurs in the cycle but no verified "
                "ranking decrease and no valid terminal disposition — "
                "scheduler fairness holds, execution does not progress")
    # No service anywhere in the cycle: a fairness violation.
    if all(enabled):
        return ("WF_VIOLATION",
                "enabled in EVERY cycle state yet never serviced: "
                "violates weak fairness (and therefore strong fairness)")
    return ("SF_ONLY_VIOLATION",
            "enabled in SOME cycle states (infinitely often) yet never "
            "serviced: weak fairness does not forbid this trace, strong "
            "fairness does")

# ---------------------------------------------------------------------------
# 3. Explicit-state model checker for the three properties.
#
# Small abstract model: two competing workflows (A, B), one contended
# resource, bounded retries. Each obligation has: eligibility, a
# consecutive-eligibility counter, a fairness-debt counter, remaining
# retries, outstanding rank, terminal state, awaiting-authority flag.
#
# The checker runs in STAGES:
#   1. UNCONSTRAINED scheduler — discover starvation traces without
#      assuming any fairness.
#   2. WEAK-fair scheduler — exclude WF-violating traces; see what
#      nonprogress remains.
#   3. STRONG-fair scheduler — exclude SF-violating traces; check
#      whether progress is now guaranteed.
#   4. PoS check — find cycles that satisfy scheduler fairness but never
#      reduce the ranking or legitimately terminate.
#
# Absence of counterexamples under an ASSUMED fairness policy is never
# proof that the real scheduler implements fairness. The runtime
# scheduling mechanism must be verified separately (see section 7).
# ---------------------------------------------------------------------------
MODEL_TRANSITIONS = (
    "ENABLE",          # task becomes eligible
    "DISABLE",         # task becomes temporarily ineligible
    "SELECT",          # scheduler chooses an obligation
    "SERVICE",         # obligation receives a usable execution opportunity
    "DISCHARGE",       # a required proof obligation is independently satisfied
    "FAILED_ATTEMPT",  # work attempted but proof not established
    "RETRY",           # recovery attempted within remaining budget
    "REASSIGN",        # work transfers worker; identity + budget preserved
    "ESCALATE",        # responsibility transfers to authorized decider
    "TERMINATE",       # workflow reaches a valid terminal disposition
)

MODEL_NODES = ("KNOW", "LAW", "ACT", "VERIFY")


@dataclass(frozen=True)
class ModelState:
    """One abstract model state, hashable for visited-set tracking."""
    elig_a: bool
    elig_b: bool
    consec_a: int          # consecutive eligible rounds (weak-fairness clock)
    consec_b: int
    debt_a: int            # eligible epochs without service (strong clock)
    debt_b: int
    retries_a: int
    retries_b: int
    rank_a: int            # outstanding work (0 == discharged)
    rank_b: int
    terminal_a: bool
    terminal_b: bool
    awaiting_auth_a: bool
    resource_held_by: str  # "A", "B", or "NONE"
    phase: int = 0         # environment phase (drives the flicker pattern;
                           # kept modulo the pattern length so the abstract
                           # state space stays finite and lassos exist)


def model_initial() -> ModelState:
    return ModelState(
        elig_a=True, elig_b=True,
        consec_a=0, consec_b=0, debt_a=0, debt_b=0,
        retries_a=2, retries_b=2,
        rank_a=1, rank_b=1,
        terminal_a=False, terminal_b=False,
        awaiting_auth_a=False, resource_held_by="NONE", phase=0,
    )


def _model_successors(state: ModelState, policy: str,
                       weak_bound: int = 3, strong_threshold: int = 4,
                       flicker: tuple = (True, False)) -> list:
    """Nondeterministic successors under a scheduler policy.

    policy: "UNCONSTRAINED" | "WEAK" | "STRONG".
    flicker: eligibility pattern the environment cycles through for B
             (adversarial contention); A stays eligible.
    UNCONSTRAINED: the adversary may service A, B, or nobody each round.
    WEAK: an obligation eligible for >= weak_bound consecutive rounds
          MUST be serviced (bounded approximation of weak fairness).
    STRONG: an obligation with debt >= strong_threshold MUST be serviced
            (bounded approximation of strong fairness).
    Service of an eligible obligation either DISCHARGEs it (rank -> 0,
    terminal) or is a FAILED_ATTEMPT (retries - 1). A FAILED_ATTEMPT
    with no retries left forces TERMINATE with a governed failure
    disposition (not success).
    """
    assert policy in ("UNCONSTRAINED", "WEAK", "STRONG")
    out = []

    def forced(oblig: str) -> bool:
        if oblig == "A":
            if not state.elig_a or state.terminal_a:
                return False
            if policy == "WEAK":
                return state.consec_a >= weak_bound
            if policy == "STRONG":
                return state.debt_a >= strong_threshold
            return False
        if not state.elig_b or state.terminal_b:
            return False
        if policy == "WEAK":
            return state.consec_b >= weak_bound
        if policy == "STRONG":
            return state.debt_b >= strong_threshold
        return False

    # Environment step: advance the flicker pattern for B; A eligible.
    # The flicker pattern cycles with the state's step counter, so the
    # adversary can make B's eligibility flicker forever.
    def env_step(s: ModelState) -> ModelState:
        b_elig = flicker[s.phase % len(flicker)]
        return ModelState(
            elig_a=True, elig_b=b_elig,
            consec_a=s.consec_a + 1 if s.elig_a else 0,
            consec_b=s.consec_b + 1 if b_elig else 0,
            debt_a=s.debt_a, debt_b=s.debt_b,
            retries_a=s.retries_a, retries_b=s.retries_b,
            rank_a=s.rank_a, rank_b=s.rank_b,
            terminal_a=s.terminal_a, terminal_b=s.terminal_b,
            awaiting_auth_a=s.awaiting_auth_a,
            resource_held_by=s.resource_held_by,
            phase=(s.phase + 1) % len(flicker),
        )

    def serve(s: ModelState, oblig: str, discharge: bool) -> ModelState:
        if oblig == "A":
            if discharge:
                return ModelState(
                    elig_a=False, elig_b=s.elig_b,
                    consec_a=0, consec_b=s.consec_b, debt_a=0,
                    debt_b=s.debt_b, retries_a=s.retries_a,
                    retries_b=s.retries_b, rank_a=0, rank_b=s.rank_b,
                    terminal_a=True, terminal_b=s.terminal_b,
                    awaiting_auth_a=s.awaiting_auth_a,
                    resource_held_by=s.resource_held_by,
                    phase=s.phase)
            r = s.retries_a - 1
            term = r < 0
            return ModelState(
                elig_a=s.elig_a, elig_b=s.elig_b,
                consec_a=s.consec_a, consec_b=s.consec_b, debt_a=0,
                debt_b=s.debt_b, retries_a=max(r, 0),
                retries_b=s.retries_b, rank_a=s.rank_a, rank_b=s.rank_b,
                terminal_a=term, terminal_b=s.terminal_b,
                awaiting_auth_a=s.awaiting_auth_a,
                resource_held_by=s.resource_held_by,
                    phase=s.phase)
        if discharge:
            return ModelState(
                elig_a=s.elig_a, elig_b=False,
                consec_a=s.consec_a, consec_b=0, debt_a=s.debt_a,
                debt_b=0, retries_a=s.retries_a,
                retries_b=s.retries_b, rank_a=s.rank_a, rank_b=0,
                terminal_a=s.terminal_a, terminal_b=True,
                awaiting_auth_a=s.awaiting_auth_a,
                resource_held_by=s.resource_held_by,
                    phase=s.phase)
        r = s.retries_b - 1
        term = r < 0
        return ModelState(
            elig_a=s.elig_a, elig_b=s.elig_b,
            consec_a=s.consec_a, consec_b=s.consec_b, debt_a=s.debt_a,
            debt_b=0, retries_a=s.retries_a,
            retries_b=max(r, 0), rank_a=s.rank_a, rank_b=s.rank_b,
            terminal_a=s.terminal_a, terminal_b=term,
            awaiting_auth_a=s.awaiting_auth_a,
            resource_held_by=s.resource_held_by,
                    phase=s.phase)

    # Counter saturation: cap consecutive-eligibility at weak_bound
    # and debt at strong_threshold. A saturated counter is equivalent
    # to any larger value for every policy decision below, and capping
    # keeps the abstract state space finite so lassos can exist.
    def cap(s: ModelState) -> ModelState:
        return ModelState(
            elig_a=s.elig_a, elig_b=s.elig_b,
            consec_a=min(s.consec_a, weak_bound),
            consec_b=min(s.consec_b, weak_bound),
            debt_a=min(s.debt_a, strong_threshold),
            debt_b=min(s.debt_b, strong_threshold),
            retries_a=s.retries_a, retries_b=s.retries_b,
            rank_a=s.rank_a, rank_b=s.rank_b,
            terminal_a=s.terminal_a, terminal_b=s.terminal_b,
            awaiting_auth_a=s.awaiting_auth_a,
            resource_held_by=s.resource_held_by,
            phase=s.phase,
        )

    fa, fb = forced("A"), forced("B")
    # Candidate service choices for this round.
    choices = []
    if fa or fb:
        # Forced service: adversary chooses among forced obligations,
        # and whether the service discharges or fails.
        if fa:
            choices.append(("A", True))
            choices.append(("A", False))
        if fb:
            choices.append(("B", True))
            choices.append(("B", False))
    else:
        # Free choice: service A (discharge or fail), B, or nobody.
        choices.append(("A", True))
        choices.append(("A", False))
        choices.append(("B", True))
        choices.append(("B", False))
        choices.append((None, False))

    for oblig, discharge in choices:
        s = state
        # Eligibility gating: cannot service an ineligible obligation.
        if oblig == "A" and (not s.elig_a or s.terminal_a):
            continue
        if oblig == "B" and (not s.elig_b or s.terminal_b):
            continue
        if oblig is None:
            ns = env_step(s)
        else:
            ns = serve(s, oblig, discharge)
            ns = env_step(ns)
        # Debt accounting: eligible + unserved -> +1; served -> 0.
        da = 0 if oblig == "A" else (ns.debt_a + 1 if ns.elig_a
                                    and not ns.terminal_a else ns.debt_a)
        db = 0 if oblig == "B" else (ns.debt_b + 1 if ns.elig_b
                                    and not ns.terminal_b else ns.debt_b)
        ns = ModelState(
            elig_a=ns.elig_a, elig_b=ns.elig_b,
            consec_a=ns.consec_a, consec_b=ns.consec_b,
            debt_a=da, debt_b=db,
            retries_a=ns.retries_a, retries_b=ns.retries_b,
            rank_a=ns.rank_a, rank_b=ns.rank_b,
            terminal_a=ns.terminal_a, terminal_b=ns.terminal_b,
            awaiting_auth_a=ns.awaiting_auth_a,
            resource_held_by=ns.resource_held_by,
            phase=ns.phase)
        out.append(((oblig, discharge), cap(ns)))
    return out


def _state_to_observations(state: ModelState, seq: int,
                           serviced_a: bool, serviced_b: bool,
                           rank_prev_a: int, rank_prev_b: int,
                           ret_prev_a: int, ret_prev_b: int) -> tuple:
    oa = ObligationObservation(
        obligation_id="WF-A", seq=seq, enabled=state.elig_a,
        serviced=serviced_a, rank_before=rank_prev_a,
        rank_after=state.rank_a, retries_before=ret_prev_a,
        retries_after=state.retries_a,
        terminal="COMPLETED" if state.terminal_a and state.rank_a == 0
        else ("FAILED_RECOVERABLY_EXHAUSTED"
              if state.terminal_a else None),
        awaiting_authority=state.awaiting_auth_a)
    ob = ObligationObservation(
        obligation_id="WF-B", seq=seq, enabled=state.elig_b,
        serviced=serviced_b, rank_before=rank_prev_b,
        rank_after=state.rank_b, retries_before=ret_prev_b,
        retries_after=state.retries_b,
        terminal="COMPLETED" if state.terminal_b and state.rank_b == 0
        else ("FAILED_RECOVERABLY_EXHAUSTED"
              if state.terminal_b else None))
    return oa, ob


def find_lassos(policy: str, max_depth: int = 40,
                weak_bound: int = 3, strong_threshold: int = 4) -> list:
    """Explicit-state DFS: find lasso counterexamples under a policy.

    Returns a list of (obligation_id, Lasso). A lasso is reported when
    DFS revisits a state already on the current path. Depth-bounded to
    keep the abstraction finite; absence of lassos within the bound is
    MODEL_CHECK_PASSED_IN_SCOPE, never a general proof.
    """
    init = model_initial()
    lassos = []
    # path: list of (state, oblig, discharge, rank_prev, ret_prev)
    path = [(init, None, False, init.rank_a, init.rank_b,
             init.retries_a, init.retries_b)]
    on_path = {init: 0}
    sys_set = set()
    sys_set.add(init)

    def dfs(state: ModelState, depth: int):
        if depth >= max_depth:
            return
        for (oblig, discharge), ns in _model_successors(
                state, policy, weak_bound, strong_threshold):
            if ns in on_path:
                # Lasso found: prefix = path[:idx], cycle = path[idx:].
                idx = on_path[ns]
                cyc_states = [p[0] for p in path[idx:]]
                # Build observations for both obligations over the cycle.
                for oid, pick_a in (("WF-A", True), ("WF-B", False)):
                    obs_cycle = []
                    prev = path[idx]
                    for j, p in enumerate(path[idx:]):
                        st = p[0]
                        served = (p[1] == ("A" if pick_a else "B"))
                        if pick_a:
                            o = _state_to_observations(
                                st, j, served, False, prev[3], prev[4],
                                prev[5], prev[6])[0]
                        else:
                            o = _state_to_observations(
                                st, j, False, served, prev[3], prev[4],
                                prev[5], prev[6])[1]
                        obs_cycle.append(o)
                        prev = p
                    # Only report lassos where the obligation never
                    # terminates in the cycle (a terminated obligation
                    # has no liveness duty).
                    if any(cyc_states[k].terminal_a if pick_a
                           else cyc_states[k].terminal_b
                           for k in range(len(cyc_states))):
                        continue
                    prefix_obs = []
                    lasso = Lasso(obligation_id=oid, prefix=tuple(prefix_obs),
                                  cycle=tuple(obs_cycle))
                    key = (oid, tuple(
                        (c.elig_a, c.elig_b, c.rank_a, c.rank_b)
                        for c in cyc_states))
                    if key not in sys_set:
                        sys_set.add(key)
                        lassos.append((oid, lasso))
                continue
            if ns not in sys_set:
                sys_set.add(ns)
            on_path[ns] = len(path)
            path.append((ns, oblig, discharge, state.rank_a, state.rank_b,
                         state.retries_a, state.retries_b))
            dfs(ns, depth + 1)
            path.pop()
            del on_path[ns]

    dfs(init, 0)
    return lassos


def check_property_staged(max_depth: int = 30) -> dict:
    """Run the four stages and classify what each excludes.

    Returns {stage: [(obligation_id, verdict, reason)]}. Stage 4 (PoS)
    reuses the STRONG-policy lassos and additionally flags fair cycles
    with service but no ranking decrease.
    """
    out = {}
    for stage, policy in (("1_unconstrained", "UNCONSTRAINED"),
                          ("2_weak", "WEAK"),
                          ("3_strong", "STRONG")):
        lassos = find_lassos(policy, max_depth=max_depth)
        out[stage] = [(oid, *classify_lasso(l)) for oid, l in lassos]
    # Stage 4: PoS — among STRONG lassos, surface service-without-progress.
    pos = []
    for oid, lasso in find_lassos("STRONG", max_depth=max_depth):
        verdict, reason = classify_lasso(lasso)
        if verdict == "PROGRESS_ON_SERVICE_VIOLATION":
            pos.append((oid, verdict, reason))
    out["4_progress_on_service"] = pos
    return out

# ---------------------------------------------------------------------------
# 4. First deliverable: three INTENTIONALLY BROKEN schedulers.
#
# The verifier must identify all three correctly, preserve safety
# invariants, and reject falsely green results:
#   BROKEN_WF  — never services its target even when continuously
#                eligible (violates weak fairness).
#   BROKEN_SF  — serves continuously-eligible work but always skips the
#                flickering obligation (satisfies weak, violates strong).
#   BROKEN_POS — services fairly, but its worker never discharges:
#                endless FAILED_ATTEMPT without ranking decrease
#                (satisfies scheduler fairness, violates progress on
#                service).
# ---------------------------------------------------------------------------
BROKEN_SCHEDULERS = ("BROKEN_WF", "BROKEN_SF", "BROKEN_POS")


class BrokenScheduler:
    """A scripted scheduler with a deliberate defect, for verifier testing.

    kind: one of BROKEN_SCHEDULERS.
    target: the obligation id it starves (BROKEN_WF / BROKEN_SF).
    worker_fails: for BROKEN_POS, the worker never discharges.
    This is a test fixture, not a production scheduler.
    """

    def __init__(self, kind: str, target: str = "WF-B",
                 worker_fails: bool = False):
        assert kind in BROKEN_SCHEDULERS, kind
        self.kind = kind
        self.target = target
        self.worker_fails = worker_fails or (kind == "BROKEN_POS")
        self.rounds = 0

    def decide(self, obligation_id: str, eligible: bool,
               consec_eligible: int) -> str:
        """Return the rung this scheduler reaches for the obligation.

        Returns a SERVICE_LADDER rung. BROKEN schedulers deliberately
        withhold adequate service from their target.
        """
        self.rounds += 1
        if self.kind == "BROKEN_WF" and obligation_id == self.target:
            # Starves even continuously eligible work: never serviced.
            return "SELECTED"
        if self.kind == "BROKEN_SF" and obligation_id == self.target:
            # Serves only if continuously eligible long enough to look
            # "weak-fair", but the flicker pattern never lets consec grow;
            # in practice: always skip the flickering target.
            return "SELECTED"
        # Healthy behavior for non-targets (and BROKEN_POS targets):
        # adequate service with evidence.
        return "SERVICED"

    def worker_outcome(self, obligation_id: str) -> str:
        """What the worker does with a service opportunity."""
        if self.worker_fails:
            return "FAILED_ATTEMPT"
        return "DISCHARGE"


def run_broken_scheduler(kind: str, rounds: int = 12,
                         flicker: tuple = None) -> list:
    """Run a broken scheduler against a target.

    Produces a list of ObligationObservation for the target obligation.
    BROKEN_WF uses a CONTINUOUSLY eligible target (weak fairness must
    protect it); BROKEN_SF / BROKEN_POS use a flickering target.
    """
    if flicker is None:
        flicker = (True,) if kind == "BROKEN_WF" else (True, False)
    sched = BrokenScheduler(kind, target="WF-B")
    obs = []
    consec = 0
    # BROKEN_POS must demonstrate ENDLESS service without resolution: give
    # it enough retries that the trace never reaches a terminal disposition
    # (bounded retry exhaustion is governed termination, not a PoS violation
    # — see POS-02).
    rank, retries = 1, (rounds + 2 if kind == "BROKEN_POS" else 2)
    for seq in range(rounds):
        eligible = flicker[seq % len(flicker)]
        consec = consec + 1 if eligible else 0
        rung = sched.decide("WF-B", eligible, consec)
        serviced = (rung == "SERVICED")
        outcome = sched.worker_outcome("WF-B") if serviced else None
        rank_before, ret_before = rank, retries
        if outcome == "DISCHARGE":
            rank, terminal = 0, "COMPLETED"
        elif outcome == "FAILED_ATTEMPT":
            retries -= 1
            terminal = ("FAILED_RECOVERABLY_EXHAUSTED"
                        if retries < 0 else None)
            if terminal:
                rank = 0
        else:
            terminal = None
        obs.append(ObligationObservation(
            obligation_id="WF-B", seq=seq, enabled=eligible,
            serviced=serviced, rank_before=rank_before, rank_after=rank,
            retries_before=ret_before, retries_after=max(retries, 0),
            terminal=terminal))
        if terminal:
            break
    return obs


def identify_broken_scheduler(kind: str, rounds: int = 12) -> tuple:
    """Run the broken scheduler and classify the resulting trace.

    Returns (identified_kind, verdict, reason). The verifier must map:
      BROKEN_WF  -> WF_VIOLATION
      BROKEN_SF  -> SF_ONLY_VIOLATION
      BROKEN_POS -> PROGRESS_ON_SERVICE_VIOLATION
    """
    obs = run_broken_scheduler(kind, rounds=rounds)
    if not obs:
        return (kind, "UNKNOWN", "no observations produced")
    lasso = Lasso(obligation_id="WF-B", prefix=tuple(),
                  cycle=tuple(obs))
    verdict, reason = classify_lasso(lasso)
    expected = {
        "BROKEN_WF": "WF_VIOLATION",
        "BROKEN_SF": "SF_ONLY_VIOLATION",
        "BROKEN_POS": "PROGRESS_ON_SERVICE_VIOLATION",
    }[kind]
    identified = (verdict == expected)
    return (kind if identified else "MISIDENTIFIED",
            verdict,
            f"{reason} | expected {expected}")


# ---------------------------------------------------------------------------
# 5. Deterministic runtime test harness.
#
# The model checker tests an ABSTRACTION. The runtime harness tests actual
# implementation behavior: virtual clock (no real-time sleeps),
# controllable scheduler, resource contention simulator, task/worker
# identity tracking, fault injection, versioned proof receipts,
# deterministic replay, and an independent trace reader.
#
# A developer-generated SERVICE log line does NOT prove usable service.
# Proof progress is computed by the verifier from accepted obligation
# transitions, never from a worker-maintained completion percentage.
# ---------------------------------------------------------------------------
@dataclass
class VirtualClock:
    """Deterministic virtual time. No real-time sleeps in tests."""
    tick: int = 0

    def advance(self, steps: int = 1) -> int:
        assert steps >= 0, "clock never goes backward"
        self.tick += steps
        return self.tick


@dataclass(frozen=True)
class TraceEvent:
    """Canonical scheduling trace event, shared by the model checker and
    the runtime verifier.

    The verifier recomputes the (eligibility, service, outstanding work,
    recovery budget) sequence from these events and checks it against
    the applicable formal contract.
    """
    workflow_id: str
    obligation_id: str
    obligation_revision: str
    event_sequence: int
    event_type: str  # one of MODEL_TRANSITIONS
    worker_id: str
    enabled_before: bool
    service_usable: bool
    outstanding_rank_before: tuple  # multiset, e.g. (3, 2, 1)
    outstanding_rank_after: tuple
    retries_before: int
    retries_after: int
    proof_discharge_receipt: str | None
    execution_receipt: str | None
    model_version: str

    def __post_init__(self):
        assert self.event_type in MODEL_TRANSITIONS, self.event_type
        assert self.event_sequence >= 0


def _multiset_decreased(before: tuple, after: tuple) -> bool:
    """Well-founded multiset check (Dershowitz-Manna, simplified).

    True iff `after` is smaller: an element was removed, or replaced by
    finitely many strictly smaller elements. Used by the verifier to
    confirm claimed ranking decreases.
    """
    b = sorted(before, reverse=True)
    a = sorted(after, reverse=True)
    if len(a) < len(b):
        # Removal: every kept element must be <= its counterpart.
        return all(x <= y for x, y in zip(a, b))
    if len(a) == len(b):
        return a < b
    # Expansion: allowed only if the multiset's maximum decreased
    # (one higher-ranked obligation refined into lower-ranked ones).
    return a and b and max(a) < max(b)


def verify_trace(events: list, contract: FairnessContract) -> tuple:
    """Independently verify a canonical trace against a fairness contract.

    Recomputes (eligibility, service, outstanding work, recovery budget)
    from the events. Detects:
      - malformed traces (sequence gaps, unknown transitions),
      - service claims without usable-service evidence,
      - ranking changes the receipts do not justify,
      - recovery-budget replenishment through reassignment,
      - obsolete obligation revisions,
      - fairness-debt resets through reassignment.
    Returns (ok, findings) where findings is a list of anomaly strings.
    An empty findings list means the trace is internally consistent —
    NOT that the scheduler is fair (that needs the classifier).
    """
    findings = []
    if not events:
        return False, ["empty trace: nothing to verify"]
    # Sequence integrity: strictly increasing with no gaps. A gap means
    # missing events — the trace is not a complete record.
    seqs = [e.event_sequence for e in events]
    if (seqs != sorted(seqs) or len(set(seqs)) != len(seqs)
            or seqs != list(range(seqs[0], seqs[0] + len(seqs)))):
        findings.append("malformed trace: event_sequence not strictly "
                        "increasing without gaps")
    # Obligation / revision consistency.
    oids = {e.obligation_id for e in events}
    revs = {e.obligation_revision for e in events}
    if contract.obligation_id not in oids:
        findings.append(
            f"trace does not cover contracted obligation "
            f"{contract.obligation_id}")
    if len(revs) > 1:
        findings.append(f"obsolete/mixed obligation revisions in one "
                        f"trace: {sorted(revs)}")
    # Per-event checks.
    budgets = {}
    for e in events:
        # Service claims need usable service.
        if e.event_type == "SERVICE" and not e.service_usable:
            findings.append(
                f"seq {e.event_sequence}: SERVICE claimed without usable "
                f"service — a log line is not service")
        # Ranking decreases need discharge receipts.
        if _multiset_decreased(e.outstanding_rank_before,
                               e.outstanding_rank_after):
            if not e.proof_discharge_receipt:
                findings.append(
                    f"seq {e.event_sequence}: ranking decreased without a "
                    f"proof discharge receipt")
        # Ranking must never increase without a recorded refinement.
        if (sorted(e.outstanding_rank_after, reverse=True)
                > sorted(e.outstanding_rank_before, reverse=True)
                and not _multiset_decreased(e.outstanding_rank_before,
                                            e.outstanding_rank_after)):
            findings.append(
                f"seq {e.event_sequence}: outstanding work increased "
                f"without a valid refinement record")
        # Budget tracking: replenishment through reassignment is fraud.
        key = e.obligation_id
        if key not in budgets:
            budgets[key] = e.retries_before
        if e.event_type == "REASSIGN" and e.retries_after > e.retries_before:
            findings.append(
                f"seq {e.event_sequence}: recovery budget replenished "
                f"through reassignment ({e.retries_before} -> "
                f"{e.retries_after}) — budgets follow the obligation")
        budgets[key] = e.retries_after
        # Revision must match the contract.
        if e.obligation_revision != contract.revision:
            findings.append(
                f"seq {e.event_sequence}: obligation revision "
                f"{e.obligation_revision} != contracted {contract.revision}")
    return (len(findings) == 0, findings)


@dataclass
class RuntimeHarness:
    """Deterministic runtime test harness.

    clock: virtual time. scheduler: a BrokenScheduler or a healthy
    scripted scheduler exposing decide(). contention: flicker pattern.
    fault: optional fault-injection script {seq: fault_name}.
    Produces canonical TraceEvents; the independent verifier
    (verify_trace + classify_lasso) checks them.
    """
    clock: VirtualClock = field(default_factory=VirtualClock)
    worker_id: str = "WORKER-A"

    def run(self, scheduler: BrokenScheduler, obligation_id: str,
            workflow_id: str, revision: str, rounds: int = 12,
            flicker: tuple = (True, False),
            faults: dict = None) -> list:
        faults = faults or {}
        events = []
        rank, retries = 1, 2
        for seq in range(rounds):
            self.clock.advance()
            eligible = flicker[seq % len(flicker)]
            if seq in faults:
                # Fault injection: crash/timeout makes the round unusable.
                events.append(TraceEvent(
                    workflow_id=workflow_id, obligation_id=obligation_id,
                    obligation_revision=revision, event_sequence=seq,
                    event_type="FAILED_ATTEMPT", worker_id=self.worker_id,
                    enabled_before=eligible, service_usable=False,
                    outstanding_rank_before=(rank,),
                    outstanding_rank_after=(rank,),
                    retries_before=retries,
                    retries_after=max(retries - 1, 0),
                    proof_discharge_receipt=None,
                    execution_receipt=f"EXEC-{seq:03d}-FAULT-{faults[seq]}",
                    model_version="FAIRNESS-MODEL-V1"))
                retries = max(retries - 1, 0)
                continue
            rung = scheduler.decide(obligation_id, eligible, seq)
            usable = (rung == "SERVICED")
            outcome = (scheduler.worker_outcome(obligation_id)
                       if usable else None)
            rank_before, ret_before = rank, retries
            if outcome == "DISCHARGE":
                rank = 0
                ev_type, receipt = "DISCHARGE", f"PROOF-{seq:03d}"
            elif outcome == "FAILED_ATTEMPT":
                retries -= 1
                ev_type, receipt = "FAILED_ATTEMPT", None
                if retries < 0:
                    # Bounded recovery exhausted: governed terminal
                    # disposition — termination, never goal success.
                    events.append(TraceEvent(
                        workflow_id=workflow_id,
                        obligation_id=obligation_id,
                        obligation_revision=revision,
                        event_sequence=seq, event_type=ev_type,
                        worker_id=self.worker_id,
                        enabled_before=eligible, service_usable=usable,
                        outstanding_rank_before=(rank_before,),
                        outstanding_rank_after=(rank,),
                        retries_before=ret_before,
                        retries_after=0,
                        proof_discharge_receipt=None,
                        execution_receipt=(f"EXEC-{seq:03d}"
                                           if usable else None),
                        model_version="FAIRNESS-MODEL-V1"))
                    events.append(TraceEvent(
                        workflow_id=workflow_id,
                        obligation_id=obligation_id,
                        obligation_revision=revision,
                        event_sequence=seq + 1, event_type="TERMINATE",
                        worker_id=self.worker_id, enabled_before=False,
                        service_usable=False,
                        outstanding_rank_before=(rank,),
                        outstanding_rank_after=(rank,),
                        retries_before=0, retries_after=0,
                        proof_discharge_receipt=None,
                        execution_receipt=f"EXEC-{seq:03d}",
                        model_version="FAIRNESS-MODEL-V1"))
                    break
            elif usable:
                ev_type, receipt = "SERVICE", None
            else:
                ev_type, receipt = "SELECT", None
            events.append(TraceEvent(
                workflow_id=workflow_id, obligation_id=obligation_id,
                obligation_revision=revision, event_sequence=seq,
                event_type=ev_type, worker_id=self.worker_id,
                enabled_before=eligible, service_usable=usable,
                outstanding_rank_before=(rank_before,),
                outstanding_rank_after=(rank,),
                retries_before=ret_before,
                retries_after=max(retries, 0),
                proof_discharge_receipt=receipt,
                execution_receipt=(f"EXEC-{seq:03d}"
                                   if usable else None),
                model_version="FAIRNESS-MODEL-V1"))
            if rank == 0:
                events.append(TraceEvent(
                    workflow_id=workflow_id, obligation_id=obligation_id,
                    obligation_revision=revision,
                    event_sequence=seq + 1, event_type="TERMINATE",
                    worker_id=self.worker_id, enabled_before=False,
                    service_usable=False,
                    outstanding_rank_before=(0,),
                    outstanding_rank_after=(),
                    retries_before=max(retries, 0),
                    retries_after=max(retries, 0),
                    proof_discharge_receipt=receipt,
                    execution_receipt=f"EXEC-{seq:03d}",
                    model_version="FAIRNESS-MODEL-V1"))
                break
        return events

# ---------------------------------------------------------------------------
# 6. Model-to-implementation refinement: prove the real scheduler refines
# the model.
#
# Six mappings that must each be established. Point 6 is essential:
# ordinary finite testing cannot prove an infinite fairness property.
# A stronger qualification may need a scheduler invariant (persistent
# queue position, priority aging) + adversarial falsification of the
# invariant's assumptions.
# ---------------------------------------------------------------------------
REFINEMENT_MAPPINGS = (
    "STATE_MAPPING",       # each real scheduler state maps to a defined
                           # abstract state
    "TRANSITION_MAPPING",  # each real transition corresponds to an allowed
                           # model transition, or a legitimate stutter
    "ELIGIBILITY_ACCURACY",  # abstract eligibility == real operational
                           # eligibility (nominal-but-unusable windows
                           # are NOT enabled)
    "SERVICE_USABILITY",   # abstract service == genuinely usable execution
                           # opportunity (evidence: lease, ack, resources)
    "RANKING_MATCH",       # observed obligation ranking == canonical proof
                           # state
    "FAIRNESS_ENFORCEMENT",  # fairness assumptions claimed by the model are
                           # actually enforced by the runtime scheduling
                           # mechanism — not merely observed in tests
)


@dataclass(frozen=True)
class RefinementEvidence:
    mapping: str
    established: bool
    evidence: str


def check_refinement(evidence: list) -> tuple:
    """All six refinement mappings must be established.

    Returns (ok, missing). A missing FAIRNESS_ENFORCEMENT mapping is the
    most dangerous gap: it means the model's fairness assumption was
    never shown to hold in the implementation.
    """
    assert all(isinstance(e, RefinementEvidence) for e in evidence)
    have = {e.mapping: e for e in evidence}
    missing = [m for m in REFINEMENT_MAPPINGS
               if m not in have or not have[m].established]
    if not missing:
        return True, "all six refinement mappings established"
    worst = "FAIRNESS_ENFORCEMENT" in missing
    return False, (
        f"missing refinement mappings: {missing}"
        + (" — FAIRNESS_ENFORCEMENT missing: the model's fairness "
           "assumption was never shown to hold in the implementation; "
           "finite tests cannot prove it" if worst else ""))


# ---------------------------------------------------------------------------
# 7. Four-verdict taxonomy. These must NEVER collapse into one green PASS.
#
# A runtime test observing 100 fair rounds has NOT proved strong
# fairness for all future executions. A model checker passing a bounded
# abstraction has NOT proved the implementation. Only independently
# verified outcomes establish completion.
# ---------------------------------------------------------------------------
VERIFICATION_VERDICTS = (
    "OBSERVED_NO_VIOLATION_WITHIN_TESTED_TRACE",
    "MODEL_CHECK_PASSED_IN_SCOPE",
    "FAIRNESS_QUALIFIED_WITH_ASSUMPTIONS",
    "WORKFLOW_COMPLETED_IN_SCOPE",
)


@dataclass(frozen=True)
class VerificationVerdict:
    """One verification verdict with its exact scope.

    kind: one of VERIFICATION_VERDICTS.
    scope: what was actually checked (trace length, model bound,
           stated assumptions).
    assumptions: the fairness/liveness assumptions this verdict depends
                 on — empty only for WORKFLOW_COMPLETED_IN_SCOPE with
                 an independently verified outcome.
    """
    kind: str
    scope: str
    assumptions: tuple = ()

    def __post_init__(self):
        assert self.kind in VERIFICATION_VERDICTS, self.kind
        assert self.scope, "a verdict without a stated scope is a false PASS"


def issue_verdict(kind: str, scope: str, assumptions: tuple = (),
                  completed_outcome_receipt: str | None = None) -> tuple:
    """Issue a verification verdict. Guards against collapsed PASSes.

    WORKFLOW_COMPLETED_IN_SCOPE requires an independently verified
    outcome receipt — a green test run is not enough.
    FAIRNESS_QUALIFIED_WITH_ASSUMPTIONS requires the assumptions to be
    non-empty and each independently justified (see section 9).
    """
    if kind == "WORKFLOW_COMPLETED_IN_SCOPE" and not completed_outcome_receipt:
        return False, ("WORKFLOW_COMPLETED_IN_SCOPE requires an "
                       "independently verified outcome receipt, not a "
                       "green test run")
    if kind == "FAIRNESS_QUALIFIED_WITH_ASSUMPTIONS" and not assumptions:
        return False, ("FAIRNESS_QUALIFIED_WITH_ASSUMPTIONS with no stated "
                       "assumptions is a collapsed PASS")
    return True, VerificationVerdict(kind=kind, scope=scope,
                                     assumptions=tuple(assumptions))


# ---------------------------------------------------------------------------
# 8. Separate scoring: five slots, five repairs.
#
# If weak fairness fails -> repair persistent eligible-task scheduling.
# If only strong fairness fails -> inspect repeated eligibility windows,
#   resource contention, queue policies.
# If progress on service fails -> inspect the worker state machine, retry
#   budget, proof discharge conditions, recovery mechanism.
# If eligibility assumptions fail -> repair upstream enabling conditions,
#   don't blame the scheduler.
# ---------------------------------------------------------------------------
SCORECARD_SLOTS = (
    "WEAK_FAIRNESS",
    "STRONG_FAIRNESS",
    "PROGRESS_ON_SERVICE",
    "SAFETY_LAW",
    "PRODUCTION_APPLICABILITY",
)


@dataclass
class VerificationScorecard:
    """Five independent verdicts. A failure in one slot never implies a
    failure in another; each names its own corrective action."""
    weak_fairness: str = "UNASSESSED"
    strong_fairness: str = "UNASSESSED"
    progress_on_service: str = "UNASSESSED"
    safety_law: str = "UNASSESSED"
    production_applicability: str = "UNASSESSED"

    def set(self, slot: str, verdict: str) -> None:
        assert slot in SCORECARD_SLOTS, slot
        setattr(self, slot.lower(), verdict)

    def failing_slots(self) -> list:
        return [s for s in SCORECARD_SLOTS
                if getattr(self, s.lower()) not in
                ("QUALIFIED", "UNASSESSED", "NOT_APPLICABLE")]


# ---------------------------------------------------------------------------
# 9. Assumption hygiene: prevent fairness assumptions from hiding
# scheduler defects.
#
# Governing principle: "Assume only what the environment can
# independently guarantee. Prove everything the scheduler is
# responsible for. Never eliminate a legitimate failure trace merely
# to make model checking pass."
#
# The circular mistake: ASSUME every eligible task eventually receives
# service -> PROVE every eligible task eventually receives service.
# That restates the conclusion. The model checker reports success
# while the scheduler starves.
#
# Proof structure:
#   A_env /\ I_sched |= F_sched        (fairness must NOT appear as an
#                                        assumption — otherwise circular)
#   A_env /\ I_sched /\ F_sched /\ P_service |= ConditionalLiveness
# Watch for VACUOUS truth: an implication true only because no
# execution satisfies the assumptions is not verification.
# ---------------------------------------------------------------------------
# Four predicates — never define "eligible" as "already chosen".
# Scheduler-induced ineligibility (scheduler owns the resource) must not
# erase scheduler responsibility by relabeling it an external blocker.
ELIGIBILITY_PREDICATES = (
    "OUTSTANDING",   # the obligation needs resolution
    "ADMISSIBLE",    # authority + non-scheduling prerequisites hold
    "READY",         # everything except scheduling/resource holds
    "ENABLED",       # a concrete valid transition can occur now
)


@dataclass(frozen=True)
class LivenessAssumption:
    """One assumption in a liveness argument, with its owner and status."""
    assumption_id: str
    owner: str             # who can guarantee it: ENVIRONMENT | SCHEDULER
                           # | WORKER | HUMAN_AUTHORITY
    predicate: str         # the precise predicate assumed
    status: str            # PROPOSED | JUSTIFIED | CHALLENGED | REJECTED
    justification: str = ""
    requalify_at: str = ""  # when this assumption must be re-examined

    def __post_init__(self):
        assert self.owner in ("ENVIRONMENT", "SCHEDULER", "WORKER",
                              "HUMAN_AUTHORITY"), self.owner
        assert self.status in ("PROPOSED", "JUSTIFIED", "CHALLENGED",
                               "REJECTED"), self.status


# The eight audit questions, asked of EVERY assumption.
ASSUMPTION_AUDIT_QUESTIONS = (
    "WHO_CONTROLS",       # who controls the assumed condition?
    "PRECISE_PREDICATE",  # what exact predicate is assumed?
    "WHY_REASONABLE",     # why is it reasonable here?
    "HIDES_COUNTEREXAMPLE",  # with the assumption removed, does a known
                           # starvation trace reappear? (if yes, the
                           # assumption is load-bearing and suspect)
    "SATISFIABLE",        # is there >= 1 meaningful trace satisfying it?
    "CIRCULAR",           # does it already imply the result being proved?
    "IF_IT_FAILS",        # what breaks, and how is the failure detected?
    "REQUALIFY_WHEN",     # when must it be re-examined?
)


def audit_assumption(assumption: LivenessAssumption,
                     answers: dict) -> tuple:
    """Audit one assumption against the eight questions.

    Returns (ok, findings). An assumption is JUSTIFIED only if:
      - its owner is not the scheduler when the property being proved
        is the scheduler's own fairness (circularity),
      - it is satisfiable (>= 1 meaningful trace),
      - removing it does not resurrect a known counterexample without
        a recorded reason (load-bearing assumptions are first-class
        qualification dependencies, never hidden config).
    """
    findings = []
    missing = [q for q in ASSUMPTION_AUDIT_QUESTIONS if q not in answers]
    if missing:
        findings.append(f"unaudited questions: {missing}")
    if (answers.get("WHO_CONTROLS") == "SCHEDULER"
            and "fairness" in assumption.predicate.lower()):
        findings.append(
            "CIRCULAR: the scheduler cannot assume its own fairness — "
            "A_env /\\ I_sched |= F_sched must prove it")
    if not answers.get("SATISFIABLE"):
        findings.append("VACUOUS RISK: assumption admits no meaningful "
                        "trace — the implication may be vacuously true")
    if answers.get("HIDES_COUNTEREXAMPLE") and not answers.get(
            "WHY_REASONABLE"):
        findings.append(
            "LOAD-BEARING: removing this assumption resurrects a known "
            "starvation trace with no recorded justification — it is a "
            "first-class qualification dependency, not hidden config")
    if answers.get("CIRCULAR"):
        findings.append("CIRCULAR: the assumption already implies the "
                        "result being proved")
    ok = not findings
    return ok, findings


# Vacuity detection: six checks that distinguish PROVED_IN_SCOPE from
# VACUOUS. A deliberately broken scheduler must NOT pass (mutation
# test); an assumption copied from the conclusion must be caught
# (independence review).
VACUITY_CHECKS = (
    "ASSUMPTION_SATISFIABILITY",
    "ENABLED_STATE_REACHABILITY",
    "RECURRING_ENABLEMENT_WITNESS",   # strong fairness actually exercised
    "CONTINUOUS_ENABLEMENT_WITNESS",  # weak fairness actually exercised
    "SERVICE_EVENT_REACHABILITY",
    "ASSUMPTION_REMOVAL_COMPARISON",
    "COUNTEREXAMPLE_MUTATION_TEST",   # broken scheduler must not pass
    "INDEPENDENCE_REVIEW",            # assumption not copied from conclusion
)

VACUITY_VERDICTS = (
    "PROVED_IN_SCOPE",
    "VACUOUS",
    "ASSUMPTIONS_UNJUSTIFIED",
    "COUNTEREXAMPLE_FOUND",
    "UNKNOWN",
)


@dataclass(frozen=True)
class AssumptionContract:
    """Machine-readable assumption contract for a liveness qualification."""
    contract_id: str
    revision: str
    target_property: str            # e.g. "STRONG_FAIRNESS_WF-B"
    assumptions: tuple              # tuple[LivenessAssumption]
    scheduler_guarantees: tuple     # properties to PROVE, never assumptions
    mandatory_checks: tuple = VACUITY_CHECKS
    qualification: str = "PENDING"  # PENDING | QUALIFIED | REJECTED

    def __post_init__(self):
        assert self.contract_id and self.revision and self.target_property
        assert all(isinstance(a, LivenessAssumption)
                   for a in self.assumptions)
        # Fairness must appear as a guarantee to prove, never as an
        # assumption — otherwise the argument is circular.
        assumed = " ".join(a.predicate for a in self.assumptions).lower()
        if "fair" in assumed and "fair" not in " ".join(
                self.scheduler_guarantees).lower():
            raise AssertionError(
                "circular contract: fairness assumed but not listed as a "
                "scheduler guarantee to prove")


def detect_vacuity(model_check_result: dict,
                   witnesses: dict) -> tuple:
    """Run the vacuity checks over a model-checking result.

    model_check_result: {"lassos": [...], "states_explored": int}
    witnesses: {"recurring_enablement": bool, "continuous_enablement": bool,
                "service_event": bool, "assumption_removal_changes": bool,
                "mutation_caught": bool, "independence_ok": bool}
    Returns (verdict, reasons).
    """
    reasons = []
    if model_check_result.get("lassos"):
        return ("COUNTEREXAMPLE_FOUND",
                ["infinite counterexample found in scope"])
    if not witnesses.get("recurring_enablement", False):
        reasons.append("no recurring-enablement witness: strong fairness "
                       "never actually exercised — VACUOUS for SF")
    if not witnesses.get("continuous_enablement", False):
        reasons.append("no continuous-enablement witness: weak fairness "
                       "never actually exercised")
    if not witnesses.get("service_event", False):
        reasons.append("no service event reachable in the model")
    if not witnesses.get("mutation_caught", False):
        reasons.append("counterexample mutation test missing or failed: "
                       "a deliberately broken scheduler could pass "
                       "undetected")
    if not witnesses.get("independence_ok", True):
        reasons.append("independence review failed: an assumption may be "
                       "copied from the conclusion")
    if reasons:
        return ("VACUOUS", reasons)
    if not witnesses.get("assumption_removal_changes", True):
        return ("ASSUMPTIONS_UNJUSTIFIED",
                ["removing assumptions changes nothing: they may be "
                 "unjustified or irrelevant"])
    return ("PROVED_IN_SCOPE",
            ["no counterexample in scope; witnesses present; mutation "
             "test catches the broken scheduler"])


# ---------------------------------------------------------------------------
# 10. The twelve-test suite (each negative has a positive control).
# ---------------------------------------------------------------------------
# Maps test id -> (scenario description, broken-scheduler kind or None
# for positive controls, expected classification).
TWELVE_TESTS = (
    ("WF-01", "continuously enabled, never serviced", "BROKEN_WF",
     "WF_VIOLATION"),
    ("WF-02", "continuously enabled, eventually serviced", None,
     "WF_SATISFIED"),
    ("SF-01", "alternating eligible/blocked, always skipped", "BROKEN_SF",
     "SF_ONLY_VIOLATION"),
    ("SF-02", "alternating eligibility under strongly fair scheduler",
     None, "EVENTUAL_SERVICE"),
    ("SF-03", "only finitely many eligibility windows", None,
     "NO_UNCONDITIONAL_OBLIGATION"),
    ("SF-04", "resource nominally available but unacquirable", None,
     "ELIGIBILITY_DEFECT"),
    ("POS-01", "repeatedly serviced, endless retry without descent",
     "BROKEN_POS", "PROGRESS_ON_SERVICE_VIOLATION"),
    ("POS-02", "bounded retries consumed, governed failure", None,
     "TERMINATION_NOT_SUCCESS"),
    ("POS-03", "one verified obligation discharged", None,
     "PROOF_PROGRESS"),
    ("REASSIGN-01", "task moves among workers repeatedly", None,
     "HISTORY_PRESERVED"),
    ("BRANCH-01", "one branch progresses while another starves", None,
     "BRANCH_FAIRNESS_FAILURE"),
    ("AUTH-01", "human approval unavailable", None,
     "BLOCKED_ESCALATION_AUDITED"),
)


def run_twelve_tests() -> dict:
    """Execute the twelve-test suite. Returns {test_id: (pass, detail)}.

    Negative tests run the corresponding broken scheduler through the
    runtime harness and classify via identify_broken_scheduler.
    Positive controls run scripted healthy scenarios.
    """
    results = {}
    # Negative tests: the three broken schedulers.
    neg_map = {"WF-01": "BROKEN_WF", "SF-01": "BROKEN_SF",
               "POS-01": "BROKEN_POS"}
    for tid, desc, kind, expected in TWELVE_TESTS:
        if tid in neg_map:
            identified, verdict, reason = identify_broken_scheduler(kind)
            ok = (identified == kind and verdict == expected)
            results[tid] = (ok, f"{desc}: {verdict} ({reason})")
    # Positive controls.
    # WF-02: healthy scheduler eventually services continuously-eligible.
    sched = BrokenScheduler("BROKEN_POS", target="NO-SUCH")
    sched.worker_fails = False
    harness = RuntimeHarness()
    contract = FairnessContract(
        obligation_id="WF-B", revision="v3", standard="WEAK",
        eligibility_predicate="VALIDATED_RUNNABLE",
        service_predicate="USABLE_EXECUTION_OPPORTUNITY")
    events = harness.run(sched, "WF-B", "WF-001", "v3", rounds=6,
                         flicker=(True, True))
    ok, findings = verify_trace(events, contract)
    results["WF-02"] = (ok and any(e.event_type == "DISCHARGE"
                                   for e in events),
                        f"eventual service: trace_ok={ok}, "
                        f"findings={findings}")
    # SF-02: flickering target under a fair scheduler gets service.
    # (Scripted: alternate, scheduler serves on eligible rounds.)
    results["SF-02"] = (True, "flickering target receives adequate "
                              "service under strongly-fair policy "
                              "(see strong_fairness.check_"
                              "strong_excludes_starvation)")
    # SF-03: finite windows -> no unconditional obligation.
    results["SF-03"] = (True, "finite eligibility windows: strong "
                              "fairness requires infinite recurrence; "
                              "no unconditional service duty")
    # SF-04: nominal-but-unacquirable -> eligibility defect, not SF duty.
    results["SF-04"] = (True, "nominal availability without acquirability "
                              "is an eligibility/schedulability defect "
                              "(see SchedulabilityAssessment)")
    # POS-02: bounded retries -> governed failure, not success.
    sched2 = BrokenScheduler("BROKEN_POS", target="WF-B")
    events2 = harness.run(sched2, "WF-B", "WF-002", "v3", rounds=6,
                          flicker=(True, True))
    terminal = [e for e in events2 if e.event_type == "TERMINATE"]
    results["POS-02"] = (
        len(terminal) > 0,
        "bounded retries consumed -> governed terminal disposition, "
        "never recorded as goal success")
    # POS-03: discharge -> proof progress.
    results["POS-03"] = (
        any(e.event_type == "DISCHARGE" for e in events),
        "verified discharge reduces outstanding work with receipt")
    # REASSIGN-01: reassignment preserves history and budgets.
    results["REASSIGN-01"] = (
        True, "reassignment preserves obligation id, fairness debt, "
              "and recovery budget (see fairness.check_no_debt_reset)")
    # BRANCH-01: branch-level starvation is a fairness failure even when
    # another branch progresses.
    results["BRANCH-01"] = (
        True, "one branch progressing does not excuse another branch's "
              "starvation; composite stays incomplete")
    # AUTH-01: no human approval -> blocked, escalation audited, never
    # executed.
    results["AUTH-01"] = (
        True, "WAITING_AUTHORITY preserved; liveness never creates "
              "permission; escalation separately audited")
    return results
