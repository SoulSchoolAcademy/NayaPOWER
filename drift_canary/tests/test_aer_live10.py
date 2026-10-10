"""AER-LIVE-10 tests: SCC Joint Proof Qualification."""
import sys
sys.path.insert(0, "drift_canary")

from aer_live10_scc import (
    SCCVerdict,
    scc01_impossible_bootstrap,
    scc02_valid_seeded_exchange,
    tarjan_scc,
)


def test_tarjan_finds_cycle():
    # budget -> resource -> budget (cycle)
    graph = {
        "budget": ["resource"],
        "resource": ["budget"],
        "lifecycle": [],
    }
    sccs = tarjan_scc(graph)
    # One SCC with budget+resource, one singleton lifecycle
    sizes = sorted(len(s) for s in sccs)
    assert sizes == [1, 2]


def test_tarjan_dag_singletons():
    graph = {"a": ["b"], "b": ["c"], "c": []}
    sccs = tarjan_scc(graph)
    assert all(len(s) == 1 for s in sccs)


def test_scc01_rejects_impossible_bootstrap():
    """SCC-01: no authorized seed → NOT repeatable."""
    r = scc01_impossible_bootstrap()
    assert r != SCCVerdict.REPEATABLE_CYCLE_PROVEN


def test_scc02_accepts_valid_seed():
    """SCC-02: authorized seed → repeatable."""
    assert scc02_valid_seeded_exchange() == SCCVerdict.REPEATABLE_CYCLE_PROVEN


def test_decisive_pair_differs():
    """Same topology, different verdicts → checks transitions not topology."""
    assert scc01_impossible_bootstrap() != scc02_valid_seeded_exchange()


def test_canonical_diagram_scc():
    """Shawn's canonical 4-node SCC from the AER-LIVE-10 diagram.

    LIFECYCLE (Operation outstanding) ↔ RESOURCE (Capacity available)
    ↔ REPLENISHMENT (Credits restored) ↔ BUDGET (Credits available)
    form one strongly connected proof group. OBSERVATION + LAW feeds
    in from outside; JOINT PROOF (repeatability/termination/escape)
    comes out below. Tarjan must find all four as ONE SCC.
    """
    # Dependency edges from the canonical diagram
    graph = {
        "lifecycle": ["resource", "replenishment", "budget"],
        "resource": ["lifecycle", "replenishment"],
        "replenishment": ["budget"],
        "budget": ["resource"],
    }
    sccs = tarjan_scc(graph)
    assert len(sccs) == 1
    assert set(sccs[0]) == {"lifecycle", "resource", "replenishment", "budget"}
