"""D64 / AER-LIVE-9: Dependency-Ordered Invariant Verification.

Shawn's law (SN-0815, ratified 2026-10-10; directive D64 registered
#2175 comment 6102689568, Naya 3's AER-LIVE intel): verify invariants in
dependency order, but identify failures in causal execution order — two
different tasks. Establish prerequisites before conclusions, distinguish
false from unresolved evidence, name the earliest reachable causal
failure rather than the first arbitrarily checked box, and minimize
counterexamples only while preserving the model, the transitions, the
constraints, and the replay evidence.

The gap it closes: the spec (PR #2208) states the law but its machinery
is naive in three ways this mechanism refuses to inherit —
(1) its visited-set topological sort silently returns a
prerequisite-violating order on cyclic graphs (no cycle detection);
(2) nothing separates verification order from causal diagnosis order;
(3) nothing stops UNDETERMINED collapsing into FALSE. The naive checker
below (`naive_dependency_checker`) keeps all three bugs so the tests can
prove them wrong on the fixtures.

Three verdicts, never two: PROVEN_TRUE, PROVEN_FALSE, UNDETERMINED — and
UNDETERMINED never becomes PROVEN_FALSE. A failed witness kills the
certificate, never the claim: WITNESS_INVALID demotes the invariant to
UNDETERMINED and rejects the certificate that asserted PROVEN_FALSE on
it. A solver formula alone is not a failure — every rejection is backed
by a reachable, observation-compatible replay under the original model.

Circular dependencies get joint invariants, never an invented ordering:
a cycle whose members are covered by a declared joint invariant is
DEFERRED to AER-LIVE-10 (D65); a cycle with no joint is rejected with the
cycle named. First-failure in causal order: roots (no falsified
prerequisite) separated from dependents, ordered by execution position,
all equally-early blockers reported, nothing invented. This generalizes
the spec's single-primary diagnosis, which drops independent failures
that are not downstream of the earliest one.

The canonical governance layering — observation -> temporal/version ->
lifecycle -> authority -> budget/resource -> cycle preservation -> exit —
is an optional, validated annotation: dependencies may only flow forward
through the layers, never backward.

SPEC + deterministic machinery. NOT wired into kernel/, KNOW, LAW, ACT,
or any live path. Wiring needs Shawn's word.
"""

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Vocabulary.
# ---------------------------------------------------------------------------
class TriValue(Enum):
    PROVEN_TRUE = "PROVEN_TRUE"
    PROVEN_FALSE = "PROVEN_FALSE"
    UNDETERMINED = "UNDETERMINED"


# A cycle member covered by a declared joint invariant is not judged here —
# its verification belongs to AER-LIVE-10 (D65, strongly-connected groups).
DEFERRED = "DEFERRED"

# Canonical governance layering (directive D64 register). Dependencies flow
# forward through the layers, never backward.
LAYERS = (
    "observation",
    "temporal",
    "lifecycle",
    "authority",
    "budget",
    "preservation",
    "exit",
)
_LAYER_RANK = {name: i for i, name in enumerate(LAYERS)}


# ---------------------------------------------------------------------------
# Errors. Proof failures are verdicts, not exceptions; malformed
# certificates and misuse are exceptions — fail closed, never guess.
# ---------------------------------------------------------------------------
class DependencyVerificationError(Exception):
    """Base for D64 machinery errors."""


class CertificateShapeError(DependencyVerificationError):
    """The certificate is malformed — refused before any proof is
    attempted. Duplicate names, dangling references, a non-permutation
    execution order, empty witnesses: all fail here, loudly."""


class CertificateSerializationError(DependencyVerificationError):
    """Serialized certificate bytes are malformed — the cold verifier
    fails closed, never guesses."""


def _is_str(x) -> bool:
    return isinstance(x, str) and bool(x)


def _str_tuple(xs, what: str) -> tuple:
    if not isinstance(xs, tuple):
        raise CertificateShapeError(f"{what} must be a tuple, got {xs!r}")
    for x in xs:
        if not _is_str(x):
            raise CertificateShapeError(
                f"{what} must hold non-empty strings, got {x!r}")
    if len(set(xs)) != len(xs):
        raise CertificateShapeError(f"{what} holds duplicates: {xs!r}")
    return xs


# ---------------------------------------------------------------------------
# The certificate vocabulary.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Invariant:
    """One governance invariant.

    value: the certificate's CLAIMED verdict — judged by the verifier,
        never trusted.
    proof_ref: required for PROVEN_TRUE (a TRUE with no named proof is
        unproven), forbidden otherwise.
    layer: optional canonical-layer annotation; when set, the verifier
        enforces forward-only layering.
    """
    name: str
    prerequisites: tuple = ()
    value: TriValue = TriValue.UNDETERMINED
    proof_ref: Optional[str] = None
    layer: Optional[str] = None

    def __post_init__(self):
        if not _is_str(self.name):
            raise CertificateShapeError(
                f"invariant needs a non-empty name, got {self.name!r}")
        _str_tuple(self.prerequisites, f"prerequisites of {self.name!r}")
        if self.name in self.prerequisites:
            raise CertificateShapeError(
                f"invariant {self.name!r} lists itself as a prerequisite")
        if not isinstance(self.value, TriValue):
            raise CertificateShapeError(
                f"value of {self.name!r} must be a TriValue, "
                f"got {self.value!r}")
        if self.value == TriValue.PROVEN_TRUE:
            if not _is_str(self.proof_ref):
                raise CertificateShapeError(
                    f"{self.name!r} claims PROVEN_TRUE with no proof_ref — "
                    f"a TRUE with no named proof is unproven")
        elif self.proof_ref is not None:
            raise CertificateShapeError(
                f"{self.name!r} is {self.value.value} but carries a "
                f"proof_ref — no fabricated evidence (F6)")
        if self.layer is not None and self.layer not in LAYERS:
            raise CertificateShapeError(
                f"layer of {self.name!r} must be one of {LAYERS}, "
                f"got {self.layer!r}")


