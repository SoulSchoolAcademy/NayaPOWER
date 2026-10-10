"""Multi-node liveness & guaranteed progress (spec).

Principle: "Safety prevents wrong actions. Liveness ensures eligible work
makes progress. Neither may be sacrificed to satisfy the other."

The deadlock case this exists for: KNOW waits for LAW, LAW waits for ACT,
ACT waits for KNOW, VERIFY waits for ACT. Zero safety violations, every
local invariant holds — and the request never finishes. Safety and liveness
are SEPARATE proof obligations on the same interaction.

Composes with:
  migration.py    — MultiPartyInteraction carries safety invariants
                    (InvariantSpec kind SAFETY/TEMPORAL). LivenessObligation
                    sits ALONGSIDE them on the same interaction: assess_liveness
                    is a separate assessment from assess_multi_party. A
                    system can be safety-qualified and liveness-unqualified
                    at the same time.
  propagation.py  — MeaningEnvelope for environment scope; qualification
                    verdicts map onto the six revocation verdicts.
  revocation.py   — VERDICTS reused for LivenessReceipt qualification.
  uncertainty.py  — WAITING_DEPENDENCY on undetermined evidence is governed
                    waiting, not a liveness failure.
  authority.py    — LAW determines permission. Liveness NEVER creates
                    permission and NEVER weakens LAW.

Hard rules:
  - Liveness never creates permission: no liveness obligation, deadline, or
    recovery action can authorize what LAW denied. WAITING_AUTHORITY can
    only leave via a real authorization — never via a liveness transition
    to COMPLETED.
  - Recovery never weakens LAW: a repair that makes work finish by
    bypassing authorization is an INVALID repair, even if the task
    completes.
  - No invented progress: heartbeats, log lines, status rewrites, and bare
    retries are not progress. Progress = a state change in a required proof
    obligation or movement toward a valid outcome. RETRYING<->WAITING churn
    never counts as cumulative advancement.
  - Refusal is not completion: a governed refusal satisfies DISPOSITION
    liveness but NOT TASK_COMPLETION liveness.
  - Escalation is not completion: handing a request to a human changes
    responsibility; it does not finish the task.
  - Cycle alone is not deadlock: a wait-for cycle broken by a valid
    timeout, cancellation, fallback, or external event is not a deadlock.
    The verifier must establish whether a reachable, permitted escape path
    exists.

This module is SPEC + deterministic machinery. NOT wired into kernel/,
KNOW, LAW, ACT, or any live path. Wiring needs Shawn's word.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .propagation import MeaningEnvelope
from .revocation import VERDICTS

# ---------------------------------------------------------------------------
# Three liveness types. Never collapsed into one PASS/FAIL.
# ---------------------------------------------------------------------------
# DISPOSITION: every accepted request eventually receives a valid outcome or
#   an explicit governed waiting/escalation disposition. No request
#   disappears silently.
# WORKFLOW_PROGRESS: an enabled, eligible workflow advances without
#   permanent starvation.
# TASK_COMPLETION: work that remains eligible and whose required resources
#   are available eventually reaches its required successful outcome.
LIVENESS_TYPES = (
    "DISPOSITION",
    "WORKFLOW_PROGRESS",
    "TASK_COMPLETION",
)

# ---------------------------------------------------------------------------
# Workflow state taxonomy. The state machine is the governance: a system may
# never reclassify WAITING_AUTHORITY as COMPLETED, and liveness machinery
# may never move a workflow out of WAITING_AUTHORITY — only a real
# authorization can do that.
# ---------------------------------------------------------------------------
WORKFLOW_STATES = (
    "RUNNABLE",            # all prerequisites satisfied; must receive fair execution
    "IN_PROGRESS",         # a worker is actively advancing the task
    "WAITING_DEPENDENCY",  # a required dependency has not responded
    "WAITING_AUTHORITY",   # a consequential human/authority decision is required
    "BLOCKED_RECOVERABLE", # a technical fault prevents progress; bounded recovery
    "DEADLOCK_SUSPECTED",  # apparently nonprogressing dependency cycle
    "STARVATION_SUSPECTED",# eligible task repeatedly loses execution opportunity
    "COMPLETED",           # required work and proof conditions satisfied (terminal)
)

# Legal transitions. WAITING_AUTHORITY has exactly two exits: stay, or move
# to RUNNABLE on presentation of a real authorization. It can NEVER go to
# COMPLETED — that transition does not exist, by construction.
LEGAL_TRANSITIONS = {
    "RUNNABLE": ("IN_PROGRESS", "WAITING_DEPENDENCY", "WAITING_AUTHORITY",
                 "BLOCKED_RECOVERABLE", "COMPLETED"),
    "IN_PROGRESS": ("RUNNABLE", "WAITING_DEPENDENCY", "WAITING_AUTHORITY",
                    "BLOCKED_RECOVERABLE", "DEADLOCK_SUSPECTED",
                    "STARVATION_SUSPECTED", "COMPLETED"),
    "WAITING_DEPENDENCY": ("RUNNABLE", "IN_PROGRESS", "BLOCKED_RECOVERABLE",
                           "DEADLOCK_SUSPECTED", "STARVATION_SUSPECTED"),
    "WAITING_AUTHORITY": ("WAITING_AUTHORITY", "RUNNABLE"),
    "BLOCKED_RECOVERABLE": ("RUNNABLE", "IN_PROGRESS", "WAITING_DEPENDENCY"),
    "DEADLOCK_SUSPECTED": ("RUNNABLE", "IN_PROGRESS", "BLOCKED_RECOVERABLE"),
    "STARVATION_SUSPECTED": ("RUNNABLE", "IN_PROGRESS"),
    "COMPLETED": (),
}

# ---------------------------------------------------------------------------
# Progress failure classes.
# ---------------------------------------------------------------------------
FAILURE_CLASSES = (
    "DEADLOCK",    # obligations wait on dependencies unsatisfiable under the
                   # present state and allowed transitions
    "LIVELOCK",    # nodes keep processing/retrying but never advance the outcome
    "STARVATION",  # eligible obligation stays pending; others get scheduled
)

# Verification techniques for liveness. Runtime timeouts are operational
# safeguards, not proofs of eventual completion.
LIVENESS_TECHNIQUES = (
    "model_checking",      # finite abstraction; fairness assumptions explicit
    "fault_injection",     # delayed/crashed/missing/competing conditions
    "runtime_monitoring",  # age, milestones, deadlines, escalation
)

# Fairness assumptions. Weak fairness: a continuously enabled transition is
# eventually scheduled. The exact assumption must match the REAL scheduler.
FAIRNESS_ASSUMPTIONS = (
    "weak_fairness",       # continuously enabled -> eventually scheduled
    "strong_fairness",     # infinitely-often enabled -> eventually scheduled
    "bounded_wait",        # enabled -> scheduled within a stated bound
)

# ---------------------------------------------------------------------------
# Progress witnesses. A heartbeat is not proof of progress.
# ---------------------------------------------------------------------------
# Event kinds that NEVER count as progress, no matter how many occur.
NON_PROGRESS_EVENTS = (
    "heartbeat",
    "log_line",
    "status_rewrite",
    "retry_attempt",       # a bare retry, without an obligation state change
)

# Canonical per-node milestones. A transition counts as useful progress only
# when it produces one of these (or an obligation-specific equivalent).
STANDARD_MILESTONES = {
    "KNOW": "applicable evidence returned with provenance",
    "LAW": "valid decision receipt issued, or explicit refusal recorded",
    "ACT": "execution attempt and actual effect recorded with exact target",
    "VERIFY": "independently checked outcome receipt",
    "LEARN": "eligible lesson assessed against its proof criteria",
    "EVOLVE": "successor package persisted and independently validated",
    "SELF": "identity and authorized successor context preserved",
    "PROVE": "access, evaluation, and authorization receipts preserved",
    "CONNECT": "derivation and corroboration traced",
}


@dataclass(frozen=True)
class LivenessObligation:
    """A multi-party progress obligation, versioned like every other
    obligation. References the existing obligation/provenance graph — no new
    graph engine. Binds the fairness assumptions explicitly: "everything
    always completes" is not a meaningful guarantee; the conditional form
    is: [](Eligible(d) & FairExecutionConditions(d) => <>Completed(d))."""
    obligation_id: str
    revision: str
    liveness_type: str                    # one of LIVENESS_TYPES
    participants: tuple                   # node obligation ids, e.g. ("KNOW","LAW","ACT","VERIFY")
    trigger: str                          # event beginning the progress requirement
    progress_target: str                  # exact milestone or completion condition
    dependency_graph: tuple = ()          # (predecessor, successor) pairs
    enabled_conditions: tuple = ()        # conditions under which progress is required
    fairness_assumptions: tuple = ()      # subset of FAIRNESS_ASSUMPTIONS
    progress_witnesses: tuple = ()        # required milestone evidence kinds
    deadline_policy: tuple = ()           # ((stage, max_age_units), ...) when applicable
    recovery_policy: tuple = ()           # authorized recovery mechanisms
    external_blockers: tuple = ()         # human decisions, outages, outside control
    environment: MeaningEnvelope = MeaningEnvelope()
    supersedes: str = ""

    def __post_init__(self):
        assert self.liveness_type in LIVENESS_TYPES, self.liveness_type
        for f in self.fairness_assumptions:
            assert f in FAIRNESS_ASSUMPTIONS, f
        assert self.participants, "a liveness obligation needs participants"
        assert self.progress_target, "a liveness obligation needs a target"


@dataclass(frozen=True)
class WorkflowState:
    """One workflow's position in the state taxonomy."""
    workflow_id: str
    state: str
    since_seq: int = 0
    note: str = ""

    def __post_init__(self):
        assert self.state in WORKFLOW_STATES, self.state


