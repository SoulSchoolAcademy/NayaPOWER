"""D65 / AER-LIVE-10: Strongly Connected Invariant Groups and Joint Proof Qualification.

Shawn's law (SN-0816, ratified 2026-10-10): when invariants depend on one
another cyclically, no member may serve as independent proof of another.
Collapse the cycle into one joint state-transition system, ground it in
authoritative initial state, and prove reachability, safety closure,
repeatability, exit viability and progress separately.

The joint-proof law, as executable machinery:

- BETWEEN components, prerequisites first; WITHIN a component, solve
  simultaneously. ``condensation_order`` topologically orders the SCC
  condensation of the prerequisite graph (Kahn, name-sorted tie-break) so
  proof work is scheduled across components; it never ranks one member of a
  component above another. Inside a component the members are verified
  jointly, never one-by-one.
- NO MEMBER CERTIFIES ANOTHER. The verifier never accepts pre-computed
  booleans (the spec's ``JointProof`` pattern). Every property is computed
  from the presented complete legal transition relation: reachability by
  BFS, safety closure by checking every reachable transition against the
  cross-relationships, repeatability by greatest-fixed-point convergence,
  progress by maximum-mean-cycle, exit viability by constructive search.
- THE GROUP NEVER ESTABLISHES ITS OWN EXTERNAL FACTS. The declaration's
  authority must not be a member; every replenishment authorization's
  issuer must not be a member; the relation digest re-computed by the
  verifier must match the authorized digest (the group cannot swap the
  relation, the graph, or the initial state under the authorization).
- CROSS-RELATIONSHIPS no member can hold alone, checked on every reachable
  transition: replenishment implies lawful authorization; reservation
  implies capacity and ownership; a declared terminal (exit) implies no new
  cycle (the exit is genuinely terminal in the complete relation).
- REPEATABILITY VIA GREATEST FIXED POINT from the complete legal
  transition relation, with a real reachable entry. Convergence proves a
  property of the PRESENTED MODEL, so the verifier qualifies the model too:
  every verdict carries the model digest and never claims more than the
  model supports.
- VERDICTS STAY SEPARATE: REPEATABLE_PROVEN / DEADLOCK_IN_SCOPE /
  LIVELOCK_COUNTEREXAMPLE / EXIT_POSSIBLE_NOT_GUARANTEED /
  JOINT_UNDETERMINED -- because an escape path existing is not the same as
  every fair execution escaping. A refusal (ungrounded group) is
  JOINT_UNDETERMINED carrying the MINIMAL joint obstruction: exactly the
  failed grounding facts, each individually necessary, nothing else.

Composition contract with D64 (AER-LIVE-9): D64 verifies acyclic members in
dependency order and marks cycle members covered by a declared joint as
DEFERRED, carrying the joint name. This module verifies the deferred
joint: build a ``JointDeclaration`` with the same joint name and the
prerequisite graph, call ``verify_joint``. D64's DEFERRED members are this
module's ``members``; D64's verification order across components is this
module's ``condensation_order``. This module does not modify D64's code.

CODE-ONLY (declared): the mechanism, its tests, and its spec document.
Wiring to D64's DEFERRED seam and to CI is the wire lane's call.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import Enum


# ---------------------------------------------------------------------------
# Verdicts
# ---------------------------------------------------------------------------

class Verdict(Enum):
    REPEATABLE_PROVEN = "REPEATABLE_PROVEN"
    DEADLOCK_IN_SCOPE = "DEADLOCK_IN_SCOPE"
    LIVELOCK_COUNTEREXAMPLE = "LIVELOCK_COUNTEREXAMPLE"
    EXIT_POSSIBLE_NOT_GUARANTEED = "EXIT_POSSIBLE_NOT_GUARANTEED"
    JOINT_UNDETERMINED = "JOINT_UNDETERMINED"


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

# Transition kinds. The kind selects which cross-relationship is checked.
KIND_ORDINARY = "ordinary"
KIND_REPLENISH = "replenish"
KIND_RESERVE = "reserve"
KIND_COMPLETE = "complete"  # the step that reaches a terminal exit
KINDS = (KIND_ORDINARY, KIND_REPLENISH, KIND_RESERVE, KIND_COMPLETE)


@dataclass(frozen=True)
class JointTransition:
    """One legal step of the joint state-transition system.

    The declaring authority presents the COMPLETE legal transition
    relation: anything not listed here is illegal. ``progress`` is the
    advancement measure for this step (debt gain); a joint cycle is
    progressive iff some cycle's total progress is positive.
    Authorization references use the "issuer:reference" convention; the
    issuer (part before the first ':') must be external to the group.
    """
    src: str
    dst: str
    kind: str = KIND_ORDINARY
    progress: int = 0
    authorization: str | None = None  # required iff kind == "replenish"
    capacity: str | None = None       # required iff kind == "reserve"
    owner: str | None = None          # required iff kind == "reserve"


@dataclass(frozen=True)
class JointDeclaration:
    """Everything the verifier needs, presented for checking -- never trusted.

    ``declared_by`` is the external authority (a seat, a law, a signed
    record) that grounds the group. It must NOT be a member: the group
    never establishes its own external facts. ``relation_digest`` is the
    sha256 over the canonical encoding of (members, prereq graph,
    transitions, initial states, authorized initial, exits); the verifier
    recomputes it, so the presented model cannot drift under the
    authorization.
    """
    name: str
    members: frozenset
    declared_by: str
    prereq: dict                      # member -> tuple of prerequisite member names
    initial_states: frozenset         # candidate initial joint states
    authorized_initial: frozenset     # subset the authority actually authorized
    transitions: tuple                # the COMPLETE legal transition relation
    relation_digest: str
    exit_states: frozenset = frozenset()


@dataclass(frozen=True)
class JointVerdict:
    """The verifier's judgment. Qualifies the presented model only."""
    verdict: Verdict
    group: str
    model_digest: str                 # digest of the model actually judged
    obstruction: tuple = ()           # minimal blocking facts (refusal / undetermined)
    reachable: frozenset = frozenset()
    kernel: frozenset = frozenset()   # GFP: states that can continue forever
    exhibited_cycle: tuple = ()       # witness cycle (positive or zero progress)
    cycle_progress: int = 0
    exit_path: tuple = ()             # constructive exit path, if one exists
    deadlock_state: str | None = None
    safety_violations: tuple = ()
    notes: tuple = ()


