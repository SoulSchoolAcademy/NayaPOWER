"""D63 / AER-LIVE-8: Full-State Invariants for Repeatable Cycle Proofs.

Shawn's law (SN-0814, ratified 2026-10-10): repeatability requires an
inductive invariant over the FULL state — authority, budgets, resources,
time, lifecycle, evidence, obligations. Four proof obligations: entry,
invariant preservation, positive debt gain, exit availability.

The gap it closes: D62's pumping witness proves a cycle CAN repeat
unboundedly (debt grows, no finite resource exhausts). It says nothing
about whether the governance state survives the repetition. A cycle that
preserves debt but violates authority is not repeatable. D63 is the
full-state closure of D62's repeatability claim: the invariant covers
all seven components, and the verifier names the first violated
component at the exact repetition — the minimal counterexample.

Decisive CONTROL/TREATMENT pair (from the AER-LIVE-8 spec):
- CONTROL: finite retries exhaust -> reject repetition. A finite retry
  budget cannot support the arbitrary-repetition claim.
- TREATMENT: eligible waiting consumes no retry -> may remain repeatable.
  With retry_budget=None the retry constraint does not bind and the
  state invariant decides.

Repeatability is a model property of the certificate, never a production
authorization: the authorization verdict stays UNDETERMINED on every
verdict, and any attempt to upgrade a repeatability certificate to a
production authorization is refused.

SPEC + deterministic machinery. NOT wired into kernel/, KNOW, LAW, ACT,
or any live path. Wiring needs Shawn's word.
"""

import hashlib
import json
import math
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Vocabulary.
# ---------------------------------------------------------------------------
AUTHORITY = "authority_valid"
BUDGET = "budget_remaining"
RESOURCES = "resources_available"
TIME = "time_valid"
LIFECYCLE = "lifecycle_outstanding"
EVIDENCE = "evidence_intact"
OBLIGATION = "obligation_active"

# The seven components the invariant must cover.
_COMPONENTS = (
    AUTHORITY, BUDGET, RESOURCES, TIME, LIFECYCLE, EVIDENCE, OBLIGATION,
)

# Boolean components (budget is continuous and governed separately).
_BOOLEAN_COMPONENTS = (
    AUTHORITY, RESOURCES, TIME, LIFECYCLE, EVIDENCE, OBLIGATION,
)

REPEATABLE = "REPEATABLE"
NOT_REPEATABLE = "NOT_REPEATABLE"
UNDETERMINED = "UNDETERMINED"

# Sampled repetition counts at which the exit must stay available and the
# demonstration triples are replayed.
_SAMPLE_KS = (0, 1, 2, 3, 5, 8, 13, 64, 1000)


# ---------------------------------------------------------------------------
# Errors. Proof failures are verdicts, not exceptions; malformed
# certificates and misuse are exceptions — fail closed, never guess.
# ---------------------------------------------------------------------------
class FullStateRepeatabilityError(Exception):
    """Base for D63 machinery errors."""


class CertificateShapeError(FullStateRepeatabilityError):
    """The certificate is malformed — refused before any proof is attempted."""


class NonMinimalCertificateError(FullStateRepeatabilityError):
    """The certificate is not minimized — a no-op step pads the cycle.
    Refused with the redundant step named, never silently repaired."""


class ProductionAuthorizationError(FullStateRepeatabilityError):
    """A repeatability certificate was presented as a production
    authorization. Repeatability is a model property, not a live grant —
    this is always refused."""


class CertificateSerializationError(FullStateRepeatabilityError):
    """Serialized certificate bytes are malformed — the cold verifier
    fails closed, never guesses."""