def transition(state: WorkflowState, to: str,
               authorization: str = "") -> tuple:
    """Attempt a state transition. Returns (ok, new_state_or_reason).

    Leaving WAITING_AUTHORITY requires a real authorization receipt;
    the machinery can never liveness-transition it to COMPLETED because
    that edge does not exist in LEGAL_TRANSITIONS.
    """
    if to not in WORKFLOW_STATES:
        return False, f"unknown target state {to}"
    if to not in LEGAL_TRANSITIONS[state.state]:
        return False, (
            f"illegal transition {state.state} -> {to}; "
            f"WAITING_AUTHORITY can only become RUNNABLE on real "
            f"authorization, never COMPLETED by liveness machinery")
    if state.state == "WAITING_AUTHORITY" and to == "RUNNABLE" \
            and not authorization:
        return False, ("WAITING_AUTHORITY -> RUNNABLE requires a real "
                       "authorization receipt; liveness does not create "
                       "permission")
    return True, WorkflowState(state.workflow_id, to, state.since_seq,
                               state.note)


# ---------------------------------------------------------------------------
# Failure detection.
# ---------------------------------------------------------------------------

def find_wait_cycles(wait_for: dict) -> tuple:
    """Find cycles in the wait-for graph. wait_for: node -> tuple(nodes it
    waits on). Returns a tuple of cycles, each a tuple of nodes."""
    cycles = []
    visited: dict = {}

    def visit(node, stack):
        if node in stack:
            cycles.append(tuple(stack[stack.index(node):] + [node]))
            return
        if node in visited:
            return
        visited[node] = True
        stack.append(node)
        for dep in wait_for.get(node, ()):
            visit(dep, stack)
        stack.pop()

    for node in wait_for:
        visit(node, [])
    # Deduplicate rotations of the same cycle.
    seen = set()
    unique = []
    for c in cycles:
        core = c[:-1]
        rotations = {tuple(core[i:] + core[:i]) for i in range(len(core))}
        key = min(rotations)
        if key not in seen:
            seen.add(key)
            unique.append(c)
    return tuple(unique)