# ---------------------------------------------------------------------------
# Canonical encoding / digests
# ---------------------------------------------------------------------------

def _canon_transition(t: JointTransition) -> tuple:
    return (t.src, t.dst, t.kind, t.progress, t.authorization, t.capacity, t.owner)


def canonical_model_encoding(declaration: JointDeclaration) -> str:
    """Canonical byte-stable encoding of everything the verdict rests on."""
    prereq = {k: sorted(v) for k, v in declaration.prereq.items()}
    payload = {
        "members": sorted(declaration.members),
        "declared_by": declaration.declared_by,
        "prereq": prereq,
        "initial_states": sorted(declaration.initial_states),
        "authorized_initial": sorted(declaration.authorized_initial),
        "transitions": sorted(_canon_transition(t) for t in declaration.transitions),
        "exit_states": sorted(declaration.exit_states),
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def model_digest_of(declaration: JointDeclaration) -> str:
    return hashlib.sha256(canonical_model_encoding(declaration).encode()).hexdigest()


def make_declaration(*, name, members, declared_by, prereq, initial_states,
                     authorized_initial, transitions, exit_states=frozenset()):
    """Build a declaration with the digest computed honestly.

    Use this to construct declarations in tests and callers; hand-editing
    the digest afterwards is exactly the tamper the verifier refuses.
    """
    decl = JointDeclaration(
        name=name,
        members=frozenset(members),
        declared_by=declared_by,
        prereq={k: tuple(v) for k, v in prereq.items()},
        initial_states=frozenset(initial_states),
        authorized_initial=frozenset(authorized_initial),
        transitions=tuple(transitions),
        relation_digest="",
        exit_states=frozenset(exit_states),
    )
    return JointDeclaration(**{**decl.__dict__, "relation_digest": model_digest_of(decl)})


# ---------------------------------------------------------------------------
# Tarjan SCC (the verifier's own; the spec's naive checker is kept below as
# the defective baseline and is never used by verify_joint)
# ---------------------------------------------------------------------------

def tarjan_scc(graph: dict) -> list:
    """Tarjan's strongly-connected-components algorithm (iterative).

    ``graph``: {node: iterable of dependencies}. Returns a list of
    frozensets, each one SCC. Deterministic: roots and adjacency visited
    in sorted order.
    """
    index_of: dict = {}
    lowlink: dict = {}
    on_stack: set = set()
    stack: list = []
    result: list = []
    counter = 0

    # Every node that appears anywhere belongs to some SCC.
    all_nodes = set(graph)
    for deps in graph.values():
        all_nodes.update(deps)

    for root in sorted(all_nodes):
        if root in index_of:
            continue
        index_of[root] = lowlink[root] = counter
        counter += 1
        stack.append(root)
        on_stack.add(root)
        work = [(root, iter(sorted(graph.get(root, ()))))]
        while work:
            node, it = work[-1]
            descended = False
            for dep in it:
                if dep not in index_of:
                    index_of[dep] = lowlink[dep] = counter
                    counter += 1
                    stack.append(dep)
                    on_stack.add(dep)
                    work.append((dep, iter(sorted(graph.get(dep, ())))))
                    descended = True
                    break
                elif dep in on_stack:
                    if index_of[dep] < lowlink[node]:
                        lowlink[node] = index_of[dep]
            if descended:
                continue
            work.pop()
            if work:
                parent = work[-1][0]
                if lowlink[node] < lowlink[parent]:
                    lowlink[parent] = lowlink[node]
            if lowlink[node] == index_of[node]:
                scc = set()
                while True:
                    w = stack.pop()
                    on_stack.discard(w)
                    scc.add(w)
                    if w == node:
                        break
                result.append(frozenset(scc))
    return result


def condensation_order(graph: dict) -> list:
    """Topological order of the SCC condensation (Kahn, name-sorted).

    Between components, prerequisites first; within a component the
    members are solved simultaneously -- the order schedules proof work,
    it never ranks one member above another.
    """
    sccs = tarjan_scc(graph)
    comp_of = {n: i for i, s in enumerate(sccs) for n in s}
    # Edge dep_comp -> node_comp: the prerequisite's component comes first.
    succ: dict = {i: set() for i in range(len(sccs))}
    indeg = {i: 0 for i in range(len(sccs))}
    for node, deps in graph.items():
        for dep in deps:
            a, b = comp_of[dep], comp_of[node]
            if a != b and b not in succ[a]:
                succ[a].add(b)
                indeg[b] += 1
    key = {i: tuple(sorted(sccs[i])) for i in range(len(sccs))}
    ready = sorted([i for i, d in indeg.items() if d == 0], key=lambda i: key[i])
    order = []
    while ready:
        i = ready.pop(0)
        order.append(sccs[i])
        for b in sorted(succ[i], key=lambda j: key[j]):
            indeg[b] -= 1
            if indeg[b] == 0:
                ready.append(b)
        ready.sort(key=lambda j: key[j])
    if len(order) != len(sccs):
        raise ValueError("condensation is not a DAG -- Tarjan invariant violated")
    return order


# ---------------------------------------------------------------------------
# The verifier
# ---------------------------------------------------------------------------

def _issuer_of(authorization: str) -> str:
    """The issuer of an "issuer:reference" authorization (whole string if no ':')."""
    return authorization.split(":", 1)[0].strip()


def _successors(transitions: tuple) -> dict:
    succ: dict = {}
    for t in transitions:
        succ.setdefault(t.src, []).append(t)
    return succ


def _reachable(initial: frozenset, succ: dict) -> frozenset:
    seen = set(initial)
    frontier = list(initial)
    while frontier:
        s = frontier.pop()
        for t in succ.get(s, ()):
            if t.dst not in seen:
                seen.add(t.dst)
                frontier.append(t.dst)
    return frozenset(seen)


def _greatest_fixed_point(states: frozenset, succ: dict) -> frozenset:
    """States that can continue forever: the GFP of 'has a successor in the set'.

    Iterated elimination of dead ends. Convergence proves a property of
    the presented model: every surviving state lies on some infinite walk.
    """
    kernel = set(states)
    while True:
        doomed = {s for s in kernel
                  if not any(t.dst in kernel for t in succ.get(s, ()))}
        if not doomed:
            return frozenset(kernel)
        kernel -= doomed


def _max_mean_cycle(nodes: frozenset, succ: dict):
    """Karp's maximum-mean-weight cycle. Returns (mean, cycle) or (None, ()).

    Positive max mean <=> a positive-progress cycle exists in the subgraph.
    """
    nodes = list(nodes)
    n = len(nodes)
    if n == 0:
        return None, ()
    idx = {s: i for i, s in enumerate(nodes)}
    preds: dict = {s: [] for s in nodes}
    for s in nodes:
        for t in succ.get(s, ()):
            if t.dst in idx:
                preds[t.dst].append((s, t.progress))
    neg_inf = float("-inf")
    # F[k][v]: max weight of a walk of exactly k edges ending at v.
    F = [[neg_inf] * n for _ in range(n + 1)]
    back = [[-1] * n for _ in range(n + 1)]
    for i in range(n):
        F[0][i] = 0
    for k in range(1, n + 1):
        for v in nodes:
            j = idx[v]
            best, bj = neg_inf, -1
            for u, w in preds[v]:
                cand = F[k - 1][idx[u]] + w
                if cand > best:
                    best, bj = cand, idx[u]
            F[k][j] = best
            back[k][j] = bj
    best_mean = neg_inf
    best_v = -1
    for j in range(n):
        if F[n][j] == neg_inf:
            continue
        worst = float("inf")
        for k in range(n):
            if F[k][j] == neg_inf:
                continue
            val = (F[n][j] - F[k][j]) / (n - k)
            if val < worst:
                worst = val
        if worst > best_mean:
            best_mean, best_v = worst, j
    if best_v == -1 or best_mean == neg_inf:
        return None, ()
    # Trace back a length-n walk ending at best_v; it must repeat a node.
    walk = [nodes[best_v]]
    j = best_v
    for k in range(n, 0, -1):
        j = back[k][j]
        if j == -1:
            break
        walk.append(nodes[j])
    walk.reverse()
    seen_at: dict = {}
    cycle = ()
    for i, s in enumerate(walk):
        if s in seen_at:
            cycle = tuple(walk[seen_at[s]:i + 1])
            break
        seen_at[s] = i
    return best_mean, cycle


def _cycle_progress(cycle: tuple, succ: dict) -> int:
    total = 0
    for a, b in zip(cycle, cycle[1:]):
        for t in succ.get(a, ()):
            if t.dst == b:
                total += t.progress
                break
    return total


def _find_zero_progress_cycle(kernel: frozenset, succ: dict) -> tuple:
    """Exhibit a non-positive cycle as the livelock counterexample."""
    for start in sorted(kernel):
        # DFS for a cycle through `start`; first non-positive one wins.
        stack = [(start, [start], {start})]
        while stack:
            node, path, in_path = stack.pop()
            for t in succ.get(node, ()):
                if t.dst not in kernel:
                    continue
                if t.dst == start and len(path) > 1:
                    cyc = tuple(path + [start])
                    if _cycle_progress(cyc, succ) <= 0:
                        return cyc
                elif t.dst not in in_path:
                    stack.append((t.dst, path + [t.dst], in_path | {t.dst}))
    return ()


def _exit_path(kernel: frozenset, succ: dict, exits: frozenset) -> tuple:
    """Constructive exit path from the repeatable regime to a declared exit."""
    from collections import deque
    prev: dict = {}
    queue = deque(sorted(kernel))
    seen = set(queue)
    while queue:
        s = queue.popleft()
        if s in exits:
            path = [s]
            while path[-1] in prev:
                path.append(prev[path[-1]])
            return tuple(reversed(path))
        for t in succ.get(s, ()):
            if t.dst not in seen:
                seen.add(t.dst)
                prev[t.dst] = s
                queue.append(t.dst)
    return ()


def verify_joint(declaration: JointDeclaration) -> JointVerdict:
    """Verify a strongly-connected invariant group as one joint proof obligation.

    The verifier COMPUTES every property from the presented complete
    transition relation; it never accepts pre-computed booleans. Grounding
    failures refuse with the minimal joint obstruction.
    """
    members = declaration.members
    obstruction: list = []
    notes: list = []

    def refused(why: list, extra_notes=()) -> JointVerdict:
        return JointVerdict(
            verdict=Verdict.JOINT_UNDETERMINED,
            group=declaration.name,
            model_digest=model_digest_of(declaration),
            obstruction=tuple(sorted(set(why))),
            notes=tuple(extra_notes),
        )

    # -- 1. Membership: exactly one genuine cycle -------------------------
    if not members:
        return refused(["empty membership: a joint group needs at least one member"])
    sccs = tarjan_scc({k: tuple(v) for k, v in declaration.prereq.items()})
    hit = [s for s in sccs if s == members]
    if not hit:
        covering = sorted({n for s in sccs for n in s if n in members})
        return refused([
            "members are not one strongly connected component "
            f"(members={sorted(members)}, scc-cover={covering})"
        ])
    scc = hit[0]
    prereq = {k: tuple(v) for k, v in declaration.prereq.items()}
    is_cycle = len(scc) > 1 or any(m in prereq.get(m, ()) for m in scc)
    if not is_cycle:
        return refused([
            f"singleton {sorted(scc)[0]} has no self-dependency: no cycle to solve jointly"
        ])

    # -- 2. Grounding: external facts only --------------------------------
    if declaration.declared_by in members:
        obstruction.append(
            f"authority {declaration.declared_by!r} is a member: "
            "the group would establish its own external facts"
        )
    if model_digest_of(declaration) != declaration.relation_digest:
        obstruction.append(
            "relation digest mismatch: the presented model is not the authorized one"
        )
    if not declaration.initial_states:
        obstruction.append("no initial state presented")
    unauthorized = sorted(set(declaration.initial_states) - set(declaration.authorized_initial))
    if unauthorized:
        obstruction.append(
                    "initial state(s) lack authorization: " + ", ".join(unauthorized)
        )
    if not declaration.authorized_initial:
        obstruction.append("no authorized initial allocation: the joint cycle cannot start")
    succ = _successors(declaration.transitions)
    for e in sorted(declaration.exit_states):
        if succ.get(e):
            obstruction.append(
                f"declared exit {e!r} is not terminal: terminal implies no new cycle"
            )
    if obstruction:
        return refused(obstruction)

    # -- 3. Reachability ---------------------------------------------------
    reachable = _reachable(declaration.initial_states, succ)
    if not reachable:
        return refused(["no reachable joint state from the authorized entry"],
                       extra_notes=("reachability",
                                    "the authorized initial state admits no joint state",))

    # -- 4. Safety closure: cross-relationships on every reachable step ---
    violations: list = []
    for s in sorted(reachable):
        for t in succ.get(s, ()):
            if t.kind == KIND_REPLENISH:
                # Replenishment implies lawful authorization.
                if not t.authorization:
                    violations.append(
                        f"replenish {t.src}->{t.dst} without authorization")
                elif _issuer_of(t.authorization) in members or not _issuer_of(t.authorization):
                    violations.append(
                        f"replenish {t.src}->{t.dst} authorized by {t.authorization!r}: "
                        "issuer must be external to the group")
            elif t.kind == KIND_RESERVE:
                # Reservation implies capacity and ownership.
                if not t.capacity or not t.owner:
                    violations.append(
                        f"reserve {t.src}->{t.dst} without capacity and ownership "
                        f"(capacity={t.capacity!r}, owner={t.owner!r})")
            if t.kind not in KINDS:
                violations.append(f"{t.src}->{t.dst}: unknown kind {t.kind!r}")
    if violations:
        return JointVerdict(
            verdict=Verdict.JOINT_UNDETERMINED,
            group=declaration.name,
            model_digest=model_digest_of(declaration),
            obstruction=("safety closure violated",),
            reachable=reachable,
            safety_violations=tuple(sorted(set(violations))),
            notes=("the joint invariant does not hold on every reachable step",),
        )

    # -- 5. Deadlock in scope ---------------------------------------------
    exits = set(declaration.exit_states)
    for s in sorted(reachable):
        if not succ.get(s) and s not in exits:
            return JointVerdict(
                verdict=Verdict.DEADLOCK_IN_SCOPE,
                group=declaration.name,
                model_digest=model_digest_of(declaration),
                reachable=reachable,
                deadlock_state=s,
                notes=(f"{s} is reachable, has no legal transition, "
                       "and is not a declared exit",),
            )

    # -- 6. Repeatability: greatest fixed point -----------------------------
    kernel = _greatest_fixed_point(reachable, succ) & reachable
    if not kernel:
        return JointVerdict(
            verdict=Verdict.JOINT_UNDETERMINED,
            group=declaration.name,
            model_digest=model_digest_of(declaration),
            obstruction=("no repeatable kernel: every fair execution from the "
                         "authorized entry terminates; the declared joint "
                         "cycle does not repeat",),
            reachable=reachable,
            notes=("a cycle that always terminates is not a repeatable cycle",),
        )

    # -- 7. Progress: a repeatable-looking cycle is not proof ---------------
    mean, cycle = _max_mean_cycle(kernel, succ)
    if mean is None or mean <= 0:
        counter = _find_zero_progress_cycle(kernel, succ) or cycle
        prog = _cycle_progress(counter, succ) if counter else 0
        return JointVerdict(
            verdict=Verdict.LIVELOCK_COUNTEREXAMPLE,
            group=declaration.name,
            model_digest=model_digest_of(declaration),
            reachable=reachable,
            kernel=kernel,
            exhibited_cycle=counter,
            cycle_progress=prog,
            notes=("the joint system can spin forever without advancing: "
                   "repeatability of motion is not repeatability of progress",),
        )
    progress = _cycle_progress(cycle, succ)

    # -- 8. Exit viability: constructive, and never guaranteed --------------
    path = _exit_path(kernel, succ, exits)
    if path:
        return JointVerdict(
            verdict=Verdict.EXIT_POSSIBLE_NOT_GUARANTEED,
            group=declaration.name,
            model_digest=model_digest_of(declaration),
            reachable=reachable,
            kernel=kernel,
            exhibited_cycle=cycle,
            cycle_progress=progress,
            exit_path=path,
            notes=("the strategy is proven and an exit is constructed, but the "
                   "kernel can continue forever: an escape path existing is "
                   "not the same as every fair execution escaping",),
        )
    return JointVerdict(
        verdict=Verdict.REPEATABLE_PROVEN,
        group=declaration.name,
        model_digest=model_digest_of(declaration),
        reachable=reachable,
        kernel=kernel,
        exhibited_cycle=cycle,
        cycle_progress=progress,
        notes=("no exit from the repeatable regime: the joint cycle is closed",),
    )


# ---------------------------------------------------------------------------
# NAIVE BASELINE (defective) -- Naya 5's spec machinery from PR #2209, kept
# verbatim so the test-suite proves it wrong. NEVER used by verify_joint.
# ---------------------------------------------------------------------------

class _NaiveSCCVerdict(Enum):
    REPEATABLE_CYCLE_PROVEN = "REPEATABLE_CYCLE_PROVEN"
    DEADLOCK_PROVEN_IN_SCOPE = "DEADLOCK_PROVEN_IN_SCOPE"
    LIVELOCK_COUNTEREXAMPLE = "LIVELOCK_COUNTEREXAMPLE"
    EXIT_POSSIBLE_NOT_GUARANTEED = "EXIT_POSSIBLE_NOT_GUARANTEED"
    JOINT_PROOF_UNDETERMINED = "JOINT_PROOF_UNDETERMINED"


@dataclass(frozen=True)
class _NaiveSCCGroup:
    """A strongly connected component of invariants."""
    members: tuple  # invariant names
    # Authoritative grounding (must come from outside the SCC)
    initial_state_authorized: bool
    transitions_valid: bool
    replenishment_lawful: bool
    resource_conserved: bool
    lifecycle_valid: bool


@dataclass(frozen=True)
class _NaiveJointProof:
    reachability: bool
    safety_closure: bool
    repeatability: bool
    exit_viability: bool


def naive_verify_scc(group: _NaiveSCCGroup, proof: _NaiveJointProof) -> _NaiveSCCVerdict:
    """Verify a jointly-qualified SCC per AER-LIVE-10.

    No member may certify another -- the group must be grounded in
    external authoritative state.
    """
    # Grounding check: all external facts must hold
    grounded = all([
        group.initial_state_authorized,
        group.transitions_valid,
        group.replenishment_lawful,
        group.resource_conserved,
        group.lifecycle_valid,
    ])
    if not grounded:
        return _NaiveSCCVerdict.JOINT_PROOF_UNDETERMINED

    # Four properties
    if not proof.reachability:
        return _NaiveSCCVerdict.JOINT_PROOF_UNDETERMINED
    if not proof.safety_closure:
        return _NaiveSCCVerdict.DEADLOCK_PROVEN_IN_SCOPE
    if proof.repeatability and proof.exit_viability:
        return _NaiveSCCVerdict.REPEATABLE_CYCLE_PROVEN
    if proof.exit_viability:
        return _NaiveSCCVerdict.EXIT_POSSIBLE_NOT_GUARANTEED
    return _NaiveSCCVerdict.LIVELOCK_COUNTEREXAMPLE
