"""D42 — Verification Under Missing Commit Evidence (RFD-AMB-1).

THE JOB: represent an incomplete execution history as a SET of possible
histories, preserving both compliant and violating explanations until
admissible evidence distinguishes them.

CORE LAW (Ambiguous History Integrity Law): when incomplete observations
admit both legal and violating executions, NayaNET must preserve both
possibilities, withhold definitive certification or blame, identify the
missing discriminating evidence, and prohibit dependent consequential use
of the unresolved proof. New admissible evidence may narrow the
possibilities — but missing evidence may never be silently treated as
proof of success, failure, or nonexecution. Possible compliance is not
verified compliance; possible violation is not a proven violation.

HARD REFUSALS (never invent facts):
  - a timeout does not prove rollback;
  - an acknowledgment does not prove an effect;
  - a missing receipt does not prove absence (outside covered scope).

This is a fixture-scale verifier: histories are enumerated explicitly over
a finite fact space with a hard cap. If the space exceeds the cap the
engine returns INSUFFICIENT_MODEL_OR_OBSERVABILITY instead of silently
sampling. It is NOT a production trace analyzer.

Composes with D31 (drift_canary.d31_incident): the incident verdict keeps
the four uncertainty dimensions; this engine keeps the possible histories.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Verdict vocabulary (fixed strings — asserted identical wherever imported)
# ---------------------------------------------------------------------------

SAFETY_ESTABLISHED_IN_SCOPE = "SAFETY_ESTABLISHED_IN_SCOPE"
VIOLATION_ESTABLISHED = "VIOLATION_ESTABLISHED"
AMBIGUOUS_BOTH_POSSIBLE = "AMBIGUOUS_BOTH_POSSIBLE"
INSUFFICIENT_MODEL_OR_OBSERVABILITY = "INSUFFICIENT_MODEL_OR_OBSERVABILITY"
INCONSISTENT_OBSERVATIONS_OR_MODEL = "INCONSISTENT_OBSERVATIONS_OR_MODEL"

VERDICTS = (
    SAFETY_ESTABLISHED_IN_SCOPE,
    VIOLATION_ESTABLISHED,
    AMBIGUOUS_BOTH_POSSIBLE,
    INSUFFICIENT_MODEL_OR_OBSERVABILITY,
    INCONSISTENT_OBSERVATIONS_OR_MODEL,
)

# Per-operation outcome sets (D42 mechanics)
COMMITTED = "COMMITTED"
ABORTED = "ABORTED"
NOT_EXECUTED = "NOT_EXECUTED"
UNRESOLVED = "UNRESOLVED"

OUTCOMES = (COMMITTED, ABORTED, NOT_EXECUTED, UNRESOLVED)

# Forbidden-inference codes
TIMEOUT_PROVES_NOTHING = "TIMEOUT_PROVES_NOTHING"
ACK_PROVES_NO_EFFECT = "ACK_PROVES_NO_EFFECT"
ABSENCE_PROVES_NOTHING_OUTSIDE_COVERAGE = "ABSENCE_PROVES_NOTHING_OUTSIDE_COVERAGE"

MAX_HISTORIES = 100_000


class InventedFactError(Exception):
    """Raised when code tries to derive a fact from a non-fact."""


class InconsistentEvidenceError(Exception):
    """Raised when new evidence contradicts every possible history."""


# ---------------------------------------------------------------------------
# History: one concrete possible world.
# A history is an immutable mapping fact_name -> value, plus the scenario
# that defines which facts exist and what "violation" means.
# ---------------------------------------------------------------------------

History = tuple  # tuple of sorted (fact, value) pairs — hashable, immutable


def make_history(facts: dict) -> History:
    return tuple(sorted(facts.items()))


def history_get(h: History, fact: str, default=None):
    for k, v in h:
        if k == fact:
            return v
    return default


@dataclass(frozen=True)
class Scenario:
    """The model: which facts exist, their domains, the constraints that
    make a history coherent, and the safety predicate.

    violates(history) -> True means this history is a violation.
    model_complete=False forces INSUFFICIENT_MODEL_OR_OBSERVABILITY.
    """
    scenario_id: str
    fact_domains: tuple          # ((fact_name, (values...)), ...)
    constraints: tuple = ()      # callables dict->bool (coherence)
    violates: object = None      # callable dict->bool
    model_complete: bool = True

    def __post_init__(self):
        assert self.violates is not None, "scenario needs a safety predicate"


@dataclass(frozen=True)
class Observation:
    """One admissible observation. Only TRUSTED evidence constrains
    histories — ordering edges come from trusted evidence, never from
    untrusted timestamps or worker labels."""
    observation_id: str
    fact: str
    allowed_values: tuple
    source: str
    trusted: bool = True

    def __post_init__(self):
        assert self.trusted, (
            f"observation {self.observation_id}: untrusted observations "
            f"cannot constrain histories")


def _enumerate(scenario: Scenario):
    """Explicit enumeration of coherent histories. Raises if the space
    exceeds MAX_HISTORIES — the engine refuses to silently sample."""
    names = [name for name, _ in scenario.fact_domains]
    domains = [values for _, values in scenario.fact_domains]
    total = 1
    for d in domains:
        total *= len(d)
    if total > MAX_HISTORIES:
        raise _SpaceTooBig(total)
    out = []
    def rec(i, acc):
        if i == len(names):
            if all(c(acc) for c in scenario.constraints):
                out.append(make_history(acc))
            return
        for v in domains[i]:
            acc[names[i]] = v
            rec(i + 1, acc)
            del acc[names[i]]
    rec(0, {})
    return out


class _SpaceTooBig(Exception):
    pass


def _consistent(h: History, observations: tuple) -> bool:
    for o in observations:
        if history_get(h, o.fact) not in o.allowed_values:
            return False
    return True


@dataclass
class PossibleHistories:
    """H(O): the concrete histories consistent with admissible observations.

    Evidence-monotonic: refine() can only shrink H(O), never grow it, never
    invent facts. Contradictory evidence raises InconsistentEvidenceError and
    is flagged — never silently resolved.
    """
    scenario: Scenario
    observations: tuple = ()
    _histories: tuple = field(default=None, repr=False)
    _all: tuple = field(default=None, repr=False)

    def __post_init__(self):
        if not self.scenario.model_complete:
            self._histories = ()
            self._all = ()
            return
        try:
            self._all = tuple(_enumerate(self.scenario))
        except _SpaceTooBig:
            self._histories = ()
            self._all = ()
            return
        self._histories = tuple(
            h for h in self._all if _consistent(h, self.observations))

    @property
    def histories(self) -> tuple:
        return self._histories

    def __len__(self):
        return len(self._histories)

    # -- MayViolate / MustViolate ----------------------------------------
    def may_violate(self) -> bool:
        return any(self.scenario.violates(dict(h)) for h in self._histories)

    def must_violate(self) -> bool:
        # H(O) must be nonempty before universal claims: an empty set would
        # make "all violate" vacuously true. Empty -> inconsistent, never PASS.
        return bool(self._histories) and all(
            self.scenario.violates(dict(h)) for h in self._histories)

    def all_safe(self) -> bool:
        return bool(self._histories) and not self.may_violate()

    # -- verdict -----------------------------------------------------------
    def verdict(self) -> str:
        if not self.scenario.model_complete or self._all == ():
            return INSUFFICIENT_MODEL_OR_OBSERVABILITY
        if not self._histories:
            return INCONSISTENT_OBSERVATIONS_OR_MODEL
        if self.all_safe():
            return SAFETY_ESTABLISHED_IN_SCOPE
        if self.must_violate():
            return VIOLATION_ESTABLISHED
        return AMBIGUOUS_BOTH_POSSIBLE

    # -- evidence-monotonic refinement --------------------------------------
    def refine(self, observation: Observation) -> "PossibleHistories":
        """Add one admissible observation. H(O) shrinks monotonically."""
        new = PossibleHistories(
            scenario=self.scenario,
            observations=self.observations + (observation,))
        if (self.verdict() not in (INSUFFICIENT_MODEL_OR_OBSERVABILITY,)
                and new.verdict() == INCONSISTENT_OBSERVATIONS_OR_MODEL
                and self.verdict() != INCONSISTENT_OBSERVATIONS_OR_MODEL):
            raise InconsistentEvidenceError(
                f"observation {observation.observation_id} contradicts every "
                f"possible history ({len(self._histories)} eliminated); "
                f"flagged, not silently resolved")
        assert len(new._histories) <= len(self._histories), \
            "refinement must never grow H(O)"
        return new

    def recompute(self, observations: tuple) -> "PossibleHistories":
        """Recompute from a different observation set (e.g. evidence
        removed). Histories are recomputed, never mutated."""
        return PossibleHistories(scenario=self.scenario,
                                 observations=tuple(observations))

    # -- what would distinguish? -------------------------------------------
    def discriminating_facts(self) -> tuple:
        """Facts whose value differs across remaining histories — the
        missing discriminating evidence, named explicitly."""
        if len(self._histories) < 2:
            return ()
        names = [n for n, _ in self.scenario.fact_domains]
        out = []
        for n in names:
            vals = {history_get(h, n) for h in self._histories}
            if len(vals) > 1:
                out.append(n)
        return tuple(out)

    # -- cold successor ------------------------------------------------------
    def serialize(self) -> bytes:
        payload = {
            "scenario_id": self.scenario.scenario_id,
            "fact_domains": [[n, list(v)] for n, v in
                             self.scenario.fact_domains],
            "observations": [
                {"observation_id": o.observation_id, "fact": o.fact,
                 "allowed_values": list(o.allowed_values),
                 "source": o.source, "trusted": o.trusted}
                for o in self.observations],
        }
        return json.dumps(payload, sort_keys=True).encode()

    def fingerprint(self) -> str:
        return hashlib.sha256(self.serialize()).hexdigest()[:16]


def cold_successor_reproduces(ph: PossibleHistories) -> tuple:
    """A fresh engine, versioned bytes only, must reproduce the verdict."""
    payload = json.loads(ph.serialize().decode())
    scenario = Scenario(
        scenario_id=payload["scenario_id"],
        fact_domains=tuple((n, tuple(v))
                           for n, v in payload["fact_domains"]),
        constraints=ph.scenario.constraints,
        violates=ph.scenario.violates,
        model_complete=ph.scenario.model_complete)
    obs = tuple(Observation(o["observation_id"], o["fact"],
                           tuple(o["allowed_values"]), o["source"],
                           o["trusted"]) for o in payload["observations"])
    rebuilt = PossibleHistories(scenario=scenario, observations=obs)
    same = rebuilt.verdict() == ph.verdict() and len(rebuilt) == len(ph)
    return same, (f"original {ph.verdict()} n={len(ph)} | "
                  f"rebuilt {rebuilt.verdict()} n={len(rebuilt)}")


# ---------------------------------------------------------------------------
# Forbidden inferences — the engine refuses to invent facts.
# ---------------------------------------------------------------------------

def infer_from_timeout(*, scope_covered_complete: bool = False):
    """A timeout proves nothing about rollback — not even in covered scope:
    the remote may have committed and the response was lost."""
    raise InventedFactError(
        f"{TIMEOUT_PROVES_NOTHING}: a timeout never establishes "
        f"ABORTED/rolled-back")


def infer_effect_from_ack():
    """An acknowledgment proves receipt, not an effect."""
    raise InventedFactError(
        f"{ACK_PROVES_NO_EFFECT}: an ack never establishes COMMITTED")


def infer_absence_from_missing_receipt(*, scope_covered_complete: bool):
    """A missing receipt proves absence ONLY inside covered-complete scope
    (composes with D31 ObservationScope.absence_is_evidence())."""
    if not scope_covered_complete:
        raise InventedFactError(
            f"{ABSENCE_PROVES_NOTHING_OUTSIDE_COVERAGE}: missing receipt "
            f"outside covered scope is not evidence of absence")
    return True


# ---------------------------------------------------------------------------
# Safety policy while ambiguous — what is permitted, what is withheld.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SafetyPolicy:
    """Consequential use of an unresolved proof is prohibited. Inspection
    and reconciliation are always permitted; certification, LEARN promotion,
    and blind retry are withheld until the proof is established."""
    verdict: str

    def may_inspect(self) -> bool:
        return True

    def may_reconcile(self) -> bool:
        return True

    def may_certify_safety(self) -> bool:
        return self.verdict == SAFETY_ESTABLISHED_IN_SCOPE

    def may_promote_to_learn(self) -> bool:
        # Withheld while ambiguous/insufficient/inconsistent. An established
        # violation IS established knowledge and may be learned from.
        return self.verdict in (SAFETY_ESTABLISHED_IN_SCOPE,
                               VIOLATION_ESTABLISHED)

    def may_blind_retry(self) -> bool:
        return False  # never: reconcile first, always

    def handoff_preserves_worlds(self, ph: PossibleHistories) -> tuple:
        """Handoffs carry every remaining possible history — never a
        collapsed single story."""
        return ph.histories


def diagnose(ph: PossibleHistories) -> dict:
    """The worker's diagnosis function. Takes ONLY the possible histories
    (built from observations) — never the hidden truth. Indistinguishable
    observations therefore cannot produce different diagnoses: answer-key
    leakage is structurally impossible."""
    return {
        "verdict": ph.verdict(),
        "n_histories": len(ph),
        "may_violate": ph.may_violate(),
        "must_violate": ph.must_violate(),
        "missing_discriminating_evidence": list(ph.discriminating_facts()),
        "policy": {
            "may_certify_safety": SafetyPolicy(ph.verdict()).may_certify_safety(),
            "may_promote_to_learn": SafetyPolicy(ph.verdict()).may_promote_to_learn(),
            "may_blind_retry": SafetyPolicy(ph.verdict()).may_blind_retry(),
        },
    }