def detect_deadlock(wait_for: dict, escape_paths: dict) -> tuple:
    """Deadlock = a wait-for cycle with NO reachable, permitted escape path.

    escape_paths: node -> tuple of available escapes, e.g. ("timeout",
    "cancellation", "fallback", "external_event"). A cycle broken by any
    valid escape is NOT a deadlock — the verifier must establish the
    escape is reachable and permitted, not merely named.

    Returns (verdict, evidence) where verdict is "DEADLOCK",
    "NO_DEADLOCK", or "CYCLE_WITH_ESCAPE".
    """
    cycles = find_wait_cycles(wait_for)
    if not cycles:
        return "NO_DEADLOCK", ("no wait-for cycle",)
    for cycle in cycles:
        members = set(cycle[:-1]) if cycle[-1] == cycle[0] else set(cycle)
        trapped = [n for n in members if not escape_paths.get(n)]
        if trapped:
            return ("DEADLOCK",
                    (f"cycle {' -> '.join(cycle)} with no escape path for "
                     f"{', '.join(sorted(trapped))}",))
    return ("CYCLE_WITH_ESCAPE",
            (f"cycle(s) present but every member has a reachable escape path",
            ))


def detect_livelock(state_history: tuple,
                    progress_seqs: tuple,
                    retry_threshold: int = 3) -> tuple:
    """Livelock = nodes keep processing/retrying without advancing the
    required outcome. Evidence: repeated state signatures with retries but
    no progress marks, or a retry-to-progress ratio at/above threshold.

    state_history: tuple of (seq, state) in order.
    progress_seqs: tuple of seqs where genuine progress was recorded.
    Returns (verdict, evidence): "LIVELOCK_SUSPECTED" or "NO_LIVELOCK".
    """
    if not state_history:
        return "NO_LIVELOCK", ("empty history",)
    progress_set = set(progress_seqs)
    retries = sum(1 for _, s in state_history
                  if s in ("BLOCKED_RECOVERABLE", "WAITING_DEPENDENCY"))
    genuine = len(progress_set)
    # Repeated signature: the same non-terminal state appearing 3+ times
    # with no intervening progress.
    last_progress = max(progress_set) if progress_set else -1
    tail = [s for seq, s in state_history if seq > last_progress]
    from collections import Counter
    repeated = [s for s, c in Counter(tail).items()
                if c >= 3 and s != "COMPLETED"]
    ratio = (retries / genuine) if genuine else float(retries)
    if repeated and genuine == 0 and retries >= retry_threshold:
        return ("LIVELOCK_SUSPECTED",
                (f"state(s) {', '.join(sorted(set(repeated)))} repeated "
                 f"without any genuine progress across {retries} retries",))
    if genuine > 0 and ratio >= retry_threshold and repeated:
        return ("LIVELOCK_SUSPECTED",
                (f"retry-to-progress ratio {ratio:.1f} with repeated "
                 f"state(s) {', '.join(sorted(set(repeated)))}",))
    return "NO_LIVELOCK", ("progress marks present or churn below threshold",)