@dataclass(frozen=True)
class ModelStep:
    """One step of the original model a counterexample replays.

    requires: invariants that must still hold (TRUE-state) for the step
        to execute. breaks: invariants the step falsifies.
    observations: observations the step's execution depends on — a
        witness using this step is observation-compatible only when all
        are present in the certificate's observations.
    """
    name: str
    requires: tuple = ()
    breaks: tuple = ()
    observations: tuple = ()

    def __post_init__(self):
        if not _is_str(self.name):
            raise CertificateShapeError(
                f"model step needs a non-empty name, got {self.name!r}")
        _str_tuple(self.requires, f"requires of step {self.name!r}")
        _str_tuple(self.breaks, f"breaks of step {self.name!r}")
        _str_tuple(self.observations, f"observations of step {self.name!r}")


@dataclass(frozen=True)
class Witness:
    """A failure witness (counterexample): a non-empty sequence of model
    steps that, replayed from the all-holding state under the original
    model, leaves `invariant` falsified. A solver formula alone is not a
    witness — every step must execute and the target must end FALSE."""
    invariant: str
    steps: tuple

    def __post_init__(self):
        if not _is_str(self.invariant):
            raise CertificateShapeError(
                f"witness needs a non-empty invariant name, "
                f"got {self.invariant!r}")
        _str_tuple(self.steps, f"steps of witness for {self.invariant!r}")
        if not self.steps:
            raise CertificateShapeError(
                f"witness for {self.invariant!r} has no steps — a bare "
                f"formula is not a failure")


@dataclass(frozen=True)
class JointInvariant:
    """Declared joint coverage for a circular dependency. The members'
    verification is DEFERRED to AER-LIVE-10 (D65) — D64 never invents an
    ordering for them."""
    name: str
    members: tuple

    def __post_init__(self):
        if not _is_str(self.name):
            raise CertificateShapeError(
                f"joint invariant needs a non-empty name, got {self.name!r}")
        _str_tuple(self.members, f"members of joint {self.name!r}")
        if not self.members:
            raise CertificateShapeError(
                f"joint invariant {self.name!r} covers nothing")


@dataclass(frozen=True)
class DependencyCertificate:
    """The dependency-ordered verification certificate.

    execution_order: the order the invariants were ACTUALLY evaluated in
        the live execution — a permutation of the invariant names. Causal
        diagnosis runs on this order, never on the verification order.
    model: the original model the witnesses replay under.
    witnesses: failure witnesses, at most one per invariant.
    joint_invariants: declared joint coverage for circular dependencies.
    observations: the observations on record — witness steps depending on
        absent observations are not observation-compatible.
    model_assumptions: the named assumptions the claim rests on. Never
        empty.
    """
    obligation_id: str
    boundary_ref: str
    invariants: tuple
    execution_order: tuple
    model: tuple
    witnesses: tuple
    joint_invariants: tuple = ()
    observations: tuple = ()
    model_assumptions: tuple = ()

    def __post_init__(self):
        if not _is_str(self.obligation_id):
            raise CertificateShapeError("certificate needs an obligation id")
        if not _is_str(self.boundary_ref):
            raise CertificateShapeError(
                "certificate needs a named verified boundary")
        if not isinstance(self.invariants, tuple) or not self.invariants:
            raise CertificateShapeError(
                "invariants must be a non-empty tuple")
        for inv in self.invariants:
            if not isinstance(inv, Invariant):
                raise CertificateShapeError(
                    f"{inv!r} is not an Invariant")
        names = [inv.name for inv in self.invariants]
        if len(set(names)) != len(names):
            raise CertificateShapeError(
                f"duplicate invariant names: {names!r}")
        name_set = set(names)
        for inv in self.invariants:
            for pre in inv.prerequisites:
                if pre not in name_set:
                    raise CertificateShapeError(
                        f"{inv.name!r} depends on unknown invariant "
                        f"{pre!r} — dangling references fail closed")
        _str_tuple(self.execution_order, "execution_order")
        if set(self.execution_order) != name_set:
            raise CertificateShapeError(
                "execution_order must be a permutation of the invariant "
                f"names: {sorted(self.execution_order)!r} != "
                f"{sorted(name_set)!r}")
        if not isinstance(self.model, tuple):
            raise CertificateShapeError("model must be a tuple of ModelStep")
        step_names = set()
        for step in self.model:
            if not isinstance(step, ModelStep):
                raise CertificateShapeError(f"{step!r} is not a ModelStep")
            if step.name in step_names:
                raise CertificateShapeError(
                    f"duplicate model step {step.name!r}")
            step_names.add(step.name)
            for ref in step.requires + step.breaks:
                if ref not in name_set:
                    raise CertificateShapeError(
                        f"model step {step.name!r} references unknown "
                        f"invariant {ref!r}")
        _str_tuple(self.observations, "observations")
        obs_set = set(self.observations)
        for step in self.model:
            for ob in step.observations:
                if ob not in obs_set:
                    raise CertificateShapeError(
                        f"model step {step.name!r} depends on undeclared "
                        f"observation {ob!r}")
        if not isinstance(self.witnesses, tuple):
            raise CertificateShapeError("witnesses must be a tuple")
        seen_w = set()
        for w in self.witnesses:
            if not isinstance(w, Witness):
                raise CertificateShapeError(f"{w!r} is not a Witness")
            if w.invariant not in name_set:
                raise CertificateShapeError(
                    f"witness targets unknown invariant {w.invariant!r}")
            if w.invariant in seen_w:
                raise CertificateShapeError(
                    f"duplicate witness for {w.invariant!r}")
            seen_w.add(w.invariant)
            for s in w.steps:
                if s not in step_names:
                    raise CertificateShapeError(
                        f"witness for {w.invariant!r} uses unknown model "
                        f"step {s!r}")
        if not isinstance(self.joint_invariants, tuple):
            raise CertificateShapeError("joint_invariants must be a tuple")
        joint_names = set()
        covered: set = set()
        for j in self.joint_invariants:
            if not isinstance(j, JointInvariant):
                raise CertificateShapeError(f"{j!r} is not a JointInvariant")
            if j.name in joint_names:
                raise CertificateShapeError(
                    f"duplicate joint invariant {j.name!r}")
            joint_names.add(j.name)
            for m in j.members:
                if m not in name_set:
                    raise CertificateShapeError(
                        f"joint {j.name!r} covers unknown invariant {m!r}")
                if m in covered:
                    raise CertificateShapeError(
                        f"invariant {m!r} covered by two joints — one "
                        f"joint per cycle member")
                covered.add(m)
        _str_tuple(self.model_assumptions, "model_assumptions")
        if not self.model_assumptions:
            raise CertificateShapeError(
                "verification claims rest on stated assumptions — none named")