def _is_num(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


# ---------------------------------------------------------------------------
# The state and the transition.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class FullState:
    """The full state the invariant must cover (spec order).

    budget_remaining must stay > 0 at every repetition; every boolean
    component must stay True. lifecycle_outstanding=True means the
    obligation's lifecycle is still open — a traversal that closes it
    breaks the invariant.
    """
    authority_valid: bool
    budget_remaining: float
    resources_available: bool
    time_valid: bool
    lifecycle_outstanding: bool
    evidence_intact: bool
    obligation_active: bool

    def __post_init__(self):
        for comp in _BOOLEAN_COMPONENTS:
            val = getattr(self, comp)
            if not isinstance(val, bool):
                raise CertificateShapeError(
                    f"{comp} must be a bool, got {val!r}")
        if not _is_num(self.budget_remaining):
            raise CertificateShapeError(
                f"budget_remaining must be a number, got "
                f"{self.budget_remaining!r}")

    def violated_components(self) -> tuple:
        """Names every component currently violating the invariant."""
        bad = []
        if not self.authority_valid:
            bad.append(AUTHORITY)
        if not self.budget_remaining > 0:
            bad.append(BUDGET)
        if not self.resources_available:
            bad.append(RESOURCES)
        if not self.time_valid:
            bad.append(TIME)
        if not self.lifecycle_outstanding:
            bad.append(LIFECYCLE)
        if not self.evidence_intact:
            bad.append(EVIDENCE)
        if not self.obligation_active:
            bad.append(OBLIGATION)
        return tuple(bad)


@dataclass(frozen=True)
class StateTransition:
    """One cycle step's effect on the full state.

    debt_gain: debt added per traversal by this step (>= 0; the
        per-traversal total across the cycle must be > 0).
    budget_cost: budget consumed per traversal by this step (>= 0).
    component_ttl: ((component, ttl), ...) — per-component time-to-live
        in traversals. After traversal t, the component holds iff
        t <= ttl. ttl=0 means broken from the first traversal. Components
        without a TTL entry persist indefinitely. BUDGET may not appear
        here — it is continuous and governed by budget_cost.
    """
    name: str
    debt_gain: float
    budget_cost: float = 0.0
    component_ttl: tuple = field(default_factory=tuple)

    def __post_init__(self):
        if not self.name:
            raise CertificateShapeError("a transition needs a name")
        if not _is_num(self.debt_gain) or self.debt_gain < 0:
            raise CertificateShapeError(
                f"debt_gain must be a non-negative number, got "
                f"{self.debt_gain!r}")
        if not _is_num(self.budget_cost) or self.budget_cost < 0:
            raise CertificateShapeError(
                f"budget_cost must be a non-negative number, got "
                f"{self.budget_cost!r}")
        seen = set()
        for pair in self.component_ttl:
            try:
                comp, ttl = pair
            except (TypeError, ValueError):
                raise CertificateShapeError(
                    f"bad component_ttl entry {pair!r} on step "
                    f"{self.name!r}")
            if comp == BUDGET:
                raise CertificateShapeError(
                    f"budget is continuous — govern it with budget_cost, "
                    f"not component_ttl (step {self.name!r})")
            if comp not in _BOOLEAN_COMPONENTS:
                raise CertificateShapeError(
                    f"unknown component {comp!r} on step {self.name!r}")
            if not isinstance(ttl, int) or isinstance(ttl, bool) or ttl < 0:
                raise CertificateShapeError(
                    f"ttl must be a non-negative int, got {ttl!r} on step "
                    f"{self.name!r}")
            if comp in seen:
                raise CertificateShapeError(
                    f"duplicate ttl for {comp!r} on step {self.name!r}")
            seen.add(comp)

    def is_noop(self) -> bool:
        """A pure no-op: no debt, no cost, no state effect. Minimization
        drops these; everything else is load-bearing."""
        return (self.debt_gain == 0 and self.budget_cost == 0
                and not self.component_ttl)


# ---------------------------------------------------------------------------
# The certificate.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class RepeatabilityCertificate:
    """The full-state repeatability certificate.

    boundary_ref: the named verified boundary the entry state is replayed
        from. Replayed, never trusted.
    entry_state: the full state at repetition 0.
    entry_established: proof obligation 1 — valid entry to the invariant.
    cycle: the repeated traversal — non-empty tuple of StateTransition.
        One traversal applies every step; per-traversal totals govern.
    exit_requires: boolean components the exit precondition needs
        (e.g. authority + evidence for a clean shutdown/audit). Non-empty.
    exit_cost: budget the exit itself consumes. The exit is available at
        repetition k only if the invariant holds at k AND the remaining
        budget covers the exit.
    retry_budget: None = eligible waiting (TREATMENT — the retry
        constraint does not bind); int >= 0 = finite retries (CONTROL —
        the arbitrary-repetition claim is rejected, retries exhaust at
        repetition retry_budget + 1).
    model_assumptions: the named assumptions the repeatability claim
        rests on. Never empty.
    """
    obligation_id: str
    boundary_ref: str
    entry_state: FullState
    entry_established: bool
    cycle: tuple
    exit_requires: tuple
    exit_cost: float
    retry_budget: int | None
    model_assumptions: tuple = field(default_factory=tuple)

    def __post_init__(self):
        if not self.obligation_id:
            raise CertificateShapeError("certificate needs an obligation id")
        if not self.boundary_ref:
            raise CertificateShapeError(
                "certificate needs a named verified boundary")
        if not isinstance(self.entry_state, FullState):
            raise CertificateShapeError("entry_state must be a FullState")
        if not isinstance(self.entry_established, bool):
            raise CertificateShapeError("entry_established must be a bool")
        if not self.cycle or not isinstance(self.cycle, tuple):
            raise CertificateShapeError("the cycle must be a non-empty tuple")
        for step in self.cycle:
            if not isinstance(step, StateTransition):
                raise CertificateShapeError(
                    f"cycle step {step!r} is not a StateTransition")
        if not self.exit_requires or not isinstance(self.exit_requires, tuple):
            raise CertificateShapeError(
                "exit_requires must be a non-empty tuple")
        for comp in self.exit_requires:
            if comp == BUDGET:
                raise CertificateShapeError(
                    "budget is governed by exit_cost, not exit_requires")
            if comp not in _BOOLEAN_COMPONENTS:
                raise CertificateShapeError(
                    f"unknown exit component {comp!r}")
        if not _is_num(self.exit_cost) or self.exit_cost < 0:
            raise CertificateShapeError(
                f"exit_cost must be a non-negative number, got "
                f"{self.exit_cost!r}")
        rb = self.retry_budget
        if rb is not None and (
                not isinstance(rb, int) or isinstance(rb, bool) or rb < 0):
            raise CertificateShapeError(
                f"retry_budget must be None or a non-negative int, got "
                f"{rb!r}")
        if not self.model_assumptions:
            raise CertificateShapeError(
                "repeatability claims rest on stated assumptions — none named")


_MODEL_ASSUMPTIONS = (
    "Each traversal is a closed transition on the full state: fixed debt "
    "gain, fixed budget cost, fixed per-component TTLs. The same scheduler "
    "state recurs every traversal. Full-state closure or it doesn't count.",
    "A finite retry budget cannot support the arbitrary-repetition claim: "
    "CONTROL rejects repetition when retries exhaust. Only eligible "
    "waiting (retry_budget=None) may remain repeatable: TREATMENT.",
    "Every history constructed here is a defensible hypothesis WITHIN "
    "THESE ASSUMPTIONS for repeatability analysis — never an asserted "
    "fact, never a production authorization. Model-level repeatability is "
    "kept distinct from live authority to repeat.",
)

# ---------------------------------------------------------------------------
# Per-traversal aggregates. One traversal applies every cycle step; the
# closed-transition model means the same totals recur every traversal.
# Duplicate TTLs for one component merge to the strictest (minimum).
# ---------------------------------------------------------------------------
def _cycle_totals(cycle: tuple) -> tuple:
    """Returns (debt_gain, budget_cost, ttls) per traversal."""
    gain = 0.0
    cost = 0.0
    ttls: dict = {}
    for step in cycle:
        gain += step.debt_gain
        cost += step.budget_cost
        for comp, ttl in step.component_ttl:
            if comp in ttls:
                ttls[comp] = min(ttls[comp], ttl)
            else:
                ttls[comp] = ttl
    return gain, cost, ttls


def _cycle_debt_gain(cycle: tuple) -> float:
    return _cycle_totals(cycle)[0]


def _state_after(entry: FullState, totals: tuple, k: int) -> FullState:
    """The full state after k traversals. Deterministic replay of the
    closed transition — constructed, not trusted."""
    gain, cost, ttls = totals
    budget = entry.budget_remaining - k * cost

    def holds(comp: str, entry_val: bool) -> bool:
        if comp == BUDGET:
            return budget > 0
        ttl = ttls.get(comp)
        if ttl is not None:
            return k <= ttl
        return entry_val

    return FullState(
        authority_valid=holds(AUTHORITY, entry.authority_valid),
        budget_remaining=budget,
        resources_available=holds(RESOURCES, entry.resources_available),
        time_valid=holds(TIME, entry.time_valid),
        lifecycle_outstanding=holds(LIFECYCLE, entry.lifecycle_outstanding),
        evidence_intact=holds(EVIDENCE, entry.evidence_intact),
        obligation_active=holds(OBLIGATION, entry.obligation_active),
    )


def _first_break(entry: FullState, totals: tuple) -> tuple | None:
    """The minimal counterexample: (component, repetition) of the first
    invariant violation, computed exactly. None when the invariant holds
    for arbitrarily many repetitions.

    Budget: smallest t >= 1 with B0 - t*cost <= 0, i.e. ceil(B0 / cost).
    TTL: component with ttl breaks at repetition ttl + 1.
    """
    gain, cost, ttls = totals
    candidates: list = []
    if cost > 0:
        t_break = math.ceil(entry.budget_remaining / cost)
        if t_break < 1:
            t_break = 1
        candidates.append((BUDGET, t_break))
    for comp, ttl in ttls.items():
        candidates.append((comp, ttl + 1))
    if not candidates:
        return None
    candidates.sort(key=lambda c: (c[1], c[0]))
    return candidates[0]


# ---------------------------------------------------------------------------
# Minimization. Accepted certificates must be fixed points: every cycle
# step is load-bearing (debt, cost, or state effect). Pure no-ops are
# refused with the redundant step named, never silently repaired.
# Minimization preserves defects — a TTL-bearing step is load-bearing
# even with zero debt gain.
# ---------------------------------------------------------------------------
def minimize_certificate(
        cert: RepeatabilityCertificate) -> RepeatabilityCertificate:
    """Drop pure no-op steps. Raises CertificateShapeError only on a
    degenerate cycle; a cycle that minimizes to empty is defective."""
    cycle = tuple(s for s in cert.cycle if not s.is_noop())
    if not cycle:
        raise CertificateShapeError(
            "minimization emptied the cycle: no load-bearing step — "
            "a padded cycle proves nothing")
    return RepeatabilityCertificate(
        obligation_id=cert.obligation_id,
        boundary_ref=cert.boundary_ref,
        entry_state=cert.entry_state,
        entry_established=cert.entry_established,
        cycle=cycle,
        exit_requires=cert.exit_requires,
        exit_cost=cert.exit_cost,
        retry_budget=cert.retry_budget,
        model_assumptions=cert.model_assumptions,
    )


def is_minimal(cert: RepeatabilityCertificate) -> tuple:
    """True when the certificate is a fixed point of minimization."""
    try:
        minimized = minimize_certificate(cert)
    except CertificateShapeError as e:
        return False, f"minimization fails: {e}"
    if minimized != cert:
        dropped = len(cert.cycle) - len(minimized.cycle)
        return False, (f"cycle carries {dropped} no-op step(s) — "
                       f"assert only from minimized certificates")
    return True, "minimized"


# ---------------------------------------------------------------------------
# The naive checker — the defective baseline. It sees positive debt gain
# and declares repeatable, modeling neither the other six components,
# the budget, TTLs, retries, nor the exit. The tests prove it wrong on
# the authority-expiry and budget-drain fixtures; the real verifier
# rejects both with the minimal counterexample named.
# ---------------------------------------------------------------------------
def naive_repeatability_checker(cert: RepeatabilityCertificate) -> str:
    """The defective checker: debt gain only. Declares the
    authority-expiry and budget-drain fixtures repeatable — this is the
    bug D63 exists to catch."""
    if _cycle_debt_gain(cert.cycle) > 0:
        return REPEATABLE
    return NOT_REPEATABLE


# ---------------------------------------------------------------------------
# The verifier.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class RepeatabilityVerdict:
    """What the certificate establishes — and what it does not.

    authorization is ALWAYS UNDETERMINED: the certificate proves the
    invariant holds across repetitions (a model property), never a live
    grant to repeat in production. verified_up_to is None for arbitrary
    (unbounded) repeatability, else the last verified repetition.
    demonstrated carries replayed (repetition, cumulative_debt_gain,
    budget_remaining) triples — constructed, not trusted.
    """
    obligation_id: str
    accepted: bool
    repeatability: str
    verified_up_to: int | None
    authorization: str
    demonstrated: tuple
    failure: str | None
    model_assumptions: tuple
    certificate_fingerprint: str

    def __post_init__(self):
        assert self.repeatability in (REPEATABLE, NOT_REPEATABLE), \
            self.repeatability
        assert self.authorization == UNDETERMINED, \
            "repeatability never answers the authorization question"
        if self.accepted:
            assert self.repeatability == REPEATABLE
            assert self.failure is None
        else:
            assert self.repeatability == NOT_REPEATABLE
            assert self.failure, "a rejection names its minimal counterexample"


def _fingerprint(cert: RepeatabilityCertificate) -> str:
    def step(s: StateTransition) -> tuple:
        return (s.name, s.debt_gain, s.budget_cost,
                tuple(s.component_ttl))

    def state(s: FullState) -> tuple:
        return (s.authority_valid, s.budget_remaining,
                s.resources_available, s.time_valid,
                s.lifecycle_outstanding, s.evidence_intact,
                s.obligation_active)

    canonical = json.dumps({
        "obligation_id": cert.obligation_id,
        "boundary_ref": cert.boundary_ref,
        "entry_state": state(cert.entry_state),
        "entry_established": cert.entry_established,
        "cycle": [step(s) for s in cert.cycle],
        "exit_requires": list(cert.exit_requires),
        "exit_cost": cert.exit_cost,
        "retry_budget": cert.retry_budget,
        "model_assumptions": list(cert.model_assumptions),
    }, sort_keys=True)
    return hashlib.sha256(canonical.encode()).hexdigest()


def verify_full_state_repeatability(
        cert: RepeatabilityCertificate) -> RepeatabilityVerdict:
    """Independently verify the certificate. Every check is recomputed:

    1. minimized — the certificate must be a minimization fixed point;
    2. entry — entry_established AND all seven components hold in the
       entry state (proof obligation 1);
    3. positive debt gain — per-traversal gain > 0; repetition without
       debt gain proves nothing (proof obligation 3);
    4. invariant preservation — the full state holds at every repetition;
       the first violated component at the exact repetition is the
       minimal counterexample (proof obligation 2);
    5. exit available — at every sampled finite repetition the exit
       precondition holds and the remaining budget covers the exit
       cost (proof obligation 4);
    6. CONTROL/TREATMENT — the decisive pair: a finite retry budget
       rejects the arbitrary-repetition claim (retries exhaust at
       repetition retry_budget + 1); eligible waiting (None) leaves the
       retry constraint unbound.

    On any failure the verdict is rejected with the minimal
    counterexample named. The authorization verdict is UNDETERMINED
    either way — repeatability is never a production authorization.
    """
    fingerprint = _fingerprint(cert)
    assumptions = tuple(cert.model_assumptions) + _MODEL_ASSUMPTIONS
    totals = _cycle_totals(cert.cycle)
    gain, cost, ttls = totals

    def reject(reason: str) -> RepeatabilityVerdict:
        return RepeatabilityVerdict(
            obligation_id=cert.obligation_id,
            accepted=False,
            repeatability=NOT_REPEATABLE,
            verified_up_to=None,
            authorization=UNDETERMINED,
            demonstrated=(),
            failure=reason,
            model_assumptions=assumptions,
            certificate_fingerprint=fingerprint,
        )

    # 1. Minimized.
    minimal, why = is_minimal(cert)
    if not minimal:
        return reject(f"non-minimal certificate: {why}")

    # 2. Entry: established, and the full invariant holds at repetition 0.
    if not cert.entry_established:
        return reject("entry not established — proof obligation 1 fails: "
                      "no valid entry to the invariant")
    entry_bad = cert.entry_state.violated_components()
    if entry_bad:
        return reject(f"entry violates the invariant at repetition 0: "
                      f"{', '.join(entry_bad)} — proof obligation 1 fails")

    # 3. Positive debt gain per traversal — repetition without debt
    #    gain proves nothing; checked before preservation (cheap, local).
    if gain <= 0:
        return reject(f"cycle debt gain {gain} is not positive — proof "
                      f"obligation 3 fails: repetition without debt gain "
                      f"proves nothing")

    # 4. Invariant preservation: the minimal counterexample is exact.
    broken = _first_break(cert.entry_state, totals)
    if broken is not None:
        comp, rep = broken
        return reject(
            f"invariant breaks at repetition {rep}: {comp} — a cycle "
            f"that preserves debt but violates {comp} is not repeatable "
            f"(proof obligation 2 fails)")
    verified_up_to = None  # arbitrary — no finite break exists

    # 5. Exit available after every finite repetition — precondition
    #    components hold and the remaining budget covers the exit cost.
    #    Sampled counts, replayed; the invariant already holds at each
    #    (proven above), so only the exit's own terms are checked here.
    demonstrated: list = []
    try:
        for k in _SAMPLE_KS:
            st = _state_after(cert.entry_state, totals, k)
            for comp in cert.exit_requires:
                if comp in st.violated_components():
                    return reject(
                        f"exit not available after repetition {k}: "
                        f"exit requires {comp}, invariant broken — proof "
                        f"obligation 4 fails")
            if not st.budget_remaining > cert.exit_cost:
                return reject(
                    f"exit not available after repetition {k}: needs "
                    f"budget > {cert.exit_cost}, has "
                    f"{st.budget_remaining} — proof obligation 4 fails")
            demonstrated.append(
                (k, k * gain, st.budget_remaining))
    except FullStateRepeatabilityError as e:
        return reject(f"exit check failed: {e}")

    # 6. CONTROL/TREATMENT — the decisive pair.
    if cert.retry_budget is not None:
        rb = cert.retry_budget
        return reject(
            f"CONTROL: finite retries ({rb}) exhaust at repetition "
            f"{rb + 1} — reject repetition. Only eligible waiting "
            f"(retry_budget=None) may remain repeatable (TREATMENT)")

    return RepeatabilityVerdict(
        obligation_id=cert.obligation_id,
        accepted=True,
        repeatability=REPEATABLE,
        verified_up_to=verified_up_to,
        authorization=UNDETERMINED,
        demonstrated=tuple(demonstrated),
        failure=None,
        model_assumptions=assumptions,
        certificate_fingerprint=fingerprint,
    )


def upgrade_to_authorization(verdict: RepeatabilityVerdict):
    """Mechanical separation: a repeatability certificate proves the
    invariant holds across repetitions — it never authorizes production
    repetition. Always refused."""
    raise ProductionAuthorizationError(
        "refused: repeatability is a model property of the certificate "
        "(the invariant holds across repetitions), not a live grant to "
        "repeat in production. Production repetition needs a live "
        "authority grant; this certificate is never that grant.")

# ---------------------------------------------------------------------------
# Cold verifier: reconstruct from serialized bytes alone.
# ---------------------------------------------------------------------------
def certificate_to_json(cert: RepeatabilityCertificate) -> bytes:
    def step(s: StateTransition) -> dict:
        return {"name": s.name, "debt_gain": s.debt_gain,
                "budget_cost": s.budget_cost,
                "component_ttl": [list(p) for p in s.component_ttl]}

    def state(s: FullState) -> dict:
        return {"authority_valid": s.authority_valid,
                "budget_remaining": s.budget_remaining,
                "resources_available": s.resources_available,
                "time_valid": s.time_valid,
                "lifecycle_outstanding": s.lifecycle_outstanding,
                "evidence_intact": s.evidence_intact,
                "obligation_active": s.obligation_active}

    return json.dumps({
        "obligation_id": cert.obligation_id,
        "boundary_ref": cert.boundary_ref,
        "entry_state": state(cert.entry_state),
        "entry_established": cert.entry_established,
        "cycle": [step(s) for s in cert.cycle],
        "exit_requires": list(cert.exit_requires),
        "exit_cost": cert.exit_cost,
        "retry_budget": cert.retry_budget,
        "model_assumptions": list(cert.model_assumptions),
    }, sort_keys=True).encode()


def certificate_from_json(payload: bytes) -> RepeatabilityCertificate:
    try:
        raw = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        raise CertificateSerializationError(
            f"certificate bytes are not valid JSON: {e}")

    def step(raw_step: dict) -> StateTransition:
        if not isinstance(raw_step, dict):
            raise CertificateSerializationError("step is not an object")
        try:
            return StateTransition(
                name=raw_step["name"],
                debt_gain=raw_step["debt_gain"],
                budget_cost=raw_step.get("budget_cost", 0.0),
                component_ttl=tuple(
                    tuple(p) for p in raw_step.get("component_ttl", [])),
            )
        except (KeyError, TypeError, CertificateShapeError) as e:
            raise CertificateSerializationError(f"bad step: {e}")

    def state(raw_state: dict) -> FullState:
        if not isinstance(raw_state, dict):
            raise CertificateSerializationError("entry_state is not an object")
        try:
            return FullState(
                authority_valid=bool(raw_state["authority_valid"]),
                budget_remaining=raw_state["budget_remaining"],
                resources_available=bool(raw_state["resources_available"]),
                time_valid=bool(raw_state["time_valid"]),
                lifecycle_outstanding=bool(
                    raw_state["lifecycle_outstanding"]),
                evidence_intact=bool(raw_state["evidence_intact"]),
                obligation_active=bool(raw_state["obligation_active"]),
            )
        except (KeyError, TypeError, CertificateShapeError) as e:
            raise CertificateSerializationError(f"bad entry_state: {e}")

    try:
        return RepeatabilityCertificate(
            obligation_id=raw["obligation_id"],
            boundary_ref=raw["boundary_ref"],
            entry_state=state(raw["entry_state"]),
            entry_established=bool(raw["entry_established"]),
            cycle=tuple(step(s) for s in raw["cycle"]),
            exit_requires=tuple(raw["exit_requires"]),
            exit_cost=raw["exit_cost"],
            retry_budget=raw["retry_budget"],
            model_assumptions=tuple(raw.get("model_assumptions", [])),
        )
    except (KeyError, TypeError, CertificateShapeError) as e:
        raise CertificateSerializationError(f"bad certificate: {e}")


def independent_verify(payload: bytes) -> RepeatabilityVerdict:
    """The cold verifier: reconstruct the certificate from its bytes alone
    and re-run every check. Malformed bytes fail closed."""
    return verify_full_state_repeatability(certificate_from_json(payload))


# ---------------------------------------------------------------------------
# AER-LIVE-008 fixtures — the cases that make D63 real.
# ---------------------------------------------------------------------------
_ASSUMPTIONS_008 = (
    "AER-LIVE-008: each unserved round adds exactly 1 debt at zero budget "
    "cost; the authority token expires after 50 traversals unless renewed; "
    "the exit (audit/shutdown) needs valid authority, intact evidence, "
    "and budget covering the exit cost.",
)


def _good_entry(budget: float = 100.0) -> FullState:
    return FullState(
        authority_valid=True,
        budget_remaining=budget,
        resources_available=True,
        time_valid=True,
        lifecycle_outstanding=True,
        evidence_intact=True,
        obligation_active=True,
    )


def _serve_step(**kw) -> StateTransition:
    params = dict(name="U:unserved-round", debt_gain=1.0)
    params.update(kw)
    return StateTransition(**params)


def fixtures_aer_live_008() -> dict:
    """The seven AER-LIVE-008 certificates."""
    base = dict(
        obligation_id="aer-live-008",
        boundary_ref="ledger@verified-rev",
        entry_state=_good_entry(),
        entry_established=True,
        exit_requires=(AUTHORITY, EVIDENCE),
        exit_cost=10.0,
        retry_budget=None,  # TREATMENT: eligible waiting
        model_assumptions=_ASSUMPTIONS_008,
    )
    valid = RepeatabilityCertificate(
        cycle=(_serve_step(),),
        **base,
    )
    # Debt-positive, but the authority token expires after 50 traversals.
    # The naive debt-only checker declares it repeatable — the bug D63
    # exists to catch. Minimal counterexample at repetition 51.
    authority_expiry = RepeatabilityCertificate(
        cycle=(_serve_step(component_ttl=((AUTHORITY, 50),)),),
        **base,
    )
    # Debt-positive, but each traversal costs 5 budget from 100.
    # Breaks at repetition 20 (100 - 20*5 = 0, not > 0).
    budget_drain = RepeatabilityCertificate(
        cycle=(_serve_step(budget_cost=5.0),),
        **base,
    )
    # No positive debt gain — proof obligation 3 fails outright. The step
    # still costs budget, so it survives minimization as load-bearing and
    # reaches the debt-gain check (work without progress).
    zero_gain = RepeatabilityCertificate(
        cycle=(_serve_step(debt_gain=0.0, budget_cost=1.0),),
        **base,
    )
    # CONTROL: 3 finite retries cannot support the arbitrary-repetition
    # claim — retries exhaust at repetition 4.
    finite_retries = RepeatabilityCertificate(
        cycle=(_serve_step(),),
        retry_budget=3,
        **{k: v for k, v in base.items() if k != "retry_budget"},
    )
    # Entry violates the invariant — proof obligation 1 fails at
    # repetition 0.
    broken_entry = RepeatabilityCertificate(
        entry_state=FullState(
            authority_valid=False,
            budget_remaining=100.0,
            resources_available=True,
            time_valid=True,
            lifecycle_outstanding=True,
            evidence_intact=True,
            obligation_active=True,
        ),
        cycle=(_serve_step(),),
        **{k: v for k, v in base.items() if k != "entry_state"},
    )
    # The invariant holds arbitrarily, but the exit itself costs 150
    # against a 100 budget — never affordable. Proof obligation 4 fails
    # independently of preservation.
    unaffordable_exit = RepeatabilityCertificate(
        cycle=(_serve_step(),),
        exit_cost=150.0,
        **{k: v for k, v in base.items() if k != "exit_cost"},
    )
    return {
        "valid": valid,
        "authority_expiry_defect": authority_expiry,
        "budget_drain_defect": budget_drain,
        "zero_gain_defect": zero_gain,
        "finite_retries_defect": finite_retries,
        "broken_entry_defect": broken_entry,
        "unaffordable_exit_defect": unaffordable_exit,
    }