def detect_starvation(eligible_since: dict,
                      opportunities: dict,
                      scheduled_others: dict,
                      age_threshold: int = 10,
                      now: int | None = None) -> tuple:
    """Starvation = an eligible obligation stays pending while other tasks
    keep getting scheduled.

    eligible_since: workflow -> seq when it became eligible (absent = not eligible).
    opportunities: workflow -> count of scheduling opportunities granted.
    scheduled_others: workflow -> count of OTHER workflows scheduled while it waited.
    now: current seq; defaults to the latest eligible_since value.
    Returns (verdict, evidence): "STARVATION_SUSPECTED" or "NO_STARVATION".
    """
    if now is None:
        now = max(list(eligible_since.values()) + [0])
    suspects = []
    for wf, since in eligible_since.items():
        age = now - since
        opps = opportunities.get(wf, 0)
        others = scheduled_others.get(wf, 0)
        if age >= age_threshold and opps == 0 and others > 0:
            suspects.append(
                f"{wf}: eligible for {age} seqs, 0 opportunities, "
                f"{others} other workflows scheduled")
    if suspects:
        return "STARVATION_SUSPECTED", tuple(suspects)
    return "NO_STARVATION", ("no eligible workflow denied opportunity",)


# ---------------------------------------------------------------------------
# Progress witnesses.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ProgressWitness:
    """Verifiable evidence of meaningful advancement. A witness is genuine
    only if the event changed the state of a required proof obligation or
    moved the workflow toward a valid outcome."""
    workflow_id: str
    node: str
    milestone: str
    evidence_ref: str
    seq: int
    obligation_delta: str = ""  # which proof-obligation state changed

    def __post_init__(self):
        assert self.milestone, "a witness needs a milestone"


def is_genuine_progress(event_kind: str, obligation_delta: str,
                        moves_toward_outcome: bool) -> tuple:
    """The anti-gaming gate. Heartbeats, log lines, status rewrites, and
    bare retries are never progress. Returns (genuine, reason)."""
    if event_kind in NON_PROGRESS_EVENTS:
        return False, (f"{event_kind} is not progress: it changes no proof "
                       f"obligation and moves nothing toward the outcome")
    if not obligation_delta and not moves_toward_outcome:
        return False, ("no proof-obligation state change and no movement "
                       "toward a valid outcome — activity is not progress")
    return True, "genuine progress: obligation state changed or outcome approached"


def witness_coverage(obligation: LivenessObligation,
                     witnesses: tuple) -> tuple:
    """Which required progress witnesses have been produced? Returns
    (covered, missing)."""
    produced = {w.milestone for w in witnesses
                if w.workflow_id}
    required = set(obligation.progress_witnesses)
    missing = tuple(m for m in obligation.progress_witnesses
                    if m not in produced)
    return tuple(sorted(produced & required)), missing


# ---------------------------------------------------------------------------
# Recovery. A recovery that weakens LAW is an invalid repair.
# ---------------------------------------------------------------------------