_MODEL_ASSUMPTIONS = (
    "Verification order is topological over the prerequisite graph "
    "(Kahn's algorithm, name-sorted tie-break): every prerequisite is "
    "verified before its dependents. Diagnosis order is the certificate's "
    "execution_order: the earliest reachable causal failure, never the "
    "first arbitrarily checked box.",
    "Three verdicts, never two. PROVEN_TRUE needs a named proof and "
    "PROVEN_TRUE transitive prerequisites. PROVEN_FALSE needs a reachable, "
    "observation-compatible, minimal witness replayed under the original "
    "model — or a falsified transitive prerequisite (dependent diagnosis). "
    "UNDETERMINED carries no witness and no proof, and never collapses to "
    "PROVEN_FALSE.",
    "A failed witness kills the certificate, never the claim: "
    "WITNESS_INVALID demotes the invariant to UNDETERMINED and rejects the "
    "certificate that asserted PROVEN_FALSE on it. Circular dependencies "
    "get declared joint invariants (deferred to AER-LIVE-10); an invented "
    "ordering is never substituted.",
    "Every history constructed here is a defensible hypothesis WITHIN "
    "THESE ASSUMPTIONS for dependency-ordered verification — never an "
    "asserted fact, never a production authorization.",
)


# ---------------------------------------------------------------------------
# The prerequisite graph: cycles, canonical order, transitive closure.
# ---------------------------------------------------------------------------
def _prereq_map(cert: DependencyCertificate) -> dict:
    return {inv.name: tuple(inv.prerequisites) for inv in cert.invariants}


