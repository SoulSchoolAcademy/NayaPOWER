"""AER-LIVE-10: Strongly Connected Invariant Groups (spec).

Shawn's law (SN-0816, ratified 2026-10-10): When invariants depend on
one another cyclically, no member may serve as independent proof of
another. Collapse into SCCs (Tarjan). Each SCC is one joint proof
obligation. Ground in authoritative initial state, valid transitions,
lawful replenishment, resource conservation, lifecycle constraints.

Four separate properties per SCC:
1. Reachability: nonempty reachable joint invariant exists
2. Safety closure: legal transitions preserve the joint invariant
3. Repeatability: verified strategy with positive debt gain
4. Exit viability: constructive valid exit path

Five verdicts: REPEATABLE / DEADLOCK / LIVELOCK / EXIT_POSSIBLE /
UNDETERMINED.

Decisive SCC-01 vs SCC-02: same circular graph, different initial
state. Verifier must reject impossible bootstrap, accept valid seeded
exchange — proving it checks transitions, not topology.

SPEC ONLY. Not wired into kernel/, KNOW, LAW, ACT, or any live path.
"""

from dataclasses import dataclass
from enum import Enum


class SCCVerdict(Enum):
    REPEATABLE_CYCLE_PROVEN = "REPEATABLE_CYCLE_PROVEN"
    DEADLOCK_PROVEN_IN_SCOPE = "DEADLOCK_PROVEN_IN_SCOPE"
    LIVELOCK_COUNTEREXAMPLE = "LIVELOCK_COUNTEREXAMPLE"
    EXIT_POSSIBLE_NOT_GUARANTEED = "EXIT_POSSIBLE_NOT_GUARANTEED"
    JOINT_PROOF_UNDETERMINED = "JOINT_PROOF_UNDETERMINED"


@dataclass(frozen=True)
class SCCGroup:
    """A strongly connected component of invariants."""
    members: tuple  # invariant names
    # Authoritative grounding (must come from outside the SCC)
    initial_state_authorized: bool
    transitions_valid: bool
    replenishment_lawful: bool
    resource_conserved: bool
    lifecycle_valid: bool


@dataclass(frozen=True)
class JointProof:
    reachability: bool
    safety_closure: bool
    repeatability: bool
    exit_viability: bool


def tarjan_scc(graph: dict) -> list:
    """Tarjan's SCC algorithm (spec version).

    graph: {node: [dependencies]}
    Returns list of SCCs (each a frozenset of nodes).
    """
    index_counter = [0]
    stack = []
    lowlink = {}
    index = {}
    on_stack = set()
    result = []

    def strongconnect(node):
        index[node] = index_counter[0]
        lowlink[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)
        on_stack.add(node)

        for dep in graph.get(node, []):
            if dep not in index:
                strongconnect(dep)
                lowlink[node] = min(lowlink[node], lowlink[dep])
            elif dep in on_stack:
                lowlink[node] = min(lowlink[node], index[dep])

        if lowlink[node] == index[node]:
            scc = set()
            while True:
                w = stack.pop()
                on_stack.discard(w)
                scc.add(w)
                if w == node:
                    break
            result.append(frozenset(scc))

    for node in graph:
        if node not in index:
            strongconnect(node)
    return result


def verify_scc(group: SCCGroup, proof: JointProof) -> SCCVerdict:
    """Verify a jointly-qualified SCC per AER-LIVE-10.

    No member may certify another — the group must be grounded in
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
        return SCCVerdict.JOINT_PROOF_UNDETERMINED

    # Four properties
    if not proof.reachability:
        return SCCVerdict.JOINT_PROOF_UNDETERMINED
    if not proof.safety_closure:
        return SCCVerdict.DEADLOCK_PROVEN_IN_SCOPE
    if proof.repeatability and proof.exit_viability:
        return SCCVerdict.REPEATABLE_CYCLE_PROVEN
    if proof.exit_viability:
        return SCCVerdict.EXIT_POSSIBLE_NOT_GUARANTEED
    return SCCVerdict.LIVELOCK_COUNTEREXAMPLE


# SCC-01 vs SCC-02 decisive pair
def scc01_impossible_bootstrap() -> SCCVerdict:
    """SCC-01: circular deps, NO authorized initial state → reject."""
    group = SCCGroup(
        members=("budget", "resource", "replenishment", "lifecycle"),
        initial_state_authorized=False,  # no seed!
        transitions_valid=True,
        replenishment_lawful=True,
        resource_conserved=True,
        lifecycle_valid=True,
    )
    proof = JointProof(True, True, True, True)
    result = verify_scc(group, proof)
    # Must NOT be repeatable — no authorized starting point
    assert result != SCCVerdict.REPEATABLE_CYCLE_PROVEN
    return result


def scc02_valid_seeded_exchange() -> SCCVerdict:
    """SCC-02: same graph, WITH authorized initial state → accept."""
    group = SCCGroup(
        members=("budget", "resource", "replenishment", "lifecycle"),
        initial_state_authorized=True,  # seeded!
        transitions_valid=True,
        replenishment_lawful=True,
        resource_conserved=True,
        lifecycle_valid=True,
    )
    proof = JointProof(True, True, True, True)
    result = verify_scc(group, proof)
    assert result == SCCVerdict.REPEATABLE_CYCLE_PROVEN
    return result