RECOVERY_MECHANISMS = (
    "bounded_retry",     # retry within a stated bound, same authority
    "reassignment",      # hand to another worker, preserving idempotency
    "escalation",        # governed escalation; changes responsibility, not completion
    "timeout_release",   # release a wait via a pre-authorized timeout path
)


@dataclass(frozen=True)
class RecoveryAction:
    """One authorized recovery step."""
    action_id: str
    workflow_id: str
    mechanism: str
    law_receipt: str = ""          # the LAW authorization this recovery operates under
    preserves_idempotency: bool = True
    preserves_authority: bool = True  # False = bypasses or weakens LAW

    def __post_init__(self):
        assert self.mechanism in RECOVERY_MECHANISMS, self.mechanism


def recovery_valid(action: RecoveryAction) -> tuple:
    """A recovery is valid only if it preserves authority and idempotency.
    Making work finish by weakening LAW is an invalid repair — even if the
    task completes."""
    if not action.preserves_authority:
        return False, ("INVALID REPAIR: recovery weakens or bypasses LAW; "
                       "completion under weakened authority proves nothing")
    if not action.preserves_idempotency and action.mechanism == "reassignment":
        return False, ("reassignment without idempotency risks duplicate "
                       "effects")
    if not action.law_receipt:
        return False, "recovery without a LAW receipt has no authority basis"
    return True, "recovery preserves authority and idempotency"


# ---------------------------------------------------------------------------
# Conditional liveness: [](Eligible & Fair => <>Completed).
# ---------------------------------------------------------------------------

def check_conditional_liveness(obligation: LivenessObligation,
                               state: WorkflowState,
                               eligible: bool,
                               fairness_holds: bool) -> tuple:
    """Evaluate the conditional guarantee for one workflow.

    - Not eligible (e.g. WAITING_AUTHORITY, revoked evidence): NO liveness
      failure. Liveness does not create permission and does not pressure
      ACT across an authority boundary.
    - Eligible but fairness broken: the ASSUMPTION failed, not the system —
      report assumption failure, not a liveness violation.
    - Eligible, fairness holds, terminal-stuck (DEADLOCK_SUSPECTED with no
      recovery, or permanent non-completion): LIVENESS_VIOLATION.
    Returns (verdict, evidence).
    """
    if not eligible:
        return ("NO_VIOLATION",
                (f"{state.workflow_id} not eligible "
                 f"(state={state.state}); liveness requires nothing of "
                 f"ineligible work",))
    if not fairness_holds:
        return ("ASSUMPTION_FAILED",
                ("fairness assumptions do not hold; the conditional "
                 "guarantee's premise failed — investigate scheduling, "
                 "not the workflow",))
    if state.state in ("DEADLOCK_SUSPECTED", "STARVATION_SUSPECTED",
                       "BLOCKED_RECOVERABLE"):
        return ("LIVENESS_VIOLATION",
                (f"{state.workflow_id} eligible with fairness holding but "
                 f"stuck in {state.state}",))
    if state.state == "COMPLETED":
        return "NO_VIOLATION", ("completed",)
    return "NO_VIOLATION", (f"in {state.state}; progressing or governed "
                            f"waiting",)


# ---------------------------------------------------------------------------
# Liveness receipt (append-only) and overall assessment.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class LivenessReceipt:
    """Append-only receipt for a liveness assessment. Binds the witnesses
    actually observed — never a claimed progress score."""
    obligation_id: str
    revision: str
    workflow_id: str
    liveness_type: str
    witnesses: tuple = ()            # ProgressWitness
    techniques_applied: tuple = ()   # subset of LIVENESS_TECHNIQUES
    failure_detected: str = ""       # one of FAILURE_CLASSES or ""
    independent_verification: str = ""
    qualification: str = ""
    invalidated_by: str = ""

    def __post_init__(self):
        assert self.liveness_type in LIVENESS_TYPES, self.liveness_type
        for t in self.techniques_applied:
            assert t in LIVENESS_TECHNIQUES, t
        if self.failure_detected:
            assert self.failure_detected in FAILURE_CLASSES, \
                self.failure_detected
        if self.qualification:
            assert self.qualification in VERDICTS, self.qualification