def find_cycle(prereq: dict) -> Optional[tuple]:
    """First directed cycle in the prerequisite graph, as a name path
    (start repeated at the end), or None. Iterative DFS — no recursion
    limit games, deterministic over sorted names."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in prereq}
    stack: list = []

    for root in sorted(prereq):
        if color[root] != WHITE:
            continue
        work = [(root, iter(sorted(prereq[root])))]
        color[root] = GRAY
        stack = [root]
        while work:
            node, it = work[-1]
            advanced = False
            for pre in it:
                if color[pre] == WHITE:
                    color[pre] = GRAY
                    stack.append(pre)
                    work.append((pre, iter(sorted(prereq[pre]))))
                    advanced = True
                    break
                if color[pre] == GRAY:
                    i = stack.index(pre)
                    return tuple(stack[i:] + [pre])
            if not advanced:
                color[node] = BLACK
                stack.pop()
                work.pop()
    return None


def canonical_verification_order(cert: DependencyCertificate,
                                 deferred: set) -> tuple:
    """Kahn's algorithm over the non-deferred invariants, name-sorted
    tie-break. Every prerequisite precedes its dependents; the order is
    fully determined by the graph — no invented choices."""
    prereq = _prereq_map(cert)
    nodes = sorted(n for n in prereq if n not in deferred)
    indeg = {n: 0 for n in nodes}
    dependents: dict = {n: [] for n in nodes}
    for n in nodes:
        for pre in prereq[n]:
            if pre in indeg:
                indeg[n] += 1
                dependents[pre].append(n)
    import heapq
    heap = [n for n in nodes if indeg[n] == 0]
    heapq.heapify(heap)
    order = []
    while heap:
        n = heapq.heappop(heap)
        order.append(n)
        for d in dependents[n]:
            indeg[d] -= 1
            if indeg[d] == 0:
                heapq.heappush(heap, d)
    return tuple(order)


def transitive_prereqs(name: str, prereq: dict) -> set:
    """All (transitive) prerequisites of an invariant."""
    seen: set = set()
    stack = list(prereq.get(name, ()))
    while stack:
        p = stack.pop()
        if p in seen:
            continue
        seen.add(p)
        stack.extend(prereq.get(p, ()))
    return seen


# ---------------------------------------------------------------------------
# Witness replay: reachable and observation-compatible under the original
# model, or it is not a witness at all.
# ---------------------------------------------------------------------------
def _replay_steps(invariant: str, steps: tuple,
                cert: DependencyCertificate) -> tuple:
    """Core replay over a raw step tuple (may be empty — an empty replay
    leaves every invariant holding, so it never falsifies)."""
    by_step = {s.name: s for s in cert.model}
    obs = set(cert.observations)
    state = {inv.name: True for inv in cert.invariants}
    for sname in steps:
        step = by_step[sname]
        for ob in step.observations:
            if ob not in obs:
                return False, (
                    f"step {sname!r} needs observation {ob!r} which is "
                    f"not on record — not observation-compatible")
        for req in step.requires:
            if not state[req]:
                return False, (
                    f"step {sname!r} requires {req!r} to hold, but it is "
                    f"already falsified — not reachable")
        for brk in step.breaks:
            state[brk] = False
    if state[invariant]:
        return False, (
            f"witness does not falsify {invariant!r} — a solver "
            f"formula alone is not a failure")
    return True, "replays and falsifies"


def replay_witness(witness: Witness,
                   cert: DependencyCertificate) -> tuple:
    """Replay the witness steps from the all-holding state.

    Returns (True, "replays and falsifies") when every step executes —
    each required invariant still holding, each required observation on
    record — and the target invariant ends falsified. Otherwise
    (False, reason): the witness is not reachable, not
    observation-compatible, or does not falsify — WITNESS_INVALID."""
    return _replay_steps(witness.invariant, witness.steps, cert)


def is_minimal_witness(witness: Witness,
                       cert: DependencyCertificate) -> tuple:
    """Minimality as a fixed point of single-step elimination: dropping
    any one step must break the replay or stop the falsification.
    Minimization preserves the model, the transitions, the constraints,
    and the replay evidence — a shorter witness that no longer replays
    is not a minimization, it is a different (invalid) claim."""
    steps = witness.steps
    for i in range(len(steps)):
        # The reduced tuple may be empty — _replay_steps handles it: an
        # empty replay falsifies nothing, so the dropped step was
        # load-bearing. No Witness is constructed here, so the shape
        # rule against empty witnesses is never tripped by the check
        # itself.
        ok, _ = _replay_steps(witness.invariant,
                              steps[:i] + steps[i + 1:], cert)
        if ok:
            return False, (
                f"step {steps[i]!r} is redundant — the witness is not "
                f"minimal")
    return True, "minimal: every step load-bearing"


# ---------------------------------------------------------------------------
# The verifier.
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class InvariantVerdict:
    """What the verifier judges for one invariant — and what it does not.

    verdict: PROVEN_TRUE / PROVEN_FALSE / UNDETERMINED / DEFERRED.
    independently_proven: a PROVEN_FALSE with its own valid witness
        (a dependent PROVEN_FALSE rides on a falsified prerequisite).
    witness_status: None when no witness was judged; "valid" when the
        witness replays, is observation-compatible and minimal;
        "invalid: <reason>" when it does not.
    evidence_needed: for UNDETERMINED — the blocking prerequisite or
        joint names, i.e. what evidence reconstruction must go collect.
    """
    name: str
    verdict: str
    independently_proven: bool
    witness_status: Optional[str]
    evidence_needed: tuple

    def __post_init__(self):
        if self.verdict not in (TriValue.PROVEN_TRUE.value,
                                TriValue.PROVEN_FALSE.value,
                                TriValue.UNDETERMINED.value, DEFERRED):
            raise CertificateShapeError(
                f"bad verdict {self.verdict!r} for {self.name!r}")


@dataclass(frozen=True)
class DependencyOrderVerdict:
    """The full judgment.

    primary_failures: roots — falsified invariants with no falsified
        prerequisite — ordered by execution position, ALL reported.
    dependent_failures: falsified invariants downstream of a falsified
        prerequisite, ordered by execution position.
    verification_order: the canonical topological order the prerequisites
        were verified in (non-deferred invariants).
    deferred_joints: joint invariants deferred to AER-LIVE-10.
    failure: the rejection reason, or None when accepted. An accepted
        certificate may still carry UNDETERMINED and DEFERRED invariants —
        honest unknowns are not defects.
    """
    obligation_id: str
    accepted: bool
    invariant_verdicts: tuple
    primary_failures: tuple
    dependent_failures: tuple
    verification_order: tuple
    deferred_joints: tuple
    failure: Optional[str]
    model_assumptions: tuple
    certificate_fingerprint: str

    def __post_init__(self):
        if self.accepted and self.failure is not None:
            raise CertificateShapeError(
                "an accepted verdict carries no failure")
        if not self.accepted and not self.failure:
            raise CertificateShapeError(
                "a rejection names its reason")
        names = {iv.name for iv in self.invariant_verdicts}
        falsified = {iv.name for iv in self.invariant_verdicts
                     if iv.verdict == TriValue.PROVEN_FALSE.value}
        for p in self.primary_failures:
            if p not in falsified:
                raise CertificateShapeError(
                    f"primary failure {p!r} is not PROVEN_FALSE")
        for d in self.dependent_failures:
            if d not in falsified:
                raise CertificateShapeError(
                    f"dependent failure {d!r} is not PROVEN_FALSE")
        if set(self.primary_failures) & set(self.dependent_failures):
            raise CertificateShapeError(
                "an invariant cannot be both primary and dependent")
        if set(self.primary_failures) | set(self.dependent_failures) != \
                falsified:
            raise CertificateShapeError(
                "every falsified invariant is either primary or dependent")


def _fingerprint(cert: DependencyCertificate) -> str:
    canonical = json.dumps(_cert_to_dict(cert), sort_keys=True,
                           separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


def verify_dependency_order(
        cert: DependencyCertificate) -> DependencyOrderVerdict:
    """Independently verify the certificate. Every check is recomputed:

    1. cycles — each directed cycle must be covered by exactly one
       declared joint invariant (deferred to AER-LIVE-10); an uncovered
       cycle, or a joint covering no cycle, rejects with names;
    2. layering — declared layers flow forward only;
    3. evidence honesty (F1/F6) — PROVEN_TRUE needs its proof and
       PROVEN_TRUE transitive prerequisites; PROVEN_FALSE needs a valid
       witness or a falsified prerequisite; UNDETERMINED carries no
       witness and no proof and never collapses;
    4. witness validity — reachable, observation-compatible, minimal;
       a failed witness kills the certificate and demotes the invariant
       to UNDETERMINED (never to PROVEN_FALSE);
    5. causal diagnosis — roots vs dependents in execution order.

    The loop never stops at the first defect: every invariant is judged
    so the verdict carries maximal information; the first fatal reason
    is the rejection reason.
    """
    by_name = {inv.name: inv for inv in cert.invariants}
    prereq = _prereq_map(cert)
    witness_by = {w.invariant: w for w in cert.witnesses}
    joints = {j.name: j for j in cert.joint_invariants}

    fatal: Optional[str] = None
    verdicts: dict = {}
    deferred: set = set()
    joint_of: dict = {}

    def note_fatal(reason: str):
        nonlocal fatal
        if fatal is None:
            fatal = reason

    # -- 1. cycles: joint coverage or rejection ---------------------------
    remaining = dict(prereq)
    while True:
        cyc = find_cycle(remaining)
        if cyc is None:
            break
        members = set(cyc)
        for m in sorted(members):
            covering = [j.name for j in cert.joint_invariants
                        if m in j.members]
            if len(covering) != 1:
                note_fatal(
                    f"circular dependency without a joint invariant: "
                    f"{' -> '.join(cyc)} — circular dependencies get "
                    f"joint invariants, never an invented ordering "
                    f"(AER-LIVE-10)")
                joint_of[m] = None
            else:
                joint_of[m] = covering[0]
        deferred |= members
        for m in members:
            del remaining[m]
        # Strip the removed members from every surviving prerequisite
        # list — otherwise the next find_cycle pass chases dangling
        # references (KeyError) instead of the residual graph.
        remaining = {n: tuple(p for p in pres if p not in deferred)
                     for n, pres in remaining.items()}
    for j in cert.joint_invariants:
        if not any(m in deferred and joint_of.get(m) == j.name
                   for m in j.members):
            note_fatal(
                f"joint invariant {j.name!r} covers no circular "
                f"dependency — joints exist only for cycles")
    for m in sorted(deferred):
        verdicts[m] = InvariantVerdict(
            m, DEFERRED, False, None,
            (f"deferred to AER-LIVE-10 via joint "
             f"{joint_of.get(m)!r}",) if joint_of.get(m) else ())

    order = canonical_verification_order(cert, deferred)

    # -- 2. layering: forward only -----------------------------------------
    for name in order:
        inv = by_name[name]
        if inv.layer is None:
            continue
        for pre in inv.prerequisites:
            pl = by_name[pre].layer
            if pl is not None and pre not in deferred and \
                    _LAYER_RANK[pl] > _LAYER_RANK[inv.layer]:
                note_fatal(
                    f"layering violation: {name!r} [{inv.layer}] depends "
                    f"on {pre!r} [{pl}] — dependencies flow "
                    f"{' -> '.join(LAYERS)}, never backward")

    # -- 3+4. per-invariant evidence judgment, in verification order ------
    for name in order:
        inv = by_name[name]
        tpre = transitive_prereqs(name, prereq)
        w = witness_by.get(name)
        claimed = inv.value

        if claimed == TriValue.PROVEN_TRUE:
            if w is not None:
                note_fatal(
                    f"{name!r} claims PROVEN_TRUE but carries a failure "
                    f"witness — no fabricated evidence")
                verdicts[name] = InvariantVerdict(
                    name, TriValue.UNDETERMINED.value, False,
                    "invalid: witness on a PROVEN_TRUE claim",
                    ("remove the witness or the TRUE claim",))
                continue
            bad = sorted(p for p in tpre
                         if verdicts[p].verdict in (
                             TriValue.PROVEN_FALSE.value,
                             TriValue.UNDETERMINED.value))
            if bad:
                note_fatal(
                    f"{name!r} claims PROVEN_TRUE on unproven prerequisite "
                    f"{bad[0]!r}={verdicts[bad[0]].verdict} — establish "
                    f"prerequisites before conclusions")
                verdicts[name] = InvariantVerdict(
                    name, TriValue.UNDETERMINED.value, False, None,
                    tuple(bad))
                continue
            blocked = sorted(p for p in tpre if p in deferred)
            if blocked:
                verdicts[name] = InvariantVerdict(
                    name, TriValue.UNDETERMINED.value, False, None,
                    tuple(sorted({joint_of[p] for p in blocked
                                  if joint_of.get(p)})))
                continue
            verdicts[name] = InvariantVerdict(
                name, TriValue.PROVEN_TRUE.value, True, None, ())

        elif claimed == TriValue.PROVEN_FALSE:
            if w is None:
                if any(verdicts[p].verdict == TriValue.PROVEN_FALSE.value
                       for p in tpre):
                    verdicts[name] = InvariantVerdict(
                        name, TriValue.PROVEN_FALSE.value, False, None, ())
                else:
                    note_fatal(
                        f"{name!r} claims PROVEN_FALSE with no witness "
                        f"and no falsified prerequisite — an unproven "
                        f"FALSE is not a verdict (F1)")
                    verdicts[name] = InvariantVerdict(
                        name, TriValue.UNDETERMINED.value, False, None,
                        ("a reachable witness or a falsified "
                         "prerequisite",))
                continue
            ok, reason = replay_witness(w, cert)
            if ok:
                ok, reason = is_minimal_witness(w, cert)
            if not ok:
                # A failed witness kills the certificate, never the claim:
                # the invariant falls back to UNDETERMINED — the failed
                # replay proves nothing about the invariant itself.
                note_fatal(f"witness for {name!r} invalid: {reason}")
                verdicts[name] = InvariantVerdict(
                    name, TriValue.UNDETERMINED.value, False,
                    f"invalid: {reason}",
                    ("a reachable, observation-compatible, minimal "
                     "witness",))
            else:
                verdicts[name] = InvariantVerdict(
                    name, TriValue.PROVEN_FALSE.value, True, "valid", ())

        else:  # UNDETERMINED
            if w is not None:
                note_fatal(
                    f"{name!r} is UNDETERMINED but carries a failure "
                    f"witness — no fabricated failures (F6)")
                verdicts[name] = InvariantVerdict(
                    name, TriValue.UNDETERMINED.value, False,
                    "invalid: witness on an UNDETERMINED claim",
                    ("remove the witness — UNDETERMINED means the "
                     "evidence is missing, not hidden",))
                continue
            blocked = sorted(p for p in tpre
                             if verdicts[p].verdict !=
                             TriValue.PROVEN_TRUE.value)
            verdicts[name] = InvariantVerdict(
                name, TriValue.UNDETERMINED.value, False, None,
                tuple(blocked))

    # -- witnesses on non-FALSE claims (fabrication sweep) ------------------
    for wname, w in witness_by.items():
        if wname in deferred:
            continue  # the joint's evidence is AER-LIVE-10's jurisdiction
        if wname not in verdicts:
            continue
        if by_name[wname].value != TriValue.PROVEN_FALSE:
            # Already fatalled inside the loop for TRUE/UNDETERMINED
            # claims; this sweep only guards verdicts recorded before
            # the claim check (defense in depth, no double-count).
            pass

    # -- 5. causal diagnosis in execution order -----------------------------
    pos = {n: i for i, n in enumerate(cert.execution_order)}
    falsified = [n for n in cert.execution_order
                 if verdicts[n].verdict == TriValue.PROVEN_FALSE.value]

    def has_false_prereq(n: str) -> bool:
        return any(verdicts[p].verdict == TriValue.PROVEN_FALSE.value
                   for p in transitive_prereqs(n, prereq))

    primaries = tuple(n for n in falsified if not has_false_prereq(n))
    dependents = tuple(n for n in falsified if has_false_prereq(n))

    ordered_verdicts = tuple(verdicts[n] for n in cert.execution_order)
    return DependencyOrderVerdict(
        obligation_id=cert.obligation_id,
        accepted=fatal is None,
        invariant_verdicts=ordered_verdicts,
        primary_failures=primaries,
        dependent_failures=dependents,
        verification_order=order,
        deferred_joints=tuple(sorted(joints)),
        failure=fatal,
        model_assumptions=cert.model_assumptions,
        certificate_fingerprint=_fingerprint(cert),
    )


# ---------------------------------------------------------------------------
# The naive checker — the defective baseline. Three bugs, kept deliberately:
#  1. the spec's visited-set topological sort: no cycle detection, so on a
#     cyclic graph it silently returns an order that violates
#     prerequisite-before-dependent;
#  2. the primary failure is diagnosed in VERIFICATION order, not in the
#     execution order where the failure actually happened first;
#  3. UNDETERMINED collapses to FALSE — two-valued thinking.
# The tests prove it wrong on the fixtures; the real verifier is right.
# ---------------------------------------------------------------------------
def _spec_topological_order(invariants) -> list:
    """The spec's algorithm (PR #2208), logic verbatim: visited-set DFS
    with no cycle detection."""
    by_name = {inv.name: inv for inv in invariants}
    visited = set()
    order = []

    def visit(name):
        if name in visited:
            return
        visited.add(name)
        inv = by_name[name]
        for pre in inv.prerequisites:
            visit(pre)
        order.append(name)

    for inv in invariants:
        visit(inv.name)
    return order


def naive_dependency_checker(cert: DependencyCertificate) -> dict:
    """The defective baseline: conflates verification order with causal
    order and collapses UNDETERMINED into FALSE."""
    order = _spec_topological_order(cert.invariants)
    by_name = {inv.name: inv for inv in cert.invariants}
    verdicts = {}
    for n in order:
        v = by_name[n].value
        verdicts[n] = (TriValue.PROVEN_TRUE.value
                       if v == TriValue.PROVEN_TRUE
                       else TriValue.PROVEN_FALSE.value)  # BUG 3: collapse
    primary = next((n for n in order  # BUG 2: verification order, not
                    if verdicts[n] == TriValue.PROVEN_FALSE.value),  # execution
                   None)
    return {"verification_order": order, "verdicts": verdicts,
            "primary_failure": primary}


# ---------------------------------------------------------------------------
# Serialization: the cold verifier reconstructs the certificate from bytes
# alone and re-runs every check. Malformed bytes fail closed.
# ---------------------------------------------------------------------------
def _cert_to_dict(cert: DependencyCertificate) -> dict:
    def inv(i: Invariant) -> dict:
        return {"name": i.name, "prerequisites": list(i.prerequisites),
                "value": i.value.value, "proof_ref": i.proof_ref,
                "layer": i.layer}

    def step(s: ModelStep) -> dict:
        return {"name": s.name, "requires": list(s.requires),
                "breaks": list(s.breaks),
                "observations": list(s.observations)}

    def wit(w: Witness) -> dict:
        return {"invariant": w.invariant, "steps": list(w.steps)}

    def joint(j: JointInvariant) -> dict:
        return {"name": j.name, "members": list(j.members)}

    return {
        "obligation_id": cert.obligation_id,
        "boundary_ref": cert.boundary_ref,
        "invariants": [inv(i) for i in cert.invariants],
        "execution_order": list(cert.execution_order),
        "model": [step(s) for s in cert.model],
        "witnesses": [wit(w) for w in cert.witnesses],
        "joint_invariants": [joint(j) for j in cert.joint_invariants],
        "observations": list(cert.observations),
        "model_assumptions": list(cert.model_assumptions),
    }


def _cert_from_dict(d: dict) -> DependencyCertificate:
    def tri(v: str) -> TriValue:
        return TriValue(v)

    return DependencyCertificate(
        obligation_id=d["obligation_id"],
        boundary_ref=d["boundary_ref"],
        invariants=tuple(
            Invariant(i["name"], tuple(i["prerequisites"]), tri(i["value"]),
                      i.get("proof_ref"), i.get("layer"))
            for i in d["invariants"]),
        execution_order=tuple(d["execution_order"]),
        model=tuple(
            ModelStep(s["name"], tuple(s["requires"]), tuple(s["breaks"]),
                      tuple(s.get("observations", ())))
            for s in d["model"]),
        witnesses=tuple(
            Witness(w["invariant"], tuple(w["steps"]))
            for w in d["witnesses"]),
        joint_invariants=tuple(
            JointInvariant(j["name"], tuple(j["members"]))
            for j in d.get("joint_invariants", ())),
        observations=tuple(d["observations"]),
        model_assumptions=tuple(d["model_assumptions"]),
    )


def serialize_certificate(cert: DependencyCertificate) -> bytes:
    """Canonical bytes for the cold verifier."""
    return json.dumps(_cert_to_dict(cert), sort_keys=True,
                      separators=(",", ":")).encode()


def independent_verify(raw: bytes) -> DependencyOrderVerdict:
    """Cold verification: rebuild the certificate from bytes alone and
    re-run every check. Anything malformed fails closed."""
    try:
        d = json.loads(raw.decode())
    except Exception as e:
        raise CertificateSerializationError(
            f"certificate bytes are not valid JSON: {e}")
    try:
        cert = _cert_from_dict(d)
    except Exception as e:
        raise CertificateSerializationError(
            f"certificate bytes do not decode to a valid certificate: {e}")
    return verify_dependency_order(cert)


# ---------------------------------------------------------------------------
# AER-LIVE-009 fixtures — the cases that make it real.
# ---------------------------------------------------------------------------
def aer_live9_model() -> tuple:
    """The original model the witnesses replay under."""
    return (
        ModelStep("observe_sensor", (), (), ("sensor_reading",)),
        ModelStep("advance_past_expiry", ("temporal",), ("temporal",), ()),
        ModelStep("drain_budget", ("budget",), ("budget",), ()),
        ModelStep("corrupt_evidence", ("authority",),
                  ("authority",), ()),
    )


def _aer_live9_invariants_f1():
    T, F, U = TriValue.PROVEN_TRUE, TriValue.PROVEN_FALSE, \
        TriValue.UNDETERMINED
    return (
        Invariant("obs", (), T, "OBS-7: sensor reading nominal",
                  "observation"),
        Invariant("timing", ("obs",), T,
                  "TIME-11: LAW expiry observed", "observation"),
        Invariant("temporal", ("obs", "timing"), F, None, "temporal"),
        Invariant("lifecycle", ("temporal",), F, None, "lifecycle"),
        Invariant("authority", ("temporal", "lifecycle"), F, None,
                  "authority"),
        Invariant("budget", ("obs",), F, None, "budget"),
        Invariant("preservation", ("lifecycle", "authority", "budget"), U,
                  None, "preservation"),
        Invariant("exit", ("preservation",), U, None, "exit"),
    )


def aer_live9_certificate_f1() -> DependencyCertificate:
    """F1: LAW expiry proven. The verifier produces the minimal one-cycle
    counterexample (advance_past_expiry), names the roots
    (temporal, budget) in execution order, separates the dependents
    (lifecycle, authority), and keeps preservation/exit UNDETERMINED."""
    return DependencyCertificate(
        obligation_id="AER-LIVE-009-F1",
        boundary_ref="governance-boundary-2026-10-11",
        invariants=_aer_live9_invariants_f1(),
        execution_order=("temporal", "obs", "timing", "lifecycle",
                         "authority", "budget", "preservation", "exit"),
        model=aer_live9_model(),
        witnesses=(
            Witness("temporal", ("advance_past_expiry",)),
            Witness("budget", ("drain_budget",)),
        ),
        observations=("sensor_reading",),
        model_assumptions=_MODEL_ASSUMPTIONS,
    )


def aer_live9_certificate_f6() -> DependencyCertificate:
    """F6: LAW-effective-time evidence missing. timing stays
    UNDETERMINED — no fabricated failure. The verifier preserves
    UNDETERMINED everywhere the evidence is missing and the verdict's
    evidence_needed triggers evidence reconstruction (temporal names
    timing as the missing evidence)."""
    T, U = TriValue.PROVEN_TRUE, TriValue.UNDETERMINED
    return DependencyCertificate(
        obligation_id="AER-LIVE-009-F6",
        boundary_ref="governance-boundary-2026-10-11",
        invariants=(
            Invariant("obs", (), T, "OBS-7: sensor reading nominal",
                      "observation"),
            Invariant("timing", ("obs",), U, None, "observation"),
            Invariant("temporal", ("obs", "timing"), U, None, "temporal"),
            Invariant("lifecycle", ("temporal",), U, None, "lifecycle"),
            Invariant("authority", ("temporal", "lifecycle"), U, None,
                      "authority"),
            Invariant("budget", ("obs",), T, "BUD-3: budget solvent",
                      "budget"),
            Invariant("preservation",
                      ("lifecycle", "authority", "budget"), U, None,
                      "preservation"),
            Invariant("exit", ("preservation",), U, None, "exit"),
        ),
        execution_order=("temporal", "obs", "timing", "lifecycle",
                         "authority", "budget", "preservation", "exit"),
        model=aer_live9_model(),
        witnesses=(),
        observations=("sensor_reading",),
        model_assumptions=_MODEL_ASSUMPTIONS,
    )


def aer_live9_certificate_cyclic() -> DependencyCertificate:
    """A↔B with no joint invariant: rejected with the cycle named."""
    U = TriValue.UNDETERMINED
    return DependencyCertificate(
        obligation_id="AER-LIVE-009-CYCLE",
        boundary_ref="governance-boundary-2026-10-11",
        invariants=(
            Invariant("cycle_a", ("cycle_b",), U, None, "authority"),
            Invariant("cycle_b", ("cycle_a",), U, None, "authority"),
        ),
        execution_order=("cycle_a", "cycle_b"),
        model=(),
        witnesses=(),
        model_assumptions=_MODEL_ASSUMPTIONS,
    )


def aer_live9_certificate_joint() -> DependencyCertificate:
    """A↔B with a declared joint invariant: accepted, members DEFERRED
    to AER-LIVE-10 — no invented ordering."""
    U = TriValue.UNDETERMINED
    return DependencyCertificate(
        obligation_id="AER-LIVE-009-JOINT",
        boundary_ref="governance-boundary-2026-10-11",
        invariants=(
            Invariant("cycle_a", ("cycle_b",), U, None, "authority"),
            Invariant("cycle_b", ("cycle_a",), U, None, "authority"),
            Invariant("downstream", ("cycle_a",), U, None, "budget"),
        ),
        execution_order=("cycle_a", "cycle_b", "downstream"),
        model=(),
        witnesses=(),
        joint_invariants=(JointInvariant("joint_ab",
                                         ("cycle_a", "cycle_b")),),
        model_assumptions=_MODEL_ASSUMPTIONS,
    )
