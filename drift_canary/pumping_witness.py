"""D62 / AER-LIVE-7: Minimal, Independently Verified Unbounded-Cycle Witnesses.

The pumping-witness integrity law: assert an unbounded debt upper bound ONLY
from a minimized entry-cycle-exit certificate — independently reachable entry,
positively debt-producing and arbitrarily repeatable cycle, valid exit after
every finite repetition. Minimization preserves every constraint the proof
depends on. A separate verifier reconstructs the certificate and keeps
model-level possibility distinct from actual violation or physical
realizability.

The gap it closes: D61's unbounded-debt engine exhibits a constructive
witness (the U*S language), but a short cycle is not proof of unboundedness.
Each part carries its own proof burden:

  entry  — reachable from the verified boundary (replayed, never trusted);
  cycle  — positively debt-producing AND arbitrarily repeatable: every
           traversal must repeat without exhausting anything (budgets,
           tokens, revisions, termination). The dangerous false witness is
           the cycle that can repeat only twice — a self-loop on the
           scheduler state that quietly consumes a finite recovery token
           each traversal. The verifier finds the minimal counterexample at
           the third repetition;
  exit   — reachable after EVERY finite repetition count (sampled and
           replayed, not assumed).

Full-state closure or it doesn't count. And the quantifiers stay separate:
an unbounded peak (for every bound, some history exceeds it) is NOT a proven
violation (every history breaches it). The witness can coexist with an
undetermined verdict, and must never become an unjustified starvation
accusation — the verdict answers UNRESOLVED even when the peak is proven
unbounded, and any attempt to upgrade the witness to a BREACH fails closed.

Minimization: the verifier accepts ONLY minimized certificates — every
cycle step debt-producing or resource-constraining (a zero-debt step that
carries resource costs is load-bearing for repeatability and is kept),
every entry step load-bearing, every resource claim consumed somewhere.
`minimize_certificate` produces the minimal form; a non-minimal
certificate is refused with the redundant part named, never silently
repaired.

The independent (cold) verifier reconstructs the certificate from its
serialized bytes alone and re-runs every check — the AER-LIVE-007 valid
witness keeps its unbounded peak and finite final debt, reproducible by a
cold verifier from the certificate alone.

AER-LIVE-007 fixtures (the case that makes it real):
  valid                — the real witness: reachable entry, debt-adding
                         token-free cycle, exit after every repetition;
  two_token_defect     — hidden two-token defect: the self-loop consumes one
                         finite recovery token per traversal. The naive
                         checker (which sees only the cycle shape) declares
                         unbounded; the real verifier rejects with the
                         minimal counterexample at the third repetition;
  mandatory_reset      — the cycle claims "no mandatory reset" but a reset
                         step sits inside it; rejected;
  unreachable_exit     — the exit is not reachable after some repetition
                         count; rejected.

SPEC + deterministic machinery. NOT wired into kernel/, KNOW, LAW, ACT, or
any live path. Composes with D61's unbounded-debt engine when both merge
(D61 not on main yet — shared verdict strings PROVEN_UNBOUNDED /
UNRESOLVED / BREACH / NO_BREACH; WITNESS_REJECTED is D62's own; no import
coupling). Wiring needs Shawn's word.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Vocabulary. Shared strings with the D58/D59/D60/D61 line
# (PROVEN_UNBOUNDED, UNRESOLVED, BREACH, NO_BREACH) so the directives
# compose when their PRs merge — no import coupling (none of them are on
# main yet). WITNESS_REJECTED is D62's own verdict string.
# ---------------------------------------------------------------------------
BREACH = "BREACH"
NO_BREACH = "NO_BREACH"
UNRESOLVED = "UNRESOLVED"

PROVEN_UNBOUNDED = "PROVEN_UNBOUNDED"
WITNESS_REJECTED = "WITNESS_REJECTED"


class PumpingWitnessError(Exception):
    """Base for fail-closed pumping-witness errors."""


class CertificateShapeError(PumpingWitnessError):
    """The certificate is malformed (empty cycle, inverted debts,
    unknown step, missing assumptions)."""


class EntryUnreachableError(PumpingWitnessError):
    """The entry path cannot be replayed from the verified boundary —
    the entry is not independently reachable."""


class CycleNotDebtProducingError(PumpingWitnessError):
    """A cycle traversal does not strictly increase debt — a short cycle
    is not proof of unboundedness."""


class CycleNotRepeatableError(PumpingWitnessError):
    """The cycle exhausts a finite resource. Carries the minimal
    counterexample: the first repetition that cannot complete."""


class MandatoryResetError(PumpingWitnessError):
    """A mandatory reset sits inside the claimed reset-free cycle."""


class ExitUnreachableError(PumpingWitnessError):
    """The exit is not reachable after some finite repetition count."""


class NonMinimalCertificateError(PumpingWitnessError):
    """The certificate is not minimized — minimization would drop a
    redundant part. Refused with the redundant part named."""


class StarvationAccusationError(PumpingWitnessError):
    """A pumping witness was used as a starvation accusation: an unbounded
    peak (for every bound, some history exceeds it) was presented as a
    proven violation (every history breaches it). The quantifiers stay
    separate — this is always refused."""


class CertificateSerializationError(PumpingWitnessError):
    """Serialized certificate bytes are malformed — the cold verifier
    fails closed, never guesses."""


# ---------------------------------------------------------------------------
# The certificate.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class PumpingStep:
    """One labeled transition-system step.

    debt_delta: debt added by this step (must be > 0 for cycle steps —
    a short cycle is not proof of unboundedness).
    clears_debt: when True the step clears the debt counter to 0 — the
    valid exit terminates the language and clears the counter, not the
    history (mirrors D61's S step).
    resource_costs: ((resource, per_step_cost), ...) — consumed each time
    the step runs. The two-token defect lives here: a self-loop with
    cost 1 on a finite recovery-token supply repeats only twice.
    is_mandatory_reset: a forced reset — forbidden inside the cycle.
    """
    name: str
    debt_delta: int
    resource_costs: tuple = field(default_factory=tuple)
    clears_debt: bool = False
    is_mandatory_reset: bool = False

    def __post_init__(self):
        if not self.name:
            raise CertificateShapeError("a step needs a name")
        if not isinstance(self.debt_delta, int) or isinstance(self.debt_delta, bool):
            raise CertificateShapeError(
                f"debt_delta must be an int, got {self.debt_delta!r}")
        for pair in self.resource_costs:
            res, cost = pair
            if not res or not isinstance(cost, int) or isinstance(cost, bool) \
                    or cost < 0:
                raise CertificateShapeError(
                    f"bad resource cost {pair!r} on step {self.name!r}")


@dataclass(frozen=True)
class PumpingWitnessCertificate:
    """The minimized entry-cycle-exit certificate.

    boundary_ref: the named verified boundary the entry is replayed from
    (e.g. "ledger@verified-rev"). Replayed, never trusted.
    entry_debt: debt at the verified boundary.
    entry_path: steps from the boundary to the cycle entry.
    cycle: the debt-producing cycle — non-empty.
    exit_path: steps from the cycle state to a terminal finite-debt state.
    initial_resources: ((resource, supply), ...) available at entry.
    model_assumptions: the named assumptions the unbounded upper rests on.
    """
    obligation_id: str
    boundary_ref: str
    entry_debt: int
    entry_path: tuple
    cycle: tuple
    exit_path: tuple
    initial_resources: tuple = field(default_factory=tuple)
    model_assumptions: tuple = field(default_factory=tuple)

    def __post_init__(self):
        if not self.obligation_id:
            raise CertificateShapeError("certificate needs an obligation id")
        if not self.boundary_ref:
            raise CertificateShapeError("certificate needs a named verified boundary")
        if not isinstance(self.entry_debt, int) or isinstance(self.entry_debt, bool) \
                or self.entry_debt < 0:
            raise CertificateShapeError(
                f"entry_debt must be a non-negative int, got {self.entry_debt!r}")
        if not self.cycle:
            raise CertificateShapeError("the cycle must be non-empty")
        if not self.exit_path:
            raise CertificateShapeError("the certificate needs a valid exit")
        if not self.model_assumptions:
            raise CertificateShapeError(
                "unbounded uppers rest on stated assumptions — none named")
        for res, supply in self.initial_resources:
            if not res or not isinstance(supply, int) or isinstance(supply, bool) \
                    or supply < 0:
                raise CertificateShapeError(
                    f"bad resource supply {(res, supply)!r}")


# Sampled repetition counts at which the exit must stay reachable.
_EXIT_SAMPLE_KS = (0, 1, 2, 3, 5, 8, 13, 64, 1000)

_MODEL_ASSUMPTIONS = (
    "The cycle is modeled as a closed labeled transition system: each "
    "traversal starts and ends in the same scheduler state, adds a fixed "
    "positive debt delta, and consumes a fixed per-traversal resource cost. "
    "Full-state closure or it doesn't count.",
    "Resource supplies are finite; a resource absent from "
    "initial_resources has zero supply — any positive per-traversal cost "
    "on it fails at the first repetition. Any positive per-traversal cost "
    "on a finite supply bounds the repetitions — the minimal counterexample "
    "names the first repetition that cannot complete.",
    "Every history constructed here is a defensible hypothesis WITHIN THESE "
    "ASSUMPTIONS for bound computation — never an asserted fact, never a "
    "starvation accusation. Model-level possibility is kept distinct from "
    "actual violation and physical realizability.",
)


# ---------------------------------------------------------------------------
# Replay machinery. The replay — not the receipt — is the authority.
# ---------------------------------------------------------------------------
def _resources_dict(pairs: tuple) -> dict:
    out: dict = {}
    for res, amount in pairs:
        out[res] = out.get(res, 0) + amount
    return out


def _replay_path_tracked(debt: int, resources: dict, path: tuple) -> tuple[int, int, dict]:
    """Replay a path, tracking the maximum debt attained. Returns
    (final_debt, peak_debt, remaining_resources).

    Fail-closed: a mandatory reset inside a replayed path, or a resource
    cost the supply cannot cover, raises — the path is not traversable.
    """
    resources = dict(resources)
    peak = debt
    for step in path:
        if step.is_mandatory_reset:
            raise MandatoryResetError(
                f"mandatory reset inside replayed path at step {step.name!r}")
        for res, cost in step.resource_costs:
            have = resources.get(res, 0)
            if cost > have:
                raise CycleNotRepeatableError(
                    f"step {step.name!r} needs {cost} {res}, only {have} "
                    f"available — path not traversable")
            resources[res] = have - cost
        if step.clears_debt:
            debt = 0
        else:
            debt = debt + step.debt_delta
        if debt < 0:
            raise CertificateShapeError(
                f"step {step.name!r} drove debt negative — not a debt model")
        if debt > peak:
            peak = debt
    return debt, peak, resources


def _replay_path(debt: int, resources: dict, path: tuple) -> tuple[int, dict]:
    """Replay a path. Returns (final_debt, remaining_resources).

    Fail-closed: a mandatory reset inside a replayed path, or a resource
    cost the supply cannot cover, raises — the path is not traversable.
    """
    final_debt, _, remaining = _replay_path_tracked(debt, resources, path)
    return final_debt, remaining


def _cycle_traversal_cost(cycle: tuple) -> dict:
    costs: dict = {}
    for step in cycle:
        for res, cost in step.resource_costs:
            costs[res] = costs.get(res, 0) + cost
    return costs


def _cycle_debt_gain(cycle: tuple) -> int:
    return sum(step.debt_delta for step in cycle)


# ---------------------------------------------------------------------------
# Minimization. Accepted certificates must be fixed points of this function:
# every cycle step debt-producing or resource-constraining, every entry step
# load-bearing, every resource claim consumed somewhere. Minimization
# preserves every constraint the proof depends on — it drops only redundant
# parts, and a certificate that minimizes to an empty cycle is defective,
# not minimal.
# ---------------------------------------------------------------------------
def minimize_certificate(cert: PumpingWitnessCertificate) -> PumpingWitnessCertificate:
    """Drop redundant parts: zero-debt cost-free cycle steps, identity
    entry steps, unconsumed resource claims. Minimization preserves every
    constraint the proof depends on — a zero-debt cycle step that carries
    resource costs is load-bearing for repeatability (dropping it would
    erase a fuel/token constraint and let a bounded cycle verify as
    unbounded), so it is kept. Minimization preserves defects — a
    mandatory-reset step is never dropped (it is a defect to be rejected,
    not redundancy to be repaired). Raises CertificateShapeError when no
    debt-producing step remains."""
    cycle = tuple(
        s for s in cert.cycle
        if s.debt_delta > 0 or s.is_mandatory_reset or s.resource_costs
    )
    if not cycle:
        raise CertificateShapeError(
            "minimization emptied the cycle: no debt-producing step — "
            "a short cycle is not proof of unboundedness")

    consumed: dict = {}
    for step in list(cert.entry_path) + list(cycle) + list(cert.exit_path):
        for res, cost in step.resource_costs:
            consumed[res] = consumed.get(res, 0) + cost
    resources = tuple(
        (res, supply) for res, supply in cert.initial_resources
        if res in consumed)

    entry: list = []
    for step in cert.entry_path:
        identity = (step.debt_delta == 0 and not step.resource_costs
                    and not step.clears_debt and not step.is_mandatory_reset)
        if not identity:
            entry.append(step)

    return PumpingWitnessCertificate(
        obligation_id=cert.obligation_id,
        boundary_ref=cert.boundary_ref,
        entry_debt=cert.entry_debt,
        entry_path=tuple(entry),
        cycle=cycle,
        exit_path=cert.exit_path,
        initial_resources=resources,
        model_assumptions=cert.model_assumptions,
    )


def is_minimal(cert: PumpingWitnessCertificate) -> tuple[bool, str]:
    """True when the certificate is a fixed point of minimization."""
    try:
        minimized = minimize_certificate(cert)
    except CertificateShapeError as e:
        return False, f"minimization fails: {e}"
    if minimized != cert:
        if len(minimized.cycle) != len(cert.cycle):
            return False, (f"cycle carries {len(cert.cycle) - len(minimized.cycle)} "
                           f"redundant (zero-debt, cost-free) step(s)")
        if len(minimized.entry_path) != len(cert.entry_path):
            return False, "entry_path carries identity step(s)"
        if len(minimized.initial_resources) != len(cert.initial_resources):
            return False, "initial_resources carries unconsumed claim(s)"
        return False, "certificate is not a minimization fixed point"
    return True, "minimized"


# ---------------------------------------------------------------------------
# The naive checker — the defective baseline from AER-LIVE-007. It sees the
# cycle shape (non-empty, positive debt per traversal) and declares
# unbounded, modeling neither resources, resets, nor the exit. The tests
# prove it wrong on the two-token fixture; the real verifier rejects.
# ---------------------------------------------------------------------------
def naive_unbounded_checker(cert: PumpingWitnessCertificate) -> str:
    """The defective checker: cycle shape only. Declares unbounded on the
    two-token fixture — this is the bug D62 exists to catch."""
    gain = _cycle_debt_gain(cert.cycle)
    if cert.cycle and gain > 0:
        return PROVEN_UNBOUNDED
    return WITNESS_REJECTED


# ---------------------------------------------------------------------------
# The verifier.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class PumpingWitnessVerdict:
    """What the certificate establishes — and what it does not.

    breach_verdict is ALWAYS UNRESOLVED: the pumping witness proves the
    unbounded peak (for every bound, some history exceeds it), never a
    proven violation (every history breaches it). It can coexist with an
    undetermined verdict and is never a starvation accusation.
    demonstrated carries sampled (repetitions, peak, final) triples —
    constructed and replayed, not trusted. peak is the maximum debt
    attained across the cycle traversals and the exit replay at that
    sample count.
    """
    obligation_id: str
    accepted: bool
    peak_status: str
    breach_verdict: str
    demonstrated: tuple
    failure: str | None
    model_assumptions: tuple
    certificate_fingerprint: str

    def __post_init__(self):
        assert self.peak_status in (PROVEN_UNBOUNDED, WITNESS_REJECTED), \
            self.peak_status
        assert self.breach_verdict == UNRESOLVED, \
            "the pumping witness never answers the breach question — quantifiers stay separate"
        if self.accepted:
            assert self.peak_status == PROVEN_UNBOUNDED
            assert self.failure is None
        else:
            assert self.peak_status == WITNESS_REJECTED
            assert self.failure, "a rejection names its minimal counterexample"


def _fingerprint(cert: PumpingWitnessCertificate) -> str:
    def step(s: PumpingStep) -> tuple:
        return (s.name, s.debt_delta, tuple(s.resource_costs),
                s.clears_debt, s.is_mandatory_reset)

    canonical = json.dumps({
        "obligation_id": cert.obligation_id,
        "boundary_ref": cert.boundary_ref,
        "entry_debt": cert.entry_debt,
        "entry_path": [step(s) for s in cert.entry_path],
        "cycle": [step(s) for s in cert.cycle],
        "exit_path": [step(s) for s in cert.exit_path],
        "initial_resources": list(cert.initial_resources),
        "model_assumptions": list(cert.model_assumptions),
    }, sort_keys=True)
    return hashlib.sha256(canonical.encode()).hexdigest()


def verify_pumping_witness(cert: PumpingWitnessCertificate) -> PumpingWitnessVerdict:
    """Independently verify the certificate. Every check is recomputed:

    1. minimized — the certificate must be a minimization fixed point;
    2. entry independently reachable — entry_path replayed from the named
       verified boundary;
    3. cycle positively debt-producing — every traversal strictly raises
       the peak, gain > 0;
    4. cycle arbitrarily repeatable — no finite resource is exhausted at any
       finite repetition; the first uncompletable repetition is the minimal
       counterexample;
    5. no mandatory reset inside the cycle;
    6. exit valid after every finite repetition — replayed at sampled
       counts, always terminating at finite final debt.

    On any failure the verdict is rejected with the minimal counterexample
    named. The breach verdict is UNRESOLVED either way.
    """
    fingerprint = _fingerprint(cert)
    assumptions = tuple(cert.model_assumptions) + _MODEL_ASSUMPTIONS

    def reject(reason: str) -> PumpingWitnessVerdict:
        return PumpingWitnessVerdict(
            obligation_id=cert.obligation_id,
            accepted=False,
            peak_status=WITNESS_REJECTED,
            breach_verdict=UNRESOLVED,
            demonstrated=(),
            failure=reason,
            model_assumptions=assumptions,
            certificate_fingerprint=fingerprint,
        )

    # 1. Minimized.
    minimal, why = is_minimal(cert)
    if not minimal:
        return reject(f"non-minimal certificate: {why} "
                      f"— assert only from minimized certificates")

    supplies = _resources_dict(cert.initial_resources)

    # 2. Entry independently reachable: replay from the verified boundary.
    try:
        entry_debt, after_entry = _replay_path(
            cert.entry_debt, supplies, cert.entry_path)
    except PumpingWitnessError as e:
        return reject(f"entry not independently reachable from "
                      f"{cert.boundary_ref!r}: {e}")

    # 3 + 5. Cycle: no mandatory reset, positively debt-producing.
    for step in cert.cycle:
        if step.is_mandatory_reset:
            return reject(f"mandatory reset inside the cycle at step "
                          f"{step.name!r} — the cycle is not reset-free")
    gain = _cycle_debt_gain(cert.cycle)
    if gain <= 0:
        return reject(f"cycle debt gain {gain} is not positive — a short "
                      f"cycle is not proof of unboundedness")

    # 4. Arbitrarily repeatable: no finite resource exhausted at any finite
    #    repetition. The first uncompletable repetition is the minimal
    #    counterexample. The cycle traverses on the resources remaining
    #    AFTER the entry path ran (after_entry) — not the pre-entry
    #    supplies, which overstate when the entry itself consumes.
    per_traversal = _cycle_traversal_cost(cert.cycle)
    for res, cost in sorted(per_traversal.items()):
        if cost > 0:
            supply = after_entry.get(res, 0)
            if supply < cost:
                first_failing = 1
            else:
                first_failing = supply // cost + 1
            return reject(
                f"cycle not arbitrarily repeatable: traversal "
                f"#{first_failing} exhausts {res} (supply {supply}, cost "
                f"{cost} per traversal) — minimal counterexample at "
                f"repetition {first_failing}")

    # 6. Exit valid after every finite repetition — replayed at sampled
    #    counts. The cycle consumes nothing (proven above), so the exit
    #    faces the same resources at every count; only the debt varies.
    #    demonstrated carries the TRUE peak: the maximum debt attained
    #    across the cycle traversals and the exit replay at that sample
    #    (an exit with positive-debt steps can push the peak above the
    #    pre-exit debt).
    demonstrated: list = []
    try:
        for k in _EXIT_SAMPLE_KS:
            debt_k = entry_debt + k * gain
            final_debt, peak_k, _ = _replay_path_tracked(
                debt_k, dict(after_entry), cert.exit_path)
            demonstrated.append((k, peak_k, final_debt))
    except PumpingWitnessError as e:
        return reject(f"exit not valid after every finite repetition: {e}")

    return PumpingWitnessVerdict(
        obligation_id=cert.obligation_id,
        accepted=True,
        peak_status=PROVEN_UNBOUNDED,
        breach_verdict=UNRESOLVED,
        demonstrated=tuple(demonstrated),
        failure=None,
        model_assumptions=assumptions,
        certificate_fingerprint=fingerprint,
    )


def upgrade_to_breach(verdict: PumpingWitnessVerdict):
    """Mechanical quantifier separation: a pumping witness can never be
    upgraded to a breach verdict. Always refused."""
    raise StarvationAccusationError(
        "refused: a pumping witness proves the unbounded peak (for every "
        "bound, some history exceeds it), not a proven violation (every "
        "history breaches it). The witness coexists with an undetermined "
        "verdict and is never a starvation accusation.")


# ---------------------------------------------------------------------------
# Cold verifier: reconstruct from serialized bytes alone.
# ---------------------------------------------------------------------------
def certificate_to_json(cert: PumpingWitnessCertificate) -> bytes:
    def step(s: PumpingStep) -> dict:
        return {"name": s.name, "debt_delta": s.debt_delta,
                "resource_costs": [list(p) for p in s.resource_costs],
                "clears_debt": s.clears_debt,
                "is_mandatory_reset": s.is_mandatory_reset}

    return json.dumps({
        "obligation_id": cert.obligation_id,
        "boundary_ref": cert.boundary_ref,
        "entry_debt": cert.entry_debt,
        "entry_path": [step(s) for s in cert.entry_path],
        "cycle": [step(s) for s in cert.cycle],
        "exit_path": [step(s) for s in cert.exit_path],
        "initial_resources": [list(p) for p in cert.initial_resources],
        "model_assumptions": list(cert.model_assumptions),
    }, sort_keys=True).encode()


def certificate_from_json(payload: bytes) -> PumpingWitnessCertificate:
    try:
        raw = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        raise CertificateSerializationError(
            f"certificate bytes are not valid JSON: {e}")

    def step(raw_step: dict) -> PumpingStep:
        if not isinstance(raw_step, dict):
            raise CertificateSerializationError("step is not an object")
        try:
            return PumpingStep(
                name=raw_step["name"],
                debt_delta=raw_step["debt_delta"],
                resource_costs=tuple(
                    tuple(p) for p in raw_step.get("resource_costs", [])),
                clears_debt=bool(raw_step.get("clears_debt", False)),
                is_mandatory_reset=bool(raw_step.get("is_mandatory_reset", False)),
            )
        except (KeyError, TypeError, CertificateShapeError) as e:
            raise CertificateSerializationError(f"bad step: {e}")

    try:
        return PumpingWitnessCertificate(
            obligation_id=raw["obligation_id"],
            boundary_ref=raw["boundary_ref"],
            entry_debt=raw["entry_debt"],
            entry_path=tuple(step(s) for s in raw.get("entry_path", [])),
            cycle=tuple(step(s) for s in raw.get("cycle", [])),
            exit_path=tuple(step(s) for s in raw.get("exit_path", [])),
            initial_resources=tuple(tuple(p) for p in raw.get("initial_resources", [])),
            model_assumptions=tuple(raw.get("model_assumptions", [])),
        )
    except (KeyError, TypeError, CertificateShapeError) as e:
        raise CertificateSerializationError(f"bad certificate: {e}")


def independent_verify(payload: bytes) -> PumpingWitnessVerdict:
    """The cold verifier: reconstruct the certificate from its bytes alone
    and re-run every check. Malformed bytes fail closed."""
    return verify_pumping_witness(certificate_from_json(payload))


# ---------------------------------------------------------------------------
# AER-LIVE-007 fixtures.
# ---------------------------------------------------------------------------
_ASSUMPTIONS_007 = (
    "AER-LIVE-007: the scheduler state is the cycle's fixed point; each "
    "unserved round adds exactly 1 debt; service clears the counter.",
)


def _u_step(costs=()) -> PumpingStep:
    return PumpingStep(name="U:unserved-round", debt_delta=1,
                       resource_costs=tuple(costs))


def _exit_step(extra_costs=()) -> PumpingStep:
    # The valid exit: terminates the language, clears the counter (not the
    # history) — mirrors D61's S step.
    return PumpingStep(name="S:service-round", debt_delta=0,
                       clears_debt=True,
                       resource_costs=tuple(extra_costs))


def fixtures_aer_live_007() -> dict:
    """The four AER-LIVE-007 certificates."""
    base = dict(
        obligation_id="aer-live-007",
        boundary_ref="ledger@verified-rev",
        entry_debt=2,
        entry_path=(_u_step(),),
        exit_path=(_exit_step(),),
        model_assumptions=_ASSUMPTIONS_007,
    )
    valid = PumpingWitnessCertificate(
        cycle=(_u_step(),),
        initial_resources=(),
        **base,
    )
    two_token = PumpingWitnessCertificate(
        cycle=(_u_step(costs=(("recovery_token", 1),)),),
        initial_resources=(("recovery_token", 2),),
        **base,
    )
    mandatory_reset = PumpingWitnessCertificate(
        cycle=(_u_step(),
               PumpingStep(name="R:mandatory-reset", debt_delta=0,
                           is_mandatory_reset=True)),
        initial_resources=(),
        **base,
    )
    # The exit needs one service_capacity, but none is supplied at any
    # repetition count — unreachable after every k, including k=0.
    unreachable_base = dict(base)
    unreachable_base["exit_path"] = (
        _exit_step(extra_costs=(("service_capacity", 1),)),)
    unreachable_exit = PumpingWitnessCertificate(
        cycle=(_u_step(),),
        initial_resources=(),
        **unreachable_base,
    )
    return {
        "valid": valid,
        "two_token_defect": two_token,
        "mandatory_reset_defect": mandatory_reset,
        "unreachable_exit_defect": unreachable_exit,
    }