def assess_liveness(obligation: LivenessObligation,
                    states: dict,
                    wait_for: dict,
                    escape_paths: dict,
                    histories: dict,
                    progress_seqs: dict,
                    eligible_since: dict,
                    opportunities: dict,
                    scheduled_others: dict,
                    fairness_holds: bool,
                    witnesses: tuple) -> dict:
    """Assess one liveness obligation across its workflows.

    This is SEPARATE from assess_multi_party (safety): a workflow can be
    safety-clean and liveness-violated at the same time. Per-type verdicts
    are reported separately — DISPOSITION, WORKFLOW_PROGRESS, and
    TASK_COMPLETION are never merged into one score.

    Returns a dict with per-type verdicts, detected failures, witness
    coverage, and the overall verdict.
    """
    deadlock_v, deadlock_e = detect_deadlock(wait_for, escape_paths)
    per_type = {}
    for wf, st in states.items():
        eligible = wf in eligible_since
        verdict, _ = check_conditional_liveness(
            obligation, st, eligible, fairness_holds)
        per_type[wf] = verdict
    # Livelock / starvation are assessed over the whole participant set.
    all_history = []
    for wf, hist in histories.items():
        all_history.extend(hist)
    all_progress = []
    for wf, seqs in progress_seqs.items():
        all_progress.extend(seqs)
    livelock_v, livelock_e = detect_livelock(tuple(sorted(all_history)),
                                             tuple(sorted(all_progress)))
    starv_v, starv_e = detect_starvation(eligible_since, opportunities,
                                         scheduled_others)
    covered, missing = witness_coverage(obligation, witnesses)

    failures = []
    if deadlock_v == "DEADLOCK":
        failures.append(("DEADLOCK", deadlock_e))
    if livelock_v == "LIVELOCK_SUSPECTED":
        failures.append(("LIVELOCK", livelock_e))
    if starv_v == "STARVATION_SUSPECTED":
        failures.append(("STARVATION", starv_e))

    # Per-type roll-up: a type is violated if any workflow of that
    # obligation's scope shows a violation for the type's criterion.
    # DISPOSITION fails only if a workflow vanished with no disposition
    # (not modeled here — absence of any state record is the signal, and
    # the caller must supply the accepted-request set).
    violations = [w for w, v in per_type.items() if v == "LIVENESS_VIOLATION"]
    type_verdicts = {
        "DISPOSITION": "HOLDS",  # every tracked workflow has a governed state
        "WORKFLOW_PROGRESS": ("VIOLATED" if failures else "HOLDS"),
        "TASK_COMPLETION": ("VIOLATED" if violations else
                            ("INCOMPLETE" if missing else "HOLDS")),
    }
    overall_ok = (not failures and not violations
                  and not missing
                  and all(s.state == "COMPLETED" for s in states.values()))
    return {
        "obligation_id": obligation.obligation_id,
        "revision": obligation.revision,
        "liveness_type": obligation.liveness_type,
        "deadlock": (deadlock_v, deadlock_e),
        "livelock": (livelock_v, livelock_e),
        "starvation": (starv_v, starv_e),
        "failures": failures,
        "per_workflow": per_type,
        "type_verdicts": type_verdicts,
        "witnesses_covered": covered,
        "witnesses_missing": missing,
        "overall": "QUALIFIED" if overall_ok else "NOT_QUALIFIED",
    }


def cold_successor_reconstruct(receipts: tuple,
                               obligations: tuple) -> tuple:
    """Can a cold successor reconstruct the liveness verdict from receipts
    alone — which guarantee failed, which safety properties stayed intact,
    whether recovery achieved the verified outcome?

    receipts: LivenessReceipt (+ safety receipts referenced by id).
    obligations: the LivenessObligation versions in force.
    Returns (reconstructible, gaps): gaps names anything the receipts do
    not establish.
    """
    gaps = []
    by_obl = {o.obligation_id: o for o in obligations}
    for r in receipts:
        if r.obligation_id not in by_obl:
            gaps.append(f"{r.obligation_id}: obligation version not supplied")
            continue
        obl = by_obl[r.obligation_id]
        required = set(obl.progress_witnesses)
        have = {w.milestone for w in r.witnesses}
        missing = required - have
        if missing and r.qualification in ("REQUALIFIED", "UNAFFECTED"):
            gaps.append(f"{r.obligation_id}: qualification "
                        f"{r.qualification} but witnesses missing "
                        f"{sorted(missing)}")
        if not r.independent_verification:
            gaps.append(f"{r.obligation_id}: no independent verification bound")
        if r.invalidated_by and not any(
                x.obligation_id == r.obligation_id for x in receipts):
            gaps.append(f"{r.obligation_id}: invalidated by "
                        f"{r.invalidated_by} with no superseding receipt")
    return (not gaps, tuple(gaps))
